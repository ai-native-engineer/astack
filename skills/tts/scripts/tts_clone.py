#!/usr/bin/env python3
"""Local TTS driver around mlx-audio (Qwen3-TTS by default).

Two data stores, on purpose:
  - VOICE STORE (persistent, local-only): reusable reference voices live in
    ~/.local/share/tts/voices/<name>/ (ref.wav + ref.txt). Override with
    --voice-dir, env TTS_VOICE_DIR, or ~/.config/tts/config.json.
  - PROJECT (ephemeral): generated audio + work files. Default is a fresh
    /tmp/tts-XXXX (pass --proj to pin a location). Use --out to also copy the
    finished output.wav to a directory or .wav path you want to keep.

Subcommands:
  prep   <media|wav> --voice NAME [--ref-text T | --ref-text-file F]
         Extract a clean reference clip (loudnorm, 24k mono) and store it in
         the local voice store. Uses apple-stt when reference text is omitted.
  voices List registered voices in the store.
  preptext (--text T | --text-file F) [--out F]
         Rewrite Korean script text into TTS-friendly spoken chunks.
  full   [--voice NAME | --preset-voice NAME | --instruct TEXT] (--text T | --text-file F)
         One-shot generation (whole text in a single pass).
  chunk  [--voice NAME | --preset-voice NAME | --instruct TEXT] (--text T | --text-file F)
         One sentence per line. Generate each separately, tail-fade+pad, concat.
         Writes manifest.json so single chunks can be re-rolled.
  regen  --proj DIR --seg N [--text "..." | --text-file F]
         Regenerate only chunk N (optionally edited) and rebuild output.wav.
  join   --proj DIR [--out DEST] [--loudnorm-out DEST]
         Re-concat existing normalized chunks (after manual edits).
  audit  --proj DIR [--tail 0.12] [--threshold -18]
         Flag raw chunks whose tail is still loud, a common clipped-ending sign.

DEST = a directory (writes output.wav inside) or an explicit *.wav path.
LOUDNORM DEST = a directory (writes output-loudnorm.wav inside) or an explicit *.wav path.
Runtime: mlx-audio (`mlx_audio.tts.generate`). Optional transcription: `apple-stt`.
Tools resolve from PATH plus standard Homebrew/uv locations. Model weights auto-download to the HF cache.
"""
import argparse, json, os, re, shlex, shutil, subprocess, sys, tempfile
from pathlib import Path

DEFAULT_MODEL = "mlx-community/Qwen3-TTS-12Hz-1.7B-Base-bf16"
DEFAULT_CUSTOM_MODEL = "mlx-community/Qwen3-TTS-12Hz-1.7B-CustomVoice-bf16"
DEFAULT_DESIGN_MODEL = "mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-bf16"
CONFIG_FILE = Path(
    os.environ.get("TTS_CONFIG_FILE", "~/.config/tts/config.json")
).expanduser()


def _load_config():
    try:
        value = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


_CONFIG = _load_config()
DEFAULT_VOICE = str(
    os.environ.get("TTS_DEFAULT_VOICE")
    or _CONFIG.get("default_voice")
    or "default"
)
DEFAULT_VOICE_DIR = Path(
    os.environ.get("TTS_VOICE_DIR")
    or _CONFIG.get("voice_dir")
    or "~/.local/share/tts/voices"
).expanduser()
WHISPER_MODEL = "mlx-community/whisper-large-v3-turbo"
# apple-stt uses locale tags; map mlx_audio --lang codes
_LANG_LOCALE = {"ko": "ko-KR", "en": "en-US"}


def _tool(name):
    found = shutil.which(name)
    if found:
        return found
    # Hermes background jobs can start with a minimal PATH that misses Homebrew.
    # Fall back to standard macOS locations before letting subprocess raise.
    for candidate in (
        f"~/.local/bin/{name}",
        f"/opt/homebrew/bin/{name}",
        f"/usr/local/bin/{name}",
        f"/usr/bin/{name}",
    ):
        candidate = str(Path(candidate).expanduser())
        if Path(candidate).exists():
            return candidate
    return name


FFMPEG = _tool("ffmpeg")
FFPROBE = _tool("ffprobe")
MLX_GENERATE = _tool("mlx_audio.tts.generate")
_MLX_STDIN_WRAPPER = """\
import json, runpy, sys

payload = json.load(sys.stdin)
private_flags = {"--text", "--ref_text", "--instruct"}
secrets = sorted(
    (payload[i + 1] for i, value in enumerate(payload[:-1]) if value in private_flags),
    key=len,
    reverse=True,
)

class RedactingStream:
    def __init__(self, raw):
        self.raw = raw

    def write(self, value):
        for secret in secrets:
            value = value.replace(secret, "<redacted>")
        return self.raw.write(value)

    def flush(self):
        return self.raw.flush()

    def __getattr__(self, name):
        return getattr(self.raw, name)

sys.stdout = RedactingStream(sys.stdout)
sys.stderr = RedactingStream(sys.stderr)
sys.argv = ["mlx_audio.tts.generate", *payload]
runpy.run_module("mlx_audio.tts.generate", run_name="__main__")
"""
# tail fade-out (~60ms) + leading declick + trailing silence; keeps chunk ends clean
NORM_AF = "afade=t=in:d=0.02,areverse,afade=t=in:d=0.06,areverse,apad=pad_dur={gap},aresample=24000"
EDIT_LOUDNORM_AF = "loudnorm=I=-16:TP=-1.5:LRA=11"

