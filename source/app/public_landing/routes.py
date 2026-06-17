"""Public landing routes."""

from decimal import Decimal
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from jinja2 import ChoiceLoader, FileSystemLoader

from app.auth.service import get_current_user_from_cookies
from app.core.config import get_settings
from app.shared.csrf import configure_template_environment, render_template_response
from app.tariffs.service import get_homepage_tariff, seed_initial_catalog

router = APIRouter()
LANDING_TITLE = "OpenScript — программы, боты и MVP без знаний и опыта"
LANDING_META_DESCRIPTION = (
    "OpenScript помогает людям без технического опыта создавать простые программы, "
    "боты, MVP, помощников, агентов и автоматизации под свои задачи."
)
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))
templates.env.loader = ChoiceLoader(
    [
        templates.env.loader,
        FileSystemLoader(str(Path(__file__).resolve().parents[1] / "shared" / "templates")),
    ]
)
configure_template_environment(templates)


def _template(request: Request, template_name: str, **context) -> HTMLResponse:
    settings = get_settings()
    homepage_tariff = get_homepage_tariff(settings=settings)
    if homepage_tariff is None:
        seed_initial_catalog(settings=settings)
        homepage_tariff = get_homepage_tariff(settings=settings)
    payload = {
        "title": context.pop("title", "Главная"),
        "current_user": get_current_user_from_cookies(request.cookies, settings=settings),
        "homepage_tariff": homepage_tariff,
        "homepage_tariff_price_display": _format_price(homepage_tariff.price_amount_minor, homepage_tariff.currency)
        if homepage_tariff is not None
        else None,
    }
    payload.update(context)
    return render_template_response(templates, request, template_name, settings=settings, **payload)


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


@router.get("/", response_class=HTMLResponse)
def landing_page(request: Request) -> HTMLResponse:
    return _template(
        request,
        "index.html",
        title=LANDING_TITLE,
        meta_description=LANDING_META_DESCRIPTION,
    )


@router.head("/")
def landing_head(request: Request) -> HTMLResponse:
    return landing_page(request)
