#!/usr/bin/env python3
"""
Discord, Telegram으로 요약 결과를 전송합니다.

환경변수:
  DISCORD_WEBHOOK_URL: Discord webhook URL
  TELEGRAM_BOT_TOKEN: Telegram bot token
  TELEGRAM_CHAT_ID: Telegram chat ID
"""

import hashlib
import json
import os
import sys
import urllib.error
import urllib.request
from contextlib import nullcontext
from pathlib import Path

from config import (
    CALL_SUMMARY_SUFFIX,
    CALL_TRANSCRIPT_SUFFIX,
    ENV_FILE,
    PipelineError,
    TRANSCRIPTS_DIR,
    analysis_path_for,
    atomic_write_text,
    is_dataless,
    iter_transcript_files,
    recording_lock,
    run_path_for,
    source_sha256,
    strip_process_markers,
    stt_mode,
    summary_path_for,
    transcript_path_for,
    validate_run_document,
)
from review import ContextValidationError, effective_privacy

NOTIFIED_MARKER = "<!-- notified -->"
# Telegram은 4096자를 넘는 메시지를 받지 않는다. 길이는 UTF-16 단위로 센다.
TELEGRAM_LIMIT = 4096
TRUNCATED_MARKER = "\n..."


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


def send_discord(webhook_url: str, title: str, summary: str) -> bool:
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
        with urllib.request.urlopen(req):
            pass
        print("  summary sent → Discord")
        return True
    except urllib.error.URLError:
        print("  [ERROR] DiscordDeliveryError")
        return False


def _utf16_len(text: str) -> int:
    return len(text.encode("utf-16-le")) // 2


def fit_telegram(text: str, limit: int = TELEGRAM_LIMIT) -> str:
    """Telegram 한도에 맞춰 줄 단위로 자릅니다.

    글자 단위로 자르면 `- [ ]` 같은 줄 가운데서 끊겨 닫히지 않은 `[`나 `*`가 남고,
    Telegram Markdown이 메시지 전체를 400으로 거부한다.
    """
    if _utf16_len(text) <= limit:
        return text
    budget = limit - _utf16_len(TRUNCATED_MARKER)
    kept: list[str] = []
    used = 0
    for line in text.split("\n"):
        size = _utf16_len(line) + (1 if kept else 0)
        if used + size > budget:
            break
        kept.append(line)
        used += size
    if not kept:
        # 첫 줄 하나가 한도를 넘는 경우만 글자 단위로 자른다.
        head = text[:budget]
        while _utf16_len(head) > budget:
            head = head[:-1]
        return head + TRUNCATED_MARKER
    return "\n".join(kept) + TRUNCATED_MARKER


