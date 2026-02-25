---
id: prompt-postflight-analyzer-alt
name: Prompt Postflight Analyzer (ALT)
description: Stage-1 postflight analyzer variant that weights operability, reproducibility, and maintenance risk more heavily than feature breadth.
version: 0.1.0
tags: [workflow, postflight, stage1, alt]
inputs:
  - name: repo_root
    type: path
    required: true
    default: .
    examples: ["."]
  - name: output_report
    type: path
    required: false
    default: STAGE-1-POST-FLIGHT.md
    examples: ["STAGE-1-POST-FLIGHT.md"]
  - name: weighting_mode
    type: enum
    required: false
    default: operability-heavy
    examples: ["operability-heavy"]
expected_tools: [git, rg, python3]
safety:
  dry_run_supported: true
  destructive_actions: []
  confirmation_points:
    - "Confirm before applying fixes, pruning prompts, or auto-committing"
    - "Confirm before rerunning prompts after a failed run"
outputs:
  - STAGE-1-POST-FLIGHT.md
  - skills-foundry/reports/postflight-stage1.json
  - skills-foundry/reports/postflight-stage1-risk-register.md
---

## When to use

Use this variant when stage-1 output appears feature-rich but operationally fragile and you need a postflight report that prioritizes reproducibility, onboarding, and rollback safety.

## Inputs

- `repo_root`: path to the target repository that contains `.prompts/`.
- `prompt_range` / `prompt_selection`: optional filter for prompts to inspect or run.
- `commit_mode`: whether to propose patch groupings only or also commit after confirmation.
- `report_path`: optional override for generated report output when the skill writes a report.

## Procedure

1. Collect evidence on reproducibility (setup docs, pinned tools, scripts, smoke tests) before scoring feature completeness so operational gaps are visible early.
2. Apply an operability-heavy rubric weighting that penalizes fragile setup, missing verification, and hard-to-review diffs more than incomplete nice-to-have features.
3. Generate a detailed risk register with severity, likelihood, and mitigation steps tied to concrete files/commands in the repo.
4. Write `STAGE-1-POST-FLIGHT.md` with explicit score weighting notes so future stage-2 planning understands why certain deductions were applied.
5. Recommend stage-2 investments that first improve repeatability (tests, scripts, docs, smoke runs) before broader feature expansion.
6. Summarize which high-effort improvements are probably not worth the complexity for the project’s current maturity.

## Success criteria

- Operational risk is explicitly weighted and explained in the scoring method.
- Mitigations are concrete and tied to files/commands.
- Stage-2 recommendations reduce fragility before adding breadth.

## Failure modes + recovery

- If operability evidence is missing, recover by marking unknowns explicitly instead of assuming the setup works.
- If weighting changes alter recommendations significantly, include both baseline and operability-heavy interpretations for comparison.
- If a mitigation would require major architecture changes, defer it and call out the tradeoff in the report.

## Examples

### Small Repo (10 prompts)

Review a 10-prompt repo that mostly works but has fragile setup instructions, score it lower on operability, and prioritize stage-2 prompts for smoke tests and scripted setup.

### Larger Repo (25 prompts)

Analyze a 25-prompt repo with many subsystems, highlight reproducibility gaps across runtimes, and propose a stage-2 plan that reduces maintenance risk before new features.
