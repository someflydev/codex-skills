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
- Decide whether a license file is required for the intended audience/distribution

## 4. Tag/Release Prep (Optional)

- Add a short changelog note (even if only in release notes / commit summary)
- Record notable behavior changes (CLI flags, defaults, output formats)
- Document known limitations (especially `repo-*` helper-only scope)

## 5. Post-Release Follow-Through

- Capture any new gaps in `.prompts/improvements-before-finalization.txt` or a follow-up issue tracker
- If examples were refreshed, note which commands/generated outputs they came from
