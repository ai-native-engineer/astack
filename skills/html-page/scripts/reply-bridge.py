#!/usr/bin/env python3
"""Local HTML replies, durable outbox, and explicit Herdr conversation routing."""
import argparse
import hashlib
import html
import fcntl
from contextlib import contextmanager
import json
import mimetypes
import os
from pathlib import Path
import re
import secrets
import shlex
import shutil
import signal
import sqlite3
import stat
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
from urllib.request import urlopen
import webbrowser
import xml.etree.ElementTree as ET

ASSETS = Path(__file__).resolve().parents[1] / "assets"
MEDIA = {".mp4", ".webm", ".mov", ".mp3", ".m4a", ".wav", ".ogg", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".avif", ".pdf", ".txt", ".md", ".json", ".woff", ".woff2"}
MAX_BODY = 64 * 1024


def context_summary(content):
    class ContextParser(HTMLParser):
        summary = ""

        def handle_starttag(self, tag, attrs):
            attrs = dict(attrs)
            if tag == "meta" and attrs.get("name") == "html-reply-context" and not self.summary:
                self.summary = (attrs.get("content") or "").strip()[:1600]

    parser = ContextParser()
    parser.feed(content)
    return parser.summary


def rewrite_resources(content, local_url):
    """Replace resource value spans, never copied text or serialized HTML."""
    edits = []
    lines = [0] + [match.end() for match in re.finditer("\n", content)]
    attribute = re.compile(r'''([^\s/=>]+)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+)))?''')
    resource_tags = {
        "src": {"audio", "embed", "iframe", "img", "input", "script", "source", "track", "video"},
        "href": {"a", "area", "image", "link", "use"},
        "poster": {"video"},
    }

    def reject_constant(value):
        raise ValueError(f"Not a JSON constant: {value}")

    def rewrite_json(start, end, declaration):
        body = content[start:end]
        if declaration:
            match = re.fullmatch(r"\s*(?:const|let|var)\s+[A-Za-z_$][A-Za-z0-9_$]*\s*=\s*(.*?)\s*;?\s*", body, re.S)
            if not match:
                return
            start += match.start(1)
            body = match[1]
        try:
            json.loads(body, parse_constant=reject_constant)
        except (ValueError, RecursionError):
            return
        # Tokenize validated JSON strings so a quoted example of a url field
        # cannot be mistaken for a declaration. Keep every other byte intact.
        previous = None
        for token in re.finditer(r'"(?:[^"\\]|\\.)*"', body):
            if previous and re.fullmatch(r"\s*:\s*", body[previous.end():token.start()]) and json.loads(previous[0]) == "url":
                value = json.loads(token[0])
                rewritten = local_url(value)
                if rewritten != value:
                    edits.append((start + token.start(), start + token.end(), json.dumps(rewritten, ensure_ascii=False).replace("<", "\\u003c")))
            previous = token

    class ResourceParser(HTMLParser):
        # HTMLParser otherwise parses textarea/title RCDATA as live markup.
        CDATA_CONTENT_ELEMENTS = ("script", "style", "textarea", "title", "xmp", "iframe", "noembed", "noframes")

        def __init__(self):
            super().__init__(convert_charrefs=False)
            self.copied = []
            self.script = None
            self.body_end = None

        def absolute_position(self):
            line, column = self.getpos()
            return lines[line - 1] + column

        def handle_starttag(self, tag, attrs):
            if tag in {"pre", "code"}:
                self.copied.append(tag)
            if self.copied:
                return
            raw = self.get_starttag_text()
            start = self.absolute_position()
            seen = set()
            for match in attribute.finditer(raw, re.match(r"<[^\s/>]+", raw).end(), len(raw) - 1):
                name = match[1].lower()
                if name in seen:
                    continue
                seen.add(name)
                if tag not in resource_tags.get(name, ()):
                    continue
                group = next((index for index in (2, 3, 4) if match[index] is not None), None)
                if group is None:
                    continue
                value = html.unescape(match[group])
                rewritten = local_url(value)
                if rewritten != value:
                    rewritten = html.escape(rewritten, quote=True)
                    if group == 4:
                        rewritten = '"' + rewritten + '"'
                    edits.append((start + match.start(group), start + match.end(group), rewritten))
            attrs = dict(reversed(attrs))
            kind = (attrs.get("type") or "").strip().lower()
            if tag == "script" and "src" not in attrs and kind in {"application/json", "", "text/javascript", "application/javascript", "module"}:
                self.script = (start + len(raw), kind != "application/json")

        def handle_startendtag(self, tag, attrs):
            self.handle_starttag(tag, attrs)
            # In HTML a slash does not close raw-text or copied containers.
            if tag in self.CDATA_CONTENT_ELEMENTS:
                self.set_cdata_mode(tag)

        def handle_endtag(self, tag):
            if self.copied:
                if tag in self.copied:
                    while self.copied.pop() != tag:
                        pass
                return
            if tag == "script" and self.script is not None:
                start, declaration = self.script
                rewrite_json(start, self.absolute_position(), declaration)
                self.script = None
            elif tag == "body" and self.body_end is None:
                self.body_end = self.absolute_position()

    parser = ResourceParser()
    parser.feed(content)
    parser.close()
    insertion = parser.body_end
    bridge = '<script src="/assets/reply-content.js"></script>'
    if insertion is None:
        insertion = 0 if parser.copied or parser.cdata_elem else len(content)
        if insertion == 0:
            bridge = '<script defer src="/assets/reply-content.js"></script>'
    edits.append((insertion, insertion, bridge))
    parts, cursor = [], 0
    for start, end, replacement in sorted(edits):
        parts.extend((content[cursor:start], replacement))
        cursor = end
    parts.append(content[cursor:])
    return "".join(parts)


