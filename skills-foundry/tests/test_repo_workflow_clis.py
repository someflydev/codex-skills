from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
REPO_HELPER_PREFLIGHT = ROOT / "bin" / "repo-helper-preflight"
REPO_HELPER_STAGE1_PLAN = ROOT / "bin" / "repo-helper-stage1-plan"
REPO_HELPER_POSTFLIGHT = ROOT / "bin" / "repo-helper-postflight"
REPO_HELPER_STAGE2_THEME_PLAN = ROOT / "bin" / "repo-helper-stage2-theme-plan"
REPO_HELPER_STAGE2_RUN_PLAN = ROOT / "bin" / "repo-helper-stage2-run-plan"
DEMO_REPO_RESET = ROOT / "bin" / "demo-repo-reset"

DEPRECATED_REPO_PREFLIGHT = ROOT / "bin" / "repo-preflight"
DEPRECATED_REPO_STAGE1_RUN = ROOT / "bin" / "repo-stage1-run"
DEPRECATED_REPO_POSTFLIGHT = ROOT / "bin" / "repo-postflight"
DEPRECATED_REPO_STAGE2_PLAN = ROOT / "bin" / "repo-stage2-plan"
DEPRECATED_REPO_STAGE2_RUN = ROOT / "bin" / "repo-stage2-run"


def _make_prompt_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "demo-repo"
    prompts_dir = repo_root / ".prompts"
    prompts_dir.mkdir(parents=True, exist_ok=True)
    (prompts_dir / "PROMPT_00_s.txt").write_text("System prompt\\n", encoding="utf-8")
    (prompts_dir / "PROMPT_01.txt").write_text("Task 1\\n", encoding="utf-8")
    (prompts_dir / "PROMPT_02.txt").write_text("Task 2\\n", encoding="utf-8")
    (prompts_dir / "PROMPT_03.txt").write_text("Task 3\\n", encoding="utf-8")
    (repo_root / "README.md").write_text("# Demo Repo\\n", encoding="utf-8")
    return repo_root


def _run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, capture_output=True, text=True)


def test_repo_workflow_helpers_help_runs() -> None:
    for cli in [
        REPO_HELPER_PREFLIGHT,
        REPO_HELPER_STAGE1_PLAN,
        REPO_HELPER_POSTFLIGHT,
        REPO_HELPER_STAGE2_THEME_PLAN,
        REPO_HELPER_STAGE2_RUN_PLAN,
        DEMO_REPO_RESET,
    ]:
        result = _run([str(cli), "--help"])
        assert result.returncode == 0, f"{cli.name}\n{result.stdout}\n{result.stderr}"


def test_repo_workflow_deprecated_aliases_still_work_and_warn() -> None:
    alias_map = {
        DEPRECATED_REPO_PREFLIGHT: "repo-helper-preflight",
        DEPRECATED_REPO_STAGE1_RUN: "repo-helper-stage1-plan",
        DEPRECATED_REPO_POSTFLIGHT: "repo-helper-postflight",
        DEPRECATED_REPO_STAGE2_PLAN: "repo-helper-stage2-theme-plan",
        DEPRECATED_REPO_STAGE2_RUN: "repo-helper-stage2-run-plan",
    }
    for alias_cli, canonical_name in alias_map.items():
        result = _run([str(alias_cli), "--help"])
        assert result.returncode == 0, f"{alias_cli.name}\n{result.stdout}\n{result.stderr}"
        assert "DEPRECATED alias" in result.stderr
        assert canonical_name in result.stderr


def test_repo_workflow_helpers_generate_plans_and_snapshots(tmp_path: Path) -> None:
    repo_root = _make_prompt_repo(tmp_path)

    preflight_report = repo_root / "preflight.md"
    stage1_plan = repo_root / "STAGE1-PLAN.md"
    postflight_report = repo_root / "STAGE-1-POST-FLIGHT.md"
    stage2_plan = repo_root / ".prompts" / "STAGE2-PLAN.md"
    stage2_run_plan = repo_root / "STAGE2-RUN-PLAN.md"

    preflight = _run(
        [
            str(REPO_HELPER_PREFLIGHT),
            "--repo-root",
            str(repo_root),
            "--write-report",
            str(preflight_report),
            "--require-tools",
            "git",
            "python3",
        ]
    )
    assert preflight.returncode == 0, preflight.stdout + "\n" + preflight.stderr
    assert preflight_report.exists()
    assert "Prompt Preflight Snapshot" in preflight_report.read_text(encoding="utf-8")

    stage1 = _run(
        [
            str(REPO_HELPER_STAGE1_PLAN),
            "--repo-root",
            str(repo_root),
            "--prompts-dir",
            ".prompts",
            "--start",
            "1",
            "--end",
            "2",
            "--write-plan",
            str(stage1_plan),
            "--require-tools",
            "git",
            "python3",
        ]
    )
    assert stage1.returncode == 0, stage1.stdout + "\n" + stage1.stderr
    assert stage1_plan.exists()
    stage1_text = stage1_plan.read_text(encoding="utf-8")
    assert "Stage 1 Run Plan" in stage1_text
    assert "PROMPT_01.txt" in stage1_text
    assert "PROMPT_02.txt" in stage1_text

    postflight = _run(
        [
            str(REPO_HELPER_POSTFLIGHT),
            "--repo-root",
            str(repo_root),
            "--stage",
            "stage1",
            "--output",
            str(postflight_report),
        ]
    )
    assert postflight.returncode == 0, postflight.stdout + "\n" + postflight.stderr
    assert postflight_report.exists()
    assert "Automated Snapshot" in postflight_report.read_text(encoding="utf-8")

    stage2plan = _run(
        [
            str(REPO_HELPER_STAGE2_THEME_PLAN),
            "--repo-root",
            str(repo_root),
            "--input",
            str(postflight_report),
            "--output",
            str(stage2_plan),
        ]
    )
    assert stage2plan.returncode == 0, stage2plan.stdout + "\n" + stage2plan.stderr
    assert stage2_plan.exists()
    assert "Suggested Stage-2 Prompt Themes" in stage2_plan.read_text(encoding="utf-8")

    stage2run = _run(
        [
            str(REPO_HELPER_STAGE2_RUN_PLAN),
            "--repo-root",
            str(repo_root),
            "--prompts-dir",
            ".prompts",
            "--start",
            "2",
            "--end",
            "2",
            "--write-plan",
            str(stage2_run_plan),
            "--require-tools",
            "git",
            "python3",
        ]
    )
    assert stage2run.returncode == 0, stage2run.stdout + "\n" + stage2run.stderr
    assert stage2_run_plan.exists()
    assert "Stage 2 Run Plan" in stage2_run_plan.read_text(encoding="utf-8")


