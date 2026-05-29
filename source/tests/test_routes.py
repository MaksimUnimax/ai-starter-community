from __future__ import annotations

import re
import sqlite3

from app.auth.service import authenticate_user, create_session, register_user, verify_email
from app.shared.db import get_database_path


def _connect(settings):
    conn = sqlite3.connect(str(get_database_path(settings)))
    conn.row_factory = sqlite3.Row
    return conn


def _extract_verify_token(settings, email: str) -> str:
    with _connect(settings) as conn:
        row = conn.execute(
            "SELECT body_text FROM email_outbox WHERE recipient_email = ? AND template_key = ? ORDER BY id DESC LIMIT 1",
            (email, "email_verification"),
        ).fetchone()
    assert row is not None
    match = re.search(r"/verify-email/([A-Za-z0-9_-]+)", row["body_text"])
    assert match
    return match.group(1)


def _make_authenticated_user(client, test_settings, email: str = "landing@example.com", login: str = "landinguser"):
    register_user(
        email=email,
        login=login,
        password="Secret123",
        repeat_password="Secret123",
        settings=test_settings,
    )
    token = _extract_verify_token(test_settings, email)
    verify_email(token, settings=test_settings)
    user = authenticate_user(email, "Secret123", settings=test_settings)
    session_token = create_session(user.id, settings=test_settings)
    client.cookies.set(test_settings.session_cookie_name, session_token)


def test_landing_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "OpenScript — Первый ИИ-бот без опыта" in response.text
    assert "Создайте первого ИИ-бота без опыта в программировании" in response.text
    assert "Начать первый проект" in response.text
    assert "Войти" in response.text
    assert "Вы покупаете не курс, а первый управляемый опыт разработки" in response.text
    assert "Стартовый месяц OpenScript — 4 990 ₽" in response.text
    assert "Вопросы перед стартом" in response.text
    assert 'href="#how-it-works"' in response.text
    assert 'href="/login"' in response.text
    assert "Юридическая информация" in response.text
    assert "ИП Ягофаров М.Р." in response.text
    assert "Индивидуальный предприниматель Ягофаров Максим Ринатович" not in response.text
    assert "ИНН: 741705866660" in response.text
    assert "ОГРНИП: 320745600093211" in response.text
    assert "OpenScripts@yandex.com" in response.text


def test_authenticated_landing_page_switches_to_account_and_learning_links(client, test_settings):
    _make_authenticated_user(client, test_settings)

    response = client.get("/")
    assert response.status_code == 200
    assert "Войти" not in response.text
    assert "Начать первый проект" not in response.text
    assert "Работа с ИИ" not in response.text
    assert "Обучение" in response.text
    assert "Личный кабинет" in response.text
    assert "Перейти к обучению" in response.text
    assert "Выйти" in response.text
    assert 'href="/materials/drafts/dair-smoke-20260529/"' in response.text
    assert 'href="/cabinet"' in response.text
    assert 'action="/logout"' in response.text


def test_shared_header_css_adds_compact_mobile_nav_layout(client):
    response = client.get("/static/styles.css")
    assert response.status_code == 200
    assert ".top-nav .logout-form {" in response.text
    assert ".top-nav .nav-brand-row {" in response.text
    assert ".top-nav .nav-menu-row {" in response.text
    assert ".top-nav .nav-account-compact {" in response.text
    assert ".top-nav .nav-account-email {" in response.text
    assert ".top-nav .nav-settings {" in response.text
    assert "@media (max-width: 720px)" in response.text
    assert ".top-nav .nav-inner {" in response.text
    assert "flex-direction: column;" in response.text
    assert ".top-nav .nav-brand-row {" in response.text
    assert ".top-nav .nav-links {" in response.text
    assert "grid-template-columns: repeat(2, minmax(0, 1fr));" in response.text
    assert ".top-nav .nav-links .nav-pill," in response.text
    assert "min-height: 38px;" in response.text
    assert ".top-nav .nav-form > .button {" in response.text
    assert "@media (max-width: 520px)" in response.text
    assert "grid-template-columns: 1fr;" in response.text
    assert ".top-nav .nav-settings-label {" in response.text
    assert ".top-nav .nav-settings-label {\n    display: none;" not in response.text


