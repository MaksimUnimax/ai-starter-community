from __future__ import annotations

import re
import sqlite3
from datetime import datetime, timedelta, timezone

import pytest

from app.auth.service import (
    ADMIN_USER_PAGE_SIZE,
    authenticate_user,
    create_session,
    list_users_for_admin,
    list_users_for_admin_page,
    register_user,
    verify_email,
)
from app.shared.db import get_database_path, initialize_database
from app.shared.security import hash_password


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


def _create_verified_user(test_settings, *, email: str, login: str, role: str, access_status: str, created_at: str) -> None:
    register_user(
        email=email,
        login=login,
        password="Secret123",
        repeat_password="Secret123",
        settings=test_settings,
    )
    verify_email(_extract_verify_token(test_settings, email), settings=test_settings)
    with _connect(test_settings) as conn:
        conn.execute(
            """
            UPDATE users
            SET role = ?, access_status = ?, created_at = ?, updated_at = ?
            WHERE email = ?
            """,
            (role, access_status, created_at, created_at, email),
        )
        conn.commit()


def _seed_user_list(test_settings):
    _create_verified_user(
        test_settings,
        email="user-old@example.com",
        login="userold",
        role="user",
        access_status="not_activated",
        created_at=datetime(2026, 1, 10, 9, 0, tzinfo=timezone.utc).isoformat(),
    )
    _create_verified_user(
        test_settings,
        email="moderator-mid@example.com",
        login="moderatormid",
        role="moderator",
        access_status="activated",
        created_at=datetime(2026, 1, 15, 9, 0, tzinfo=timezone.utc).isoformat(),
    )
    _create_verified_user(
        test_settings,
        email="admin-new@example.com",
        login="adminnew",
        role="admin",
        access_status="not_activated",
        created_at=datetime(2026, 1, 20, 9, 0, tzinfo=timezone.utc).isoformat(),
    )


def _insert_admin_user_row(
    test_settings,
    *,
    email: str,
    login: str,
    role: str,
    access_status: str,
    created_at: datetime,
) -> None:
    materials_access_granted_at = created_at if access_status == "activated" else None
    iso_created_at = created_at.isoformat()
    with _connect(test_settings) as conn:
        conn.execute(
            """
            INSERT INTO users (
                email, login, password_hash, role, is_active,
                email_verified_at, materials_access_granted_at, access_status, created_at, updated_at
            )
            VALUES (?, ?, ?, ?, 1, ?, ?, ?, ?, ?)
            """,
            (
                email,
                login,
                hash_password("Secret123"),
                role,
                iso_created_at,
                materials_access_granted_at.isoformat() if materials_access_granted_at is not None else None,
                access_status,
                iso_created_at,
                iso_created_at,
            ),
        )
        conn.commit()


def _seed_paginated_user_list(test_settings):
    initialize_database(get_database_path(test_settings))
    base_created_at = datetime(2026, 2, 1, 9, 0, tzinfo=timezone.utc)
    for index in range(ADMIN_USER_PAGE_SIZE):
        number = index + 1
        _insert_admin_user_row(
            test_settings,
            email=f"user-{number:03d}@example.com",
            login=f"user{number:03d}",
            role="moderator" if number == 2 else "user",
            access_status="activated" if number % 2 else "not_activated",
            created_at=base_created_at + timedelta(minutes=index),
        )
    _insert_admin_user_row(
        test_settings,
        email="admin-new@example.com",
        login="adminnew",
        role="admin",
        access_status="activated",
        created_at=base_created_at + timedelta(minutes=ADMIN_USER_PAGE_SIZE),
    )


def _login_admin(client, test_settings):
    user = authenticate_user("admin-new@example.com", "Secret123", settings=test_settings)
    session_token = create_session(user.id, settings=test_settings)
    client.cookies.set(test_settings.session_cookie_name, session_token)


def _page_body(client, path: str):
    response = client.get(path)
    assert response.status_code == 200
    return response.text


def _extract_csrf_token(body_text: str) -> str:
    match = re.search(r'name="_csrf_token" value="([^"]+)"', body_text)
    assert match, "csrf token not found"
    return match.group(1)


def test_admin_users_page_filter_form_and_labels(client, test_settings):
    _seed_user_list(test_settings)
    _login_admin(client, test_settings)

    body = _page_body(client, "/admin/users")
    assert "Дата регистрации с" in body
    assert "Дата регистрации по" in body
    assert "Роль" in body
    assert "Статус доступа" in body
    assert "Сортировка по дате регистрации" in body
    assert "Все роли" in body
    assert "Пользователь" in body
    assert "Модератор" in body
    assert "Администратор" in body
    assert "Все статусы" in body
    assert "Не активирован" in body
    assert "Активирован" in body
    assert "Сначала новые" in body
    assert "Сначала старые" in body
    assert "Применить фильтр" in body
    assert "Сбросить" in body


