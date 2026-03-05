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
| 1 | `meta-runner-bootstrap` | Generate or refresh the orchestration contract. | `test -f .prompts/PROMPT_META_RUNNER.txt` |
| 2 | `meta-runner-preflight-inspector` | Run dependency and acceptance feasibility checks. | `./skills-foundry/bin/repo-helper-preflight --help` |
| 3 | `meta-runner-stage-runner` | Execute the next prompt with artifact/smoke gates. | `./skills-foundry/bin/repo-helper-stage1-plan --help` |
| 4 | `meta-runner-port-isolation` | Avoid runtime/test port collisions when stacks overlap. | `docker ps --format '{{.Ports}}' | head -n 20` |
| 5 | `meta-runner-test-stack-isolation` | Ensure integration tests do not mutate production-like local data. | `docker compose version` |
| 6 | `meta-runner-operators-guide-author` | Publish operator-grade runbook with root-level commands. | `test -f skills-foundry/docs/OPERATOR_MANUAL.md` |
| 7 | `meta-runner-ui-audit-playwright` | Run deterministic UI audit with trace/video evidence. | `.venv/bin/pytest -q skills-foundry/tests/test_meta_runner_skills.py` |
| 8 | `meta-runner-postflight-analyzer` | Close stage with evidence-backed scoring and DoD status. | `test -f POST_FLIGHT_REPORT_META_RUNNER.md` |
| 9 | `meta-runner-reference-example-curator` | Curate and verify high-signal reference examples in deterministic flow order. | `./skills-foundry/bin/skills-flow-render` |

### Alt Lane

| Step | Skill ID | Why | Verify Command |
|---|---|---|---|
| 1 | `meta-runner-bootstrap` | Generate or refresh the orchestration contract. | `test -f .prompts/PROMPT_META_RUNNER.txt` |
| 2 | `meta-runner-preflight-inspector-alt` | Apply strict/no-auto-fix preflight policy. | `./skills-foundry/bin/repo-helper-preflight --help` |
| 3 | `meta-runner-stage-runner-alt` | Use checkpointed execution with explicit pause gates. | `./skills-foundry/bin/repo-helper-stage1-plan --help` |
| 4 | `meta-runner-port-isolation` | Avoid runtime/test port collisions when stacks overlap. | `docker ps --format '{{.Ports}}' | head -n 20` |
| 5 | `meta-runner-test-stack-isolation` | Ensure integration tests do not mutate production-like local data. | `docker compose version` |
| 6 | `meta-runner-operators-guide-author` | Publish operator-grade runbook with root-level commands. | `test -f skills-foundry/docs/OPERATOR_MANUAL.md` |
| 7 | `meta-runner-ui-audit-playwright` | Run deterministic UI audit with trace/video evidence. | `.venv/bin/pytest -q skills-foundry/tests/test_meta_runner_skills.py` |
| 8 | `meta-runner-postflight-analyzer-alt` | Use score-delta and drift-emphasis closure profile. | `test -f POST_FLIGHT_REPORT_META_RUNNER.md` |
| 9 | `meta-runner-reference-example-curator` | Curate and verify high-signal reference examples in deterministic flow order. | `./skills-foundry/bin/skills-flow-render` |

## polyglot

Backend language and architecture prompt generation flow.

### Standard Lane

| Step | Skill ID | Why | Verify Command |
|---|---|---|---|
| 1 | `backend-language-shortlister` | Narrow backend language candidates based on repo constraints. | `test -f skills-foundry/docs/BACKEND_OPTIONS.md` |
| 2 | `backend-choice-to-prompts` | Generate prompt sequence tailored to selected backend stack. | `test -f skills-foundry/templates/packs/pack.md.tmpl` |

### Alt Lane

| Step | Skill ID | Why | Verify Command |
|---|---|---|---|
| 1 | `backend-language-shortlister-alt` | Use alternate weighting for language shortlist tradeoffs. | `test -f skills-foundry/docs/BACKEND_OPTIONS.md` |
| 2 | `backend-choice-to-prompts-alt` | Generate alternative prompt structure for backend implementation. | `test -f skills-foundry/templates/packs/pack.md.tmpl` |

## storage-labs

Storage planning and synthetic dataset design flow.

### Standard Lane

