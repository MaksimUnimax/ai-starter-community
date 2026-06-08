"""Backend service for server-side cabinet account blocks."""

from __future__ import annotations

import re
from dataclasses import asdict, fields
from datetime import timedelta
from math import floor

from app.auth.schemas import UserPublic
from app.auth.service import can_manage_account_blocks
from app.core.config import Settings, get_settings
from app.shared.db import get_connection, get_database_path, initialize_database
from app.shared.utils import utc_now, utc_now_iso

from .schemas import (
    AccountBlockActivationNotification,
    AccountBlockActivationResult,
    AccountBlockCopyData,
    AccountBlockCreateInput,
    AccountBlockPublic,
    AccountBlockUpdateInput,
    _UNSET,
)


ACCOUNT_BLOCK_TYPES = ("chatgpt", "server", "mail")
ACCOUNT_BLOCK_ACTIVE_STATUS = "active"
ACCOUNT_BLOCK_INACTIVE_STATUS = "inactive"
ACCOUNT_BLOCK_EXPIRED_STATUS = "expired"
ACCOUNT_BLOCK_STATUSES = (
    ACCOUNT_BLOCK_INACTIVE_STATUS,
    ACCOUNT_BLOCK_ACTIVE_STATUS,
    ACCOUNT_BLOCK_EXPIRED_STATUS,
)
DEFAULT_ACCOUNT_BLOCK_DURATION_DAYS = 60
TITLE_MAX_LENGTH = 200
TEXT_MAX_LENGTH = 4000
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class AccountBlockError(Exception):
    """Base class for account-block service errors."""


class AccountBlockValidationError(AccountBlockError):
    pass


class AccountBlockPermissionError(AccountBlockError):
    pass


class AccountBlockNotFoundError(AccountBlockError):
    pass


def _settings(settings: Settings | None = None) -> Settings:
    return settings or get_settings()


def _database_path(settings: Settings | None = None):
    return get_database_path(_settings(settings))


def _connection(settings: Settings | None = None):
    resolved = _settings(settings)
    path = _database_path(resolved)
    initialize_database(path)
    return get_connection(path)


def _normalize_text(value: str | None, field_name: str, *, allow_empty: bool = False, limit: int = TEXT_MAX_LENGTH) -> str:
    normalized = "" if value is None else str(value).strip()
    if not normalized and not allow_empty:
        raise AccountBlockValidationError(f"{field_name} is required")
    if len(normalized) > limit:
        raise AccountBlockValidationError(f"{field_name} must be at most {limit} characters")
    return normalized


def _normalize_optional_text(value: str | None, *, limit: int = TEXT_MAX_LENGTH) -> str | None:
    if value is None:
        return None
    normalized = str(value).strip()
    if not normalized:
        return None
    if len(normalized) > limit:
        raise AccountBlockValidationError(f"value must be at most {limit} characters")
    return normalized


def _normalize_block_type(value: str | None) -> str:
    normalized = _normalize_text(value, "type").lower()
    if normalized not in ACCOUNT_BLOCK_TYPES:
        raise AccountBlockValidationError("unsupported account block type")
    return normalized


def _normalize_duration_days(value: int | str | None, *, default: int = DEFAULT_ACCOUNT_BLOCK_DURATION_DAYS) -> int:
    if value is None:
        return default
    if isinstance(value, bool):
        raise AccountBlockValidationError("duration_days must be an integer")
    if isinstance(value, int):
        normalized = value
    else:
        raw = str(value).strip()
        if not raw:
            return default
        try:
            normalized = int(raw)
        except ValueError as exc:
            raise AccountBlockValidationError("duration_days must be an integer") from exc
    if normalized <= 0:
        raise AccountBlockValidationError("duration_days must be greater than 0")
    return normalized


