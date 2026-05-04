"""Environment-driven application settings."""

from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache


def _env_int(name: str, default: int) -> int:
    raw_value = os.getenv(name)
    if raw_value is None or raw_value == "":
        return default
    try:
        return int(raw_value)
    except ValueError:
        return default


@dataclass(frozen=True)
class Settings:
    app_name: str = "AI Starter Community"
    app_env: str = "development"
    app_host: str = "127.0.0.1"
    app_port: int = 8089
    base_url: str | None = None


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings(
        app_name=os.getenv("APP_NAME", "AI Starter Community"),
        app_env=os.getenv("APP_ENV", "development"),
        app_host=os.getenv("APP_HOST", "127.0.0.1"),
        app_port=_env_int("APP_PORT", 8089),
        base_url=os.getenv("BASE_URL") or None,
    )
