# Meta Runner Discovery

## Scope

This discovery captures the current repository reality before Stage-3 implementation:

- Existing prompt lineage in `.prompts/`
- Existing workflow skills in `skills-foundry/skills/workflow/`
- Full git history context (including multi-line commits)
- Operator-supplied external prompt corpus patterns

The objective is to identify what is missing for day-to-day meta-runner adoption and define a concrete implementation target.

## Evidence

### Commit History

Observed sequence from `git log --reverse --pretty=fuller`:

- `Initial .prompts` followed by `[PRE-FLIGHT]` hardening commits.
- `[PROMPT_01]`..`[PROMPT_08]`: foundational foundry scaffolding and workflow skill packs.
- Stage-2 execution commits (`[PROMPT_09]`..`[PROMPT_13]`) hardening helper CLIs, CI smoke, safety, and docs example drift checks.
- Stage-3 prompt-set bootstrap commits:
  - `[NEW PROMPT_14-19] Add Stage-3 meta-runner prompt sequence`
  - `[STAGE-3 PRE-FLIGHT] Bake operator corpus and tighten Stage-3 prompt gates`

### Prompt Lineage

- Stage-1/Stage-2/Stage-3 prompts are present in `.prompts/PROMPT_00_s.txt` through `.prompts/PROMPT_19.txt`.
- Stage-3 scope is explicitly defined in:
  - `.prompts/PROMPT_14_s.txt`
  - `.prompts/PROMPT_15.txt`..`.prompts/PROMPT_19.txt`
  - `.prompts/PROMPT_STAGE3_MANIFEST.md`

### Current Workflow Skill Coverage

Existing workflow category includes:

- `prompt-preflight-inspector` (+ alt)
- `prompt-stage1-runner` (+ alt)
- `prompt-postflight-analyzer` (+ alt)
- `stage2-plan-generator` (+ alt)
- `stage2-preflight-inspector` (+ alt)
- `stage2-runner` (+ alt)
- `stage2-postflight-analyzer` (+ alt)

These cover stage-based prompt workflows, but not the evolved meta-runner execution pattern from the operator corpus.

## Gap Analysis

### Gap 1: No dedicated meta-runner skill category

Current skills are stage-oriented and generic. They do not provide a cohesive "meta-runner track" with explicit bootstrap/preflight/stage-run/postflight decomposition tied to modern operator usage.

### Gap 2: No direct mapping from external operator corpus to reusable skills

The repository has no explicit artifact mapping the operator's prompt corpus steps to specific skill IDs, inputs, and outputs.

### Gap 3: Missing structural verification harness for meta-runner contracts

There is no focused test module that enforces required section/safety conventions across a meta-runner skill family, and no dedicated `smoke-check-meta-runner` command.

### Gap 4: No operator adoption runbook for meta-runner flow

`OPERATOR_MANUAL.md` documents stage workflows but not a targeted meta-runner adoption path, human-notes tracking template, and prompt-to-skill mapping.

## Operator Corpus Mapping Inputs

The following operator corpus prompts are first-class requirements for Stage-3 design:

- `prompt00--CREATE-PROMPT-META-RUNNER.txt`
- `prompt01--PRE-FLIGHT-INSPECTOR.txt`
- `prompt01.1--start-build-run-with-prompt-set.txt`
- `prompt01.7--FIX-PORTS-DURING-META-RUNNER.txt`
- `prompt06.5--DESIGN-NEW-PROMPT-TO-MAKE-INTEGRATION-TESTS-ON-SEPARATE-DOCKER-STACK.txt`
- `prompt06.4--DESIGN-NEW-PROMPT-TO-CREATE-OPERATORS-GUIDE.txt`
- `prompt07--THOROUGH-PLAYWRIGHT-UI-TESTING.txt`
- `prompt02--POST-FLIGHT-REPO-AUDIT.txt`

## External Workflow Step -> Planned Capability

| External Step | Corpus Evidence | Planned Capability |
|---|---|---|
| Generate repo-specific meta runner | CREATE-PROMPT-META-RUNNER | `meta-runner-bootstrap` |
| Prompt-set preflight | PRE-FLIGHT-INSPECTOR | `meta-runner-preflight-inspector` |
| Controlled stage execution + commit discipline | start-build-run-with-prompt-set | `meta-runner-stage-runner` |
| Resolve non-conflicting service ports | FIX-PORTS-DURING-META-RUNNER | `meta-runner-port-isolation` |
| Isolated docker integration stack | SEPARATE-DOCKER-STACK | `meta-runner-test-stack-isolation` |
| Generate operator documentation | OPERATORS-GUIDE | `meta-runner-operators-guide-author` |
| Playwright-based UI audit flow | PLAYWRIGHT-UI-TESTING | `meta-runner-ui-audit-playwright` |
| Evidence-backed postflight scoring | POST-FLIGHT-REPO-AUDIT | `meta-runner-postflight-analyzer` |

## Stage-3 Design Constraints (Derived)

- Keep helper-first architecture; do not introduce a daemonized runtime orchestrator.
- Keep smoke checks deterministic and non-destructive by default.
- Enforce commit discipline with prompt-scoped prefixes and `git add -p`.
- Use root-level command examples in docs and operator guidance.
- Require evidence-backed verification before declaring prompt completion.

## Recommended Stage-3 Implementation Order

1. Plan and inventory (`PROMPT_15`)
2. Implement `skills/meta-runner/*` baseline + meaningful alt variants (`PROMPT_16`)
3. Add structural tests, smoke command, and CI check-only step (`PROMPT_17`)
4. Ship operator mapping + runbook docs (`PROMPT_18`)
5. Run postflight scoring + conditional next-prompt generation (`PROMPT_19`)

