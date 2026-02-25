---
id: stage2-postflight-analyzer
name: Stage2 Postflight Analyzer
description: Generate STAGE-2-POST-FLIGHT.md with stage-2 scores, delta vs stage-1, remaining gaps, and not-worth-it items.
version: 0.1.0
tags: [workflow, postflight, stage2]
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
  - name: output_report
    type: path
    required: false
    default: STAGE-2-POST-FLIGHT.md
    examples: ["STAGE-2-POST-FLIGHT.md"]
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
---

## When to use

Use after stage-2 execution to score the new repo state, compare outcomes against stage-1, and explicitly call out remaining gaps and low-value future work.

## Inputs

- `repo_root`: path to the target repository that contains `.prompts/`.
- `prompt_range` / `prompt_selection`: optional filter for prompts to inspect or run.
- `commit_mode`: whether to propose patch groupings only or also commit after confirmation.
- `report_path`: optional override for generated report output when the skill writes a report.

## Procedure

1. Load the current repo state, stage-2 prompt range, and `STAGE-1-POST-FLIGHT.md` to establish a baseline for delta scoring.
2. Re-score completeness/excellence and compute a clear delta vs stage-1 with evidence for major improvements and regressions.
3. List remaining gaps, fragile areas, and “not worth it” items that would add complexity without enough project value.
4. Write `STAGE-2-POST-FLIGHT.md` with scores, deltas, residual risk register, and recommended stop/continue decision points.
5. Emit a structured summary for tooling/report aggregation when useful.
6. Propose follow-up commit groupings if the postflight pass includes final cleanup edits before publishing results.

## Success criteria

- Stage-2 scores are comparable to stage-1 and include explicit deltas.
- Remaining gaps and low-value items are documented clearly.
- The report supports a stop/continue decision for further stages.

## Failure modes + recovery

- If the stage-1 report is missing or incompatible, recover by generating or normalizing it before computing deltas.
- If score deltas cannot be justified with evidence, pause and gather file/test/command evidence instead of guessing.
- If the repo changed after stage-2 but before analysis, document the extra changes and decide whether to analyze a specific commit snapshot.

## Examples

### Small Repo (10 prompts)

Compare stage-2 results against stage-1 in a 10-prompt repo, report score deltas, and mark one ambitious optimization as not worth further complexity.

### Larger Repo (25 prompts)

Produce a stage-2 postflight report for a 25-prompt repo that highlights delta improvements, residual operational risks, and a pragmatic stopping point.
