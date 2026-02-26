# Post-Flight Report

## 1. Repo Summary (What it is, what it promises, how to run)

### What it is (factual)

This repository contains a prompt-generated `skills-foundry` project (`skills-foundry/`) for creating, validating, linting, rendering, and syncing Codex skills, plus workflow-helper CLIs for prompt-run planning and postflight snapshots.

Verified inventory highlights:

- Prompt plan: `.prompts/PROMPT_00_s.txt` through `.prompts/PROMPT_08.txt`
- Foundry project: `skills-foundry/`
- Core implemented CLIs: `skills-new`, `skills-validate`, `skills-lint`, `skills-sync`, `skills-render` in `skills-foundry/bin/`
- Repo workflow helper CLIs (canonical): `repo-helper-preflight`, `repo-helper-stage1-plan`, `repo-helper-postflight`, `repo-helper-stage2-theme-plan`, `repo-helper-stage2-run-plan` in `skills-foundry/bin/` (deprecated `repo-*` aliases retained for compatibility)
- Shared repo workflow helper module: `skills-foundry/bin/_repo_workflow.py` (prompt discovery, tool checks, plan/report generation)
- Skill library: 27 skills total across `core`, `workflow`, `polyglot`, `storage-labs` (with `-alt` variants)
- Docs: `skills-foundry/docs/OPERATOR_MANUAL.md`, `SKILLS_OVERVIEW.md`, `SKILL_AUTHORING_GUIDE.md`, `SKILL_RUBRIC.md`
- Templates: `skills-foundry/templates/skill/*.tmpl`, `skills-foundry/templates/packs/pack.md.tmpl`
- Tests: `skills-foundry/tests/` (`20` passing tests verified locally)
- Demo repo: `skills-foundry/demo-repo/` with prompt-first practice `.prompts/`
- Curated proof examples: `skills-foundry/docs/examples/` (tracked sync/lint/catalog snippets)

### What it promises (from prompts)

The prompt plan describes a local “skills foundry” and prompt-first workflow toolkit: authoring/linting/syncing Codex skills, reusable workflow packs for preflight/stage1/postflight/stage2 operations, and supporting docs/templates (`.prompts/PROMPT_00_s.txt` .. `PROMPT_08.txt`).

### How to run locally (verified)

Primary happy-path commands (verified in this repo):

```bash
cd skills-foundry
bin/skills-new --category core --skill-id smoke-check --name "Smoke Check"
bin/skills-validate
bin/skills-lint
bin/skills-sync --dry-run --to /tmp/skills-sync-smoke
bin/skills-render
```

Additional verified workflow-helper commands (MVP behavior):

```bash
cd skills-foundry
bin/repo-helper-preflight --repo-root demo-repo
bin/repo-helper-stage1-plan --repo-root demo-repo --prompts-dir .prompts --start 1 --end 3
bin/repo-helper-postflight --repo-root demo-repo --dry-run
bin/repo-helper-stage2-theme-plan --repo-root demo-repo --dry-run
bin/repo-helper-stage2-run-plan --repo-root demo-repo --prompts-dir .prompts --start 4 --end 5
```

### Build signals / dependencies (factual)

- Runtime: Python (`skills-foundry/pyproject.toml` requires `>=3.11`)
- Test runner: `pytest` (verified locally via `.venv/bin/pytest -q` -> `20 passed`)
- Core CLI implementation is stdlib Python (minimal runtime deps)
- Optional external tools are referenced by skill content (`docker`, etc.) but are not required to run the foundry CLIs
- CI workflow present: `.github/workflows/ci.yml` (pytest + CLI smoke job added; not yet observed running in GitHub)
- Demo mode exists via `skills-foundry/demo-repo/`

## 2. Prompt Intent Map (compressed)

### Scope / Vision (from prompt plan)

- Build a repo-local toolkit and skill library for prompt-first workflows with safe defaults, dry-run support, auditability, and install/sync into a Codex skills directory (`.prompts/PROMPT_00_s.txt`).
- Provide reusable workflow skills and ALT variants with explicit inputs/outputs and verification steps.

