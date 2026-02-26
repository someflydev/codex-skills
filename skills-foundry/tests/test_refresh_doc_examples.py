from pathlib import Path
import json
import subprocess


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "bin" / "refresh-doc-examples"


def test_refresh_doc_examples_help_and_dry_run(tmp_path: Path) -> None:
    docs_examples = tmp_path / "docs" / "examples"
    docs_examples.mkdir(parents=True)
    manifest_path = docs_examples / "manifest.json"
    manifest_path.write_text(json.dumps({"version": 1, "entries": []}, indent=2) + "\n", encoding="utf-8")

    help_result = subprocess.run([str(CLI), "--help"], capture_output=True, text=True)
    assert help_result.returncode == 0
    assert "Refresh curated docs/examples snippets" in help_result.stdout

    dry_run = subprocess.run(
        [str(CLI), "--root", str(tmp_path), "--manifest", "docs/examples/manifest.json", "--dry-run"],
        capture_output=True,
        text=True,
    )
    assert dry_run.returncode == 0, dry_run.stdout + "\n" + dry_run.stderr
    assert "mode: dry-run" in dry_run.stdout
    assert "entries: 0" in dry_run.stdout


def test_refresh_doc_examples_can_write_from_manifest_entries(tmp_path: Path) -> None:
    source_dir = tmp_path / "reports"
    source_dir.mkdir(parents=True)
    (source_dir / "skills-lint.json").write_text(
        json.dumps(
            [
                {"skill_id": "a", "top_issue_rule_ids": ["template.when_to_use_wording"], "top_issues": ["Issue A"]},
                {"skill_id": "b", "top_issue_rule_ids": ["scope.too_broad"], "top_issues": ["Issue B"]},
            ],
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    docs_examples = tmp_path / "docs" / "examples"
    docs_examples.mkdir(parents=True)
    manifest = {
        "version": 1,
        "entries": [
            {
                "id": "lint-json",
                "type": "json-slice",
                "source": "reports/skills-lint.json",
                "target": "docs/examples/lint-snippet.json",
                "max_items": 1,
                "fields": ["skill_id", "top_issue_rule_ids"],
            },
            {
                "id": "cmd-snippet",
                "type": "command-text",
                "command": ["python3", "-c", "print('line1'); print('keep line2')"],
                "cwd": ".",
                "target": "docs/examples/cmd-snippet.txt",
                "include_substrings": ["keep"],
            },
        ],
    }
    (docs_examples / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    result = subprocess.run(
        [str(CLI), "--root", str(tmp_path), "--manifest", "docs/examples/manifest.json"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + "\n" + result.stderr

    lint_snippet = json.loads((docs_examples / "lint-snippet.json").read_text(encoding="utf-8"))
    assert lint_snippet == [{"skill_id": "a", "top_issue_rule_ids": ["template.when_to_use_wording"]}]

    cmd_text = (docs_examples / "cmd-snippet.txt").read_text(encoding="utf-8")
    assert "keep line2" in cmd_text
    assert "line1" not in cmd_text
