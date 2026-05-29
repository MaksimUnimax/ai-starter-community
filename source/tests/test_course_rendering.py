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


def test_git_backed_course_map_page_is_served_by_the_app(client, test_settings):
    _prepare_verified_user(client, test_settings, "course-map@example.com", "coursemapproof")

    materials_response = client.get("/materials")
    assert materials_response.status_code == 200
    assert "/materials/drafts/dair-smoke-20260529/" in materials_response.text
    assert "Открыть тестовую версию курса" in materials_response.text

    page_response = client.get("/materials/drafts/dair-smoke-20260529/")
    assert page_response.status_code == 200
    assert "Работа с ИИ" in page_response.text
    assert "Как разрабатывать с помощью ChatGPT и Codex" in page_response.text
    assert "Тестовая версия курса" in page_response.text
    assert "Вступление к курсу" in page_response.text
    assert "Что изучаем" in page_response.text
    assert "Зачем это нужно" in page_response.text
    assert "Где это применяется" in page_response.text
    assert "В этом курсе вы изучаете, как вести проектную работу с помощью ChatGPT и Codex без ручного написания кода." in page_response.text
    assert "Пользователю не нужно заранее знать программирование, дизайн, вёрстку, архитектуру, документацию или техническое задание." in page_response.text
    assert "Дальше ChatGPT помогает продумать задачу, подготовить документы, спланировать внешний вид" in page_response.text
    assert "Урок 1" in page_response.text
    assert "Урок 9" in page_response.text
    assert "Проектная работа с ИИ" in page_response.text
    assert "Роли пользователя, ChatGPT и Codex" in page_response.text
    assert "Документы как память проекта" in page_response.text
    assert "Новый диалог после перерыва" in page_response.text
    assert "Обновление документации" in page_response.text
    assert "ТЗ и дорожная карта" in page_response.text
    assert "Git и ключ доступа" in page_response.text
    assert "Один безопасный шаг разработки" in page_response.text
    assert "Отчёт Codex" in page_response.text
    assert "Проектная работа с ИИ: роль пользователя, ChatGPT и Codex" in page_response.text
    assert "Урок показывает первый принцип: простая идея превращается в план, а Codex выполняет конкретную техническую задачу." in page_response.text
    assert "В этом уроке вы увидите, как простая идея пользователя превращается в понятный рабочий шаг для ChatGPT и Codex." in page_response.text
    assert "Ключевые понятия" in page_response.text
    assert "Пользователь — это человек" in page_response.text
    assert "ChatGPT — это ИИ-помощник" in page_response.text
    assert "Codex — это ИИ-агент для программной разработки" in page_response.text
    assert "Как это работает в курсе" in page_response.text
    assert "ChatGPT ведёт техническую работу" in page_response.text
    assert "Codex выполняет задачу на сервере" in page_response.text
    assert "В работе участвуют три роли" not in page_response.text
    assert "Сделай мне сайт" in page_response.text
    assert "Хочу сайт для записи на консультацию" in page_response.text
    assert "Вступление" in page_response.text
    assert "Схема процесса" in page_response.text
    assert "Пользователь ставит цель" in page_response.text
    assert "ChatGPT проектирует технический шаг" in page_response.text
    assert "Codex выполняет задачу на сервере" in page_response.text
    assert "Рабочий пример" in page_response.text
    assert "С чего может начать пользователь" in page_response.text
    assert "Что делает ChatGPT дальше" in page_response.text
    assert "Что делает Codex" in page_response.text
    assert "Что проверяет пользователь" in page_response.text
    assert "Разбор примера" not in page_response.text
    assert "Практика: опишите страницу сайта" not in page_response.text
    assert "<textarea" not in page_response.text
    assert "Типичные ошибки" in page_response.text
    assert "Главный вывод урока" in page_response.text
    assert "Следующий шаг" in page_response.text
    assert "Перейти к уроку 2" in page_response.text
    assert "Структура урока" in page_response.text
    assert "Прогресс по проверке урока" in page_response.text
    assert "Прогресс зависит только от проверки знаний." in page_response.text
    assert "Пока ничего не проверено." in page_response.text
    assert "roadmap" not in page_response.text
    assert "deploy key" not in page_response.text
    assert "scope" not in page_response.text
    assert page_response.text.count('class="nav-button') == 9
    assert page_response.text.count("nav-title") == 9
    assert "lesson-strip" in page_response.text
    assert "lesson-progress" in page_response.text
    assert "lesson-shell" in page_response.text
    assert "definition-stack" in page_response.text
    assert "definition-card" in page_response.text
    assert "process-flow" in page_response.text
    assert "next-step-card" in page_response.text
    assert "Карточки" in page_response.text
    assert 'class="sidebar"' not in page_response.text
    assert 'class="workspace"' not in page_response.text
    assert 'class="hero-meta"' not in page_response.text
    assert 'class="course-map-card"' not in page_response.text
    assert 'class="course-overview"' not in page_response.text
    assert '<textarea' not in page_response.text
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
    assert "Сделай мне ИИ-агента" not in page_response.text
    assert "Опишите своего первого ИИ-агента" not in page_response.text
    assert "ИИ-агент, который помогает начинать новую задачу" not in page_response.text

    styles_response = client.get("/materials/drafts/dair-smoke-20260529/styles.css")
    assert styles_response.status_code == 200
    assert "text/css" in styles_response.headers["content-type"]
    assert ".page-shell" in styles_response.text
    assert ".lesson-nav" in styles_response.text
    assert ".course-intro" in styles_response.text
    assert ".definition-stack" in styles_response.text
    assert ".definition-card" in styles_response.text
    assert ".process-flow" in styles_response.text
    assert ".flashcard-face" in styles_response.text
    assert ".next-step-card" in styles_response.text
    assert "textarea" not in styles_response.text
    assert "checkpoint-list" not in styles_response.text

    script_response = client.get("/materials/drafts/dair-smoke-20260529/script.js")
    assert script_response.status_code == 200
    assert "application/javascript" in script_response.headers["content-type"]
    assert "const courseData" in script_response.text
    assert "lesson-nav" in script_response.text
    assert "flashcards" in script_response.text
    assert "quiz" in script_response.text
    assert "Как разрабатывать с помощью ChatGPT и Codex" in script_response.text
    assert "Проектная работа с ИИ: роль пользователя, ChatGPT и Codex" in script_response.text
    assert "Урок показывает первый принцип: простая идея превращается в план, а Codex выполняет конкретную техническую задачу." in script_response.text
    assert "В этом уроке вы увидите, как простая идея пользователя превращается в понятный рабочий шаг для ChatGPT и Codex." in script_response.text
    assert "Ключевые понятия" in script_response.text
    assert "Пользователь — это человек" in script_response.text
    assert "ChatGPT — это ИИ-помощник" in script_response.text
    assert "Codex — это ИИ-агент для программной разработки" in script_response.text
    assert "Как это работает в курсе" in script_response.text
    assert "ChatGPT ведёт техническую работу" in script_response.text
    assert "Codex выполняет задачу на сервере" in script_response.text
    assert "Сделай мне сайт" in script_response.text
    assert "Хочу сайт для записи на консультацию" in script_response.text
    assert "Вступление" in script_response.text
    assert "Схема процесса" in script_response.text
    assert "Пользователь ставит цель" in script_response.text
    assert "ChatGPT проектирует технический шаг" in script_response.text
    assert "Codex выполняет задачу на сервере" in script_response.text
    assert "В работе участвуют три роли" not in script_response.text
    assert "Рабочий пример" in script_response.text
    assert "Разбор примера" not in script_response.text
    assert "Практика: опишите страницу сайта" not in script_response.text
    assert "<textarea" not in script_response.text
    assert "Типичные ошибки" in script_response.text
    assert "Главный вывод урока" in script_response.text
    assert "Следующий шаг" in script_response.text
    assert "Перейти к уроку 2" in script_response.text
    assert "ТЗ и дорожная карта" in script_response.text
    assert "Git и ключ доступа" in script_response.text
    assert "Как дать Codex право отправлять проект в GitHub" in script_response.text
    assert "roadmap" not in script_response.text
    assert "deploy key" not in script_response.text
    assert "scope" not in script_response.text
    assert "Allow write access" not in script_response.text
    assert "публичный ключ" in script_response.text
    assert "приватный ключ" in script_response.text
    assert "разрешение на запись" in script_response.text
    assert "scrollIntoView" not in script_response.text
    assert "DAIR smoke artifact" not in script_response.text
    assert "Draft test page" not in script_response.text
    assert "SKILL.md" not in script_response.text
    assert "course.yaml" not in script_response.text
    assert ".agents/skills" not in script_response.text
    assert "Start Learning" not in script_response.text
    assert "Open review" not in script_response.text
    assert "Source notes" not in script_response.text
    assert "Sources" not in script_response.text
    assert "<textarea" not in script_response.text
    assert "checkpoint-list" not in script_response.text
    assert "Сделай мне ИИ-агента" not in script_response.text
    assert "Опишите своего первого ИИ-агента" not in script_response.text
    assert "ИИ-агент, который помогает начинать новую задачу" not in script_response.text


def test_materials_and_lesson_redirect_for_anonymous_user(client):
    materials_response = client.get("/materials", follow_redirects=False)
    lesson_response = client.get("/materials/lessons/kak-my-rabotaem-chatgpt-codex-user", follow_redirects=False)

    assert materials_response.status_code == 303
    assert materials_response.headers["location"] == "/login"
    assert lesson_response.status_code == 303
    assert lesson_response.headers["location"] == "/login"
