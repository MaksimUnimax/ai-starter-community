"""Paid option catalog services."""

from __future__ import annotations

import re
import sqlite3
from dataclasses import asdict

from app.core.config import Settings, get_settings
from app.shared.db import get_connection, get_database_path, initialize_database
from app.shared.utils import utc_now_iso

from .schemas import PaidOptionCreateInput, PaidOptionPublic, PaidOptionUpdateInput


CODE_RE = re.compile(r"^[a-z0-9_-]{3,64}$")
TITLE_MAX_LENGTH = 200
DESCRIPTION_MAX_LENGTH = 4000
INT_RE = re.compile(r"^-?\d+$")
CURRENCY_RE = re.compile(r"^[A-Z]{3}$")
ALLOWED_STATUSES = {"active", "hidden", "archived"}
_UNSET = object()


class CatalogError(Exception):
    """Base class for paid-option catalog errors."""


class ValidationError(CatalogError):
    pass


class ConflictError(CatalogError):
    pass


class NotFoundError(CatalogError):
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


def _normalize_code(value: str, field_name: str = "code") -> str:
    normalized = ("" if value is None else str(value)).strip().lower()
    if not normalized:
        raise ValidationError(f"{field_name} is required")
    if not CODE_RE.fullmatch(normalized):
        raise ValidationError(f"{field_name} must be 3-64 chars of lowercase letters, digits, underscore or hyphen")
    return normalized


def _normalize_title(value: str) -> str:
    normalized = ("" if value is None else str(value)).strip()
    if not normalized:
        raise ValidationError("title is required")
    if len(normalized) > TITLE_MAX_LENGTH:
        raise ValidationError(f"title must be at most {TITLE_MAX_LENGTH} characters")
    return normalized


