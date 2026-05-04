"""Paid option catalog schemas."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PaidOptionPublic:
    id: int
    code: str
    title: str
    description: str | None
    price_amount_minor: int | None
    currency: str
    default_duration_days: int | None
    status: str
    is_renewable: bool
    sort_order: int
    created_at: str
    updated_at: str