PHONETIC_RULES = [
    (re.compile(r"(?<![A-Za-z0-9])Claude\s+Code(?![A-Za-z0-9])", re.I), "클로드 코드"),
    (re.compile(r"(?<![A-Za-z0-9])Claude(?![A-Za-z0-9])", re.I), "클로드"),
    (re.compile(r"(?<![A-Za-z0-9])ChatGPT(?![A-Za-z0-9])", re.I), "챗지피티"),
    (re.compile(r"(?<![A-Za-z0-9])OpenAI(?![A-Za-z0-9])", re.I), "오픈에이아이"),
    (re.compile(r"(?<![A-Za-z0-9])CapCut(?![A-Za-z0-9])", re.I), "캡컷"),
    (re.compile(r"(?<![A-Za-z0-9])YouTube(?![A-Za-z0-9])", re.I), "유튜브"),
    (re.compile(r"(?<![A-Za-z0-9])Remotion(?![A-Za-z0-9])", re.I), "리모션"),
    (re.compile(r"(?<![A-Za-z0-9])GRANTER(?![A-Za-z0-9])", re.I), "그랜터"),
    (re.compile(r"(?<![A-Za-z0-9])HTML(?![A-Za-z0-9])", re.I), "에이치티엠엘"),
    (re.compile(r"(?<![A-Za-z0-9])API(?![A-Za-z0-9])", re.I), "에이피아이"),
    (re.compile(r"(?<![A-Za-z0-9])MCP(?![A-Za-z0-9])", re.I), "엠씨피"),
    (re.compile(r"(?<![A-Za-z0-9])PDF(?![A-Za-z0-9])", re.I), "피디에프"),
    (re.compile(r"(?<![A-Za-z0-9])CTA(?![A-Za-z0-9])", re.I), "씨티에이"),
    (re.compile(r"(?<![A-Za-z0-9])TTS(?![A-Za-z0-9])", re.I), "티티에스"),
    (re.compile(r"(?<![A-Za-z0-9])STT(?![A-Za-z0-9])", re.I), "에스티티"),
    (re.compile(r"(?<![A-Za-z0-9])AI(?![A-Za-z0-9])", re.I), "에이아이"),
    (re.compile(r"(?<![A-Za-z0-9])OS(?![A-Za-z0-9])", re.I), "오에스"),
]
URL_RE = re.compile(r"https?://\S+|www\.\S+", re.I)
SINO_DIGITS = ["영", "일", "이", "삼", "사", "오", "육", "칠", "팔", "구"]
SMALL_UNITS = ["", "십", "백", "천"]
SECTION_UNITS = ["", "만", "억", "조"]
ATTACH_UNITS = {"원", "만원", "억", "만", "위"}
SPACE_UNITS = {"일", "주", "초", "분", "명", "개"}
NUMBER_UNIT_RE = re.compile(
    r"(?<![A-Za-z0-9.])(\d+(?:\.\d+)?)\s*(만원|퍼센트|억|만|원|일|주|초|분|명|개|위|%)(?![A-Za-z0-9])"
)
SOFT_END_RE = re.compile(
    r"(,|，|;|:|그리고|그런데|하지만|또|또는|및|하고|하며|하면|하면서|인데|지만|위해서|께는)$"
)
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?。！？])\s+")


def run(cmd, *, display=None, **kw):
    shown = display or cmd
    print("  $", " ".join(str(c) for c in shown), file=sys.stderr)
    try:
        return subprocess.run(cmd, check=True, **kw)
    except FileNotFoundError:
        sys.exit(f"[tts] required tool not found: {cmd[0]} — install it or add it to PATH")
    except subprocess.CalledProcessError as exc:
        sys.exit(f"[tts] command failed with exit code {exc.returncode}: {shown[0]}")


