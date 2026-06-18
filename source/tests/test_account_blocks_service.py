from __future__ import annotations

import base64
import re
import sqlite3
from dataclasses import replace

import pytest

from app.account_blocks.schemas import AccountBlockCreateInput, AccountBlockUpdateInput
from app.account_blocks.service import (
    AccountBlockPermissionError,
    AccountBlockNotFoundError,
    AccountBlockValidationError,
    create_account_block,
    delete_account_block,
    get_account_block_copy_data,
    get_account_block_copy_data_map,
    get_account_block_public,
    list_account_blocks_for_viewer,
    renew_account_block,
    update_account_block,
)
from app.auth.service import authenticate_user, register_user, verify_email
from app.shared.db import get_database_path, initialize_database


def _encode_key(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def _connect(settings):
    conn = sqlite3.connect(str(get_database_path(settings)))
    conn.row_factory = sqlite3.Row
    return conn


def _extract_verify_token(settings, email: str) -> str:
    with _connect(settings) as conn:
        row = conn.execute(
            "SELECT body_text FROM email_outbox WHERE recipient_email = ? AND template_key = ? ORDER BY id DESC LIMIT 1",
            (email, "email_verification"),
        ).fetchone()
    assert row is not None
    match = re.search(r"/verify-email/([A-Za-z0-9_-]+)", row["body_text"])
    assert match
    return match.group(1)


def _create_verified_user(test_settings, email: str, login: str, role: str = "user"):
    register_user(
        email=email,
        login=login,
        password="Secret123",
        repeat_password="Secret123",
        settings=test_settings,
    )
    verify_email(_extract_verify_token(test_settings, email), settings=test_settings)
    if role != "user":
        with _connect(test_settings) as conn:
            conn.execute("UPDATE users SET role = ? WHERE email = ?", (role, email))
            conn.commit()
    return authenticate_user(email, "Secret123", settings=test_settings)


def test_account_blocks_table_and_supported_types_exist(test_settings):
    initialize_database(get_database_path(test_settings))
    with _connect(test_settings) as conn:
        tables = {
            row["name"]
            for row in conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'").fetchall()
        }
        assert "account_blocks" in tables
        columns = {
            row["name"]
            for row in conn.execute("PRAGMA table_info(account_blocks)").fetchall()
        }
    assert {
        "id",
        "owner_user_id",
        "type",
        "title",
        "login",
        "password_secret",
        "email",
        "status",
        "duration_days",
        "activated_at",
        "expires_at",
        "created_by_user_id",
        "updated_by_user_id",
        "activated_by_user_id",
        "created_at",
        "updated_at",
    }.issubset(columns)


def test_admin_and_moderator_can_create_update_list_and_delete_blocks_with_derived_titles(test_settings):
    admin = _create_verified_user(test_settings, "ab-admin@example.com", "abadmin", role="admin")
    moderator = _create_verified_user(test_settings, "ab-moderator@example.com", "abmoderator", role="moderator")
    owner = _create_verified_user(test_settings, "ab-owner@example.com", "abowner")
    other_owner = _create_verified_user(test_settings, "ab-owner-2@example.com", "abowner2")

    admin_block = create_account_block(
        actor=admin,
        data=AccountBlockCreateInput(
            owner_user_id=owner.id,
            type="chatgpt",
            title="Ignored title",
            login="chat-login",
            password_secret="chat-secret",
            email="ignored@example.com",
            duration_days=45,
        ),
        settings=test_settings,
    )
    with _connect(test_settings) as conn:
        admin_row = conn.execute("SELECT * FROM account_blocks WHERE id = ?", (admin_block.id,)).fetchone()
    assert admin_row is not None
    assert admin_row["password_secret"].startswith("enc:v1:")
    assert "chat-secret" not in admin_row["password_secret"]
    moderator_block = create_account_block(
        actor=moderator,
        data=AccountBlockCreateInput(
            owner_user_id=other_owner.id,
            type="mail",
            title="Ignored mail title",
            login="mail-login",
            password_secret="mail-secret",
            email="ignored-mail@example.com",
        ),
        settings=test_settings,
    )
    with _connect(test_settings) as conn:
        moderator_row = conn.execute("SELECT * FROM account_blocks WHERE id = ?", (moderator_block.id,)).fetchone()
    assert moderator_row is not None
    assert moderator_row["password_secret"].startswith("enc:v1:")
    assert "mail-secret" not in moderator_row["password_secret"]

    assert admin_block.owner_user_id == owner.id
    assert admin_block.title == "ChatGPT"
    assert admin_block.email is None
    assert admin_block.duration_days == 45
    assert moderator_block.owner_user_id == other_owner.id
    assert moderator_block.title == "Почта"
    assert moderator_block.email == other_owner.email

    updated_block = update_account_block(
        actor=moderator,
        block_id=admin_block.id,
        data=AccountBlockUpdateInput(
            owner_user_id=other_owner.id,
            type="mail",
            title="Should be ignored",
            login="new-login",
            password_secret="new-secret",
            email="new-owner@example.com",
            duration_days=10,
        ),
        settings=test_settings,
    )
    with _connect(test_settings) as conn:
        updated_row = conn.execute("SELECT * FROM account_blocks WHERE id = ?", (admin_block.id,)).fetchone()
    assert updated_row is not None
    assert updated_row["password_secret"].startswith("enc:v1:")
    assert "new-secret" not in updated_row["password_secret"]
    assert updated_block.owner_user_id == owner.id
    assert updated_block.type == "chatgpt"
    assert updated_block.title == "ChatGPT"
    assert updated_block.login == "new-login"
    assert updated_block.email is None

    all_blocks = list_account_blocks_for_viewer(admin, settings=test_settings)
    assert {block.id for block in all_blocks} == {admin_block.id, moderator_block.id}

    owner_blocks = list_account_blocks_for_viewer(owner, settings=test_settings)
    assert [block.id for block in owner_blocks] == [admin_block.id]

    copy_data = get_account_block_copy_data(actor=other_owner, block_id=moderator_block.id, settings=test_settings)
    assert copy_data.login == "mail-login"
    assert copy_data.password_secret == "mail-secret"
    assert copy_data.email == other_owner.email

    get_account_block_public(actor=admin, block_id=admin_block.id, settings=test_settings)

    delete_account_block(actor=admin, block_id=moderator_block.id, settings=test_settings)
    with _connect(test_settings) as conn:
        deleted = conn.execute("SELECT 1 FROM account_blocks WHERE id = ?", (moderator_block.id,)).fetchone()
    assert deleted is None


def test_user_can_only_view_own_blocks_and_cannot_manage(test_settings):
    admin = _create_verified_user(test_settings, "ab-admin-2@example.com", "abadmin2", role="admin")
    owner = _create_verified_user(test_settings, "ab-viewer@example.com", "abviewer")
    other_owner = _create_verified_user(test_settings, "ab-other@example.com", "abother")
    block = create_account_block(
        actor=admin,
        data=AccountBlockCreateInput(
            owner_user_id=owner.id,
            type="mail",
            title="Ignored mail title",
            login="mail-login",
            password_secret="mail-secret",
            email="ignored@example.com",
        ),
        settings=test_settings,
    )
    create_account_block(
        actor=admin,
        data=AccountBlockCreateInput(
            owner_user_id=other_owner.id,
            type="server",
            login="other-login",
            password_secret="other-secret",
        ),
        settings=test_settings,
    )

    own_blocks = list_account_blocks_for_viewer(owner, settings=test_settings)
    assert [item.id for item in own_blocks] == [block.id]
    assert own_blocks[0].status == "inactive"
    assert own_blocks[0].title == "Почта"
    assert own_blocks[0].activation_summary == "Не активирован"

    own_copy = get_account_block_copy_data(actor=owner, block_id=block.id, settings=test_settings)
    assert own_copy.login == "mail-login"
    assert own_copy.password_secret == "mail-secret"
    assert own_copy.email == owner.email

    with pytest.raises(AccountBlockPermissionError):
        create_account_block(
            actor=owner,
            data=AccountBlockCreateInput(
                owner_user_id=owner.id,
                type="chatgpt",
                login="x",
                password_secret="y",
            ),
            settings=test_settings,
        )
    with pytest.raises(AccountBlockPermissionError):
        update_account_block(
            actor=owner,
            block_id=block.id,
            data=AccountBlockUpdateInput(login="Denied"),
            settings=test_settings,
        )
    with pytest.raises(AccountBlockPermissionError):
        delete_account_block(actor=owner, block_id=block.id, settings=test_settings)
    with pytest.raises(AccountBlockPermissionError):
        renew_account_block(actor=owner, block_id=block.id, settings=test_settings)
    with pytest.raises(AccountBlockPermissionError):
        get_account_block_public(actor=other_owner, block_id=block.id, settings=test_settings)
    with pytest.raises(AccountBlockPermissionError):
        get_account_block_copy_data(actor=other_owner, block_id=block.id, settings=test_settings)


def test_bulk_account_block_copy_data_uses_single_block_lookup_and_preserves_owner_email(test_settings, monkeypatch):
    admin = _create_verified_user(test_settings, "ab-bulk-admin@example.com", "abbulkadmin", role="admin")
    owner = _create_verified_user(test_settings, "ab-bulk-owner@example.com", "abbulkowner")

    mail_block = create_account_block(
        actor=admin,
        data=AccountBlockCreateInput(
            owner_user_id=owner.id,
            type="mail",
            login="mail-login",
            password_secret="mail-secret",
            email="ignored@example.com",
        ),
        settings=test_settings,
    )
    server_block = create_account_block(
        actor=admin,
        data=AccountBlockCreateInput(
            owner_user_id=owner.id,
            type="server",
            login="server-login",
            password_secret="server-secret",
        ),
        settings=test_settings,
    )
    chatgpt_block = create_account_block(
        actor=admin,
        data=AccountBlockCreateInput(
            owner_user_id=owner.id,
            type="chatgpt",
            login="chat-login",
            password_secret="chat-secret",
        ),
        settings=test_settings,
    )

    def _unexpected_owner_lookup(*_args, **_kwargs):
        raise AssertionError("unexpected per-row owner lookup")

    monkeypatch.setattr("app.account_blocks.service._fetch_user_row", _unexpected_owner_lookup)

    copy_data_by_id = get_account_block_copy_data_map(
        block_ids=[mail_block.id, server_block.id, chatgpt_block.id],
        owner_email=owner.email,
        settings=test_settings,
    )

    assert copy_data_by_id[mail_block.id].login == "mail-login"
    assert copy_data_by_id[mail_block.id].password_secret == "mail-secret"
    assert copy_data_by_id[mail_block.id].email == owner.email
    assert copy_data_by_id[server_block.id].login == "server-login"
    assert copy_data_by_id[server_block.id].password_secret == "server-secret"
    assert copy_data_by_id[server_block.id].email is None
    assert copy_data_by_id[chatgpt_block.id].login == "chat-login"
    assert copy_data_by_id[chatgpt_block.id].password_secret == "chat-secret"
    assert copy_data_by_id[chatgpt_block.id].email is None


def test_admin_account_block_list_uses_stored_mail_email_when_bulk_owner_lookup_missing(
    test_settings,
    monkeypatch,
):
    admin = _create_verified_user(test_settings, "ab-missing-owner-admin@example.com", "abmissingowneradmin", role="admin")
    owner = _create_verified_user(test_settings, "ab-missing-owner@example.com", "abmissingowner")

    mail_block = create_account_block(
        actor=admin,
        data=AccountBlockCreateInput(
            owner_user_id=owner.id,
            type="mail",
            login="mail-login",
            password_secret="mail-secret",
        ),
        settings=test_settings,
    )
    server_block = create_account_block(
        actor=admin,
        data=AccountBlockCreateInput(
            owner_user_id=owner.id,
            type="server",
            login="server-login",
            password_secret="server-secret",
        ),
        settings=test_settings,
    )

    def _unexpected_owner_lookup(*_args, **_kwargs):
        raise AssertionError("unexpected per-row owner lookup")

    monkeypatch.setattr("app.account_blocks.service._fetch_user_row", _unexpected_owner_lookup)
    monkeypatch.setattr("app.account_blocks.service._fetch_user_rows_by_ids", lambda *_args, **_kwargs: {})

    blocks = list_account_blocks_for_viewer(admin, settings=test_settings)
    blocks_by_id = {block.id: block for block in blocks}

    assert set(blocks_by_id) == {mail_block.id, server_block.id}
    assert blocks_by_id[mail_block.id].email == owner.email
    assert blocks_by_id[mail_block.id].can_copy_email is True
    assert blocks_by_id[server_block.id].email is None


def test_invalid_account_block_payloads_are_rejected(test_settings):
    admin = _create_verified_user(test_settings, "ab-admin-3@example.com", "abadmin3", role="admin")
    with pytest.raises(AccountBlockValidationError):
        create_account_block(
            actor=admin,
            data=AccountBlockCreateInput(
                owner_user_id=0,
                type="chatgpt",
                login="login",
                password_secret="secret",
            ),
            settings=test_settings,
        )
    with pytest.raises(AccountBlockValidationError):
        create_account_block(
            actor=admin,
            data=AccountBlockCreateInput(
                owner_user_id=admin.id,
                type="unknown",
                login="login",
                password_secret="secret",
            ),
            settings=test_settings,
        )
    with pytest.raises(AccountBlockNotFoundError):
        get_account_block_public(actor=admin, block_id=99999, settings=test_settings)


def test_password_secret_round_trips_through_encrypted_storage_and_legacy_plaintext_rows_still_read(test_settings):
    admin = _create_verified_user(test_settings, "ab-encrypt-admin@example.com", "abencryptadmin", role="admin")
    owner = _create_verified_user(test_settings, "ab-encrypt-owner@example.com", "abencryptowner")

    encrypted_block = create_account_block(
        actor=admin,
        data=AccountBlockCreateInput(
            owner_user_id=owner.id,
            type="server",
            login="encrypted-login",
            password_secret="encrypted-secret",
        ),
        settings=test_settings,
    )
    with _connect(test_settings) as conn:
        encrypted_row = conn.execute("SELECT * FROM account_blocks WHERE id = ?", (encrypted_block.id,)).fetchone()
    assert encrypted_row is not None
    assert encrypted_row["password_secret"].startswith("enc:v1:")
    assert "encrypted-secret" not in encrypted_row["password_secret"]

    copy_data = get_account_block_copy_data(actor=owner, block_id=encrypted_block.id, settings=test_settings)
    assert copy_data.password_secret == "encrypted-secret"

    with _connect(test_settings) as conn:
        conn.execute(
            """
            INSERT INTO account_blocks (
                owner_user_id, type, title, login, password_secret, email,
                status, duration_days, activated_at, expires_at,
                created_by_user_id, updated_by_user_id, activated_by_user_id,
                created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, NULL, NULL, ?, ?, NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            """,
            (
                owner.id,
                "server",
                "Сервер",
                "legacy-login",
                "legacy-secret",
                None,
                "inactive",
                60,
                admin.id,
                admin.id,
            ),
        )
        legacy_row = conn.execute(
            "SELECT id FROM account_blocks WHERE login = ? ORDER BY id DESC LIMIT 1",
            ("legacy-login",),
        ).fetchone()
    assert legacy_row is not None
    legacy_copy = get_account_block_copy_data(actor=owner, block_id=int(legacy_row["id"]), settings=test_settings)
    assert legacy_copy.password_secret == "legacy-secret"


def test_empty_password_secret_stays_empty_without_encryption(test_settings):
    admin = _create_verified_user(test_settings, "ab-empty-admin@example.com", "abemptyadmin", role="admin")
    owner = _create_verified_user(test_settings, "ab-empty-owner@example.com", "abemptyowner")

    block = create_account_block(
        actor=admin,
        data=AccountBlockCreateInput(
            owner_user_id=owner.id,
            type="mail",
            login="empty-login",
            password_secret="",
        ),
        settings=test_settings,
    )
    with _connect(test_settings) as conn:
        row = conn.execute("SELECT * FROM account_blocks WHERE id = ?", (block.id,)).fetchone()
    assert row is not None
    assert row["password_secret"] == ""
    copy_data = get_account_block_copy_data(actor=owner, block_id=block.id, settings=test_settings)
    assert copy_data.password_secret == ""


def test_missing_password_secret_key_blocks_new_secret_write(test_settings):
    admin = _create_verified_user(test_settings, "ab-missing-key-admin@example.com", "abmissingkeyadmin", role="admin")
    owner = _create_verified_user(test_settings, "ab-missing-key-owner@example.com", "abmissingkeyowner")
    missing_key_settings = replace(test_settings, account_blocks_password_secret_key=None)

    with pytest.raises(AccountBlockValidationError):
        create_account_block(
            actor=admin,
            data=AccountBlockCreateInput(
                owner_user_id=owner.id,
                type="chatgpt",
                login="missing-key-login",
                password_secret="missing-key-secret",
            ),
            settings=missing_key_settings,
        )


def test_malformed_and_wrong_key_encrypted_password_secret_fail_closed_on_read(test_settings):
    admin = _create_verified_user(test_settings, "ab-bad-admin@example.com", "abbadadmin", role="admin")
    owner = _create_verified_user(test_settings, "ab-bad-owner@example.com", "abbadowner")

    block = create_account_block(
        actor=admin,
        data=AccountBlockCreateInput(
            owner_user_id=owner.id,
            type="server",
            login="bad-login",
            password_secret="bad-secret",
        ),
        settings=test_settings,
    )

    wrong_key_settings = replace(
        test_settings,
        account_blocks_password_secret_key=_encode_key(b"fedcba9876543210fedcba9876543210"),
    )
    with pytest.raises(AccountBlockValidationError):
        get_account_block_copy_data(actor=owner, block_id=block.id, settings=wrong_key_settings)

    with _connect(test_settings) as conn:
        conn.execute(
            "UPDATE account_blocks SET password_secret = ? WHERE id = ?",
            ("enc:v1:invalid.invalid", block.id),
        )

    with pytest.raises(AccountBlockValidationError):
        get_account_block_copy_data(actor=owner, block_id=block.id, settings=test_settings)
