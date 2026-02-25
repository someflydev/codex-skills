from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "bin" / "skills-lint"


def test_skills_lint_stub_help_runs() -> None:
    result = subprocess.run([str(CLI), "--help"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "Stub CLI" in result.stdout


def test_skills_lint_stub_no_args_prints_next_steps() -> None:
    result = subprocess.run([str(CLI)], capture_output=True, text=True)
    assert result.returncode == 0
    assert "Next steps:" in result.stdout
