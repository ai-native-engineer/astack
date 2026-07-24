#!/usr/bin/env python3
"""context/ 소스 아카이브 현황 뷰어.

각 .md의 YAML frontmatter(없으면 파일명·본문 헤더에서 best-effort)를 읽어
소스별 수집 현황을 표로 출력한다. --source 로 특정 소스의 anchor(증분 기준점)만 조회.
표준 라이브러리만 사용 (의존성 0).

  python3 context_status.py [dir]                     # 현황 표
  python3 context_status.py --resolve-dir --root DIR  # 프로젝트의 출력 경로
  python3 context_status.py [dir] --source slack      # slack anchor만 출력
"""
import argparse
import contextlib
import glob
import io
import os
import re
import sys
import tempfile


def parse_frontmatter(text):
    """맨 위 --- ~ --- 블록을 flat key:value dict로. 없으면 None."""
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    meta = {}
    for line in text[3:end].splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        k, v = line.split(":", 1)
        meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta


def fallback_meta(text, path):
    """frontmatter 없는 기존 아카이브: 파일명·본문 헤더에서 best-effort."""
    meta = {"_nometa": "1"}
    base = os.path.basename(path)
    m = re.match(r"\d{6}-([0-9a-zA-Z가-힣]+)-", base)
    if m:
        meta["source"] = m.group(1)
    mc = re.search(r"수집일[:：]\s*([0-9]{4}-[0-9]{2}-[0-9]{2})", text)
    if mc:
        meta["collected_last"] = mc.group(1)
    mf = re.search(r"초수집[:：]\s*([0-9]{4}-[0-9]{2}-[0-9]{2})", text)
    meta["collected_first"] = mf.group(1) if mf else meta.get("collected_last", "")
    mr = re.search(
        r"범위[:：]\s*([0-9]{4}-[0-9]{2}-[0-9]{2})\s*~\s*([0-9]{4}-[0-9]{2}-[0-9]{2})", text
    )
    if mr:
        meta["range_start"], meta["range_end"] = mr.group(1), mr.group(2)
    return meta


