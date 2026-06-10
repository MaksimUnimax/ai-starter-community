"""Admin dashboard routes."""

from __future__ import annotations

import re
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path
from urllib.parse import urlencode

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates

from app.auth.service import (
    ADMIN_USER_DEFAULT_SORT,
    ALLOWED_ADMIN_USER_ACCESS_STATUSES,
    ALLOWED_ROLES,
    ROLE_LABELS_RU,
    NotFoundError as AuthNotFoundError,
    RoleError,
    ValidationError as AuthValidationError,
    get_user_by_email,
    get_user_by_session_token,
    list_users_for_admin,
    role_label_ru,
    set_user_materials_access,
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
from app.account_blocks.schemas import AccountBlockCreateInput, AccountBlockUpdateInput
from app.account_blocks.service import (
    DEFAULT_ACCOUNT_BLOCK_DURATION_DAYS,
    AccountBlockNotFoundError,
    AccountBlockPermissionError,
    AccountBlockValidationError,
    activate_account_block,
    create_account_block,
    delete_account_block,
    get_account_block_copy_data,
    get_account_block_public,
    list_account_blocks_for_viewer,
    renew_account_block,
    update_account_block,
)
from app.notifications.email_service import send_account_block_activation_email
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


ACCOUNT_BLOCK_MANAGEMENT_QUERY_PARAM = "account_blocks_user_email"
ACCOUNT_BLOCK_CREATE_DEFAULT_DURATION_DAYS = 30
ACCOUNT_BLOCK_NOTICE_MESSAGES = {
    "created": "Блок создан.",
    "updated": "Блок сохранён.",
    "deleted": "Блок удалён.",
    "activated": "Блок активирован.",
    "renewed": "Активация продлена.",
    "activated_email_sent": "Блок активирован. Уведомление отправлено на почту пользователя.",
    "activated_email_failed": "Блок активирован, но письмо отправить не удалось.",
    "selected_user_not_found": "Пользователь не найден.",
}


def _account_block_notice(request: Request) -> str | None:
    notice_key = (request.query_params.get("account_blocks_notice") or "").strip().lower()
    return ACCOUNT_BLOCK_NOTICE_MESSAGES.get(notice_key)


def _selected_account_block_email(request: Request, fallback_email: str) -> str:
    raw_email = (request.query_params.get(ACCOUNT_BLOCK_MANAGEMENT_QUERY_PARAM) or "").strip()
    return raw_email or fallback_email


def _user_attr(user, key: str):
    if isinstance(user, dict):
        return user.get(key)
    return getattr(user, key)


def _account_block_owner_email(settings, owner_user_id: int) -> str | None:
    for owner in list_users_for_admin(settings=settings):
        if int(_user_attr(owner, "id")) == int(owner_user_id):
            return str(_user_attr(owner, "email"))
    return None


def _account_block_owner_summary(user) -> dict[str, object]:
    return {
        "id": int(_user_attr(user, "id")),
        "email": str(_user_attr(user, "email")),
        "login": str(_user_attr(user, "login")),
        "role": str(_user_attr(user, "role")),
        "role_label": _user_attr(user, "role_label") if isinstance(user, dict) else role_label_ru(user.role),
        "display_label": f"{_user_attr(user, 'login')} · {_user_attr(user, 'email')}",
    }


def _account_block_card_context(block, copy_data, owner_summary: dict[str, object] | None = None) -> dict[str, object]:
    return {
        "id": block.id,
        "owner_user_id": block.owner_user_id,
        "owner": owner_summary,
        "type": block.type,
        "type_label": {
            "chatgpt": "ChatGPT",
            "server": "Сервер",
            "mail": "Почта",
        }.get(block.type, block.type),
        "title": block.title,
        "login": copy_data.login,
        "password_secret": copy_data.password_secret,
        "status": block.status,
        "status_label": {
            "active": "Активно",
            "inactive": "Неактивно",
            "expired": "Истекло",
        }.get(block.status, block.status),
        "duration_days": block.duration_days,
        "activation_day": block.activation_day,
        "activation_summary": block.activation_summary,
        "is_active": block.is_active,
        "is_expired": block.is_expired,
    }


def _resolve_account_block_selected_user(user, settings, request: Request):
    selected_email = _selected_account_block_email(request, user.email)
    notice = _account_block_notice(request)
    if selected_email == user.email:
        return user, selected_email, notice
    try:
        selected_user = get_user_by_email(selected_email, settings=settings)
    except AuthValidationError:
        return None, selected_email, "Пользователь не найден."
    if selected_user is None:
        return None, selected_email, "Пользователь не найден."
    return selected_user, selected_email, notice


def _parse_account_block_duration(value: str | None, *, default: int = DEFAULT_ACCOUNT_BLOCK_DURATION_DAYS) -> int:
    raw = (value or "").strip()
    if not raw:
        return default
    try:
        parsed = int(raw)
    except ValueError as exc:
        raise AccountBlockValidationError("duration_days must be an integer") from exc
    if parsed <= 0:
        raise AccountBlockValidationError("duration_days must be greater than 0")
    return parsed


def _parse_optional_account_block_duration(value: str | None) -> int | None:
    raw = (value or "").strip()
    if not raw:
        return None
    try:
        parsed = int(raw)
    except ValueError as exc:
        raise AccountBlockValidationError("duration_days must be an integer") from exc
    if parsed <= 0:
        raise AccountBlockValidationError("duration_days must be greater than 0")
    return parsed


def _resolve_create_duration_days(form) -> int:
    return _parse_account_block_duration(
        form.get("duration_days"),
        default=ACCOUNT_BLOCK_CREATE_DEFAULT_DURATION_DAYS,
    )


def _admin_account_block_query_string(selected_email: str | None) -> str:
    if not selected_email:
        return ""
    return f"?{urlencode({ACCOUNT_BLOCK_MANAGEMENT_QUERY_PARAM: selected_email})}"


def _admin_account_block_page_context(user, settings, request: Request) -> dict[str, object]:
    selected_user, selected_email, notice = _resolve_account_block_selected_user(user, settings, request)
    selected_summary = _account_block_owner_summary(selected_user) if selected_user is not None else None
    blocks = []
    if selected_user is not None:
        blocks = [
            _account_block_card_context(
                block,
                get_account_block_copy_data(actor=user, block_id=block.id, settings=settings),
                selected_summary,
            )
            for block in list_account_blocks_for_viewer(user, owner_user_id=int(selected_user.id), settings=settings)
        ]
    return {
        "account_blocks_manage_mode": True,
        "account_block_notice": notice,
        "account_block_selected_user": selected_user,
        "account_block_selected_user_email": selected_email,
        "account_block_selected_user_summary": selected_summary,
        "account_block_owner_options": [
            {
                "email": _user_attr(owner, "email"),
                "login": _user_attr(owner, "login"),
                "role": _user_attr(owner, "role"),
                "role_label": role_label_ru(_user_attr(owner, "role")),
                "display_label": f"{_user_attr(owner, 'login')} · {_user_attr(owner, 'email')}",
            }
            for owner in list_users_for_admin(settings=settings)
        ],
        "account_block_blocks": blocks,
        "account_block_query_string": _admin_account_block_query_string(selected_email),
        "account_block_create_default_duration_days": ACCOUNT_BLOCK_CREATE_DEFAULT_DURATION_DAYS,
        "account_block_type_options": [
            {"value": "chatgpt", "label": "ChatGPT"},
            {"value": "server", "label": "Сервер"},
            {"value": "mail", "label": "Почта"},
        ],
    }


def _admin_account_block_redirect(*, notice_key: str, selected_user_email: str | None = None) -> RedirectResponse:
    query = {"account_blocks_notice": notice_key}
    if selected_user_email:
        query[ACCOUNT_BLOCK_MANAGEMENT_QUERY_PARAM] = selected_user_email
    return RedirectResponse(url=f"/admin/account-blocks?{urlencode(query)}", status_code=303)


def _selected_email_for_block(request: Request, settings, fallback_email: str, owner_user_id: int) -> str:
    selected_email = _selected_account_block_email(request, fallback_email)
    if selected_email != fallback_email:
        return selected_email
    owner_email = _account_block_owner_email(settings, owner_user_id)
    return owner_email or fallback_email


def _role_error_response(message: str) -> PlainTextResponse:
    lowered = message.lower()
    if "admin role cannot be changed" in lowered:
        text = "Нельзя изменить роль администратора."
    elif "unsupported moderator role" in lowered:
        text = "Можно только назначать или убирать модератора."
    elif "unsupported role" in lowered:
        text = "Выберите допустимую роль."
    else:
        text = "Не удалось изменить роль пользователя."
    return PlainTextResponse(text, status_code=400)


def _admin_users_redirect(request: Request) -> RedirectResponse:
    redirect_url = "/admin/users"
    if request.url.query:
        redirect_url = f"{redirect_url}?{request.url.query}"
    return RedirectResponse(url=redirect_url, status_code=303)


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
        "show_on_homepage": "0",
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
        "show_on_homepage": "1" if tariff.show_on_homepage else "0",
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
        "show_on_homepage": "1" if _checkbox_is_true(form.get("show_on_homepage")) else "0",
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
    raw_show_on_homepage=None,
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
    show_on_homepage = _checkbox_is_true(raw_show_on_homepage)
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
        "show_on_homepage": show_on_homepage,
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
                "show_on_homepage_label": "Да" if tariff.show_on_homepage else "Нет",
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


@router.api_route("/admin/account-blocks", methods=["GET", "HEAD"], response_class=HTMLResponse)
def admin_account_blocks(request: Request):
    settings = get_settings()
    user, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response
    return _template(
        request,
        "account_blocks.html",
        title=page_title("Блоки аккаунтов"),
        admin_email=user.email,
        admin_login=user.login,
        **_admin_account_block_page_context(user, settings, request),
    )


@router.post("/admin/account-blocks")
async def admin_account_blocks_create(request: Request, type: str = Form(default=""), login: str = Form(default=""), password_secret: str = Form(default=""), duration_days: str = Form(default="")):
    settings = get_settings()
    user, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response
    form = await request.form()
    selected_user, selected_email, _ = _resolve_account_block_selected_user(user, settings, request)
    if selected_user is None:
        raise HTTPException(status_code=400, detail="Пользователь не найден.")
    try:
        created_block = create_account_block(
            actor=user,
            data=AccountBlockCreateInput(
                owner_user_id=int(selected_user.id),
                type=type,
                login=login,
                password_secret=password_secret,
                duration_days=_resolve_create_duration_days(form),
            ),
            settings=settings,
        )
    except AuthNotFoundError:
        raise HTTPException(status_code=404, detail="user not found")
    except AccountBlockPermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except (AccountBlockValidationError, AccountBlockNotFoundError, AuthValidationError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return _admin_account_block_redirect(notice_key="created", selected_user_email=selected_email)


@router.post("/admin/account-blocks/{block_id}")
async def admin_account_blocks_update(request: Request, block_id: int, login: str = Form(default=""), password_secret: str = Form(default="")):
    settings = get_settings()
    user, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response
    try:
        existing_block = get_account_block_public(actor=user, block_id=block_id, settings=settings)
        selected_email = _selected_email_for_block(
            request,
            settings,
            user.email,
            existing_block.owner_user_id,
        )
        update_account_block(
            actor=user,
            block_id=block_id,
            data=AccountBlockUpdateInput(
                login=login,
                password_secret=password_secret,
            ),
            settings=settings,
        )
    except AccountBlockPermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except AccountBlockNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AccountBlockValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return _admin_account_block_redirect(notice_key="updated", selected_user_email=selected_email)


@router.post("/admin/account-blocks/{block_id}/delete")
def admin_account_blocks_delete(request: Request, block_id: int):
    settings = get_settings()
    user, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response
    try:
        existing_block = get_account_block_public(actor=user, block_id=block_id, settings=settings)
        selected_email = _selected_email_for_block(
            request,
            settings,
            user.email,
            existing_block.owner_user_id,
        )
        delete_account_block(actor=user, block_id=block_id, settings=settings)
    except AccountBlockPermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except AccountBlockNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return _admin_account_block_redirect(notice_key="deleted", selected_user_email=selected_email)


@router.post("/admin/account-blocks/{block_id}/activate")
def admin_account_blocks_activate(request: Request, block_id: int, duration_days: str = Form(default="")):
    settings = get_settings()
    user, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response
    try:
        existing_block = get_account_block_public(actor=user, block_id=block_id, settings=settings)
        selected_email = _selected_email_for_block(
            request,
            settings,
            user.email,
            existing_block.owner_user_id,
        )
        activation_result = activate_account_block(
            actor=user,
            block_id=block_id,
            duration_days=_parse_optional_account_block_duration(duration_days),
            settings=settings,
        )
        notice_key = "activated"
        if activation_result.notification is not None:
            try:
                send_account_block_activation_email(activation_result.notification, settings=settings)
                notice_key = "activated_email_sent"
            except Exception as exc:  # pragma: no cover - defensive logging path
                notice_key = "activated_email_failed"
                logger.warning(
                    "Account block activation email failed for block_id=%s owner_user_id=%s: %s",
                    block_id,
                    activation_result.block.owner_user_id,
                    exc,
                )
        else:
            notice_key = "activated_email_failed"
    except AccountBlockPermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except AccountBlockNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AccountBlockValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return _admin_account_block_redirect(notice_key=notice_key, selected_user_email=selected_email)


@router.post("/admin/account-blocks/{block_id}/renew")
def admin_account_blocks_renew(request: Request, block_id: int, duration_days: str = Form(default="")):
    settings = get_settings()
    user, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response
    try:
        existing_block = get_account_block_public(actor=user, block_id=block_id, settings=settings)
        selected_email = _selected_email_for_block(
            request,
            settings,
            user.email,
            existing_block.owner_user_id,
        )
        renew_account_block(
            actor=user,
            block_id=block_id,
            duration_days=_parse_optional_account_block_duration(duration_days),
            settings=settings,
        )
    except AccountBlockPermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except AccountBlockNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AccountBlockValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return _admin_account_block_redirect(notice_key="renewed", selected_user_email=selected_email)


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
    if role not in {"user", "moderator"}:
        return _role_error_response("unsupported moderator role")
    try:
        update_user_role(user_id=user_id, new_role=role, settings=settings)
    except AuthNotFoundError:
        raise HTTPException(status_code=404, detail="user not found")
    except RoleError as exc:
        return _role_error_response(str(exc))
    return _admin_users_redirect(request)


@router.post("/admin/users/{user_id}/materials-access/grant")
def admin_user_materials_access_grant(request: Request, user_id: int):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response
    try:
        set_user_materials_access(user_id=user_id, granted=True, settings=settings)
    except AuthNotFoundError as exc:
        raise HTTPException(status_code=404, detail="user not found") from exc
    return _admin_users_redirect(request)


@router.post("/admin/users/{user_id}/materials-access/revoke")
def admin_user_materials_access_revoke(request: Request, user_id: int):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response
    try:
        set_user_materials_access(user_id=user_id, granted=False, settings=settings)
    except AuthNotFoundError as exc:
        raise HTTPException(status_code=404, detail="user not found") from exc
    return _admin_users_redirect(request)


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
        raw_show_on_homepage=form.get("show_on_homepage"),
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
        raw_show_on_homepage=form.get("show_on_homepage"),
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
                show_on_homepage=payload["show_on_homepage"],
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
