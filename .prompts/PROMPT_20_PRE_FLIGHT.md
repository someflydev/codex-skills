# PROMPT_20 Pre-Flight Snapshot

## Scope Checked

- `.prompts/PROMPT_20.txt`

## Checks Run

- Required prompt sections present (Objective, Dependencies, Artifacts, Required Scope, Acceptance, Anti-Scope, Guardrails, Evidence).
- Acceptance commands use root-level invocation forms.
- No accidental forward references to unrelated prompt numbers.

## Fixes Applied

1. Added explicit optional state-file artifact (`.skills-flow-state.json`) to match CLI behavior expectations.
2. Added `--state-file` requirement in `skills-flow-next` scope.
3. Added acceptance command to verify `--mark-done` flow with explicit state file path.

## Decision

- GO for `PROMPT_20` execution.
