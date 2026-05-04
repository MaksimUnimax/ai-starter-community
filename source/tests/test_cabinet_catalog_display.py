from __future__ import annotations

from app.auth.service import register_user, verify_email
from app.tariffs.service import seed_initial_catalog


def _verify_registered_user(client, test_settings, email: str, login: str):
    register_user(
        email=email,
        login=login,
        password="Secret123",
        repeat_password="Secret123",
        settings=test_settings,
    )
    outbox = client.get("/check-email?registered=1")
    assert outbox.status_code == 200


def _extract_token_from_db(test_settings, email: str):
    import sqlite3

    with sqlite3.connect(test_settings.database_path) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT body_text FROM email_outbox WHERE recipient_email = ? AND template_key = ? ORDER BY id DESC LIMIT 1",
            (email, "email_verification"),
        ).fetchone()
    assert row is not None
    import re

    match = re.search(r"/verify-email/([A-Za-z0-9_-]+)", row["body_text"])
    assert match
    return match.group(1)


def test_cabinet_displays_active_tariff_catalog_and_no_payment_action(client, test_settings):
    seed_initial_catalog(settings=test_settings)
    _verify_registered_user(client, test_settings, "cabinet-catalog@example.com", "cabinetcatalog")
    token = _extract_token_from_db(test_settings, "cabinet-catalog@example.com")
    verify_email(token, settings=test_settings)

    login_response = client.post(
        "/login",
        data={"email_or_login": "cabinet-catalog@example.com", "password": "Secret123"},
        follow_redirects=False,
    )
    assert login_response.status_code == 303

    cabinet_response = client.get("/cabinet")
    assert cabinet_response.status_code == 200
    assert "Доступ не активирован" in cabinet_response.text
    assert "Стартовый доступ" in cabinet_response.text
    assert "4990 ₽" in cabinet_response.text
    assert "AI / GPT-инструмент" in cabinet_response.text
    assert "Сервер" in cabinet_response.text
    assert "VPN" in cabinet_response.text
    assert "Оплата будет подключена следующим этапом" in cabinet_response.text
    assert "action=\"/checkout\"" not in cabinet_response.text
    assert "checkout" not in cabinet_response.text.lower()

