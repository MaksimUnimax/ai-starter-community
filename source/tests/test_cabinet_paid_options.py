from __future__ import annotations

import re
import sqlite3

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


def _extract_paid_option_titles(body: str) -> list[str]:
    return re.findall(r'<h3 class="paid-option__title">([^<]+)</h3>', body)


def test_cabinet_paid_options_block_hides_base_option_and_sorts_visible_addons(client, test_settings):
    _create_paid_option(
        test_settings,
        code="ai_gpt_tool",
        title="AI / GPT-инструмент",
        description="Базовый AI-инструмент для старта.",
        price_amount_minor=699000,
        currency="RUB",
        default_duration_days=None,
        status="active",
        is_renewable=True,
        sort_order=0,
    )
    _create_paid_option(
        test_settings,
        code="cabinet_addon_two_thousand_chatgpt_plus",
        title="Chat GPT Plus",
        description="Оплаченный на месяц аккаунт Chat GPT Plus",
        price_amount_minor=200000,
        currency="RUB",
        default_duration_days=30,
        status="active",
        is_renewable=True,
        sort_order=0,
    )
    _create_paid_option(
        test_settings,
        code="cabinet_addon_four_thousand_server_plus_chatgpt",
        title="Сервер + ChatGPT Plus",
        description="Аренда сервера, плюс оплаченный аккаунт ChatGPT Plus.",
        price_amount_minor=400000,
        currency="RUB",
        default_duration_days=30,
        status="active",
        is_renewable=True,
        sort_order=0,
    )
    _create_paid_option(
        test_settings,
        code="cabinet_addon_two_thousand_server",
        title="Сервер",
        description="Аренда сервера.",
        price_amount_minor=200000,
        currency="RUB",
        default_duration_days=30,
        status="active",
        is_renewable=True,
        sort_order=1,
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
    _create_paid_option(
        test_settings,
        code="cabinet_hidden_option",
        title="Скрытая опция",
        description="Не должна отображаться в кабинете.",
        price_amount_minor=100000,
        currency="RUB",
        default_duration_days=30,
        status="hidden",
        is_renewable=True,
        sort_order=99,
    )

    active_option_codes = {item.code for item in list_paid_options(settings=test_settings)}
    assert active_option_codes == {
        "ai_gpt_tool",
        "cabinet_addon_two_thousand_chatgpt_plus",
        "cabinet_addon_four_thousand_server_plus_chatgpt",
        "cabinet_addon_two_thousand_server",
    }
    assert "cabinet_archived_option" not in active_option_codes
    assert "cabinet_hidden_option" not in active_option_codes

    _login_registered_user(client, test_settings, "cabinet-paid-options@example.com", "cabinetpaidoptions")

    response = client.get("/cabinet")
    assert response.status_code == 200
    body = response.text

    assert body.index('data-local-accounts-root') < body.index('data-prompts-library-root') < body.index('data-paid-options-root')
    assert "Активация опций" in body
    assert "Доступно для подключения: 3" in body
    assert "Сейчас активных опций" not in body
    assert "Здесь показаны активные платные опции, которые можно будет подключать к аккаунту." in body
    assert "AI / GPT-инструмент" not in body
    assert "ai_gpt_tool" not in body
    assert "Архивная опция" not in body
    assert "Скрытая опция" not in body
    assert "Сервер + ChatGPT Plus" in body
    assert "Chat GPT Plus" in body
    assert "Сервер" in body
    assert _extract_paid_option_titles(body) == [
        "Сервер + ChatGPT Plus",
        "Chat GPT Plus",
        "Сервер",
    ]
    assert "4 000 ₽" in body
    assert body.index("4 000 ₽") < body.index("2 000 ₽")
    assert body.count('type="button" data-paid-option-buy>Купить</button>') == 3
    assert body.count('data-paid-option-card') == 3
    assert 'data-paid-options-list' in body
    assert 'data-paid-options-notice' in body
    assert 'Оплата пока не подключена. Эта кнопка подготовлена для следующего этапа.' in body
    assert '/cabinet/payments' not in body
    assert '/admin/payments' not in body
    assert '/cabinet/paid-options' not in body
    assert "Аккаунты" in body
    assert "Промпты" in body
    assert "Промпты из курса" in body


def test_cabinet_paid_options_block_places_null_price_last_when_present(client, test_settings):
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
        sort_order=2,
    )
    _create_paid_option(
        test_settings,
        code="cabinet_active_two_thousand_a",
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
        code="cabinet_active_four_thousand",
        title="Опция на 4 000 ₽",
        description="Активная опция с сроком.",
        price_amount_minor=400000,
        currency="RUB",
        default_duration_days=30,
        status="active",
        is_renewable=True,
        sort_order=0,
    )
    _create_paid_option(
        test_settings,
        code="cabinet_active_two_thousand_b",
        title="Опция на 2 000 ₽, вторая",
        description="Еще одна активная опция.",
        price_amount_minor=200000,
        currency="RUB",
        default_duration_days=30,
        status="active",
        is_renewable=True,
        sort_order=3,
    )

    _login_registered_user(client, test_settings, "cabinet-paid-options-null-price@example.com", "cabinetpaidoptionsnullprice")

    response = client.get("/cabinet")
    assert response.status_code == 200
    body = response.text

    assert "Доступно для подключения: 4" in body
    assert _extract_paid_option_titles(body) == [
        "Опция на 4 000 ₽",
        "Опция на 2 000 ₽",
        "Опция на 2 000 ₽, вторая",
        "Опция без цены",
    ]
    assert body.index("4 000 ₽") < body.index("2 000 ₽")
    assert body.rindex("2 000 ₽") < body.index("Цена не указана")
    assert body.count('type="button" data-paid-option-buy>Купить</button>') == 4
    assert 'Оплата пока не подключена. Эта кнопка подготовлена для следующего этапа.' in body