def test_admin_users_page_query_param_guard_behavior(client, test_settings):
    _seed_user_list(test_settings)

    anonymous_response = client.get("/admin/users?role=user&created_sort=desc", follow_redirects=False)
    assert anonymous_response.status_code == 303
    assert anonymous_response.headers["location"] == "/login"

    _login_admin(client, test_settings)
    admin_response = client.get("/admin/users?role=user&created_sort=desc")
    assert admin_response.status_code == 200

    client.cookies.clear()
    register_user(
        email="regular@example.com",
        login="regularuser",
        password="Secret123",
        repeat_password="Secret123",
        settings=test_settings,
    )
    verify_email(_extract_verify_token(test_settings, "regular@example.com"), settings=test_settings)
    regular_user = authenticate_user("regular@example.com", "Secret123", settings=test_settings)
    client.cookies.set(test_settings.session_cookie_name, create_session(regular_user.id, settings=test_settings))
    user_response = client.get("/admin/users?role=user&created_sort=desc")
    assert user_response.status_code == 403

    client.cookies.clear()
    with _connect(test_settings) as conn:
        conn.execute("UPDATE users SET role = ? WHERE email = ?", ("moderator", "regular@example.com"))
        conn.commit()
    moderator = authenticate_user("regular@example.com", "Secret123", settings=test_settings)
    client.cookies.set(test_settings.session_cookie_name, create_session(moderator.id, settings=test_settings))
    moderator_response = client.get("/admin/users?role=user&created_sort=desc")
    assert moderator_response.status_code == 403


def test_admin_users_page_default_role_status_sort_filters(client, test_settings):
    _seed_user_list(test_settings)
    _login_admin(client, test_settings)

    body = _page_body(client, "/admin/users")
    assert body.index("admin-new@example.com") < body.index("moderator-mid@example.com") < body.index("user-old@example.com")

    filtered_body = _page_body(client, "/admin/users?role=user")
    assert "user-old@example.com" in filtered_body
    assert "moderator-mid@example.com" not in filtered_body
    assert "admin-new@example.com" not in filtered_body

    filtered_body = _page_body(client, "/admin/users?role=moderator")
    assert "moderator-mid@example.com" in filtered_body
    assert "user-old@example.com" not in filtered_body
    assert "admin-new@example.com" not in filtered_body

    filtered_body = _page_body(client, "/admin/users?role=admin")
    assert "admin-new@example.com" in filtered_body
    assert "user-old@example.com" not in filtered_body
    assert "moderator-mid@example.com" not in filtered_body


def test_admin_users_page_access_status_filters(client, test_settings):
    _seed_user_list(test_settings)
    _login_admin(client, test_settings)

    filtered_body = _page_body(client, "/admin/users?access_status=not_activated")
    assert "user-old@example.com" in filtered_body
    assert "admin-new@example.com" in filtered_body
    assert "moderator-mid@example.com" not in filtered_body

    filtered_body = _page_body(client, "/admin/users?access_status=activated")
    assert "moderator-mid@example.com" in filtered_body
    assert "user-old@example.com" not in filtered_body
    assert "admin-new@example.com" not in filtered_body


def test_admin_users_page_date_range_filters(client, test_settings):
    _seed_user_list(test_settings)
    _login_admin(client, test_settings)

    filtered_body = _page_body(client, "/admin/users?created_from=2026-01-12")
    assert "moderator-mid@example.com" in filtered_body
    assert "admin-new@example.com" in filtered_body
    assert "user-old@example.com" not in filtered_body

    filtered_body = _page_body(client, "/admin/users?created_to=2026-01-15")
    assert "user-old@example.com" in filtered_body
    assert "moderator-mid@example.com" in filtered_body
    assert "admin-new@example.com" not in filtered_body

    filtered_body = _page_body(client, "/admin/users?created_from=2026-01-11&created_to=2026-01-16")
    assert "moderator-mid@example.com" in filtered_body
    assert "user-old@example.com" not in filtered_body
    assert "admin-new@example.com" not in filtered_body


def test_admin_users_page_created_sort_orders(client, test_settings):
    _seed_user_list(test_settings)
    _login_admin(client, test_settings)

    desc_body = _page_body(client, "/admin/users?created_sort=desc")
    assert desc_body.index("admin-new@example.com") < desc_body.index("moderator-mid@example.com") < desc_body.index("user-old@example.com")

    asc_body = _page_body(client, "/admin/users?created_sort=asc")
    assert asc_body.index("user-old@example.com") < asc_body.index("moderator-mid@example.com") < asc_body.index("admin-new@example.com")


@pytest.mark.parametrize(
    ("path", "expected"),
    [
        ("/admin/users?role=owner", "Выберите допустимую роль."),
        ("/admin/users?access_status=archived", "Выберите допустимый статус доступа."),
        ("/admin/users?created_from=2026-13-01", "Укажите корректную дату регистрации."),
        ("/admin/users?created_to=2026-02-30", "Укажите корректную дату регистрации."),
        ("/admin/users?created_sort=sideways", "Выберите допустимый порядок сортировки."),
    ],
)
def test_admin_users_page_rejects_invalid_filters(client, test_settings, path, expected):
    _seed_user_list(test_settings)
    _login_admin(client, test_settings)

    response = client.get(path)
    assert response.status_code == 400
    assert expected in response.text