def activate_client(endpoint):
    if sys.platform != "darwin" or not shutil.which("swift"):
        return False
    processes = subprocess.run(["ps", "-A", "-o", "pid=,ppid=,args="], capture_output=True, text=True, timeout=5, check=True)
    parents, clients = {}, []
    for line in processes.stdout.splitlines():
        parts = line.strip().split(None, 2)
        if len(parts) != 3:
            continue
        try:
            pid, parent = int(parts[0]), int(parts[1])
            argv = shlex.split(parts[2])
        except ValueError:
            continue
        parents[pid] = parent
        if argv and Path(argv[0]).name == "herdr" and (argv[1:] == ["--session", endpoint] or (endpoint == "default" and not argv[1:])):
            clients.append(pid)
    chains = []
    for pid in clients:
        chain = []
        while pid > 1 and pid not in chain:
            chain.append(pid)
            pid = parents.get(pid, 0)
        chains.append(",".join(map(str, chain)))
    if not chains:
        return False
    # Activate an existing terminal host, not an invented Herdr.app or a new
    # terminal. Multiple distinct GUI hosts are deliberately left untouched.
    script = '''import AppKit
var hosts: [pid_t: NSRunningApplication] = [:]
for chain in CommandLine.arguments.dropFirst() {
    for value in chain.split(separator: ",") {
        if let pid = Int32(value), let app = NSRunningApplication(processIdentifier: pid), app.activationPolicy == .regular {
            hosts[pid] = app
            break
        }
    }
}
guard hosts.count == 1, let app = hosts.values.first else { exit(1) }
app.activate(options: [])
RunLoop.current.run(until: Date(timeIntervalSinceNow: 0.2))
exit(app.isActive ? 0 : 1)
'''
    return subprocess.run(["swift", "-e", script, *chains], capture_output=True, timeout=15).returncode == 0


def empty_prompt(text, agent):
    lines = [line.strip() for line in text.splitlines()]
    if agent == "claude":
        # Status lines below the editor are not part of a user's draft.
        rules = [i for i, line in enumerate(lines) if re.fullmatch(r"[─━═]{3,}", line)]
        if len(rules) < 2:
            return False
        body = [line for line in lines[rules[-2] + 1:rules[-1]] if line]
        return body == ["❯"]
    if agent == "gjc":
        starts = [i for i, line in enumerate(lines) if re.fullmatch(r"╭─+╮", line)]
        if not starts:
            return False
        body = lines[starts[-1] + 1:]
        while body and not body[-1]:
            body.pop()
        if len(body) != 2 or not re.fullmatch(r"╰─+╯", body[-1]):
            return False
        return bool(re.fullmatch(r"│ > Type your message\.\.\. (?:↩: Steer · )?⌥Q: Queue(?: \(busy\))? · [^│]*New line[^│]*│", body[0]))
    if agent != "codex":
        return False
    prompts = [(i, re.fullmatch(r"[›»](?:[ \t]+(.*))?", line)) for i, line in enumerate(lines)]
    prompts = [(i, match) for i, match in prompts if match]
    if not prompts or (prompts[-1][1][1] or "") not in {"", "Ask Codex to do anything"}:
        return False
    footer = re.compile(r"^(?:[─━═]+|.*(?:\d+% context left|Context \d+% left).*|[?←].*(?:shortcuts|agents).*)$")
    return all(not line or footer.fullmatch(line) for line in lines[prompts[-1][0] + 1:])


def foreground_owners(processes, agent):
    owners = []
    for process in processes:
        executable = Path(process.get("argv0", process.get("name", ""))).name.lower()
        argv = process.get("argv") or []
        scripted = agent == "gjc" and executable in {"bun", "node"} and len(argv) > 1 and Path(argv[1]).name == "gjc"
        if executable == agent or scripted:
            owners.append(process)
    return owners


def gjc_session_matches(processes, native_id):
    # Herdr can retain an unrelated Devin ID behind GJC's custom reporter.
    if not re.fullmatch(r"[a-zA-Z0-9_-]{1,128}", native_id):
        return False
    for owner in foreground_owners(processes, "gjc"):
        cwd = owner.get("cwd")
        if not cwd or not Path(cwd).is_absolute():
            continue
        path = Path(cwd) / ".gjc/state/sdk" / (native_id + ".json")
        try:
            info = path.lstat()
            if not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid() or info.st_mode & 0o077:
                continue
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, dict) and data.get("version") == 1 and data.get("sessionId") == native_id and data.get("pid") == owner["pid"]:
                return True
        except (OSError, ValueError, TypeError):
            continue
    return False


def digest(value):
    return hashlib.sha256(value.encode()).hexdigest()


def process_start(pid):
    result = subprocess.run(["ps", "-p", str(pid), "-o", "lstart="], capture_output=True, text=True, check=False)
    return result.stdout.strip() if result.returncode == 0 else ""


def normalize_payload(body, allow_empty=False):
    payload = {key: body.get(key, "") for key in ("text", "quote", "sheet", "location")}
    if any(not isinstance(value, str) for value in payload.values()):
        raise ValueError("응답은 텍스트여야 합니다.")
    source_items = body.get("items", [])
    if not isinstance(source_items, list):
        raise ValueError("선택 결과는 항목 목록이어야 합니다.")
    items, ids = [], set()
    for item in source_items:
        if not isinstance(item, dict):
            raise ValueError("응답 항목 형식을 확인하세요.")
        key, label, values, memo = item.get("id"), item.get("label", ""), item.get("values", []), item.get("memo", "")
        if not isinstance(key, str) or not key.strip() or len(key) > 64 or key in ids:
            raise ValueError("응답 항목 ID는 비어 있지 않은 고유한 값이어야 합니다.")
        if not isinstance(label, str) or not isinstance(memo, str) or not isinstance(values, list) or any(not isinstance(value, str) for value in values):
            raise ValueError("항목의 선택과 메모 형식을 확인하세요.")
        ids.add(key)
        items.append({"id": key, "label": label, "values": values, "memo": memo})
    if items:
        payload["items"] = items
        # The sheet is a derived mirror of structured items, not another answer.
        payload["sheet"] = ""
    strings = list(payload[key] for key in ("text", "quote", "sheet", "location"))
    for item in items:
        strings.extend([item["id"], item["label"], item["memo"], *item["values"]])
    meaningful = payload["text"].strip() or payload["sheet"].strip() or any(item["values"] or item["memo"].strip() for item in items)
    if not allow_empty and not meaningful:
        raise ValueError("항목을 고르거나 메모를 적어 주세요.")
    if len(json.dumps(payload, ensure_ascii=False)) > 20000 or any(re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f\ufffe\uffff]", value) for value in strings):
        raise ValueError("응답은 제어문자 없이 20,000자 이내로 작성하세요.")
    return payload


