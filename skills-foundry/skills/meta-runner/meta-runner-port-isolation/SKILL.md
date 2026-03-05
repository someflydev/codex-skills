---
id: meta-runner-port-isolation
name: Meta Runner Port Isolation
description: Find safe non-default ports for runtime/test services and propagate updates with explicit verification and rollback notes.
version: 0.1.0
tags: [meta-runner, ports, docker]
inputs:
  - name: repo_root
    type: path
    required: true
    default: .
    examples: ["."]
  - name: prefer_near_default
    type: bool
    required: false
    default: true
    examples: [true, false]
  - name: dry_run
    type: bool
    required: false
    default: true
    examples: [true, false]
expected_tools: [docker, rg, python3]
safety:
  dry_run_supported: true
  destructive_actions: []
  confirmation_points:
    - "Confirm before changing live compose port mappings"
    - "Confirm before applying port changes across multiple files"
outputs:
  - docs/PORT_ISOLATION_NOTES.md
  - docker-compose.yml
  - docker-compose.test.yml
---

## When to use

Use when production-like and test stacks must run simultaneously without default-port collisions.

## Inputs

- `repo_root`: target repository path.
- `prefer_near_default`: choose visually similar non-default ports when available.
- `dry_run`: preview changes before applying.

## Procedure

1. Enumerate currently used ports from compose files and running containers.
2. Propose non-default alternatives close to service defaults.
3. Verify candidate ports are unused.
4. Apply updates across compose/config/docs with explicit mapping table.
5. Validate services bind correctly and health checks pass.
6. Document rollback mappings and verification outputs.

## Success criteria

- No default-port collisions remain between active stacks.
- Port changes are consistent across configs and docs.
- Verification evidence includes live bind checks.

## Failure modes + recovery

- If no safe remap can be verified, stop and keep existing mappings until operator approval is provided.
- If no suitable nearby port is free, expand search range and document rationale.
- If service health fails after remap, revert mapping and re-test incrementally.
- If docs drift from config, regenerate mapping notes before commit.

## Examples

### Dual-stack local development

Move test services to nearby non-default host ports while keeping internal service ports unchanged.

### Collision remediation

Detect conflict with an existing long-lived container and remap safely with verification logs.
