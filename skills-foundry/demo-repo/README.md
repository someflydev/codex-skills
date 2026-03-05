# Demo Repo (Tiny Prompt Set)

This is a tiny practice repository for the `skills-foundry` prompt-first workflow.

## What is here

- `.prompts/` with a small 6-file sequence (`PROMPT_00_s.txt` through `PROMPT_05.txt`)
- The prompts describe a minimal CLI toy project so you can test the workflow mechanics without a large build

## Suggested practice run

1. From the real repo root, inspect the prompt files:
   ```bash
   rg --files skills-foundry/demo-repo/.prompts | sort
   ```
2. Run a prompt preflight on this demo repo (using your workflow skill/process).
3. Execute prompts in order and create `[PROMPT_XX]` commits with `git add -p`.
4. Run postflight and generate a stage-2 plan only if you intentionally introduce issues.

## Meta-Runner Practice Path

When practicing the Stage-3 flow, map prompt steps to `meta-runner-*` skills:

1. Bootstrap/refresh runner contract: `meta-runner-bootstrap`
2. Preflight prompt batch: `meta-runner-preflight-inspector`
3. Execute next prompt safely: `meta-runner-stage-runner`
4. Verify contracts/smoke: `./skills-foundry/bin/smoke-check-meta-runner --check-only`
5. Postflight score + next-step decision: `meta-runner-postflight-analyzer`

## Notes

- Keep the demo small; the goal is to practice sequencing, verification, and commit hygiene.
- You can copy this folder and mutate the prompt set to test preflight edge cases.
