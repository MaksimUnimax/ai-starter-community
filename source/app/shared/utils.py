"""Generic helpers shared by future modules."""

from __future__ import annotations


def page_title(section: str, app_name: str = "AI Starter Community") -> str:
    section = section.strip()
    if not section:
        return app_name
    return f"{section} · {app_name}"
