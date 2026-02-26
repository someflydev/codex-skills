#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


PROMPT_RE = re.compile(r"^PROMPT_(\d+)(?:_s)?\.txt$")


@dataclass
class PromptFile:
    path: Path
    number: int
    is_system: bool


def _resolve_repo_root(repo_root: Path) -> Path:
    return repo_root.resolve()


def _resolve_prompts_dir(repo_root: Path, prompts_dir: Path) -> Path:
    if prompts_dir.is_absolute():
        return prompts_dir
    return (repo_root / prompts_dir).resolve()


def discover_prompts(prompts_dir: Path) -> tuple[list[PromptFile], list[Path]]:
    prompt_files: list[PromptFile] = []
    unparseable: list[Path] = []
    if not prompts_dir.exists():
        return prompt_files, unparseable

    for path in sorted(prompts_dir.iterdir()):
        if not path.is_file():
            continue
        if not path.name.startswith("PROMPT_") or path.suffix != ".txt":
            continue
        match = PROMPT_RE.match(path.name)
        if not match:
            unparseable.append(path)
            continue
        prompt_files.append(
            PromptFile(
                path=path,
                number=int(match.group(1)),
                is_system=path.name.endswith("_s.txt"),
            )
        )
    return prompt_files, unparseable


def prompt_number_gaps(prompts: list[PromptFile]) -> list[int]:
    numbers = sorted({p.number for p in prompts})
    gaps: list[int] = []
    if not numbers:
        return gaps
    for n in range(numbers[0], numbers[-1] + 1):
        if n not in numbers:
            gaps.append(n)
    return gaps


def tool_status(tool_names: list[str]) -> tuple[list[str], list[str]]:
    present: list[str] = []
    missing: list[str] = []
    for tool in tool_names:
        (present if shutil.which(tool) else missing).append(tool)
    return present, missing


