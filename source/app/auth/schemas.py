"""Auth-related data structures."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class UserPublic:
    id: int
    email: str
    login: str
    role: str
    is_active: bool
    access_status: str
    email_verified_at: str | None
    materials_access_granted_at: str | None

    @property
    def email_verified(self) -> bool:
        return self.email_verified_at is not None

    @property
    def materials_access_granted(self) -> bool:
        return self.materials_access_granted_at is not None
