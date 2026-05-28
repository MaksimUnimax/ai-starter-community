from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[2]
COURSE_ROOT = ROOT / "source" / "app" / "materials" / "course_content"
COURSE_YAML = COURSE_ROOT / "course.yaml"
LESSON = COURSE_ROOT / "lessons" / "01-kak-my-rabotaem.md"
ANSWER = COURSE_ROOT / "answers" / "01-kak-my-rabotaem.md"
ASSETS_README = COURSE_ROOT / "assets" / "README.md"


REQUIRED_HEADINGS = [
    "Название",
    "Для кого урок",
    "Цель",
    "Простое объяснение",
    "Бытовая аналогия",
    "Что пользователь увидит",
    "Практика по шагам",
    "Задание",
    "Готовый ответ",
    "Самопроверка",
    "Какой отчёт принести в ChatGPT",
    "Типичные ошибки",
    "Критерии готово",
    "Переход к следующему уроку",
]

FORBIDDEN_MARKERS = [
    "todo",
    "placeholder",
    "заглушка",
    "заполнить потом",
    "later",
]


def _git_status(paths):
    cmd = ["git", "-C", str(ROOT), "status", "--short", "--"]
    cmd.extend(paths)
    return subprocess.check_output(cmd, text=True).strip()


def test_course_files_exist():
    assert COURSE_YAML.is_file()
    assert LESSON.is_file()
    assert ANSWER.is_file()
    assert ASSETS_README.is_file()


def test_course_yaml_references_lesson_and_answer():
    text = COURSE_YAML.read_text(encoding="utf-8")
    assert "course_id: work-with-ai" in text
    assert "lesson-01" in text
    assert "lesson_path: lessons/01-kak-my-rabotaem.md" in text
    assert "answer_path: answers/01-kak-my-rabotaem.md" in text


def test_lesson_contains_required_headings():
    text = LESSON.read_text(encoding="utf-8")
    for heading in REQUIRED_HEADINGS:
        assert f"## {heading}" in text or f"# {heading}" in text


def test_lesson_has_practical_task_self_check_and_answer_reference():
    text = LESSON.read_text(encoding="utf-8")
    assert "## Практика по шагам" in text
    assert "## Самопроверка" in text
    assert "## Готовый ответ" in text
    assert "../answers/01-kak-my-rabotaem.md" in text


def test_lesson_has_no_placeholder_markers():
    text = LESSON.read_text(encoding="utf-8").lower()
    for marker in FORBIDDEN_MARKERS:
        assert marker not in text


def test_answer_has_pass_fail_checklist():
    text = ANSWER.read_text(encoding="utf-8")
    assert "# Pass/Fail Checklist" in text
    assert "# Ready Answer" in text


def test_no_ui_or_auth_files_changed():
    forbidden_paths = [
        "source/app/auth",
        "source/app/user_cabinet",
        "source/app/materials/routes.py",
        "source/app/materials/templates",
        "source/app/shared/templates/base.html",
    ]
    status = _git_status(forbidden_paths)
    assert status == ""
