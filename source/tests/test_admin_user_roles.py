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


def test_admin_can_assign_and_remove_moderator_role(client, test_settings):
    admin = _create_verified_user(test_settings, "moderator-admin@example.com", "moderatoradmin", role="admin")
    target = _create_verified_user(test_settings, "moderator-target@example.com", "moderatortarget")
    _login_as(client, test_settings, admin.email)

    response = client.post(f"/admin/users/{target.id}/role", data={"role": "moderator"}, follow_redirects=False)
    assert response.status_code == 303
    assert _role_for_email(test_settings, target.email) == "moderator"

    response = client.post(f"/admin/users/{target.id}/role", data={"role": "user"}, follow_redirects=False)
    assert response.status_code == 303
    assert _role_for_email(test_settings, target.email) == "user"


def test_admin_page_shows_moderator_controls_and_safe_fields(client, test_settings):
    admin = _create_verified_user(test_settings, "moderator-list-admin@example.com", "moderatorlistadmin", role="admin")
    user = _create_verified_user(test_settings, "moderator-list-user@example.com", "moderatorlistuser")
    _login_as(client, test_settings, admin.email)

    response = client.get("/admin/users")
    assert response.status_code == 200
    body = response.text
    assert "Сделать модератором" in body
    assert "Убрать модератора" not in body
    assert "Администратор" in body
    assert user.email in body
    assert "password_hash" not in body.lower()
    assert "token_hash" not in body.lower()


def test_non_admins_cannot_assign_moderators(client, test_settings):
    target = _create_verified_user(test_settings, "moderator-protected@example.com", "moderatorprotected")

    anonymous_response = client.post(f"/admin/users/{target.id}/role", data={"role": "moderator"}, follow_redirects=False)
    assert anonymous_response.status_code == 303
    assert anonymous_response.headers["location"] == "/login"

    _create_verified_user(test_settings, "moderator-normal@example.com", "moderatornormal")
    _login_as(client, test_settings, "moderator-normal@example.com")
    user_response = client.post(f"/admin/users/{target.id}/role", data={"role": "moderator"})
    assert user_response.status_code == 403

    client.cookies.clear()
    _create_verified_user(test_settings, "moderator-staff@example.com", "moderatorstaff", role="moderator")
    _login_as(client, test_settings, "moderator-staff@example.com")
    moderator_response = client.post(f"/admin/users/{target.id}/role", data={"role": "moderator"})
    assert moderator_response.status_code == 403


def test_admin_cannot_demote_admin_or_set_arbitrary_roles(client, test_settings):
    admin = _create_verified_user(test_settings, "moderator-last-admin@example.com", "moderatorlastadmin", role="admin")
    target = _create_verified_user(test_settings, "moderator-target-admin@example.com", "moderatortargetadmin", role="admin")
    _login_as(client, test_settings, admin.email)

    response = client.post(f"/admin/users/{admin.id}/role", data={"role": "user"})
    assert response.status_code == 400
    assert _role_for_email(test_settings, admin.email) == "admin"

    arbitrary_response = client.post(f"/admin/users/{target.id}/role", data={"role": "owner"})
    assert arbitrary_response.status_code == 400
    assert "модератора" in arbitrary_response.text.lower()
    assert _role_for_email(test_settings, target.email) == "admin"
