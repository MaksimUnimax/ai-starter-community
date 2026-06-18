from __future__ import annotations

from app.auth.schemas import UserPublic
from app.auth.service import can_manage_account_blocks, is_admin_role


def test_account_block_management_helper_is_scoped_to_admin_and_moderator():
    assert is_admin_role("admin")
    assert not is_admin_role("moderator")
    assert not is_admin_role("user")
    assert can_manage_account_blocks("admin")
    assert can_manage_account_blocks("moderator")
    assert not can_manage_account_blocks("user")
    assert not can_manage_account_blocks(None)


def test_account_block_management_helper_accepts_user_objects():
    admin = UserPublic(
        id=1,
        email="admin@example.com",
        login="admin",
        role="admin",
        is_active=True,
        access_status="activated",
        email_verified_at="2026-06-08T00:00:00+00:00",
        materials_access_granted_at=None,
    )
    moderator = UserPublic(
        id=2,
        email="moderator@example.com",
        login="moderator",
        role="moderator",
        is_active=True,
        access_status="activated",
        email_verified_at="2026-06-08T00:00:00+00:00",
        materials_access_granted_at=None,
    )
    user = UserPublic(
        id=3,
        email="user@example.com",
        login="user",
        role="user",
        is_active=True,
        access_status="not_activated",
        email_verified_at=None,
        materials_access_granted_at=None,
    )

    assert can_manage_account_blocks(admin)
    assert can_manage_account_blocks(moderator)
    assert not can_manage_account_blocks(user)


def test_account_block_management_roles_are_the_only_staff_roles():
    assert can_manage_account_blocks("ADMIN")
    assert can_manage_account_blocks(" moderator ")
    assert not can_manage_account_blocks("guest")
