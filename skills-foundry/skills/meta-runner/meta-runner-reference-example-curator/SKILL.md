---
id: meta-runner-reference-example-curator
name: Meta Runner Reference Example Curator
description: Curate, sequence, and verify high-signal reference examples for meta-runner adoption with clear standard/alt pathways.
version: 0.1.0
tags: [meta-runner, references, curation]
inputs:
  - name: repo_root
    type: path
    required: true
    default: .
    examples: ["."]
  - name: focus_track
    type: enum
    required: false
    default: meta-runner
    examples: ["meta-runner", "workflow", "cross-track"]
  - name: include_alt_lane
    type: bool
    required: false
    default: true
    examples: [true, false]
expected_tools: [git, rg, python3]
safety:
  dry_run_supported: true
  destructive_actions: []
  confirmation_points:
    - "Confirm before changing flow ordering used by operators"
outputs:
  - docs/REFERENCE_EXAMPLES_CURATION.md
  - skills-foundry/flows/meta-runner.json
  - skills-foundry/docs/SKILL_FLOWS.md
---

## When to use

Use when expanding or refining reference examples for meta-runner workflows so operators have a clear and verified sequence.

## Inputs

- `repo_root`: repository root path.
- `focus_track`: track scope for curation changes.
- `include_alt_lane`: whether alt-lane ordering must be updated in lockstep.

## Procedure

1. Inventory current reference examples and flow ordering.
2. Rank candidate examples by operator impact and verification quality.
3. Propose standard/alt lane updates with dependency notes.
4. Regenerate flow docs and verify next-step CLI output remains coherent.
5. Validate reference examples with tests/compact validation.
6. Produce curation notes with rationale and deferred candidates.

## Success criteria

- Flow ordering remains deterministic and dependency-safe.
- New curated examples appear in generated flow docs.
- Validation/tests confirm structural integrity.

## Failure modes + recovery

- If ordering introduces ambiguity, halt and revert to last deterministic sequence.
- If flow docs and manifests diverge, regenerate and re-verify before commit.
- If candidate quality evidence is weak, defer additions and record why.

## Examples

### Curate Stage-4 Additions

Add new reference examples to meta-runner and workflow lanes with evidence-backed ordering.

### Audit Existing Curated Set

Run validation-focused curation pass without changing lane order.
