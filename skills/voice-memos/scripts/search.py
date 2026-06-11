#!/usr/bin/env python3
"""음성 메모 전사본 검색 스크립트.

날짜, 키워드, 최근 N개 등 다양한 조건으로 전사 파일을 검색합니다.
"""

import argparse
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

import vm_notes

TRANSCRIPTS_DIR = Path.home() / ".voice-memos/transcripts"
CALL_RECORDINGS_DIR = (
    Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/녹음"
)

# 에이닷 통화 녹음 파일명: `<이름>_<휴대폰번호>_<YYYYMMDD>_<HHMMSS>.txt`
# 예: `홍길동님_01012345678_20260407_165111.txt`
CALL_FILENAME_RE = re.compile(r"^(.+?)_(\d{10,11})_(\d{8})_(\d{6})\.txt$")


def parse_date_range(date_str: str) -> tuple[datetime, datetime]:
    """날짜 문자열을 파싱하여 시작/끝 datetime을 반환합니다.

    지원 형식: 2026-03-10, 2026-03, 2026, today, yesterday, this-week, this-month
    """
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    if date_str == "today":
        return today, today + timedelta(days=1)
    elif date_str == "yesterday":
        return today - timedelta(days=1), today
    elif date_str == "this-week":
        start = today - timedelta(days=today.weekday())
        return start, today + timedelta(days=1)
    elif date_str == "this-month":
        start = today.replace(day=1)
        return start, today + timedelta(days=1)

    # YYYY-MM-DD
    if re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt, dt + timedelta(days=1)
    # YYYY-MM
    elif re.match(r"^\d{4}-\d{2}$", date_str):
        dt = datetime.strptime(date_str, "%Y-%m")
        if dt.month == 12:
            end = dt.replace(year=dt.year + 1, month=1)
        else:
            end = dt.replace(month=dt.month + 1)
        return dt, end
    # YYYY
    elif re.match(r"^\d{4}$", date_str):
        dt = datetime.strptime(date_str, "%Y")
        return dt, dt.replace(year=dt.year + 1)
    else:
        print(f"지원하지 않는 날짜 형식: {date_str}", file=sys.stderr)
        sys.exit(1)


def dir_to_datetime(transcript_path: Path) -> datetime | None:
    """Voice Memos transcript 디렉터리 경로에서 datetime을 파싱합니다.

    지원 형식: `YYYYMMDD/HHMMSS`, `YYYYMMDD/HHMMSS-<uuid8>`.
    UUID suffix는 같은 초에 생성된 녹음을 구분하기 위해 extract.py가 붙입니다.
    """
    try:
        time_part = transcript_path.parent.name.split("-", 1)[0]
        date_part = transcript_path.parent.parent.name
        return datetime.strptime(f"{date_part} {time_part}", "%Y%m%d %H%M%S")
    except ValueError:
        return None


def is_call_recording(path: Path) -> bool:
    """파일이 iCloud 통화 녹음(.txt) 디렉터리에 속하는지 확인합니다."""
    return path.parent == CALL_RECORDINGS_DIR


def call_to_datetime(path: Path) -> datetime | None:
    """통화 녹음 파일명에서 datetime을 파싱합니다."""
    match = CALL_FILENAME_RE.match(path.name)
    if not match:
        return None
    try:
        return datetime.strptime(
            f"{match.group(3)} {match.group(4)}", "%Y%m%d %H%M%S"
        )
    except ValueError:
        return None


def file_to_datetime(path: Path) -> datetime | None:
    """파일 종류(Voice Memo / 통화 녹음 / Apple Notes)에 맞춰 datetime을 추출합니다."""
    if vm_notes.is_note(path):
        return vm_notes.note_meta(path).get("mtime")
    if is_call_recording(path):
        return call_to_datetime(path)
    return dir_to_datetime(path)


def iter_transcript_files() -> list[Path]:
    """전사/메모 파일 목록을 반환합니다.

    - Voice Memos transcript: `~/.voice-memos/transcripts/**/transcript.md`
    - iCloud 통화 녹음: `~/Library/Mobile Documents/com~apple~CloudDocs/녹음/*.txt`
    - Apple Notes: `~/Library/.../NoteStore.sqlite` (mode=ro 직접 쿼리)
    """
    files = list(TRANSCRIPTS_DIR.rglob("transcript.md"))
    if CALL_RECORDINGS_DIR.exists():
        files.extend(
            f
            for f in CALL_RECORDINGS_DIR.glob("*.txt")
            if CALL_FILENAME_RE.match(f.name)
        )
    vm_notes.refresh_notes_meta()
    files.extend(vm_notes.all_note_paths())
    return files


def search_by_date(date_str: str) -> list[Path]:
    """날짜로 전사/메모 파일을 검색합니다."""
    start, end = parse_date_range(date_str)
    results = []
    for f in sorted(iter_transcript_files(), key=str):
        dt = file_to_datetime(f)
        if dt and start <= dt < end:
            results.append(f)
    return results


