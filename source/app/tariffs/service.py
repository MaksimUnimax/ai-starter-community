"""Tariff catalog services and seed helpers."""

from __future__ import annotations

import re
import sqlite3
import secrets
from dataclasses import asdict

from app.core.config import Settings, get_settings
from app.shared.db import get_connection, get_database_path, initialize_database
from app.shared.utils import utc_now_iso

from .schemas import TariffCreateInput, TariffOptionLinkInput, TariffPublic, TariffUpdateInput


STARTER_TARIFF_CODE = "starter_4990_rub"
STARTER_TARIFF_TITLE = "Стартовый доступ"
STARTER_TARIFF_DESCRIPTION = "Базовый тариф для старта работы с сервисом."

CODE_RE = re.compile(r"^[a-z0-9_-]{3,64}$")
TITLE_MAX_LENGTH = 200
DESCRIPTION_MAX_LENGTH = 4000
INT_RE = re.compile(r"^-?\d+$")
CURRENCY_RE = re.compile(r"^[A-Z]{3}$")
ALLOWED_STATUSES = {"active", "hidden", "archived"}
_UNSET = object()


class CatalogError(Exception):
    """Base class for tariff catalog errors."""


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


def _generate_unique_code(connection, prefix: str, table_name: str) -> str:
    for _ in range(100):
        candidate = f"{prefix}{secrets.token_hex(8)}"
        row = connection.execute(f"SELECT 1 FROM {table_name} WHERE code = ?", (candidate,)).fetchone()
        if row is None:
            return candidate
    raise CatalogError("failed to generate code")


def _resolve_create_code(connection, value, *, prefix: str, table_name: str) -> tuple[str, bool]:
    raw = "" if value is None else str(value).strip().lower()
    if raw:
        return _normalize_code(raw), False
    return _generate_unique_code(connection, prefix, table_name), True


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


def _tariff_from_row(row) -> TariffPublic:
    return TariffPublic(
        id=int(row["id"]),
        code=str(row["code"]),
        title=str(row["title"]),
        description=row["description"],
        price_amount_minor=int(row["price_amount_minor"]),
        currency=str(row["currency"]),
        status=str(row["status"]),
        sort_order=int(row["sort_order"]),
        created_at=str(row["created_at"]),
        updated_at=str(row["updated_at"]),
    )


def _tariff_row_is_visible(row, include_hidden: bool, include_archived: bool) -> bool:
    status = str(row["status"])
    if status == "hidden" and not include_hidden:
        return False
    if status == "archived" and not include_archived:
        return False
    return True


def _lookup_tariff_row(
    connection,
    code: str,
    *,
    include_hidden: bool = True,
    include_archived: bool = True,
):
    normalized_code = ("" if code is None else str(code)).strip().lower()
    if not normalized_code:
        return None
    row = connection.execute("SELECT * FROM tariffs WHERE code = ?", (normalized_code,)).fetchone()
    if row is None or not _tariff_row_is_visible(row, include_hidden, include_archived):
        return None
    return row


def _paid_option_row_from_link(row) -> dict:
    payload = dict(row)
    payload["is_renewable"] = bool(payload["is_renewable"])
    return payload


def _linked_option_rows(
    connection,
    tariff_id: int,
    *,
    include_hidden: bool = False,
    include_archived: bool = False,
) -> list[dict]:
    statuses = ["active"]
    if include_hidden:
        statuses.append("hidden")
    if include_archived:
        statuses.append("archived")
    placeholders = ",".join("?" for _ in statuses)
    rows = connection.execute(
        f"""
        SELECT
            po.*,
            topt.included_duration_days,
            topt.included_quantity,
            topt.created_at AS link_created_at
        FROM tariff_options AS topt
        JOIN paid_options AS po ON po.id = topt.option_id
        WHERE topt.tariff_id = ?
          AND po.status IN ({placeholders})
        ORDER BY po.sort_order ASC, po.id ASC, po.code ASC
        """,
        (tariff_id, *statuses),
    ).fetchall()
    return [_paid_option_row_from_link(row) for row in rows]


def _lookup_paid_option_row(
    connection,
    code: str,
    *,
    include_hidden: bool = True,
    include_archived: bool = True,
):
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


