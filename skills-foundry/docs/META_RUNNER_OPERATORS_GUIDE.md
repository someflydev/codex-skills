# Meta Runner Operators Guide

## Purpose

Convert day-to-day prompt execution into a repeatable skill-driven workflow without losing commit discipline, verification rigor, or operator control.

## When To Use Meta-Runner Skills vs Manual Prompt Copy/Paste

- Use `meta-runner-*` skills when:
  - `.prompts/` already has a structured stage and acceptance criteria.
  - You need resume-aware execution from in-progress state.
  - You want consistent `git add -p` commit boundaries and smoke/verification gates.
- Use manual prompt copy/paste when:
  - You are prototyping a single one-off prompt.
  - Prompt text is intentionally ephemeral and not meant for reuse.

## Prompt Commit Prefix Discipline

Every execution commit should use:

- `[PROMPT_XX, AGENT_ARCHITECT] ...`
- `[PROMPT_XX, AGENT_BUILDER] ...`
- `[PROMPT_XX, AGENT_AUDITOR] ...`

Where `PROMPT_XX` matches the active `.prompts/PROMPT_XX*.txt` file.

## Human Notes Template

Create `human-notes.md` in the target repo and log each run step:

```markdown
# human-notes

## Run: <date-time>

- Prompt: PROMPT_15.txt
- Skill: meta-runner-preflight-inspector
- Agent Role: AGENT_ARCHITECT
- Commands:
  - .venv/bin/pytest -q skills-foundry/tests/test_meta_runner_skills.py
- Outcome: PASS
- Commit(s):
  - [PROMPT_15, AGENT_ARCHITECT] ...
- Follow-ups:
  - <none or list>
```

## Minimal Adoption Path (First 60 Minutes)

1. Bootstrap or refresh runner:
   - `meta-runner-bootstrap`
2. Preflight current stage:
   - `meta-runner-preflight-inspector`
3. Execute next dependency-ready prompt:
   - `meta-runner-stage-runner`
4. Verify contracts/smoke:
   - `./skills-foundry/bin/smoke-check-meta-runner --check-only`
5. Record run and commit with prompt-scoped prefix.

## Full-Run Path

1. `meta-runner-bootstrap`
2. `meta-runner-preflight-inspector` (or strict `meta-runner-preflight-inspector-alt`)
3. `meta-runner-stage-runner` (or checkpointed `meta-runner-stage-runner-alt`)
4. Optional branches as needed:
   - `meta-runner-port-isolation`
   - `meta-runner-test-stack-isolation`
   - `meta-runner-operators-guide-author`
   - `meta-runner-ui-audit-playwright`
5. `meta-runner-postflight-analyzer` (or delta-focused alt)

## Root-Level Verification Commands

```bash
.venv/bin/pytest -q skills-foundry/tests/test_meta_runner_skills.py
./skills-foundry/bin/smoke-check-meta-runner --check-only
```
