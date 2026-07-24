#!/usr/bin/env python3
"""Compatibility shim: unrestricted transcript replacement is retired."""

import argparse
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="Deprecated non-mutating correction shim")
    parser.add_argument("args", nargs="*", help=argparse.SUPPRESS)
    parser.parse_known_args()
    print(
        "correct.py no longer changes transcripts. "
        "Use: uv run python scripts/review.py review --analysis <analysis.json>",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
