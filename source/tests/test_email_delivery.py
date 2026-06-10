from __future__ import annotations

import re
import sqlite3
from unittest.mock import MagicMock, patch

import pytest

from app.auth.service import (
    AuthError,
    create_password_reset_request,
    register_user,
    resend_verification_request,
    verify_email,
)
from app.core.config import Settings
from app.notifications.email_service import (
    EmailConfigError,
    EmailDeliveryError,
    send_email_verification,
    send_password_reset,
)
from app.shared.db import get_database_path


def _connect(settings: Settings):
    return sqlite3.connect(str(get_database_path(settings)))


def _fetch_one(settings: Settings, sql: str, params: tuple = ()):
    with _connect(settings) as conn:
        conn.row_factory = sqlite3.Row
        return conn.execute(sql, params).fetchone()


def _smtp_settings(**overrides) -> Settings:
    base = {
        "app_name": "AI Starter Community",
        "app_env": "test",
        "app_host": "127.0.0.1",
        "app_port": 8089,
        "base_url": "http://127.0.0.1:8089",
        "database_path": overrides.pop("database_path"),
        "session_cookie_name": "ai_starter_community_session_test",
        "session_expiry_hours": 168,
        "session_cookie_secure": False,
        "email_mode": "smtp",
        "email_from_address": "no-reply@example.com",
        "email_from_name": "AI Starter Community",
        "smtp_host": "smtp.example.com",
        "smtp_port": 587,
        "smtp_username": None,
        "smtp_password": None,
        "smtp_use_tls": False,
        "smtp_use_starttls": True,
        "smtp_timeout_seconds": 10,
        "email_resend_from_address": None,
        "email_resend_from_name": None,
        "email_resend_smtp_host": None,
        "email_resend_smtp_port": None,
        "email_resend_smtp_username": None,
        "email_resend_smtp_password": None,
        "email_resend_smtp_use_tls": False,
        "email_resend_smtp_use_starttls": True,
        "email_resend_smtp_timeout_seconds": 10,
        "email_verification_token_expiry_hours": 24,
        "password_reset_token_expiry_minutes": 30,
    }
    base.update(overrides)
    return Settings(**base)


def test_smtp_config_missing_required_values_fails_safely(tmp_path):
    settings = _smtp_settings(
        database_path=str(tmp_path / "smtp-missing.sqlite3"),
        email_from_address=None,
    )
    with pytest.raises(EmailConfigError, match="EMAIL_FROM_ADDRESS"):
        send_email_verification("user@example.com", "http://127.0.0.1:8089/verify-email/token", settings=settings)

    settings = _smtp_settings(
        database_path=str(tmp_path / "smtp-missing-host.sqlite3"),
        smtp_host=None,
    )
    with pytest.raises(EmailConfigError, match="SMTP_HOST"):
        send_email_verification("user@example.com", "http://127.0.0.1:8089/verify-email/token", settings=settings)

    settings = _smtp_settings(
        database_path=str(tmp_path / "smtp-missing-port.sqlite3"),
        smtp_port=None,
    )
    with pytest.raises(EmailConfigError, match="SMTP_PORT"):
        send_email_verification("user@example.com", "http://127.0.0.1:8089/verify-email/token", settings=settings)


def test_smtp_config_rejects_partial_credentials_and_conflicting_tls(tmp_path):
    partial_credentials = _smtp_settings(
        database_path=str(tmp_path / "smtp-partial.sqlite3"),
        smtp_username="user",
        smtp_password=None,
    )
    with pytest.raises(EmailConfigError, match="SMTP_USERNAME/SMTP_PASSWORD"):
        send_password_reset("user@example.com", "http://127.0.0.1:8089/reset-password/token", settings=partial_credentials)

    partial_credentials = _smtp_settings(
        database_path=str(tmp_path / "smtp-partial-password.sqlite3"),
        smtp_username=None,
        smtp_password="pass",
    )
    with pytest.raises(EmailConfigError, match="SMTP_USERNAME/SMTP_PASSWORD"):
        send_password_reset("user@example.com", "http://127.0.0.1:8089/reset-password/token", settings=partial_credentials)

    conflicting_tls = _smtp_settings(
        database_path=str(tmp_path / "smtp-conflict.sqlite3"),
        smtp_use_tls=True,
        smtp_use_starttls=True,
    )
    with pytest.raises(EmailConfigError, match="cannot both be true"):
        send_password_reset("user@example.com", "http://127.0.0.1:8089/reset-password/token", settings=conflicting_tls)


def test_outbox_mode_preserves_current_behavior(test_settings):
    user = register_user(
        email="outbox@example.com",
        login="outboxuser",
        password="Secret123",
        repeat_password="Secret123",
        settings=test_settings,
    )
    row = _fetch_one(
        test_settings,
        "SELECT * FROM email_outbox WHERE recipient_email = ? ORDER BY id DESC LIMIT 1",
        (user.email,),
    )
    assert row["status"] == "queued"
    assert "/verify-email/" in row["body_text"]


