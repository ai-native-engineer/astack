#!/usr/bin/env python3
import argparse
from pathlib import Path


PRUNE_SUBSTRINGS = (
    "/about-us/strate.md",
    "/sustainability/sustainability/",
)


def main() -> None:
    ap = argparse.ArgumentParser(description="Prune obviously broken recursive crawl page files")
    ap.add_argument("pages_dir", help="recursive-crawl/pages directory")
    args = ap.parse_args()

    pages_dir = Path(args.pages_dir)
    removed = []
    for page in pages_dir.rglob("*.md"):
        posix = page.as_posix()
        if any(token in posix for token in PRUNE_SUBSTRINGS):
            removed.append(page)

    for page in removed:
        page.unlink(missing_ok=True)
        print(page)

    print(f"removed: {len(removed)}")


if __name__ == "__main__":
    main()
