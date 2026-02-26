#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


FOUNDRY_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = FOUNDRY_ROOT / "skills"
TEMPLATES_ROOT = FOUNDRY_ROOT / "templates" / "skill"
REPORTS_ROOT = FOUNDRY_ROOT / "reports"
DOCS_ROOT = FOUNDRY_ROOT / "docs"

REQUIRED_METADATA_KEYS = [
    "id",
    "name",
    "description",
    "version",
    "tags",
    "inputs",
    "expected_tools",
    "safety",
    "outputs",
]

REQUIRED_SECTIONS = [
    "When to use",
    "Inputs",
    "Procedure",
    "Success criteria",
    "Failure modes + recovery",
    "Examples",
]

HEADING_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
FRONT_MATTER_START = "---"


@dataclass
class ValidationMessage:
    level: str
    code: str
    message: str


@dataclass
class SkillDocument:
    path: Path
    text: str
    front_matter_text: str | None
    body_text: str
    metadata: dict[str, Any]
    section_map: dict[str, str]
    messages: list[ValidationMessage]

    @property
    def skill_id(self) -> str:
        return str(self.metadata.get("id") or self.path.parent.name)

    @property
    def has_errors(self) -> bool:
        return any(m.level == "ERROR" for m in self.messages)


def discover_skill_files(skills_root: Path) -> list[Path]:
    return sorted(skills_root.rglob("SKILL.md"))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def split_front_matter(text: str) -> tuple[str | None, str, list[ValidationMessage]]:
    msgs: list[ValidationMessage] = []
    lines = text.splitlines()
    if not lines or lines[0].strip() != FRONT_MATTER_START:
        msgs.append(ValidationMessage("ERROR", "missing_front_matter", "File must start with YAML front matter delimited by ---"))
        return None, text, msgs

    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == FRONT_MATTER_START:
            end_idx = i
            break
    if end_idx is None:
        msgs.append(ValidationMessage("ERROR", "unterminated_front_matter", "Front matter opening --- is not closed"))
        return None, text, msgs

    fm = "\n".join(lines[1:end_idx])
    body = "\n".join(lines[end_idx + 1 :])
    return fm, body, msgs


def _parse_scalar(value: str) -> Any:
    v = value.strip()
    if not v:
        return ""
    if v.lower() in {"true", "false"}:
        return v.lower() == "true"
    if re.fullmatch(r"\d+", v):
        return int(v)
    if v.startswith("[") and v.endswith("]"):
        inner = v[1:-1].strip()
        if not inner:
            return []
        parts = [p.strip() for p in inner.split(",")]
        cleaned: list[str] = []
        for p in parts:
            if (p.startswith('"') and p.endswith('"')) or (p.startswith("'") and p.endswith("'")):
                cleaned.append(p[1:-1])
            else:
                cleaned.append(p)
        return cleaned
    if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
        return v[1:-1]
    return v


def parse_front_matter_minimal(front_matter: str) -> tuple[dict[str, Any], list[ValidationMessage]]:
    metadata: dict[str, Any] = {}
    msgs: list[ValidationMessage] = []
    lines = front_matter.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        if line.startswith(" "):
            msgs.append(ValidationMessage("ERROR", "bad_indentation", f"Unexpected indented line in front matter: {line!r}"))
            i += 1
            continue
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):(?:\s*(.*))?$", line)
        if not m:
            msgs.append(ValidationMessage("ERROR", "bad_yaml_line", f"Could not parse front matter line: {line!r}"))
            i += 1
            continue
        key, raw_val = m.group(1), (m.group(2) or "")
        if raw_val == "":
            block_lines: list[str] = []
            i += 1
            while i < len(lines) and (lines[i].startswith("  ") or not lines[i].strip()):
                block_lines.append(lines[i])
                i += 1
            # Keep block text to avoid depending on external YAML libraries.
            metadata[key] = "\n".join(block_lines).rstrip("\n")
            continue
        metadata[key] = _parse_scalar(raw_val)
        i += 1
    return metadata, msgs