def load(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    meta = parse_frontmatter(text)
    if meta is None:
        meta = fallback_meta(text, path)
    meta.setdefault("source", "?")
    meta["_file"] = os.path.basename(path)
    return meta


def resolve_context_dir(root):
    """프로젝트 root에서 유일한 context 출력 디렉터리를 절대 경로로 반환한다."""
    root = os.path.realpath(os.path.abspath(root))
    if os.path.isdir(os.path.join(root, ".obsidian")):
        raise ValueError(
            f"OBSIDIAN_VAULT context archive disabled: {root}; "
            "use the vault ingest workflow"
        )
    current = os.path.join(root, "01-context", "company")
    legacy = os.path.join(root, "context")
    current_exists = os.path.isdir(current)
    legacy_exists = os.path.isdir(legacy)
    if current_exists and legacy_exists:
        raise ValueError(f"CONFLICT both context directories exist: {current} and {legacy}")
    if legacy_exists:
        return legacy
    return current


def self_check_resolver():
    with tempfile.TemporaryDirectory() as tmp:
        root = os.path.join(tmp, "explicit root")
        os.makedirs(root)
        root = os.path.realpath(root)
        current = os.path.join(root, "01-context", "company")
        legacy = os.path.join(root, "context")

        assert resolve_context_dir(root) == current  # neither: new default
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = main(["--resolve-dir", "--root", root])
        assert result == 0 and output.getvalue().strip() == current

        os.makedirs(current)
        assert resolve_context_dir(root) == current  # new only
        os.rmdir(current)
        os.rmdir(os.path.dirname(current))

        os.makedirs(legacy)
        assert resolve_context_dir(root) == legacy  # legacy only

        os.makedirs(current)
        try:
            resolve_context_dir(root)
        except ValueError as exc:
            assert str(exc).startswith("CONFLICT "), exc
        else:
            raise AssertionError("both context directories must conflict")
        errors = io.StringIO()
        with contextlib.redirect_stderr(errors):
            result = main(["--resolve-dir", "--root", root])
        assert result != 0 and errors.getvalue().startswith("CONFLICT ")

        os.rmdir(current)
        os.rmdir(os.path.dirname(current))
        os.rmdir(legacy)
        assert resolve_context_dir(root).startswith(os.path.realpath(root) + os.sep)

        os.makedirs(current)
        errors = io.StringIO()
        with contextlib.redirect_stderr(errors):
            result = main(["--root", root])
        assert result == 1 and errors.getvalue().startswith("(no .md in ")

        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = main(["--root", root, "--source", "slack"])
        assert result == 0 and output.getvalue() == "\n", (result, output.getvalue())

        obsidian_root = os.path.join(tmp, "obsidian vault")
        os.makedirs(os.path.join(obsidian_root, ".obsidian"))
        try:
            resolve_context_dir(obsidian_root)
        except ValueError as exc:
            assert str(exc).startswith("OBSIDIAN_VAULT "), exc
        else:
            raise AssertionError("Obsidian vaults must not resolve an internal context directory")
        errors = io.StringIO()
        with contextlib.redirect_stderr(errors):
            result = main(["--resolve-dir", "--root", obsidian_root])
        assert result != 0 and errors.getvalue().startswith("OBSIDIAN_VAULT ")

    print("ok")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="context/ 아카이브 수집 현황 뷰어")
    ap.add_argument("dir", nargs="?", default=None,
                    help="아카이브 폴더 (생략하면 프로젝트 root에서 해소)")
    ap.add_argument("--root", default=".", help="프로젝트 root (기본: 현재 디렉터리)")
    ap.add_argument("--resolve-dir", action="store_true",
                    help="선택한 아카이브 폴더의 절대 경로만 출력")
    ap.add_argument("--self-check-resolver", action="store_true",
                    help="임시 디렉터리에서 resolver 계약을 검사")
    ap.add_argument("--source", help="이 소스의 anchor(증분 기준점)만 출력")
    args = ap.parse_args(argv)

    if args.self_check_resolver:
        return self_check_resolver()

    try:
        if args.dir is None:
            archive_dir = resolve_context_dir(args.root)
        else:
            archive_dir = args.dir
            if not os.path.isabs(archive_dir):
                archive_dir = os.path.join(args.root, archive_dir)
            archive_dir = os.path.realpath(os.path.abspath(archive_dir))
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 2

    if args.resolve_dir:
        print(archive_dir)
        return 0

    files = sorted(glob.glob(os.path.join(archive_dir, "*.md")))
    if not files:
        if args.source:
            print("")
            return 0
        print(f"(no .md in {archive_dir})", file=sys.stderr)
        return 1
    rows = [load(f) for f in files]

    # --source: 해당 소스의 anchor만 (가장 최근 수집본 기준). 재수집 증분에 사용.
    if args.source:
        cand = [r for r in rows if r.get("source") == args.source and r.get("anchor")]
        cand.sort(key=lambda r: r.get("collected_last", ""), reverse=True)
        print(cand[0]["anchor"] if cand else "")
        return 0

    for r in rows:
        rs, re_ = r.get("range_start", ""), r.get("range_end", "")
        r["_range"] = f"{rs} ~ {re_}" if (rs or re_) else ""

    cols = [
        ("SOURCE", "source", 10),
        ("FIRST", "collected_first", 11),
        ("LAST", "collected_last", 11),
        ("RANGE", "_range", 25),
        ("ITEMS", "items", 6),
        ("ANCHOR", "anchor", 22),
        ("FILE", "_file", 40),
    ]
    hdr = " ".join(name.ljust(w) for name, _, w in cols)
    print(hdr)
    print("-" * len(hdr))
    for r in sorted(rows, key=lambda r: (r.get("source", ""), r.get("_file", ""))):
        flag = "*" if r.get("_nometa") else " "
        line = " ".join(str(r.get(key, "") or "").ljust(w)[:w] for _, key, w in cols)
        print(flag + line)
    if any(r.get("_nometa") for r in rows):
        print("\n* = frontmatter 없음 (본문 best-effort). 다음 머지 때 frontmatter가 얹힘.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
