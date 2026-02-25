---
id: synthetic-data-spec-author
name: Synthetic Data Spec Author
description: Author YAML dataset specifications with entities, distributions, integrity rules, and PII-safe policies for realistic synthetic data workflows.
version: 0.1.0
tags: [storage-labs, synthetic-data, specs, authoring]
inputs:
  - name: industry
    type: enum
    required: true
    default: ecommerce
    examples: ["ecommerce", "healthcare-scheduling", "fintech-ledger", "saas-billing", "logistics", "education"]
  - name: workflow
    type: string
    required: true
    default: ""
    examples: ["order fulfillment and returns", "appointment booking and no-show handling"]
  - name: dataset_name
    type: string
    required: true
    default: ""
    examples: ["orders_and_returns", "appointments_weekly"]
  - name: output_path
    type: path
    required: false
    default: data/specs/<industry>/<dataset>.yaml
    examples: ["data/specs/ecommerce/orders_and_returns.yaml"]
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

Use when you need a synthetic dataset specification YAML for a specific industry workflow with realistic structure, distributions, and privacy-safe generation rules.

## Inputs

- `industry`: one of the supported example domains (ecommerce, healthcare scheduling, fintech ledger, SaaS billing, logistics, education) or a compatible extension.
- `workflow`: real-world business workflow to model (ingest, update, report, archive, replay, etc.).
- `dataset_name`: stable slug used in the output filename.
- `output_path`: default target is `data/specs/<industry>/<dataset>.yaml`.

## Procedure

1. Translate the requested industry workflow into a dataset design with entities, relationships, and cardinalities that support the target queries and reports.
2. Define fields with distributions (categorical, numeric, seasonal, long-tail, event timing) and document assumptions in the YAML spec comments or metadata.
3. Add time-series behavior rules (arrival patterns, seasonality, retries, cancellations, delayed updates) where relevant.
4. Encode referential integrity rules and cross-entity constraints so generated data can be loaded into relational, document, or analytics stores without obvious inconsistencies.
5. Include PII-safe rules and a redaction policy section that prevents real identifiers or sensitive combinations from leaking into generated output.
6. Write the final YAML to `data/specs/<industry>/<dataset>.yaml` and provide a short summary of supported use cases.

## Success criteria

- The spec defines entities, relationships, cardinalities, field distributions, time behavior, integrity rules, and PII-safe policy.
- The YAML path follows `data/specs/<industry>/<dataset>.yaml`.
- The resulting spec is realistic enough to support ingest/query/report testing scenarios.

## Failure modes + recovery

- If the workflow is underspecified, recover by proposing a minimal entity set and asking for missing reporting/query needs.
- If realism assumptions conflict with privacy constraints, favor PII-safe rules and document the realism tradeoff.
- If the spec grows too complex, split it into smaller workflow-specific datasets with shared reference entities.

## Examples

### Small Repo (10 prompts)

Author `data/specs/ecommerce/orders_and_returns.yaml` for an ecommerce order lifecycle with seasonal demand, returns, refunds, and PII-safe customer fields.

### Larger Repo (25 prompts)

Create a fintech ledger dataset spec with accounts, transactions, settlements, reversals, time-series spikes, and explicit referential integrity rules for replay and audit workflows.

