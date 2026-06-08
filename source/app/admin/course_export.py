"""Admin-only course ZIP export for the current course draft."""

from __future__ import annotations

import io
import json
import re
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


COURSE_DRAFT_ID = "dair_smoke_20260529"
COURSE_DRAFT_ROOT = Path(__file__).resolve().parents[1] / "materials" / "course_content" / "drafts" / COURSE_DRAFT_ID
STATIC_ROOT = Path(__file__).resolve().parents[1] / "static"
INDEX_HTML_PATH = COURSE_DRAFT_ROOT / "index.html"
SCRIPT_JS_PATH = COURSE_DRAFT_ROOT / "script.js"
STYLES_CSS_PATH = COURSE_DRAFT_ROOT / "styles.css"
README_PATH = COURSE_DRAFT_ROOT / "README.md"

LESSON_START_RE = re.compile(r'(?m)^\s*id: "(lesson-\d+)",?$')
TITLE_RE = re.compile(r'^\s*title:\s*"(?P<value>.*?)"', re.M | re.S)
NAV_TITLE_RE = re.compile(r'^\s*navTitle:\s*"(?P<value>.*?)"', re.M | re.S)
COURSE_TITLE_RE = re.compile(r'^\s*title:\s*"(?P<value>.*?)"', re.M | re.S)
COURSE_SUBTITLE_RE = re.compile(r'^\s*courseTitle:\s*"(?P<value>.*?)"', re.M | re.S)
STRING_FIELD_RE_TEMPLATE = r'^\s*{field}:\s*"(?P<value>.*?)"'
TEMPLATE_FIELD_RE_TEMPLATE = r'^\s*{field}:\s*`(?P<value>.*?)`'
PROMPT_FORM_RE = re.compile(
    r'promptForm:\s*{\s*'
    r'id:\s*"(?P<id>[^"]+)"\s*,\s*'
    r'label:\s*"(?P<label>[^"]+)"\s*,\s*'
    r'description:\s*"(?P<description>[^"]+)"\s*,\s*'
    r'actionsLabel:\s*"(?P<actions_label>[^"]+)"\s*,\s*'
    r'filename:\s*"(?P<filename>[^"]+)"\s*,\s*'
    r'markdown:\s*`(?P<markdown>.*?)`\s*',
    re.S,
)
PROMPT_FILENAME_RE = re.compile(r'^\s*starterPromptFilename:\s*"(?P<value>.*?)"', re.M | re.S)
PROMPT_MARKDOWN_RE = re.compile(r'^\s*starterPromptMarkdown:\s*`(?P<value>.*?)`', re.M | re.S)
PROMPT_PLACEMENT_RE = re.compile(r'^\s*starterPromptPlacement:\s*"(?P<value>.*?)"', re.M | re.S)


@dataclass(frozen=True)
class CourseExportPackage:
    filename: str
    content: bytes
    manifest: dict[str, Any]


def _current_utc() -> datetime:
    return datetime.now(timezone.utc)


def _read_text(path: Path) -> str:
    if not path.is_file():
        raise FileNotFoundError(f"Missing course export source file: {path}")
    return path.read_text(encoding="utf-8")


def _extract_string_field(field_name: str, text: str) -> str | None:
    pattern = re.compile(STRING_FIELD_RE_TEMPLATE.format(field=re.escape(field_name)), re.M | re.S)
    match = pattern.search(text)
    if match:
        return match.group("value")
    return None


def _extract_template_field(field_name: str, text: str) -> str | None:
    pattern = re.compile(TEMPLATE_FIELD_RE_TEMPLATE.format(field=re.escape(field_name)), re.M | re.S)
    match = pattern.search(text)
    if match:
        return match.group("value")
    return None


def _extract_string_array(field_name: str, text: str) -> list[str]:
    pattern = re.compile(rf'^\s*{re.escape(field_name)}:\s*\[(?P<body>.*?)\]', re.M | re.S)
    match = pattern.search(text)
    if not match:
        return []
    body = match.group("body")
    return [item for item in re.findall(r'"((?:[^"\\]|\\.)*)"', body, re.S)]


def _extract_lesson_sections(script_text: str) -> list[dict[str, Any]]:
    matches = list(LESSON_START_RE.finditer(script_text))
    sections: list[dict[str, Any]] = []
    for index, match in enumerate(matches):
        start = match.start()
        next_start = matches[index + 1].start() if index + 1 < len(matches) else script_text.find("\nconst state", start)
        if next_start == -1:
            next_start = len(script_text)
        section_text = script_text[start:next_start].rstrip()
        sections.append(
            {
                "id": match.group(1),
                "order": int(match.group(1).split("-", 1)[1]),
                "title": _extract_string_field("title", section_text) or match.group(1),
                "nav_title": _extract_string_field("navTitle", section_text) or _extract_string_field("title", section_text) or match.group(1),
                "section_text": section_text,
            }
        )
    return sections


