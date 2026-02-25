#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from _skills_common import load_skill_document, validate_skills, validation_failed, lint_skills, write_lint_reports


@dataclass
class SkillEntry:
    skill_id: str
    category: str
    source_dir: Path
    source_skill_md: Path
    description: str
    tags: list[str]
    expected_tools: list[str]
    input_names: list[str]


@dataclass
class SyncPlan:
    create: list[SkillEntry]
    update: list[SkillEntry]
    unchanged: list[SkillEntry]
    would_prune: list[Path]


def _as_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(v) for v in value]
    if isinstance(value, str):
        inner = value.strip()
        if inner.startswith("[") and inner.endswith("]"):
            parts = [p.strip().strip('"').strip("'") for p in inner[1:-1].split(",") if p.strip()]
            return parts
    return []


def _parse_input_names(front_matter_text: str | None) -> list[str]:
    if not front_matter_text:
        return []
    names: list[str] = []
    for line in front_matter_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- name:"):
            names.append(stripped.split(":", 1)[1].strip().strip('"').strip("'"))
    return names


def collect_skill_entries(skills_root: Path) -> list[SkillEntry]:
    entries: list[SkillEntry] = []
    for skill_md in sorted(skills_root.rglob("SKILL.md")):
        doc = load_skill_document(skill_md)
        category = skill_md.parent.parent.name if skill_md.parent.parent != skills_root else "uncategorized"
        entries.append(
            SkillEntry(
                skill_id=str(doc.metadata.get("id") or skill_md.parent.name),
                category=category,
                source_dir=skill_md.parent,
                source_skill_md=skill_md,
                description=str(doc.metadata.get("description") or ""),
                tags=_as_list(doc.metadata.get("tags")),
                expected_tools=_as_list(doc.metadata.get("expected_tools")),
                input_names=_parse_input_names(doc.front_matter_text),
            )
        )
    return entries


