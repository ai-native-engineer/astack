#!/usr/bin/env python3
"""
에이닷 통화 녹음(.m4a) 자동 전사.

iCloud 녹음 폴더의 통화 m4a를 apple-stt로 전사해
transcripts/<YYYYMMDD>/<HHMMSS>/transcript.md 로 저장한다.

Apple Voice Memos와 달리 통화 m4a에는 tsrp atom이 없어 extract.py로는
처리할 수 없으므로 별도 경로로 둔다. 저장 포맷은 extract.py와 동일하게
`## 전사 내용` 마커를 포함하므로, 이후 summarize.py / notify.py 파이프라인이
그대로 이어받는다.

에이닷이 자동 전사 .txt를 함께 올린 통화는 search.py가 이미 인덱싱하므로
여기서는 .m4a만 대상으로 한다. (같은 통화의 .txt 유무와 무관하게 m4a를 전사)
"""

import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

CALLS_DIR = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/녹음"
TRANSCRIPTS_DIR = Path.home() / ".voice-memos/transcripts"
APPLE_STT = Path.home() / "scripts/apple-stt"

# <이름>_<휴대폰번호>_<YYYYMMDD>_<HHMMSS>.m4a
FILENAME_RE = re.compile(r"^(.+?)_(\d{10,11})_(\d{8})_(\d{6})\.m4a$")

DOWNLOAD_TIMEOUT = 180  # dataless 다운로드 대기 상한(초)
SETTLE_CHECKS = 3       # 크기 안정 판정 연속 횟수
SETTLE_INTERVAL = 2     # 안정 체크 간격(초)


def is_dataless(path: Path) -> bool:
    """iCloud placeholder(미다운로드) 여부. 로컬 블록이 0이면 dataless."""
    return path.stat().st_blocks == 0


def materialize(path: Path) -> bool:
    """dataless면 brctl download로 받아 완료까지 대기. 로컬에 있으면 즉시 True."""
    if not is_dataless(path):
        return True
    subprocess.run(["brctl", "download", str(path)], check=False, capture_output=True)
    waited = 0
    while waited < DOWNLOAD_TIMEOUT:
        if path.stat().st_blocks > 0:
            return True
        time.sleep(SETTLE_INTERVAL)
        waited += SETTLE_INTERVAL
    return path.stat().st_blocks > 0


def wait_until_settled(path: Path) -> None:
    """파일 크기가 SETTLE_CHECKS회 연속 동일할 때까지 대기(업로드/다운로드 안정화)."""
    last = -1
    stable = 0
    while stable < SETTLE_CHECKS:
        size = path.stat().st_size
        if size == last and size > 0:
            stable += 1
        else:
            stable = 0
            last = size
        time.sleep(SETTLE_INTERVAL)


def parse_filename(name: str):
    """파일명에서 (연락처, 번호, YYYYMMDD, HHMMSS, datetime) 추출. 불일치 시 None."""
    match = FILENAME_RE.match(name)
    if not match:
        return None
    contact, phone, date_part, time_part = match.groups()
    try:
        dt = datetime.strptime(f"{date_part}{time_part}", "%Y%m%d%H%M%S")
    except ValueError:
        return None
    return contact, phone, date_part, time_part, dt


def transcript_has_body(path: Path) -> bool:
    """transcript.md에 실제 전사 본문이 있는지 확인(멱등 처리용)."""
    try:
        content = path.read_text(encoding="utf-8")
    except OSError:
        return False
    idx = content.find("## 전사 내용")
    if idx == -1:
        return False
    body = re.sub(r"<!--.*?-->", "", content[idx + len("## 전사 내용"):]).strip()
    return bool(body)


def transcribe(path: Path) -> str | None:
    """apple-stt로 타임스탬프 포함 전사. stdout 텍스트 반환, 실패 시 None."""
    result = subprocess.run(
        [str(APPLE_STT), "-t", "-q", str(path)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"  [ERROR] apple-stt 실패: {path.name}\n{result.stderr}", file=sys.stderr)
        return None
    text = result.stdout.strip()
    return text or None


def generate_markdown(contact: str, phone: str, dt: datetime, name: str, text: str) -> str:
    """extract.py와 동일한 `## 전사 내용` 마커 포맷으로 변환."""
    date_str = dt.strftime("%Y-%m-%d %H:%M:%S")
    contact_label = contact[:-1] if contact.endswith("님") else contact
    lines = [
        f"# {date_str} {contact_label}님과의 통화",
        "",
        f"- **녹음일시**: {date_str}",
        f"- **상대**: {contact} ({phone})",
        "- **언어**: ko-KR",
        f"- **원본파일**: `{name}`",
        "- **전사**: apple-stt (화자 라벨 없음)",
        "",
        "## 전사 내용",
        "",
        text,
        "",
    ]
    return "\n".join(lines)


def process_file(path: Path, force: bool = False) -> bool:
    """단일 통화 m4a를 처리. 성공 시 True."""
    parsed = parse_filename(path.name)
    if parsed is None:
        return False
    contact, phone, date_part, time_part, dt = parsed

    out_dir = TRANSCRIPTS_DIR / date_part / time_part
    out_path = out_dir / "transcript.md"
    if out_path.exists() and not force and transcript_has_body(out_path):
        return False

    if not materialize(path):
        print(f"  [ERROR] iCloud 다운로드 실패: {path.name}", file=sys.stderr)
        return False
    wait_until_settled(path)

    text = transcribe(path)
    if not text:
        return False

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        generate_markdown(contact, phone, dt, path.name, text), encoding="utf-8"
    )
    print(f"  {path.name} → {date_part}/{time_part}/transcript.md")
    return True


def main():
    import argparse

    parser = argparse.ArgumentParser(description="에이닷 통화 녹음(.m4a) 자동 전사")
    parser.add_argument("--file", type=str, help="특정 m4a 파일만 처리")
    parser.add_argument("--force", action="store_true", help="이미 전사된 파일도 재처리")
    parser.add_argument("--all", action="store_true", help="모든 m4a 처리(기본 동작과 동일)")
    args = parser.parse_args()

    if args.file:
        filepath = Path(args.file).expanduser()
        if not filepath.exists():
            print(f"File not found: {filepath}", file=sys.stderr)
            sys.exit(1)
        process_file(filepath, force=args.force)
        return

    if not CALLS_DIR.exists():
        print(f"  통화 폴더 없음: {CALLS_DIR}")
        return

    files = sorted(CALLS_DIR.glob("*.m4a"))
    processed = sum(1 for file in files if process_file(file, force=args.force))
    print(f"  {processed}/{len(files)} 전사됨")


if __name__ == "__main__":
    main()
