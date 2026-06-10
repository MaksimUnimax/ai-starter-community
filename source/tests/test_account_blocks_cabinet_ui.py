from __future__ import annotations

import re
import sqlite3
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode
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


def _grant_materials_access(test_settings, email: str) -> None:
    with _connect(test_settings) as conn:
        conn.execute(
            "UPDATE users SET materials_access_granted_at = CURRENT_TIMESTAMP WHERE email = ?",
            (email,),
        )
        conn.commit()


def _extract_accounts_section(body_text: str) -> str:
    start_marker = '<section id="accounts" class="card stack accounts-card" data-local-accounts-root data-account-blocks-source="server">'
    end_marker = '\n  <section class="card stack prompts-library-card" data-prompts-library-root>'
    start = body_text.find(start_marker)
    end = body_text.find(end_marker, start)
    assert start != -1
    assert end != -1
    return body_text[start:end]


def _extract_builder_shell(accounts_section: str) -> str:
    start_marker = '<div class="accounts-builder-shell">'
    end_marker = '<div class="accounts-grid">'
    start = accounts_section.find(start_marker)
    end = accounts_section.find(end_marker, start)
    assert start != -1
    if end == -1:
        end = len(accounts_section)
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
    _grant_materials_access(test_settings, owner.email)

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
    assert 'id="accounts"' in response.text

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
    assert "Осталось 60 дней" in accounts_section
    assert "Не активирован" in accounts_section
    assert "Срок завершён" not in accounts_section
    assert "Осталось после активации" not in accounts_section
    assert "Владелец:" not in accounts_section
    assert "account-owner-group__title" not in accounts_section
    assert "account-owner-group__meta" not in accounts_section
    assert "account-card__owner-line" not in accounts_section
    assert "Срок действия" not in accounts_section
    assert "из 60" not in accounts_section
    assert "После активации блок работает 60 дней" not in accounts_section
    assert 'data-account-block-form="create"' not in accounts_section
    assert "Платная опция" not in accounts_section
    assert "Без привязки" not in accounts_section
    assert "Продлить активацию" not in accounts_section


