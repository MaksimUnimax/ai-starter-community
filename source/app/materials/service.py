"""Materials access helpers."""

from __future__ import annotations

from app.auth.schemas import UserPublic


def user_has_materials_access(user: UserPublic | None) -> bool:
    return bool(user and user.materials_access_granted_at is not None)