def test_repo_helper_stage1_plan_can_execute_with_deterministic_runner_and_write_log(tmp_path: Path) -> None:
    repo_root = _make_prompt_repo(tmp_path)
    run_log = repo_root / "STAGE1-RUN-LOG.md"
    stage1_plan = repo_root / "STAGE1-PLAN.md"

    result = _run(
        [
            str(REPO_HELPER_STAGE1_PLAN),
            "--repo-root",
            str(repo_root),
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
            "--require-tools",
            "python3",
        ]
    )

    assert result.returncode == 0, result.stdout + "\n" + result.stderr
    assert stage1_plan.exists()
    assert run_log.exists()
    log_text = run_log.read_text(encoding="utf-8")
    assert "# Stage 1 Execution Log" in log_text
    assert "PROMPT_01.txt" in log_text
    assert "PROMPT_02.txt" in log_text
    assert "- status: `success`" in log_text
    assert "RUN" in log_text


def test_repo_helper_stage1_plan_execute_stops_on_first_failure_and_logs_it(tmp_path: Path) -> None:
    repo_root = _make_prompt_repo(tmp_path)
    run_log = repo_root / "STAGE1-RUN-FAIL.md"

    result = _run(
        [
            str(REPO_HELPER_STAGE1_PLAN),
            "--repo-root",
            str(repo_root),
            "--prompts-dir",
            ".prompts",
            "--start",
            "1",
            "--end",
            "3",
            "--execute",
            "--runner-shell-template",
            (
                "python3 -c 'import os,sys; p=os.path.basename(sys.argv[1]); "
                "print(p); raise SystemExit(7 if p == \"PROMPT_02.txt\" else 0)' {prompt_path}"
            ),
            "--run-log",
            "STAGE1-RUN-FAIL.md",
            "--require-tools",
            "python3",
        ]
    )

    assert result.returncode == 7, result.stdout + "\n" + result.stderr
    assert run_log.exists()
    log_text = run_log.read_text(encoding="utf-8")
    assert "PROMPT_01.txt" in log_text
    assert "PROMPT_02.txt" in log_text
    assert "PROMPT_03.txt" not in log_text
    assert "- status: `failed`" in log_text
    assert "- returncode: `7`" in log_text


def test_repo_helper_stage1_plan_execute_enforces_guardrails(tmp_path: Path) -> None:
    repo_root = _make_prompt_repo(tmp_path)

    too_many = _run(
        [
            str(REPO_HELPER_STAGE1_PLAN),
            "--repo-root",
            str(repo_root),
            "--prompts-dir",
            ".prompts",
            "--start",
            "1",
            "--end",
            "1",
            "--execute",
            "--max-prompts",
            "1",
            "--runner-shell-template",
            "python3 -c 'print(\"ok\")' {prompt_path}",
            "--run-log",
            "STAGE1-RUN-LOG.md",
            "--require-tools",
            "python3",
        ]
    )
    assert too_many.returncode == 2
    assert "--max-prompts" in too_many.stdout

    outside_log = _run(
        [
            str(REPO_HELPER_STAGE1_PLAN),
            "--repo-root",
            str(repo_root),
            "--prompts-dir",
            ".prompts",
            "--start",
            "1",
            "--end",
            "1",
            "--execute",
            "--runner-shell-template",
            "python3 -c 'print(\"ok\")' {prompt_path}",
            "--run-log",
            "../outside-log.md",
            "--no-max-prompts",
            "--require-tools",
            "python3",
        ]
    )
    assert outside_log.returncode == 2
    assert "--allow-outside-repo-artifacts" in outside_log.stdout


def test_repo_helper_stage1_plan_execute_timeout_writes_run_log(tmp_path: Path) -> None:
    repo_root = _make_prompt_repo(tmp_path)
    run_log = repo_root / "STAGE1-TIMEOUT-LOG.md"

    result = _run(
        [
            str(REPO_HELPER_STAGE1_PLAN),
            "--repo-root",
            str(repo_root),
            "--prompts-dir",
            ".prompts",
            "--start",
            "1",
            "--end",
            "1",
            "--execute",
            "--runner-shell-template",
            "python3 -c 'import time; time.sleep(0.2)' {prompt_path}",
            "--runner-timeout-seconds",
            "0.05",
            "--run-log",
            "STAGE1-TIMEOUT-LOG.md",
            "--no-max-prompts",
            "--require-tools",
            "python3",
        ]
    )

    assert result.returncode == 124, result.stdout + "\n" + result.stderr
    assert run_log.exists()
    log_text = run_log.read_text(encoding="utf-8")
    assert "timed_out" in log_text
    assert "Timed out after 0.05 second(s)" in log_text
