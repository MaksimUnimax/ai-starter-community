"""Admin dashboard routes."""

from __future__ import annotations

import re
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates

from app.auth.service import (
    ADMIN_USER_DEFAULT_SORT,
    ALLOWED_ADMIN_USER_ACCESS_STATUSES,
    ALLOWED_ROLES,
    ROLE_LABELS_RU,
    NotFoundError as AuthNotFoundError,
    RoleError,
    get_user_by_session_token,
    list_users_for_admin,
    update_user_role,
)
from app.admin.course_export import build_course_export
from app.core.config import get_settings
from app.paid_options.schemas import PaidOptionCreateInput, PaidOptionUpdateInput
from app.paid_options.service import (
    ConflictError as PaidOptionConflictError,
    NotFoundError as PaidOptionNotFoundError,
    ValidationError as PaidOptionValidationError,
    archive_paid_option,
    create_paid_option,
    get_paid_option_by_code,
    list_paid_options,
    list_paid_options_for_admin,
    update_paid_option,
)
from app.shared.utils import page_title
from app.tariffs.schemas import TariffCreateInput, TariffUpdateInput
from app.tariffs.service import (
    ConflictError as TariffConflictError,
    NotFoundError as TariffNotFoundError,
    ValidationError as TariffValidationError,
    attach_option_to_tariff,
    archive_tariff,
    detach_option_from_tariff,
    create_tariff,
    get_tariff_by_code,
    list_tariff_options,
    list_tariffs_for_admin,
    update_tariff_option_link,
    update_tariff,
)

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))

TARIFF_CODE_RE = re.compile(r"^[a-z0-9_-]{3,64}$")
ALLOWED_TARIFF_STATUSES = {"active", "hidden", "archived"}
ADMIN_USER_SORT_OPTIONS = {"desc": "Сначала новые", "asc": "Сначала старые"}


def _admin_user_filter_error(message: str) -> PlainTextResponse:
    lowered = message.lower()
    if "role" in lowered and "unsupported" in lowered:
        text = "Выберите допустимую роль."
    elif "access status" in lowered or "status" in lowered:
        text = "Выберите допустимый статус доступа."
    elif "created sort" in lowered:
        text = "Выберите допустимый порядок сортировки."
    elif "date" in lowered:
        text = "Укажите корректную дату регистрации."
    else:
        text = "Не удалось применить фильтр."
    return PlainTextResponse(text, status_code=400)


def _parse_admin_user_date(value: str | None) -> date | None:
    raw = (value or "").strip()
    if not raw:
        return None
    return date.fromisoformat(raw)


def _parse_admin_user_filters(request: Request) -> tuple[dict[str, object], str | None]:
    query = request.query_params
    raw_role = (query.get("role") or "all").strip().lower()
    if raw_role in {"", "all"}:
        role = None
        role_value = "all"
    elif raw_role in ALLOWED_ROLES:
        role = raw_role
        role_value = raw_role
    else:
        return {}, "unsupported role"

    raw_access_status = (query.get("access_status") or "all").strip().lower()
    if raw_access_status in {"", "all"}:
        access_status = None
        access_status_value = "all"
    elif raw_access_status in ALLOWED_ADMIN_USER_ACCESS_STATUSES:
        access_status = raw_access_status
        access_status_value = raw_access_status
    else:
        return {}, "unsupported access status"

    raw_created_sort = (query.get("created_sort") or ADMIN_USER_DEFAULT_SORT).strip().lower() or ADMIN_USER_DEFAULT_SORT
    if raw_created_sort not in ADMIN_USER_SORT_OPTIONS:
        return {}, "unsupported created sort"

    try:
        created_from = _parse_admin_user_date(query.get("created_from"))
        created_to = _parse_admin_user_date(query.get("created_to"))
    except ValueError:
        return {}, "invalid date"

    return {
        "role": role,
        "access_status": access_status,
        "created_from": created_from,
        "created_to": created_to,
        "created_sort": raw_created_sort,
        "filter_role": role_value,
        "filter_access_status": access_status_value,
        "created_from_value": (query.get("created_from") or "").strip(),
        "created_to_value": (query.get("created_to") or "").strip(),
        "query_string": request.url.query,
    }, None


def _status_label(value: str) -> str:
    return {
        "active": "активен",
        "hidden": "скрыт",
        "archived": "архив",
    }.get(value, value)