def test_login_and_register_pages(client):
    login_response = client.get("/login")
    login_head_response = client.head("/login")
    register_response = client.get("/register")
    check_email_response = client.get("/check-email")
    resend_response = client.get("/resend-verification")
    cabinet_response = client.get("/cabinet", follow_redirects=False)
    assert login_response.status_code == 200
    assert login_head_response.status_code == 200
    assert register_response.status_code == 200
    assert check_email_response.status_code == 200
    assert resend_response.status_code == 200
    assert cabinet_response.status_code == 303
    assert cabinet_response.headers["location"] == "/login"
    assert "Вход в аккаунт" in login_response.text
    assert "Регистрация" in register_response.text
    assert "Регистрация временно закрыта" in register_response.text
    assert "Перейти ко входу" in register_response.text
    assert "/login" in register_response.text
    assert "Создать аккаунт" not in register_response.text
    assert "Нет аккаунта?" in login_response.text
    assert "Зарегистрироваться" in login_response.text
    assert "Забыли пароль?" in login_response.text
    assert "Уже есть аккаунт?" in register_response.text
    assert "Войти" in register_response.text
    assert "Проверьте почту" in check_email_response.text
    assert "Не пришло письмо подтверждения?" in check_email_response.text
    assert "/resend-verification" in check_email_response.text
    assert "Повторная отправка письма подтверждения" in resend_response.text
    assert "/static/styles.css" in login_response.text
    assert "/static/styles.css" in register_response.text
    assert "Электронная почта или логин" in login_response.text
    assert "Регистрация временно закрыта" in register_response.text
    assert "Перейти ко входу" in register_response.text
    assert "Создать аккаунт" not in register_response.text
    assert "Подтверждение почты" not in login_response.text
    assert "Не пришло письмо подтверждения?" not in login_response.text
    assert "Отправить письмо подтверждения" not in login_response.text


def test_auth_utility_pages_use_shared_base_and_styles(client):
    check_email_response = client.get("/check-email")
    verify_email_response = client.get("/verify-email/example-token")
    forgot_response = client.get("/forgot-password")
    reset_response = client.get("/reset-password/example-token")
    resend_response = client.get("/resend-verification")

    assert check_email_response.status_code == 200
    assert verify_email_response.status_code == 200
    assert forgot_response.status_code == 200
    assert reset_response.status_code == 200
    assert resend_response.status_code == 200

    for response in (
        check_email_response,
        verify_email_response,
        forgot_response,
        reset_response,
        resend_response,
    ):
        assert "/static/styles.css" in response.text
        assert "OpenScript" in response.text
        assert "Юридическая информация" in response.text
        assert "ИП Ягофаров М.Р." in response.text
        assert "Индивидуальный предприниматель Ягофаров Максим Ринатович" not in response.text
        assert "ИНН: 741705866660" in response.text
        assert "ОГРНИП: 320745600093211" in response.text
        assert "OpenScripts@yandex.com" in response.text
        assert "Личный кабинет" not in response.text
        assert "Работа с ИИ" not in response.text
        assert "Админ-панель" not in response.text

    assert "Не пришло письмо подтверждения?" in check_email_response.text
    assert "Укажите адрес электронной почты, чтобы мы смогли найти ваш аккаунт." in forgot_response.text
    assert "Если такой адрес электронной почты зарегистрирован" not in forgot_response.text
    assert "Подтвердить почту" not in forgot_response.text
    assert "Вернуться ко входу" in forgot_response.text
    assert "Войти" in reset_response.text or "Вернуться ко входу" in reset_response.text
    assert "Повторная отправка письма подтверждения" in resend_response.text


def test_placeholder_post_routes_redirect(client):
    login_response = client.post(
        "/login",
        data={"email_or_login": "user@example.com", "password": "secret"},
        follow_redirects=False,
    )
    register_response = client.post(
        "/register",
        data={
            "email": "user@example.com",
            "login": "user123",
            "password": "Secret123",
            "repeat_password": "Secret123",
        },
        follow_redirects=False,
    )
    logout_response = client.post("/logout", follow_redirects=False)
    assert login_response.status_code == 200
    assert register_response.status_code == 403
    assert "Регистрация временно закрыта" in register_response.text
    assert "/login" in register_response.text
    assert logout_response.status_code == 303
