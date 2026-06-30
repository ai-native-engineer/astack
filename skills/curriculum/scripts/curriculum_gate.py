#!/usr/bin/env python3
"""curriculum 게이트 - 산문 지시로 자꾸 건너뛰는 결정론적 단계를 산출물/exit-code로 강제.

일곱 서브커맨드 (각각 review.md / authoring.md 3-0절이 hard gate로 참조):
  explore       딥 탐색: 강의 모듈 DB + 강의자료 워크스페이스/조직 노션 전수 + 로컬 교안을 전수로 모아 후보 목록 산출물 생성.
                모듈 DB는 아직 빈약하므로 항상 강의자료 워크스페이스/조직 노션 전수(워크스페이스별 `ntn api /search`)도 함께 본다.
                참고 자료 최신순 10개 미만/DB 미탐색/노션 미탐색이면 비0 종료, 이 산출물 없이 제작/검수 시작 금지(#3 딥 탐색 건너뜀 처방).
  gate-candidates 후보 검토 게이트: explore 산출물의 [x] 후보, 근거, 최선 후보 1개를 확인한다.
                "검색 파일만 만들고 실제 원문은 안 봄"을 막는다.
  verify-pages  page-id 실존 확인: 직접 Notion REST(신뢰 채널)로 확인, 추측/환각 금지.
                404(환각)와 401/403(integration 미공유)을 구분. 하나라도 미확인이면 비0 종료
                (고객사 A 신종: 없는 page-id 18곳 환각 + 미공유를 404로 오판 처방).
  verify-media  로컬 원본 작업본 vs 산출물 미디어 ref 대조. 원본에 있고 산출물에 없으면 비0 종료
                ("반영했다" 단정 후 이미지 누락 #7, transplant 누락 처방).
  review-draft  "초안 띡" smell 린터: 신호 없는 섹션(복붙/이미지/체크리스트 0)·이미지 없는 산출물 섹션·
                AI slop·안심말·빈펜스를 file:line으로 잡고 고신호면 비0. 판단(페르소나 비평)은 review.md.
  gate-review   검수 산출물 게이트(Phase4 반영 전제): 검수 리포트 존재 + 교안 review-draft 고신호 0이어야 exit 0.
                explore가 제작 시작을 게이트하듯, 이건 반영을 게이트한다(검수 생략/약점표만 내고 끝 방지).
  status        워크스페이스 단계 현황(게이트 아님, 조회용): explore 산출물/검수 리포트 존재 + 교안 고신호로
                어느 Phase까지 통과했고 다음 필수 게이트가 무엇인지 판정. 단계 전환을 산문 추론 대신 기계 판정.

게이트 통과 = exit 0. 모델은 응답에 (실행 명령 + exit code + 핵심 출력 라인)을 인용해야 한다 - 증거 없이 통과 단정 금지.
explore의 ntn은 hang/0바이트 실측이 있어(notion-sync.md) timeout. 백그라운드 금지.
verify-pages는 ntn 크로스오염(notion-sync 4-0절)을 피해 직접 REST를 쓴다 - 환각 차단 게이트가
오염 가능한 채널을 쓰면 거짓 통과한다.
"""
import argparse, glob, json, os, re, subprocess, sys, time, urllib.error, urllib.request

NOTION_VERSION = "2022-06-28"  # page/block read 호환되는 안정 API 버전
CHECKED_CANDIDATE = re.compile(r"^\s*-\s*\[[xX]\]\s*(.+)")
EVIDENCE = re.compile(r"근거\s*[:：]\s*(.*)")
BEST_SOURCE = re.compile(r"^\s*(?:최선 후보|최선 선택|선택 후보)\s*[:：]\s*(.+\S)\s*$")


def run_ntn(args, workspace_id=None, timeout=90):
    """ntn 호출. (rc, stdout, stderr). timeout이면 rc=124. solve-don't-punt: 멈추지 말고 신호 반환."""
    env = dict(os.environ)
    if workspace_id:
        env["NOTION_WORKSPACE_ID"] = workspace_id
    try:
        p = subprocess.run(["ntn", *args], capture_output=True, text=True,
                           timeout=timeout, env=env)
        return p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired:
        return 124, "", f"ntn timeout {timeout}s (hang 의심 - 직접 API 폴백 notion-sync 4-0절)"
    except FileNotFoundError:
        return 127, "", "ntn 미설치/PATH 없음"


