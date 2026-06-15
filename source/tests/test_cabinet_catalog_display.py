from __future__ import annotations

import re
import sqlite3

from app.auth.service import register_user, verify_email
from app.shared.tariff_display import get_homepage_tariff_context
from app.tariffs.service import STARTER_TARIFF_CODE, create_tariff, seed_initial_catalog, update_tariff


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


def _extract_accounts_section(body_text: str) -> str:
    match = re.search(
        r'<section class="card stack accounts-card" data-local-accounts-root>(.*?)</section>',
        body_text,
        re.S,
    )
    assert match is not None
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
    assert "Главная" in cabinet_response.text
    assert "Личный кабинет будет доступен после оплаты" in cabinet_response.text
    assert "После оплаты тарифа откроются личный кабинет, обучение и материалы." in cabinet_response.text
    assert "Доступ ограничен" in cabinet_response.text
    assert "nav-account-compact" in cabinet_response.text
    assert "nav-account-name" in cabinet_response.text
    assert "nav-account-email" not in cabinet_response.text
    assert "nav-account-dropdown" in cabinet_response.text
    assert "nav-account-menu" in cabinet_response.text
    assert "nav-account-link" not in cabinet_response.text
    assert "nav-settings" not in cabinet_response.text
    assert 'href="/cabinet/settings"' in cabinet_response.text
    assert '/static/account-menu.js' in cabinet_response.text
    assert "Обучение" in cabinet_response.text
    assert "hero-bg-desktop" in cabinet_response.text
    assert "hero-bg-mobile" in cabinet_response.text
    assert "Обучающий проект" not in cabinet_response.text
    assert "Перейти к обучению" not in cabinet_response.text
    assert "Скачать файл" not in cabinet_response.text
    assert "Пройдите обучение, затем скачайте файл, вставьте в чат ChatGPT и следуйте его инструкциям." not in cabinet_response.text
    assert cabinet_response.text.count('class="button button-primary learning-button"') == 0
    assert "Доступ откроется после оплаты." not in cabinet_response.text
    assert "Аккаунты" not in cabinet_response.text
    assert "Промпты" not in cabinet_response.text
    assert "data-local-accounts-root" not in cabinet_response.text
    assert "data-prompts-library-root" not in cabinet_response.text
    assert "/static/cabinet-local-accounts.js" not in cabinet_response.text
    assert "/static/cabinet-prompts-library.js" not in cabinet_response.text
    assert 'href="/materials/drafts/dair-smoke-20260529/"' in cabinet_response.text
    assert 'href="/cabinet/learning/project-file"' not in cabinet_response.text
    assert "raw.githubusercontent.com" not in cabinet_response.text
    assert "Доступные тарифы" not in cabinet_response.text
    assert "Оплата" not in cabinet_response.text
    assert "Что дальше" not in cabinet_response.text
    assert "Раздел «Работа с ИИ» будет доступен после оплаты." not in cabinet_response.text
    assert "активирован" not in cabinet_response.text
    assert "доступен по роли" not in cabinet_response.text
    assert "Стартовый доступ" not in cabinet_response.text
    assert "Оплата будет подключена позже." not in cabinet_response.text
    assert "Последний платёж" not in cabinet_response.text
    homepage_tariff_context = get_homepage_tariff_context(settings=test_settings)
    if homepage_tariff_context["homepage_tariff"] is not None:
        assert homepage_tariff_context["homepage_tariff"].title in cabinet_response.text
        assert homepage_tariff_context["homepage_tariff_price_display"] in cabinet_response.text
    assert "access-locked-pricing" in cabinet_response.text
    assert "pricing-actions" not in cabinet_response.text


