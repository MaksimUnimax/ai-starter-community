from __future__ import annotations

import importlib

import pytest
from fastapi.testclient import TestClient

from app.core.config import Settings, get_settings


@pytest.fixture()
def test_settings(tmp_path, monkeypatch) -> Settings:
    db_path = tmp_path / "ai_starter_community.sqlite3"
    monkeypatch.setenv("APP_NAME", "AI Starter Community")
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("APP_HOST", "127.0.0.1")
    monkeypatch.setenv("APP_PORT", "8089")
    monkeypatch.setenv("BASE_URL", "http://127.0.0.1:8089")
    monkeypatch.setenv("DATABASE_PATH", str(db_path))
    monkeypatch.setenv("SESSION_COOKIE_NAME", "ai_starter_community_session_test")
    monkeypatch.setenv("SESSION_EXPIRY_HOURS", "168")
    monkeypatch.setenv("SESSION_COOKIE_SECURE", "false")
    monkeypatch.setenv("EMAIL_MODE", "outbox")
    monkeypatch.setenv("EMAIL_FROM_ADDRESS", "no-reply@example.com")
    monkeypatch.setenv("EMAIL_FROM_NAME", "AI Starter Community")
    monkeypatch.setenv("SMTP_HOST", "smtp.example.com")
    monkeypatch.setenv("SMTP_PORT", "587")
    monkeypatch.setenv("SMTP_USE_TLS", "false")
    monkeypatch.setenv("SMTP_USE_STARTTLS", "true")
    monkeypatch.setenv("SMTP_TIMEOUT_SECONDS", "10")
    monkeypatch.setenv("EMAIL_VERIFICATION_TOKEN_EXPIRY_HOURS", "24")
    monkeypatch.setenv("PASSWORD_RESET_TOKEN_EXPIRY_MINUTES", "30")
    get_settings.cache_clear()
    return Settings(
        app_name="AI Starter Community",
        app_env="test",
        app_host="127.0.0.1",
        app_port=8089,
        base_url="http://127.0.0.1:8089",
        database_path=str(db_path),
        session_cookie_name="ai_starter_community_session_test",
        session_expiry_hours=168,
        session_cookie_secure=False,
        email_mode="outbox",
        email_from_address="no-reply@example.com",
        email_from_name="AI Starter Community",
        smtp_host="smtp.example.com",
        smtp_port=587,
        smtp_username=None,
        smtp_password=None,
        smtp_use_tls=False,
        smtp_use_starttls=True,
        smtp_timeout_seconds=10,
        email_verification_token_expiry_hours=24,
        password_reset_token_expiry_minutes=30,
    )


@pytest.fixture()
def app(test_settings):
    import app.main as app_main

    importlib.reload(app_main)
    return app_main.app


@pytest.fixture()
def client(app):
    return TestClient(app)