def git_status_short(repo_root: Path) -> str | None:
    git_dir = repo_root / ".git"
    if not git_dir.exists():
        return None
    proc = subprocess.run(
        ["git", "-C", str(repo_root), "status", "--short"],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        return None
    return proc.stdout.strip()


def _render_prompt_inventory_md(
    title: str,
    repo_root: Path,
    prompts_dir: Path,
    prompts: list[PromptFile],
    unparseable: list[Path],
    gaps: list[int],
) -> str:
    lines = [f"# {title}", "", f"- repo_root: `{repo_root}`", f"- prompts_dir: `{prompts_dir}`", ""]
    lines.append(f"- prompt_files: {len(prompts)}")
    lines.append(f"- unparseable_prompt_files: {len(unparseable)}")
    lines.append(f"- numeric_gaps: {', '.join(f'{n:02d}' for n in gaps) if gaps else '(none)'}")
    lines.append("")
    lines.append("## Prompt Files")
    lines.append("")
    for prompt in prompts:
        kind = "system" if prompt.is_system else "task"
        lines.append(f"- `{prompt.path.name}` ({kind}, num={prompt.number:02d})")
    if unparseable:
        lines.append("")
        lines.append("## Unparseable Prompt Filenames")
        lines.append("")
        for path in unparseable:
            lines.append(f"- `{path.name}`")
    lines.append("")
    return "\n".join(lines)


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _stage_selection(prompts: list[PromptFile], start: int | None, end: int | None, include_system: bool) -> list[PromptFile]:
    selected: list[PromptFile] = []
    for prompt in prompts:
        if prompt.is_system:
            if include_system:
                selected.append(prompt)
            continue
        if start is not None and prompt.number < start:
            continue
        if end is not None and prompt.number > end:
            continue
        selected.append(prompt)
    return selected


def _build_preflight_parser(prog: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=prog,
        description="MVP prompt preflight helper: inspect .prompts inventory, ordering, and prerequisites.",
    )
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--prompts-dir", type=Path, default=Path(".prompts"))
    parser.add_argument("--write-report", type=Path, help="Optional path to write a markdown preflight snapshot")
    parser.add_argument("--require-tools", nargs="*", default=["git", "rg", "python3"])
    return parser


def main_repo_preflight() -> int:
    parser = _build_preflight_parser(Path(__file__).name)
    args = parser.parse_args()

    repo_root = _resolve_repo_root(args.repo_root)
    prompts_dir = _resolve_prompts_dir(repo_root, args.prompts_dir)
    prompts, unparseable = discover_prompts(prompts_dir)
    gaps = prompt_number_gaps(prompts)
    present, missing = tool_status(args.require_tools)

    print(f"Repo root: {repo_root}")
    print(f"Prompts dir: {prompts_dir}")
    if not prompts_dir.exists():
        print("ERROR: .prompts directory not found")
        return 2
    print(f"Prompt files found: {len(prompts)}")
    if unparseable:
        print(f"- Unparseable prompt filenames: {len(unparseable)}")
        for path in unparseable:
            print(f"  - {path.name}")
    print(f"- Numeric gaps: {', '.join(f'{n:02d}' for n in gaps) if gaps else '(none)'}")
    print(f"- Tools present: {', '.join(present) if present else '(none)'}")
    print(f"- Tools missing: {', '.join(missing) if missing else '(none)'}")

    status = git_status_short(repo_root)
    if status is None:
        print("- Git status: unavailable (not a git repo or git command failed)")
    elif not status:
        print("- Git status: clean")
    else:
        print("- Git status: dirty")
        for line in status.splitlines()[:20]:
            print(f"  {line}")

    if args.write_report:
        report_path = args.write_report if args.write_report.is_absolute() else repo_root / args.write_report
        _write_text(
            report_path,
            _render_prompt_inventory_md(
                title="Prompt Preflight Snapshot",
                repo_root=repo_root,
                prompts_dir=prompts_dir,
                prompts=prompts,
                unparseable=unparseable,
                gaps=gaps,
            ),
        )
        print(f"Wrote report: {report_path}")

    print("\nNext steps:")
    print("  - Run your prompt preflight inspection process (or skill) before executing prompts.")
    print("  - Use `git add -p` for any prompt-fix commits and prefix messages with [PRE-FLIGHT].")
    return 1 if missing else 0


def _build_stage_run_parser(prog: str, stage_label: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=prog,
        description=f"MVP {stage_label} run helper: verify prerequisites and print an execution/checkpoint plan.",
    )
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--prompts-dir", type=Path, default=Path(".prompts"))
    parser.add_argument("--start", type=int)
    parser.add_argument("--end", type=int)
    parser.add_argument("--include-system", action="store_true", help="Include PROMPT_*_s.txt files in the plan")
    parser.add_argument("--write-plan", type=Path, help="Optional markdown path for the generated run plan")
    parser.add_argument("--require-tools", nargs="*", default=["git", "python3"])
    return parser


def _run_stage_plan(stage_label: str, args: argparse.Namespace) -> int:
    repo_root = _resolve_repo_root(args.repo_root)
    prompts_dir = _resolve_prompts_dir(repo_root, args.prompts_dir)
    prompts, unparseable = discover_prompts(prompts_dir)
    if not prompts_dir.exists():
        print("ERROR: .prompts directory not found")
        return 2
    if unparseable:
        print("ERROR: Unparseable prompt filenames present. Fix names before proceeding:")
        for path in unparseable:
            print(f"- {path.name}")
        return 2

    selected = _stage_selection(prompts, args.start, args.end, args.include_system)
    present, missing = tool_status(args.require_tools)
    print(f"{stage_label} run plan for repo: {repo_root}")
    print(f"- prompts selected: {len(selected)}")
    print(f"- tools present: {', '.join(present) if present else '(none)'}")
    print(f"- tools missing: {', '.join(missing) if missing else '(none)'}")
    for prompt in selected:
        print(f"  - {prompt.path.name}")

    lines = [f"# {stage_label} Run Plan", "", f"- repo_root: `{repo_root}`", ""]
    lines.append("## Selected Prompts")
    lines.append("")
    for prompt in selected:
        lines.append(f"- `{prompt.path.name}`")
    lines += [
        "",
        "## Execution Notes",
        "",
        "- This MVP helper plans and verifies a prompt run; it does not execute prompts automatically.",
        "- After each prompt, summarize changes and prepare `[PROMPT_XX]` commit messages.",
        "- Use `git add -p` to stage prompt-sized patch groups.",
        "- Run relevant tests/verification commands before each commit.",
        "",
    ]
    plan_md = "\n".join(lines)

    if args.write_plan:
        out_path = args.write_plan if args.write_plan.is_absolute() else repo_root / args.write_plan
        _write_text(out_path, plan_md)
        print(f"Wrote plan: {out_path}")

    return 1 if missing else 0


def main_repo_stage1_run() -> int:
    parser = _build_stage_run_parser(Path(__file__).name, "Stage 1")
    parser.set_defaults(include_system=True)
    args = parser.parse_args()
    return _run_stage_plan("Stage 1", args)


def _inventory_counts(repo_root: Path) -> dict[str, int | bool]:
    return {
        "prompt_files": len(list((repo_root / ".prompts").glob("PROMPT_*.txt"))) if (repo_root / ".prompts").exists() else 0,
        "tests_py": len(list(repo_root.rglob("test_*.py"))),
        "docs_md": len(list(repo_root.rglob("docs/*.md"))),
        "has_ci": (repo_root / ".github" / "workflows").exists(),
        "has_readme": any((repo_root / name).exists() for name in ["README.md", "README.MD", "README"]),
    }


def _build_postflight_parser(prog: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=prog,
        description="MVP postflight helper: capture repo snapshot and write a post-flight report skeleton.",
    )
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--stage", choices=["stage1", "stage2"], default="stage1")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    return parser


def main_repo_postflight() -> int:
    parser = _build_postflight_parser(Path(__file__).name)
    args = parser.parse_args()
    repo_root = _resolve_repo_root(args.repo_root)
    stage_name = args.stage.upper().replace("STAGE", "STAGE-")
    default_name = f"{stage_name}-POST-FLIGHT.md"
    output = args.output or Path(default_name)
    output_path = output if output.is_absolute() else repo_root / output

    counts = _inventory_counts(repo_root)
    status = git_status_short(repo_root)
    status_summary = "unavailable"
    if status is not None:
        status_summary = "clean" if not status else "dirty"

    report = "\n".join(
        [
            f"# {stage_name} POST-FLIGHT (MVP Snapshot)",
            "",
            "## Automated Snapshot",
            "",
            f"- repo_root: `{repo_root}`",
            f"- git_status: `{status_summary}`",
            f"- prompt_files: {counts['prompt_files']}",
            f"- python_test_files: {counts['tests_py']}",
            f"- docs_markdown_files: {counts['docs_md']}",
            f"- ci_present: {counts['has_ci']}",
            f"- root_readme_present: {counts['has_readme']}",
            "",
            "## Manual Review Checklist (fill in)",
            "",
            "- Completeness score /100:",
            "- Excellence score /10:",
            "- What shipped:",
            "- Regressions / breakages:",
            "- Top missing artifacts:",
            "- Recommended next prompts / follow-ups:",
            "",
        ]
    )

    if args.dry_run:
        print(report)
        return 0

    _write_text(output_path, report)
    print(f"Wrote postflight snapshot: {output_path}")
    return 0


def _build_stage2_plan_parser(prog: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=prog,
        description="MVP stage-2 planning helper: write a small follow-up prompt plan outline from a postflight report.",
    )
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--input", dest="input_report", type=Path, default=Path("STAGE-1-POST-FLIGHT.md"))
    parser.add_argument("--output", type=Path, default=Path(".prompts/STAGE2-PLAN.md"))
    parser.add_argument("--dry-run", action="store_true")
    return parser


def main_repo_stage2_plan() -> int:
    parser = _build_stage2_plan_parser(Path(__file__).name)
    args = parser.parse_args()
    repo_root = _resolve_repo_root(args.repo_root)
    input_report = args.input_report if args.input_report.is_absolute() else repo_root / args.input_report
    output_path = args.output if args.output.is_absolute() else repo_root / args.output

    counts = _inventory_counts(repo_root)
    stage2_items: list[str] = []
    if not counts["has_ci"]:
        stage2_items.append("Add CI workflow for pytest + core CLI smoke checks")
    if not counts["has_readme"]:
        stage2_items.append("Add root README with quickstart and artifact map")
    if counts["tests_py"] < 5:
        stage2_items.append("Expand test coverage for sync edge cases and render/new CLIs")
    if len(stage2_items) < 3:
        stage2_items.append("Refine docs and examples to match real CLI semantics")
        stage2_items.append("Harden lint/validate heuristics and reduce false positives")

    lines = [
        "# Stage-2 Plan (MVP Helper)",
        "",
        f"- repo_root: `{repo_root}`",
        f"- input_postflight_report: `{input_report}`",
        f"- input_exists: {input_report.exists()}",
        "",
        "## Suggested Stage-2 Prompt Themes (3-6)",
        "",
    ]
    for idx, item in enumerate(stage2_items[:6], start=1):
        lines.append(f"{idx}. {item}")
    lines += [
        "",
        "## Draft Prompt Guidance",
        "",
        "- Keep prompts narrowly scoped with explicit deliverables and acceptance checks.",
        "- Insert verification gates (tests/lint/smoke) after risky changes.",
        "- Continue prompt-prefixed commit discipline with `git add -p`.",
        "",
    ]
    plan = "\n".join(lines)

    if args.dry_run:
        print(plan)
        return 0

    _write_text(output_path, plan)
    print(f"Wrote stage-2 plan outline: {output_path}")
    return 0


def main_repo_stage2_run() -> int:
    parser = _build_stage_run_parser(Path(__file__).name, "Stage 2")
    args = parser.parse_args()
    return _run_stage_plan("Stage 2", args)
