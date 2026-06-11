#!/usr/bin/env python3
"""Apple Notes 저수준 접근 모듈.

NoteStore.sqlite를 mode=ro로 직접 읽고, ZDATA(zlib + protobuf)를 디코딩해
노트 본문을 추출한다. 상위 모듈(search.py 등)은 아래 공개 함수만 쓴다:

- refresh_notes_meta()   캐시 갱신 (파일 수집 시 1회 호출)
- all_note_paths()       노트 가상 Path 목록
- is_note(path)          가상 Path 판별
- note_meta(path)        {pk, title, folder, locked, mtime, ...} (없으면 {})
- note_body(path)        본문 텍스트 (잠긴 노트는 "")
- note_haystack(path)    title + body (키워드 검색용)

Apple Notes는 가상 Path(`apple-note:<Z_PK>`)로 표현해 다른 소스와 동일한
list[Path] 인터페이스를 유지한다.
"""

import gzip
import sqlite3
import subprocess
import sys
import time
import zlib
from datetime import datetime, timezone
from pathlib import Path

APPLE_NOTES_DB = (
    Path.home() / "Library/Group Containers/group.com.apple.notes/NoteStore.sqlite"
)

NOTE_PATH_PREFIX = "apple-note:"

# Apple Notes 메타 캐시 (Path → dict). refresh_notes_meta() 호출 시 갱신.
_NOTES_META: dict[Path, dict] = {}


def is_note(path: Path) -> bool:
    """Apple Notes 가상 Path인지 판별."""
    return str(path).startswith(NOTE_PATH_PREFIX)


def _note_path(pk: int) -> Path:
    return Path(f"{NOTE_PATH_PREFIX}{pk}")


# ── protobuf / zlib 디코딩 ────────────────────────────────────────────


def _read_varint(data: bytes, pos: int) -> tuple[int, int]:
    result, shift = 0, 0
    while pos < len(data):
        b = data[pos]
        pos += 1
        result |= (b & 0x7F) << shift
        if not (b & 0x80):
            return result, pos
        shift += 7
        if shift > 64:
            raise ValueError("varint too long")
    raise ValueError("truncated varint")


def _pb_find_field(data: bytes, target_fn: int) -> bytes | None:
    """단순 protobuf 파서: 첫 번째 매칭 length-delimited 필드 반환."""
    pos = 0
    while pos < len(data):
        try:
            tag, pos = _read_varint(data, pos)
        except ValueError:
            return None
        wt = tag & 0x07
        fn = tag >> 3
        if wt == 0:
            try:
                _, pos = _read_varint(data, pos)
            except ValueError:
                return None
        elif wt == 2:
            try:
                length, pos = _read_varint(data, pos)
            except ValueError:
                return None
            if pos + length > len(data):
                return None
            if fn == target_fn:
                return data[pos : pos + length]
            pos += length
        elif wt == 1:
            pos += 8
        elif wt == 5:
            pos += 4
        else:
            return None
    return None


def _decompress_zdata(blob: bytes) -> bytes:
    if blob[:2] == b"\x1f\x8b":
        return gzip.decompress(blob)
    try:
        return zlib.decompress(blob)
    except zlib.error:
        return zlib.decompress(blob, -zlib.MAX_WBITS)


def _decode_note_body(zdata: bytes) -> str:
    """ZDATA(zlib + protobuf) → 본문 텍스트.

    경로: NoteStoreProto -> document(2) -> note(3) -> note_text(2)
    """
    raw = _decompress_zdata(zdata)
    doc = _pb_find_field(raw, 2)
    if doc is None:
        return ""
    note = _pb_find_field(doc, 3)
    if note is None:
        return ""
    text = _pb_find_field(note, 2)
    if text is None:
        return ""
    return text.decode("utf-8", errors="replace")


def _core_data_to_dt(ts: float | None) -> datetime | None:
    """Core Data timestamp(2001-01-01 UTC 기준 초)를 로컬 naive datetime으로."""
    if ts is None:
        return None
    return datetime.fromtimestamp(ts + 978307200, tz=timezone.utc).astimezone().replace(tzinfo=None)


# ── sqlite ro 읽기 + 캐시 ─────────────────────────────────────────────


