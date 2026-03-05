# Meta Runner Skills Plan

## Goal

Implement a new `meta-runner` skill category that encodes the operator's evolved workflow as reusable, testable, and safety-bounded skills.

## Planned Skill Inventory

Required baseline skills:

1. `meta-runner-bootstrap`
2. `meta-runner-preflight-inspector`
3. `meta-runner-stage-runner`
4. `meta-runner-port-isolation`
5. `meta-runner-test-stack-isolation`
6. `meta-runner-operators-guide-author`
7. `meta-runner-ui-audit-playwright`
8. `meta-runner-postflight-analyzer`

Planned ALT variants (meaningful policy divergence):

- `meta-runner-stage-runner-alt` (checkpointed and stricter gating)
- `meta-runner-preflight-inspector-alt` (strict/no-auto-fix-first policy)
- `meta-runner-postflight-analyzer-alt` (score-delta and drift-emphasis profile)

## Skill Contracts

| Skill ID | Trigger Intent | Expected Tools | Expected Outputs | Safety Model |
|---|---|---|---|---|
| `meta-runner-bootstrap` | Create/update `.prompts/PROMPT_META_RUNNER.txt` from live prompt corpus | `git`, `rg`, `python3`, `uv` | `.prompts/PROMPT_META_RUNNER.txt` | Dry-run supported; no destructive actions |
| `meta-runner-preflight-inspector` | Run preflight checks against target prompt batch | `git`, `rg`, `python3` | `.prompts/improvements-before-*.txt`, preflight report | Confirm before applying fixes |
| `meta-runner-stage-runner` | Execute the next prompt sequence with gates and commit discipline | `git`, `rg`, `python3`, `pytest` | run logs, prompt completion summaries | Stop on failing checks; no hidden background processes |
| `meta-runner-port-isolation` | Detect and assign safe non-default ports across runtime/test stacks | `docker`, `rg`, `python3` | updated compose/config docs and checks | Confirm before changing active runtime mappings |
| `meta-runner-test-stack-isolation` | Keep test stack isolated from development/prod-like state | `docker`, `docker compose`, `make` | isolated compose/runtime wiring + verification evidence | Non-destructive by default; explicit teardown confirmations |
| `meta-runner-operators-guide-author` | Produce/update operations guide with real commands | `rg`, `python3` | `OPERATORS_GUIDE.md` (or repo-specific equivalent) | Docs-only unless user approves execution checks |
| `meta-runner-ui-audit-playwright` | Plan and run deterministic Playwright audits for high-signal flows | `uv`, `python3`, `pytest`, `playwright` | audit plan, coverage matrix, e2e reports | Deterministic waits; no unsafe environment assumptions |
| `meta-runner-postflight-analyzer` | Score completeness/excellence and propose next prompt batch | `git`, `rg`, `python3`, `pytest` | postflight report + improvements log updates | Evidence-first scoring; no fabricated verification |

## Operator Corpus Preservation Mapping

| Operator Corpus Prompt | Preserved In Skill | Notes |
|---|---|---|
| `CREATE-PROMPT-META-RUNNER` | `meta-runner-bootstrap` | Adds resume-aware start logic and tool verification policy |
| `PRE-FLIGHT-INSPECTOR` | `meta-runner-preflight-inspector` | Prioritized issue table + safe-auto fix discipline |
| `start-build-run-with-prompt-set` | `meta-runner-stage-runner` | Prompt-scoped execution loop + commit boundaries |
| `FIX-PORTS-DURING-META-RUNNER` | `meta-runner-port-isolation` | Non-conflicting, near-default port allocation strategy |
| `SEPARATE-DOCKER-STACK` | `meta-runner-test-stack-isolation` | Isolated test stack and non-destructive safety boundaries |
| `OPERATORS-GUIDE` | `meta-runner-operators-guide-author` | Verified command catalog + troubleshooting sections |
| `PLAYWRIGHT-UI-TESTING` | `meta-runner-ui-audit-playwright` | CUJ-based audit with trace/video evidence |
| `POST-FLIGHT-REPO-AUDIT` | `meta-runner-postflight-analyzer` | rubric scoring, closure table, and next-step generation |

## Integration Targets

- `skills-foundry/skills/meta-runner/*/SKILL.md`
- `skills-foundry/docs/SKILLS_OVERVIEW.md` (category index update)
- `skills-foundry/README.md` (category mention and quickstart references)
- Stage-3 verification:
  - `skills-foundry/tests/test_meta_runner_skills.py`
  - `skills-foundry/bin/smoke-check-meta-runner`
  - `.github/workflows/ci.yml` check-only smoke step

## Acceptance Strategy (Stage-3)

1. Implement inventory and run `skills-validate`, `skills-lint`, and `skills-render`.
2. Add structural tests for required meta-runner contracts.
3. Add deterministic smoke-check command for meta-runner group.
4. Add CI check-only smoke step.
5. Publish operator mapping and adoption guide.
6. Run postflight with evidence-backed scoring and update Stage-3 DoD.

## Risks and Mitigations

- Risk: overbuilding a generic orchestration engine.
  - Mitigation: keep skills narrowly scoped and composable.
- Risk: flaky runtime checks.
  - Mitigation: default check-only/dry-run modes and explicit failure exits.
- Risk: prompt completion ambiguity in long-lived repos.
  - Mitigation: resume logic based on prompt files + commit prefixes + artifact evidence.

