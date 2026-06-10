from __future__ import annotations

import re
import sqlite3
from pathlib import Path

import pytest

from app.auth.service import (
    ConflictError,
    NotFoundError,
    NotVerifiedError,
    UnauthorizedError,
    ValidationError,
    authenticate_user,
    create_password_reset_request,
    create_session,
    get_user_by_session_token,
    register_user,
    resend_verification_request,
    reset_password,
    revoke_session,
    verify_email,
)
from app.core.config import Settings, database_path_from_settings
from app.shared.db import get_database_path
from app.shared.security import validate_new_password


def _db_path(settings: Settings):
    return get_database_path(settings)


def _connect(settings: Settings):
    return sqlite3.connect(str(_db_path(settings)))


def _fetch_one(settings: Settings, sql: str, params: tuple = ()):
    with _connect(settings) as conn:
        conn.row_factory = sqlite3.Row
        return conn.execute(sql, params).fetchone()


def _extract_token_from_link(body_text: str) -> str:
    match = re.search(r"/(?:verify-email|reset-password)/([A-Za-z0-9_-]+)", body_text)
    assert match, "token link not found"
    return match.group(1)


def _make_test_user(settings: Settings):
    return register_user(
        email="user@example.com",
        login="testuser",
        password="Secret123",
        repeat_password="Secret123",
        settings=settings,
    )


def test_default_database_path_points_into_state():
    default_settings = Settings()
    path = database_path_from_settings(default_settings)
    assert str(path).startswith("/opt/ai-starter-community/state/")
    assert str(path).endswith("ai_starter_community.sqlite3")


def test_register_creates_unverified_user_and_outbox(test_settings):
    user = register_user(
        email="User@Example.com",
        login="TestUser",
        password="Secret123",
        repeat_password="Secret123",
        settings=test_settings,
    )

    assert user.email == "user@example.com"
    assert user.login == "testuser"
    assert user.email_verified_at is None
    assert user.access_status == "not_activated"

    user_row = _fetch_one(test_settings, "SELECT * FROM users WHERE email = ?", ("user@example.com",))
    assert user_row["password_hash"] != "Secret123"
    assert user_row["password_hash"].startswith("$2")
    assert user_row["email_verified_at"] is None
    assert user_row["access_status"] == "not_activated"

    token_row = _fetch_one(
        test_settings,
        "SELECT * FROM auth_tokens WHERE user_id = ? AND token_type = ?",
        (user_row["id"], "email_verification"),
    )
    assert token_row is not None
    assert token_row["used_at"] is None

    outbox_row = _fetch_one(
        test_settings,
        "SELECT * FROM email_outbox WHERE recipient_email = ? ORDER BY id DESC LIMIT 1",
        ("user@example.com",),
    )
    assert outbox_row is not None
    assert outbox_row["template_key"] == "email_verification"
    assert "/verify-email/" in outbox_row["body_text"]


def test_resend_verification_request_creates_new_outbox_message(test_settings):
    user = _make_test_user(test_settings)
    before_count = _fetch_one(
        test_settings,
        "SELECT COUNT(*) AS c FROM email_outbox WHERE recipient_email = ? AND template_key = ?",
        (user.email, "email_verification"),
    )["c"]

    assert resend_verification_request("user@example.com", settings=test_settings) is True

    after_count = _fetch_one(
        test_settings,
        "SELECT COUNT(*) AS c FROM email_outbox WHERE recipient_email = ? AND template_key = ?",
        (user.email, "email_verification"),
    )["c"]
    assert after_count == before_count + 1


def test_resend_verification_request_is_generic_for_missing_or_verified_user(test_settings):
    assert resend_verification_request("missing@example.com", settings=test_settings) is False

    user = _make_test_user(test_settings)
    verification_row = _fetch_one(
        test_settings,
        "SELECT * FROM email_outbox WHERE recipient_email = ? AND template_key = ? ORDER BY id DESC LIMIT 1",
        (user.email, "email_verification"),
    )
    verify_token = _extract_token_from_link(verification_row["body_text"])
    verify_email(verify_token, settings=test_settings)
    assert resend_verification_request("user@example.com", settings=test_settings) is False


