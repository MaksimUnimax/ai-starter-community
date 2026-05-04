"""Materials access helpers."""

from __future__ import annotations

from app.auth.schemas import UserPublic
from app.auth.service import user_can_access_materials


def user_has_materials_access(user: UserPublic | None) -> bool:
    return user_can_access_materials(user)
