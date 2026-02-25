---
id: backend-choice-to-prompts
name: Backend Choice To Prompts
description: Convert a selected backend language/framework stack into ordered PROMPT_XX files that implement an HTMX-first backend with clear boundaries.
version: 0.1.0
tags: [polyglot, backend, prompts, generator]
inputs:
  - name: repo_root
    type: path
    required: true
    default: .
    examples: ["."]
  - name: selected_stack
    type: object
    required: true
    default: {}
    examples: [{language: "Python", framework: "FastAPI", templates: "Jinja2"}]
  - name: project_constraints
    type: object
    required: true
    default: {}
    examples: [{frontend_js: minimal, htmx_first: true, db: "sqlite"}]
  - name: prompt_start_number
    type: int
    required: false
    default: 9
    examples: [9, 10, 20]
expected_tools: [git, rg, python3]
safety:
  dry_run_supported: true
  destructive_actions: []
  confirmation_points:
    - "Confirm before writing or overwriting PROMPT_XX files in .prompts/"
outputs:
  - .prompts/PROMPT_<NN>.txt
  - skills-foundry/reports/backend-choice-to-prompts-plan.md
---

## When to use

Use after a backend stack has been chosen and you need an ordered prompt sequence that implements the backend while preserving project constraints.

## Inputs

- `repo_root`: target repo containing `.prompts/`.
- `selected_stack`: chosen language/framework combo plus templating, package manager, and deployment assumptions.
- `project_constraints`: non-negotiables such as minimal frontend JS, HTMX-first interactions, sensible templates, and clean data layer boundaries.
- `prompt_start_number`: first prompt number to write so new prompts fit the existing sequence.

## Procedure

1. Inspect existing `.prompts/` files to avoid collisions, preserve numbering continuity, and reuse naming conventions.
2. Translate the selected stack into a minimal implementation plan before writing prompts (project bootstrap, data layer, templates/views, HTMX interactions, testing, deployment).
3. Generate ordered `PROMPT_XX.txt` files in `.prompts/` that explicitly enforce:
   - minimal frontend JavaScript
   - HTMX-first request/response flows
   - sensible template structure and server-rendered HTML defaults
   - clear data layer boundaries (repositories/services/models) with low coupling
4. Add verification gates throughout the generated prompt sequence (tests, smoke checks, schema checks, linting) so stack-specific failures surface early.
5. End the generated sequence with a prompt that proves the backend works end-to-end and documents follow-up options.
6. Write a short planning report summarizing the generated prompts, assumptions, and unresolved decisions.

## Success criteria

- New prompts are ordered, non-colliding, and repo-convention friendly.
- The generated prompt set keeps HTMX-first/minimal-JS constraints explicit.
- Data layer boundaries are specified early enough to prevent architectural drift.

## Failure modes + recovery

- If the selected stack is underspecified, stop and request missing choices (templating engine, package manager, database, deployment target) before writing prompts.
- If `.prompts/` numbering would collide, recover by proposing a renumbered range and asking for confirmation.
- If the stack conflicts with HTMX-first goals, document the tradeoff and generate prompts that minimize JS scope explicitly.

## Examples

### Small Repo (10 prompts)

Starting at `PROMPT_09`, generate 4-6 backend prompts for a chosen Python/FastAPI/Jinja stack, including repository boundaries, HTMX endpoints, tests, and a smoke proof prompt.

### Larger Repo (25 prompts)

Generate an 8-10 prompt backend implementation sequence for a chosen stack in a larger repo, preserving existing numbering and adding validation gates between infrastructure and feature prompts.

