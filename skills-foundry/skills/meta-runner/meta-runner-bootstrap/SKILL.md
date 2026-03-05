---
id: meta-runner-bootstrap
name: Meta Runner Bootstrap
description: Generate or refresh a repository-specific .prompts/PROMPT_META_RUNNER.txt from live prompt inventory and execution history.
version: 0.1.0
tags: [meta-runner, bootstrap, prompts]
inputs:
  - name: repo_root
    type: path
    required: true
    default: .
    examples: [".", "../target-repo"]
  - name: prompts_dir
    type: path
    required: false
    default: .prompts
    examples: [".prompts"]
  - name: output_path
    type: path
    required: false
    default: .prompts/PROMPT_META_RUNNER.txt
    examples: [".prompts/PROMPT_META_RUNNER.txt"]
expected_tools: [git, rg, python3, uv]
safety:
  dry_run_supported: true
  destructive_actions: []
  confirmation_points:
    - "Confirm before overwriting an existing PROMPT_META_RUNNER.txt"
    - "Confirm before adding optional support files under .prompts/_meta or .prompts/rendered"
outputs:
  - .prompts/PROMPT_META_RUNNER.txt
  - .prompts/rendered/RENDER_LOG.md
---

## When to use

Use at the start of a repo or when prompt inventory/history has changed and the orchestration contract must be regenerated with dependency-aware resume behavior.

## Inputs

- `repo_root`: target repository path.
- `prompts_dir`: prompt directory to scan.
- `output_path`: destination meta-runner path.

## Procedure

1. Scan `.prompts/` recursively and classify prompt/system/template/support files.
2. Extract dependency hints, runtime/smoke references, and acceptance command patterns.
3. Parse git commit subjects for prompt completion prefixes and derive resume state.
4. Generate `PROMPT_META_RUNNER.txt` with execution modes, roles, gates, drift stops, and start procedure.
5. If template mode is required, create/update `.prompts/rendered/RENDER_LOG.md` without overwriting templates.
6. Re-read the generated file and verify section completeness before presenting commit groupings.

## Success criteria

- Generated file reflects current prompt structure and commit-history evidence.
- Start procedure resumes from the next dependency-ready prompt when prior execution exists.
- Tool verification and smoke-gate rules are explicit and actionable.

## Failure modes + recovery

- If `.prompts/` is missing, stop and request the correct repo root.
- If prompt dependencies are ambiguous, report competing chains and ask for operator direction.
- If generation would overwrite custom runner logic, show a targeted diff and require confirmation.

## Examples

### New repo bootstrap

Create the first `PROMPT_META_RUNNER.txt` from `PROMPT_00_s` + `PROMPT_01..N`, with start behavior defaulting to initial run.

### Existing repo refresh

Refresh `PROMPT_META_RUNNER.txt` after new prompts are added; resume mode picks the next uncompleted prompt using commit prefixes and artifact evidence.
