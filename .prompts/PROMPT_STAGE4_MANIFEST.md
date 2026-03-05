# Prompt Stage-4 Manifest

## Stage-4 Theme

Reference-examples expansion: improve completeness and operator value by closing partial coverage gaps, adding high-signal net-new examples, and wiring strong verification/docs evidence.

## Stage-4 Prompt Sequence

1. `PROMPT_22.txt` - planning + batch prompt generation + manifest wiring
2. `PROMPT_23.txt` - Batch A: close partial coverage gaps
3. `PROMPT_24.txt` - Batch B: add new high-signal reference examples
4. `PROMPT_25.txt` - Batch C: verification/docs integration + readiness

## Definition of Done (Stage-4)

- [ ] Baseline reference-example inventory and status table exists and is evidence-backed.
- [ ] Partial coverage gaps are reduced with deterministic, repo-context path handling.
- [ ] Net-new high-signal reference examples are fully implemented (contract + checklist + examples).
- [ ] Flow/docs integration includes new examples with root-level invocation guidance.
- [ ] Validation/tests/smoke checks pass after each batch.
- [ ] Expansion plan is updated with Stage-4 completion status and next-wave recommendation.

## Stop Condition

If any Stage-4 prompt fails acceptance criteria:
1) stop immediately,
2) report exact failing command/output,
3) do not continue to later Stage-4 prompts until failure is resolved.
