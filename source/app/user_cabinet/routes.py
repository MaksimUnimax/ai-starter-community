"""User cabinet routes guarded by the session cookie."""

from decimal import Decimal
import logging
from pathlib import Path
from urllib.parse import urlencode

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from jinja2 import ChoiceLoader, FileSystemLoader

from app.auth.service import (
    AuthError,
    can_manage_account_blocks,
    NotFoundError,
    UnauthorizedError,
    ValidationError,
    change_password,
    get_current_user_from_cookies,
    get_user_by_email,
    list_users_for_admin,
    role_label_ru,
)
from app.account_blocks.schemas import AccountBlockCreateInput, AccountBlockUpdateInput
from app.account_blocks.service import (
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
from app.core.config import get_settings
from app.notifications.email_service import send_account_block_activation_email
from app.shared.tariff_display import get_homepage_tariff_context
from app.paid_options.service import list_paid_options
from app.materials.service import user_has_materials_access
from app.user_cabinet.prompts_library import load_cabinet_prompts

router = APIRouter()
logger = logging.getLogger(__name__)
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))
templates.env.loader = ChoiceLoader(
    [
        templates.env.loader,
        FileSystemLoader(str(Path(__file__).resolve().parents[1] / "shared" / "templates")),
    ]
)
LEARNING_COURSE_URL = "/materials/drafts/dair-smoke-20260529/"
LEARNING_PROJECT_DOWNLOAD_URL = "/cabinet/learning/project-file"
LEARNING_PROJECT_FILE_NAME = "02_СТАРТ_ПРОЕКТА_GIT_ДОКУМЕНТАЦИЯ_СТРУКТУРА.md"
LEARNING_PROJECT_FILE_PATH = Path(__file__).resolve().parent / "private_files" / LEARNING_PROJECT_FILE_NAME
BASE_CABINET_PAID_OPTION_CODE = "ai_gpt_tool"
ACCOUNT_BLOCK_DURATION_DAYS = 60
ACCOUNT_BLOCK_CREATE_DEFAULT_DURATION_DAYS = 30
ACCOUNT_BLOCK_TYPE_LABELS = {
    "chatgpt": "ChatGPT",
    "server": "Сервер",
    "mail": "Почта",
    "vpn": "ВПН",
}
ACCOUNT_BLOCK_CARD_TITLE_LABELS = {
    "chatgpt": "Chat",
}
ACCOUNT_BLOCK_CARD_TYPE_LABELS = {
    "chatgpt": "GPT",
}
ACCOUNT_BLOCK_STATUS_LABELS = {
    "active": "Активно",
    "inactive": "Неактивно",
    "expired": "Истекло",
}
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


def _account_block_owner_summary(user) -> dict[str, object]:
    return {
        "id": int(user["id"]) if isinstance(user, dict) else int(user.id),
        "email": user["email"] if isinstance(user, dict) else user.email,
        "login": user["login"] if isinstance(user, dict) else user.login,
        "role": user["role"] if isinstance(user, dict) else user.role,
        "role_label": user.get("role_label") if isinstance(user, dict) else role_label_ru(user.role),
        "display_label": f"{user['login']} · {user['email']}" if isinstance(user, dict) else f"{user.login} · {user.email}",
    }


def _user_attr(user, key: str):
    if isinstance(user, dict):
        return user.get(key)
    return getattr(user, key)


def _account_block_owner_email(settings, owner_user_id: int) -> str | None:
    for owner in list_users_for_admin(settings=settings):
        if int(_user_attr(owner, "id")) == int(owner_user_id):
            return str(_user_attr(owner, "email"))
    return None


def _account_block_card_context(block, copy_data, owner_summary: dict[str, object] | None = None) -> dict[str, object]:
    return {
        "id": block.id,
        "owner_user_id": block.owner_user_id,
        "owner": owner_summary,
        "type": block.type,
        "type_label": ACCOUNT_BLOCK_TYPE_LABELS.get(block.type, block.type),
        "display_title": ACCOUNT_BLOCK_CARD_TITLE_LABELS.get(block.type, block.title),
        "display_type_label": ACCOUNT_BLOCK_CARD_TYPE_LABELS.get(block.type, ACCOUNT_BLOCK_TYPE_LABELS.get(block.type, block.type)),
        "title": block.title,
        "login": copy_data.login,
        "password_secret": copy_data.password_secret,
        "status": block.status,
        "status_label": ACCOUNT_BLOCK_STATUS_LABELS.get(block.status, block.status),
        "duration_days": block.duration_days,
        "activation_day": block.activation_day,
        "activation_summary": block.activation_summary,
        "is_active": block.is_active,
        "is_expired": block.is_expired,
    }


