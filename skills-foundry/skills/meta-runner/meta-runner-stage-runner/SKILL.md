---
id: meta-runner-stage-runner
name: Meta Runner Stage Runner
description: Execute the next dependency-ready prompt sequence with artifact gates, smoke checks, auditor verification, and prompt-scoped commits.
version: 0.1.0
tags: [meta-runner, runner, execution]
inputs:
  - name: repo_root
    type: path
    required: true
    default: .
    examples: ["."]
  - name: prompts_dir
    type: path
    required: false
    default: .prompts
    examples: [".prompts"]
  - name: stage_label
    type: string
    required: false
    default: auto
    examples: ["stage3", "auto"]
expected_tools: [git, rg, python3, pytest]
safety:
  dry_run_supported: true
  destructive_actions: []
  confirmation_points:
    - "Confirm before auto-commit mode"
    - "Confirm before continuing after any failed acceptance or smoke check"
outputs:
  - .prompts/run-logs/stage/<prompt-id>.md
  - .prompts/run-logs/stage/summary.md
  - .git/COMMIT_EDITMSG
---

## When to use

Use to run a prompt stage end-to-end while preserving deterministic stop conditions and prompt-scoped commit boundaries.

## Inputs

- `repo_root`: target repository path.
- `prompts_dir`: location of prompt files.
- `stage_label`: optional run label for logs.

## Procedure

1. Determine next prompt from `.prompts` inventory + commit-prefix evidence + dependency readiness.
2. Run prompt scope only; do not execute future prompts preemptively.
3. Validate declared artifacts and acceptance commands.
4. Run smoke checks for runtime-affecting prompts.
5. Require auditor PASS before proposing commit.
6. Commit with `[PROMPT_{num}, AGENT_{role}]` prefix using `git add -p`, then move to next prompt.

## Success criteria

- Execution resumes correctly from current repo state.
- Each prompt produces verification evidence before commit.
- No cross-prompt batching in commits.

## Failure modes + recovery

- If a prompt fails acceptance, stop immediately and capture failing command/output.
- If commit prefix format is wrong, amend before continuing.
- If dependency chain is unclear, pause and request architecture clarification.

## Examples

### Resume in-progress stage

Detect completed prompts from commit history and continue from the earliest uncompleted dependency-ready prompt.

### Fresh stage execution

Run from first system prompt when no prior prompt execution evidence exists.
