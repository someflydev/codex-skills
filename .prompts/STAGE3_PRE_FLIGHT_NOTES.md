# Stage-3 Pre-Flight Notes

Scope checked:
- `.prompts/PROMPT_14_s.txt`
- `.prompts/PROMPT_15.txt` .. `.prompts/PROMPT_19.txt`
- `.prompts/PROMPT_STAGE3_MANIFEST.md`
- `.prompts/PROMPT_MANIFEST.md`

## Summary

- Prompt numbering/order: PASS (`14_s`, then `15..19`, no gaps).
- Cross-prompt dependency references: PASS (all references align to current numbering).
- Structural completeness of Stage-3 task prompts: PASS.
  - Each includes Objective, Dependencies, Artifacts, Required Scope, Acceptance Criteria, Anti-Scope, Overengineering Guardrails, and Evidence section.
- Tool preflight snapshot (`repo-helper-preflight`): PASS with required tools `git python3 rg uv docker`.

## Requested Updates Applied

1. Operator corpus baked into Stage-3 planning requirements
- `PROMPT_15` now explicitly requires integrating relevant operator corpus prompts from the provided excerpt.
- Acceptance criteria now checks those corpus prompt identifiers are reflected in discovery/plan outputs.

2. CI meta-runner smoke step made required
- `PROMPT_17` now requires `.github/workflows/ci.yml` update with `smoke-check-meta-runner --check-only`.
- Acceptance criteria includes explicit CI grep validation.

3. Stage-3 DoD tightened
- `PROMPT_STAGE3_MANIFEST.md` now includes required CI smoke step and explicit operator-corpus mapping checkbox.

## Residual Risks (non-blocking)

1. External prompt corpus path variability
- `PROMPT_15` still supports explicit path override when `../prompts/` is absent.

2. Follow-up prompt generation cap discipline in `PROMPT_19`
- Optional `PROMPT_20..22` generation remains capped and evidence-gated.

## Go/No-Go

- GO for Stage-3 execution.
- Suggested run order:
  1. `PROMPT_15.txt`
  2. `PROMPT_16.txt`
  3. `PROMPT_17.txt`
  4. `PROMPT_18.txt`
  5. `PROMPT_19.txt`

## Generated Artifacts

- `.prompts/STAGE3_PRE_FLIGHT_SNAPSHOT.md`
- `.prompts/STAGE3_PRE_FLIGHT_NOTES.md`