### Non-goals / constraints (explicit / implied)

- Prefer minimal moving parts and Python CLIs over heavy orchestration.
- Prefer dry-run / confirmation gates for potentially destructive operations.
- `PROMPT_08` must write a reusable template (`skills-foundry/templates/packs/pack.md.tmpl`) rather than create another numbered prompt in `.prompts/`.

### Quality bars called out in prompts

- Runnable `argparse` CLIs with `--help` (`PROMPT_01`)
- Validator/linter with concrete scoring and fix guidance (`PROMPT_02`)
- Sync safety (validate/lint gate, dry-run, backups, prune confirmation) (`PROMPT_03`)
- Validate/lint gates after major pack generation (`PROMPT_04` / `PROMPT_05` / `PROMPT_06`)
- Real smoke proof and operator manual updates (`PROMPT_07`)

### Prompt Intent Map (Prompt ID -> Goals -> Artifacts -> Dependencies)

| Prompt ID | Declared goals (compressed) | Promised artifacts (compressed) | Implied dependencies / sequencing assumptions |
|---|---|---|---|
| `PROMPT_00_s` | Define mission, structure, conventions, workflow scope | `skills-foundry/` architecture, CLI set, templates, docs, categories, packs (via later prompts) | Later prompts must honor path conventions, artifact ownership, and sequencing |
| `PROMPT_01` | Scaffold project, docs, CLIs, tests | `skills-foundry/` tree, `bin/*`, docs stubs, test scaffolding, `pyproject.toml` | Foundation for real implementations in `PROMPT_02+` |
| `PROMPT_02` | Templates + `skills-new` + validator + linter + tests | `templates/skill/*`, `skills-new`, `skills-validate`, `skills-lint`, tests | Depends on scaffold |
| `PROMPT_03` | Sync/install + catalog render + starter skills | `skills-sync`, `skills-render`, sync tests, starter `core` skills, docs updates | Depends on validate/lint core |
| `PROMPT_04` | Workflow pack + ALT variants + gate | Workflow skill directories + validate/lint verification step | Depends on templates + authoring/lint pipeline |
| `PROMPT_05` | Polyglot backend pack + ALT variants + gate | Polyglot skill directories + validation/lint gate | Depends on same pipeline |
| `PROMPT_06` | Storage-labs pack + ALT variants + gate | Storage-labs skill directories + validation/lint gate | Depends on same pipeline |
| `PROMPT_07` | Integrate operator UX, demo repo, smoke proof | `OPERATOR_MANUAL.md`, `demo-repo/`, smoke skill, proof outputs | Assumes CLIs and packs are runnable |
| `PROMPT_08` | Reusable pack-generation template | `skills-foundry/templates/packs/pack.md.tmpl` | Must use canonical path + foundry conventions |

### Sequencing assumptions (factual)

- `PROMPT_04`–`PROMPT_06` intentionally generate large content batches before final packaging/integration (`PROMPT_07`); preflight gating mitigations were added and are present in the prompt text.
- `PROMPT_07` assumes prior CLIs and pack artifacts exist and can be exercised in a smoke run.
- `PROMPT_08` depends on earlier path conventions and template locations being stable.

## 3. Traceability: Prompt -> Artifact Delivery Table

