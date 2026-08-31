#!/usr/bin/env python3
"""Tiro 회의 노트를 CLI로 조회한다. 전사는 파일로만 받는다."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

from config import RUNTIME_DIR

CONFIG_PATH = Path(
    os.environ.get("VOICE_MEMOS_TIRO_CONFIG", "~/.config/voice-memos/tiro.json")
).expanduser()
TOKEN_KEY = "TIRO_TOKEN"
LABEL = "[티로]"


class TiroError(RuntimeError):
    pass


def require_binaries() -> None:
    missing = [name for name in ("agents-env", "tiro") if shutil.which(name) is None]
    if missing:
        joined = ", ".join(missing)
        raise TiroError(
            f"{joined} 가 PATH에 없다. tiro는 `pnpm add -g @theplato/tiro-cli`, "
            "토큰은 agents-env의 TIRO_TOKEN이다."
        )


def tiro_argv(tiro_args: list[str], *, workspace: str | None = None) -> list[str]:
    argv = ["agents-env", "run", TOKEN_KEY, "--", "tiro", "--json", *tiro_args]
    if workspace:
        argv.extend(["--workspace", workspace])
    return argv


def run_tiro(tiro_args: list[str], *, workspace: str | None = None) -> str:
    require_binaries()
    result = subprocess.run(
        tiro_argv(tiro_args, workspace=workspace),
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip() or f"exit {result.returncode}"
        raise TiroError(detail)
    return result.stdout


def parse_ndjson(raw: str) -> tuple[list[dict], str | None]:
    notes: list[dict] = []
    cursor = None
    for line in raw.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(item, dict):
            continue
        if item.get("_cursor"):
            cursor = str(item["_cursor"])
            continue
        if item.get("ok") is False:
            error = item.get("error") or {}
            raise TiroError(error.get("message") or line)
        notes.append(item)
    return notes, cursor


def list_workspaces() -> list[dict]:
    stdout = run_tiro(["wiki", "workspaces"])
    payload = stdout.strip()
    if not payload:
        return []
    try:
        parsed = json.loads(payload)
    except json.JSONDecodeError:
        notes, _ = parse_ndjson(payload)
        return notes
    if isinstance(parsed, list):
        return [item for item in parsed if isinstance(item, dict)]
    if isinstance(parsed, dict) and parsed.get("guid"):
        return [parsed]
    if isinstance(parsed, dict) and isinstance(parsed.get("data"), list):
        return [item for item in parsed["data"] if isinstance(item, dict)]
    return []


def save_workspace(guid: str) -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(
        json.dumps({"workspace": guid}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def resolve_workspace() -> str:
    env = os.environ.get("TIRO_WORKSPACE", "").strip()
    if env:
        return env
    if CONFIG_PATH.exists():
        try:
            data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise TiroError(f"{CONFIG_PATH} 를 읽지 못했다: {error}") from error
        workspace = data.get("workspace") if isinstance(data, dict) else None
        if isinstance(workspace, str) and workspace.strip():
            return workspace.strip()
    workspaces = list_workspaces()
    guids = [
        str(item["guid"]).strip()
        for item in workspaces
        if isinstance(item.get("guid"), str) and str(item["guid"]).strip()
    ]
    if len(guids) == 1:
        save_workspace(guids[0])
        return guids[0]
    if not guids:
        raise TiroError("접근 가능한 Tiro 워크스페이스가 없다.")
    lines = [
        "워크스페이스가 여러 개다. TIRO_WORKSPACE 또는 ~/.config/voice-memos/tiro.json 에 guid를 넣어라."
    ]
    for item in workspaces:
        guid = item.get("guid")
        name = item.get("name") or ""
        if guid:
            lines.append(f"  {guid}  {name}")
    raise TiroError("\n".join(lines))


def date_flags(date_str: str) -> dict[str, str]:
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    if date_str == "today":
        start, end = today, today + timedelta(days=1)
    elif date_str == "yesterday":
        start, end = today - timedelta(days=1), today
    elif date_str == "this-week":
        start, end = today - timedelta(days=today.weekday()), today + timedelta(days=1)
    elif date_str == "this-month":
        start, end = today.replace(day=1), today + timedelta(days=1)
    else:
        if re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
            start = datetime.strptime(date_str, "%Y-%m-%d")
            end = start + timedelta(days=1)
        elif re.match(r"^\d{4}-\d{2}$", date_str):
            start = datetime.strptime(date_str, "%Y-%m")
            end = (
                start.replace(year=start.year + 1, month=1)
                if start.month == 12
                else start.replace(month=start.month + 1)
            )
        elif re.match(r"^\d{4}$", date_str):
            start = datetime.strptime(date_str, "%Y")
            end = start.replace(year=start.year + 1)
        else:
            raise TiroError(f"지원하지 않는 날짜 형식: {date_str}")
    return {
        "since": start.strftime("%Y-%m-%d"),
        "until": end.strftime("%Y-%m-%d"),
    }


def format_note(note: dict) -> str:
    title = note.get("title") or "(제목 없음)"
    created = str(note.get("createdAt") or "")[:10]
    guid = note.get("guid") or ""
    seconds = note.get("recordingDurationSeconds")
    duration = ""
    if isinstance(seconds, int) and seconds > 0:
        duration = f"  {seconds // 60}m"
    return f"{LABEL} {created}  {guid}{duration}  {title}"


def cmd_list(args: argparse.Namespace) -> int:
    workspace = resolve_workspace()
    tiro_args = ["notes", "list", "--limit", str(args.limit)]
    if args.date:
        flags = date_flags(args.date)
        tiro_args.extend(["--since", flags["since"], "--until", flags["until"]])
    notes, _ = parse_ndjson(run_tiro(tiro_args, workspace=workspace))
    if args.count:
        print(len(notes))
        return 0
    for note in notes:
        print(format_note(note))
        if not args.no_preview and note.get("webUrl"):
            print(f"  {note['webUrl']}")
    return 0


def cmd_search(args: argparse.Namespace) -> int:
    workspace = resolve_workspace()
    tiro_args = ["notes", "search", args.keyword, "--limit", str(args.limit)]
    if args.date:
        flags = date_flags(args.date)
        tiro_args.extend(["--since", flags["since"], "--until", flags["until"]])
    notes, _ = parse_ndjson(run_tiro(tiro_args, workspace=workspace))
    for note in notes:
        print(format_note(note))
        if not args.no_preview and note.get("webUrl"):
            print(f"  {note['webUrl']}")
    return 0


def cmd_get(args: argparse.Namespace) -> int:
    stdout = run_tiro(["notes", "get", args.guid])
    print(stdout.rstrip())
    return 0


def default_transcript_path(guid: str) -> Path:
    directory = RUNTIME_DIR / "tiro"
    directory.mkdir(parents=True, exist_ok=True)
    safe = "".join(char if char.isalnum() or char in "-_" else "-" for char in guid)
    return directory / f"{safe}.md"


def cmd_transcript(args: argparse.Namespace) -> int:
    output = (
        Path(args.output).expanduser()
        if args.output
        else default_transcript_path(args.guid)
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    tiro_args = [
        "notes",
        "transcript",
        args.guid,
        "--format",
        "md",
        "--output",
        str(output),
        "--force",
    ]
    if args.no_timestamps:
        tiro_args.append("--no-timestamps")
    stdout = run_tiro(tiro_args)
    print(stdout.rstrip())
    print(output)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Tiro 회의 노트 조회")
    sub = parser.add_subparsers(dest="command", required=True)

    listing = sub.add_parser("list", help="최근 노트 메타")
    listing.add_argument("--limit", type=int, default=10)
    listing.add_argument("--date")
    listing.add_argument("--count", action="store_true")
    listing.add_argument("--no-preview", action="store_true")
    listing.set_defaults(func=cmd_list)

    searching = sub.add_parser("search", help="키워드 검색")
    searching.add_argument("keyword")
    searching.add_argument("--limit", type=int, default=10)
    searching.add_argument("--date")
    searching.add_argument("--no-preview", action="store_true")
    searching.set_defaults(func=cmd_search)

    getting = sub.add_parser("get", help="노트 메타 JSON")
    getting.add_argument("guid")
    getting.set_defaults(func=cmd_get)

    transcript = sub.add_parser("transcript", help="전사를 파일로 저장")
    transcript.add_argument("guid")
    transcript.add_argument("--output")
    transcript.add_argument("--no-timestamps", action="store_true")
    transcript.set_defaults(func=cmd_transcript)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        return args.func(args)
    except TiroError as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
