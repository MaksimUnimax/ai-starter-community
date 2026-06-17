from __future__ import annotations

import re
import sqlite3

from app.auth.service import authenticate_user, create_session, register_user, verify_email


def _connect(settings):
    conn = sqlite3.connect(str(settings.database_path))
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


def _extract_csrf_token(body_text: str) -> str:
    match = re.search(r'name="_csrf_token" value="([^"]+)"', body_text)
    assert match, "csrf token not found"
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
    client.cookies.set(test_settings.session_cookie_name, create_session(user.id, settings=test_settings))
    return user


def test_login_and_logout_forms_require_csrf_tokens(client, test_settings, caplog):
    _create_verified_user(test_settings, "csrf-login@example.com", "csrflogin")

    login_page = client.get("/login")
    assert login_page.status_code == 200
    assert 'name="_csrf_token"' in login_page.text
    csrf_token = _extract_csrf_token(login_page.text)

    missing_token_response = client.post(
        "/login",
        data={"email_or_login": "csrflogin", "password": "Secret123"},
        follow_redirects=False,
    )
    invalid_token = "invalid-csrf-token"
    invalid_token_response = client.post(
        "/login",
        data={
            "email_or_login": "csrflogin",
            "password": "Secret123",
            "_csrf_token": invalid_token,
        },
        follow_redirects=False,
    )
    valid_login_response = client.post(
        "/login",
        data={
            "email_or_login": "csrflogin",
            "password": "Secret123",
            "_csrf_token": csrf_token,
        },
        follow_redirects=False,
    )

    assert missing_token_response.status_code == 403
    assert invalid_token_response.status_code == 403
    assert invalid_token not in invalid_token_response.text
    assert invalid_token not in caplog.text
    assert valid_login_response.status_code == 303
    assert client.cookies.get(test_settings.session_cookie_name)

    settings_page = client.get("/cabinet/settings")
    assert settings_page.status_code == 200
    assert 'name="_csrf_token"' in settings_page.text
    logout_token = _extract_csrf_token(settings_page.text)

    logout_missing_token = client.post("/logout", follow_redirects=False)
    logout_invalid_token = client.post(
        "/logout",
        data={"_csrf_token": "invalid-csrf-token"},
        follow_redirects=False,
    )
    logout_valid = client.post(
        "/logout",
        data={"_csrf_token": logout_token},
        follow_redirects=False,
    )

    assert logout_missing_token.status_code == 403
    assert logout_invalid_token.status_code == 403
    assert logout_valid.status_code == 303
    assert client.get("/cabinet", follow_redirects=False).status_code == 303


def test_admin_csrf_token_is_session_bound_and_allows_state_change(client, test_settings):
    admin_one = _create_verified_user(test_settings, "csrf-admin-one@example.com", "csrfadminone", role="admin")
    admin_two = _create_verified_user(test_settings, "csrf-admin-two@example.com", "csrfadmintwo", role="admin")
    target = _create_verified_user(test_settings, "csrf-target@example.com", "csrftarget")

    _login_as(client, test_settings, admin_one.email)
    first_page = client.get("/admin/users")
    assert first_page.status_code == 200
    assert 'name="_csrf_token"' in first_page.text
    first_token = _extract_csrf_token(first_page.text)

    client.cookies.clear()
    _login_as(client, test_settings, admin_two.email)
    second_page = client.get("/admin/users")
    assert second_page.status_code == 200
    second_token = _extract_csrf_token(second_page.text)
    assert first_token != second_token

    reused_token_response = client.post(
        f"/admin/users/{target.id}/role",
        data={"role": "moderator", "_csrf_token": first_token},
        follow_redirects=False,
    )
    valid_token_response = client.post(
        f"/admin/users/{target.id}/role",
        data={"role": "moderator", "_csrf_token": second_token},
        follow_redirects=False,
    )

    assert reused_token_response.status_code == 403
    assert valid_token_response.status_code == 303

    with _connect(test_settings) as conn:
        row = conn.execute("SELECT role FROM users WHERE email = ?", (target.email,)).fetchone()
    assert row is not None
    assert row["role"] == "moderator"


def test_cabinet_account_block_create_requires_csrf_token(client, test_settings):
    admin = _create_verified_user(test_settings, "csrf-cabinet-admin@example.com", "csrfcabinetadmin", role="admin")
    owner = _create_verified_user(test_settings, "csrf-cabinet-owner@example.com", "csrfcabinetowner")

    _login_as(client, test_settings, admin.email)
    cabinet_page = client.get(f"/cabinet?account_blocks_user_email={owner.email}")
    assert cabinet_page.status_code == 200
    assert 'name="_csrf_token"' in cabinet_page.text
    csrf_token = _extract_csrf_token(cabinet_page.text)

    missing_token_response = client.post(
        f"/cabinet/account-blocks?account_blocks_user_email={owner.email}",
        data={
            "type": "server",
            "login": "cabinet-login",
            "password_secret": "cabinet-password",
            "duration_days": "30",
        },
        follow_redirects=False,
    )
    invalid_token_response = client.post(
        f"/cabinet/account-blocks?account_blocks_user_email={owner.email}",
        data={
            "type": "server",
            "login": "cabinet-login",
            "password_secret": "cabinet-password",
            "duration_days": "30",
            "_csrf_token": "invalid-csrf-token",
        },
        follow_redirects=False,
    )
    valid_response = client.post(
        f"/cabinet/account-blocks?account_blocks_user_email={owner.email}",
        data={
            "type": "server",
            "login": "cabinet-login",
            "password_secret": "cabinet-password",
            "duration_days": "30",
            "_csrf_token": csrf_token,
        },
        follow_redirects=False,
    )

    assert missing_token_response.status_code == 403
    assert invalid_token_response.status_code == 403
    assert valid_response.status_code == 303

    with _connect(test_settings) as conn:
        row = conn.execute("SELECT * FROM account_blocks WHERE login = ?", ("cabinet-login",)).fetchone()
    assert row is not None
    assert row["owner_user_id"] == owner.id
    assert row["password_secret"] != "cabinet-password"
    assert str(row["password_secret"]).startswith("enc:v1:")
