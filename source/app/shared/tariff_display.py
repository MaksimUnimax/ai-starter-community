"""Shared tariff display helpers."""

from __future__ import annotations

from decimal import Decimal

from app.core.config import Settings, get_settings
from app.tariffs.service import get_homepage_tariff, list_homepage_tariffs


def format_tariff_price(amount_minor: int | None, currency: str | None) -> str:
    if amount_minor is None:
        return "Цена не указана"

    amount = Decimal(int(amount_minor)) / Decimal(100)
    if amount == amount.to_integral():
        amount_text = f"{int(amount):,}".replace(",", " ")
    else:
        amount_text = f"{amount:,.2f}".replace(",", " ").replace(".", ",")

    currency_code = (currency or "RUB").upper()
    currency_suffix = "₽" if currency_code == "RUB" else currency_code
    return f"{amount_text} {currency_suffix}"


def _tariff_alignment_class(pricing_text_align: str | None) -> str:
    align = "left" if pricing_text_align is None else str(pricing_text_align).strip().lower()
    if align not in {"left", "center"}:
        align = "left"
    return f"tariff-card-align-{align}"


def _tariff_card_context(tariff, *, is_primary: bool) -> dict[str, object]:
    return {
        "id": tariff.id,
        "code": tariff.code,
        "title": tariff.title,
        "description": tariff.description,
        "price_display": format_tariff_price(tariff.price_amount_minor, tariff.currency),
        "sort_order": tariff.sort_order,
        "pricing_text_align": tariff.pricing_text_align,
        "alignment_class": _tariff_alignment_class(tariff.pricing_text_align),
        "is_primary": is_primary,
    }


def get_homepage_tariff_context(settings: Settings | None = None) -> dict[str, object]:
    resolved = settings or get_settings()
    homepage_tariff = get_homepage_tariff(settings=resolved)
    return {
        "homepage_tariff": homepage_tariff,
        "homepage_tariff_price_display": (
            format_tariff_price(homepage_tariff.price_amount_minor, homepage_tariff.currency)
            if homepage_tariff is not None
            else None
        ),
        "homepage_tariff_card": _tariff_card_context(homepage_tariff, is_primary=True) if homepage_tariff is not None else None,
    }


def get_homepage_tariffs_context(
    settings: Settings | None = None,
    *,
    limit: int | None = None,
) -> dict[str, object]:
    resolved = settings or get_settings()
    homepage_tariffs = list_homepage_tariffs(settings=resolved, limit=limit)
    homepage_tariff_cards = [
        _tariff_card_context(tariff, is_primary=index == 0)
        for index, tariff in enumerate(homepage_tariffs)
    ]
    homepage_tariff = homepage_tariffs[0] if homepage_tariffs else None
    return {
        "homepage_tariff": homepage_tariff,
        "homepage_tariff_price_display": (
            format_tariff_price(homepage_tariff.price_amount_minor, homepage_tariff.currency)
            if homepage_tariff is not None
            else None
        ),
        "homepage_tariff_card": _tariff_card_context(homepage_tariff, is_primary=True) if homepage_tariff is not None else None,
        "homepage_tariffs": homepage_tariffs,
        "homepage_tariff_cards": homepage_tariff_cards,
    }
