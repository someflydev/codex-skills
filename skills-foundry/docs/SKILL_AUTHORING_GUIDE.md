# Skill Authoring Guide

## Goal

Write narrowly scoped, composable skills with explicit inputs, executable procedures, and clear
success criteria.

## Recommended Pattern

1. Define one job per skill.
2. State inputs and expected tools explicitly.
3. Provide deterministic steps with confirmations for risky actions.
4. Include realistic examples and failure recovery.

## Anti-Patterns

- Skills that try to redesign the whole project
- Vague steps ("improve quality") without checks
- Hidden assumptions about tools or paths
- Cosmetic `_ALT` variants with no behavioral difference