def _normalize_owner_user_id(value: int | str | None, field_name: str = "owner_user_id") -> int:
    if value is None:
        raise AccountBlockValidationError(f"{field_name} is required")
    if isinstance(value, bool):
        raise AccountBlockValidationError(f"{field_name} must be an integer")
    if isinstance(value, int):
        normalized = value
    else:
        raw = str(value).strip()
        if not raw:
            raise AccountBlockValidationError(f"{field_name} is required")
        try:
            normalized = int(raw)
        except ValueError as exc:
            raise AccountBlockValidationError(f"{field_name} must be an integer") from exc
    if normalized <= 0:
        raise AccountBlockValidationError(f"{field_name} must be greater than 0")
    return normalized


def _normalize_email(value: str | None) -> str | None:
    normalized = _normalize_optional_text(value)
    if normalized is None:
        return None
    if not EMAIL_RE.fullmatch(normalized):
        raise AccountBlockValidationError("email must be a valid email address")
    return normalized.lower()


def _normalize_password_secret(value: str | None) -> str:
    # Password values are kept behind the service boundary. App-level encryption is not yet implemented.
    return _normalize_text(value, "password_secret", allow_empty=True)


def _normalize_account_block_input(data: AccountBlockCreateInput | AccountBlockUpdateInput | None = None, *, create: bool) -> dict[str, object]:
    if data is None:
        raise AccountBlockValidationError("data is required")
    if create:
        payload = asdict(data)
        owner_user_id = _normalize_owner_user_id(payload["owner_user_id"])
        block_type = _normalize_block_type(payload["type"])
        title = _normalize_text(payload["title"], "title", limit=TITLE_MAX_LENGTH)
        login = _normalize_text(payload.get("login"), "login", allow_empty=True)
        password_secret = _normalize_password_secret(payload.get("password_secret"))
        email = _normalize_email(payload.get("email"))
        duration_days = _normalize_duration_days(payload.get("duration_days"))
        return {
            "owner_user_id": owner_user_id,
            "type": block_type,
            "title": title,
            "login": login,
            "password_secret": password_secret,
            "email": email,
            "duration_days": duration_days,
        }

    payload = {field.name: getattr(data, field.name) for field in fields(data)}
    cleaned: dict[str, object] = {}
    if payload.get("owner_user_id") is not _UNSET:
        cleaned["owner_user_id"] = _normalize_owner_user_id(payload["owner_user_id"])
    if payload.get("type") is not _UNSET:
        cleaned["type"] = _normalize_block_type(payload["type"])
    if payload.get("title") is not _UNSET:
        cleaned["title"] = _normalize_text(payload["title"], "title", limit=TITLE_MAX_LENGTH)
    if payload.get("login") is not _UNSET:
        cleaned["login"] = _normalize_text(payload["login"], "login", allow_empty=True)
    if payload.get("password_secret") is not _UNSET:
        cleaned["password_secret"] = _normalize_password_secret(payload["password_secret"])
    if payload.get("email") is not _UNSET:
        cleaned["email"] = _normalize_email(payload["email"])
    if payload.get("duration_days") is not _UNSET:
        cleaned["duration_days"] = _normalize_duration_days(payload["duration_days"])
    if not cleaned:
        raise AccountBlockValidationError("no account block fields provided")
    return cleaned


def _fetch_user_row(user_id: int, settings: Settings | None = None):
    with _connection(settings) as connection:
        return connection.execute("SELECT * FROM users WHERE id = ?", (int(user_id),)).fetchone()


def _assert_actor_can_manage(actor: UserPublic | None) -> None:
    if actor is None or not can_manage_account_blocks(actor):
        raise AccountBlockPermissionError("account block management requires admin or moderator access")


def _assert_viewer_can_access_block(actor: UserPublic | None, block_owner_user_id: int) -> None:
    if actor is None:
        raise AccountBlockPermissionError("authentication required")
    if can_manage_account_blocks(actor):
        return
    if int(actor.id) != int(block_owner_user_id):
        raise AccountBlockPermissionError("access denied")


