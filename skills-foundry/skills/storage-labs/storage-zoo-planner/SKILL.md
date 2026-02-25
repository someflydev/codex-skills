---
id: storage-zoo-planner
name: Storage Zoo Planner
description: Plan a storage-paradigm experiment matrix and synthetic dataset catalog with backend-agnostic contracts, workflows, and small-machine Docker profiles.
version: 0.1.0
tags: [storage-labs, storage, planning, synthetic-data]
inputs:
  - name: repo_root
    type: path
    required: true
    default: .
    examples: ["."]
  - name: target_industries
    type: list
    required: false
    default: []
    examples: [["ecommerce", "logistics"], ["fintech", "saas"]]
  - name: machine_profile
    type: enum
    required: false
    default: small-machine
    examples: ["small-machine", "developer-laptop", "full-lab"]
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

Use when you want a backend-language-agnostic plan for experimenting with multiple storage paradigms using realistic synthetic datasets and repeatable workflows.

## Inputs

- `repo_root`: target project root where `docs/` and `data/` will be planned.
- `target_industries`: optional industry focus list to bias dataset examples and workflows.
- `machine_profile`: hardware envelope used to choose default Docker Compose recommendations and smaller fallback profiles.
- `output_root`: repo-relative root for writing docs and `data/` planning artifacts.

## Procedure

1. Define the storage zoo scope and include at minimum these paradigms: relational (Postgres, SQLite), document (MongoDB), key-value (Redis/KeyDB), columnar analytics (DuckDB), graph (Neo4j), search (Elasticsearch or Meilisearch), and streaming/log (Kafka or Redpanda).
2. For each paradigm, propose experiment goals, likely dataset fit, and backend-language-agnostic interface contracts (HTTP/JSON APIs, CLI commands, import/export formats, schemas).
3. Draft dataset shapes and sizes across multiple industries, including realistic volume tiers (toy, dev, medium) and representative workflows (ingest, query, report, archive, replay).
4. Write `docs/STORAGE_ZOO_PLAN.md` with the experiment matrix, Docker Compose recommendations, service dependency notes, and explicit "small machine" profiles that can run on limited hardware.
5. Write `docs/DATASETS_CATALOG.md` with dataset candidates, size tiers, privacy assumptions, and storage-paradigm mapping.
6. Create `data/` planning stubs/spec descriptions (not necessarily full generators) that define where seed generator specs, schemas, and fixture metadata should live.

## Success criteria

- The plan covers all required storage paradigms and names representative engines.
- Interface contracts and workflows are backend-language-agnostic.
- Docker Compose recommendations include a constrained "small machine" profile.
- The dataset catalog maps realistic workflows and size tiers to storage experiments.

## Failure modes + recovery

- If the plan becomes too infrastructure-heavy, recover by reducing the default active services and documenting optional tiers in Compose profiles.
- If dataset scope is vague, recover by selecting 2-3 anchor industries and marking others as phase-two candidates.
- If interface contracts leak language-specific assumptions, rewrite them as HTTP/JSON, CLI, or file-format contracts.

## Examples

### Small Repo (10 prompts)

Plan a compact storage zoo for ecommerce and SaaS billing with SQLite, DuckDB, Redis, and Meilisearch active by default, plus optional heavier services in a secondary Compose profile.

### Larger Repo (25 prompts)

Produce a full storage-zoo plan spanning all required paradigms, dataset tiers, and replay/archive workflows, with a small-machine profile and a fuller team-lab profile.

