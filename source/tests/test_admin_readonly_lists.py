from __future__ import annotations

import re
import sqlite3

import pytest

from app.auth.service import authenticate_user, create_session, register_user, verify_email
from app.shared.db import get_database_path
from app.tariffs.service import STARTER_TARIFF_CODE, seed_initial_catalog


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


@pytest.mark.parametrize(
    ("path",),
    [
        ("/admin/users",),
        ("/admin/tariffs",),
        ("/admin/paid-options",),
    ],
)
def test_anonymous_admin_list_pages_redirect_to_login(client, path):
    response = client.get(path, follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/login"


@pytest.mark.parametrize(
    ("path",),
    [
        ("/admin/users",),
        ("/admin/tariffs",),
        ("/admin/paid-options",),
    ],
)
def test_normal_user_gets_forbidden_on_admin_list_pages(client, test_settings, path):
    _make_user(client, test_settings, "user@example.com", "regularuser", role="user")
    response = client.get(path)
    assert response.status_code == 403
    assert "Forbidden" in response.text


@pytest.mark.parametrize(
    ("path",),
    [
        ("/admin/users",),
        ("/admin/tariffs",),
        ("/admin/paid-options",),
    ],
)
def test_admin_user_can_open_admin_list_pages(client, test_settings, path):
    _make_user(client, test_settings, "admin@example.com", "adminuser", role="admin")
    if path != "/admin/users":
        seed_initial_catalog(settings=test_settings)
    response = client.get(path)
    assert response.status_code == 200


def test_admin_users_shows_safe_fields_and_hides_sensitive_data(client, test_settings):
    _make_user(client, test_settings, "admin@example.com", "adminuser", role="admin")
    register_user(
        email="viewer@example.com",
        login="vieweruser",
        password="Secret123",
        repeat_password="Secret123",
        settings=test_settings,
    )
    with _connect(test_settings) as conn:
        conn.execute(
            """
            UPDATE users
            SET role = ?, is_active = 0, email_verified_at = NULL,
                materials_access_granted_at = CURRENT_TIMESTAMP,
                access_status = ?, updated_at = CURRENT_TIMESTAMP
            WHERE email = ?
            """,
            ("user", "activated", "viewer@example.com"),
        )
        conn.commit()

    response = client.get("/admin/users")
    assert response.status_code == 200
    body = response.text
    assert "admin@example.com" in body
    assert "viewer@example.com" in body
    assert "adminuser" in body
    assert "vieweruser" in body
    assert "verified" in body
    assert "unverified" in body
    assert "yes" in body
    assert "no" in body
    assert "password_hash" not in body.lower()
    assert "token_hash" not in body.lower()
    assert "raw token" not in body.lower()
    assert "cookie" not in body.lower()
    assert "email_outbox" not in body.lower()


def test_admin_tariffs_shows_starter_tariff_and_admin_controls(client, test_settings):
    _make_user(client, test_settings, "admin@example.com", "adminuser", role="admin")
    seed_initial_catalog(settings=test_settings)

    response = client.get("/admin/tariffs")
    assert response.status_code == 200
    body = response.text
    assert STARTER_TARIFF_CODE in body
    assert "Стартовый доступ" in body
    assert "AI / GPT-инструмент" in body
    assert "/admin/tariffs/new" in body
    assert f"/admin/tariffs/{STARTER_TARIFF_CODE}/edit" in body
    assert f"/admin/tariffs/{STARTER_TARIFF_CODE}/archive" in body
    assert "/admin/paid-options/new" not in body
    assert "/admin/payments" not in body


def test_admin_paid_options_shows_catalog_and_admin_controls(client, test_settings):
    _make_user(client, test_settings, "admin@example.com", "adminuser", role="admin")
    seed_initial_catalog(settings=test_settings)

    response = client.get("/admin/paid-options")
    assert response.status_code == 200
    body = response.text
    assert "AI / GPT-инструмент" in body
    assert "Сервер" in body
    assert "VPN" in body
    assert "отдельная цена не задана" in body
    assert "/admin/paid-options/new" in body
    assert "/admin/paid-options/ai_gpt_tool/edit" in body
    assert "/admin/paid-options/ai_gpt_tool/archive" in body
    assert "/admin/tariffs/" not in body
    assert "/admin/payments" not in body


def test_admin_dashboard_links_to_read_only_list_pages(client, test_settings):
    _make_user(client, test_settings, "admin@example.com", "adminuser", role="admin")
    response = client.get("/admin")
    assert response.status_code == 200
    body = response.text
    assert '/admin/users' in body
    assert '/admin/tariffs' in body
    assert '/admin/paid-options' in body
    assert 'Материалы - позже' in body
    assert 'Платежи - позже' in body
