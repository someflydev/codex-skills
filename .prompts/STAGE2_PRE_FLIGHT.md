# Stage-2 Pre-Flight

## 1. Stage-2 Goal Alignment (mapped to report P0/P1)

### Baseline (from `POST_FLIGHT_REPORT.md`)
- Completeness: `91 / 100`
- Excellence: `8 / 10`
- Open issues: no `P0/P1/P2`; remaining `P3` polish only
- Highest-leverage improvement: narrow opt-in execution path on top of `repo-helper-*`

### Alignment Summary
- `PROMPT_09` directly targets the report's highest-leverage improvement (narrow helper execution MVP).
- `PROMPT_10` converts the new behavior into regression protection (tests + CI).
- `PROMPT_11` adds safety/idempotency guardrails and validator UX nudge (`--compact` discoverability).
- `PROMPT_12` addresses remaining packaging trust gap (`LICENSE`) and alias deprecation policy (human-gated where required).
- `PROMPT_13` addresses drift-control and rubric/lint maintenance clarity without frontend scope.

### P0/P1 handling
- No P0/P1 issues exist in the report; Stage-2 correctly focuses on the report's highest-leverage improvement plus remaining P3 items.

## 2. Prompt Dependency Graph

### Stage-2 prompts in order
1. `PROMPT_09.txt` — Narrow Stage-1 Execution Mode (Opt-In) + Deterministic Run Artifacts
2. `PROMPT_10.txt` — Behavior-Level Tests + CI Gates for Helper Execution and Smoke Path
3. `PROMPT_11.txt` — Safety Guardrails + Idempotent Cleanup for Helper Execution and Validator UX
4. `PROMPT_12.txt` — Packaging + Release Hygiene Baseline (License Decision + Deprecation Policy)
5. `PROMPT_13.txt` — Light Specs + Drift-Control Hooks (Examples Refresh + Lint Rule Mapping)

### Dependency graph (artifact-level)
- `PROMPT_09` -> `PROMPT_10`
  - execution-mode behavior in `skills-foundry/bin/_repo_workflow.py` / `repo-helper-stage1-plan`
  - `PROMPT_10` adds tests + CI gates for that behavior
- `PROMPT_09` -> `PROMPT_11`
  - execution-mode guardrails build on the Stage-1 execution MVP
- `PROMPT_10` -> `PROMPT_12` (soft)
  - canonical helper naming and CI/docs stability help package/release docs stay coherent
- `PROMPT_12` -> `PROMPT_13` (soft)
  - packaging/docs stabilization helps final drift-control prompt land cleanly

### Independence check (hard-rule compliance)
- All prompts are runnable independently.
- `PROMPT_10` and `PROMPT_11` now explicitly define conditional acceptance branches when `PROMPT_09` has not been executed.
- `PROMPT_12` now explicitly defines an independent blocker path when no license choice is provided.

## 3. Prompt-by-Prompt QA (issues + fixes)

### `PROMPT_09.txt`
Status: `Pass (after edits)`

Verified improvements
- Fixed repo-root-relative path examples for `--write-plan` / `--run-log` when `--repo-root demo-repo` is used.
- Clarified runner template semantics to avoid implicit shell behavior.
- Acceptance examples now use explicit shell-mode naming (`--runner-shell-template`) and remain deterministic.

Residual notes (non-blocking)
- The prompt intentionally allows exact flag names to differ if semantics are equivalent; acceptable.

### `PROMPT_10.txt`
Status: `Pass (after edits)`

Verified improvements
- Added explicit conditional acceptance branch for cases where `PROMPT_09` execution mode is absent.
- CI checks remain realistic and scoped.
- Added acceptable `grep -E` fallback note for environments without `rg`.

### `PROMPT_11.txt`
Status: `Pass (after edits)`

Verified improvements
- Added explicit conditional acceptance branch for execution-guardrail work if `PROMPT_09` is absent.
- Clarified smoke-script reset criterion by requiring explicit verification only if a reset-related flag is introduced.

Residual notes (non-blocking)
- The prompt still leaves flexibility on whether smoke-script reset support is added; this is acceptable because `demo-repo-reset` remains the mandatory path.

### `PROMPT_12.txt`
Status: `Pass (after edits)`

Verified improvements
- Reworded independence to satisfy the hard rule (independent with explicit blocker path).
- Acceptance checks are less brittle (`repo-helper-` + `DEPRECATIONS.md` references, case-insensitive `license` check).

Residual notes (non-blocking)
- License text remains intentionally human-gated; this is correct and desirable.

### `PROMPT_13.txt`
Status: `Pass`