def format_reply(artifact, payload, reply_id=""):
    attrs = {"artifact": artifact["id"], "rev": artifact["revision"][:12]}
    if reply_id:
        attrs["id"] = reply_id
    root = ET.Element("feedback", attrs)
    pending = []
    for item in payload.get("items", []):
        if item["values"]:
            answer = ET.SubElement(root, "answer", {"id": item["id"]})
            if len(item["values"]) == 1:
                answer.text = item["values"][0]
            else:
                for value in item["values"]:
                    ET.SubElement(answer, "value").text = value
        else:
            pending.append(item["id"])
        if item["memo"].strip():
            ET.SubElement(root, "note", {"for": item["id"]}).text = item["memo"].strip()
    if pending:
        ET.SubElement(root, "unanswered").text = " ".join(pending)
    if payload.get("sheet", "").strip():
        ET.SubElement(root, "answers").text = payload["sheet"].strip()
    location = payload.get("location", "")
    if "#" in location:
        ET.SubElement(root, "at").text = "#" + location.split("#", 1)[1]
    for key, tag in [("quote", "quote"), ("text", "memo")]:
        if payload.get(key, "").strip():
            ET.SubElement(root, tag).text = payload[key].strip()
    ET.indent(root, space="  ")
    title = " ".join(artifact["title"].split())
    return f"## {title} 피드백\n" + ET.tostring(root, encoding="unicode")


