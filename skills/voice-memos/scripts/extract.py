#!/usr/bin/env python3
"""
Apple Voice Memos 전사 추출 스크립트 (apple-stt 기반).

Recordings 폴더의 .m4a 파일을 apple-stt(macOS SpeechAnalyzer)로 직접 전사해
마크다운 파일로 저장합니다. Apple 기본 전사(tsrp atom)에 의존하지 않으므로
OS 백그라운드 전사 완료를 기다릴 필요가 없습니다.
"""

import re
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

from config import RECORDINGS_DIR, TRANSCRIPTS_DIR, VOCAB_FILE, ensure_runtime_dirs

LOCALE = "ko-KR"

# 녹음이 아직 진행 중일 때 미완성 파일을 전사하는 것을 막는다.
SETTLE_QUIET_SECONDS = 3.0  # 이 시간 동안 파일 변화가 없어야 "쓰기 완료"로 본다
SETTLE_MAX_WAIT = 90.0  # 안정화를 기다리는 최대 시간 (긴 녹음 대비)
SETTLE_POLL_INTERVAL = 2.0


def wait_until_settled(filepath: Path) -> bool:
    """파일 쓰기가 끝날(녹음 종료) 때까지 기다린다.

    크기/mtime이 SETTLE_QUIET_SECONDS 동안 변하지 않으면 안정으로 판단한다.
    SETTLE_MAX_WAIT를 넘기면 False(아직 불안정)로 포기하고 다음 트리거에 맡긴다.

    참고: lsof로 '녹음 중'을 판정하려 했으나, Voice Memos는 녹음 정지 후에도
    파일을 쓰기 핸들(FD 'u')로 계속 열어두기 때문에 신뢰할 수 없다(2026-05-31 실험).
    크기 고정만이 신뢰 가능한 '쓰기 종료' 신호다.
    """
    deadline = time.monotonic() + SETTLE_MAX_WAIT
    last_sig = None
    quiet_since = None

    while time.monotonic() < deadline:
        try:
            st = filepath.stat()
        except FileNotFoundError:
            return False
        sig = (st.st_size, st.st_mtime)

        if sig != last_sig:
            # 아직 쓰이는 중: 안정 타이머 리셋
            last_sig = sig
            quiet_since = time.monotonic()
        else:
            if quiet_since is None:
                quiet_since = time.monotonic()
            if time.monotonic() - quiet_since >= SETTLE_QUIET_SECONDS:
                return True

        time.sleep(SETTLE_POLL_INTERVAL)

    return False


def _run_apple_stt(audio_path: Path) -> str:
    """주어진 오디오 파일을 apple-stt로 전사해 텍스트를 반환합니다. 실패 시 빈 문자열."""
    stt = shutil.which("apple-stt")
    if stt is None:
        print("apple-stt 명령을 찾을 수 없습니다 (PATH 확인)", file=sys.stderr)
        return ""

    cmd = [stt, "--quiet", "--locale", LOCALE]
    if VOCAB_FILE.exists():
        cmd += ["--vocab-file", str(VOCAB_FILE)]
    cmd.append(str(audio_path))

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as exc:
        print(f"  apple-stt 실패: {audio_path.name}\n{exc.stderr}", file=sys.stderr)
        return ""

    return result.stdout.strip()


def _convert_to_m4a(filepath: Path) -> Path | None:
    """ffmpeg로 오디오 스트림만 m4a로 추출한다. 실패 시 None.

    .qta(Apple Watch·타기기 동기화 포맷)는 AAC 오디오 + 비디오 스트림이 든
    mp4 컨테이너라 apple-stt(AVAudioFile)가 직접 못 읽는다. 오디오만 떼어내면 전사 가능.
    """
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        print("ffmpeg 명령을 찾을 수 없습니다 (.qta 변환 불가)", file=sys.stderr)
        return None

    import tempfile

    fd, tmp_name = tempfile.mkstemp(suffix=".m4a", prefix="vm_qta_")
    import os

    os.close(fd)
    tmp_path = Path(tmp_name)
    cmd = [
        ffmpeg, "-y", "-i", str(filepath),
        "-vn", "-map", "0:a:0", "-c:a", "aac",
        str(tmp_path),
    ]
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=600)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        print(f"  ffmpeg 변환 실패: {filepath.name}", file=sys.stderr)
        tmp_path.unlink(missing_ok=True)
        return None
    if tmp_path.stat().st_size == 0:
        tmp_path.unlink(missing_ok=True)
        return None
    return tmp_path


