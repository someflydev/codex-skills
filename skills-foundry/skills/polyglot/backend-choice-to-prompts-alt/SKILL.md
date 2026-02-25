---
id: backend-choice-to-prompts-alt
name: Backend Choice To Prompts (ALT)
description: Learning-oriented prompt generator that turns a selected backend stack into an HTMX-first build sequence emphasizing unique paradigms and educational tradeoffs.
version: 0.1.0
tags: [polyglot, backend, prompts, generator, alt]
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
    examples: [{language: "Elixir", framework: "Phoenix", templates: "HEEx"}]
  - name: project_constraints
    type: object
    required: true
    default: {}
    examples: [{frontend_js: minimal, htmx_first: true, learning_value: high}]
  - name: learning_goal
    type: string
    required: false
    default: "Explore a unique backend paradigm while shipping a usable vertical slice"
    examples: ["Learn actor-model concurrency", "Learn functional pipelines in web backends"]
expected_tools: [git, rg, python3]
safety:
  dry_run_supported: true
  destructive_actions: []
  confirmation_points:
    - "Confirm before writing or overwriting PROMPT_XX files in .prompts/"
    - "Confirm before generating prompts that introduce unfamiliar infrastructure"
outputs:
  - .prompts/PROMPT_<NN>.txt
  - skills-foundry/reports/backend-choice-to-prompts-plan.md
---

## When to use

Use when the chosen backend stack is selected partly for learning value or unique paradigms and you want prompts that teach the team while still delivering a working HTMX-first backend.

## Inputs

- `repo_root`: target repo containing `.prompts/`.
- `selected_stack`: chosen language/framework combo, often with a less-common paradigm or runtime model.
- `project_constraints`: project non-negotiables, including minimal JS and HTMX-first behavior.
- `learning_goal`: the educational outcome the generated prompts should reinforce.

## Procedure

1. Inspect existing `.prompts/` numbering and conventions, then reserve a prompt range for the new backend sequence.
2. Convert the selected stack and `learning_goal` into a staged teaching plan: fundamentals first, then one vertical slice, then operational hardening.
3. Generate ordered `PROMPT_XX.txt` files that preserve the same project constraints as the base variant while emphasizing:
   - HTMX-first server interactions over client-side JS frameworks
   - template organization that showcases the stack's paradigm (for example functional composition, actors, channels, etc.)
   - explicit data layer boundaries so experimentation does not spread architectural confusion
   - explanatory verification checkpoints that validate learning and runtime behavior
4. Call out where the stack is unusual and add prompts that reduce onboarding risk (glossary, local dev setup, testing patterns) before deeper feature work.
5. End with a smoke proof prompt plus a short retrospective prompt suggestion for what the team learned and what to standardize.
6. Write a planning report that distinguishes educational prompts from delivery-critical prompts.

## Success criteria

- The generated prompt sequence remains HTMX-first/minimal-JS and ships a usable vertical slice.
- Unique paradigm concepts are introduced in a teachable order instead of being scattered.
- Prompt outputs clearly separate learning scaffolding from production-hardening follow-ups.

## Failure modes + recovery

- If the selected stack is too unfamiliar for the team, recover by inserting extra setup and testing prompts before feature prompts.
- If learning-focused prompts start diluting delivery goals, rebalance toward a smaller vertical slice and defer advanced topics.
- If `.prompts/` numbering or naming conflicts appear, stop and request a new range before writing files.

## Examples

### Small Repo (10 prompts)

Generate a short Elixir/Phoenix-oriented prompt sequence that teaches the core paradigm, implements one HTMX-friendly server-rendered flow, and ends with a smoke proof.

### Larger Repo (25 prompts)

Create a learning-first prompt expansion for a unique backend stack, with onboarding prompts, clear data-boundary prompts, and verification gates before advanced features.

