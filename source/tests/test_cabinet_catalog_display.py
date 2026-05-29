from __future__ import annotations

from app.auth.service import register_user, verify_email


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


def test_cabinet_displays_course_shell_without_tariffs_or_payment_noise(client, test_settings):
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
    assert "/static/styles.css" in cabinet_response.text
    assert "Личный кабинет" in cabinet_response.text
    assert "Настройки" in cabinet_response.text
    assert "⚙" not in cabinet_response.text
    assert 'href="/cabinet/settings"' in cabinet_response.text
    assert "Аккаунт" in cabinet_response.text
    assert "Логин: <strong>cabinetcatalog</strong>" in cabinet_response.text
    assert "Email: cabinet-catalog@example.com" in cabinet_response.text
    assert "Главная" in cabinet_response.text
    assert "Обучение" in cabinet_response.text
    assert "Работа с ИИ" not in cabinet_response.text
    assert "Здесь находится курс и материалы по работе с ИИ." in cabinet_response.text
    assert "Перейти к обучению" in cabinet_response.text
    assert "/materials/drafts/dair-smoke-20260529/" in cabinet_response.text
    assert cabinet_response.text.index("<h2 class=\"section-title\">Обучение</h2>") < cabinet_response.text.index("<h2 class=\"section-title\">Аккаунт</h2>")
    assert "Доступные тарифы" not in cabinet_response.text
    assert "Оплата" not in cabinet_response.text
    assert "Что дальше" not in cabinet_response.text
    assert "Раздел «Работа с ИИ» будет доступен после оплаты." not in cabinet_response.text
    assert "активирован" not in cabinet_response.text
    assert "доступен по роли" not in cabinet_response.text
    assert "Стартовый доступ" not in cabinet_response.text
    assert "Оплата будет подключена позже." not in cabinet_response.text
    assert "Последний платёж" not in cabinet_response.text
