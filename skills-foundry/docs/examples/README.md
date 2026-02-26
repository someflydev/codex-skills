# Curated Example Outputs

Tracked snapshots for front-facing docs and packaging.

These are intentionally curated excerpts/samples (not live runtime `reports/` output), so the repo can show proof artifacts without requiring a local rerun first.

Current samples:

- `skills-sync-dry-run.txt` - example sync plan output
- `skills-sync-prune-dry-run.txt` - example prune-capable dry-run sync output
- `skills-lint-summary.md` - sample lint summary excerpt
- `skills-lint-json-snippet.json` - sample lint JSON excerpt (with stable rule IDs)
- `skills-catalog-snippet.md` - sample rendered catalog excerpt

Refresh workflow:

- Manifest/spec: `docs/examples/manifest.json`
- Local refresh helper: `bin/refresh-doc-examples`
- Preview changes without writing: `cd skills-foundry && bin/refresh-doc-examples --dry-run`
