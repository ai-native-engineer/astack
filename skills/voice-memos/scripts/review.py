#!/usr/bin/env python3
"""Local context, review, and append-only correction state."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sqlite3
import sys
import tempfile
import unicodedata
import uuid
from contextlib import nullcontext
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import quote

from config import (
    AnalysisSchemaError,
    CONTEXT_DIR,
    PipelineError,
    REVIEW_DB_PATH,
    RecordingBusy,
    recording_lock,
    source_sha256,
    validate_analysis_document,
)


SCHEMA_VERSION = 1
DB_SCHEMA_VERSION = 1
CONTEXT_FIELDS = {
    "schema_version",
    "privacy",
    "topic",
    "project",
    "participants",
    "terms",
}
PRIVACY_MODES = {"standard", "local"}
DECISIONS = {"keep", "apple_alternative", "claude_suggestion", "manual"}
HEX64_RE = re.compile(r"^[0-9a-f]{64}$")
EVENT_ID_RE = re.compile(r"^[A-Za-z0-9._-]{1,64}$")
PROJECT_SCOPE_RE = re.compile(r"^project:[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
DEFAULT_CONTEXT_DIR = CONTEXT_DIR
DEFAULT_DB_PATH = REVIEW_DB_PATH


class ContextValidationError(ValueError):
    pass


class PrivacyModeValidationError(ContextValidationError):
    pass


class CorrectionConflict(ValueError):
    pass


class CorrectionStoreError(PipelineError):
    code = "CorrectionStoreError"


def _canonical_hash(value: dict[str, Any]) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _clean_text(
    value: Any,
    field: str,
    *,
    max_bytes: int,
    allow_empty: bool = True,
) -> str:
    if not isinstance(value, str):
        raise ContextValidationError(f"{field}: string required")
    value = value.strip()
    if not allow_empty and not value:
        raise ContextValidationError(f"{field}: empty value")
    if any(unicodedata.category(char) == "Cc" for char in value):
        raise ContextValidationError(f"{field}: control character")
    if len(value.encode("utf-8")) > max_bytes:
        raise ContextValidationError(f"{field}: exceeds {max_bytes} UTF-8 bytes")
    return value


def validate_privacy(value: Any) -> str:
    if not isinstance(value, str) or value not in PRIVACY_MODES:
        raise PrivacyModeValidationError(
            "PrivacyModeValidationError: privacy must be standard or local"
        )
    return value


def _clean_list(value: Any, field: str, *, max_items: int) -> list[str]:
    if not isinstance(value, list):
        raise ContextValidationError(f"{field}: array required")
    if len(value) > max_items:
        raise ContextValidationError(f"{field}: exceeds {max_items} items")
    result: list[str] = []
    seen: set[str] = set()
    for index, item in enumerate(value):
        item = _clean_text(
            item,
            f"{field}[{index}]",
            max_bytes=128,
            allow_empty=False,
        )
        if len(item.split()) > 2:
            raise ContextValidationError(f"{field}[{index}]: expected one or two words")
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def validate_context(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ContextValidationError("context: object required")
    unknown = sorted(set(value) - CONTEXT_FIELDS)
    if unknown:
        raise ContextValidationError(f"context: unknown fields: {', '.join(unknown)}")
    schema_version = value.get("schema_version")
    if isinstance(schema_version, bool) or schema_version != SCHEMA_VERSION:
        raise ContextValidationError("schema_version: expected 1")
    return {
        "schema_version": SCHEMA_VERSION,
        "privacy": validate_privacy(value["privacy"]) if "privacy" in value else "standard",
        "topic": _clean_text(value.get("topic", ""), "topic", max_bytes=512),
        "project": _clean_text(value.get("project", ""), "project", max_bytes=128),
        "participants": _clean_list(
            value.get("participants", []), "participants", max_items=50
        ),
        "terms": _clean_list(value.get("terms", []), "terms", max_items=100),
    }


def context_fingerprint(context: dict[str, Any]) -> str:
    return _canonical_hash(validate_context(context))


def context_terms_fingerprint(terms: list[str]) -> str:
    return hashlib.sha256("\0".join(terms).encode("utf-8")).hexdigest()


def context_for_recording(
    recording_id: str, directory: Path = DEFAULT_CONTEXT_DIR
) -> tuple[dict[str, Any], bool]:
    path = context_path(recording_id, directory)
    if path.exists():
        return load_context(path), False
    return validate_context({"schema_version": SCHEMA_VERSION}), True


def effective_privacy(
    recording_id: str | None,
    run_metadata: dict[str, Any],
    directory: Path = DEFAULT_CONTEXT_DIR,
) -> str:
    """Fail closed on malformed current policy; local wins over stale metadata."""
    run_privacy = (
        validate_privacy(run_metadata["privacy"])
        if "privacy" in run_metadata
        else "standard"
    )
    if recording_id is None:
        return run_privacy
    sidecar = context_path(recording_id, directory)
    if not sidecar.exists():
        return run_privacy
    current_privacy = load_context(sidecar)["privacy"]
    return "local" if "local" in {run_privacy, current_privacy} else "standard"


def build_context_pack(
    context: dict[str, Any],
    store: "ReviewStore",
    common_vocab: Path,
) -> dict[str, Any]:
    """Apply explicit, saved project/global, then common priority exactly once."""
    context = validate_context(context)
    ordered = [*context["participants"], *context["terms"]]
    ordered.extend(store.active_terms(project=context["project"]))
    if common_vocab.exists():
        try:
            ordered.extend(common_vocab.read_text(encoding="utf-8").splitlines())
        except (OSError, UnicodeError) as exc:
            raise ContextValidationError(f"common vocab read failed: {exc}") from exc

    selected: list[str] = []
    dropped: list[str] = []
    seen: set[str] = set()
    for raw in ordered:
        term = raw.strip()
        if not term or term.startswith("#") or term in seen:
            continue
        seen.add(term)
        invalid = (
            len(term.split()) > 2
            or len(term.encode("utf-8")) > 128
            or any(unicodedata.category(char) == "Cc" for char in term)
        )
        if invalid or len(selected) == 100:
            dropped.append(term)
        else:
            selected.append(term)
    return {
        "selected": selected,
        "dropped": dropped,
        "fingerprint": context_terms_fingerprint(selected),
    }


def recording_id_for(path: Path) -> str:
    path = path.expanduser()
    if not path.is_file():
        raise ContextValidationError(f"audio file not found: {path}")
    try:
        return source_sha256(path)
    except OSError as exc:
        raise ContextValidationError(f"audio read failed: {path}: {exc}") from exc


def context_path(recording_id: str, directory: Path = DEFAULT_CONTEXT_DIR) -> Path:
    _validate_hash(recording_id, "recording_id")
    return directory.expanduser() / f"{recording_id}.json"


def load_context(path: Path) -> dict[str, Any]:
    try:
        if path.stat().st_size > 64 * 1024:
            raise ContextValidationError(f"context exceeds 64 KiB: {path}")
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ContextValidationError(f"context read failed: {path}: {exc}") from exc
    return validate_context(value)


def _atomic_write(path: Path, content: str, *, mode: int = 0o600) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            delete=False,
        ) as handle:
            temp_path = Path(handle.name)
            os.chmod(temp_path, mode)
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, path)
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)


def write_context(
    audio_path: Path,
    *,
    project: str | None = None,
    participants: Iterable[str] = (),
    terms: Iterable[str] = (),
    privacy: str | None = None,
    directory: Path = DEFAULT_CONTEXT_DIR,
    reprocess: bool = False,
) -> tuple[str, Path, dict[str, Any]]:
    recording_id = recording_id_for(audio_path)
    path = context_path(recording_id, directory)
    with recording_lock(recording_id):
        if path.exists():
            context = load_context(path)
        else:
            context = validate_context({"schema_version": SCHEMA_VERSION})

        if project is not None:
            context["project"] = project
        if privacy is not None:
            context["privacy"] = privacy
        context["participants"] = list(
            dict.fromkeys([*context["participants"], *participants])
        )
        context["terms"] = list(dict.fromkeys([*context["terms"], *terms]))
        context = validate_context(context)

        _atomic_write(
            path,
            json.dumps(context, ensure_ascii=False, indent=2) + "\n",
        )
        if reprocess:
            marker = path.with_suffix(".reprocess")
            _atomic_write(
                marker,
                datetime.now(timezone.utc).isoformat().replace("+00:00", "Z") + "\n",
            )
    return recording_id, path, context


def utf8_slice(text: str, start_byte: int, end_byte: int) -> str:
    if any(isinstance(value, bool) or not isinstance(value, int) for value in (start_byte, end_byte)):
        raise CorrectionConflict("CorrectionConflict: byte offsets must be integers")
    encoded = text.encode("utf-8")
    if start_byte < 0 or end_byte <= start_byte or end_byte > len(encoded):
        raise CorrectionConflict("CorrectionConflict: byte span out of range")
    try:
        return encoded[start_byte:end_byte].decode("utf-8")
    except UnicodeDecodeError as exc:
        raise CorrectionConflict("CorrectionConflict: offset is not a UTF-8 boundary") from exc


def validate_exact_span(
    text: str,
    start_byte: int,
    end_byte: int,
    original_text: str,
) -> str:
    actual = utf8_slice(text, start_byte, end_byte)
    if actual != original_text:
        raise CorrectionConflict("CorrectionConflict: original_text does not match byte span")
    return actual


def _validate_hash(value: str, field: str) -> str:
    if not isinstance(value, str) or not HEX64_RE.fullmatch(value):
        raise CorrectionConflict(f"CorrectionConflict: invalid {field}")
    return value


def segment_fingerprint(
    source_audio_sha256: str,
    start_ms: int,
    end_ms: int,
    text: str,
) -> str:
    _validate_hash(source_audio_sha256, "source_audio_sha256")
    if any(isinstance(value, bool) or not isinstance(value, int) for value in (start_ms, end_ms)):
        raise CorrectionConflict("CorrectionConflict: segment times must be integer milliseconds")
    if start_ms < 0 or end_ms < start_ms or not isinstance(text, str):
        raise CorrectionConflict("CorrectionConflict: invalid segment")
    return _canonical_hash(
        {
            "end_ms": end_ms,
            "source_audio_sha256": source_audio_sha256,
            "start_ms": start_ms,
            "text": text,
        }
    )


def target_id(
    fingerprint: str,
    start_byte: int,
    end_byte: int,
    original_text: str,
) -> str:
    _validate_hash(fingerprint, "segment_fingerprint")
    if any(isinstance(value, bool) or not isinstance(value, int) for value in (start_byte, end_byte)):
        raise CorrectionConflict("CorrectionConflict: byte offsets must be integers")
    if start_byte < 0 or end_byte <= start_byte:
        raise CorrectionConflict("CorrectionConflict: invalid byte span")
    if not isinstance(original_text, str):
        raise CorrectionConflict("CorrectionConflict: original_text must be a string")
    return _canonical_hash(
        {
            "end_byte": end_byte,
            "original_text": original_text,
            "segment_fingerprint": fingerprint,
            "start_byte": start_byte,
        }
    )


def term_target_id(term: str, scope: str) -> str:
    return _canonical_hash({"scope": scope, "term": term})


CREATE_SCHEMA = (
    """
    CREATE TABLE IF NOT EXISTS events (
        event_id TEXT PRIMARY KEY CHECK(length(event_id) BETWEEN 1 AND 64 AND event_id NOT GLOB '*[^A-Za-z0-9._-]*'),
        recording_id TEXT NOT NULL CHECK(length(recording_id) = 64 AND recording_id NOT GLOB '*[^0-9a-f]*'),
        target_id TEXT NOT NULL CHECK(length(target_id) = 64 AND target_id NOT GLOB '*[^0-9a-f]*'),
        event_type TEXT NOT NULL CHECK(event_type IN ('decision', 'save_term', 'revoke_term')),
        segment_id TEXT NOT NULL,
        segment_fingerprint TEXT NOT NULL CHECK(length(segment_fingerprint) = 64 AND segment_fingerprint NOT GLOB '*[^0-9a-f]*'),
        revision INTEGER NOT NULL CHECK(revision > 0),
        supersedes_event_id TEXT REFERENCES events(event_id),
        decision TEXT CHECK(decision IN ('keep', 'apple_alternative', 'claude_suggestion', 'manual')),
        start_byte INTEGER,
        end_byte INTEGER,
        original_text TEXT,
        replacement TEXT,
        term TEXT,
        term_scope TEXT,
        created_at TEXT NOT NULL,
        UNIQUE(recording_id, target_id, revision),
        CHECK((revision = 1 AND supersedes_event_id IS NULL) OR (revision > 1 AND supersedes_event_id IS NOT NULL)),
        CHECK(
            (event_type = 'decision'
                AND decision IS NOT NULL
                AND start_byte IS NOT NULL AND start_byte >= 0
                AND end_byte IS NOT NULL AND end_byte > start_byte
                AND original_text IS NOT NULL
                AND ((decision = 'keep' AND replacement IS NULL)
                     OR (decision != 'keep' AND replacement IS NOT NULL AND length(CAST(replacement AS BLOB)) <= 4096))
                AND term IS NULL AND term_scope IS NULL)
            OR
            (event_type IN ('save_term', 'revoke_term')
                AND decision IS NULL AND start_byte IS NULL AND end_byte IS NULL
                AND original_text IS NULL AND replacement IS NULL
                AND term IS NOT NULL AND length(CAST(term AS BLOB)) BETWEEN 1 AND 128
                AND (term_scope = 'global' OR (substr(term_scope, 1, 8) = 'project:'
                    AND length(term_scope) BETWEEN 9 AND 72
                    AND instr(term_scope, '/') = 0 AND instr(term_scope, '\\') = 0
                    AND instr(term_scope, '..') = 0 AND instr(term_scope, ' ') = 0)))
        )
    )
    """,
    "CREATE INDEX IF NOT EXISTS events_recording_segment ON events(recording_id, segment_id, revision)",
    """
    CREATE TRIGGER IF NOT EXISTS events_revision_chain
    BEFORE INSERT ON events
    WHEN NEW.revision > 1 AND NOT EXISTS (
        SELECT 1 FROM events previous
        WHERE previous.event_id = NEW.supersedes_event_id
          AND previous.recording_id = NEW.recording_id
          AND previous.target_id = NEW.target_id
          AND previous.revision = NEW.revision - 1
    )
    BEGIN
        SELECT RAISE(ABORT, 'broken revision chain');
    END
    """,
    """
    CREATE TRIGGER IF NOT EXISTS events_append_only_update
    BEFORE UPDATE ON events
    BEGIN
        SELECT RAISE(ABORT, 'events are append-only');
    END
    """,
    """
    CREATE TRIGGER IF NOT EXISTS events_append_only_delete
    BEFORE DELETE ON events
    BEGIN
        SELECT RAISE(ABORT, 'events are append-only');
    END
    """,
)


class ReviewStore:
    def __init__(self, path: Path = DEFAULT_DB_PATH):
        self.path = path.expanduser().resolve()
        self.connection: sqlite3.Connection | None = None
        self.read_only = False
        self.error: str | None = None
        existed = self.path.exists()
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            os.chmod(self.path.parent, 0o700)
            if existed:
                os.chmod(self.path, 0o600)
            else:
                self.path.touch(mode=0o600, exist_ok=False)
            connection = sqlite3.connect(self.path, timeout=5, isolation_level=None)
            connection.row_factory = sqlite3.Row
            connection.execute("PRAGMA foreign_keys = ON")
            connection.execute("PRAGMA busy_timeout = 5000")
            self.connection = connection
            result = [row[0] for row in connection.execute("PRAGMA quick_check")]
            if result != ["ok"]:
                raise CorrectionStoreError(f"quick_check failed: {result}")
            self._migrate(existed)
            os.chmod(self.path, 0o600)
        except (OSError, sqlite3.DatabaseError, CorrectionStoreError) as exc:
            if self.connection is not None:
                self.connection.close()
            self._open_read_only(exc)

    def _open_read_only(self, error: Exception) -> None:
        self.read_only = True
        self.error = (
            f"CorrectionStoreError: {error}; restore the newest {self.path.name}.backup-* "
            "or move the damaged database before retrying"
        )
        self.connection = None
        if not self.path.exists():
            return
        try:
            uri = f"file:{quote(str(self.path), safe='/')}?mode=ro"
            connection = sqlite3.connect(uri, uri=True, timeout=5, isolation_level=None)
            connection.row_factory = sqlite3.Row
            connection.execute("PRAGMA query_only = ON")
            self.connection = connection
        except sqlite3.DatabaseError:
            self.connection = None

    def _migrate(self, existed: bool) -> None:
        assert self.connection is not None
        version = self.connection.execute("PRAGMA user_version").fetchone()[0]
        if version > DB_SCHEMA_VERSION:
            raise CorrectionStoreError(f"unsupported schema version: {version}")
        if version == DB_SCHEMA_VERSION:
            return

        if existed and self.path.stat().st_size:
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
            backup_path = self.path.with_name(f"{self.path.name}.backup-{stamp}")
            backup_path.touch(mode=0o600, exist_ok=False)
            backup = sqlite3.connect(backup_path)
            try:
                self.connection.backup(backup)
            finally:
                backup.close()
            os.chmod(backup_path, 0o600)

        try:
            self.connection.execute("BEGIN IMMEDIATE")
            for statement in CREATE_SCHEMA:
                self.connection.execute(statement)
            self.connection.execute(f"PRAGMA user_version = {DB_SCHEMA_VERSION}")
            self.connection.execute("COMMIT")
        except Exception:
            if self.connection.in_transaction:
                self.connection.execute("ROLLBACK")
            raise

    def close(self) -> None:
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def __enter__(self) -> ReviewStore:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def _writable(self) -> sqlite3.Connection:
        if self.read_only or self.connection is None:
            raise CorrectionStoreError(self.error or "CorrectionStoreError: store unavailable")
        return self.connection

    def next_revision(self, recording_id: str, target: str) -> tuple[int, str | None]:
        connection = self.connection
        if connection is None:
            raise CorrectionStoreError(self.error or "CorrectionStoreError: store unavailable")
        row = connection.execute(
            """
            SELECT event_id, revision FROM events
            WHERE recording_id = ? AND target_id = ?
            ORDER BY revision DESC LIMIT 1
            """,
            (recording_id, target),
        ).fetchone()
        return (1, None) if row is None else (row["revision"] + 1, row["event_id"])

    def _append(self, values: dict[str, Any], event_id: str | None = None) -> dict[str, Any]:
        connection = self._writable()
        event_id = event_id or str(uuid.uuid4())
        if not EVENT_ID_RE.fullmatch(event_id):
            raise CorrectionStoreError("CorrectionStoreError: invalid event_id")
        try:
            connection.execute("BEGIN IMMEDIATE")
            existing = connection.execute(
                "SELECT * FROM events WHERE event_id = ?", (event_id,)
            ).fetchone()
            if existing is not None:
                for key, value in values.items():
                    if existing[key] != value:
                        raise CorrectionStoreError("event_id already belongs to another event")
                connection.execute("COMMIT")
                return dict(existing)

            revision, previous_id = self.next_revision(
                values["recording_id"], values["target_id"]
            )
            row = {
                **values,
                "event_id": event_id,
                "revision": revision,
                "supersedes_event_id": previous_id,
                "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            }
            columns = tuple(row)
            connection.execute(
                f"INSERT INTO events ({', '.join(columns)}) VALUES ({', '.join('?' for _ in columns)})",
                tuple(row[column] for column in columns),
            )
            connection.execute("COMMIT")
            return row
        except Exception as exc:
            if connection.in_transaction:
                connection.execute("ROLLBACK")
            if isinstance(exc, CorrectionStoreError):
                raise
            raise CorrectionStoreError(f"CorrectionStoreError: {exc}") from exc

    def append_decision(
        self,
        *,
        recording_id: str,
        segment_id: str,
        source_audio_sha256: str,
        start_ms: int,
        end_ms: int,
        segment_text: str,
        start_byte: int,
        end_byte: int,
        original_text: str,
        decision: str,
        replacement: str | None = None,
        event_id: str | None = None,
    ) -> dict[str, Any]:
        _validate_hash(recording_id, "recording_id")
        if recording_id != source_audio_sha256:
            raise CorrectionConflict("CorrectionConflict: recording ID does not match source audio")
        if not isinstance(segment_id, str) or not segment_id or len(segment_id) > 128:
            raise CorrectionConflict("CorrectionConflict: invalid segment_id")
        if any(unicodedata.category(char) == "Cc" for char in segment_id):
            raise CorrectionConflict("CorrectionConflict: segment_id has control character")
        if decision not in DECISIONS:
            raise CorrectionConflict("CorrectionConflict: unknown decision")
        validate_exact_span(segment_text, start_byte, end_byte, original_text)
        if decision == "keep":
            if replacement is not None:
                raise CorrectionConflict("CorrectionConflict: keep cannot have replacement")
        else:
            if not isinstance(replacement, str):
                raise CorrectionConflict("CorrectionConflict: replacement must be a string")
            if any(unicodedata.category(char) == "Cc" for char in replacement):
                raise CorrectionConflict("CorrectionConflict: replacement has control character")
            if len(replacement.encode("utf-8")) > 4096:
                raise CorrectionConflict("CorrectionConflict: replacement exceeds 4096 UTF-8 bytes")

        fingerprint = segment_fingerprint(
            source_audio_sha256, start_ms, end_ms, segment_text
        )
        target = target_id(fingerprint, start_byte, end_byte, original_text)
        return self._append(
            {
                "recording_id": recording_id,
                "target_id": target,
                "event_type": "decision",
                "segment_id": segment_id,
                "segment_fingerprint": fingerprint,
                "decision": decision,
                "start_byte": start_byte,
                "end_byte": end_byte,
                "original_text": original_text,
                "replacement": replacement,
                "term": None,
                "term_scope": None,
            },
            event_id,
        )

    def append_term(
        self,
        *,
        recording_id: str,
        term: str,
        scope: str,
        revoke: bool = False,
        event_id: str | None = None,
    ) -> dict[str, Any]:
        _validate_hash(recording_id, "recording_id")
        try:
            term = _clean_text(term, "term", max_bytes=128, allow_empty=False)
        except ContextValidationError as exc:
            raise CorrectionConflict(f"CorrectionConflict: {exc}") from exc
        if len(term.split()) > 2:
            raise CorrectionConflict("CorrectionConflict: saved term must be one or two words")
        if scope != "global" and not PROJECT_SCOPE_RE.fullmatch(scope):
            raise CorrectionConflict("CorrectionConflict: scope must be global or project:<slug>")
        target = term_target_id(term, scope)
        return self._append(
            {
                "recording_id": recording_id,
                "target_id": target,
                "event_type": "revoke_term" if revoke else "save_term",
                "segment_id": "__terms__",
                "segment_fingerprint": target,
                "decision": None,
                "start_byte": None,
                "end_byte": None,
                "original_text": None,
                "replacement": None,
                "term": term,
                "term_scope": scope,
            },
            event_id,
        )

    def heads(self, recording_id: str, *, event_type: str | None = None) -> list[sqlite3.Row]:
        if self.connection is None:
            return []
        sql = """
            SELECT event.* FROM events event
            JOIN (
                SELECT target_id, MAX(revision) AS revision
                FROM events WHERE recording_id = ? GROUP BY target_id
            ) head ON head.target_id = event.target_id AND head.revision = event.revision
            WHERE event.recording_id = ?
        """
        params: list[Any] = [recording_id, recording_id]
        if event_type is not None:
            sql += " AND event.event_type = ?"
            params.append(event_type)
        try:
            return list(self.connection.execute(sql, params))
        except sqlite3.DatabaseError:
            if self.read_only:
                return []
            raise

    def active_terms(self, *, project: str = "") -> list[str]:
        if self.read_only:
            raise CorrectionStoreError(
                self.error or "CorrectionStoreError: store is read-only"
            )
        if self.connection is None:
            return []
        scopes = ["global"]
        if project:
            scopes.insert(0, f"project:{project}")
        placeholders = ",".join("?" for _ in scopes)
        rows = self.connection.execute(
            f"""
            SELECT event.* FROM events event
            WHERE event.event_type = 'save_term' AND event.term_scope IN ({placeholders})
              AND NOT EXISTS (
                  SELECT 1 FROM events newer
                  WHERE newer.target_id = event.target_id
                    AND newer.event_type IN ('save_term', 'revoke_term')
                    AND (newer.created_at > event.created_at
                         OR (newer.created_at = event.created_at AND newer.event_id > event.event_id))
              )
            ORDER BY CASE WHEN event.term_scope = ? THEN 0 ELSE 1 END, event.created_at
            """,
            (*scopes, scopes[0]),
        )
        return [row["term"] for row in rows]


def _analysis_segment_times(segment: dict[str, Any]) -> tuple[int, int]:
    try:
        start = float(segment["start"])
        end = float(segment["end"])
    except (KeyError, TypeError, ValueError) as exc:
        raise CorrectionConflict("CorrectionConflict: invalid segment time") from exc
    if start < 0 or end < start:
        raise CorrectionConflict("CorrectionConflict: invalid segment time")
    return int(round(start * 1000)), int(round(end * 1000))


def load_analysis(path: Path) -> dict[str, Any]:
    try:
        if path.stat().st_size > 50 * 1024 * 1024:
            raise CorrectionConflict("CorrectionConflict: analysis file exceeds 50 MiB")
        analysis = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise CorrectionConflict(f"CorrectionConflict: analysis read failed: {exc}") from exc
    try:
        validate_analysis_document(analysis)
    except AnalysisSchemaError as exc:
        raise CorrectionConflict(f"CorrectionConflict: {exc}") from exc
    source = analysis.get("source")
    if not isinstance(source, dict):
        raise CorrectionConflict("CorrectionConflict: analysis source missing")
    _validate_hash(source.get("audio_sha256"), "source audio hash")
    segments = analysis.get("segments")
    if not isinstance(segments, list):
        raise CorrectionConflict("CorrectionConflict: segments must be an array")
    seen: set[str] = set()
    for segment in segments:
        if not isinstance(segment, dict):
            raise CorrectionConflict("CorrectionConflict: segment must be an object")
        segment_id = segment.get("id")
        text = segment.get("text")
        if not isinstance(segment_id, str) or not segment_id or segment_id in seen:
            raise CorrectionConflict("CorrectionConflict: invalid or duplicate segment id")
        if not isinstance(text, str):
            raise CorrectionConflict("CorrectionConflict: segment text must be a string")
        if any(unicodedata.category(char) == "Cc" for char in segment_id + text):
            raise CorrectionConflict("CorrectionConflict: segment contains control character")
        seen.add(segment_id)
        _analysis_segment_times(segment)
        alternatives = segment.get("alternatives", [])
        if not isinstance(alternatives, list):
            raise CorrectionConflict("CorrectionConflict: alternatives must be an array")
        for alternative in alternatives:
            if not isinstance(alternative, dict) or not isinstance(alternative.get("text"), str):
                raise CorrectionConflict("CorrectionConflict: invalid alternative")
            if any(unicodedata.category(char) == "Cc" for char in alternative["text"]):
                raise CorrectionConflict("CorrectionConflict: alternative has control character")
    return analysis


def candidate_segments(analysis: dict[str, Any]) -> list[dict[str, Any]]:
    segments = analysis["segments"]
    has_confidence = any(segment.get("review_confidence") is not None for segment in segments)
    candidates: list[dict[str, Any]] = []
    for segment in segments:
        text = segment["text"].strip()
        alternatives = segment.get("alternatives", [])
        alternative_texts = [
            item.get("text", "").strip()
            for item in alternatives
            if isinstance(item, dict) and isinstance(item.get("text"), str)
        ]
        disagreement = any(value and value != text for value in alternative_texts)
        partial_missing = has_confidence and segment.get("review_confidence") is None
        if segment.get("review_required") is True or disagreement or partial_missing:
            candidates.append(segment)
    return candidates


def _segment_identity(
    recording_id: str, segment: dict[str, Any]
) -> tuple[str, int, int, str]:
    start_ms, end_ms = _analysis_segment_times(segment)
    text = segment["text"]
    return (
        segment_fingerprint(recording_id, start_ms, end_ms, text),
        start_ms,
        end_ms,
        text,
    )


def render_status(analysis: dict[str, Any], store: ReviewStore) -> str:
    recording_id = analysis["source"]["audio_sha256"]
    candidates = candidate_segments(analysis)
    heads = store.heads(recording_id, event_type="decision")
    current_fingerprints = {
        segment["id"]: _segment_identity(recording_id, segment)[0]
        for segment in analysis["segments"]
    }
    stale = sum(
        row["segment_id"] in current_fingerprints
        and row["segment_fingerprint"] != current_fingerprints[row["segment_id"]]
        for row in heads
    )
    decided_targets = {row["target_id"] for row in heads if row["segment_fingerprint"] in current_fingerprints.values()}
    candidate_targets = set()
    for segment in candidates:
        fingerprint, _, _, text = _segment_identity(recording_id, segment)
        candidate_targets.add(target_id(fingerprint, 0, len(text.encode("utf-8")), text))
    decided = len(candidate_targets & decided_targets)
    store_status = "read-only" if store.read_only else "ok"
    return "\n".join(
        (
            f"store: {store_status}",
            f"recording: {recording_id}",
            f"candidates: {len(candidates)}",
            f"decided: {decided}",
            f"pending: {len(candidates) - decided}",
            f"stale: {stale}",
        )
    )


def render_review_item(segment: dict[str, Any]) -> str:
    lines = [
        f"[{segment['id']}] {float(segment['start']):.2f}s-{float(segment['end']):.2f}s",
        segment["text"],
    ]
    for index, alternative in enumerate(segment.get("alternatives", []), start=1):
        if isinstance(alternative, dict) and isinstance(alternative.get("text"), str):
            lines.append(f"alternative {index}: {alternative['text']}")
    return "\n".join(lines)


def review_interactive(analysis: dict[str, Any], store: ReviewStore) -> int:
    recording_id = analysis["source"]["audio_sha256"]
    existing = {row["target_id"] for row in store.heads(recording_id, event_type="decision")}
    project = analysis.get("context", {}).get("project", "")
    completed = 0
    for segment in candidate_segments(analysis):
        fingerprint, start_ms, end_ms, text = _segment_identity(recording_id, segment)
        full_end = len(text.encode("utf-8"))
        target = target_id(fingerprint, 0, full_end, text)
        if target in existing:
            continue
        print(render_review_item(segment))
        try:
            choice = input("keep [k], approve alternative [a], edit [e], skip [s], quit [q]: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if choice in {"q", "quit"}:
            break
        if choice in {"s", "skip", ""}:
            continue
        decision = "keep"
        replacement: str | None = None
        if choice in {"a", "approve"}:
            alternatives = [
                item["text"]
                for item in segment.get("alternatives", [])
                if isinstance(item, dict) and isinstance(item.get("text"), str)
            ]
            if not alternatives:
                print("no Apple alternative")
                continue
            decision, replacement = "apple_alternative", alternatives[0]
        elif choice in {"e", "edit"}:
            try:
                replacement = input("replacement: ")
            except (EOFError, KeyboardInterrupt):
                print()
                break
            decision = "manual"
        elif choice not in {"k", "keep"}:
            print("unknown choice")
            continue

        store.append_decision(
            recording_id=recording_id,
            segment_id=segment["id"],
            source_audio_sha256=recording_id,
            start_ms=start_ms,
            end_ms=end_ms,
            segment_text=text,
            start_byte=0,
            end_byte=full_end,
            original_text=text,
            decision=decision,
            replacement=replacement,
        )
        completed += 1
        if replacement:
            choices = f"project:{project} / global / no" if project else "global / no"
            try:
                scope = input(f"save term? {choices} [no]: ").strip() or "no"
            except (EOFError, KeyboardInterrupt):
                print()
                break
            if scope != "no":
                try:
                    store.append_term(
                        recording_id=recording_id,
                        term=replacement,
                        scope=scope,
                    )
                except CorrectionConflict as exc:
                    print(f"term not saved: {exc}")
    return completed


def render_final_transcript(analysis: dict[str, Any], store: ReviewStore) -> str:
    recording_id = analysis["source"]["audio_sha256"]
    rows = store.heads(recording_id, event_type="decision")
    by_segment: dict[str, list[sqlite3.Row]] = {}
    for row in rows:
        by_segment.setdefault(row["segment_id"], []).append(row)

    rendered: list[str] = []
    for segment in analysis["segments"]:
        fingerprint, _, _, text = _segment_identity(recording_id, segment)
        edits: list[tuple[int, int, str]] = []
        for row in by_segment.get(segment["id"], []):
            if row["segment_fingerprint"] != fingerprint or row["decision"] == "keep":
                continue
            validate_exact_span(text, row["start_byte"], row["end_byte"], row["original_text"])
            edits.append((row["start_byte"], row["end_byte"], row["replacement"]))
        edits.sort(reverse=True)
        previous_start = len(text.encode("utf-8")) + 1
        encoded = text.encode("utf-8")
        for start, end, replacement in edits:
            if end > previous_start:
                raise CorrectionConflict("CorrectionConflict: overlapping approved spans")
            encoded = encoded[:start] + replacement.encode("utf-8") + encoded[end:]
            previous_start = start
        rendered.append(encoded.decode("utf-8"))
    return "\n".join(rendered).rstrip() + "\n"


def _atomic_render(path: Path, content: str) -> None:
    _atomic_write(path, content, mode=0o600)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Local Apple STT review")
    subparsers = parser.add_subparsers(dest="command", required=True)

    context = subparsers.add_parser("context", help="create or update recording context")
    context.add_argument("--file", type=Path, required=True)
    context.add_argument("--project")
    context.add_argument("--participant", action="append", default=[])
    context.add_argument("--term", action="append", default=[])
    context.add_argument("--privacy")
    context.add_argument("--reprocess", action="store_true")
    context.add_argument("--context-dir", type=Path, default=DEFAULT_CONTEXT_DIR)

    for command in ("status", "review", "render"):
        child = subparsers.add_parser(command)
        child.add_argument("--analysis", type=Path, required=True)
        child.add_argument("--db", type=Path, default=DEFAULT_DB_PATH)
        if command == "render":
            child.add_argument("--output", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "context":
            recording_id, path, context = write_context(
                args.file,
                project=args.project,
                participants=args.participant,
                terms=args.term,
                privacy=args.privacy,
                directory=args.context_dir,
                reprocess=args.reprocess,
            )
            print(f"recording: {recording_id}")
            print(f"context: {path}")
            print(f"privacy: {context['privacy']}")
            return 0

        analysis = load_analysis(args.analysis)
        lock = (
            nullcontext()
            if args.command == "status"
            else recording_lock(analysis["source"]["audio_sha256"])
        )
        with lock, ReviewStore(args.db) as store:
            if args.command == "status":
                print(render_status(analysis, store))
                if store.error:
                    print(store.error, file=sys.stderr)
                return 2 if store.read_only else 0
            if args.command in {"review", "render"} and store.read_only:
                raise CorrectionStoreError(store.error or "review store is read-only")
            if args.command == "review":
                completed = review_interactive(analysis, store)
                print(f"recorded: {completed}")
                return 0
            content = render_final_transcript(analysis, store)
            if args.output:
                _atomic_render(args.output.expanduser(), content)
                print(args.output)
            else:
                sys.stdout.write(content)
            return 0
    except (
        ContextValidationError,
        CorrectionConflict,
        CorrectionStoreError,
        RecordingBusy,
    ) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
