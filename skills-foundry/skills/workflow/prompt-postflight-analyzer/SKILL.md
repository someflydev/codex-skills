---
id: prompt-postflight-analyzer
name: Prompt Postflight Analyzer
description: Analyze a completed stage-1 repo state and generate STAGE-1-POST-FLIGHT.md with completeness, excellence, risks, and next investments.
version: 0.1.0
tags: [workflow, postflight, stage1]
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
  - name: rubric_profile
    type: enum
    required: false
    default: balanced
    examples: ["balanced", "delivery-first"]
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
---

## When to use

Use after stage-1 execution completes to score the repo outcome, document missing artifacts and risks, and produce a grounded handoff into stage-2 planning.

## Inputs

- `repo_root`: path to the target repository that contains `.prompts/`.
- `prompt_range` / `prompt_selection`: optional filter for prompts to inspect or run.
- `commit_mode`: whether to propose patch groupings only or also commit after confirmation.
- `report_path`: optional override for generated report output when the skill writes a report.

## Procedure

1. Load the repo filesystem, `.prompts/` set, and recent commit history so the analysis is based on actual delivered artifacts rather than prompt intent alone.
2. Score completeness and excellence using an explicit rubric, citing evidence (files, commands, docs, tests) for major deductions or bonuses.
3. List top missing artifacts, setup fragility, overengineering risks, and unclear operator workflows that still block reliable use.
4. Write `STAGE-1-POST-FLIGHT.md` with scores, risk register, and recommended stage-2 investments ordered by impact and execution risk.
5. Add a machine-readable summary (JSON/structured report) if the workflow tooling consumes postflight scores programmatically.
6. Propose `[PROMPT_XX]` or `[PRE-FLIGHT]` follow-up commit themes if the analysis itself is being committed after additional fixes.

## Success criteria

- Stage-1 scores are justified with concrete repo evidence.
- Missing artifacts and risks are actionable rather than vague.
- Stage-2 recommendations clearly connect to score improvements.

## Failure modes + recovery

- If the repo state is incomplete or dirty in unexpected ways, report assumptions and recover by analyzing the current state as-is rather than fabricating missing outputs.
- If rubric criteria conflict, document the tradeoff and ask the operator which weighting to prioritize before finalizing the score.
- If prompt files and filesystem outputs disagree, recover by listing both and marking the discrepancy in the risk register.

## Examples

### Small Repo (10 prompts)

Analyze a 10-prompt repo, produce `STAGE-1-POST-FLIGHT.md`, score documentation/setup gaps, and recommend 3 stage-2 prompts focused on tests and operator UX.

### Larger Repo (25 prompts)

Score a 25-prompt repo with multiple subsystems, quantify overengineering risk in the risk register, and map each recommended stage-2 investment to expected score gains.