def test_register_rejects_duplicates_and_password_rules(test_settings):
    _make_test_user(test_settings)

    with pytest.raises(ConflictError):
        register_user(
            email="user@example.com",
            login="anotherlogin",
            password="Secret123",
            repeat_password="Secret123",
            settings=test_settings,
        )

    with pytest.raises(ConflictError):
        register_user(
            email="other@example.com",
            login="testuser",
            password="Secret123",
            repeat_password="Secret123",
            settings=test_settings,
        )

    with pytest.raises(ValidationError, match="password must not contain spaces"):
        register_user(
            email="other2@example.com",
            login="otherlogin",
            password=" Secret 123 ",
            repeat_password=" Secret 123 ",
            settings=test_settings,
        )

    with pytest.raises(ValidationError, match="passwords do not match"):
        register_user(
            email="other3@example.com",
            login="otherlogin2",
            password="Secret123",
            repeat_password="Secret124",
            settings=test_settings,
        )


def test_password_policy_trims_and_rejects_spaces():
    assert validate_new_password("  Secret123  ") == "Secret123"
    with pytest.raises(ValueError, match="password must not contain spaces"):
        validate_new_password("Se cret123")
    with pytest.raises(ValueError, match="password is required"):
        validate_new_password("   ")


def test_email_verification_and_login_by_email_or_login(test_settings):
    user = _make_test_user(test_settings)
    outbox_row = _fetch_one(
        test_settings,
        "SELECT * FROM email_outbox WHERE recipient_email = ? ORDER BY id DESC LIMIT 1",
        (user.email,),
    )
    token = _extract_token_from_link(outbox_row["body_text"])

    verified_user = verify_email(token, settings=test_settings)
    assert verified_user.email_verified_at is not None

    user_by_email = authenticate_user("user@example.com", "Secret123", settings=test_settings)
    user_by_login = authenticate_user("testuser", "Secret123", settings=test_settings)
    assert user_by_email.id == verified_user.id
    assert user_by_login.id == verified_user.id

    with pytest.raises(UnauthorizedError):
        authenticate_user("user@example.com", "wrongpassword", settings=test_settings)


def test_login_requires_verification_before_success(test_settings):
    register_user(
        email="nov@example.com",
        login="novuser",
        password="Secret123",
        repeat_password="Secret123",
        settings=test_settings,
    )
    with pytest.raises(NotVerifiedError):
        authenticate_user("nov@example.com", "Secret123", settings=test_settings)


def test_password_reset_flow_revokes_sessions(test_settings):
    user = _make_test_user(test_settings)
    verification_row = _fetch_one(
        test_settings,
        "SELECT * FROM email_outbox WHERE recipient_email = ? ORDER BY id DESC LIMIT 1",
        (user.email,),
    )
    verify_token = _extract_token_from_link(verification_row["body_text"])
    verify_email(verify_token, settings=test_settings)

    session_token = create_session(user.id, settings=test_settings)
    assert get_user_by_session_token(session_token, settings=test_settings) is not None

    assert create_password_reset_request("user@example.com", settings=test_settings) is True
    reset_row = _fetch_one(
        test_settings,
        "SELECT * FROM email_outbox WHERE recipient_email = ? AND template_key = ? ORDER BY id DESC LIMIT 1",
        (user.email, "password_reset"),
    )
    reset_token = _extract_token_from_link(reset_row["body_text"])

    reset_user = reset_password(
        token=reset_token,
        new_password="NewSecret123",
        repeat_password="NewSecret123",
        settings=test_settings,
    )
    assert reset_user.id == user.id
    assert get_user_by_session_token(session_token, settings=test_settings) is None
    assert authenticate_user("user@example.com", "NewSecret123", settings=test_settings).id == user.id


