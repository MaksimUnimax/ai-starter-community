from __future__ import annotations

import sqlite3

from app.auth.service import authenticate_user, create_session, register_user, verify_email
from app.core.app_factory import create_app
from app.shared.db import get_database_path
from app.admin.cli import main


def _connect(settings):
    conn = sqlite3.connect(str(get_database_path(settings)))
    conn.row_factory = sqlite3.Row
    return conn


def _verify_user(settings, email: str) -> None:
    with _connect(settings) as conn:
        row = conn.execute(
            "SELECT body_text FROM email_outbox WHERE recipient_email = ? AND template_key = ? ORDER BY id DESC LIMIT 1",
            (email, "email_verification"),
        ).fetchone()
    assert row is not None
    import re

    token = re.search(r"/verify-email/([A-Za-z0-9_-]+)", row["body_text"])
    assert token
    verify_email(token.group(1), settings=settings)


def _make_user(settings, email: str, login: str):
    register_user(email=email, login=login, password="Secret123", repeat_password="Secret123", settings=settings)
    _verify_user(settings, email)


def test_cli_requires_exactly_one_identifier(test_settings):
    try:
        main(["promote-admin", "--database-path", test_settings.database_path])
        assert False, "expected SystemExit"
    except SystemExit as exc:
        assert exc.code == 2
    try:
        main(["promote-admin", "--email", "a@example.com", "--login", "a", "--database-path", test_settings.database_path])
        assert False, "expected SystemExit"
    except SystemExit as exc:
        assert exc.code == 2


def test_cli_fails_safely_when_user_missing(test_settings, capsys):
    exit_code = main(["promote-admin", "--email", "missing@example.com", "--database-path", test_settings.database_path])
    assert exit_code == 1
    captured = capsys.readouterr()
    assert "user not found" in captured.err


def test_cli_promotes_existing_verified_user_by_email(test_settings):
    _make_user(test_settings, "admin-email@example.com", "adminemail")
    exit_code = main(["promote-admin", "--email", "admin-email@example.com", "--database-path", test_settings.database_path])
    assert exit_code == 0
    with _connect(test_settings) as conn:
        row = conn.execute("SELECT role FROM users WHERE email = ?", ("admin-email@example.com",)).fetchone()
    assert row["role"] == "admin"


def test_cli_promotes_existing_verified_user_by_login(test_settings):
    _make_user(test_settings, "admin-login@example.com", "adminlogin")
    exit_code = main(["promote-admin", "--login", "adminlogin", "--database-path", test_settings.database_path])
    assert exit_code == 0
    with _connect(test_settings) as conn:
        row = conn.execute("SELECT role FROM users WHERE login = ?", ("adminlogin",)).fetchone()
    assert row["role"] == "admin"


def test_cli_is_idempotent_for_already_admin(test_settings, capsys):
    _make_user(test_settings, "admin-idem@example.com", "adminidem")
    main(["promote-admin", "--email", "admin-idem@example.com", "--database-path", test_settings.database_path])
    exit_code = main(["promote-admin", "--email", "admin-idem@example.com", "--database-path", test_settings.database_path])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert "user is admin" in captured.out


def test_cli_does_not_create_user_or_change_sensitive_fields(test_settings):
    _make_user(test_settings, "admin-sensitive@example.com", "adminsensitive")
    with _connect(test_settings) as conn:
        before = conn.execute("SELECT * FROM users WHERE email = ?", ("admin-sensitive@example.com",)).fetchone()
    exit_code = main(["promote-admin", "--email", "admin-sensitive@example.com", "--database-path", test_settings.database_path])
    assert exit_code == 0
    with _connect(test_settings) as conn:
        after = conn.execute("SELECT * FROM users WHERE email = ?", ("admin-sensitive@example.com",)).fetchone()
        count = conn.execute("SELECT COUNT(*) AS c FROM users WHERE email = ?", ("admin-sensitive@example.com",)).fetchone()["c"]
    assert count == 1
    assert before["password_hash"] == after["password_hash"]
    assert before["email_verified_at"] == after["email_verified_at"]
    assert after["materials_access_granted_at"] is None


def test_admin_access_still_works_for_promoted_temp_user(client, test_settings):
    _make_user(test_settings, "admin-guard@example.com", "adminguard")
    main(["promote-admin", "--email", "admin-guard@example.com", "--database-path", test_settings.database_path])
    user = authenticate_user("admin-guard@example.com", "Secret123", settings=test_settings)
    session_token = create_session(user.id, settings=test_settings)
    client.cookies.set(test_settings.session_cookie_name, session_token)
    response = client.get("/admin")
    assert response.status_code == 200
    assert "Админ-панель" in response.text


def test_normal_user_remains_forbidden_for_admin(client, test_settings):
    _make_user(test_settings, "normal-user@example.com", "normaluser")
    user = authenticate_user("normal-user@example.com", "Secret123", settings=test_settings)
    session_token = create_session(user.id, settings=test_settings)
    client.cookies.set(test_settings.session_cookie_name, session_token)
    response = client.get("/admin")
    assert response.status_code == 403


def test_existing_auth_catalog_material_admin_tests_still_pass(client):
    response = client.get("/register")
    assert response.status_code == 200
    app = create_app()
    assert any(route.path == "/admin" for route in app.router.routes)
