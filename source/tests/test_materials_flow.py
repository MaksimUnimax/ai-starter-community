from __future__ import annotations

import hashlib
import sqlite3
from urllib.parse import unquote

from app.auth.service import authenticate_user, create_session, register_user, verify_email
from app.materials.routes import LESSON_TEST_SCRIPT_URL, LESSON_TEST_STYLES_URL, LESSON_TEST_URL
from app.materials.service import user_has_materials_access
from app.shared.db import get_database_path, initialize_database
from app.tariffs.service import STARTER_TARIFF_CODE, seed_initial_catalog, update_tariff
from app.user_cabinet.routes import (
    LEARNING_PROJECT_DOWNLOAD_URL,
    LEARNING_PROJECT_FILE_PATH,
    LEARNING_PROJECT_FILE_NAME,
)


def _connect(settings):
    conn = sqlite3.connect(str(get_database_path(settings)))
    conn.row_factory = sqlite3.Row
    return conn


def _extract_token_from_db(settings, email: str) -> str:
    import re

    with _connect(settings) as conn:
        row = conn.execute(
            "SELECT body_text FROM email_outbox WHERE recipient_email = ? AND template_key = ? ORDER BY id DESC LIMIT 1",
            (email, "email_verification"),
        ).fetchone()
    assert row is not None
    match = re.search(r"/verify-email/([A-Za-z0-9_-]+)", row["body_text"])
    assert match
    return match.group(1)


def _set_homepage_tariff(test_settings, *, price_amount_minor: int = 699000, title: str = "Стартовый доступ") -> None:
    seed_initial_catalog(settings=test_settings)
    update_tariff(
        STARTER_TARIFF_CODE,
        title=title,
        price_amount_minor=price_amount_minor,
        settings=test_settings,
    )


def _prepare_verified_user(
    client,
    test_settings,
    email: str,
    login: str,
    grant_access: bool = False,
    role: str = "user",
):
    initialize_database(get_database_path(test_settings))
    register_user(
        email=email,
        login=login,
        password="Secret123",
        repeat_password="Secret123",
        settings=test_settings,
    )
    token = _extract_token_from_db(test_settings, email)
    verify_email(token, settings=test_settings)
    if grant_access or role != "user":
        with _connect(test_settings) as conn:
            if role != "user":
                conn.execute("UPDATE users SET role = ? WHERE email = ?", (role, email))
            if grant_access:
                conn.execute(
                    "UPDATE users SET materials_access_granted_at = CURRENT_TIMESTAMP WHERE email = ?",
                    (email,),
                )
            conn.commit()


def _login_verified_user(client, test_settings, email: str):
    user = authenticate_user(email, "Secret123", settings=test_settings)
    session_token = create_session(user.id, settings=test_settings)
    client.cookies.set(test_settings.session_cookie_name, session_token)


def _prepare_and_login_verified_user(
    client,
    test_settings,
    email: str,
    login: str,
    grant_access: bool = False,
    role: str = "user",
):
    _prepare_verified_user(client, test_settings, email, login, grant_access=grant_access, role=role)
    _login_verified_user(client, test_settings, email)


