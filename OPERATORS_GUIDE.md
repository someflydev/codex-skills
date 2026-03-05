# OPERATORS_GUIDE

This guide is for the current `codex-skills` repository and its primary deliverable, `skills-foundry/`.
It is evidence-driven and intentionally avoids inventing services, datastores, APIs, or Make targets that are not present in this repo.

## 1. Installation & System Requirements

### Required tools

- `git`
- `python3` (3.10+; 3.11 used in CI)
- `uv`
- `pytest`
- `ripgrep` (`rg`) for operator discovery workflows

### Optional tools

- `docker` and `docker compose` (used by some workflow/meta-runner checks and external project targeting)

### Install commands

macOS (Homebrew):

```bash
brew install git python@3.11 uv ripgrep
```

Ubuntu/Debian:

```bash
sudo apt-get update
sudo apt-get install -y git python3 python3-venv python3-pip ripgrep
python3 -m pip install --user uv
```

Fedora:

```bash
sudo dnf install -y git python3 python3-pip ripgrep
python3 -m pip install --user uv
```

Arch Linux:

```bash
sudo pacman -S --needed git python python-pip ripgrep
python -m pip install --user uv
```

### Project bootstrap

```bash
uv venv .venv
uv pip install --python .venv/bin/python pytest
.venv/bin/pytest -q skills-foundry
```

## 2. Service Catalog & Internal Locations

This repository is primarily a CLI/tooling project (not a long-running service app).

| Component | Type | Language/Runtime | Path | Responsibility |
|---|---|---|---|---|
| `skills-foundry/bin/*` | Local CLI toolchain | Python + Bash | `skills-foundry/bin` | Skill creation, validation, linting, sync, rendering, workflow helpers |
| `skills-foundry/tests/*` | Test suite | Python/pytest | `skills-foundry/tests` | Functional and contract coverage for CLIs and workflow logic |
| GitHub Actions CI | CI job | Ubuntu + Python 3.11 | `.github/workflows/ci.yml` | Runs tests + smoke checks |
| Prompt plan inventory | Prompt orchestration inputs | Markdown/text | `.prompts/` | Prompt sequence and stage manifests |

## 3. Log Locations & Tailing

### Primary runtime logs for this repo

- Most operational output is CLI stdout/stderr (interactive shell or CI logs).
- Git history/ref logs:
  - `.git/logs/HEAD`
  - `.git/logs/refs/heads/main`

### Local tailing patterns

```bash
tail -f .git/logs/HEAD
tail -f .git/logs/refs/heads/main
```

### CI log access patterns

- GitHub UI: Actions tab -> run -> step logs.
- If `gh` CLI is available:

```bash
gh run list
gh run view --log
```

## 4. Storage Backends

For this repository itself, no application database backend is implemented in-repo.

Storage model in practice:

- Filesystem-backed artifacts:
  - docs, prompts, reports, flow manifests, generated markdown
- Git object database/history:
  - commit evidence, branch/ref logs

Notes:

- Some skill content references external stacks (Postgres/Redis/Mongo/Elasticsearch) as target-project guidance.
- Those are not first-class runtime backends for this repository codebase.

## 5. Raw Data Exploration

This repo's "raw operational data" is generated artifacts and reports:

- Lint JSON: `skills-foundry/reports/skills-lint.json`
- Catalog markdown: `skills-foundry/reports/SKILLS_CATALOG.md`
- Curated examples: `skills-foundry/docs/examples/*`
- Prompt/finalization logs: `.prompts/improvements-before-*.txt`

Useful commands:

```bash
ls -la skills-foundry/reports
head -n 80 skills-foundry/reports/skills-lint.json
ls -la skills-foundry/docs/examples
rg -n "Round:|Stage-3|meta-runner" .prompts/improvements-before-finalization.txt
```

## 6. AI/Brain Operations (if applicable)

No in-repo AI "brain" runtime service was discovered in this repository.

- There is no local model-serving service, queue consumer, or inference engine implemented under `codex-skills`.
- AI-related content in this repo is procedural/prompt guidance and operational workflows, not a running inference stack.

## 7. Exhaustive Database Query Catalog

Datastore discovery result for this repository: **none** (no in-repo Postgres/Redis/Mongo/Elasticsearch runtime service definitions).

Evidence commands:

```bash
rg --files | rg '(^|/)Makefile$|docker-compose|compose\.ya?ml' || true
rg -n "postgres|redis|mongo|elasticsearch|opensearch|neo4j" -S skills-foundry .prompts README.md || true
```

