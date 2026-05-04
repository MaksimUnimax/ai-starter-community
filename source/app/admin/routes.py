"""Admin dashboard routes."""

from __future__ import annotations

import re
from decimal import Decimal, InvalidOperation
from pathlib import Path

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.auth.service import get_user_by_session_token, list_users_for_admin
from app.core.config import get_settings
from app.paid_options.service import list_paid_options
from app.shared.utils import page_title
from app.tariffs.schemas import TariffCreateInput, TariffUpdateInput
from app.tariffs.service import (
    ConflictError as TariffConflictError,
    NotFoundError as TariffNotFoundError,
    ValidationError as TariffValidationError,
    archive_tariff,
    create_tariff,
    get_tariff_by_code,
    list_tariff_options,
    list_tariffs_for_admin,
    update_tariff,
)

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))

TARIFF_CODE_RE = re.compile(r"^[a-z0-9_-]{3,64}$")
ALLOWED_TARIFF_STATUSES = {"active", "hidden", "archived"}


def _template(request: Request, template_name: str, **context) -> HTMLResponse:
    status_code = context.pop("status_code", 200)
    payload = {"request": request, "title": context.pop("title", page_title("AI Starter Community"))}
    payload.update(context)
    return templates.TemplateResponse(request, template_name, payload, status_code=status_code)


def _admin_user_or_redirect(request: Request, settings=None):
    resolved = settings or get_settings()
    session_token = request.cookies.get(resolved.session_cookie_name)
    user = get_user_by_session_token(session_token, settings=resolved)
    if user is None:
        return None, RedirectResponse(url="/login", status_code=303)
    if user.role != "admin":
        return user, PlainTextResponse("Forbidden", status_code=403)
    return user, None


def _format_minor_amount(amount_minor: int) -> str:
    amount = Decimal(amount_minor) / Decimal(100)
    return f"{amount:,.2f}".replace(",", " ").replace(".", ",")


