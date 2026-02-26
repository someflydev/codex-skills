# Deprecations (Workflow Helpers)

This file tracks deprecations that affect operator-facing CLI usage.

## Current Deprecations

| Deprecated command | Canonical replacement | Status | Target removal | Notes |
|---|---|---|---|---|
| `bin/repo-preflight` | `bin/repo-helper-preflight` | Deprecated alias (prints warning) | Next breaking CLI cleanup release (TBD) | Helper-first naming clarifies scope |
| `bin/repo-stage1-run` | `bin/repo-helper-stage1-plan` | Deprecated alias (prints warning) | Next breaking CLI cleanup release (TBD) | Canonical command supports opt-in Stage-1 execution MVP |
| `bin/repo-postflight` | `bin/repo-helper-postflight` | Deprecated alias (prints warning) | Next breaking CLI cleanup release (TBD) | Snapshot helper only |
| `bin/repo-stage2-plan` | `bin/repo-helper-stage2-theme-plan` | Deprecated alias (prints warning) | Next breaking CLI cleanup release (TBD) | Theme-planning helper only |
| `bin/repo-stage2-run` | `bin/repo-helper-stage2-run-plan` | Deprecated alias (prints warning) | Next breaking CLI cleanup release (TBD) | Run-plan helper only |

## Policy Notes

- Deprecated aliases remain for compatibility while docs and operator habits migrate.
- Removal timing is intentionally conservative and may shift until a clear versioning cadence exists.
- Changelog entries should call out any alias removals or behavior changes before they land.