def test_admin_users_role_change_preserves_query_filters(client, test_settings):
    _seed_user_list(test_settings)
    _login_admin(client, test_settings)

    page = _page_body(client, "/admin/users")
    csrf_token = _extract_csrf_token(page)

    with _connect(test_settings) as conn:
        row = conn.execute("SELECT id FROM users WHERE email = ?", ("user-old@example.com",)).fetchone()
    assert row is not None

    response = client.post(
        f"/admin/users/{row['id']}/role?role=user&created_sort=desc",
        data={"role": "moderator", "_csrf_token": csrf_token},
        follow_redirects=False,
    )
    assert response.status_code == 303
    assert response.headers["location"] == "/admin/users?role=user&created_sort=desc"


def test_admin_users_page_stays_safe(client, test_settings):
    _seed_user_list(test_settings)
    _login_admin(client, test_settings)

    body = _page_body(client, "/admin/users?role=user&created_sort=desc")
    assert "password_hash" not in body.lower()
    assert "token_hash" not in body.lower()
    assert "raw token" not in body.lower()
    assert "cookie" not in body.lower()
    assert "email_outbox" not in body.lower()


def test_admin_users_page_paginates_results(client, test_settings):
    _seed_paginated_user_list(test_settings)
    _login_admin(client, test_settings)

    page_one = _page_body(client, "/admin/users?created_sort=desc&page=1")
    assert "Страница 1 из 2" in page_one
    assert re.search(r'href="/admin/users\?created_sort=desc(?:&amp;|&)page=2"', page_one)
    assert "admin-new@example.com" in page_one
    assert "user-001@example.com" not in page_one
    assert "Модератор" in page_one

    page_two = _page_body(client, "/admin/users?created_sort=desc&page=2")
    assert "Страница 2 из 2" in page_two
    assert "admin-new@example.com" not in page_two
    assert "user-001@example.com" in page_two
    assert re.search(r'href="/admin/users\?created_sort=desc(?:&amp;|&)page=1"', page_two)


def test_admin_users_page_handles_invalid_page_values(client, test_settings):
    _seed_paginated_user_list(test_settings)
    _login_admin(client, test_settings)

    invalid_page_body = _page_body(client, "/admin/users?created_sort=desc&page=not-a-number")
    assert "Страница 1 из 2" in invalid_page_body
    assert "admin-new@example.com" in invalid_page_body
    assert "user-001@example.com" not in invalid_page_body

    overflow_page_body = _page_body(client, "/admin/users?created_sort=desc&page=999")
    assert "Страница 2 из 2" in overflow_page_body
    assert "admin-new@example.com" not in overflow_page_body
    assert "user-001@example.com" in overflow_page_body


def test_list_users_for_admin_supports_filters_and_safe_fields(test_settings):
    _seed_user_list(test_settings)

    users_desc = list_users_for_admin(settings=test_settings)
    assert [user["email"] for user in users_desc] == [
        "admin-new@example.com",
        "moderator-mid@example.com",
        "user-old@example.com",
    ]
    assert all("password_hash" not in user for user in users_desc)
    assert all("token_hash" not in user for user in users_desc)

    users_role = list_users_for_admin(settings=test_settings, role="moderator")
    assert [user["email"] for user in users_role] == ["moderator-mid@example.com"]

    users_status = list_users_for_admin(settings=test_settings, access_status="activated")
    assert [user["email"] for user in users_status] == ["moderator-mid@example.com"]

    users_from = list_users_for_admin(settings=test_settings, created_from=datetime(2026, 1, 12, tzinfo=timezone.utc).date())
    assert [user["email"] for user in users_from] == ["admin-new@example.com", "moderator-mid@example.com"]


def test_list_users_for_admin_page_supports_bounds_and_metadata(test_settings):
    _seed_paginated_user_list(test_settings)

    page_one = list_users_for_admin_page(settings=test_settings, created_sort="asc")
    assert page_one["pagination"]["page"] == 1
    assert page_one["pagination"]["page_size"] == ADMIN_USER_PAGE_SIZE
    assert page_one["pagination"]["total_count"] == ADMIN_USER_PAGE_SIZE + 1
    assert page_one["pagination"]["total_pages"] == 2
    assert page_one["pagination"]["has_previous"] is False
    assert page_one["pagination"]["has_next"] is True
    assert page_one["pagination"]["next_page"] == 2
    assert len(page_one["users"]) == ADMIN_USER_PAGE_SIZE
    assert page_one["users"][0]["email"] == "user-001@example.com"
    assert page_one["users"][-1]["email"] == "user-050@example.com"

    page_last = list_users_for_admin_page(settings=test_settings, page=999, created_sort="asc")
    assert page_last["pagination"]["page"] == 2
    assert page_last["pagination"]["has_previous"] is True
    assert page_last["pagination"]["has_next"] is False
    assert page_last["pagination"]["previous_page"] == 1
    assert [user["email"] for user in page_last["users"]] == ["admin-new@example.com"]
