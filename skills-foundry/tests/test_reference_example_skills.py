from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMMON_PATH = ROOT / "bin" / "_skills_common.py"

SPEC = importlib.util.spec_from_file_location("skills_common_reference_examples", COMMON_PATH)
assert SPEC is not None
assert SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


NEW_SKILLS = {
    "workflow": [
        "prompt-resume-reconciler",
        "prompt-commit-batch-planner",
    ],
    "core": [
        "manual-command-prooflogger",
    ],
    "meta-runner": [
        "meta-runner-reference-example-curator",
    ],
}


def _load_validated_skill(path: Path) -> MODULE.SkillDocument:
    doc = MODULE.load_skill_document(path)
    return MODULE.validate_skill_document(doc, ROOT)


def test_new_reference_example_skill_contracts_are_valid() -> None:
    for category, skill_ids in NEW_SKILLS.items():
        for skill_id in skill_ids:
            skill_dir = ROOT / "skills" / category / skill_id
            skill_path = skill_dir / "SKILL.md"
            checklist_path = skill_dir / "CHECKLIST.md"
            examples_path = skill_dir / "EXAMPLES.md"

            assert skill_path.exists(), f"Missing skill contract: {skill_path}"
            assert checklist_path.exists(), f"Missing checklist: {checklist_path}"
            assert examples_path.exists(), f"Missing examples: {examples_path}"

            doc = _load_validated_skill(skill_path)
            error_messages = [m for m in doc.messages if m.level == "ERROR"]
            assert not error_messages, f"Validation errors in {skill_path}: {error_messages}"


def test_new_reference_examples_are_wired_into_flows_and_rendered_docs() -> None:
    core_flow = json.loads((ROOT / "flows" / "core.json").read_text(encoding="utf-8"))
    workflow_flow = json.loads((ROOT / "flows" / "workflow.json").read_text(encoding="utf-8"))
    meta_flow = json.loads((ROOT / "flows" / "meta-runner.json").read_text(encoding="utf-8"))

    def lane_skill_ids(flow: dict, lane: str) -> set[str]:
        return {step["skill_id"] for step in flow["lanes"][lane]}

    assert "manual-command-prooflogger" in lane_skill_ids(core_flow, "standard")
    assert "manual-command-prooflogger" in lane_skill_ids(core_flow, "alt")

    assert "prompt-resume-reconciler" in lane_skill_ids(workflow_flow, "standard")
    assert "prompt-commit-batch-planner" in lane_skill_ids(workflow_flow, "standard")
    assert "prompt-resume-reconciler" in lane_skill_ids(workflow_flow, "alt")
    assert "prompt-commit-batch-planner" in lane_skill_ids(workflow_flow, "alt")

    assert "meta-runner-reference-example-curator" in lane_skill_ids(meta_flow, "standard")
    assert "meta-runner-reference-example-curator" in lane_skill_ids(meta_flow, "alt")

    rendered = (ROOT / "docs" / "SKILL_FLOWS.md").read_text(encoding="utf-8")
    for skill_id in (
        "manual-command-prooflogger",
        "prompt-resume-reconciler",
        "prompt-commit-batch-planner",
        "meta-runner-reference-example-curator",
    ):
        assert skill_id in rendered
