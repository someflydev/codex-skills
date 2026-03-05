---
id: meta-runner-postflight-analyzer
name: Meta Runner Postflight Analyzer
description: Audit completed prompt batches, score readiness, update DoD closure, and generate next-step prompt recommendations only when evidence supports them.
version: 0.1.0
tags: [meta-runner, postflight, scoring]
inputs:
  - name: repo_root
    type: path
    required: true
    default: .
    examples: ["."]
  - name: output_report
    type: path
    required: false
    default: POST_FLIGHT_REPORT_META_RUNNER.md
    examples: ["POST_FLIGHT_REPORT_META_RUNNER.md"]
  - name: max_new_prompts
    type: int
    required: false
    default: 3
    examples: [1, 3]
expected_tools: [git, rg, python3, pytest]
safety:
  dry_run_supported: true
  destructive_actions: []
  confirmation_points:
    - "Confirm before generating new PROMPT_XX files"
    - "Confirm before marking unresolved DoD items as accepted risk"
outputs:
  - POST_FLIGHT_REPORT_META_RUNNER.md
  - .prompts/improvements-before-finalization.txt
  - .prompts/PROMPT_STAGE3_MANIFEST.md
---

## When to use

Use after a stage run to produce evidence-backed closure status, readiness scores, and tightly scoped follow-up prompts.

## Inputs

- `repo_root`: target repository path.
- `output_report`: postflight report destination.
- `max_new_prompts`: cap for optional next prompts.

## Procedure

1. Verify artifacts and acceptance outputs from completed stage prompts.
2. Re-run key tests/smoke checks and capture command evidence.
3. Score completeness (0-100) and excellence (1-10) with rationale.
4. Update Stage-3 DoD checklist status in the manifest.
5. Append an improvements log entry with top gaps and evidence.
6. Generate 1-3 follow-up prompts only if unresolved high-value gaps remain.

## Success criteria

- Scores are evidence-based and reproducible.
- DoD closure state is explicit and current.
- Follow-up prompt generation is conditional and minimal.

## Failure modes + recovery

- If mandatory evidence checks fail, stop and mark the report as blocked until checks pass.
- If required checks cannot run, list blockers and refrain from inflating scores.
- If DoD evidence conflicts with report claims, reconcile and rerun checks.
- If new prompt suggestions exceed scope, reduce to minimal high-leverage set.

## Examples

### Stage-3 closure pass

Produce a postflight report with DoD closure table and no new prompts when all required gates pass.

### Conditional follow-up generation

Detect one unresolved P1 gap and generate a single targeted `PROMPT_20.txt`.
