"""Environment-driven application settings."""

from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


def _env_int(name: str, default: int) -> int:
    raw_value = os.getenv(name)
    if raw_value is None or raw_value == "":
        return default
    try:
        return int(raw_value)
    except ValueError:
        return default


def _env_bool(name: str, default: bool) -> bool:
    raw_value = os.getenv(name)
    if raw_value is None or raw_value == "":
        return default
    return raw_value.strip().lower() in {"1", "true", "yes", "on"}


def _env_optional_str(name: str) -> str | None:
    raw_value = os.getenv(name)
    if raw_value is None:
        return None
    value = raw_value.strip()
    return value or None


def _env_optional_int(name: str) -> int | None:
    raw_value = os.getenv(name)
    if raw_value is None or raw_value == "":
        return None
    return int(raw_value)


@dataclass(frozen=True)
class Settings:
    app_name: str = "AI Starter Community"
    app_env: str = "development"
    app_host: str = "127.0.0.1"
    app_port: int = 8089
    base_url: str = "http://127.0.0.1:8089"
    database_path: str = "/opt/ai-starter-community/state/ai_starter_community.sqlite3"
    session_cookie_name: str = "ai_starter_community_session"
    session_expiry_hours: int = 168
    session_cookie_secure: bool = False
    email_mode: str = "outbox"
    email_from_address: str | None = None
    email_from_name: str | None = None
    smtp_host: str | None = None
    smtp_port: int | None = None
    smtp_username: str | None = None
    smtp_password: str | None = None
    smtp_use_tls: bool = False
    smtp_use_starttls: bool = True
    smtp_timeout_seconds: int = 10
    email_resend_from_address: str | None = None
    email_resend_from_name: str | None = None
    email_resend_smtp_host: str | None = None
    email_resend_smtp_port: int | None = None
    email_resend_smtp_username: str | None = None
    email_resend_smtp_password: str | None = None
    email_resend_smtp_use_tls: bool = False
    email_resend_smtp_use_starttls: bool = True
    email_resend_smtp_timeout_seconds: int = 10
    email_verification_token_expiry_hours: int = 24
    password_reset_token_expiry_minutes: int = 30


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings(
        app_name=os.getenv("APP_NAME", "AI Starter Community"),
        app_env=os.getenv("APP_ENV", "development"),
        app_host=os.getenv("APP_HOST", "127.0.0.1"),
        app_port=_env_int("APP_PORT", 8089),
        base_url=os.getenv("BASE_URL", "http://127.0.0.1:8089") or "http://127.0.0.1:8089",
        database_path=os.getenv(
            "DATABASE_PATH",
            "/opt/ai-starter-community/state/ai_starter_community.sqlite3",
        ),
        session_cookie_name=os.getenv("SESSION_COOKIE_NAME", "ai_starter_community_session"),
        session_expiry_hours=_env_int("SESSION_EXPIRY_HOURS", 168),
        session_cookie_secure=_env_bool("SESSION_COOKIE_SECURE", False),
        email_mode=os.getenv("EMAIL_MODE", "outbox"),
        email_from_address=_env_optional_str("EMAIL_FROM_ADDRESS"),
        email_from_name=_env_optional_str("EMAIL_FROM_NAME"),
        smtp_host=_env_optional_str("SMTP_HOST"),
        smtp_port=_env_optional_int("SMTP_PORT"),
        smtp_username=_env_optional_str("SMTP_USERNAME"),
        smtp_password=_env_optional_str("SMTP_PASSWORD"),
        smtp_use_tls=_env_bool("SMTP_USE_TLS", False),
        smtp_use_starttls=_env_bool("SMTP_USE_STARTTLS", True),
        smtp_timeout_seconds=_env_int("SMTP_TIMEOUT_SECONDS", 10),
        email_resend_from_address=_env_optional_str("EMAIL_RESEND_FROM_ADDRESS"),
        email_resend_from_name=_env_optional_str("EMAIL_RESEND_FROM_NAME"),
        email_resend_smtp_host=_env_optional_str("EMAIL_RESEND_SMTP_HOST"),
        email_resend_smtp_port=_env_optional_int("EMAIL_RESEND_SMTP_PORT"),
        email_resend_smtp_username=_env_optional_str("EMAIL_RESEND_SMTP_USERNAME"),
        email_resend_smtp_password=_env_optional_str("EMAIL_RESEND_SMTP_PASSWORD"),
        email_resend_smtp_use_tls=_env_bool("EMAIL_RESEND_SMTP_USE_TLS", False),
        email_resend_smtp_use_starttls=_env_bool("EMAIL_RESEND_SMTP_USE_STARTTLS", True),
        email_resend_smtp_timeout_seconds=_env_int("EMAIL_RESEND_SMTP_TIMEOUT_SECONDS", 10),
        email_verification_token_expiry_hours=_env_int("EMAIL_VERIFICATION_TOKEN_EXPIRY_HOURS", 24),
        password_reset_token_expiry_minutes=_env_int("PASSWORD_RESET_TOKEN_EXPIRY_MINUTES", 30),
    )


def database_path_from_settings(settings: Settings | None = None) -> Path:
    current_settings = settings or get_settings()
    return Path(current_settings.database_path)
