# Reference Examples Expansion Plan

## Scope

Expand high-value reference examples in this repository through staged, acceptance-driven prompt batches.

- Focus area: reference examples for prompt-first orchestration, operator workflows, verification discipline, and runbook usability.
- Explicitly out of scope: adding new external data sources.

## Domain And Workflow Inference (Evidence-Based)

Practical domain inferred from repository evidence:
- prompt-first repository build orchestration,
- reusable operational/reference assets (`skills-foundry/skills/*`),
- deterministic validation/smoke checks,
- operator-facing docs and examples.

Key evidence:
- `skills-foundry/bin/*` CLIs (authoring, validation, sync, render, flow-next, smoke checks)
- `skills-foundry/docs/*` operational/manual/runbook surfaces
- `.prompts/PROMPT_00_s.txt`..`PROMPT_21.txt` prompt lineage
- `skills-foundry/tests/*` contract/behavior coverage

## Baseline Coverage (Phase 1)

Discovery commands run:

```bash
./skills-foundry/bin/skills-validate --compact
.venv/bin/pytest -q skills-foundry
find skills-foundry/skills -name SKILL.md | sort
```

Observed status:
- Total reference examples discovered: 38
- Structural artifacts present for all 38 (`SKILL.md`, `CHECKLIST.md`, `EXAMPLES.md`)
- Validation status: 0 errors, 13 warnings (`missing_output_path`), mapping to 11 examples marked Partial
- Test suite status: `41 passed`

### Current Example Inventory

