---
id: stage2-postflight-analyzer-alt
name: Stage2 Postflight Analyzer (ALT)
description: Stage-2 postflight analyzer variant that emphasizes deltas, regression detection, and explicit pruning of low-value future work.
version: 0.1.0
tags: [workflow, postflight, stage2, alt]
inputs:
  - name: repo_root
    type: path
    required: true
    default: .
    examples: ["."]
  - name: stage1_postflight_report
    type: path
    required: true
    default: STAGE-1-POST-FLIGHT.md
    examples: ["STAGE-1-POST-FLIGHT.md"]
  - name: regression_threshold
    type: int
    required: false
    default: 5
    examples: [3, 5]
expected_tools: [git, rg, python3]
safety:
  dry_run_supported: true
  destructive_actions: []
  confirmation_points:
    - "Confirm before applying fixes, pruning prompts, or auto-committing"
    - "Confirm before rerunning prompts after a failed run"
outputs:
  - STAGE-2-POST-FLIGHT.md
  - skills-foundry/reports/postflight-stage2.json
  - skills-foundry/reports/stage2-regressions.md
---

## When to use

Use this variant when you want the stage-2 postflight report to focus on regression detection, score deltas, and aggressively pruning “maybe later” items that do not justify the added complexity.

## Inputs

- `repo_root`: path to the target repository that contains `.prompts/`.
- `prompt_range` / `prompt_selection`: optional filter for prompts to inspect or run.
- `commit_mode`: whether to propose patch groupings only or also commit after confirmation.
- `report_path`: optional override for generated report output when the skill writes a report.

## Procedure

1. Load stage-1 and stage-2 evidence and compute deltas first, highlighting regressions or score drops that exceed `regression_threshold`.
2. Trace each regression to concrete causes (missing docs, broken tests, added setup complexity, inconsistent artifact locations) and propose targeted mitigations.
3. Separate remaining ideas into `worth doing` vs `not worth it` with explicit reasons tied to scope, complexity, or maintenance cost.
4. Write `STAGE-2-POST-FLIGHT.md` and an auxiliary regression report summarizing regression severity, evidence, and recovery actions.
5. Call out any stage-2 gains that came with unacceptable operational cost so the operator can decide whether to keep or roll back thematically.
6. Provide a concise recommendation on whether to stop, stabilize, or begin another planning cycle.

## Success criteria

- Regressions are detected and justified with evidence.
- Low-value follow-up work is explicitly pruned, not just left vague.
- The report provides a clear next action recommendation.

## Failure modes + recovery

- If regression evidence is incomplete, recover by re-running relevant tests/commands before finalizing the report.
- If pruning decisions depend on product/business goals, defer those items and request human prioritization.
- If stage-2 changes are too entangled to compare cleanly, recover by analyzing per-subsystem deltas instead of forcing a single aggregate conclusion.

## Examples

### Small Repo (10 prompts)

For a 10-prompt repo, detect a small regression in setup complexity after stage-2, recommend a targeted fix, and explicitly drop a low-value optimization from further planning.

### Larger Repo (25 prompts)

For a 25-prompt repo, produce a delta-focused stage-2 report with a regression appendix and a pruned list of ideas that would overengineer the project.
