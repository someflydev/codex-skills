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


def test_skills_validate_categorizes_missing_output_paths(tmp_path: Path) -> None:
    skills_root = tmp_path / "skills"
    skill_dir = skills_root / "workflow" / "warn-codes"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        textwrap.dedent(
            """\
            ---
            id: warn-codes
            name: Warn Codes
            description: Exercise output-path warning categorization.
            version: 0.1.0
            tags: [workflow, test]
            inputs:
              - name: repo_root
                type: path
                required: true
                examples: ["."]
            expected_tools: [git]
            safety:
              dry_run_supported: true
              destructive_actions: []
              confirmation_points:
                - "Confirm before write"
            outputs:
              - skills/core/example-skill/SKILL.md
              - skills-foundry/reports/example-report.md
              - docs/EXAMPLE.md
              - build/custom-artifact.txt
            ---

            ## When to use
            Use this test skill to verify warning code categorization.

            ## Inputs
            - `repo_root`: target repo root.

            ## Procedure
            1. Inspect the repo.
            2. Generate outputs.
            3. Validate and report.

            ## Success criteria
            Output paths are described and categorized correctly.

            ## Failure modes + recovery
            Recover by correcting paths and retrying.

            ## Examples
            Example: validate this skill and inspect warning codes.
            """
        ),
        encoding="utf-8",
    )

    result = subprocess.run(
        [str(CLI), "--skills-root", str(skills_root), "--repo-root", str(tmp_path)],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + "\n" + result.stderr
    assert "missing_output_path_install_target_relative" in result.stdout
    assert "missing_output_path_expected_future" in result.stdout
    assert "missing_output_path: Referenced output path does not exist yet (best effort): build/custom-artifact.txt" in result.stdout


def test_skills_validate_can_suppress_expected_output_warnings_and_show_summary(tmp_path: Path) -> None:
    skills_root = tmp_path / "skills"
    skill_dir = skills_root / "workflow" / "warn-summary"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        textwrap.dedent(
            """\
            ---
            id: warn-summary
            name: Warn Summary
            description: Exercise warning suppression and summaries.
            version: 0.1.0
            tags: [workflow, test]
            inputs:
              - name: repo_root
                type: path
                required: true
                examples: ["."]
            expected_tools: [git]
            safety:
              dry_run_supported: true
              destructive_actions: []
              confirmation_points:
                - "Confirm before write"
            outputs:
              - skills/core/example-skill/SKILL.md
              - skills-foundry/reports/example-report.md
              - build/custom-artifact.txt
            ---

            ## When to use
            Use this test skill to verify warning suppression and summaries.

            ## Inputs
            - `repo_root`: target repo root.

            ## Procedure
            1. Inspect the repo.
            2. Generate outputs.
            3. Validate and report.

            ## Success criteria
            Output paths are described and categorized correctly.

            ## Failure modes + recovery
            Recover by correcting paths and retrying.

            ## Examples
            Example: validate this skill and inspect warning summaries.
            """
        ),
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            str(CLI),
            "--skills-root",
            str(skills_root),
            "--repo-root",
            str(tmp_path),
            "--suppress-expected-output-warnings",
            "--warning-code-summary",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + "\n" + result.stderr
    assert "missing_output_path_install_target_relative" not in result.stdout
    assert "missing_output_path_expected_future" not in result.stdout
    assert "Warning Code Summary:" in result.stdout
    assert "- missing_output_path: 1" in result.stdout


def test_skills_validate_prints_compact_hint_on_noisy_verbose_run(tmp_path: Path) -> None:
    skills_root = tmp_path / "skills"
    skill_dir = skills_root / "workflow" / "warn-hint"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        textwrap.dedent(
            """\
            ---
            id: warn-hint
            name: Warn Hint
            description: Exercise compact hint behavior on noisy validation output.
            version: 0.1.0
            tags: [workflow, test]
            inputs:
              - name: repo_root
                type: path
                required: true
                examples: ["."]
            expected_tools: [git]
            safety:
              dry_run_supported: true
              destructive_actions: []
              confirmation_points:
                - "Confirm before write"
            outputs:
              - build/out-1.txt
              - build/out-2.txt
              - build/out-3.txt
              - build/out-4.txt
              - build/out-5.txt
              - build/out-6.txt
              - build/out-7.txt
              - build/out-8.txt
              - build/out-9.txt
              - build/out-10.txt
            ---

            ## When to use
            Use this test skill to verify compact hint output.

            ## Inputs
            - `repo_root`: target repo root.

            ## Procedure
            1. Inspect the repo.
            2. Generate outputs.
            3. Validate and report.

            ## Success criteria
            Output warnings are shown and the compact hint appears.

            ## Failure modes + recovery
            Recover by correcting paths and retrying.

            ## Examples
            Example: validate this skill without compact mode.
            """
        ),
        encoding="utf-8",
    )

    result = subprocess.run(
        [str(CLI), "--skills-root", str(skills_root), "--repo-root", str(tmp_path)],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + "\n" + result.stderr
    assert "Hint: this run has a high warning count." in result.stdout
    assert "--compact" in result.stdout


def test_skills_validate_compact_alias_enables_warning_triage_preset(tmp_path: Path) -> None:
    skills_root = tmp_path / "skills"
    skill_dir = skills_root / "workflow" / "warn-compact"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        textwrap.dedent(
            """\
            ---
            id: warn-compact
            name: Warn Compact
            description: Exercise compact validation output preset.
            version: 0.1.0
            tags: [workflow, test]
            inputs:
              - name: repo_root
                type: path
                required: true
                examples: ["."]
            expected_tools: [git]
            safety:
              dry_run_supported: true
              destructive_actions: []
              confirmation_points:
                - "Confirm before write"
            outputs:
              - skills/core/example-skill/SKILL.md
              - skills-foundry/reports/example-report.md
              - STAGE-1-POST-FLIGHT.md
            ---

            ## When to use
            Use this test skill to verify compact validation behavior.

            ## Inputs
            - `repo_root`: target repo root.

            ## Procedure
            1. Inspect the repo.
            2. Generate outputs.
            3. Validate and report.

            ## Success criteria
            Output paths are described and categorized correctly.

            ## Failure modes + recovery
            Recover by correcting paths and retrying.

            ## Examples
            Example: validate this skill with compact output enabled.
            """
        ),
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            str(CLI),
            "--skills-root",
            str(skills_root),
            "--repo-root",
            str(tmp_path),
            "--compact",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + "\n" + result.stderr
    # `skills/` and reports outputs are suppressed by the compact preset.
    assert "missing_output_path_install_target_relative" not in result.stdout
    assert "missing_output_path_expected_future" not in result.stdout
    # Generic warning remains visible and a grouped summary is printed.
    assert "missing_output_path: Referenced output path does not exist yet (best effort): STAGE-1-POST-FLIGHT.md" in result.stdout
    assert "Warning Code Summary:" in result.stdout
    assert "- missing_output_path: 1" in result.stdout
    assert "Hint: this run has a high warning count." not in result.stdout