def _extract_prompt_exports(section_text: str, lesson_id: str) -> list[dict[str, str]]:
    exports: list[dict[str, str]] = []

    filename = _extract_string_field("starterPromptFilename", section_text)
    markdown = _extract_template_field("starterPromptMarkdown", section_text)
    if filename and markdown is not None:
        exports.append(
            {
                "lesson_id": lesson_id,
                "prompt_id": lesson_id,
                "title": markdown.splitlines()[0].lstrip("# ").strip() if markdown.splitlines() else filename,
                "filename": filename,
                "archive_path": f"prompts/{lesson_id}-{filename}",
                "markdown": markdown,
                "source_field": "starterPromptMarkdown",
            }
        )

    for form in PROMPT_FORM_RE.finditer(section_text):
        markdown = form.group("markdown")
        title = markdown.splitlines()[0].lstrip("# ").strip() if markdown.splitlines() else form.group("label")
        exports.append(
            {
                "lesson_id": lesson_id,
                "prompt_id": form.group("id"),
                "title": title,
                "filename": form.group("filename"),
                "archive_path": f"prompts/{lesson_id}-{form.group('filename')}",
                "markdown": markdown,
                "source_field": f'promptForm:{form.group("id")}',
            }
        )

    return exports


def _extract_lesson_filename(order: int, title: str) -> str:
    translit_map = {
        "а": "a",
        "б": "b",
        "в": "v",
        "г": "g",
        "д": "d",
        "е": "e",
        "ё": "e",
        "ж": "zh",
        "з": "z",
        "и": "i",
        "й": "y",
        "к": "k",
        "л": "l",
        "м": "m",
        "н": "n",
        "о": "o",
        "п": "p",
        "р": "r",
        "с": "s",
        "т": "t",
        "у": "u",
        "ф": "f",
        "х": "h",
        "ц": "ts",
        "ч": "ch",
        "ш": "sh",
        "щ": "shch",
        "ъ": "",
        "ы": "y",
        "ь": "",
        "э": "e",
        "ю": "yu",
        "я": "ya",
    }

    slug_parts: list[str] = []
    for char in title.lower():
        if char in translit_map:
            slug_parts.append(translit_map[char])
        elif char.isascii() and char.isalnum():
            slug_parts.append(char)
        else:
            slug_parts.append("-")
    slug = re.sub(r"-+", "-", "".join(slug_parts)).strip("-")
    if not slug:
        slug = "lesson"
    return f"{order:02d}-{slug}.md"


def _build_lesson_markdown(section: dict[str, Any]) -> str:
    section_text = section["section_text"].rstrip()
    nav_title = section["nav_title"]
    title = section["title"]
    order = section["order"]
    markdown_lines = [
        f"# {title}",
        "",
        f"- Lesson id: `{section['id']}`",
        f"- Navigation title: {nav_title}",
        f"- Exported from: `{COURSE_DRAFT_ID}/script.js`",
        "",
        "## Canonical source excerpt",
        "",
        "```js",
        section_text,
        "```",
    ]
    return "\n".join(markdown_lines) + "\n"


def _build_rendered_course_html(index_html: str) -> str:
    rendered = index_html.replace('href="styles.css"', 'href="../source/styles.css"')
    rendered = rendered.replace('src="script.js"', 'src="../source/script.js"')
    rendered = rendered.replace(
        '/static/images/human_ai_hero_background_v2.png',
        '../assets/static/images/human_ai_hero_background_v2.png',
    )
    rendered = rendered.replace(
        '/static/images/mobile_vitruvian_NO_SQUARES_transparent.webp',
        '../assets/static/images/mobile_vitruvian_NO_SQUARES_transparent.webp',
    )
    return rendered


