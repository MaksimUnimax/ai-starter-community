from __future__ import annotations

import re
import sqlite3

import pytest

from app.auth.service import authenticate_user, create_session, register_user, verify_email
from app.shared.db import get_database_path
from app.tariffs.service import (
    STARTER_TARIFF_CODE,
    create_tariff,
    get_tariff_by_code,
    list_tariffs,
    list_tariffs_for_admin,
    seed_initial_catalog,
)


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


def _make_admin(client, test_settings, email: str = "admin@example.com", login: str = "adminuser") -> None:
    register_user(
        email=email,
        login=login,
        password="Secret123",
        repeat_password="Secret123",
        settings=test_settings,
    )
    token = _extract_verify_token(test_settings, email)
    verify_email(token, settings=test_settings)
    with _connect(test_settings) as conn:
        conn.execute("UPDATE users SET role = ? WHERE email = ?", ("admin", email))
        conn.commit()
    user = authenticate_user(email, "Secret123", settings=test_settings)
    session_token = create_session(user.id, settings=test_settings)
    client.cookies.set(test_settings.session_cookie_name, session_token)


@pytest.mark.parametrize(
    ("path",),
    [
        ("/admin/tariffs/new",),
    ],
)
def test_anonymous_tariff_create_redirects_to_login(client, path):
    response = client.get(path, follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/login"


def test_normal_user_cannot_open_tariff_create_page(client, test_settings):
    _make_admin(client, test_settings, email="user@example.com", login="regularuser")
    with _connect(test_settings) as conn:
        conn.execute("UPDATE users SET role = ? WHERE email = ?", ("user", "user@example.com"))
        conn.commit()

    response = client.get("/admin/tariffs/new")
    assert response.status_code == 403
    assert "Forbidden" in response.text


def test_admin_can_open_tariff_create_page(client, test_settings):
    _make_admin(client, test_settings)
    response = client.get("/admin/tariffs/new")
    assert response.status_code == 200
    body = response.text
    assert "Создание тарифа" in body
    assert 'name="code"' in body
    assert "Код нельзя изменить после создания." in body


def test_admin_can_create_tariff_via_ui(client, test_settings):
    _make_admin(client, test_settings)

    response = client.post(
        "/admin/tariffs/new",
        data={
            "code": "ui_tariff_create",
            "title": "UI Tariff",
            "description": "Tariff created from admin UI",
            "price_rub": "12.34",
            "currency": "RUB",
            "status": "active",
            "sort_order": "7",
        },
        follow_redirects=False,
    )

    assert response.status_code == 303
    assert response.headers["location"] == "/admin/tariffs"

    tariff = get_tariff_by_code("ui_tariff_create", settings=test_settings)
    assert tariff is not None
    assert tariff.title == "UI Tariff"
    assert tariff.description == "Tariff created from admin UI"
    assert tariff.price_amount_minor == 1234
    assert tariff.currency == "RUB"
    assert tariff.status == "active"
    assert tariff.sort_order == 7


def test_admin_tariff_create_rejects_duplicate_code_safely(client, test_settings):
    _make_admin(client, test_settings)
    payload = {
        "code": "ui_tariff_duplicate",
        "title": "UI Tariff",
        "description": "",
        "price_rub": "10",
        "currency": "RUB",
        "status": "active",
        "sort_order": "0",
    }

    first = client.post("/admin/tariffs/new", data=payload, follow_redirects=False)
    assert first.status_code == 303
    second = client.post("/admin/tariffs/new", data=payload)
    assert second.status_code == 400
    assert "already exists" in second.text.lower()
    assert get_tariff_by_code("ui_tariff_duplicate", settings=test_settings) is not None


@pytest.mark.parametrize(
    ("payload", "needle"),
    [
        (
            {
                "code": "Bad Code",
                "title": "UI Tariff",
                "description": "",
                "price_rub": "10",
                "currency": "RUB",
                "status": "active",
                "sort_order": "0",
            },
            "code",
        ),
        (
            {
                "code": "ui_tariff_negative",
                "title": "UI Tariff",
                "description": "",
                "price_rub": "-1",
                "currency": "RUB",
                "status": "active",
                "sort_order": "0",
            },
            "price",
        ),
    ],
)
def test_admin_tariff_create_rejects_invalid_input_safely(client, test_settings, payload, needle):
    _make_admin(client, test_settings)
    response = client.post("/admin/tariffs/new", data=payload)
    assert response.status_code == 400
    assert needle in response.text.lower()
    assert get_tariff_by_code(payload["code"].lower().replace(" ", "_"), settings=test_settings) is None


def test_admin_edit_page_shows_code_as_read_only(client, test_settings):
    _make_admin(client, test_settings)
    create_tariff(
        code="ui_tariff_edit",
        title="UI Tariff",
        description="Initial description",
        price_amount_minor=1000,
        status="active",
        settings=test_settings,
    )

    response = client.get("/admin/tariffs/ui_tariff_edit/edit")
    assert response.status_code == 200
    body = response.text
    assert "Редактирование тарифа" in body
    assert 'name="code"' in body
    assert "readonly" in body
    assert "ui_tariff_edit" in body
    assert "Код нельзя изменить после создания." in body


def test_admin_post_edit_updates_allowed_fields_and_keeps_code(client, test_settings):
    _make_admin(client, test_settings)
    create_tariff(
        code="ui_tariff_update",
        title="UI Tariff",
        description="Initial description",
        price_amount_minor=1000,
        currency="RUB",
        status="active",
        sort_order=1,
        settings=test_settings,
    )

    response = client.post(
        "/admin/tariffs/ui_tariff_update/edit",
        data={
            "code": "ui_tariff_update",
            "title": "UI Tariff Updated",
            "description": "Updated description",
            "price_rub": "55.50",
            "currency": "RUB",
            "status": "hidden",
            "sort_order": "9",
        },
        follow_redirects=False,
    )
    assert response.status_code == 303
    assert response.headers["location"] == "/admin/tariffs"

    tariff = get_tariff_by_code("ui_tariff_update", settings=test_settings)
    assert tariff is not None
    assert tariff.code == "ui_tariff_update"
    assert tariff.title == "UI Tariff Updated"
    assert tariff.description == "Updated description"
    assert tariff.price_amount_minor == 5550
    assert tariff.status == "hidden"
    assert tariff.sort_order == 9


def test_admin_post_edit_rejects_code_changes(client, test_settings):
    _make_admin(client, test_settings)
    create_tariff(
        code="ui_tariff_code_lock",
        title="UI Tariff",
        description="Initial description",
        price_amount_minor=1000,
        currency="RUB",
        status="active",
        sort_order=1,
        settings=test_settings,
    )

    response = client.post(
        "/admin/tariffs/ui_tariff_code_lock/edit",
        data={
            "code": "ui_tariff_code_changed",
            "title": "UI Tariff Updated",
            "description": "Updated description",
            "price_rub": "55.50",
            "currency": "RUB",
            "status": "hidden",
            "sort_order": "9",
        },
    )

    assert response.status_code == 400
    assert "code" in response.text.lower()

    tariff = get_tariff_by_code("ui_tariff_code_lock", settings=test_settings)
    assert tariff is not None
    assert tariff.title == "UI Tariff"
    assert get_tariff_by_code("ui_tariff_code_changed", settings=test_settings) is None


def test_admin_post_archive_sets_tariff_status_archived(client, test_settings):
    _make_admin(client, test_settings)
    create_tariff(
        code="ui_tariff_archive",
        title="UI Tariff",
        description="Initial description",
        price_amount_minor=1000,
        currency="RUB",
        status="active",
        sort_order=1,
        settings=test_settings,
    )

    response = client.post("/admin/tariffs/ui_tariff_archive/archive", follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/admin/tariffs"

    tariff = get_tariff_by_code("ui_tariff_archive", settings=test_settings)
    assert tariff is not None
    assert tariff.status == "archived"
    assert "ui_tariff_archive" not in {item.code for item in list_tariffs(settings=test_settings)}
    assert "ui_tariff_archive" in {item.code for item in list_tariffs_for_admin(settings=test_settings)}


def test_admin_tariff_list_shows_controls_without_paid_option_crud_ui(client, test_settings):
    _make_admin(client, test_settings)
    seed_initial_catalog(settings=test_settings)

    response = client.get("/admin/tariffs")
    assert response.status_code == 200
    body = response.text
    assert "/admin/tariffs/new" in body
    assert f"/admin/tariffs/{STARTER_TARIFF_CODE}/edit" in body
    assert f"/admin/tariffs/{STARTER_TARIFF_CODE}/archive" in body
    assert "/admin/paid-options/new" not in body
    assert "/admin/paid-options/" not in body
    assert "/admin/payments" not in body
