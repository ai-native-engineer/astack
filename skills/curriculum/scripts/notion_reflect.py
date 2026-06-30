#!/usr/bin/env python3
"""리폼/재생성한 로컬 클립 .md를 기존 노션 페이지에 반영(이미지/북마크 유실 없이).

문제: `ntn pages update`는 본문 전체 교체라, 로컬 .md가 이미지를 로컬 경로(`![](rel/x.png)`)로
참조하면 그대로 올릴 때 노션 이미지가 유실된다(file:// attachment ref가 아니라서). 북마크 카드도 마찬가지.

해법(재업로드/재삽입 방식 - 로컬 .md+PNG가 입력 기준이라 노션 상태에 의존하지 않아 robust):
  1) 이미지/북마크 디렉티브를 strip한 텍스트로 `ntn pages update`(본문 전체 교체, properties는 보존).
  2) 로컬 PNG는 `ntn files create`로 업로드 -> image 블록을, 출처는 `[[bookmark: URL]]` 디렉티브를 bookmark 블록을
     `PATCH /v1/blocks/<anchor>/children` `position.after_block`으로 삽입.
     앵커 = 직전 '실텍스트'(역방향 탐색, 콜아웃/표/태그/펜스/디렉티브 건너뜀). 같은 앵커 공유 연속 자산은 체이닝(순서 보존).
  3) round-trip: 페이지를 다시 떠 image/bookmark 블록 수 == 로컬 수인지 확인.

자료 표기 규칙(authoring 3-3): 인라인 `[출처: URL]` 금지. 출처는 섹션 하단 `[[bookmark: URL]]` 디렉티브로 둔다
(convert_sources 류 변환으로 생성). 이미지는 `![alt](rel/path)`.

전제: NOTION_WORKSPACE_ID env 설정(워크스페이스). 페이지 properties(제목/속성)는 건드리지 않는다.
주의: child_page/database가 있는 페이지엔 쓰지 않는다(update가 본문을 지운다). 성숙/발행 페이지는 4-1 발산 게이트 먼저. 동시 ntn 다중 실행 금지(키체인 락).

usage: NOTION_WORKSPACE_ID=<ws> python3 notion_reflect.py --report <검수.md> <page_id> <local.md> [<page_id> <local.md> ...]
exit 0 = 모든 페이지 round-trip 일치, 비0 = 하나라도 불일치/앵커 실패.
"""
import argparse, subprocess, sys, json, os, re

EXT_CT = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
          ".gif": "image/gif", ".webp": "image/webp", ".svg": "image/svg+xml"}
IMG_RE = re.compile(r'!\[.*?\]\(([^)]+\.(?:png|jpe?g|gif|webp|svg))\)', re.I)
BM_RE = re.compile(r'^\[\[bookmark:\s*(\S+?)\s*\]\]\s*$', re.I)
RECURSE = ("toggle", "heading_1", "heading_2", "heading_3", "bulleted_list_item",
           "numbered_list_item", "to_do", "callout")


def ntn(args, text_stdin=None, bin_stdin=None, timeout=180):
    env = dict(os.environ)  # NOTION_WORKSPACE_ID는 호출자가 설정
    if bin_stdin is not None:
        r = subprocess.run(["ntn"] + args, input=bin_stdin, capture_output=True, env=env, timeout=timeout)
        return r.stdout.decode("utf-8", "ignore"), r.stderr.decode("utf-8", "ignore")
    kw = dict(capture_output=True, text=True, env=env, timeout=timeout)
    if text_stdin is None:
        kw["stdin"] = subprocess.DEVNULL  # stdin EOF 대기 hang 방지(필수)
    else:
        kw["input"] = text_stdin
    r = subprocess.run(["ntn"] + args, **kw)
    return r.stdout, r.stderr


def api(path, method=None, body=None):
    args = ["api"] + (["--method", method] if method else []) + [path]
    out, err = ntn(args, text_stdin=body)
    try:
        return json.loads(out)
    except Exception:
        return {"_raw": out[:160], "_err": err[:160]}


