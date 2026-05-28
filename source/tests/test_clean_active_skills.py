from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SKILLS_ROOT = REPO_ROOT / ".agents" / "skills"

ACTIVE_SKILLS = {
    "dair-lesson-generator": {
        "markers": (
            "name: lesson-generator",
            "index.html",
            "styles.css",
            "script.js",
        ),
        "min_lines": 20,
    },
    "opendesign-manalkaff": {"markers": (), "min_lines": 20},
    "opendesign-nexu": {"markers": (), "min_lines": 20},
    "anthropic-frontend-design": {"markers": (), "min_lines": 20},
    "taste-skill": {"markers": (), "min_lines": 20},
    "microsoft-frontend-design-review": {"markers": (), "min_lines": 20},
    "ilm-alan-frontend-design": {"markers": (), "min_lines": 20},
    "mblode-agent-skills": {"markers": (), "min_lines": 20},
}

BANNED_SKILLS = (
    "openscript-course-authoring",
    "openscript-lesson-ui-opendesign",
    "vercel-web-design-guidelines",
)

BANNED_TESTS = (
    "test_course_authoring_skill.py",
    "test_lesson_ui_opendesign_skill.py",
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_active_skill_folders_and_files_exist() -> None:
    for skill_name in ACTIVE_SKILLS:
        skill_root = SKILLS_ROOT / skill_name
        assert skill_root.is_dir(), skill_name
        assert (skill_root / "SKILL.md").is_file(), skill_name
        assert (skill_root / "README.md").is_file(), skill_name


def test_banned_custom_skills_and_tests_are_gone() -> None:
    for skill_name in BANNED_SKILLS:
        assert not (SKILLS_ROOT / skill_name).exists(), skill_name
    for test_name in BANNED_TESTS:
        assert not (REPO_ROOT / "source" / "tests" / test_name).exists(), test_name


def test_active_skill_readmes_have_activation_snippets() -> None:
    for skill_name in ACTIVE_SKILLS:
        text = _read(SKILLS_ROOT / skill_name / "README.md")
        assert "This folder contains an active repo-scoped Codex skill." in text
        assert f"${skill_name}" in text
        assert f"/opt/ai-starter-community/.agents/skills/{skill_name}/SKILL.md" in text


def test_clean_skill_text_is_not_summary_only() -> None:
    banned_markers = (
        "Read the upstream",
        "read upstream",
        "summary only",
        "local_reference_summary",
        "docs_reference_only",
    )
    for skill_name, info in ACTIVE_SKILLS.items():
        text = _read(SKILLS_ROOT / skill_name / "SKILL.md")
        assert len(text.splitlines()) >= info["min_lines"], skill_name
        for marker in banned_markers:
            assert marker not in text, f"{skill_name}: {marker}"
        for marker in info["markers"]:
            assert marker in text, f"{skill_name}: {marker}"


def test_open_design_skills_are_non_empty_full_copies() -> None:
    for skill_name in ACTIVE_SKILLS:
        if skill_name == "dair-lesson-generator":
            continue
        text = _read(SKILLS_ROOT / skill_name / "SKILL.md")
        assert len(text.splitlines()) > 20, skill_name
