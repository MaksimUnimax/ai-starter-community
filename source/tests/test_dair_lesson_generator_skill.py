from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_ROOT = REPO_ROOT / ".agents" / "skills" / "dair-lesson-generator"
DAIR_SKILL = SKILL_ROOT / "SKILL.md"
README = SKILL_ROOT / "README.md"
COURSE_AUTHORING_SKILL = REPO_ROOT / ".agents" / "skills" / "openscript-course-authoring" / "SKILL.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_dair_skill_files_exist() -> None:
    assert DAIR_SKILL.is_file()
    assert README.is_file()


def test_dair_skill_contains_required_concepts() -> None:
    text = _read(DAIR_SKILL)
    assert text.startswith("---")
    assert "name: lesson-generator" in text
    assert "Build compact, standalone multi-lesson course artifacts" in text
    assert "lesson navigation" in text
    assert "objectives" in text
    assert "flashcards" in text
    assert "quizzes" in text
    assert "index.html" in text
    assert "styles.css" in text
    assert "script.js" in text
    assert any(token in text for token in ("smoke", "parse", "Start Learning", "feedback"))


def test_dair_skill_does_not_instruct_read_upstream_as_working_path() -> None:
    text = _read(DAIR_SKILL).lower()
    assert "read upstream" not in text


def test_dair_skill_is_not_old_summary_shape() -> None:
    text = _read(DAIR_SKILL)
    assert not text.startswith("# lesson-generator")
    assert "Purpose:" not in text
    assert "When to use:" not in text


def test_course_authoring_skill_still_exists_and_was_not_modified() -> None:
    assert COURSE_AUTHORING_SKILL.is_file()
    assert "openscript-course-authoring" in _read(COURSE_AUTHORING_SKILL)