def test_forgot_password_generic_behavior_and_reused_token_fail(test_settings):
    user = _make_test_user(test_settings)
    verify_row = _fetch_one(
        test_settings,
        "SELECT * FROM email_outbox WHERE recipient_email = ? ORDER BY id DESC LIMIT 1",
        (user.email,),
    )
    verify_token = _extract_token_from_link(verify_row["body_text"])
    verify_email(verify_token, settings=test_settings)

    assert create_password_reset_request("missing@example.com", settings=test_settings) is False
    assert _fetch_one(
        test_settings,
        "SELECT * FROM email_outbox WHERE recipient_email = ? AND template_key = ? ORDER BY id DESC LIMIT 1",
        ("missing@example.com", "password_reset"),
    ) is None

    assert create_password_reset_request("user@example.com", settings=test_settings) is True
    reset_row = _fetch_one(
        test_settings,
        "SELECT * FROM email_outbox WHERE recipient_email = ? AND template_key = ? ORDER BY id DESC LIMIT 1",
        (user.email, "password_reset"),
    )
    reset_token = _extract_token_from_link(reset_row["body_text"])
    reset_password(
        token=reset_token,
        new_password="AnotherSecret123",
        repeat_password="AnotherSecret123",
        settings=test_settings,
    )

    with pytest.raises(NotFoundError):
        reset_password(
            token=reset_token,
            new_password="AnotherSecret123",
            repeat_password="AnotherSecret123",
            settings=test_settings,
        )


def test_route_flow_register_page_is_closed(client, test_settings):
    db_path = Path(test_settings.database_path)
    assert not db_path.exists()

    register_response = client.get("/register")
    assert register_response.status_code == 200
    assert "Регистрация временно закрыта" in register_response.text
    assert "Перейти ко входу" in register_response.text
    assert "/login" in register_response.text
    assert "Создать аккаунт" not in register_response.text

    register_post_response = client.post(
        "/register",
        data={
            "email": "route@example.com",
            "login": "routeuser",
            "password": "Secret123",
            "repeat_password": "Secret123",
        },
        follow_redirects=False,
    )
    assert register_post_response.status_code == 403
    assert "Регистрация временно закрыта" in register_post_response.text
    assert "/login" in register_post_response.text

    assert not db_path.exists()


def test_route_flow_login_cabinet_logout_still_works(client, test_settings):
    register_user(
        email="route@example.com",
        login="routeuser",
        password="Secret123",
        repeat_password="Secret123",
        settings=test_settings,
    )
    outbox_row = _fetch_one(
        test_settings,
        "SELECT * FROM email_outbox WHERE recipient_email = ? AND template_key = ? ORDER BY id DESC LIMIT 1",
        ("route@example.com", "email_verification"),
    )
    verify_token = _extract_token_from_link(outbox_row["body_text"])
    verify_response = client.get(f"/verify-email/{verify_token}")
    assert verify_response.status_code == 200
    assert "Почта подтверждена" in verify_response.text

    login_email_response = client.post(
        "/login",
        data={"email_or_login": "route@example.com", "password": "Secret123"},
        follow_redirects=False,
    )
    assert login_email_response.status_code == 303
    assert "location" in login_email_response.headers
    assert test_settings.session_cookie_name in login_email_response.headers.get("set-cookie", "")

    cabinet_response = client.get("/cabinet")
    assert cabinet_response.status_code == 200
    assert "route@example.com" in cabinet_response.text
    assert "routeuser" in cabinet_response.text
    assert "Личный кабинет будет доступен после оплаты" in cabinet_response.text
    assert "После оплаты тарифа откроются личный кабинет, обучение и материалы." in cabinet_response.text
    assert "Аккаунты" not in cabinet_response.text
    assert "/static/cabinet-local-accounts.js" not in cabinet_response.text
    assert "Главная" in cabinet_response.text
    assert "Обучающий блок" not in cabinet_response.text
    assert "Обучающий проект" not in cabinet_response.text
    assert "Перейти к обучению" not in cabinet_response.text
    assert "Скачать файл" not in cabinet_response.text
    assert 'href="/materials/drafts/dair-smoke-20260529/"' not in cabinet_response.text
    assert 'href="/cabinet/learning/project-file"' not in cabinet_response.text
    assert "Выйти" in cabinet_response.text

    logout_response = client.post("/logout", follow_redirects=False)
    assert logout_response.status_code == 303
    assert test_settings.session_cookie_name in logout_response.headers.get("set-cookie", "")

    cabinet_after_logout = client.get("/cabinet", follow_redirects=False)
    assert cabinet_after_logout.status_code == 303
    assert cabinet_after_logout.headers["location"] == "/login"