def _ensure_notes_synced(first_change_window: float = 15.0, settle: float = 2.0) -> None:
    """Notes.app이 안 떠 있으면 백그라운드로 띄워 iCloud 동기화를 트리거한다.

    macOS Notes는 앱이 실행 중일 때만 iCloud 동기화를 한다. 앱이 꺼져 있던
    동안 다른 기기(iPhone 등)에서 쓴 메모는 로컬 NoteStore.sqlite에 존재하지
    않아 mode=ro 직쿼리로는 절대 잡히지 않는다. (2026-06-11 실측: 9일치 메모
    누락 → 앱 실행 14초 뒤 동기화·체크포인트로 해소. WAL 가독성은 문제없음.)

    앱이 이미 실행 중이면 로컬 DB를 최신으로 간주하고 즉시 반환한다.
    우리가 띄운 Notes.app은 종료하지 않으므로 대기 비용은 세션당 1회다.
    """
    if subprocess.run(["pgrep", "-x", "Notes"], capture_output=True).returncode == 0:
        return
    wal = APPLE_NOTES_DB.with_name(APPLE_NOTES_DB.name + "-wal")

    def latest_mtime() -> float:
        m = APPLE_NOTES_DB.stat().st_mtime
        if wal.exists():
            m = max(m, wal.stat().st_mtime)
        return m

    try:
        subprocess.run(["open", "-gja", "Notes"], capture_output=True, timeout=10)
    except (OSError, subprocess.TimeoutExpired):
        return
    print("Notes.app 미실행 — iCloud 동기화 대기 중 (최대 15초)...", file=sys.stderr)
    before = latest_mtime()
    deadline = time.time() + first_change_window
    last_change: float | None = None
    while time.time() < deadline:
        time.sleep(0.5)
        now_m = latest_mtime()
        if now_m != before:
            before = now_m
            last_change = time.time()
            deadline = max(deadline, time.time() + settle + 0.5)
        elif last_change is not None and time.time() - last_change >= settle:
            break  # 변경이 멈춘 지 settle초 — 동기화 안정화로 간주


def refresh_notes_meta() -> None:
    """NoteStore.sqlite를 mode=ro로 직접 읽어 캐시를 갱신."""
    _NOTES_META.clear()
    if not APPLE_NOTES_DB.exists():
        return
    _ensure_notes_synced()
    try:
        conn = sqlite3.connect(f"file:{APPLE_NOTES_DB}?mode=ro", uri=True)
    except sqlite3.OperationalError:
        return
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT Z_PK, ZTITLE2 FROM ZICCLOUDSYNCINGOBJECT WHERE ZTITLE2 IS NOT NULL"
        )
        folder_map = {pk: name for pk, name in cur.fetchall()}

        cur.execute(
            """
            SELECT
              c.Z_PK, c.ZTITLE1, c.ZMODIFICATIONDATE1,
              c.ZFOLDER, c.ZCRYPTOINITIALIZATIONVECTOR, d.ZDATA
            FROM ZICCLOUDSYNCINGOBJECT c
            LEFT JOIN ZICNOTEDATA d ON d.ZNOTE = c.Z_PK
            WHERE c.ZTITLE1 IS NOT NULL
            """
        )
        for pk, title, mtime_raw, folder_pk, crypto_iv, zdata in cur.fetchall():
            path = _note_path(pk)
            _NOTES_META[path] = {
                "pk": pk,
                "title": title,
                "mtime": _core_data_to_dt(mtime_raw),
                "folder": folder_map.get(folder_pk, "_unfiled"),
                "locked": crypto_iv is not None,
                "zdata": zdata,
                "body": None,  # lazy 디코딩
            }
    finally:
        conn.close()


# ── 공개 접근자 ───────────────────────────────────────────────────────


def all_note_paths() -> list[Path]:
    """캐시된 모든 노트의 가상 Path."""
    return list(_NOTES_META.keys())


def note_meta(path: Path) -> dict:
    """노트 메타(dict). 없으면 빈 dict."""
    return _NOTES_META.get(path, {})


def note_body(path: Path) -> str:
    """캐시된 본문 반환. 처음 호출 시 디코딩. 잠긴 노트는 ""."""
    meta = _NOTES_META.get(path)
    if not meta or meta.get("locked") or not meta.get("zdata"):
        return ""
    if meta["body"] is None:
        try:
            meta["body"] = _decode_note_body(meta["zdata"])
        except Exception:
            meta["body"] = ""
    return meta["body"]


def note_haystack(path: Path) -> str:
    """키워드 검색용 텍스트 (제목 + 본문)."""
    meta = _NOTES_META.get(path, {})
    return (meta.get("title") or "") + "\n" + note_body(path)
