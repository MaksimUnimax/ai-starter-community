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


PaidOptionView = PaidOptionPublic


@dataclass(frozen=True, slots=True)
class PaidOptionCreateInput:
    code: str
    title: str
    description: str | None = None
    price_amount_minor: int | None = None
    currency: str = "RUB"
    default_duration_days: int | None = None
    status: str = "active"
    is_renewable: bool = True
    sort_order: int = 0


@dataclass(frozen=True, slots=True)
class PaidOptionUpdateInput:
    title: str | None = None
    description: str | None = None
    price_amount_minor: int | None = None
    currency: str | None = None
    default_duration_days: int | None = None
    status: str | None = None
    is_renewable: bool | None = None
    sort_order: int | None = None
