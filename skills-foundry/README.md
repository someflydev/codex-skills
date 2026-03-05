# skills-foundry

Repo-local toolkit for authoring, validating, linting, rendering, and syncing reusable Codex skills.

## What Works Today

- `./skills-foundry/bin/skills-new`: create a skill skeleton from templates
- `./skills-foundry/bin/skills-validate`: validate skill front matter + required sections (`--compact` recommended for day-to-day runs)
- `./skills-foundry/bin/skills-lint`: score skills and write JSON/Markdown lint reports
- `./skills-foundry/bin/skills-sync`: validate/lint + sync skills into `~/.codex/skills` (or another target) with dry-run, backups, and prune confirmation
- `./skills-foundry/bin/skills-render`: render a skills catalog markdown page
- `./skills-foundry/bin/repo-helper-*`: **MVP workflow helpers** for prompt inventory, run planning, postflight snapshots, and stage-2 planning (not full prompt execution automation)
- `skills-foundry/skills/meta-runner/*`: Stage-3 skill pack for resume-aware meta-runner bootstrap, preflight, stage execution, isolation workflows, and postflight scoring

## Quickstart

```bash
uv venv .venv
uv pip install --python .venv/bin/python pytest

./skills-foundry/bin/skills-new --category core --skill-id demo-skill --name "Demo Skill"
./skills-foundry/bin/skills-validate --compact
./skills-foundry/bin/skills-lint
./skills-foundry/bin/skills-sync --dry-run --to /tmp/skills-sync-smoke
./skills-foundry/bin/skills-render
```

See `docs/OPERATOR_MANUAL.md` for the prompt-first workflow walkthrough and smoke-run evidence.
For release readiness checks, see `docs/RELEASE_CHECKLIST.md`.
For helper alias migration policy, see `docs/DEPRECATIONS.md`.
For release notes/changelog conventions, see `CHANGELOG.md`.
Repository license terms are in the repo root `../LICENSE` (MIT).

## Project Layout

- `bin/` - CLI tools and workflow helpers
- `skills/` - source skill library (`<category>/<skill-id>/`)
- `skills/meta-runner/` - meta-runner orchestration skills (Stage-3)
- `templates/` - skill and pack-generation templates
- `docs/` - operator and authoring docs
- `docs/examples/` - curated tracked example outputs/snippets for packaging and front-facing proof
- `reports/` - generated lint/catalog outputs (intentionally git-ignored except `.gitkeep`)
- `demo-repo/` - tiny prompt-first practice repo
- `tests/` - pytest coverage for core CLIs

## Current Limitations

- `repo-helper-*` workflow commands are planning/snapshot helpers today; they do not execute prompts automatically.
- Deprecated `repo-*` aliases are still shipped for compatibility and print a migration warning to stderr.
- Alias removal timing is documented in `docs/DEPRECATIONS.md` and may shift until a stable release cadence exists.
- Lint/validate heuristics are practical but still evolving.
- CI is set up, but release packaging is still evolving (for example: release process remains manual).

## Curated Proof Artifacts

For tracked examples that do not require rerunning the CLIs locally, see `docs/examples/`.
Use `./skills-foundry/bin/refresh-doc-examples --check` to verify tracked snippets are current.
Use `./skills-foundry/bin/refresh-doc-examples` to refresh tracked snippets after intentional output changes.