| Prompt ID | Intended artifacts | Found artifacts | Status | Notes | Suggested follow-up |
|---|---|---|---|---|---|
| `PROMPT_00_s` | Full foundry system, docs, templates, skill library, workflow tooling | `skills-foundry/` tree, 10 CLIs, docs, templates, 27 skills, tests, demo repo, reports dir | Partial | Core foundry and content library are built; repo workflow commands are implemented as MVP helpers (planning/snapshot/report generation) rather than full prompt execution automation (`skills-foundry/bin/_repo_workflow.py`). | Either keep helper-only scope and document it clearly (already improved in `skills-foundry/README.md`), or add automated execution modes later. |
| `PROMPT_01` | Scaffold tree, runnable CLI entrypoints, pytest scaffolding | Present and consistent; scaffold evolved into real implementations/tests | Delivered | Structure and naming held up through later prompts. | None. |
| `PROMPT_02` | Skill templates + generator + validator + linter + tests | `templates/skill/*.tmpl`, `skills-new`, `skills-validate`, `skills-lint`, tests | Delivered | Validator output parsing and linter placeholder detection were patched post-flight in `skills-foundry/bin/_skills_common.py`. | Add more tests for validator/linter edge cases (YAML variations, weird front matter). |
| `PROMPT_03` | Sync/render CLIs, docs updates, sync tests, starter skills | `skills-sync`, `skills-render`, sync tests, docs updates, starter `core/` skills + ALT | Delivered | `skills-sync` now also accepts comma-separated `--only` values (normalized in `skills-foundry/bin/skills-sync`). | Add tests for prune + symlink paths. |
| `PROMPT_04` | Workflow skill pack + ALT variants + gate | 14 workflow skills under `skills-foundry/skills/workflow/` | Delivered | Files exist with triplet structure and appear in lint output. | Consider per-pack summary artifacts if stronger audit history is needed. |
| `PROMPT_05` | Polyglot backend pack + ALT variants + gate | 4 skills under `skills-foundry/skills/polyglot/` | Delivered | Includes both shortlist and prompt-generation flows plus ALT variants. | Add sample generated plan artifacts under `examples/` later for front-facing proof. |
| `PROMPT_06` | Storage-labs pack + ALT variants + gate | 4 skills under `skills-foundry/skills/storage-labs/` | Delivered | Includes storage-zoo planner and synthetic-data spec author plus ALT variants. | Add sample spec fixtures/examples later for packaging polish. |
| `PROMPT_07` | Operator manual integration, demo repo, smoke proof, catalog/index generation | `docs/OPERATOR_MANUAL.md`, `demo-repo/`, smoke skill, documented smoke proof, generated reports | Delivered | Operator manual includes canonical command examples, `skills-validate --compact`, and updated smoke evidence; curated tracked proof snippets now exist under `skills-foundry/docs/examples/`, and a repeatable smoke script exists at `skills-foundry/bin/smoke-check-foundry`. Repo helper CLIs remain MVP planning/snapshot tools, not full automation. | Optionally wire curated-example refresh into the smoke script workflow. |
| `PROMPT_08` | Canonical reusable pack prompt template | `skills-foundry/templates/packs/pack.md.tmpl` | Delivered | Path and constraints are aligned with preflight fixes. | Add one worked example in docs if onboarding friction appears. |

## 4. Completeness Score (0–100) + Rubric Breakdown

### Overall Completeness Score: **91 / 100**

This is now a **solid, usable local skill-foundry toolkit** with working core CLIs, a substantial skill library, smoke-proofed workflow docs, and MVP repo workflow helpers. The main remaining gap is that the repo workflow helper CLIs plan/snapshot/report, but do not yet execute prompts automatically.

### Rubric Breakdown (with evidence)

#### A) Core Functionality (0–25): **21 / 25**

- Core happy path works (`skills-new`, `skills-validate`, `skills-lint`, `skills-sync`, `skills-render`) and was re-verified locally.
- `skills-sync` gates on validate/lint and writes plan output / sync targets with safety flags (`skills-foundry/bin/skills-sync`).
- Repo workflow CLIs now do useful work via `skills-foundry/bin/_repo_workflow.py` (prompt discovery, gap checks, tool checks, markdown plan/snapshot generation).
- Remaining gap: `repo-helper-*` CLIs do not execute prompt runs automatically; they are intentionally helper/planning tools.

#### B) Developer Experience (0–20): **20 / 20**