def _account_block_notice(request: Request) -> str | None:
    notice_key = (request.query_params.get("account_blocks_notice") or "").strip().lower()
    return ACCOUNT_BLOCK_NOTICE_MESSAGES.get(notice_key)


def _selected_account_block_email(request: Request, fallback_email: str) -> str:
    raw_email = (request.query_params.get("account_blocks_user_email") or "").strip()
    return raw_email or fallback_email


def _paid_option_duration_days(option) -> int:
    if option.default_duration_days is not None and int(option.default_duration_days) > 0:
        return int(option.default_duration_days)
    return ACCOUNT_BLOCK_DURATION_DAYS


def _active_paid_options_for_cabinet(settings):
    options = [
        option
        for option in list_paid_options(settings=settings)
        if option.code != BASE_CABINET_PAID_OPTION_CODE
    ]
    options.sort(key=_cabinet_paid_option_sort_key)
    return [
        {
            "id": option.id,
            "code": option.code,
            "title": option.title,
            "description": option.description,
            "formatted_price": _format_price(option.price_amount_minor, option.currency),
            "currency": option.currency,
            "default_duration_days": option.default_duration_days,
            "resolved_duration_days": _paid_option_duration_days(option),
            "is_renewable": option.is_renewable,
            "status": option.status,
        }
        for option in options
    ]


def _resolve_account_block_selected_user(user, settings, request: Request) -> tuple[object | None, str, str | None]:
    manage_mode = can_manage_account_blocks(user)
    notice = _account_block_notice(request)
    selected_email = _selected_account_block_email(request, user.email)

    if not manage_mode:
        return user, user.email, notice

    if selected_email != user.email:
        try:
            selected_user = get_user_by_email(selected_email, settings=settings)
        except ValidationError:
            return None, selected_email, "Пользователь не найден."
        if selected_user is None:
            return None, selected_email, "Пользователь не найден."
        return selected_user, selected_email, notice

    return user, user.email, notice


def _account_block_management_context(user, settings, request: Request) -> dict[str, object]:
    manage_mode = can_manage_account_blocks(user)
    selected_user, selected_email, notice = _resolve_account_block_selected_user(user, settings, request)
    selected_owner_summary = _account_block_owner_summary(selected_user) if selected_user is not None else None
    selected_blocks = []
    if selected_user is not None:
        visible_blocks = list_account_blocks_for_viewer(user, owner_user_id=int(selected_user.id), settings=settings)
        if not manage_mode:
            visible_blocks = [block for block in visible_blocks if block.is_active]
        selected_blocks = [
            _account_block_card_context(
                block,
                get_account_block_copy_data(actor=user, block_id=block.id, settings=settings),
                selected_owner_summary,
            )
            for block in visible_blocks
        ]

    return {
        "account_blocks_manage_mode": manage_mode,
        "account_block_query_string": f"?{urlencode({'account_blocks_user_email': selected_email})}" if manage_mode else "",
        "account_block_owner_options": [
            {
                "email": _user_attr(owner, "email"),
                "login": _user_attr(owner, "login"),
                "role": _user_attr(owner, "role"),
                "role_label": role_label_ru(_user_attr(owner, "role")),
                "display_label": f"{_user_attr(owner, 'login')} · {_user_attr(owner, 'email')}",
            }
            for owner in list_users_for_admin(settings=settings)
        ]
        if manage_mode
        else [],
        "account_block_selected_user": selected_user,
        "account_block_selected_user_email": selected_email,
        "account_block_selected_user_summary": selected_owner_summary,
        "account_block_blocks": selected_blocks,
        "account_block_notice": notice,
        "account_block_create_default_duration_days": ACCOUNT_BLOCK_CREATE_DEFAULT_DURATION_DAYS,
    }


def _cabinet_account_block_redirect(*, notice_key: str, selected_user_email: str | None = None) -> RedirectResponse:
    query = {"account_blocks_notice": notice_key}
    if selected_user_email:
        query["account_blocks_user_email"] = selected_user_email
    return RedirectResponse(url=f"/cabinet?{urlencode(query)}", status_code=303)