def _format_price_input(amount_minor: int) -> str:
    amount = Decimal(amount_minor) / Decimal(100)
    text = format(amount, "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text


def _empty_tariff_form_data() -> dict[str, str]:
    return {
        "code": "",
        "title": "",
        "description": "",
        "price_rub": "",
        "currency": "RUB",
        "status": "active",
        "sort_order": "0",
    }


def _tariff_form_data_from_tariff(tariff) -> dict[str, str]:
    return {
        "code": tariff.code,
        "title": tariff.title,
        "description": tariff.description or "",
        "price_rub": _format_price_input(tariff.price_amount_minor),
        "currency": tariff.currency,
        "status": tariff.status,
        "sort_order": str(tariff.sort_order),
    }


def _tariff_form_data_from_form(form) -> dict[str, str]:
    return {
        "code": _normalize_text(form.get("code")),
        "title": _normalize_text(form.get("title")),
        "description": _normalize_text(form.get("description")),
        "price_rub": _normalize_text(form.get("price_rub")),
        "currency": _normalize_text(form.get("currency")) or "RUB",
        "status": _normalize_text(form.get("status")) or "active",
        "sort_order": _normalize_text(form.get("sort_order")) or "0",
    }


def _parse_positive_money_to_minor(value: str | None) -> tuple[int | None, str | None]:
    raw = (value or "").strip()
    if not raw:
        return None, "price is required"
    raw = raw.replace(",", ".")
    try:
        amount = Decimal(raw)
    except InvalidOperation:
        return None, "price must be a valid ruble amount"
    if not amount.is_finite() or amount < 0:
        return None, "price must be a non-negative amount"
    minor = amount * Decimal(100)
    if minor != minor.to_integral_value():
        return None, "price must have at most 2 decimal places"
    return int(minor), None


def _parse_non_negative_int(value: str | None, field_name: str, default: int = 0) -> tuple[int | None, str | None]:
    raw = (value or "").strip()
    if not raw:
        return default, None
    try:
        parsed = int(raw)
    except ValueError:
        return None, f"{field_name} must be an integer"
    if parsed < 0:
        return None, f"{field_name} must be greater than or equal to 0"
    return parsed, None


def _normalize_text(value: str | None) -> str:
    return (value or "").strip()


def _tariff_form_errors_from_service(exc: Exception) -> dict[str, str]:
    message = str(exc)
    lowered = message.lower()
    if "code already exists" in lowered:
        return {"code": message}
    if "code is required" in lowered or lowered.startswith("code "):
        return {"code": message}
    if lowered.startswith("title "):
        return {"title": message}
    if lowered.startswith("description "):
        return {"description": message}
    if "price_amount_minor" in lowered:
        return {"price_rub": message}
    if lowered.startswith("currency "):
        return {"currency": message}
    if lowered.startswith("status "):
        return {"status": message}
    if lowered.startswith("sort_order "):
        return {"sort_order": message}
    return {"form": message}


def _validate_tariff_form_input(
    *,
    raw_code: str | None = None,
    raw_title: str | None = None,
    raw_description: str | None = None,
    raw_price_rub: str | None = None,
    raw_currency: str | None = None,
    raw_status: str | None = None,
    raw_sort_order: str | None = None,
    include_code: bool = True,
) -> tuple[dict[str, object], dict[str, str]]:
    errors: dict[str, str] = {}
    code = _normalize_text(raw_code).lower()
    title = _normalize_text(raw_title)
    description = _normalize_text(raw_description) or None
    price_minor, price_error = _parse_positive_money_to_minor(raw_price_rub)
    currency = (_normalize_text(raw_currency) or "RUB").upper()
    status = (_normalize_text(raw_status) or "active").lower()
    sort_order, sort_error = _parse_non_negative_int(raw_sort_order, "sort_order")

    if include_code:
        if not code:
            errors["code"] = "code is required"
        elif not TARIFF_CODE_RE.fullmatch(code):
            errors["code"] = "code must be 3-64 chars of lowercase letters, digits, underscore or hyphen"
    if not title:
        errors["title"] = "title is required"
    elif len(title) > 200:
        errors["title"] = "title must be at most 200 characters"
    if description is not None and len(description) > 4000:
        errors["description"] = "description must be at most 4000 characters"
    if price_error:
        errors["price_rub"] = price_error
    if not re.fullmatch(r"^[A-Z]{3}$", currency):
        errors["currency"] = "currency must be a 3-letter uppercase code"
    if status not in ALLOWED_TARIFF_STATUSES:
        errors["status"] = "status must be active, hidden, or archived"
    if sort_error:
        errors["sort_order"] = sort_error

    payload = {
        "code": code,
        "title": title,
        "description": description,
        "price_amount_minor": price_minor,
        "currency": currency,
        "status": status,
        "sort_order": sort_order if sort_order is not None else 0,
    }
    return payload, errors


def _paid_options_for_admin(settings):
    rows = []
    for option in list_paid_options(include_hidden=True, include_archived=True, settings=settings):
        rows.append(
            {
                "code": option.code,
                "title": option.title,
                "description": option.description or "—",
                "price_display": "отдельная цена не задана"
                if option.price_amount_minor is None
                else _format_minor_amount(option.price_amount_minor),
                "currency": option.currency,
                "default_duration_days": "—" if option.default_duration_days is None else option.default_duration_days,
                "status": option.status,
                "is_renewable": option.is_renewable,
                "sort_order": option.sort_order,
                "created_at": option.created_at,
                "updated_at": option.updated_at,
            }
        )
    return rows


def _tariffs_for_admin(settings):
    tariffs = list_tariffs_for_admin(settings=settings)
    rows = []
    for tariff in tariffs:
        linked_options = list_tariff_options(tariff.code, include_hidden=True, include_archived=True, settings=settings)
        rows.append(
            {
                "code": tariff.code,
                "title": tariff.title,
                "description": tariff.description or "—",
                "price_display": _format_minor_amount(tariff.price_amount_minor),
                "currency": tariff.currency,
                "status": tariff.status,
                "sort_order": tariff.sort_order,
                "included_options_summary": ", ".join(option["title"] for option in linked_options) if linked_options else "—",
                "created_at": tariff.created_at,
                "updated_at": tariff.updated_at,
            }
        )
    return rows


def _render_tariff_form(
    request: Request,
    *,
    mode: str,
    form_data: dict[str, str],
    errors: dict[str, str] | None = None,
    tariff=None,
    status_code: int = 200,
):
    is_create = mode == "create"
    return _template(
        request,
        "tariff_form.html",
        status_code=status_code,
        title=page_title("Создать тариф" if is_create else "Редактировать тариф"),
        mode=mode,
        is_create=is_create,
        tariff=tariff,
        form_data=form_data,
        errors=errors or {},
        submit_label="Создать тариф" if is_create else "Сохранить изменения",
    )


@router.api_route("/admin", methods=["GET", "HEAD"], response_class=HTMLResponse)
def admin_dashboard(request: Request):
    settings = get_settings()
    user, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response
    return _template(
        request,
        "dashboard.html",
        title=page_title("Админ-панель"),
        admin_email=user.email,
        admin_login=user.login,
    )


@router.api_route("/admin/users", methods=["GET", "HEAD"], response_class=HTMLResponse)
def admin_users(request: Request):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response
    return _template(
        request,
        "users.html",
        title=page_title("Пользователи"),
        users=list_users_for_admin(settings=settings),
    )


@router.api_route("/admin/tariffs", methods=["GET", "HEAD"], response_class=HTMLResponse)
def admin_tariffs(request: Request):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response
    return _template(
        request,
        "tariffs.html",
        title=page_title("Тарифы"),
        tariffs=_tariffs_for_admin(settings=settings),
    )


@router.api_route("/admin/tariffs/new", methods=["GET", "HEAD"], response_class=HTMLResponse)
def admin_tariffs_new(request: Request):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response
    return _render_tariff_form(request, mode="create", form_data=_empty_tariff_form_data())


@router.post("/admin/tariffs/new", response_class=HTMLResponse)
async def admin_tariffs_new_submit(request: Request):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response

    form = await request.form()
    payload, errors = _validate_tariff_form_input(
        raw_code=form.get("code"),
        raw_title=form.get("title"),
        raw_description=form.get("description"),
        raw_price_rub=form.get("price_rub"),
        raw_currency=form.get("currency"),
        raw_status=form.get("status"),
        raw_sort_order=form.get("sort_order"),
        include_code=True,
    )
    if errors:
        return _render_tariff_form(
            request,
            mode="create",
            form_data=_tariff_form_data_from_form(form),
            errors=errors,
            status_code=400,
        )

    try:
        create_tariff(data=TariffCreateInput(**payload), settings=settings)
    except TariffConflictError as exc:
        errors = _tariff_form_errors_from_service(exc)
        return _render_tariff_form(
            request,
            mode="create",
            form_data=_tariff_form_data_from_form(form),
            errors=errors,
            status_code=400,
        )
    except TariffValidationError as exc:
        errors = _tariff_form_errors_from_service(exc)
        return _render_tariff_form(
            request,
            mode="create",
            form_data=_tariff_form_data_from_form(form),
            errors=errors,
            status_code=400,
        )

    return RedirectResponse(url="/admin/tariffs", status_code=303)


@router.api_route("/admin/tariffs/{code}/edit", methods=["GET", "HEAD"], response_class=HTMLResponse)
def admin_tariffs_edit(request: Request, code: str):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response

    tariff = get_tariff_by_code(code, settings=settings)
    if tariff is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return _render_tariff_form(request, mode="edit", form_data=_tariff_form_data_from_tariff(tariff), tariff=tariff)


@router.post("/admin/tariffs/{code}/edit", response_class=HTMLResponse)
async def admin_tariffs_edit_submit(request: Request, code: str):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response

    tariff = get_tariff_by_code(code, settings=settings)
    if tariff is None:
        raise HTTPException(status_code=404, detail="Not Found")

    form = await request.form()
    payload, errors = _validate_tariff_form_input(
        raw_title=form.get("title"),
        raw_description=form.get("description"),
        raw_price_rub=form.get("price_rub"),
        raw_currency=form.get("currency"),
        raw_status=form.get("status"),
        raw_sort_order=form.get("sort_order"),
        include_code=False,
    )
    posted_code = _normalize_text(form.get("code")).lower()
    if posted_code and posted_code != tariff.code:
        errors["code"] = "code cannot be changed after creation"
    if errors:
        return _render_tariff_form(
            request,
            mode="edit",
            form_data={**_tariff_form_data_from_tariff(tariff), **_tariff_form_data_from_form(form)},
            tariff=tariff,
            errors=errors,
            status_code=400,
        )

    try:
        update_tariff(
            code=tariff.code,
            data=TariffUpdateInput(
                title=payload["title"],
                description=payload["description"],
                price_amount_minor=payload["price_amount_minor"],
                currency=payload["currency"],
                status=payload["status"],
                sort_order=payload["sort_order"],
            ),
            settings=settings,
        )
    except TariffNotFoundError:
        raise HTTPException(status_code=404, detail="Not Found")
    except (TariffConflictError, TariffValidationError) as exc:
        errors = _tariff_form_errors_from_service(exc)
        return _render_tariff_form(
            request,
            mode="edit",
            form_data={**_tariff_form_data_from_tariff(tariff), **_tariff_form_data_from_form(form)},
            tariff=tariff,
            errors=errors,
            status_code=400,
        )

    return RedirectResponse(url="/admin/tariffs", status_code=303)


@router.post("/admin/tariffs/{code}/archive")
def admin_tariffs_archive(request: Request, code: str):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response
    try:
        archive_tariff(code, settings=settings)
    except TariffNotFoundError:
        raise HTTPException(status_code=404, detail="Not Found")
    return RedirectResponse(url="/admin/tariffs", status_code=303)


@router.api_route("/admin/paid-options", methods=["GET", "HEAD"], response_class=HTMLResponse)
def admin_paid_options(request: Request):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response
    return _template(
        request,
        "paid_options.html",
        title=page_title("Платные опции"),
        paid_options=_paid_options_for_admin(settings=settings),
    )
