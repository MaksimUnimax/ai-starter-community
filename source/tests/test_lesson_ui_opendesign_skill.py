from __future__ import annotations

import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_ROOT = REPO_ROOT / ".agents" / "skills" / "openscript-lesson-ui-opendesign"
REF_SKILL = SKILL_ROOT / "references" / "manalkaff_opendesign_SKILL.md"
TEST_FILE = Path(__file__).resolve()


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_skill_directory_and_files_exist() -> None:
    assert SKILL_ROOT.is_dir()
    assert (SKILL_ROOT / "README.md").is_file()
    assert (SKILL_ROOT / "SKILL.md").is_file()
    assert REF_SKILL.is_file()
    assert (SKILL_ROOT / "templates" / "lesson_ui_blocks.md").is_file()
    assert (SKILL_ROOT / "templates" / "visual_qa_checklist.md").is_file()
    assert (SKILL_ROOT / "templates" / "browser_proof_report.md").is_file()


def test_skill_contract_mentions_separation_and_local_reference() -> None:
    text = _read(SKILL_ROOT / "SKILL.md")
    assert "separate from `openscript-course-authoring`" in text
    assert "Do not read external upstream docs" in text
    assert "references/manalkaff_opendesign_SKILL.md" in text


def test_skill_contract_forbids_bad_ui_patterns() -> None:
    text = _read(SKILL_ROOT / "SKILL.md")
    assert "No raw markdown artifacts" in text
    assert "No raw `.md` answer links" in text
    assert "Do not ship fake interactive controls" in text
    assert "Do not keep `.md` answer links as the primary user-facing path" in text


def test_skill_contract_requires_real_controls_and_proof() -> None:
    text = _read(SKILL_ROOT / "SKILL.md")
    assert "Quiz has choices." in text
    assert "Проверить" in text
    assert "feedback area" in text
    assert "Checklist is clickable, not disabled." in text
    assert "rendered HTML" in text
    assert "browser proof" in text or "browser proof report" in text


def test_skill_contract_forbids_package_install_without_approval() -> None:
    text = _read(SKILL_ROOT / "SKILL.md")
    assert "Do not install packages without explicit approval." in text


def test_repository_changes_stay_within_skill_scope() -> None:
    result = subprocess.run(
        ["git", "status", "--short", "--untracked-files=all"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    allowed_prefixes = (
        "?? .agents/skills/openscript-lesson-ui-opendesign/",
        "A  .agents/skills/openscript-lesson-ui-opendesign/",
        "M  .agents/skills/openscript-lesson-ui-opendesign/",
        "D  .agents/skills/openscript-lesson-ui-opendesign/",
        "?? source/tests/test_lesson_ui_opendesign_skill.py",
        "M  source/tests/test_lesson_ui_opendesign_skill.py",
    )
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        if line.startswith("?? source/app/"):
            continue
        assert line.startswith(allowed_prefixes), f"unexpected changed file: {line}"
    assert TEST_FILE.is_file()
