#!/usr/bin/env python3
"""curriculum scripts self-check.

실행 목적: 게이트 스크립트의 핵심 실패 모드가 회귀하지 않았는지 확인한다.
"""
import contextlib
import io
import os
import subprocess
import sys
import tempfile
from types import SimpleNamespace

import curriculum_gate as gate
import fidelity_lint
import notion_reflect as reflect_gate

ROOT = os.path.dirname(__file__)
GATE = os.path.join(ROOT, "curriculum_gate.py")
FORMAT = os.path.join(ROOT, "format_scan.py")
FIDELITY = os.path.join(ROOT, "fidelity_lint.py")
REFLECT = os.path.join(ROOT, "notion_reflect.py")


def write(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def run(*args):
    return subprocess.run([sys.executable, *args], text=True, capture_output=True)


def expect(label, rc, *args):
    p = run(*args)
    if p.returncode != rc:
        print(f"FAIL {label}: expected rc={rc}, got {p.returncode}")
        print((p.stdout + p.stderr)[-1200:])
        return False
    print(f"OK {label}")
    return True


def check(label, condition, detail=""):
    if not condition:
        print(f"FAIL {label}: {detail}")
        return False
    print(f"OK {label}")
    return True


def expect_output(label, rc, args, includes=(), excludes=()):
    p = run(*args)
    output = p.stdout + p.stderr
    ok = p.returncode == rc and all(s in output for s in includes) and all(s not in output for s in excludes)
    if not ok:
        print(f"FAIL {label}: expected rc={rc}, got {p.returncode}")
        print(output[-1200:])
        return False
    print(f"OK {label}")
    return True


def main():
    ok = True
    with tempfile.TemporaryDirectory() as td:
        empty = os.path.join(td, "empty.md")
        orig = os.path.join(td, "orig.md")
        prod_missing = os.path.join(td, "prod-missing.md")
        prod_ok = os.path.join(td, "prod-ok.md")
        bad = os.path.join(td, "bad.md")
        good = os.path.join(td, "good.md")
        other_dir = os.path.join(td, "other")
        other_good = os.path.join(other_dir, "good.md")
        format_bad = os.path.join(td, "format-bad.md")
        reflect_image = os.path.join(td, "reflect-image.md")
        unsupported_image = os.path.join(td, "unsupported-image.md")
        unsupported_reference = os.path.join(td, "unsupported-reference.md")
        reflect_asset = os.path.join(td, "asset.png")
        report = os.path.join(td, "report.md")
        format_report = os.path.join(td, "format-report.md")
        cand_unchecked = os.path.join(td, "curriculum-candidates-unchecked.md")
        cand_blank = os.path.join(td, "curriculum-candidates-blank.md")
        cand_ok = os.path.join(td, "curriculum-candidates-ok.md")
        explore_out = os.path.join(td, "curriculum-candidates-invalid-notion.md")
        local_error_out = os.path.join(td, "curriculum-candidates-invalid-local.md")
        partial_notion = os.path.join(td, "partial-notion.json")
        list_notion = os.path.join(td, "list-notion.json")
        malformed_notion = os.path.join(td, "malformed-notion.json")
        partial_notion_out = os.path.join(td, "curriculum-candidates-partial-notion.md")
        status_ws = os.path.join(td, "workspace")
        status_archives = os.path.join(status_ws, "archives")
        os.makedirs(status_archives)
        os.makedirs(other_dir)

        write(empty, "# text only\n")
        write(orig, "![a](file:///asset/a.png)\n")
        write(prod_missing, "# output\n")
        write(prod_ok, "![a](file:///asset/a.png)\n")
        write(bad, "# 1. 결과 화면\n설명만 있습니다.\n")
        write(good, "# 1. 실습\n아래 프롬프트를 복사합니다.\n\n```text\nhello\n```\n")
        write(other_good, "# 1. 실습\n아래 프롬프트를 복사합니다.\n\n```text\ndifferent\n```\n")
        write(format_bad, "# 1. 실습\n설명입니다.\n- 단계 하나\n")
        write(reflect_image, '# 1. 충분히 긴 결과 화면\n![결과](<asset.png?raw=1> "제목")\n')
        write(unsupported_image, '# 1. 결과\n<img src="asset.png">\n')
        write(unsupported_reference, '# 1. 결과\n![asset]\n\n[asset]: asset.png\n')
        write(partial_notion, '{"results":[{"object":"page","id":"00000000-0000-0000-0000-000000000001","properties":{}}],"has_more":true,"next_cursor":"next"}')
        write(list_notion, '[{"object":"page","id":"00000000-0000-0000-0000-000000000001","properties":{}}]')
        write(malformed_notion, '{"results":[{},{},{},{},{},{},{},{},{},{}],"has_more":false,"next_cursor":null}')
        write(reflect_asset, "not-a-real-png-but-readable")
        write(cand_unchecked, "# Curriculum 딥 탐색 후보\n\n> 게이트 상태: **OK**\n\n- [ ] 원본 A - id `a` | 근거: \n\n최선 후보: 원본 A\n")
        write(cand_blank, "# Curriculum 딥 탐색 후보\n\n> 게이트 상태: **OK**\n\n- [x] 원본 A - id `a` | 근거: \n\n최선 후보: 원본 A\n")
        candidate_ok = "# Curriculum 딥 탐색 후보\n\n> 게이트 상태: **OK**\n\n- [x] 원본 A - id `a` | 근거: 프롬프트 3개와 결과 이미지 확인\n\n최선 후보: 원본 A\n"
        write(cand_ok, candidate_ok)
        candidate_digest = gate._sha256_file(cand_ok)
        write(report, f"# 검수\n\n교안: `{os.path.basename(good)}`\n후보: `{os.path.basename(cand_ok)}`\n"
              f"교안 SHA256: {gate._sha256_file(good)}\n후보 SHA256: {os.path.basename(cand_ok)}={candidate_digest}\n\n"
              "review-draft before -> after: 고신호 1 -> 0\n")
        write(format_report, f"# 검수\n\n교안: `{os.path.basename(format_bad)}`\n후보: `{os.path.basename(cand_ok)}`\n"
              f"교안 SHA256: {gate._sha256_file(format_bad)}\n후보 SHA256: {os.path.basename(cand_ok)}={candidate_digest}\n\n"
              "review-draft before -> after: 고신호 1 -> 0\n")
        write(os.path.join(status_ws, "curriculum-candidates-active.md"), candidate_ok)
        write(os.path.join(status_archives, "검수-ARCHIVED-ONLY.md"), "# archived\n")

        ok &= expect_output("explore rejects invalid Notion JSON", 1,
                            [GATE, "explore", "--topic", "실습", "--no-db", "--notion-hits", bad,
                             "--local-root", td, "--min-candidates", "1", "--out", explore_out],
                            includes=("노션 검색 JSON 읽기/파싱/완전성 실패",))
        ok &= expect_output("explore rejects partial local search failure", 1,
                            [GATE, "explore", "--topic", "실습", "--no-db", "--no-notion",
                             "--local-root", td, "--local-root", os.path.join(td, "missing"),
                             "--min-candidates", "1", "--out", local_error_out],
                            includes=("로컬 교안 검색 실패",))
        ok &= expect_output("explore rejects partial Notion pagination", 1,
                            [GATE, "explore", "--topic", "실습", "--no-db", "--notion-hits", partial_notion,
                             "--local-root", td, "--min-candidates", "1", "--out", partial_notion_out],
                            includes=("노션 검색 JSON 읽기/파싱/완전성 실패", "페이지네이션 미완"))
        ok &= expect_output("explore rejects unmarked Notion result list", 1,
                            [GATE, "explore", "--topic", "실습", "--no-db", "--notion-hits", list_notion,
                             "--local-root", td, "--min-candidates", "1",
                             "--out", os.path.join(td, "curriculum-candidates-list-notion.md")],
                            includes=("raw search JSON 객체가 아님",))
        ok &= expect_output("explore rejects malformed Notion result items", 1,
                            [GATE, "explore", "--topic", "실습", "--no-db", "--notion-hits", malformed_notion,
                             "--local-root", td, "--min-candidates", "1",
                             "--out", os.path.join(td, "curriculum-candidates-malformed-notion.md")],
                            includes=("유효한 page id",))
        original_run_ntn = gate.run_ntn
        db_calls = iter([
            (0, '{"results":[{"id":"00000000-0000-0000-0000-000000000001","properties":{}}],"has_more":true,"next_cursor":"next"}', ""),
            (1, "", "second page failed"),
        ])
        gate.run_ntn = lambda *_args, **_kwargs: next(db_calls)
        try:
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                partial_db_rc = gate.cmd_explore(SimpleNamespace(
                    workspace_id="test", datasource="fake", limit=1, no_db=False,
                    topic="실습", local_root=[td], notion_hits=None, no_notion=True,
                    min_candidates=1, out=os.path.join(td, "curriculum-candidates-partial-db.md"),
                ))
        finally:
            gate.run_ntn = original_run_ntn
        ok &= check("explore rejects DB failure after a successful page", partial_db_rc == 1)
        gate.run_ntn = lambda *_args, **_kwargs: (
            0, '[{"id":"00000000-0000-0000-0000-000000000001","properties":{}}]', "")
        try:
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                list_db_rc = gate.cmd_explore(SimpleNamespace(
                    workspace_id="test", datasource="fake", limit=1, no_db=False,
                    topic="실습", local_root=[td], notion_hits=None, no_notion=True,
                    min_candidates=1, out=os.path.join(td, "curriculum-candidates-list-db.md"),
                ))
        finally:
            gate.run_ntn = original_run_ntn
        ok &= check("explore rejects DB result without completeness marker", list_db_rc == 1)
        ok &= expect("verify-media rejects zero-media source", 1, GATE, "verify-media", empty, empty)
        ok &= expect("verify-media catches missing ref", 1, GATE, "verify-media", orig, prod_missing)
        ok &= expect("verify-media accepts preserved ref", 0, GATE, "verify-media", orig, prod_ok)
        ok &= expect("gate-candidates rejects unchecked source", 1, GATE, "gate-candidates", cand_unchecked)
        ok &= expect("gate-candidates rejects blank evidence", 1, GATE, "gate-candidates", cand_blank)
        ok &= expect("gate-candidates accepts checked evidence", 0, GATE, "gate-candidates", cand_ok)
        ok &= expect("review-draft catches weak draft", 1, GATE, "review-draft", bad)
        ok &= expect("review-draft accepts signal draft", 0, GATE, "review-draft", good)
        ok &= expect("gate-review requires candidates", 2, GATE, "gate-review", "--report", report, good)
        ok &= expect("gate-review rejects report bound to another draft", 1, GATE, "gate-review",
                     "--candidates", cand_ok, "--report", format_report, good)
        ok &= expect("gate-review rejects same-name draft with another hash", 1, GATE, "gate-review",
                     "--candidates", cand_ok, "--report", report, other_good)
        ok &= expect_output("gate-review rejects format_scan violation", 1,
                            [GATE, "gate-review", "--candidates", cand_ok, "--report", format_report, format_bad],
                            includes=("format_scan", "줄글+불렛"))
        ok &= expect("gate-review accepts candidates plus report", 0, GATE, "gate-review", "--candidates", cand_ok, "--report", report, good)
        ok &= expect("format_scan requires input", 2, FORMAT)
        ok &= expect("format_scan help", 0, FORMAT, "--help")
        ok &= expect_output("status is visibility-only and excludes archives", 0, [GATE, "status", status_ws],
                            includes=("가시성 전용",), excludes=("ARCHIVED-ONLY",))
        ok &= check("verify-pages maps 401 to invalid token", gate._page_state(401, None).startswith("UNAUTHORIZED"))
        ok &= check("verify-pages maps 403 to permission/capability", gate._page_state(403, None).startswith("FORBIDDEN"))
        ok &= check("verify-pages keeps 404 ambiguous", gate._page_state(404, None).startswith("MISSING-OR-UNSHARED"))
        image_forms = ("![a](asset.png?raw=1)", "![a](<asset.png>)", '![a](asset.png "title")')
        ok &= check("notion_reflect recognizes Markdown image variants",
                    all(len(reflect_gate.image_refs(form)) == 1 for form in image_forms))
        unsupported_image_rejected = True
        for path in (unsupported_image, unsupported_reference):
            try:
                reflect_gate.parse(path)
                unsupported_image_rejected = False
            except reflect_gate.SafetyError:
                pass
        ok &= check("notion_reflect rejects unsupported image syntax", unsupported_image_rejected)
        ok &= check("notion_reflect rejects Notion self-anchor bookmark",
                    reflect_gate.is_blocked_bookmark("https://app.notion.com/p/page#block"))
        try:
            reflect_gate.validate_content_roundtrip("# 본문\n반영해야 할 핵심 문장입니다.", "")
            missing_body_rejected = False
        except reflect_gate.SafetyError:
            missing_body_rejected = True
        ok &= check("notion_reflect rejects missing body on round-trip", missing_body_rejected)
        try:
            reflect_gate.validate_content_roundtrip(
                "# 본문\n승인한 핵심 문장입니다.",
                "# 본문\n승인한 핵심 문장입니다.\n\n승인하지 않은 추가 문장입니다.",
            )
            extra_body_rejected = False
        except reflect_gate.SafetyError:
            extra_body_rejected = True
        ok &= check("notion_reflect rejects unapproved extra body", extra_body_rejected)
        lost_structure_rejected = True
        for expected, flattened in (
            ("# 본문\n```python\nprint(1)\n```", "본문 python print(1)"),
            ("# 본문\n- [ ] 확인", "본문 확인"),
            ("# A\n## B", "## A\n# B"),
            ("- 첫째\n둘째", "첫째\n- 둘째"),
            ("<callout>A</callout>\nB", "A\n<callout>B</callout>"),
            ("<summary>A</summary>\nB", "A\n<summary>B</summary>"),
        ):
            try:
                reflect_gate.validate_content_roundtrip(expected, flattened)
                lost_structure_rejected = False
            except reflect_gate.SafetyError:
                pass
        ok &= check("notion_reflect rejects lost Markdown structure", lost_structure_rejected)
        image_change_rejected = True
        for actual in (
            "# A\n![결과](https://example.com/other.png)\n# B",
            "# A\n# B\n![결과](https://example.com/result.png)",
        ):
            try:
                reflect_gate.validate_content_roundtrip(
                    "# A\n![결과](https://example.com/result.png)\n# B", actual)
                image_change_rejected = False
            except reflect_gate.SafetyError:
                pass
        ok &= check("notion_reflect rejects changed or moved image", image_change_rejected)
        attachment_loss_rejected = True
        for tag in ("video", "file"):
            try:
                reflect_gate.validate_content_roundtrip(
                    f'# 본문\n설명\n<{tag} src="file://asset"></{tag}>',
                    "# 본문\n설명",
                )
                attachment_loss_rejected = False
            except reflect_gate.SafetyError:
                pass
        ok &= check("notion_reflect rejects lost file or video attachment", attachment_loss_rejected)
        fidelity_result = fidelity_lint.lint(
            "# 본문\n일반적인 바이브 코딩 흐름이라는 과거 예외 문구가 있어도 새로운 내용을 통과시키지 않습니다.",
            ["검증 원본에는 전혀 다른 기존 설명만 들어 있습니다."],
        )
        ok &= check("fidelity lint has no project-specific marker bypass", not fidelity_result["ok"])
        short_sections = "\n".join(f"# {index}\n새 내용 {index}" for index in range(20))
        short_result = fidelity_lint.lint(short_sections, ["무관한 검증 원본입니다."])
        ok &= check("fidelity lint rejects short net-new blocks", not short_result["ok"])
        mixed_short = fidelity_lint.lint(
            "원본하나\n\n원본둘\n\n원본셋\n\n새내용갑\n\n새내용을",
            ["원본하나 원본둘 원본셋 원본넷 원본다섯"],
        )
        ok &= check("fidelity lint keeps per-block short coverage", not mixed_short["ok"])
        ok &= expect("fidelity lint rejects target as its own source", 2, FIDELITY,
                     "--target", good, "--source", good)
        ok &= expect("notion_reflect help", 0, REFLECT, "--help")
        ok &= expect("notion_reflect requires report before env/ntn", 2, REFLECT, "page-id", good)
        no_ntn_env = dict(os.environ, NOTION_WORKSPACE_ID="test-workspace", PATH="")
        reflected = subprocess.run(
            [sys.executable, REFLECT, "--candidates", cand_ok, "--report", report,
             "--expected-title", "테스트", "--expected-parent-id", "workspace",
             "--expected-last-edited-time", "2026-01-01T00:00:00.000Z",
             "00000000-0000-0000-0000-000000000000", reflect_image],
            text=True, capture_output=True, env=no_ntn_env,
        )
        output = reflected.stdout + reflected.stderr
        ok &= check("notion_reflect blocks local images before ntn", reflected.returncode == 1
                    and "로컬 이미지 반영 차단" in output and "NO WRITE" in output,
                    output[-1200:])

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