def test_cabinet_settings_page_and_password_change_flow(client, test_settings):
    user = register_user(
        email="settings@example.com",
        login="settingsuser",
        password="Secret123",
        repeat_password="Secret123",
        settings=test_settings,
    )
    verification_row = _fetch_one(
        test_settings,
        "SELECT * FROM email_outbox WHERE recipient_email = ? AND template_key = ? ORDER BY id DESC LIMIT 1",
        (user.email, "email_verification"),
    )
    verify_token = _extract_token_from_link(verification_row["body_text"])
    verify_email(verify_token, settings=test_settings)

    anon_settings_page = client.get("/cabinet/settings", follow_redirects=False)
    assert anon_settings_page.status_code == 303
    assert anon_settings_page.headers["location"] == "/login"

    anon_submit = client.post(
        "/cabinet/settings/password",
        data={
            "current_password": "Secret123",
            "password": "NewSecret123",
            "repeat_password": "NewSecret123",
        },
        follow_redirects=False,
    )
    assert anon_submit.status_code == 303
    assert anon_submit.headers["location"] == "/login"

    login_response = client.post(
        "/login",
        data={"email_or_login": "settings@example.com", "password": "Secret123"},
        follow_redirects=False,
    )
    assert login_response.status_code == 303

    settings_page = client.get("/cabinet/settings")
    assert settings_page.status_code == 200
    assert "Настройки" in settings_page.text
    assert "Смена пароля" in settings_page.text
    assert 'name="current_password"' in settings_page.text
    assert 'name="password"' in settings_page.text
    assert 'name="repeat_password"' in settings_page.text
    assert '/cabinet/settings/password' in settings_page.text
    assert 'href="/cabinet"' in settings_page.text

    row_before = _fetch_one(
        test_settings,
        "SELECT password_hash FROM users WHERE email = ?",
        (user.email,),
    )
    assert row_before is not None
    password_hash_before = row_before["password_hash"]

    wrong_current_response = client.post(
        "/cabinet/settings/password",
        data={
            "current_password": "WrongSecret123",
            "password": "NewSecret123",
            "repeat_password": "NewSecret123",
        },
    )
    assert wrong_current_response.status_code == 200
    assert "Текущий пароль неверный." in wrong_current_response.text
    assert _fetch_one(
        test_settings,
        "SELECT password_hash FROM users WHERE email = ?",
        (user.email,),
    )["password_hash"] == password_hash_before

    mismatch_response = client.post(
        "/cabinet/settings/password",
        data={
            "current_password": "Secret123",
            "password": "NewSecret123",
            "repeat_password": "NewSecret124",
        },
    )
    assert mismatch_response.status_code == 200
    assert "Новые пароли не совпадают." in mismatch_response.text
    assert _fetch_one(
        test_settings,
        "SELECT password_hash FROM users WHERE email = ?",
        (user.email,),
    )["password_hash"] == password_hash_before

    success_response = client.post(
        "/cabinet/settings/password",
        data={
            "current_password": "Secret123",
            "password": "NewSecret123",
            "repeat_password": "NewSecret123",
        },
        follow_redirects=False,
    )
    assert success_response.status_code == 303
    assert success_response.headers["location"] == "/cabinet/settings?success=1"

    success_page = client.get("/cabinet/settings?success=1")
    assert success_page.status_code == 200
    assert "Пароль изменён." in success_page.text

    with pytest.raises(UnauthorizedError):
        authenticate_user("settings@example.com", "Secret123", settings=test_settings)
    assert authenticate_user("settings@example.com", "NewSecret123", settings=test_settings).id == user.id
    assert _fetch_one(
        test_settings,
        "SELECT password_hash FROM users WHERE email = ?",
        (user.email,),
    )["password_hash"] != password_hash_before