def _python_from_launcher(launcher):
    path = Path(launcher).expanduser()
    if not path.is_file():
        sys.exit(
            "[tts] mlx_audio.tts.generate not found — install with "
            "`uv tool install mlx-audio` or add ~/.local/bin to PATH"
        )
    try:
        first = path.open(encoding="utf-8").readline().strip()
    except OSError as exc:
        sys.exit(f"[tts] cannot inspect mlx-audio launcher '{path}': {exc}")
    if not first.startswith("#!"):
        sys.exit(f"[tts] mlx-audio launcher has no Python shebang: {path}")
    parts = shlex.split(first[2:])
    if not parts:
        sys.exit(f"[tts] mlx-audio launcher has an invalid shebang: {path}")
    if Path(parts[0]).name == "env" and len(parts) > 1:
        python = shutil.which(parts[1])
    else:
        python = parts[0]
    if not python or not Path(python).is_file():
        sys.exit(f"[tts] mlx-audio Python runtime not found from launcher: {path}")
    return python


def _private_dir(path):
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True, mode=0o700)
    try:
        path.chmod(0o700)
    except OSError as exc:
        sys.exit(f"[tts] cannot secure private directory '{path}': {exc}")
    return path


def _private_file(path):
    path = Path(path)
    try:
        path.chmod(0o600)
    except OSError as exc:
        sys.exit(f"[tts] cannot secure private file '{path}': {exc}")
    return path


def ffprobe_dur(p):
    out = run(
        [FFPROBE, "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nk=1:nw=1", str(p)],
        capture_output=True, text=True)
    return float(out.stdout.strip())


def voice_store(args):
    d = (getattr(args, "voice_dir", None) or os.environ.get("TTS_VOICE_DIR")
         or str(DEFAULT_VOICE_DIR))
    return Path(d).expanduser()


def voice_path(args):
    name = str(args.voice)
    if not re.fullmatch(r"[\w][\w.-]*", name):
        sys.exit(f"[tts] invalid voice name '{name}'; use letters, numbers, '.', '_' or '-'")
    return voice_store(args) / name


def find_apple_stt():
    found = shutil.which("apple-stt")
    local = Path("~/scripts/apple-stt").expanduser()
    return found or (str(local) if local.is_file() and os.access(local, os.X_OK) else None)


def resolve_proj(args):
    """Pin args.proj to a usable dir (fresh /tmp/tts-XXXX if not given)."""
    if getattr(args, "proj", None):
        p = Path(args.proj).expanduser()
        _private_dir(p)
    else:
        p = Path(tempfile.mkdtemp(prefix="tts-"))
        p.chmod(0o700)
    args.proj = str(p)
    return p


def load_voice(args):
    dest = voice_path(args)
    ref, txt = dest / "ref.wav", dest / "ref.txt"
    if not ref.exists() or not txt.exists():
        sys.exit(f"[tts] voice '{args.voice}' not found in {voice_store(args)} "
                 f"— run `prep --voice {args.voice}` first")
    _private_dir(dest.parent)
    _private_dir(dest)
    _private_file(ref)
    _private_file(txt)
    return ref, _read_optional_text_file(txt, "reference text")


def _read_optional_text_file(path, label):
    try:
        return " ".join(Path(path).expanduser().read_text(encoding="utf-8").split())
    except OSError as exc:
        sys.exit(f"[tts] cannot read {label} '{path}': {exc}")


def generation_source(args):
    voice = getattr(args, "voice", None)
    preset = getattr(args, "preset_voice", None)
    instruct = getattr(args, "instruct", None)
    if getattr(args, "instruct_file", None):
        instruct = _read_optional_text_file(args.instruct_file, "instruction file")
    if instruct is not None:
        instruct = " ".join(instruct.split())
        if not instruct:
            sys.exit("[tts] instruction is empty")
    if voice and preset:
        sys.exit("[tts] choose either --voice or --preset-voice")
    if voice and instruct:
        sys.exit("[tts] --voice cannot be combined with --instruct; use --preset-voice for CustomVoice")
    if preset:
        preset = " ".join(preset.split())
        if not preset:
            sys.exit("[tts] preset voice is empty")
        source = {"mode": "preset", "preset_voice": preset}
        if instruct:
            source["instruct"] = instruct
        return source
    if instruct:
        return {"mode": "design", "instruct": instruct}

    args.voice = voice or DEFAULT_VOICE
    ref, _ = load_voice(args)
    return {
        "mode": "clone",
        "voice": args.voice,
        "ref_audio": str(ref.resolve()),
        "ref_text_file": str((ref.parent / "ref.txt").resolve()),
    }


def model_for_source(args, source):
    if getattr(args, "model", None):
        return args.model
    if source["mode"] == "preset":
        return DEFAULT_CUSTOM_MODEL
    if source["mode"] == "design":
        return DEFAULT_DESIGN_MODEL
    return DEFAULT_MODEL


