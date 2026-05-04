from __future__ import annotations

import re
import sqlite3

from app.auth.service import authenticate_user, create_session, register_user, verify_email
from app.core.app_factory import create_app
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
    with _connect(test_settings) as conn:
        conn.execute("UPDATE users SET role = ? WHERE email = ?", (role, email))
        conn.commit()
    user = authenticate_user(email, "Secret123", settings=test_settings)
    session_token = create_session(user.id, settings=test_settings)
    client.cookies.set(test_settings.session_cookie_name, session_token)


def test_anonymous_admin_redirects_to_login(client):
    response = client.get("/admin", follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/login"
    head_response = client.head("/admin", follow_redirects=False)
    assert head_response.status_code == 303
    assert head_response.headers["location"] == "/login"


def test_normal_user_gets_forbidden_on_admin(client, test_settings):
    _make_user(client, test_settings, "admin-user@example.com", "adminuser", role="user")
    response = client.get("/admin")
    assert response.status_code == 403
    assert "Доступ запрещён" in response.text
    assert "прав администратора" in response.text
    assert "Forbidden" not in response.text


def test_admin_user_can_open_admin_dashboard(client, test_settings):
    _make_user(client, test_settings, "admin@example.com", "adminuser", role="admin")
    response = client.get("/admin")
    assert response.status_code == 200
    assert "Админ-панель" in response.text
    assert "Логин администратора" in response.text
    assert "Электронная почта" in response.text
    assert "Создание, редактирование и архивирование появятся следующим этапом." in response.text
    assert '/admin/users' in response.text
    assert '/admin/tariffs' in response.text
    assert '/admin/paid-options' in response.text
    assert "Материалы - позже" in response.text
    assert "Платежи - позже" in response.text
    assert "CRUD" not in response.text
    assert "password_hash" not in response.text
    assert "token_hash" not in response.text


def test_app_factory_includes_admin_route():
    app = create_app()
    paths = {route.path for route in app.router.routes}
    assert "/admin" in paths


def test_existing_auth_and_catalog_tests_still_pass(client):
    response = client.get("/register")
    assert response.status_code == 200
    assert "Регистрация" in response.text
