"""Prompt library helpers for the personal cabinet."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

COURSE_DRAFT_ID = "dair_smoke_20260529"
COURSE_SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "materials"
    / "course_content"
    / "drafts"
    / COURSE_DRAFT_ID
    / "script.js"
)

STARTER_PROMPT_FILENAME_RE = re.compile(r'starterPromptFilename:\s*"(?P<filename>[^"]+)"')
STARTER_PROMPT_LABEL_RE = re.compile(r'starterPromptLabel:\s*"(?P<label>[^"]+)"')
PROMPT_FORM_RE = re.compile(
    r'promptForm:\s*\{\s*id:\s*"(?P<id>[^"]+)"\s*,\s*label:\s*"(?P<label>[^"]+)"\s*,\s*description:\s*"(?P<description>[^"]+)"\s*,\s*actionsLabel:\s*"(?P<actions_label>[^"]+)"\s*,\s*filename:\s*"(?P<filename>[^"]+)"\s*,\s*markdown:\s*',
    re.S,
)


def _read_course_script() -> str:
    return COURSE_SCRIPT_PATH.read_text(encoding="utf-8")


def _skip_whitespace(text: str, index: int) -> int:
    while index < len(text) and text[index].isspace():
        index += 1
    return index


def _extract_template_literal(text: str, index: int) -> tuple[str, int]:
    position = _skip_whitespace(text, index)
    if position >= len(text) or text[position] != "`":
        raise ValueError("Expected a template literal")

    chars: list[str] = []
    cursor = position + 1
    while cursor < len(text):
        char = text[cursor]
        if char == "\\":
            if cursor + 1 >= len(text):
                raise ValueError("Unterminated escape in template literal")
            escaped = text[cursor + 1]
            if escaped == "`":
                chars.append("`")
                cursor += 2
                continue
            if escaped == "\\":
                chars.append("\\")
                cursor += 2
                continue
            if escaped == "$" and cursor + 2 < len(text) and text[cursor + 2] == "{":
                chars.append("${")
                cursor += 3
                continue
            escape_map = {
                "n": "\n",
                "r": "\r",
                "t": "\t",
                "b": "\b",
                "f": "\f",
                "v": "\v",
                "0": "\0",
            }
            chars.append(escape_map.get(escaped, escaped))
            cursor += 2
            continue
        if char == "`":
            return "".join(chars), cursor + 1
        chars.append(char)
        cursor += 1

    raise ValueError("Unterminated template literal")


def _extract_section(script_text: str, lesson_id: str, next_lesson_id: str) -> str:
    start = script_text.index(f'id: "{lesson_id}"')
    end = script_text.index(f'id: "{next_lesson_id}"', start)
    return script_text[start:end]


def _normalize_title(markdown: str) -> str:
    match = re.search(r"^\s*#\s+(.+?)\s*$", markdown, re.M)
    if match:
        return match.group(1).strip()

    for line in markdown.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return "Prompt"


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower())
    return slug.strip("-") or "prompt"


def _lesson_owner_label(lesson_number: int) -> str:
    return f"Урок {lesson_number}"


def _build_starter_prompt(section: str, lesson_number: int) -> dict[str, Any]:
    filename_match = STARTER_PROMPT_FILENAME_RE.search(section)
    if filename_match is None:
        raise ValueError(f"Missing starterPromptFilename for lesson {lesson_number}")

    markdown_marker = section.index("starterPromptMarkdown:")
    markdown, _ = _extract_template_literal(section, markdown_marker + len("starterPromptMarkdown:"))
    label_match = STARTER_PROMPT_LABEL_RE.search(section)
    filename = filename_match.group("filename")
    title = _normalize_title(markdown)
    prompt_id = f"lesson-{lesson_number}-{_slugify(Path(filename).stem)}"

    return {
        "id": prompt_id,
        "lesson_number": lesson_number,
        "owner_label": _lesson_owner_label(lesson_number),
        "source_label": label_match.group("label") if label_match else None,
        "title": title,
        "filename": filename,
        "markdown": markdown,
    }


def load_cabinet_prompts() -> list[dict[str, Any]]:
    """Return the current built-in course prompts from the canonical course source."""

    script_text = _read_course_script()
    lesson6 = _extract_section(script_text, "lesson-6", "lesson-7")
    lesson7 = _extract_section(script_text, "lesson-7", "lesson-8")
    lesson8 = _extract_section(script_text, "lesson-8", "lesson-9")

    prompts = [
        _build_starter_prompt(lesson6, 6),
        _build_starter_prompt(lesson7, 7),
    ]

    prompt_form_matches = list(PROMPT_FORM_RE.finditer(lesson8))
    for match in prompt_form_matches:
        markdown, _ = _extract_template_literal(lesson8, match.end())
        filename = match.group("filename")
        prompts.append(
            {
                "id": match.group("id"),
                "lesson_number": 8,
                "owner_label": _lesson_owner_label(8),
                "source_label": match.group("label"),
                "title": _normalize_title(markdown),
                "filename": filename,
                "markdown": markdown,
            }
        )

    return prompts