Verified
- Scope remains narrow, local, and frontend-free.
- Artifact plan and acceptance criteria are executable and consistent with repo conventions.

### `PROMPT_STAGE2_MANIFEST.md`
Status: `Pass (after edits)`

Verified improvements
- Minimal deterministic value slice now uses repo-root-relative run-log path semantics.
- DoD-S2 license checkbox now explicitly notes the human-gated blocker condition for `PROMPT_12`.

## 4. Acceptance Criteria Feasibility (CI-safe?)

| Prompt | Feasibility | CI-safe? | Notes |
|---|---|---|---|
| `PROMPT_09` | Feasible | Yes (deterministic local mode) | Explicit shell-template mode removes hidden execution ambiguity. |
| `PROMPT_10` | Feasible | Yes | CI updates are local/stdlib; conditional branch covers pre-`PROMPT_09` runs. |
| `PROMPT_11` | Feasible | Mostly | POSIX `/tmp` usage is compatible with current CI target (`ubuntu-latest`) and local macOS/Linux. |
| `PROMPT_12` | Feasible | Human-gated | Correctly blocks legal-text changes until explicit license choice is provided. |
| `PROMPT_13` | Feasible | Mostly | Local refresh hooks and dry-run checks are CI-safe in principle; no external services required. |

### Environment assumptions validated
- `skills-foundry/pyproject.toml` requires Python 3.11+ (matches current CI setup).
- `.github/workflows/ci.yml` exists and is small enough to extend.
- Existing helper CLI/test/doc paths referenced in the prompts are present.

## 5. Naming / Path / Convention Alignment

### Alignment checks passed
- Prompt numbering/order is sequential (`PROMPT_09`..`PROMPT_13`).
- Artifact paths follow repo conventions (`skills-foundry/bin`, `docs`, `tests`, `docs/examples`).
- Canonical helper command names (`repo-helper-*`) are consistently used.
- Stage-2 manifest and prompt manifest both reference the same prompt order and intent.
- No frontend/web scope artifacts are introduced.

### Remaining naming/path risks (non-blocking)
- `PROMPT_12` introduces `skills-foundry/docs/DEPRECATIONS.md` (new doc) and a root `LICENSE`; this is consistent and non-conflicting.
- `PROMPT_13` introduces a `docs/examples/manifest.json`; no naming conflicts detected.

## 6. Overengineering Risks + Guardrails Verification

### Guardrail verification (pass)
- Every Stage-2 prompt includes:
  - explicit artifact list
  - executable acceptance criteria
  - anti-scope section
  - overengineering guardrails section
- All Stage-2 prompts explicitly avoid frontend/site work.
- No prompt introduces heavy dependencies or services by default.

### Residual complexity risks (acceptable)
- `PROMPT_09` execution mode could grow into a framework if the implementation ignores prompt guardrails.
  - Guardrails are explicit and sufficient for a helper-first MVP.
- `PROMPT_13` lint/rubric rule mapping could drift toward config refactors.
  - Prompt explicitly constrains this to lightweight docs/IDs and local hooks.

## 7. Recommended Edits (patch list) + Priority

### Applied in this pre-flight refinement round
1. Fixed repo-root-relative path examples in `PROMPT_09.txt` (`STAGE1-PLAN.md`, `STAGE1-RUN-LOG.md`).
2. Clarified explicit shell vs non-shell runner template semantics in `PROMPT_09.txt`.
3. Added conditional acceptance branch language to `PROMPT_10.txt`.
4. Added conditional acceptance branch + reset-option clarification to `PROMPT_11.txt`.
5. Reworded `PROMPT_12.txt` independence line to explicit blocker-path semantics.
6. Tightened `PROMPT_12.txt` success-path acceptance checks.
7. Fixed matching run-log path example and license blocker note in `.prompts/PROMPT_STAGE2_MANIFEST.md`.

### Remaining recommended edits (optional / low priority)
- None required before execution.
- Optional future polish: add `grep -E` fallback notes to `PROMPT_STAGE2_MANIFEST.md` DoD checks if execution environments without `rg` are expected.

## 8. Go/No-Go Decision

### Decision: **GO**

The Stage-2 prompt set is now safe to execute in order.

Why GO
- Sequencing is coherent and minimal.
- Acceptance criteria are executable and realistic for this repo/CI context.
- Artifact naming/paths are consistent with repo conventions.
- No hidden frontend scope or heavy dependency creep is present.
- Overengineering guardrails are explicit in every prompt.

Execution note
- `PROMPT_12.txt` remains intentionally human-gated for the license decision. This is a planned blocker path, not a pre-flight failure.
