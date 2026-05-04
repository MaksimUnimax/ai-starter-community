from __future__ import annotations

import re
import sqlite3

import pytest

from app.auth.service import (
    ALLOWED_ROLES,
    ROLE_LABELS_RU,
    RoleError,
    authenticate_user,
    create_session,
    normalize_role,
    register_user,
    role_label_ru,
    update_user_role,
    verify_email,
)
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


def _create_verified_user(test_settings, email: str, login: str, role: str = "user"):
    register_user(
        email=email,
        login=login,
        password="Secret123",
        repeat_password="Secret123",
        settings=test_settings,
    )
    verify_email(_extract_verify_token(test_settings, email), settings=test_settings)
    if role != "user":
        with _connect(test_settings) as conn:
            conn.execute("UPDATE users SET role = ? WHERE email = ?", (role, email))
            conn.commit()
    return authenticate_user(email, "Secret123", settings=test_settings)


def _login_as(client, test_settings, email: str):
    user = authenticate_user(email, "Secret123", settings=test_settings)
    session_token = create_session(user.id, settings=test_settings)
    client.cookies.set(test_settings.session_cookie_name, session_token)
    return user


def _role_for_email(test_settings, email: str) -> str:
    with _connect(test_settings) as conn:
        row = conn.execute("SELECT role FROM users WHERE email = ?", (email,)).fetchone()
    assert row is not None
    return str(row["role"])


def test_role_policy_is_explicit_and_labeled_in_russian():
    assert ALLOWED_ROLES == ("user", "moderator", "admin")
    assert ROLE_LABELS_RU == {
        "user": "пользователь",
        "moderator": "модератор",
        "admin": "администратор",
    }
    assert role_label_ru("moderator") == "модератор"
    with pytest.raises(RoleError):
        normalize_role("owner")


def test_update_user_role_rejects_unknown_role(test_settings):
    user = _create_verified_user(test_settings, "role-invalid@example.com", "roleinvalid")
    with pytest.raises(RoleError):
        update_user_role(user_id=user.id, new_role="owner", settings=test_settings)


def test_admin_users_page_shows_role_management_controls(client, test_settings):
    _create_verified_user(test_settings, "admin@example.com", "adminuser", role="admin")
    _create_verified_user(test_settings, "viewer@example.com", "vieweruser")
    _login_as(client, test_settings, "admin@example.com")

    response = client.get("/admin/users")
    assert response.status_code == 200
    body = response.text
    assert "Изменить роль" in body
    assert "Сохранить роль" in body
    assert "пользователь" in body
    assert "модератор" in body
    assert "администратор" in body
    assert "/admin/users/" in body
    assert "/role" in body
    assert "password_hash" not in body.lower()
    assert "token_hash" not in body.lower()
    assert "raw token" not in body.lower()
    assert "cookie" not in body.lower()
    assert "email_outbox" not in body.lower()


def test_admin_can_change_user_roles(client, test_settings):
    admin = _create_verified_user(test_settings, "role-admin@example.com", "roleadmin", role="admin")
    target = _create_verified_user(test_settings, "role-target@example.com", "roletarget")
    _login_as(client, test_settings, admin.email)

    response = client.post(f"/admin/users/{target.id}/role", data={"role": "moderator"}, follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/admin/users"
    assert _role_for_email(test_settings, target.email) == "moderator"

    response = client.post(f"/admin/users/{target.id}/role", data={"role": "user"}, follow_redirects=False)
    assert response.status_code == 303
    assert _role_for_email(test_settings, target.email) == "user"

    response = client.post(f"/admin/users/{target.id}/role", data={"role": "admin"}, follow_redirects=False)
    assert response.status_code == 303
    assert _role_for_email(test_settings, target.email) == "admin"


def test_admin_role_change_rejects_invalid_role(client, test_settings):
    admin = _create_verified_user(test_settings, "invalid-admin@example.com", "invalidadmin", role="admin")
    target = _create_verified_user(test_settings, "invalid-target@example.com", "invalidtarget")
    _login_as(client, test_settings, admin.email)

    response = client.post(f"/admin/users/{target.id}/role", data={"role": "owner"})
    assert response.status_code == 400
    assert "Выберите допустимую роль" in response.text
    assert _role_for_email(test_settings, target.email) == "user"


def test_last_admin_cannot_be_demoted(client, test_settings):
    admin = _create_verified_user(test_settings, "last-admin@example.com", "lastadmin", role="admin")
    _login_as(client, test_settings, admin.email)

    response = client.post(f"/admin/users/{admin.id}/role", data={"role": "user"})
    assert response.status_code == 400
    assert "последнего администратора" in response.text
    assert _role_for_email(test_settings, admin.email) == "admin"


def test_non_admin_moderator_and_anonymous_cannot_change_roles(client, test_settings):
    target = _create_verified_user(test_settings, "protected-target@example.com", "protectedtarget")

    anonymous_response = client.post(f"/admin/users/{target.id}/role", data={"role": "admin"}, follow_redirects=False)
    assert anonymous_response.status_code == 303
    assert anonymous_response.headers["location"] == "/login"

    _create_verified_user(test_settings, "normal-poster@example.com", "normalposter")
    _login_as(client, test_settings, "normal-poster@example.com")
    user_response = client.post(f"/admin/users/{target.id}/role", data={"role": "admin"})
    assert user_response.status_code == 403

    client.cookies.clear()
    _create_verified_user(test_settings, "moderator-poster@example.com", "moderatorposter", role="moderator")
    _login_as(client, test_settings, "moderator-poster@example.com")
    moderator_response = client.post(f"/admin/users/{target.id}/role", data={"role": "admin"})
    assert moderator_response.status_code == 403
    assert _role_for_email(test_settings, target.email) == "user"