def extract_list_items_from_front_matter_block(front_matter: str, key: str) -> list[str]:
    lines = front_matter.splitlines()
    items: list[str] = []
    in_block = False
    block_indent = 0

    inline_match = re.search(rf"(?m)^{re.escape(key)}:\s*(\[[^\n]*\])\s*$", front_matter)
    if inline_match:
        parsed = _parse_scalar(inline_match.group(1))
        if isinstance(parsed, list):
            return [str(x) for x in parsed]

    for line in lines:
        if not in_block:
            if re.match(rf"^{re.escape(key)}:\s*$", line):
                in_block = True
            continue

        if not line.strip():
            continue
        current_indent = len(line) - len(line.lstrip(" "))
        if current_indent == 0:
            break
        if block_indent == 0:
            block_indent = current_indent
        if current_indent < block_indent:
            break
        stripped = line.strip()
        if stripped.startswith("- "):
            items.append(stripped[2:].strip())
    return items


def classify_missing_output_path_warning(token: str) -> ValidationMessage:
    normalized = token.replace("\\", "/").lstrip("./")
    if normalized.startswith("skills/"):
        return ValidationMessage(
            "WARN",
            "missing_output_path_install_target_relative",
            f"Referenced output path does not exist in repo root (likely install-target-relative): {token}",
        )
    if normalized.startswith(
        (
            "skills-foundry/reports/",
            "reports/",
            "docs/",
            "data/",
            "schemas/",
            "manifests/",
        )
    ):
        return ValidationMessage(
            "WARN",
            "missing_output_path_expected_future",
            f"Referenced output path does not exist yet (likely future-generated artifact): {token}",
        )
    return ValidationMessage(
        "WARN",
        "missing_output_path",
        f"Referenced output path does not exist yet (best effort): {token}",
    )


def extract_sections(body_text: str) -> dict[str, str]:
    matches = list(HEADING_RE.finditer(body_text))
    sections: dict[str, str] = {}
    for idx, match in enumerate(matches):
        title = match.group(1).strip()
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(body_text)
        sections[title] = body_text[start:end].strip()
    return sections


def load_skill_document(path: Path) -> SkillDocument:
    text = read_text(path)
    fm_text, body_text, msgs = split_front_matter(text)
    metadata: dict[str, Any] = {}
    if fm_text is not None:
        parsed, parse_msgs = parse_front_matter_minimal(fm_text)
        metadata = parsed
        msgs.extend(parse_msgs)
    sections = extract_sections(body_text)
    return SkillDocument(
        path=path,
        text=text,
        front_matter_text=fm_text,
        body_text=body_text,
        metadata=metadata,
        section_map=sections,
        messages=msgs,
    )


def _normalize_section_name(name: str) -> str:
    return re.sub(r"\s+", " ", name.strip().lower())


def validate_skill_document(doc: SkillDocument, repo_root: Path) -> SkillDocument:
    msgs = list(doc.messages)
    fm_text = doc.front_matter_text or ""

    for key in REQUIRED_METADATA_KEYS:
        if key not in doc.metadata:
            msgs.append(ValidationMessage("ERROR", "missing_metadata_key", f"Missing required metadata key: {key}"))

    skill_id = str(doc.metadata.get("id", ""))
    if skill_id and not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", skill_id):
        msgs.append(ValidationMessage("ERROR", "bad_skill_id", "Metadata id must be stable kebab-case"))

    tags = doc.metadata.get("tags")
    if tags is not None and not isinstance(tags, list):
        msgs.append(ValidationMessage("ERROR", "bad_tags_type", "tags must be an inline YAML list (e.g. [tag-a, tag-b]) in this scaffold"))

    normalized = {_normalize_section_name(k): k for k in doc.section_map}
    for required in REQUIRED_SECTIONS:
        if _normalize_section_name(required) not in normalized:
            msgs.append(ValidationMessage("ERROR", "missing_section", f"Missing required section: {required}"))

    if "safety" in doc.metadata:
        for subkey in ["dry_run_supported", "destructive_actions", "confirmation_points"]:
            if f"{subkey}:" not in fm_text:
                msgs.append(ValidationMessage("ERROR", "missing_safety_subkey", f"safety must include {subkey}"))

    if "inputs" in doc.metadata:
        for token in ["- name:", "type:", "required:", "examples:"]:
            if token not in fm_text:
                msgs.append(ValidationMessage("ERROR", "missing_input_shape", f"inputs must include field token {token}"))

    if "outputs" in doc.metadata:
        for ref in extract_list_items_from_front_matter_block(fm_text, "outputs"):
            token = ref.split()[0].strip("`,'\"")
            if token.startswith("http://") or token.startswith("https://"):
                continue
            if "<" in token or ">" in token:
                continue
            path = (repo_root / token).resolve() if not Path(token).is_absolute() else Path(token)
            if not path.exists():
                msgs.append(classify_missing_output_path_warning(token))

    doc.messages = msgs
    return doc


