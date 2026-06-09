"""Tariff catalog schemas."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TariffPublic:
    id: int
    code: str
    title: str
    description: str | None
    price_amount_minor: int
    currency: str
    status: str
    show_on_homepage: bool
    sort_order: int
    created_at: str
    updated_at: str


TariffView = TariffPublic


@dataclass(frozen=True, slots=True)
class TariffCreateInput:
    title: str
    description: str | None = None
    price_amount_minor: int = 0
    currency: str = "RUB"
    status: str = "active"
    show_on_homepage: bool = False
    sort_order: int = 0
    code: str | None = None


@dataclass(frozen=True, slots=True)
class TariffUpdateInput:
    title: str | None = None
    description: str | None = None
    price_amount_minor: int | None = None
    currency: str | None = None
    status: str | None = None
    show_on_homepage: bool | None = None
    sort_order: int | None = None


@dataclass(frozen=True, slots=True)
class TariffOptionLinkInput:
    included_duration_days: int | None = None
    included_quantity: int | None = None
