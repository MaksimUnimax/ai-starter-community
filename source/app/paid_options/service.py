"""Paid option catalog services."""

from __future__ import annotations

from app.core.config import Settings, get_settings
from app.shared.db import get_connection, get_database_path, initialize_database
from app.shared.utils import utc_now_iso

from .schemas import PaidOptionPublic


def _settings(settings: Settings | None = None) -> Settings:
    return settings or get_settings()


def _database_path(settings: Settings | None = None):
    return get_database_path(_settings(settings))


def _connection(settings: Settings | None = None):
    resolved = _settings(settings)
    path = _database_path(resolved)
    initialize_database(path)
    return get_connection(path)


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
            f"SELECT * FROM paid_options WHERE status IN ({placeholders}) ORDER BY sort_order ASC, id ASC",
            tuple(statuses),
        ).fetchall()
        return [_paid_option_from_row(row) for row in rows]


def get_paid_option_by_code(code: str, settings: Settings | None = None) -> PaidOptionPublic | None:
    normalized_code = (code or "").strip().lower()
    with _connection(settings) as connection:
        row = connection.execute("SELECT * FROM paid_options WHERE code = ?", (normalized_code,)).fetchone()
        return _paid_option_from_row(row) if row else None


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
    if not normalized_code:
        raise ValueError("paid option code is required")
    now_iso = utc_now_iso()
    with _connection(settings) as connection:
        row = connection.execute("SELECT * FROM paid_options WHERE code = ?", (normalized_code,)).fetchone()
        if row is None:
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
                    title,
                    description,
                    price_amount_minor,
                    currency,
                    default_duration_days,
                    status,
                    is_renewable,
                    sort_order,
                    now_iso,
                    now_iso,
                ),
            )
            row = connection.execute("SELECT * FROM paid_options WHERE id = ?", (cursor.lastrowid,)).fetchone()
        return _paid_option_from_row(row)


def archive_paid_option(code: str, settings: Settings | None = None) -> bool:
    normalized_code = (code or "").strip().lower()
    if not normalized_code:
        return False
    now_iso = utc_now_iso()
    with _connection(settings) as connection:
        cursor = connection.execute(
            "UPDATE paid_options SET status = ?, updated_at = ? WHERE code = ? AND status != ?",
            ("archived", now_iso, normalized_code, "archived"),
        )
        return cursor.rowcount > 0