def test_outbox_confirmation_resend_uses_secondary_when_configured(tmp_path):
    settings = _smtp_settings(
        database_path=str(tmp_path / "outbox-secondary.sqlite3"),
        email_mode="outbox",
        email_resend_from_address="no-reply@openscript.ru",
        email_resend_from_name="OpenScript",
        email_resend_smtp_host="smtp.mailtrap.example",
        email_resend_smtp_port=2525,
        email_resend_smtp_username="mailtrap-user",
        email_resend_smtp_password="mailtrap-pass",
        email_resend_smtp_use_starttls=True,
    )
    user = register_user(
        email="secondary@example.com",
        login="secondaryuser",
        password="Secret123",
        repeat_password="Secret123",
        settings=settings,
    )
    initial_row = _fetch_one(
        settings,
        "SELECT * FROM email_outbox WHERE recipient_email = ? AND template_key = ? ORDER BY id ASC LIMIT 1",
        (user.email, "email_verification"),
    )
    assert initial_row["purpose"] == "confirmation_initial"
    assert initial_row["smtp_channel"] == "primary"
    assert initial_row["from_address"] == "no-reply@example.com"
    assert initial_row["provider_configured"] == 1
    assert initial_row["fallback_reason"] is None

    assert resend_verification_request(user.email, settings=settings) is True
    resend_row = _fetch_one(
        settings,
        "SELECT * FROM email_outbox WHERE recipient_email = ? AND template_key = ? ORDER BY id DESC LIMIT 1",
        (user.email, "email_verification"),
    )
    assert resend_row["purpose"] == "confirmation_resend"
    assert resend_row["smtp_channel"] == "secondary_resend"
    assert resend_row["from_address"] == "no-reply@openscript.ru"
    assert resend_row["provider_configured"] == 1
    assert resend_row["fallback_reason"] is None


def test_confirmation_resend_falls_back_to_primary_without_secondary(tmp_path):
    settings = _smtp_settings(
        database_path=str(tmp_path / "outbox-fallback.sqlite3"),
        email_mode="outbox",
    )
    user = register_user(
        email="fallback@example.com",
        login="fallbackuser",
        password="Secret123",
        repeat_password="Secret123",
        settings=settings,
    )
    assert resend_verification_request(user.email, settings=settings) is True
    resend_row = _fetch_one(
        settings,
        "SELECT * FROM email_outbox WHERE recipient_email = ? AND template_key = ? ORDER BY id DESC LIMIT 1",
        (user.email, "email_verification"),
    )
    assert resend_row["purpose"] == "confirmation_resend"
    assert resend_row["smtp_channel"] == "primary"
    assert resend_row["from_address"] == "no-reply@example.com"
    assert resend_row["provider_configured"] == 1
    assert resend_row["fallback_reason"] == "secondary_smtp_not_configured_falling_back_to_primary"


def test_smtp_verification_send_uses_starttls_and_no_login_when_credentials_missing(tmp_path):
    settings = _smtp_settings(database_path=str(tmp_path / "smtp-success.sqlite3"))
    with patch("app.notifications.smtp_adapter.smtplib.SMTP") as smtp_cls:
        smtp_client = MagicMock()
        smtp_cls.return_value.__enter__.return_value = smtp_client

        email_id = send_email_verification(
            "user@example.com",
            "http://127.0.0.1:8089/verify-email/token",
            settings=settings,
        )

    assert email_id > 0
    smtp_client.starttls.assert_called_once()
    smtp_client.login.assert_not_called()
    smtp_client.send_message.assert_called_once()

    row = _fetch_one(settings, "SELECT * FROM email_outbox ORDER BY id DESC LIMIT 1")
    assert row["status"] == "sent"
    assert row["body_text"] == "[redacted: sent via smtp]"
    assert "/verify-email/" not in row["body_text"]
    assert row["purpose"] == "confirmation_initial"
    assert row["smtp_channel"] == "primary"
    assert row["from_address"] == "no-reply@example.com"
    assert row["provider_configured"] == 1


def test_smtp_reset_send_uses_login_when_credentials_present(tmp_path):
    settings = _smtp_settings(
        database_path=str(tmp_path / "smtp-login.sqlite3"),
        smtp_username="smtp-user",
        smtp_password="smtp-pass",
        smtp_use_starttls=True,
    )
    with patch("app.notifications.smtp_adapter.smtplib.SMTP") as smtp_cls:
        smtp_client = MagicMock()
        smtp_cls.return_value.__enter__.return_value = smtp_client

        email_id = send_password_reset(
            "user@example.com",
            "http://127.0.0.1:8089/reset-password/token",
            settings=settings,
        )

    assert email_id > 0
    smtp_client.starttls.assert_called_once()
    smtp_client.login.assert_called_once_with("smtp-user", "smtp-pass")
    smtp_client.send_message.assert_called_once()

    row = _fetch_one(settings, "SELECT * FROM email_outbox ORDER BY id DESC LIMIT 1")
    assert row["status"] == "sent"
    assert row["body_text"] == "[redacted: sent via smtp]"
    assert row["purpose"] == "password_reset"
    assert row["smtp_channel"] == "primary"
    assert row["provider_configured"] == 1


