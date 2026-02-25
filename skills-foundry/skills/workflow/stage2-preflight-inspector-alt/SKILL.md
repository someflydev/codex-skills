---
id: stage2-preflight-inspector-alt
name: Stage2 Preflight Inspector (ALT)
description: Stage-2 preflight variant that generates patch bundles first and applies fixes only after reviewing patch files for new prompt changes.
version: 0.1.0
tags: [workflow, preflight, stage2, alt]
inputs:
  - name: repo_root
    type: path
    required: true
    default: .
    examples: ["."]
  - name: patch_dir
    type: path
    required: false
    default: .prompts/stage2-preflight-patches
    examples: [".prompts/stage2-preflight-patches"]
  - name: apply_after_review
    type: bool
    required: false
    default: false
    examples: [false, true]
expected_tools: [git, rg, python3, diff]
safety:
  dry_run_supported: true
  destructive_actions: []
  confirmation_points:
    - "Confirm before applying fixes, pruning prompts, or auto-committing"
    - "Confirm before rerunning prompts after a failed run"
outputs:
  - .prompts/improvements-before-stage2-run.txt
  - .prompts/stage2-preflight-patches/<theme>.patch
  - skills-foundry/reports/stage2-preflight.md
---

## When to use

Use this variant when stage-2 prompt changes are risky and you want patch artifacts reviewed before any stage-2 prompt text is modified.

## Inputs

- `repo_root`: path to the target repository that contains `.prompts/`.
- `prompt_range` / `prompt_selection`: optional filter for prompts to inspect or run.
- `commit_mode`: whether to propose patch groupings only or also commit after confirmation.
- `report_path`: optional override for generated report output when the skill writes a report.

## Procedure

1. Run stage-2 preflight checks in report-only mode first, collecting issues and generating patch bundles grouped by theme (ordering, dependency, naming, clarity).
2. Review generated patch bundles with the operator and confirm which themes can be applied without changing stage-2 intent.
3. Apply approved patch bundles, rerun the stage-2 preflight audit, and regenerate patches if the prompt text shifted under review.
4. Append the stage2 preflight improvements log with round-by-round patch outcomes and unresolved decisions.
5. Produce `[PRE-FLIGHT]` commit recommendations grouped by patch bundle to keep review focused and auditable.
6. Escalate any cross-stage or architecture-impacting changes as human-intent decisions instead of patching them automatically.

## Success criteria

- Patch bundles exist for all applied changes.
- Stage-2 prompt fixes remain narrowly scoped and reviewed before application.
- The rerun audit confirms no new stage-2 dependency regressions.

## Failure modes + recovery

- If patch bundles become stale after edits, recover by regenerating from current files and discarding stale patch artifacts.
- If review feedback changes prompt intent, stop and request a revised stage-2 plan rather than force-fitting patch bundles.
- If stage-2 fixes require stage-1 prompt rewrites, defer and document the dependency in the report.

## Examples

### Small Repo (10 prompts)

Generate and review patch bundles for 3 new stage-2 prompts in a 10-prompt repo, apply only the ordering and naming patches, and rerun preflight before stage-2 execution.

### Larger Repo (25 prompts)

Patch-first audit of 6 stage-2 prompts in a 25-prompt repo, with theme-grouped patch files and explicit deferral of architecture-level rewrites.