def btext(b):
    t = b.get("type"); rt = b.get(t, {}).get("rich_text") or []
    return ''.join(x.get('plain_text', '') for x in rt) if isinstance(rt, list) else ''


def norm(s):
    return re.sub(r'[*_`#>\s]', '', s)


def flatten(pid):
    flat = []
    def walk(bid):
        for b in api(f"/v1/blocks/{bid}/children?page_size=100").get("results", []):
            flat.append((b["id"], btext(b), bid, b.get("type")))
            if b.get("has_children") and b["type"] in RECURSE:
                walk(b["id"])
    walk(pid)
    return flat


SKIP = re.compile(r'^(<!--|!\[|</|<\w+|\||```|\[\[bookmark:|---|\*\*\*|___)')  # 앵커 후보 제외 라인(구분선 포함)


def parse(mdpath):
    """본문(이미지/북마크 strip) + assets=[(kind, payload, anchor)] 반환. kind: image|bookmark."""
    raw = open(mdpath, encoding="utf-8").read()
    if raw.startswith("---"):  # frontmatter 제거(업로드 본문에 넣지 않음)
        raw = raw.split("---", 2)[2]
    lines = raw.split("\n")
    assets, body = [], []

    def anchor_for(i):
        for j in range(i - 1, -1, -1):
            s = lines[j].strip()
            if not s or SKIP.match(s):
                continue
            s = re.sub(r'[*_`>#]', '', s).strip()
            s = re.sub(r'^[-*•]\s+', '', s); s = re.sub(r'^\d+\.\s+', '', s)
            if s:
                return s
        return ""

    for i, l in enumerate(lines):
        mi = IMG_RE.search(l)
        mb = BM_RE.match(l.strip())
        if mi and not mi.group(1).startswith(("http://", "https://")):
            abspath = os.path.normpath(os.path.join(os.path.dirname(mdpath), mi.group(1)))
            assets.append(("image", abspath, anchor_for(i)))
        elif mb:
            assets.append(("bookmark", mb.group(1), anchor_for(i)))
        else:
            body.append(l)
    return "\n".join(body), assets


def asset_block(kind, payload):
    if kind == "image":
        ct = EXT_CT.get(os.path.splitext(payload)[1].lower(), "image/png")
        with open(payload, "rb") as fh:
            up, _ = ntn(["files", "create", "--filename", os.path.basename(payload), "--content-type", ct], bin_stdin=fh.read())
        upid = up.split("\t")[0].strip()
        if not re.match(r'^[0-9a-f]{8}-', upid):
            return None, f"업로드실패 {os.path.basename(payload)}: {up[:50]}"
        return {"object": "block", "type": "image",
                "image": {"type": "file_upload", "file_upload": {"id": upid}}}, None
    return {"object": "block", "type": "bookmark", "bookmark": {"url": payload}}, None