def test_smtp_ssl_branch_uses_smpt_ssl(tmp_path):
    settings = _smtp_settings(
        database_path=str(tmp_path / "smtp-ssl.sqlite3"),
        smtp_use_tls=True,
        smtp_use_starttls=False,
    )
    with patch("app.notifications.smtp_adapter.smtplib.SMTP_SSL") as smtp_ssl_cls:
        smtp_client = MagicMock()
        smtp_ssl_cls.return_value.__enter__.return_value = smtp_client

        send_email_verification(
            "user@example.com",
            "http://127.0.0.1:8089/verify-email/token",
            settings=settings,
        )

    smtp_ssl_cls.assert_called_once()
    smtp_client.starttls.assert_not_called()
    smtp_client.send_message.assert_called_once()


def test_smtp_resend_uses_secondary_provider_and_redacts_body(tmp_path):
    settings = _smtp_settings(
        database_path=str(tmp_path / "smtp-secondary.sqlite3"),
        email_mode="smtp",
        email_resend_from_address="no-reply@openscript.ru",
        email_resend_from_name="OpenScript",
        email_resend_smtp_host="smtp.mailtrap.example",
        email_resend_smtp_port=2525,
        email_resend_smtp_username="mailtrap-user",
        email_resend_smtp_password="mailtrap-pass",
        email_resend_smtp_use_starttls=True,
    )
    with patch("app.notifications.smtp_adapter.smtplib.SMTP") as smtp_cls:
        smtp_client = MagicMock()
        smtp_cls.return_value.__enter__.return_value = smtp_client

        email_id = send_email_verification(
            "user@example.com",
            "http://127.0.0.1:8089/verify-email/token",
            settings=settings,
            purpose="confirmation_resend",
        )

    assert email_id > 0
    smtp_client.starttls.assert_called_once()
    smtp_client.login.assert_called_once_with("mailtrap-user", "mailtrap-pass")
    smtp_client.send_message.assert_called_once()

    row = _fetch_one(settings, "SELECT * FROM email_outbox ORDER BY id DESC LIMIT 1")
    assert row["status"] == "sent"
    assert row["body_text"] == "[redacted: sent via smtp]"
    assert row["purpose"] == "confirmation_resend"
    assert row["smtp_channel"] == "secondary_resend"
    assert row["from_address"] == "no-reply@openscript.ru"
    assert row["provider_configured"] == 1
    assert row["fallback_reason"] is None
    assert "/verify-email/" not in row["body_text"]


def test_smtp_delivery_failure_marks_audit_failed(tmp_path):
    settings = _smtp_settings(database_path=str(tmp_path / "smtp-failure.sqlite3"))
    with patch("app.notifications.smtp_adapter.smtplib.SMTP") as smtp_cls:
        smtp_client = MagicMock()
        smtp_client.send_message.side_effect = RuntimeError("provider boom")
        smtp_cls.return_value.__enter__.return_value = smtp_client

        with pytest.raises(EmailDeliveryError, match="SMTP delivery failed"):
            send_password_reset(
                "user@example.com",
                "http://127.0.0.1:8089/reset-password/token",
                settings=settings,
            )

    row = _fetch_one(settings, "SELECT * FROM email_outbox ORDER BY id DESC LIMIT 1")
    assert row["status"] == "failed"
    assert row["body_text"] == "[redacted: sent via smtp]"
    assert row["error"] is not None
    assert "token" not in row["error"].lower()


def test_auth_flow_wraps_email_delivery_failures_safely(tmp_path):
    db_path = str(tmp_path / "smtp-auth.sqlite3")
    registration_settings = _smtp_settings(
        database_path=db_path,
        email_mode="outbox",
    )
    verified_user = register_user(
        email="auth2@example.com",
        login="authuser2",
        password="Secret123",
        repeat_password="Secret123",
        settings=registration_settings,
    )
    registration_row = _fetch_one(
        registration_settings,
        "SELECT * FROM email_outbox WHERE recipient_email = ? ORDER BY id DESC LIMIT 1",
        (verified_user.email,),
    )
    verify_email(
        re.search(r"/verify-email/([A-Za-z0-9_-]+)", registration_row["body_text"]).group(1),
        settings=registration_settings,
    )

    settings = _smtp_settings(database_path=db_path)
    with patch("app.notifications.smtp_adapter.smtplib.SMTP") as smtp_cls:
        smtp_client = MagicMock()
        smtp_client.send_message.side_effect = RuntimeError("provider boom")
        smtp_cls.return_value.__enter__.return_value = smtp_client

        with pytest.raises(AuthError, match="Не удалось отправить письмо"):
            register_user(
                email="auth@example.com",
                login="authuser",
                password="Secret123",
                repeat_password="Secret123",
                settings=settings,
            )

    with patch("app.notifications.smtp_adapter.smtplib.SMTP") as smtp_cls:
        smtp_client = MagicMock()
        smtp_client.send_message.side_effect = RuntimeError("provider boom")
        smtp_cls.return_value.__enter__.return_value = smtp_client

        assert create_password_reset_request("auth2@example.com", settings=settings) is False