def validate_skills(skills_root: Path, repo_root: Path) -> list[SkillDocument]:
    docs: list[SkillDocument] = []
    for path in discover_skill_files(skills_root):
        docs.append(validate_skill_document(load_skill_document(path), repo_root))
    return docs


def format_validate_summary(docs: list[SkillDocument]) -> str:
    total = len(docs)
    errors = sum(1 for d in docs for m in d.messages if m.level == "ERROR")
    warns = sum(1 for d in docs for m in d.messages if m.level == "WARN")
    lines = [f"Validated {total} skills: {errors} error(s), {warns} warning(s)"]
    for doc in docs:
        if not doc.messages:
            lines.append(f"- OK {doc.path}")
            continue
        lines.append(f"- {doc.path}")
        for msg in doc.messages:
            lines.append(f"  [{msg.level}] {msg.code}: {msg.message}")
    return "\n".join(lines)


def validation_failed(docs: list[SkillDocument]) -> bool:
    return any(doc.has_errors for doc in docs)


def _count_numbered_steps(text: str) -> int:
    return len(re.findall(r"(?m)^\d+\.\s+", text))


def lint_skill(doc: SkillDocument) -> dict[str, Any]:
    issues: list[str] = []
    fixes: list[str] = []
    completeness = 100
    excellence = 10

    normalized_sections = {_normalize_section_name(k): v for k, v in doc.section_map.items()}

    if doc.has_errors:
        err_count = sum(1 for m in doc.messages if m.level == "ERROR")
        completeness -= min(60, err_count * 10)
        excellence -= min(5, err_count)
        issues.append("Validation errors present")
        fixes.append("Run skills-validate and fix missing metadata/sections before linting for quality")

    for required in REQUIRED_SECTIONS:
        if _normalize_section_name(required) not in normalized_sections:
            completeness -= 8
            excellence -= 1
            issues.append(f"Missing section: {required}")
            fixes.append(f"Add a `## {required}` section with concrete content")

    procedure_body = normalized_sections.get("procedure", "")
    step_count = _count_numbered_steps(procedure_body)
    if step_count == 0:
        completeness -= 15
        excellence -= 2
        issues.append("Procedure steps are not numbered")
        fixes.append("Rewrite the Procedure section as explicit numbered steps (1., 2., 3.)")
    elif step_count < 3:
        completeness -= 8
        excellence -= 1
        issues.append("Procedure is too short to be executable")
        fixes.append("Expand the Procedure section to at least 3 concrete numbered steps")

    fm_text = doc.front_matter_text or ""
    if "expected_tools:" not in fm_text:
        completeness -= 10
        excellence -= 1
        issues.append("expected_tools is missing")
        fixes.append("Add `expected_tools` to front matter with the tools the skill depends on")

    if "confirmation_points:" not in fm_text:
        completeness -= 8
        excellence -= 1
        issues.append("Safety confirmation points are missing")
        fixes.append("Add `safety.confirmation_points` with explicit approval checkpoints")

    if "examples:" not in fm_text and "## Examples" not in doc.body_text:
        completeness -= 10
        excellence -= 1
        issues.append("Examples are missing")
        fixes.append("Add realistic examples in metadata and the Examples section")

    inputs_block = doc.metadata.get("inputs", "")
    inputs_blob = inputs_block if isinstance(inputs_block, str) else json.dumps(inputs_block)
    for token, label in [("type:", "typed inputs"), ("examples:", "input examples")]:
        if token not in inputs_blob and token not in fm_text:
            completeness -= 8
            excellence -= 1
            issues.append(f"Inputs missing {label}")
            fixes.append("Ensure each input includes `type` and `examples` fields")
            break

    examples_body = normalized_sections.get("examples", "")
    if len(examples_body) < 60:
        completeness -= 6
        excellence -= 1
        issues.append("Examples section is too thin")
        fixes.append("Add realistic example scenarios with concrete inputs and outcomes")

    failure_body = normalized_sections.get("failure modes + recovery", "")
    if failure_body and "recover" not in failure_body.lower() and "retry" not in failure_body.lower():
        completeness -= 4
        excellence -= 1
        issues.append("Failure modes section lacks recovery guidance")
        fixes.append("Add explicit recovery or retry steps to Failure modes + recovery")

    combined_text = (str(doc.metadata.get("description", "")) + "\n" + normalized_sections.get("when to use", "")).lower()
    if any(term in combined_text for term in ["everything", "all tasks", "do anything", "universal"]):
        completeness -= 6
        excellence -= 2
        issues.append("Scope appears too broad")
        fixes.append("Narrow the skill to one job and move extra responsibilities into separate skills")

    if any(term in procedure_body.lower() for term in ["make it great", "do the thing", "improve as needed"]):
        completeness -= 6
        excellence -= 2
        issues.append("Procedure is vague / not executable")
        fixes.append("Replace vague instructions with explicit commands, files, and verification steps")

    description_text = str(doc.metadata.get("description", "")).strip().lower()
    when_to_use_body = normalized_sections.get("when to use", "")
    if description_text in {"describe the skill purpose here.", "describe the skill purpose here"}:
        completeness -= 12
        excellence -= 3
        issues.append("Placeholder description text remains")
        fixes.append("Replace the template placeholder description with a specific one-line value proposition")
    if "use this skill when you need a focused, repeatable workflow for `" in when_to_use_body.lower():
        completeness -= 8
        excellence -= 2
        issues.append("When to use section still contains template wording")
        fixes.append("Rewrite `When to use` with a concrete scenario and trigger conditions")
    if "example 1: run on a small repo" in examples_body.lower() and "example 2: run in dry-run mode first" in examples_body.lower():
        completeness -= 8
        excellence -= 2
        issues.append("Examples section appears to be uncustomized template content")
        fixes.append("Replace template examples with realistic, task-specific scenarios and outcomes")

    completeness = max(0, completeness)
    excellence = max(0, min(10, excellence))
    top_issues = issues[:5]
    suggested_fixes = fixes[:5]

    return {
        "skill_id": doc.skill_id,
        "path": str(doc.path),
        "completeness_score_100": completeness,
        "excellence_score_10": excellence,
        "top_issues": top_issues,
        "suggested_fixes": suggested_fixes,
        "validation_errors": [m.message for m in doc.messages if m.level == "ERROR"],
        "validation_warnings": [m.message for m in doc.messages if m.level == "WARN"],
    }