class Store:
    def __init__(self, root):
        self.root = Path(root).expanduser().resolve()
        self.root.mkdir(parents=True, exist_ok=True, mode=0o700)
        self.db = self.root / "replies.sqlite3"
        with self.connect() as db:
            db.executescript("""
                CREATE TABLE IF NOT EXISTS artifacts (
                    id TEXT PRIMARY KEY, path TEXT, title TEXT, revision TEXT,
                    agent TEXT, conversation TEXT, endpoint TEXT, content TEXT, media TEXT,
                    conversation_label TEXT NOT NULL DEFAULT '');
                CREATE TABLE IF NOT EXISTS replies (
                    id TEXT PRIMARY KEY, artifact TEXT, payload TEXT, state TEXT,
                    detail TEXT, created REAL, updated REAL);
                CREATE TABLE IF NOT EXISTS turn_gates (
                    target TEXT PRIMARY KEY, saw_working INTEGER, started REAL);
                CREATE TABLE IF NOT EXISTS receivers (
                    artifact TEXT PRIMARY KEY, pid INTEGER, heartbeat REAL);
            """)
            if "conversation_label" not in {row[1] for row in db.execute("PRAGMA table_info(artifacts)")}:
                db.execute("ALTER TABLE artifacts ADD COLUMN conversation_label TEXT NOT NULL DEFAULT ''")
        self.db.chmod(0o600)

    @contextmanager
    def connect(self):
        db = sqlite3.connect(self.db, timeout=10)
        db.row_factory = sqlite3.Row
        try:
            with db:
                yield db
        finally:
            db.close()

    def artifact(self, artifact_id):
        with self.connect() as db:
            row = db.execute("SELECT * FROM artifacts WHERE id=?", (artifact_id,)).fetchone()
        if not row:
            raise ValueError("자료를 찾을 수 없습니다.")
        return dict(row)

    def register(self, path, title, agent, conversation, endpoint, conversation_label=""):
        path = Path(path).expanduser().resolve(strict=True)
        if path.suffix.lower() not in {".html", ".htm"}:
            raise ValueError("HTML 파일을 지정하세요.")
        content = path.read_text(encoding="utf-8")
        revision = digest(content)
        artifact_id = digest(json.dumps([str(path), revision, agent, conversation, endpoint], ensure_ascii=False, separators=(",", ":")))[:32]
        media = {}

        def local_url(raw):
            parsed = urlsplit(raw)
            if parsed.scheme not in {"", "file"} or parsed.netloc:
                return raw
            candidate = Path(unquote(parsed.path))
            if not candidate.is_absolute():
                candidate = path.parent / candidate
            candidate = candidate.resolve()
            if not candidate.is_file() or candidate.suffix.lower() not in MEDIA:
                return raw
            key = digest(str(candidate))[:24]
            media[key] = str(candidate)
            suffix = "#" + parsed.fragment if parsed.fragment else ""
            return f"/media/{artifact_id}/{key}{suffix}"

        content = rewrite_resources(content, local_url)
        with self.connect() as db:
            db.execute("INSERT OR IGNORE INTO artifacts (id,path,title,revision,agent,conversation,endpoint,content,media,conversation_label) VALUES (?,?,?,?,?,?,?,?,?,?)",
                       (artifact_id, str(path), title or path.stem, revision, agent, conversation, endpoint, content, json.dumps(media), conversation_label))
            if conversation_label:
                db.execute("UPDATE artifacts SET conversation_label=? WHERE id=?", (conversation_label, artifact_id))
        return self.artifact(artifact_id)

    def enqueue(self, artifact_id, body):
        self.artifact(artifact_id)
        key = body.get("id", "")
        if not isinstance(key, str) or not re.fullmatch(r"[a-zA-Z0-9_-]{8,80}", key):
            raise ValueError("응답 식별자가 올바르지 않습니다.")
        payload = normalize_payload(body)
        serialized = json.dumps(payload, ensure_ascii=False, sort_keys=True)
        now = time.time()
        with self.connect() as db:
            db.execute("INSERT OR IGNORE INTO replies VALUES (?,?,?,?,?,?,?)", (key, artifact_id, serialized, "queued", "대상 대화를 확인하고 있습니다.", now, now))
            previous = db.execute("SELECT * FROM replies WHERE id=?", (key,)).fetchone()
            if previous["artifact"] != artifact_id or previous["payload"] != serialized:
                raise ValueError("같은 응답 식별자로 다른 내용을 보낼 수 없습니다.")
        return self.reply(key, artifact_id)

    def reply(self, key, artifact_id):
        with self.connect() as db:
            row = db.execute("SELECT id,state,detail,created,updated FROM replies WHERE id=? AND artifact=?", (key, artifact_id)).fetchone()
        if not row:
            raise ValueError("응답을 찾을 수 없습니다.")
        return dict(row)

    def update(self, key, state, detail):
        with self.connect() as db:
            db.execute("UPDATE replies SET state=?,detail=?,updated=? WHERE id=?", (state, detail, time.time(), key))

    def update_queued(self, key, state, detail):
        with self.connect() as db:
            db.execute("UPDATE replies SET state=?,detail=?,updated=? WHERE id=? AND state='queued'", (state, detail, time.time(), key))

    def recover(self):
        with self.connect() as db:
            db.execute("UPDATE replies SET state='uncertain',detail='전송 도중 서비스가 종료됐습니다. 원래 대화에서 수신 여부를 확인하세요.' WHERE state='sending'")

    def pending(self):
        with self.connect() as db:
            rows = db.execute("SELECT r.*,a.endpoint,a.agent,a.conversation FROM replies r JOIN artifacts a ON a.id=r.artifact WHERE r.state IN ('queued','held','uncertain','sending') ORDER BY r.created,r.rowid").fetchall()
        result, seen = [], set()
        for row in rows:
            target = (row["endpoint"], row["agent"], row["conversation"])
            if target not in seen and row["state"] == "queued":
                result.append(dict(row))
            seen.add(target)
        return result

    def gate(self, artifact, state):
        target = json.dumps([artifact[k] for k in ("endpoint", "agent", "conversation")])
        with self.connect() as db:
            gate = db.execute("SELECT * FROM turn_gates WHERE target=?", (target,)).fetchone()
            if not gate:
                return False
            if state == "queued":
                db.execute("UPDATE turn_gates SET saw_working=1 WHERE target=?", (target,))
            elif state == "ready" and gate["saw_working"]:
                db.execute("DELETE FROM turn_gates WHERE target=?", (target,))
                return False
        return True

    def begin_turn(self, artifact):
        target = json.dumps([artifact[k] for k in ("endpoint", "agent", "conversation")])
        with self.connect() as db:
            db.execute("INSERT OR REPLACE INTO turn_gates VALUES (?,0,?)", (target, time.time()))

    def claim(self, key):
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT artifact FROM replies WHERE id=? AND state='queued'", (key,)).fetchone()
            if not row or self._active_receiver(db, row["artifact"]):
                return False
            return db.execute("UPDATE replies SET state='sending',detail='Herdr에 전달 중입니다.',updated=? WHERE id=? AND state='queued'", (time.time(), key)).rowcount == 1

    def _active_receiver(self, db, artifact_id):
        return db.execute("""
            SELECT r.* FROM receivers r JOIN artifacts a ON a.id=r.artifact
            JOIN artifacts target ON target.id=?
            WHERE a.endpoint=target.endpoint AND a.agent=target.agent
              AND a.conversation=target.conversation AND r.heartbeat>? LIMIT 1
        """, (artifact_id, time.time() - 5)).fetchone()

    def has_receiver(self, artifact_id):
        with self.connect() as db:
            return self._active_receiver(db, artifact_id) is not None

    def receive(self, artifact_id, native_id, timeout):
        artifact = self.artifact(artifact_id)
        if artifact["agent"] != "codex" or not native_id or native_id != artifact["conversation"]:
            raise ValueError("Run receive from the originating Codex session; CODEX_THREAD_ID must match the registered conversation.")
        pid = os.getpid()
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            if self._active_receiver(db, artifact_id):
                raise ValueError("A receiver is already waiting for this conversation.")
            heartbeat = time.time()
            db.execute("INSERT OR REPLACE INTO receivers VALUES (?,?,?)", (artifact_id, pid, heartbeat))
        try:
            deadline = time.monotonic() + timeout
            while time.monotonic() < deadline:
                result = None
                with self.connect() as db:
                    db.execute("BEGIN IMMEDIATE")
                    now = time.time()
                    if db.execute("UPDATE receivers SET heartbeat=? WHERE artifact=? AND pid=? AND heartbeat=? AND heartbeat>?", (now, artifact_id, pid, heartbeat, now - 5)).rowcount != 1:
                        raise ValueError("This receiver registration expired or was replaced.")
                    row = db.execute("""
                        SELECT r.* FROM replies r JOIN artifacts a ON a.id=r.artifact
                        WHERE a.endpoint=? AND a.agent=? AND a.conversation=?
                          AND r.state IN ('queued','held','sending','uncertain')
                        ORDER BY r.created,r.rowid LIMIT 1
                    """, (artifact["endpoint"], artifact["agent"], artifact["conversation"])).fetchone()
                    if row and row["artifact"] == artifact_id and row["state"] in {"queued", "held"}:
                        result = {"reply_id": row["id"], "conversation": native_id, "message": reply_text(artifact, row)}
                        db.execute("UPDATE replies SET state='received',detail='이 HTML을 만든 세션의 대기 도구로 응답을 반환했습니다. 에이전트의 반영 완료는 별도입니다.',updated=? WHERE id=?", (now, row["id"]))
                # Track only committed heartbeats so error cleanup still owns its row.
                heartbeat = now
                if result is not None:
                    return result
                time.sleep(0.2)
            return None
        finally:
            with self.connect() as db:
                db.execute("DELETE FROM receivers WHERE artifact=? AND pid=? AND heartbeat=?", (artifact_id, pid, heartbeat))

    def cancel(self, key, artifact_id):
        with self.connect() as db:
            if db.execute("UPDATE replies SET state='cancelled',detail='대기 중인 응답을 취소했습니다.',updated=? WHERE id=? AND artifact=? AND state IN ('queued','held')", (time.time(), key, artifact_id)).rowcount != 1:
                raise ValueError("전송이 시작된 응답은 취소할 수 없습니다.")

    def retry(self, key, artifact_id):
        with self.connect() as db:
            if db.execute("UPDATE replies SET state='queued',detail='원래 대화를 다시 확인합니다.',updated=? WHERE id=? AND artifact=? AND state='held'", (time.time(), key, artifact_id)).rowcount != 1:
                raise ValueError("이미 처리되거나 전송 중인 응답은 다시 보낼 수 없습니다.")

    def observe_turns(self, transport_factory):
        with self.connect() as db:
            gates = [dict(r) for r in db.execute("SELECT * FROM turn_gates")]
        for gate in gates:
            endpoint, agent, conversation = json.loads(gate["target"])
            artifact = dict(endpoint=endpoint, agent=agent, conversation=conversation)
            try:
                state, _, _ = transport_factory(endpoint).resolve(artifact)
                self.gate(artifact, state)
            except (ValueError, OSError, subprocess.TimeoutExpired):
                continue
            # Native input acceptance is not a turn receipt. Pause later messages if no
            # working transition was observed within the CLI's startup grace plus polling.
            if not gate["saw_working"] and time.time() - gate["started"] > 15 and state == "ready":
                with self.connect() as db:
                    db.execute("UPDATE replies SET state='held',detail='앞선 응답의 작업 시작을 확인하지 못했습니다. 원래 대화를 확인한 뒤 연결을 다시 확인하세요.' WHERE state='queued' AND artifact IN (SELECT id FROM artifacts WHERE endpoint=? AND agent=? AND conversation=?)", (endpoint, agent, conversation))
                    db.execute("DELETE FROM turn_gates WHERE target=?", (gate["target"],))