def test_moderator_can_search_user_by_email_and_manage_selected_user_blocks(client, test_settings):
    admin = _create_verified_user(test_settings, "cab-ui-admin-2@example.com", "cabuiadmin2", role="admin")
    moderator = _create_verified_user(test_settings, "cab-ui-moderator@example.com", "cabuimoderator", role="moderator")
    owner_a = _create_verified_user(test_settings, "cab-ui-owner-a@example.com", "cabuiownera")
    _login_as(client, test_settings, moderator.email)

    cabinet_response = client.get(f"/cabinet?account_blocks_user_email={owner_a.email}")
    assert cabinet_response.status_code == 200
    assert "Администратор и модератор выбирают пользователя по email и управляют только его блоками." in cabinet_response.text
    assert "Email пользователя" in cabinet_response.text
    assert owner_a.email in cabinet_response.text
    accounts_section = _extract_accounts_section(cabinet_response.text)
    builder_shell = _extract_builder_shell(accounts_section)
    assert "Добавить блок" in builder_shell
    assert 'name="duration_days"' in builder_shell
    assert 'data-account-block-duration-input' in builder_shell
    assert 'name="duration_days" type="number" min="1" value="30"' in builder_shell
    assert 'name="owner_user_id"' not in builder_shell
    assert 'name="title"' not in builder_shell
    assert f'action="/cabinet/account-blocks?{urlencode({"account_blocks_user_email": owner_a.email})}' in builder_shell
    with _connect(test_settings) as conn:
        assert (
            conn.execute(
                "SELECT COUNT(*) AS c FROM email_outbox WHERE template_key = ?",
                ("account_block_activation",),
            ).fetchone()["c"]
            == 0
        )

    create_response = client.post(
        f"/cabinet/account-blocks?{urlencode({'account_blocks_user_email': owner_a.email})}",
        data={
            "type": "server",
            "duration_days": "",
            "login": "mod-block-login",
            "password_secret": "mod-block-password",
        },
        follow_redirects=False,
    )
    assert create_response.status_code == 303
    assert create_response.headers["location"] == f"/cabinet?{urlencode({'account_blocks_notice': 'created', 'account_blocks_user_email': owner_a.email})}"

    with _connect(test_settings) as conn:
        row = conn.execute("SELECT * FROM account_blocks WHERE login = ?", ("mod-block-login",)).fetchone()
    assert row is not None
    block_id = int(row["id"])
    assert int(row["owner_user_id"]) == owner_a.id
    assert row["type"] == "server"
    assert row["title"] == "Сервер"
    assert row["email"] is None
    assert int(row["duration_days"]) == 30

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
    assert update_response.headers["location"] == f"/cabinet?{urlencode({'account_blocks_notice': 'updated', 'account_blocks_user_email': owner_a.email})}"
    with _connect(test_settings) as conn:
        assert (
            conn.execute(
                "SELECT COUNT(*) AS c FROM email_outbox WHERE template_key = ?",
                ("account_block_activation",),
            ).fetchone()["c"]
            == 0
        )

    activation_now = datetime(2026, 6, 8, 12, 0, 0, tzinfo=timezone.utc)
    with patch("app.account_blocks.service.utc_now", return_value=activation_now):
        activate_response = client.post(
            f"/cabinet/account-blocks/{block_id}/activate?{urlencode({'account_blocks_user_email': owner_a.email})}",
            data={
                "duration_days": "",
            },
            follow_redirects=False,
        )
    assert activate_response.status_code == 303
    assert activate_response.headers["location"] == f"/cabinet?{urlencode({'account_blocks_notice': 'activated_email_sent', 'account_blocks_user_email': owner_a.email})}"

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
    assert updated_row["activated_at"] == activation_now.isoformat()
    assert updated_row["expires_at"] == (activation_now + timedelta(days=30)).isoformat()

    with _connect(test_settings) as conn:
        email_row = conn.execute(
            """
            SELECT *
            FROM email_outbox
            WHERE recipient_email = ? AND template_key = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (owner_a.email, "account_block_activation"),
        ).fetchone()
    assert email_row is not None
    assert email_row["subject"] == "Активирована опция OpenScript"
    assert "updated-login" not in email_row["body_text"]
    assert "updated-password" not in email_row["body_text"]

    renewal_now = activation_now + timedelta(days=22)
    with patch("app.account_blocks.service.utc_now", return_value=renewal_now):
        active_page = client.get(f"/cabinet?{urlencode({'account_blocks_user_email': owner_a.email})}")
    accounts_section = _extract_accounts_section(active_page.text)
    assert "Редактировать" in accounts_section
    assert "Удалить" in accounts_section
    assert "Активировать" in accounts_section
    assert "Продлить активацию" in accounts_section
    assert "Сервер" in accounts_section
    assert "account-card__owner-line" in accounts_section
    assert "Пользователь:" in accounts_section
    assert "Осталось 8 дней" in accounts_section
    assert f'/cabinet/account-blocks/{block_id}/delete?{urlencode({"account_blocks_user_email": owner_a.email})}' in accounts_section
    assert f'/cabinet/account-blocks/{block_id}/activate?{urlencode({"account_blocks_user_email": owner_a.email})}' in accounts_section
    assert f'/cabinet/account-blocks/{block_id}/renew?{urlencode({"account_blocks_user_email": owner_a.email})}' in accounts_section
    assert 'name="duration_days"' in accounts_section
    edit_form = _extract_first_edit_form(accounts_section)
    assert 'name="login"' in edit_form
    assert 'name="password_secret"' in edit_form
    assert "data-account-card-edit-form" in edit_form
    assert 'hidden' in edit_form
    assert "Платная опция" not in builder_shell
    assert "Без привязки" not in builder_shell

    with patch("app.account_blocks.service.utc_now", return_value=renewal_now):
        renew_response = client.post(
            f"/cabinet/account-blocks/{block_id}/renew?{urlencode({'account_blocks_user_email': owner_a.email})}",
            data={
                "duration_days": "30",
            },
            follow_redirects=False,
        )
    assert renew_response.status_code == 303
    assert renew_response.headers["location"] == f"/cabinet?{urlencode({'account_blocks_notice': 'renewed', 'account_blocks_user_email': owner_a.email})}"

    with _connect(test_settings) as conn:
        renewed_row = conn.execute("SELECT * FROM account_blocks WHERE id = ?", (block_id,)).fetchone()
    assert renewed_row is not None
    assert renewed_row["expires_at"] == (renewal_now + timedelta(days=38)).isoformat()

    delete_response = client.post(
        f"/cabinet/account-blocks/{block_id}/delete?{urlencode({'account_blocks_user_email': owner_a.email})}",
        follow_redirects=False,
    )
    assert delete_response.status_code == 303
    assert delete_response.headers["location"] == f"/cabinet?{urlencode({'account_blocks_notice': 'deleted', 'account_blocks_user_email': owner_a.email})}"

    with _connect(test_settings) as conn:
        deleted_row = conn.execute("SELECT 1 FROM account_blocks WHERE id = ?", (block_id,)).fetchone()
    assert deleted_row is None
    with _connect(test_settings) as conn:
        email_row = conn.execute(
            """
            SELECT *
            FROM email_outbox
            WHERE recipient_email = ? AND template_key = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (owner_a.email, "account_block_activation"),
        ).fetchone()
    assert email_row is not None
    assert email_row["subject"] == "Активирована опция OpenScript"
    assert "У вас активирована опция: Сервер." in email_row["body_text"]
    assert "https://openscript.ru/" in email_row["body_text"]
    assert "https://openscript.ru/cabinet" in email_row["body_text"]
    assert "updated-login" not in email_row["body_text"]
    assert "updated-password" not in email_row["body_text"]


