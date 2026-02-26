# Operator Manual

## Purpose

Run the `skills-foundry` workflow end-to-end on repositories that use ordered `.prompts/` files, from prompt preflight through stage-2 postflight.

## Install `skills-foundry`

`skills-foundry` is a local toolset in this repo (`skills-foundry/bin/*`). Use it in-place or add the `bin/` directory to your `PATH`.

### Local setup (recommended)

```bash
cd skills-foundry
uv venv .venv
uv pip install --python .venv/bin/python pytest
```

Run tools directly from `bin/` (no activation required), for example `bin/skills-validate`.

## Author Or Update Skills

1. Create a new skill skeleton:
   ```bash
   cd skills-foundry
   bin/skills-new --category workflow --skill-id my-skill --name "My Skill"
   ```
2. Edit `SKILL.md` (required), then refine `EXAMPLES.md` and `CHECKLIST.md`.
3. Keep IDs stable; evolve `version` as behavior changes.
4. Treat `-alt` variants as separate skills with separate IDs and versions.

## Validate + Lint

Run validation before syncing or relying on a new skill pack:

```bash
cd skills-foundry
bin/skills-validate
bin/skills-lint
```

- `skills-validate` checks front matter and required sections.
- `skills-lint` writes reports to `skills-foundry/reports/skills-lint.json` and `skills-foundry/reports/skills-lint.md`.

## Sync To `~/.codex/skills`

Dry-run first:

```bash
cd skills-foundry
bin/skills-sync --dry-run
```

Typical real sync (copy strategy):

```bash
cd skills-foundry
bin/skills-sync --strategy copy
```

Useful options:

- `--strategy symlink` for local iteration.
- `--only skill-a --only skill-b` to sync a subset (comma-separated values are also accepted).
- `--prune --yes` to remove stale installed skills (review dry-run first).
- `--to /custom/path` to sync into a sandbox/test location instead of `~/.codex/skills`.

`skills-sync` writes an installed-skill index (`INDEX.md`) in the target directory during a real (non-dry-run) sync.

## Use Skills On A New Repo

1. Preflight the prompt set before the first run.
2. Run the stage-1 prompts and commit in prompt-sized patches.
3. Postflight stage-1 and generate a stage-2 plan.
4. Run stage-2 preflight, then execute stage-2 prompts with checkpoints.
5. Postflight stage-2, prune low-value follow-ups, and document the final state.

Recommended operator habit: use `git add -p` and prompt-prefixed commits (for example `[PROMPT_07] ...`) after each prompt run.

## Demo Repo (Tiny Prompt Set)

A tiny practice repo lives at `skills-foundry/demo-repo/` with a simple 6-file `.prompts/` sequence.

- Prompt set path: `skills-foundry/demo-repo/.prompts/`
- Run instructions: `skills-foundry/demo-repo/README.md`
- Use it to test the prompt-first workflow without a large build.

## Prompt-First Repo Lifecycle Walkthrough

### Stage 1

1. `stage-1 preflight`
   - Audit `.prompts/` for ordering, dependencies, naming, and scope risks.
   - Apply only conservative fixes.
2. `stage-1 run`
   - Execute prompts in order.
   - Group diffs into prompt-sized commits.
3. `stage-1 postflight`
   - Review what shipped, what drifted, and what broke.
   - Produce a risk register and stage-2 inputs.

### Stage 2

1. `stage-2 plan`
   - Turn postflight findings into a small, ordered hardening/expansion plan.
2. `stage-2 preflight`
   - Re-check the new prompt set for sequencing and dependency issues.
3. `stage-2 run`
   - Execute stage-2 prompts with checkpoints and verification gates.
4. `stage-2 postflight`
   - Measure deltas vs stage-1, capture regressions, and define follow-ups.

## Smoke Run (Executed)

The following smoke commands were actually run in this repo on February 25, 2026.

Canonical command examples (repo root -> foundry root):

```bash
cd skills-foundry
bin/skills-new --category core --skill-id smoke-check --name "Smoke Check"
bin/skills-validate
bin/skills-lint
bin/skills-sync --dry-run --to /tmp/skills-sync-smoke
bin/skills-render
```

### Key outputs and results

- `skills-new`
  - Created `skills-foundry/skills/core/smoke-check/{SKILL.md,EXAMPLES.md,CHECKLIST.md}`.
- `skills-validate`
  - `Validated 27 skills: 0 error(s), 60 warning(s)`
  - Warnings were best-effort missing output paths (expected for many skill-declared outputs that are created only when the skills run).
- `skills-lint`
  - `Linted 27 skills`
  - Reports generated: `skills-foundry/reports/skills-lint.json`, `skills-foundry/reports/skills-lint.md`
  - `smoke-check` and existing skills scored `completeness=100 excellence=10`
- `skills-sync --dry-run --to /tmp/skills-sync-smoke`
  - Pre-sync validation/lint ran automatically.
  - Sync plan: `create=27, update=0, unchanged=0, would-prune=0`
  - Confirmed no files were written in dry-run mode.
- `skills-render`
  - Rendered catalog for `27` skills.
  - Output: `skills-foundry/reports/SKILLS_CATALOG.md`

### Additional index generation proof

Because `--dry-run` does not write the target index, an extra local sync was run to generate a real index without touching `~/.codex/skills`:

```bash
cd skills-foundry
bin/skills-sync --to /tmp/skills-sync-smoke
```

Result:

- Installed-skill index generated at `/tmp/skills-sync-smoke/INDEX.md` (36 lines during this run).

### Bin script sanity check

All operator-facing scripts in `skills-foundry/bin/` were checked with `--help` and passed (`10/10` executable, `10/10` exit code `0`).

## Sync Notes (Copy vs Symlink)

- Use `--strategy copy` for a portable installed snapshot.
- Use `--strategy symlink` while iterating locally when you want changes in the source repo to be reflected immediately in the installed skill directory.
- Use `--dry-run` before pruning or overwriting large sets.

## Design Notes

### Keep Skills Narrowly Scoped But Composable

- Give each skill one job with a clear input/output contract.
- Prefer small, chainable skills over one giant orchestrator skill.
- Compose through files and reports (for example, preflight report -> plan generator -> runner).

### Avoid Overengineering In Skills

- Start with direct procedures and only add scripts when repetition or reliability demands it.
- Avoid speculative plugin systems or meta-frameworks inside skill packs.
- Add verification gates early so weak skill content is caught before downstream packs depend on it.

### Evolve Skill Packs Without Breaking IDs

- Keep `id` stable once the skill is used in docs or operator workflows.
- Use `version` changes and changelog notes (in repo docs/commits) for evolution.
- Add new variants as new IDs (`-alt`) instead of silently changing existing skill semantics.