def _lookup_link_row(connection, tariff_id: int, option_id: int):
    return connection.execute(
        """
        SELECT
            po.*,
            topt.included_duration_days,
            topt.included_quantity,
            topt.created_at AS link_created_at
        FROM tariff_options AS topt
        JOIN paid_options AS po ON po.id = topt.option_id
        WHERE topt.tariff_id = ? AND topt.option_id = ?
        """,
        (tariff_id, option_id),
    ).fetchone()


def _coerce_create_payload(
    data: TariffCreateInput | None,
    *,
    code: str | None,
    title: str | None,
    description: str | None,
    price_amount_minor,
    currency: str | None,
    status: str | None,
    sort_order,
) -> dict:
    if data is not None:
        if any(value is not None for value in (code, title, description, price_amount_minor, currency, status, sort_order)):
            raise ValidationError("pass either data or keyword arguments, not both")
        return asdict(data)
    return {
        "code": code,
        "title": title,
        "description": description,
        "price_amount_minor": price_amount_minor,
        "currency": currency,
        "status": status,
        "sort_order": sort_order,
    }


def _coerce_update_payload(
    data: TariffUpdateInput | None,
    *,
    title,
    description,
    price_amount_minor,
    currency,
    status,
    sort_order,
) -> dict:
    if data is not None:
        if any(value is not _UNSET for value in (title, description, price_amount_minor, currency, status, sort_order)):
            raise ValidationError("pass either data or keyword arguments, not both")
        return asdict(data)
    return {
        "title": title,
        "description": description,
        "price_amount_minor": price_amount_minor,
        "currency": currency,
        "status": status,
        "sort_order": sort_order,
    }


def _coerce_link_payload(
    data: TariffOptionLinkInput | None,
    *,
    included_duration_days,
    included_quantity,
) -> dict:
    if data is not None:
        if any(value is not _UNSET for value in (included_duration_days, included_quantity)):
            raise ValidationError("pass either data or keyword arguments, not both")
        return asdict(data)
    return {
        "included_duration_days": included_duration_days,
        "included_quantity": included_quantity,
    }


def list_tariffs(
    include_hidden: bool = False,
    include_archived: bool = False,
    settings: Settings | None = None,
) -> list[TariffPublic]:
    statuses = ["active"]
    if include_hidden:
        statuses.append("hidden")
    if include_archived:
        statuses.append("archived")
    placeholders = ",".join("?" for _ in statuses)
    with _connection(settings) as connection:
        rows = connection.execute(
            f"SELECT * FROM tariffs WHERE status IN ({placeholders}) ORDER BY sort_order ASC, id ASC, code ASC",
            tuple(statuses),
        ).fetchall()
        return [_tariff_from_row(row) for row in rows]


def list_tariffs_for_admin(settings: Settings | None = None) -> list[TariffPublic]:
    return list_tariffs(include_hidden=True, include_archived=True, settings=settings)


def get_tariff_by_code(code: str, settings: Settings | None = None) -> TariffPublic | None:
    with _connection(settings) as connection:
        row = connection.execute("SELECT * FROM tariffs WHERE code = ?", ((code or "").strip().lower(),)).fetchone()
        return _tariff_from_row(row) if row else None


def get_tariff_with_options(
    code: str,
    include_hidden: bool = False,
    include_archived: bool = False,
    settings: Settings | None = None,
) -> dict:
    normalized_code = _normalize_code(code)
    with _connection(settings) as connection:
        tariff_row = _lookup_tariff_row(
            connection,
            normalized_code,
            include_hidden=include_hidden,
            include_archived=include_archived,
        )
        if tariff_row is None:
            raise NotFoundError("tariff not found")
        return {
            "tariff": _tariff_from_row(tariff_row),
            "options": _linked_option_rows(
                connection,
                int(tariff_row["id"]),
                include_hidden=include_hidden,
                include_archived=include_archived,
            ),
        }


