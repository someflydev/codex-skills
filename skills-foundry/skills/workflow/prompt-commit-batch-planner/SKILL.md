---
id: prompt-commit-batch-planner
name: Prompt Commit Batch Planner
description: Plan Tim Pope style commit groups for prompt-scoped changes, using dependency-safe boundaries and audit-friendly rationale.
version: 0.1.0
tags: [workflow, git, commits]
inputs:
  - name: repo_root
    type: path
    required: true
    default: .
    examples: ["."]
  - name: prompt_id
    type: string
    required: true
    default: PROMPT_XX
    examples: ["PROMPT_24", "PROMPT_25"]
  - name: agent_role
    type: string
    required: false
    default: AGENT_BUILDER
    examples: ["AGENT_ARCHITECT", "AGENT_BUILDER", "AGENT_AUDITOR"]
expected_tools: [git, rg]
safety:
  dry_run_supported: true
  destructive_actions: []
  confirmation_points:
    - "Confirm before staging/committing any hunk set"
outputs:
  - docs/COMMIT_BATCH_PLAN.md
  - skills-foundry/reports/commit-batch-plan.json
---

## When to use

Use after prompt-scoped implementation to create clean, reviewable commit groups with required prefix discipline.

## Inputs

- `repo_root`: repository root path.
- `prompt_id`: prompt identifier used in commit prefix.
- `agent_role`: role token for commit prefix.

## Procedure

1. Inspect changed files and classify hunks by behavior/intent.
2. Propose minimal commit groups with one responsibility each.
3. Validate that each group maps to the active prompt scope only.
4. Draft multi-line commit messages with rationale and verification notes.
5. Confirm group ordering (architecture -> implementation -> tests/docs).
6. Produce final batch plan and staging guidance (`git add -p`).

## Success criteria

- Commit groups are prompt-scoped and reviewable.
- Prefix format matches `[PROMPT_{num}, AGENT_{role}]`.
- Message body explains why each group exists.

## Failure modes + recovery

- If hunks are entangled, split with minimal refactors before committing.
- If scope crosses prompts, defer unrelated hunks to a separate run.
- If prefix cannot be derived safely, stop and ask for prompt mapping confirmation.

## Examples

### Prompt-Scoped Build Commit Plan

Generate grouped commit subjects and rationale for implementation + verification hunks.

### Audit-Only Review

Produce commit plan text without staging or committing.
