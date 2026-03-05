# Meta Runner Prompt Mapping

## Prompt-Step To Skill ID Mapping

| Workflow Step | Prompt Pattern | Skill ID |
|---|---|---|
| Create/refresh orchestration contract | `prompt00--CREATE-PROMPT-META-RUNNER` | `meta-runner-bootstrap` |
| Prompt set preflight | `prompt01--PRE-FLIGHT-INSPECTOR` | `meta-runner-preflight-inspector` |
| Stage run execution loop | `prompt01.1--start-build-run-with-prompt-set` | `meta-runner-stage-runner` |
| Port conflict remediation | `prompt01.7--FIX-PORTS-DURING-META-RUNNER` | `meta-runner-port-isolation` |
| Separate integration docker stack | `prompt06.5--DESIGN-NEW-PROMPT-TO-MAKE-INTEGRATION-TESTS-ON-SEPARATE-DOCKER-STACK` | `meta-runner-test-stack-isolation` |
| Operators guide generation | `prompt06.4--DESIGN-NEW-PROMPT-TO-CREATE-OPERATORS-GUIDE` | `meta-runner-operators-guide-author` |
| UI audit via Playwright | `prompt07--THOROUGH-PLAYWRIGHT-UI-TESTING` | `meta-runner-ui-audit-playwright` |
| Postflight score + follow-ups | `prompt02--POST-FLIGHT-REPO-AUDIT` | `meta-runner-postflight-analyzer` |

## ALT Skill Mapping

| Situation | Recommended ALT Skill |
|---|---|
| Need strict no-auto-fix preflight controls | `meta-runner-preflight-inspector-alt` |
| Need checkpoint-by-checkpoint execution | `meta-runner-stage-runner-alt` |
| Need score-delta drift analysis | `meta-runner-postflight-analyzer-alt` |

## Prompt Execution Example

1. Active prompt: `PROMPT_17.txt`
2. Skill: `meta-runner-stage-runner`
3. Commit prefix: `[PROMPT_17, AGENT_AUDITOR]`
4. Verification:
   - `.venv/bin/pytest -q skills-foundry/tests/test_meta_runner_skills.py`
   - `./skills-foundry/bin/smoke-check-meta-runner --check-only`

## Adoption Checklist

- [ ] `human-notes.md` created for the run
- [ ] Prompt-step to `meta-runner-` skill selected before execution
- [ ] Verification commands recorded
- [ ] Commit prefix uses `PROMPT_XX` and `AGENT_` role
