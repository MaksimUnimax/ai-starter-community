from __future__ import annotations

import re
import sqlite3
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import pytest

from app.account_blocks.schemas import AccountBlockCreateInput
from app.account_blocks.service import (
    AccountBlockPermissionError,
    activate_account_block,
    create_account_block,
    get_account_block_public,
)
from app.auth.service import authenticate_user, register_user, verify_email
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


def test_activation_sets_timer_and_prepares_notification_without_sending_email(test_settings):
    admin = _create_verified_user(test_settings, "act-admin@example.com", "actadmin", role="admin")
    owner = _create_verified_user(test_settings, "act-owner@example.com", "actowner")
    block = create_account_block(
        actor=admin,
        data=AccountBlockCreateInput(
            owner_user_id=owner.id,
            type="mail",
            title="Mail access",
            login="mail-login",
            password_secret="mail-secret",
            email="mail@example.com",
        ),
        settings=test_settings,
    )
    fixed_now = datetime(2026, 6, 8, 12, 0, 0, tzinfo=timezone.utc)

    with patch("app.account_blocks.service.utc_now", return_value=fixed_now):
        result = activate_account_block(actor=admin, block_id=block.id, settings=test_settings)

    assert result.block.status == "active"
    assert result.block.is_active is True
    assert result.block.is_expired is False
    assert result.block.remaining_days == 60
    assert result.block.activated_at == fixed_now.isoformat()
    assert result.block.expires_at == (fixed_now + timedelta(days=60)).isoformat()
    assert result.block.activated_by_user_id == admin.id
    assert result.notification is not None
    assert result.notification.recipient_email == owner.email
    assert result.notification.subject == "Аккаунт в кабинете активирован"
    assert "Mail access" in result.notification.body_text
    assert "Почта" in result.notification.body_text
    assert result.notification.expires_at == result.block.expires_at

    with _connect(test_settings) as conn:
        activation_logs = conn.execute(
            "SELECT * FROM email_outbox WHERE template_key = ?",
            ("account_block_activation",),
        ).fetchall()
    assert activation_logs == []


def test_reactivation_resets_timer_and_expiry_computes_on_read(test_settings):
    admin = _create_verified_user(test_settings, "react-admin@example.com", "reactadmin", role="admin")
    owner = _create_verified_user(test_settings, "react-owner@example.com", "reactowner")
    block = create_account_block(
        actor=admin,
        data=AccountBlockCreateInput(
            owner_user_id=owner.id,
            type="server",
            title="Server access",
            login="server-login",
            password_secret="server-secret",
        ),
        settings=test_settings,
    )

    first_now = datetime(2026, 6, 8, 12, 0, 0, tzinfo=timezone.utc)
    second_now = datetime(2026, 6, 18, 9, 30, 0, tzinfo=timezone.utc)
    expired_now = second_now + timedelta(days=61)

    with patch("app.account_blocks.service.utc_now", return_value=first_now):
        first_activation = activate_account_block(actor=admin, block_id=block.id, settings=test_settings)

    with patch("app.account_blocks.service.utc_now", return_value=second_now):
        second_activation = activate_account_block(actor=admin, block_id=block.id, settings=test_settings)

    assert second_activation.block.activated_at == second_now.isoformat()
    assert second_activation.block.expires_at == (second_now + timedelta(days=60)).isoformat()
    assert second_activation.block.expires_at != first_activation.block.expires_at

    with patch("app.account_blocks.service.utc_now", return_value=expired_now):
        expired_view = get_account_block_public(actor=owner, block_id=block.id, settings=test_settings)

    assert expired_view.status == "expired"
    assert expired_view.is_active is False
    assert expired_view.is_expired is True
    assert expired_view.remaining_days == 0


def test_user_cannot_activate_account_blocks(test_settings):
    admin = _create_verified_user(test_settings, "deny-admin@example.com", "denyadmin", role="admin")
    owner = _create_verified_user(test_settings, "deny-owner@example.com", "denyowner")
    block = create_account_block(
        actor=admin,
        data=AccountBlockCreateInput(
            owner_user_id=owner.id,
            type="chatgpt",
            title="Denied",
            login="deny-login",
            password_secret="deny-secret",
        ),
        settings=test_settings,
    )
    with pytest.raises(AccountBlockPermissionError):
        activate_account_block(actor=owner, block_id=block.id, settings=test_settings)
