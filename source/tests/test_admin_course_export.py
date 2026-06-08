from __future__ import annotations

import json
import re
import sqlite3
import zipfile
from datetime import datetime, timezone
from io import BytesIO
from urllib.parse import unquote

from app.admin import course_export
from app.auth.service import authenticate_user, create_session, register_user, verify_email
from app.shared.db import get_database_path


def _connect(settings):
    conn = sqlite3.connect(str(get_database_path(settings)))
    conn.row_factory = sqlite3.Row
    return conn


def _extract_verify_token(settings, email: str) -> str:
    with _connect(settings) as conn:
        row = conn.execute(
            "SELECT body_text FROM email_outbox WHERE recipient_email = ? AND template_key = ? ORDER BY id DESC LIMIT 1",
            (email, "email_verification"),
        ).fetchone()
    assert row is not None
    match = re.search(r"/verify-email/([A-Za-z0-9_-]+)", row["body_text"])
    assert match
    return match.group(1)


def _make_user(client, test_settings, email: str, login: str, role: str = "user") -> None:
    register_user(
        email=email,
        login=login,
        password="Secret123",
        repeat_password="Secret123",
        settings=test_settings,
    )
    token = _extract_verify_token(test_settings, email)
    verify_email(token, settings=test_settings)
    with _connect(test_settings) as conn:
        conn.execute("UPDATE users SET role = ? WHERE email = ?", (role, email))
        conn.commit()
    user = authenticate_user(email, "Secret123", settings=test_settings)
    session_token = create_session(user.id, settings=test_settings)
    client.cookies.set(test_settings.session_cookie_name, session_token)


def _open_zip(response):
    return zipfile.ZipFile(BytesIO(response.content))


def test_admin_course_export_button_is_visible_on_dashboard(client, test_settings):
    _make_user(client, test_settings, "export-admin@example.com", "exportadmin", role="admin")
    response = client.get("/admin")
    assert response.status_code == 200
    assert "Скачать курс архивом" in response.text
    assert 'href="/admin/course-export"' in response.text


