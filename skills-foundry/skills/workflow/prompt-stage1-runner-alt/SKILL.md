---
id: prompt-stage1-runner-alt
name: Prompt Stage1 Runner (ALT)
description: Checkpointed stage-1 runner variant that groups commits by subsystem and inserts stricter verification pauses between prompt ranges.
version: 0.1.0
tags: [workflow, runner, stage1, alt]
inputs:
  - name: repo_root
    type: path
    required: true
    default: .
    examples: ["."]
  - name: checkpoint_every
    type: int
    required: false
    default: 3
    examples: [2, 3]
  - name: commit_grouping
    type: enum
    required: false
    default: subsystem
    examples: ["subsystem", "prompt"]
expected_tools: [git, rg, python3, pytest]
safety:
  dry_run_supported: true
  destructive_actions: []
  confirmation_points:
    - "Confirm before applying fixes, pruning prompts, or auto-committing"
    - "Confirm before rerunning prompts after a failed run"
outputs:
  - skills-foundry/reports/stage1-run-summary.md
  - skills-foundry/reports/stage1-checkpoints.md
  - .prompts/run-logs/stage1/<prompt-id>.md
---

## When to use

Use this variant when you want more operational control during stage-1 execution: regular checkpoints, extra verification pauses, and commit grouping that can span multiple prompts by subsystem.

## Inputs

- `repo_root`: path to the target repository that contains `.prompts/`.
- `prompt_range` / `prompt_selection`: optional filter for prompts to inspect or run.
- `commit_mode`: whether to propose patch groupings only or also commit after confirmation.
- `report_path`: optional override for generated report output when the skill writes a report.

## Procedure

1. Precompute prompt order and split it into checkpoint batches (`checkpoint_every`) so the operator sees planned pause points before execution begins.
2. Run prompts sequentially inside each batch, but delay commits until the batch checkpoint unless a prompt introduces high-risk structural changes.
3. At each checkpoint, run targeted verification commands (tests/linters relevant to changed areas), summarize failures, and propose subsystem-oriented commit groups with `[PROMPT_XX]` prefixes referencing the dominant prompt in the batch.
4. Require explicit confirmation before continuing to the next batch when verification fails or when a prompt changes critical workflow scripts.
5. Record checkpoint outcomes, pending follow-ups, and rerun commands in a checkpoint report for later auditing.
6. If an interruption occurs mid-batch, recover by replaying from the last completed checkpoint rather than guessing the correct resume point.

## Success criteria

- Checkpoint boundaries are explicit and auditable.
- Commit grouping strategy is applied consistently (subsystem-first in this variant).
- Resume instructions are clear after interruptions.

## Failure modes + recovery

- If verification fails at a checkpoint, stop and recover by fixing the failing subsystem before executing the next batch.
- If commit grouping spans prompts ambiguously, recover by splitting the batch diff and staging smaller hunks with `git add -p`.
- If a prompt modifies execution assumptions mid-run, rerun the remaining batch planning step before continuing.

## Examples

### Small Repo (10 prompts)

Run a 10-prompt repo in batches of 3 prompts, perform a lint/test checkpoint after each batch, and commit grouped changes by subsystem with clear `[PROMPT_XX]` messages.

### Larger Repo (25 prompts)

Run a 25-prompt repo with checkpoint batches and pause after infrastructure-heavy prompts to verify scripts/tests before allowing the next batch to proceed.
