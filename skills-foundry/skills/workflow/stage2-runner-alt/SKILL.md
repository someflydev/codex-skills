---
id: stage2-runner-alt
name: Stage2 Runner (ALT)
description: Checkpointed stage-2 runner variant with batch execution, rollback-first checkpoints, and stricter pause conditions.
version: 0.1.0
tags: [workflow, runner, stage2, alt]
inputs:
  - name: repo_root
    type: path
    required: true
    default: .
    examples: ["."]
  - name: batch_size
    type: int
    required: false
    default: 2
    examples: [1, 2, 3]
  - name: rollback_tag_prefix
    type: string
    required: false
    default: stage2-checkpoint
    examples: ["stage2-checkpoint"]
expected_tools: [git, rg, python3, pytest]
safety:
  dry_run_supported: true
  destructive_actions: []
  confirmation_points:
    - "Confirm before applying fixes, pruning prompts, or auto-committing"
    - "Confirm before rerunning prompts after a failed run"
outputs:
  - skills-foundry/reports/stage2-run-summary.md
  - skills-foundry/reports/stage2-checkpoints.md
  - .prompts/run-logs/stage2/<prompt-id>.md
---

## When to use

Use this variant when stage-2 prompts are high-risk and you want batch checkpoints, rollback markers, and stricter verification pauses during execution.

## Inputs

- `repo_root`: path to the target repository that contains `.prompts/`.
- `prompt_range` / `prompt_selection`: optional filter for prompts to inspect or run.
- `commit_mode`: whether to propose patch groupings only or also commit after confirmation.
- `report_path`: optional override for generated report output when the skill writes a report.

## Procedure

1. Split the stage-2 prompt range into execution batches (`batch_size`) and create rollback checkpoints (for example tags or documented commits) before each batch starts.
2. Run prompts sequentially within a batch and record per-prompt diffs, but hold final commit decisions until the batch checkpoint unless an immediate commit is safer.
3. At each checkpoint, run requested verifications, summarize failures, and propose `[PROMPT_XX]` commit messages plus rollback instructions tied to the checkpoint marker.
4. Stop automatically when a prompt changes core workflow scripts, install commands, or build assumptions, and require explicit confirmation before continuing.
5. Update the checkpoint report with batch outcomes, rollback markers, and exact resume commands.
6. If recovery is needed, return to the last checkpoint cleanly, fix the issue, and rerun only the affected batch.

## Success criteria

- Rollback checkpoints exist and are documented before high-risk batches.
- Verification pauses are enforced at batch boundaries.
- Recovery can restart from the last known-good checkpoint without replaying the entire stage-2 run.

## Failure modes + recovery

- If a checkpoint marker cannot be created safely, recover by documenting a manual rollback point before proceeding.
- If batch diffs become too large for review, recover by reducing `batch_size` and rerunning from the last checkpoint.
- If a rollback attempt leaves stray changes, stop and re-establish a clean checkpoint before continuing.

## Examples

### Small Repo (10 prompts)

Run a 10-prompt repo’s stage-2 work in batches of 2 prompts with rollback checkpoints, using the checkpoint report to resume cleanly after a failed verification.

### Larger Repo (25 prompts)

Execute stage-2 prompts in a 25-prompt repo with checkpoint pauses around risky workflow changes, documenting rollback markers and batch-level commit plans.
