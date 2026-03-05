# Examples - Prompt Resume Reconciler

## Determine Next Prompt After Interrupted Run

```bash
./skills-foundry/bin/repo-helper-preflight --help
./skills-foundry/bin/skills-flow-next --group workflow --lane standard
```

## Evidence Notes Pattern

- Commit evidence: `git log --oneline -n 30`
- Artifact evidence: `rg -n "Acceptance Criteria" .prompts/PROMPT_*.txt`
