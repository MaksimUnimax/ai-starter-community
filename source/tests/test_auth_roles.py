from __future__ import annotations

from app.auth.schemas import UserPublic
from app.auth.service import (
    ROLE_ADMIN,
    ROLE_MODERATOR,
    ROLE_USER,
    can_manage_moderators,
    is_admin_role,
    is_moderator_role,
    normalize_role,
    role_label_ru,
)


def test_role_helpers_cover_admin_moderator_and_user():
    assert is_admin_role(ROLE_ADMIN)
    assert is_moderator_role(ROLE_MODERATOR)
    assert not is_admin_role(ROLE_MODERATOR)
    assert not is_moderator_role(ROLE_USER)
    assert can_manage_moderators(ROLE_ADMIN)
    assert not can_manage_moderators(ROLE_MODERATOR)
    assert not can_manage_moderators(ROLE_USER)
    assert role_label_ru(ROLE_MODERATOR) == "модератор"
    assert normalize_role(ROLE_USER) == ROLE_USER


def test_can_manage_moderators_accepts_user_objects():
    admin = UserPublic(
        id=1,
        email="admin@example.com",
        login="admin",
        role=ROLE_ADMIN,
        is_active=True,
        access_status="activated",
        email_verified_at="2026-06-08T00:00:00+00:00",
        materials_access_granted_at=None,
    )
    moderator = UserPublic(
        id=2,
        email="moderator@example.com",
        login="moderator",
        role=ROLE_MODERATOR,
        is_active=True,
        access_status="activated",
        email_verified_at="2026-06-08T00:00:00+00:00",
        materials_access_granted_at=None,
    )

    assert can_manage_moderators(admin)
    assert not can_manage_moderators(moderator)
    assert not can_manage_moderators(None)
