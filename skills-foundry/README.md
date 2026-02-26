# skills-foundry

Repo-local toolkit for authoring, validating, linting, rendering, and syncing reusable Codex skills.

## What Works Today

- `bin/skills-new`: create a skill skeleton from templates
- `bin/skills-validate`: validate skill front matter + required sections
- `bin/skills-lint`: score skills and write JSON/Markdown lint reports
- `bin/skills-sync`: validate/lint + sync skills into `~/.codex/skills` (or another target) with dry-run, backups, and prune confirmation
- `bin/skills-render`: render a skills catalog markdown page
- `bin/repo-*`: **MVP workflow helpers** for prompt inventory, run planning, postflight snapshots, and stage-2 planning (not full prompt execution automation)

## Quickstart

```bash
cd skills-foundry
uv venv .venv
uv pip install --python .venv/bin/python pytest

bin/skills-new --category core --skill-id demo-skill --name "Demo Skill"
bin/skills-validate
bin/skills-lint
bin/skills-sync --dry-run --to /tmp/skills-sync-smoke
bin/skills-render
```

See `docs/OPERATOR_MANUAL.md` for the prompt-first workflow walkthrough and smoke-run evidence.

## Project Layout

- `bin/` - CLI tools and workflow helpers
- `skills/` - source skill library (`<category>/<skill-id>/`)
- `templates/` - skill and pack-generation templates
- `docs/` - operator and authoring docs
- `docs/examples/` - curated tracked example outputs/snippets for packaging and front-facing proof
- `reports/` - generated lint/catalog outputs (intentionally git-ignored except `.gitkeep`)
- `demo-repo/` - tiny prompt-first practice repo
- `tests/` - pytest coverage for core CLIs

## Current Limitations

- `repo-*` workflow commands are planning/snapshot helpers today; they do not execute prompts automatically.
- Lint/validate heuristics are practical but still evolving.
- CI/release packaging is not set up yet.

## Curated Proof Artifacts

For tracked examples that do not require rerunning the CLIs locally, see `docs/examples/`.