def _effective_status(stored_status: str, expires_at: str | None) -> tuple[str, bool, bool, int | None]:
    now = utc_now()
    normalized_status = stored_status if stored_status in ACCOUNT_BLOCK_STATUSES else ACCOUNT_BLOCK_INACTIVE_STATUS
    if normalized_status == ACCOUNT_BLOCK_ACTIVE_STATUS:
        if expires_at is None:
            return ACCOUNT_BLOCK_INACTIVE_STATUS, False, False, None
        expires_dt = _parse_iso_datetime(expires_at)
        if expires_dt is None:
            return ACCOUNT_BLOCK_INACTIVE_STATUS, False, False, None
        if now >= expires_dt:
            return ACCOUNT_BLOCK_EXPIRED_STATUS, False, True, 0
        remaining_seconds = max(0, int((expires_dt - now).total_seconds()))
        remaining_days = max(0, floor(remaining_seconds / 86400))
        return ACCOUNT_BLOCK_ACTIVE_STATUS, True, False, remaining_days
    if normalized_status == ACCOUNT_BLOCK_EXPIRED_STATUS:
        return ACCOUNT_BLOCK_EXPIRED_STATUS, False, True, 0 if expires_at else None
    return ACCOUNT_BLOCK_INACTIVE_STATUS, False, False, None


def _parse_iso_datetime(value: str | None):
    if value is None:
        return None
    from datetime import datetime

    return datetime.fromisoformat(value)


def _account_block_from_row(row) -> AccountBlockPublic:
    status, is_active, is_expired, remaining_days = _effective_status(str(row["status"]), row["expires_at"])
    return AccountBlockPublic(
        id=int(row["id"]),
        owner_user_id=int(row["owner_user_id"]),
        type=str(row["type"]),
        title=str(row["title"]),
        login=str(row["login"]),
        email=row["email"],
        status=status,
        duration_days=int(row["duration_days"]),
        activated_at=row["activated_at"],
        expires_at=row["expires_at"],
        remaining_days=remaining_days,
        is_active=is_active,
        is_expired=is_expired,
        created_by_user_id=row["created_by_user_id"],
        updated_by_user_id=row["updated_by_user_id"],
        activated_by_user_id=row["activated_by_user_id"],
        created_at=str(row["created_at"]),
        updated_at=str(row["updated_at"]),
    )


def _fetch_account_block_row(block_id: int, settings: Settings | None = None):
    with _connection(settings) as connection:
        return connection.execute("SELECT * FROM account_blocks WHERE id = ?", (int(block_id),)).fetchone()


def _assert_owner_exists(owner_user_id: int, settings: Settings | None = None) -> None:
    if _fetch_user_row(owner_user_id, settings=settings) is None:
        raise AccountBlockNotFoundError("owner user not found")


def _public_view_for_block(block_row) -> AccountBlockPublic:
    return _account_block_from_row(block_row)


def list_account_blocks_for_viewer(
    viewer: UserPublic,
    *,
    owner_user_id: int | None = None,
    settings: Settings | None = None,
) -> list[AccountBlockPublic]:
    with _connection(settings) as connection:
        if can_manage_account_blocks(viewer):
            if owner_user_id is None:
                rows = connection.execute(
                    """
                    SELECT *
                    FROM account_blocks
                    ORDER BY owner_user_id ASC, updated_at DESC, id DESC
                    """,
                ).fetchall()
            else:
                rows = connection.execute(
                    """
                    SELECT *
                    FROM account_blocks
                    WHERE owner_user_id = ?
                    ORDER BY updated_at DESC, id DESC
                    """,
                    (int(owner_user_id),),
                ).fetchall()
        else:
            resolved_owner_user_id = int(owner_user_id) if owner_user_id is not None else int(viewer.id)
            if resolved_owner_user_id != int(viewer.id):
                raise AccountBlockPermissionError("access denied")
            rows = connection.execute(
                """
                SELECT *
                FROM account_blocks
                WHERE owner_user_id = ?
                ORDER BY updated_at DESC, id DESC
                """,
                (resolved_owner_user_id,),
            ).fetchall()
    return [_public_view_for_block(row) for row in rows]