def _build_manifest(
    *,
    generated_at: datetime,
    course_title: str,
    course_subtitle: str,
    lesson_sections: list[dict[str, Any]],
    prompt_exports: list[dict[str, str]],
    source_files: list[dict[str, str]],
    rendered_files: list[dict[str, str]],
    asset_files: list[dict[str, str]],
    archive_filename: str,
) -> dict[str, Any]:
    lessons = []
    final_section = None
    for section in lesson_sections:
        entry = {
            "id": section["id"],
            "order": section["order"],
            "title": section["title"],
            "nav_title": section["nav_title"],
        }
        if section["id"] == "lesson-10":
            final_section = {**entry, "archive_path": "lessons/final.md"}
        else:
            entry["archive_path"] = f"lessons/{_extract_lesson_filename(section['order'], section['title'])}"
            lessons.append(entry)

    prompt_entries = []
    for export in prompt_exports:
        prompt_entries.append(
            {
                "lesson_id": export["lesson_id"],
                "prompt_id": export["prompt_id"],
                "title": export["title"],
                "archive_path": export["archive_path"],
                "source_filename": export["filename"],
                "source_field": export["source_field"],
            }
        )

    return {
        "generated_at_utc": generated_at.isoformat().replace("+00:00", "Z"),
        "source_draft_id": COURSE_DRAFT_ID,
        "course_title": course_title,
        "course_subtitle": course_subtitle,
        "numbered_lesson_count": len(lessons),
        "has_final_section": bool(final_section),
        "final_section_id": "lesson-10" if final_section else None,
        "archive_filename": archive_filename,
        "fresh_from_current_source": True,
        "lessons": lessons,
        "final_section": final_section,
        "prompt_files": prompt_entries,
        "source_files": source_files,
        "rendered_files": rendered_files,
        "assets": asset_files,
    }


def build_course_export(*, generated_at: datetime | None = None) -> CourseExportPackage:
    """Build a fresh ZIP export for the current course draft."""

    generated_at = generated_at or _current_utc()
    index_html = _read_text(INDEX_HTML_PATH)
    script_text = _read_text(SCRIPT_JS_PATH)
    styles_text = _read_text(STYLES_CSS_PATH)
    readme_text = _read_text(README_PATH) if README_PATH.is_file() else None

    lesson_sections = _extract_lesson_sections(script_text)
    prompt_exports: list[dict[str, str]] = []
    for section in lesson_sections:
        prompt_exports.extend(_extract_prompt_exports(section["section_text"], section["id"]))

    archive_filename = f"course-export-{COURSE_DRAFT_ID}-{generated_at.strftime('%Y%m%dT%H%M%SZ')}.zip"
    rendered_html = _build_rendered_course_html(index_html)
    source_files = [
        {
            "source_path": str(INDEX_HTML_PATH),
            "archive_path": "source/index.html",
        },
        {
            "source_path": str(SCRIPT_JS_PATH),
            "archive_path": "source/script.js",
        },
        {
            "source_path": str(STYLES_CSS_PATH),
            "archive_path": "source/styles.css",
        },
    ]
    if readme_text is not None:
        source_files.append(
            {
                "source_path": str(README_PATH),
                "archive_path": "source/README.md",
            }
        )

    rendered_files = [
        {
            "source_path": str(INDEX_HTML_PATH),
            "archive_path": "rendered/course.html",
            "description": "Offline browser snapshot with relative links to source files and assets",
        }
    ]

    asset_source_paths = [
        STATIC_ROOT / "images" / "human_ai_hero_background_v2.png",
        STATIC_ROOT / "images" / "mobile_vitruvian_NO_SQUARES_transparent.webp",
    ]
    asset_files = []
    for path in asset_source_paths:
        if path.is_file():
            asset_files.append(
                {
                    "source_path": str(path),
                    "archive_path": f"assets/{path.relative_to(STATIC_ROOT.parent)}",
                }
            )

    manifest = _build_manifest(
        generated_at=generated_at,
        course_title=_extract_string_field("title", script_text) or "Работа с ИИ",
        course_subtitle=_extract_string_field("courseTitle", script_text) or "",
        lesson_sections=lesson_sections,
        prompt_exports=prompt_exports,
        source_files=source_files,
        rendered_files=rendered_files,
        asset_files=asset_files,
        archive_filename=archive_filename,
    )

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2))
        archive.writestr("rendered/course.html", rendered_html.encode("utf-8"))
        archive.writestr("source/index.html", index_html.encode("utf-8"))
        archive.writestr("source/script.js", script_text.encode("utf-8"))
        archive.writestr("source/styles.css", styles_text.encode("utf-8"))
        if readme_text is not None:
            archive.writestr("source/README.md", readme_text.encode("utf-8"))

        for section in lesson_sections:
            if section["id"] == "lesson-10":
                continue
            archive_path = f"lessons/{_extract_lesson_filename(section['order'], section['title'])}"
            archive.writestr(archive_path, _build_lesson_markdown(section).encode("utf-8"))

        archive.writestr(
            "lessons/final.md",
            _build_lesson_markdown(next(section for section in lesson_sections if section["id"] == "lesson-10")).encode("utf-8"),
        )

        for prompt in prompt_exports:
            archive.writestr(prompt["archive_path"], prompt["markdown"].encode("utf-8"))

        for asset in asset_files:
            source_path = Path(asset["source_path"])
            archive.writestr(asset["archive_path"], source_path.read_bytes())

    return CourseExportPackage(filename=archive_filename, content=buffer.getvalue(), manifest=manifest)