def test_route_flow_login_by_login_and_password_reset(client, test_settings):
    register_user(
        email="loginroute@example.com",
        login="loginroute",
        password="Secret123",
        repeat_password="Secret123",
        settings=test_settings,
    )

    verify_row = _fetch_one(
        test_settings,
        "SELECT * FROM email_outbox WHERE recipient_email = ? AND template_key = ? ORDER BY id DESC LIMIT 1",
        ("loginroute@example.com", "email_verification"),
    )
    verify_token = _extract_token_from_link(verify_row["body_text"])
    verify_response = client.get(f"/verify-email/{verify_token}")
    assert verify_response.status_code == 200

    login_response = client.post(
        "/login",
        data={"email_or_login": "loginroute", "password": "Secret123"},
        follow_redirects=False,
    )
    assert login_response.status_code == 303
    assert test_settings.session_cookie_name in login_response.headers.get("set-cookie", "")

    forgot_response = client.post("/forgot-password", data={"email": "loginroute@example.com"})
    assert forgot_response.status_code == 200
    assert "Если такой адрес электронной почты зарегистрирован" in forgot_response.text
    assert forgot_response.text.count("Если такой адрес электронной почты зарегистрирован") == 1
    assert forgot_response.text.count("Укажите адрес электронной почты, чтобы мы смогли найти ваш аккаунт.") == 1
    assert "Подтвердить почту" not in forgot_response.text
    assert "Вернуться ко входу" in forgot_response.text

    reset_row = _fetch_one(
        test_settings,
        "SELECT * FROM email_outbox WHERE recipient_email = ? AND template_key = ? ORDER BY id DESC LIMIT 1",
        ("loginroute@example.com", "password_reset"),
    )
    reset_token = _extract_token_from_link(reset_row["body_text"])
    reset_response = client.post(
        "/reset-password",
        data={
            "token": reset_token,
            "password": "NewSecret123",
            "repeat_password": "NewSecret123",
        },
    )
    assert reset_response.status_code == 200
    assert "Теперь можно войти в систему" in reset_response.text
    assert "Вернуться ко входу" in reset_response.text or "Войти" in reset_response.text

    relogin_response = client.post(
        "/login",
        data={"email_or_login": "loginroute", "password": "NewSecret123"},
        follow_redirects=False,
    )
    assert relogin_response.status_code == 303
    cabinet_response = client.get("/cabinet")
    assert cabinet_response.status_code == 200
    assert "loginroute@example.com" in cabinet_response.text


def test_settings_page_layout_and_password_change(client, test_settings):
    register_user(
        email="settingsflow@example.com",
        login="settingsflow",
        password="Secret123",
        repeat_password="Secret123",
        settings=test_settings,
    )
    verify_row = _fetch_one(
        test_settings,
        "SELECT * FROM email_outbox WHERE recipient_email = ? AND template_key = ? ORDER BY id DESC LIMIT 1",
        ("settingsflow@example.com", "email_verification"),
    )
    verify_token = _extract_token_from_link(verify_row["body_text"])
    verify_response = client.get(f"/verify-email/{verify_token}")
    assert verify_response.status_code == 200

    login_response = client.post(
        "/login",
        data={"email_or_login": "settingsflow@example.com", "password": "Secret123"},
        follow_redirects=False,
    )
    assert login_response.status_code == 303

    settings_response = client.get("/cabinet/settings")
    assert settings_response.status_code == 200
    assert "settings-shell" in settings_response.text
    assert "settings-card" in settings_response.text
    assert "settings-meta" in settings_response.text
    assert "settings-form" in settings_response.text
    assert "Управляйте паролем и данными учётной записи без лишнего визуального шума." in settings_response.text
    assert "Аккаунт" in settings_response.text
    assert "Email" in settings_response.text
    assert "Смена пароля" in settings_response.text
    assert "Текущий пароль" in settings_response.text
    assert "Новый пароль" in settings_response.text
    assert "Повтор нового пароля" in settings_response.text

    password_response = client.post(
        "/cabinet/settings/password",
        data={
            "current_password": "Secret123",
            "password": "Secret456",
            "repeat_password": "Secret456",
        },
        follow_redirects=False,
    )
    assert password_response.status_code == 303
    assert password_response.headers["location"] == "/cabinet/settings?success=1"
    assert authenticate_user("settingsflow@example.com", "Secret456", settings=test_settings).email == "settingsflow@example.com"