def get_account_block_public(
    *,
    actor: UserPublic,
    block_id: int,
    settings: Settings | None = None,
) -> AccountBlockPublic:
    row = _fetch_account_block_row(block_id, settings=settings)
    if row is None:
        raise AccountBlockNotFoundError("account block not found")
    _assert_viewer_can_access_block(actor, int(row["owner_user_id"]))
    return _public_view_for_block(row)


def get_account_block_copy_data(
    *,
    actor: UserPublic,
    block_id: int,
    settings: Settings | None = None,
) -> AccountBlockCopyData:
    row = _fetch_account_block_row(block_id, settings=settings)
    if row is None:
        raise AccountBlockNotFoundError("account block not found")
    _assert_viewer_can_access_block(actor, int(row["owner_user_id"]))
    return AccountBlockCopyData(
        login=str(row["login"]),
        password_secret=str(row["password_secret"]),
        email=row["email"],
    )


def create_account_block(
    *,
    actor: UserPublic,
    data: AccountBlockCreateInput,
    settings: Settings | None = None,
) -> AccountBlockPublic:
    _assert_actor_can_manage(actor)
    payload = _normalize_account_block_input(data, create=True)
    owner_user_id = int(payload["owner_user_id"])
    _assert_owner_exists(owner_user_id, settings=settings)
    now_iso = utc_now_iso()
    with _connection(settings) as connection:
        cursor = connection.execute(
            """
            INSERT INTO account_blocks (
                owner_user_id, type, title, login, password_secret, email,
                status, duration_days, activated_at, expires_at,
                created_by_user_id, updated_by_user_id, activated_by_user_id,
                created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, NULL, NULL, ?, ?, NULL, ?, ?)
            """,
            (
                owner_user_id,
                str(payload["type"]),
                str(payload["title"]),
                str(payload["login"]),
                str(payload["password_secret"]),
                payload["email"],
                ACCOUNT_BLOCK_INACTIVE_STATUS,
                int(payload["duration_days"]),
                int(actor.id),
                int(actor.id),
                now_iso,
                now_iso,
            ),
        )
        block_id = int(cursor.lastrowid)
        row = connection.execute("SELECT * FROM account_blocks WHERE id = ?", (block_id,)).fetchone()
        if row is None:
            raise AccountBlockError("account block insert failed")
        return _public_view_for_block(row)


def update_account_block(
    *,
    actor: UserPublic,
    block_id: int,
    data: AccountBlockUpdateInput,
    settings: Settings | None = None,
) -> AccountBlockPublic:
    _assert_actor_can_manage(actor)
    payload = _normalize_account_block_input(data, create=False)
    with _connection(settings) as connection:
        row = connection.execute("SELECT * FROM account_blocks WHERE id = ?", (int(block_id),)).fetchone()
        if row is None:
            raise AccountBlockNotFoundError("account block not found")
        updates: list[str] = []
        params: list[object] = []
        if "owner_user_id" in payload:
            owner_user_id = int(payload["owner_user_id"])
            _assert_owner_exists(owner_user_id, settings=settings)
            updates.append("owner_user_id = ?")
            params.append(owner_user_id)
        if "type" in payload:
            updates.append("type = ?")
            params.append(str(payload["type"]))
        if "title" in payload:
            updates.append("title = ?")
            params.append(str(payload["title"]))
        if "login" in payload:
            updates.append("login = ?")
            params.append(str(payload["login"]))
        if "password_secret" in payload:
            updates.append("password_secret = ?")
            params.append(str(payload["password_secret"]))
        if "email" in payload:
            updates.append("email = ?")
            params.append(payload["email"])
        if "duration_days" in payload:
            updates.append("duration_days = ?")
            params.append(int(payload["duration_days"]))
        updates.append("updated_by_user_id = ?")
        params.append(int(actor.id))
        updates.append("updated_at = ?")
        params.append(utc_now_iso())
        params.append(int(block_id))
        connection.execute(
            f"UPDATE account_blocks SET {', '.join(updates)} WHERE id = ?",
            params,
        )
        updated = connection.execute("SELECT * FROM account_blocks WHERE id = ?", (int(block_id),)).fetchone()
        if updated is None:
            raise AccountBlockError("account block update failed")
        return _public_view_for_block(updated)


