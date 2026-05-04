"""Public landing routes."""

from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.core.config import get_settings
from app.shared.utils import page_title

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))


@router.get("/", response_class=HTMLResponse)
def landing_page(request: Request) -> HTMLResponse:
    settings = get_settings()
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "request": request,
            "title": page_title("Главная", settings.app_name),
            "app_name": settings.app_name,
        },
    )
