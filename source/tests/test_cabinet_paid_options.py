from __future__ import annotations

import re
import sqlite3
from pathlib import Path

from app.auth.service import register_user, verify_email
from app.paid_options.service import create_paid_option, list_paid_options


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
    with sqlite3.connect(test_settings.database_path) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT body_text FROM email_outbox WHERE recipient_email = ? AND template_key = ? ORDER BY id DESC LIMIT 1",
            (email, "email_verification"),
        ).fetchone()
    assert row is not None
    match = re.search(r"/verify-email/([A-Za-z0-9_-]+)", row["body_text"])
    assert match
    return match.group(1)


def _login_registered_user(client, test_settings, email: str, login: str):
    _verify_registered_user(client, test_settings, email, login)
    token = _extract_token_from_db(test_settings, email)
    verify_email(token, settings=test_settings)

    login_response = client.post(
        "/login",
        data={"email_or_login": email, "password": "Secret123"},
        follow_redirects=False,
    )
    assert login_response.status_code == 303


def _create_paid_option(test_settings, **kwargs):
    return create_paid_option(settings=test_settings, **kwargs)


def test_cabinet_paid_options_block_renders_active_catalog_and_safe_buy_notice(client, test_settings):
    _create_paid_option(
        test_settings,
        code="cabinet_active_null_price",
        title="Опция без цены",
        description="Опция без указанной цены.",
        price_amount_minor=None,
        currency="RUB",
        default_duration_days=None,
        status="active",
        is_renewable=True,
        sort_order=0,
    )
    _create_paid_option(
        test_settings,
        code="cabinet_active_two_thousand",
        title="Опция на 2 000 ₽",
        description="Опция с указанной стоимостью.",
        price_amount_minor=200000,
        currency="RUB",
        default_duration_days=30,
        status="active",
        is_renewable=True,
        sort_order=1,
    )
    _create_paid_option(
        test_settings,
        code="cabinet_active_six_nine_nine",
        title="Опция на 6 990 ₽",
        description="Ещё одна активная опция.",
        price_amount_minor=699000,
        currency="RUB",
        default_duration_days=None,
        status="active",
        is_renewable=False,
        sort_order=2,
    )
    _create_paid_option(
        test_settings,
        code="cabinet_active_four_thousand",
        title="Опция на 4 000 ₽",
        description="Активная опция с сроком.",
        price_amount_minor=400000,
        currency="RUB",
        default_duration_days=30,
        status="active",
        is_renewable=True,
        sort_order=3,
    )
    _create_paid_option(
        test_settings,
        code="cabinet_archived_option",
        title="Архивная опция",
        description="Не должна отображаться в кабинете.",
        price_amount_minor=500000,
        currency="RUB",
        default_duration_days=30,
        status="archived",
        is_renewable=True,
        sort_order=99,
    )

    active_option_codes = {item.code for item in list_paid_options(settings=test_settings)}
    assert active_option_codes == {
        "cabinet_active_null_price",
        "cabinet_active_two_thousand",
        "cabinet_active_six_nine_nine",
        "cabinet_active_four_thousand",
    }
    assert "cabinet_archived_option" not in active_option_codes

    _login_registered_user(client, test_settings, "cabinet-paid-options@example.com", "cabinetpaidoptions")

    response = client.get("/cabinet")
    assert response.status_code == 200
    body = response.text

    assert body.index('data-local-accounts-root') < body.index('data-prompts-library-root') < body.index('data-paid-options-root')
    assert "Активация опций" in body
    assert "Сейчас активных опций: 4" in body
    assert "Здесь показаны активные платные опции, которые можно будет подключать к аккаунту." in body
    assert "Опция без цены" in body
    assert "Опция на 2 000 ₽" in body
    assert "Опция на 6 990 ₽" in body
    assert "Опция на 4 000 ₽" in body
    assert "Архивная опция" not in body
    assert "Цена не указана" in body
    assert "2 000 ₽" in body
    assert "6 990 ₽" in body
    assert "4 000 ₽" in body
    assert "Срок: 30 дней" in body
    assert "Можно продлевать" in body
    assert body.count('type="button" data-paid-option-buy>Купить</button>') == 4
    assert body.count('data-paid-option-card') == 4
    assert 'data-paid-options-list' in body
    assert 'data-paid-options-notice' in body
    assert 'Оплата пока не подключена. Эта кнопка подготовлена для следующего этапа.' in body
    assert '/cabinet/payments' not in body
    assert '/admin/payments' not in body
    assert '/cabinet/paid-options' not in body
    routes_text = Path("/tmp/ai-starter-paid-options-block-20260608/source/app/user_cabinet/routes.py").read_text(encoding="utf-8")
    assert '"/cabinet/payments"' not in routes_text
    assert '"/cabinet/paid-options"' not in routes_text
    assert "payment provider" not in routes_text.lower()
    assert "Аккаунты" in body
    assert "Промпты" in body
    assert "Промпты из курса" in body


def test_cabinet_paid_options_block_shows_empty_state_when_catalog_is_empty(client, test_settings):
    _login_registered_user(client, test_settings, "cabinet-paid-options-empty@example.com", "cabinetpaidoptionsempty")

    response = client.get("/cabinet")
    assert response.status_code == 200
    body = response.text

    assert "Активация опций" in body
    assert "Сейчас активных опций: 0" in body
    assert "Пока нет активных опций для подключения." in body
    assert 'type="button" data-paid-option-buy>Купить</button>' not in body
    assert "data-paid-options-list" not in body
    assert "Аккаунты" in body
    assert "Промпты" in body