def test_materials_redirects_unauthenticated_user(client):
    response = client.get("/materials", follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/login"


def test_shared_stylesheet_uses_main_page_theme(client):
    response = client.get("/static/styles.css")
    assert response.status_code == 200
    assert "--bg: #faf6f1;" in response.text
    assert "--primary: #c45c26;" in response.text
    assert "font-family: var(--font-display);" in response.text
    assert ".learning-card-note," in response.text
    assert "width: min(60ch, 100%);" in response.text
    assert "margin-left: auto;" in response.text
    assert "margin-right: auto;" in response.text
    assert "text-align: center;" in response.text


def test_materials_shows_locked_state_without_access(client, test_settings):
    _set_homepage_tariff(test_settings)
    _prepare_and_login_verified_user(client, test_settings, "materials-locked@example.com", "materialslocked")
    response = client.get("/materials")
    assert response.status_code == 200
    assert "/static/styles.css" in response.text
    assert "Обучение" in response.text
    assert "Работа с ИИ" in response.text
    assert "Как разрабатывать с помощью ChatGPT и Codex" in response.text
    assert "Вступление к курсу" in response.text
    assert "Что изучаем" in response.text
    assert "Зачем это нужно" in response.text
    assert "Где это применяется" in response.text
    assert "course-access-badge" in response.text
    assert "Стартовый доступ — 6 990 ₽" in response.text
    assert "4 990 ₽" not in response.text
    assert "Полный доступ откроется после оплаты тарифа." in response.text
    assert "Сейчас вы видите вводную часть и тариф для оплаты." not in response.text
    assert "К разделу материалов" not in response.text
    assert "Уроки курса" not in response.text
    assert "Как мы работаем: ChatGPT проектирует, Codex выполняет, пользователь проверяет" not in response.text
    assert "/materials/lessons/kak-my-rabotaem-chatgpt-codex-user" not in response.text
    assert "Доступные тарифы" not in response.text
    assert "Быстрый старт" not in response.text
    assert "Команды для копирования" not in response.text
    assert "Payment" not in response.text
    assert "Locked" not in response.text

    lesson_response = client.get("/materials/lessons/kak-my-rabotaem-chatgpt-codex-user")
    assert lesson_response.status_code == 200
    assert "Как мы работаем: ChatGPT проектирует, Codex выполняет, пользователь проверяет" in lesson_response.text
    assert "Урок и его материалы откроются после оплаты тарифа." in lesson_response.text
    assert "lesson-content" not in lesson_response.text


def test_draft_learning_route_shows_paywall_for_unpaid_user_and_full_course_for_paid_user(client, test_settings):
    _set_homepage_tariff(test_settings)
    client.cookies.clear()
    anonymous_response = client.get("/materials/drafts/dair-smoke-20260529/", follow_redirects=False)
    assert anonymous_response.status_code == 303
    assert anonymous_response.headers["location"] == "/login"

    _prepare_and_login_verified_user(client, test_settings, "materials-draft-locked@example.com", "materialsdraftlocked")

    locked_response = client.get("/materials/drafts/dair-smoke-20260529/")
    assert locked_response.status_code == 200
    assert "learning access required" not in locked_response.text
    assert "Обучение" in locked_response.text
    assert "Работа с ИИ" in locked_response.text
    assert "Как разрабатывать с помощью ChatGPT и Codex" in locked_response.text
    assert "Вступление к курсу" in locked_response.text
    assert "Что изучаем" in locked_response.text
    assert "Зачем это нужно" in locked_response.text
    assert "Где это применяется" in locked_response.text
    assert "course-access-badge" in locked_response.text
    assert "Стартовый доступ — 6 990 ₽" in locked_response.text
    assert "Полный доступ откроется после оплаты тарифа." in locked_response.text
    assert "Сейчас вы видите вводную часть и тариф для оплаты." not in locked_response.text
    assert "quiz-list" not in locked_response.text
    assert "lesson-shell" not in locked_response.text

    client.cookies.clear()
    _prepare_and_login_verified_user(
        client,
        test_settings,
        "materials-draft-paid@example.com",
        "materialsdraftpaid",
        grant_access=True,
    )
    paid_response = client.get("/materials/drafts/dair-smoke-20260529/")
    assert paid_response.status_code == 200
    assert "learning access required" not in paid_response.text
    assert "quiz-list" in paid_response.text
    assert "lesson-shell" in paid_response.text
    assert "Полный доступ откроется после оплаты тарифа." not in paid_response.text
    assert "Вступление к курсу" in paid_response.text
    assert "Стартовый доступ — 6 990 ₽" not in paid_response.text


def test_access_status_alone_does_not_unlock_materials_or_cabinet(client, test_settings):
    _set_homepage_tariff(test_settings)
    _prepare_and_login_verified_user(client, test_settings, "materials-status-only@example.com", "materialsstatus")
    with _connect(test_settings) as conn:
        conn.execute(
            "UPDATE users SET access_status = 'activated' WHERE email = ?",
            ("materials-status-only@example.com",),
        )
        conn.commit()

    user = authenticate_user("materials-status-only@example.com", "Secret123", settings=test_settings)
    assert user.access_status == "activated"
    assert user.materials_access_granted_at is None
    assert user_has_materials_access(user) is False

    _login_verified_user(client, test_settings, "materials-status-only@example.com")
    materials_response = client.get("/materials")
    cabinet_response = client.get("/cabinet")
    assert materials_response.status_code == 200
    assert cabinet_response.status_code == 200
    assert "Обучение" in materials_response.text
    assert "Вступление к курсу" in materials_response.text
    assert "Личный кабинет будет доступен после оплаты" in cabinet_response.text
    assert "После оплаты тарифа откроются личный кабинет, обучение и материалы." in cabinet_response.text
    assert "Стартовый доступ — 6 990 ₽" in materials_response.text
    assert "Стартовый доступ — 6 990 ₽" in cabinet_response.text
    lesson_response = client.get("/materials/lessons/kak-my-rabotaem-chatgpt-codex-user")
    assert lesson_response.status_code == 200
    assert "Урок и его материалы откроются после оплаты тарифа." in lesson_response.text


def test_materials_shows_placeholder_sections_when_access_granted(client, test_settings):
    _prepare_and_login_verified_user(client, test_settings, "materials-open@example.com", "materialsopen", grant_access=True)
    response = client.get("/materials")
    assert response.status_code == 200
    assert "Работа с ИИ" in response.text
    assert "Курс для новичков без опыта программирования." in response.text
    assert "Уроки курса" in response.text
    assert "Как мы работаем: ChatGPT проектирует, Codex выполняет, пользователь проверяет" in response.text
    assert "/materials/lessons/kak-my-rabotaem-chatgpt-codex-user" in response.text
    assert "/static/styles.css" in response.text
    assert "Личный кабинет" in response.text
    assert "Вернуться в личный кабинет" in response.text
    assert "/cabinet" in response.text
    assert "/admin" not in response.text
    assert "Payment" not in response.text
    assert "Content" not in response.text


def test_cabinet_contains_materials_link_and_locked_hint(client, test_settings):
    _set_homepage_tariff(test_settings)
    _prepare_and_login_verified_user(client, test_settings, "materials-cabinet@example.com", "materialscabinet")
    response = client.get("/cabinet")
    assert response.status_code == 200
    assert "Главная" in response.text
    assert "Личный кабинет будет доступен после оплаты" in response.text
    assert "После оплаты тарифа откроются личный кабинет, обучение и материалы." in response.text
    assert "Стартовый доступ — 6 990 ₽" in response.text
    assert "Аккаунты" not in response.text
    assert "/static/cabinet-local-accounts.js" not in response.text
    assert "Обучающий блок" not in response.text
    assert "Перейти к обучению" not in response.text
    assert "Обучающий проект" not in response.text
    assert "Скачать файл" not in response.text
    assert 'href="/materials/drafts/dair-smoke-20260529/"' not in response.text
    assert 'href="/cabinet/learning/project-file"' not in response.text
    assert "Пройдите обучение, затем скачайте файл, вставьте в чат ChatGPT и следуйте его инструкциям." not in response.text


def test_staff_roles_can_open_materials_without_payment_marker(client, test_settings):
    for role, email, login in [
        ("admin", "materials-admin@example.com", "materialsadmin"),
        ("moderator", "materials-moderator@example.com", "materialsmode"),
    ]:
        client.cookies.clear()
        _prepare_and_login_verified_user(client, test_settings, email, login, role=role)
        response = client.get("/materials")
        assert response.status_code == 200
        assert "Работа с ИИ" in response.text
        assert "Уроки курса" in response.text
        assert "Как мы работаем: ChatGPT проектирует, Codex выполняет, пользователь проверяет" in response.text
        assert "/materials/lessons/kak-my-rabotaem-chatgpt-codex-user" in response.text
        assert "Раздел «Работа с ИИ» будет доступен после оплаты." not in response.text


def test_cabinet_access_labels_for_staff_and_paid_user(client, test_settings):
    _prepare_and_login_verified_user(client, test_settings, "cabinet-paid@example.com", "cabinetpaid", grant_access=True)
    paid_response = client.get("/cabinet")
    assert paid_response.status_code == 200
    assert "Аккаунты" in paid_response.text
    assert "/static/cabinet-local-accounts.js" in paid_response.text
    assert "Перейти к обучению" in paid_response.text
    assert "Скачать файл" in paid_response.text
    assert 'href="/materials/drafts/dair-smoke-20260529/"' in paid_response.text
    assert 'href="/cabinet/learning/project-file"' in paid_response.text

    client.cookies.clear()
    _prepare_and_login_verified_user(client, test_settings, "cabinet-moderator@example.com", "cabinetmod", role="moderator")
    moderator_response = client.get("/cabinet")
    assert moderator_response.status_code == 200
    assert "Аккаунты" in moderator_response.text
    assert "Перейти к обучению" in moderator_response.text
    assert "Скачать файл" in moderator_response.text
    assert 'href="/materials/drafts/dair-smoke-20260529/"' in moderator_response.text
    assert 'href="/cabinet/learning/project-file"' in moderator_response.text

    client.cookies.clear()
    _prepare_and_login_verified_user(client, test_settings, "cabinet-admin@example.com", "cabinetadm", role="admin")
    admin_response = client.get("/cabinet")
    assert admin_response.status_code == 200
    assert "Аккаунты" in admin_response.text
    assert "Перейти к обучению" in admin_response.text
    assert "Скачать файл" in admin_response.text
    assert 'href="/materials/drafts/dair-smoke-20260529/"' in admin_response.text
    assert 'href="/cabinet/learning/project-file"' in admin_response.text


def test_settings_page_is_compact_and_password_change_still_works(client, test_settings):
    _prepare_and_login_verified_user(client, test_settings, "settings-user@example.com", "settingsuser")
    response = client.get("/cabinet/settings")
    assert response.status_code == 200
    assert "settings-shell" in response.text
    assert "settings-card" in response.text
    assert "settings-meta" in response.text
    assert "settings-form" in response.text
    assert "Управляйте паролем и данными учётной записи без лишнего визуального шума." in response.text
    assert "Аккаунт" in response.text
    assert "Email" in response.text
    assert "Смена пароля" in response.text
    assert "Текущий пароль" in response.text
    assert "Новый пароль" in response.text
    assert "Повтор нового пароля" in response.text

    post_response = client.post(
        "/cabinet/settings/password",
        data={
            "current_password": "Secret123",
            "password": "Secret456",
            "repeat_password": "Secret456",
        },
        follow_redirects=False,
    )
    assert post_response.status_code == 303
    assert post_response.headers["location"] == "/cabinet/settings?success=1"
    assert authenticate_user("settings-user@example.com", "Secret456", settings=test_settings).email == "settings-user@example.com"


def test_learning_access_helper_and_project_download_route(client, test_settings):
    client.cookies.clear()
    anonymous_response = client.get(LEARNING_PROJECT_DOWNLOAD_URL, follow_redirects=False)
    assert anonymous_response.status_code == 303
    assert anonymous_response.headers["location"] == "/login"

    _prepare_and_login_verified_user(client, test_settings, "learning-locked@example.com", "learninglocked")
    locked_response = client.get(LEARNING_PROJECT_DOWNLOAD_URL, follow_redirects=False)
    assert locked_response.status_code == 403
    assert user_has_materials_access(authenticate_user("learning-locked@example.com", "Secret123", settings=test_settings)) is False

    with _connect(test_settings) as conn:
        conn.execute(
            "UPDATE users SET materials_access_granted_at = CURRENT_TIMESTAMP WHERE email = ?",
            ("learning-locked@example.com",),
        )
        conn.commit()

    unlocked_user = authenticate_user("learning-locked@example.com", "Secret123", settings=test_settings)
    assert user_has_materials_access(unlocked_user) is True

    client.cookies.clear()
    session_token = create_session(unlocked_user.id, settings=test_settings)
    client.cookies.set(test_settings.session_cookie_name, session_token)
    download_response = client.get(LEARNING_PROJECT_DOWNLOAD_URL)
    assert download_response.status_code == 200
    assert "attachment" in download_response.headers.get("content-disposition", "").lower()
    assert LEARNING_PROJECT_FILE_NAME in unquote(download_response.headers.get("content-disposition", ""))
    assert hashlib.sha256(download_response.content).hexdigest() == hashlib.sha256(LEARNING_PROJECT_FILE_PATH.read_bytes()).hexdigest()
    assert LEARNING_PROJECT_FILE_PATH.is_file()
    assert "/static/" not in str(LEARNING_PROJECT_FILE_PATH)

    client.cookies.clear()
    _prepare_and_login_verified_user(client, test_settings, "learning-admin@example.com", "learningadmin", role="admin")
    assert user_has_materials_access(authenticate_user("learning-admin@example.com", "Secret123", settings=test_settings)) is True
    admin_download_response = client.get(LEARNING_PROJECT_DOWNLOAD_URL)
    assert admin_download_response.status_code == 200
    assert hashlib.sha256(admin_download_response.content).hexdigest() == hashlib.sha256(LEARNING_PROJECT_FILE_PATH.read_bytes()).hexdigest()


def test_materials_redirects_unauthenticated_user_is_unchanged(client):
    response = client.get("/materials", follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/login"


def test_materials_access_column_exists_after_schema_init(test_settings):
    initialize_database(get_database_path(test_settings))
    with _connect(test_settings) as conn:
        columns = {row["name"] for row in conn.execute("PRAGMA table_info(users)").fetchall()}
    assert "materials_access_granted_at" in columns
