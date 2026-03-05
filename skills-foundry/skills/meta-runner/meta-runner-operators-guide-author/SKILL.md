---
id: meta-runner-operators-guide-author
name: Meta Runner Operators Guide Author
description: Build or refresh an operator-grade guide with root-level commands, diagnostics, datastore queries, and troubleshooting runbooks.
version: 0.1.0
tags: [meta-runner, docs, operations]
inputs:
  - name: repo_root
    type: path
    required: true
    default: .
    examples: ["."]
  - name: output_path
    type: path
    required: false
    default: OPERATORS_GUIDE.md
    examples: ["OPERATORS_GUIDE.md", "docs/OPERATORS_GUIDE.md"]
  - name: verify_commands
    type: bool
    required: false
    default: true
    examples: [true, false]
expected_tools: [rg, git, python3]
safety:
  dry_run_supported: true
  destructive_actions: []
  confirmation_points:
    - "Confirm before writing a new operators guide path"
    - "Confirm before running commands that may modify runtime state"
outputs:
  - OPERATORS_GUIDE.md
  - docs/manual-tool-invocation-outputs.md
---

## When to use

Use when operational docs need to be generated or refreshed with concrete, verified commands and troubleshooting guidance.

## Inputs

- `repo_root`: target repository path.
- `output_path`: operators guide destination.
- `verify_commands`: execute command examples and capture outputs.

## Procedure

1. Inventory services, storage backends, key scripts, and make targets.
2. Draft required guide sections with repo-specific commands and paths.
3. Normalize commands to root-level invocation where possible.
4. Verify representative commands and capture input/output evidence.
5. Add troubleshooting scenarios and quick diagnosis queries.
6. Cross-link related docs and ensure command examples are copy-pasteable.

## Success criteria

- Guide is concrete, repo-specific, and operationally useful.
- Command examples are verified or clearly marked as non-runnable with reasons.
- Root-level command forms are preferred throughout.

## Failure modes + recovery

- If core verification commands fail repeatedly, stop and publish a prerequisite/blocker checklist before proceeding.
- If required services are unavailable, document exact prerequisites and defer verification.
- If command examples are stale, update docs and rerun verification capture.
- If output path conflicts with existing docs conventions, align and document move rationale.

## Examples

### Initial guide creation

Generate a complete operators guide after stack inventory, including datastore query catalog and smoke commands.

### Drift refresh

Re-verify command examples after tooling changes and update manual invocation outputs.
