from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
FOUNDRY_ROOT = Path(__file__).resolve().parents[1]
BIN_DIR = FOUNDRY_ROOT / "bin"

REPO_HELPER_PREFLIGHT = BIN_DIR / "repo-helper-preflight"
REPO_HELPER_STAGE1_PLAN = BIN_DIR / "repo-helper-stage1-plan"
REPO_HELPER_POSTFLIGHT = BIN_DIR / "repo-helper-postflight"
REPO_HELPER_STAGE2_THEME_PLAN = BIN_DIR / "repo-helper-stage2-theme-plan"
REPO_HELPER_STAGE2_RUN_PLAN = BIN_DIR / "repo-helper-stage2-run-plan"


def _run(cmd: list[str], *, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def _copy_foundry_tree(tmp_path: Path) -> Path:
    destination = tmp_path / "skills-foundry-copy"
    shutil.copytree(
        FOUNDRY_ROOT,
        destination,
        ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"),
    )
    return destination


def test_end_to_end_foundry_smoke_script_and_refresh_in_isolated_copy(tmp_path: Path) -> None:
    foundry_copy = _copy_foundry_tree(tmp_path)
    sync_target = tmp_path / "installed-skills"

    smoke_result = _run(
        [
            str(foundry_copy / "bin" / "smoke-check-foundry"),
            "--with-real-sync",
            "--sync-target",
            str(sync_target),
        ],
        cwd=foundry_copy,
    )
    assert smoke_result.returncode == 0, smoke_result.stdout + "\n" + smoke_result.stderr
    assert "[smoke] skills-new (smoke-check)" in smoke_result.stdout
    assert "[smoke] skills-sync --dry-run" in smoke_result.stdout
    assert "[smoke] real sync complete" in smoke_result.stdout
    assert "[smoke] done" in smoke_result.stdout
    assert (sync_target / "INDEX.md").exists()

    reports_dir = foundry_copy / "reports"
    assert (reports_dir / "skills-lint.json").exists()
    assert (reports_dir / "skills-lint.md").exists()
    assert (reports_dir / "SKILLS_CATALOG.md").exists()

    refresh_result = _run([str(foundry_copy / "bin" / "refresh-doc-examples")], cwd=foundry_copy)
    assert refresh_result.returncode == 0, refresh_result.stdout + "\n" + refresh_result.stderr
    assert "[write] refreshed:" in refresh_result.stdout

    examples_dir = foundry_copy / "docs" / "examples"
    lint_json_snippet = examples_dir / "skills-lint-json-snippet.json"
    prune_snippet = examples_dir / "skills-sync-prune-dry-run.txt"
    assert lint_json_snippet.exists()
    assert prune_snippet.exists()
    assert "top_issue_rule_ids" in lint_json_snippet.read_text(encoding="utf-8")
    prune_text = prune_snippet.read_text(encoding="utf-8")
    assert "Sync plan:" in prune_text
    assert "would-prune:" in prune_text


def test_end_to_end_repo_helper_flow_uses_actual_demo_prompt_assets(tmp_path: Path) -> None:
    demo_source = FOUNDRY_ROOT / "demo-repo"
    repo_copy = tmp_path / "demo-repo"
    shutil.copytree(
        demo_source,
        repo_copy,
        ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"),
    )

    preflight_report = repo_copy / "preflight.md"
    stage1_plan = repo_copy / "STAGE1-PLAN.md"
    run_log = repo_copy / "STAGE1-RUN-LOG.md"
    postflight_report = repo_copy / "STAGE-1-POST-FLIGHT.md"
    stage2_theme_plan = repo_copy / ".prompts" / "STAGE2-PLAN.md"
    stage2_run_plan = repo_copy / "STAGE2-RUN-PLAN.md"

    preflight = _run(
        [
            str(REPO_HELPER_PREFLIGHT),
            "--repo-root",
            str(repo_copy),
            "--write-report",
            str(preflight_report),
        ],
        cwd=REPO_ROOT,
    )
    assert preflight.returncode == 0, preflight.stdout + "\n" + preflight.stderr
    assert preflight_report.exists()
    assert "Prompt Preflight Snapshot" in preflight_report.read_text(encoding="utf-8")

    stage1 = _run(
        [
            str(REPO_HELPER_STAGE1_PLAN),
            "--repo-root",
            str(repo_copy),
            "--prompts-dir",
            ".prompts",
            "--start",
            "1",
            "--end",
            "2",
            "--write-plan",
            "STAGE1-PLAN.md",
            "--execute",
            "--runner-shell-template",
            "python3 -c 'import sys; print(\"RUN\", sys.argv[1])' {prompt_path}",
            "--run-log",
            "STAGE1-RUN-LOG.md",
            "--runner-timeout-seconds",
            "5",
        ],
        cwd=REPO_ROOT,
    )
    assert stage1.returncode == 0, stage1.stdout + "\n" + stage1.stderr
    assert stage1_plan.exists()
    assert run_log.exists()
    stage1_plan_text = stage1_plan.read_text(encoding="utf-8")
    run_log_text = run_log.read_text(encoding="utf-8")
    assert "Stage 1 Run Plan" in stage1_plan_text
    assert "PROMPT_01.txt" in stage1_plan_text
    assert "PROMPT_02.txt" in stage1_plan_text
    assert "PROMPT_01.txt" in run_log_text
    assert "PROMPT_02.txt" in run_log_text
    assert "- status: `success`" in run_log_text

    postflight = _run(
        [
            str(REPO_HELPER_POSTFLIGHT),
            "--repo-root",
            str(repo_copy),
            "--stage",
            "stage1",
            "--output",
            str(postflight_report),
        ],
        cwd=REPO_ROOT,
    )
    assert postflight.returncode == 0, postflight.stdout + "\n" + postflight.stderr
    assert postflight_report.exists()
    assert "Automated Snapshot" in postflight_report.read_text(encoding="utf-8")

    stage2_theme = _run(
        [
            str(REPO_HELPER_STAGE2_THEME_PLAN),
            "--repo-root",
            str(repo_copy),
            "--input",
            str(postflight_report),
            "--output",
            str(stage2_theme_plan),
        ],
        cwd=REPO_ROOT,
    )
    assert stage2_theme.returncode == 0, stage2_theme.stdout + "\n" + stage2_theme.stderr
    assert stage2_theme_plan.exists()
    assert "Suggested Stage-2 Prompt Themes" in stage2_theme_plan.read_text(encoding="utf-8")

    stage2_run = _run(
        [
            str(REPO_HELPER_STAGE2_RUN_PLAN),
            "--repo-root",
            str(repo_copy),
            "--prompts-dir",
            ".prompts",
            "--start",
            "2",
            "--end",
            "3",
            "--write-plan",
            str(stage2_run_plan),
        ],
        cwd=REPO_ROOT,
    )
    assert stage2_run.returncode == 0, stage2_run.stdout + "\n" + stage2_run.stderr
    assert stage2_run_plan.exists()
    assert "Stage 2 Run Plan" in stage2_run_plan.read_text(encoding="utf-8")
