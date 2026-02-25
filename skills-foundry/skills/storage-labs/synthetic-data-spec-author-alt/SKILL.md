---
id: synthetic-data-spec-author-alt
name: Synthetic Data Spec Author (ALT)
description: Deep-realism synthetic data spec authoring variant that favors fewer datasets with richer edge cases, temporal behavior, and integrity constraints.
version: 0.1.0
tags: [storage-labs, synthetic-data, specs, authoring, alt]
inputs:
  - name: industry
    type: enum
    required: true
    default: healthcare-scheduling
    examples: ["ecommerce", "healthcare-scheduling", "fintech-ledger", "saas-billing", "logistics", "education"]
  - name: workflow
    type: string
    required: true
    default: ""
    examples: ["multi-clinic appointment scheduling and rescheduling"]
  - name: dataset_name
    type: string
    required: true
    default: ""
    examples: ["clinic_appointments_detailed"]
  - name: realism_depth
    type: enum
    required: false
    default: deep
    examples: ["deep", "very-deep"]
expected_tools: [git, rg, python3]
safety:
  dry_run_supported: true
  destructive_actions: []
  confirmation_points:
    - "Confirm before overwriting an existing data/specs/<industry>/<dataset>.yaml file"
outputs:
  - data/specs/<industry>/<dataset>.yaml
---

## When to use

Use when you want fewer synthetic datasets but much deeper realism, including nuanced edge cases, richer temporal behavior, and stricter integrity constraints.

## Inputs

- `industry`: target domain such as ecommerce, healthcare scheduling, fintech ledger, SaaS billing, logistics, or education.
- `workflow`: the precise workflow to model, including exceptions and operational edge cases.
- `dataset_name`: stable slug for the YAML filename under `data/specs/<industry>/`.
- `realism_depth`: controls how aggressively to model rare events, anomalies, and operational quirks.

## Procedure

1. Narrow scope to one high-value workflow and explicitly prefer depth of realism over breadth of entities.
2. Model entities, relationships, and cardinalities with edge cases (late events, retries, partial failures, reversals, cancellations, duplicate submissions) that matter for realistic testing.
3. Define detailed field distributions and time-series behavior, including seasonality, burstiness, drift, and rare-event rates.
4. Add strict referential integrity rules plus invariant checks that catch subtle inconsistencies during synthetic generation.
5. Write a strong PII-safe and redaction policy that preserves realism patterns without exposing real identities or reconstructable sensitive records.
6. Output `data/specs/<industry>/<dataset>.yaml` and summarize what realism dimensions are covered vs intentionally deferred.

## Success criteria

- The YAML spec is deeply realistic for a single workflow and documents edge-case behavior.
- Referential integrity and invariant rules are explicit and testable.
- Privacy/redaction policy remains strong despite richer realism modeling.

## Failure modes + recovery

- If deep realism balloons the scope, recover by deferring secondary entities and documenting them as future specs.
- If rare-event modeling becomes guesswork, encode assumptions and confidence levels instead of pretending certainty.
- If privacy-safe constraints remove too much realism, preserve aggregate patterns and event timing while redacting sensitive identifiers.

## Examples

### Small Repo (10 prompts)

Author a deep healthcare scheduling spec with appointment booking, rescheduling, cancellations, no-shows, provider availability changes, and privacy-safe patient identifiers.

### Larger Repo (25 prompts)

Produce a deep-realism SaaS billing or fintech ledger spec with retries, reversals, late settlements, seasonality, and invariant checks suitable for replay and audit experiments.

