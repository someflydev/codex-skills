# Skill Rubric Rule IDs (Lightweight Mapping)

This document maps stable lint issue rule IDs to the human-readable issue text emitted by `skills-lint`.

Code remains authoritative for scoring behavior and final rule emission:
- `skills-foundry/bin/_skills_common.py` (`lint_skill()` and lint issue mapping helpers)

## Rule IDs (Current)

| Rule ID | Typical issue text | Meaning / operator action |
|---|---|---|
| `section.missing` | `Missing section: <name>` | Add the required markdown section with concrete content |
| `validation.errors_present` | `Validation errors present` | Run `skills-validate` and fix schema/required-section issues first |
| `procedure.not_numbered` | `Procedure steps are not numbered` | Rewrite procedure as numbered executable steps |
| `procedure.too_short` | `Procedure is too short to be executable` | Expand to at least 3 concrete steps |
| `procedure.vague` | `Procedure is vague / not executable` | Replace vague wording with explicit commands/files/checks |
| `metadata.expected_tools_missing` | `expected_tools is missing` | Add `expected_tools` metadata |
| `safety.confirmation_points_missing` | `Safety confirmation points are missing` | Add `safety.confirmation_points` |
| `examples.missing` | `Examples are missing` | Add realistic examples metadata/body content |
| `examples.too_thin` | `Examples section is too thin` | Expand examples with scenarios and outcomes |
| `inputs.metadata_incomplete` | `Inputs missing typed inputs` / `Inputs missing input examples` | Ensure input `type` and `examples` are present |
| `failure_modes.recovery_missing` | `Failure modes section lacks recovery guidance` | Add explicit recovery or retry guidance |
| `scope.too_broad` | `Scope appears too broad` | Narrow the skill to one reusable job |
| `template.placeholder_description` | `Placeholder description text remains` | Replace template placeholder description |
| `template.when_to_use_wording` | `When to use section still contains template wording` | Rewrite for the specific skill scenario |
| `template.examples_uncustomized` | `Examples section appears to be uncustomized template content` | Replace template examples with task-specific examples |
| `lint.generic_issue` | Fallback for unmapped issue text | Treat as generic lint issue; inspect text and update mapping if stable |

## Maintenance Notes

- Add or update mappings when new stable lint issue text is introduced.
- Prefer stable, category-like IDs over exact wording in downstream tooling/docs.
- If wording changes but semantics do not, keep the existing rule ID.
