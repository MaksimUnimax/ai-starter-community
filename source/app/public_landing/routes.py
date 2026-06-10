"""Public landing routes."""

from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from jinja2 import ChoiceLoader, FileSystemLoader

from app.auth.service import get_current_user_from_cookies
from app.core.config import get_settings
from app.shared.tariff_display import get_homepage_tariff_context

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


def _template(request: Request, template_name: str, **context) -> HTMLResponse:
    payload = {
        "request": request,
        "title": context.pop("title", "Главная"),
        "current_user": get_current_user_from_cookies(request.cookies, settings=get_settings()),
    }
    payload.update(context)
    return templates.TemplateResponse(request, template_name, payload)
@router.get("/", response_class=HTMLResponse)
def landing_page(request: Request) -> HTMLResponse:
    settings = get_settings()
    return _template(request, "index.html", title=LANDING_TITLE, meta_description=LANDING_META_DESCRIPTION, **get_homepage_tariff_context(settings=settings))


@router.head("/")
def landing_head(request: Request) -> HTMLResponse:
    return landing_page(request)