| example_id | category | status | evidence_paths |
|---|---|---|---|
| `changelog-drafter` | `core` | Full | `skills-foundry/skills/core/changelog-drafter/SKILL.md`, `skills-foundry/skills/core/changelog-drafter/CHECKLIST.md`, `skills-foundry/skills/core/changelog-drafter/EXAMPLES.md` |
| `hello-skill` | `core` | Full | `skills-foundry/skills/core/hello-skill/SKILL.md`, `skills-foundry/skills/core/hello-skill/CHECKLIST.md`, `skills-foundry/skills/core/hello-skill/EXAMPLES.md` |
| `hello-skill-alt` | `core` | Full | `skills-foundry/skills/core/hello-skill-alt/SKILL.md`, `skills-foundry/skills/core/hello-skill-alt/CHECKLIST.md`, `skills-foundry/skills/core/hello-skill-alt/EXAMPLES.md` |
| `repo-tree-summarizer` | `core` | Full | `skills-foundry/skills/core/repo-tree-summarizer/SKILL.md`, `skills-foundry/skills/core/repo-tree-summarizer/CHECKLIST.md`, `skills-foundry/skills/core/repo-tree-summarizer/EXAMPLES.md` |
| `smoke-check` | `core` | Full | `skills-foundry/skills/core/smoke-check/SKILL.md`, `skills-foundry/skills/core/smoke-check/CHECKLIST.md`, `skills-foundry/skills/core/smoke-check/EXAMPLES.md` |
| `meta-runner-bootstrap` | `meta-runner` | Partial | `skills-foundry/skills/meta-runner/meta-runner-bootstrap/SKILL.md`, `skills-foundry/skills/meta-runner/meta-runner-bootstrap/CHECKLIST.md`, `skills-foundry/skills/meta-runner/meta-runner-bootstrap/EXAMPLES.md` |
| `meta-runner-operators-guide-author` | `meta-runner` | Full | `skills-foundry/skills/meta-runner/meta-runner-operators-guide-author/SKILL.md`, `skills-foundry/skills/meta-runner/meta-runner-operators-guide-author/CHECKLIST.md`, `skills-foundry/skills/meta-runner/meta-runner-operators-guide-author/EXAMPLES.md` |
| `meta-runner-port-isolation` | `meta-runner` | Partial | `skills-foundry/skills/meta-runner/meta-runner-port-isolation/SKILL.md`, `skills-foundry/skills/meta-runner/meta-runner-port-isolation/CHECKLIST.md`, `skills-foundry/skills/meta-runner/meta-runner-port-isolation/EXAMPLES.md` |
| `meta-runner-postflight-analyzer` | `meta-runner` | Full | `skills-foundry/skills/meta-runner/meta-runner-postflight-analyzer/SKILL.md`, `skills-foundry/skills/meta-runner/meta-runner-postflight-analyzer/CHECKLIST.md`, `skills-foundry/skills/meta-runner/meta-runner-postflight-analyzer/EXAMPLES.md` |
| `meta-runner-postflight-analyzer-alt` | `meta-runner` | Full | `skills-foundry/skills/meta-runner/meta-runner-postflight-analyzer-alt/SKILL.md`, `skills-foundry/skills/meta-runner/meta-runner-postflight-analyzer-alt/CHECKLIST.md`, `skills-foundry/skills/meta-runner/meta-runner-postflight-analyzer-alt/EXAMPLES.md` |
| `meta-runner-preflight-inspector` | `meta-runner` | Full | `skills-foundry/skills/meta-runner/meta-runner-preflight-inspector/SKILL.md`, `skills-foundry/skills/meta-runner/meta-runner-preflight-inspector/CHECKLIST.md`, `skills-foundry/skills/meta-runner/meta-runner-preflight-inspector/EXAMPLES.md` |
| `meta-runner-preflight-inspector-alt` | `meta-runner` | Full | `skills-foundry/skills/meta-runner/meta-runner-preflight-inspector-alt/SKILL.md`, `skills-foundry/skills/meta-runner/meta-runner-preflight-inspector-alt/CHECKLIST.md`, `skills-foundry/skills/meta-runner/meta-runner-preflight-inspector-alt/EXAMPLES.md` |
| `meta-runner-stage-runner` | `meta-runner` | Partial | `skills-foundry/skills/meta-runner/meta-runner-stage-runner/SKILL.md`, `skills-foundry/skills/meta-runner/meta-runner-stage-runner/CHECKLIST.md`, `skills-foundry/skills/meta-runner/meta-runner-stage-runner/EXAMPLES.md` |
| `meta-runner-stage-runner-alt` | `meta-runner` | Partial | `skills-foundry/skills/meta-runner/meta-runner-stage-runner-alt/SKILL.md`, `skills-foundry/skills/meta-runner/meta-runner-stage-runner-alt/CHECKLIST.md`, `skills-foundry/skills/meta-runner/meta-runner-stage-runner-alt/EXAMPLES.md` |
| `meta-runner-test-stack-isolation` | `meta-runner` | Partial | `skills-foundry/skills/meta-runner/meta-runner-test-stack-isolation/SKILL.md`, `skills-foundry/skills/meta-runner/meta-runner-test-stack-isolation/CHECKLIST.md`, `skills-foundry/skills/meta-runner/meta-runner-test-stack-isolation/EXAMPLES.md` |
| `meta-runner-ui-audit-playwright` | `meta-runner` | Full | `skills-foundry/skills/meta-runner/meta-runner-ui-audit-playwright/SKILL.md`, `skills-foundry/skills/meta-runner/meta-runner-ui-audit-playwright/CHECKLIST.md`, `skills-foundry/skills/meta-runner/meta-runner-ui-audit-playwright/EXAMPLES.md` |
| `backend-choice-to-prompts` | `polyglot` | Full | `skills-foundry/skills/polyglot/backend-choice-to-prompts/SKILL.md`, `skills-foundry/skills/polyglot/backend-choice-to-prompts/CHECKLIST.md`, `skills-foundry/skills/polyglot/backend-choice-to-prompts/EXAMPLES.md` |
| `backend-choice-to-prompts-alt` | `polyglot` | Full | `skills-foundry/skills/polyglot/backend-choice-to-prompts-alt/SKILL.md`, `skills-foundry/skills/polyglot/backend-choice-to-prompts-alt/CHECKLIST.md`, `skills-foundry/skills/polyglot/backend-choice-to-prompts-alt/EXAMPLES.md` |
| `backend-language-shortlister` | `polyglot` | Full | `skills-foundry/skills/polyglot/backend-language-shortlister/SKILL.md`, `skills-foundry/skills/polyglot/backend-language-shortlister/CHECKLIST.md`, `skills-foundry/skills/polyglot/backend-language-shortlister/EXAMPLES.md` |
| `backend-language-shortlister-alt` | `polyglot` | Full | `skills-foundry/skills/polyglot/backend-language-shortlister-alt/SKILL.md`, `skills-foundry/skills/polyglot/backend-language-shortlister-alt/CHECKLIST.md`, `skills-foundry/skills/polyglot/backend-language-shortlister-alt/EXAMPLES.md` |
| `storage-zoo-planner` | `storage-labs` | Full | `skills-foundry/skills/storage-labs/storage-zoo-planner/SKILL.md`, `skills-foundry/skills/storage-labs/storage-zoo-planner/CHECKLIST.md`, `skills-foundry/skills/storage-labs/storage-zoo-planner/EXAMPLES.md` |
| `storage-zoo-planner-alt` | `storage-labs` | Full | `skills-foundry/skills/storage-labs/storage-zoo-planner-alt/SKILL.md`, `skills-foundry/skills/storage-labs/storage-zoo-planner-alt/CHECKLIST.md`, `skills-foundry/skills/storage-labs/storage-zoo-planner-alt/EXAMPLES.md` |
| `synthetic-data-spec-author` | `storage-labs` | Full | `skills-foundry/skills/storage-labs/synthetic-data-spec-author/SKILL.md`, `skills-foundry/skills/storage-labs/synthetic-data-spec-author/CHECKLIST.md`, `skills-foundry/skills/storage-labs/synthetic-data-spec-author/EXAMPLES.md` |
| `synthetic-data-spec-author-alt` | `storage-labs` | Full | `skills-foundry/skills/storage-labs/synthetic-data-spec-author-alt/SKILL.md`, `skills-foundry/skills/storage-labs/synthetic-data-spec-author-alt/CHECKLIST.md`, `skills-foundry/skills/storage-labs/synthetic-data-spec-author-alt/EXAMPLES.md` |
| `prompt-postflight-analyzer` | `workflow` | Partial | `skills-foundry/skills/workflow/prompt-postflight-analyzer/SKILL.md`, `skills-foundry/skills/workflow/prompt-postflight-analyzer/CHECKLIST.md`, `skills-foundry/skills/workflow/prompt-postflight-analyzer/EXAMPLES.md` |
| `prompt-postflight-analyzer-alt` | `workflow` | Partial | `skills-foundry/skills/workflow/prompt-postflight-analyzer-alt/SKILL.md`, `skills-foundry/skills/workflow/prompt-postflight-analyzer-alt/CHECKLIST.md`, `skills-foundry/skills/workflow/prompt-postflight-analyzer-alt/EXAMPLES.md` |
| `prompt-preflight-inspector` | `workflow` | Full | `skills-foundry/skills/workflow/prompt-preflight-inspector/SKILL.md`, `skills-foundry/skills/workflow/prompt-preflight-inspector/CHECKLIST.md`, `skills-foundry/skills/workflow/prompt-preflight-inspector/EXAMPLES.md` |
| `prompt-preflight-inspector-alt` | `workflow` | Full | `skills-foundry/skills/workflow/prompt-preflight-inspector-alt/SKILL.md`, `skills-foundry/skills/workflow/prompt-preflight-inspector-alt/CHECKLIST.md`, `skills-foundry/skills/workflow/prompt-preflight-inspector-alt/EXAMPLES.md` |
| `prompt-stage1-runner` | `workflow` | Full | `skills-foundry/skills/workflow/prompt-stage1-runner/SKILL.md`, `skills-foundry/skills/workflow/prompt-stage1-runner/CHECKLIST.md`, `skills-foundry/skills/workflow/prompt-stage1-runner/EXAMPLES.md` |
| `prompt-stage1-runner-alt` | `workflow` | Full | `skills-foundry/skills/workflow/prompt-stage1-runner-alt/SKILL.md`, `skills-foundry/skills/workflow/prompt-stage1-runner-alt/CHECKLIST.md`, `skills-foundry/skills/workflow/prompt-stage1-runner-alt/EXAMPLES.md` |
| `stage2-plan-generator` | `workflow` | Full | `skills-foundry/skills/workflow/stage2-plan-generator/SKILL.md`, `skills-foundry/skills/workflow/stage2-plan-generator/CHECKLIST.md`, `skills-foundry/skills/workflow/stage2-plan-generator/EXAMPLES.md` |
| `stage2-plan-generator-alt` | `workflow` | Full | `skills-foundry/skills/workflow/stage2-plan-generator-alt/SKILL.md`, `skills-foundry/skills/workflow/stage2-plan-generator-alt/CHECKLIST.md`, `skills-foundry/skills/workflow/stage2-plan-generator-alt/EXAMPLES.md` |
| `stage2-postflight-analyzer` | `workflow` | Partial | `skills-foundry/skills/workflow/stage2-postflight-analyzer/SKILL.md`, `skills-foundry/skills/workflow/stage2-postflight-analyzer/CHECKLIST.md`, `skills-foundry/skills/workflow/stage2-postflight-analyzer/EXAMPLES.md` |
| `stage2-postflight-analyzer-alt` | `workflow` | Partial | `skills-foundry/skills/workflow/stage2-postflight-analyzer-alt/SKILL.md`, `skills-foundry/skills/workflow/stage2-postflight-analyzer-alt/CHECKLIST.md`, `skills-foundry/skills/workflow/stage2-postflight-analyzer-alt/EXAMPLES.md` |
| `stage2-preflight-inspector` | `workflow` | Partial | `skills-foundry/skills/workflow/stage2-preflight-inspector/SKILL.md`, `skills-foundry/skills/workflow/stage2-preflight-inspector/CHECKLIST.md`, `skills-foundry/skills/workflow/stage2-preflight-inspector/EXAMPLES.md` |
| `stage2-preflight-inspector-alt` | `workflow` | Partial | `skills-foundry/skills/workflow/stage2-preflight-inspector-alt/SKILL.md`, `skills-foundry/skills/workflow/stage2-preflight-inspector-alt/CHECKLIST.md`, `skills-foundry/skills/workflow/stage2-preflight-inspector-alt/EXAMPLES.md` |
| `stage2-runner` | `workflow` | Full | `skills-foundry/skills/workflow/stage2-runner/SKILL.md`, `skills-foundry/skills/workflow/stage2-runner/CHECKLIST.md`, `skills-foundry/skills/workflow/stage2-runner/EXAMPLES.md` |
| `stage2-runner-alt` | `workflow` | Full | `skills-foundry/skills/workflow/stage2-runner-alt/SKILL.md`, `skills-foundry/skills/workflow/stage2-runner-alt/CHECKLIST.md`, `skills-foundry/skills/workflow/stage2-runner-alt/EXAMPLES.md` |

