#!/usr/bin/env python3
"""Lossless SRT ingestion and shared JSON, Markdown, and JavaScript outputs.

Run this file with --help for the CLI. Import it directly for the same validated
cue contract. Only explicitly auto-generated captions permit rolling reduction.
"""

import argparse
import html
import json
import math
import os
from pathlib import Path
import re
import sys
import tempfile
from datetime import datetime, timezone
from urllib.parse import quote, urlsplit


KINDS = ("manual", "auto", "unknown")
_INDEX = re.compile(r"[0-9]+\Z")
_TIME = r"([0-9]{2,}):([0-5][0-9]):([0-5][0-9])[,.]([0-9]{3})"
_TIMING = re.compile(rf"{_TIME}\s+-->\s+{_TIME}\Z")
_TIMESTAMP_SHAPE = r"(?:[+-]?[0-9]+:[^\s]*|[+-]?(?:nan|inf(?:inity)?))"
_TIMING_HEADER = re.compile(
    rf"^{_TIMESTAMP_SHAPE}\s*-->|-->\s*{_TIMESTAMP_SHAPE}$|^-->$"
    r"|^[+-]?[0-9]+:[^\s:]*:[^\s]*(?:\s|$)",
    re.IGNORECASE,
)
_TAG = re.compile(r"<!--.*?-->|</?[A-Za-z][^>]*>", re.DOTALL)
_BREAK = re.compile(r"<br\s*/?>", re.IGNORECASE)
_MARKDOWN_PUNCTUATION = re.compile(r"([\\`*_{}\[\]()#+\-.!|~=])")
_JS_NAME = re.compile(r"[A-Za-z_$][A-Za-z0-9_$]*\Z")
_JS_RESERVED = frozenset(
    "await break case catch class const continue debugger default delete do else "
    "enum export extends false finally for function if implements import in "
    "instanceof interface let new null package private protected public return "
    "static super switch this throw true try typeof var void while with yield "
    "arguments eval".split()
)


def _seconds(parts):
    hours, minutes, seconds, millis = map(int, parts)
    return hours * 3600 + minutes * 60 + seconds + millis / 1000


def _timing(line, number):
    match = _TIMING.fullmatch(line.strip())
    if not match:
        raise ValueError(f"Invalid or empty SRT timestamp at line {number}")
    try:
        return _seconds(match.groups()[:4]), _seconds(match.groups()[4:])
    except (OverflowError, ValueError) as error:
        raise ValueError(f"Nonfinite SRT timestamp at line {number}") from error


def _caption_text(lines):
    # Strip actual markup before decoding entities: an encoded '<' is dialogue.
    cleaned = html.unescape(_TAG.sub("", _BREAK.sub("\n", "\n".join(lines))))
    return "\n".join(line for line in cleaned.split("\n") if line.strip())


def parse_srt(text: str) -> list[dict]:
    """Parse index/timestamp pairs, never blank-line blocks or numeric dialogue."""
    if not isinstance(text, str):
        raise ValueError("SRT input must be text")
    lines = text.lstrip("\ufeff").replace("\r\n", "\n").replace("\r", "\n").split("\n")
    position = 0
    while position < len(lines) and not lines[position].strip():
        position += 1
    if position == len(lines):
        raise ValueError("SRT contains no valid cues")
    cues = []
    while position < len(lines):
        if not _INDEX.fullmatch(lines[position].strip()):
            raise ValueError(f"Expected an SRT index at line {position + 1}")
        if position + 1 >= len(lines):
            raise ValueError(f"Missing SRT timestamp after line {position + 1}")
        start, end = _timing(lines[position + 1], position + 2)
        position += 2
        body = []
        while position < len(lines):
            line = lines[position].strip()
            following = lines[position + 1].strip() if position + 1 < len(lines) else ""
            if _INDEX.fullmatch(line) and _TIMING_HEADER.search(following):
                # Timestamp-shaped headers fail closed; an arrow alone in
                # dialogue (such as '42\nx --> y') does not start a cue.
                break
            if _TIMING.fullmatch(line):
                raise ValueError(f"SRT timestamp has no index at line {position + 1}")
            body.append(lines[position])
            position += 1
        cues.append({"start": start, "end": end, "text": _caption_text(body)})
    return _validate_cues(cues)


