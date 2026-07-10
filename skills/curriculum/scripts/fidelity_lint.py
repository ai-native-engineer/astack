#!/usr/bin/env python3
"""교안 내용 블록이 선언한 기존 자료에서 왔는지 보수적으로 검사한다.

usage: python3 fidelity_lint.py --target <draft.md> --source <source.md> [--source ...]
exit 0 = net-new 블록 비율과 표가 허용 범위, exit 1 = 위반, exit 2 = 입력 오류.
"""
import argparse
import os
import re
import sys


COVERAGE_MIN = 0.5
NET_NEW_MAX = 0.35
TOKEN = re.compile(r"[가-힣a-z0-9]+")


def normalized(text):
    return "".join(TOKEN.findall(text.lower()))


def trigrams(text):
    return {text[i:i + 3] for i in range(len(text) - 2)} if len(text) >= 3 else set()


def blocks(markdown):
    """Markdown을 fidelity 판정용 (kind, text) 블록으로 나눈다."""
    lines = markdown.splitlines()
    result = []
    index = 0
    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if not stripped:
            index += 1
            continue
        if stripped.startswith("```"):
            group = [line]
            index += 1
            while index < len(lines) and not lines[index].strip().startswith("```"):
                group.append(lines[index])
                index += 1
            if index < len(lines):
                group.append(lines[index])
                index += 1
            result.append(("code", "\n".join(group)))
            continue
        if stripped.startswith("<callout") or stripped.startswith("<table"):
            kind = "callout" if stripped.startswith("<callout") else "table"
            closing = f"</{kind}>"
            group = [line]
            while closing not in group[-1] and index + 1 < len(lines):
                index += 1
                group.append(lines[index])
            index += 1
            result.append((kind, re.sub(r"<[^>]+>", " ", "\n".join(group))))
            continue
        if stripped.startswith("#"):
            result.append(("heading", stripped.lstrip("# ")))
            index += 1
            continue
        if stripped.startswith(("![", "[[bookmark:", "<unknown")):
            index += 1
            continue
        group = [line]
        index += 1
        while index < len(lines):
            following = lines[index].strip()
            if not following or following.startswith(("#", "```", "<callout", "<table", "![", "[[bookmark:", "<unknown")):
                break
            group.append(lines[index])
            index += 1
        result.append(("paragraph", "\n".join(group)))
    return result


def lint(target, sources):
    source_trigrams = set()
    for source in sources:
        source_trigrams |= trigrams(normalized(source))

    checked = []
    net_new = []
    def evaluate(kind, text):
        grams = trigrams(normalized(text))
        if not grams:
            return
        coverage = len(grams & source_trigrams) / len(grams)
        checked.append((kind, coverage, text))
        if coverage < COVERAGE_MIN:
            net_new.append((kind, round(coverage, 2), text.strip().replace("\n", " ")[:70]))

    in_objectives = False
    for kind, text in blocks(target):
        if kind == "heading":
            in_objectives = "학습 목표" in text or "학습목표" in text
            continue
        if in_objectives:
            continue
        evaluate(kind, text)

    ratio = len(net_new) / len(checked) if checked else 0.0
    new_table = any(kind == "table" for kind, _, _ in net_new)
    no_checkable = not checked
    return {
        "ok": not no_checkable and ratio <= NET_NEW_MAX and not new_table,
        "checked": len(checked),
        "net_new": len(net_new),
        "ratio": round(ratio, 2),
        "new_table": new_table,
        "no_checkable": no_checkable,
        "violations": net_new,
    }


def read(path):
    try:
        with open(path, encoding="utf-8") as file:
            return file.read()
    except (OSError, UnicodeDecodeError) as error:
        raise ValueError(f"입력 읽기 실패: {path}: {error}") from error


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--target", required=True)
    parser.add_argument("--source", action="append", required=True)
    args = parser.parse_args(argv)
    if any(os.path.realpath(path) == os.path.realpath(args.target) for path in args.source):
        print("target 자신을 source로 선언할 수 없습니다.", file=sys.stderr)
        return 2
    try:
        result = lint(read(args.target), [read(path) for path in args.source])
    except ValueError as error:
        print(error, file=sys.stderr)
        return 2

    verdict = "PASS" if result["ok"] else "FAIL"
    print(f"FIDELITY {verdict}: net-new {result['net_new']}/{result['checked']} 블록 "
          f"(비율 {result['ratio']}, 한도 {NET_NEW_MAX})"
          f"{' + net-new 표' if result['new_table'] else ''}"
          f"{' + 판정 가능한 본문 없음' if result['no_checkable'] else ''}")
    for kind, coverage, preview in result["violations"]:
        print(f"  net-new[{kind} cov={coverage}] {preview}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
