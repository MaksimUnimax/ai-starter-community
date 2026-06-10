"""Shared tariff display helpers."""

from __future__ import annotations

from decimal import Decimal

from app.core.config import Settings, get_settings
from app.tariffs.service import get_homepage_tariff


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
    }
