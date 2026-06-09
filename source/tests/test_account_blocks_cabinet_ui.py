from __future__ import annotations

import re
import sqlite3
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

from app.account_blocks.schemas import AccountBlockCreateInput
from app.account_blocks.service import activate_account_block, create_account_block
from app.auth.service import authenticate_user, create_session, register_user, verify_email


def _connect(settings):
    conn = sqlite3.connect(str(settings.database_path))
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


def _login_as(client, test_settings, email: str):
    user = authenticate_user(email, "Secret123", settings=test_settings)
    client.cookies.set(test_settings.session_cookie_name, create_session(user.id, settings=test_settings))
    return user


def _extract_accounts_section(body_text: str) -> str:
    start_marker = '<section class="card stack accounts-card" data-local-accounts-root data-account-blocks-source="server">'
    end_marker = '\n  <section class="card stack prompts-library-card" data-prompts-library-root>'
    start = body_text.find(start_marker)
    end = body_text.find(end_marker, start)
    assert start != -1
    assert end != -1
    return body_text[start:end]


def _extract_builder_shell(accounts_section: str) -> str:
    start_marker = '<div class="accounts-builder-shell">'
    end_marker = '<p class="accounts-notice"'
    start = accounts_section.find(start_marker)
    end = accounts_section.find(end_marker, start)
    assert start != -1
    assert end != -1
    return accounts_section[start:end]


def _extract_first_edit_form(accounts_section: str) -> str:
    start_marker = '<form class="account-card__edit-form"'
    start = accounts_section.find(start_marker)
    assert start != -1
    end = accounts_section.find("</form>", start)
    assert end != -1
    return accounts_section[start:end]


def test_user_sees_compact_server_backed_account_blocks_and_copy_only_controls(client, test_settings):
    admin = _create_verified_user(test_settings, "cab-ui-admin@example.com", "cabuiadmin", role="admin")
    owner = _create_verified_user(test_settings, "cab-ui-owner@example.com", "cabuiowner")

    active_block = create_account_block(
        actor=admin,
        data=AccountBlockCreateInput(
            owner_user_id=owner.id,
            type="chatgpt",
            login="owner-chat-login",
            password_secret="owner-chat-password",
        ),
        settings=test_settings,
    )
    create_account_block(
        actor=admin,
        data=AccountBlockCreateInput(
            owner_user_id=owner.id,
            type="mail",
            login="owner-mail-login",
            password_secret="owner-mail-password",
        ),
        settings=test_settings,
    )

    fixed_now = datetime(2026, 6, 8, 12, 0, 0, tzinfo=timezone.utc)
    with patch("app.account_blocks.service.utc_now", return_value=fixed_now):
        activate_account_block(actor=admin, block_id=active_block.id, settings=test_settings)

    _login_as(client, test_settings, owner.email)
    with patch("app.account_blocks.service.utc_now", return_value=fixed_now):
        response = client.get("/cabinet")

    assert response.status_code == 200
    assert "/static/cabinet-local-accounts.js" in response.text
    assert "data-account-blocks-source=\"server\"" in response.text

    accounts_section = _extract_accounts_section(response.text)
    assert "Данные хранятся на сервере и доступны после входа в кабинет с любого устройства." in accounts_section
    assert "Данные сохраняются только в этом браузере." not in accounts_section
    assert "Добавить блок" not in accounts_section
    assert "Редактировать" not in accounts_section
    assert "Удалить" not in accounts_section
    assert "Активировать" not in accounts_section
    assert 'name="title"' not in accounts_section
    assert 'name="email"' not in accounts_section
    assert "data-account-card-edit-form" not in accounts_section
    assert "Скопировать" in accounts_section
    assert "ChatGPT" in accounts_section
    assert "Почта" in accounts_section
    assert "Активен: день 1 из 60" in accounts_section
    assert "Не активирован" in accounts_section
    assert "Срок завершён: 60 из 60 дней" not in accounts_section
    assert "Осталось после активации" not in accounts_section
    assert "Владелец:" not in accounts_section
    assert "account-owner-group__title" not in accounts_section
    assert "account-owner-group__meta" not in accounts_section
    assert "account-card__owner-line" not in accounts_section
    assert "Срок действия" not in accounts_section


