---
id: meta-runner-stage-runner-alt
name: Meta Runner Stage Runner (ALT Checkpointed)
description: Checkpointed stage runner variant with mandatory verification pauses and stricter failure handling between prompt batches.
version: 0.1.0
tags: [meta-runner, runner, alt, checkpoint]
inputs:
  - name: repo_root
    type: path
    required: true
    default: .
    examples: ["."]
  - name: checkpoint_every
    type: int
    required: false
    default: 1
    examples: [1, 2]
  - name: enforce_smoke_on_docs
    type: bool
    required: false
    default: false
    examples: [false, true]
expected_tools: [git, rg, python3, pytest]
safety:
  dry_run_supported: true
  destructive_actions: []
  confirmation_points:
    - "Confirm before crossing each checkpoint boundary"
    - "Confirm before overriding a failed checkpoint"
outputs:
  - .prompts/run-logs/stage/checkpoints.md
  - .prompts/run-logs/stage/<prompt-id>.md
---

## When to use

Use when you want stronger operational control with explicit checkpoints and stricter manual approval gates across prompt execution.

## Inputs

- `repo_root`: target repository path.
- `checkpoint_every`: prompts per checkpoint.
- `enforce_smoke_on_docs`: optionally require smoke even for docs-only prompts.

## Procedure

1. Resolve pending prompts and split into checkpoints.
2. Execute each prompt with standard gates.
3. At each checkpoint, run additional targeted verification before commit finalization.
4. Halt on any failed checkpoint until operator confirms remediation.
5. Record checkpoint outcomes and remaining prompt queue.
6. Continue only after explicit go-ahead.

## Success criteria

- Every checkpoint has PASS/FAIL status and evidence.
- Prompt queue progression is deterministic and audited.
- No checkpoint bypass without explicit operator approval.

## Failure modes + recovery

- If checkpoint verification fails, stop and generate minimal repair plan.
- If smoke checks are flaky, switch to check-only mode and document limitations.
- If resumed state diverges from logs, rebuild prompt queue before proceeding.

## Examples

### Strict stage-3 run

Execute Stage-3 one prompt per checkpoint with mandatory verification and explicit continuation decisions.

### Team handoff mode

Use checkpoints so another operator can resume from the latest PASS boundary.
