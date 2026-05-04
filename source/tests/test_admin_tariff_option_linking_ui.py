from __future__ import annotations

import re
import sqlite3

import pytest

from app.auth.service import authenticate_user, create_session, register_user, verify_email
from app.paid_options.service import create_paid_option, get_paid_option_by_code, upsert_paid_option
from app.shared.db import get_database_path
from app.tariffs.service import STARTER_TARIFF_CODE, get_tariff_by_code, list_tariff_options, seed_initial_catalog


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


def _seed_linking_catalog(test_settings):
    seed_initial_catalog(settings=test_settings)
    active_option = upsert_paid_option(
        code="ui_link_active",
        title="Attachable Option",
        description="Active option for tariff linking",
        price_amount_minor=0,
        currency="RUB",
        status="active",
        sort_order=50,
        settings=test_settings,
    )
    archived_option = upsert_paid_option(
        code="ui_link_archived",
        title="Archived Option",
        description="Archived option for tariff linking",
        price_amount_minor=0,
        currency="RUB",
        status="archived",
        sort_order=51,
        settings=test_settings,
    )
    return active_option.code, archived_option.code


@pytest.mark.parametrize(
    ("path",),
    [
        (f"/admin/tariffs/{STARTER_TARIFF_CODE}/options",),
    ],
)
def test_anonymous_tariff_options_redirects_to_login(client, path):
    response = client.get(path, follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/login"


def test_normal_user_gets_forbidden_on_tariff_options_page(client, test_settings):
    _make_admin(client, test_settings, email="user@example.com", login="regularuser")
    with _connect(test_settings) as conn:
        conn.execute("UPDATE users SET role = ? WHERE email = ?", ("user", "user@example.com"))
        conn.commit()

    response = client.get(f"/admin/tariffs/{STARTER_TARIFF_CODE}/options")
    assert response.status_code == 403
    assert "Forbidden" in response.text


def test_admin_tariff_options_page_returns_404_for_missing_tariff(client, test_settings):
    _make_admin(client, test_settings)
    response = client.get("/admin/tariffs/missing_tariff/options")
    assert response.status_code == 404


def test_admin_tariff_options_page_shows_linked_and_attachable_options(client, test_settings):
    _make_admin(client, test_settings)
    active_code, archived_code = _seed_linking_catalog(test_settings)

    response = client.get(f"/admin/tariffs/{STARTER_TARIFF_CODE}/options")
    assert response.status_code == 200
    body = response.text
    assert "Опции тарифа" in body
    assert STARTER_TARIFF_CODE in body
    assert "Стартовый доступ" in body
    assert "AI / GPT-инструмент" in body
    assert "Сервер" in body
    assert "VPN" in body
    assert active_code in body
    assert archived_code not in body
    assert "/admin/payments" not in body
    assert "/admin/paid-options/new" not in body


def test_admin_tariff_options_page_has_tariffs_list_link(client, test_settings):
    _make_admin(client, test_settings)
    seed_initial_catalog(settings=test_settings)

    response = client.get("/admin/tariffs")
    assert response.status_code == 200
    body = response.text
    assert f"/admin/tariffs/{STARTER_TARIFF_CODE}/options" in body


def test_admin_attach_option_links_active_option_and_updates_metadata_on_repeat_attach(client, test_settings):
    _make_admin(client, test_settings)
    active_code, _ = _seed_linking_catalog(test_settings)

    first = client.post(
        f"/admin/tariffs/{STARTER_TARIFF_CODE}/options/attach",
        data={
            "option_code": active_code,
            "included_duration_days": "10",
            "included_quantity": "2",
        },
        follow_redirects=False,
    )
    assert first.status_code == 303
    assert first.headers["location"] == f"/admin/tariffs/{STARTER_TARIFF_CODE}/options"

    second = client.post(
        f"/admin/tariffs/{STARTER_TARIFF_CODE}/options/attach",
        data={
            "option_code": active_code,
            "included_duration_days": "15",
            "included_quantity": "4",
        },
        follow_redirects=False,
    )
    assert second.status_code == 303

    links = [row for row in list_tariff_options(STARTER_TARIFF_CODE, include_hidden=True, include_archived=True, settings=test_settings) if row["code"] == active_code]
    assert len(links) == 1
    assert links[0]["included_duration_days"] == 15
    assert links[0]["included_quantity"] == 4


def test_admin_attach_archived_option_is_rejected_safely(client, test_settings):
    _make_admin(client, test_settings)
    _, archived_code = _seed_linking_catalog(test_settings)

    response = client.post(
        f"/admin/tariffs/{STARTER_TARIFF_CODE}/options/attach",
        data={
            "option_code": archived_code,
            "included_duration_days": "",
            "included_quantity": "",
        },
    )
    assert response.status_code == 400
    assert "archived" in response.text.lower()


def test_admin_post_update_changes_link_metadata(client, test_settings):
    _make_admin(client, test_settings)
    active_code, _ = _seed_linking_catalog(test_settings)
    client.post(
        f"/admin/tariffs/{STARTER_TARIFF_CODE}/options/attach",
        data={
            "option_code": active_code,
            "included_duration_days": "10",
            "included_quantity": "2",
        },
        follow_redirects=False,
    )

    response = client.post(
        f"/admin/tariffs/{STARTER_TARIFF_CODE}/options/{active_code}/update",
        data={
            "included_duration_days": "21",
            "included_quantity": "8",
        },
        follow_redirects=False,
    )
    assert response.status_code == 303
    links = [row for row in list_tariff_options(STARTER_TARIFF_CODE, include_hidden=True, include_archived=True, settings=test_settings) if row["code"] == active_code]
    assert len(links) == 1
    assert links[0]["included_duration_days"] == 21
    assert links[0]["included_quantity"] == 8


def test_admin_post_detach_removes_relation_without_deleting_records(client, test_settings):
    _make_admin(client, test_settings)
    active_code, _ = _seed_linking_catalog(test_settings)
    client.post(
        f"/admin/tariffs/{STARTER_TARIFF_CODE}/options/attach",
        data={
            "option_code": active_code,
            "included_duration_days": "10",
            "included_quantity": "2",
        },
        follow_redirects=False,
    )

    response = client.post(
        f"/admin/tariffs/{STARTER_TARIFF_CODE}/options/{active_code}/detach",
        follow_redirects=False,
    )
    assert response.status_code == 303
    assert response.headers["location"] == f"/admin/tariffs/{STARTER_TARIFF_CODE}/options"
    assert get_tariff_by_code(STARTER_TARIFF_CODE, settings=test_settings) is not None
    assert get_paid_option_by_code(active_code, settings=test_settings) is not None
    assert active_code not in {row["code"] for row in list_tariff_options(STARTER_TARIFF_CODE, include_hidden=True, include_archived=True, settings=test_settings)}


def test_admin_missing_link_errors_are_safe(client, test_settings):
    _make_admin(client, test_settings)
    _seed_linking_catalog(test_settings)

    update_response = client.post(
        f"/admin/tariffs/{STARTER_TARIFF_CODE}/options/ui_link_active/update",
        data={
            "included_duration_days": "1",
            "included_quantity": "1",
        },
    )
    assert update_response.status_code == 404

    detach_response = client.post(
        f"/admin/tariffs/{STARTER_TARIFF_CODE}/options/ui_link_active/detach",
    )
    assert detach_response.status_code == 404

    attach_response = client.post(
        f"/admin/tariffs/{STARTER_TARIFF_CODE}/options/missing_option/attach",
        data={
            "included_duration_days": "",
            "included_quantity": "",
        },
    )
    assert attach_response.status_code == 404


def test_admin_tariff_options_page_is_read_safe(client, test_settings):
    _make_admin(client, test_settings)
    _seed_linking_catalog(test_settings)

    response = client.get(f"/admin/tariffs/{STARTER_TARIFF_CODE}/options")
    assert response.status_code == 200
    body = response.text
    assert "<form" in body
    assert "/admin/payments" not in body
    assert "payment" not in body.lower()
