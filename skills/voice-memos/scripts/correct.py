#!/usr/bin/env python3
"""
사전 기반 전사 오류 교정.

corrections.json의 매핑을 사용하여
전사 마크다운 파일의 오류를 일괄 치환합니다.
"""

import json
import sys
from pathlib import Path

from config import CORRECTIONS_FILE, TRANSCRIPTS_DIR, iter_transcript_files

CORRECTION_MARKER = "<!-- corrected -->"


def load_corrections() -> dict:
    """corrections.json을 로드합니다."""
    if not CORRECTIONS_FILE.exists():
        return {}
    return json.loads(CORRECTIONS_FILE.read_text(encoding="utf-8"))


def correct_file(filepath: Path, corrections: dict, force: bool = False) -> bool:
    """단일 파일의 전사 오류를 교정합니다."""
    content = filepath.read_text(encoding="utf-8")

    if CORRECTION_MARKER in content and not force:
        return False

    original = content
    for wrong, right in corrections.items():
        content = content.replace(wrong, right)

    if content == original and CORRECTION_MARKER in content:
        return False

    if CORRECTION_MARKER not in content:
        content = content.rstrip() + "\n\n" + CORRECTION_MARKER + "\n"

    if content != original:
        filepath.write_text(content, encoding="utf-8")
        changes = sum(original.count(wrong) for wrong in corrections if wrong in original)
        if changes:
            print(f"  {filepath.name} ({changes}건 교정)")
        return True

    return False


def main():
    import argparse

    parser = argparse.ArgumentParser(description="사전 기반 전사 오류 교정")
    parser.add_argument("--file", type=str, help="특정 파일만 교정")
    parser.add_argument("--force", action="store_true", help="이미 교정된 파일도 재처리")
    parser.add_argument("--all", action="store_true", help="모든 전사 파일 교정")
    args = parser.parse_args()

    corrections = load_corrections()
    if not corrections:
        print(f"단어장이 비어있거나 없습니다: {CORRECTIONS_FILE}", file=sys.stderr)
        sys.exit(1)

    if args.file:
        correct_file(Path(args.file).expanduser(), corrections, force=args.force)
        return

    files = iter_transcript_files(TRANSCRIPTS_DIR)
    if args.all:
        processed = sum(1 for file in files if correct_file(file, corrections, force=args.force))
    else:
        processed = sum(1 for file in files if correct_file(file, corrections))

    print(f"  {processed}/{len(files)} 교정됨")


if __name__ == "__main__":
    main()
