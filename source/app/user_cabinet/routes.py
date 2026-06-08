"""User cabinet routes guarded by the session cookie."""

from decimal import Decimal
from pathlib import Path

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from jinja2 import ChoiceLoader, FileSystemLoader

from app.auth.service import (
    AuthError,
    NotFoundError,
    UnauthorizedError,
    ValidationError,
    change_password,
    get_current_user_from_cookies,
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