def test_cabinet_shows_active_learning_links_when_access_granted(client, test_settings):
    _verify_registered_user(client, test_settings, "cabinet-access@example.com", "cabinetaccess")
    token = _extract_token_from_db(test_settings, "cabinet-access@example.com")
    verify_email(token, settings=test_settings)

    with sqlite3.connect(test_settings.database_path) as conn:
        conn.execute(
            "UPDATE users SET materials_access_granted_at = CURRENT_TIMESTAMP WHERE email = ?",
            ("cabinet-access@example.com",),
        )
        conn.commit()

    login_response = client.post(
        "/login",
        data={"email_or_login": "cabinet-access@example.com", "password": "Secret123"},
        follow_redirects=False,
    )
    assert login_response.status_code == 303

    cabinet_response = client.get("/cabinet")
    assert cabinet_response.status_code == 200
    assert "Обучающий блок" in cabinet_response.text
    assert "Обучение" in cabinet_response.text
    assert "Обучающий проект" in cabinet_response.text
    assert "nav-account-compact" in cabinet_response.text
    assert "nav-account-dropdown" in cabinet_response.text
    assert "nav-account-menu" in cabinet_response.text
    assert "nav-account-link" not in cabinet_response.text
    assert "nav-settings" not in cabinet_response.text
    assert 'href="/cabinet/settings"' in cabinet_response.text
    assert 'href="/materials/drafts/dair-smoke-20260529/"' in cabinet_response.text
    assert "Доступ откроется после оплаты." not in cabinet_response.text
    assert 'href="/cabinet/learning/project-file"' in cabinet_response.text
    assert "Перейти к обучению" in cabinet_response.text
    assert "Скачать файл" in cabinet_response.text
    assert "Пройдите обучение, затем скачайте файл, вставьте в чат ChatGPT и следуйте его инструкциям." in cabinet_response.text
    assert cabinet_response.text.count('class="button button-primary learning-button"') == 2
    assert "raw.githubusercontent.com" not in cabinet_response.text

    client.cookies.clear()
    _verify_registered_user(client, test_settings, "cabinet-admin-access@example.com", "cabinetadminaccess")
    token = _extract_token_from_db(test_settings, "cabinet-admin-access@example.com")
    verify_email(token, settings=test_settings)
    with sqlite3.connect(test_settings.database_path) as conn:
        conn.execute(
            "UPDATE users SET role = 'admin' WHERE email = ?",
            ("cabinet-admin-access@example.com",),
        )
        conn.commit()
    login_response = client.post(
        "/login",
        data={"email_or_login": "cabinet-admin-access@example.com", "password": "Secret123"},
        follow_redirects=False,
    )
    assert login_response.status_code == 303
    admin_response = client.get("/cabinet")
    assert admin_response.status_code == 200
    assert "Обучающий блок" in admin_response.text
    assert "Доступ откроется после оплаты." not in admin_response.text
    assert "nav-account-compact" in admin_response.text
    assert "nav-account-dropdown" in admin_response.text
    assert "nav-account-menu" in admin_response.text
    assert "nav-account-link" not in admin_response.text
    assert "nav-settings" not in admin_response.text
    assert 'href="/cabinet/settings"' in admin_response.text
    assert 'href="/materials/drafts/dair-smoke-20260529/"' in admin_response.text
    assert 'href="/cabinet/learning/project-file"' in admin_response.text


def test_locked_cabinet_pricing_renders_two_selected_tariffs(client, test_settings):
    seed_initial_catalog(settings=test_settings)
    update_tariff(
        STARTER_TARIFF_CODE,
        show_on_homepage=False,
        settings=test_settings,
    )
    create_tariff(
        code="cabinet_selected_alpha",
        title="Cabinet selected alpha",
        description="Первая выбранная тарифная карточка.",
        price_amount_minor=200000,
        currency="RUB",
        status="active",
        show_on_homepage=True,
        sort_order=1,
        title_font_size_px=24,
        price_font_size_px=38,
        description_font_size_px=14,
        settings=test_settings,
    )
    create_tariff(
        code="cabinet_selected_beta",
        title="Cabinet selected beta",
        description="Вторая выбранная тарифная карточка.",
        price_amount_minor=300000,
        currency="RUB",
        status="active",
        show_on_homepage=True,
        sort_order=2,
        pricing_text_align="center",
        title_font_size_px=28,
        price_font_size_px=42,
        description_font_size_px=16,
        settings=test_settings,
    )
    _verify_registered_user(client, test_settings, "cabinet-selected@example.com", "cabinetselected")
    token = _extract_token_from_db(test_settings, "cabinet-selected@example.com")
    verify_email(token, settings=test_settings)

    login_response = client.post(
        "/login",
        data={"email_or_login": "cabinet-selected@example.com", "password": "Secret123"},
        follow_redirects=False,
    )
    assert login_response.status_code == 303

    cabinet_response = client.get("/cabinet")
    assert cabinet_response.status_code == 200
    body = cabinet_response.text
    assert "Cabinet selected alpha" in body
    assert "Cabinet selected beta" in body
    assert "2 000 ₽" in body
    assert "3 000 ₽" in body
    assert body.index("Cabinet selected alpha") < body.index("Cabinet selected beta")
    assert body.count("pricing-tariff-card") >= 2
    assert body.count("pricing-tariff-title") >= 2
    assert body.count("pricing-tariff-price") >= 2
    assert body.count("pricing-tariff-description") >= 2
    assert body.count('class="pricing-tariff-card') >= 2
    assert body.count("--tariff-title-font-size: 24px") == 1
    assert body.count("--tariff-title-font-size: 28px") == 1
    assert body.count("--tariff-price-font-size: 38px") == 1
    assert body.count("--tariff-price-font-size: 42px") == 1
    assert body.count("--tariff-description-font-size: 14px") == 1
    assert body.count("--tariff-description-font-size: 16px") == 1
    assert "pricing-tariff-badge" not in body
    assert "ТАРИФ 1" not in body
    assert "ТАРИФ 2" not in body
    assert '<article class="pricing-tariff-card pricing-tariff-card--featured tariff-card-align-left"' in body
    assert '<article class="pricing-tariff-card tariff-card-align-center"' in body
    assert "tariff-card-align-left" in body
    assert "tariff-card-align-center" in body
    assert "access-locked-pricing" in body
