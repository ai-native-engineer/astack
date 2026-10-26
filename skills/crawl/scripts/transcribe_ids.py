#!/usr/bin/env python3
"""Execute shared caption acquisition for newline-delimited YouTube video IDs.

Only verified successes are cached. Acquisitions stay in persistent attempt
folders under <dest>/transcripts/<id>/, including unsuccessful refreshes.
"""

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone


VIDEO_ID = re.compile(r"[A-Za-z0-9_-]{11}\Z")
HELPERS = ("fetch-subs.sh", "captions.py")
# Pace distinct acquisitions, including the single explicitly transient retry.
ACQUISITION_INTERVAL = 4
TRANSIENT = re.compile(
    r"\b429\b|too many requests|HTTP(?: Error)?\s+(?:408|500|502|503|504)\b|"
    r"timed? out|connection (?:reset|refused)|network is unreachable|"
    r"temporary failure in name resolution",
    re.IGNORECASE,
)
PERMANENT = re.compile(
    r"malformed|invalid|parse|conversion|ffmpeg|unsupported|"
    r"authentication|sign in|not a bot|permission denied|no cues|zero cues",
    re.IGNORECASE,
)


def resolve_helpers(script_dir, environ):
    """Choose override, bundled pair, or canonical pair, never mixed copies."""
    if "YOUTUBE_SCRIPTS" in environ:
        override = environ["YOUTUBE_SCRIPTS"]
        if not override:
            raise ValueError("YOUTUBE_SCRIPTS must name a directory containing fetch-subs.sh and captions.py")
        directory = Path(override).expanduser().resolve()
    elif any((script_dir / name).exists() for name in HELPERS):
        directory = script_dir
    else:
        directory = (script_dir / "../../youtube/scripts").resolve()
    if not all((directory / name).is_file() for name in HELPERS):
        raise ValueError("caption helpers missing; set YOUTUBE_SCRIPTS to a directory containing fetch-subs.sh and captions.py")
    return directory


def load_captions(directory):
    spec = importlib.util.spec_from_file_location("crawl_shared_captions", directory / "captions.py")
    module = importlib.util.module_from_spec(spec)
    # Import the chosen copy without leaving bytecode in the shared/plugin tree.
    previous = sys.dont_write_bytecode
    try:
        sys.dont_write_bytecode = True
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = previous
    if not all(callable(getattr(module, name, None)) for name in ("load_document", "markdown")):
        raise ValueError("captions.py must provide load_document(path) and markdown(document)")
    return module


def digest(data):
    return hashlib.sha256(data).hexdigest()


