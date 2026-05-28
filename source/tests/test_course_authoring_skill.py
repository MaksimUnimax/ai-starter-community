from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SKILL_ROOT = ROOT / ".agents" / "skills" / "openscript-course-authoring"
TEMPLATES = SKILL_ROOT / "templates"
COURSE_CONTENT_DIR = ROOT / "source" / "app" / "materials" / "course_content"


def test_skill_directory_exists():
    assert SKILL_ROOT.is_dir()


def test_skill_files_exist():
    assert (SKILL_ROOT / "SKILL.md").is_file()
    assert (SKILL_ROOT / "README.md").is_file()


def test_skill_templates_exist():
    expected = ["course.yaml", "lesson.md", "answer.md", "report.md"]
    for name in expected:
        assert (TEMPLATES / name).is_file()


def test_skill_contract_terms():
    text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8").lower()
    assert "dair lesson-generator" in text
    assert "chatgpt designs" in text
    assert "codex executes" in text
    assert "empty lessons" in text
    assert "placeholder lessons" in text
    assert "ready answers" in text
    assert "checkable tasks" in text


def test_skill_does_not_include_generated_course_output_inside_skill_folder():
    assert not (SKILL_ROOT / "course_content").exists()
