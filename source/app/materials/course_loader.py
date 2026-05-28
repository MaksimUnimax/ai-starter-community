"""Load course content for the "Работа с ИИ" materials area."""

from __future__ import annotations

import ast
from functools import lru_cache
from html import escape
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


def _render_plain_markdown(text: str) -> str:
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


def _collect_interactive_block(lines: list[str], start_index: int) -> tuple[str, list[str], int]:
    block_type = lines[start_index].strip()[3:].strip()
    block_lines: list[str] = []
    index = start_index + 1
    while index < len(lines):
        stripped = lines[index].strip()
        if stripped == ":::":  # end of block
            return block_type, block_lines, index
        block_lines.append(lines[index])
        index += 1
    raise CourseContentError(f"Unterminated interactive block: {block_type}")


def _render_check_block(block_lines: list[str]) -> str:
    question_parts: list[str] = []
    answer_parts: list[str] = []
    section = "question"

    for raw_line in block_lines:
        stripped = raw_line.strip()
        if not stripped:
            continue
        if stripped.startswith("question:"):
            section = "question"
            rest = stripped[len("question:") :].strip()
            if rest:
                question_parts.append(rest)
            continue
        if stripped.startswith("answer:"):
            section = "answer"
            rest = stripped[len("answer:") :].strip()
            if rest:
                answer_parts.append(rest)
            continue
        if section == "answer":
            answer_parts.append(stripped)
        else:
            question_parts.append(stripped)

    question = " ".join(question_parts).strip()
    answer = " ".join(answer_parts).strip()
    return (
        '<details class="lesson-check">'
        '<summary>Показать ответ</summary>'
        f'<p><strong>Вопрос:</strong> {_render_inline(question)}</p>'
        f'<p><strong>Ответ:</strong> {_render_inline(answer)}</p>'
        "</details>"
    )


def _render_task_block(block_lines: list[str]) -> str:
    title = "Практическое задание"
    input_lines: list[str] = []
    question_items: list[str] = []
    answer_ref = ""
    section: str | None = None

    for raw_line in block_lines:
        stripped = raw_line.strip()
        if not stripped:
            if section == "input":
                input_lines.append("")
            continue
        if stripped.startswith("title:"):
            title = stripped[len("title:") :].strip() or title
            section = None
            continue
        if stripped.startswith("input:"):
            section = "input"
            continue
        if stripped.startswith("questions:"):
            section = "questions"
            continue
        if stripped.startswith("answer_ref:"):
            answer_ref = stripped[len("answer_ref:") :].strip()
            section = None
            continue
        if section == "input":
            input_lines.append(raw_line)
        elif section == "questions" and stripped.startswith(("- ", "* ")):
            question_items.append(stripped[2:].strip())
        else:
            input_lines.append(raw_line)

    input_html = _render_plain_markdown("\n".join(input_lines).strip()) if input_lines else ""
    question_html = "".join(f"<li>{_render_inline(item)}</li>" for item in question_items)
    answer_link = ""
    if answer_ref:
        answer_link = (
            '<p class="form-help">'
            f'Ответ смотри здесь: <a href="{escape(answer_ref, quote=True)}">{escape(answer_ref)}</a>'
            "</p>"
        )

    parts = [
        '<section class="lesson-task card stack">',
        f"<h3>{escape(title)}</h3>",
    ]
    if input_html:
        parts.append('<div class="lesson-task-input stack">')
        parts.append("<p class=\"muted\">Входные данные</p>")
        parts.append(input_html)
        parts.append("</div>")
    if question_html:
        parts.append('<div class="lesson-task-questions stack">')
        parts.append("<p class=\"muted\">Что нужно найти</p>")
        parts.append(f"<ul>{question_html}</ul>")
        parts.append("</div>")
    if answer_link:
        parts.append(answer_link)
    parts.append("</section>")
    return "\n".join(parts)


def _render_checklist_block(block_lines: list[str]) -> str:
    items: list[str] = []
    for raw_line in block_lines:
        stripped = raw_line.strip()
        if not stripped:
            continue
        match = re.match(r"^[-*]\s+\[( |x|X)\]\s+(.*)$", stripped)
        if match:
            checked = match.group(1).lower() == "x"
            label = match.group(2).strip()
            checkbox = '<input type="checkbox" disabled checked>' if checked else '<input type="checkbox" disabled>'
            items.append(f"<li>{checkbox} {_render_inline(label)}</li>")
        else:
            items.append(f"<li>{_render_inline(stripped)}</li>")
    return f'<ul class="lesson-checklist">{"" .join(items)}</ul>'


def _render_interactive_block(block_type: str, block_lines: list[str]) -> str:
    normalized = block_type.lower()
    if normalized == "check":
        return _render_check_block(block_lines)
    if normalized == "task":
        return _render_task_block(block_lines)
    if normalized == "checklist":
        return _render_checklist_block(block_lines)
    return _render_plain_markdown("\n".join(block_lines))


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
    """Render a safe subset of Markdown and custom interactive blocks into HTML."""

    lines = text.splitlines()
    html_parts: list[str] = []
    plain_buffer: list[str] = []
    index = 0

    def flush_plain() -> None:
        if plain_buffer:
            rendered = _render_plain_markdown("\n".join(plain_buffer))
            if rendered:
                html_parts.append(rendered)
            plain_buffer.clear()

    while index < len(lines):
        stripped = lines[index].strip()
        if stripped.startswith(":::") and stripped != ":::":
            flush_plain()
            block_type, block_lines, end_index = _collect_interactive_block(lines, index)
            html_parts.append(_render_interactive_block(block_type, block_lines))
            index = end_index + 1
            continue
        plain_buffer.append(lines[index])
        index += 1

    flush_plain()
    return "\n".join(part for part in html_parts if part)


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
