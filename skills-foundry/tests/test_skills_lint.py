from pathlib import Path
import json
import subprocess
import textwrap


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "bin" / "skills-lint"


def test_lint_scoring_works_on_sample_skill(tmp_path: Path) -> None:
    skills_root = tmp_path / "skills"
    skill_dir = skills_root / "core" / "sample-skill"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        textwrap.dedent(
            """\
            ---
            id: sample-skill
            name: Sample Skill
            description: Demonstrate lint scoring.
            version: 0.1.0
            tags: [core, demo]
            inputs:
              - name: target_path
                type: path
                required: true
                default: "."
                examples: [".", "src/"]
            expected_tools: [git, rg]
            safety:
              dry_run_supported: true
              destructive_actions: []
              confirmation_points:
                - "Confirm before writing"
            outputs:
              - docs/DEMO.md
            ---

            ## When to use
            Use this for a focused demo.

            ## Inputs
            - `target_path`: repo path.

            ## Procedure
            1. Inspect the target.
            2. Apply the change.
            3. Verify the result.

            ## Success criteria
            Output exists and changes are summarized.

            ## Failure modes + recovery
            If a command fails, recover by fixing the input and retrying.

            ## Examples
            Example: run on a small repo and confirm the generated report path.
            """
        ),
        encoding="utf-8",
    )

    reports_dir = tmp_path / "reports"
    result = subprocess.run(
        [
            str(CLI),
            "--skills-root",
            str(skills_root),
            "--repo-root",
            str(tmp_path),
            "--reports-dir",
            str(reports_dir),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert (reports_dir / "skills-lint.json").exists()
    assert (reports_dir / "skills-lint.md").exists()

    data = json.loads((reports_dir / "skills-lint.json").read_text(encoding="utf-8"))
    assert len(data) == 1
    item = data[0]
    assert item["skill_id"] == "sample-skill"
    assert item["path"] == "skills/core/sample-skill/SKILL.md"
    assert "completeness_score_100" in item
    assert "excellence_score_10" in item
    assert "top_issues" in item
    assert "suggested_fixes" in item


def test_skills_lint_help_runs() -> None:
    result = subprocess.run([str(CLI), "--help"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "Lint skills" in result.stdout


def test_skills_lint_can_emit_absolute_paths(tmp_path: Path) -> None:
    skills_root = tmp_path / "skills"
    skill_dir = skills_root / "core" / "sample-skill"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        textwrap.dedent(
            """\
            ---
            id: sample-skill
            name: Sample Skill
            description: Demonstrate lint path formatting.
            version: 0.1.0
            tags: [core, demo]
            inputs:
              - name: target_path
                type: path
                required: true
                examples: ["."]
            expected_tools: [git]
            safety:
              dry_run_supported: true
              destructive_actions: []
              confirmation_points:
                - "Confirm before writing"
            outputs:
              - docs/DEMO.md
            ---

            ## When to use
            Use this for a focused demo.

            ## Inputs
            - `target_path`: repo path.

            ## Procedure
            1. Inspect the target.
            2. Apply the change.
            3. Verify the result.

            ## Success criteria
            Output exists and changes are summarized.

            ## Failure modes + recovery
            Recover by fixing inputs and retrying.

            ## Examples
            Example: run on a small repo and confirm the generated report path.
            """
        ),
        encoding="utf-8",
    )

    reports_dir = tmp_path / "reports"
    result = subprocess.run(
        [
            str(CLI),
            "--skills-root",
            str(skills_root),
            "--repo-root",
            str(tmp_path),
            "--reports-dir",
            str(reports_dir),
            "--absolute-paths",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + "\n" + result.stderr
    data = json.loads((reports_dir / "skills-lint.json").read_text(encoding="utf-8"))
    assert Path(data[0]["path"]).is_absolute()
