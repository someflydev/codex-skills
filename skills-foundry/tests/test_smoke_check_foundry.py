from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
SMOKE_CHECK_CLI = ROOT / "bin" / "smoke-check-foundry"


def test_smoke_check_foundry_help_runs() -> None:
    result = subprocess.run(
        [str(SMOKE_CHECK_CLI), "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + "\n" + result.stderr
    assert "Usage: smoke-check-foundry" in result.stdout
    assert "--dry-run-only" in result.stdout


def test_smoke_check_foundry_invalid_flag_exits_non_zero() -> None:
    result = subprocess.run(
        [str(SMOKE_CHECK_CLI), "--definitely-not-a-real-flag"],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "unknown argument" in result.stderr
    assert "Usage: smoke-check-foundry" in result.stderr