def _selected_email_for_block(request: Request, settings, fallback_email: str, owner_user_id: int) -> str:
    selected_email = _selected_account_block_email(request, fallback_email)
    if selected_email != fallback_email:
        return selected_email
    owner_email = _account_block_owner_email(settings, owner_user_id)
    return owner_email or fallback_email


def _parse_account_block_form_fields(
    *,
    owner_user_id: int,
    block_type: str,
    login: str,
    password_secret: str,
    duration_days: int,
) -> AccountBlockCreateInput:
    return AccountBlockCreateInput(
        owner_user_id=owner_user_id,
        type=block_type,
        login=login,
        password_secret=password_secret,
        duration_days=duration_days,
    )


def _parse_account_block_update_fields(
    *,
    login: str | None,
    password_secret: str | None,
) -> AccountBlockUpdateInput:
    return AccountBlockUpdateInput(
        login=login if login is not None else None,
        password_secret=password_secret if password_secret is not None else None,
    )


def _parse_account_block_duration(value: str | None, *, default: int = ACCOUNT_BLOCK_DURATION_DAYS) -> int:
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


def _format_price(amount_minor: int | None, currency: str | None) -> str:
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


def _cabinet_paid_option_sort_key(option):
    amount_minor = option.price_amount_minor
    return (
        amount_minor is None,
        -(amount_minor or 0),
        int(option.sort_order),
        option.title.casefold(),
        int(option.id),
    )


def _active_paid_options_for_cabinet(settings):
    options = [
        option
        for option in list_paid_options(settings=settings)
        if option.code != BASE_CABINET_PAID_OPTION_CODE
    ]
    options.sort(key=_cabinet_paid_option_sort_key)
    return [
        {
            "id": option.id,
            "code": option.code,
            "title": option.title,
            "description": option.description,
            "formatted_price": _format_price(option.price_amount_minor, option.currency),
            "currency": option.currency,
            "default_duration_days": option.default_duration_days,
            "resolved_duration_days": _paid_option_duration_days(option),
            "is_renewable": option.is_renewable,
            "status": option.status,
        }
        for option in options
    ]


def _template(request: Request, template_name: str, **context) -> HTMLResponse:
    payload = {
        "request": request,
        "title": context.pop("title", "Страница"),
        "current_user": get_current_user_from_cookies(request.cookies, settings=get_settings()),
    }
    payload.update(context)
    return templates.TemplateResponse(request, template_name, payload)


def _locked_response(
    request: Request,
    *,
    title: str,
    locked_title: str,
    locked_message: str,
    locked_action_label: str = "На главную",
    locked_action_url: str = "/",
    locked_secondary_label: str | None = None,
    locked_secondary_url: str | None = None,
    current_user=None,
):
    return _template(
        request,
        "access_locked.html",
        title=title,
        locked_title=locked_title,
        locked_message=locked_message,
        locked_action_label=locked_action_label,
        locked_action_url=locked_action_url,
        locked_secondary_label=locked_secondary_label,
        locked_secondary_url=locked_secondary_url,
        current_user=current_user,
        **get_homepage_tariff_context(settings=get_settings()),
    )


def _password_change_message(exc: ValidationError | UnauthorizedError | AuthError) -> str:
    message = str(exc)
    normalized = message.lower()
    if isinstance(exc, UnauthorizedError):
        return "Текущий пароль неверный."
    if "passwords do not match" in normalized:
        return "Новые пароли не совпадают."
    if (
        "password is required" in normalized
        or "at least 8 characters" in normalized
        or "at most 128 characters" in normalized
        or "must not contain spaces" in normalized
    ):
        return "Пароль должен быть не короче 8 символов и без пробелов."
    return "Не удалось сменить пароль."


def _require_authenticated_user(request: Request):
    settings = get_settings()
    user = get_current_user_from_cookies(request.cookies, settings=settings)
    if user is None:
        return settings, None, RedirectResponse(url="/login", status_code=303)
    return settings, user, None