def lint_skills(skills_root: Path, repo_root: Path) -> list[dict[str, Any]]:
    docs = validate_skills(skills_root, repo_root)
    return [lint_skill(doc) for doc in docs]


def write_lint_reports(results: list[dict[str, Any]], reports_dir: Path) -> tuple[Path, Path]:
    reports_dir.mkdir(parents=True, exist_ok=True)
    json_path = reports_dir / "skills-lint.json"
    md_path = reports_dir / "skills-lint.md"
    json_path.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")

    lines = ["# Skills Lint Report", "", f"Total skills: {len(results)}", ""]
    for item in results:
        lines.append(f"## {item['skill_id']}")
        lines.append(f"- Path: `{item['path']}`")
        lines.append(f"- completeness_score_100: {item['completeness_score_100']}")
        lines.append(f"- excellence_score_10: {item['excellence_score_10']}")
        if item["top_issues"]:
            lines.append("- top_issues:")
            for issue in item["top_issues"]:
                lines.append(f"  - {issue}")
        else:
            lines.append("- top_issues: []")
        if item["suggested_fixes"]:
            lines.append("- suggested_fixes:")
            for fix in item["suggested_fixes"]:
                lines.append(f"  - {fix}")
        else:
            lines.append("- suggested_fixes: []")
        lines.append("")
    md_path.write_text("\n".join(lines), encoding="utf-8")
    return json_path, md_path


def render_template_text(template_text: str, replacements: dict[str, str]) -> str:
    rendered = template_text
    for key, value in replacements.items():
        rendered = rendered.replace("{{" + key + "}}", value)
    return rendered


def ensure_kebab_case(value: str) -> bool:
    return bool(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value))
