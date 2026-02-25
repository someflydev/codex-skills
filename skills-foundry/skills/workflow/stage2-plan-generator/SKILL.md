---
id: stage2-plan-generator
name: Stage2 Plan Generator
description: Generate 3-6 ordered stage-2 PROMPT_XX.txt files from STAGE-1-POST-FLIGHT.md, current repo state, and existing prompt history.
version: 0.1.0
tags: [workflow, stage2, planning]
inputs:
  - name: repo_root
    type: path
    required: true
    default: .
    examples: ["."]
  - name: postflight_report
    type: path
    required: true
    default: STAGE-1-POST-FLIGHT.md
    examples: ["STAGE-1-POST-FLIGHT.md"]
  - name: prompt_count_target
    type: int
    required: false
    default: 4
    examples: [3, 6]
expected_tools: [git, rg, python3]
safety:
  dry_run_supported: true
  destructive_actions: []
  confirmation_points:
    - "Confirm before applying fixes, pruning prompts, or auto-committing"
    - "Confirm before rerunning prompts after a failed run"
outputs:
  - .prompts/PROMPT_<NN>.txt
  - skills-foundry/reports/stage2-plan.md
---

## When to use

Use after stage-1 postflight to produce a focused stage-2 prompt plan that addresses missing artifacts and risk hotspots without duplicating completed work.

## Inputs

- `repo_root`: path to the target repository that contains `.prompts/`.
- `prompt_range` / `prompt_selection`: optional filter for prompts to inspect or run.
- `commit_mode`: whether to propose patch groupings only or also commit after confirmation.
- `report_path`: optional override for generated report output when the skill writes a report.

## Procedure

1. Read `STAGE-1-POST-FLIGHT.md`, current `.prompts/`, and the repo filesystem to identify unresolved gaps, fragile areas, and completed work that should not be repeated.
2. Choose the next prompt numbers in sequence and draft 3-6 stage-2 prompts with explicit deliverables, acceptance criteria, and non-goals.
3. Ensure each proposed prompt has a clean dependency boundary (what it requires, what it creates, what later prompts can depend on).
4. Bias the plan toward improvements that measurably raise completeness/excellence scores while keeping each prompt reviewable and testable.
5. Write the new prompt files and a summary plan report describing rationale, ordering, and expected score deltas.
6. Propose patch groupings and `[PROMPT_XX]` commit messages for the generated stage-2 prompt files.

## Success criteria

- New stage-2 prompts are ordered, explicit, and non-duplicative.
- Each prompt includes deliverables and acceptance criteria.
- The stage-2 plan explains why the proposed prompts improve postflight scores.

## Failure modes + recovery

- If `STAGE-1-POST-FLIGHT.md` is missing, stop and recover by generating postflight first rather than guessing stage-2 priorities.
- If next prompt numbers are ambiguous due to parallel branches, recover by asking the operator which numbering sequence is canonical.
- If proposed prompts depend on unbuilt infrastructure, split the plan and add prerequisite prompts before continuing.

## Examples

### Small Repo (10 prompts)

Generate 4 stage-2 prompts for a 10-prompt repo that improve tests, docs, and operator scripts, with explicit acceptance criteria and no repeated scaffolding work.

### Larger Repo (25 prompts)

Draft 6 stage-2 prompts for a 25-prompt repo, sequencing them around risk reduction and score impact while preserving previously completed subsystems.