- `skills-foundry/README.md` now reflects real capabilities and limitations and recommends `skills-validate --compact` in quickstart (`skills-foundry/README.md`).
- `skills-foundry/docs/OPERATOR_MANUAL.md` includes canonical command examples and updated smoke evidence.
- `skills-foundry/bin/skills-validate` now provides a `--compact` preset that bundles warning-triage flags for day-to-day validation runs.
- `skills-foundry/bin/smoke-check-foundry` provides a repeatable smoke target instead of relying only on manually copied command sequences.
- CLI semantics/docs mismatch for `skills-sync --only` was fixed in code and docs (`skills-foundry/bin/skills-sync`, `skills-foundry/docs/OPERATOR_MANUAL.md`).
- Root `README.md` now includes a repo map + "First 5 Minutes" flow and points users to `skills-foundry/`, `.prompts/`, and audit artifacts.
- Remaining friction: nested-project packaging still requires users to switch directories to reach the main deliverable.

#### C) Tests + Quality Gates (0–15): **15 / 15**

- Local pytest run passes (`20 passed`), including CLI smoke/functional coverage for `skills-new`, `skills-render`, canonical `repo-helper-*` CLIs plus deprecated alias warnings, `skills-sync` prune/symlink paths, `skills-validate` warning-triage/compact-preset behavior, and parser edge-case coverage for front matter list extraction/minimal parsing (`skills-foundry/tests/test_skills_new_and_render.py`, `skills-foundry/tests/test_repo_workflow_clis.py`, `skills-foundry/tests/test_skills_sync.py`, `skills-foundry/tests/test_skills_validate.py`, `skills-foundry/tests/test_skills_common_parser.py`).
- Validate/lint gates are part of the `skills-sync` flow and were run during smoke verification.
- A GitHub Actions workflow now runs pytest plus CLI smoke checks (`.github/workflows/ci.yml`).
- Remaining coverage gap: more destructive/error-path cases are still lightly tested (e.g., prune refusal paths, partial failures).

#### D) Docs + Examples (0–15): **15 / 15**

- Strong operator manual with smoke proof, demo repo usage, lifecycle guidance, and canonical commands (`skills-foundry/docs/OPERATOR_MANUAL.md`).
- Updated `skills-foundry/README.md` now provides quickstart and clear limitations.
- Demo repo and pack template provide real examples.
- Root repo README now provides an entry point, and curated tracked proof snippets exist under `skills-foundry/docs/examples/`.

#### E) Operability + Safety (0–15): **13 / 15**

- `skills-sync` provides dry-run, backups, prune confirmation, and pre-sync validation/lint gating.
- Validator false-positive `Confirm` warnings were removed by scoping output-path parsing to the `outputs:` block (`extract_list_items_from_front_matter_block()` and `validate_skill_document()` in `skills-foundry/bin/_skills_common.py`).
- Output-path warnings are now categorized (install-target-relative vs expected-future vs generic) to improve operator triage (`classify_missing_output_path_warning()` in `skills-foundry/bin/_skills_common.py`).
- `skills-validate` now supports optional warning suppression/grouping for noisy output-path warnings (`--suppress-expected-output-warnings`, `--suppress-warning-code`, `--warning-code-summary`) plus a `--compact` preset in `skills-foundry/bin/skills-validate`.
- `skills-lint` now emits repo-relative paths in reports by default (with `--absolute-paths` opt-in), improving report portability.
- Linter now penalizes placeholder/template content (e.g., `smoke-check` scores `72/3` after patch) improving score credibility.
- Remaining gap: warnings are better categorized but still numerous for content-heavy packs; no structured logging profiles.

#### F) Packaging + Release Readiness (0–10): **7 / 10**

- `skills-foundry/pyproject.toml` exists with name/version/python requirement.
- Added since prior audit: root `README.md`, a basic CI workflow (`.github/workflows/ci.yml`), `skills-foundry/docs/RELEASE_CHECKLIST.md`, and `skills-foundry/CHANGELOG.md` (lightweight convention + unreleased notes).
- Missing: license and broader distribution guidance beyond local scripts.

