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
from app.materials.service import user_has_materials_access

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))
templates.env.loader = ChoiceLoader(
    [
        templates.env.loader,
        FileSystemLoader(str(Path(__file__).resolve().parents[1] / "user_cabinet" / "templates")),
        FileSystemLoader(str(Path(__file__).resolve().parents[1] / "shared" / "templates")),
    ]
)
LESSON_TEST_URL = "/materials/drafts/dair-smoke-20260529/"
LESSON_TEST_STYLES_URL = "/materials/drafts/dair-smoke-20260529/styles.css"
LESSON_TEST_SCRIPT_URL = "/materials/drafts/dair-smoke-20260529/script.js"
LESSON_TEST_ROOT = Path(__file__).resolve().parent / "course_content" / "drafts" / "dair_smoke_20260529"


def _require_learning_access(request: Request):
    settings = get_settings()
    user = get_current_user_from_cookies(request.cookies, settings=settings)
    if user is None:
        return None, RedirectResponse(url="/login", status_code=303)
    if not user_has_materials_access(user):
        raise HTTPException(status_code=403, detail="learning access required")
    return user, None


def _read_lesson_test_asset(filename: str) -> str:
    path = LESSON_TEST_ROOT / filename
    if not path.is_file():
        raise HTTPException(status_code=404, detail=f"Missing lesson test file: {filename}")
    return path.read_text(encoding="utf-8")


def _template(request: Request, template_name: str, **context) -> HTMLResponse:
    payload = {
        "request": request,
        "title": context.pop("title", "Работа с ИИ"),
        "current_user": get_current_user_from_cookies(request.cookies, settings=get_settings()),
    }
    payload.update(context)
    return templates.TemplateResponse(request, template_name, payload)


def _locked_response(
    request: Request,
    *,
    title: str,
    locked_title: str,
    locked_message: str,
    locked_action_label: str = "На главную",
    locked_action_url: str = "/",
    locked_secondary_label: str | None = None,
    locked_secondary_url: str | None = None,
    current_user=None,
):
    return _template(
        request,
        "access_locked.html",
        title=title,
        locked_title=locked_title,
        locked_message=locked_message,
        locked_action_label=locked_action_label,
        locked_action_url=locked_action_url,
        locked_secondary_label=locked_secondary_label,
        locked_secondary_url=locked_secondary_url,
        current_user=current_user,
    )


@router.get("/materials", response_class=HTMLResponse)
def materials_page(request: Request):
    settings = get_settings()
    user = get_current_user_from_cookies(request.cookies, settings=settings)
    if user is None:
        return RedirectResponse(url="/login", status_code=303)
    if not user_has_materials_access(user):
        return _locked_response(
            request,
            title="Работа с ИИ",
            locked_title="Раздел «Работа с ИИ» закрыт",
            locked_message="Доступ к материалам и урокам откроется после оплаты тарифа.",
            locked_action_label="На главную",
            locked_action_url="/",
            locked_secondary_label="В личный кабинет",
            locked_secondary_url="/cabinet",
            current_user=user,
        )
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
        lesson_test_url=LESSON_TEST_URL,
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
    if not user_has_materials_access(user):
        return _locked_response(
            request,
            title=lesson["title"],
            locked_title=lesson["title"],
            locked_message="Урок и его материалы откроются после оплаты тарифа.",
            locked_action_label="К разделу материалов",
            locked_action_url="/materials",
            locked_secondary_label="На главную",
            locked_secondary_url="/",
            current_user=user,
        )
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


@router.get(LESSON_TEST_URL, response_class=HTMLResponse)
def lesson_test_page(request: Request):
    _, redirect_response = _require_learning_access(request)
    if redirect_response is not None:
        return redirect_response
    return HTMLResponse(_read_lesson_test_asset("index.html"))


@router.get(LESSON_TEST_STYLES_URL)
def lesson_test_styles(request: Request):
    _, redirect_response = _require_learning_access(request)
    if redirect_response is not None:
        return redirect_response
    return Response(
        _read_lesson_test_asset("styles.css"),
        media_type="text/css; charset=utf-8",
    )


@router.get(LESSON_TEST_SCRIPT_URL)
def lesson_test_script(request: Request):
    _, redirect_response = _require_learning_access(request)
    if redirect_response is not None:
        return redirect_response
    return Response(
        _read_lesson_test_asset("script.js"),
        media_type="application/javascript; charset=utf-8",
    )
