"""User cabinet placeholder routes."""

from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.shared.utils import page_title

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))


@router.get("/cabinet", response_class=HTMLResponse)
def cabinet_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "cabinet.html",
        {
            "request": request,
            "title": page_title("Кабинет"),
            "access_status": "Доступ не активирован",
        },
    )
