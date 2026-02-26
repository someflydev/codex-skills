# Changelog

This is a lightweight changelog for `skills-foundry`.

Use it for release notes and notable local hardening changes. Keep entries brief,
operator-facing, and specific (CLI flags/defaults, report formats, workflow
behavior, docs changes that affect usage).

## Unreleased

### Added

- `skills-validate --compact` preset for lower-noise day-to-day validation runs.
- `bin/smoke-check-foundry` repeatable smoke script target.
- `docs/RELEASE_CHECKLIST.md` lightweight release-readiness checklist.
- Canonical `repo-helper-*` workflow helper CLIs with clearer helper-first naming.

### Changed

- Lint reports now emit repo-relative paths by default (`skills-lint --absolute-paths` to opt in).
- Root README includes a repo map and "First 5 Minutes" onboarding flow.
- `repo-*` helper CLIs are now deprecated aliases that print migration warnings to stderr.

### Notes

- `repo-*` commands are MVP workflow helpers (planning/snapshots), not full prompt execution automation.
- Alias deprecation policy and removal targets are tracked in `docs/DEPRECATIONS.md`.
