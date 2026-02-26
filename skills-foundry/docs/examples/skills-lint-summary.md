# Lint Summary (Example)

Example excerpt from `skills-lint` output after post-flight fixes:

```text
Linted 27 skills
- JSON report: skills-foundry/reports/skills-lint.json
- Markdown report: skills-foundry/reports/skills-lint.md
- smoke-check: completeness=72 excellence=3
- prompt-preflight-inspector: completeness=100 excellence=10
- prompt-preflight-inspector-alt: completeness=100 excellence=10
```

Notes:

- `smoke-check` is intentionally a scaffold/smoke artifact and now scores lower due placeholder-template detection.
- Most workflow/polyglot/storage-labs skills score highly because they contain richer, customized content.
