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


def _prepare_verified_user(
    client,
    test_settings,
    email: str,
    login: str = "lessonuser",
    grant_access: bool = False,
    role: str = "user",
):
    register_user(
        email=email,
        login=login,
        password="Secret123",
        repeat_password="Secret123",
        settings=test_settings,
    )
    token = _extract_token_from_db(test_settings, email)
    verify_email(token, settings=test_settings)
    if role != "user" or grant_access:
        with _connect(test_settings) as conn:
            if role != "user":
                conn.execute("UPDATE users SET role = ? WHERE email = ?", (role, email))
            if grant_access:
                conn.execute(
                    "UPDATE users SET materials_access_granted_at = CURRENT_TIMESTAMP WHERE email = ?",
                    (email,),
                )
            conn.commit()
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
    _prepare_verified_user(client, test_settings, "course-render@example.com", "courserender", grant_access=True)

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
    _prepare_verified_user(client, test_settings, "course-map@example.com", "coursemapproof", grant_access=True)

    materials_response = client.get("/materials")
    assert materials_response.status_code == 200
    assert "/materials/drafts/dair-smoke-20260529/" in materials_response.text
    assert "Открыть карту курса" in materials_response.text

    page_response = client.get("/materials/drafts/dair-smoke-20260529/")
    styles_response = client.get("/materials/drafts/dair-smoke-20260529/styles.css")
    script_response = client.get("/materials/drafts/dair-smoke-20260529/script.js")

    assert page_response.status_code == 200
    assert "Работа с ИИ" in page_response.text
    assert "Как разрабатывать с помощью ChatGPT и Codex" in page_response.text
    assert page_response.text.count('class="course-head hero"') == 1
    assert "/static/images/human_ai_hero_background_v2.png" in page_response.text
    assert "/static/images/mobile_vitruvian_NO_SQUARES_transparent.webp" in page_response.text
    assert "hero-bg-desktop" in page_response.text
    assert "hero-bg-mobile" in page_response.text
    assert "На главную" in page_response.text
    assert "Тестовая версия курса" not in page_response.text
    assert "тестовая версия урока" not in page_response.text
    assert "Курс показывает, как вести проектную работу с ИИ без ручного написания кода: от простой идеи до проверенного результата." in page_response.text
    assert "Вступление к курсу" in page_response.text
    assert "Что изучаем" in page_response.text
    assert "Зачем это нужно" in page_response.text
    assert "Где это применяется" in page_response.text
    assert page_response.text.count("course-intro-part") == 3
    assert page_response.text.count('class="nav-button') == 9
    assert page_response.text.count("nav-title") == 9
    assert "Codex, AGENTS.md, Skills, токены и роль модели" in page_response.text
    assert "PowerShell, Terminal и подключение к серверу" in page_response.text
    assert "Сервер, Codex, AGENTS.md и Skills" not in page_response.text
    assert page_response.text.count("Вернуться в личный кабинет") == 2
    assert page_response.text.count('href="/cabinet"') == 2
    assert "Прогресс зависит от прохождения проверки знаний." in page_response.text
    assert "Пока ничего не проверено." in page_response.text
    assert styles_response.status_code == 200
    assert "text/css" in styles_response.headers["content-type"]
    assert ".page-shell" in styles_response.text
    assert ".course-head {" in styles_response.text
    assert "text-align: center;" in styles_response.text
    assert ".lesson-nav" in styles_response.text
    assert ".course-intro" in styles_response.text
    assert ".course-intro-body" in styles_response.text
    assert ".course-intro-part" in styles_response.text
    assert ".course-intro .section-heading" in styles_response.text
    assert "text-align: center;" in styles_response.text
    assert "line-height: 1.45;" in styles_response.text
    assert ".course-note {" in styles_response.text
    assert "color: var(--accent-strong);" in styles_response.text
    assert "@media (max-width: 680px)" in styles_response.text
    assert ".hero-bg-mobile {\n    display: none;" in styles_response.text
    assert ".hero-bg-desktop {\n    display: none;" in styles_response.text
    assert ".definition-stack" in styles_response.text
    assert ".definition-card" in styles_response.text
    assert ".process-flow" in styles_response.text
    assert "linear-gradient(180deg, #fff 0%, #fff6ec 100%)" not in styles_response.text
    assert ".flashcard.is-revealed" in styles_response.text
    assert ".flashcard-title" in styles_response.text
    assert ".next-step-card" in styles_response.text
    assert "textarea" not in styles_response.text
    assert "checkpoint-list" not in styles_response.text
    assert script_response.status_code == 200
    assert "application/javascript" in script_response.headers["content-type"]
    assert "const courseData" in script_response.text
    assert "lesson-nav" in script_response.text
    assert "flashcards" in script_response.text
    assert "getLessonIdFromUrl" in script_response.text
    assert "syncLessonQueryParam" in script_response.text
    assert "new URLSearchParams(window.location.search).get(\"lesson\")" in script_response.text
    assert "window.history.replaceState" in script_response.text
    assert "location.hash" not in script_response.text
    assert "scrollIntoView" in script_response.text
    assert "labelTranslations" not in script_response.text
    assert "translateLessonMarkup" not in script_response.text
    assert "translateLabel" not in script_response.text
    assert "Проверка знаний" in script_response.text
    assert "getSectionQuestionCount" in script_response.text
    assert "getSectionAnsweredCount" in script_response.text
    assert "getSectionQuiz(section, quizIndex)" in script_response.text
    assert 'state.answeredQuestions[quizKey(section.id, index)] !== undefined' in script_response.text
    assert "renderStructuredLesson" in script_response.text
    assert 'section.nextStepTargetId || "lesson-2"' in script_response.text
    assert 'id: "lesson-9"' in script_response.text
    assert 'review: "lesson-9"' in script_response.text
    assert 'navTitle: "Урок 9 — Частые ошибки и правила безопасной работы"' in script_response.text
    assert "lesson-" + "10" not in script_response.text
    assert "Документы проекта: техническое задание (ТЗ), roadmap, правила и контекст" in script_response.text
    assert "Старт проекта: сначала документация, потом разработка" in script_response.text
    assert "ChatGPT выступает как ведущий специалист" in script_response.text
    assert "Git: история, commit, push и откат" in script_response.text
    assert "Старт работы и рабочие run’ы Codex" in script_response.text
    assert "Codex, AGENTS.md, Skills, токены и роль модели" in script_response.text
    assert "PowerShell, Terminal и подключение к серверу" in script_response.text
    assert 'navTitle: "Урок 4 — Codex, AGENTS.md, Skills, токены и роль модели"' in script_response.text
    assert 'navTitle: "Урок 5 — PowerShell, Terminal и подключение к серверу"' in script_response.text
    assert 'navTitle: "Урок 6 — Старт проекта: сначала документация, потом разработка"' in script_response.text
    assert "В нашем методе работы" in script_response.text
    assert "Как Codex тратит токены и ресурсы" in script_response.text
    assert "Как оптимизировать расход Codex" in script_response.text
    assert "Что такое permissions и как выставить допуск" in script_response.text
    assert "5 основных команд Codex внутри terminal" in script_response.text
    assert "Что такое токены в работе Codex?" in script_response.text
    assert "Токены — это единицы ресурса" in script_response.text
    assert "5-часовые лимиты" in script_response.text
    assert "Недельные лимиты" in script_response.text
    assert "/status" in script_response.text
    assert "/model" in script_response.text
    assert "/permissions" in script_response.text
    assert "/skills" in script_response.text
    assert "/plugins" in script_response.text
    assert "token usage" in script_response.text
    assert "Где работает Codex" not in script_response.text
    assert "Пример правильной задачи для Codex" not in script_response.text
    assert "Codex settings → Usage" not in script_response.text
    assert "codex -C" not in script_response.text
    assert "искать лимиты через" not in script_response.text
    assert "принимать результат без отчёта" not in script_response.text
    lesson3_start = script_response.text.index('id: "lesson-3"')
    lesson4_start = script_response.text.index('id: "lesson-4"')
    lesson5_start = script_response.text.index('id: "lesson-5"')
    lesson6_start = script_response.text.index('id: "lesson-6"')
    lesson7_start = script_response.text.index('id: "lesson-7"')
    assert lesson4_start < lesson5_start < lesson6_start < lesson7_start
    lesson3_section = script_response.text[lesson3_start:lesson4_start]
    lesson4_section = script_response.text[lesson4_start:lesson5_start]
    lesson5_section = script_response.text[lesson5_start:lesson6_start]
    lesson6_section = script_response.text[lesson6_start:lesson7_start]
    assert "В следующем уроке разберём Codex, AGENTS.md, Skills, токены и роль модели." in lesson3_section
    assert "Перейти к уроку 4" in lesson3_section
    assert "В следующем уроке разберём PowerShell, Terminal и подключение к серверу." in lesson4_section
    assert "Перейти к уроку 5" in lesson4_section
    assert "В следующем уроке разберём старт проекта: сначала документация, потом разработка." in lesson5_section
    assert "Перейти к уроку 6" in lesson5_section
    assert "В следующем уроке разберём старт работы и рабочие run’ы Codex." in lesson6_section
    assert "Перейти к уроку 7" in lesson6_section
    lesson4_agents_index = lesson4_section.index('label: "AGENTS.md"')
    lesson4_skills_index = lesson4_section.index('label: "Skills"')
    lesson4_errors_index = lesson4_section.index('label: "Частые ошибки"')
    assert lesson4_agents_index < lesson4_skills_index < lesson4_errors_index
    assert "Какую модель выбирать для Codex" in script_response.text
    assert "Частые ошибки и правила безопасной работы" in script_response.text
    assert "Обновление документации и новый диалог" in script_response.text
    assert "Зарегистрировать аккаунт GitHub" in script_response.text
    assert "Что нельзя делать" not in lesson3_section
    assert "Вступление" in script_response.text
    assert "После урока вы сможете" in script_response.text
    assert "Почему проект находится на удалённом сервере" in lesson5_section
    assert "Сервер может работать 24/7" in lesson5_section
    assert "К проекту можно позже дать доступ другим людям" in lesson5_section
    assert "На сервере можно подготовить правильное окружение" in lesson5_section
    assert "Codex живёт и работает там же" in lesson5_section
    assert "Как открыть PowerShell на Windows" in lesson5_section
    assert "Как открыть Terminal на macOS" in lesson5_section
    assert "SSH-команду" in lesson5_section
    assert "личного кабинета" in lesson5_section
    assert "окно связи с сервером" in lesson5_section
    assert "codex" in lesson5_section
    assert "привет ты кто?" in lesson5_section
    assert "Практическое задание" in lesson5_section
    assert "Что важно для ученика" not in lesson5_section
    assert "Безопасные команды" not in lesson5_section
    assert "Опасные команды" not in lesson5_section
    assert "Что нельзя показывать в чат" not in lesson5_section
    assert "Секреты" not in lesson5_section
    assert "Ученик" not in lesson5_section
    assert "Главный вывод урока" in script_response.text
    assert "Следующий урок" in script_response.text
    assert "Тестовая версия курса" not in script_response.text
    assert "тестовая версия урока" not in script_response.text
    assert "DAIR smoke artifact" not in script_response.text
    assert "Draft test page" not in script_response.text
    assert "SKILL.md" not in script_response.text
    assert "course.yaml" not in script_response.text
    assert ".agents/skills" not in script_response.text
    assert "Start Learning" not in script_response.text
    assert "Open review" not in script_response.text
    assert "Source notes" not in script_response.text
    assert "Sources" not in script_response.text
    assert "<textarea" in script_response.text
    assert "checkpoint-list" not in script_response.text
    assert "Сделай мне ИИ-агента" not in script_response.text
    assert "Опишите своего первого ИИ-агента" not in script_response.text
    assert "ИИ-агент, который помогает начинать новую задачу" not in script_response.text
    assert "Кто что делает: пользователь, ChatGPT и Codex" not in script_response.text
    assert "Почему проект начинается с документов" not in script_response.text
    assert "Как начинать новый диалог после перерыва" not in script_response.text
    assert "Как обновляется документация во время работы" not in script_response.text
    assert "Зачем нужны ТЗ и дорожная карта" not in script_response.text
    assert "Как идёт один безопасный шаг разработки" not in script_response.text
    assert "Что значит отчёт Codex" not in script_response.text
    assert "Сервер, Codex, AGENTS.md и Skills" not in script_response.text
    assert "Codex, AGENTS.md и Skills" not in script_response.text
    assert script_response.text.count("Зарегистрировать аккаунт GitHub") >= 2
    assert "Смотреть prompt" in script_response.text
    assert "Скопировать prompt" in script_response.text
    assert "Скачать .md" in script_response.text
    lesson3_task_start = lesson3_section.index('label: "Практическое задание"')
    lesson3_task_end = lesson3_section.index('label: "Итог"', lesson3_task_start)
    lesson3_task_section = lesson3_section[lesson3_task_start:lesson3_task_end]
    assert "Зарегистрировать аккаунт GitHub" in lesson3_task_section
    assert "https://github.com/" in lesson3_task_section
    assert "https://github.com/signup" in lesson3_task_section
    assert "https://github.com/login" in lesson3_task_section
    assert "К концу урока у ученика должен быть зарегистрированный и авторизованный аккаунт GitHub" in lesson3_task_section
    assert "подтвердите email" in lesson3_task_section.lower()
    assert "Что нельзя делать" not in lesson3_task_section
    assert "не отправляйте пароль в чат" not in lesson3_task_section
    assert "не отправляйте коды подтверждения в чат" not in lesson3_task_section
    assert "не используйте чужой аккаунт" not in lesson3_task_section
    lesson6_prompt_start = lesson6_section.index('label: "Готовый prompt"')
    lesson6_practice_start = lesson6_section.index("afterStarterPromptHtml")
    assert lesson6_prompt_start < lesson6_practice_start
    assert "Запустить старт проекта через ChatGPT" in lesson6_section
    assert "В этой практике вы не пишете код и не проверяете <strong>GitHub</strong> как технический специалист." in lesson6_section
    assert "Ваша задача — запустить проект правильно: дать <strong>ChatGPT</strong> стартовый <strong>prompt</strong>, отвечать простыми словами и довести проект до состояния, когда <strong>ChatGPT</strong> скажет, что основа готова для первого рабочего <strong>run Codex</strong>." in lesson6_section
    assert "<strong>Что нужно сделать</strong>" in lesson6_section
    assert "<strong>Важно</strong>" in lesson6_section
    assert "Опишите вашу идею или проект." in lesson6_section
    assert "Вам не нужно заранее знать технические ответы." in lesson6_section
    assert "не знаю" in lesson6_section
    assert "объясни простыми словами" in lesson6_section
    assert "предложи лучший вариант для моего проекта" in lesson6_section
    assert "<strong>Какие вопросы может задавать ChatGPT</strong>" in lesson6_section
    assert "<strong>Что делает ChatGPT на этом этапе</strong>" in lesson6_section
    assert "<strong>Что делает Codex на этом этапе</strong>" in lesson6_section
    assert "<strong>Что делает ChatGPT после отчёта Codex</strong>" in lesson6_section
    assert "<strong>ChatGPT</strong> читает отчёт <strong>Codex</strong>, проверяет <strong>GitHub</strong>, <strong>commit</strong>, <strong>push</strong>, изменённые файлы и документацию, а потом объясняет вам простыми словами:" in lesson6_section
    assert "Вам не нужно самостоятельно разбирать <strong>commit</strong>, <strong>push</strong> и отчёт как программисту." in lesson6_section
    assert "Практика завершена не тогда, когда <strong>prompt</strong> просто вставлен в чат." in lesson6_section
    assert "Практика завершена тогда, когда <strong>ChatGPT</strong> подтвердил, что основа проекта готова." in lesson6_section
    assert "<strong>Критерий готовности</strong>" in lesson6_section
    assert "проектная основа создана, приложение и документация находятся в GitHub" in lesson6_section
    assert "Скопировать prompt" in lesson6_section
    assert "SSH deploy key" not in lesson6_section
    assert "deploy key" not in lesson6_section
    assert "Когда практика стартового проекта считается завершённой?" in lesson6_section


