"""SQLite persistence helpers for the AI Starter Community MVP."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from app.core.config import Settings, database_path_from_settings

SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    login TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user',
    is_active INTEGER NOT NULL DEFAULT 1,
    email_verified_at TEXT NULL,
    materials_access_granted_at TEXT NULL,
    access_status TEXT NOT NULL DEFAULT 'not_activated',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_hash TEXT UNIQUE NOT NULL,
    created_at TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    revoked_at TEXT NULL
);

CREATE TABLE IF NOT EXISTS auth_tokens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_hash TEXT UNIQUE NOT NULL,
    token_type TEXT NOT NULL,
    target_email TEXT NULL,
    created_at TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    used_at TEXT NULL,
    revoked_at TEXT NULL
);

CREATE TABLE IF NOT EXISTS email_outbox (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipient_email TEXT NOT NULL,
    subject TEXT NOT NULL,
    body_text TEXT NOT NULL,
    template_key TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'queued',
    created_at TEXT NOT NULL,
    sent_at TEXT NULL,
    error TEXT NULL
);

CREATE TABLE IF NOT EXISTS account_blocks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type TEXT NOT NULL,
    title TEXT NOT NULL,
    login TEXT NOT NULL DEFAULT '',
    password_secret TEXT NOT NULL DEFAULT '',
    email TEXT NULL,
    status TEXT NOT NULL DEFAULT 'inactive',
    duration_days INTEGER NOT NULL DEFAULT 60,
    activated_at TEXT NULL,
    expires_at TEXT NULL,
    created_by_user_id INTEGER NULL REFERENCES users(id) ON DELETE SET NULL,
    updated_by_user_id INTEGER NULL REFERENCES users(id) ON DELETE SET NULL,
    activated_by_user_id INTEGER NULL REFERENCES users(id) ON DELETE SET NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    CHECK (type IN ('chatgpt', 'server', 'mail', 'vpn')),
    CHECK (status IN ('inactive', 'active', 'expired'))
);

CREATE INDEX IF NOT EXISTS idx_account_blocks_owner_user_id ON account_blocks(owner_user_id);
CREATE INDEX IF NOT EXISTS idx_account_blocks_owner_user_type ON account_blocks(owner_user_id, type);
CREATE INDEX IF NOT EXISTS idx_account_blocks_status ON account_blocks(status);

CREATE TABLE IF NOT EXISTS tariffs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    description TEXT NULL,
    price_amount_minor INTEGER NOT NULL,
    currency TEXT NOT NULL DEFAULT 'RUB',
    status TEXT NOT NULL DEFAULT 'active',
    show_on_homepage INTEGER NOT NULL DEFAULT 0,
    sort_order INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS paid_options (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    description TEXT NULL,
    price_amount_minor INTEGER NULL,
    currency TEXT NOT NULL DEFAULT 'RUB',
    default_duration_days INTEGER NULL,
    status TEXT NOT NULL DEFAULT 'active',
    is_renewable INTEGER NOT NULL DEFAULT 1,
    sort_order INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tariff_options (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tariff_id INTEGER NOT NULL REFERENCES tariffs(id) ON DELETE CASCADE,
    option_id INTEGER NOT NULL REFERENCES paid_options(id) ON DELETE CASCADE,
    included_duration_days INTEGER NULL,
    included_quantity INTEGER NULL,
    created_at TEXT NOT NULL,
    UNIQUE(tariff_id, option_id)
);
"""


def get_database_path(settings: Settings | None = None) -> Path:
    return database_path_from_settings(settings)


def ensure_database_parent_exists(path: Path | str) -> Path:
    db_path = Path(path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return db_path


def get_connection(path: Path | str) -> sqlite3.Connection:
    db_path = Path(path)
    connection = sqlite3.connect(str(db_path))
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database(path: Path | str) -> None:
    db_path = ensure_database_parent_exists(path)
    with sqlite3.connect(str(db_path)) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.executescript(SCHEMA_SQL)
        _ensure_account_blocks_type_vpn(connection)
        _ensure_users_materials_access_granted_at_column(connection)
        _ensure_tariffs_show_on_homepage_column(connection)


def _ensure_account_blocks_type_vpn(connection: sqlite3.Connection) -> None:
    row = connection.execute(
        "SELECT sql FROM sqlite_master WHERE type = 'table' AND name = 'account_blocks'",
    ).fetchone()
    schema_sql = str(row[0]) if row is not None and row[0] is not None else ""
    if "vpn" in schema_sql.lower():
        return

    connection.execute("PRAGMA foreign_keys = OFF")
    try:
        connection.executescript(
            """
            ALTER TABLE account_blocks RENAME TO account_blocks_legacy;

            CREATE TABLE account_blocks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                owner_user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                type TEXT NOT NULL,
                title TEXT NOT NULL,
                login TEXT NOT NULL DEFAULT '',
                password_secret TEXT NOT NULL DEFAULT '',
                email TEXT NULL,
                status TEXT NOT NULL DEFAULT 'inactive',
                duration_days INTEGER NOT NULL DEFAULT 60,
                activated_at TEXT NULL,
                expires_at TEXT NULL,
                created_by_user_id INTEGER NULL REFERENCES users(id) ON DELETE SET NULL,
                updated_by_user_id INTEGER NULL REFERENCES users(id) ON DELETE SET NULL,
                activated_by_user_id INTEGER NULL REFERENCES users(id) ON DELETE SET NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                CHECK (type IN ('chatgpt', 'server', 'mail', 'vpn')),
                CHECK (status IN ('inactive', 'active', 'expired'))
            );

            INSERT INTO account_blocks (
                id,
                owner_user_id,
                type,
                title,
                login,
                password_secret,
                email,
                status,
                duration_days,
                activated_at,
                expires_at,
                created_by_user_id,
                updated_by_user_id,
                activated_by_user_id,
                created_at,
                updated_at
            )
            SELECT
                id,
                owner_user_id,
                type,
                title,
                login,
                password_secret,
                email,
                status,
                duration_days,
                activated_at,
                expires_at,
                created_by_user_id,
                updated_by_user_id,
                activated_by_user_id,
                created_at,
                updated_at
            FROM account_blocks_legacy;

            DROP TABLE account_blocks_legacy;
            """
        )
        connection.executescript(
            """
            CREATE INDEX IF NOT EXISTS idx_account_blocks_owner_user_id ON account_blocks(owner_user_id);
            CREATE INDEX IF NOT EXISTS idx_account_blocks_owner_user_type ON account_blocks(owner_user_id, type);
            CREATE INDEX IF NOT EXISTS idx_account_blocks_status ON account_blocks(status);
            """
        )
    finally:
        connection.execute("PRAGMA foreign_keys = ON")


def _ensure_users_materials_access_granted_at_column(connection: sqlite3.Connection) -> None:
    columns = {
        row[1]
        for row in connection.execute("PRAGMA table_info(users)").fetchall()
    }
    if "materials_access_granted_at" not in columns:
        connection.execute("ALTER TABLE users ADD COLUMN materials_access_granted_at TEXT NULL")


def _ensure_tariffs_show_on_homepage_column(connection: sqlite3.Connection) -> None:
    columns = {
        row[1]
        for row in connection.execute("PRAGMA table_info(tariffs)").fetchall()
    }
    if "show_on_homepage" not in columns:
        connection.execute("ALTER TABLE tariffs ADD COLUMN show_on_homepage INTEGER NOT NULL DEFAULT 0")
