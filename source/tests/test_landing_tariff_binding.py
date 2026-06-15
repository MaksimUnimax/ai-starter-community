from __future__ import annotations

from app.tariffs.service import (
    STARTER_TARIFF_CODE,
    create_tariff,
    get_homepage_tariff,
    seed_initial_catalog,
    update_tariff,
)
from app.shared.tariff_display import get_homepage_tariff_context, get_homepage_tariffs_context


def test_homepage_tariff_selection_prefers_selected_tariff_over_first_active(test_settings):
    seed_initial_catalog(settings=test_settings)
    update_tariff(
        STARTER_TARIFF_CODE,
        show_on_homepage=False,
        settings=test_settings,
    )
    create_tariff(
        code="homepage_first",
        title="Homepage first",
        price_amount_minor=1000,
        currency="RUB",
        status="active",
        show_on_homepage=False,
        sort_order=1,
        settings=test_settings,
    )
    create_tariff(
        code="homepage_selected",
        title="Homepage selected",
        price_amount_minor=2000,
        currency="RUB",
        status="active",
        show_on_homepage=True,
        sort_order=10,
        settings=test_settings,
    )

    homepage_tariff = get_homepage_tariff(settings=test_settings)
    assert homepage_tariff is not None
    assert homepage_tariff.code == "homepage_selected"
    assert homepage_tariff.show_on_homepage is True


def test_homepage_tariff_selection_skips_inactive_tariffs(test_settings):
    create_tariff(
        code="homepage_hidden",
        title="Homepage hidden",
        price_amount_minor=3000,
        currency="RUB",
        status="hidden",
        show_on_homepage=True,
        sort_order=0,
        settings=test_settings,
    )
    create_tariff(
        code="homepage_active",
        title="Homepage active",
        price_amount_minor=4000,
        currency="RUB",
        status="active",
        show_on_homepage=True,
        sort_order=2,
        settings=test_settings,
    )

    homepage_tariff = get_homepage_tariff(settings=test_settings)
    assert homepage_tariff is not None
    assert homepage_tariff.code == "homepage_active"
    assert homepage_tariff.status == "active"


def test_landing_page_uses_homepage_tariff_price(client, test_settings):
    seed_initial_catalog(settings=test_settings)
    update_tariff(
        STARTER_TARIFF_CODE,
        show_on_homepage=False,
        settings=test_settings,
    )
    create_tariff(
        code="homepage_tariff_selected",
        title="Homepage tariff selected",
        price_amount_minor=699000,
        currency="RUB",
        status="active",
        show_on_homepage=True,
        sort_order=10,
        settings=test_settings,
    )
    update_tariff(
        STARTER_TARIFF_CODE,
        price_amount_minor=499000,
        settings=test_settings,
    )

    response = client.get("/")
    assert response.status_code == 200
    assert "Homepage tariff selected — 6 990 ₽" in response.text
    assert "Что входит в 6 990 ₽?" in response.text
    assert "4 990 ₽" not in response.text


def test_homepage_tariffs_context_returns_two_selected_tariffs_in_stable_order(test_settings):
    seed_initial_catalog(settings=test_settings)
    update_tariff(
        STARTER_TARIFF_CODE,
        show_on_homepage=False,
        settings=test_settings,
    )
    create_tariff(
        code="homepage_selected_alpha",
        title="Homepage selected alpha",
        price_amount_minor=200000,
        currency="RUB",
        status="active",
        show_on_homepage=True,
        sort_order=1,
        settings=test_settings,
    )
    create_tariff(
        code="homepage_selected_beta",
        title="Homepage selected beta",
        price_amount_minor=300000,
        currency="RUB",
        status="active",
        show_on_homepage=True,
        sort_order=1,
        pricing_text_align="center",
        settings=test_settings,
    )
    create_tariff(
        code="homepage_selected_gamma",
        title="Homepage selected gamma",
        price_amount_minor=400000,
        currency="RUB",
        status="active",
        show_on_homepage=True,
        sort_order=2,
        settings=test_settings,
    )

    context = get_homepage_tariffs_context(settings=test_settings, limit=2)

    assert [tariff.code for tariff in context["homepage_tariffs"]] == [
        "homepage_selected_alpha",
        "homepage_selected_beta",
    ]
    assert [card["title"] for card in context["homepage_tariff_cards"]] == [
        "Homepage selected alpha",
        "Homepage selected beta",
    ]
    assert [card["alignment_class"] for card in context["homepage_tariff_cards"]] == [
        "tariff-card-align-left",
        "tariff-card-align-center",
    ]
    assert context["homepage_tariff"].code == "homepage_selected_alpha"
    assert context["homepage_tariff_price_display"] == "2 000 ₽"
    single_context = get_homepage_tariff_context(settings=test_settings)
    assert single_context["homepage_tariff"] is not None
    assert single_context["homepage_tariff_card"] is not None
    assert single_context["homepage_tariff_card"]["alignment_class"] == "tariff-card-align-left"
