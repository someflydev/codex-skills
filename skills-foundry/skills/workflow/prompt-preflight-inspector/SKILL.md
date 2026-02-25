---
id: prompt-preflight-inspector
name: Prompt Preflight Inspector
description: Audit ordered .prompts files for ordering, dependency, clarity, and scope risks before the first build run.
version: 0.1.0
tags: [workflow, preflight, prompts]
inputs:
  - name: repo_root
    type: path
    required: true
    default: .
    examples: [".", "../target-repo"]
  - name: max_fix_severity
    type: enum
    required: false
    default: MEDIUM
    examples: ["LOW", "MEDIUM"]
  - name: apply
    type: bool
    required: false
    default: false
    examples: [false, true]
expected_tools: [git, rg, python3]
safety:
  dry_run_supported: true
  destructive_actions: []
  confirmation_points:
    - "Confirm before applying fixes, pruning prompts, or auto-committing"
    - "Confirm before rerunning prompts after a failed run"
outputs:
  - .prompts/improvements-before-initial-run.txt
  - skills-foundry/reports/preflight.md
  - .prompts/preflight-patches/<issue-id>.patch
---

## When to use

Use before running `PROMPT_00_s` / `PROMPT_01..N` to catch sequencing, naming, dependency, and overengineering problems in the prompt set and optionally apply conservative, intent-preserving fixes.

## Inputs

- `repo_root`: path to the target repository that contains `.prompts/`.
- `prompt_range` / `prompt_selection`: optional filter for prompts to inspect or run.
- `commit_mode`: whether to propose patch groupings only or also commit after confirmation.
- `report_path`: optional override for generated report output when the skill writes a report.

## Procedure

1. Confirm the target repo has a `.prompts/` directory and capture a baseline with `git status --short` and `rg --files .prompts | sort`.
2. Load every `PROMPT_*.txt` and `PROMPT_*_s.txt` file in order; extract referenced artifacts, commands, and implied prerequisites.
3. Build a prompt dependency map and flag forward references, missing prerequisites, naming collisions, contradictory constraints, and overengineering risks.
4. Write a prioritized issue list with concrete suggested fixes, marking each item as SAFE-AUTO, NEEDS-CONFIRMATION, or NEEDS-HUMAN-INTENT.
5. If `apply=true`, limit changes to `max_fix_severity`, generate patch previews (`--write-patches`) when requested, and re-run preflight after each approved fix round.
6. Propose Tim Pope style patch groupings and `[PRE-FLIGHT]` commit messages, then recommend `git add -p` for human review before any commit action.

## Success criteria

- The prompt set is reloaded and re-checked after each applied fix round.
- Remaining BLOCKER/HIGH issues are either fixed or explicitly deferred with human approval.
- A readable preflight report and append-only improvements log are produced.

## Failure modes + recovery

- If `.prompts/` is missing or unreadable, stop immediately and report the exact path and recovery steps.
- If prompt text implies multiple incompatible architectures, defer changes and ask for human intent instead of guessing.
- If an automated edit would widen scope, recover by reverting just that patch and rerun preflight in report-only mode.

## Examples

### Small Repo (10 prompts)

Inspect a 10-prompt repo, detect a missing `PROMPT_04` verification gate, suggest a SAFE-AUTO wording fix, apply it, append the fix log, and rerun until no BLOCKER/HIGH issues remain.

### Larger Repo (25 prompts)

Audit a 25-prompt repo with stage-1 and stage-2 sections, identify duplicate artifact ownership and prompt-order hazards, write a theme-grouped fix plan, and leave architecture choices as human-intent questions.
