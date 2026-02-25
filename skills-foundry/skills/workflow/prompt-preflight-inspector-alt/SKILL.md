---
id: prompt-preflight-inspector-alt
name: Prompt Preflight Inspector (ALT)
description: Patch-first prompt preflight variant that prioritizes conservative diffs, written evidence, and lower-severity auto-fix ceilings.
version: 0.1.0
tags: [workflow, preflight, prompts, alt]
inputs:
  - name: repo_root
    type: path
    required: true
    default: .
    examples: [".", "../target-repo"]
  - name: patch_dir
    type: path
    required: false
    default: .prompts/preflight-patches
    examples: [".prompts/preflight-patches"]
  - name: auto_apply_ceiling
    type: enum
    required: false
    default: LOW
    examples: ["NIT", "LOW"]
expected_tools: [git, rg, python3, diff]
safety:
  dry_run_supported: true
  destructive_actions: []
  confirmation_points:
    - "Confirm before applying fixes, pruning prompts, or auto-committing"
    - "Confirm before rerunning prompts after a failed run"
outputs:
  - .prompts/improvements-before-initial-run.txt
  - .prompts/preflight-patches/<theme>.patch
  - skills-foundry/reports/preflight.md
---

## When to use

Use this variant when you want the same preflight coverage but prefer patch artifacts first, lower default auto-apply severity, and stronger evidence for every proposed change.

## Inputs

- `repo_root`: path to the target repository that contains `.prompts/`.
- `prompt_range` / `prompt_selection`: optional filter for prompts to inspect or run.
- `commit_mode`: whether to propose patch groupings only or also commit after confirmation.
- `report_path`: optional override for generated report output when the skill writes a report.

## Procedure

1. Snapshot the repo state and load prompts in numeric order, but keep the run read-only while collecting issues and candidate patch hunks.
2. Classify issues by severity and theme, then generate patch files per theme before any apply step so the operator can inspect exact diffs.
3. Default to `auto_apply_ceiling=LOW`; require explicit confirmation before applying MEDIUM+ edits or any rename that changes prompt numbering or artifact paths.
4. Apply approved patches incrementally, re-open affected prompts, and verify no new forward references or naming collisions were introduced.
5. Record every round in `.prompts/improvements-before-initial-run.txt` with timestamps, issue ids, and follow-ups.
6. Produce `[PRE-FLIGHT]` commit recommendations grouped by patch file/theme and emphasize `git add -p` review before commit.

## Success criteria

- Every applied change has a corresponding patch artifact or explicit justification.
- Auto-applied edits stay within the approved severity ceiling.
- The prompt set remains intent-preserving after the rerun check.

## Failure modes + recovery

- If a generated patch no longer applies cleanly after another edit, recover by regenerating the patch from current prompt text instead of forcing it.
- If severity classification is ambiguous, stop and request confirmation rather than silently escalating auto-apply scope.
- If multiple patch themes overlap in the same lines, split the patch set and retry to keep commits reviewable.

## Examples

### Small Repo (10 prompts)

Generate patch files for a 10-prompt repo with naming inconsistencies, auto-apply only LOW typo/clarity fixes, and leave a MEDIUM sequencing rewrite as a confirmation item.

### Larger Repo (25 prompts)

Run patch-first preflight across 25 prompts, emit per-theme patch bundles (`ordering`, `artifact-paths`, `wording`), then apply only approved themes and rerun the audit.