def create_tariff(
    *,
    data: TariffCreateInput | None = None,
    code: str | None = None,
    title: str | None = None,
    description: str | None = None,
    price_amount_minor=None,
    currency: str | None = None,
    status: str | None = None,
    sort_order=None,
    settings: Settings | None = None,
) -> TariffPublic:
    payload = _coerce_create_payload(
        data,
        code=code,
        title=title,
        description=description,
        price_amount_minor=price_amount_minor,
        currency=currency,
        status=status,
        sort_order=sort_order,
    )
    normalized_title = _normalize_title(payload["title"])
    normalized_description = _normalize_description(payload["description"])
    normalized_price = _normalize_int(payload["price_amount_minor"], "price_amount_minor", allow_none=False, minimum=0)
    normalized_currency = _normalize_currency("RUB" if payload["currency"] is None else payload["currency"])
    normalized_status = _normalize_status("active" if payload["status"] is None else payload["status"])
    normalized_sort_order = _normalize_int(0 if payload["sort_order"] is None else payload["sort_order"], "sort_order", allow_none=False, minimum=0)

    resolved = _settings(settings)
    now_iso = utc_now_iso()
    with _connection(resolved) as connection:
        normalized_code, generated = _resolve_create_code(connection, payload["code"], prefix="tariff_", table_name="tariffs")
        if not generated:
            existing = connection.execute("SELECT id FROM tariffs WHERE code = ?", (normalized_code,)).fetchone()
            if existing is not None:
                raise ConflictError("tariff code already exists")
        while True:
            try:
                cursor = connection.execute(
                    """
                    INSERT INTO tariffs (
                        code, title, description, price_amount_minor, currency,
                        status, sort_order, created_at, updated_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        normalized_code,
                        normalized_title,
                        normalized_description,
                        normalized_price,
                        normalized_currency,
                        normalized_status,
                        normalized_sort_order,
                        now_iso,
                        now_iso,
                    ),
                )
            except sqlite3.IntegrityError as exc:
                if not generated:
                    raise ConflictError("tariff code already exists") from exc
                normalized_code = _generate_unique_code(connection, "tariff_", "tariffs")
                continue
            row = connection.execute("SELECT * FROM tariffs WHERE id = ?", (cursor.lastrowid,)).fetchone()
            if row is None:
                raise CatalogError("tariff creation failed")
            return _tariff_from_row(row)


def update_tariff(
    code: str,
    *,
    data: TariffUpdateInput | None = None,
    title=_UNSET,
    description=_UNSET,
    price_amount_minor=_UNSET,
    currency=_UNSET,
    status=_UNSET,
    sort_order=_UNSET,
    settings: Settings | None = None,
) -> TariffPublic:
    normalized_code = _normalize_code(code)
    payload = _coerce_update_payload(
        data,
        title=title,
        description=description,
        price_amount_minor=price_amount_minor,
        currency=currency,
        status=status,
        sort_order=sort_order,
    )
    updates: dict[str, object] = {}
    if payload["title"] is not _UNSET:
        updates["title"] = _normalize_title(payload["title"])
    if payload["description"] is not _UNSET:
        updates["description"] = _normalize_description(payload["description"])
    if payload["price_amount_minor"] is not _UNSET:
        updates["price_amount_minor"] = _normalize_int(payload["price_amount_minor"], "price_amount_minor", minimum=0)
    if payload["currency"] is not _UNSET:
        if payload["currency"] is None:
            raise ValidationError("currency is required")
        updates["currency"] = _normalize_currency(payload["currency"])
    if payload["status"] is not _UNSET:
        if payload["status"] is None:
            raise ValidationError("status is required")
        updates["status"] = _normalize_status(payload["status"])
    if payload["sort_order"] is not _UNSET:
        updates["sort_order"] = _normalize_int(payload["sort_order"], "sort_order", minimum=0)

    resolved = _settings(settings)
    now_iso = utc_now_iso()
    with _connection(resolved) as connection:
        row = connection.execute("SELECT * FROM tariffs WHERE code = ?", (normalized_code,)).fetchone()
        if row is None:
            raise NotFoundError("tariff not found")
        if not updates:
            return _tariff_from_row(row)
        set_clause = ", ".join(f"{column} = ?" for column in updates)
        params = (*updates.values(), now_iso, normalized_code)
        connection.execute(
            f"UPDATE tariffs SET {set_clause}, updated_at = ? WHERE code = ?",
            params,
        )
        updated = connection.execute("SELECT * FROM tariffs WHERE code = ?", (normalized_code,)).fetchone()
        if updated is None:
            raise CatalogError("tariff update failed")
        return _tariff_from_row(updated)


def get_homepage_tariff(settings: Settings | None = None) -> TariffPublic | None:
    # The current schema no longer stores a homepage flag; keep startup working
    # by exposing the first active tariff in the existing sort order.
    with _connection(settings) as connection:
        row = connection.execute(
            """
            SELECT *
            FROM tariffs
            WHERE status = 'active'
            ORDER BY sort_order ASC, id ASC, code ASC
            LIMIT 1
            """
        ).fetchone()
        return _tariff_from_row(row) if row is not None else None


def archive_tariff(code: str, settings: Settings | None = None) -> bool:
    normalized_code = _normalize_code(code)
    now_iso = utc_now_iso()
    with _connection(settings) as connection:
        row = connection.execute("SELECT * FROM tariffs WHERE code = ?", (normalized_code,)).fetchone()
        if row is None:
            raise NotFoundError("tariff not found")
        if str(row["status"]) == "archived":
            return False
        connection.execute(
            "UPDATE tariffs SET status = ?, updated_at = ? WHERE code = ?",
            ("archived", now_iso, normalized_code),
        )
        return True


def list_tariff_options(
    tariff_code: str,
    include_hidden: bool = False,
    include_archived: bool = False,
    settings: Settings | None = None,
) -> list[dict]:
    normalized_code = (tariff_code or "").strip().lower()
    if not normalized_code:
        return []
    with _connection(settings) as connection:
        tariff_row = connection.execute("SELECT * FROM tariffs WHERE code = ?", (normalized_code,)).fetchone()
        if tariff_row is None:
            return []
        return _linked_option_rows(
            connection,
            int(tariff_row["id"]),
            include_hidden=include_hidden,
            include_archived=include_archived,
        )


def list_active_tariffs_with_options(settings: Settings | None = None) -> list[dict]:
    with _connection(settings) as connection:
        tariffs = connection.execute(
            """
            SELECT *
            FROM tariffs
            WHERE status = 'active'
            ORDER BY sort_order ASC, id ASC, code ASC
            """
        ).fetchall()
        result: list[dict] = []
        for tariff_row in tariffs:
            tariff_payload = dict(tariff_row)
            tariff_payload["options"] = _linked_option_rows(
                connection,
                int(tariff_row["id"]),
                include_hidden=False,
                include_archived=False,
            )
            result.append(tariff_payload)
        return result


def _upsert_tariff_option_link(
    connection,
    tariff_row,
    option_row,
    *,
    included_duration_days: int | None,
    included_quantity: int | None,
) -> dict:
    existing = _lookup_link_row(connection, int(tariff_row["id"]), int(option_row["id"]))
    now_iso = utc_now_iso()
    if existing is None:
        connection.execute(
            """
            INSERT INTO tariff_options (
                tariff_id, option_id, included_duration_days, included_quantity, created_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                int(tariff_row["id"]),
                int(option_row["id"]),
                included_duration_days,
                included_quantity,
                now_iso,
            ),
        )
    else:
        connection.execute(
            """
            UPDATE tariff_options
            SET included_duration_days = ?, included_quantity = ?
            WHERE tariff_id = ? AND option_id = ?
            """,
            (
                included_duration_days,
                included_quantity,
                int(tariff_row["id"]),
                int(option_row["id"]),
            ),
        )
    updated = _lookup_link_row(connection, int(tariff_row["id"]), int(option_row["id"]))
    if updated is None:
        raise CatalogError("tariff option link update failed")
    return _paid_option_row_from_link(updated)


