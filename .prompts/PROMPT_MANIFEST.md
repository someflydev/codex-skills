# Prompt Manifest

This manifest lists the prompt sequence present in `.prompts/`, including the Stage-2 plan prompts added after post-flight auditing.

## Stage 1 (Executed / existing)

| Prompt ID | Role | Summary | Depends On |
|---|---|---|---|
| `PROMPT_00_s.txt` | system | Mission, structure, conventions, path rules | — |
| `PROMPT_01.txt` | task | Scaffold foundry project, docs, CLIs, tests | `PROMPT_00_s.txt` |
| `PROMPT_02.txt` | task | Skill templates + `skills-new` + validate/lint | `PROMPT_01.txt` |
| `PROMPT_03.txt` | task | Sync/render CLIs + starter skills | `PROMPT_02.txt` |
| `PROMPT_04.txt` | task | Workflow skill pack + ALT variants + verification gate | `PROMPT_02.txt`, `PROMPT_03.txt` |
| `PROMPT_05.txt` | task | Polyglot backend pack + ALT variants + verification gate | `PROMPT_02.txt`, `PROMPT_03.txt` |
| `PROMPT_06.txt` | task | Storage-labs pack + ALT variants + verification gate | `PROMPT_02.txt`, `PROMPT_03.txt` |
| `PROMPT_07.txt` | task | Operator integration + demo repo + smoke proof | `PROMPT_01.txt`..`PROMPT_06.txt` |
| `PROMPT_08.txt` | task | Reusable pack-generation prompt template | `PROMPT_00_s.txt` conventions |

## Stage 2 (Planned)

See `.prompts/PROMPT_STAGE2_MANIFEST.md` for goals, DoD-S2, and stop conditions.

| Prompt ID | Role | Summary | Intended Order | Primary Dependencies |
|---|---|---|---|---|
| `PROMPT_09.txt` | task | Narrow opt-in Stage-1 execution mode + deterministic run logs | 1 | `skills-foundry/bin/_repo_workflow.py`, canonical `repo-helper-*` CLIs |
| `PROMPT_10.txt` | task | Behavior tests + CI gates for helper execution and smoke path | 2 | `PROMPT_09.txt` (preferred), `.github/workflows/ci.yml`, tests |
| `PROMPT_11.txt` | task | Safety/idempotency guardrails + validator compact hint | 3 | `PROMPT_09.txt`, `PROMPT_10.txt` (preferred) |
| `PROMPT_12.txt` | task | Packaging/release hygiene baseline (license + deprecation policy) | 4 | Prior docs/changelog/release checklist; human license choice required |
| `PROMPT_13.txt` | task | Light specs + drift-control hooks for examples/rubric maintenance | 5 | Prior docs/tests stable; final Stage-2 polish |

## Execution Notes

- Stage-2 prompts are intentionally narrow and acceptance-driven.
- If any Stage-2 prompt fails its acceptance criteria, stop and report before continuing.
- Continue prompt-scoped commit discipline (`[PROMPT_XX] ...`) with `git add -p`.