def test_admin_course_export_redirects_anonymous_to_login(client):
    response = client.get("/admin/course-export", follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/login"


def test_admin_course_export_forbids_non_admin_users(client, test_settings):
    _make_user(client, test_settings, "export-user@example.com", "exportuser", role="user")
    response = client.get("/admin/course-export")
    assert response.status_code == 403
    assert "Доступ запрещён" in response.text
    assert "прав администратора" in response.text


def test_admin_course_export_returns_fresh_zip_attachment_and_manifest(client, test_settings):
    _make_user(client, test_settings, "export-admin-zip@example.com", "exportadminzip", role="admin")

    response = client.get("/admin/course-export")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/zip")
    disposition = response.headers.get("content-disposition", "")
    assert "attachment" in disposition.lower()
    assert re.search(r"course-export-dair_smoke_20260529-\d{8}T\d{6}Z\.zip", unquote(disposition))

    with _open_zip(response) as archive:
        names = set(archive.namelist())
        manifest = json.loads(archive.read("manifest.json").decode("utf-8"))
        assert manifest["source_draft_id"] == "dair_smoke_20260529"
        assert manifest["course_title"] == "Работа с ИИ"
        assert manifest["course_subtitle"] == "Как вести разработку через ChatGPT и Codex"
        assert manifest["numbered_lesson_count"] == 9
        assert manifest["has_final_section"] is True
        assert manifest["final_section_id"] == "lesson-10"
        assert manifest["fresh_from_current_source"] is True
        assert manifest["generated_at_utc"].endswith("Z")

        lesson_titles = [lesson["title"] for lesson in manifest["lessons"]]
        assert len(lesson_titles) == 9
        assert lesson_titles[3] == "Codex, AGENTS.md, Skills, токены и роль модели"
        assert lesson_titles[4] == "PowerShell, Terminal и подключение к серверу"
        assert lesson_titles[5] == "Старт проекта: сначала документация, потом разработка"
        assert lesson_titles[6] == "Процесс работы"
        assert manifest["final_section"]["archive_path"] == "lessons/final.md"
        assert manifest["final_section"]["id"] == "lesson-10"
        assert manifest["final_section"]["title"] == "Поздравляем, вы завершили курс"

        expected_names = {
            "manifest.json",
            "rendered/course.html",
            "source/index.html",
            "source/script.js",
            "source/styles.css",
            "source/README.md",
            "lessons/final.md",
            "prompts/lesson-6-start_project_documentation_prompt.md",
            "prompts/lesson-7-prefix_extension_for_chatgpt_prompt.md",
            "prompts/lesson-8-project_docs_update_prompt.md",
            "prompts/lesson-8-new_project_dialogue_prompt.md",
            "assets/static/images/human_ai_hero_background_v2.png",
            "assets/static/images/mobile_vitruvian_NO_SQUARES_transparent.webp",
        }
        expected_names.update(lesson["archive_path"] for lesson in manifest["lessons"])
        assert expected_names.issubset(names)

        prompt_paths = {item["archive_path"] for item in manifest["prompt_files"]}
        assert prompt_paths == {
            "prompts/lesson-6-start_project_documentation_prompt.md",
            "prompts/lesson-7-prefix_extension_for_chatgpt_prompt.md",
            "prompts/lesson-8-project_docs_update_prompt.md",
            "prompts/lesson-8-new_project_dialogue_prompt.md",
        }

        asset_paths = {item["archive_path"] for item in manifest["assets"]}
        assert asset_paths == {
            "assets/static/images/human_ai_hero_background_v2.png",
            "assets/static/images/mobile_vitruvian_NO_SQUARES_transparent.webp",
        }

        source_paths = {item["archive_path"] for item in manifest["source_files"]}
        assert source_paths == {
            "source/index.html",
            "source/script.js",
            "source/styles.css",
            "source/README.md",
        }
        rendered_paths = {item["archive_path"] for item in manifest["rendered_files"]}
        assert rendered_paths == {"rendered/course.html"}

        rendered_html = archive.read("rendered/course.html").decode("utf-8")
        assert '../source/styles.css' in rendered_html
        assert '../source/script.js' in rendered_html
        assert '../assets/static/images/human_ai_hero_background_v2.png' in rendered_html
        assert '../assets/static/images/mobile_vitruvian_NO_SQUARES_transparent.webp' in rendered_html

        lesson4_text = archive.read("lessons/04-codex-agents-md-skills-tokeny-i-rol-modeli.md").decode("utf-8")
        assert "# Codex, AGENTS.md, Skills, токены и роль модели" in lesson4_text
        assert "Canonical source excerpt" in lesson4_text
        assert "navTitle: \"Урок 4 — Codex, AGENTS.md, Skills, токены и роль модели\"" in lesson4_text

        lesson7_text = archive.read("lessons/07-protsess-raboty.md").decode("utf-8")
        assert "# Процесс работы" in lesson7_text
        assert "starterPromptPlacement: \"block\"" in lesson7_text
        assert "контекстное окно" in lesson7_text
        assert "prefix-расширение" in lesson7_text

        prompt6 = archive.read("prompts/lesson-6-start_project_documentation_prompt.md").decode("utf-8")
        assert prompt6.startswith("# Старт проекта с разработки документации")
        assert "technical_spec.md" in prompt6
        prompt7 = archive.read("prompts/lesson-7-prefix_extension_for_chatgpt_prompt.md").decode("utf-8")
        assert prompt7.startswith("# Prompt для создания расширения")
        assert "manifest.json" in prompt7
        prompt8 = archive.read("prompts/lesson-8-project_docs_update_prompt.md").decode("utf-8")
        assert prompt8.startswith("# Prompt для обновления документов проекта")
        prompt9 = archive.read("prompts/lesson-8-new_project_dialogue_prompt.md").decode("utf-8")
        assert prompt9.startswith("# Prompt для нового диалога по проекту")


def test_course_export_is_fresh_per_request(monkeypatch):
    first = datetime(2026, 6, 8, 12, 0, 0, tzinfo=timezone.utc)
    second = datetime(2026, 6, 8, 12, 0, 1, tzinfo=timezone.utc)
    times = iter([first, second])
    monkeypatch.setattr(course_export, "_current_utc", lambda: next(times))

    export_one = course_export.build_course_export()
    export_two = course_export.build_course_export()

    assert export_one.filename != export_two.filename
    assert export_one.manifest["generated_at_utc"] == "2026-06-08T12:00:00Z"
    assert export_two.manifest["generated_at_utc"] == "2026-06-08T12:00:01Z"
    assert export_one.manifest["fresh_from_current_source"] is True
    assert export_two.manifest["fresh_from_current_source"] is True
