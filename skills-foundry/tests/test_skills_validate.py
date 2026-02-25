from pathlib import Path
import subprocess
import textwrap


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "bin" / "skills-validate"


def test_skills_validate_fails_missing_yaml_fields(tmp_path: Path) -> None:
    skills_root = tmp_path / "skills"
    skill_dir = skills_root / "workflow" / "bad-skill"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        textwrap.dedent(
            """\
            ---
            id: bad-skill
            name: Bad Skill
            version: 0.1.0
            tags: [workflow]
            inputs:
              - name: target
                type: path
                required: true
                examples: ["."]
            expected_tools: [git]
            safety:
              dry_run_supported: true
              destructive_actions: []
              confirmation_points:
                - "Confirm"
            outputs:
              - docs/OUT.md
            ---

            ## When to use
            test

            ## Inputs
            test

            ## Procedure
            1. Do a thing.
            2. Check it.
            3. Report it.

            ## Success criteria
            done

            ## Failure modes + recovery
            recover by retrying

            ## Examples
            example usage
            """
        ),
        encoding="utf-8",
    )

    result = subprocess.run(
        [str(CLI), "--skills-root", str(skills_root), "--repo-root", str(tmp_path)],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "Missing required metadata key: description" in result.stdout


def test_skills_validate_help_runs() -> None:
    result = subprocess.run([str(CLI), "--help"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "Validate skills" in result.stdout