def attach_option_to_tariff(
    tariff_code: str,
    option_code: str,
    *,
    data: TariffOptionLinkInput | None = None,
    included_duration_days=_UNSET,
    included_quantity=_UNSET,
    settings: Settings | None = None,
) -> dict:
    payload = _coerce_link_payload(
        data,
        included_duration_days=included_duration_days,
        included_quantity=included_quantity,
    )
    normalized_duration = None if payload["included_duration_days"] is _UNSET else _normalize_int(
        payload["included_duration_days"],
        "included_duration_days",
        allow_none=True,
        minimum=0,
    )
    normalized_quantity = None if payload["included_quantity"] is _UNSET else _normalize_int(
        payload["included_quantity"],
        "included_quantity",
        allow_none=True,
        minimum=0,
    )
    normalized_tariff_code = _normalize_code(tariff_code)
    normalized_option_code = _normalize_code(option_code)

    with _connection(settings) as connection:
        tariff_row = _lookup_tariff_row(connection, normalized_tariff_code, include_hidden=True, include_archived=True)
        if tariff_row is None:
            raise NotFoundError("tariff not found")
        if str(tariff_row["status"]) == "archived":
            raise ValidationError("archived tariff cannot be modified")
        option_row = _lookup_paid_option_row(connection, normalized_option_code, include_hidden=True, include_archived=True)
        if option_row is None:
            raise NotFoundError("paid option not found")
        if str(option_row["status"]) == "archived":
            raise ValidationError("archived paid option cannot be attached")
        return _upsert_tariff_option_link(
            connection,
            tariff_row,
            option_row,
            included_duration_days=normalized_duration,
            included_quantity=normalized_quantity,
        )


