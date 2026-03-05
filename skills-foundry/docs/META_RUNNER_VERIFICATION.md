# Meta Runner Verification

## Purpose

Provide a deterministic verification checklist for the Stage-3 meta-runner skill group.

## Root-Level Commands

Run from repository root:

```bash
.venv/bin/pytest -q skills-foundry/tests/test_meta_runner_skills.py
./skills-foundry/bin/smoke-check-meta-runner --help
./skills-foundry/bin/smoke-check-meta-runner --check-only
```

Optional full-suite verification:

```bash
.venv/bin/pytest -q skills-foundry
```

## What These Checks Validate

- Required `meta-runner` skill IDs exist.
- Required metadata and section contracts are present in each `SKILL.md`.
- Safety contracts include dry-run and confirmation points.
- Failure-mode sections include explicit stop/halt behavior.
- Meta-runner smoke command runs deterministic non-destructive checks.

## CI Expectation

`.github/workflows/ci.yml` includes a lightweight check-only smoke step:

```bash
bin/smoke-check-meta-runner --check-only
```