def test_admin_can_create_edit_activate_and_delete_account_blocks(client, test_settings):
    admin = _create_verified_user(test_settings, "cab-ui-admin-2@example.com", "cabuiadmin2", role="admin")
    owner_a = _create_verified_user(test_settings, "cab-ui-owner-a@example.com", "cabuiownera")
    owner_b = _create_verified_user(test_settings, "cab-ui-owner-b@example.com", "cabuiownerb")
    _login_as(client, test_settings, admin.email)

    cabinet_response = client.get(f"/cabinet?owner_id={owner_a.id}")
    assert cabinet_response.status_code == 200
    assert "Администратор и модератор могут управлять блоками всех пользователей." in cabinet_response.text
    accounts_section = _extract_accounts_section(cabinet_response.text)
    builder_shell = _extract_builder_shell(accounts_section)
    assert "Добавить блок" in builder_shell
    assert "Владелец" not in builder_shell
    assert 'name="owner_user_id"' not in builder_shell
    assert 'name="type"' in builder_shell
    assert 'name="login"' in builder_shell
    assert 'name="password_secret"' in builder_shell
    assert 'name="title"' not in builder_shell
    assert 'name="email"' not in builder_shell
    assert f'action="/cabinet/account-blocks?owner_id={owner_a.id}"' in builder_shell
    assert "Сохранить" not in builder_shell
    assert "Удалить" not in builder_shell
    assert "Активировать" not in builder_shell

    create_response = client.post(
        f"/cabinet/account-blocks?owner_id={owner_a.id}",
        data={
            "type": "server",
            "login": "admin-block-login",
            "password_secret": "admin-block-password",
        },
        follow_redirects=False,
    )
    assert create_response.status_code == 303
    assert create_response.headers["location"] == f"/cabinet?account_blocks_notice=created&owner_id={owner_a.id}"

    with _connect(test_settings) as conn:
        row = conn.execute("SELECT * FROM account_blocks WHERE login = ?", ("admin-block-login",)).fetchone()
    assert row is not None
    block_id = int(row["id"])
    assert row["title"] == "Сервер"
    assert int(row["owner_user_id"]) == owner_a.id
    assert row["type"] == "server"
    assert row["email"] is None

    update_response = client.post(
        f"/cabinet/account-blocks/{block_id}",
        data={
            "type": "mail",
            "title": "Should be ignored",
            "login": "updated-login",
            "password_secret": "updated-password",
            "email": "updated@example.com",
        },
        follow_redirects=False,
    )
    assert update_response.status_code == 303
    assert update_response.headers["location"] == f"/cabinet?account_blocks_notice=updated&owner_id={owner_a.id}"

    fixed_now = datetime(2026, 6, 8, 12, 0, 0, tzinfo=timezone.utc)
    with patch("app.account_blocks.service.utc_now", return_value=fixed_now):
        activate_response = client.post(f"/cabinet/account-blocks/{block_id}/activate", follow_redirects=False)
    assert activate_response.status_code == 303
    assert activate_response.headers["location"] == f"/cabinet?account_blocks_notice=activated&owner_id={owner_a.id}"

    with _connect(test_settings) as conn:
        updated_row = conn.execute("SELECT * FROM account_blocks WHERE id = ?", (block_id,)).fetchone()
    assert updated_row is not None
    assert int(updated_row["owner_user_id"]) == owner_a.id
    assert updated_row["type"] == "server"
    assert updated_row["title"] == "Сервер"
    assert updated_row["login"] == "updated-login"
    assert updated_row["password_secret"] == "updated-password"
    assert updated_row["email"] is None
    assert updated_row["status"] == "active"
    assert updated_row["activated_at"] == fixed_now.isoformat()
    assert updated_row["expires_at"] == (fixed_now + timedelta(days=60)).isoformat()

    with patch("app.account_blocks.service.utc_now", return_value=fixed_now):
        active_page = client.get("/cabinet")
    accounts_section = _extract_accounts_section(active_page.text)
    assert "Редактировать" in accounts_section
    assert "Удалить" in accounts_section
    assert "Активировать" in accounts_section
    assert "Сервер" in accounts_section
    assert "account-owner-group__title" not in accounts_section
    assert "account-owner-group__meta" not in accounts_section
    assert "account-card__owner-line" not in accounts_section
    assert "Владелец:" not in accounts_section
    assert "Срок действия" not in accounts_section
    assert '<div class="account-actions account-actions--view">' in accounts_section
    assert f'<form class="account-action-form" method="post" action="/cabinet/account-blocks/{block_id}/delete">' in accounts_section
    assert f'<form class="account-action-form" method="post" action="/cabinet/account-blocks/{block_id}/activate">' in accounts_section
    assert "formaction=" not in accounts_section
    edit_form = _extract_first_edit_form(accounts_section)
    assert 'name="login"' in edit_form
    assert 'name="password_secret"' in edit_form
    assert 'name="title"' not in edit_form
    assert 'name="owner_user_id"' not in edit_form
    assert 'name="type"' not in edit_form
    assert 'name="email"' not in edit_form
    assert "data-account-card-edit-form" in edit_form
    assert 'hidden' in edit_form
    assert "Активен: день 1 из 60" in accounts_section

    delete_response = client.post(f"/cabinet/account-blocks/{block_id}/delete", follow_redirects=False)
    assert delete_response.status_code == 303
    assert delete_response.headers["location"] == f"/cabinet?account_blocks_notice=deleted&owner_id={owner_a.id}"

    with _connect(test_settings) as conn:
        deleted_row = conn.execute("SELECT 1 FROM account_blocks WHERE id = ?", (block_id,)).fetchone()
    assert deleted_row is None


