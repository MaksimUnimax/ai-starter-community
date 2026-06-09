from __future__ import annotations

import re
import sqlite3
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode
from unittest.mock import patch

from app.account_blocks.schemas import AccountBlockCreateInput
from app.account_blocks.service import create_account_block
from app.auth.service import authenticate_user, create_session, register_user, verify_email
from app.paid_options.schemas import PaidOptionCreateInput
from app.paid_options.service import create_paid_option


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


def test_admin_can_search_user_by_email_and_manage_selected_user_blocks(client, test_settings):
    admin = _create_verified_user(test_settings, "admin-ui-admin@example.com", "adminuiadmin", role="admin")
    owner = _create_verified_user(test_settings, "admin-ui-owner@example.com", "adminuiowner")
    paid_option = create_paid_option(
        data=PaidOptionCreateInput(
            code="admin_ui_monthly",
            title="Admin UI Monthly",
            description="Thirty day test option",
            price_amount_minor=1000,
            currency="RUB",
            default_duration_days=30,
            status="active",
            is_renewable=True,
            sort_order=1,
        ),
        settings=test_settings,
    )
    seed_block = create_account_block(
        actor=admin,
        data=AccountBlockCreateInput(
            owner_user_id=owner.id,
            type="mail",
            login="seed-login",
            password_secret="seed-secret",
            duration_days=15,
        ),
        settings=test_settings,
    )

    _login_as(client, test_settings, admin.email)

    response = client.get(f"/admin/account-blocks?{urlencode({'account_blocks_user_email': owner.email})}")
    assert response.status_code == 200
    body = response.text
    assert "Блоки аккаунтов" in body
    assert "Email пользователя" in body
    assert owner.email in body
    assert "seed-login" in body
    assert "Платная опция" in body
    assert 'name="account_blocks_user_email"' in body
    assert 'name="paid_option_code"' in body
    assert 'data-account-block-paid-option-select' in body
    assert 'data-account-block-duration-input' in body
    assert f'action="/admin/account-blocks?{urlencode({"account_blocks_user_email": owner.email})}' in body
    assert "Добавить блок" in body
    assert "Неактивно" in body or "Не активирован" in body
    assert "Продлить активацию" not in body

    create_response = client.post(
        f"/admin/account-blocks?{urlencode({'account_blocks_user_email': owner.email})}",
        data={
            "type": "server",
            "paid_option_code": paid_option.code,
            "duration_days": "",
            "login": "admin-ui-login",
            "password_secret": "admin-ui-password",
        },
        follow_redirects=False,
    )
    assert create_response.status_code == 303
    assert create_response.headers["location"] == f"/admin/account-blocks?{urlencode({'account_blocks_notice': 'created', 'account_blocks_user_email': owner.email})}"

    with _connect(test_settings) as conn:
        row = conn.execute("SELECT * FROM account_blocks WHERE login = ?", ("admin-ui-login",)).fetchone()
    assert row is not None
    block_id = int(row["id"])
    assert row["title"] == "Сервер"
    assert int(row["owner_user_id"]) == owner.id
    assert int(row["duration_days"]) == 30

    activation_now = datetime(2026, 6, 8, 12, 0, 0, tzinfo=timezone.utc)
    with patch("app.account_blocks.service.utc_now", return_value=activation_now):
        activate_response = client.post(
            f"/admin/account-blocks/{block_id}/activate?{urlencode({'account_blocks_user_email': owner.email})}",
            data={"duration_days": "45"},
            follow_redirects=False,
        )
    assert activate_response.status_code == 303
    assert activate_response.headers["location"] == f"/admin/account-blocks?{urlencode({'account_blocks_notice': 'activated_email_sent', 'account_blocks_user_email': owner.email})}"

    with _connect(test_settings) as conn:
        activated_row = conn.execute("SELECT * FROM account_blocks WHERE id = ?", (block_id,)).fetchone()
    assert activated_row is not None
    assert activated_row["expires_at"] == (activation_now + timedelta(days=45)).isoformat()

    with _connect(test_settings) as conn:
        email_row = conn.execute(
            """
            SELECT *
            FROM email_outbox
            WHERE recipient_email = ? AND template_key = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (owner.email, "account_block_activation"),
        ).fetchone()
    assert email_row is not None
    assert email_row["subject"] == "Активирована опция OpenScript"
    assert "admin-ui-login" not in email_row["body_text"]
    assert "admin-ui-password" not in email_row["body_text"]

    with patch("app.account_blocks.service.utc_now", return_value=activation_now):
        active_page = client.get(f"/admin/account-blocks?{urlencode({'account_blocks_user_email': owner.email})}")
    assert active_page.status_code == 200
    active_body = active_page.text
    assert "Осталось 45 дней" in active_body
    assert "Продлить активацию" in active_body

    renewal_now = activation_now + timedelta(days=1)
    with patch("app.account_blocks.service.utc_now", return_value=renewal_now):
        renew_response = client.post(
            f"/admin/account-blocks/{block_id}/renew?{urlencode({'account_blocks_user_email': owner.email})}",
            data={"duration_days": "30"},
            follow_redirects=False,
        )
    assert renew_response.status_code == 303
    assert renew_response.headers["location"] == f"/admin/account-blocks?{urlencode({'account_blocks_notice': 'renewed', 'account_blocks_user_email': owner.email})}"

    with _connect(test_settings) as conn:
        renewed_row = conn.execute("SELECT * FROM account_blocks WHERE id = ?", (block_id,)).fetchone()
    assert renewed_row is not None
    assert renewed_row["expires_at"] == (activation_now + timedelta(days=75)).isoformat()

    with patch("app.account_blocks.service.utc_now", return_value=renewal_now):
        renewed_page = client.get(f"/admin/account-blocks?{urlencode({'account_blocks_user_email': owner.email})}")
    assert renewed_page.status_code == 200
    renewed_body = renewed_page.text
    assert "Осталось 74 дня" in renewed_body
    assert "Продлить активацию" in renewed_body
