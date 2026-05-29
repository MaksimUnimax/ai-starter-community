from __future__ import annotations

import re
import sqlite3

from app.auth.service import authenticate_user, create_session, register_user, verify_email
from app.materials.course_loader import get_lesson, list_lessons, load_course, render_markdown


def _connect(test_settings):
    conn = sqlite3.connect(str(test_settings.database_path))
    conn.row_factory = sqlite3.Row
    return conn


def _extract_token_from_db(test_settings, email: str) -> str:
    with _connect(test_settings) as conn:
        row = conn.execute(
            "SELECT body_text FROM email_outbox WHERE recipient_email = ? AND template_key = ? ORDER BY id DESC LIMIT 1",
            (email, "email_verification"),
        ).fetchone()
    assert row is not None
    match = re.search(r"/verify-email/([A-Za-z0-9_-]+)", row["body_text"])
    assert match
    return match.group(1)


def _prepare_verified_user(client, test_settings, email: str, login: str = "lessonuser"):
    register_user(
        email=email,
        login=login,
        password="Secret123",
        repeat_password="Secret123",
        settings=test_settings,
    )
    token = _extract_token_from_db(test_settings, email)
    verify_email(token, settings=test_settings)
    user = authenticate_user(email, "Secret123", settings=test_settings)
    session_token = create_session(user.id, settings=test_settings)
    client.cookies.set(test_settings.session_cookie_name, session_token)


def test_course_loader_reads_course_yaml():
    course = load_course()
    lessons = course["lessons"]

    assert course["course_id"] == "work-with-ai"
    assert course["title"] == "Работа с ИИ"
    assert course["status"] == "draft"
    assert len(lessons) == 1
    assert lessons[0]["slug"] == "kak-my-rabotaem-chatgpt-codex-user"
    assert lessons[0]["lesson_path"] == "lessons/01-kak-my-rabotaem.md"
    assert lessons[0]["answer_path"] == "answers/01-kak-my-rabotaem.md"


def test_list_lessons_returns_lesson_1():
    lessons = list_lessons()
    assert len(lessons) == 1
    assert lessons[0]["order"] == 1
    assert lessons[0]["title"] == "Как мы работаем: ChatGPT проектирует, Codex выполняет, пользователь проверяет"


def test_get_lesson_finds_lesson_by_slug():
    lesson = get_lesson("kak-my-rabotaem-chatgpt-codex-user")
    assert lesson["title"] == "Как мы работаем: ChatGPT проектирует, Codex выполняет, пользователь проверяет"
    assert ":::task" in lesson["content"]
    assert lesson["content"].count(":::check") >= 5
    assert "CHATGPT_REPORT_BEGIN" in lesson["content"]


def test_render_markdown_handles_interactive_blocks_and_escapes_html():
    html = render_markdown(
        """Before
:::check
question: Что показывает `RESULT`?
answer: `RESULT` показывает итог run.
:::
After
"""
    )

    assert "<details" in html
    assert "Показать ответ" in html
    assert "Что показывает <code>RESULT</code>?" in html
    assert "RESULT" in html

    task_html = render_markdown(
        """:::task
title: Найди поля в отчёте
input:
```text
RESULT: SUCCESS
```
questions:
- Где `RESULT`?
- Какой `TASK_ID`?
answer_ref: ../answers/01-kak-my-rabotaem.md
:::
"""
    )
    assert "lesson-task" in task_html
    assert "Найди поля в отчёте" in task_html
    assert "RESULT: SUCCESS" in task_html
    assert "lesson-checklist" not in task_html

    checklist_html = render_markdown(
        """:::checklist
- [ ] Я нашёл RESULT
- [x] Я нашёл TASK_ID
:::
"""
    )
    assert "lesson-checklist" in checklist_html
    assert 'type="checkbox"' in checklist_html
    assert "checked" in checklist_html

    safe_html = render_markdown("<script>alert(1)</script>")
    assert "<script>" not in safe_html
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in safe_html