def notion_get(path, token, timeout=30):
    """Notion REST GET. (status, json|None). 신뢰 채널 - notion-sync 4-0절 ntn 크로스오염 우회."""
    req = urllib.request.Request(
        "https://api.notion.com/v1" + path,
        headers={"Authorization": "Bearer " + token, "Notion-Version": NOTION_VERSION},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, None  # 404 환각 / 401·403 미공유를 호출부가 구분
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return 0, None


def _title_of(page):
    """Notion 페이지 객체에서 title 추출. 어느 DB든 type=='title'인 property를 찾는다."""
    for prop in (page.get("properties") or {}).values():
        if prop.get("type") == "title":
            return "".join(t.get("plain_text", "") for t in prop.get("title", [])) or "(제목없음)"
    if isinstance(page.get("title"), list):  # 검색 결과의 database 객체는 top-level title
        return "".join(t.get("plain_text", "") for t in page["title"]) or "(제목없음)"
    return "(제목없음)"


def _edited_ts(page):
    """Notion 객체의 최신성 정렬 키. last_edited_time(없으면 created_time)의 ISO 문자열.
    검색/DB 결과 모두 top-level에 ISO8601(예 2026-06-29T01:23:00.000Z)을 준다. 비면 ''(맨 뒤)."""
    return page.get("last_edited_time") or page.get("created_time") or ""


def _date_label(iso):
    """ISO8601 -> YYYY-MM-DD(앞 10자), 비면 '날짜미상'. 후보 줄 앞 수정일 표기용."""
    return iso[:10] if iso else "날짜미상"


# 미디어 ref 패턴. 마크다운 ![](), <img>, <file>, <video>, file://·attachment 까지 잡는다.
# (이전 버전은 file://·attachment·<file>·<video>만 잡아 가장 흔한 ![](...)를 놓쳐 빈 set->거짓 '누락 0'을 냈다.)
MEDIA_PATTERNS = [
    re.compile(r"!\[[^\n]*?\]\(\s*(?:<([^>]+)>|([^)\s]+))"),                 # ![](url) 또는 ![](<url 공백 허용>)
    re.compile(r"<(?:img|source|file|video)[^>]*\bsrc\s*=\s*[\"']([^\"']+)"),  # <img>/<source>/<file>/<video> src(따옴표/공백 관대)
    re.compile(r"(?:file://|attachment:)[^\s)\]\}\"'>,;]+"),                 # bare file:// / attachment:
]


def _norm_media_key(raw):
    """비교 키 정규화: query suffix(?X-Amz·&cache - get마다 토큰이 달라짐) 절단 + 종결 문장부호 제거."""
    return re.split(r"[?&]", raw, maxsplit=1)[0].rstrip(",.;:)]}\"'")


def media_keys(text):
    keys = set()
    for pat in MEDIA_PATTERNS:
        for m in pat.finditer(text):
            raw = next((g for g in m.groups() if g), None) if m.groups() else m.group(0)  # 첫 매칭 그룹(angle/bare)
            if raw:
                keys.add(_norm_media_key(raw))
    return keys


def cmd_explore(a):
    ws = a.workspace_id
    db_lines, local_lines = [], []
    n_db = n_local = 0
    db_failed = truncated = False

    if a.datasource:
        cursor, got = None, []
        for _ in range(20):  # 페이지네이션 상한(20*limit) - cursor 무한루프 방지
            q = ["datasources", "query", a.datasource, "--limit", str(a.limit), "--json"]
            if cursor:
                q += ["--start-cursor", cursor]
            rc, out, err = run_ntn(q, ws)
            if rc != 0:
                db_lines.append(f"- (DB 조회 실패 rc={rc}: {err.strip()[:120]})")
                db_failed = not got
                break
            try:
                data = json.loads(out)
            except json.JSONDecodeError:
                db_lines.append("- (DB 응답 JSON 파싱 실패 - `ntn datasources query` 직접 확인)")
                db_failed = not got
                break
            got += data.get("results", []) if isinstance(data, dict) else (data if isinstance(data, list) else [])
            nxt = data.get("next_cursor") if isinstance(data, dict) else None
            if isinstance(data, dict) and data.get("has_more") and nxt:
                cursor = nxt
                continue
            break
        else:
            truncated = True  # 20페이지 상한 도달 = 전수 아닐 수 있음
        for pg in sorted(got, key=_edited_ts, reverse=True):  # 최신순(최근 수정일 우선)
            pid, title = pg.get("id", ""), _title_of(pg)
            db_lines.append(f"- [ ] ({_date_label(_edited_ts(pg))}) {title} - id `{pid}` - `ntn pages get {pid}`  | 근거: ")
            n_db += 1
    elif a.no_db:
        db_lines.append("- (--no-db: 강의 모듈 DB 의도적 제외. 응답에 그 이유를 사용자에게 명시할 것.)")
    else:
        db_lines.append("- (--datasource 미지정: 강의 모듈 DB 미탐색 = 게이트 미완.)")

    tokens = [t for t in re.split(r"\s+", a.topic) if len(t) >= 2]
    if tokens:
        roots = a.local_root or ["."]
        rg_cmd = ["rg", "-l", "-i", "--glob", "*.md", "--glob", "!curriculum-candidates-*.md"]  # 자기 산출물 self-match 제외
        for t in tokens:
            rg_cmd += ["-e", t]
        rg_cmd += roots
        def _mtime(f):
            try:
                return os.path.getmtime(f)
            except OSError:
                return 0.0
        try:
            p = subprocess.run(rg_cmd, capture_output=True, text=True, timeout=60)
            for f in sorted(set(filter(None, p.stdout.splitlines())), key=_mtime, reverse=True):  # 최신순(mtime)
                mt = _mtime(f)
                d = time.strftime("%Y-%m-%d", time.localtime(mt)) if mt else "날짜미상"
                local_lines.append(f"- [ ] ({d}) {f}  | 근거: ")
                n_local += 1
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            local_lines.append(f"- (로컬 rg 실패: {e})")
    if not local_lines:
        local_lines.append("- (로컬 후보 0 - --topic 토큰/--local-root 점검)")

    # 강의자료 워크스페이스/조직 노션 전수: 워크스페이스별 `ntn api /search` 결과 JSON을 에이전트가 넘긴다.
    # 게이트는 generic - 토큰/워크스페이스 태그는 스크립트에 박지 않고 authoring 3-0/AGENTS.md가 정본.
    notion_lines, n_notion = [], 0
    if a.notion_hits:
        for hf in a.notion_hits:
            try:
                with open(hf, encoding="utf-8") as fp:
                    data = json.load(fp)
            except (OSError, json.JSONDecodeError) as ex:
                notion_lines.append(f"- ({hf} 읽기/파싱 실패: {ex} - `ntn api /search` 출력을 그 경로에 저장했는지 확인)")
                continue
            results = data.get("results", []) if isinstance(data, dict) else (data if isinstance(data, list) else [])
            notion_lines.append(f"- **`{os.path.basename(hf)}` - {len(results)}건** (최신순)")
            for pg in sorted(results, key=_edited_ts, reverse=True):  # 최신순(최근 수정일 우선)
                pid, title = pg.get("id", ""), _title_of(pg)
                notion_lines.append(f"  - [ ] ({_date_label(_edited_ts(pg))}) {title} - id `{pid}` - `ntn pages get {pid}`  | 근거: ")
                n_notion += 1
    elif a.no_notion:
        notion_lines.append("- (--no-notion: 강의자료 워크스페이스/조직 노션 전수 의도적 제외. 응답에 그 이유를 사용자에게 명시할 것.)")
    else:
        notion_lines.append("- (--notion-hits 미지정: 강의자료 워크스페이스/조직 노션 전수 미탐색 = 게이트 미완. 워크스페이스별 `ntn api /search` 결과를 넘겨라.)")

    total = n_db + n_local + n_notion
    problems = []
    if a.datasource and db_failed:
        problems.append("DB 조회 실패")
    if not a.datasource and not a.no_db:
        problems.append("DB 미탐색 - `--datasource <ds-id>`(AGENTS.md) 주거나, 의도적 로컬-only면 `--no-db` 명시")
    if not a.notion_hits and not a.no_notion:
        problems.append("노션 전수 미탐색 - 강의자료 워크스페이스/조직 워크스페이스 각각 `ntn api /search` 후 `--notion-hits <file>...` 주거나, 의도적 제외면 `--no-notion` 명시")
    mc = max(1, a.min_candidates)  # 0/음수로 게이트 우회 금지(후보 0 통과 방지)
    if total < mc:
        problems.append(f"후보 {total} < 최소 {mc}")
    if truncated:
        problems.append("페이지네이션 20페이지 상한 도달 - 전수 아닐 수 있음")
    status = "MISS(게이트 미완)" if problems else "OK"

    slug = re.sub(r"[^0-9A-Za-z가-힣]+", "-", a.topic)[:40].strip("-") or "untitled"
    out_path = a.out or f"curriculum-candidates-{slug}.md"
    body = (
        f"# Curriculum 딥 탐색 후보 - {a.topic}\n\n"
        f"> curriculum_gate.py explore 산출물. **이 파일 없이 제작/검수 시작 금지**(review.md 게이트0).\n"
        f"> 게이트 상태: **{status}**" + (f" - {'; '.join(problems)}" if problems else "") + "\n"
        f"> 후보 {total}개 (DB {n_db}, 노션 {n_notion}, 로컬 {n_local}). 통과 조건: 후보 >= {mc}(참고 자료 최신순 {mc}개 이상) AND DB 탐색됨(또는 --no-db) AND 노션 전수 탐색됨(또는 --no-notion).\n"
        f"> 후보는 **최신순(최근 수정일 우선)**으로 정렬되고 각 줄 앞 `(YYYY-MM-DD)`가 수정일이다 - 낡은 자료보다 최근 검증 자료를 먼저 검토한다.\n"
        f"> 각 후보를 `ntn pages get`으로 실제로 떠서 비교한 것만 `[x]` + 근거 칸(떠온 핵심 1줄)을 채운다. 근거 빈 [x]는 미검토로 간주.\n\n"
        f"## 강의 모듈 DB\n" + "\n".join(db_lines) + "\n\n"
        f"## 강의자료 워크스페이스/조직 노션 전수 검색\n" + "\n".join(notion_lines) + "\n\n"
        f"## 로컬 교안\n" + "\n".join(local_lines) + "\n"
    )
    try:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(body)
    except OSError as e:
        print(f"산출물 쓰기 실패: {e}", file=sys.stderr)
        return 2
    print(f"산출물: {out_path}  상태={status}  (후보 {total}: DB {n_db}, 노션 {n_notion}, 로컬 {n_local})")
    if problems:
        print("실패: " + "; ".join(problems) + " -> 게이트 미통과, 제작/검수 진행 금지.", file=sys.stderr)
        return 1
    return 0


def _has_real_evidence(text):
    value = text.strip().strip("-").strip()
    return bool(value) and value.lower() not in {"todo", "tbd", "none", "n/a"} and value not in {"없음", "미검토"}


def _candidate_gate(path):
    try:
        with open(path, encoding="utf-8") as f:
            lines = f.read().splitlines()
    except (FileNotFoundError, IsADirectoryError, UnicodeDecodeError, PermissionError) as e:
        return [f"{path}: 후보 파일 읽기 실패: {e}"], f"{path}: 읽기 실패"

    text = "\n".join(lines)
    problems = []
    status = "?"
    m_status = re.search(r"게이트 상태:\s*\*\*([^*]+)\*\*", text)
    if not m_status:
        problems.append("explore 게이트 상태 없음")
    else:
        status = m_status.group(1).strip()
        if status != "OK":
            problems.append(f"explore 게이트 상태가 OK 아님: {status}")

    checked = []
    for i, line in enumerate(lines):
        if not CHECKED_CANDIDATE.match(line):
            continue
        evidence = ""
        m_ev = EVIDENCE.search(line)
        if m_ev:
            evidence = m_ev.group(1)
        else:
            for nxt in lines[i + 1:i + 4]:
                if re.match(r"^\s*-\s*\[[ xX]\]", nxt):
                    break
                m_next = EVIDENCE.search(nxt)
                if m_next:
                    evidence = m_next.group(1)
                    break
        checked.append((i + 1, evidence))

    if not checked:
        problems.append("[x]로 실제 검토 표시된 후보 없음")
    for line_no, evidence in checked:
        if not _has_real_evidence(evidence):
            problems.append(f"{path}:{line_no} 체크된 후보의 근거가 비어 있음")

    best = [m.group(1).strip() for line in lines for m in [BEST_SOURCE.match(line)] if m]
    if not best:
        problems.append("최선 후보: ... 라인 없음")
    elif not _has_real_evidence(best[-1]):
        problems.append("최선 후보 값이 비어 있음")

    evidence_count = sum(1 for _, ev in checked if _has_real_evidence(ev))
    summary = f"{path}: status={status} checked={len(checked)} evidence={evidence_count} best={'yes' if best else 'no'}"
    return problems, summary


def _run_candidate_gate(paths):
    all_problems = []
    for path in paths:
        problems, summary = _candidate_gate(path)
        print(summary)
        all_problems.extend(problems)
    return all_problems


def cmd_gate_candidates(a):
    problems = _run_candidate_gate(a.candidates)
    if problems:
        for p in problems:
            print(f"실패: {p}", file=sys.stderr)
        print("후보 검토 게이트 실패: 검색 산출물만 있고 원문 검토 근거가 부족함. 제작/반영 전 후보 원문을 열어 근거와 최선 후보를 채운다.", file=sys.stderr)
        return 1
    print("후보 검토 게이트 통과: 체크된 후보, 근거, 최선 후보 확인.")
    return 0


def cmd_verify_pages(a):
    token = os.environ.get("NOTION_API_KEY")
    if not token:
        print("NOTION_API_KEY 없음 - `agents-env run NOTION_API_KEY@<tag> -- python3 ... verify-pages ...`로 "
              "주입(태그-워크스페이스 매핑은 notion-sync 4-2절).", file=sys.stderr)
        return 2
    bad = 0
    print(f"{'page-id':38} 상태")
    for pid in a.page_ids:
        status, body = notion_get("/pages/" + pid, token)
        if status == 200 and body and body.get("id"):
            state = "REAL"
        elif status == 404:
            state = "NOTFOUND(404 - 환각 가능)"
        elif status in (401, 403):
            state = f"NO-ACCESS({status} - integration 미공유. 페이지에 연결 후 재시도)"
        elif status == 0:
            state = "NET/TIMEOUT(직접 확인)"
        else:
            state = f"HTTP {status}"
        if state != "REAL":
            bad += 1
        print(f"{pid:38} {state}")
    if bad:
        print(f"\n실패: {bad}개 실존 미확인. 단정/반영 금지. 404(환각, 고객사 A 신종)와 "
              f"401/403(미공유)을 구분해 정직하게 표기하고, 미공유면 사용자에게 공유를 요청한다.", file=sys.stderr)
        return 1
    print("\n통과: 전부 실존 확인(직접 REST 신뢰 채널).")
    return 0


def cmd_verify_media(a):
    try:
        with open(a.original, encoding="utf-8") as f:
            orig = media_keys(f.read())
        with open(a.produced, encoding="utf-8") as f:
            prod = media_keys(f.read())
    except (FileNotFoundError, IsADirectoryError, UnicodeDecodeError, PermissionError) as e:
        print(f"입력 파일 오류: {e}", file=sys.stderr)
        return 2
    if not orig:
        print("실패: 원본 미디어 ref 0개 - 잘못된 원본이거나 미디어 없는 자료. 미디어 이식이면 올바른 원본을, "
              "텍스트-only면 verify-media를 건너뛴다(이 결과를 '미디어 개선' 증거로 인용 금지).", file=sys.stderr)
        return 1
    missing = sorted(orig - prod)
    print("대조 범위: ![](), <img>, <file>, <video>, file://, attachment "
          "(북마크/child_page/unknown 블록은 범위 밖 - notion-sync 4-2절 자산 4종으로 별도 보존).")
    print("전제: 원본/산출물은 file:// ref 보존 작업본 .md (ntn get의 만료 S3 URL은 매번 토큰이 달라 비교 불가).")
    print(f"원본 미디어 ref {len(orig)} / 산출물 {len(prod)} / 누락 {len(missing)}")
    for k in missing:
        print(f"  누락: {k}")
    if missing:
        print(f"\n실패: 원본 미디어 {len(missing)}개가 산출물에서 빠짐. "
              f"'반영 완료' 단정 금지 - 이식/제작 누락 처방(#7, transplant).", file=sys.stderr)
        return 1
    if a.require_new and not (prod - orig):
        print("\n실패: --require-new인데 이식 외 새 이미지가 0개(prod-orig=0) - 새 산출물/도메인엔 "
              "이식 외 이미지를 1개 이상 확보한다. 개념 이미지는 검색/이식으로, Codex 생성은 세상에 "
              "실물 없는 이번 회차 산출물 결과 화면에만('왜 이미지 개선 안하냐' 처방, 100% 대응 추구 금지).", file=sys.stderr)
        return 1
    print("통과: 원본 미디어 ref 전부 산출물에 존재." + (f" 새 이미지 {len(prod - orig)}개." if a.require_new else ""))
    return 0


# review-draft / gate-review: "초안 띡" smell 린터 + 검수 산출물 게이트.
# 오늘 반복된 답답함을 기계로 잡는다("화면만, 실습 없음" / "설명 과잉, 신호 없음" / "이미지 개선 안함" / AI slop).
# 판단(사용자 관점 페르소나 비평)은 review.md.
SLOP_SYMBOL = re.compile(r"[→—·①-⑳§]")  # 화살표 em-dash 가운뎃점 동그라미숫자 섹션기호
REASSURE = re.compile(r"괜찮아요|당황하지|겁먹지|걱정\s*마|걱정하지|어렵지\s*않|쫄지|두려워")
CLICHE = re.compile(r"정공법|명예제|필살기|치트키")
SOURCE_INLINE = re.compile(r"\[출처\s*[:：]")  # [출처:] 인라인 표기 - 섹션 하단 북마크 카드로
# 노션 구조/표기 게이트 - authoring 3-1~3-3 산문을 기계화. 렌더 깨짐=HIGH, 톤 컨벤션=warn.
ASIDE = re.compile(r"<aside\b|^>\s*\[!")          # <aside>/> [!NOTE] - 노션서 평탄화됨, <callout>으로
COLOR_VAL = re.compile(r'\bcolor\s*=\s*["\']([^"\']+)["\']')  # color="X" 값 추출(한 줄 여럿 가능)
STD_COLOR = re.compile(r'^(?:default|gray|brown|orange|yellow|green|blue|purple|pink|red)(?:_bg|_background)?$')
CALLOUT_ICON = re.compile(r'<callout\b[^>]*\bicon\s*=\s*["\']([^"\']+)["\']')  # callout 아이콘
OK_EMOJI = {"🚨", "⚠", "🤔", "💡"}                # authoring 3-3 콜아웃 이모지 4종(VS16 제거 비교)
SEC_NUM = re.compile(r'^#[ \t]+(?:STEP[ \t]+)?(\d+)(\.\d+)?', re.I)  # # N / # STEP N / 소수 # N.M
META_HEAD = re.compile(r"Q&A|과제|타임라인|도입|복습|워밍업|마무리|정리|예고|준비물|소개"
                       r"|학습 ?목표|오늘의 결과물|배울 내용|개요|심화 자료|더 알아보|참고 자료|부록")  # 비-콘텐츠/프레이밍/참고(신호 불요)
VISUAL_HEAD = re.compile(r"산출물|결과|완성|목업|데모|대시보드|미리보기|프리뷰|도식|아키텍처")  # 결과/산출물 표시 섹션만(화면/흐름/구조 단독은 빌드 섹션이라 제외)


MD_IMG = re.compile(r"!\[[^\]]*\]\(")  # ![alt](  - alt 있어도 이미지로 인식(이전 `![](`만 봐서 alt 있는 이미지를 신호 누락)
PROSE_DENSE_CHARS = 120
PROSE_DENSE_LINES = 3
PROSE_DENSE_SENTENCES = 3


def _new_sec(head, ln):
    h = head.strip()
    return {"head": h or "(파일 시작)", "start": ln,
            "content": bool(h) and not META_HEAD.search(h) and not re.match(r"0[.\s]|0$", h),  # 서술형 헤딩도 콘텐츠(메타/0만 제외)
            "visual": bool(VISUAL_HEAD.search(h)),
            "image": False, "callouts": 0}


def _new_unit(head, ln, content):
    # 신호 단위(# 또는 ## 마다 리셋) - 부모 #의 이미지 하나가 자식 ## 들을 가리지 않게(Codex #2)
    return {"head": head, "start": ln, "content": content, "prose": 0, "sig": 0}


def _check_fence(findings, line, lang, body):
    """text/빈 펜스가 흐름(ASCII 화살표) 또는 다른 언어(json/js/markdown) 내용이면 경고."""
    if lang not in ("", "text", "plain text"):
        return
    nonempty = [l for l in body if l.strip()]
    if not nonempty:
        return
    first = nonempty[0].strip()
    looks_settings = first.startswith("[") or any(re.match(r"\S+\s*:\s", l.strip()) for l in nonempty[:3])
    if sum(1 for l in body if "->" in l) >= 2 and not looks_settings:
        findings.append((line, "warn", "flow-as-text",
            "흐름을 text 펜스 ASCII 화살표로 그림 - mermaid flowchart로(authoring 3-3)"))
    if first == "{" or first.startswith('{"') or first.startswith("[{"):  # {{ 표현식 제외
        findings.append((line, "warn", "code-lang", "JSON 내용인데 text 펜스 - json 언어로(authoring 3-3)"))
    elif re.search(r"^\s*(const|let|function|return)\b", "\n".join(body), re.M):
        findings.append((line, "warn", "code-lang", "JS 코드인데 text 펜스 - javascript 언어로(authoring 3-3)"))
    elif any(re.match(r"#{1,6}\s", l.strip()) for l in body):
        findings.append((line, "warn", "code-lang", "마크다운 프롬프트인데 text 펜스 - markdown 언어로(authoring 3-3)"))


def _scan_draft(lines):
    """교안 라인 -> 정렬된 findings [(line, sev, kind, msg)]. review-draft/gate-review 공용."""
    findings = []
    in_fence = fence_content = False
    fence_lang, fence_body, fence_open = "", [], 0
    sec = _new_sec("", 1)
    unit = _new_unit(sec["head"], 1, sec["content"])
    prose_start, prose_block = None, []
    sec_nums = []  # (정수 섹션번호, 줄) - 루프 후 연속성 검사
    fnb = next((j for j, l in enumerate(lines) if l.strip()), None)  # 첫 비공백 줄
    frontmatter_end = None
    if fnb is not None and lines[fnb].strip() == "---":
        findings.append((fnb + 1, "HIGH", "frontmatter",
            "업로드 본문 맨 앞 frontmatter(--- 블록) - ntn이 본문 첫 블록으로 박는다. 첫 콘텐츠 블록부터(authoring 3-1)"))
        for j in range(fnb + 1, len(lines)):
            if lines[j].strip() == "---":
                frontmatter_end = j + 1
                break

    def close_unit(u):
        if u["content"] and u["prose"] >= 2 and u["sig"] == 0:  # 1줄(정의/도입)은 면제, 2줄+ 무신호만 슬롭
            findings.append((u["start"], "HIGH", "no-signal",
                f"섹션 '{u['head']}'에 복붙 프롬프트/이미지/체크리스트가 하나도 없음 - 화면만/설명만이라 수강생이 칠 게 없다"))
        elif u["sig"] and u["prose"] > 2 * u["sig"]:
            findings.append((u["start"], "warn", "slop-dilute",
                f"섹션 '{u['head']}' 산문 {u['prose']}줄 vs 신호 {u['sig']}줄 - 산문 항목을 불렛/넘버링/표로 구조화(문장을 압축하지 말 것; 1-2줄 자연 산문은 허용)"))

    def close_sec(s):
        if s["content"] and s["visual"] and not s["image"]:
            findings.append((s["start"], "HIGH", "needs-image",
                f"섹션 '{s['head']}'(산출물/결과/화면류)에 이미지가 0개 - 이미지를 확보해 넣는다(개념은 검색/이식, 산출물 화면만 캡처/생성; '왜 이미지 개선 안하냐' 처방)"))
        if s["callouts"] > 3:
            findings.append((s["start"], "warn", "callout-overuse", f"섹션 '{s['head']}' 콜아웃 {s['callouts']}개(>3 남발)"))

    def close_prose_block():
        nonlocal prose_start, prose_block
        if not prose_block:
            return
        joined = " ".join(prose_block)
        sentences = len(re.findall(r"[.!?。！？]+(?=\s|$)", joined))  # 문장 종결만(파일명/URL 내부 점 제외)
        if (len(joined) >= PROSE_DENSE_CHARS or
                len(prose_block) >= PROSE_DENSE_LINES or
                sentences >= PROSE_DENSE_SENTENCES):
            findings.append((prose_start, "HIGH", "dense-prose",
                f"긴 산문 블록({len(joined)}자/{len(prose_block)}줄) - 1줄 설명 + 나머지 항목을 불렛/표/프롬프트/체크리스트로 분리(문장을 더 압축해 빽빽하게 만드는 건 AI-terse 결함; 1-2줄 자연 산문은 허용)"))
        prose_start, prose_block = None, []

    def add_prose_line(line, text):
        nonlocal prose_start, prose_block
        if prose_start is None:
            prose_start = line
        prose_block.append(text.strip())

    for i, raw in enumerate(lines, 1):
        s = raw.lstrip(" \t")
        if frontmatter_end and i <= frontmatter_end:
            close_prose_block()
            continue
        if s.startswith("```"):
            close_prose_block()
            if not in_fence:
                fence_lang, fence_body, fence_open = s[3:].strip(), [], i
                if not fence_lang:
                    findings.append((i, "HIGH", "empty-fence", "빈 코드펜스(언어 없음) - 노션이 JS로 하이라이팅, 내용에 맞는 언어 명시(authoring 3-3)"))
                in_fence, fence_content = True, False
            else:
                if fence_content:  # 내용 있는 펜스만 복붙 신호(빈 펜스 게이밍 차단)
                    unit["sig"] += 1
                _check_fence(findings, fence_open, fence_lang, fence_body)
                in_fence = False
            continue
        if in_fence:
            if s.strip():
                fence_content = True
            fence_body.append(s)
            continue
        if s.startswith("# "):
            close_prose_block()
            m = SEC_NUM.match(s)
            if m and m.group(2):  # 소수 번호 # 2.5
                findings.append((i, "warn", "section-decimal",
                    f"소수 섹션번호 '{m.group(1)}{m.group(2)}' - 정수로(authoring 3-2)"))
            elif m:
                sec_nums.append((int(m.group(1)), i))
            close_unit(unit)
            close_sec(sec)
            sec = _new_sec(s[2:], i)
            unit = _new_unit(sec["head"], i, sec["content"])
            continue
        if s.startswith("## "):  # 소제목 = 새 신호 단위(부모 섹션 content 상속)
            close_prose_block()
            close_unit(unit)
            unit = _new_unit(s[3:].strip(), i, sec["content"])
            continue
        if MD_IMG.search(s) or ("file://" in s) or ("<img" in s) or ("<file" in s) or ("<video" in s):
            close_prose_block()  # 이미지=구조 경계, 앞 산문 블록 종료(콜아웃/이미지 너머 병합 방지)
            sec["image"] = True
            unit["sig"] += 1
        elif re.match(r"[-*]\s*\[[ xX]\]\s*\S", s):  # 내용 있는 체크박스만 신호(빈 [ ] 게이밍 차단)
            close_prose_block()  # 체크박스=구조 경계
            unit["sig"] += 1
        elif "<callout" in s:
            close_prose_block()  # 콜아웃 경계, 산문이 콜아웃 본문과 병합되지 않게
            sec["callouts"] += 1
        elif s and not re.match(r"[-*#>|!]|\d+\.|<", s):  # 이미지(!)·리스트·헤딩·표·콜아웃 줄은 산문 아님
            unit["prose"] += 1
            add_prose_line(i, s)
            if len(re.findall(r"[.!?。]+(?=\s|$)", s)) > 3:
                findings.append((i, "warn", "long-prose", "한 블록 3문장 초과 줄글 - 불렛/넘버링으로 쪼갠다"))
        else:
            close_prose_block()
        if SLOP_SYMBOL.search(s):
            findings.append((i, "HIGH", "slop-symbol", "AI 티 기호(화살표/em-dash/가운뎃점/동그라미숫자/섹션기호) - anti-patterns.md 표기로"))
        if REASSURE.search(s):
            findings.append((i, "HIGH", "reassure", "안심 상투(괜찮아요/당황하지 류) - 통삭제 또는 본문에 녹임"))
        if CLICHE.search(s):
            findings.append((i, "HIGH", "cliche", "클리셰 라벨(정공법/필살기 류) - 구체 사실로"))
        if SOURCE_INLINE.search(s):
            findings.append((i, "HIGH", "source-inline", "[출처:] 인라인 표기 - 본문 출처 텍스트 금지, 섹션 하단 북마크 카드로(authoring 3-3절)"))
        if ASIDE.search(s):
            findings.append((i, "HIGH", "aside", "<aside>/> [!NOTE] - 노션서 평탄화됨, <callout>으로(authoring 3-1)"))
        for cm in COLOR_VAL.finditer(s):
            if not STD_COLOR.match(cm.group(1)):
                findings.append((i, "HIGH", "nonstd-color",
                    f"비표준 색 '{cm.group(1)}' - 노션 표준 팔레트만(authoring 3-1)"))
        im = CALLOUT_ICON.search(s)
        if im and im.group(1).replace("️", "") not in OK_EMOJI:
            findings.append((i, "warn", "callout-emoji",
                f"콜아웃 아이콘 '{im.group(1)}' - 🚨⚠️🤔💡 4종만(authoring 3-3)"))
    close_prose_block()
    close_unit(unit)
    close_sec(sec)
    nums = sorted(set(n for n, _ in sec_nums))
    if nums:
        missing = [x for x in range(1, nums[-1] + 1) if x not in nums]
        if missing:
            findings.append((sec_nums[0][1], "warn", "section-gap",
                f"섹션 번호 끊김 - 빠진 번호 {missing}(authoring 3-2 1부터 연속)"))
    findings.sort()
    return findings


def _read_lines(path):
    with open(path, encoding="utf-8") as f:
        return f.read().split("\n")


def cmd_review_draft(a):
    try:
        lines = _read_lines(a.draft)
    except (FileNotFoundError, IsADirectoryError, UnicodeDecodeError, PermissionError) as e:
        print(f"입력 파일 오류: {e}", file=sys.stderr)
        return 2
    findings = _scan_draft(lines)
    n_high = sum(1 for f in findings if f[1] == "HIGH")
    for ln, sev, kind, msg in findings:
        print(f"{a.draft}:{ln}  [{sev}] {kind}: {msg}")
    print(f"\n고신호 {n_high} / 경고 {len(findings) - n_high}")
    if n_high:
        print("실패: 초안 띡 smell - 개선 후 재실행. 신호 없는 섹션/이미지 없는 산출물 섹션/slop을 '핵심만, 수강생이 뭘 보고 칠지'로 고친다.", file=sys.stderr)
        return 1
    print("통과: 고신호 초안 띡 smell 없음(기계 검사). 사용자 관점 페르소나 비평은 review.md로 별도 진행.")
    return 0


def cmd_gate_review(a):
    """검수 산출물 게이트(Phase 4 반영 전제): 검수 리포트 존재 + 교안 review-draft 고신호 0."""
    candidates = getattr(a, "candidates", None) or []
    if candidates:
        problems = _run_candidate_gate(candidates)
        if problems:
            for p in problems:
                print(f"후보 검토 실패: {p}", file=sys.stderr)
            print("검수 게이트 실패: --candidates 후보 검토 게이트 미통과. 기존 자료를 실제로 본 근거 없이 반영 금지.", file=sys.stderr)
            return 1
    try:
        with open(a.report, encoding="utf-8") as f:
            rep = f.read()
    except (FileNotFoundError, IsADirectoryError, UnicodeDecodeError, PermissionError) as e:
        print(f"검수 리포트 없음/오류: {e} - 검수 없이 반영 금지(약점표만 내고 끝 방지).", file=sys.stderr)
        return 1
    if len(rep.strip()) < 40:
        print(f"검수 리포트 {a.report}가 비어있음(<40자) - 라운드별 '페르소나 발견/실제 바꾼 것/before->after' 기록 필요.", file=sys.stderr)
        return 1
    _low = rep.lower()
    has_delta = "->" in rep or "before" in _low or "after" in _low or ("전" in rep and "후" in rep)
    has_gate = any(k in rep for k in ("review-draft", "verify-media", "verify-pages", "고신호", "페르소나"))
    if not (has_delta and has_gate):
        print(f"검수 리포트 {a.report} 형식 미달 - 라운드별 'before->after' 개선 델타 + 게이트 출력"
              "(review-draft/verify-media/페르소나 발견) 인용이 있어야 한다. 빈 '검수했습니다'는 불가.", file=sys.stderr)
        return 1
    try:
        lines = _read_lines(a.draft)
    except (FileNotFoundError, IsADirectoryError, UnicodeDecodeError, PermissionError) as e:
        print(f"교안 파일 오류: {e}", file=sys.stderr)
        return 2
    n_high = sum(1 for f in _scan_draft(lines) if f[1] == "HIGH")
    if n_high:
        print(f"검수 게이트 실패: 교안에 고신호 smell {n_high}개 남음(`review-draft {a.draft}`로 확인) - 개선 후 재실행. 반영 금지.", file=sys.stderr)
        return 1
    print(f"검수 게이트 통과: 리포트 {a.report} 존재 + 교안 고신호 smell 0. Phase 4 반영 가능.")
    return 0


def cmd_status(a):
    """워크스페이스 단계별 게이트 산출물 인벤토리 + 다음 필수 게이트. 단계 전환을 산문 추론 대신 기계 판정."""
    ws = a.workspace
    if not os.path.isdir(ws):
        print(f"워크스페이스 디렉토리 아님: {ws}", file=sys.stderr)
        return 2

    def find(pat):
        return sorted(glob.glob(os.path.join(ws, "**", pat), recursive=True))

    cand = find("curriculum-candidates-*.md")
    reviews = find("검수-*.md")
    print(f"# Curriculum status: {ws}\n")

    print(f"[딥탐색(Phase 2/3)] explore 산출물 {len(cand)}개")
    for c in cand:
        m = re.search(r"게이트 상태: \*\*([^*]+)\*\*", open(c, encoding="utf-8").read(600))
        print(f"  - {os.path.relpath(c, ws)}: {m.group(1).strip() if m else '?'}")
    if not cand:
        print("  -> 없음. 제작/검수 전 `explore`로 후보 산출물 생성")

    print(f"\n[검수(Phase 5)] 검수 리포트 {len(reviews)}개")
    for r in reviews:
        print(f"  - {os.path.relpath(r, ws)}")
    if not reviews:
        print("  -> 없음. 반영 전 검수(review.md) -> `검수-<회차>.md` 리포트")

    draft_high_total = 0
    if a.draft:
        print("\n[교안 review-draft 고신호]")
        for d in a.draft:
            try:
                n_high = sum(1 for f in _scan_draft(_read_lines(d)) if f[1] == "HIGH")
            except (OSError, UnicodeDecodeError) as e:
                print(f"  - {d}: 읽기 실패 {e}")
                continue
            draft_high_total += n_high
            print(f"  - {os.path.basename(d)}: 고신호 {n_high}  "
                  f"{'OK 반영 가능' if n_high == 0 else 'X 개선 필요(review-draft로 확인)'}")

    print("\n[다음 필수 게이트]")
    if a.draft and draft_high_total:
        print(f"  review-draft 개선 - 교안 고신호 {draft_high_total} 남음(0까지 고치고 재확인)")
    elif not cand and not reviews:
        print("  explore - 딥탐색 후보 산출물 (없이 제작/검수 시작 금지)")
    elif not reviews:
        print("  검수 루프(review.md) -> 검수 리포트 + gate-review 통과 (없이 반영 금지)")
    else:
        print("  gate-review --report <검수.md> <교안> 통과 확인 후 반영")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    e = sub.add_parser("explore", help="딥 탐색 -> 후보 목록 산출물(후보 0/DB 미탐색이면 비0)")
    e.add_argument("--topic", required=True, help="주제/키워드(공백으로 여러 토큰 OR 검색)")
    e.add_argument("--workspace-id", dest="workspace_id", help="대상 워크스페이스의 NOTION_WORKSPACE_ID")
    e.add_argument("--datasource", help="강의 모듈 data-source-id(프로젝트 AGENTS.md)")
    e.add_argument("--no-db", action="store_true", help="강의 모듈 DB 의도적 제외(로컬-only를 명시적 선택으로)")
    e.add_argument("--notion-hits", dest="notion_hits", nargs="*",
                   help="워크스페이스별 `ntn api /search` 결과 JSON(반복) - 강의자료 워크스페이스/조직 워크스페이스 둘 다 권장(authoring 3-0)")
    e.add_argument("--no-notion", dest="no_notion", action="store_true",
                   help="강의자료 워크스페이스/조직 노션 전수 의도적 제외(명시적 선택으로)")
    e.add_argument("--local-root", action="append", help="로컬 교안 탐색 루트(반복 가능, 기본 .)")
    e.add_argument("--limit", type=int, default=1000, help="DB 페이지당(기본 1000, has_more면 cursor 루프)")
    e.add_argument("--min-candidates", type=int, default=10, help="이 수 미만이면 게이트 미통과(기본 10 = 참고 자료 최신순 10개 이상). 니치 주제로 줄일 땐 응답에 사유 명시")
    e.add_argument("--out", help="산출물 경로(기본 ./curriculum-candidates-<주제>.md)")
    e.set_defaults(func=cmd_explore)

    vp = sub.add_parser("verify-pages", help="page-id 실존 확인(환각 차단, 직접 REST). NOTION_API_KEY 주입 필요")
    vp.add_argument("page_ids", nargs="+", help="확인할 page-id들")
    vp.set_defaults(func=cmd_verify_pages)

    vm = sub.add_parser("verify-media", help="로컬 원본 작업본 vs 산출물 미디어 ref 대조")
    vm.add_argument("original", help="원본 .md(이식 출처, file:// ref 보존 작업본 - ntn get 출력 아님)")
    vm.add_argument("produced", help="산출물 .md(교안)")
    vm.add_argument("--require-new", dest="require_new", action="store_true",
                    help="새 산출물/도메인용: 이식 외 새 이미지(prod-orig)를 1개 이상 확보(검색/이식 우선, 생성은 산출물 화면 최후)했는지 - 0이면 비0")
    vm.set_defaults(func=cmd_verify_media)

    rd = sub.add_parser("review-draft", help="초안 띡 smell 린터(신호 없는 섹션/이미지 없는 산출물 섹션/slop, 있으면 비0)")
    rd.add_argument("draft", help="검사할 교안 .md")
    rd.set_defaults(func=cmd_review_draft)

    gc = sub.add_parser("gate-candidates", help="후보 검토 게이트([x] 후보 + 근거 + 최선 후보 확인)")
    gc.add_argument("candidates", nargs="+", help="curriculum-candidates-*.md")
    gc.set_defaults(func=cmd_gate_candidates)

    gr = sub.add_parser("gate-review", help="검수 산출물 게이트(후보 근거 + 리포트 존재 + 교안 고신호 0, Phase4 반영 전제)")
    gr.add_argument("--candidates", nargs="+", help="curriculum-candidates-*.md(여러 파일 가능) - source evidence 게이트")
    gr.add_argument("--report", required=True, help="검수 리포트 .md(라운드별 발견/개선/before->after)")
    gr.add_argument("draft", help="검사할 교안 .md")
    gr.set_defaults(func=cmd_gate_review)

    st = sub.add_parser("status", help="워크스페이스 단계별 게이트 산출물 인벤토리 + 다음 필수 게이트")
    st.add_argument("workspace", help="커리큘럼 워크스페이스 디렉토리")
    st.add_argument("--draft", action="append", help="교안 .md(반복 가능) - review-draft 고신호 수 표시")
    st.set_defaults(func=cmd_status)

    a = ap.parse_args()
    sys.exit(a.func(a))


if __name__ == "__main__":
    main()
