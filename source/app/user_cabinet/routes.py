"""User cabinet routes guarded by the session cookie."""

from collections import defaultdict
from decimal import Decimal
from pathlib import Path

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
    update_account_block,
)
from app.core.config import get_settings
from app.paid_options.service import list_paid_options
from app.materials.service import user_has_materials_access
from app.user_cabinet.prompts_library import load_cabinet_prompts

router = APIRouter()
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
ACCOUNT_BLOCK_TYPE_LABELS = {
    "chatgpt": "ChatGPT",
    "server": "Сервер",
    "mail": "Почта",
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
    "activated": "Блок активирован на 60 дней.",
}


def _account_block_owner_summary(user) -> dict[str, object]:
    return {
        "id": int(user["id"]) if isinstance(user, dict) else int(user.id),
        "email": user["email"] if isinstance(user, dict) else user.email,
        "login": user["login"] if isinstance(user, dict) else user.login,
        "role": user["role"] if isinstance(user, dict) else user.role,
        "role_label": user.get("role_label") if isinstance(user, dict) else role_label_ru(user.role),
        "display_label": (
            f"{user['login']} · {user['email']}" if isinstance(user, dict) else f"{user.login} · {user.email}"
        ),
    }


def _account_block_card_context(block, copy_data, owner_summary: dict[str, object] | None = None) -> dict[str, object]:
    return {
        "id": block.id,
        "owner_user_id": block.owner_user_id,
        "owner": owner_summary,
        "type": block.type,
        "type_label": ACCOUNT_BLOCK_TYPE_LABELS.get(block.type, block.type),
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


def _selected_owner_id(request: Request, fallback_owner_id: int) -> int:
    raw_owner_id = (request.query_params.get("owner_id") or "").strip()
    if not raw_owner_id:
        return int(fallback_owner_id)
    try:
        owner_id = int(raw_owner_id)
    except ValueError:
        return int(fallback_owner_id)
    return owner_id if owner_id > 0 else int(fallback_owner_id)


def _account_block_management_context(user, settings, request: Request) -> dict[str, object]:
    manage_mode = can_manage_account_blocks(user)
    notice = _account_block_notice(request)

    if manage_mode:
        owners = [_account_block_owner_summary(owner) for owner in list_users_for_admin(settings=settings)]
        owners_by_id = {int(owner["id"]): owner for owner in owners}
        selected_owner_id = _selected_owner_id(request, int(user.id))
        if selected_owner_id not in owners_by_id and owners:
            selected_owner_id = int(user.id) if int(user.id) in owners_by_id else int(owners[0]["id"])
        blocks_by_owner: dict[int, list[dict[str, object]]] = defaultdict(list)
        for block in list_account_blocks_for_viewer(user, settings=settings):
            copy_data = get_account_block_copy_data(actor=user, block_id=block.id, settings=settings)
            blocks_by_owner[block.owner_user_id].append(
                _account_block_card_context(block, copy_data, owners_by_id.get(block.owner_user_id))
            )
        account_block_groups = [
            {
                "owner": owner,
                "blocks": blocks_by_owner.get(int(owner["id"]), []),
            }
            for owner in owners
            if blocks_by_owner.get(int(owner["id"]))
        ]
        return {
            "account_blocks_manage_mode": True,
            "account_block_owner_options": owners,
            "account_block_selected_owner_id": selected_owner_id,
            "account_block_groups": account_block_groups,
            "account_block_notice": notice,
        }

    owner_summary = _account_block_owner_summary(user)
    blocks = [
        _account_block_card_context(
            block,
            get_account_block_copy_data(actor=user, block_id=block.id, settings=settings),
            owner_summary,
        )
        for block in list_account_blocks_for_viewer(user, settings=settings)
    ]
    return {
        "account_blocks_manage_mode": False,
        "account_block_owner_options": [],
        "account_block_selected_owner_id": int(user.id),
        "account_block_groups": [{"owner": owner_summary, "blocks": blocks}] if blocks else [],
        "account_block_notice": notice,
    }


def _cabinet_account_block_redirect(*, notice_key: str, owner_user_id: int | None = None) -> RedirectResponse:
    query = [f"account_blocks_notice={notice_key}"]
    if owner_user_id is not None:
        query.append(f"owner_id={int(owner_user_id)}")
    return RedirectResponse(url=f"/cabinet?{'&'.join(query)}", status_code=303)


def _parse_account_block_form_fields(
    *,
    owner_user_id: int,
    block_type: str,
    login: str,
    password_secret: str,
) -> AccountBlockCreateInput:
    return AccountBlockCreateInput(
        owner_user_id=owner_user_id,
        type=block_type,
        login=login,
        password_secret=password_secret,
        duration_days=ACCOUNT_BLOCK_DURATION_DAYS,
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
        account_block_duration_days=ACCOUNT_BLOCK_DURATION_DAYS,
        account_block_type_options=[
            {"value": "chatgpt", "label": "ChatGPT"},
            {"value": "server", "label": "Сервер"},
            {"value": "mail", "label": "Почта"},
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
    owner_user_id: int = Form(default=0),
    block_type: str = Form(alias="type", default=""),
    login: str = Form(default=""),
    password_secret: str = Form(default=""),
):
    settings, user, redirect_response = _require_authenticated_user(request)
    if redirect_response is not None:
        return redirect_response
    if not can_manage_account_blocks(user):
        raise HTTPException(status_code=403, detail="account block management requires moderator or admin access")
    try:
        created_block = create_account_block(
            actor=user,
            data=_parse_account_block_form_fields(
                owner_user_id=owner_user_id,
                block_type=block_type,
                login=login,
                password_secret=password_secret,
            ),
            settings=settings,
        )
    except AccountBlockPermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except (AccountBlockValidationError, AccountBlockNotFoundError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return _cabinet_account_block_redirect(notice_key="created", owner_user_id=created_block.owner_user_id)


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
    return _cabinet_account_block_redirect(notice_key="updated", owner_user_id=updated_block.owner_user_id)


@router.post("/cabinet/account-blocks/{block_id}/delete")
def cabinet_delete_account_block(request: Request, block_id: int):
    settings, user, redirect_response = _require_authenticated_user(request)
    if redirect_response is not None:
        return redirect_response
    if not can_manage_account_blocks(user):
        raise HTTPException(status_code=403, detail="account block management requires moderator or admin access")
    try:
        existing_block = get_account_block_public(actor=user, block_id=block_id, settings=settings)
        delete_account_block(actor=user, block_id=block_id, settings=settings)
    except AccountBlockPermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except AccountBlockNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return _cabinet_account_block_redirect(notice_key="deleted", owner_user_id=existing_block.owner_user_id)


@router.post("/cabinet/account-blocks/{block_id}/activate")
def cabinet_activate_account_block(request: Request, block_id: int):
    settings, user, redirect_response = _require_authenticated_user(request)
    if redirect_response is not None:
        return redirect_response
    if not can_manage_account_blocks(user):
        raise HTTPException(status_code=403, detail="account block management requires moderator or admin access")
    try:
        activation_result = activate_account_block(actor=user, block_id=block_id, settings=settings)
    except AccountBlockPermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except AccountBlockNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return _cabinet_account_block_redirect(
        notice_key="activated",
        owner_user_id=activation_result.block.owner_user_id,
    )
