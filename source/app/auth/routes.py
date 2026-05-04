"""Authentication placeholder routes."""

from pathlib import Path

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.shared.utils import page_title

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "login.html",
        {"request": request, "title": page_title("Вход")},
    )


@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "register.html",
        {"request": request, "title": page_title("Регистрация")},
    )


@router.post("/login")
def login_submit(email: str = Form(default=""), password: str = Form(default="")) -> RedirectResponse:
    _ = (email, password)
    return RedirectResponse(url="/login?status=placeholder", status_code=303)


@router.post("/register")
def register_submit(email: str = Form(default=""), password: str = Form(default="")) -> RedirectResponse:
    _ = (email, password)
    return RedirectResponse(url="/register?status=placeholder", status_code=303)


@router.post("/logout")
def logout() -> RedirectResponse:
    return RedirectResponse(url="/login", status_code=303)
