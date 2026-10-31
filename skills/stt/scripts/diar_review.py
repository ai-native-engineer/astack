#!/usr/bin/env python3
"""Review a stt_diarize.sh result in the browser: play turns and name speakers.

usage: diar_review.py <run-dir> [--audio PATH] [--port N] [--idle-minutes M] [--no-open]

Serves assets/diar-review.html on 127.0.0.1 and prints its address. Naming a
speaker rewrites this run's names.json and diarized.md; with "remember" it also
stores the voice through voices.py so later runs find the same person. The
server stops on its own once the page has been closed for --idle-minutes.
"""

from __future__ import annotations

import argparse
import hmac
import http.server
import json
from pathlib import Path
import re
import secrets
import sys
import threading
import time
from urllib.parse import parse_qs, urlsplit
import webbrowser

import diar_views
import voices

PAGE = Path(__file__).resolve().parent.parent / "assets" / "diar-review.html"
AUDIO_TYPES = {".m4a": "audio/mp4", ".mp4": "audio/mp4", ".mov": "video/quicktime",
               ".wav": "audio/wav", ".mp3": "audio/mpeg", ".aac": "audio/aac",
               ".flac": "audio/flac", ".ogg": "audio/ogg", ".opus": "audio/ogg",
               ".webm": "audio/webm", ".caf": "audio/x-caf"}
SAMPLE_SECONDS = 8.0
MAX_NAME_LENGTH = 40
# Brackets and asterisks would break the **[name]** markers in diarized.md.
BAD_NAME = re.compile(r"[\[\]*\n\r\t]")


class ReviewError(ValueError):
    """A request the page should show to the user instead of failing."""


class Run:
    def __init__(self, run_dir: Path, audio: Path | None = None):
        self.dir = run_dir.resolve()
        for name in ("transcript.json", "speakers.json"):
            if not (self.dir / name).is_file():
                raise SystemExit(f"{self.dir / name} not found; run stt_diarize.sh again for a reviewable result")
        meta_path = self.dir / "run.json"
        meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.is_file() else {}
        self.audio = audio.resolve() if audio else (Path(meta["audio"]) if meta.get("audio") else None)
        self.offset = float(meta.get("start") or 0.0)
        self.segments, self.gaps = diar_views.load_transcript(self.dir / "transcript.json")
        self.turns = [(start, end, label) for start, end, label, _ in self.segments]
        self.speakers = {k: v for k, v in voices.load_speakers(self.dir).items() if not k.startswith("_")}
        self.lock = threading.Lock()

    @property
    def names_path(self) -> Path:
        return self.dir / "names.json"

    def names(self) -> dict:
        if not self.names_path.is_file():
            return {}
        return json.loads(self.names_path.read_text(encoding="utf-8"))

    def sample(self, label: str) -> list[float] | None:
        """Up to SAMPLE_SECONDS from the longest turn nobody else overlaps."""
        own = [t for t in self.turns if t[2] == label]
        others = [t for t in self.turns if t[2] != label]
        clean = [t for t in own if not any(o[0] < t[1] and o[1] > t[0] for o in others)]
        if not own:
            return None
        start, end, _ = max(clean or own, key=lambda t: t[1] - t[0])
        start += max(0.0, (end - start - SAMPLE_SECONDS) / 2)
        return [round(start + self.offset, 2), round(min(end, start + SAMPLE_SECONDS) + self.offset, 2)]

    def state(self) -> dict:
        names = self.names()
        rows = [r for r in diar_views.turn_rows(self.segments, self.gaps, names) if r["label"] != "gap"]
        labels = sorted(set(self.speakers) | {t[2] for t in self.turns})
        return {
            "title": self.audio.name if self.audio else self.dir.name,
            "audio": bool(self.audio and self.audio.is_file()),
            "markdown": (self.dir / "diarized.md").read_text(encoding="utf-8")
            if (self.dir / "diarized.md").is_file() else "",
            "speakers": [{
                "label": label,
                "seconds": round(self.speakers.get(label, {}).get("seconds", 0.0), 1),
                "display": diar_views.display(label, names),
                "name": names.get(label, {}).get("name"),
                "sure": bool(names.get(label, {}).get("sure")),
                "manual": bool(names.get(label, {}).get("manual")),
                # A name kept to this recording should not start remembering on the next save.
                "remember": names.get(label, {}).get("remembered", True),
                "score": names.get(label, {}).get("score"),
                "sample": self.sample(label),
            } for label in labels],
            "rows": [{
                "label": row["label"],
                "display": diar_views.display(row["label"], names),
                "start": round(row["start"] + self.offset, 2),
                "end": round(row["end"] + self.offset, 2),
                "text": row["text"],
            } for row in rows],
            "voices": [{"name": n, "count": c} for n, c in sorted(voices.sample_counts().items())],
            "minEnrollSeconds": voices.MIN_ENROLL_SECONDS,
        }

    def save(self, names: dict) -> None:
        voices.write_private(self.names_path, names)
        text = diar_views.render(self.segments, self.gaps, self.offset, names)
        (self.dir / "diarized.md").write_text(text + "\n" if text else "", encoding="utf-8")

    def name(self, label: str, name: str, remember: bool) -> None:
        if label not in self.speakers:
            raise ReviewError(f"알 수 없는 화자입니다: {label}")
        name = " ".join(name.split())
        if not name or len(name) > MAX_NAME_LENGTH or BAD_NAME.search(name):
            raise ReviewError(f"이름은 1~{MAX_NAME_LENGTH}자로, [ ] * 없이 적어 주세요.")
        if remember:
            try:
                voices.enroll(self.dir, label, name)
            except SystemExit:
                raise ReviewError(f"말한 시간이 {voices.MIN_ENROLL_SECONDS:.0f}초보다 짧아 목소리를 기억할 수 없습니다. "
                                  "이 녹음에서만 이름을 붙여 주세요.") from None
        names = self.names()
        names[label] = {"name": name, "sure": True, "manual": True, "remembered": remember}
        self.save(names)

    def clear(self, label: str) -> None:
        names = self.names()
        names.pop(label, None)
        self.save(names)

    def forget(self, name: str) -> None:
        voices.forget(name)
        names = {k: v for k, v in self.names().items() if v.get("manual") or v.get("name") != name}
        self.save(names)


