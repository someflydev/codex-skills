from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FLOW_NEXT = ROOT / "bin" / "skills-flow-next"
FLOW_RENDER = ROOT / "bin" / "skills-flow-render"
FLOWS_ROOT = ROOT / "flows"


def _run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, capture_output=True, text=True)


def test_skills_flow_next_help_and_group_listing() -> None:
    help_result = _run([str(FLOW_NEXT), "--help"])
    assert help_result.returncode == 0
    assert "resolve the next invocation step" in help_result.stdout

    list_result = _run([str(FLOW_NEXT), "--list-groups"])
    assert list_result.returncode == 0, list_result.stdout + "\n" + list_result.stderr
    assert "meta-runner" in list_result.stdout
    assert "workflow" in list_result.stdout


def test_skills_flow_next_reports_next_step_for_lane() -> None:
    result = _run([str(FLOW_NEXT), "--group", "meta-runner", "--lane", "standard"])
    assert result.returncode == 0, result.stdout + "\n" + result.stderr
    assert "Group: meta-runner" in result.stdout
    assert "Lane: standard" in result.stdout
    assert "Next step: 1" in result.stdout
    assert "Next skill: meta-runner-bootstrap" in result.stdout


def test_skills_flow_next_mark_done_updates_state_file(tmp_path: Path) -> None:
    state_path = tmp_path / "skills-flow-state.json"
    result = _run(
        [
            str(FLOW_NEXT),
            "--group",
            "workflow",
            "--lane",
            "standard",
            "--state-file",
            str(state_path),
            "--mark-done",
        ]
    )
    assert result.returncode == 0, result.stdout + "\n" + result.stderr
    assert "Marked done step: 1" in result.stdout
    assert "Next step: 2" in result.stdout
    assert state_path.exists()

    state = json.loads(state_path.read_text(encoding="utf-8"))
    assert state["groups"]["workflow"]["standard"]["last_completed_step"] == 1


def test_skills_flow_render_writes_markdown(tmp_path: Path) -> None:
    output = tmp_path / "SKILL_FLOWS.md"
    result = _run([str(FLOW_RENDER), "--flows-root", str(FLOWS_ROOT), "--output", str(output)])
    assert result.returncode == 0, result.stdout + "\n" + result.stderr
    assert output.exists()
    text = output.read_text(encoding="utf-8")
    assert "# Skill Flows" in text
    assert "## meta-runner" in text
    assert "### Standard Lane" in text
    assert "### Alt Lane" in text
