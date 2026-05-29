"""User cabinet routes guarded by the session cookie."""

from pathlib import Path

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
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

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))
templates.env.loader = ChoiceLoader(
    [
        templates.env.loader,
        FileSystemLoader(str(Path(__file__).resolve().parents[1] / "shared" / "templates")),
    ]
)


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

    return _template(
        request,
        "cabinet.html",
        title="Личный кабинет",
        user_email=user.email,
        user_login=user.login,
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
