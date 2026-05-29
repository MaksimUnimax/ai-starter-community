"""Materials page routes."""

from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from jinja2 import ChoiceLoader, FileSystemLoader

from app.auth.service import get_current_user_from_cookies
from app.core.config import get_settings
from app.materials.course_loader import (
    get_lesson,
    list_lessons,
    load_course,
    render_markdown,
    LessonNotFoundError,
)

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))
templates.env.loader = ChoiceLoader(
    [
        templates.env.loader,
        FileSystemLoader(str(Path(__file__).resolve().parents[1] / "shared" / "templates")),
    ]
)
DAIR_SMOKE_TEST_URL = "/materials/drafts/dair-smoke-20260529/"
DAIR_SMOKE_DRAFT_ROOT = Path(__file__).resolve().parent / "course_content" / "drafts" / "dair_smoke_20260529"
DAIR_SMOKE_PREVIEW_HTML = """
  <section
    style="max-width: 1280px; margin: 16px auto 0; padding: 16px 20px; border: 1px solid #e8ded0; border-radius: 18px; background: linear-gradient(180deg, #fffdf8 0%, #fff9f0 100%); color: #231f1a;"
    aria-label="DAIR smoke draft preview"
  >
    <p style="margin: 0 0 8px; text-transform: uppercase; letter-spacing: 0.15em; font-size: 0.74rem; color: #c2410c; font-weight: 700;">Draft test page</p>
    <h1 style="margin: 0; font-family: Georgia, serif; font-size: clamp(1.8rem, 3vw, 2.4rem); line-height: 1.1;">Работа с ИИ</h1>
    <h2 style="margin: 10px 0 0; font-family: Georgia, serif; font-size: clamp(1.1rem, 2vw, 1.55rem); line-height: 1.2;">Как мы работаем: ChatGPT проектирует, Codex выполняет, пользователь проверяет</h2>
    <p style="margin: 10px 0 0; color: #766f66;">ChatGPT проектирует шаг, Codex выполняет точную задачу, пользователь проверяет результат и приносит отчёт обратно.</p>
  </section>
"""


def _read_dair_smoke_asset(filename: str) -> str:
    path = DAIR_SMOKE_DRAFT_ROOT / filename
    if not path.is_file():
        raise HTTPException(status_code=404, detail=f"Missing DAIR smoke artifact file: {filename}")
    return path.read_text(encoding="utf-8")


def _template(request: Request, template_name: str, **context) -> HTMLResponse:
    payload = {
        "request": request,
        "title": context.pop("title", "Работа с ИИ"),
        "current_user": get_current_user_from_cookies(request.cookies, settings=get_settings()),
    }
    payload.update(context)
    return templates.TemplateResponse(request, template_name, payload)


@router.get("/materials", response_class=HTMLResponse)
def materials_page(request: Request):
    settings = get_settings()
    user = get_current_user_from_cookies(request.cookies, settings=settings)
    if user is None:
        return RedirectResponse(url="/login", status_code=303)
    course = load_course()
    return _template(
        request,
        "materials.html",
        title="Работа с ИИ",
        course_title=course["title"],
        course_audience=course["audience"],
        lessons=list_lessons(),
        user_email=user.email,
        user_login=user.login,
        dair_smoke_test_url=DAIR_SMOKE_TEST_URL,
    )


@router.head("/materials")
def materials_head(request: Request):
    settings = get_settings()
    user = get_current_user_from_cookies(request.cookies, settings=settings)
    if user is None:
        return RedirectResponse(url="/login", status_code=303)
    return materials_page(request)


@router.get("/materials/lessons/{slug}", response_class=HTMLResponse)
def lesson_page(request: Request, slug: str):
    settings = get_settings()
    user = get_current_user_from_cookies(request.cookies, settings=settings)
    if user is None:
        return RedirectResponse(url="/login", status_code=303)
    try:
        lesson = get_lesson(slug)
    except LessonNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return _template(
        request,
        "lesson.html",
        title=lesson["title"],
        course_title=load_course()["title"],
        lesson=lesson,
        lesson_html=render_markdown(lesson["content"]),
    )


@router.head("/materials/lessons/{slug}")
def lesson_head(request: Request, slug: str):
    return lesson_page(request, slug)


@router.get(DAIR_SMOKE_TEST_URL, response_class=HTMLResponse)
def dair_smoke_test_page(request: Request):
    settings = get_settings()
    user = get_current_user_from_cookies(request.cookies, settings=settings)
    if user is None:
        return RedirectResponse(url="/login", status_code=303)
    html = _read_dair_smoke_asset("index.html").replace("<body>", f"<body>{DAIR_SMOKE_PREVIEW_HTML}", 1)
    return HTMLResponse(html)


@router.get("/materials/drafts/dair-smoke-20260529/styles.css")
def dair_smoke_test_styles():
    return Response(
        _read_dair_smoke_asset("styles.css"),
        media_type="text/css; charset=utf-8",
    )


@router.get("/materials/drafts/dair-smoke-20260529/script.js")
def dair_smoke_test_script():
    return Response(
        _read_dair_smoke_asset("script.js"),
        media_type="application/javascript; charset=utf-8",
    )