def _role_error_response(message: str) -> PlainTextResponse:
    lowered = message.lower()
    if "last admin" in lowered:
        text = "Нельзя изменить роль последнего администратора."
    elif "unsupported role" in lowered:
        text = "Выберите допустимую роль."
    else:
        text = "Не удалось изменить роль пользователя."
    return PlainTextResponse(text, status_code=400)


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
        return user, PlainTextResponse("Доступ запрещён\nУ вашей учётной записи нет прав администратора.", status_code=403)
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


def _parse_optional_non_negative_int(value: str | None, field_name: str) -> tuple[int | None, str | None]:
    raw = (value or "").strip()
    if not raw:
        return None, None
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
        return {"code": "Тариф с таким кодом уже существует."}
    if "code is required" in lowered or lowered.startswith("code "):
        return {"code": "Укажите системный код тарифа."}
    if lowered.startswith("title "):
        return {"title": "Укажите название тарифа."}
    if lowered.startswith("description "):
        return {"description": "Описание тарифа слишком длинное."}
    if "price_amount_minor" in lowered:
        if "at most 2 decimal places" in lowered:
            return {"price_rub": "Цена может содержать не более 2 знаков после запятой."}
        if "non-negative" in lowered:
            return {"price_rub": "Цена не может быть отрицательной."}
        return {"price_rub": "Введите корректную цену в рублях."}
    if lowered.startswith("currency "):
        return {"currency": "Валюта должна быть кодом из 3 заглавных букв."}
    if lowered.startswith("status "):
        return {"status": "Статус должен быть активен, скрыт или архив."}
    if lowered.startswith("sort_order "):
        return {"sort_order": "Порядок сортировки должен быть целым числом не меньше 0."}
    return {"form": "Не удалось сохранить тариф."}


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
        if code and not TARIFF_CODE_RE.fullmatch(code):
            errors["code"] = "Системный код тарифа должен содержать 3-64 символа: строчные латинские буквы, цифры, подчёркивание или дефис."
        elif code is None or code == "":
            code = None
    elif code == "":
        code = None
    if not title:
        errors["title"] = "Укажите название тарифа."
    elif len(title) > 200:
        errors["title"] = "Название тарифа должно быть не длиннее 200 символов."
    if description is not None and len(description) > 4000:
        errors["description"] = "Описание тарифа должно быть не длиннее 4000 символов."
    if price_error:
        if price_error == "price is required":
            errors["price_rub"] = "Укажите цену тарифа."
        elif price_error == "price must be a valid ruble amount":
            errors["price_rub"] = "Введите корректную цену в рублях."
        elif price_error == "price must be a non-negative amount":
            errors["price_rub"] = "Цена не может быть отрицательной."
        else:
            errors["price_rub"] = "Цена может содержать не более 2 знаков после запятой."
    if not re.fullmatch(r"^[A-Z]{3}$", currency):
        errors["currency"] = "Валюта должна быть кодом из 3 заглавных букв."
    if status not in ALLOWED_TARIFF_STATUSES:
        errors["status"] = "Статус должен быть активен, скрыт или архив."
    if sort_error:
        errors["sort_order"] = "Порядок сортировки должен быть целым числом не меньше 0."

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
    for option in list_paid_options_for_admin(settings=settings):
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
                "status_label": _status_label(option.status),
                "is_renewable": option.is_renewable,
                "sort_order": option.sort_order,
                "created_at": option.created_at,
                "updated_at": option.updated_at,
            }
        )
    return rows


def _empty_tariff_option_attach_form_data() -> dict[str, str]:
    return {
        "option_code": "",
        "included_duration_days": "",
        "included_quantity": "",
    }


def _tariff_option_form_value(value) -> str:
    if value is None:
        return ""
    return str(value)


def _tariff_option_link_rows(settings, tariff_code: str, *, link_overrides: dict[str, dict[str, str]] | None = None) -> list[dict[str, object]]:
    linked_rows = list_tariff_options(tariff_code, include_hidden=True, include_archived=True, settings=settings)
    rows: list[dict[str, object]] = []
    for link in linked_rows:
        code = str(link["code"])
        override = (link_overrides or {}).get(code, {})
        rows.append(
            {
                "code": code,
                "title": str(link["title"]),
                "status_label": _status_label(str(link["status"])),
                "included_duration_days": _tariff_option_form_value(override.get("included_duration_days", link["included_duration_days"])),
                "included_quantity": _tariff_option_form_value(override.get("included_quantity", link["included_quantity"])),
            }
        )
    return rows


