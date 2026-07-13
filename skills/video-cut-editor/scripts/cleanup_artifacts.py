#!/usr/bin/env python3
"""List or delete video-cut-editor generated artifacts while preserving media outputs."""

from __future__ import annotations

import argparse
import shutil
import sys
import tempfile
from pathlib import Path


DIR_PATTERNS = ("*.video-cut-artifacts", "edit-*-video-cut-editor", "merged-spot-check")
FILE_PATTERNS = (
    "spot-check-summary.json",
    "*.join-map.json",
    "*.join-map.waveform-audit.json",
    "*.join-map.waveform-audit.md",
    "*.waveform-audit.*",
    "merged-spot-*",
    "*.merge.log",
    "*.render.log",
    "*.qa-report.md",
    "qa-report.md",
)
PRESERVE_SUFFIXES = (".mp4", ".mov", ".m4v")


def fail(message: str, code: int = 1) -> int:
    print(f"error: {message}", file=sys.stderr)
    return code


def collect(root: Path) -> list[Path]:
    found: dict[Path, None] = {}
    for pattern in DIR_PATTERNS:
        for path in root.glob(pattern):
            if path.is_dir():
                found[path] = None
    for pattern in FILE_PATTERNS:
        for path in root.glob(pattern):
            if path.is_file() and path.suffix.lower() not in PRESERVE_SUFFIXES:
                found[path] = None
    return sorted(found)


def remove(path: Path) -> None:
    if path.is_dir():
        shutil.rmtree(path)
    elif path.exists():
        path.unlink()


def run_self_test() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "edit-demo-video-cut-editor").mkdir()
        (root / "merged-spot-check").mkdir()
        (root / "demo.video-cut-artifacts").mkdir()
        (root / "spot-check-summary.json").write_text("[]\n")
        (root / "demo.join-map.json").write_text("{}\n")
        (root / "demo.join-map.waveform-audit.md").write_text("audit\n")
        (root / "demo.waveform-audit.tight.csv").write_text("audit\n")
        (root / "merged-spot-head.wav").write_text("audio\n")
        (root / "demo.merge.log").write_text("log\n")
        (root / "keep.edited.mp4").write_text("media\n")
        candidates = collect(root)
        names = {item.name for item in candidates}
        assert "edit-demo-video-cut-editor" in names
        assert "merged-spot-check" in names
        assert "demo.video-cut-artifacts" in names
        assert "spot-check-summary.json" in names
        assert "demo.join-map.json" in names
        assert "demo.join-map.waveform-audit.md" in names
        assert "demo.waveform-audit.tight.csv" in names
        assert "merged-spot-head.wav" in names
        assert "demo.merge.log" in names
        assert "keep.edited.mp4" not in names
        for item in candidates:
            remove(item)
        assert (root / "keep.edited.mp4").exists()
    print("self_test: ok")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="List or delete video-cut-editor generated artifacts.")
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    parser.add_argument("--delete", action="store_true", help="delete candidates; default only lists them")
    parser.add_argument("--self-test", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.self_test:
        return run_self_test()
    root = args.root.expanduser().resolve()
    if not root.exists() or not root.is_dir():
        return fail(f"root directory not found: {root}")
    candidates = collect(root)
    action = "delete" if args.delete else "dry_run"
    print(f"root: {root}")
    print(f"action: {action}")
    print(f"candidates: {len(candidates)}")
    for path in candidates:
        print(path)
    if args.delete:
        for path in candidates:
            remove(path)
        print("cleanup: ok")
    else:
        print("dry_run: pass --delete to remove candidates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
