# Prompt Stage-2 Manifest

## Stage-2 Goals

Maximize completeness and excellence from the current `POST_FLIGHT_REPORT.md` baseline while explicitly controlling complexity creep.

Current baseline extracted from `POST_FLIGHT_REPORT.md`:
- Completeness: `91 / 100`
- General excellence: `8 / 10`
- P0/P1/P2: none remaining
- Remaining issues: P3 polish + limited automation breadth
- Highest-leverage improvement: add one narrow opt-in execution path on top of the helper CLIs (single safe stage, helper-first)

## Stage-2 Targets (derived from report)

### Must-fix (P0)
- None currently open.

### Should-fix (P1)
- None currently open.

### High-leverage Stage-2 targets (from P3 + report guidance)
- Add one narrow, safe, opt-in Stage-1 execution path on top of `repo-helper-*` planning helpers.
- Increase behavior-level coverage and CI checks for canonical helper commands and smoke script.
- Add safety/idempotency guardrails around helper execution and local smoke/demo cleanup.
- Close packaging gap with a chosen license + deprecation policy docs (requires human license choice).
- Add drift-control hooks for docs/examples and a lightweight rubric/lint rule mapping.

## Definition of Done for Stage-2 (DoD-S2)

- [ ] `repo-helper-stage1-plan` supports one opt-in execution mode with serial prompt execution, stop-on-failure, and run-log output (`skills-foundry/bin/_repo_workflow.py`, `skills-foundry/bin/repo-helper-stage1-plan`).
- [ ] Stage-1 execution MVP is covered by tests (success + failure path) and passes locally:
  - `cd skills-foundry && ../.venv/bin/pytest -q tests/test_repo_workflow_clis.py`
- [ ] CI uses canonical `repo-helper-*` commands and runs the scripted smoke check in dry-run mode:
  - `rg -n "repo-helper-" .github/workflows/ci.yml`
  - `rg -n "smoke-check-foundry --dry-run-only" .github/workflows/ci.yml`
- [ ] Operator safety/idempotency guardrails exist for helper execution/demo cleanup (bounded execution + dry-run reset tooling) with tests/docs.
- [ ] `skills-validate` provides a visible low-noise discovery path when warnings are high (hinting `--compact` if default verbose mode is used).
- [ ] Root packaging hygiene includes a real `LICENSE` file after explicit human choice:
  - `test -f LICENSE`
- [ ] Deprecation policy for deprecated `repo-*` aliases is documented:
  - `test -f skills-foundry/docs/DEPRECATIONS.md`
- [ ] Curated example refresh hook and manifest exist:
  - `test -f skills-foundry/bin/refresh-doc-examples`
  - `test -f skills-foundry/docs/examples/manifest.json`
- [ ] Additional curated proof snippets exist (lint JSON snippet + sync prune dry-run example).
- [ ] Full test suite passes at end of Stage-2:
  - `cd skills-foundry && ../.venv/bin/pytest -q`

## Minimal Deterministic Value Slice (must be provable by Stage-2 end)

- Bring-up (deterministic):
  - `cd skills-foundry && bin/repo-helper-stage1-plan --repo-root demo-repo --start 1 --end 2 --execute --runner-cmd-template "<deterministic local command>" --run-log demo-repo/STAGE1-RUN-LOG.md`
- Validation (deterministic):
  - `cd skills-foundry && bin/skills-validate --compact`
- Teardown (deterministic):
  - `cd skills-foundry && bin/demo-repo-reset --dry-run` (and non-dry-run if explicitly requested during prompt execution)
- Behavior-level proof:
  - `cd skills-foundry && ../.venv/bin/pytest -q tests/test_repo_workflow_clis.py`

## Planned Prompt Sequence + Why

1. `PROMPT_09.txt` — Narrow Stage-1 Execution Mode (Opt-In) + Deterministic Run Artifacts
   - Highest leverage completeness gain with minimal automation scope.

2. `PROMPT_10.txt` — Behavior-Level Tests + CI Gates for Helper Execution and Smoke Path
   - Locks in new behavior and prevents regression/drift in CI and helper command naming.

3. `PROMPT_11.txt` — Safety Guardrails + Idempotent Cleanup for Helper Execution and Validator UX
   - Adds operational safety and repeatability before expanding packaging/release expectations.

4. `PROMPT_12.txt` — Packaging + Release Hygiene Baseline (License Decision + Deprecation Policy)
   - Closes the largest remaining reuse/trust gap (license + deprecation policy docs).

5. `PROMPT_13.txt` — Light Specs + Drift-Control Hooks (Examples Refresh + Lint Rule Mapping)
   - Raises excellence by reducing documentation/proof drift and clarifying lint/rubric maintenance.

## Complexity / Overengineering Controls (Stage-2 wide)

- Keep helper-first design: no full workflow engine, no multi-stage orchestration framework.
- Prefer stdlib scripts and small docs/tests updates over new dependencies.
- Each prompt must land executable acceptance criteria and stop on failures.
- Defer frontend/site work entirely (explicit anti-scope for Stage-2).
- Avoid config-heavy lint/rubric refactors; prefer lightweight rule IDs/docs first.

## Stop Condition (Mandatory)

If any prompt fails its acceptance criteria:
1. Stop immediately.
2. Do not continue to later Stage-2 prompts.
3. Report:
   - which acceptance criterion failed,
   - exact command/output,
   - files touched,
   - recommended minimal follow-up prompt or patch.