def _tariff_options_page_context(
    settings,
    tariff,
    *,
    attach_form_data: dict[str, str] | None = None,
    errors: dict[str, str] | None = None,
    link_overrides: dict[str, dict[str, str]] | None = None,
) -> dict[str, object]:
    linked_options = _tariff_option_link_rows(settings, tariff.code, link_overrides=link_overrides)
    linked_codes = {option["code"] for option in linked_options}
    available_paid_options = [
        {
            "code": option.code,
            "title": option.title,
            "status_label": _status_label(option.status),
        }
        for option in list_paid_options(settings=settings)
        if option.code not in linked_codes
    ]
    return {
        "tariff": tariff,
        "linked_options": linked_options,
        "available_paid_options": available_paid_options,
        "attach_form_data": attach_form_data or _empty_tariff_option_attach_form_data(),
        "errors": errors or {},
    }


def _render_tariff_options_page(
    request: Request,
    settings,
    tariff,
    *,
    attach_form_data: dict[str, str] | None = None,
    errors: dict[str, str] | None = None,
    link_overrides: dict[str, dict[str, str]] | None = None,
    status_code: int = 200,
):
    return _template(
        request,
        "tariff_options.html",
        status_code=status_code,
        title=page_title(f"Опции тарифа: {tariff.title}"),
        **_tariff_options_page_context(
            settings,
            tariff,
            attach_form_data=attach_form_data,
            errors=errors,
            link_overrides=link_overrides,
        ),
    )


def _empty_paid_option_form_data() -> dict[str, object]:
    return {
        "code": "",
        "title": "",
        "description": "",
        "price_rub": "",
        "currency": "RUB",
        "default_duration_days": "",
        "status": "active",
        "is_renewable": True,
        "sort_order": "0",
    }


def _paid_option_form_data_from_option(option) -> dict[str, object]:
    return {
        "code": option.code,
        "title": option.title,
        "description": option.description or "",
        "price_rub": "" if option.price_amount_minor is None else _format_price_input(option.price_amount_minor),
        "currency": option.currency,
        "default_duration_days": "" if option.default_duration_days is None else str(option.default_duration_days),
        "status": option.status,
        "is_renewable": bool(option.is_renewable),
        "sort_order": str(option.sort_order),
    }


def _paid_option_form_data_from_form(form) -> dict[str, object]:
    return {
        "code": _normalize_text(form.get("code")),
        "title": _normalize_text(form.get("title")),
        "description": _normalize_text(form.get("description")),
        "price_rub": _normalize_text(form.get("price_rub")),
        "currency": _normalize_text(form.get("currency")) or "RUB",
        "default_duration_days": _normalize_text(form.get("default_duration_days")),
        "status": _normalize_text(form.get("status")) or "active",
        "is_renewable": _checkbox_is_true(form.get("is_renewable")),
        "sort_order": _normalize_text(form.get("sort_order")) or "0",
    }


def _checkbox_is_true(value) -> bool:
    if value is None:
        return False
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return value != 0
    raw = str(value).strip().lower()
    return raw not in {"", "0", "false", "off", "no"}


def _parse_optional_money_to_minor(value: str | None) -> tuple[int | None, str | None]:
    raw = (value or "").strip()
    if not raw:
        return None, None
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


def _paid_option_form_errors_from_service(exc: Exception) -> dict[str, str]:
    message = str(exc)
    lowered = message.lower()
    if "code already exists" in lowered:
        return {"code": "Платная опция с таким кодом уже существует."}
    if "code is required" in lowered or lowered.startswith("code "):
        return {"code": "Укажите системный код платной опции."}
    if lowered.startswith("title "):
        return {"title": "Укажите название платной опции."}
    if lowered.startswith("description "):
        return {"description": "Описание платной опции слишком длинное."}
    if "price_amount_minor" in lowered:
        if "at most 2 decimal places" in lowered:
            return {"price_rub": "Цена может содержать не более 2 знаков после запятой."}
        if "non-negative" in lowered:
            return {"price_rub": "Цена не может быть отрицательной."}
        return {"price_rub": "Введите корректную цену в рублях."}
    if lowered.startswith("currency "):
        return {"currency": "Валюта должна быть кодом из 3 заглавных букв."}
    if lowered.startswith("default_duration_days "):
        return {"default_duration_days": "Срок по умолчанию должен быть целым числом не меньше 0."}
    if lowered.startswith("status "):
        return {"status": "Статус должен быть активен, скрыт или архив."}
    if lowered.startswith("is_renewable "):
        return {"is_renewable": "Значение поля «Можно продлевать» некорректно."}
    if lowered.startswith("sort_order "):
        return {"sort_order": "Порядок сортировки должен быть целым числом не меньше 0."}
    return {"form": "Не удалось сохранить платную опцию."}


