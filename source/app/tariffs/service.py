"""Tariff catalog services and seed helpers."""

from __future__ import annotations

from app.core.config import Settings, get_settings
from app.shared.db import get_connection, get_database_path, initialize_database
from app.shared.utils import utc_now_iso

from .schemas import TariffPublic


STARTER_TARIFF_CODE = "starter_4990_rub"
STARTER_TARIFF_TITLE = "Стартовый доступ"
STARTER_TARIFF_DESCRIPTION = "Базовый тариф для старта работы с сервисом."


def _settings(settings: Settings | None = None) -> Settings:
    return settings or get_settings()


def _database_path(settings: Settings | None = None):
    return get_database_path(_settings(settings))


def _connection(settings: Settings | None = None):
    resolved = _settings(settings)
    path = _database_path(resolved)
    initialize_database(path)
    return get_connection(path)


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


def _option_row_from_code(connection, code: str):
    return connection.execute("SELECT * FROM paid_options WHERE code = ?", (code,)).fetchone()


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
            f"SELECT * FROM tariffs WHERE status IN ({placeholders}) ORDER BY sort_order ASC, id ASC",
            tuple(statuses),
        ).fetchall()
        return [_tariff_from_row(row) for row in rows]


def get_tariff_by_code(code: str, settings: Settings | None = None) -> TariffPublic | None:
    with _connection(settings) as connection:
        row = connection.execute("SELECT * FROM tariffs WHERE code = ?", ((code or "").strip().lower(),)).fetchone()
        return _tariff_from_row(row) if row else None


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
    if not normalized_code:
        raise ValueError("tariff code is required")
    now_iso = utc_now_iso()
    with _connection(settings) as connection:
        row = connection.execute("SELECT * FROM tariffs WHERE code = ?", (normalized_code,)).fetchone()
        if row is None:
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
                    title,
                    description,
                    price_amount_minor,
                    currency,
                    status,
                    sort_order,
                    now_iso,
                    now_iso,
                ),
            )
            row = connection.execute("SELECT * FROM tariffs WHERE id = ?", (cursor.lastrowid,)).fetchone()
        return _tariff_from_row(row)


def archive_tariff(code: str, settings: Settings | None = None) -> bool:
    normalized_code = (code or "").strip().lower()
    if not normalized_code:
        return False
    now_iso = utc_now_iso()
    with _connection(settings) as connection:
        cursor = connection.execute(
            "UPDATE tariffs SET status = ?, updated_at = ? WHERE code = ? AND status != ?",
            ("archived", now_iso, normalized_code, "archived"),
        )
        return cursor.rowcount > 0


def list_tariff_options(tariff_code: str, settings: Settings | None = None) -> list[dict]:
    normalized_code = (tariff_code or "").strip().lower()
    with _connection(settings) as connection:
        rows = connection.execute(
            """
            SELECT
                po.*,
                topt.included_duration_days,
                topt.included_quantity,
                topt.created_at AS link_created_at
            FROM tariff_options AS topt
            JOIN tariffs AS t ON t.id = topt.tariff_id
            JOIN paid_options AS po ON po.id = topt.option_id
            WHERE t.code = ?
            ORDER BY po.sort_order ASC, po.id ASC
            """,
            (normalized_code,),
        ).fetchall()
        return [dict(row) for row in rows]


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
            option_rows = connection.execute(
                """
                SELECT
                    po.*,
                    topt.included_duration_days,
                    topt.included_quantity,
                    topt.created_at AS link_created_at
                FROM tariff_options AS topt
                JOIN paid_options AS po ON po.id = topt.option_id
                WHERE topt.tariff_id = ?
                  AND po.status = 'active'
                ORDER BY po.sort_order ASC, po.id ASC, po.code ASC
                """,
                (int(tariff_row["id"]),),
            ).fetchall()
            tariff_payload = dict(tariff_row)
            tariff_payload["options"] = [dict(option_row) for option_row in option_rows]
            result.append(tariff_payload)
        return result


def _ensure_tariff_option_link(
    connection,
    tariff_code: str,
    option_code: str,
    included_duration_days: int | None = None,
    included_quantity: int | None = None,
) -> None:
    tariff_row = connection.execute("SELECT * FROM tariffs WHERE code = ?", (tariff_code,)).fetchone()
    option_row = _option_row_from_code(connection, option_code)
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
