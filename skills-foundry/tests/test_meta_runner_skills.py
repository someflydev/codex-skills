from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMMON_PATH = ROOT / "bin" / "_skills_common.py"
META_RUNNER_ROOT = ROOT / "skills" / "meta-runner"

SPEC = importlib.util.spec_from_file_location("skills_common_test_module_meta_runner", COMMON_PATH)
assert SPEC is not None
assert SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


REQUIRED_SKILL_IDS = {
    "meta-runner-bootstrap",
    "meta-runner-preflight-inspector",
    "meta-runner-stage-runner",
    "meta-runner-port-isolation",
    "meta-runner-test-stack-isolation",
    "meta-runner-operators-guide-author",
    "meta-runner-ui-audit-playwright",
    "meta-runner-postflight-analyzer",
    "meta-runner-preflight-inspector-alt",
    "meta-runner-stage-runner-alt",
    "meta-runner-postflight-analyzer-alt",
}


def _load_skill(path: Path) -> MODULE.SkillDocument:
    doc = MODULE.load_skill_document(path)
    return MODULE.validate_skill_document(doc, ROOT)


def test_meta_runner_required_skill_ids_exist() -> None:
    assert META_RUNNER_ROOT.exists(), f"Missing meta-runner root: {META_RUNNER_ROOT}"
    found = {
        p.parent.name
        for p in META_RUNNER_ROOT.rglob("SKILL.md")
    }
    missing = REQUIRED_SKILL_IDS - found
    assert not missing, f"Missing required meta-runner skills: {sorted(missing)}"


def test_meta_runner_skills_have_required_metadata_and_sections() -> None:
    for skill_path in sorted(META_RUNNER_ROOT.rglob("SKILL.md")):
        doc = _load_skill(skill_path)
        assert doc.front_matter_text is not None, f"Front matter missing: {skill_path}"
        for key in MODULE.REQUIRED_METADATA_KEYS:
            assert key in doc.metadata, f"{skill_path}: missing metadata key {key}"
        for section in MODULE.REQUIRED_SECTIONS:
            assert section in doc.section_map, f"{skill_path}: missing section {section}"


def test_meta_runner_skills_define_safety_contract_and_stop_signals() -> None:
    for skill_path in sorted(META_RUNNER_ROOT.rglob("SKILL.md")):
        doc = _load_skill(skill_path)
        safety_block = str(doc.metadata.get("safety", ""))
        assert "dry_run_supported:" in safety_block, f"{skill_path}: missing dry_run_supported in safety"
        assert "confirmation_points:" in safety_block, f"{skill_path}: missing confirmation_points in safety"

        failure_text = doc.section_map.get("Failure modes + recovery", "").lower()
        assert "stop" in failure_text or "halt" in failure_text, (
            f"{skill_path}: Failure modes section must include explicit stop/halt behavior"
        )