def _validate_paid_option_form_input(
    *,
    raw_code: str | None = None,
    raw_title: str | None = None,
    raw_description: str | None = None,
    raw_price_rub: str | None = None,
    raw_currency: str | None = None,
    raw_default_duration_days: str | None = None,
    raw_status: str | None = None,
    raw_is_renewable=None,
    raw_sort_order: str | None = None,
    include_code: bool = True,
) -> tuple[dict[str, object], dict[str, str]]:
    errors: dict[str, str] = {}
    code = _normalize_text(raw_code).lower()
    title = _normalize_text(raw_title)
    description = _normalize_text(raw_description) or None
    price_minor, price_error = _parse_optional_money_to_minor(raw_price_rub)
    currency = (_normalize_text(raw_currency) or "RUB").upper()
    default_duration_days, duration_error = _parse_optional_non_negative_int(raw_default_duration_days, "default_duration_days")
    status = (_normalize_text(raw_status) or "active").lower()
    is_renewable = _checkbox_is_true(raw_is_renewable)
    sort_order, sort_error = _parse_non_negative_int(raw_sort_order, "sort_order")

    if include_code:
        if code and not TARIFF_CODE_RE.fullmatch(code):
            errors["code"] = "Системный код платной опции должен содержать 3-64 символа: строчные латинские буквы, цифры, подчёркивание или дефис."
        elif code == "":
            code = None
    elif code == "":
        code = None
    if not title:
        errors["title"] = "Укажите название платной опции."
    elif len(title) > 200:
        errors["title"] = "Название платной опции должно быть не длиннее 200 символов."
    if description is not None and len(description) > 4000:
        errors["description"] = "Описание платной опции должно быть не длиннее 4000 символов."
    if price_error:
        if price_error == "price must be a valid ruble amount":
            errors["price_rub"] = "Введите корректную цену в рублях."
        elif price_error == "price must be a non-negative amount":
            errors["price_rub"] = "Цена не может быть отрицательной."
        else:
            errors["price_rub"] = "Цена может содержать не более 2 знаков после запятой."
    if not re.fullmatch(r"^[A-Z]{3}$", currency):
        errors["currency"] = "Валюта должна быть кодом из 3 заглавных букв."
    if duration_error:
        errors["default_duration_days"] = "Срок по умолчанию должен быть целым числом не меньше 0."
    if status not in ALLOWED_TARIFF_STATUSES:
        errors["status"] = "Статус должен быть активен, скрыт или архив."
    if sort_error:
        errors["sort_order"] = "Порядок сортировки должен быть целым числом не меньше 0."

    payload = {
        "code": code,
        "title": title,
        "description": description,
        "price_amount_minor": price_minor,
        "currency": currency,
        "default_duration_days": default_duration_days,
        "status": status,
        "is_renewable": is_renewable,
        "sort_order": sort_order if sort_order is not None else 0,
    }
    return payload, errors


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
                "status_label": _status_label(tariff.status),
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


def _validate_tariff_option_link_form_input(
    *,
    raw_option_code: str | None = None,
    raw_included_duration_days: str | None = None,
    raw_included_quantity: str | None = None,
    include_option_code: bool = True,
) -> tuple[dict[str, str], dict[str, str]]:
    errors: dict[str, str] = {}
    option_code = _normalize_text(raw_option_code).lower()
    duration_days, duration_error = _parse_optional_non_negative_int(raw_included_duration_days, "included_duration_days")
    quantity, quantity_error = _parse_optional_non_negative_int(raw_included_quantity, "included_quantity")

    if include_option_code:
        if not option_code:
            errors["option_code"] = "Выберите платную опцию."
        elif not TARIFF_CODE_RE.fullmatch(option_code):
            errors["option_code"] = "Системный код платной опции должен содержать 3-64 символа: строчные латинские буквы, цифры, подчёркивание или дефис."
    if duration_error:
        errors["included_duration_days"] = "Включённый срок должен быть целым числом не меньше 0."
    if quantity_error:
        errors["included_quantity"] = "Включённое количество должно быть целым числом не меньше 0."

    payload = {
        "option_code": option_code,
        "included_duration_days": "" if duration_days is None else str(duration_days),
        "included_quantity": "" if quantity is None else str(quantity),
    }
    return payload, errors


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


