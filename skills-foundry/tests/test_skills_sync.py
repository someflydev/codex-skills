from pathlib import Path
import subprocess
import textwrap


ROOT = Path(__file__).resolve().parents[1]
SYNC_CLI = ROOT / "bin" / "skills-sync"


def _write_valid_skill(skills_root: Path, category: str, skill_id: str, description: str) -> None:
    skill_dir = skills_root / category / skill_id
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(
        textwrap.dedent(
            f"""\
            ---
            id: {skill_id}
            name: {skill_id.replace('-', ' ').title()}
            description: {description}
            version: 0.1.0
            tags: [{category}, demo]
            inputs:
              - name: target_path
                type: path
                required: true
                default: "."
                examples: ["."]
            expected_tools: [git, rg]
            safety:
              dry_run_supported: true
              destructive_actions: []
              confirmation_points:
                - "Confirm before writing"
            outputs:
              - docs/{skill_id}.md
            ---

            ## When to use
            Use this for sync testing.

            ## Inputs
            - `target_path`: repo path.

            ## Procedure
            1. Inspect the repo.
            2. Apply the change.
            3. Verify and report.

            ## Success criteria
            Outputs are produced and summarized.

            ## Failure modes + recovery
            Recover by correcting inputs and retrying.

            ## Examples
            Example: run against a demo repo and confirm generated outputs.
            """
        ),
        encoding="utf-8",
    )


def test_skills_sync_copy_creates_expected_structure(tmp_path: Path) -> None:
    source_skills = tmp_path / "skills"
    _write_valid_skill(source_skills, "core", "hello-skill", "A hello-world skill")

    target_root = tmp_path / "installed-skills"
    backup_root = tmp_path / "backups"
    reports_dir = tmp_path / "reports"

    result = subprocess.run(
        [
            str(SYNC_CLI),
            "--from",
            str(source_skills),
            "--to",
            str(target_root),
            "--backup-dir",
            str(backup_root),
            "--reports-dir",
            str(reports_dir),
            "--repo-root",
            str(tmp_path),
            "--strategy",
            "copy",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + "\n" + result.stderr
    assert (target_root / "hello-skill" / "SKILL.md").exists()
    assert (target_root / "INDEX.md").exists()
    assert not (target_root / "hello-skill").is_symlink()
    assert (reports_dir / "skills-lint.json").exists()
    assert (reports_dir / "skills-lint.md").exists()


def test_skills_sync_dry_run_does_not_write(tmp_path: Path) -> None:
    source_skills = tmp_path / "skills"
    _write_valid_skill(source_skills, "core", "changelog-drafter", "A changelog drafting skill")

    target_root = tmp_path / "installed-skills"
    backup_root = tmp_path / "backups"
    reports_dir = tmp_path / "reports"

    result = subprocess.run(
        [
            str(SYNC_CLI),
            "--from",
            str(source_skills),
            "--to",
            str(target_root),
            "--backup-dir",
            str(backup_root),
            "--reports-dir",
            str(reports_dir),
            "--repo-root",
            str(tmp_path),
            "--dry-run",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + "\n" + result.stderr
    assert not target_root.exists()