def source_from_manifest(man):
    source = man.get("source")
    if isinstance(source, dict):
        return source
    if man.get("ref_audio"):
        ref_audio = Path(man["ref_audio"]).expanduser()
        source = {"mode": "clone", "ref_audio": str(ref_audio)}
        ref_text_file = ref_audio.with_name("ref.txt")
        if ref_text_file.exists():
            source["ref_text_file"] = str(ref_text_file)
        elif man.get("ref_text"):
            source["ref_text"] = man["ref_text"]  # legacy manifest fallback
        return source
    sys.exit("[tts] chunk manifest has no generation source")


def source_cli_args(source):
    mode = source.get("mode")
    if mode == "clone":
        ref_audio = Path(source.get("ref_audio", "")).expanduser()
        if not ref_audio.is_file():
            sys.exit(f"[tts] reference audio not found: {ref_audio}")
        if source.get("ref_text_file"):
            ref_text = _read_optional_text_file(source["ref_text_file"], "reference text")
        else:
            ref_text = " ".join(str(source.get("ref_text", "")).split())
        if not ref_text:
            sys.exit("[tts] reference text is empty")
        return ["--ref_audio", str(ref_audio), "--ref_text", ref_text]
    if mode == "preset":
        if not source.get("preset_voice"):
            sys.exit("[tts] preset generation source has no preset_voice")
        args = ["--voice", str(source["preset_voice"])]
        if source.get("instruct"):
            args += ["--instruct", str(source["instruct"])]
        return args
    if mode == "design":
        if not source.get("instruct"):
            sys.exit("[tts] design generation source has no instruction")
        return ["--instruct", str(source["instruct"])]
    sys.exit(f"[tts] unsupported generation source mode: {mode!r}")


def gen_one(model, source, text, out_dir, prefix, extra=None):
    if not text.strip():
        sys.exit("[tts] generation text is empty")
    out_dir = Path(out_dir)
    with tempfile.TemporaryDirectory(prefix=".tts-generate-", dir=out_dir) as tmp:
        tmp = Path(tmp)
        payload = ["--model", model, *source_cli_args(source),
                   "--text", text, "--output_path", str(tmp), "--file_prefix", prefix]
        if extra:
            payload += extra
        run(
            [_python_from_launcher(MLX_GENERATE), "-c", _MLX_STDIN_WRAPPER],
            input=json.dumps(payload), text=True,
            display=[MLX_GENERATE, "--model", model, "<private input via stdin>"],
        )
        hits = sorted(tmp.glob(f"{prefix}*.wav"))
        if not hits:
            sys.exit(f"[tts] generation produced no wav for prefix {prefix}")
        result = out_dir / f"{prefix}_000.wav"
        if len(hits) == 1:
            os.replace(hits[0], result)
        else:
            _concat(hits, result)
        return _private_file(result)


def gen_extra_from_args(args):
    flag_map = {
        "lang": "--lang_code",
        "duration_multiplier": "--duration_multiplier",
        "speed": "--speed",
        "ddpm_steps": "--ddpm_steps",
        "temperature": "--temperature",
        "top_p": "--top_p",
        "top_k": "--top_k",
        "repetition_penalty": "--repetition_penalty",
    }
    extra = []
    for attr, flag in flag_map.items():
        val = getattr(args, attr, None)
        if val is not None:
            extra += [flag, str(val)]
    return extra


def merge_gen_extra(base, overrides):
    merged = list(base)
    for flag, value in zip(overrides[::2], overrides[1::2]):
        if flag in merged:
            merged[merged.index(flag) + 1] = value
        else:
            merged += [flag, value]
    return merged


def load_manifest(proj):
    project = Path(proj).expanduser()
    path = project / "manifest.json"
    try:
        man = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        sys.exit(f"[tts] cannot read chunk manifest '{path}': {exc}")
    if not isinstance(man.get("segments"), list) or not man["segments"]:
        sys.exit(f"[tts] invalid chunk manifest '{path}': need non-empty segments")
    _private_dir(project)
    _private_file(path)
    return man


def write_manifest(proj, manifest):
    path = Path(proj) / "manifest.json"
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    _private_file(path)


