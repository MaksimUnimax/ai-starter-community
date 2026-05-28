from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_ROOT = REPO_ROOT / ".agents" / "skills" / "mblode-agent-skills"
VERCEL_ROOT = REPO_ROOT / ".agents" / "skills" / "vercel-web-design-guidelines"

COMPANION_FILES = (
    "product-ui.md",
    "marketing-ui.md",
    "aesthetic-direction.md",
    "design-in-code.md",
    "references/cro.md",
    "references/testing.md",
    "references/modern.md",
)


def test_mblode_active_skill_package_is_complete() -> None:
    assert SKILL_ROOT.is_dir()
    assert (SKILL_ROOT / "SKILL.md").is_file()
    assert (SKILL_ROOT / "README.md").is_file()
    for rel_path in COMPANION_FILES:
        assert (SKILL_ROOT / rel_path).is_file(), rel_path
    assert not VERCEL_ROOT.exists()


def test_mblode_active_skill_readme_mentions_companions() -> None:
    text = (SKILL_ROOT / "README.md").read_text(encoding="utf-8")
    assert "active repo-scoped Codex skill" in text
    assert "companion files" in text
    assert "$mblode-agent-skills" in text
    assert "/opt/ai-starter-community/.agents/skills/mblode-agent-skills/SKILL.md" in text


def test_mblode_skill_files_are_nonempty() -> None:
    for rel_path in ("SKILL.md",) + COMPANION_FILES:
        text = (SKILL_ROOT / rel_path).read_text(encoding="utf-8")
        assert len(text.splitlines()) > 20, rel_path
