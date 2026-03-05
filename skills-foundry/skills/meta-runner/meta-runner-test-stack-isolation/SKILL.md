---
id: meta-runner-test-stack-isolation
name: Meta Runner Test Stack Isolation
description: Enforce separate integration-test compose stack, volumes, and commands so tests never touch production-like local data.
version: 0.1.0
tags: [meta-runner, docker, integration-tests]
inputs:
  - name: repo_root
    type: path
    required: true
    default: .
    examples: ["."]
  - name: test_compose
    type: path
    required: false
    default: docker-compose.test.yml
    examples: ["docker-compose.test.yml"]
  - name: verify_only
    type: bool
    required: false
    default: true
    examples: [true, false]
expected_tools: [docker, docker-compose, make, rg]
safety:
  dry_run_supported: true
  destructive_actions:
    - "docker compose down -v (test stack only, with explicit confirmation)"
  confirmation_points:
    - "Confirm before running any volume-destructive command"
    - "Confirm before changing Makefile targets used by CI"
outputs:
  - docker-compose.test.yml
  - Makefile
  - docs/TEST_STACK_ISOLATION.md
---

## When to use

Use when integration tests need real services but must be strictly isolated from production-like development data.

## Inputs

- `repo_root`: target repository path.
- `test_compose`: isolated compose file path.
- `verify_only`: check configuration without applying destructive actions.

## Procedure

1. Audit current compose and Make targets for destructive/test coupling patterns.
2. Define isolated test stack services, ports, and volumes.
3. Wire safe Make commands (`test`, `check`, `seed-test`, `reset-dev`) with explicit boundaries.
4. Validate simultaneous operation of dev and test stacks.
5. Run smoke checks against test stack only.
6. Document isolation guarantees and known limits.

## Success criteria

- Test operations do not mutate production-like volumes.
- Safe command boundaries are documented and verifiable.
- Isolation smoke checks pass in check-only mode.

## Failure modes + recovery

- If test stack still shares data paths, stop and patch mounts before running tests.
- If Make targets are ambiguous, split targets and document exclusive usage.
- If simultaneous stack startup fails, resolve port or volume naming conflicts first.

## Examples

### Integration safety hardening

Introduce `docker-compose.test.yml` and safe Make targets so `make test` only targets isolated services.

### Audit-only pass

Run check-only verification to confirm existing stack separation before a release branch cut.
