from __future__ import annotations

import importlib.util
import sys
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMMON_PATH = ROOT / "bin" / "_skills_common.py"

SPEC = importlib.util.spec_from_file_location("skills_common_test_module", COMMON_PATH)
assert SPEC is not None
assert SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def test_extract_outputs_block_ignores_nested_lists_in_other_blocks() -> None:
    front_matter = textwrap.dedent(
        """\
        id: sample-skill
        safety:
          dry_run_supported: true
          destructive_actions: []
          confirmation_points:
            - Confirm before write
        outputs:
          - docs/OUT.md
          - skills/core/example/SKILL.md
        expected_tools: [git]
        """
    )

    outputs = MODULE.extract_list_items_from_front_matter_block(front_matter, "outputs")

    assert outputs == ["docs/OUT.md", "skills/core/example/SKILL.md"]


def test_extract_outputs_block_supports_inline_list_syntax() -> None:
    front_matter = textwrap.dedent(
        """\
        id: sample-inline
        outputs: [docs/OUT.md, skills-foundry/reports/out.md, "build/custom.txt"]
        expected_tools: [git]
        """
    )

    outputs = MODULE.extract_list_items_from_front_matter_block(front_matter, "outputs")

    assert outputs == ["docs/OUT.md", "skills-foundry/reports/out.md", "build/custom.txt"]


def test_parse_front_matter_minimal_handles_comments_and_blank_lines() -> None:
    front_matter = textwrap.dedent(
        """\
        # top-level comment
        id: parser-comment-test

        name: Parser Comment Test
        description: Ensure comments and blanks do not break parsing.
        version: 0.1.0
        tags: [workflow, parser]
        expected_tools: [git]
        safety:
          dry_run_supported: true
          destructive_actions: []
          confirmation_points:
            - Confirm before write
        """
    )

    metadata, messages = MODULE.parse_front_matter_minimal(front_matter)

    assert messages == []
    assert metadata["id"] == "parser-comment-test"
    assert metadata["tags"] == ["workflow", "parser"]
    assert "confirmation_points:" in str(metadata["safety"])

