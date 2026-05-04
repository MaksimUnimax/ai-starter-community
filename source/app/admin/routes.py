"""Admin dashboard routes."""

from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.auth.service import get_user_by_session_token
from app.core.config import get_settings
from app.shared.utils import page_title

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))


def _template(request: Request, template_name: str, **context) -> HTMLResponse:
    payload = {"request": request, "title": context.pop("title", page_title("AI Starter Community"))}
    payload.update(context)
    return templates.TemplateResponse(request, template_name, payload)


def _admin_user_or_redirect(request: Request):
    settings = get_settings()
    session_token = request.cookies.get(settings.session_cookie_name)
    user = get_user_by_session_token(session_token, settings=settings)
    if user is None:
        return None, RedirectResponse(url="/login", status_code=303)
    if user.role != "admin":
        return user, PlainTextResponse("Forbidden", status_code=403)
    return user, None


@router.api_route("/admin", methods=["GET", "HEAD"], response_class=HTMLResponse)
def admin_dashboard(request: Request):
    user, response = _admin_user_or_redirect(request)
    if response is not None:
        return response
    return _template(
        request,
        "dashboard.html",
        title=page_title("Админ-панель"),
        admin_email=user.email,
        admin_login=user.login,
    )