class Herdr:
    def __init__(self, endpoint, executable=None):
        self.endpoint = endpoint
        self.executable = executable or shutil.which("herdr")
        if not self.executable:
            raise ValueError("herdr 실행 파일을 찾을 수 없습니다.")

    def call(self, *args):
        env = {k: v for k, v in os.environ.items() if k not in {"HERDR_SOCKET_PATH", "HERDR_SESSION", "HERDR_PANE_ID"}}
        result = subprocess.run([self.executable, "--session", self.endpoint, *args],
                                capture_output=True, text=True, timeout=10, env=env)
        if args[:2] in {("agent", "read"), ("pane", "read")} and result.returncode == 0:
            return {"text": result.stdout}
        if args[:2] in {("agent", "prompt"), ("pane", "run")} and result.returncode == 0 and not result.stdout.strip():
            return {"accepted": True}
        try:
            data = json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            raise ValueError("Herdr 응답을 확인할 수 없습니다.") from exc
        if result.returncode or "error" in data:
            error = data.get("error", {})
            raise ValueError(error.get("code", "herdr_error"))
        return data.get("result", data)

    def locate(self, artifact):
        result = self.call("pane", "list")
        panes = result.get("panes", [])
        process_info = {}
        if artifact["agent"] == "gjc":
            matches = []
            for candidate in panes:
                if candidate.get("agent") != "gjc":
                    continue
                info = self.call("pane", "process-info", "--pane", candidate["pane_id"])["process_info"]
                if gjc_session_matches(info.get("foreground_processes", []), artifact["conversation"]):
                    matches.append(candidate)
                    process_info[candidate["pane_id"]] = info
        else:
            matches = [p for p in panes if p.get("agent") == artifact["agent"]
                       and (p.get("agent_session") or {}).get("agent") == artifact["agent"]
                       and (p.get("agent_session") or {}).get("source") == "herdr:" + artifact["agent"]
                       and (p.get("agent_session") or {}).get("kind") == "id"
                       and (p.get("agent_session") or {}).get("value") == artifact["conversation"]]
        if len(matches) != 1:
            raise ValueError("원래 대화를 하나로 확인할 수 없습니다. 세션 연결을 확인한 뒤 다시 시도하세요.")
        pane = matches[0]
        info = process_info.get(pane["pane_id"])
        if info is None:
            info = self.call("pane", "process-info", "--pane", pane["pane_id"])["process_info"]
        processes = info.get("foreground_processes", [])
        # A retained session reference can remain behind a foreground shell or editor.
        owners = foreground_owners(processes, artifact["agent"])
        if not owners:
            raise ValueError("대화가 현재 패널 입력을 받고 있지 않습니다.")
        identity = (pane["pane_id"], pane.get("terminal_id"), tuple(p["pid"] for p in owners), artifact["agent"])
        return pane, identity

    def focus(self, artifact):
        pane, identity = self.locate(artifact)
        if not identity[1]:
            raise ValueError("원래 세션의 터미널 식별자를 확인하지 못했습니다.")
        _, current = self.locate(artifact)
        if identity != current:
            raise ValueError("이동 직전에 대상 세션이 바뀌었습니다. 다시 확인하세요.")
        # Navigation is deliberate and independent of send readiness: a working
        # conversation or a user draft is safe to view, never safe to type into.
        workspace_id, tab_id = pane.get("workspace_id"), pane.get("tab_id")
        if not workspace_id or not tab_id:
            raise ValueError("원래 세션의 워크스페이스와 탭을 확인하지 못했습니다.")
        # `agent focus` only marks the pane focused; the client keeps showing its current
        # workspace and tab, so select those first and verify the client-level snapshot.
        self.call("workspace", "focus", workspace_id)
        self.call("tab", "focus", tab_id)
        self.call("agent", "focus", identity[0])
        snapshot = self.call("api", "snapshot").get("snapshot", {})
        selected = (snapshot.get("focused_workspace_id"), snapshot.get("focused_tab_id"), snapshot.get("focused_pane_id"))
        shown = self.call("pane", "get", identity[0]).get("pane", {})
        if selected != (workspace_id, tab_id, identity[0]) or shown.get("terminal_id") != identity[1]:
            raise ValueError("원래 세션의 선택 상태를 확인하지 못했습니다.")
        activated = False
        try:
            activated = activate_client(self.endpoint)
        except (OSError, subprocess.SubprocessError):
            pass
        return {"focused": True, "activated": activated,
                "label": "원래 세션을 선택했습니다." if activated else "원래 세션을 선택했습니다. Herdr 창을 확인하세요."}

    def resolve(self, artifact):
        try:
            pane, identity = self.locate(artifact)
        except ValueError as error:
            return "held", str(error), None
        state = pane.get("agent_status", "unknown")
        if state == "working":
            return "queued", "원래 세션이 작업 중입니다. 입력 가능한 상태가 되면 전달합니다.", identity
        if state not in {"idle", "done"}:
            return "held", "원래 세션의 질문이나 승인 화면을 먼저 확인하세요.", identity
        reader = "pane" if artifact["agent"] == "gjc" else "agent"
        screen = self.call(reader, "read", pane["pane_id"], "--source", "detection", "--format", "text", "--lines", "80")
        text = screen.get("text", screen.get("output", ""))
        # Unknown prompt shapes fail closed. Never append to a draft or answer an approval.
        if not empty_prompt(text, artifact["agent"]):
            return "held", "비어 있는 입력창을 확인하지 못했습니다. 원래 대화의 입력 내용을 확인하세요.", identity
        return "ready", "전달할 수 있습니다.", identity

    def send(self, identity, message):
        if identity[3] == "gjc":
            # Herdr's custom agents are not agent.prompt targets. pane.run submits
            # literal text and Enter together after native PID and draft checks.
            self.call("pane", "run", identity[0], message)
        else:
            self.call("agent", "prompt", identity[0], message)


def reply_text(artifact, row):
    return format_reply(artifact, json.loads(row["payload"]), row["id"])


def dispatch(store, row, transport_factory=Herdr):
    artifact = store.artifact(row["artifact"])
    try:
        if store.has_receiver(artifact["id"]):
            return
        transport = transport_factory(artifact["endpoint"])
        state, detail, identity = transport.resolve(artifact)
        if state == "held":
            store.update_queued(row["id"], state, detail)
            return
        if store.gate(artifact, state):
            store.update_queued(row["id"], "queued", "앞선 응답의 작업 시작과 종료를 기다리고 있습니다.")
            return
        if state != "ready":
            store.update_queued(row["id"], state, detail)
            return
        state2, detail2, identity2 = transport.resolve(artifact)
        if state2 != "ready" or identity != identity2:
            store.update_queued(row["id"], "held", "전송 직전에 대상 상태가 바뀌었습니다. 연결을 다시 확인하세요.")
            return
        # Commit before touching the terminal. A crash can never cause an automatic replay.
        if not store.claim(row["id"]):
            return
        transport.send(identity, reply_text(artifact, row))
        store.begin_turn(artifact)
        store.update(row["id"], "sent", "Herdr 입력 전달을 마쳤습니다. 에이전트의 반영 완료는 아직 확인하지 않았습니다.")
    except (ValueError, OSError, subprocess.TimeoutExpired):
        current = store.reply(row["id"], row["artifact"])
        if current["state"] not in {"sending", "queued"}:
            return
        state = "uncertain" if current["state"] == "sending" else "held"
        store.update(row["id"], state, "전달 결과를 확인할 수 없습니다. 자동 재전송하지 않습니다." if state == "uncertain" else "Herdr 연결을 확인하지 못했습니다. 응답은 보관했습니다.")


