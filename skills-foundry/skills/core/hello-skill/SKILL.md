---
id: hello-skill
name: Hello Skill
description: Print a simple hello-world style result for workflow sanity checks.
version: 0.1.0
tags: [core, demo]
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
  - skills/core/hello-skill/SKILL.md
  - skills/core/hello-skill/EXAMPLES.md
  - skills/core/hello-skill/CHECKLIST.md
---

## When to use

Use this skill when you need a focused, repeatable workflow for `Hello Skill`.

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
