from __future__ import annotations

from app.tariffs.service import create_tariff, get_homepage_tariff


def test_homepage_tariff_selection_prefers_lowest_sort_order_active_visible_tariff(test_settings):
    create_tariff(
        code="homepage_later",
        title="Homepage later",
        price_amount_minor=1000,
        currency="RUB",
        status="active",
        show_on_homepage=True,
        sort_order=10,
        settings=test_settings,
    )
    create_tariff(
        code="homepage_first",
        title="Homepage first",
        price_amount_minor=2000,
        currency="RUB",
        status="active",
        show_on_homepage=True,
        sort_order=1,
        settings=test_settings,
    )

    homepage_tariff = get_homepage_tariff(settings=test_settings)
    assert homepage_tariff is not None
    assert homepage_tariff.code == "homepage_first"
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
