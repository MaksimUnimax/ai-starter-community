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
    sort_order: int
    created_at: str
    updated_at: str