def test_moderator_can_manage_account_blocks_but_cannot_access_admin_dashboard(client, test_settings):
    moderator = _create_verified_user(test_settings, "cab-ui-moderator@example.com", "cabuimoderator", role="moderator")
    owner = _create_verified_user(test_settings, "cab-ui-moderator-owner@example.com", "cabuimoderatorowner")
    _login_as(client, test_settings, moderator.email)

    admin_response = client.get("/admin")
    assert admin_response.status_code == 403

    create_response = client.post(
        f"/cabinet/account-blocks?owner_id={owner.id}",
        data={
            "type": "chatgpt",
            "login": "moderator-login",
            "password_secret": "moderator-password",
        },
        follow_redirects=False,
    )
    assert create_response.status_code == 303

    with _connect(test_settings) as conn:
        row = conn.execute("SELECT * FROM account_blocks WHERE login = ?", ("moderator-login",)).fetchone()
    assert row is not None
    block_id = int(row["id"])

    update_response = client.post(
        f"/cabinet/account-blocks/{block_id}",
        data={
            "type": "server",
            "title": "Ignored title",
            "login": "moderator-login-updated",
            "password_secret": "moderator-password-updated",
            "email": "ignored@example.com",
        },
        follow_redirects=False,
    )
    assert update_response.status_code == 303

    fixed_now = datetime(2026, 6, 8, 12, 0, 0, tzinfo=timezone.utc)
    with patch("app.account_blocks.service.utc_now", return_value=fixed_now):
        activate_response = client.post(f"/cabinet/account-blocks/{block_id}/activate", follow_redirects=False)
    assert activate_response.status_code == 303

    delete_response = client.post(f"/cabinet/account-blocks/{block_id}/delete", follow_redirects=False)
    assert delete_response.status_code == 303


def test_regular_user_cannot_post_account_block_management_actions(client, test_settings):
    admin = _create_verified_user(test_settings, "cab-ui-deny-admin@example.com", "cabuidenyadmin", role="admin")
    owner = _create_verified_user(test_settings, "cab-ui-deny-owner@example.com", "cabuidenyowner")
    block = create_account_block(
        actor=admin,
        data=AccountBlockCreateInput(
            owner_user_id=owner.id,
            type="server",
            login="denied-login",
            password_secret="denied-password",
        ),
        settings=test_settings,
    )

    _login_as(client, test_settings, owner.email)

    create_response = client.post(
        "/cabinet/account-blocks",
        data={
            "type": "chatgpt",
            "login": "nope",
            "password_secret": "nope",
        },
    )
    assert create_response.status_code == 403

    update_response = client.post(
        f"/cabinet/account-blocks/{block.id}",
        data={
            "type": "server",
            "title": "Should not update",
            "login": "nope",
            "password_secret": "nope",
            "email": "nope@example.com",
        },
    )
    assert update_response.status_code == 403

    delete_response = client.post(f"/cabinet/account-blocks/{block.id}/delete")
    assert delete_response.status_code == 403

    activate_response = client.post(f"/cabinet/account-blocks/{block.id}/activate")
    assert activate_response.status_code == 403


def test_expired_account_block_shows_finished_day_counter_without_active_label(client, test_settings):
    admin = _create_verified_user(test_settings, "cab-ui-expire-admin@example.com", "cabuiexpireadmin", role="admin")
    owner = _create_verified_user(test_settings, "cab-ui-expire-owner@example.com", "cabuiexpireowner")
    block = create_account_block(
        actor=admin,
        data=AccountBlockCreateInput(
            owner_user_id=owner.id,
            type="mail",
            login="expire-login",
            password_secret="expire-password",
        ),
        settings=test_settings,
    )

    activation_now = datetime(2026, 6, 8, 12, 0, 0, tzinfo=timezone.utc)
    expired_now = activation_now + timedelta(days=61)
    with patch("app.account_blocks.service.utc_now", return_value=activation_now):
        activate_account_block(actor=admin, block_id=block.id, settings=test_settings)

    _login_as(client, test_settings, owner.email)
    with patch("app.account_blocks.service.utc_now", return_value=expired_now):
        response = client.get("/cabinet")

    accounts_section = _extract_accounts_section(response.text)
    assert "Почта" in accounts_section
    assert "Срок завершён: 60 из 60 дней" in accounts_section
    assert "Активно" not in accounts_section
    assert "Активен: день" not in accounts_section
    assert "Осталось после активации" not in accounts_section
    assert "Срок действия" not in accounts_section
