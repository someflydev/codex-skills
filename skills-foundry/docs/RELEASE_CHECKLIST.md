# Release Checklist (Lightweight)

Use this checklist before tagging a version or sharing the foundry more broadly.

## 1. Verify Core Behavior

- Run `cd skills-foundry && ../.venv/bin/pytest -q`
- Run `cd skills-foundry && bin/skills-validate --compact`
- Run `cd skills-foundry && bin/skills-lint`
- Run `cd skills-foundry && bin/smoke-check-foundry --dry-run-only`

## 2. Check Docs and Examples

- `skills-foundry/README.md` reflects current CLI behavior and limitations
- `skills-foundry/docs/OPERATOR_MANUAL.md` matches the current smoke flow
- Refresh `skills-foundry/docs/examples/` snippets if output formats changed
- `POST_FLIGHT_REPORT.md` and `FRONT_FACING_IDEAS.md` are updated if post-flight work changed scope

## 3. Check Packaging Signals

- CI workflow file exists and is current (`.github/workflows/ci.yml`)
- Root `README.md` still points to the correct entrypoints
- Version in `skills-foundry/pyproject.toml` is intentional for this release
- `LICENSE` exists at the repo root and matches the intended distribution terms
- `skills-foundry/docs/DEPRECATIONS.md` reflects current deprecated aliases and canonical replacements

## 4. Tag/Release Prep (Optional)

- Update `skills-foundry/CHANGELOG.md` (or capture equivalent release notes if intentionally not using the changelog file)
- Record notable behavior changes (CLI flags, defaults, output formats)
- Document known limitations (especially `repo-helper-*` helper-only scope and deprecated `repo-*` aliases)
- If alias removals are planned, add/update a deprecation-policy note and target in `skills-foundry/docs/DEPRECATIONS.md`

## 4a. Changelog / Release Notes Convention (Lightweight)

- Prefer one `## Unreleased` section in `skills-foundry/CHANGELOG.md` while iterating locally.
- When tagging/releasing, move the relevant bullets into a dated/versioned section and start a fresh `## Unreleased`.
- Keep entries concrete and operator-facing: what changed, why it matters, and any migration/behavior notes.

## 5. Post-Release Follow-Through

- Capture any new gaps in `.prompts/improvements-before-finalization.txt` or a follow-up issue tracker
- If examples were refreshed, note which commands/generated outputs they came from