def test_materials_and_lesson_pages_render_course_content(client, test_settings):
    _prepare_verified_user(client, test_settings, "course-render@example.com", "courserender")

    materials_response = client.get("/materials")
    assert materials_response.status_code == 200
    assert "Работа с ИИ" in materials_response.text
    assert "Уроки курса" in materials_response.text
    assert "Как мы работаем: ChatGPT проектирует, Codex выполняет, пользователь проверяет" in materials_response.text
    assert "/materials/lessons/kak-my-rabotaem-chatgpt-codex-user" in materials_response.text
    assert "Доступные тарифы" not in materials_response.text
    assert "Оплата" not in materials_response.text
    assert "Последний платёж" not in materials_response.text

    lesson_response = client.get("/materials/lessons/kak-my-rabotaem-chatgpt-codex-user")
    assert lesson_response.status_code == 200
    assert "Как мы работаем: ChatGPT проектирует, Codex выполняет, пользователь проверяет" in lesson_response.text
    assert "Какой отчёт принести в ChatGPT" in lesson_response.text
    assert "lesson-check" in lesson_response.text
    assert "lesson-task" in lesson_response.text
    assert "lesson-checklist" in lesson_response.text
    assert "Показать ответ" in lesson_response.text
    assert "Вернуться к материалам" in lesson_response.text
    assert "/materials" in lesson_response.text


def test_lesson_test_page_is_served_by_the_app(client, test_settings):
    _prepare_verified_user(client, test_settings, "lesson-test@example.com", "lessontest")

    materials_response = client.get("/materials")
    assert materials_response.status_code == 200
    assert "/materials/drafts/dair-smoke-20260529/" in materials_response.text
    assert "Открыть тестовую версию урока" in materials_response.text

    page_response = client.get("/materials/drafts/dair-smoke-20260529/")
    assert page_response.status_code == 200
    assert "Работа с ИИ" in page_response.text
    assert "Как мы работаем" in page_response.text
    assert "ChatGPT" in page_response.text
    assert "Codex" in page_response.text
    assert "Тестовая версия урока" in page_response.text
    assert "Начать урок" in page_response.text
    assert "Перейти к проверке" in page_response.text
    assert "Структура урока" in page_response.text
    assert "Прогресс" in page_response.text
    assert 'href="styles.css"' in page_response.text
    assert 'src="script.js"' in page_response.text
    assert "DAIR smoke artifact" not in page_response.text
    assert "Draft test page" not in page_response.text
    assert "SKILL.md" not in page_response.text
    assert "course.yaml" not in page_response.text
    assert ".agents/skills" not in page_response.text
    assert "Start Learning" not in page_response.text
    assert "Open review" not in page_response.text
    assert "Source notes" not in page_response.text
    assert "Sources" not in page_response.text
    assert "/tmp/dair_smoke_20260529" not in page_response.text
    assert "file://" not in page_response.text

    styles_response = client.get("/materials/drafts/dair-smoke-20260529/styles.css")
    assert styles_response.status_code == 200
    assert "text/css" in styles_response.headers["content-type"]
    assert ".page-shell" in styles_response.text
    assert ".lesson-nav" in styles_response.text

    script_response = client.get("/materials/drafts/dair-smoke-20260529/script.js")
    assert script_response.status_code == 200
    assert "application/javascript" in script_response.headers["content-type"]
    assert "const courseData" in script_response.text
    assert "lesson-nav" in script_response.text
    assert "flashcards" in script_response.text
    assert "quiz" in script_response.text
    assert "checkpoint-list" in script_response.text
    assert "DAIR smoke artifact" not in script_response.text
    assert "Draft test page" not in script_response.text
    assert "SKILL.md" not in script_response.text
    assert "course.yaml" not in script_response.text
    assert ".agents/skills" not in script_response.text
    assert "Start Learning" not in script_response.text
    assert "Open review" not in script_response.text
    assert "Source notes" not in script_response.text
    assert "Sources" not in script_response.text


def test_materials_and_lesson_redirect_for_anonymous_user(client):
    materials_response = client.get("/materials", follow_redirects=False)
    lesson_response = client.get("/materials/lessons/kak-my-rabotaem-chatgpt-codex-user", follow_redirects=False)

    assert materials_response.status_code == 303
    assert materials_response.headers["location"] == "/login"
    assert lesson_response.status_code == 303
    assert lesson_response.headers["location"] == "/login"
