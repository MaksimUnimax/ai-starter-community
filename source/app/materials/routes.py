"""Materials page routes."""

from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from jinja2 import ChoiceLoader, FileSystemLoader

from app.auth.service import get_user_by_session_token
from app.core.config import get_settings
from app.materials.service import user_has_materials_access

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))
templates.env.loader = ChoiceLoader(
    [
        templates.env.loader,
        FileSystemLoader(str(Path(__file__).resolve().parents[1] / "shared" / "templates")),
    ]
)


def _template(request: Request, template_name: str, **context) -> HTMLResponse:
    payload = {"request": request, "title": context.pop("title", "Материалы")}
    payload.update(context)
    return templates.TemplateResponse(request, template_name, payload)


@router.get("/materials", response_class=HTMLResponse)
def materials_page(request: Request):
    settings = get_settings()
    session_token = request.cookies.get(settings.session_cookie_name)
    user = get_user_by_session_token(session_token, settings=settings)
    if user is None:
        return RedirectResponse(url="/login", status_code=303)

    has_access = user_has_materials_access(user)
    return _template(
        request,
        "materials.html",
        title="Материалы",
        user_email=user.email,
        user_login=user.login,
        has_materials_access=has_access,
    )


@router.head("/materials")
def materials_head(request: Request):
    settings = get_settings()
    session_token = request.cookies.get(settings.session_cookie_name)
    user = get_user_by_session_token(session_token, settings=settings)
    if user is None:
        return RedirectResponse(url="/login", status_code=303)
    return materials_page(request)
