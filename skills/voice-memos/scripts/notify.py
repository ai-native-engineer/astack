#!/usr/bin/env python3
"""
Discord, Telegram으로 요약 결과를 전송합니다.

환경변수:
  DISCORD_WEBHOOK_URL: Discord webhook URL
  TELEGRAM_BOT_TOKEN: Telegram bot token
  TELEGRAM_CHAT_ID: Telegram chat ID
"""

import json
import os
import urllib.error
import urllib.request
from pathlib import Path

from config import (
    ENV_FILE,
    TRANSCRIPTS_DIR,
    iter_transcript_files,
    strip_process_markers,
    summary_path_for,
    transcript_path_for,
)

NOTIFIED_MARKER = "<!-- notified -->"


def load_env():
    """간단한 .env 파일 로더."""
    if not ENV_FILE.exists():
        return
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())


def read_summary_file(filepath: Path) -> str | None:
    """별도 요약 파일의 본문을 읽습니다."""
    content = strip_process_markers(filepath.read_text(encoding="utf-8"))
    return content if content else None


def extract_summary_from_transcript(filepath: Path) -> str | None:
    """전사 파일 내에 포함된 요약 섹션을 추출합니다."""
    content = filepath.read_text(encoding="utf-8")
    start = content.find("## 요약")
    if start == -1:
        return None

    end = content.find("## 전사 내용", start)
    snippet = content[start:end] if end != -1 else content[start:]
    snippet = strip_process_markers(snippet)
    return snippet if snippet else None


def send_discord(webhook_url: str, title: str, summary: str):
    """Discord webhook으로 메시지를 전송합니다."""
    if len(summary) > 2048:
        summary = summary[:2045] + "..."

    payload = json.dumps(
        {
            "embeds": [
                {
                    "title": title,
                    "description": summary,
                    "color": 5814783,
                }
            ]
        }
    ).encode("utf-8")

    req = urllib.request.Request(
        webhook_url,
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    try:
        urllib.request.urlopen(req)
        print(f"  {title} → Discord")
    except urllib.error.URLError as error:
        print(f"  [ERROR] Discord: {error}")


def send_telegram(token: str, chat_id: str, title: str, summary: str):
    """Telegram bot으로 메시지를 전송합니다."""
    text = f"*{title}*\n\n{summary}"
    if len(text) > 4096:
        text = text[:4093] + "..."

    payload = json.dumps(
        {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown",
        }
    ).encode("utf-8")

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    try:
        urllib.request.urlopen(req)
        print(f"  {title} → Telegram")
    except urllib.error.URLError as error:
        print(f"  [ERROR] Telegram: {error}")


def format_title(filepath: Path) -> str:
    """디렉터리 경로(YYYYMMDD/HHMMSS)에서 읽기 쉬운 제목을 생성합니다."""
    suffix = "녹음 요약"
    try:
        from datetime import datetime

        time_part = filepath.parent.name
        date_part = filepath.parent.parent.name
        dt = datetime.strptime(f"{date_part} {time_part}", "%Y%m%d %H%M%S")
        return dt.strftime(f"%Y년 %m월 %d일 %H시 %M분 %S초 {suffix}")
    except ValueError:
        return filepath.parent.name


def is_notified(filepath: Path | None) -> bool:
    """파일이 이미 알림 전송되었는지 확인합니다."""
    if filepath is None or not filepath.exists():
        return False
    content = filepath.read_text(encoding="utf-8")
    return NOTIFIED_MARKER in content


def mark_notified(filepath: Path):
    """파일에 알림 전송 마커를 추가합니다."""
    content = filepath.read_text(encoding="utf-8")
    if NOTIFIED_MARKER not in content:
        filepath.write_text(content.rstrip() + f"\n{NOTIFIED_MARKER}\n", encoding="utf-8")


def notify_from_paths(
    transcript_path: Path | None,
    summary_path: Path | None,
    force: bool = False,
):
    """전사/요약 파일 조합을 기준으로 알림을 전송합니다."""
    if not force and (is_notified(summary_path) or is_notified(transcript_path)):
        return False

    summary = None
    marker_target = None
    title_file = None

    if summary_path is not None and summary_path.exists():
        summary = read_summary_file(summary_path)
        if summary:
            marker_target = summary_path
            title_file = summary_path

    if summary is None and transcript_path is not None and transcript_path.exists():
        summary = extract_summary_from_transcript(transcript_path)
        if summary:
            marker_target = transcript_path
            title_file = transcript_path

    # 요약이 없으면 전문을 보내지 않고 스킵
    if not summary or marker_target is None:
        return False

    title = format_title(title_file)
    sent = False

    discord_url = os.environ.get("DISCORD_WEBHOOK_URL")
    if discord_url:
        send_discord(discord_url, title, summary)
        sent = True

    telegram_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if telegram_token and telegram_chat_id:
        send_telegram(telegram_token, telegram_chat_id, title, summary)
        sent = True

    if not sent:
        print("  [SKIP] Discord/Telegram 설정 없음")
        return False

    mark_notified(marker_target)
    return True


def resolve_input_paths(filepath: Path) -> tuple[Path | None, Path | None]:
    """입력 파일이 전사 파일인지 요약 파일인지 판별합니다."""
    filepath = filepath.expanduser()
    if not filepath.exists():
        return None, None

    filepath = filepath.resolve()
    if filepath.name == "summary.md":
        return transcript_path_for(filepath), filepath
    else:
        return filepath, summary_path_for(filepath)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="요약 결과를 Discord/Telegram으로 전송")
    parser.add_argument("--file", type=str, help="특정 전사 또는 요약 파일 전송")
    args = parser.parse_args()

    load_env()

    if args.file:
        transcript_path, summary_path = resolve_input_paths(Path(args.file))
        if transcript_path is None and summary_path is None:
            print(f"File not found: {args.file}")
            raise SystemExit(1)
        notify_from_paths(transcript_path, summary_path, force=True)
        return

    files = sorted(iter_transcript_files(TRANSCRIPTS_DIR), reverse=True)
    sent = 0
    for transcript_path in files:
        if notify_from_paths(transcript_path, summary_path_for(transcript_path)):
            sent += 1

    print(f"  {sent}/{len(files)} 전송됨")


if __name__ == "__main__":
    main()