def update_tariff_option_link(
    tariff_code: str,
    option_code: str,
    *,
    data: TariffOptionLinkInput | None = None,
    included_duration_days=_UNSET,
    included_quantity=_UNSET,
    settings: Settings | None = None,
) -> dict:
    payload = _coerce_link_payload(
        data,
        included_duration_days=included_duration_days,
        included_quantity=included_quantity,
    )
    normalized_duration = None if payload["included_duration_days"] is _UNSET else _normalize_int(
        payload["included_duration_days"],
        "included_duration_days",
        allow_none=True,
        minimum=0,
    )
    normalized_quantity = None if payload["included_quantity"] is _UNSET else _normalize_int(
        payload["included_quantity"],
        "included_quantity",
        allow_none=True,
        minimum=0,
    )
    normalized_tariff_code = _normalize_code(tariff_code)
    normalized_option_code = _normalize_code(option_code)

    with _connection(settings) as connection:
        tariff_row = _lookup_tariff_row(connection, normalized_tariff_code, include_hidden=True, include_archived=True)
        if tariff_row is None:
            raise NotFoundError("tariff not found")
        option_row = _lookup_paid_option_row(connection, normalized_option_code, include_hidden=True, include_archived=True)
        if option_row is None:
            raise NotFoundError("paid option not found")
        existing = _lookup_link_row(connection, int(tariff_row["id"]), int(option_row["id"]))
        if existing is None:
            raise NotFoundError("tariff option link not found")
        normalized_duration = (
            existing["included_duration_days"]
            if payload["included_duration_days"] is _UNSET
            else _normalize_int(payload["included_duration_days"], "included_duration_days", allow_none=True, minimum=0)
        )
        normalized_quantity = (
            existing["included_quantity"]
            if payload["included_quantity"] is _UNSET
            else _normalize_int(payload["included_quantity"], "included_quantity", allow_none=True, minimum=0)
        )
        return _upsert_tariff_option_link(
            connection,
            tariff_row,
            option_row,
            included_duration_days=normalized_duration,
            included_quantity=normalized_quantity,
        )


def detach_option_from_tariff(
    tariff_code: str,
    option_code: str,
    settings: Settings | None = None,
) -> bool:
    normalized_tariff_code = _normalize_code(tariff_code)
    normalized_option_code = _normalize_code(option_code)
    with _connection(settings) as connection:
        tariff_row = _lookup_tariff_row(connection, normalized_tariff_code, include_hidden=True, include_archived=True)
        if tariff_row is None:
            raise NotFoundError("tariff not found")
        option_row = _lookup_paid_option_row(connection, normalized_option_code, include_hidden=True, include_archived=True)
        if option_row is None:
            raise NotFoundError("paid option not found")
        cursor = connection.execute(
            "DELETE FROM tariff_options WHERE tariff_id = ? AND option_id = ?",
            (int(tariff_row["id"]), int(option_row["id"])),
        )
        return cursor.rowcount > 0