def render_skills_catalog(entries: list[SkillEntry], output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Skills Catalog", "", f"Total skills: {len(entries)}", ""]
    by_category: dict[str, list[SkillEntry]] = {}
    for entry in entries:
        by_category.setdefault(entry.category, []).append(entry)
    for category in sorted(by_category):
        lines.append(f"## {category}")
        lines.append("")
        for entry in sorted(by_category[category], key=lambda e: e.skill_id):
            lines.append(f"### {entry.skill_id}")
            lines.append(f"- Description: {entry.description or '(missing description)'}")
            lines.append(f"- Tags: {', '.join(entry.tags) if entry.tags else '(none)'}")
            lines.append(
                f"- Inputs: {', '.join(entry.input_names) if entry.input_names else '(no inputs parsed)'}"
            )
            lines.append(
                f"- Expected tools: {', '.join(entry.expected_tools) if entry.expected_tools else '(none)'}"
            )
            lines.append(f"- Path: `{entry.source_skill_md}`")
            lines.append("")
    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path


def _load_target_skill_map(target_root: Path) -> dict[str, Path]:
    mapping: dict[str, Path] = {}
    if not target_root.exists():
        return mapping
    for child in sorted(target_root.iterdir()):
        if child.name.startswith("."):
            continue
        skill_md = child / "SKILL.md"
        if child.is_dir() and skill_md.exists():
            mapping[child.name] = child
    return mapping


def _same_skill_content(source_skill_md: Path, target_skill_md: Path) -> bool:
    if not target_skill_md.exists():
        return False
    return source_skill_md.read_text(encoding="utf-8") == target_skill_md.read_text(encoding="utf-8")


def build_sync_plan(entries: list[SkillEntry], target_root: Path, only_ids: list[str] | None = None, prune: bool = False) -> SyncPlan:
    selected = [e for e in entries if not only_ids or e.skill_id in set(only_ids)]
    target_map = _load_target_skill_map(target_root)

    create: list[SkillEntry] = []
    update: list[SkillEntry] = []
    unchanged: list[SkillEntry] = []
    for entry in selected:
        target_dir = target_root / entry.skill_id
        target_skill_md = target_dir / "SKILL.md"
        if not target_dir.exists():
            create.append(entry)
        elif _same_skill_content(entry.source_skill_md, target_skill_md):
            unchanged.append(entry)
        else:
            update.append(entry)

    would_prune: list[Path] = []
    if prune and not only_ids:
        source_ids = {e.skill_id for e in entries}
        for skill_id, path in target_map.items():
            if skill_id not in source_ids:
                would_prune.append(path)

    return SyncPlan(create=create, update=update, unchanged=unchanged, would_prune=sorted(would_prune))


def print_sync_plan(plan: SyncPlan) -> None:
    print("Sync plan:")
    print(f"- create: {len(plan.create)}")
    for e in plan.create:
        print(f"  - {e.skill_id}")
    print(f"- update: {len(plan.update)}")
    for e in plan.update:
        print(f"  - {e.skill_id}")
    print(f"- unchanged: {len(plan.unchanged)}")
    for e in plan.unchanged:
        print(f"  - {e.skill_id}")
    print(f"- would-prune: {len(plan.would_prune)}")
    for p in plan.would_prune:
        print(f"  - {p}")


def _timestamp() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def default_backup_dir(target_root: Path) -> Path:
    return target_root.parent / f"skills-backups-{_timestamp()}"


def _backup_existing_skill_md(target_dir: Path, backup_dir: Path, dry_run: bool) -> None:
    skill_md = target_dir / "SKILL.md"
    if not skill_md.exists():
        return
    backup_path = backup_dir / target_dir.name / "SKILL.md"
    if dry_run:
        print(f"- would backup: {skill_md} -> {backup_path}")
        return
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(skill_md, backup_path)


def _remove_target(target_dir: Path, dry_run: bool) -> None:
    if not target_dir.exists() and not target_dir.is_symlink():
        return
    if dry_run:
        print(f"- would remove existing target: {target_dir}")
        return
    if target_dir.is_symlink() or target_dir.is_file():
        target_dir.unlink()
    else:
        shutil.rmtree(target_dir)


def _sync_one(entry: SkillEntry, target_root: Path, strategy: str, backup_dir: Path, dry_run: bool) -> None:
    target_dir = target_root / entry.skill_id
    if target_dir.exists() or target_dir.is_symlink():
        _backup_existing_skill_md(target_dir, backup_dir, dry_run)
        _remove_target(target_dir, dry_run)

    if dry_run:
        print(f"- would {strategy}: {entry.source_dir} -> {target_dir}")
        return

    target_root.mkdir(parents=True, exist_ok=True)
    if strategy == "copy":
        shutil.copytree(entry.source_dir, target_dir)
    elif strategy == "symlink":
        target_dir.symlink_to(entry.source_dir.resolve(), target_is_directory=True)
    else:
        raise ValueError(f"Unknown strategy: {strategy}")


def _prune_targets(paths: list[Path], backup_dir: Path, dry_run: bool) -> None:
    for path in paths:
        _backup_existing_skill_md(path, backup_dir, dry_run)
        _remove_target(path, dry_run)


def write_target_index(entries: list[SkillEntry], target_root: Path, dry_run: bool) -> Path:
    index_path = target_root / "INDEX.md"
    by_category: dict[str, list[SkillEntry]] = {}
    for entry in entries:
        by_category.setdefault(entry.category, []).append(entry)
    lines = ["# Skill Index", ""]
    for category in sorted(by_category):
        lines.append(f"## {category}")
        for entry in sorted(by_category[category], key=lambda e: e.skill_id):
            desc = entry.description or "(missing description)"
            lines.append(f"- `{entry.skill_id}`: {desc}")
        lines.append("")
    if dry_run:
        print(f"- would write index: {index_path}")
        return index_path
    target_root.mkdir(parents=True, exist_ok=True)
    index_path.write_text("\n".join(lines), encoding="utf-8")
    return index_path


def run_validate_and_lint_for_sync(skills_root: Path, repo_root: Path, reports_dir: Path) -> tuple[list[SkillEntry], list[dict[str, Any]]]:
    docs = validate_skills(skills_root, repo_root)
    if validation_failed(docs):
        raise RuntimeError("Validation failed; refusing to sync")
    lint_results = lint_skills(skills_root, repo_root)
    write_lint_reports(lint_results, reports_dir)
    entries = collect_skill_entries(skills_root)
    return entries, lint_results


def apply_sync(
    entries: list[SkillEntry],
    plan: SyncPlan,
    target_root: Path,
    strategy: str,
    backup_dir: Path,
    prune: bool,
    dry_run: bool,
) -> None:
    for entry in plan.create + plan.update:
        _sync_one(entry, target_root=target_root, strategy=strategy, backup_dir=backup_dir, dry_run=dry_run)
    if prune and plan.would_prune:
        _prune_targets(plan.would_prune, backup_dir=backup_dir, dry_run=dry_run)
    write_target_index([*plan.create, *plan.update, *plan.unchanged], target_root=target_root, dry_run=dry_run)
