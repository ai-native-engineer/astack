#!/usr/bin/env python3
"""검증된 로컬 교안 1개를 Notion 페이지 1개에 fail-closed로 반영한다.

본문 옆 <local.md>.fidelity.json이 필요하다. 이식본은 sources를 선언하고,
대응 원본이 없는 네이티브 교안만 {"native": true}를 명시한다.
로컬 이미지가 있으면 ntn이 upload id를 기계 판독 가능하게 반환하기 전까지 쓰기 전에 중단한다.

usage: NOTION_WORKSPACE_ID=<ws> python3 notion_reflect.py --expected-title "<title>" \
  --expected-parent-id <parent-id> --expected-last-edited-time <ISO-time> \
  --candidates <candidates.md> --report <review.md> <page_id> <local.md>
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from urllib.parse import unquote, urlparse

IMAGE_RE = re.compile(r'!\[[^\]\n]*\]\(([^)\n]+)\)')
HTML_IMAGE_RE = re.compile(r'<(?:img|source)\b[^>]*\bsrc\s*=\s*(?:"[^"]+"|\'[^\']+\'|[^\s>]+)', re.I)
REFERENCE_IMAGE_RE = re.compile(r'!\[[^\]\n]*\]\[[^\]\n]*\]')
SHORTCUT_IMAGE_RE = re.compile(r'!\[[^\]\n]+\](?![ \t]*[\[(])')
HTML_ATTACHMENT_RE = re.compile(
    r'<(?P<kind>video|file)\b[^>]*\bsrc\s*=\s*(?:"(?P<dq>[^"]+)"|\'(?P<sq>[^\']+)\'|(?P<bare>[^\s>]+))[^>]*>',
    re.I,
)
BM_RE = re.compile(r'^\[\[bookmark:\s*(\S+?)\s*\]\]\s*$', re.I)
SKIP = re.compile(r'^(<!--|!\[|</|<\w+|\||```|\[\[bookmark:|---|\*\*\*|___)')
FIDELITY_LINT = os.path.join(os.path.dirname(__file__), "fidelity_lint.py")


class SafetyError(RuntimeError):
    pass


def short(*values):
    return " | ".join(str(v).strip().replace("\n", " ")[:160] for v in values if str(v).strip())


def ntn(args, input_text=None, timeout=180):
    """returncode를 버리지 않고 (stdout, stderr, returncode)로 반환한다."""
    kwargs = {"capture_output": True, "text": True, "env": dict(os.environ), "timeout": timeout}
    kwargs["stdin" if input_text is None else "input"] = subprocess.DEVNULL if input_text is None else input_text
    try:
        result = subprocess.run(["ntn"] + args, **kwargs)
    except FileNotFoundError as e:
        raise SafetyError("ntn 실행 파일을 찾지 못했습니다.") from e
    except subprocess.TimeoutExpired as e:
        raise SafetyError(f"ntn timeout({timeout}s): {' '.join(args)}") from e
    return result.stdout, result.stderr, result.returncode


def require_ntn(args, input_text=None):
    out, err, rc = ntn(args, input_text)
    if rc:
        raise SafetyError(f"ntn exit {rc}: {' '.join(args)}: {short(err, out) or '출력 없음'}")
    return out


def api(path, method=None, body=None):
    args = ["api"] + (["--method", method] if method else []) + [path]
    out = require_ntn(args, body)
    try:
        data = json.loads(out)
    except json.JSONDecodeError as e:
        raise SafetyError(f"Notion API 비JSON 응답: {path}: {short(out) or '빈 응답'}") from e
    if not isinstance(data, dict) or data.get("object") == "error":
        raise SafetyError(f"Notion API 오류: {path}: {short(data)}")
    return data


def block_text(block):
    block_type = block.get("type")
    if block_type == "bookmark":
        return str((block.get("bookmark") or {}).get("url") or "")
    rich_text = block.get(block_type, {}).get("rich_text") or []
    return ''.join(x.get("plain_text", "") for x in rich_text) if isinstance(rich_text, list) else ""


def norm(text):
    return re.sub(r'[*_`#>\s]', '', text)


def image_refs(text):
    """Markdown image destination을 title/query/angle 형식까지 정규화해 반환한다."""
    refs = []
    for match in IMAGE_RE.finditer(text):
        raw = match.group(1).strip()
        if raw.startswith("<"):
            closing = raw.find(">")
            if closing < 2:
                continue
            ref = raw[1:closing].strip()
        else:
            ref = raw.split(None, 1)[0].strip()
        refs.append((match, ref))
    return refs


def preceding_anchor(markdown, position):
    for line in reversed(markdown[:position].splitlines()):
        if image_refs(line) or BM_RE.match(line.strip()):
            continue
        anchor = content_fingerprint(line)
        if anchor:
            return anchor
    return ""


def image_asset_signature(markdown):
    signature = []
    for match, ref in image_refs(markdown):
        anchor = preceding_anchor(markdown, match.start())
        signature.append((ref, anchor))
    return signature


def attachment_signature(markdown):
    signature = []
    for match in HTML_ATTACHMENT_RE.finditer(markdown):
        ref = next(value for value in (match.group("dq"), match.group("sq"), match.group("bare")) if value)
        signature.append((match.group("kind").lower(), ref, preceding_anchor(markdown, match.start())))
    return signature


def is_blocked_bookmark(url):
    parsed = urlparse(url)
    return (parsed.netloc.lower() == "app.notion.com"
            and parsed.path.startswith("/p/") and bool(parsed.fragment))


def flatten(page_id):
    flat = []

    def walk(block_id):
        cursor = None
        while True:
            path = f"/v1/blocks/{block_id}/children?page_size=100"
            if cursor:
                path += f"&start_cursor={cursor}"
            data = api(path)
            results = data.get("results")
            if not isinstance(results, list):
                raise SafetyError(f"children results 누락: {block_id}")
            for block in results:
                if not block.get("id") or not block.get("type"):
                    raise SafetyError(f"식별 불가능한 block 응답: {block_id}")
                flat.append((block["id"], block_text(block), block_id, block["type"]))
                if block.get("has_children") and block["type"] not in (
                        "child_page", "child_database", "synced_block", "unsupported"):
                    walk(block["id"])
            if not data.get("has_more"):
                break
            cursor = data.get("next_cursor")
            if not cursor:
                raise SafetyError(f"pagination cursor 누락: {block_id}")

    walk(page_id)
    return flat


def parse(mdpath):
    try:
        raw = open(mdpath, encoding="utf-8").read()
    except (OSError, UnicodeDecodeError) as e:
        raise SafetyError(f"교안 읽기 실패: {mdpath}: {e}") from e
    if raw.startswith("---"):
        frontmatter = re.match(r'\A---\r?\n.*?\r?\n---\r?\n?', raw, re.S)
        if not frontmatter:
            raise SafetyError(f"닫히지 않은 frontmatter: {mdpath}")
        raw = raw[frontmatter.end():]
    if HTML_IMAGE_RE.search(raw) or REFERENCE_IMAGE_RE.search(raw) or SHORTCUT_IMAGE_RE.search(raw):
        raise SafetyError("HTML/reference-style 이미지는 안전하게 round-trip할 수 없습니다. "
                          "한 줄짜리 `![alt](destination)` 형식으로 바꾸세요.")
    lines = raw.split("\n")
    body, assets = [], []

    def anchor_for(index):
        for line in reversed(lines[:index]):
            text = line.strip()
            if not text or SKIP.match(text):
                continue
            text = re.sub(r'[*_`>#]', '', text).strip()
            text = re.sub(r'^[-*•]\s+|^\d+\.\s+|^\[[ xX]*\]\s*', '', text)
            if text:
                return text
        return ""

    for index, line in enumerate(lines):
        images, bookmark = image_refs(line), BM_RE.match(line.strip())
        local_images = [(match, ref) for match, ref in images
                        if urlparse(ref).scheme.lower() not in ("http", "https", "file")]
        if local_images:
            if len(images) != 1 or line.strip() != local_images[0][0].group(0):
                raise SafetyError("로컬 이미지는 한 줄에 디렉티브 하나만 둡니다: " + line.strip()[:120])
            ref = unquote(urlparse(local_images[0][1]).path)
            assets.append(("image", os.path.normpath(os.path.join(os.path.dirname(mdpath), ref)),
                           anchor_for(index)))
        elif bookmark:
            assets.append(("bookmark", bookmark.group(1), anchor_for(index)))
        else:
            body.append(line)
    return "\n".join(body), assets


def need_file(path, label):
    if not path or not os.path.isfile(path) or not os.access(path, os.R_OK):
        raise SafetyError(f"{label} 파일 없음/읽기 불가: {path}")


def fidelity(mdpath):
    sidecar = mdpath + ".fidelity.json"
    need_file(sidecar, "충실도 사이드카")
    try:
        spec = json.load(open(sidecar, encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as e:
        raise SafetyError(f"충실도 사이드카 읽기 실패: {e}") from e
    if not isinstance(spec, dict):
        raise SafetyError("충실도 사이드카는 JSON 객체여야 합니다.")
    if spec.get("native") is True:
        if spec.get("sources"):
            raise SafetyError("native=true와 sources를 함께 선언할 수 없습니다.")
        return "native=true"
    if spec.get("native") not in (None, False):
        raise SafetyError("native 예외는 JSON boolean true로만 명시합니다.")
    sources = spec.get("sources")
    if not isinstance(sources, list) or not sources or not all(isinstance(x, str) and x for x in sources):
        raise SafetyError("충실도 sources를 1개 이상 선언하세요.")
    need_file(FIDELITY_LINT, "충실도 린터")
    command = [sys.executable, FIDELITY_LINT, "--target", mdpath]
    target_real = os.path.realpath(mdpath)
    for source in sources:
        source = source if os.path.isabs(source) else os.path.join(os.path.dirname(sidecar), source)
        need_file(source, "충실도 소스")
        if os.path.realpath(source) == target_real:
            raise SafetyError("교안 자신을 충실도 source로 선언할 수 없습니다.")
        command += ["--source", source]
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired) as e:
        raise SafetyError(f"충실도 린터 실행 실패: {e}") from e
    if result.returncode:
        raise SafetyError(f"충실도 린터 exit {result.returncode}: {short(result.stdout, result.stderr)}")
    return short(result.stdout) or "PASS"


def local_preflight(mdpath, report, candidates):
    for path, label in [(mdpath, "교안"), (report, "검수 리포트")]:
        need_file(path, label)
    if not candidates:
        raise SafetyError("--candidates가 필요합니다.")
    for path in candidates:
        need_file(path, "후보 검토")
    body, assets = parse(mdpath)
    if not body.strip():
        raise SafetyError("이미지/북마크를 뺀 본문이 비었습니다.")
    for kind, payload, anchor in assets:
        key = norm(anchor)[:22]
        matches = sum(key in norm(line) for line in body.splitlines()) if len(key) >= 6 else 0
        if matches != 1:
            raise SafetyError(f"자산 앵커는 본문 한 곳에만 매칭되어야 합니다: {payload}: {anchor!r}")
        if kind == "image":
            need_file(payload, "로컬 이미지")
        else:
            url = urlparse(payload)
            if url.scheme not in ("http", "https") or not url.netloc:
                raise SafetyError(f"북마크 URL 오류: {payload}")
            if is_blocked_bookmark(payload):
                raise SafetyError(f"Notion 자기참조 북마크 금지: {payload}")
    images = [payload for kind, payload, _ in assets if kind == "image"]
    if images:
        # ponytail: ntn 0.16.0에 upload id 출력 계약이 생기면 이 차단만 교체한다.
        raise SafetyError("로컬 이미지 반영 차단: ntn 0.16.0 `files create`는 성공 stdout이 비어 "
                          "upload id를 확인할 수 없습니다. update 전 중단: "
                          + ", ".join(os.path.basename(path) for path in images))
    try:
        import curriculum_gate as gate
    except ImportError as e:
        raise SafetyError(f"curriculum_gate import 실패: {e}") from e
    rc = gate.cmd_gate_review(argparse.Namespace(report=report, draft=mdpath, candidates=candidates))
    if rc:
        raise SafetyError(f"gate-review exit {rc}")
    return body, assets, fidelity(mdpath)


def content_fingerprint(markdown):
    """자산/마크업 표현 차이를 빼고 본문 순서를 비교할 문자열을 만든다."""
    text = IMAGE_RE.sub("", markdown)
    text = re.sub(r'^\s*\[\[bookmark:\s*\S+?\s*\]\]\s*$', '', text, flags=re.I | re.M)
    text = re.sub(r'<[^>]+>', ' ', text)
    return ''.join(re.findall(r'[가-힣a-z0-9]+', text.lower()))


def structure_counts(markdown):
    return {
        "callout": len(re.findall(r'<callout\b', markdown, re.I)),
        "table": len(re.findall(r'<table\b', markdown, re.I)),
        "table_row": len(re.findall(r'<tr\b', markdown, re.I)),
        "table_cell": len(re.findall(r'<td\b', markdown, re.I)),
        "details": len(re.findall(r'<details\b', markdown, re.I)),
        "summary": len(re.findall(r'<summary\b', markdown, re.I)),
        "toggle": len(re.findall(r'\{[^}\n]*\btoggle\s*=\s*["\']?true', markdown, re.I)),
        "heading_1": len(re.findall(r'^#(?!#)\s+', markdown, re.M)),
        "heading_2": len(re.findall(r'^##(?!#)\s+', markdown, re.M)),
        "heading_3": len(re.findall(r'^###(?!#)\s+', markdown, re.M)),
        "code_fence": len(re.findall(r'^```', markdown, re.M)),
        "checklist": len(re.findall(r'^\s*[-*+]\s+\[[ xX]\]\s+', markdown, re.M)),
        "unordered_list": len(re.findall(r'^\s*[-*+]\s+(?!\[[ xX]\])', markdown, re.M)),
        "ordered_list": len(re.findall(r'^\s*\d+\.\s+', markdown, re.M)),
    }


def structural_signature(markdown):
    """블록 종류와 해당 텍스트의 결합 순서를 비교한다."""
    signature = []
    in_fence = False
    for line in markdown.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            signature.append(("fence", stripped[3:].strip().lower()))
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        heading = re.match(r'^(#{1,3})\s+(.+)$', stripped)
        checklist = re.match(r'^[-*+]\s+\[([ xX])\]\s+(.+)$', stripped)
        unordered = re.match(r'^[-*+]\s+(.+)$', stripped)
        ordered = re.match(r'^(\d+)\.\s+(.+)$', stripped)
        if heading:
            signature.append((f"h{len(heading.group(1))}", content_fingerprint(heading.group(2))))
        elif checklist:
            signature.append(("check", checklist.group(1).lower(), content_fingerprint(checklist.group(2))))
        elif unordered:
            signature.append(("ul", content_fingerprint(unordered.group(1))))
        elif ordered:
            signature.append(("ol", ordered.group(1), content_fingerprint(ordered.group(2))))
        for tag in re.finditer(r'</?(?:callout|table|tr|td|details|summary)\b', stripped, re.I):
            signature.append(("tag", tag.group(0).lower()))
    return signature


def container_signature(markdown):
    signature = []
    for tag in ("callout", "table", "tr", "td", "details", "summary"):
        pattern = re.compile(fr'<{tag}\b[^>]*>(.*?)</{tag}>', re.I | re.S)
        for match in pattern.finditer(markdown):
            signature.append((match.start(), tag, content_fingerprint(match.group(1))))
    return [(tag, content) for _, tag, content in sorted(signature)]


def validate_content_roundtrip(expected, actual):
    expected_fingerprint = content_fingerprint(expected)
    actual_fingerprint = content_fingerprint(actual)
    if not expected_fingerprint or expected_fingerprint != actual_fingerprint:
        raise SafetyError("round-trip 본문 불일치: 재조회한 텍스트가 승인 본문과 정확히 일치하지 않습니다.")
    expected_structure = structure_counts(expected)
    actual_structure = structure_counts(actual)
    if expected_structure != actual_structure:
        raise SafetyError(f"round-trip 구조 불일치: 기대 {expected_structure}, 실제 {actual_structure}")
    expected_signature = structural_signature(expected)
    actual_signature = structural_signature(actual)
    if expected_signature != actual_signature:
        raise SafetyError("round-trip 블록 순서/결합 불일치: heading/list/fence 구조가 달라졌습니다.")
    if container_signature(expected) != container_signature(actual):
        raise SafetyError("round-trip 컨테이너 내용 불일치: callout/table/details 범위가 달라졌습니다.")
    if image_asset_signature(expected) != image_asset_signature(actual):
        raise SafetyError("round-trip 이미지 불일치: ref, 순서, 앵커가 승인 본문과 다릅니다.")
    if attachment_signature(expected) != attachment_signature(actual):
        raise SafetyError("round-trip file/video 불일치: ref, 순서, 앵커가 승인 본문과 다릅니다.")


def page_title(metadata):
    for prop in (metadata.get("properties") or {}).values():
        if isinstance(prop, dict) and prop.get("type") == "title":
            return ''.join(x.get("plain_text", "") for x in prop.get("title", [])).strip()
    return ""


def parent_identity(parent):
    if not isinstance(parent, dict):
        return ""
    parent_type = parent.get("type")
    if parent_type == "workspace":
        return "workspace"
    value = parent.get(parent_type) if isinstance(parent_type, str) else None
    return str(value or "").replace("-", "").lower()


def page_markdown(page_id):
    data = api(f"/v1/pages/{page_id}/markdown")
    if data.get("truncated") or data.get("unknown_block_ids"):
        raise SafetyError("Markdown 백업이 truncated이거나 unknown block을 포함합니다.")
    if not isinstance(data.get("markdown"), str):
        raise SafetyError("Markdown API 응답에 markdown 문자열이 없습니다.")
    return data["markdown"]


def remote_preflight(page_id, expected_title, expected_parent_id, expected_last_edited_time):
    pattern = r'(?:[0-9a-f]{32}|[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})'
    if not re.fullmatch(pattern, page_id.lower()):
        raise SafetyError(f"page_id 형식 오류: {page_id}")
    metadata = api(f"/v1/pages/{page_id}")
    actual_id = str(metadata.get("id", "")).replace("-", "").lower()
    if actual_id != page_id.replace("-", "").lower():
        raise SafetyError(f"page identity 불일치: {metadata.get('id')!r}")
    title = page_title(metadata)
    if not title or title != expected_title:
        raise SafetyError(f"page title 불일치: 기대 {expected_title!r}, 실제 {title!r}")
    blocked_types = {"child_page", "child_database", "synced_block", "unsupported"}
    found_blocked = sorted({block_type for *_, block_type in flatten(page_id)
                            if block_type in blocked_types})
    if found_blocked:
        raise SafetyError("전체교체 불가 블록이 있습니다: " + ", ".join(found_blocked))
    parent = metadata.get("parent")
    if not isinstance(parent, dict):
        raise SafetyError("page parent 응답이 없습니다.")
    normalized_expected_parent = ("workspace" if expected_parent_id == "workspace"
                                  else expected_parent_id.replace("-", "").lower())
    if parent_identity(parent) != normalized_expected_parent:
        raise SafetyError(f"page parent 불일치: 기대 {expected_parent_id!r}, 실제 {parent!r}")
    actual_last_edited_time = metadata.get("last_edited_time")
    if actual_last_edited_time != expected_last_edited_time:
        raise SafetyError("page last_edited_time 불일치: 승인/프리플라이트 뒤 페이지가 변경되었습니다. "
                          f"기대 {expected_last_edited_time!r}, 실제 {actual_last_edited_time!r}")
    backup = page_markdown(page_id)
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False,
                                         prefix=f"notion-backup-{actual_id[:8]}-", suffix=".md") as file:
            file.write(backup)
            backup_path = file.name
    except OSError as e:
        raise SafetyError(f"백업 파일 생성 실패: {e}") from e
    return title, parent, backup, backup_path


def rollback(page_id, backup):
    try:
        out, err, rc = ntn(["pages", "update", page_id], backup)
    except SafetyError as e:
        return False, str(e)
    if rc:
        return False, f"ntn exit {rc}: {short(err, out)}"
    try:
        restored = page_markdown(page_id)
    except SafetyError as e:
        return False, f"복구 후 검증 실패: {e}"
    same = restored.replace("\r\n", "\n").strip() == backup.replace("\r\n", "\n").strip()
    return same, "백업 일치" if same else "복구 후 Markdown 불일치"


def reflect(page_id, mdpath, expected_title, expected_parent_id, expected_last_edited_time,
            report, candidates):
    update_started = False
    backup = backup_path = None
    try:
        body, assets, fidelity_result = local_preflight(mdpath, report, candidates)
        title, parent, backup, backup_path = remote_preflight(
            page_id, expected_title, expected_parent_id, expected_last_edited_time)
        metadata_now = api(f"/v1/pages/{page_id}")
        current_id = str(metadata_now.get("id", "")).replace("-", "").lower()
        if (current_id != page_id.replace("-", "").lower()
                or page_title(metadata_now) != title
                or metadata_now.get("parent") != parent
                or metadata_now.get("last_edited_time") != expected_last_edited_time):
            raise SafetyError("update 직전 페이지 snapshot 불일치: preflight 뒤 사용자 편집 가능성이 있어 중단합니다.")
        print(f"PREFLIGHT OK: page={page_id} title={title!r} fidelity={fidelity_result} backup={backup_path}")
        update_started = True
        require_ntn(["pages", "update", page_id], body)
        flat, used = flatten(page_id), set()
        previous = (None, None, None)
        inserted = 0
        for kind, payload, anchor in assets:  # local image는 preflight에서 이미 차단됨
            key = norm(anchor)[:22]
            if key == previous[0] and previous[1]:
                block_id, parent_id = previous[1:]
            else:
                match = next(((bid, parent) for bid, text, parent, _ in flat
                              if bid not in used and key in norm(text)), None)
                if not match:
                    raise SafetyError(f"update 후 북마크 앵커 누락: {anchor!r}")
                block_id, parent_id = match
                used.add(block_id)
            request = {"children": [{"object": "block", "type": "bookmark",
                                      "bookmark": {"url": payload}}],
                       "position": {"type": "after_block", "after_block": {"id": block_id}}}
            result = api(f"/v1/blocks/{parent_id}/children", "PATCH", json.dumps(request))
            created = result.get("results")
            if (not isinstance(created, list) or len(created) != 1 or not created[0].get("id")
                    or (created[0].get("bookmark") or {}).get("url") != payload):
                raise SafetyError(f"북마크 삽입 확인 실패: {payload}")
            inserted += 1
            previous = (key, created[0]["id"], parent_id)
        roundtrip = flatten(page_id)
        roundtrip_markdown = page_markdown(page_id)
        validate_content_roundtrip(body, roundtrip_markdown)
        metadata_after = api(f"/v1/pages/{page_id}")
        actual_id_after = str(metadata_after.get("id", "")).replace("-", "").lower()
        if (actual_id_after != page_id.replace("-", "").lower()
                or page_title(metadata_after) != title or metadata_after.get("parent") != parent):
            raise SafetyError("round-trip 페이지 정체성 불일치: id/title/parent가 바뀌었습니다.")
        expected_images = len(image_refs(body))
        expected_bookmark_signatures = [(payload, norm(anchor)[:22])
                                        for kind, payload, anchor in assets if kind == "bookmark"]
        actual_bookmark_entries = [(index, text) for index, (_, text, _, block_type) in enumerate(roundtrip)
                                   if block_type == "bookmark"]
        actual_images = sum(t == "image" for *_, t in roundtrip)
        actual_bookmark_urls = [url for _, url in actual_bookmark_entries]
        expected_bookmark_urls = [url for url, _ in expected_bookmark_signatures]
        if actual_bookmark_urls != expected_bookmark_urls:
            raise SafetyError("round-trip 북마크 URL/순서 불일치")
        for (url, anchor), (index, actual_url) in zip(expected_bookmark_signatures, actual_bookmark_entries):
            preceding_text = [text for _, text, _, block_type in roundtrip[:index]
                              if block_type not in ("bookmark", "image") and text]
            if actual_url != url or not any(anchor in norm(text) for text in preceding_text):
                raise SafetyError(f"round-trip 북마크 앵커 불일치: {url}")
        actual_bookmarks = len(actual_bookmark_entries)
        if expected_images != actual_images or len(expected_bookmark_signatures) != inserted or inserted != actual_bookmarks:
            raise SafetyError("round-trip 불일치: "
                              f"image {expected_images}/{actual_images}, "
                              f"bookmark {len(expected_bookmark_signatures)}/{inserted}/{actual_bookmarks}")
        print(f"OK {os.path.basename(mdpath)}: image {actual_images}, bookmark {actual_bookmarks}, page={page_id}")
        return True
    except Exception as e:
        print(f"FAIL {os.path.basename(mdpath)}: {e}", file=sys.stderr)
        if update_started and backup is not None:
            ok, detail = rollback(page_id, backup)
            print(f"{'ROLLBACK OK' if ok else 'ROLLBACK FAILED'}: {detail}; backup={backup_path}", file=sys.stderr)
        else:
            print("NO WRITE: preflight 단계에서 중단했습니다.", file=sys.stderr)
        return False


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--candidates", action="append", required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--expected-title", required=True)
    parser.add_argument("--expected-parent-id", required=True,
                        help="직전 REST preflight에서 확인한 parent id. workspace parent는 workspace")
    parser.add_argument("--expected-last-edited-time", required=True,
                        help="직전 REST preflight에서 확인한 last_edited_time")
    parser.add_argument("--skip-gate", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("pair", nargs=2, metavar=("PAGE_ID", "LOCAL_MD"))
    args = parser.parse_args(argv)
    if args.skip_gate:
        parser.error("--skip-gate는 fail-closed 반영에서 사용할 수 없습니다.")
    if not os.environ.get("NOTION_WORKSPACE_ID"):
        parser.error("NOTION_WORKSPACE_ID env가 필요합니다.")
    return 0 if reflect(args.pair[0], args.pair[1], args.expected_title,
                        args.expected_parent_id, args.expected_last_edited_time,
                        args.report, args.candidates) else 1


if __name__ == "__main__":
    sys.exit(main())
