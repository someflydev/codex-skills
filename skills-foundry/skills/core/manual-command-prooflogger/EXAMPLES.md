# Examples - Manual Command Prooflogger

## Capture Validation And Test Evidence

```bash
./skills-foundry/bin/skills-validate --compact
.venv/bin/pytest -q skills-foundry
```

## Capture Flow Command Evidence

```bash
./skills-foundry/bin/skills-flow-next --list-groups
./skills-foundry/bin/skills-flow-render
```