@router.get("/cabinet", response_class=HTMLResponse)
def cabinet_page(request: Request):
    settings, user, redirect_response = _require_authenticated_user(request)
    if redirect_response is not None:
        return redirect_response
    if not user_has_materials_access(user):
        return _locked_response(
            request,
            title="Личный кабинет",
            locked_title="Личный кабинет будет доступен после оплаты",
            locked_message="После оплаты тарифа откроются личный кабинет, обучение и материалы.",
            locked_action_label="На главную",
            locked_action_url="/",
            locked_secondary_label="К обучению",
            locked_secondary_url=LEARNING_COURSE_URL,
            current_user=user,
        )
    learning_access = user_has_materials_access(user)
    active_paid_options = _active_paid_options_for_cabinet(settings)
    account_block_context = _account_block_management_context(user, settings, request)

    return _template(
        request,
        "cabinet.html",
        title="Личный кабинет",
        learning_access=learning_access,
        learning_course_url=LEARNING_COURSE_URL if learning_access else None,
        learning_download_url=LEARNING_PROJECT_DOWNLOAD_URL if learning_access else None,
        cabinet_prompts=load_cabinet_prompts(),
        active_paid_options=active_paid_options,
        active_paid_options_count=len(active_paid_options),
        account_block_type_options=[
            {"value": "chatgpt", "label": "ChatGPT"},
            {"value": "server", "label": "Сервер"},
            {"value": "mail", "label": "Почта"},
            {"value": "vpn", "label": "ВПН"},
        ],
        **account_block_context,
    )


@router.head("/cabinet")
def cabinet_head(request: Request):
    response = cabinet_page(request)
    return response


@router.get("/cabinet/settings", response_class=HTMLResponse)
def cabinet_settings_page(request: Request):
    settings, user, redirect_response = _require_authenticated_user(request)
    if redirect_response is not None:
        return redirect_response
    return _template(
        request,
        "settings.html",
        title="Настройки",
        user_email=user.email,
        user_login=user.login,
        success=request.query_params.get("success") == "1",
        notice="Пароль изменён." if request.query_params.get("success") == "1" else None,
    )


@router.head("/cabinet/settings")
def cabinet_settings_head(request: Request):
    response = cabinet_settings_page(request)
    return response


@router.get("/cabinet/learning/project-file")
def cabinet_learning_project_file(request: Request):
    settings, user, redirect_response = _require_authenticated_user(request)
    if redirect_response is not None:
        return redirect_response
    if not user_has_materials_access(user):
        raise HTTPException(status_code=403, detail="learning access required")
    if not LEARNING_PROJECT_FILE_PATH.is_file():
        raise HTTPException(status_code=404, detail="learning project file not found")
    return FileResponse(
        path=str(LEARNING_PROJECT_FILE_PATH),
        filename=LEARNING_PROJECT_FILE_NAME,
        media_type="text/markdown; charset=utf-8",
    )


@router.post("/cabinet/settings/password", response_class=HTMLResponse)
def cabinet_change_password(
    request: Request,
    current_password: str = Form(default=""),
    password: str = Form(default=""),
    repeat_password: str = Form(default=""),
) -> HTMLResponse:
    settings, user, redirect_response = _require_authenticated_user(request)
    if redirect_response is not None:
        return redirect_response
    try:
        change_password(
            user_id=user.id,
            current_password=current_password,
            new_password=password,
            repeat_password=repeat_password,
            settings=settings,
        )
    except NotFoundError:
        return RedirectResponse(url="/login", status_code=303)
    except (ValidationError, UnauthorizedError, AuthError) as exc:
        return _template(
            request,
            "settings.html",
            title="Настройки",
            user_email=user.email,
            user_login=user.login,
            error=_password_change_message(exc),
            success=False,
        )
    return RedirectResponse(url="/cabinet/settings?success=1", status_code=303)