## Full-Implementation Checklist (Hard Gate)

An example is "Full" only when all are true:

1) Contract artifact completeness:
- implementation spec file exists and is internally coherent,
- checklist and examples artifacts exist and align to the same behavior.

2) Repository integration:
- referenced artifact paths are valid for this repository context,
- root-level runnable commands are present where required.

3) Verification coverage:
- relevant tests exist and pass,
- smoke checks exist for workflow/runtime-impacting behavior and are non-destructive by default.

4) Documentation wiring:
- operator-facing docs reference the example correctly,
- any ordering/flow docs remain synchronized.

5) Evidence quality:
- acceptance commands are executable,
- outputs are reproducible and auditable.

## Gap Analysis

### Finish Existing Partials First (Highest Leverage)

Current partial set (11 examples) concentrates in two areas:
- workflow postflight/preflight examples,
- meta-runner runtime/output-path examples.

Primary gap pattern:
- `missing_output_path` warnings where referenced paths do not exist in-repo yet.

Recommendation:
- Batch A should normalize path realism and/or seed minimal fixture artifacts so these examples become executable and warning-free in this repository context.

### Add Net-New Examples Next

After closing partials, add new reference examples that improve:
- resume-mode prompt execution,
- deterministic commit-group planning,
- operator troubleshooting playbooks,
- verification artifact capture.

