# codex-skills

Prompt-built Codex skills tooling and content, with the generated project living in `skills-foundry/`.

## What Is In This Repo

- `.prompts/` - the ordered prompt plan used to build and iterate the project
- `skills-foundry/` - the actual deliverable (CLI tools, skill library, templates, docs, tests)
- `POST_FLIGHT_REPORT.md` - engineering audit + completeness scoring
- `FRONT_FACING_IDEAS.md` - packaging/readme/frontend positioning concepts

## Repo Map (Quick Orientation)

```text
codex-skills/
├── .prompts/                      # prompt plan + preflight/finalization logs
├── skills-foundry/                # main deliverable (use this first)
│   ├── bin/                       # CLI tools + smoke script
│   ├── skills/                    # source skill library
│   ├── docs/                      # operator/authoring docs + examples
│   ├── templates/                 # skill/pack templates
│   ├── tests/                     # pytest coverage
│   └── reports/                   # generated local outputs (git-ignored)
├── POST_FLIGHT_REPORT.md          # engineering audit
└── FRONT_FACING_IDEAS.md          # packaging/frontend concepts
```

## First 5 Minutes

1. Run the tests to confirm your local setup:
   - `cd skills-foundry && .venv/bin/pytest -q` (or create `.venv` first from the quickstart below)
2. Run compact validation to see a lower-noise health check:
   - `cd skills-foundry && bin/skills-validate --compact`
3. Run the repeatable smoke script:
   - `cd skills-foundry && bin/smoke-check-foundry --dry-run-only`
4. Read the operator workflow:
   - `skills-foundry/docs/OPERATOR_MANUAL.md`
5. Review tracked proof snippets:
   - `skills-foundry/docs/examples/`

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
- `skills-foundry/docs/RELEASE_CHECKLIST.md` for a lightweight release readiness checklist

## Prompt Lineage / Audit Artifacts

- Initial prompt preflight fixes: `.prompts/improvements-before-initial-run.txt`
- Finalization audit/fix log: `.prompts/improvements-before-finalization.txt`

## Current Scope (Important)

- `skills-foundry/bin/skills-*` commands are functional and tested.
- `skills-foundry/bin/repo-*` commands are **MVP workflow helpers** (preflight inventory, run planning, postflight snapshots, stage-2 planning). They do not execute prompts automatically.