def test_unverified_login_shows_resend_link(client, test_settings):
    register_user(
        email="needsverify@example.com",
        login="needsverify",
        password="Secret123",
        repeat_password="Secret123",
        settings=test_settings,
    )

    login_response = client.post(
        "/login",
        data={"email_or_login": "needsverify@example.com", "password": "Secret123"},
    )
    assert login_response.status_code == 200
    assert "Email не подтверждён." in login_response.text
    assert "Не пришло письмо подтверждения?" in login_response.text
    assert "/resend-verification" in login_response.text
    assert "Подтверждение почты" not in client.get("/login").text


def test_login_and_reset_pages_show_clear_rules(client):
    login_response = client.get("/login")
    forgot_response = client.get("/forgot-password")
    reset_response = client.get("/reset-password/example-token")

    assert "Электронная почта или логин" in login_response.text
    assert "Зарегистрироваться" in login_response.text
    assert "Забыли пароль?" in login_response.text
    assert "Подтверждение почты" not in login_response.text
    assert "Не пришло письмо подтверждения?" not in login_response.text
    assert "/resend-verification" not in login_response.text
    assert "Укажите адрес электронной почты, чтобы мы смогли найти ваш аккаунт." in forgot_response.text
    assert "Если такой адрес электронной почты зарегистрирован" not in forgot_response.text
    assert "Подтвердить почту" not in forgot_response.text
    assert "Вернуться ко входу" in forgot_response.text
    assert "минимум 8 символов" in reset_response.text
    assert "без пробелов внутри" in reset_response.text
    assert "Вернуться ко входу" in reset_response.text or "Войти" in reset_response.text
    assert "/static/styles.css" in login_response.text


def test_cabinet_shows_logout_button_and_access_text(client, test_settings):
    register_user(
        email="cabinetux@example.com",
        login="cabinetux",
        password="Secret123",
        repeat_password="Secret123",
        settings=test_settings,
    )
    verification_row = _fetch_one(
        test_settings,
        "SELECT * FROM email_outbox WHERE recipient_email = ? AND template_key = ? ORDER BY id DESC LIMIT 1",
        ("cabinetux@example.com", "email_verification"),
    )
    verify_token = _extract_token_from_link(verification_row["body_text"])
    verify_email(verify_token, settings=test_settings)

    login_response = client.post(
        "/login",
        data={"email_or_login": "cabinetux@example.com", "password": "Secret123"},
        follow_redirects=False,
    )
    assert login_response.status_code == 303

    cabinet_response = client.get("/cabinet")
    assert cabinet_response.status_code == 200
    assert "cabinetux@example.com" in cabinet_response.text
    assert "cabinetux" in cabinet_response.text
    assert "Личный кабинет будет доступен после оплаты" in cabinet_response.text
    assert "После оплаты тарифа откроются личный кабинет, обучение и материалы." in cabinet_response.text
    assert "Аккаунты" not in cabinet_response.text
    assert "Добавить блок" not in cabinet_response.text
    assert "Главная" in cabinet_response.text
    assert "Обучающий блок" not in cabinet_response.text
    assert "Обучающий проект" not in cabinet_response.text
    assert "Перейти к обучению" not in cabinet_response.text
    assert "Скачать файл" not in cabinet_response.text
    assert 'href="/materials/drafts/dair-smoke-20260529/"' not in cabinet_response.text
    assert 'href="/cabinet/learning/project-file"' not in cabinet_response.text
    assert "Выйти" in cabinet_response.text
    assert "/static/styles.css" in cabinet_response.text
    assert "Работа с ИИ" not in cabinet_response.text


def test_password_hash_is_not_plaintext_and_session_revocation(test_settings):
    user = register_user(
        email="hash@example.com",
        login="hashuser",
        password="Secret123",
        repeat_password="Secret123",
        settings=test_settings,
    )
    row = _fetch_one(
        test_settings,
        "SELECT * FROM users WHERE id = ?",
        (user.id,),
    )
    assert row["password_hash"] != "Secret123"
    assert row["password_hash"].startswith("$2")

    session_token = create_session(user.id, settings=test_settings)
    assert get_user_by_session_token(session_token, settings=test_settings) is not None
    assert revoke_session(session_token, settings=test_settings) is True
    assert get_user_by_session_token(session_token, settings=test_settings) is None
