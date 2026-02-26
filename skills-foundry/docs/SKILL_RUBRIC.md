# Skill Rubric

This document is a human-readable rubric guide. The current scoring behavior is implemented in code (`skills-foundry/bin/_skills_common.py`, `lint_skill()`), which is the authoritative source when doc and code differ.

## Scoring

- Completeness: 0-100
- Excellence: 0-10

## Core Checks

- Required metadata fields present
- Required sections present
- Procedure steps are explicit and executable
- Inputs are typed and include examples
- Safety confirmations and expected tools are documented
- Examples are realistic
- Failure modes include recovery steps
- Scope is narrow enough to be reusable

## Output Format (Target)

The linter should emit per-skill scores, issues, and concrete suggested fixes.