def atomic_write(path, data):
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(prefix=f".{path.name}.", dir=path.parent, delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def load_bundle(path, video_id, video_dir, captions):
    """Delegate caption validation; verify identity and retained sibling files."""
    path = path.resolve()
    path.relative_to(video_dir.resolve())
    if path.name != f"{video_id}.captions.json":
        raise ValueError("unexpected captions JSON filename")
    document = captions.load_document(path)
    if document["video_id"] != video_id or not document["cues"]:
        raise ValueError("captions must match the video ID and contain cues")
    source = Path(document["source"]["path"]).resolve()
    if source.parent != path.parent or source.suffix.lower() != ".srt" or not source.is_file():
        raise ValueError("source SRT must remain beside captions JSON")
    if source.stat().st_size == 0:
        raise ValueError("source SRT is empty")
    metadata_path = path.with_name(f"{video_id}.metadata.json")
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    if metadata != document["metadata"]:
        raise ValueError("retained metadata does not match captions JSON")
    return document


def cached_success(video_id, report, video_dir, captions):
    try:
        receipt = json.loads((video_dir / "success.json").read_text(encoding="utf-8"))
        if receipt["status"] != "success" or receipt["video_id"] != video_id:
            return False
        relative = Path(receipt["captions_path"])
        if relative.is_absolute():
            return False
        path = video_dir / relative
        load_bundle(path, video_id, video_dir, captions)
        markdown = report.read_bytes()
        return (
            bool(markdown)
            and digest(path.read_bytes()) == receipt["captions_sha256"]
            and digest(markdown) == receipt["markdown_sha256"]
        )
    except (OSError, ValueError, UnicodeError, KeyError, TypeError):
        return False


def success_report(document, captions):
    markdown = captions.markdown(document)
    if not isinstance(markdown, str) or not markdown.startswith("---\n"):
        raise ValueError("caption converter did not produce Markdown frontmatter")
    frontmatter, separator, body = markdown[4:].partition("\n---\n")
    if not separator or not body.strip():
        raise ValueError("caption converter produced an empty report")
    return (
        "---\n" + frontmatter + '\ntranscript_status: "success"\n'
        + "caption_kind: " + json.dumps(document["kind"]) + "\n---\n" + body
    ).encode("utf-8")


def publish_success(video_id, path, report, video_dir, data):
    receipt_path = video_dir / "success.json"
    receipt = {
        "status": "success",
        "video_id": video_id,
        "captions_path": str(path.relative_to(video_dir)),
        "captions_sha256": digest(path.read_bytes()),
        "markdown_sha256": digest(data),
    }
    # Commit the report last: every preceding failure leaves the old report intact.
    # An interruption between writes leaves mismatched hashes, never a cache hit.
    try:
        atomic_write(receipt_path, (json.dumps(receipt, indent=2) + "\n").encode("utf-8"))
        atomic_write(report, data)
    except OSError:
        receipt_path.unlink(missing_ok=True)
        raise


def write_no_captions(video_id, report):
    if report.exists():
        text = report.read_text(encoding="utf-8")
        frontmatter = text[4:].partition("\n---\n")[0] if text.startswith("---\n") else ""
        if not re.search(r'^transcript_status: *[\"\']?no_captions[\"\']? *$', frontmatter, re.MULTILINE):
            # Unknown/legacy reports are also preserved, but never called success.
            return False
    processed = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    text = (
        f'---\ntitle: "YouTube {video_id}"\nurl: https://youtu.be/{video_id}\n'
        f'youtube_id: {video_id}\ntranscript_status: "no_captions"\n'
        f"processed_at: {processed}\n---\n\n# YouTube {video_id}\n\n## 자막\n\n_(자막 없음)_\n"
    )
    atomic_write(report, text.encode("utf-8"))
    return True


def acquire(video_id, video_dir, directory, run, sleep, stderr):
    for attempt_number in range(2):
        # mkdtemp is deliberate: source evidence survives this process and errors.
        attempt = Path(tempfile.mkdtemp(prefix="attempt-", dir=video_dir))
        result = run(
            ["bash", str(directory / "fetch-subs.sh"), f"https://www.youtube.com/watch?v={video_id}", str(attempt)],
            stdin=subprocess.DEVNULL, capture_output=True, text=True,
            encoding="utf-8", errors="replace", check=False,
        )
        # The shared helper emits sanitized diagnostics; never echo/eval stdout.
        diagnostics = result.stderr or ""
        if diagnostics:
            stderr.write(diagnostics)
            if not diagnostics.endswith("\n"):
                stderr.write("\n")
        if (
            attempt_number == 0 and result.returncode == 3
            and TRANSIENT.search(diagnostics) and not PERMANENT.search(diagnostics)
        ):
            print(f"{video_id}: transient acquisition error; retrying once after {ACQUISITION_INTERVAL}s", file=stderr)
            sleep(ACQUISITION_INTERVAL)
            continue
        return result, attempt


def transcribe(lines, destination, force=False, *, run=None, sleep=None, environ=None,
               script_dir=None, stdout=None, stderr=None):
    """Run a batch; inject subprocess.run/time.sleep for offline tests."""
    run = subprocess.run if run is None else run
    sleep = time.sleep if sleep is None else sleep
    environ = os.environ if environ is None else environ
    stdout = sys.stdout if stdout is None else stdout
    stderr = sys.stderr if stderr is None else stderr
    script_dir = Path(__file__).resolve().parent if script_dir is None else Path(script_dir).resolve()
    totals = dict(success=0, skip=0, no_captions=0, failure=0)
    ids = []
    seen = set()
    for number, line in enumerate(lines, 1):
        video_id = line.rstrip("\r\n")
        if not video_id:
            continue
        if not VIDEO_ID.fullmatch(video_id):
            print(f"input line {number}: expected exactly one 11-character video ID; rejected", file=stderr)
            totals["failure"] += 1
        elif video_id not in seen:
            ids.append(video_id)
            seen.add(video_id)

    def summary():
        print(" ".join(f"{key}={value}" for key, value in totals.items()), file=stdout)

    if not ids:
        summary()
        return 1 if totals["failure"] else 0
    try:
        directory = resolve_helpers(script_dir, environ)
        captions = load_captions(directory)
        destination = Path(destination).resolve()
        destination.mkdir(parents=True, exist_ok=True)
    except (OSError, ValueError, ImportError, SyntaxError) as error:
        print(f"transcribe-ids: helper/output setup failed: {error}", file=stderr)
        totals["failure"] += len(ids)
        summary()
        return 1

    attempted = False
    for video_id in ids:
        report = destination / f"{video_id}.md"
        video_dir = destination / "transcripts" / video_id
        if not force and cached_success(video_id, report, video_dir, captions):
            totals["skip"] += 1
            print(f"skip {video_id}", file=stdout)
            continue
        try:
            video_dir.mkdir(parents=True, exist_ok=True)
            # A failed forced refresh must be retried on the next ordinary run.
            # Only the success receipt is invalidated; no raw/report is removed.
            (video_dir / "success.json").unlink(missing_ok=True)
            if attempted:
                sleep(ACQUISITION_INTERVAL)
            attempted = True
            result, attempt = acquire(video_id, video_dir, directory, run, sleep, stderr)
            status = result.returncode
            if status == 2:
                recorded = write_no_captions(video_id, report)
                totals["no_captions"] += 1
                note = "" if recorded else " (existing report retained; not a current success)"
                print(f"no_captions {video_id}{note}", file=stdout)
                continue
            if status != 0:
                raise ValueError(f"fetch-subs exited {status}; check acquisition diagnostics and retry later")
            paths = [
                line.partition("=")[2] for line in result.stdout.splitlines()
                if line.startswith("CAPTIONS_PATH=")
            ]
            if len(paths) != 1:
                raise ValueError("fetch-subs must emit exactly one CAPTIONS_PATH")
            path = Path(paths[0])
            if not path.is_absolute():
                raise ValueError("CAPTIONS_PATH must be absolute")
            path.resolve().relative_to(attempt.resolve())
            document = load_bundle(path, video_id, video_dir, captions)
            data = success_report(document, captions)
            publish_success(video_id, path, report, video_dir, data)
        except (OSError, ValueError, UnicodeError, KeyError, TypeError, subprocess.SubprocessError) as error:
            totals["failure"] += 1
            print(
                f"failure {video_id}: {error}; prior report retained if present. "
                f"Inspect retained files under {video_dir} and rerun.",
                file=stderr,
            )
            continue
        totals["success"] += 1
        print(f"success {video_id}", file=stdout)
    summary()
    return 1 if totals["failure"] else 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", help="report directory; raw acquisitions are kept below transcripts/<id>/")
    parser.add_argument("--force", action="store_true", help="reacquire even a verified success")
    args = parser.parse_args(argv)
    return transcribe(sys.stdin, args.destination, args.force)


if __name__ == "__main__":
    sys.exit(main())
