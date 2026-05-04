"""Generic helpers shared by future modules."""

from __future__ import annotations

from datetime import datetime, timezone


def page_title(section: str, app_name: str = "AI Starter Community") -> str:
    section = section.strip()
    if not section:
        return app_name
    return f"{section} · {app_name}"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def utc_now_iso() -> str:
    return utc_now().isoformat()
