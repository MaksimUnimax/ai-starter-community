from __future__ import annotations

import re
import sqlite3

from app.auth.service import authenticate_user, create_session, register_user, verify_email
from app.shared.db import get_database_path
from app.tariffs.service import STARTER_TARIFF_CODE, seed_initial_catalog, update_tariff


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


def _create_verified_user(test_settings, *, email: str, login: str, role: str = "user") -> None:
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


def _login_as(client, test_settings, email: str):
    user = authenticate_user(email, "Secret123", settings=test_settings)
    session_token = create_session(user.id, settings=test_settings)
    client.cookies.set(test_settings.session_cookie_name, session_token)
    return user


def _user_row(test_settings, email: str):
    with _connect(test_settings) as conn:
        return conn.execute(
            """
            SELECT email, role, access_status, materials_access_granted_at
            FROM users
            WHERE email = ?
            """,
            (email,),
        ).fetchone()


def _set_homepage_tariff(test_settings, *, price_amount_minor: int = 699000, title: str = "Стартовый доступ") -> None:
    seed_initial_catalog(settings=test_settings)
    update_tariff(
        STARTER_TARIFF_CODE,
        title=title,
        price_amount_minor=price_amount_minor,
        settings=test_settings,
    )


def test_admin_users_page_shows_paid_access_state_and_controls(client, test_settings):
    _create_verified_user(test_settings, email="admin-access-admin@example.com", login="adminaccessadmin", role="admin")
    _create_verified_user(test_settings, email="admin-access-open@example.com", login="adminaccessopen")
    with _connect(test_settings) as conn:
        conn.execute(
            "UPDATE users SET materials_access_granted_at = CURRENT_TIMESTAMP, access_status = 'activated' WHERE email = ?",
            ("admin-access-open@example.com",),
        )
        conn.commit()

    _login_as(client, test_settings, "admin-access-admin@example.com")
    response = client.get("/admin/users")
    assert response.status_code == 200
    body = response.text
    assert "Доступ к материалам" in body
    assert "Доступ выдан" in body
    assert "Доступ не выдан" in body
    assert "Выдать доступ" in body
    assert "Отозвать доступ" in body
    assert "/materials-access/grant" in body
    assert "/materials-access/revoke" in body
    assert "materials_access_granted_at" not in body.lower()
    assert "password_hash" not in body.lower()
    assert "token_hash" not in body.lower()


def test_admin_can_grant_and_revoke_paid_access(client, test_settings):
    _set_homepage_tariff(test_settings)
    _create_verified_user(test_settings, email="admin-grant-admin@example.com", login="admingrantadmin", role="admin")
    _create_verified_user(test_settings, email="admin-grant-user@example.com", login="admingrantuser")

    _login_as(client, test_settings, "admin-grant-admin@example.com")
    target_user = authenticate_user("admin-grant-user@example.com", "Secret123", settings=test_settings)

    grant_response = client.post(f"/admin/users/{target_user.id}/materials-access/grant", follow_redirects=False)
    assert grant_response.status_code == 303

    granted = _user_row(test_settings, "admin-grant-user@example.com")
    assert granted is not None
    assert granted["materials_access_granted_at"] is not None
    assert granted["access_status"] == "activated"

    client.cookies.clear()
    _login_as(client, test_settings, "admin-grant-user@example.com")
    cabinet_response = client.get("/cabinet")
    assert cabinet_response.status_code == 200
    assert "Аккаунты" in cabinet_response.text
    assert "/static/cabinet-local-accounts.js" in cabinet_response.text

    materials_response = client.get("/materials")
    assert materials_response.status_code == 200
    assert "Работа с ИИ" in materials_response.text
    assert "Полный доступ к урокам откроется после оплаты тарифа." not in materials_response.text

    client.cookies.clear()
    _login_as(client, test_settings, "admin-grant-admin@example.com")
    revoke_response = client.post(f"/admin/users/{target_user.id}/materials-access/revoke", follow_redirects=False)
    assert revoke_response.status_code == 303

    revoked = _user_row(test_settings, "admin-grant-user@example.com")
    assert revoked is not None
    assert revoked["materials_access_granted_at"] is None
    assert revoked["access_status"] == "not_activated"

    client.cookies.clear()
    _login_as(client, test_settings, "admin-grant-user@example.com")
    locked_cabinet = client.get("/cabinet")
    assert locked_cabinet.status_code == 200
    assert "Личный кабинет будет доступен после оплаты" in locked_cabinet.text
    assert "/static/cabinet-local-accounts.js" not in locked_cabinet.text

    locked_materials = client.get("/materials")
    assert locked_materials.status_code == 200
    assert "Обучение" in locked_materials.text
    assert "Вступление к курсу" in locked_materials.text
    assert "Стартовый доступ" in locked_materials.text
    assert "Полный доступ к урокам откроется после оплаты тарифа." in locked_materials.text


def test_non_admins_cannot_grant_or_revoke_paid_access(client, test_settings):
    _create_verified_user(test_settings, email="admin-grant-target@example.com", login="admingranttarget")
    _create_verified_user(test_settings, email="admin-grant-admin2@example.com", login="admingrantadmin2", role="admin")

    target_user = authenticate_user("admin-grant-target@example.com", "Secret123", settings=test_settings)
    anonymous_response = client.post(f"/admin/users/{target_user.id}/materials-access/grant", follow_redirects=False)
    assert anonymous_response.status_code == 303
    assert anonymous_response.headers["location"] == "/login"

    _login_as(client, test_settings, "admin-grant-target@example.com")
    target_again = authenticate_user("admin-grant-admin2@example.com", "Secret123", settings=test_settings)
    user_grant_response = client.post(f"/admin/users/{target_again.id}/materials-access/grant")
    assert user_grant_response.status_code == 403
    user_revoke_response = client.post(f"/admin/users/{target_again.id}/materials-access/revoke")
    assert user_revoke_response.status_code == 403

    client.cookies.clear()
    _create_verified_user(test_settings, email="admin-grant-moderator@example.com", login="admingrantmoderator", role="moderator")
    _login_as(client, test_settings, "admin-grant-moderator@example.com")
    moderator_grant_response = client.post(f"/admin/users/{target_again.id}/materials-access/grant")
    assert moderator_grant_response.status_code == 403
    moderator_revoke_response = client.post(f"/admin/users/{target_again.id}/materials-access/revoke")
    assert moderator_revoke_response.status_code == 403


def test_access_status_alone_does_not_unlock_paid_access(client, test_settings):
    _set_homepage_tariff(test_settings)
    _create_verified_user(test_settings, email="admin-grant-status-only@example.com", login="admingrantstatus")
    with _connect(test_settings) as conn:
        conn.execute(
            "UPDATE users SET access_status = 'activated' WHERE email = ?",
            ("admin-grant-status-only@example.com",),
        )
        conn.commit()

    user = authenticate_user("admin-grant-status-only@example.com", "Secret123", settings=test_settings)
    assert user.access_status == "activated"
    assert user.materials_access_granted_at is None

    _login_as(client, test_settings, "admin-grant-status-only@example.com")
    cabinet_response = client.get("/cabinet")
    materials_response = client.get("/materials")
    assert cabinet_response.status_code == 200
    assert materials_response.status_code == 200
    assert "Личный кабинет будет доступен после оплаты" in cabinet_response.text
    assert "Обучение" in materials_response.text
