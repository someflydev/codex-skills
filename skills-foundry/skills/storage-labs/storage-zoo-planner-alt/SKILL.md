---
id: storage-zoo-planner-alt
name: Storage Zoo Planner (ALT)
description: Broad-coverage storage zoo planner that prioritizes many datasets and wide paradigm coverage with lighter realism and faster iteration.
version: 0.1.0
tags: [storage-labs, storage, planning, synthetic-data, alt]
inputs:
  - name: repo_root
    type: path
    required: true
    default: .
    examples: ["."]
  - name: coverage_target
    type: enum
    required: false
    default: broad
    examples: ["broad", "very-broad"]
  - name: machine_profile
    type: enum
    required: false
    default: small-machine
    examples: ["small-machine", "developer-laptop"]
  - name: output_root
    type: path
    required: false
    default: .
    examples: ["."]
expected_tools: [git, rg, python3, docker]
safety:
  dry_run_supported: true
  destructive_actions: []
  confirmation_points:
    - "Confirm before overwriting docs/STORAGE_ZOO_PLAN.md or docs/DATASETS_CATALOG.md"
outputs:
  - docs/STORAGE_ZOO_PLAN.md
  - docs/DATASETS_CATALOG.md
  - data/
---

## When to use

Use when you want many dataset scenarios and broad storage coverage quickly, even if each dataset's realism depth is intentionally lighter in the first pass.

## Inputs

- `repo_root`: target project root.
- `coverage_target`: desired breadth of industries and storage-paradigm combinations.
- `machine_profile`: hardware limit used to decide what stays in default vs optional Compose profiles.
- `output_root`: repo-relative path for docs and `data/` planning artifacts.

## Procedure

1. Start from the full required storage paradigm list and maximize coverage across industries before deepening any single dataset.
2. Define lightweight backend-agnostic interface contracts (HTTP/JSON, CLI, import/export) that enable quick experiments across many services.
3. Build a wide `docs/DATASETS_CATALOG.md` with many dataset candidates, broad industry coverage, small/medium size tiers, and lighter realism notes where assumptions are simplified.
4. Write `docs/STORAGE_ZOO_PLAN.md` with an experiment matrix that emphasizes fast spin-up, shared fixtures, and Docker Compose profiles that keep the default profile small-machine-friendly.
5. Create `data/` spec placeholders and naming conventions so many datasets can be added incrementally without redesigning the layout.
6. Mark high-realism upgrades explicitly as later follow-ups rather than inflating the initial plan.

## Success criteria

- Coverage across paradigms and industries is broad and clearly organized.
- Compose recommendations support quick iteration on limited hardware.
- Lighter realism assumptions are explicit so future upgrades are possible.

## Failure modes + recovery

- If breadth makes the plan unreadable, recover by grouping datasets by industry and workflow families.
- If small-machine defaults become overloaded, move heavier services into optional profiles and note startup order.
- If realism assumptions become misleading, annotate them and downgrade confidence for those datasets.

## Examples

### Small Repo (10 prompts)

Create a broad catalog with small sample datasets across ecommerce, education, and logistics while keeping only a subset of services active in the default Compose profile.

### Larger Repo (25 prompts)

Plan a wide experiment matrix for many industries and storage engines with shared contracts and fixture formats, deferring deep realism to later prompts.