def make_server(run: Run, port: int = 0) -> http.server.ThreadingHTTPServer:
    token = secrets.token_urlsafe(16)

    class Handler(http.server.BaseHTTPRequestHandler):
        def log_message(self, *_args) -> None:
            pass

        def allowed(self) -> bool:
            server.last_seen = time.monotonic()
            query = parse_qs(urlsplit(self.path).query)
            host_ok = self.headers.get("Host") in (f"127.0.0.1:{server.server_port}",
                                                   f"localhost:{server.server_port}")
            token_ok = hmac.compare_digest(query.get("t", [""])[0], token)
            if not (host_ok and token_ok):
                self.send_error(403)
                return False
            return True

        def send_json(self, payload: dict, status: int = 200) -> None:
            body = json.dumps(payload, ensure_ascii=False).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self) -> None:
            if not self.allowed():
                return
            route = urlsplit(self.path).path
            if route == "/":
                body = PAGE.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                self.wfile.write(body)
            elif route == "/api/state":
                with run.lock:
                    self.send_json(run.state())
            elif route == "/api/ping":
                self.send_json({"ok": True})
            elif route == "/audio" and run.audio and run.audio.is_file():
                self.send_audio()
            else:
                self.send_error(404)

        def send_audio(self) -> None:
            size = run.audio.stat().st_size
            start, end = 0, size - 1
            match = re.fullmatch(r"bytes=(\d*)-(\d*)", self.headers.get("Range", ""))
            if match and (match[1] or match[2]):
                if match[1]:
                    start = int(match[1])
                    end = min(int(match[2]), size - 1) if match[2] else size - 1
                else:
                    start = max(0, size - int(match[2]))
                if start > end or start >= size:
                    self.send_response(416)
                    self.send_header("Content-Range", f"bytes */{size}")
                    self.end_headers()
                    return
                self.send_response(206)
                self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
            else:
                self.send_response(200)
            self.send_header("Content-Type", AUDIO_TYPES.get(run.audio.suffix.lower(), "application/octet-stream"))
            self.send_header("Accept-Ranges", "bytes")
            self.send_header("Content-Length", str(end - start + 1))
            self.end_headers()
            with run.audio.open("rb") as source:
                source.seek(start)
                left = end - start + 1
                while left > 0:
                    chunk = source.read(min(left, 1 << 16))
                    if not chunk:
                        break
                    try:
                        self.wfile.write(chunk)
                    except (BrokenPipeError, ConnectionResetError):
                        return
                    left -= len(chunk)

        def do_POST(self) -> None:
            if not self.allowed():
                return
            if self.headers.get("Content-Type", "").split(";")[0] != "application/json":
                self.send_error(415)
                return
            try:
                body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
                route = urlsplit(self.path).path
                with run.lock:
                    if route == "/api/name":
                        run.name(str(body.get("label", "")), str(body.get("name", "")), bool(body.get("remember")))
                    elif route == "/api/clear":
                        run.clear(str(body.get("label", "")))
                    elif route == "/api/forget":
                        run.forget(str(body.get("name", "")))
                    else:
                        self.send_error(404)
                        return
                    self.send_json(run.state())
            except ReviewError as exc:
                self.send_json({"error": str(exc)}, 400)
            except (ValueError, json.JSONDecodeError):
                self.send_json({"error": "요청을 읽지 못했습니다."}, 400)

    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), Handler)
    server.daemon_threads = True
    server.token = token
    server.last_seen = time.monotonic()
    server.url = f"http://127.0.0.1:{server.server_port}/?t={token}"
    return server


def stop_when_idle(server, idle_seconds: float) -> None:
    while True:
        time.sleep(min(30.0, idle_seconds))
        if time.monotonic() - server.last_seen > idle_seconds:
            server.shutdown()
            return


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--audio", type=Path, help="source audio when run.json is missing or moved")
    parser.add_argument("--port", type=int, default=0)
    parser.add_argument("--idle-minutes", type=float, default=10.0)
    parser.add_argument("--no-open", action="store_true")
    args = parser.parse_args()
    run = Run(args.run_dir, args.audio)
    server = make_server(run, args.port)
    threading.Thread(target=stop_when_idle, args=(server, args.idle_minutes * 60), daemon=True).start()
    print(server.url, flush=True)
    if not run.audio or not run.audio.is_file():
        print("audio not found; pass --audio to enable playback", file=sys.stderr)
    if not args.no_open:
        webbrowser.open(server.url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
