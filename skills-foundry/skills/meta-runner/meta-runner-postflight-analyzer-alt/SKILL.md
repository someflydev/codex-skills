---
id: meta-runner-postflight-analyzer-alt
name: Meta Runner Postflight Analyzer (ALT Delta)
description: Delta-focused postflight variant that compares score movement across stages and emphasizes drift detection over broad expansion plans.
version: 0.1.0
tags: [meta-runner, postflight, alt, drift]
inputs:
  - name: repo_root
    type: path
    required: true
    default: .
    examples: ["."]
  - name: baseline_report
    type: path
    required: false
    default: POST_FLIGHT_REPORT.md
    examples: ["POST_FLIGHT_REPORT.md"]
  - name: output_report
    type: path
    required: false
    default: POST_FLIGHT_REPORT_META_RUNNER.md
    examples: ["POST_FLIGHT_REPORT_META_RUNNER.md"]
expected_tools: [git, rg, python3, pytest]
safety:
  dry_run_supported: true
  destructive_actions: []
  confirmation_points:
    - "Confirm before changing previous-score baselines"
    - "Confirm before creating any follow-up prompts"
outputs:
  - POST_FLIGHT_REPORT_META_RUNNER.md
  - .prompts/improvements-before-finalization.txt
---

## When to use

Use when stakeholders care most about measurable score deltas, residual drift risk, and minimal follow-up scope.

## Inputs

- `repo_root`: target repository path.
- `baseline_report`: prior postflight baseline.
- `output_report`: delta report destination.

## Procedure

1. Load baseline and current artifacts.
2. Compute score deltas and identify highest-impact changes.
3. Build a drift register for naming, docs, CI, and smoke behavior.
4. Validate unresolved items with direct command evidence.
5. Propose minimal fix set and capped prompt follow-ups.
6. Append concise finalization log entry.

## Success criteria

- Delta table is explicit and evidence-backed.
- Drift risks are prioritized by operational impact.
- Follow-ups remain bounded and justified.

## Failure modes + recovery

- If delta evidence is inconsistent or missing, stop and rerun baseline/current checks before scoring.
- If baseline report is missing, fall back to current-state scoring and note limitation.
- If drift cannot be reproduced, mark as suspected and add repro steps.
- If follow-up list grows, split into immediate vs deferred and cap immediate items.

## Examples

### Score delta review

Compare Stage-2 and Stage-3 scores to identify what materially improved and what still blocks adoption.

### Drift triage

Focus on unresolved CI/docs drift and generate only one immediate follow-up prompt.