def serve(store, port=0, delivery=True):
    lock = (store.root / "server.lock").open("a")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError as exc:
        raise ValueError("This state directory already has a service owner.") from exc
    store.recover()
    nonce = secrets.token_urlsafe(32)
    stopping = threading.Event()

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_args):
            pass

        def valid_host(self):
            return self.headers.get("Host") == f"127.0.0.1:{self.server.server_port}"

        def respond(self, data, kind="application/json", code=200):
            if not isinstance(data, bytes):
                data = (json.dumps(data, ensure_ascii=False) if kind == "application/json" else data).encode()
            self.send_response(code)
            self.send_header("Content-Type", kind + ("; charset=utf-8" if kind.startswith("text/") or kind == "application/json" else ""))
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(data)

        def do_HEAD(self):
            self.do_GET()

        def do_GET(self):
            if not self.valid_host():
                return self.respond({"error": "invalid host"}, code=403)
            parts = urlsplit(self.path).path.strip("/").split("/")
            try:
                if parts == ["health"]:
                    return self.respond({"ok": True, "delivery": delivery})
                if len(parts) == 2 and parts[0] == "assets" and parts[1] in {"reply-panel.js", "reply-content.js"}:
                    return self.respond((ASSETS / parts[1]).read_bytes(), "text/javascript")
                if len(parts) >= 2 and parts[0] == "artifact":
                    artifact = store.artifact(parts[1])
                    if len(parts) == 2:
                        page = (ASSETS / "reply-panel.html").read_text()
                        meta = {k: artifact[k] for k in ("id", "title", "conversation", "conversation_label", "agent", "revision")}
                        meta.update(csrf=nonce, delivery=delivery, context=context_summary(artifact["content"]))
                        page = page.replace("__REPLY_META__", json.dumps(meta, ensure_ascii=False).replace("<", "\\u003c"))
                        return self.respond(page, "text/html")
                    if parts[2:] == ["content"]:
                        return self.respond(artifact["content"], "text/html")
                    if parts[2:] == ["connection"]:
                        if store.has_receiver(artifact["id"]):
                            return self.respond({"state": "listening", "label": "원래 대화에서 응답을 기다리고 있습니다"})
                        if not delivery:
                            return self.respond({"state": "preview", "label": "미리보기 · 응답은 보관됩니다"})
                        try:
                            state, _, _ = Herdr(artifact["endpoint"]).resolve(artifact)
                        except (ValueError, OSError, subprocess.TimeoutExpired):
                            state = "held"
                        label = "원래 대화로 전달할 수 있습니다" if state == "ready" else "원래 대화가 작업 중입니다 · 응답은 대기합니다" if state == "queued" else "세션 연결 확인 필요 · 응답은 보관됩니다"
                        return self.respond({"state": "listening" if state == "ready" else state, "label": label})
                    if len(parts) == 4 and parts[2] == "reply":
                        return self.respond(store.reply(parts[3], parts[1]))
                if len(parts) == 3 and parts[0] == "media":
                    artifact = store.artifact(parts[1])
                    path = Path(json.loads(artifact["media"])[parts[2]])
                    size = path.stat().st_size
                    start, end = 0, size - 1
                    partial = self.headers.get("Range")
                    if partial:
                        match = re.fullmatch(r"bytes=(\d+)-(\d*)", partial)
                        if not match:
                            return self.respond({"error": "unsupported range"}, code=416)
                        start = int(match[1]); end = min(int(match[2]) if match[2] else end, end)
                        if start > end:
                            return self.respond({"error": "invalid range"}, code=416)
                    self.send_response(206 if partial else 200)
                    self.send_header("Content-Type", mimetypes.guess_type(path)[0] or "application/octet-stream")
                    self.send_header("Content-Length", str(end - start + 1))
                    self.send_header("Accept-Ranges", "bytes")
                    self.send_header("X-Content-Type-Options", "nosniff")
                    if partial:
                        self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
                    self.end_headers()
                    if self.command != "HEAD":
                        with path.open("rb") as f:
                            f.seek(start); remaining = end - start + 1
                            while remaining:
                                chunk = f.read(min(1024 * 1024, remaining))
                                if not chunk:
                                    break
                                self.wfile.write(chunk); remaining -= len(chunk)
                    return
                return self.respond({"error": "not found"}, code=404)
            except (ValueError, KeyError, OSError):
                return self.respond({"error": "자료를 읽을 수 없습니다."}, code=404)

        def do_POST(self):
            origin = f"http://127.0.0.1:{self.server.server_port}"
            if not self.valid_host() or self.headers.get("Origin") != origin or self.headers.get("X-Reply-CSRF") != nonce:
                return self.respond({"error": "요청 출처를 확인할 수 없습니다."}, code=403)
            try:
                size = int(self.headers.get("Content-Length", "0"))
                if size < 2 or size > MAX_BODY:
                    raise ValueError("응답이 너무 큽니다.")
                body = json.loads(self.rfile.read(size))
                if not isinstance(body, dict):
                    raise ValueError("응답은 JSON 객체여야 합니다.")
                parts = urlsplit(self.path).path.strip("/").split("/")
                if len(parts) == 3 and parts[0] == "artifact" and parts[2] == "focus":
                    artifact = store.artifact(parts[1])
                    if not delivery:
                        return self.respond({"error": "미리보기에서는 세션을 이동하지 않습니다."}, code=409)
                    try:
                        return self.respond(Herdr(artifact["endpoint"]).focus(artifact))
                    except (ValueError, OSError, subprocess.TimeoutExpired) as error:
                        return self.respond({"error": str(error) if isinstance(error, ValueError) else "Herdr 연결을 확인하지 못했습니다. 세션은 새로 만들지 않았습니다."}, code=409)
                if len(parts) == 3 and parts[0] == "artifact" and parts[2] == "preview":
                    artifact = store.artifact(parts[1])
                    message = format_reply(artifact, normalize_payload(body, allow_empty=True), body.get("id", ""))
                    return self.respond({"message": message, "characters": len(message)})
                if len(parts) == 3 and parts[0] == "artifact" and parts[2] == "reply":
                    row = store.enqueue(parts[1], body)
                    if not delivery:
                        store.update_queued(row["id"], "held", "미리보기 모드입니다. 응답을 저장했으며 터미널에는 보내지 않았습니다.")
                    return self.respond(store.reply(row["id"], parts[1]), code=202)
                if len(parts) == 5 and parts[0] == "artifact" and parts[2] == "reply" and parts[4] == "retry":
                    row = store.reply(parts[3], parts[1])
                    if row["state"] != "held":
                        raise ValueError("전달 중이거나 결과가 불확실한 응답은 다시 보낼 수 없습니다.")
                    if delivery:
                        store.retry(row["id"], parts[1])
                    return self.respond(store.reply(parts[3], parts[1]))
                if len(parts) == 5 and parts[0] == "artifact" and parts[2] == "reply" and parts[4] == "cancel":
                    store.cancel(parts[3], parts[1])
                    return self.respond(store.reply(parts[3], parts[1]))
                return self.respond({"error": "not found"}, code=404)
            except ValueError as error:
                return self.respond({"error": str(error)}, code=400)
            except (TypeError, KeyError):
                return self.respond({"error": "응답 형식이나 상태를 확인하세요."}, code=400)

    if not port:
        try:
            port = int(json.loads((store.root / "server.json").read_text())["port"])
        except (OSError, ValueError, KeyError):
            pass
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    server.daemon_threads = True
    descriptor = {"port": server.server_port, "pid": os.getpid(), "delivery": delivery, "process_start": process_start(os.getpid())}
    (store.root / "server.json").write_text(json.dumps(descriptor))
    (store.root / "server.json").chmod(0o600)

    def worker():
        while not stopping.wait(1):
            if delivery:
                store.observe_turns(Herdr)
                for row in store.pending():
                    dispatch(store, row)

    threading.Thread(target=worker, daemon=True).start()
    try:
        server.serve_forever(poll_interval=0.2)
    finally:
        stopping.set(); server.server_close(); lock.close()


