from __future__ import annotations

import sqlite3

from app.auth.service import register_user, verify_email
from app.shared.db import get_database_path, initialize_database


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


def _prepare_verified_user(client, test_settings, email: str, login: str, grant_access: bool = False):
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
    if grant_access:
        with _connect(test_settings) as conn:
            conn.execute(
                "UPDATE users SET materials_access_granted_at = CURRENT_TIMESTAMP WHERE email = ?",
                (email,),
            )
            conn.commit()
    login_response = client.post(
        "/login",
        data={"email_or_login": email, "password": "Secret123"},
        follow_redirects=False,
    )
    assert login_response.status_code == 303


def test_materials_redirects_unauthenticated_user(client):
    response = client.get("/materials", follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/login"


def test_materials_shows_locked_state_without_access(client, test_settings):
    _prepare_verified_user(client, test_settings, "materials-locked@example.com", "materialslocked")
    response = client.get("/materials")
    assert response.status_code == 200
    assert "Материалы будут доступны после оплаты" in response.text
    assert "После первой оплаты доступ к материалам останется навсегда." in response.text
    assert "Быстрый старт" not in response.text


def test_materials_shows_placeholder_sections_when_access_granted(client, test_settings):
    _prepare_verified_user(client, test_settings, "materials-open@example.com", "materialsopen", grant_access=True)
    response = client.get("/materials")
    assert response.status_code == 200
    assert "Материалы будут доступны после оплаты" not in response.text
    assert "Быстрый старт" in response.text
    assert "Как работать с AI-агентом" in response.text
    assert "Команды для копирования" in response.text
    assert "Частые ошибки" in response.text
    assert "Видеоинструкции" in response.text
    assert "Ссылки на чаты" in response.text


def test_cabinet_contains_materials_link_and_locked_hint(client, test_settings):
    _prepare_verified_user(client, test_settings, "materials-cabinet@example.com", "materialscabinet")
    response = client.get("/cabinet")
    assert response.status_code == 200
    assert "/materials" in response.text
    assert "Материалы будут доступны после оплаты" in response.text


def test_materials_access_column_exists_after_schema_init(test_settings):
    initialize_database(get_database_path(test_settings))
    with _connect(test_settings) as conn:
        columns = {row["name"] for row in conn.execute("PRAGMA table_info(users)").fetchall()}
    assert "materials_access_granted_at" in columns