@router.get("/admin/course-export")
def admin_course_export(request: Request):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response

    export = build_course_export()
    headers = {
        "Content-Disposition": f'attachment; filename="{export.filename}"',
    }
    return Response(content=export.content, media_type="application/zip", headers=headers)


@router.api_route("/admin/users", methods=["GET", "HEAD"], response_class=HTMLResponse)
def admin_users(request: Request):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response
    filters, error = _parse_admin_user_filters(request)
    if error is not None:
        return _admin_user_filter_error(error)
    return _template(
        request,
        "users.html",
        title=page_title("Пользователи"),
        users=list_users_for_admin(
            settings=settings,
            role=filters["role"],
            access_status=filters["access_status"],
            created_from=filters["created_from"],
            created_to=filters["created_to"],
            created_sort=filters["created_sort"],
        ),
        allowed_roles=ALLOWED_ROLES,
        role_labels=ROLE_LABELS_RU,
        filter_role=filters["filter_role"],
        filter_access_status=filters["filter_access_status"],
        created_from_value=filters["created_from_value"],
        created_to_value=filters["created_to_value"],
        created_sort=filters["created_sort"],
        query_string=filters["query_string"],
    )


@router.post("/admin/users/{user_id}/role")
async def admin_user_role_update(request: Request, user_id: int):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response
    form = await request.form()
    role = _normalize_text(form.get("role"))
    try:
        update_user_role(user_id=user_id, new_role=role, settings=settings)
    except AuthNotFoundError:
        raise HTTPException(status_code=404, detail="user not found")
    except RoleError as exc:
        return _role_error_response(str(exc))
    redirect_url = "/admin/users"
    if request.url.query:
        redirect_url = f"{redirect_url}?{request.url.query}"
    return RedirectResponse(url=redirect_url, status_code=303)


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
        errors["code"] = "Системный код нельзя изменить после создания."
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


def _tariff_option_link_errors_from_service(exc: Exception) -> dict[str, str]:
    message = str(exc)
    lowered = message.lower()
    if "archived paid option" in lowered:
        return {"option_code": "Архивные опции нельзя добавлять к тарифу."}
    if "paid option" in lowered or "option" in lowered:
        return {"option_code": "Платная опция не найдена или недоступна для добавления."}
    if "included_duration_days" in lowered:
        return {"included_duration_days": "Включённый срок должен быть целым числом не меньше 0."}
    if "included_quantity" in lowered:
        return {"included_quantity": "Включённое количество должно быть целым числом не меньше 0."}
    return {"form": "Не удалось изменить связь тарифа и опции."}


@router.api_route("/admin/tariffs/{code}/options", methods=["GET", "HEAD"], response_class=HTMLResponse)
def admin_tariff_options(request: Request, code: str):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response

    tariff = get_tariff_by_code(code, settings=settings)
    if tariff is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return _render_tariff_options_page(request, settings, tariff)


@router.post("/admin/tariffs/{code}/options/attach", response_class=HTMLResponse)
async def admin_tariff_options_attach(request: Request, code: str):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response

    tariff = get_tariff_by_code(code, settings=settings)
    if tariff is None:
        raise HTTPException(status_code=404, detail="Not Found")

    form = await request.form()
    payload, errors = _validate_tariff_option_link_form_input(
        raw_option_code=form.get("option_code"),
        raw_included_duration_days=form.get("included_duration_days"),
        raw_included_quantity=form.get("included_quantity"),
        include_option_code=True,
    )
    if errors:
        return _render_tariff_options_page(
            request,
            settings,
            tariff,
            attach_form_data=payload,
            errors=errors,
            status_code=400,
        )

    try:
        attach_option_to_tariff(
            code,
            payload["option_code"],
            included_duration_days=None if payload["included_duration_days"] == "" else int(payload["included_duration_days"]),
            included_quantity=None if payload["included_quantity"] == "" else int(payload["included_quantity"]),
            settings=settings,
        )
    except TariffNotFoundError:
        raise HTTPException(status_code=404, detail="Not Found")
    except TariffValidationError as exc:
        errors = _tariff_option_link_errors_from_service(exc)
        return _render_tariff_options_page(
            request,
            settings,
            tariff,
            attach_form_data=payload,
            errors=errors,
            status_code=400,
        )

    return RedirectResponse(url=f"/admin/tariffs/{tariff.code}/options", status_code=303)


