---
id: changelog-drafter
name: Changelog Drafter
description: Draft a changelog entry from recent scoped changes.
version: 0.1.0
tags: [core, docs]
inputs:
  - name: target_path
    type: path
    required: true
    default: "."
    examples: [".", "src/"]
expected_tools: [git, rg]
safety:
  dry_run_supported: true
  destructive_actions: []
  confirmation_points:
    - "Confirm before overwriting files"
outputs:
  - skills/core/changelog-drafter/SKILL.md
  - skills/core/changelog-drafter/EXAMPLES.md
  - skills/core/changelog-drafter/CHECKLIST.md
---

## When to use

Use this skill when you need a focused, repeatable workflow for `Changelog Drafter`.

## Inputs

- `target_path` (`path`, required): path to operate on.

## Procedure

1. Confirm inputs and assumptions.
2. Inspect the target files or repo state.
3. Apply the scoped changes safely.
4. Verify outputs and summarize results.

## Success criteria

- The intended files are created or updated.
- Outputs are described clearly.
- Safety checks are followed.

## Failure modes + recovery

- If prerequisites are missing, stop and report what to install.
- If a write would be unsafe, switch to dry-run and ask for confirmation.
- Recover by restoring from backup or rerunning with corrected inputs.

## Examples

- Example 1: Run on a small repo to apply a narrow change and summarize the result.
- Example 2: Run in dry-run mode first, review the plan, then rerun after confirmation.
