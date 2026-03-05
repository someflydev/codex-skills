---
id: meta-runner-preflight-inspector-alt
name: Meta Runner Preflight Inspector (ALT Strict)
description: Strict preflight variant that forbids auto-edits by default and requires explicit operator sign-off for every proposed change.
version: 0.1.0
tags: [meta-runner, preflight, alt, strict]
inputs:
  - name: repo_root
    type: path
    required: true
    default: .
    examples: ["."]
  - name: prompt_selection
    type: string
    required: false
    default: stage-current
    examples: ["stage3", "PROMPT_15..PROMPT_19"]
  - name: fail_on_med
    type: bool
    required: false
    default: true
    examples: [true, false]
expected_tools: [git, rg, python3]
safety:
  dry_run_supported: true
  destructive_actions: []
  confirmation_points:
    - "Confirm every file edit individually; no batch SAFE-AUTO application"
    - "Confirm before downgrading MEDIUM findings when fail_on_med=true"
outputs:
  - .prompts/STAGE3_PRE_FLIGHT_NOTES.md
  - .prompts/STAGE3_PRE_FLIGHT_SNAPSHOT.md
---

## When to use

Use when you need maximum operator control and auditable preflight decisions before prompt execution in a sensitive or high-churn repository.

## Inputs

- `repo_root`: target repository path.
- `prompt_selection`: stage or explicit prompt range.
- `fail_on_med`: treat MED findings as stop conditions.

## Procedure

1. Run full prompt dependency and command-feasibility analysis.
2. Emit findings table sorted by severity and execution risk.
3. Require explicit operator approval before any file modification.
4. Re-run preflight after each accepted change.
5. Stop if `fail_on_med=true` and any MED finding remains unresolved.
6. Provide strict go/no-go decision with unresolved-item list.

## Success criteria

- No unresolved BLOCKER/HIGH findings.
- MED findings resolved or explicitly accepted under operator sign-off.
- Snapshot clearly records each decision gate.

## Failure modes + recovery

- If repeated edits create dependency drift, restore prior prompt text from git and restart analysis.
- If operator intent is unclear, stop instead of inferring architecture changes.
- If command feasibility cannot be validated locally, mark as blocked and provide repro steps.

## Examples

### Strict stage gate

Require zero BLOCKER/HIGH/MED issues before allowing Stage-3 execution.

### Regulated workflow

Use per-edit sign-off to preserve full traceability for prompt governance changes.