def _valid_time(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    try:
        return math.isfinite(value) and value >= 0
    except OverflowError:
        return False


def _validate_cues(cues):
    if not isinstance(cues, list) or not cues:
        raise ValueError("Captions must contain a nonempty list of valid cues")
    validated = []
    last_start = -1
    for index, cue in enumerate(cues, 1):
        if not isinstance(cue, dict):
            raise ValueError(f"Cue {index} must be an object")
        start, end, text = cue.get("start"), cue.get("end"), cue.get("text")
        if not _valid_time(start) or not _valid_time(end):
            raise ValueError(f"Cue {index} timestamps must be finite, nonnegative numbers")
        if end < start:
            raise ValueError(f"Cue {index} end must not precede start")
        if start < last_start:
            raise ValueError(f"Cue {index} violates stable start ordering")
        if not isinstance(text, str) or not text.strip():
            raise ValueError(f"Cue {index} has empty or invalid text")
        validated.append({"start": start, "end": end, "text": text})
        last_start = start
    return validated


def normalize_cues(cues, kind: str) -> list[dict]:
    """Preserve timings and speech; reduce only overlapping adjacent auto rolls.

    Strict temporal overlap is required, not adjacency after an end or a gap.
    Prefix growth must add a word/line boundary. Whole-line window rolls require
    multiline cues; uncertain partial-word/suffix matches are deliberately kept.
    The preceding *input* interval is used, so a long merged span cannot bridge
    a later silence. Output intervals are unions of observed intervals only.
    """
    if kind not in KINDS:
        raise ValueError(f"Unknown caption kind: {kind!r}")
    validated = _validate_cues(cues)
    if kind != "auto":
        return validated
    result = []
    previous = None
    for cue in validated:
        merged_text = None
        if previous is not None and cue["start"] < min(previous["end"], cue["end"]):
            old, new = previous["text"], cue["text"]
            if old == new:
                merged_text = result[-1]["text"]
            elif new.startswith(old) and new[len(old):len(old) + 1].isspace():
                merged_text = result[-1]["text"][:-len(old)] + new
            else:
                old_lines, new_lines = old.split("\n"), new.split("\n")
                if len(old_lines) > 1 and len(new_lines) > 1:
                    for count in range(min(len(old_lines), len(new_lines)) - 1, 0, -1):
                        if old_lines[-count:] == new_lines[:count]:
                            merged_text = result[-1]["text"] + "\n" + "\n".join(new_lines[count:])
                            break
        if merged_text is None:
            result.append(dict(cue))
        else:
            result[-1]["text"] = merged_text
            result[-1]["end"] = max(result[-1]["end"], cue["end"])
        previous = cue
    return result


def _required_string(value, name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a nonempty string")
    return value


def _json_text(value):
    try:
        text = json.dumps(value, ensure_ascii=False, allow_nan=False, indent=2) + "\n"
        text.encode("utf-8")
        return text
    except (TypeError, ValueError, UnicodeError) as error:
        raise ValueError("Document must contain valid UTF-8 JSON values") from error


def _validate_document(document):
    if not isinstance(document, dict):
        raise ValueError("Caption document must be a JSON object")
    _required_string(document.get("video_id"), "video_id")
    _required_string(document.get("language"), "language")
    if document.get("kind") not in KINDS:
        raise ValueError("Document kind must be manual, auto, or unknown")
    source = document.get("source")
    if not isinstance(source, dict) or source.get("format") != "srt":
        raise ValueError("source must describe an SRT file")
    _required_string(source.get("path"), "source.path")
    if not isinstance(source.get("client"), str):
        raise ValueError("source.client must be a string")
    if not isinstance(document.get("metadata"), dict):
        raise ValueError("metadata must be an object")
    validated = dict(document)
    validated["source"] = dict(source)
    validated["metadata"] = dict(document["metadata"])
    # Validation is not normalization: loading/rendering never deduplicates again.
    validated["cues"] = _validate_cues(document.get("cues"))
    _json_text(validated)
    return validated


def make_document(srt_path, video_id, language, kind="unknown", title="", metadata=None, client="") -> dict:
    """Read an SRT without modifying it; unknown is for direct local ingestion."""
    if metadata is not None and not isinstance(metadata, dict):
        raise ValueError("metadata must be an object")
    if not isinstance(title, str):
        raise ValueError("title must be a string")
    info = dict(metadata) if metadata is not None else {}
    if title:
        info["title"] = title
    source = Path(srt_path).resolve()
    document = {
        "video_id": video_id,
        "language": language,
        "kind": kind,
        "source": {"path": str(source), "format": "srt", "client": client},
        "metadata": info,
        "cues": normalize_cues(parse_srt(source.read_text(encoding="utf-8-sig")), kind),
    }
    return _validate_document(document)


def _reject_constant(value):
    raise ValueError(f"Nonfinite JSON number is not allowed: {value}")


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def _read_json(path):
    return json.loads(
        Path(path).read_text(encoding="utf-8-sig"),
        parse_constant=_reject_constant,
        object_pairs_hook=_unique_object,
    )


def load_document(path) -> dict:
    """Load JSON only; relative source paths are relative to the JSON file."""
    document = _validate_document(_read_json(path))
    source = Path(document["source"]["path"])
    if not source.is_absolute():
        document["source"]["path"] = str((Path(path).resolve().parent / source).resolve())
    return document


def _protect_output(path, protected):
    target = Path(path)
    for original in protected:
        source = Path(original)
        if target.resolve() == source.resolve() or (
            target.exists() and source.exists() and os.path.samefile(target, source)
        ):
            raise ValueError("Output must not overwrite an input or source caption file")
    if target.suffix.lower() == ".srt":
        raise ValueError("Generated output must not overwrite source captions (.srt)")


def _atomic_write(path, text, protected=()):
    _protect_output(path, protected)
    # Encode before touching any output, including when JSON contains surrogates.
    data = text.encode("utf-8")
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(prefix=f".{target.name}.", dir=target.parent, delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, target)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def write_document(document, path):
    """Validate first, then atomically replace JSON without touching the SRT."""
    validated = _validate_document(document)
    _atomic_write(path, _json_text(validated), (validated["source"]["path"],))


def _clock(seconds):
    seconds = int(seconds)
    hours, rest = divmod(seconds, 3600)
    minutes, seconds = divmod(rest, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    return f"{minutes:02d}:{seconds:02d}"


def _metadata_string(metadata, key, default=""):
    value = metadata.get(key)
    return value if isinstance(value, str) and value.strip() else default


def _json_scalar(value):
    # YAML forbids raw C1 controls and normalizes raw Unicode line separators.
    text = json.dumps(value, ensure_ascii=False)
    for number in (*range(0x7f, 0xa0), 0x2028, 0x2029):
        text = text.replace(chr(number), f"\\u{number:04x}")
    return text


def _markdown_text(text):
    # Escape before HTML encoding so generated entities are not backslash-escaped.
    escaped = _MARKDOWN_PUNCTUATION.sub(r"\\\1", text)
    # Literal indentation must not create a code block where those escapes and
    # entities would be displayed verbatim instead of as the original dialogue.
    return re.sub(
        r"^[ \t]+", lambda match: "".join(f"&#{ord(character)};" for character in match[0]),
        html.escape(escaped), flags=re.MULTILINE,
    )


def _markdown_url(url):
    try:
        parts = urlsplit(url)
        if parts.scheme.lower() in ("http", "https") and parts.hostname and not any(
            character.isspace() or ord(character) < 32 or ord(character) == 0x7f for character in url
        ):
            return "<" + quote(url, safe=":/?#[]@!$&'()*+,;=%") + ">"
    except ValueError:
        pass
    return _markdown_text(" ".join(url.splitlines()))


def markdown(document) -> str:
    """Render the validated document offline, including every normalized cue."""
    document = _validate_document(document)
    metadata = document["metadata"]
    video_id, language = document["video_id"], document["language"]
    title = _metadata_string(metadata, "title", f"YouTube {video_id}")
    url = f"https://www.youtube.com/watch?v={quote(video_id, safe='')}"
    channel = _metadata_string(metadata, "channel")
    duration = _metadata_string(metadata, "duration_string")
    if not duration and _valid_time(metadata.get("duration")):
        duration = _clock(metadata["duration"])
    date = ""
    upload_date = metadata.get("upload_date")
    if isinstance(upload_date, str) and re.fullmatch(r"[0-9]{8}", upload_date):
        try:
            date = datetime.strptime(upload_date, "%Y%m%d").date().isoformat()
        except ValueError:
            pass
    frontmatter = {"title": title, "url": url, "channel": channel}
    if date:
        frontmatter["date"] = date
    if duration:
        frontmatter["duration"] = duration
    frontmatter.update({
        "lang": language,
        "youtube_id": video_id,
        "processed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    })
    lines = ["---"]
    lines.extend(f"{key}: {_json_scalar(value)}" for key, value in frontmatter.items())
    lines.extend(["---", "", f"# {_markdown_text(' '.join(title.splitlines()))}", "", f"- 영상: <{url}>"])
    if channel:
        channel_url = _metadata_string(metadata, "channel_url")
        lines.append(f"- 채널: {_markdown_text(' '.join(channel.splitlines()))}" + (f" {_markdown_url(channel_url)}" if channel_url else ""))
    if date:
        lines.append(f"- 발행: {date}")
    if duration:
        lines.append(f"- 길이: {_markdown_text(' '.join(duration.splitlines()))}")
    lines.extend(["", f"## 자막 ({_markdown_text(' '.join(language.splitlines()))})", ""])
    last_group = None
    for cue in document["cues"]:
        group = int(cue["start"] // 60)
        if group != last_group:
            lines.extend([f"### [{_clock(group * 60)}]", ""])
            last_group = group
        lines.extend(["  \n".join(_markdown_text(cue["text"]).split("\n")), ""])
    return "\n".join(lines)


def javascript(document, var_name="SUBS") -> str:
    """Serialize cues for a standalone file or inline script, not executable text."""
    if not isinstance(var_name, str) or not _JS_NAME.fullmatch(var_name) or var_name in _JS_RESERVED:
        raise ValueError("var_name must be a nonreserved ASCII JavaScript identifier")
    document = _validate_document(document)
    data = json.dumps(document["cues"], ensure_ascii=False, allow_nan=False)
    for character, escaped in (("<", "\\u003c"), (">", "\\u003e"), ("&", "\\u0026"), ("\u2028", "\\u2028"), ("\u2029", "\\u2029")):
        data = data.replace(character, escaped)
    return f"const {var_name} = {data};\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    normalize = commands.add_parser("normalize", help="SRT to validated captions JSON")
    normalize.add_argument("input")
    normalize.add_argument("output")
    normalize.add_argument("--video-id", required=True)
    normalize.add_argument("--language", required=True)
    normalize.add_argument("--kind", choices=KINDS, default="unknown")
    normalize.add_argument("--metadata", help="Existing yt-dlp metadata JSON (no network access)")
    for command in ("markdown", "javascript"):
        renderer = commands.add_parser(command, help=f"Render captions JSON as {command}")
        renderer.add_argument("input")
        renderer.add_argument("output")
        if command == "javascript":
            renderer.add_argument("--var-name", default="SUBS")
    validate = commands.add_parser("validate", help="Validate captions JSON without modifying it")
    validate.add_argument("input")
    args = parser.parse_args(argv)
    try:
        if args.command == "normalize":
            metadata = _read_json(args.metadata) if args.metadata else None
            document = make_document(args.input, args.video_id, args.language, args.kind, metadata=metadata)
            protected = [args.input]
            if args.metadata:
                protected.append(args.metadata)
            _protect_output(args.output, protected)
            write_document(document, args.output)
        else:
            document = load_document(args.input)
            if args.command != "validate":
                output = markdown(document) if args.command == "markdown" else javascript(document, args.var_name)
                _atomic_write(args.output, output, (args.input, document["source"]["path"]))
    except (OSError, ValueError, UnicodeError) as error:
        print(f"captions: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