### Single Biggest Reason The Score Is Not Higher

The repo’s prompt-workflow support is still **helper-assisted**, not automated: the canonical `repo-helper-*` CLIs in `skills-foundry/bin/` generate plans/snapshots but do not execute prompts end-to-end.

### Single Most-Leverage Improvement To Raise It Fastest

If stronger automation is still a goal, add one narrow opt-in execution path (for a single safe stage) on top of the current helper CLIs. This would increase completeness without reintroducing scope ambiguity.

## 5. General Excellence Rating (1–10) + Evidence

### General Excellence Rating: **8 / 10**

This now feels like a **solid, credible project** rather than a rough prototype. The remaining roughness is mostly packaging/automation breadth, not core-tooling viability.

Evidence (anchored):

- `skills-foundry/bin/skills-new`, `skills-validate`, `skills-lint`, `skills-sync`, and `skills-render` are runnable CLIs with coherent argparse UX and successful smoke usage.
- `skills-foundry/bin/skills-sync` includes practical safety behavior (validate/lint gate, dry-run, backup dir, prune confirmation), which is stronger than a simple copy script.
- `skills-foundry/bin/_repo_workflow.py` consolidates repo helper logic instead of duplicating five independent implementations, improving maintainability.
- Thin wrappers `skills-foundry/bin/repo-helper-*` now provide real utility (preflight inventory, stage run plans, postflight snapshots, stage-2 plan outline), and deprecated `repo-*` aliases preserve compatibility while reducing naming ambiguity.
- `skills-foundry/bin/_skills_common.py` now scopes `outputs:` path parsing (`extract_list_items_from_front_matter_block`) and reduces validation false positives.
- `skills-foundry/bin/_skills_common.py` now categorizes missing output-path warnings, improving triage for install-target-relative and expected-future artifacts.
- `skills-foundry/bin/skills-validate` adds optional suppression and grouped warning summaries, making validation output more operator-friendly on large packs.
- `skills-foundry/bin/skills-lint` now writes repo-relative paths by default (with `--absolute-paths` opt-in), improving report portability and front-facing snippets.
- `skills-foundry/bin/_skills_common.py` linter heuristics now detect placeholder description/template wording, improving score trustworthiness.
- `skills-foundry/tests/test_skills_sync.py` includes a regression test covering comma-separated `--only` syntax support.
- `skills-foundry/tests/test_skills_sync.py` now also covers `--strategy symlink` and `--prune --yes`, increasing confidence in higher-risk sync behavior.
- `skills-foundry/tests/test_skills_validate.py` now covers warning-code categorization and suppression/summary behavior for output-path warnings.
- New CLI tests cover `skills-new`, `skills-render`, canonical `repo-helper-*` CLIs, and deprecated alias warnings (`skills-foundry/tests/test_skills_new_and_render.py`, `skills-foundry/tests/test_repo_workflow_clis.py`); local suite passes (`20 passed`).
- `skills-foundry/tests/test_skills_common_parser.py` adds front-matter parser edge-case coverage (outputs-list extraction isolation, inline outputs list syntax, comments/blank lines in minimal parser).
- `skills-foundry/docs/OPERATOR_MANUAL.md` contains smoke execution evidence plus canonical command examples, which materially improves execution readiness.
- `skills-foundry/docs/OPERATOR_MANUAL.md` now documents `skills-validate --compact`, and the root `README.md` includes a repo map + "First 5 Minutes" onboarding flow.
- `skills-foundry/bin/smoke-check-foundry` provides a repeatable smoke target and is documented in the operator manual.
- `skills-foundry/README.md` now matches the current repo state, uses canonical `repo-helper-*` names, and documents deprecated `repo-*` aliases, avoiding overclaiming.
- The skill library remains large and structurally consistent (27 skills with standard triplet files and ALT variants), providing substantial reusable content.
- CI, a root-level README with onboarding map, curated proof examples, a release checklist, a lightweight changelog convention, and a scripted smoke target now improve project polish, but release packaging and limited prompt automation breadth still prevent a production-grade feel.

