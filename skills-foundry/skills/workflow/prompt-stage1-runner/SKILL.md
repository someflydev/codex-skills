---
id: prompt-stage1-runner
name: Prompt Stage1 Runner
description: Run PROMPT_00_s and PROMPT_01..N in order with prerequisite checks, summaries, and commit discipline after each prompt.
version: 0.1.0
tags: [workflow, runner, stage1]
inputs:
  - name: repo_root
    type: path
    required: true
    default: .
    examples: ["."]
  - name: start_prompt
    type: string
    required: false
    default: PROMPT_00_s.txt
    examples: ["PROMPT_00_s.txt", "PROMPT_03.txt"]
  - name: end_prompt
    type: string
    required: false
    default: ""
    examples: ["PROMPT_08.txt"]
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
  - skills-foundry/reports/stage1-run-summary.md
  - .prompts/run-logs/stage1/<prompt-id>.md
  - .git/COMMIT_EDITMSG
---

## When to use

Use after preflight is green to execute the stage-1 prompt sequence in order while checking tool prerequisites, summarizing each prompt result, and enforcing reviewable commit boundaries.

## Inputs

- `repo_root`: path to the target repository that contains `.prompts/`.
- `prompt_range` / `prompt_selection`: optional filter for prompts to inspect or run.
- `commit_mode`: whether to propose patch groupings only or also commit after confirmation.
- `report_path`: optional override for generated report output when the skill writes a report.

## Procedure

1. Verify prerequisites (`git`, runtime/tooling commands referenced by upcoming prompts, and test commands such as `python3`/`pytest`) before starting execution.
2. Resolve the prompt run range (default `PROMPT_00_s.txt` then `PROMPT_01..N`) and print the exact ordered list to execute.
3. Run one prompt at a time, capture outputs/artifacts created or modified, and stop immediately on failures that require human intent or missing tooling.
4. After each prompt, inspect the diff, summarize changed files, and propose Tim Pope style `[PROMPT_XX]` commit messages with `git add -p` patch groupings.
5. If `auto_commit=true`, require explicit confirmation before committing; otherwise stop after proposing patch groups and messages for manual review.
6. Append a stage-1 run summary report with prompt outcomes, skipped items, and rerun instructions when a prompt fails.

## Success criteria

- Prompts are executed strictly in order within the selected range.
- Every prompt completion includes a change summary and proposed commit grouping.
- Failures are actionable, with prerequisites or rerun steps documented.

## Failure modes + recovery

- If a prerequisite command is missing, stop before running the next prompt and report install guidance by platform so the operator can retry cleanly.
- If a prompt leaves the repo in a conflicted or partially applied state, recover by summarizing the diff and asking whether to commit partial progress or revert manually.
- If prompt ordering is inconsistent with available files, recover by re-running preflight and correcting the prompt set before continuing.

## Examples

### Small Repo (10 prompts)

Run a 10-prompt stage-1 sequence, stop after `PROMPT_04` to propose two commit groups (`validators` and `docs`), then continue after confirmation and finish with a stage1 run summary.

### Larger Repo (25 prompts)

Execute prompts `PROMPT_00_s` through `PROMPT_25` in a 25-prompt repo, pausing on a missing tool dependency, documenting install steps, and resuming from the failed prompt after setup is fixed.