@router.post("/admin/tariffs/{code}/options/{option_code}/update", response_class=HTMLResponse)
async def admin_tariff_options_update(request: Request, code: str, option_code: str):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response

    tariff = get_tariff_by_code(code, settings=settings)
    if tariff is None:
        raise HTTPException(status_code=404, detail="Not Found")

    form = await request.form()
    payload, errors = _validate_tariff_option_link_form_input(
        raw_included_duration_days=form.get("included_duration_days"),
        raw_included_quantity=form.get("included_quantity"),
        include_option_code=False,
    )
    if errors:
        return _render_tariff_options_page(
            request,
            settings,
            tariff,
            errors=errors,
            link_overrides={
                option_code: {
                    "included_duration_days": payload["included_duration_days"],
                    "included_quantity": payload["included_quantity"],
                }
            },
            status_code=400,
        )

    try:
        update_tariff_option_link(
            code,
            option_code,
            included_duration_days=None if payload["included_duration_days"] == "" else int(payload["included_duration_days"]),
            included_quantity=None if payload["included_quantity"] == "" else int(payload["included_quantity"]),
            settings=settings,
        )
    except TariffNotFoundError:
        raise HTTPException(status_code=404, detail="Not Found")
    except TariffValidationError as exc:
        errors = _tariff_option_link_errors_from_service(exc)
        return _render_tariff_options_page(
            request,
            settings,
            tariff,
            errors=errors,
            link_overrides={
                option_code: {
                    "included_duration_days": payload["included_duration_days"],
                    "included_quantity": payload["included_quantity"],
                }
            },
            status_code=400,
        )

    return RedirectResponse(url=f"/admin/tariffs/{tariff.code}/options", status_code=303)


@router.post("/admin/tariffs/{code}/options/{option_code}/detach")
def admin_tariff_options_detach(request: Request, code: str, option_code: str):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response

    tariff = get_tariff_by_code(code, settings=settings)
    if tariff is None:
        raise HTTPException(status_code=404, detail="Not Found")

    try:
        detached = detach_option_from_tariff(code, option_code, settings=settings)
    except TariffNotFoundError:
        raise HTTPException(status_code=404, detail="Not Found")
    if not detached:
        raise HTTPException(status_code=404, detail="Not Found")

    return RedirectResponse(url=f"/admin/tariffs/{tariff.code}/options", status_code=303)


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


@router.api_route("/admin/paid-options/new", methods=["GET", "HEAD"], response_class=HTMLResponse)
def admin_paid_options_new(request: Request):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response
    return _template(
        request,
        "paid_option_form.html",
        title=page_title("Создать платную опцию"),
        mode="create",
        is_create=True,
        option=None,
        form_data=_empty_paid_option_form_data(),
        errors={},
        submit_label="Создать платную опцию",
    )


