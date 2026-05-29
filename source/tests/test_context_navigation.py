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


def _make_user(client, test_settings, email: str, login: str, role: str = "user") -> None:
    register_user(
        email=email,
        login=login,
        password="Secret123",
        repeat_password="Secret123",
        settings=test_settings,
    )
    token = _extract_verify_token(test_settings, email)
    verify_email(token, settings=test_settings)
    if role != "user":
        with _connect(test_settings) as conn:
            conn.execute("UPDATE users SET role = ? WHERE email = ?", (role, email))
            conn.commit()
    user = authenticate_user(email, "Secret123", settings=test_settings)
    session_token = create_session(user.id, settings=test_settings)
    client.cookies.set(test_settings.session_cookie_name, session_token)


def _nav_block(body: str) -> str:
    start = body.index("<header")
    end = body.index("</header>") + len("</header>")
    return body[start:end]


def test_anonymous_navigation_shows_public_links_and_login(client):
    response = client.get("/login")
    assert response.status_code == 200
    nav = _nav_block(response.text)
    assert "Что вы получите" in nav
    assert "Первый проект" in nav
    assert "Как проходит работа" in nav
    assert "Цена" in nav
    assert "Войти" in nav
    assert "Начать первый проект" not in nav
    assert "Личный кабинет" not in nav
    assert "Работа с ИИ" not in nav
    assert "Админ-панель" not in nav
    assert "Регистрация" not in nav


def test_login_and_register_pages_link_to_each_other(client):
    login_response = client.get("/login")
    register_response = client.get("/register")

    assert login_response.status_code == 200
    assert register_response.status_code == 200
    assert "Нет аккаунта?" in login_response.text
    assert "Зарегистрироваться" in login_response.text
    assert "/register" in login_response.text
    assert "Уже есть аккаунт?" in register_response.text
    assert "Войти" in register_response.text
    assert "/login" in register_response.text


def test_authenticated_user_navigation_order_and_labels(client, test_settings):
    _make_user(client, test_settings, "nav-user@example.com", "navuser", role="user")

    landing = client.get("/login")
    cabinet = client.get("/cabinet")

    assert landing.status_code == 200
    assert cabinet.status_code == 200

    for body in (landing.text, cabinet.text):
        nav = _nav_block(body)
        assert "Войти" not in nav
        assert "Начать первый проект" not in nav
        assert "Регистрация" not in nav
        assert "Админ-панель" not in nav
        assert "Главная" in nav
        assert "Обучение" in nav
        assert "Личный кабинет" in nav
        assert "Выйти" in nav

    cabinet_nav = _nav_block(cabinet.text)
    assert cabinet_nav.index("Главная") < cabinet_nav.index("Обучение") < cabinet_nav.index("Личный кабинет") < cabinet_nav.index("Выйти")


def test_authenticated_moderator_navigation_has_no_admin_panel(client, test_settings):
    _make_user(client, test_settings, "nav-moderator@example.com", "navmoderator", role="moderator")

    landing = client.get("/login")
    cabinet = client.get("/cabinet")

    assert landing.status_code == 200
    assert cabinet.status_code == 200

    for body in (landing.text, cabinet.text):
        nav = _nav_block(body)
        assert "Войти" not in nav
        assert "Админ-панель" not in nav
        assert "Главная" in nav
        assert "Обучение" in nav
        assert "Личный кабинет" in nav
        assert "Выйти" in nav


def test_authenticated_admin_navigation_includes_admin_panel(client, test_settings):
    _make_user(client, test_settings, "nav-admin@example.com", "navadmin", role="admin")

    landing = client.get("/login")
    cabinet = client.get("/cabinet")

    assert landing.status_code == 200
    assert cabinet.status_code == 200

    for body in (landing.text, cabinet.text):
        nav = _nav_block(body)
        assert "Войти" not in nav
        assert "Начать первый проект" not in nav
        assert "Регистрация" not in nav
        assert "Главная" in nav
        assert "Обучение" in nav
        assert "Личный кабинет" in nav
        assert "Админ-панель" in nav
        assert "Выйти" in nav

    cabinet_nav = _nav_block(cabinet.text)
    assert cabinet_nav.index("Главная") < cabinet_nav.index("Обучение") < cabinet_nav.index("Личный кабинет") < cabinet_nav.index("Админ-панель") < cabinet_nav.index("Выйти")
