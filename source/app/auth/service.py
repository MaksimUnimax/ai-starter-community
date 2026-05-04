"""Placeholder auth service layer.

No persistent user creation or password storage is implemented yet.
"""

from __future__ import annotations


def placeholder_auth_context(action: str) -> dict[str, str]:
    return {"action": action, "status": "placeholder"}
