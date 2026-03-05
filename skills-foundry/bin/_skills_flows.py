#!/usr/bin/env python3
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


FOUNDRY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FLOWS_ROOT = FOUNDRY_ROOT / "flows"
DEFAULT_DOC_OUTPUT = FOUNDRY_ROOT / "docs" / "SKILL_FLOWS.md"
DEFAULT_STATE_FILE = Path(".skills-flow-state.json")

SUPPORTED_LANES = ("standard", "alt")


@dataclass(frozen=True)
class FlowStep:
    step: int
    skill_id: str
    why: str
    verify_cmd: str


@dataclass(frozen=True)
class FlowManifest:
    path: Path
    group_id: str
    description: str
    lanes: dict[str, list[FlowStep]]


def _read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: manifest root must be a JSON object")
    return data


def _normalize_steps(raw_steps: list[Any], *, group_id: str, lane: str, path: Path) -> list[FlowStep]:
    steps: list[FlowStep] = []
    for idx, item in enumerate(raw_steps, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"{path}: {group_id}/{lane} step {idx} must be an object")
        skill_id = str(item.get("skill_id", "")).strip()
        if not skill_id:
            raise ValueError(f"{path}: {group_id}/{lane} step {idx} missing skill_id")
        step_num = item.get("step", idx)
        if not isinstance(step_num, int) or step_num <= 0:
            raise ValueError(f"{path}: {group_id}/{lane} step {idx} has invalid step number")
        why = str(item.get("why", "")).strip() or "No rationale provided."
        verify_cmd = str(item.get("verify_cmd", "")).strip() or "(none)"
        steps.append(FlowStep(step=step_num, skill_id=skill_id, why=why, verify_cmd=verify_cmd))

    steps.sort(key=lambda s: s.step)
    expected = list(range(1, len(steps) + 1))
    actual = [s.step for s in steps]
    if actual != expected:
        raise ValueError(
            f"{path}: {group_id}/{lane} step numbers must be contiguous 1..N (got {actual})"
        )
    return steps


def load_manifest(path: Path) -> FlowManifest:
    data = _read_json(path)
    group_id = str(data.get("group_id", "")).strip()
    if not group_id:
        raise ValueError(f"{path}: missing group_id")
    description = str(data.get("description", "")).strip() or "No description provided."
    lanes_raw = data.get("lanes")
    if not isinstance(lanes_raw, dict):
        raise ValueError(f"{path}: missing lanes object")

    lanes: dict[str, list[FlowStep]] = {}
    for lane in SUPPORTED_LANES:
        raw_steps = lanes_raw.get(lane)
        if not isinstance(raw_steps, list) or not raw_steps:
            raise ValueError(f"{path}: lane '{lane}' must be a non-empty array")
        lanes[lane] = _normalize_steps(raw_steps, group_id=group_id, lane=lane, path=path)

    return FlowManifest(path=path, group_id=group_id, description=description, lanes=lanes)


def load_manifests(flows_root: Path) -> list[FlowManifest]:
    if not flows_root.exists():
        return []
    manifests: list[FlowManifest] = []
    for path in sorted(flows_root.glob("*.json")):
        manifests.append(load_manifest(path))
    return manifests


def manifest_by_group(manifests: list[FlowManifest], group_id: str) -> FlowManifest:
    for manifest in manifests:
        if manifest.group_id == group_id:
            return manifest
    raise KeyError(group_id)


def list_groups(manifests: list[FlowManifest]) -> list[tuple[str, str]]:
    return [(m.group_id, m.description) for m in sorted(manifests, key=lambda item: item.group_id)]


def read_state(state_file: Path) -> dict[str, Any]:
    if not state_file.exists():
        return {"groups": {}}
    data = json.loads(state_file.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return {"groups": {}}
    groups = data.get("groups")
    if not isinstance(groups, dict):
        data["groups"] = {}
    return data


def write_state(state_file: Path, state: dict[str, Any]) -> None:
    state_file.parent.mkdir(parents=True, exist_ok=True)
    state_file.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def get_completed_step(state: dict[str, Any], group_id: str, lane: str) -> int:
    groups = state.get("groups", {})
    group_state = groups.get(group_id, {})
    lane_state = group_state.get(lane, {})
    completed = lane_state.get("last_completed_step", 0)
    if isinstance(completed, int) and completed >= 0:
        return completed
    return 0


def set_completed_step(state: dict[str, Any], group_id: str, lane: str, completed_step: int) -> None:
    groups = state.setdefault("groups", {})
    group_state = groups.setdefault(group_id, {})
    lane_state = group_state.setdefault(lane, {})
    lane_state["last_completed_step"] = completed_step


@dataclass(frozen=True)
class NextStepResolution:
    completed_step: int
    next_step: FlowStep | None
    marked_done_step: int | None


def resolve_next_step(
    manifest: FlowManifest,
    lane: str,
    *,
    from_step: int | None,
    state: dict[str, Any],
    mark_done: bool,
) -> NextStepResolution:
    steps = manifest.lanes[lane]
    max_step = len(steps)

    completed = from_step if from_step is not None else get_completed_step(state, manifest.group_id, lane)
    if completed < 0 or completed > max_step:
        raise ValueError(f"completed step {completed} is out of range 0..{max_step}")

    marked_done_step: int | None = None
    if mark_done:
        if from_step is not None:
            marked_done_step = completed
        else:
            marked_done_step = completed + 1 if completed < max_step else completed
        set_completed_step(state, manifest.group_id, lane, marked_done_step)
        completed = marked_done_step

    next_num = completed + 1
    next_step = steps[next_num - 1] if 1 <= next_num <= max_step else None
    return NextStepResolution(completed_step=completed, next_step=next_step, marked_done_step=marked_done_step)


def render_flows_markdown(manifests: list[FlowManifest]) -> str:
    lines: list[str] = []
    lines.append("# Skill Flows")
    lines.append("")
    lines.append("Ordered invocation lanes for skill groups. Keep skill IDs stable; ordering lives in flow manifests.")
    lines.append("")

    for manifest in sorted(manifests, key=lambda item: item.group_id):
        lines.append(f"## {manifest.group_id}")
        lines.append("")
        lines.append(manifest.description)
        lines.append("")
        for lane in SUPPORTED_LANES:
            lines.append(f"### {lane.title()} Lane")
            lines.append("")
            lines.append("| Step | Skill ID | Why | Verify Command |")
            lines.append("|---|---|---|---|")
            for step in manifest.lanes[lane]:
                lines.append(
                    f"| {step.step} | `{step.skill_id}` | {step.why} | `{step.verify_cmd}` |"
                )
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"
