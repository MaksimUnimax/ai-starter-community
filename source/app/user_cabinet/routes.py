"""User cabinet routes guarded by the session cookie."""

from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from jinja2 import ChoiceLoader, FileSystemLoader

from app.auth.service import get_current_user_from_cookies, has_staff_materials_access
from app.core.config import get_settings
from app.tariffs.service import list_active_tariffs_with_options

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


@router.get("/cabinet", response_class=HTMLResponse)
def cabinet_page(request: Request):
    settings = get_settings()
    user = get_current_user_from_cookies(request.cookies, settings=settings)
    if user is None:
        return RedirectResponse(url="/login", status_code=303)

    staff_access = has_staff_materials_access(user.role)
    paid_access = user.materials_access_granted_at is not None
    materials_access_active = staff_access or paid_access
    if staff_access:
        materials_access_label = "доступен по роли"
        materials_access_hint = "Раздел «Работа с ИИ» доступен для вашей роли."
    elif paid_access:
        materials_access_label = "активирован"
        materials_access_hint = "Раздел «Работа с ИИ» открыт и доступен ниже."
    else:
        materials_access_label = "не активирован"
        materials_access_hint = "Раздел «Работа с ИИ» будет доступен после оплаты."
    account_status_label = "активен" if user.is_active else "неактивен"
    tariffs = list_active_tariffs_with_options(settings=settings)
    return _template(
        request,
        "cabinet.html",
        title="Личный кабинет",
        user_email=user.email,
        user_login=user.login,
        account_status_label=account_status_label,
        materials_access_active=materials_access_active,
        materials_access_by_role=staff_access,
        materials_access_label=materials_access_label,
        materials_access_hint=materials_access_hint,
        tariffs=tariffs,
    )


@router.head("/cabinet")
def cabinet_head(request: Request):
    response = cabinet_page(request)
    return response