## Prioritized Expansion Backlog

### Top 5 Immediate Targets

1) Partial-path normalization and fixture seeding for warning-heavy examples.
2) Resume-state reconciliation reference example (prompt sequence + commit evidence + artifact gates).
3) Commit-grouping reference example (Tim Pope style grouping with prompt boundaries).
4) Verification-proof logger example (command input/output capture for operator audits).
5) Flow-aware runbook reference examples wired into generated flow docs.

### Next 10 Near-Term Targets

1) Drift triage reference example (artifact mismatch recovery).
2) Prompt dependency graph extraction example.
3) Prompt acceptance command synthesizer example.
4) Non-destructive smoke orchestration example.
5) Stage transition audit reference example.
6) Reference example quality scorer rubric helper.
7) CLI invocation normalization example pack.
8) Prompt corpus-to-skill mapping maintainer example.
9) Prompt manifest consistency checker example.
10) Pre-flight readiness summary generator example.

### Long-Tail Targets (Ordered Candidate Pool)

- Cross-track dependency conflict resolver
- Prompt numbering policy enforcer
- Prompt anti-scope regression checker
- Example freshness checker for docs snippets
- Runbook scenario simulator
- Failure signature cataloger
- Minimal patch recommendation helper
- Prompt acceptance replay tool
- Artifact drift timeline reporter
- Stage completion dashboard generator (docs-only)
- Demo repo parity checker
- Prompt-template rendering safety checker
- Operator handoff checklist author
- Batch stop-condition verifier
- Prompt evidence bundle exporter

