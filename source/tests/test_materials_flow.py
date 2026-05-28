from __future__ import annotations

import sqlite3

from app.auth.service import authenticate_user, create_session, register_user, verify_email
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


def _prepare_verified_user(
    client,
    test_settings,
    email: str,
    login: str,
    grant_access: bool = False,
    role: str = "user",
):
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
    if grant_access or role != "user":
        with _connect(test_settings) as conn:
            if role != "user":
                conn.execute("UPDATE users SET role = ? WHERE email = ?", (role, email))
            if grant_access:
                conn.execute(
                    "UPDATE users SET materials_access_granted_at = CURRENT_TIMESTAMP WHERE email = ?",
                    (email,),
                )
            conn.commit()


def _login_verified_user(client, test_settings, email: str):
    user = authenticate_user(email, "Secret123", settings=test_settings)
    session_token = create_session(user.id, settings=test_settings)
    client.cookies.set(test_settings.session_cookie_name, session_token)


def _prepare_and_login_verified_user(
    client,
    test_settings,
    email: str,
    login: str,
    grant_access: bool = False,
    role: str = "user",
):
    _prepare_verified_user(client, test_settings, email, login, grant_access=grant_access, role=role)
    _login_verified_user(client, test_settings, email)


def test_materials_redirects_unauthenticated_user(client):
    response = client.get("/materials", follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/login"


def test_materials_shows_locked_state_without_access(client, test_settings):
    _prepare_and_login_verified_user(client, test_settings, "materials-locked@example.com", "materialslocked")
    response = client.get("/materials")
    assert response.status_code == 200
    assert "/static/styles.css" in response.text
    assert "Личный кабинет" in response.text
    assert "Работа с ИИ" in response.text
    assert "Раздел «Работа с ИИ» готовится." in response.text
    assert "Здесь будут уроки, задания и материалы курса." in response.text
    assert "Что будет внутри" in response.text
    assert "Как это будет устроено" in response.text
    assert "Вернуться в личный кабинет" in response.text
    assert "/cabinet" in response.text
    assert "Раздел «Работа с ИИ» будет доступен после оплаты." not in response.text
    assert "После первой оплаты доступ к разделу останется навсегда." not in response.text
    assert "Быстрый старт" not in response.text
    assert "Как работать с AI-агентом" not in response.text
    assert "Команды для копирования" not in response.text
    assert "/admin" not in response.text
    assert "Payment" not in response.text
    assert "Locked" not in response.text


def test_materials_shows_placeholder_sections_when_access_granted(client, test_settings):
    _prepare_and_login_verified_user(client, test_settings, "materials-open@example.com", "materialsopen", grant_access=True)
    response = client.get("/materials")
    assert response.status_code == 200
    assert "Раздел «Работа с ИИ» готовится." in response.text
    assert "Здесь будут уроки, задания и материалы курса." in response.text
    assert "Что будет внутри" in response.text
    assert "Как это будет устроено" in response.text
    assert "/static/styles.css" in response.text
    assert "Личный кабинет" in response.text
    assert "Работа с ИИ" in response.text
    assert "Вернуться в личный кабинет" in response.text
    assert "/cabinet" in response.text
    assert "/admin" not in response.text
    assert "Payment" not in response.text
    assert "Content" not in response.text


def test_cabinet_contains_materials_link_and_locked_hint(client, test_settings):
    _prepare_and_login_verified_user(client, test_settings, "materials-cabinet@example.com", "materialscabinet")
    response = client.get("/cabinet")
    assert response.status_code == 200
    assert "/materials" in response.text
    assert "Перейти к материалам" in response.text
    assert "Логин: <strong>materialscabinet</strong>" in response.text
    assert "Email: materials-cabinet@example.com" in response.text
    assert "Здесь появятся курсы, уроки и материалы по работе с ИИ." in response.text
    assert "Сейчас раздел готовится." in response.text
    assert "Доступ к разделу «Работа с ИИ»" not in response.text
    assert "Раздел «Работа с ИИ» будет доступен после оплаты." not in response.text


def test_staff_roles_can_open_materials_without_payment_marker(client, test_settings):
    for role, email, login in [
        ("admin", "materials-admin@example.com", "materialsadmin"),
        ("moderator", "materials-moderator@example.com", "materialsmode"),
    ]:
        client.cookies.clear()
        _prepare_and_login_verified_user(client, test_settings, email, login, role=role)
        response = client.get("/materials")
        assert response.status_code == 200
        assert "Раздел «Работа с ИИ» готовится." in response.text
        assert "Здесь будут уроки, задания и материалы курса." in response.text
        assert "Быстрый старт" not in response.text
        assert "Раздел «Работа с ИИ» будет доступен после оплаты." not in response.text


def test_cabinet_access_labels_for_staff_and_paid_user(client, test_settings):
    _prepare_and_login_verified_user(client, test_settings, "cabinet-paid@example.com", "cabinetpaid", grant_access=True)
    paid_response = client.get("/cabinet")
    assert paid_response.status_code == 200
    assert "Логин: <strong>cabinetpaid</strong>" in paid_response.text
    assert "Email: cabinet-paid@example.com" in paid_response.text
    assert "Перейти к материалам" in paid_response.text

    client.cookies.clear()
    _prepare_and_login_verified_user(client, test_settings, "cabinet-moderator@example.com", "cabinetmod", role="moderator")
    moderator_response = client.get("/cabinet")
    assert moderator_response.status_code == 200
    assert "Логин: <strong>cabinetmod</strong>" in moderator_response.text
    assert "Email: cabinet-moderator@example.com" in moderator_response.text
    assert "Перейти к материалам" in moderator_response.text

    client.cookies.clear()
    _prepare_and_login_verified_user(client, test_settings, "cabinet-admin@example.com", "cabinetadm", role="admin")
    admin_response = client.get("/cabinet")
    assert admin_response.status_code == 200
    assert "Логин: <strong>cabinetadm</strong>" in admin_response.text
    assert "Email: cabinet-admin@example.com" in admin_response.text
    assert "Перейти к материалам" in admin_response.text


def test_materials_redirects_unauthenticated_user_is_unchanged(client):
    response = client.get("/materials", follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/login"


def test_materials_access_column_exists_after_schema_init(test_settings):
    initialize_database(get_database_path(test_settings))
    with _connect(test_settings) as conn:
        columns = {row["name"] for row in conn.execute("PRAGMA table_info(users)").fetchall()}
    assert "materials_access_granted_at" in columns
