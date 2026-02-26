from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
SKILLS_NEW_CLI = ROOT / "bin" / "skills-new"
SKILLS_RENDER_CLI = ROOT / "bin" / "skills-render"


def test_skills_new_then_render_catalog(tmp_path: Path) -> None:
    skills_root = tmp_path / "skills"
    reports_dir = tmp_path / "reports"
    output_catalog = reports_dir / "SKILLS_CATALOG.md"

    new_result = subprocess.run(
        [
            str(SKILLS_NEW_CLI),
            "--category",
            "core",
            "--skill-id",
            "demo-skill",
            "--name",
            "Demo Skill",
            "--description",
            "A demo skill for CLI smoke testing.",
            "--skills-root",
            str(skills_root),
        ],
        capture_output=True,
        text=True,
    )
    assert new_result.returncode == 0, new_result.stdout + "\n" + new_result.stderr
    skill_dir = skills_root / "core" / "demo-skill"
    assert (skill_dir / "SKILL.md").exists()
    assert (skill_dir / "EXAMPLES.md").exists()
    assert (skill_dir / "CHECKLIST.md").exists()

    render_result = subprocess.run(
        [
            str(SKILLS_RENDER_CLI),
            "--skills-root",
            str(skills_root),
            "--output",
            str(output_catalog),
            "--repo-root",
            str(tmp_path),
        ],
        capture_output=True,
        text=True,
    )
    assert render_result.returncode == 0, render_result.stdout + "\n" + render_result.stderr
    assert output_catalog.exists()
    catalog_text = output_catalog.read_text(encoding="utf-8")
    assert "Total skills: 1" in catalog_text
    assert "demo-skill" in catalog_text
    assert "A demo skill for CLI smoke testing." in catalog_text