def transcribe(filepath: Path) -> str:
    """오디오를 전사해 텍스트를 반환합니다. 실패 시 빈 문자열.

    .qta는 apple-stt가 직접 못 읽으므로 ffmpeg로 m4a 변환 후 전사한다.
    .m4a도 혹시 직접 전사가 실패하면 ffmpeg 변환을 폴백으로 시도한다.
    """
    suffix = filepath.suffix.lower()

    if suffix == ".qta":
        converted = _convert_to_m4a(filepath)
        if converted is None:
            return ""
        try:
            return _run_apple_stt(converted)
        finally:
            converted.unlink(missing_ok=True)

    text = _run_apple_stt(filepath)
    if text:
        return text

    # .m4a 직접 전사 실패 시 ffmpeg 변환 폴백
    converted = _convert_to_m4a(filepath)
    if converted is None:
        return ""
    try:
        return _run_apple_stt(converted)
    finally:
        converted.unlink(missing_ok=True)


_TIMESTAMP_RE = re.compile(r"(\d{8})\s+(\d{6})")


def parse_filename(filename):
    """파일명 앞쪽의 'YYYYMMDD HHMMSS' 타임스탬프를 추출합니다.

    '20260309 145819-UUID.m4a'            → ('20260309', '145819', '2026-03-09 14:58:19')
    '20260309 입대 전 일기-track0.qta'      → ('20260309', '...', ...)  ← 제목이 있어도 안전
    split('-') 방식은 사용자가 앱에서 이름을 한글로 바꾼 녹음(예: '...-track0.composition.qta')에서
    시간 부분이 깨졌다. 정규식으로 앞쪽 타임스탬프만 뽑아 그 문제를 막는다.
    """
    m = _TIMESTAMP_RE.search(filename)
    if m:
        date_part, time_part = m.group(1), m.group(2)
        try:
            dt = datetime.strptime(f"{date_part} {time_part}", "%Y%m%d %H%M%S")
            return date_part, time_part, dt.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            return date_part, time_part, f"{date_part} {time_part}"

    # 타임스탬프 패턴이 없으면 최대한 안전하게 폴백
    base = filename.replace(".m4a", "").replace(".qta", "").split("-")[0].strip()
    return base[:8] or "00000000", "000000", base


def generate_markdown(filepath, text):
    """전사 텍스트를 마크다운으로 변환합니다."""
    _, _, date_str = parse_filename(filepath.name)

    lines = [
        f"# {date_str}",
        "",
        f"- **녹음일시**: {date_str}",
        f"- **언어**: {LOCALE}",
        f"- **원본파일**: `{filepath.name}`",
        "- **전사엔진**: apple-stt",
        "",
        "## 전사 내용",
        "",
        text,
        "",
    ]
    return "\n".join(lines)


def process_file(filepath, force=False):
    """단일 m4a 파일을 처리합니다. 성공 시 True 반환."""
    date_part, time_part, _ = parse_filename(filepath.name)
    out_dir = TRANSCRIPTS_DIR / date_part / time_part
    out_path = out_dir / "transcript.md"

    if out_path.exists() and not force:
        if filepath.stat().st_mtime <= out_path.stat().st_mtime:
            return False

    # 녹음이 진행 중이면(파일이 아직 쓰이는 중) 완료될 때까지 기다린 뒤 전사한다.
    # 미완성 파일을 전사하고 mtime 스킵에 걸려 완성본을 놓치는 문제를 방지.
    if not wait_until_settled(filepath):
        print(f"  대기 초과/불안정, 다음 트리거에서 재시도: {filepath.name}", file=sys.stderr)
        return False

    text = transcribe(filepath)
    if not text.strip():
        return False

    md = generate_markdown(filepath, text)
    ensure_runtime_dirs()
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")
    print(f"  {filepath.name} → {date_part}/{time_part}/transcript.md")
    return True


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Apple Voice Memos 전사 추출 (apple-stt)")
    parser.add_argument("--file", type=str, help="특정 m4a 파일만 처리")
    parser.add_argument("--force", action="store_true", help="이미 추출된 파일도 재처리")
    parser.add_argument("--all", action="store_true", help="모든 m4a 파일 처리")
    args = parser.parse_args()

    if args.file:
        filepath = Path(args.file).expanduser()
        if not filepath.exists():
            print(f"File not found: {filepath}", file=sys.stderr)
            sys.exit(1)
        process_file(filepath, force=args.force)
        return

    files = sorted(
        f for ext in ("*.m4a", "*.qta") for f in RECORDINGS_DIR.glob(ext)
    )
    if args.all:
        processed = sum(1 for file in files if process_file(file, force=args.force))
    else:
        processed = sum(1 for file in files if process_file(file))

    print(f"  {processed}/{len(files)} 처리됨")


if __name__ == "__main__":
    main()