@router.post("/cabinet/account-blocks")
def cabinet_create_account_block(
    request: Request,
    block_type: str = Form(alias="type", default=""),
    login: str = Form(default=""),
    password_secret: str = Form(default=""),
    duration_days: str = Form(default=""),
):
    settings, user, redirect_response = _require_authenticated_user(request)
    if redirect_response is not None:
        return redirect_response
    if not can_manage_account_blocks(user):
        raise HTTPException(status_code=403, detail="account block management requires moderator or admin access")
    try:
        selected_user, selected_email, _ = _resolve_account_block_selected_user(user, settings, request)
        if selected_user is None:
            raise HTTPException(status_code=400, detail="Пользователь не найден.")
        created_block = create_account_block(
            actor=user,
            data=_parse_account_block_form_fields(
                owner_user_id=int(selected_user.id),
                block_type=block_type,
                login=login,
                password_secret=password_secret,
                duration_days=_resolve_create_duration_days({"duration_days": duration_days}),
            ),
            settings=settings,
        )
    except AccountBlockPermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except (AccountBlockValidationError, AccountBlockNotFoundError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return _cabinet_account_block_redirect(notice_key="created", selected_user_email=selected_email)


@router.post("/cabinet/account-blocks/{block_id}")
def cabinet_update_account_block(
    request: Request,
    block_id: int,
    login: str = Form(default=""),
    password_secret: str = Form(default=""),
):
    settings, user, redirect_response = _require_authenticated_user(request)
    if redirect_response is not None:
        return redirect_response
    if not can_manage_account_blocks(user):
        raise HTTPException(status_code=403, detail="account block management requires moderator or admin access")
    try:
        existing_block = get_account_block_public(actor=user, block_id=block_id, settings=settings)
        selected_email = _selected_email_for_block(
            request,
            settings,
            user.email,
            existing_block.owner_user_id,
        )
        updated_block = update_account_block(
            actor=user,
            block_id=block_id,
            data=_parse_account_block_update_fields(
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
    return _cabinet_account_block_redirect(notice_key="updated", selected_user_email=selected_email)


@router.post("/cabinet/account-blocks/{block_id}/delete")
def cabinet_delete_account_block(request: Request, block_id: int):
    settings, user, redirect_response = _require_authenticated_user(request)
    if redirect_response is not None:
        return redirect_response
    if not can_manage_account_blocks(user):
        raise HTTPException(status_code=403, detail="account block management requires moderator or admin access")
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
    return _cabinet_account_block_redirect(notice_key="deleted", selected_user_email=selected_email)


@router.post("/cabinet/account-blocks/{block_id}/activate")
def cabinet_activate_account_block(
    request: Request,
    block_id: int,
    duration_days: str = Form(default=""),
):
    settings, user, redirect_response = _require_authenticated_user(request)
    if redirect_response is not None:
        return redirect_response
    if not can_manage_account_blocks(user):
        raise HTTPException(status_code=403, detail="account block management requires moderator or admin access")
    try:
        existing_block = get_account_block_public(actor=user, block_id=block_id, settings=settings)
        selected_email = _selected_email_for_block(
            request,
            settings,
            user.email,
            existing_block.owner_user_id,
        )
        duration_days_value = _parse_optional_account_block_duration(duration_days)
        activation_result = activate_account_block(
            actor=user,
            block_id=block_id,
            duration_days=duration_days_value,
            settings=settings,
        )
        notice_key = "activated"
        if activation_result.notification is not None:
            try:
                send_account_block_activation_email(activation_result.notification, settings=settings)
                notice_key = "activated_email_sent"
            except Exception as exc:
                logger.warning(
                    "Account block activation email failed for block_id=%s owner_user_id=%s: %s",
                    block_id,
                    activation_result.block.owner_user_id,
                    exc,
                )
                notice_key = "activated_email_failed"
        else:
            notice_key = "activated_email_failed"
    except AccountBlockPermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except AccountBlockNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AccountBlockValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return _cabinet_account_block_redirect(
        notice_key=notice_key,
        selected_user_email=selected_email,
    )


@router.post("/cabinet/account-blocks/{block_id}/renew")
def cabinet_renew_account_block(
    request: Request,
    block_id: int,
    duration_days: str = Form(default=""),
):
    settings, user, redirect_response = _require_authenticated_user(request)
    if redirect_response is not None:
        return redirect_response
    if not can_manage_account_blocks(user):
        raise HTTPException(status_code=403, detail="account block management requires moderator or admin access")
    try:
        existing_block = get_account_block_public(actor=user, block_id=block_id, settings=settings)
        selected_email = _selected_email_for_block(
            request,
            settings,
            user.email,
            existing_block.owner_user_id,
        )
        duration_days_value = _parse_optional_account_block_duration(duration_days)
        renew_account_block(
            actor=user,
            block_id=block_id,
            duration_days=duration_days_value,
            settings=settings,
        )
    except AccountBlockPermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except AccountBlockNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AccountBlockValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return _cabinet_account_block_redirect(notice_key="renewed", selected_user_email=selected_email)