@router.post("/admin/paid-options/new", response_class=HTMLResponse)
async def admin_paid_options_new_submit(request: Request):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response

    form = await request.form()
    payload, errors = _validate_paid_option_form_input(
        raw_code=form.get("code"),
        raw_title=form.get("title"),
        raw_description=form.get("description"),
        raw_price_rub=form.get("price_rub"),
        raw_currency=form.get("currency"),
        raw_default_duration_days=form.get("default_duration_days"),
        raw_status=form.get("status"),
        raw_is_renewable=form.get("is_renewable"),
        raw_sort_order=form.get("sort_order"),
        include_code=True,
    )
    if errors:
        return _template(
            request,
            "paid_option_form.html",
            status_code=400,
            title=page_title("Создать платную опцию"),
            mode="create",
            is_create=True,
            option=None,
            form_data=_paid_option_form_data_from_form(form),
            errors=errors,
            submit_label="Создать платную опцию",
        )

    try:
        create_paid_option(data=PaidOptionCreateInput(**payload), settings=settings)
    except PaidOptionConflictError as exc:
        errors = _paid_option_form_errors_from_service(exc)
        return _template(
            request,
            "paid_option_form.html",
            status_code=400,
            title=page_title("Создать платную опцию"),
            mode="create",
            is_create=True,
            option=None,
            form_data=_paid_option_form_data_from_form(form),
            errors=errors,
            submit_label="Создать платную опцию",
        )
    except PaidOptionValidationError as exc:
        errors = _paid_option_form_errors_from_service(exc)
        return _template(
            request,
            "paid_option_form.html",
            status_code=400,
            title=page_title("Создать платную опцию"),
            mode="create",
            is_create=True,
            option=None,
            form_data=_paid_option_form_data_from_form(form),
            errors=errors,
            submit_label="Создать платную опцию",
        )

    return RedirectResponse(url="/admin/paid-options", status_code=303)


@router.api_route("/admin/paid-options/{code}/edit", methods=["GET", "HEAD"], response_class=HTMLResponse)
def admin_paid_options_edit(request: Request, code: str):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response

    option = get_paid_option_by_code(code, settings=settings)
    if option is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return _template(
        request,
        "paid_option_form.html",
        title=page_title("Редактировать платную опцию"),
        mode="edit",
        is_create=False,
        option=option,
        form_data=_paid_option_form_data_from_option(option),
        errors={},
        submit_label="Сохранить изменения",
    )


@router.post("/admin/paid-options/{code}/edit", response_class=HTMLResponse)
async def admin_paid_options_edit_submit(request: Request, code: str):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response

    option = get_paid_option_by_code(code, settings=settings)
    if option is None:
        raise HTTPException(status_code=404, detail="Not Found")

    form = await request.form()
    payload, errors = _validate_paid_option_form_input(
        raw_title=form.get("title"),
        raw_description=form.get("description"),
        raw_price_rub=form.get("price_rub"),
        raw_currency=form.get("currency"),
        raw_default_duration_days=form.get("default_duration_days"),
        raw_status=form.get("status"),
        raw_is_renewable=form.get("is_renewable"),
        raw_sort_order=form.get("sort_order"),
        include_code=False,
    )
    posted_code = _normalize_text(form.get("code")).lower()
    if posted_code and posted_code != option.code:
        errors["code"] = "Системный код нельзя изменить после создания."
    if errors:
        return _template(
            request,
            "paid_option_form.html",
            status_code=400,
            title=page_title("Редактировать платную опцию"),
            mode="edit",
            is_create=False,
            option=option,
            form_data={**_paid_option_form_data_from_option(option), **_paid_option_form_data_from_form(form)},
            errors=errors,
            submit_label="Сохранить изменения",
        )

    try:
        update_paid_option(
            code=option.code,
            data=PaidOptionUpdateInput(
                title=payload["title"],
                description=payload["description"],
                price_amount_minor=payload["price_amount_minor"],
                currency=payload["currency"],
                default_duration_days=payload["default_duration_days"],
                status=payload["status"],
                is_renewable=payload["is_renewable"],
                sort_order=payload["sort_order"],
            ),
            settings=settings,
        )
    except PaidOptionNotFoundError:
        raise HTTPException(status_code=404, detail="Not Found")
    except (PaidOptionConflictError, PaidOptionValidationError) as exc:
        errors = _paid_option_form_errors_from_service(exc)
        return _template(
            request,
            "paid_option_form.html",
            status_code=400,
            title=page_title("Редактировать платную опцию"),
            mode="edit",
            is_create=False,
            option=option,
            form_data={**_paid_option_form_data_from_option(option), **_paid_option_form_data_from_form(form)},
            errors=errors,
            submit_label="Сохранить изменения",
        )

    return RedirectResponse(url="/admin/paid-options", status_code=303)


@router.post("/admin/paid-options/{code}/archive")
def admin_paid_options_archive(request: Request, code: str):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response
    try:
        archive_paid_option(code, settings=settings)
    except PaidOptionNotFoundError:
        raise HTTPException(status_code=404, detail="Not Found")
    return RedirectResponse(url="/admin/paid-options", status_code=303)
