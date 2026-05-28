"""Load course content for the "Работа с ИИ" materials area."""

from __future__ import annotations

from functools import lru_cache
from html import escape
import ast
from pathlib import Path
import re
from typing import Any


COURSE_ROOT = Path(__file__).resolve().parent / "course_content"
COURSE_FILE = COURSE_ROOT / "course.yaml"


class CourseContentError(ValueError):
    """Raised when course content is missing or invalid."""


class LessonNotFoundError(LookupError):
    """Raised when a requested lesson slug does not exist."""


def _resolve_inside_course(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        raise CourseContentError(f"Absolute paths are not allowed: {relative_path}")
    resolved = (COURSE_ROOT / path).resolve()
    try:
        resolved.relative_to(COURSE_ROOT.resolve())
    except ValueError as exc:
        raise CourseContentError(f"Path escapes course_content: {relative_path}") from exc
    return resolved


def _render_inline(text: str) -> str:
    output: list[str] = []
    last_index = 0
    for match in re.finditer(r"`([^`]+)`", text):
        output.append(escape(text[last_index : match.start()]))
        output.append(f"<code>{escape(match.group(1))}</code>")
        last_index = match.end()
    output.append(escape(text[last_index:]))
    return "".join(output)


def _parse_scalar(raw_value: str) -> Any:
    value = raw_value.strip()
    if not value:
        return ""
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        try:
            return ast.literal_eval(value)
        except (SyntaxError, ValueError):
            return value[1:-1]
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    return value


def _parse_course_yaml(text: str) -> dict[str, Any]:
    lines = text.splitlines()
    index = 0
    data: dict[str, Any] = {}

    while index < len(lines):
        raw_line = lines[index]
        line = raw_line.rstrip()
        stripped = line.strip()

        if not stripped or stripped.startswith("#"):
            index += 1
            continue

        match = re.match(r"^([A-Za-z0-9_]+):(?:\s*(.*))?$", stripped)
        if not match:
            raise CourseContentError(f"Unsupported course YAML line: {raw_line}")

        key = match.group(1)
        value = match.group(2) or ""

        if key == "source_tools":
            items: list[Any] = []
            index += 1
            while index < len(lines):
                bullet_raw = lines[index]
                bullet = bullet_raw.strip()
                if not bullet:
                    index += 1
                    continue
                if not bullet.startswith("- "):
                    break
                items.append(_parse_scalar(bullet[2:]))
                index += 1
            data[key] = items
            continue

        if key == "lessons":
            lessons: list[dict[str, Any]] = []
            index += 1
            current: dict[str, Any] | None = None
            while index < len(lines):
                nested_raw = lines[index]
                nested = nested_raw.rstrip()
                nested_stripped = nested.strip()
                if not nested_stripped:
                    index += 1
                    continue
                if nested_stripped.startswith("- "):
                    if current:
                        lessons.append(current)
                    current = {}
                    inline = nested_stripped[2:]
                    if inline:
                        inline_match = re.match(r"^([A-Za-z0-9_]+):\s*(.*)$", inline)
                        if not inline_match:
                            raise CourseContentError(f"Unsupported lesson line: {nested_raw}")
                        current[inline_match.group(1)] = _parse_scalar(inline_match.group(2))
                    index += 1
                    continue
                if current is None:
                    break
                field_match = re.match(r"^\s{4}([A-Za-z0-9_]+):\s*(.*)$", nested_raw)
                if not field_match:
                    break
                current[field_match.group(1)] = _parse_scalar(field_match.group(2))
                index += 1
            if current:
                lessons.append(current)
            data[key] = lessons
            continue

        data[key] = _parse_scalar(value)
        index += 1

    return data


def render_markdown(text: str) -> str:
    """Render a small safe subset of Markdown into HTML."""

    html_parts: list[str] = []
    paragraph: list[str] = []
    code_lines: list[str] = []
    list_mode: str | None = None
    in_code_block = False

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            joined = " ".join(part.strip() for part in paragraph if part.strip())
            if joined:
                html_parts.append(f"<p>{_render_inline(joined)}</p>")
            paragraph = []

    def close_list() -> None:
        nonlocal list_mode
        if list_mode == "ul":
            html_parts.append("</ul>")
        elif list_mode == "ol":
            html_parts.append("</ol>")
        list_mode = None

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()

        if stripped.startswith("```"):
            flush_paragraph()
            close_list()
            if in_code_block:
                html_parts.append(f"<pre><code>{escape(chr(10).join(code_lines))}</code></pre>")
                code_lines = []
                in_code_block = False
            else:
                in_code_block = True
            continue

        if in_code_block:
            code_lines.append(line)
            continue

        if not stripped:
            flush_paragraph()
            close_list()
            continue

        heading_match = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if heading_match:
            flush_paragraph()
            close_list()
            level = len(heading_match.group(1))
            content = _render_inline(heading_match.group(2).strip())
            html_parts.append(f"<h{level}>{content}</h{level}>")
            continue

        unordered_match = re.match(r"^[-*]\s+(.*)$", stripped)
        ordered_match = re.match(r"^\d+\.\s+(.*)$", stripped)
        if unordered_match or ordered_match:
            flush_paragraph()
            desired_mode = "ul" if unordered_match else "ol"
            if list_mode and list_mode != desired_mode:
                close_list()
            if list_mode is None:
                html_parts.append("<ul>" if desired_mode == "ul" else "<ol>")
                list_mode = desired_mode
            item_text = unordered_match.group(1) if unordered_match else ordered_match.group(1)
            html_parts.append(f"<li>{_render_inline(item_text.strip())}</li>")
            continue

        flush_paragraph()
        close_list()
        paragraph.append(stripped)

    flush_paragraph()
    close_list()
    if in_code_block and code_lines:
        html_parts.append(f"<pre><code>{escape(chr(10).join(code_lines))}</code></pre>")

    return "\n".join(html_parts)


@lru_cache(maxsize=1)
def load_course() -> dict[str, Any]:
    if not COURSE_FILE.is_file():
        raise CourseContentError(f"Missing course metadata file: {COURSE_FILE}")

    raw_course = _parse_course_yaml(COURSE_FILE.read_text(encoding="utf-8"))
    lessons: list[dict[str, Any]] = []

    for item in raw_course.get("lessons", []):
        lesson_path = _resolve_inside_course(item["lesson_path"])
        answer_path = _resolve_inside_course(item["answer_path"])
        lesson_text = lesson_path.read_text(encoding="utf-8")
        answer_text = answer_path.read_text(encoding="utf-8")
        lessons.append(
            {
                "id": item["id"],
                "order": item["order"],
                "title": item["title"],
                "slug": item["slug"],
                "status": item["status"],
                "lesson_path": item["lesson_path"],
                "answer_path": item["answer_path"],
                "lesson_file": lesson_path,
                "answer_file": answer_path,
                "content": lesson_text,
                "answer_content": answer_text,
            }
        )

    raw_course["lessons"] = sorted(lessons, key=lambda lesson: lesson["order"])
    raw_course["course_file"] = COURSE_FILE
    return raw_course


def list_lessons() -> list[dict[str, Any]]:
    return list(load_course()["lessons"])


def get_lesson(slug: str) -> dict[str, Any]:
    for lesson in list_lessons():
        if lesson["slug"] == slug:
            return lesson
    raise LessonNotFoundError(f"Lesson not found: {slug}")