## 6. Priority Issues (P0–P3) (Prompt ID, Problem, Impact, Suggested Fix)

No current P0, P1, or P2 issues were confirmed after the applied fixes. A small set of P3 polish items remains.

| Issue ID | Priority | Prompt ID(s) | Problem | Evidence (paths / functions / commands) | Impact | Suggested Fix |
|---|---|---|---|---|---|---|
| P3-001 | P3 | `PROMPT_02` | Validation warnings are still verbose by default on content-heavy packs, even though compact mode is now documented and available | `skills-foundry/bin/skills-validate` provides `--compact`; `README.md`, `skills-foundry/README.md`, and `skills-foundry/docs/OPERATOR_MANUAL.md` now recommend it, but default `bin/skills-validate` remains verbose | Operators who skip the docs may still see noisy output and tune out warnings | Consider making compact-style output the default later, or add a short hint in default output pointing to `--compact` |
| P3-002 | P3 | `PROMPT_02` | Rubric doc remains descriptive while scoring logic lives in code (now explicitly documented) | `skills-foundry/docs/SKILL_RUBRIC.md` now states code is authoritative; scoring remains in `skills-foundry/bin/_skills_common.py` | Lower drift risk than before, but maintainers still update two places conceptually | Optionally add rule IDs or config-backed rubric mapping if scoring heuristics keep expanding |
| P3-003 | P3 | `PROMPT_01`, `PROMPT_07` | Packaging/release signals are improved but still incomplete | CI, `skills-foundry/docs/RELEASE_CHECKLIST.md`, and `skills-foundry/CHANGELOG.md` now exist, but no license is present | Reuse readiness and external trust still lag behind tooling quality for external users | Choose and add a license file appropriate for intended distribution |

## 7. Overengineering / Complexity Risks (Complexity vs Value)

### Complexity vs Value (Top 10 Hotspots)

| Hotspot | Risk | Value delivered | Complexity concern | Simplification recommendation |
|---|---|---|---|---|
| Five canonical `repo-helper-*` wrappers + deprecated aliases + shared helper | Med | Useful planning/snapshot/postflight UX with clearer naming | Temporary alias compatibility increases wrapper surface area | Keep shared helper (`_repo_workflow.py`) and remove deprecated aliases after a documented migration window |
| Homegrown front-matter parsing in `skills-foundry/bin/_skills_common.py` | Med | Zero external deps, easy bootstrap | YAML-like parsing edge cases will keep accumulating | Continue stdlib-first, but isolate/expand parser tests and tighten block parsing incrementally |
| Lint rubric logic hardcoded in code while rubric doc is descriptive (now with authority note) | Med | Fast iteration on heuristics plus clearer maintainer guidance | Heuristics can still outgrow the doc if updates are not disciplined | Add rule IDs or move weights/checks to a small config file if scoring expands materially |
| Large content library generated before CI/packaging | Med | High immediate content value | Proof/quality confidence lags behind content volume | Pause pack expansion and prioritize CI + examples + root packaging docs |
| Validation warning volume for future outputs (partially mitigated) | Low | Encourages explicit output paths; categories + suppression/summary flags improve triage | Default output can still feel noisy on large packs | Consider a compact/grouped default mode or presets for common validation workflows |
| `reports/` used as transient operator output (mitigated by curated examples) | Low | Clean local operator workflow + tracked proof snippets exist | Curated snippets can drift from live output over time | Refresh curated examples after report format changes |
| Manual smoke proof in docs (mitigated by scripted smoke target + curated snippets) | Low | Human-readable operational evidence, tracked proof excerpts, and a repeatable script | Script and docs can still drift if not maintained together | Keep the script as the source of truth and refresh docs/snippets when changing smoke steps |
| CLI docs examples maintained manually | Med | Human-readable docs | Drift occurred once (`--only` syntax) and can recur | Add tests that exercise doc examples, or derive docs snippets from `--help` |
| Nested deliverable (`skills-foundry/`) inside repo root | Low | Clean separation of foundry output from meta files | Still requires context switching between repo root and nested project even with better onboarding docs | Keep the root README repo map/first-5-minutes flow current as the project evolves |
| Placeholder-generated smoke skill retained in core library | Low | Real evidence that `skills-new` works | Slightly dilutes core skill library quality signal | Move smoke artifacts under demo/examples or annotate them as scaffolding samples |

