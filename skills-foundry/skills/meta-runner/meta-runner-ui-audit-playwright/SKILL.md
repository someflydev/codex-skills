---
id: meta-runner-ui-audit-playwright
name: Meta Runner UI Audit Playwright
description: Design and execute deterministic Playwright audits for critical user journeys with trace/video diagnostics and wiring-fix feedback loops.
version: 0.1.0
tags: [meta-runner, playwright, e2e]
inputs:
  - name: repo_root
    type: path
    required: true
    default: .
    examples: ["."]
  - name: flow_scope
    type: string
    required: false
    default: critical
    examples: ["critical", "all"]
  - name: headed
    type: bool
    required: false
    default: false
    examples: [false, true]
expected_tools: [uv, python3, pytest, playwright]
safety:
  dry_run_supported: true
  destructive_actions: []
  confirmation_points:
    - "Confirm before installing browser dependencies"
    - "Confirm before applying UI wiring fixes detected during audit"
outputs:
  - docs/e2e-audit-plan.md
  - docs/e2e-coverage-matrix.md
  - docs/e2e-audit-report.md
  - artifacts/e2e-audit/<run-id>/RUN.json
---

## When to use

Use when a prompt stage requires high-confidence UI verification against real backend behavior and reproducible diagnostics artifacts.

## Inputs

- `repo_root`: target repository path.
- `flow_scope`: audit scope for user journeys.
- `headed`: run browser in headed mode for local debugging.

## Procedure

1. Discover frontend surfaces and map critical user journeys.
2. Create coverage matrix linking backend contracts to UI assertions.
3. Ensure deterministic setup (seed, environment, event-driven waits).
4. Implement/execute Playwright tests with tracing enabled.
5. Capture per-flow artifacts (video, trace, screenshot, console/network logs).
6. Report mismatches and implement low-risk wiring fixes with regression coverage.

## Success criteria

- Critical flows are covered by deterministic tests.
- Audit report includes actionable evidence for pass/fail outcomes.
- Artifacts are organized by run and flow.

## Failure modes + recovery

- If stack cannot start, stop and publish prerequisite checklist.
- If tests are flaky, replace sleeps with event-driven waits and isolate fixtures.
- If fixes are high-risk, propose patches and stop for operator approval.

## Examples

### Critical flow audit

Audit login/dashboard/filter journeys with trace artifacts and a wiring mismatch report.

### Regression lock-in

After fixing a UI data-binding bug, add targeted Playwright assertions and rerun affected flows.
