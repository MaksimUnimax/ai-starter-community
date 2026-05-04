from __future__ import annotations

import re
import sqlite3

import pytest

from app.auth.service import authenticate_user, create_session, register_user, verify_email
from app.paid_options.service import (
    create_paid_option,
    get_paid_option_by_code,
    list_paid_options,
    list_paid_options_for_admin,
)
from app.shared.db import get_database_path
from app.tariffs.service import seed_initial_catalog


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
        ("/admin/paid-options/new",),
    ],
)
def test_anonymous_paid_option_create_redirects_to_login(client, path):
    response = client.get(path, follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/login"


def test_normal_user_cannot_open_paid_option_create_page(client, test_settings):
    _make_admin(client, test_settings, email="user@example.com", login="regularuser")
    with _connect(test_settings) as conn:
        conn.execute("UPDATE users SET role = ? WHERE email = ?", ("user", "user@example.com"))
        conn.commit()

    response = client.get("/admin/paid-options/new")
    assert response.status_code == 403
    assert "Доступ запрещён" in response.text
    assert "прав администратора" in response.text
    assert "Forbidden" not in response.text


def test_admin_can_open_paid_option_create_page(client, test_settings):
    _make_admin(client, test_settings)
    response = client.get("/admin/paid-options/new")
    assert response.status_code == 200
    body = response.text
    assert "Создание платной опции" in body
    assert "/static/styles.css" in body
    assert "Системный код" in body
    assert 'class="form"' in body
    assert "form-row" in body
    assert "form-actions" in body
    assert "button-primary" in body
    assert "button-secondary" in body
    assert "textarea" in body
    assert "select" in body
    assert "Название" in body
    assert "Описание" in body
    assert "Цена, ₽" in body
    assert "Валюта" in body
    assert "Срок по умолчанию, дней" in body
    assert "Статус" in body
    assert "Можно продлевать" in body
    assert "Порядок сортировки" in body
    assert "Code" not in body
    assert "Title" not in body
    assert "Description" not in body
    assert "Status" not in body
    assert "Is renewable" not in body
    assert "Sort order" not in body
    assert 'name="code"' in body
    assert "Нужен программе. Можно оставить пустым — система создаст код автоматически." in body


def test_admin_can_create_paid_option_via_ui(client, test_settings):
    _make_admin(client, test_settings)

    response = client.post(
        "/admin/paid-options/new",
        data={
            "code": "ui_paid_option_create",
            "title": "UI Paid Option",
            "description": "Created from admin UI",
            "price_rub": "12.34",
            "currency": "RUB",
            "default_duration_days": "30",
            "status": "active",
            "is_renewable": "1",
            "sort_order": "7",
        },
        follow_redirects=False,
    )

    assert response.status_code == 303
    assert response.headers["location"] == "/admin/paid-options"

    option = get_paid_option_by_code("ui_paid_option_create", settings=test_settings)
    assert option is not None
    assert option.title == "UI Paid Option"
    assert option.description == "Created from admin UI"
    assert option.price_amount_minor == 1234
    assert option.currency == "RUB"
    assert option.default_duration_days == 30
    assert option.status == "active"
    assert option.is_renewable is True
    assert option.sort_order == 7


def test_admin_can_create_paid_option_without_code_via_ui(client, test_settings):
    _make_admin(client, test_settings)

    response = client.post(
        "/admin/paid-options/new",
        data={
            "code": "",
            "title": "UI Paid Option Without Code",
            "description": "Created without manual code",
            "price_rub": "",
            "currency": "RUB",
            "default_duration_days": "",
            "status": "active",
            "is_renewable": "1",
            "sort_order": "7",
        },
        follow_redirects=False,
    )

    assert response.status_code == 303
    created = next(item for item in list_paid_options_for_admin(settings=test_settings) if item.title == "UI Paid Option Without Code")
    assert created.code.startswith("option_")
    assert re.fullmatch(r"[a-z0-9_-]{3,64}", created.code)


def test_admin_paid_option_create_rejects_duplicate_code_safely(client, test_settings):
    _make_admin(client, test_settings)
    payload = {
        "code": "ui_paid_option_duplicate",
        "title": "UI Paid Option",
        "description": "",
        "price_rub": "10",
        "currency": "RUB",
        "default_duration_days": "",
        "status": "active",
        "is_renewable": "1",
        "sort_order": "0",
    }

    first = client.post("/admin/paid-options/new", data=payload, follow_redirects=False)
    assert first.status_code == 303
    second = client.post("/admin/paid-options/new", data=payload)
    assert second.status_code == 400
    assert "существует" in second.text.lower()
    assert get_paid_option_by_code("ui_paid_option_duplicate", settings=test_settings) is not None


@pytest.mark.parametrize(
    ("payload", "needle"),
    [
        (
            {
                "code": "Bad Code",
                "title": "UI Paid Option",
                "description": "",
                "price_rub": "10",
                "currency": "RUB",
                "default_duration_days": "",
                "status": "active",
                "is_renewable": "1",
                "sort_order": "0",
            },
            "код",
        ),
        (
            {
                "code": "ui_paid_option_negative",
                "title": "UI Paid Option",
                "description": "",
                "price_rub": "-1",
                "currency": "RUB",
                "default_duration_days": "",
                "status": "active",
                "is_renewable": "1",
                "sort_order": "0",
            },
            "цен",
        ),
        (
            {
                "code": "ui_paid_option_bad_duration",
                "title": "UI Paid Option",
                "description": "",
                "price_rub": "10",
                "currency": "RUB",
                "default_duration_days": "abc",
                "status": "active",
                "is_renewable": "1",
                "sort_order": "0",
            },
            "срок",
        ),
    ],
)
def test_admin_paid_option_create_rejects_invalid_input_safely(client, test_settings, payload, needle):
    _make_admin(client, test_settings)
    response = client.post("/admin/paid-options/new", data=payload)
    assert response.status_code == 400
    assert needle in response.text.lower()
    assert get_paid_option_by_code(payload["code"].lower().replace(" ", "_"), settings=test_settings) is None


def test_admin_paid_option_create_preserves_blank_price_as_null(client, test_settings):
    _make_admin(client, test_settings)
    response = client.post(
        "/admin/paid-options/new",
        data={
            "code": "ui_paid_option_blank_price",
            "title": "Blank Price",
            "description": "",
            "price_rub": "",
            "currency": "RUB",
            "default_duration_days": "",
            "status": "active",
            "is_renewable": "1",
            "sort_order": "0",
        },
        follow_redirects=False,
    )
    assert response.status_code == 303
    option = get_paid_option_by_code("ui_paid_option_blank_price", settings=test_settings)
    assert option is not None
    assert option.price_amount_minor is None


def test_admin_paid_option_create_preserves_explicit_zero_price(client, test_settings):
    _make_admin(client, test_settings)
    response = client.post(
        "/admin/paid-options/new",
        data={
            "code": "ui_paid_option_zero_price",
            "title": "Zero Price",
            "description": "",
            "price_rub": "0",
            "currency": "RUB",
            "default_duration_days": "",
            "status": "active",
            "is_renewable": "1",
            "sort_order": "0",
        },
        follow_redirects=False,
    )
    assert response.status_code == 303
    option = get_paid_option_by_code("ui_paid_option_zero_price", settings=test_settings)
    assert option is not None
    assert option.price_amount_minor == 0


def test_admin_edit_page_shows_code_as_read_only_and_null_price_label(client, test_settings):
    _make_admin(client, test_settings)
    create_paid_option(
        code="ui_paid_option_edit_null",
        title="UI Paid Option",
        description="Initial description",
        price_amount_minor=None,
        currency="RUB",
        default_duration_days=None,
        status="active",
        is_renewable=True,
        sort_order=1,
        settings=test_settings,
    )

    response = client.get("/admin/paid-options/ui_paid_option_edit_null/edit")
    assert response.status_code == 200
    body = response.text
    assert "/static/styles.css" in body
    assert "Редактирование платной опции" in body
    assert 'class="form"' in body
    assert "form-row" in body
    assert "form-actions" in body
    assert "button-primary" in body
    assert "button-secondary" in body
    assert "textarea" in body
    assert "select" in body
    assert "Системный код" in body
    assert "Название" in body
    assert "Описание" in body
    assert "Цена, ₽" in body
    assert "Валюта" in body
    assert "Срок по умолчанию, дней" in body
    assert "Статус" in body
    assert "Можно продлевать" in body
    assert "Порядок сортировки" in body
    assert "Code" not in body
    assert "Title" not in body
    assert 'name="code"' in body
    assert "readonly" in body
    assert "ui_paid_option_edit_null" in body
    assert "Системный код нельзя изменить после создания." in body
    assert "Отдельная цена не задана." in body
    assert 'name="price_rub" value=""' in body


def test_admin_post_edit_updates_allowed_fields_and_keeps_code(client, test_settings):
    _make_admin(client, test_settings)
    create_paid_option(
        code="ui_paid_option_update",
        title="UI Paid Option",
        description="Initial description",
        price_amount_minor=1000,
        currency="RUB",
        default_duration_days=10,
        status="active",
        is_renewable=True,
        sort_order=1,
        settings=test_settings,
    )

    response = client.post(
        "/admin/paid-options/ui_paid_option_update/edit",
        data={
            "code": "ui_paid_option_update",
            "title": "UI Paid Option Updated",
            "description": "Updated description",
            "price_rub": "",
            "currency": "RUB",
            "default_duration_days": "45",
            "status": "hidden",
            "sort_order": "9",
        },
        follow_redirects=False,
    )
    assert response.status_code == 303
    assert response.headers["location"] == "/admin/paid-options"

    option = get_paid_option_by_code("ui_paid_option_update", settings=test_settings)
    assert option is not None
    assert option.code == "ui_paid_option_update"
    assert option.title == "UI Paid Option Updated"
    assert option.description == "Updated description"
    assert option.price_amount_minor is None
    assert option.currency == "RUB"
    assert option.default_duration_days == 45
    assert option.status == "hidden"
    assert option.is_renewable is False
    assert option.sort_order == 9


def test_admin_post_edit_rejects_code_changes(client, test_settings):
    _make_admin(client, test_settings)
    create_paid_option(
        code="ui_paid_option_code_lock",
        title="UI Paid Option",
        description="Initial description",
        price_amount_minor=1000,
        currency="RUB",
        default_duration_days=10,
        status="active",
        is_renewable=True,
        sort_order=1,
        settings=test_settings,
    )

    response = client.post(
        "/admin/paid-options/ui_paid_option_code_lock/edit",
        data={
            "code": "ui_paid_option_code_changed",
            "title": "UI Paid Option Updated",
            "description": "Updated description",
            "price_rub": "55.50",
            "currency": "RUB",
            "default_duration_days": "45",
            "status": "hidden",
            "is_renewable": "1",
            "sort_order": "9",
        },
    )

    assert response.status_code == 400
    assert "системный код" in response.text.lower()
    option = get_paid_option_by_code("ui_paid_option_code_lock", settings=test_settings)
    assert option is not None
    assert option.title == "UI Paid Option"
    assert get_paid_option_by_code("ui_paid_option_code_changed", settings=test_settings) is None


def test_admin_post_archive_sets_paid_option_status_archived(client, test_settings):
    _make_admin(client, test_settings)
    create_paid_option(
        code="ui_paid_option_archive",
        title="UI Paid Option",
        description="Initial description",
        price_amount_minor=1000,
        currency="RUB",
        default_duration_days=10,
        status="active",
        is_renewable=True,
        sort_order=1,
        settings=test_settings,
    )

    response = client.post("/admin/paid-options/ui_paid_option_archive/archive", follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/admin/paid-options"

    option = get_paid_option_by_code("ui_paid_option_archive", settings=test_settings)
    assert option is not None
    assert option.status == "archived"
    assert "ui_paid_option_archive" not in {item.code for item in list_paid_options(settings=test_settings)}
    assert "ui_paid_option_archive" in {item.code for item in list_paid_options_for_admin(settings=test_settings)}


def test_admin_paid_option_list_shows_controls_without_tariff_linking_ui(client, test_settings):
    _make_admin(client, test_settings)
    seed_initial_catalog(settings=test_settings)

    response = client.get("/admin/paid-options")
    assert response.status_code == 200
    body = response.text
    assert "Код" in body
    assert "Название" in body
    assert "Описание" in body
    assert "Цена, ₽" in body
    assert "Валюта" in body
    assert "Срок по умолчанию, дней" in body
    assert "Статус" in body
    assert "Можно продлевать" in body
    assert "Порядок сортировки" in body
    assert "/admin/paid-options/new" in body
    assert "/admin/paid-options/ai_gpt_tool/edit" in body
    assert "/admin/paid-options/ai_gpt_tool/archive" in body
    assert "/admin/tariffs/" not in body
    assert "/admin/payments" not in body


def test_admin_paid_option_form_does_not_expose_payment_ui(client, test_settings):
    _make_admin(client, test_settings)
    response = client.get("/admin/paid-options/new")
    body = response.text
    assert "payment" not in body.lower()
    assert "оплата" not in body.lower()
