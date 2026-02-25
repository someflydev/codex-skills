---
id: backend-language-shortlister
name: Backend Language Shortlister
description: Propose and compare 15 backend language options with framework choices, tradeoffs, and an explicit final selection menu.
version: 0.1.0
tags: [polyglot, backend, advisor, shortlisting]
inputs:
  - name: problem_domain
    type: string
    required: true
    default: ""
    examples: ["Internal analytics dashboard with admin workflows"]
  - name: constraints
    type: object
    required: true
    default: {}
    examples: [{perf: medium, hiring: high, portability: medium, simplicity: high}]
  - name: output_path
    type: path
    required: false
    default: docs/BACKEND_OPTIONS.md
    examples: ["docs/BACKEND_OPTIONS.md", "skills-foundry/reports/BACKEND_OPTIONS.md"]
  - name: bias_mode
    type: enum
    required: false
    default: balanced
    examples: ["balanced", "performance-first", "simplicity-first"]
expected_tools: [git, rg, python3]
safety:
  dry_run_supported: true
  destructive_actions: []
  confirmation_points:
    - "Confirm before overwriting an existing BACKEND_OPTIONS.md report"
outputs:
  - docs/BACKEND_OPTIONS.md
  - skills-foundry/reports/BACKEND_OPTIONS.md
---

## When to use

Use when a project needs a structured backend stack shortlist before committing to a single language/framework combination.

## Inputs

- `problem_domain`: plain-language description of the product and workloads.
- `constraints`: weighted constraints such as performance, hiring, portability, simplicity, ops burden, and team familiarity.
- `output_path`: default report path is `docs/BACKEND_OPTIONS.md`; use `skills-foundry/reports/BACKEND_OPTIONS.md` when running from foundry tooling.
- `bias_mode`: optional tie-breaker preference when tradeoffs are close.

## Procedure

1. Restate the domain and normalize constraints into explicit weights so tradeoffs are comparable.
2. Propose exactly 15 backend languages (mix mainstream and situational options) that plausibly fit the domain.
3. For each language, document:
   - 2-3 common web frameworks (or a stdlib/server-only option)
   - core strengths (constructs, paradigms, runtime characteristics)
   - risks and costs (hiring, maturity, tooling, runtime ops, lock-in)
   - fit for HTMX + Tailwind + Plotly-style rendering (server templates, HTML generation, asset handling)
   - developer workflow notes (testing, packaging, env management, dependency tooling)
4. Rank the options using the stated constraints and explain why the top 3 rise above the rest.
5. End with a clear "choose one" interaction that presents a selection menu and asks the user for the exact answers needed to proceed (language, framework, deployment target, DB preference, auth needs, and non-functional constraints).
6. Write the report to `output_path` and summarize the top recommendation plus the next decision required from the user.

## Success criteria

- The report contains exactly 15 language options with comparable sections.
- HTMX/Tailwind/Plotly-style server-rendering fit is evaluated for every option.
- The final section includes an actionable selection menu and explicit questions.

## Failure modes + recovery

- If constraints are vague or conflicting, recover by proposing default weights and asking the user to confirm the ranking criteria before finalizing the top 3.
- If a language lacks credible framework options for the domain, keep it in the list only with a clearly marked low-fit score and rationale.
- If the report path is outside the repo layout, stop and ask for a repo-relative destination.

## Examples

### Small Repo (10 prompts)

Shortlist 15 backend options for an internal dashboard and rank them with simplicity + hiring weighted highest, then ask the operator to choose one framework for a minimal HTMX-first stack.

### Larger Repo (25 prompts)

Compare 15 languages for a multi-tenant analytics app, include deployment and portability tradeoffs, and end with a menu that captures architecture decisions needed for downstream prompt generation.

