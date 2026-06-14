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


def _nav_links_block(body: str) -> str:
    start = body.index('<nav class="nav-links"')
    end = body.index("</nav>", start) + len("</nav>")
    return body[start:end]


def test_anonymous_navigation_shows_public_links_and_login(client):
    response = client.get("/login")
    assert response.status_code == 200
    nav = _nav_block(response.text)
    assert 'class="button button-secondary nav-pill"' in nav
    assert "Главная" in nav
    assert "Вход / регистрация" in nav
    assert 'href="/"' in nav
    assert 'href="/login"' in nav
    assert "Что вы получите" not in nav
    assert "Первый проект" not in nav
    assert "Как проходит работа" not in nav
    assert "Цена" not in nav
    assert "Личный кабинет" not in nav
    assert "Работа с ИИ" not in nav
    assert "Админ-панель" not in nav
    assert "nav-account-compact" not in nav
    assert "nav-account-dropdown" not in nav


def test_login_and_register_pages_link_to_each_other(client):
    login_response = client.get("/login")
    register_response = client.get("/register")

    assert login_response.status_code == 200
    assert register_response.status_code == 200
    assert "Зарегистрироваться" in login_response.text
    assert "Забыл пароль?" in login_response.text
    assert "Нет аккаунта?" not in login_response.text
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
        nav_links = _nav_links_block(body)
        assert "Войти" not in nav
        assert "Главная" in nav
        assert "Обучение" in nav
        assert "Личный кабинет" in nav
        assert "nav-account-compact" in nav
        assert "nav-account-name" in nav
        assert "nav-account-email" not in nav
        assert "nav-account-dropdown" in nav
        assert "nav-account-menu" in nav
        assert "nav-account-link" not in nav
        assert "nav-settings" not in nav
        assert 'href="/cabinet/settings"' in nav
        assert "nav-pill" in nav
        assert 'method="post"' in nav
        assert 'action="/logout"' in nav
        assert "Выйти" in nav
        assert "Регистрация" not in nav
        assert "Начать первый проект" not in nav
        assert "Работа с ИИ" not in nav
        assert "Настройки" in nav
        assert "Выйти" in nav
        assert "Выйти" not in nav_links
        assert "Настройки" not in nav_links

    assert "navuser" in landing.text
    assert "nav-user@example.com" not in landing.text
    cabinet_nav = _nav_block(cabinet.text)
    assert cabinet_nav.index("Главная") < cabinet_nav.index("Обучение") < cabinet_nav.index("Личный кабинет") < cabinet_nav.index("nav-account-dropdown")


def test_authenticated_moderator_navigation_has_no_admin_panel(client, test_settings):
    _make_user(client, test_settings, "nav-moderator@example.com", "navmoderator", role="moderator")

    landing = client.get("/login")
    cabinet = client.get("/cabinet")

    assert landing.status_code == 200
    assert cabinet.status_code == 200

    for body in (landing.text, cabinet.text):
        nav = _nav_block(body)
        nav_links = _nav_links_block(body)
        assert "Войти" not in nav
        assert "Админ-панель" not in nav
        assert "Главная" in nav
        assert "Обучение" in nav
        assert "Личный кабинет" in nav
        assert "nav-account-compact" in nav
        assert "nav-account-email" not in nav
        assert "nav-account-dropdown" in nav
        assert "nav-account-menu" in nav
        assert "nav-account-link" not in nav
        assert "nav-settings" not in nav
        assert 'href="/cabinet/settings"' in nav
        assert 'method="post"' in nav
        assert 'action="/logout"' in nav
        assert "Выйти" in nav
        assert "Выйти" not in nav_links
        assert "Настройки" not in nav_links


def test_authenticated_admin_navigation_includes_admin_panel(client, test_settings):
    _make_user(client, test_settings, "nav-admin@example.com", "navadmin", role="admin")

    landing = client.get("/login")
    cabinet = client.get("/cabinet")

    assert landing.status_code == 200
    assert cabinet.status_code == 200

    for body in (landing.text, cabinet.text):
        nav = _nav_block(body)
        nav_links = _nav_links_block(body)
        assert "Войти" not in nav
        assert "Главная" in nav
        assert "Обучение" in nav
        assert "Личный кабинет" in nav
        assert "Админ-панель" in nav
        assert "nav-account-compact" in nav
        assert "nav-account-email" not in nav
        assert "nav-account-dropdown" in nav
        assert "nav-account-menu" in nav
        assert "nav-account-link" not in nav
        assert "nav-settings" not in nav
        assert 'href="/cabinet/settings"' in nav
        assert 'method="post"' in nav
        assert 'action="/logout"' in nav
        assert "Выйти" in nav
        assert "Выйти" not in nav_links
        assert "Настройки" not in nav_links

    assert "navadmin" in landing.text
    assert "nav-admin@example.com" not in landing.text
    cabinet_nav = _nav_block(cabinet.text)
    assert cabinet_nav.index("Главная") < cabinet_nav.index("Обучение") < cabinet_nav.index("Личный кабинет") < cabinet_nav.index("Админ-панель") < cabinet_nav.index("nav-account-dropdown")
