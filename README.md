# codex-skills

Prompt-built Codex skills tooling and content, with the generated project living in `skills-foundry/`.

## What Is In This Repo

- `.prompts/` - the ordered prompt plan used to build and iterate the project
- `skills-foundry/` - the actual deliverable (CLI tools, skill library, templates, docs, tests)
- `POST_FLIGHT_REPORT.md` - engineering audit + completeness scoring
- `FRONT_FACING_IDEAS.md` - packaging/readme/frontend positioning concepts

## Start Here

If you want to use the generated toolkit, start in `skills-foundry/`:

```bash
cd skills-foundry
uv venv .venv
uv pip install --python .venv/bin/python pytest
.venv/bin/pytest -q
bin/skills-validate
bin/skills-lint
```

Then read:

- `skills-foundry/README.md` for current capabilities and quickstart
- `skills-foundry/docs/OPERATOR_MANUAL.md` for the prompt-first workflow and smoke-run examples
- `skills-foundry/docs/examples/` for tracked proof snippets (sync plan, lint summary, catalog excerpt)

## Prompt Lineage / Audit Artifacts

- Initial prompt preflight fixes: `.prompts/improvements-before-initial-run.txt`
- Finalization audit/fix log: `.prompts/improvements-before-finalization.txt`

## Current Scope (Important)

- `skills-foundry/bin/skills-*` commands are functional and tested.
- `skills-foundry/bin/repo-*` commands are **MVP workflow helpers** (preflight inventory, run planning, postflight snapshots, stage-2 planning). They do not execute prompts automatically.
