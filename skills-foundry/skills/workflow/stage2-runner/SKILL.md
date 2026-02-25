---
id: stage2-runner
name: Stage2 Runner
description: Run stage-2 prompts in order with commit discipline, summaries, and rollback guidance after each prompt.
version: 0.1.0
tags: [workflow, runner, stage2]
inputs:
  - name: repo_root
    type: path
    required: true
    default: .
    examples: ["."]
  - name: prompt_selection
    type: string
    required: false
    default: newest-stage2-prompts
    examples: ["PROMPT_09..PROMPT_12", "newest-stage2-prompts"]
  - name: auto_commit
    type: bool
    required: false
    default: false
    examples: [false, true]
expected_tools: [git, rg, python3, pytest]
safety:
  dry_run_supported: true
  destructive_actions: []
  confirmation_points:
    - "Confirm before applying fixes, pruning prompts, or auto-committing"
    - "Confirm before rerunning prompts after a failed run"
outputs:
  - skills-foundry/reports/stage2-run-summary.md
  - .prompts/run-logs/stage2/<prompt-id>.md
---

## When to use

Use after stage-2 preflight is green to execute newly added stage-2 prompts in order while preserving the same reviewable commit discipline used in stage-1.

## Inputs

- `repo_root`: path to the target repository that contains `.prompts/`.
- `prompt_range` / `prompt_selection`: optional filter for prompts to inspect or run.
- `commit_mode`: whether to propose patch groupings only or also commit after confirmation.
- `report_path`: optional override for generated report output when the skill writes a report.

## Procedure

1. Resolve the stage-2 prompt range and verify the selected prompts are newer additions intended for stage-2 execution.
2. Run each stage-2 prompt in order, capturing changed files, command outputs, and any verification steps requested by the prompt.
3. After each prompt, inspect the diff and propose `[PROMPT_XX]` commit messages with patch groupings suitable for `git add -p` review.
4. Provide rollback guidance after each prompt (what changed, what to revert manually if needed, and safe resume points).
5. If `auto_commit=true`, require explicit confirmation before each commit and stop on failed verification commands until the operator resolves them.
6. Write a stage-2 run summary with completed prompts, deferred prompts, and exact resume commands for interruptions.

## Success criteria

- Stage-2 prompts run in the intended order with no hidden skips.
- Each prompt completion includes reviewable commit guidance and rollback notes.
- Resume instructions exist for any interrupted stage-2 run.

## Failure modes + recovery

- If a stage-2 prompt fails midway, recover by summarizing the partial diff and confirming whether to commit partial work or revert before retrying.
- If rollback guidance is unclear because multiple prompts were mixed, stop and recover by re-establishing one-prompt-at-a-time boundaries.
- If a stage-2 prompt changes required tooling, rerun prerequisite checks before continuing to the next prompt.

## Examples

### Small Repo (10 prompts)

Run 3 stage-2 prompts in a 10-prompt repo, commit after each prompt with `[PROMPT_XX]` messages, and document rollback steps when one prompt changes shared scripts.

### Larger Repo (25 prompts)

Execute a larger 25-prompt repo’s stage-2 range, pausing for verification between prompts and maintaining clear resume points for long-running changes.
