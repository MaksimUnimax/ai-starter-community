"""Account-block schemas for server-side cabinet credential blocks."""

from __future__ import annotations

from dataclasses import dataclass


_UNSET = object()


@dataclass(frozen=True, slots=True)
class AccountBlockPublic:
    id: int
    owner_user_id: int
    type: str
    title: str
    login: str
    email: str | None
    status: str
    duration_days: int
    activated_at: str | None
    expires_at: str | None
    remaining_days: int | None
    is_active: bool
    is_expired: bool
    created_by_user_id: int | None
    updated_by_user_id: int | None
    activated_by_user_id: int | None
    created_at: str
    updated_at: str

    @property
    def can_copy_email(self) -> bool:
        return self.type == "mail" and bool(self.email)


@dataclass(frozen=True, slots=True)
class AccountBlockCreateInput:
    owner_user_id: int
    type: str
    title: str
    login: str = ""
    password_secret: str = ""
    email: str | None = None
    duration_days: int = 60


@dataclass(frozen=True, slots=True)
class AccountBlockUpdateInput:
    owner_user_id: int | None | object = _UNSET
    type: str | None | object = _UNSET
    title: str | None | object = _UNSET
    login: str | None | object = _UNSET
    password_secret: str | None | object = _UNSET
    email: str | None | object = _UNSET
    duration_days: int | None | object = _UNSET


@dataclass(frozen=True, slots=True, repr=False)
class AccountBlockCopyData:
    login: str
    password_secret: str
    email: str | None


@dataclass(frozen=True, slots=True)
class AccountBlockActivationNotification:
    recipient_email: str
    subject: str
    body_text: str
    template_key: str
    block_id: int
    owner_user_id: int
    owner_login: str
    owner_email: str
    block_title: str
    block_type: str
    activated_at: str
    expires_at: str


@dataclass(frozen=True, slots=True)
class AccountBlockActivationResult:
    block: AccountBlockPublic
    notification: AccountBlockActivationNotification | None