def _concat(wavs, out):
    out = Path(out)
    listf = out.with_suffix(".concat.txt")
    listf.write_text("\n".join(f"file '{Path(w).resolve()}'" for w in wavs) + "\n",
                     encoding="utf-8")
    run([FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", str(listf),
         "-ar", "24000", "-ac", "1", "-c:a", "pcm_s16le", str(out)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    listf.unlink(missing_ok=True)
    _private_file(out)


def _normalize(raw, norm, gap):
    run([FFMPEG, "-y", "-i", str(raw), "-af", NORM_AF.format(gap=gap),
         "-ar", "24000", "-ac", "1", "-c:a", "pcm_s16le", str(norm)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    _private_file(norm)


def _deliver(src, out):
    """Copy the finished wav to a user-chosen DEST (dir or *.wav). Returns dest."""
    if not out:
        return None
    dst = Path(out).expanduser()
    dst = dst if dst.suffix.lower() == ".wav" else dst / "output.wav"
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return _private_file(dst)


def _deliver_loudnorm(src, out):
    """Render an edit-ready loudness-normalized copy. Returns dest."""
    if not out:
        return None
    dst = Path(out).expanduser()
    dst = dst if dst.suffix.lower() == ".wav" else dst / "output-loudnorm.wav"
    dst.parent.mkdir(parents=True, exist_ok=True)
    run([FFMPEG, "-y", "-i", str(src), "-af", EDIT_LOUDNORM_AF,
         "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le", str(dst)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return _private_file(dst)


def _read_text(args):
    if getattr(args, "text", None) is not None:
        return args.text
    if getattr(args, "text_file", None):
        try:
            return Path(args.text_file).read_text(encoding="utf-8")
        except OSError as exc:
            sys.exit(f"[tts] cannot read text file '{args.text_file}': {exc}")
    sys.exit("[tts] need --text or --text-file")


def _ko_under_10000(n):
    if n == 0:
        return SINO_DIGITS[0]
    out = []
    digits = list(map(int, str(n)))
    total = len(digits)
    for i, d in enumerate(digits):
        if d == 0:
            continue
        pos = total - i - 1
        if d == 1 and pos > 0:
            out.append(SMALL_UNITS[pos])
        else:
            out.append(SINO_DIGITS[d] + SMALL_UNITS[pos])
    return "".join(out)


def _int_to_ko(n):
    if n == 0:
        return SINO_DIGITS[0]
    parts = []
    section = 0
    while n:
        chunk = n % 10000
        if chunk:
            spoken = _ko_under_10000(chunk)
            unit = SECTION_UNITS[section] if section < len(SECTION_UNITS) else ""
            parts.append(spoken + unit)
        n //= 10000
        section += 1
    return "".join(reversed(parts))


def _number_to_ko(num):
    if "." not in num:
        return _int_to_ko(int(num))
    whole, frac = num.split(".", 1)
    spoken = _int_to_ko(int(whole)) + " 점 " + " ".join(SINO_DIGITS[int(d)] for d in frac)
    return spoken


def _convert_number_units(text):
    def repl(m):
        num, unit = m.group(1), m.group(2)
        spoken = _number_to_ko(num)
        if unit == "%":
            unit = "퍼센트"
        if unit in ATTACH_UNITS:
            return spoken + unit
        if unit in SPACE_UNITS or unit == "퍼센트":
            return spoken + " " + unit
        return spoken + unit
    return NUMBER_UNIT_RE.sub(repl, text)


def _apply_phonetic_rules(text):
    text = URL_RE.sub("링크", text)
    for pat, repl in PHONETIC_RULES:
        text = pat.sub(repl, text)
    return text


def _normalize_spaces(text):
    text = text.replace("\u00a0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\s+([,.!?;:])", r"\1", text)
    return text.strip()


def _is_soft_end(text):
    return bool(SOFT_END_RE.search(text.rstrip()))


def _split_long_line(line, max_chars):
    if len(line) <= max_chars:
        return [line]
    parts = [p.strip() for p in SENTENCE_SPLIT_RE.split(line) if p.strip()]
    if len(parts) <= 1:
        return [line]
    out, buf = [], ""
    for part in parts:
        if not buf:
            buf = part
        elif len(buf) + 1 + len(part) <= max_chars or _is_soft_end(buf):
            buf += " " + part
        else:
            out.append(buf)
            buf = part
    if buf:
        out.append(buf)
    return out


def _prep_segments(text, min_chars, max_chars):
    lines = []
    for raw in text.splitlines():
        line = _normalize_spaces(raw)
        if line:
            lines.extend(_split_long_line(line, max_chars))
    if not lines:
        return []

    segments, buf = [], ""
    for line in lines:
        if not buf:
            buf = line
            continue
        if _is_soft_end(buf) or len(buf) < min_chars:
            buf = _normalize_spaces(buf + " " + line)
        else:
            segments.append(buf)
            buf = line
    if buf:
        segments.append(buf)

    merged = []
    for seg in segments:
        if merged and (_is_soft_end(merged[-1]) or len(merged[-1]) < min_chars):
            merged[-1] = _normalize_spaces(merged[-1] + " " + seg)
        else:
            merged.append(seg)
    return merged


def _preptext_warnings(segments, max_chunks, max_chars):
    warnings = []
    if len(segments) > max_chunks:
        warnings.append(
            f"chunk count {len(segments)} > target {max_chunks}; audit risk may increase"
        )
    for i, seg in enumerate(segments, 1):
        if _is_soft_end(seg):
            warnings.append(f"seg_{i:04d} ends with a soft/continuing phrase")
        if len(seg) > max_chars:
            warnings.append(f"seg_{i:04d} is long ({len(seg)} chars); pronunciation may blur")
        if re.search(r"(?<![A-Za-z0-9])[A-Z]{2,}(?![A-Za-z0-9])", seg):
            warnings.append(f"seg_{i:04d} still contains uppercase acronym")
        if URL_RE.search(seg):
            warnings.append(f"seg_{i:04d} still contains URL")
    return warnings


def prep_spoken_text(text, *, convert_numbers=True, min_chars=18, max_chars=190):
    text = _apply_phonetic_rules(text)
    if convert_numbers:
        text = _convert_number_units(text)
    segments = _prep_segments(text, min_chars=min_chars, max_chars=max_chars)
    return segments


# ---- subcommands -----------------------------------------------------------

def cmd_preptext(args):
    segments = prep_spoken_text(
        _read_text(args),
        convert_numbers=not args.no_number_convert,
        min_chars=args.min_chars,
        max_chars=args.max_chars,
    )
    if not segments:
        sys.exit("[tts] preptext produced no non-empty segments")

    out_text = "\n\n".join(segments) + "\n"
    if args.out:
        dst = Path(args.out).expanduser()
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(out_text, encoding="utf-8")
        _private_file(dst)
        print(f"[tts] preptext -> {dst} ({len(segments)} chunks)", file=sys.stderr)
    else:
        sys.stdout.write(out_text)
        print(f"[tts] preptext chunks: {len(segments)}", file=sys.stderr)

    for warning in _preptext_warnings(segments, args.max_chunks, args.max_chars):
        print(f"[tts] WARN: {warning}", file=sys.stderr)

def cmd_prep(args):
    apple_stt = None
    if args.ref_text is not None:
        one = " ".join(args.ref_text.split())
    elif args.ref_text_file:
        one = _read_optional_text_file(args.ref_text_file, "reference text")
    else:
        apple_stt = find_apple_stt()
        if not apple_stt:
            sys.exit("[tts] apple-stt not found; pass --ref-text or --ref-text-file")
        one = None
    if one == "":
        sys.exit("[tts] reference text is empty")

    dest = voice_path(args)
    store = _private_dir(dest.parent)
    with tempfile.TemporaryDirectory(prefix=".tts-prep-", dir=store) as tmp:
        tmp = Path(tmp)
        ref, txt = tmp / "ref.wav", tmp / "ref.txt"
        af = "loudnorm=I=-16:TP=-1.5:LRA=11,aresample=24000"
        cmd = [FFMPEG, "-y"]
        if args.ss is not None:
            cmd += ["-ss", str(args.ss)]
        cmd += ["-i", str(Path(args.media).expanduser()), "-map", "0:a:0"]
        if args.dur is not None:
            cmd += ["-t", str(args.dur)]
        cmd += ["-af", af, "-ac", "1", "-c:a", "pcm_s16le", str(ref)]
        run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        duration = ffprobe_dur(ref)
        if duration <= 0:
            sys.exit("[tts] prepared reference audio is empty")
        if apple_stt:
            locale = _LANG_LOCALE.get(args.lang, args.lang)
            run([apple_stt, str(ref), "-o", str(txt), "-l", locale, "-q"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            try:
                one = " ".join(txt.read_text(encoding="utf-8").split())
            except OSError as exc:
                sys.exit(f"[tts] cannot read generated reference text: {exc}")
        if not one:
            sys.exit("[tts] reference text is empty")
        txt.write_text(one + "\n", encoding="utf-8")
        _private_dir(dest)
        os.replace(ref, dest / "ref.wav")
        os.replace(txt, dest / "ref.txt")
        _private_file(dest / "ref.wav")
        _private_file(dest / "ref.txt")
    print(f"[tts] voice '{args.voice}' stored: {dest} ({duration:.1f}s)")


def cmd_voices(args):
    store = voice_store(args)
    if not store.exists():
        print(f"[tts] no voices yet ({store})"); return
    _private_dir(store)
    print(f"[tts] voice store: {store}")
    for d in sorted(store.iterdir()):
        if (d / "ref.wav").exists():
            _private_dir(d)
            _private_file(d / "ref.wav")
            if (d / "ref.txt").exists():
                _private_file(d / "ref.txt")
            has_text = "yes" if (d / "ref.txt").exists() else "no"
            print(f"  {d.name:16} {ffprobe_dur(d/'ref.wav'):5.1f}s  ref_text={has_text}")


def cmd_full(args):
    source = generation_source(args)
    model = model_for_source(args, source)
    proj = resolve_proj(args)
    out = gen_one(model, source, _read_text(args), proj, "output",
                  extra=gen_extra_from_args(args) + ["--join_audio"])
    final = proj / "output.wav"
    if out != final:
        _concat([out], final)
    msg = f"[tts] full -> {final} ({ffprobe_dur(final):.1f}s)"
    dst = _deliver(final, args.out)
    if dst:
        msg += f"\n[tts] saved copy -> {dst}"
    ldst = _deliver_loudnorm(final, getattr(args, "loudnorm_out", None))
    if ldst:
        msg += f"\n[tts] saved loudnorm copy -> {ldst}"
    print(msg)


def cmd_chunk(args):
    source = generation_source(args)
    model = model_for_source(args, source)
    proj = resolve_proj(args)
    chunks = proj / "chunks"
    if (proj / "manifest.json").exists() or (chunks.exists() and any(chunks.iterdir())):
        sys.exit(f"[tts] chunk project already exists: {proj} — use regen/join or a new --proj")
    _private_dir(chunks)
    segs = [ln.strip() for ln in _read_text(args).splitlines() if ln.strip()]
    if not segs:
        sys.exit("[tts] text has no non-empty lines (one sentence per line)")
    gen_extra = gen_extra_from_args(args)
    manifest = {"model": model, "source": source,
                "gap": args.gap, "lang": args.lang, "gen_extra": gen_extra,
                "segments": segs}
    write_manifest(proj, manifest)
    for i, seg in enumerate(segs, 1):
        idx = f"{i:04d}"
        print(f">>> chunk {idx} ({len(seg)} chars)")
        raw = gen_one(model, source, seg + "\n\n", chunks, f"seg_{idx}",
                      extra=gen_extra)
        _normalize(raw, chunks / f"norm_{idx}.wav", args.gap)
    cmd_join(args)


def cmd_regen(args):
    proj = Path(args.proj).expanduser()
    man = load_manifest(proj)
    n = args.seg
    if n < 1 or n > len(man["segments"]):
        sys.exit(f"[tts] --seg out of range (1..{len(man['segments'])})")
    changed_text = args.text is not None or getattr(args, "text_file", None)
    if changed_text:
        text = _read_text(args).strip()
        if not text:
            sys.exit("[tts] regenerated text is empty")
        man["segments"][n - 1] = text
    chunks = proj / "chunks"; idx = f"{n:04d}"; seg = man["segments"][n - 1]
    print(f">>> regen chunk {idx} ({len(seg)} chars)")
    gen_extra = merge_gen_extra(man.get("gen_extra", []), gen_extra_from_args(args))
    raw = gen_one(man["model"], source_from_manifest(man), seg + "\n\n",
                  chunks, f"seg_{idx}", extra=gen_extra)
    _normalize(raw, chunks / f"norm_{idx}.wav", man["gap"])
    if changed_text:
        write_manifest(proj, man)
    cmd_join(args)


def cmd_join(args):
    proj = Path(args.proj).expanduser()
    count = len(load_manifest(proj)["segments"])
    norms = [proj / "chunks" / f"norm_{i:04d}.wav" for i in range(1, count + 1)]
    missing = [p.name for p in norms if not p.exists()]
    if missing:
        sys.exit(f"[tts] missing normalized chunks: {', '.join(missing)}")
    final = proj / "output.wav"
    _concat(norms, final)
    msg = f"[tts] output -> {final} ({ffprobe_dur(final):.1f}s, {len(norms)} chunks)"
    dst = _deliver(final, getattr(args, "out", None))
    if dst:
        msg += f"\n[tts] saved copy -> {dst}"
    ldst = _deliver_loudnorm(final, getattr(args, "loudnorm_out", None))
    if ldst:
        msg += f"\n[tts] saved loudnorm copy -> {ldst}"
    print(msg)


def _tail_max_volume(path, tail):
    proc = run(
        [FFMPEG, "-hide_banner", "-sseof", f"-{tail}", "-i", str(path),
         "-af", "volumedetect", "-f", "null", "-"],
        capture_output=True, text=True)
    text = proc.stderr + proc.stdout
    m = re.search(r"max_volume:\s*(-?\d+(?:\.\d+)?) dB", text)
    return float(m.group(1)) if m else None


def cmd_audit(args):
    proj = Path(args.proj).expanduser()
    count = len(load_manifest(proj)["segments"])
    chunks = [proj / "chunks" / f"seg_{i:04d}_000.wav" for i in range(1, count + 1)]
    missing = [p.name for p in chunks if not p.exists()]
    if missing:
        sys.exit(f"[tts] missing raw chunks: {', '.join(missing)}")
    flagged = []
    for p in chunks:
        mv = _tail_max_volume(p, args.tail)
        name = p.stem.replace("_000", "")
        if mv is None:
            print(f"{name}: unknown")
            continue
        risk = mv > args.threshold
        print(f"{name}: tail_max={mv:.1f} dB" + ("  RISK" if risk else ""))
        if risk:
            flagged.append(name)
    if flagged:
        print("[tts] flagged:", ", ".join(flagged))
        print("[tts] try regen on flagged chunks with --duration-multiplier 1.08 and/or shorter text")
    else:
        print("[tts] no loud tails above threshold")


def add_generation_tuning_args(parser):
    parser.add_argument("--duration-multiplier", dest="duration_multiplier",
                        type=float,
                        help="model duration multiplier; try 1.05-1.12 for clipped endings")
    parser.add_argument("--speed", type=float,
                        help="model speech speed")
    parser.add_argument("--ddpm-steps", dest="ddpm_steps", type=int,
                        help="diffusion steps; higher can improve quality but is slower")
    parser.add_argument("--temperature", type=float,
                        help="sampling temperature")
    parser.add_argument("--top-p", dest="top_p", type=float,
                        help="sampling top-p")
    parser.add_argument("--top-k", dest="top_k", type=int,
                        help="sampling top-k")
    parser.add_argument("--repetition-penalty", dest="repetition_penalty",
                        type=float,
                        help="sampling repetition penalty")


def add_text_args(parser, *, required=True):
    group = parser.add_mutually_exclusive_group(required=required)
    group.add_argument("--text")
    group.add_argument("--text-file", dest="text_file")


def add_generation_source_args(parser):
    source = parser.add_mutually_exclusive_group()
    source.add_argument(
        "--voice",
        help=f"registered reference voice (default: {DEFAULT_VOICE})",
    )
    source.add_argument(
        "--preset-voice", dest="preset_voice",
        help="Qwen3-TTS preset speaker, such as Aiden, Ryan, or Vivian",
    )
    instruction = parser.add_mutually_exclusive_group()
    instruction.add_argument(
        "--instruct",
        help="voice description, or style instruction with --preset-voice",
    )
    instruction.add_argument(
        "--instruct-file", dest="instruct_file",
        help="read voice description/style instruction from a UTF-8 file",
    )


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--voice-dir", dest="voice_dir", help="override voice store")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("prep"); p.add_argument("media")
    p.add_argument("--voice", required=True); p.add_argument("--ss", type=float)
    p.add_argument("--dur", type=float); p.add_argument("--lang", default="ko")
    ref_text = p.add_mutually_exclusive_group()
    ref_text.add_argument("--ref-text")
    ref_text.add_argument("--ref-text-file")
    p.set_defaults(func=cmd_prep)

    p = sub.add_parser("voices"); p.set_defaults(func=cmd_voices)

    p = sub.add_parser("preptext")
    add_text_args(p)
    p.add_argument("--out", help="write spoken TTS script to this file")
    p.add_argument("--min-chars", type=int, default=18,
                   help="merge very short segments with the next segment")
    p.add_argument("--max-chars", type=int, default=190,
                   help="warn when a segment is longer than this")
    p.add_argument("--max-chunks", type=int, default=25,
                   help="warn when chunk count exceeds this target")
    p.add_argument("--no-number-convert", action="store_true",
                   help="do not rewrite number+unit expressions")
    p.set_defaults(func=cmd_preptext)

    for name, fn in (("full", cmd_full), ("chunk", cmd_chunk)):
        p = sub.add_parser(name)
        add_generation_source_args(p)
        p.add_argument("--proj", help="work dir (default /tmp/tts-XXXX)")
        p.add_argument("--out", help="also save final to this dir or *.wav path")
        p.add_argument("--loudnorm-out", dest="loudnorm_out",
                       help="also render edit-ready loudnorm copy to this dir or *.wav path")
        add_text_args(p)
        p.add_argument(
            "--model",
            help="override the mode's default Qwen3-TTS model (for example VoxCPM2)",
        )
        p.add_argument("--gap", type=float, default=0.30)
        p.add_argument("--lang", default="ko")
        add_generation_tuning_args(p)
        p.set_defaults(func=fn)

    p = sub.add_parser("regen"); p.add_argument("--proj", required=True)
    p.add_argument("--seg", type=int, required=True)
    add_text_args(p, required=False)
    p.add_argument("--out", help="also save final to this dir or *.wav path")
    p.add_argument("--loudnorm-out", dest="loudnorm_out",
                   help="also render edit-ready loudnorm copy to this dir or *.wav path")
    add_generation_tuning_args(p)
    p.set_defaults(func=cmd_regen)

    p = sub.add_parser("join"); p.add_argument("--proj", required=True)
    p.add_argument("--out", help="also save final to this dir or *.wav path")
    p.add_argument("--loudnorm-out", dest="loudnorm_out",
                   help="also render edit-ready loudnorm copy to this dir or *.wav path")
    p.set_defaults(func=cmd_join)

    p = sub.add_parser("audit")
    p.add_argument("--proj", required=True)
    p.add_argument("--tail", type=float, default=0.12,
                   help="tail window in seconds to inspect on raw chunks")
    p.add_argument("--threshold", type=float, default=-18.0,
                   help="flag if tail max volume is above this dB value")
    p.set_defaults(func=cmd_audit)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
