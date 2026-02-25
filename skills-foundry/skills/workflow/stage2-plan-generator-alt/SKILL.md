---
id: stage2-plan-generator-alt
name: Stage2 Plan Generator (ALT)
description: Stage-2 plan generator variant that prioritizes risk burn-down and operational hardening before feature-completeness maximization.
version: 0.1.0
tags: [workflow, stage2, planning, alt]
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
  - name: planning_mode
    type: enum
    required: false
    default: risk-first
    examples: ["risk-first"]
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
  - skills-foundry/reports/stage2-plan-risk-matrix.md
---

## When to use

Use this variant when stage-1 postflight identifies major fragility and you want stage-2 prompts sequenced to reduce operational risk before chasing maximum feature coverage.

## Inputs

- `repo_root`: path to the target repository that contains `.prompts/`.
- `prompt_range` / `prompt_selection`: optional filter for prompts to inspect or run.
- `commit_mode`: whether to propose patch groupings only or also commit after confirmation.
- `report_path`: optional override for generated report output when the skill writes a report.

## Procedure

1. Parse the postflight risk register and cluster issues by severity/likelihood so prompt planning starts from the highest-risk failure modes.
2. Draft stage-2 prompts that reduce risk first (tests, validation, scripts, documentation, rollback safety), then add feature work only after those prerequisites are covered.
3. For each prompt, document the specific risk(s) it mitigates and the acceptance checks that prove the mitigation works.
4. Keep prompt count small and sharply scoped to avoid reintroducing overengineering during the hardening phase.
5. Write the stage-2 prompt files and a risk-first planning report with sequencing rationale and deferred items.
6. Recommend `[PROMPT_XX]` commit groups that mirror the risk themes so review remains straightforward.

## Success criteria

- Each stage-2 prompt is tied to explicit risk mitigation goals.
- Hardening work is sequenced before dependent feature expansion.
- Deferred feature ideas are documented instead of silently dropped.

## Failure modes + recovery

- If the postflight report lacks a usable risk register, recover by extracting risks from the repo and prompts explicitly before drafting prompts.
- If risk-first sequencing conflicts with business priorities, document the tradeoff and request operator prioritization.
- If a prompt grows beyond a reviewable unit, split it and regenerate numbering before proceeding.

## Examples

### Small Repo (10 prompts)

Plan 3-4 stage-2 prompts for a 10-prompt repo that first add smoke tests and setup validation, then address one high-impact missing feature.

### Larger Repo (25 prompts)

Create a 5-6 prompt risk-first stage-2 plan for a 25-prompt repo, tying each prompt to a specific postflight risk and measurable mitigation check.
