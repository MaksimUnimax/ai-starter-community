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
        email_verification_token_expiry_hours=_env_int("EMAIL_VERIFICATION_TOKEN_EXPIRY_HOURS", 24),
        password_reset_token_expiry_minutes=_env_int("PASSWORD_RESET_TOKEN_EXPIRY_MINUTES", 30),
    )


def database_path_from_settings(settings: Settings | None = None) -> Path:
    current_settings = settings or get_settings()
    return Path(current_settings.database_path)
