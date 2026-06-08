from __future__ import annotations

import html
import re
import sqlite3
from pathlib import Path

from app.auth.service import register_user, verify_email
from app.user_cabinet.prompts_library import load_cabinet_prompts


def _verify_registered_user(client, test_settings, email: str, login: str):
    register_user(
        email=email,
        login=login,
        password="Secret123",
        repeat_password="Secret123",
        settings=test_settings,
    )
    outbox = client.get("/check-email?registered=1")
    assert outbox.status_code == 200


def _extract_token_from_db(test_settings, email: str):
    with sqlite3.connect(test_settings.database_path) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT body_text FROM email_outbox WHERE recipient_email = ? AND template_key = ? ORDER BY id DESC LIMIT 1",
            (email, "email_verification"),
        ).fetchone()
    assert row is not None
    match = re.search(r"/verify-email/([A-Za-z0-9_-]+)", row["body_text"])
    assert match
    return match.group(1)


def _extract_built_in_prompt_markdowns(body_text: str) -> dict[str, str]:
    pattern = re.compile(
        r'<article\s+class="prompt-card prompt-card--built-in prompt-card--collapsed"[^>]*data-prompt-id="(?P<id>[^"]+)".*?'
        r'<div class="prompt-card__body"[^>]*hidden[^>]*>.*?'
        r'<textarea class="textarea prompt-textarea" data-prompt-textarea readonly rows="12">(?P<markdown>.*?)</textarea>',
        re.S,
    )
    return {match.group("id"): html.unescape(match.group("markdown")) for match in pattern.finditer(body_text)}