def _extract_snippets(
    haystack: str, keywords: list[str], radius: int = 120, max_snippets: int = 2
) -> tuple[int, list[str]]:
    """본문에서 키워드 매칭 주변 스니펫과 총 매칭 횟수를 추출합니다.

    radius: 매칭 위치 좌우로 포함할 글자 수.
    max_snippets: 파일당 최대 스니펫 수(겹치는 구간은 합쳐 1개로).
    transcript는 한 줄이 문단 통째인 경우가 많아, 라인 단위가 아니라
    매칭 위치 ±radius로 잘라 줄바꿈을 공백으로 평탄화한다.
    """
    low = haystack.lower()
    positions: list[tuple[int, int]] = []  # (pos, match_len)
    for kw in keywords:
        k = kw.lower()
        if not k:
            continue
        start = 0
        while True:
            i = low.find(k, start)
            if i == -1:
                break
            positions.append((i, len(k)))
            start = i + len(k)
    total = len(positions)
    positions.sort()
    snippets: list[str] = []
    used: list[tuple[int, int]] = []
    for pos, mlen in positions:
        if len(snippets) >= max_snippets:
            break
        s = max(0, pos - radius)
        e = min(len(haystack), pos + mlen + radius)
        if any(s < ue and e > us for us, ue in used):
            continue  # 이미 출력한 스니펫과 겹침
        used.append((s, e))
        body = haystack[s:e].replace("\n", " ").strip()
        snippets.append(f"{'…' if s > 0 else ''}{body}{'…' if e < len(haystack) else ''}")
    return total, snippets


def search_by_keyword(
    keywords: list[str], mode: str = "any"
) -> list[tuple[Path, int, list[str]]]:
    """키워드(들)로 전사/메모 본문을 검색합니다.

    keywords: 검색어 리스트. mode="any"는 하나라도 매칭, "all"은 전부 매칭.
    반환: (path, 총_매칭_횟수, 스니펫) 리스트. 매칭 횟수 내림차순 정렬.
    """
    needles = [k.lower() for k in keywords if k]
    results: list[tuple[Path, int, list[str]]] = []
    for f in sorted(iter_transcript_files(), key=str):
        if vm_notes.is_note(f):
            haystack = vm_notes.note_haystack(f)
        else:
            try:
                haystack = f.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
        low = haystack.lower()
        present = [n for n in needles if n in low]
        matched = len(present) == len(needles) if mode == "all" else bool(present)
        if not matched:
            continue
        total, snippets = _extract_snippets(haystack, keywords)
        results.append((f, total, snippets))
    results.sort(key=lambda t: t[1], reverse=True)
    return results


def list_recent(n: int) -> list[Path]:
    """최근 N개 전사 파일을 반환합니다."""
    files = sorted(
        iter_transcript_files(),
        key=lambda p: file_to_datetime(p) or datetime.min,
        reverse=True,
    )
    return files[:n]


def list_all_dates() -> list[str]:
    """전사 파일이 있는 날짜 목록을 반환합니다."""
    dates = set()
    for f in iter_transcript_files():
        dt = file_to_datetime(f)
        if dt:
            dates.add(dt.strftime("%Y-%m-%d"))
    return sorted(dates, reverse=True)


