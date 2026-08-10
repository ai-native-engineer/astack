#!/usr/bin/env python3
"""GitHub's 1 MiB Markdown render limit을 넘는 생성물을 링크된 조각으로 분할한다."""

import argparse
import glob
import os
import re
import shutil
import tempfile

SOURCE = re.compile(r"^<!-- source: (https://\S+) -->\n?")
MARKER = "<!-- chunk-start -->\n"


def chunks(text, limit):
    """UTF-8 경계를 보존하고 가능하면 줄 경계에서 자른다."""
    out = []
    while len(text.encode()) > limit:
        raw = text.encode()
        cut = limit
        while cut and (raw[cut] & 0xC0) == 0x80:
            cut -= 1
        head = raw[:cut].decode()
        line = head.rfind("\n")
        if line >= limit // 2:
            head = head[:line + 1]
        while head.endswith("\n\n"):
            head = head[:-1]
        out.append(head)
        text = text[len(head):]
    out.append(text)
    return out


def process(path, limit, force=False):
    text = open(path, encoding="utf-8", errors="replace").read()
    match = SOURCE.match(text)
    if not match:
        return 0
    part_dir = os.path.splitext(path)[0] + ".parts"
    old_parts = sorted(glob.glob(os.path.join(part_dir, "part-*.md")))
    if old_parts and "# Split page" in text:
        headers_current = all(
            open(part, encoding="utf-8").readline().startswith("<!-- source: ")
            for part in old_parts
        )
        if not force and headers_current and all(os.path.getsize(part) <= limit for part in old_parts):
            return 0
        body = "".join(
            open(part, encoding="utf-8").read().split(MARKER, 1)[1]
            for part in old_parts
        )
    else:
        if os.path.getsize(path) <= limit:
            return 0
        body = text[match.end():]
    source = match.group(1)
    body = body.rstrip("\n") + "\n"
    parts = chunks(body, limit - min(4096, limit // 4))
    if os.path.isdir(part_dir):
        shutil.rmtree(part_dir)
    os.makedirs(part_dir)
    links = []
    for number, part in enumerate(parts, 1):
        name = f"part-{number:03d}.md"
        links.append(f"- [Part {number}]({os.path.basename(part_dir)}/{name})")
        with open(os.path.join(part_dir, name), "w", encoding="utf-8") as f:
            f.write(f"<!-- source: {source} -->\n<!-- part of: {source} -->\n\n{MARKER}{part}")
    with open(path, "w", encoding="utf-8") as f:
        f.write(
            f"<!-- source: {source} -->\n\n# Split page\n\n"
            "This generated page exceeded GitHub's Markdown render limit. "
            "Its complete content is preserved in ordered parts.\n\n"
            + "\n".join(links) + "\n"
        )
    return len(parts)


def self_test():
    with tempfile.TemporaryDirectory() as root:
        path = os.path.join(root, "x.md")
        body = ("한글 and text\n" * 200)
        with open(path, "w", encoding="utf-8") as f:
            f.write("<!-- source: https://example.com/x -->\n" + body)
        assert process(path, 1024) > 1
        part_dir = os.path.join(root, "x.parts")
        rebuilt = "".join(
            open(p, encoding="utf-8").read().split(MARKER, 1)[1]
            for p in sorted(glob.glob(os.path.join(part_dir, "*.md")))
        )
        assert rebuilt == body
        assert all(os.path.getsize(p) <= 1024 for p in glob.glob(os.path.join(part_dir, "*.md")))
        first_count = len(glob.glob(os.path.join(part_dir, "*.md")))
        assert process(path, 512) > first_count
        rebuilt = "".join(
            open(p, encoding="utf-8").read().split(MARKER, 1)[1]
            for p in sorted(glob.glob(os.path.join(part_dir, "*.md")))
        )
        assert rebuilt == body
        assert all(os.path.getsize(p) <= 512 for p in glob.glob(os.path.join(part_dir, "*.md")))
        assert all(not open(p, "rb").read().endswith(b"\n\n") for p in glob.glob(os.path.join(part_dir, "*.md")))
    print("self-test ok")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("target", nargs="?")
    parser.add_argument("--limit", type=int, default=1024 * 1024)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    if not args.target:
        parser.error("target is required")
    files = [args.target] if args.target.endswith(".md") else glob.glob(
        os.path.join(args.target, "**", "*.md"), recursive=True
    )
    split = pages = 0
    for path in files:
        count = process(path, args.limit, args.force)
        if count:
            pages += 1
            split += count
            print(f"  {path}: {count} parts")
    print(f"대형 Markdown 분할: {pages}개 페이지 / {split}개 조각")


if __name__ == "__main__":
    main()