def test_git_backed_course_map_page_requires_learning_access(client, test_settings):
    anon_page = client.get("/materials/drafts/dair-smoke-20260529/", follow_redirects=False)
    anon_styles = client.get("/materials/drafts/dair-smoke-20260529/styles.css", follow_redirects=False)
    anon_script = client.get("/materials/drafts/dair-smoke-20260529/script.js", follow_redirects=False)

    assert anon_page.status_code == 303
    assert anon_page.headers["location"] == "/login"
    assert anon_styles.status_code == 303
    assert anon_styles.headers["location"] == "/login"
    assert anon_script.status_code == 303
    assert anon_script.headers["location"] == "/login"

    _prepare_verified_user(client, test_settings, "course-lock@example.com", "courselock")

    locked_page = client.get("/materials/drafts/dair-smoke-20260529/", follow_redirects=False)
    locked_styles = client.get("/materials/drafts/dair-smoke-20260529/styles.css", follow_redirects=False)
    locked_script = client.get("/materials/drafts/dair-smoke-20260529/script.js", follow_redirects=False)

    assert locked_page.status_code == 403
    assert locked_styles.status_code == 403
    assert locked_script.status_code == 403

    with _connect(test_settings) as conn:
        conn.execute(
            "UPDATE users SET materials_access_granted_at = CURRENT_TIMESTAMP WHERE email = ?",
            ("course-lock@example.com",),
        )
        conn.commit()

    authorized_page = client.get("/materials/drafts/dair-smoke-20260529/")
    authorized_styles = client.get("/materials/drafts/dair-smoke-20260529/styles.css")
    authorized_script = client.get("/materials/drafts/dair-smoke-20260529/script.js")

    assert authorized_page.status_code == 200
    assert authorized_styles.status_code == 200
    assert authorized_script.status_code == 200
    assert "Работа с ИИ" in authorized_page.text
    assert "application/javascript" in authorized_script.headers["content-type"]

    client.cookies.clear()
    _prepare_verified_user(client, test_settings, "course-admin@example.com", "courseadmin", role="admin")
    admin_page = client.get("/materials/drafts/dair-smoke-20260529/")
    admin_styles = client.get("/materials/drafts/dair-smoke-20260529/styles.css")
    admin_script = client.get("/materials/drafts/dair-smoke-20260529/script.js")

    assert admin_page.status_code == 200
    assert admin_styles.status_code == 200
    assert admin_script.status_code == 200


def test_materials_and_lesson_redirect_for_anonymous_user(client):
    materials_response = client.get("/materials", follow_redirects=False)
    lesson_response = client.get("/materials/lessons/kak-my-rabotaem-chatgpt-codex-user", follow_redirects=False)

    assert materials_response.status_code == 303
    assert materials_response.headers["location"] == "/login"
    assert lesson_response.status_code == 303
    assert lesson_response.headers["location"] == "/login"