def test_cabinet_prompt_library_renders_course_prompts_and_custom_prompt_template(client, test_settings):
    _verify_registered_user(client, test_settings, "cabinet-prompts@example.com", "cabinetprompts")
    token = _extract_token_from_db(test_settings, "cabinet-prompts@example.com")
    verify_email(token, settings=test_settings)

    login_response = client.post(
        "/login",
        data={"email_or_login": "cabinet-prompts@example.com", "password": "Secret123"},
        follow_redirects=False,
    )
    assert login_response.status_code == 303

    cabinet_response = client.get("/cabinet")
    assert cabinet_response.status_code == 200
    assert cabinet_response.text.index('data-local-accounts-root') < cabinet_response.text.index('data-prompts-library-root')
    assert "Промпты" in cabinet_response.text
    assert "Промпты из курса" in cabinet_response.text
    assert cabinet_response.text.count('class="prompt-card prompt-card--built-in prompt-card--collapsed"') == 4
    assert "Мои промпты" in cabinet_response.text
    assert "Добавить промпт" in cabinet_response.text
    assert "Редактировать" in cabinet_response.text
    assert "Сохранить" in cabinet_response.text
    assert "Скопировать" in cabinet_response.text
    assert "Скачать .md" in cabinet_response.text
    assert "Сбросить к версии курса" in cabinet_response.text
    assert "Удалить" in cabinet_response.text
    assert "data-prompts-custom-template" in cabinet_response.text
    assert 'class="prompt-card prompt-card--custom prompt-card--collapsed"' in cabinet_response.text
    assert 'data-prompt-custom data-prompt-expanded="false"' in cabinet_response.text
    assert 'aria-controls="prompt-body-custom"' in cabinet_response.text
    assert "Файл: custom-prompt.md" in cabinet_response.text
    assert "openscript:cabinet:prompts-library:v1" in client.get("/static/cabinet-prompts-library.js").text
    assert cabinet_response.text.count('aria-expanded="false"') >= 4
    assert cabinet_response.text.count("data-prompt-body") >= 5
    assert cabinet_response.text.count("Развернуть") >= 5

    collapsed_cards = re.findall(
        r'<article\s+class="prompt-card prompt-card--built-in prompt-card--collapsed"[^>]*>.*?</article>',
        cabinet_response.text,
        re.S,
    )
    assert len(collapsed_cards) == 4
    for card_html in collapsed_cards:
        assert 'data-prompt-expanded="false"' in card_html
        assert "prompt-card__filename" in card_html
        assert "data-prompt-body" in card_html
        assert "hidden" in card_html
        assert 'data-prompt-toggle' in card_html
        assert 'aria-expanded="false"' in card_html
        assert "Развернуть" in card_html

    prompts = load_cabinet_prompts()
    assert len(prompts) == 4
    assert [prompt["lesson_number"] for prompt in prompts] == [6, 7, 8, 8]
    assert [prompt["owner_label"] for prompt in prompts] == ["Урок 6", "Урок 7", "Урок 8", "Урок 8"]
    assert [prompt["filename"] for prompt in prompts] == [
        "start_project_documentation_prompt.md",
        "prefix_extension_for_chatgpt_prompt.md",
        "project_docs_update_prompt.md",
        "new_project_dialogue_prompt.md",
    ]
    assert [prompt["id"] for prompt in prompts] == [
        "lesson-6-start-project-documentation-prompt",
        "lesson-7-prefix-extension-for-chatgpt-prompt",
        "lesson-8-project-docs-update-prompt",
        "lesson-8-new-project-dialogue-prompt",
    ]

    expected_source = {
        prompt["id"]: prompt
        for prompt in prompts
    }
    rendered_markdowns = _extract_built_in_prompt_markdowns(cabinet_response.text)
    assert set(rendered_markdowns) == set(expected_source)
    assert "Старт проекта с разработки документации" in cabinet_response.text
    assert "Prompt для создания расширения" in cabinet_response.text
    assert "Prompt для обновления документов проекта" in cabinet_response.text
    assert "Prompt для нового диалога по проекту" in cabinet_response.text
    assert "start_project_documentation_prompt.md" in cabinet_response.text
    assert "prefix_extension_for_chatgpt_prompt.md" in cabinet_response.text
    assert "project_docs_update_prompt.md" in cabinet_response.text
    assert "new_project_dialogue_prompt.md" in cabinet_response.text

    for prompt in prompts:
        rendered = rendered_markdowns[prompt["id"]]
        assert rendered == prompt["markdown"]
        assert prompt["title"] in cabinet_response.text
        assert prompt["owner_label"] in cabinet_response.text
        assert prompt["filename"] in cabinet_response.text

    assert "Ты — ChatGPT, ведущий технический специалист проекта." in cabinet_response.text
    assert "Сначала ответь только одной фразой:" in cabinet_response.text
    assert "Опишите свою идею проекта простыми словами" in cabinet_response.text
    assert "Мне нужно сделать простое browser-расширение для ChatGPT." in cabinet_response.text
    assert "Сделай расширение для Chrome и Edge." in cabinet_response.text
    assert "https://chatgpt.com/*" in cabinet_response.text
    assert "Мне нужно обновить документы проекта после текущего этапа работы." in cabinet_response.text
    assert "Public docs repo: [ССЫЛКА НА ПУБЛИЧНЫЙ РЕПОЗИТОРИЙ ДОКУМЕНТОВ]" in cabinet_response.text
    assert "Prompt для обновления документов проекта" in cabinet_response.text
    assert "Начни работу по проекту строго по документам проекта." in cabinet_response.text
    assert "Не продолжай по памяти." in cabinet_response.text
    assert "Prompt для нового диалога по проекту" in cabinet_response.text

    course_script = Path(
        "/opt/ai-starter-community/source/app/materials/course_content/drafts/dair_smoke_20260529/script.js"
    ).read_text(encoding="utf-8")
    assert "starterPromptMarkdown:" in course_script
    assert 'starterPromptFilename: "start_project_documentation_prompt.md"' in course_script
    assert 'starterPromptLabel: "Prompt для создания расширения"' in course_script
    assert 'label: "Prompt для обновления документов"' in course_script
    assert 'label: "Prompt для нового диалога"' in course_script
    assert 'id: "lesson-8-project-docs-update-prompt"' in course_script
    assert 'id: "lesson-8-new-project-dialogue-prompt"' in course_script
    routes_text = Path("/opt/ai-starter-community/source/app/user_cabinet/routes.py").read_text(encoding="utf-8")
    assert '"/cabinet/prompts"' not in routes_text
    assert "openscript:cabinet:local-accounts:v1" in client.get("/static/cabinet-local-accounts.js").text
    assert "Личный кабинет" in cabinet_response.text
