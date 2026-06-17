from __future__ import annotations

from pathlib import Path

from app.shared.db import SQLITE_BUSY_TIMEOUT_MS, get_connection, initialize_database


def test_file_backed_sqlite_connections_enable_busy_timeout_and_wal(test_settings):
    db_path = Path(test_settings.database_path)
    initialize_database(db_path)

    with get_connection(db_path) as connection:
        busy_timeout = connection.execute("PRAGMA busy_timeout").fetchone()[0]
        journal_mode = connection.execute("PRAGMA journal_mode").fetchone()[0]

    assert int(busy_timeout) == SQLITE_BUSY_TIMEOUT_MS
    assert str(journal_mode).lower() == "wal"


def test_in_memory_sqlite_connections_keep_busy_timeout_without_forcing_wal():
    initialize_database(":memory:")

    with get_connection(":memory:") as connection:
        busy_timeout = connection.execute("PRAGMA busy_timeout").fetchone()[0]
        journal_mode = connection.execute("PRAGMA journal_mode").fetchone()[0]

    assert int(busy_timeout) == SQLITE_BUSY_TIMEOUT_MS
    assert str(journal_mode).lower() != "wal"