def _normalize_description(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = str(value).strip()
    if not normalized:
        return None
    if len(normalized) > DESCRIPTION_MAX_LENGTH:
        raise ValidationError(f"description must be at most {DESCRIPTION_MAX_LENGTH} characters")
    return normalized


def _normalize_currency(value: str | None) -> str:
    normalized = "RUB" if value is None else str(value).strip().upper()
    if not CURRENCY_RE.fullmatch(normalized):
        raise ValidationError("currency must be a 3-letter uppercase code")
    return normalized


def _normalize_status(value: str | None) -> str:
    normalized = "active" if value is None else str(value).strip().lower()
    if normalized not in ALLOWED_STATUSES:
        raise ValidationError("status must be active, hidden, or archived")
    return normalized


def _normalize_int(value, field_name: str, *, allow_none: bool = False, minimum: int = 0) -> int | None:
    if value is None:
        if allow_none:
            return None
        raise ValidationError(f"{field_name} is required")
    if isinstance(value, bool):
        raise ValidationError(f"{field_name} must be an integer")
    if isinstance(value, int):
        normalized = value
    else:
        raw = str(value).strip()
        if not INT_RE.fullmatch(raw):
            raise ValidationError(f"{field_name} must be an integer")
        normalized = int(raw)
    if normalized < minimum:
        raise ValidationError(f"{field_name} must be >= {minimum}")
    return normalized


def _normalize_boolish(value, field_name: str) -> int:
    if isinstance(value, bool):
        return 1 if value else 0
    if isinstance(value, int) and value in {0, 1}:
        return value
    raw = str(value).strip().lower()
    if raw in {"1", "true", "yes", "on"}:
        return 1
    if raw in {"0", "false", "no", "off"}:
        return 0
    raise ValidationError(f"{field_name} must be a boolean")


def _paid_option_from_row(row) -> PaidOptionPublic:
    return PaidOptionPublic(
        id=int(row["id"]),
        code=str(row["code"]),
        title=str(row["title"]),
        description=row["description"],
        price_amount_minor=row["price_amount_minor"],
        currency=str(row["currency"]),
        default_duration_days=row["default_duration_days"],
        status=str(row["status"]),
        is_renewable=bool(row["is_renewable"]),
        sort_order=int(row["sort_order"]),
        created_at=str(row["created_at"]),
        updated_at=str(row["updated_at"]),
    )


def _lookup_paid_option_row(connection, code: str, *, include_hidden: bool = True, include_archived: bool = True):
    normalized_code = ("" if code is None else str(code)).strip().lower()
    if not normalized_code:
        return None
    row = connection.execute("SELECT * FROM paid_options WHERE code = ?", (normalized_code,)).fetchone()
    if row is None:
        return None
    status = str(row["status"])
    if status == "hidden" and not include_hidden:
        return None
    if status == "archived" and not include_archived:
        return None
    return row


def _coerce_create_payload(
    data: PaidOptionCreateInput | None,
    *,
    code: str | None,
    title: str | None,
    description: str | None,
    price_amount_minor,
    currency: str | None,
    default_duration_days,
    status: str | None,
    is_renewable,
    sort_order,
) -> dict:
    if data is not None:
        if any(
            value is not None
            for value in (code, title, description, price_amount_minor, currency, default_duration_days, status, is_renewable, sort_order)
        ):
            raise ValidationError("pass either data or keyword arguments, not both")
        return asdict(data)
    return {
        "code": code,
        "title": title,
        "description": description,
        "price_amount_minor": price_amount_minor,
        "currency": currency,
        "default_duration_days": default_duration_days,
        "status": status,
        "is_renewable": is_renewable,
        "sort_order": sort_order,
    }


def _coerce_update_payload(
    data: PaidOptionUpdateInput | None,
    *,
    title,
    description,
    price_amount_minor,
    currency,
    default_duration_days,
    status,
    is_renewable,
    sort_order,
) -> dict:
    if data is not None:
        if any(
            value is not _UNSET
            for value in (title, description, price_amount_minor, currency, default_duration_days, status, is_renewable, sort_order)
        ):
            raise ValidationError("pass either data or keyword arguments, not both")
        return asdict(data)
    return {
        "title": title,
        "description": description,
        "price_amount_minor": price_amount_minor,
        "currency": currency,
        "default_duration_days": default_duration_days,
        "status": status,
        "is_renewable": is_renewable,
        "sort_order": sort_order,
    }


def list_paid_options(
    include_hidden: bool = False,
    include_archived: bool = False,
    settings: Settings | None = None,
) -> list[PaidOptionPublic]:
    statuses = ["active"]
    if include_hidden:
        statuses.append("hidden")
    if include_archived:
        statuses.append("archived")
    placeholders = ",".join("?" for _ in statuses)
    with _connection(settings) as connection:
        rows = connection.execute(
            f"SELECT * FROM paid_options WHERE status IN ({placeholders}) ORDER BY sort_order ASC, id ASC, code ASC",
            tuple(statuses),
        ).fetchall()
        return [_paid_option_from_row(row) for row in rows]


def list_paid_options_for_admin(settings: Settings | None = None) -> list[PaidOptionPublic]:
    return list_paid_options(include_hidden=True, include_archived=True, settings=settings)


def get_paid_option_by_code(code: str, settings: Settings | None = None) -> PaidOptionPublic | None:
    normalized_code = (code or "").strip().lower()
    with _connection(settings) as connection:
        row = connection.execute("SELECT * FROM paid_options WHERE code = ?", (normalized_code,)).fetchone()
        return _paid_option_from_row(row) if row else None


def create_paid_option(
    *,
    data: PaidOptionCreateInput | None = None,
    code: str | None = None,
    title: str | None = None,
    description: str | None = None,
    price_amount_minor=None,
    currency: str | None = None,
    default_duration_days=None,
    status: str | None = None,
    is_renewable=None,
    sort_order=None,
    settings: Settings | None = None,
) -> PaidOptionPublic:
    payload = _coerce_create_payload(
        data,
        code=code,
        title=title,
        description=description,
        price_amount_minor=price_amount_minor,
        currency=currency,
        default_duration_days=default_duration_days,
        status=status,
        is_renewable=is_renewable,
        sort_order=sort_order,
    )
    normalized_code = _normalize_code(payload["code"])
    normalized_title = _normalize_title(payload["title"])
    normalized_description = _normalize_description(payload["description"])
    normalized_price = _normalize_int(payload["price_amount_minor"], "price_amount_minor", allow_none=True, minimum=0)
    normalized_currency = _normalize_currency("RUB" if payload["currency"] is None else payload["currency"])
    normalized_default_duration_days = _normalize_int(
        payload["default_duration_days"],
        "default_duration_days",
        allow_none=True,
        minimum=0,
    )
    normalized_status = _normalize_status("active" if payload["status"] is None else payload["status"])
    normalized_is_renewable = _normalize_boolish(True if payload["is_renewable"] is None else payload["is_renewable"], "is_renewable")
    normalized_sort_order = _normalize_int(0 if payload["sort_order"] is None else payload["sort_order"], "sort_order", allow_none=False, minimum=0)

    resolved = _settings(settings)
    now_iso = utc_now_iso()
    with _connection(resolved) as connection:
        existing = connection.execute("SELECT id FROM paid_options WHERE code = ?", (normalized_code,)).fetchone()
        if existing is not None:
            raise ConflictError("paid option code already exists")
        cursor = connection.execute(
            """
            INSERT INTO paid_options (
                code, title, description, price_amount_minor, currency,
                default_duration_days, status, is_renewable, sort_order,
                created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                normalized_code,
                normalized_title,
                normalized_description,
                normalized_price,
                normalized_currency,
                normalized_default_duration_days,
                normalized_status,
                normalized_is_renewable,
                normalized_sort_order,
                now_iso,
                now_iso,
            ),
        )
        row = connection.execute("SELECT * FROM paid_options WHERE id = ?", (cursor.lastrowid,)).fetchone()
        if row is None:
            raise CatalogError("paid option creation failed")
        return _paid_option_from_row(row)


def update_paid_option(
    code: str,
    *,
    data: PaidOptionUpdateInput | None = None,
    title=_UNSET,
    description=_UNSET,
    price_amount_minor=_UNSET,
    currency=_UNSET,
    default_duration_days=_UNSET,
    status=_UNSET,
    is_renewable=_UNSET,
    sort_order=_UNSET,
    settings: Settings | None = None,
) -> PaidOptionPublic:
    normalized_code = _normalize_code(code)
    payload = _coerce_update_payload(
        data,
        title=title,
        description=description,
        price_amount_minor=price_amount_minor,
        currency=currency,
        default_duration_days=default_duration_days,
        status=status,
        is_renewable=is_renewable,
        sort_order=sort_order,
    )
    updates: dict[str, object] = {}
    if payload["title"] is not _UNSET:
        updates["title"] = _normalize_title(payload["title"])
    if payload["description"] is not _UNSET:
        updates["description"] = _normalize_description(payload["description"])
    if payload["price_amount_minor"] is not _UNSET:
        updates["price_amount_minor"] = _normalize_int(payload["price_amount_minor"], "price_amount_minor", allow_none=True, minimum=0)
    if payload["currency"] is not _UNSET:
        if payload["currency"] is None:
            raise ValidationError("currency is required")
        updates["currency"] = _normalize_currency(payload["currency"])
    if payload["default_duration_days"] is not _UNSET:
        updates["default_duration_days"] = _normalize_int(
            payload["default_duration_days"],
            "default_duration_days",
            allow_none=True,
            minimum=0,
        )
    if payload["status"] is not _UNSET:
        if payload["status"] is None:
            raise ValidationError("status is required")
        updates["status"] = _normalize_status(payload["status"])
    if payload["is_renewable"] is not _UNSET:
        if payload["is_renewable"] is None:
            raise ValidationError("is_renewable is required")
        updates["is_renewable"] = _normalize_boolish(payload["is_renewable"], "is_renewable")
    if payload["sort_order"] is not _UNSET:
        updates["sort_order"] = _normalize_int(payload["sort_order"], "sort_order", allow_none=False, minimum=0)

    resolved = _settings(settings)
    now_iso = utc_now_iso()
    with _connection(resolved) as connection:
        row = connection.execute("SELECT * FROM paid_options WHERE code = ?", (normalized_code,)).fetchone()
        if row is None:
            raise NotFoundError("paid option not found")
        if not updates:
            return _paid_option_from_row(row)
        set_clause = ", ".join(f"{column} = ?" for column in updates)
        params = (*updates.values(), now_iso, normalized_code)
        connection.execute(
            f"UPDATE paid_options SET {set_clause}, updated_at = ? WHERE code = ?",
            params,
        )
        updated = connection.execute("SELECT * FROM paid_options WHERE code = ?", (normalized_code,)).fetchone()
        if updated is None:
            raise CatalogError("paid option update failed")
        return _paid_option_from_row(updated)


def archive_paid_option(code: str, settings: Settings | None = None) -> bool:
    normalized_code = _normalize_code(code)
    now_iso = utc_now_iso()
    with _connection(settings) as connection:
        row = connection.execute("SELECT * FROM paid_options WHERE code = ?", (normalized_code,)).fetchone()
        if row is None:
            raise NotFoundError("paid option not found")
        if str(row["status"]) == "archived":
            return False
        connection.execute(
            "UPDATE paid_options SET status = ?, updated_at = ? WHERE code = ?",
            ("archived", now_iso, normalized_code),
        )
        return True


def upsert_paid_option(
    *,
    code: str,
    title: str,
    description: str | None = None,
    price_amount_minor: int | None = None,
    currency: str = "RUB",
    default_duration_days: int | None = None,
    status: str = "active",
    is_renewable: int = 1,
    sort_order: int = 0,
    settings: Settings | None = None,
) -> PaidOptionPublic:
    normalized_code = (code or "").strip().lower()
    with _connection(settings) as connection:
        row = connection.execute("SELECT * FROM paid_options WHERE code = ?", (normalized_code,)).fetchone()
        if row is not None:
            return _paid_option_from_row(row)
    return create_paid_option(
        code=normalized_code,
        title=title,
        description=description,
        price_amount_minor=price_amount_minor,
        currency=currency,
        default_duration_days=default_duration_days,
        status=status,
        is_renewable=is_renewable,
        sort_order=sort_order,
        settings=settings,
    )