| Step | Skill ID | Why | Verify Command |
|---|---|---|---|
| 1 | `storage-zoo-planner` | Plan multi-store architecture and workload fit. | `test -f skills-foundry/docs/STORAGE_ZOO_PLAN.md` |
| 2 | `synthetic-data-spec-author` | Design deterministic synthetic datasets for storage experiments. | `test -f skills-foundry/docs/DATASETS_CATALOG.md` |

### Alt Lane

| Step | Skill ID | Why | Verify Command |
|---|---|---|---|
| 1 | `storage-zoo-planner-alt` | Use alternate storage scoring and risk emphasis. | `test -f skills-foundry/docs/STORAGE_ZOO_PLAN.md` |
| 2 | `synthetic-data-spec-author-alt` | Use alternate data profile strategy for experiments. | `test -f skills-foundry/docs/DATASETS_CATALOG.md` |

## workflow

Prompt-first workflow execution from preflight through Stage-2 postflight.

### Standard Lane

| Step | Skill ID | Why | Verify Command |
|---|---|---|---|
| 1 | `prompt-preflight-inspector` | Validate prompt ordering and dependency risks before execution. | `./skills-foundry/bin/repo-helper-preflight --help` |
| 2 | `prompt-stage1-runner` | Run Stage-1 prompt sequence with bounded commit discipline. | `./skills-foundry/bin/repo-helper-stage1-plan --help` |
| 3 | `prompt-postflight-analyzer` | Generate Stage-1 postflight score and risk summary. | `./skills-foundry/bin/repo-helper-postflight --help` |
| 4 | `stage2-plan-generator` | Generate focused Stage-2 prompt expansion from postflight output. | `./skills-foundry/bin/repo-helper-stage2-theme-plan --help` |
| 5 | `stage2-preflight-inspector` | Preflight-check new Stage-2 prompts before execution. | `./skills-foundry/bin/repo-helper-preflight --help` |
| 6 | `stage2-runner` | Run Stage-2 prompt sequence with acceptance gates. | `./skills-foundry/bin/repo-helper-stage2-run-plan --help` |
| 7 | `stage2-postflight-analyzer` | Close Stage-2 loop and identify only high-leverage follow-ups. | `./skills-foundry/bin/repo-helper-postflight --help` |
| 8 | `prompt-resume-reconciler` | Reconcile prompt completion evidence before continuing an interrupted run. | `./skills-foundry/bin/skills-flow-next --group workflow --lane standard` |
| 9 | `prompt-commit-batch-planner` | Plan prompt-scoped Tim Pope style commit batches with clear rationale. | `git log --oneline -n 5` |

### Alt Lane

| Step | Skill ID | Why | Verify Command |
|---|---|---|---|
| 1 | `prompt-preflight-inspector-alt` | Use stricter preflight scoring and fix gating. | `./skills-foundry/bin/repo-helper-preflight --help` |
| 2 | `prompt-stage1-runner-alt` | Use checkpointed Stage-1 execution approach. | `./skills-foundry/bin/repo-helper-stage1-plan --help` |
| 3 | `prompt-postflight-analyzer-alt` | Use alternate postflight emphasis profile. | `./skills-foundry/bin/repo-helper-postflight --help` |
| 4 | `stage2-plan-generator-alt` | Generate Stage-2 plans with alternate prioritization. | `./skills-foundry/bin/repo-helper-stage2-theme-plan --help` |
| 5 | `stage2-preflight-inspector-alt` | Apply stricter stage-specific preflight checks. | `./skills-foundry/bin/repo-helper-preflight --help` |
| 6 | `stage2-runner-alt` | Use alternate stage execution strategy. | `./skills-foundry/bin/repo-helper-stage2-run-plan --help` |
| 7 | `stage2-postflight-analyzer-alt` | Use alternate postflight scoring for Stage-2. | `./skills-foundry/bin/repo-helper-postflight --help` |
| 8 | `prompt-resume-reconciler` | Reconcile prompt completion evidence before continuing an interrupted run. | `./skills-foundry/bin/skills-flow-next --group workflow --lane standard` |
| 9 | `prompt-commit-batch-planner` | Plan prompt-scoped Tim Pope style commit batches with clear rationale. | `git log --oneline -n 5` |
