#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    prog = Path(__file__).name
    parser = argparse.ArgumentParser(
        prog=prog,
        description=f"Stub CLI for {prog} (PROMPT_01 scaffold).",
    )
    parser.add_argument(
        "extra",
        nargs="*",
        help="Placeholder positional arguments for future implementation.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"{prog} 0.1.0-stub",
    )
    return parser


def main() -> int:
    parser = build_parser()
    if len(sys.argv) == 1:
        parser.print_help()
        print("\nNext steps:")
        print(f"  - Implement real behavior for {Path(__file__).name} in later prompts.")
        print("  - Run with --help to inspect options while the interface evolves.")
        return 0

    args = parser.parse_args()
    print(f"{Path(__file__).name}: stub command invoked with args={args.extra}")
    print("Implementation is pending a later prompt.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
