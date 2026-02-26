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
- `skills/docs-tools/` currently exists as an intentionally empty placeholder category for future documentation-oriented utility skills.

## Sync Model

Skills are authored locally, validated/linted, then synchronized into `~/.codex/skills` using
`bin/skills-sync`.

## Sync Strategies

- `copy`: stable snapshot in the target directory; safest for portability and sharing.
- `symlink`: faster local iteration while authoring, but target behavior depends on the source repo
  still existing at the same path.

## Versioning Guidance

- Keep `id` stable once a skill is published.
- Bump `version` for meaningful changes in procedure, safety, or outputs.
- Prefer new `-alt` skill ids for materially different variants instead of rewriting existing skill
  behavior under the same id.