def upsert_tariff(
    *,
    code: str,
    title: str,
    price_amount_minor: int,
    currency: str = "RUB",
    description: str | None = None,
    status: str = "active",
    sort_order: int = 0,
    settings: Settings | None = None,
) -> TariffPublic:
    normalized_code = (code or "").strip().lower()
    with _connection(settings) as connection:
        row = connection.execute("SELECT * FROM tariffs WHERE code = ?", (normalized_code,)).fetchone()
        if row is not None:
            return _tariff_from_row(row)
    return create_tariff(
        code=code,
        title=title,
        price_amount_minor=price_amount_minor,
        currency=currency,
        description=description,
        status=status,
        sort_order=sort_order,
        settings=settings,
    )


def seed_initial_catalog(database_path: str | None = None, settings: Settings | None = None) -> None:
    resolved = _settings(settings)
    path = database_path or str(_database_path(resolved))
    initialize_database(path)
    with get_connection(path) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        now_iso = utc_now_iso()

        def upsert_option(
            code: str,
            title: str,
            description: str | None = None,
            price_amount_minor: int | None = None,
            default_duration_days: int | None = None,
            status: str = "active",
            is_renewable: int = 1,
            sort_order: int = 0,
        ) -> None:
            normalized_code = code.strip().lower()
            row = connection.execute("SELECT * FROM paid_options WHERE code = ?", (normalized_code,)).fetchone()
            if row is None:
                connection.execute(
                    """
                    INSERT INTO paid_options (
                        code, title, description, price_amount_minor, currency,
                        default_duration_days, status, is_renewable, sort_order,
                        created_at, updated_at
                    )
                    VALUES (?, ?, ?, ?, 'RUB', ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        normalized_code,
                        title,
                        description,
                        price_amount_minor,
                        default_duration_days,
                        status,
                        is_renewable,
                        sort_order,
                        now_iso,
                        now_iso,
                    ),
                )

        upsert_tariff(
            code=STARTER_TARIFF_CODE,
            title=STARTER_TARIFF_TITLE,
            description=STARTER_TARIFF_DESCRIPTION,
            price_amount_minor=499000,
            currency="RUB",
            status="active",
            sort_order=0,
            settings=resolved,
        )
        upsert_option(
            code="ai_gpt_tool",
            title="AI / GPT-инструмент",
            description="Базовый AI-инструмент для старта.",
            price_amount_minor=None,
            default_duration_days=None,
            status="active",
            is_renewable=1,
            sort_order=0,
        )
        upsert_option(
            code="server",
            title="Сервер",
            description="Серверная часть для базового рабочего окружения.",
            price_amount_minor=None,
            default_duration_days=None,
            status="active",
            is_renewable=1,
            sort_order=1,
        )
        upsert_option(
            code="vpn",
            title="VPN",
            description="Защищённый доступ для рабочих задач.",
            price_amount_minor=None,
            default_duration_days=None,
            status="active",
            is_renewable=1,
            sort_order=2,
        )
        _ensure_tariff_option_link(connection, STARTER_TARIFF_CODE, "ai_gpt_tool")
        _ensure_tariff_option_link(connection, STARTER_TARIFF_CODE, "server")
        _ensure_tariff_option_link(connection, STARTER_TARIFF_CODE, "vpn")


def _ensure_tariff_option_link(
    connection,
    tariff_code: str,
    option_code: str,
    included_duration_days: int | None = None,
    included_quantity: int | None = None,
) -> None:
    tariff_row = connection.execute("SELECT * FROM tariffs WHERE code = ?", (tariff_code,)).fetchone()
    option_row = connection.execute("SELECT * FROM paid_options WHERE code = ?", (option_code,)).fetchone()
    if tariff_row is None or option_row is None:
        return
    existing = connection.execute(
        "SELECT id FROM tariff_options WHERE tariff_id = ? AND option_id = ?",
        (int(tariff_row["id"]), int(option_row["id"])),
    ).fetchone()
    if existing is None:
        connection.execute(
            """
            INSERT INTO tariff_options (
                tariff_id, option_id, included_duration_days, included_quantity, created_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                int(tariff_row["id"]),
                int(option_row["id"]),
                included_duration_days,
                included_quantity,
                utc_now_iso(),
            ),
        )