def delete_account_block(
    *,
    actor: UserPublic,
    block_id: int,
    settings: Settings | None = None,
) -> None:
    _assert_actor_can_manage(actor)
    with _connection(settings) as connection:
        row = connection.execute("SELECT * FROM account_blocks WHERE id = ?", (int(block_id),)).fetchone()
        if row is None:
            raise AccountBlockNotFoundError("account block not found")
        connection.execute("DELETE FROM account_blocks WHERE id = ?", (int(block_id),))


def _activation_notification_for_row(row, *, settings: Settings | None = None) -> AccountBlockActivationNotification | None:
    owner_row = _fetch_user_row(int(row["owner_user_id"]), settings=settings)
    if owner_row is None:
        return None
    recipient_email = str(owner_row["email"])
    if not recipient_email:
        return None
    title = str(row["title"])
    type_label = {
        "chatgpt": "ChatGPT",
        "server": "Сервер",
        "mail": "Почта",
    }.get(str(row["type"]), str(row["type"]))
    activated_at = str(row["activated_at"])
    expires_at = str(row["expires_at"])
    subject = "Аккаунт в кабинете активирован"
    body_text = (
        f"Здравствуйте, {str(owner_row['login'])}.\n\n"
        f"Блок \"{title}\" ({type_label}) активирован.\n"
        f"Срок действия: до {expires_at}.\n"
        "Зайдите в личный кабинет, чтобы посмотреть состояние и срок действия блока."
    )
    return AccountBlockActivationNotification(
        recipient_email=recipient_email,
        subject=subject,
        body_text=body_text,
        template_key="account_block_activation",
        block_id=int(row["id"]),
        owner_user_id=int(row["owner_user_id"]),
        owner_login=str(owner_row["login"]),
        owner_email=recipient_email,
        block_title=title,
        block_type=str(row["type"]),
        activated_at=activated_at,
        expires_at=expires_at,
    )


def activate_account_block(
    *,
    actor: UserPublic,
    block_id: int,
    settings: Settings | None = None,
) -> AccountBlockActivationResult:
    _assert_actor_can_manage(actor)
    now = utc_now()
    now_iso = now.isoformat()
    with _connection(settings) as connection:
        row = connection.execute("SELECT * FROM account_blocks WHERE id = ?", (int(block_id),)).fetchone()
        if row is None:
            raise AccountBlockNotFoundError("account block not found")
        duration_days = int(row["duration_days"] or DEFAULT_ACCOUNT_BLOCK_DURATION_DAYS)
        expires_at = (now + timedelta(days=duration_days)).isoformat()
        connection.execute(
            """
            UPDATE account_blocks
            SET status = ?,
                activated_at = ?,
                expires_at = ?,
                activated_by_user_id = ?,
                updated_by_user_id = ?,
                updated_at = ?
            WHERE id = ?
            """,
            (
                ACCOUNT_BLOCK_ACTIVE_STATUS,
                now_iso,
                expires_at,
                int(actor.id),
                int(actor.id),
                now_iso,
                int(block_id),
            ),
        )
        updated = connection.execute("SELECT * FROM account_blocks WHERE id = ?", (int(block_id),)).fetchone()
        if updated is None:
            raise AccountBlockError("account block activation failed")
    notification = _activation_notification_for_row(updated, settings=settings)
    return AccountBlockActivationResult(
        block=_public_view_for_block(updated),
        notification=notification,
    )