def send_telegram(token: str, chat_id: str, title: str, summary: str) -> bool:
    """Telegram bot으로 메시지를 전송합니다.

    Markdown이 거부되면(400) 같은 글을 서식 없이 한 번 더 보낸다. 요약에 Telegram
    legacy Markdown이 받지 않는 문자(`_`, 짝 없는 `[`)가 남아도 알림은 도착해야 한다.
    """
    text = fit_telegram(f"*{title}*\n\n{summary}")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    for parse_mode in ("Markdown", None):
        message = {"chat_id": chat_id, "text": text}
        if parse_mode:
            message["parse_mode"] = parse_mode
        req = urllib.request.Request(
            url,
            data=json.dumps(message).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(req):
                pass
        except urllib.error.HTTPError as exc:
            if parse_mode and exc.code == 400:
                print("  [WARN] TelegramMarkdownRejected: retry as plain text")
                continue
            print("  [ERROR] TelegramDeliveryError")
            return False
        except urllib.error.URLError:
            print("  [ERROR] TelegramDeliveryError")
            return False
        print("  summary sent → Telegram" + ("" if parse_mode else " (plain text)"))
        return True
    return False


def format_title(filepath: Path) -> str:
    """디렉터리 경로(YYYYMMDD/HHMMSS)에서 읽기 쉬운 제목을 생성합니다."""
    if filepath.name.endswith(CALL_SUMMARY_SUFFIX):
        return filepath.name[: -len(CALL_SUMMARY_SUFFIX)]
    if filepath.name.endswith(CALL_TRANSCRIPT_SUFFIX):
        return filepath.name[: -len(CALL_TRANSCRIPT_SUFFIX)]

    suffix = "녹음 요약"
    try:
        from datetime import datetime

        time_part = filepath.parent.name.split("-", 1)[0]
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
        atomic_write_text(filepath, content.rstrip() + f"\n{NOTIFIED_MARKER}\n")


def _strict_delivery_metadata(transcript_path: Path | None) -> dict | None | bool:
    if transcript_path is None:
        return None
    run_path = run_path_for(transcript_path)
    try:
        if not run_path.exists():
            return (
                False
                if analysis_path_for(transcript_path).exists()
                or stt_mode() != "legacy"
                else None
            )
        metadata = json.loads(run_path.read_text(encoding="utf-8"))
        validate_run_document(metadata)
        source = metadata.get("source")
        recording_id = source.get("audio_sha256") if isinstance(source, dict) else None
        if (
            not isinstance(recording_id, str)
            or len(recording_id) != 64
            or any(char not in "0123456789abcdef" for char in recording_id)
            or metadata.get("recording_id") != recording_id
        ):
            return False
        summary_path = summary_path_for(transcript_path)
        if not summary_path.exists():
            return False
        summary_body_sha256 = hashlib.sha256(
            strip_process_markers(summary_path.read_text(encoding="utf-8")).encode(
                "utf-8"
            )
        ).hexdigest()
        if (
            metadata.get("result") != "processed"
            or metadata.get("mode") == "shadow"
            or metadata.get("review_state") != "finalizable"
            or metadata.get("summary_state") != "fresh"
            or metadata.get("summary_parent_sha256") != source_sha256(transcript_path)
            or metadata.get("summary_body_sha256") != summary_body_sha256
            or not metadata.get("summary_generator_fingerprint")
            or effective_privacy(recording_id, metadata) != "standard"
        ):
            return False
        return metadata
    except (
        OSError,
        UnicodeError,
        ValueError,
        ContextValidationError,
        PipelineError,
    ):
        return False


def _notify_from_paths_unlocked(
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
        sent = send_discord(discord_url, title, summary) or sent

    telegram_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if telegram_token and telegram_chat_id:
        sent = send_telegram(telegram_token, telegram_chat_id, title, summary) or sent

    if not sent:
        print("  [SKIP] Discord/Telegram 설정 없음")
        return False

    mark_notified(marker_target)
    return True


def notify_from_paths(
    transcript_path: Path | None,
    summary_path: Path | None,
    force: bool = False,
):
    metadata = _strict_delivery_metadata(transcript_path)
    if metadata is False:
        print("  notification skipped: artifact not finalizable")
        return False
    source = metadata.get("source") if isinstance(metadata, dict) else None
    recording_id = source.get("audio_sha256") if isinstance(source, dict) else None
    lock = recording_lock(recording_id) if recording_id is not None else nullcontext()
    with lock:
        if isinstance(metadata, dict) and _strict_delivery_metadata(transcript_path) is False:
            return False
        return _notify_from_paths_unlocked(transcript_path, summary_path, force=force)


def resolve_input_paths(filepath: Path) -> tuple[Path | None, Path | None]:
    """입력 파일이 전사 파일인지 요약 파일인지 판별합니다."""
    filepath = filepath.expanduser()
    if not filepath.exists():
        return None, None

    filepath = filepath.resolve()
    if filepath.name == "summary.md" or filepath.name.endswith(CALL_SUMMARY_SUFFIX):
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
    deferred = 0
    for transcript_path in files:
        if is_dataless(transcript_path):
            deferred += 1
            continue
        try:
            if notify_from_paths(transcript_path, summary_path_for(transcript_path)):
                sent += 1
        except OSError as exc:
            # iCloud 산출물이 아직 로컬에 내려오지 않으면 읽기가 EDEADLK로 실패한다.
            # 마커를 남기지 않으므로 다음 pass에서 다시 시도된다. 한 파일 때문에 배치를 죽이지 않는다.
            deferred += 1
            print(
                f"  [WARN] NotifyDeferred:{type(exc).__name__} {transcript_path.parent.name}",
                file=sys.stderr,
            )

    print(f"  {sent}/{len(files)} 전송됨" + (f" (보류 {deferred})" if deferred else ""))


if __name__ == "__main__":
    main()
