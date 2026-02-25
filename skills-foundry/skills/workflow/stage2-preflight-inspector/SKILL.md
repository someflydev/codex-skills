---
id: stage2-preflight-inspector
name: Stage2 Preflight Inspector
description: Run preflight checks specifically against newly added stage-2 prompt files and their dependencies before stage-2 execution.
version: 0.1.0
tags: [workflow, preflight, stage2]
inputs:
  - name: repo_root
    type: path
    required: true
    default: .
    examples: ["."]
  - name: stage2_prompt_glob
    type: string
    required: false
    default: .prompts/PROMPT_<new>.txt
    examples: [".prompts/PROMPT_09.txt..PROMPT_12.txt"]
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
  - .prompts/improvements-before-stage2-run.txt
  - skills-foundry/reports/stage2-preflight.md
---

## When to use

Use after generating stage-2 prompts to run the same quality/dependency checks as stage-1 preflight, but focused only on the new stage-2 prompt subset and its integration points.

## Inputs

- `repo_root`: path to the target repository that contains `.prompts/`.
- `prompt_range` / `prompt_selection`: optional filter for prompts to inspect or run.
- `commit_mode`: whether to propose patch groupings only or also commit after confirmation.
- `report_path`: optional override for generated report output when the skill writes a report.

## Procedure

1. Identify the stage-2 prompt subset (usually newly added highest-numbered prompts) and load surrounding prompt context needed to validate dependencies.
2. Check ordering, artifact dependencies, naming, clarity, and scope for the stage-2 prompts while preserving existing approved stage-1 prompts unless a cross-reference is broken.
3. Write a prioritized issue list and fix plan focused on stage-2 prompts, distinguishing local fixes from cross-stage changes that need confirmation.
4. If `apply=true`, apply only approved intent-preserving fixes, append `.prompts/improvements-before-stage2-run.txt`, and rerun the stage-2 preflight check.
5. Propose `[PRE-FLIGHT]` commit groupings for stage-2 prompt fixes, emphasizing `git add -p` and small patch sets.
6. Stop when stage-2 prompts are green or when remaining issues require human intent decisions.

## Success criteria

- Stage-2 prompt subset is validated without unintentionally rewriting stage-1 scope.
- Cross-stage dependencies are explicit and correct.
- A stage2-specific preflight report/log is produced for auditability.

## Failure modes + recovery

- If the stage-2 prompt subset cannot be isolated safely, recover by expanding context only as needed and documenting the assumption.
- If a stage-2 prompt depends on unimplemented stage-1 outputs, stop and recover by fixing the stage-2 plan instead of patching around the gap.
- If fixes require architecture choices, defer to human intent and rerun after clarification.

## Examples

### Small Repo (10 prompts)

Preflight-check 3 new stage-2 prompts added to a 10-prompt repo, apply wording/ordering fixes, and leave one architecture tradeoff as a confirmation item.

### Larger Repo (25 prompts)

Audit a 25-prompt repo with 6 new stage-2 prompts, detect a forward reference to a report not yet generated, and rewrite prompt ordering before the stage-2 run.
