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
    assert "Личный кабинет будет доступен после оплаты" in cabinet_response.text
    assert "После оплаты тарифа откроются личный кабинет, обучение и материалы." in cabinet_response.text
    assert "data-local-accounts-root" not in cabinet_response.text
    assert "data-prompts-library-root" not in cabinet_response.text
    assert "Промпты" not in cabinet_response.text
    assert "Промпты из курса" not in cabinet_response.text
    assert "Мои промпты" not in cabinet_response.text
    assert "Добавить промпт" not in cabinet_response.text
    assert "Редактировать" not in cabinet_response.text
    assert "Сохранить" not in cabinet_response.text
    assert "Скопировать" not in cabinet_response.text
    assert "Скачать .md" not in cabinet_response.text
    assert "Сбросить к версии курса" not in cabinet_response.text
    assert "Удалить" not in cabinet_response.text
    assert "data-prompts-custom-template" not in cabinet_response.text
    assert 'class="prompt-card prompt-card--custom prompt-card--collapsed"' not in cabinet_response.text
    assert 'data-prompt-custom data-prompt-expanded="false"' not in cabinet_response.text
    assert 'aria-controls="prompt-body-custom"' not in cabinet_response.text
    assert "Файл: custom-prompt.md" not in cabinet_response.text
    assert "openscript:cabinet:prompts-library:v1" not in cabinet_response.text
    assert cabinet_response.text.count('aria-expanded="false"') == 0
    assert cabinet_response.text.count("data-prompt-body") == 0
    assert cabinet_response.text.count("Развернуть") == 0
    assert "Старт проекта с разработки документации" not in cabinet_response.text
    assert "Prompt для создания расширения" not in cabinet_response.text
    assert "Prompt для обновления документов проекта" not in cabinet_response.text
    assert "Prompt для нового диалога по проекту" not in cabinet_response.text
    assert "start_project_documentation_prompt.md" not in cabinet_response.text
    assert "prefix_extension_for_chatgpt_prompt.md" not in cabinet_response.text
    assert "project_docs_update_prompt.md" not in cabinet_response.text
    assert "new_project_dialogue_prompt.md" not in cabinet_response.text
    assert "Ты — ChatGPT, ведущий технический специалист проекта." not in cabinet_response.text
    assert "Сначала ответь только одной фразой:" not in cabinet_response.text
    assert "Опишите свою идею проекта простыми словами" not in cabinet_response.text
    assert "Мне нужно сделать простое browser-расширение для ChatGPT." not in cabinet_response.text
    assert "Сделай расширение для Chrome и Edge." not in cabinet_response.text
    assert "https://chatgpt.com/*" not in cabinet_response.text
    assert "Мне нужно обновить документы проекта после текущего этапа работы." not in cabinet_response.text
    assert "Public docs repo: [ССЫЛКА НА ПУБЛИЧНЫЙ РЕПОЗИТОРИЙ ДОКУМЕНТОВ]" not in cabinet_response.text
    assert "Начни работу по проекту строго по документам проекта." not in cabinet_response.text
    assert "Не продолжай по памяти." not in cabinet_response.text
    assert "Prompt для нового диалога по проекту" not in cabinet_response.text
    assert "Личный кабинет" in cabinet_response.text