## Batch Strategy (Stage-4)

### Batch A (Prompt 23) - Close Partial Coverage Gaps

Theme:
- convert current Partial examples to Full by resolving repository-context path gaps and adding minimal fixtures where appropriate.

### Batch B (Prompt 24) - Add New High-Signal Reference Examples

Theme:
- implement a focused set of net-new examples centered on resume, commit discipline, and verification traceability.

### Batch C (Prompt 25) - Verification, Docs, And Flow Integration

Theme:
- ensure new/updated examples are wired into tests, smoke checks, docs, and flow manifests with deterministic operator guidance.

## Prompt Dependencies

- `PROMPT_22.txt`: planning + batch prompt generation + manifest wiring
- `PROMPT_23.txt`: depends on 22 outputs
- `PROMPT_24.txt`: depends on 23 baseline stabilization
- `PROMPT_25.txt`: depends on 23 and 24 for final verification/wiring

## Readiness Notes

- Inventory evidence is sufficient to proceed.
- Validation/test tooling already works in current environment.
- Pre-flight pass must run before executing Stage-4 batches.

## Stage-4 Execution Status

### Batch A - Close Partial Coverage Gaps

- Status: Completed
- Result: compact validation warning count reduced from 13 to 0 without introducing destructive scaffolding.
- Evidence:
  - `./skills-foundry/bin/skills-validate --compact` -> `Validated 38 skills: 0 error(s), 0 warning(s)` (after Batch A changes)
  - `.venv/bin/pytest -q skills-foundry` -> passed
  - `./skills-foundry/bin/smoke-check-meta-runner --check-only` -> PASS

### Batch B - Add High-Signal Net-New Reference Examples

- Status: Completed
- Added examples:
  - `prompt-resume-reconciler`
  - `prompt-commit-batch-planner`
  - `manual-command-prooflogger`
  - `meta-runner-reference-example-curator`
- Integration:
  - wired into `flows/core.json`, `flows/workflow.json`, `flows/meta-runner.json`
  - regenerated `docs/SKILL_FLOWS.md`
  - added targeted integration test: `tests/test_reference_example_skills.py`

### Batch C - Verification, Docs, And Expansion Readiness

- Status: Completed
- Docs/examples manifest expanded with flow-reference snippets and validated with:
  - `./skills-foundry/bin/refresh-doc-examples --check`
- Operator docs refreshed for Stage-4 examples:
  - `skills-foundry/docs/OPERATOR_MANUAL.md`
  - `skills-foundry/README.md`

## Readiness Recommendation

- Stage-4 is ready to close.
- Recommended next wave: focus on one narrow follow-up batch that turns the new reference examples into end-to-end demonstration runs in `skills-foundry/demo-repo/` with explicit proof logs, while keeping non-destructive defaults.