def running(store):
    try:
        info = json.loads((store.root / "server.json").read_text())
        with urlopen(f'http://127.0.0.1:{info["port"]}/health', timeout=1) as response:
            if json.load(response).get("ok"):
                return info
    except (OSError, ValueError, KeyError):
        pass
    return None


def clean_env(env=None):
    # Herdr pane variables would redirect the CLI to the calling pane's own socket.
    return {k: v for k, v in (env or os.environ).items() if k not in {"HERDR_SOCKET_PATH", "HERDR_SESSION", "HERDR_PANE_ID"}}


def herdr_executable(env=None):
    env = env or os.environ
    executable = env.get("HERDR_BIN_PATH") or shutil.which("herdr")
    if not executable:
        raise ValueError("herdr 실행 파일을 찾을 수 없습니다.")
    return executable


def herdr_session_for_socket(executable, socket, env=None):
    """Map the pane's socket path to the Herdr session name the CLI must be given."""
    result = subprocess.run([executable, "session", "list"], capture_output=True, text=True, timeout=10, env=clean_env(env))
    wanted = {socket, str(Path(socket).resolve())}
    for line in result.stdout.splitlines()[1:]:
        parts = line.split()
        if len(parts) >= 4 and parts[-1] in wanted:
            return parts[0]
    raise ValueError(f"소켓 {socket}에 해당하는 Herdr 세션을 찾지 못했습니다. --session을 지정하세요.")


def gjc_session_id(processes):
    # GJC keeps its native ID only in its private SDK descriptor; the descriptor must name the foreground PID.
    for owner in foreground_owners(processes, "gjc"):
        cwd = owner.get("cwd")
        if not cwd or not Path(cwd).is_absolute():
            continue
        folder = Path(cwd) / ".gjc/state/sdk"
        try:
            candidates = sorted(folder.glob("*.json"))
        except OSError:
            continue
        for path in candidates:
            try:
                info = path.lstat()
                if not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid() or info.st_mode & 0o077:
                    continue
                data = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, ValueError, TypeError):
                continue
            if isinstance(data, dict) and data.get("version") == 1 and data.get("pid") == owner["pid"] and data.get("sessionId") == path.stem:
                return path.stem
    return None


def detect_origin(env=None):
    """Identify the Herdr session, agent and native conversation ID of the pane running this process."""
    env = env or os.environ
    pane_id, socket = env.get("HERDR_PANE_ID"), env.get("HERDR_SOCKET_PATH")
    if not pane_id or not socket:
        raise ValueError("Herdr 패널 안에서 실행되지 않았습니다(HERDR_PANE_ID 없음). --session, --agent, --conversation을 직접 지정하세요.")
    executable = herdr_executable(env)
    endpoint = herdr_session_for_socket(executable, socket, env)
    herdr = Herdr(endpoint, executable)
    pane = herdr.call("pane", "get", pane_id).get("pane", {})
    agent = pane.get("agent")
    if agent in {"claude", "codex"}:
        session = pane.get("agent_session") or {}
        conversation = session.get("value") if session.get("kind") == "id" and session.get("source") == "herdr:" + agent else None
        if not conversation:
            raise ValueError(f"패널 {pane_id}의 {agent} 대화 ID를 Herdr가 아직 모릅니다. 잠시 뒤 다시 실행하거나 --conversation을 지정하세요.")
    elif agent == "gjc":
        info = herdr.call("pane", "process-info", "--pane", pane_id)["process_info"]
        conversation = gjc_session_id(info.get("foreground_processes", []))
        if not conversation:
            raise ValueError(f"패널 {pane_id}의 GJC 세션 descriptor를 찾지 못했습니다. --conversation을 지정하세요.")
    else:
        raise ValueError(f"패널 {pane_id}에서 에이전트를 확인하지 못했습니다(agent={agent!r}).")
    return {"endpoint": endpoint, "agent": agent, "conversation": conversation, "pane": pane_id}


def ensure_service(store):
    """Return the running service record, starting a detached server first when none answers."""
    info = running(store)
    if info:
        return info, False
    store.root.mkdir(parents=True, exist_ok=True)
    log = (store.root / "service.log").open("a")
    subprocess.Popen([sys.executable, str(Path(__file__).resolve()), "--state-dir", str(store.root), "serve"],
                     stdin=subprocess.DEVNULL, stdout=log, stderr=log, start_new_session=True, env=clean_env())
    # A cold Python start plus socket bind completes well under a second; 5 s leaves room for a loaded machine.
    for _ in range(50):
        time.sleep(0.1)
        info = running(store)
        if info:
            return info, True
    raise ValueError(f"회신 서비스가 5초 안에 뜨지 않았습니다. {store.root / 'service.log'}를 확인하세요.")