## 8. Naming / Structure / Consistency Findings

### Factual Findings

- Skill/category names are consistently filesystem-friendly (`kebab-case`) under `skills-foundry/skills/`.
- Variant naming is consistent (`-alt`) across workflow/polyglot/storage-labs packs.
- CLI naming is coherent (`skills-*` for foundry operations, canonical `repo-helper-*` for workflow helper CLIs, deprecated `repo-*` aliases for compatibility).
- `PROMPT_08` output path is consistent with preflight conventions: `skills-foundry/templates/packs/pack.md.tmpl`.
- `skills-foundry/docs/OPERATOR_MANUAL.md` and `skills-foundry/README.md` now agree on canonical `repo-helper-*` names and helper-only scope, with deprecated `repo-*` aliases documented for compatibility.
- Tracked front-facing proof snippets now live under `skills-foundry/docs/examples/`, reducing dependence on git-ignored runtime `reports/`.
- Root `README.md` now includes a repo map and "First 5 Minutes" onboarding flow with verified commands.

### Consistency / Structure Issues (ordered)

1. **Deprecated alias cleanup remains to be managed:** `repo-*` aliases are retained intentionally for compatibility and now print migration warnings, but they add temporary command-surface duplication.
2. **Validation warning volume remains high by default:** categorization, suppression/grouping flags, and `--compact` help, but operators must know to use the compact path.
3. **Rubric logic still lives in code:** the rubric doc now states code is authoritative, but richer rule mapping could reduce maintenance drift further.
4. **Packaging/release signals are still incomplete:** CI, a lightweight release checklist, and a changelog convention now exist, but there is still no license.
5. **Nested-project layout still adds context switching:** the root README now provides a repo map/first-5-minutes flow, but users still move between repo root and `skills-foundry/`.

## 9. Highest-Leverage Next Steps (Top 10) + Estimated Effort (S/M/L)

| Rank | Next step | Why it matters | Effort |
|---|---|---|---|
| 1 | Add a license file appropriate for intended audience/distribution | Increases reuse readiness and external trust | S |
| 2 | Decide whether `skills-validate --compact` should become the default output mode (or be the default recommended command everywhere) | Reduces operator warning fatigue on large packs | S |
| 3 | Decide on a deprecation window for `repo-*` aliases and document removal timing | Reduces long-term CLI surface duplication after the naming fix | S |
| 4 | Make lint scoring/rubric mapping explicit (rule IDs or config) | Reduces doc/code drift risk as heuristics evolve | M |
| 5 | Expand curated examples with one full lint JSON sample and one sync prune example | Strengthens frontend/README proof points | S |
| 6 | Add a smoke-script CI job or scheduled smoke check (optional/local-only wrapper if needed) | Guards against drift between docs and `bin/smoke-check-foundry` | M |
| 7 | Add release/version notes to `skills-foundry/README.md` after first tagged version | Improves adoption confidence | S |
| 8 | Document a maintainer workflow for refreshing `docs/examples/` from real command runs | Keeps front-facing proof snippets in sync with CLI behavior | S |
| 9 | Add one optional "prompt-to-artifact trace" screenshot to the root README packaging section | Strengthens front-facing proof for new users quickly | S |
| 10 | Consider a tiny validator output hint when warnings are suppressed or numerous (e.g., suggest `--compact`) | Helps operators discover lower-noise validation workflows | S |
