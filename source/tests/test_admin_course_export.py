from __future__ import annotations

import json
import re
import sqlite3
import zipfile
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path
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


COURSE_DRAFT_ROOT = Path(__file__).resolve().parents[1] / "app" / "materials" / "course_content" / "drafts" / "dair_smoke_20260529"
STATIC_ASSET_REF_RE = re.compile(r'(?P<ref>(?:/static/)?(?:course-assets|images)/[^\s"\'`<>)]+)')


def _course_asset_refs() -> list[str]:
    text = ""
    for name in ["index.html", "styles.css", "script.js"]:
        path = COURSE_DRAFT_ROOT / name
        if path.exists():
            text += "\n" + path.read_text(encoding="utf-8")
    return sorted(
        {
            match.group("ref").removeprefix("/static/")
            for match in STATIC_ASSET_REF_RE.finditer(text)
            if match.group("ref").removeprefix("/static/") and ".." not in match.group("ref").removeprefix("/static/").split("/")
        }
    )


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
        assert manifest["course_subtitle"] == "Как вести разработку через ChatGPT и Codex"
        assert manifest["numbered_lesson_count"] == 9
        assert manifest["has_final_section"] is True
        assert manifest["final_section_id"] == "lesson-10"
        assert manifest["fresh_from_current_source"] is True
        assert manifest["generated_at_utc"].endswith("Z")

        lesson_titles = [lesson["title"] for lesson in manifest["lessons"]]
        assert len(lesson_titles) == 9
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
        }
        expected_names.update(lesson["archive_path"] for lesson in manifest["lessons"])
        expected_asset_paths = {f"assets/static/{ref}" for ref in _course_asset_refs()}
        expected_names.update(expected_asset_paths)
        assert expected_names.issubset(names)

        asset_paths = {item["archive_path"] for item in manifest["assets"]}
        assert asset_paths == expected_asset_paths
        assert len(asset_paths) == 53
        assert sum(1 for path in asset_paths if path.startswith("assets/static/course-assets/")) == 51
        assert sum(1 for path in asset_paths if path.startswith("assets/static/images/")) == 2
        assert sum(1 for path in asset_paths if path.startswith("assets/static/course-assets/dair-smoke-20260529/git-carousel/")) == 6
        assert sum(1 for path in asset_paths if path.startswith("assets/static/course-assets/lesson-5/")) == 10
        assert sum(1 for path in asset_paths if path.startswith("assets/static/course-assets/lesson-6/")) == 17
        assert sum(1 for path in asset_paths if path.startswith("assets/static/course-assets/lesson-7/")) == 7
        assert sum(1 for path in asset_paths if path.startswith("assets/static/course-assets/lesson-8/")) == 11

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
