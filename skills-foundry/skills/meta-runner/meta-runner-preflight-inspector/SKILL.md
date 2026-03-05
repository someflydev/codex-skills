---
id: meta-runner-preflight-inspector
name: Meta Runner Preflight Inspector
description: Run prompt-batch preflight audits for ordering, dependencies, safety, and acceptance-criteria feasibility before execution.
version: 0.1.0
tags: [meta-runner, preflight, prompts]
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
  - name: apply_safe_auto
    type: bool
    required: false
    default: false
    examples: [false, true]
expected_tools: [git, rg, python3]
safety:
  dry_run_supported: true
  destructive_actions: []
  confirmation_points:
    - "Confirm before applying any SAFE-AUTO edits"
    - "Confirm before changing prompt dependencies or numbering"
outputs:
  - .prompts/STAGE3_PRE_FLIGHT_NOTES.md
  - .prompts/STAGE3_PRE_FLIGHT_SNAPSHOT.md
  - .prompts/improvements-before-initial-run.txt
---

## When to use

Use before executing a new prompt batch (for example Stage-3) to catch sequencing hazards, missing artifacts, unrealistic acceptance commands, and scope creep.

## Inputs

- `repo_root`: target repository path.
- `prompt_selection`: stage or explicit prompt range.
- `apply_safe_auto`: whether to apply non-semantic fixups.

## Procedure

1. Load selected prompt files plus dependency context prompts.
2. Build a dependency graph from declared artifacts and acceptance checks.
3. Validate command feasibility and root-level invocation consistency.
4. Produce prioritized issues with fix scopes: SAFE-AUTO, NEEDS-CONFIRMATION, NEEDS-HUMAN-INTENT.
5. If `apply_safe_auto=true`, apply only intent-preserving edits and append improvement logs.
6. Re-run the preflight snapshot and provide go/no-go plus commit suggestions.

## Success criteria

- BLOCKER/HIGH issues are fixed or explicitly deferred with operator approval.
- Prompt ordering and dependency edges are explicit.
- Preflight outputs are append-only and auditable.

## Failure modes + recovery

- If prompts contain contradictory constraints, stop and request operator intent.
- If acceptance commands require unavailable system tools, report install path and pause.
- If edits would alter architecture direction, downgrade to proposal-only mode.

## Examples

### Stage-3 readiness check

Audit `PROMPT_15..PROMPT_19`, ensure CI-smoke requirement is explicit, and produce a go/no-go decision.

### Prompt hotfix round

Run preflight after adding a new prompt, apply SAFE-AUTO wording fixes, and regenerate snapshot notes.
