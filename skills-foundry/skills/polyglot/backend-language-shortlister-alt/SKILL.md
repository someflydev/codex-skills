---
id: backend-language-shortlister-alt
name: Backend Language Shortlister (ALT)
description: Hiring-first backend options advisor that favors boring, stable languages and frameworks with mature tooling and easy staffing.
version: 0.1.0
tags: [polyglot, backend, advisor, shortlisting, alt]
inputs:
  - name: problem_domain
    type: string
    required: true
    default: ""
    examples: ["CRUD-heavy internal platform with audit trails"]
  - name: constraints
    type: object
    required: true
    default: {}
    examples: [{perf: medium, hiring: very_high, portability: medium, simplicity: high}]
  - name: output_path
    type: path
    required: false
    default: docs/BACKEND_OPTIONS.md
    examples: ["docs/BACKEND_OPTIONS.md", "skills-foundry/reports/BACKEND_OPTIONS.md"]
  - name: stability_floor
    type: enum
    required: false
    default: proven-in-production
    examples: ["proven-in-production", "mainstream-only"]
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

Use when the primary goal is selecting a backend stack that is boring, stable, easy to hire for, and operationally predictable.

## Inputs

- `problem_domain`: plain-language description of the backend problem to solve.
- `constraints`: weighted constraints, with hiring velocity and operational stability expected to dominate.
- `output_path`: default `docs/BACKEND_OPTIONS.md`; foundry runs may target `skills-foundry/reports/BACKEND_OPTIONS.md`.
- `stability_floor`: how aggressively to filter out niche or immature stacks.

## Procedure

1. Normalize the constraints with an explicit hiring/stability bias and state that bias at the top of the report.
2. Propose exactly 15 language options, but rank mainstream production-proven ecosystems highest by default.
3. For each language, provide:
   - 2-3 mature frameworks (or stdlib option) with long-term support posture
   - strengths relevant to maintainability and onboarding
   - risks/costs with emphasis on hiring pool size, debugging ease, and ops complexity
   - fit for HTMX + Tailwind + Plotly-style rendering with server-template ergonomics called out
   - dev workflow notes (testing defaults, packaging, environment management, CI friction)
4. Penalize options that require rare expertise unless they offer a compelling business advantage.
5. End with a clear "choose one" interaction menu that asks the user to confirm the top candidate or override it with a reason.
6. Write the report and explicitly recommend one boring/default choice plus one conservative fallback.

## Success criteria

- The report compares 15 languages using a stability/hiring-first rubric.
- Ranking logic is explicit and consistent with the stated bias.
- The final menu makes it easy for the user to choose a conservative stack quickly.

## Failure modes + recovery

- If the user values learning or novelty more than stability, recover by switching to the non-ALT shortlister or re-running with different weights.
- If a niche option appears near the top, explain the exceptional reason clearly or lower it.
- If HTMX-first rendering is a poor fit for the domain, call that out before ranking frameworks.

## Examples

### Small Repo (10 prompts)

Generate a hiring-first shortlist for an internal CRUD/admin app, rank Python, TypeScript, and Go ecosystems highly, and end with a simple selection menu for a conservative team.

### Larger Repo (25 prompts)

Create a stability-biased backend options report for a multi-team platform and ask for final selection inputs needed to generate downstream implementation prompts.

