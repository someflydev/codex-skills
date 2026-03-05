---
id: manual-command-prooflogger
name: Manual Command Prooflogger
description: Capture exact command inputs/outputs with exit codes into a durable markdown artifact for audit and operator handoff.
version: 0.1.0
tags: [core, verification, docs]
inputs:
  - name: repo_root
    type: path
    required: true
    default: .
    examples: ["."]
  - name: output_file
    type: path
    required: false
    default: manual-tool-invocation-outputs.md
    examples: ["manual-tool-invocation-outputs.md"]
  - name: delimiter
    type: string
    required: false
    default: =============================================================================
    examples: ["============================================================================="]
expected_tools: [bash]
safety:
  dry_run_supported: true
  destructive_actions: []
  confirmation_points:
    - "Confirm before running commands that may modify project state"
outputs:
  - docs/manual-command-prooflogging.md
  - manual-tool-invocation-outputs.md
---

## When to use

Use when you need reproducible command evidence for documentation, audits, or regression verification.

## Inputs

- `repo_root`: repository root path.
- `output_file`: markdown file used for captured command evidence.
- `delimiter`: readable separator between command/result blocks.

## Procedure

1. Enumerate commands to verify and classify as read-only or mutating.
2. Run commands in deterministic order from repo root.
3. Capture command input, stdout/stderr summary, and exit code.
4. Append each pair with the configured delimiter and spacing.
5. Flag non-zero exits with concise diagnosis notes.
6. Save prooflog and summarize verification coverage.

## Success criteria

- Evidence file includes command, output, and exit code for each step.
- Delimiters make scan/review easy.
- Non-zero exits are documented with context.

## Failure modes + recovery

- If output is nondeterministic, document variable fields and rerun minimal reproduction.
- If a command is unsafe in current context, skip and record rationale.
- If prooflog format drifts, normalize with a single template and rerun captures.

## Examples

### Document Root-Level Tool Invocations

Capture command/output pairs for docs examples before a release.

### Verify Smoke/Test Commands

Record smoke/test command outputs as evidence for a postflight report.