def reflect(page_id, mdpath, skip_gate=False, report=None, candidates=None):
    if not skip_gate:  # 검수 게이트: 리포트 + 고신호 0을 확인해 검수 루프를 강제
        import curriculum_gate as cg
        if not report:
            print(f"✗ {os.path.basename(mdpath)}: 검수 리포트 없음 - --report <검수.md> 필요(--skip-gate로만 우회)")
            return False
        rc = cg.cmd_gate_review(argparse.Namespace(report=report, draft=mdpath, candidates=candidates or []))
        if rc:
            print(f"✗ {os.path.basename(mdpath)}: gate-review 미통과, 반영 거부(--skip-gate로만 우회)")
            return False
    body, assets = parse(mdpath)
    n_img = sum(1 for k, _, _ in assets if k == "image")
    n_bm = sum(1 for k, _, _ in assets if k == "bookmark")
    out, err = ntn(["pages", "update", page_id], text_stdin=body)
    if err and "error" in err.lower() and "Updated" not in out:
        print(f"✗ {mdpath}: update 실패 {err[:140]}"); return False
    flat = flatten(page_id)
    used = set()
    prev_an, prev_block, prev_parent = None, None, None  # 같은 앵커 공유 연속 자산 체이닝
    ins_img, ins_bm = 0, 0
    for kind, payload, anchor in assets:
        if kind == "image" and not os.path.exists(payload):
            print(f"    ✗ 로컬 파일 없음: {payload}"); continue
        an = norm(anchor)[:22]
        if an and an == prev_an and prev_block:
            bid, parent = prev_block, prev_parent  # 직전 삽입 자산 뒤로 체이닝(순서 보존)
        else:
            match = next(((b, p) for b, txt, p, _ in flat
                          if b not in used and an and an in norm(txt)), None)
            if not match:
                print(f"    ✗ 앵커 못찾음: '{anchor[:26]}' ({kind}:{os.path.basename(str(payload))})"); continue
            bid, parent = match; used.add(bid)
        block, err2 = asset_block(kind, payload)
        if block is None:
            print(f"    ✗ {err2}"); continue
        ib = json.dumps({"children": [block], "position": {"type": "after_block", "after_block": {"id": bid}}})
        res = api(f"/v1/blocks/{parent}/children", method="PATCH", body=ib)
        new_blocks = res.get("results") if isinstance(res.get("results"), list) else None
        if new_blocks:
            if kind == "image": ins_img += 1
            else: ins_bm += 1
            prev_an, prev_block, prev_parent = an, new_blocks[0]["id"], parent
        else:
            print(f"    ✗ 삽입실패 {kind}:{os.path.basename(str(payload))}: {str(res)[:90]}")
    rt = flatten(page_id)
    rt_img = sum(1 for _, _, _, t in rt if t == "image")
    rt_bm = sum(1 for _, _, _, t in rt if t == "bookmark")
    ok = (ins_img == n_img == rt_img) and (ins_bm == n_bm == rt_bm)
    print(f"{'OK ' if ok else '⚠ '} {os.path.basename(mdpath)}: 이미지 {n_img}/{ins_img}/{rt_img} 북마크 {n_bm}/{ins_bm}/{rt_bm}  page={page_id}")
    return ok


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--candidates", action="append", help="curriculum-candidates-*.md. 1개면 전체 pair에 공통 적용, pair 수만큼 반복하면 순서대로 적용")
    ap.add_argument("--report", action="append", help="검수 리포트 .md. 1개면 전체 pair에 공통 적용, pair 수만큼 반복하면 순서대로 적용")
    ap.add_argument("--skip-gate", action="store_true", help="검수 리포트/gate-review를 의도적으로 우회")
    ap.add_argument("pairs", nargs="+", help="<page_id> <local.md> 반복")
    ns = ap.parse_args()
    if len(ns.pairs) < 2 or len(ns.pairs) % 2 != 0:
        print(__doc__); sys.exit(2)
    pairs = list(zip(ns.pairs[0::2], ns.pairs[1::2]))
    reports = ns.report or []
    candidate_files = ns.candidates or []
    if not ns.skip_gate and len(reports) not in (1, len(pairs)):
        print("✗ --report 필요: 1개(전체 공통) 또는 page/md pair 수만큼 지정. 의도적 우회는 --skip-gate.", file=sys.stderr)
        sys.exit(2)
    if not ns.skip_gate and candidate_files and len(candidate_files) not in (1, len(pairs)):
        print("✗ --candidates는 1개(전체 공통) 또는 page/md pair 수만큼 지정.", file=sys.stderr)
        sys.exit(2)
    if not os.environ.get("NOTION_WORKSPACE_ID"):
        print("✗ NOTION_WORKSPACE_ID env 필요"); sys.exit(2)
    results = []
    for i, (pid, md) in enumerate(pairs):
        report = None if ns.skip_gate else (reports[0] if len(reports) == 1 else reports[i])
        candidates = [] if ns.skip_gate or not candidate_files else [candidate_files[0] if len(candidate_files) == 1 else candidate_files[i]]
        results.append((md, reflect(pid, md, skip_gate=ns.skip_gate, report=report, candidates=candidates)))
    bad = [md for md, ok in results if not ok]
    print(f"\n=== 완료 {len(results) - len(bad)}/{len(results)} ===")
    for md in bad:
        print(f"  재시도 필요: {md}")
    sys.exit(1 if bad else 0)