def run_checks(path):
    """Run the skill's syntax and design checks; return the failing report or None."""
    scripts = Path(__file__).resolve().parent
    for label, command in (("syntax", ["bash", str(scripts / "verify.sh"), "--syntax", str(path)]),
                           ("design", [sys.executable, "-I", str(scripts / "check-design.py"), str(path)])):
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        try:
            report = json.loads(result.stdout.strip().splitlines()[-1])
        except (ValueError, IndexError):
            report = {"ok": False, "errors": [result.stderr.strip() or f"{label} check produced no report"]}
        if not report.get("ok"):
            return {"check": label, "report": report}
    return None


def publish(store, args):
    path = Path(args.file).expanduser().resolve(strict=True)
    failed = run_checks(path)
    if failed:
        print(json.dumps({"delivery": False, "file": str(path), **failed}, ensure_ascii=False))
        return 1
    given = (args.session, args.agent, args.conversation)
    try:
        if all(given):
            origin = {"endpoint": args.session, "agent": args.agent, "conversation": args.conversation, "pane": None}
        elif any(given):
            raise ValueError("--session, --agent, --conversation은 셋 다 주거나 셋 다 생략합니다.")
        else:
            origin = detect_origin()
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        file_url = path.as_uri()
        print(json.dumps({"delivery": False, "file": str(path), "file_url": file_url, "reason": str(error)}, ensure_ascii=False))
        if not args.no_open:
            webbrowser.open(file_url)
        return 3
    info, started = ensure_service(store)
    artifact = store.register(str(path), args.title, origin["agent"], origin["conversation"], origin["endpoint"], args.conversation_label)
    url = f'http://127.0.0.1:{info["port"]}/artifact/{artifact["id"]}'
    print(json.dumps({"url": url, "artifact": artifact["id"], "revision": artifact["revision"][:12], "delivery": info["delivery"],
                      "agent": origin["agent"], "conversation": origin["conversation"], "endpoint": origin["endpoint"], "pane": origin["pane"],
                      "service_started": started, "log": str(store.root / "service.log")}, ensure_ascii=False))
    if not args.no_open:
        webbrowser.open(url)
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state-dir", required=True, help="Persistent, private reply directory owned by this workflow")
    sub = parser.add_subparsers(dest="command", required=True)
    start = sub.add_parser("serve", help="Run the local reply service until stopped; no boot registration")
    start.add_argument("--port", type=int, default=0)
    start.add_argument("--preview", action="store_true", help="Save replies without sending terminal input")
    launch = sub.add_parser("open", help="Register a frozen HTML revision and open its reply view")
    launch.add_argument("file")
    launch.add_argument("--title")
    launch.add_argument("--session", required=True, help="Explicit Herdr server session, such as default")
    launch.add_argument("--conversation", required=True, help="Native conversation ID from the originating agent")
    launch.add_argument("--conversation-label", default="", help="Human-readable task name; display only, never used for routing")
    launch.add_argument("--agent", choices=["codex", "claude", "gjc"], required=True)
    launch.add_argument("--no-open", action="store_true")
    ship = sub.add_parser("publish", help="Check the page, detect this pane's conversation, start the service if needed, register and open")
    ship.add_argument("file")
    ship.add_argument("--title")
    ship.add_argument("--conversation-label", default="", help="Human-readable task name; display only")
    ship.add_argument("--session", help="Override auto-detection; requires --agent and --conversation too")
    ship.add_argument("--agent", choices=["codex", "claude", "gjc"])
    ship.add_argument("--conversation")
    ship.add_argument("--no-open", action="store_true")
    receiver = sub.add_parser("receive", help="Wait in the originating Codex tool call; returns one reply without terminal input")
    receiver.add_argument("artifact")
    receiver.add_argument("--timeout", type=float, default=300, help="Bounded wait in seconds; the caller may run it as a yielded tool process")
    inspect = sub.add_parser("inspect", help="Resolve a compact artifact/reply reference to its source and complete stored answers")
    inspect.add_argument("artifact")
    inspect.add_argument("--reply")
    sub.add_parser("status", help="Show service state and pending reply counts")
    sub.add_parser("stop", help="Stop only this state directory's recorded server instance; retain replies")
    args = parser.parse_args()
    store = Store(args.state_dir)
    if args.command == "serve":
        if running(store):
            parser.error("This state directory already has a running service.")
        serve(store, args.port, not args.preview)
    elif args.command == "open":
        info = running(store)
        if not info:
            parser.error("Start serve in a managed background process first; its stdout/stderr belong in your task log.")
        artifact = store.register(args.file, args.title, args.agent, args.conversation, args.session, args.conversation_label)
        url = f'http://127.0.0.1:{info["port"]}/artifact/{artifact["id"]}'
        print(json.dumps({"url": url, "artifact": artifact["id"], "revision": artifact["revision"], "delivery": info["delivery"]}))
        if not args.no_open:
            webbrowser.open(url)
    elif args.command == "publish":
        sys.exit(publish(store, args))
    elif args.command == "receive":
        if args.timeout <= 0:
            parser.error("timeout must be positive")
        print(json.dumps(store.receive(args.artifact, os.environ.get("CODEX_THREAD_ID"), args.timeout), ensure_ascii=False), flush=True)
    elif args.command == "inspect":
        artifact = store.artifact(args.artifact)
        result = {key: artifact[key] for key in ("id", "title", "path", "revision", "agent", "conversation", "conversation_label", "endpoint")}
        if args.reply:
            with store.connect() as db:
                row = db.execute("SELECT * FROM replies WHERE id=? AND artifact=?", (args.reply, args.artifact)).fetchone()
            if not row:
                parser.error("Reply does not belong to this artifact.")
            result["reply"] = {"id": row["id"], "state": row["state"], "payload": json.loads(row["payload"])}
        print(json.dumps(result, ensure_ascii=False))
    elif args.command == "stop":
        info = running(store)
        if not info:
            print(json.dumps({"running": False}))
        elif not info.get("process_start") or info["process_start"] != process_start(info["pid"]):
            parser.error("Server process identity changed; refusing to signal it.")
        else:
            os.kill(info["pid"], signal.SIGTERM)
            print(json.dumps({"stop_requested": True, "pid": info["pid"]}))
    else:
        with store.connect() as db:
            counts = {r[0]: r[1] for r in db.execute("SELECT state,count(*) FROM replies GROUP BY state")}
        print(json.dumps({"server": running(store), "replies": counts}))


if __name__ == "__main__":
    main()