def format_result(
    filepath: Path,
    show_preview: bool = True,
    match_count: int | None = None,
    match_snippets: list[str] | None = None,
) -> str:
    """검색 결과를 포맷팅합니다.

    라벨은 데이터 소스 출처만 표시한다:
    - [음성 메모]  Apple Voice Memos
    - [에이닷]    에이닷 통화 녹음
    - [메모]      Apple Notes

    match_count/match_snippets가 주어지면(키워드 검색) 라벨에 매칭 횟수를 붙이고,
    미리보기를 파일 도입부 대신 매칭 위치 주변 스니펫으로 대체한다.
    """
    dt = file_to_datetime(filepath)
    date_str = (
        dt.strftime("%Y-%m-%d %H:%M:%S")
        if dt
        else (
            str(filepath)
            if vm_notes.is_note(filepath)
            else (filepath.name if is_call_recording(filepath) else filepath.parent.name)
        )
    )

    if vm_notes.is_note(filepath):
        meta = vm_notes.note_meta(filepath)
        title = meta.get("title", "?")
        folder = meta.get("folder", "?")
        line = f"  [메모]      {date_str}  {folder}/{title}"
        if match_count is not None:
            line += f"  ({match_count}회)"
        if show_preview:
            if match_snippets:
                for sn in match_snippets:
                    line += f"\n         {sn}"
            elif meta.get("locked"):
                line += "\n         (잠긴 메모 — 본문 검색 제외)"
            else:
                body = vm_notes.note_body(filepath)
                if body:
                    # 본문 첫 줄이 제목과 동일한 경우가 많아 두 번째 줄부터 미리보기
                    lines = [ln for ln in body.splitlines() if ln.strip()]
                    if lines and lines[0].strip() == title.strip() and len(lines) > 1:
                        preview_src = "\n".join(lines[1:])
                    else:
                        preview_src = body
                    preview = preview_src.strip()[:120].replace("\n", " ")
                    if preview:
                        line += f"\n         {preview}..."
        return line

    if is_call_recording(filepath):
        match = CALL_FILENAME_RE.match(filepath.name)
        contact = match.group(1) if match else filepath.stem
        line = f"  [에이닷]    {date_str}  {contact}"
    else:
        line = (
            f"  [음성 메모] {date_str}  "
            f"{filepath.parent.parent.name}/{filepath.parent.name}"
        )

    if match_count is not None:
        line += f"  ({match_count}회)"

    if show_preview:
        if match_snippets:
            for sn in match_snippets:
                line += f"\n         {sn}"
            return line
        content = filepath.read_text(encoding="utf-8")
        if is_call_recording(filepath):
            summary_block = _extract_call_summary(content)
            if summary_block:
                indented = "\n".join(
                    f"         {ln}" if ln else "" for ln in summary_block.splitlines()
                )
                line += f"\n{indented}"
            else:
                # [통화요약] 섹션이 없으면 [녹음 내용] 일부를 폴백으로 노출
                idx = content.find("[녹음 내용]")
                if idx != -1:
                    preview = (
                        content[idx + len("[녹음 내용]") :]
                        .strip()[:80]
                        .replace("\n", " ")
                    )
                    if preview:
                        line += f"\n         {preview}..."
        else:
            idx = content.find("## 전사 내용")
            if idx != -1:
                preview = (
                    content[idx + len("## 전사 내용") :]
                    .strip()[:80]
                    .replace("\n", " ")
                )
                if preview:
                    line += f"\n         {preview}..."

    return line


def _extract_call_summary(content: str) -> str:
    """에이닷 통화 녹음 .txt에서 `[통화요약]` 블록을 추출합니다.

    `[통화요약]` 헤더 자체를 포함해 `[녹음 내용]` 직전까지 반환.
    섹션이 없으면 빈 문자열.
    """
    start = content.find("[통화요약]")
    if start == -1:
        return ""
    end = content.find("[녹음 내용]", start)
    block = content[start:end] if end != -1 else content[start:]
    return block.rstrip()


def main():
    parser = argparse.ArgumentParser(description="음성 메모 전사본 검색")
    parser.add_argument("--date", type=str, help="날짜로 검색 (2026-03-10, 2026-03, today, yesterday, this-week, this-month)")
    parser.add_argument("--keyword", type=str, help="키워드로 내용 검색")
    parser.add_argument("--any", dest="any_kw", type=str, help="쉼표로 구분한 키워드 중 하나라도 매칭 (OR)")
    parser.add_argument("--all", dest="all_kw", type=str, help="쉼표로 구분한 키워드 모두 매칭 (AND)")
    parser.add_argument("--recent", type=int, help="최근 N개 파일 표시")
    parser.add_argument("--dates", action="store_true", help="전사 파일이 있는 날짜 목록")
    parser.add_argument("--no-preview", action="store_true", help="미리보기 숨김")
    parser.add_argument("--count", action="store_true", help="파일 수만 표시")
    args = parser.parse_args()

    if args.dates:
        dates = list_all_dates()
        print(f"총 {len(dates)}일의 녹음:")
        for d in dates:
            print(f"  {d}")
        return

    kw_results: list[tuple[Path, int, list[str]]] | None = None
    results = []
    if args.date:
        results = search_by_date(args.date)
    elif args.all_kw:
        kws = [k.strip() for k in args.all_kw.split(",") if k.strip()]
        kw_results = search_by_keyword(kws, mode="all")
    elif args.any_kw:
        kws = [k.strip() for k in args.any_kw.split(",") if k.strip()]
        kw_results = search_by_keyword(kws, mode="any")
    elif args.keyword:
        kw_results = search_by_keyword([args.keyword], mode="any")
    elif args.recent:
        results = list_recent(args.recent)
    else:
        results = list_recent(10)

    if args.count:
        print(f"{len(kw_results) if kw_results is not None else len(results)}건")
        return

    if kw_results is not None:
        if not kw_results:
            print("검색 결과 없음")
            return
        print(f"{len(kw_results)}건 검색됨 (매칭 많은 순):")
        for f, cnt, snips in kw_results:
            print(format_result(f, show_preview=not args.no_preview, match_count=cnt, match_snippets=snips))
        return

    if not results:
        print("검색 결과 없음")
        return

    print(f"{len(results)}건 검색됨:")
    for f in results:
        print(format_result(f, show_preview=not args.no_preview))


if __name__ == "__main__":
    main()
