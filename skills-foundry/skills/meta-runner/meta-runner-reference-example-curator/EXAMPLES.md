# Examples - Meta Runner Reference Example Curator

## Curate New Stage Additions

```bash
./skills-foundry/bin/skills-flow-next --group meta-runner --lane standard
./skills-foundry/bin/skills-flow-render
```

## Verify Curation Quality

```bash
./skills-foundry/bin/skills-validate --compact
.venv/bin/pytest -q skills-foundry/tests/test_skills_flow_next.py
```
