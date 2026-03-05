---
id: prompt-resume-reconciler
name: Prompt Resume Reconciler
description: Reconcile prompt execution state using prompt files, commit prefixes, and artifact evidence to determine the next dependency-ready prompt.
version: 0.1.0
tags: [workflow, resume, prompts]
inputs:
  - name: repo_root
    type: path
    required: true
    default: .
    examples: ["."]
  - name: prompts_dir
    type: path
    required: false
    default: .prompts
    examples: [".prompts"]
  - name: strict_artifact_gate
    type: bool
    required: false
    default: true
    examples: [true, false]
expected_tools: [git, rg, python3]
safety:
  dry_run_supported: true
  destructive_actions: []
  confirmation_points:
    - "Confirm before marking a prompt as completed when evidence is ambiguous"
outputs:
  - docs/RESUME_RECONCILIATION.md
  - skills-foundry/reports/resume-reconciliation.json
---

## When to use

Use when prompt execution has been interrupted or the repo has mixed manual/automated commits and you need a deterministic "next prompt" decision.

## Inputs

- `repo_root`: repository root path.
- `prompts_dir`: location of prompt files.
- `strict_artifact_gate`: require artifact evidence in addition to commit-prefix evidence.

## Procedure

1. Enumerate prompt files and derive candidate sequence with dependency hints.
2. Parse commit subjects for prompt completion prefixes (`[PROMPT_XX]`, `[PROMPT_XX, AGENT_*]`).
3. Collect artifact evidence for each prompt's acceptance outputs.
4. Mark prompts complete only when commit and artifact evidence are coherent.
5. Select the earliest dependency-ready uncompleted prompt.
6. Write reconciliation summary and confidence notes for operator review.

## Success criteria

- Next prompt decision is reproducible from repository state.
- Ambiguous completion signals are called out explicitly.
- Output includes both commit and artifact evidence references.

## Failure modes + recovery

- If dependencies are ambiguous, halt and request sequencing clarification.
- If commit evidence conflicts with artifact evidence, mark as unresolved and do not auto-advance.
- If prompt files are missing, stop and report missing paths.

## Examples

### Resume after partial Stage run

Reconcile completed prompt commits vs artifacts and output the next safe prompt to execute.

### Audit-only reconciliation

Run read-only reconciliation to verify expected prompt completion before a handoff.
