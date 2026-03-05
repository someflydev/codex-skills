# Prompt Stage-3 Manifest

## Stage-3 Theme

Meta-runner skills expansion: convert the operator's evolved real-world prompt orchestration flow into reusable, rigor-tested `skills-foundry` assets under a new `meta-runner` category.

## Stage-3 Prompt Sequence

1. `PROMPT_14_s.txt` — Stage-3 system constraints for meta-runner expansion
2. `PROMPT_15.txt` — discovery + architecture plan
3. `PROMPT_16.txt` — implement `skills/meta-runner/*` (base + ALT)
4. `PROMPT_17.txt` — tests/smoke/safety verification harness
5. `PROMPT_18.txt` — operators guide + prompt-to-skill mapping for adoption
6. `PROMPT_19.txt` — postflight audit + conditional next-prompt generation

## Definition of Done (Stage-3)

- [ ] `skills-foundry/skills/meta-runner/` exists with required baseline skills:
  - bootstrap
  - preflight-inspector
  - stage-runner
  - port-isolation
  - test-stack-isolation
  - operators-guide-author
  - ui-audit-playwright
  - postflight-analyzer
- [ ] At least 3 meaningful `_alt` variants exist in `meta-runner/`.
- [ ] Structural contract tests exist and pass (`test_meta_runner_skills.py`).
- [ ] A non-destructive meta-runner smoke command exists and passes.
- [ ] CI includes a lightweight meta-runner smoke check step (`smoke-check-meta-runner --check-only`).
- [ ] Operator docs include:
  - prompt-step -> skill mapping
  - human-notes run-tracking template
  - root-level command examples
- [ ] Discovery/plan artifacts explicitly map relevant operator corpus prompts into meta-runner skill capabilities.
- [ ] `POST_FLIGHT_REPORT_META_RUNNER.md` exists with evidence-backed scorecard.
- [ ] `.prompts/improvements-before-finalization.txt` includes a Stage-3 log entry.

## Stop Condition

If any prompt fails acceptance criteria:
1) stop immediately,
2) report exact failing command/output,
3) do not continue to later Stage-3 prompts until failure is resolved.
