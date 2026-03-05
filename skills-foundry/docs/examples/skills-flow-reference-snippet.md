# Skill Flows

Ordered invocation lanes for skill groups. Keep skill IDs stable; ordering lives in flow manifests.

## core

Core utility skills and lightweight repo hygiene flow.

### Standard Lane

| Step | Skill ID | Why | Verify Command |
|---|---|---|---|
| 1 | `repo-tree-summarizer` | Inventory repository structure before modifications. | `rg --files . | head -n 50` |
| 2 | `changelog-drafter` | Draft meaningful change summaries once implementation stabilizes. | `test -f skills-foundry/CHANGELOG.md` |
| 3 | `smoke-check` | Run a bounded smoke pass before final commit recommendation. | `./skills-foundry/bin/smoke-check-foundry --dry-run-only` |
| 4 | `hello-skill` | Create or validate a simple baseline skill artifact. | `./skills-foundry/bin/skills-validate --compact` |
| 5 | `manual-command-prooflogger` | Capture reproducible command proof logs for audits and handoffs. | `test -f manual-tool-invocation-outputs.md || true` |

### Alt Lane

| Step | Skill ID | Why | Verify Command |
|---|---|---|---|
| 1 | `repo-tree-summarizer` | Inventory repository structure before modifications. | `rg --files . | head -n 50` |
| 2 | `changelog-drafter` | Draft meaningful change summaries once implementation stabilizes. | `test -f skills-foundry/CHANGELOG.md` |
| 3 | `smoke-check` | Run a bounded smoke pass before final commit recommendation. | `./skills-foundry/bin/smoke-check-foundry --dry-run-only` |
| 4 | `hello-skill-alt` | Use alternate baseline skill style when testing variant wording. | `./skills-foundry/bin/skills-validate --compact` |
| 5 | `manual-command-prooflogger` | Capture reproducible command proof logs for audits and handoffs. | `test -f manual-tool-invocation-outputs.md || true` |

## meta-runner

Resume-aware meta-runner flow from bootstrap through postflight closure.

### Standard Lane

| Step | Skill ID | Why | Verify Command |
|---|---|---|---|