Because zero datastores were discovered in this repo, there is no applicable 15-queries-per-datastore catalog to execute here.

## 8. Makefile Command Reference

Makefile discovery result: **no Makefile present** in this repository.

Evidence command:

```bash
rg --files | rg '(^|/)Makefile$' || true
```

Operational command surface (equivalent entrypoints) is `skills-foundry/bin/*`.

High-signal operator commands:

| Command | Purpose |
|---|---|
| `./skills-foundry/bin/skills-new` | Create a skill skeleton |
| `./skills-foundry/bin/skills-validate --compact` | Validate skills with low-noise warnings |
| `./skills-foundry/bin/skills-lint` | Generate lint reports |
| `./skills-foundry/bin/skills-sync --dry-run` | Preview skill install/sync changes |
| `./skills-foundry/bin/skills-render` | Render skills catalog |
| `./skills-foundry/bin/smoke-check-foundry --dry-run-only` | Repeatable core smoke run |
| `./skills-foundry/bin/smoke-check-meta-runner --check-only` | Meta-runner verification smoke |
| `./skills-foundry/bin/skills-flow-next --list-groups` | List ordered skill-flow groups |
| `./skills-foundry/bin/skills-flow-render` | Generate `docs/SKILL_FLOWS.md` |

## 9. Testing Strategy

### Unit/contract checks

```bash
.venv/bin/pytest -q skills-foundry/tests
```

### Full foundry regression

```bash
.venv/bin/pytest -q skills-foundry
```

### Smoke checks

```bash
./skills-foundry/bin/smoke-check-foundry --dry-run-only
./skills-foundry/bin/smoke-check-meta-runner --check-only
```

### CI parity check

- CI file: `.github/workflows/ci.yml`
- CI currently runs pytest, help smoke, validate/lint smoke, scripted smoke, and meta-runner check-only smoke.

## 10. CLI Debugger Quickstarts

### Python (primary)

Built-in `pdb` quickstart:

```bash
python3 -m pdb skills-foundry/bin/skills-validate --help
```

Drop-in breakpoint pattern for scripts/tests:

```python
import pdb; pdb.set_trace()
```

Optional richer debugger (if installed): `pudb`

```bash
pudb3 skills-foundry/bin/skills-lint
```

### Bash scripts

Trace execution:

```bash
bash -x skills-foundry/bin/smoke-check-foundry --dry-run-only
```

Strict mode baseline used in scripts:

```bash
set -euo pipefail
```

### Git troubleshooting

```bash
git status --short
git log --oneline -n 20
```

## 11. Interesting API/Curl Requests

No in-repo HTTP API service endpoints were discovered for this repository's runtime.

Evidence command:

```bash
rg -n "localhost|/api|/health|http://|https://" -S skills-foundry/bin skills-foundry/tests README.md skills-foundry/docs || true
```

Operational interactions are CLI-based, not HTTP-based, for this repo.

## 12. Troubleshooting Scenarios

### 1) `LC_ALL` warning noise in shell output

Symptom:
- repeated `setlocale: LC_ALL: cannot change locale (C.UTF-8)`

Resolution:
- inspect shell init files (`.zshrc`, `.bashrc`, sourced scripts) and align locale settings with available locales on host.

### 2) `skills-validate` reports missing output-path warnings

Symptom:
- warning volume too high during normal workflow

Resolution:

```bash
./skills-foundry/bin/skills-validate --compact
./skills-foundry/bin/skills-validate --warning-code-summary
```

### 3) Flow sequencing confusion across skill groups

Symptom:
- operator unsure which skill to run next

Resolution:

```bash
./skills-foundry/bin/skills-flow-next --list-groups
./skills-foundry/bin/skills-flow-next --group meta-runner --lane standard
```

### 4) Meta-runner contract drift after edits

Symptom:
- CI or local checks fail around meta-runner docs/contracts

Resolution:

```bash
.venv/bin/pytest -q skills-foundry/tests/test_meta_runner_skills.py
./skills-foundry/bin/smoke-check-meta-runner --check-only
```

### 5) Curated docs examples go stale

Symptom:
- `refresh-doc-examples --check` fails

Resolution:

```bash
./skills-foundry/bin/refresh-doc-examples --check
./skills-foundry/bin/refresh-doc-examples
```

### 6) Unexpected dirty worktree from generated artifacts

Symptom:
- report/docs files changed after smoke/tests

Resolution:

```bash
git status --short
./skills-foundry/bin/skills-flow-render
```

Then review and commit prompt-scoped changes with `git add -p`.
