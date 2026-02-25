# Operator Manual

## Purpose

Run the skills-foundry workflow end-to-end on repositories that use ordered `.prompts/` files.

## Planned Workflow

1. Author/update skills and templates.
2. Validate and lint skills.
3. Sync skills into `~/.codex/skills`.
4. Use installed skills on a target repo.

## Sync Notes (copy vs symlink)

- Use `--strategy copy` for a portable installed snapshot.
- Use `--strategy symlink` while iterating locally when you want changes in the source repo to be
  reflected immediately in the installed skill directory.
- Use `--dry-run` before pruning or overwriting large sets.

## Versioning Skills

- Keep `id` stable and change `version` as the skill evolves.
- Treat `_ALT` / `-alt` variants as separate skills with separate ids and independent versions.

## Status

`skills-new`, `skills-validate`, `skills-lint`, `skills-render`, and `skills-sync` are available in
basic form and will be expanded in later prompts.
