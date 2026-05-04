"""Admin dashboard routes."""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.auth.service import get_user_by_session_token, list_users_for_admin
from app.core.config import get_settings
from app.paid_options.service import list_paid_options
from app.tariffs.service import list_tariffs, list_tariff_options
from app.shared.utils import page_title

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))


def _template(request: Request, template_name: str, **context) -> HTMLResponse:
    payload = {"request": request, "title": context.pop("title", page_title("AI Starter Community"))}
    payload.update(context)
    return templates.TemplateResponse(request, template_name, payload)


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


def _tariffs_for_admin(settings):
    tariffs = list_tariffs(include_hidden=True, include_archived=True, settings=settings)
    rows = []
    for tariff in tariffs:
        linked_options = list_tariff_options(tariff.code, settings=settings)
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