def test_moderator_can_manage_account_blocks_but_cannot_access_admin_dashboard(client, test_settings):
    moderator = _create_verified_user(test_settings, "cab-ui-moderator@example.com", "cabuimoderator", role="moderator")
    owner = _create_verified_user(test_settings, "cab-ui-moderator-owner@example.com", "cabuimoderatorowner")
    _login_as(client, test_settings, moderator.email)

    admin_response = client.get("/admin")
    assert admin_response.status_code == 403
    admin_blocks_response = client.get("/admin/account-blocks?account_blocks_user_email=test@example.com")
    assert admin_blocks_response.status_code == 403

    create_response = client.post(
        f"/cabinet/account-blocks?{urlencode({'account_blocks_user_email': owner.email})}",
        data={
            "type": "chatgpt",
            "login": "moderator-login",
            "password_secret": "moderator-password",
        },
        follow_redirects=False,
    )
    assert create_response.status_code == 303
    assert create_response.headers["location"] == f"/cabinet?{urlencode({'account_blocks_notice': 'created', 'account_blocks_user_email': owner.email})}"

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
    assert update_response.headers["location"] == f"/cabinet?{urlencode({'account_blocks_notice': 'updated', 'account_blocks_user_email': owner.email})}"

    activation_now = datetime(2026, 6, 8, 12, 0, 0, tzinfo=timezone.utc)
    with patch("app.account_blocks.service.utc_now", return_value=activation_now):
        activate_response = client.post(
            f"/cabinet/account-blocks/{block_id}/activate?{urlencode({'account_blocks_user_email': owner.email})}",
            data={"duration_days": "45"},
            follow_redirects=False,
        )
    assert activate_response.status_code == 303
    assert activate_response.headers["location"] == f"/cabinet?{urlencode({'account_blocks_notice': 'activated_email_sent', 'account_blocks_user_email': owner.email})}"

    with _connect(test_settings) as conn:
        activated_row = conn.execute("SELECT * FROM account_blocks WHERE id = ?", (block_id,)).fetchone()
    assert activated_row is not None
    assert activated_row["expires_at"] == (activation_now + timedelta(days=45)).isoformat()

    with patch("app.account_blocks.service.utc_now", return_value=activation_now + timedelta(days=1)):
        active_page = client.get(f"/cabinet?{urlencode({'account_blocks_user_email': owner.email})}")
    accounts_section = _extract_accounts_section(active_page.text)
    assert "Продлить активацию" in accounts_section
    assert "Осталось 44 дня" in accounts_section

    renew_response = client.post(
        f"/cabinet/account-blocks/{block_id}/renew?{urlencode({'account_blocks_user_email': owner.email})}",
        data={"duration_days": "30"},
        follow_redirects=False,
    )
    assert renew_response.status_code == 303
    assert renew_response.headers["location"] == f"/cabinet?{urlencode({'account_blocks_notice': 'renewed', 'account_blocks_user_email': owner.email})}"

    delete_response = client.post(
        f"/cabinet/account-blocks/{block_id}/delete?{urlencode({'account_blocks_user_email': owner.email})}",
        follow_redirects=False,
    )
    assert delete_response.status_code == 303
    assert delete_response.headers["location"] == f"/cabinet?{urlencode({'account_blocks_notice': 'deleted', 'account_blocks_user_email': owner.email})}"


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
    renew_response = client.post(f"/cabinet/account-blocks/{block.id}/renew")
    assert renew_response.status_code == 403


def test_expired_account_block_shows_finished_day_counter_without_active_label(client, test_settings):
    admin = _create_verified_user(test_settings, "cab-ui-expire-admin@example.com", "cabuiexpireadmin", role="admin")
    owner = _create_verified_user(test_settings, "cab-ui-expire-owner@example.com", "cabuiexpireowner")
    _grant_materials_access(test_settings, owner.email)
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
    assert "Срок завершён" in accounts_section
    assert "Осталось" not in accounts_section
    assert "Активно" not in accounts_section
    assert "Активен:" not in accounts_section
    assert "Осталось после активации" not in accounts_section
    assert "Срок действия" not in accounts_section
    assert "из 60" not in accounts_section
    assert "60 дней" not in accounts_section
    assert "Продлить активацию" not in accounts_section
