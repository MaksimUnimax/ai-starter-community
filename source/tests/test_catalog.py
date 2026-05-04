from __future__ import annotations

import sqlite3

from app.paid_options.service import archive_paid_option, get_paid_option_by_code, list_paid_options, upsert_paid_option
from app.shared.db import get_database_path, initialize_database
from app.tariffs.service import (
    STARTER_TARIFF_CODE,
    archive_tariff,
    get_tariff_by_code,
    list_tariff_options,
    list_tariffs,
    seed_initial_catalog,
    upsert_tariff,
)


def _connect(settings):
    conn = sqlite3.connect(str(get_database_path(settings)))
    conn.row_factory = sqlite3.Row
    return conn


def _fetch_one(settings, sql: str, params: tuple = ()):
    with _connect(settings) as conn:
        conn.row_factory = sqlite3.Row
        return conn.execute(sql, params).fetchone()


def _count(settings, table: str) -> int:
    with _connect(settings) as conn:
        return int(conn.execute(f"SELECT COUNT(*) AS c FROM {table}").fetchone()["c"])


def test_catalog_schema_exists(test_settings):
    initialize_database(get_database_path(test_settings))
    with _connect(test_settings) as conn:
        rows = conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'").fetchall()
    names = {row["name"] for row in rows}
    assert "tariffs" in names
    assert "paid_options" in names
    assert "tariff_options" in names


def test_seed_creates_starter_catalog_and_links(test_settings):
    seed_initial_catalog(settings=test_settings)

    tariff = get_tariff_by_code(STARTER_TARIFF_CODE, settings=test_settings)
    assert tariff is not None
    assert tariff.title == "Стартовый доступ"
    assert tariff.price_amount_minor == 499000
    assert tariff.currency == "RUB"
    assert tariff.status == "active"

    option_codes = {option.code for option in list_paid_options(settings=test_settings)}
    assert {"ai_gpt_tool", "server", "vpn"} <= option_codes

    tariff_option_codes = {row["code"] for row in list_tariff_options(STARTER_TARIFF_CODE, settings=test_settings)}
    assert tariff_option_codes == {"ai_gpt_tool", "server", "vpn"}


def test_seed_is_idempotent_and_does_not_duplicate_rows(test_settings):
    seed_initial_catalog(settings=test_settings)
    counts_before = {
        "tariffs": _count(test_settings, "tariffs"),
        "paid_options": _count(test_settings, "paid_options"),
        "tariff_options": _count(test_settings, "tariff_options"),
    }

    seed_initial_catalog(settings=test_settings)
    counts_after = {
        "tariffs": _count(test_settings, "tariffs"),
        "paid_options": _count(test_settings, "paid_options"),
        "tariff_options": _count(test_settings, "tariff_options"),
    }

    assert counts_before == counts_after
    assert counts_after["tariffs"] == 1
    assert counts_after["paid_options"] == 3
    assert counts_after["tariff_options"] == 3


def test_seed_does_not_overwrite_existing_manual_changes(test_settings):
    seed_initial_catalog(settings=test_settings)
    with _connect(test_settings) as conn:
        conn.execute(
            "UPDATE tariffs SET title = ?, price_amount_minor = ?, status = ? WHERE code = ?",
            ("Custom Tariff", 777000, "hidden", STARTER_TARIFF_CODE),
        )
        conn.execute(
            "UPDATE paid_options SET title = ?, price_amount_minor = ?, status = ? WHERE code = ?",
            ("Custom GPT", 123, "hidden", "ai_gpt_tool"),
        )
        conn.commit()

    seed_initial_catalog(settings=test_settings)

    tariff_row = _fetch_one(test_settings, "SELECT * FROM tariffs WHERE code = ?", (STARTER_TARIFF_CODE,))
    option_row = _fetch_one(test_settings, "SELECT * FROM paid_options WHERE code = ?", ("ai_gpt_tool",))
    assert tariff_row["title"] == "Custom Tariff"
    assert tariff_row["price_amount_minor"] == 777000
    assert tariff_row["status"] == "hidden"
    assert option_row["title"] == "Custom GPT"
    assert option_row["price_amount_minor"] == 123
    assert option_row["status"] == "hidden"


def test_list_tariffs_and_options_hide_non_active_by_default(test_settings):
    seed_initial_catalog(settings=test_settings)
    upsert_tariff(
        code="hidden_tariff",
        title="Hidden tariff",
        price_amount_minor=100,
        status="hidden",
        settings=test_settings,
    )
    upsert_paid_option(
        code="hidden_option",
        title="Hidden option",
        price_amount_minor=0,
        status="hidden",
        settings=test_settings,
    )

    tariffs = list_tariffs(settings=test_settings)
    paid_options = list_paid_options(settings=test_settings)
    assert all(tariff.status == "active" for tariff in tariffs)
    assert all(option.status == "active" for option in paid_options)
    assert "hidden_tariff" not in {tariff.code for tariff in tariffs}
    assert "hidden_option" not in {option.code for option in paid_options}


def test_lookup_by_code_is_generic(test_settings):
    seed_initial_catalog(settings=test_settings)
    upsert_tariff(
        code="custom_tariff",
        title="Custom tariff",
        price_amount_minor=123456,
        status="active",
        settings=test_settings,
    )
    upsert_paid_option(
        code="custom_option",
        title="Custom option",
        price_amount_minor=0,
        status="active",
        settings=test_settings,
    )

    tariff = get_tariff_by_code("custom_tariff", settings=test_settings)
    option = get_paid_option_by_code("custom_option", settings=test_settings)
    assert tariff is not None and tariff.title == "Custom tariff"
    assert option is not None and option.title == "Custom option"


def test_archive_helpers_change_status_without_deleting(test_settings):
    seed_initial_catalog(settings=test_settings)
    assert archive_tariff(STARTER_TARIFF_CODE, settings=test_settings) is True
    assert archive_paid_option("ai_gpt_tool", settings=test_settings) is True

    tariff = get_tariff_by_code(STARTER_TARIFF_CODE, settings=test_settings)
    option = get_paid_option_by_code("ai_gpt_tool", settings=test_settings)
    assert tariff is not None and tariff.status == "archived"
    assert option is not None and option.status == "archived"

    tariffs = list_tariffs(settings=test_settings)
    paid_options = list_paid_options(settings=test_settings)
    assert STARTER_TARIFF_CODE not in {item.code for item in tariffs}
    assert "ai_gpt_tool" not in {item.code for item in paid_options}


def test_existing_auth_tests_still_pass(client, test_settings):
    response = client.get("/register")
    assert response.status_code == 200
    assert "Регистрация" in response.text
