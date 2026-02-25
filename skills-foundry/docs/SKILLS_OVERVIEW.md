# Skills Overview

## Purpose

`skills-foundry` is a repo-local workspace for building and curating Codex skills that can be
installed into `~/.codex/skills/<skill-id>/SKILL.md`.

## Organization

- `skills/<category>/<skill-id>/` stores source skill artifacts.
- `templates/` stores reusable authoring templates.
- `bin/` stores operator CLIs.
- `reports/` stores generated validation/lint/preflight/catalog outputs.
- `docs/` stores durable operator and authoring documentation.

## Sync Model

Skills are authored locally, validated/linted, then synchronized into `~/.codex/skills` using
`bin/skills-sync` (implemented in later prompts).
