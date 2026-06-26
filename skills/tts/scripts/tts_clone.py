#!/usr/bin/env python3
"""Local voice-clone TTS driver around mlx-audio (default Qwen3-TTS).

Two data stores, on purpose:
  - VOICE STORE (persistent): reusable reference voices live in
    ~/.local/share/tts/voices/<name>/ (ref.wav + ref.txt). Override with
    --voice-dir or env TTS_VOICE_DIR. Never put these in /tmp or git.
  - PROJECT (ephemeral): generated audio + work files. Default is a fresh
    /tmp/tts-XXXX (pass --proj to pin a location). Use --out to also copy the
    finished output.wav to a directory or .wav path you want to keep.

Subcommands:
  prep   <media|wav> --voice NAME [--ss S --dur D --lang ko]
         Extract a clean reference clip (loudnorm, 24k mono) + transcribe with
         mlx_whisper -> <store>/NAME/ref.wav, ref.txt
  voices List registered voices in the store.
  preptext (--text T | --text-file F) [--out F]
         Rewrite Korean script text into TTS-friendly spoken chunks.
  full   --voice NAME (--text T | --text-file F) [--proj DIR] [--out DEST] [--loudnorm-out DEST] [--model M]
         One-shot generation (whole text in a single pass).
  chunk  --voice NAME --text-file F [--proj DIR] [--out DEST] [--loudnorm-out DEST] [--model M] [--gap 0.30]
         One sentence per line. Generate each separately, tail-fade+pad, concat.
         Writes manifest.json so single chunks can be re-rolled.
  regen  --proj DIR --seg N [--text "..."] [--out DEST] [--loudnorm-out DEST]
         Regenerate only chunk N (optionally edited) and rebuild output.wav.
  join   --proj DIR [--out DEST] [--loudnorm-out DEST]
         Re-concat existing normalized chunks (after manual edits).
  audit  --proj DIR [--tail 0.12] [--threshold -18]
         Flag raw chunks whose tail is still loud, a common clipped-ending sign.

DEST = a directory (writes output.wav inside) or an explicit *.wav path.
LOUDNORM DEST = a directory (writes output-loudnorm.wav inside) or an explicit *.wav path.
Runtime: mlx-audio (`mlx_audio.tts.generate`). Transcription: `mlx_whisper`.
Both resolved from PATH. Weights auto-download to the HF cache by repo id.
"""
import argparse, json, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

DEFAULT_MODEL = "mlx-community/Qwen3-TTS-12Hz-1.7B-Base-bf16"
WHISPER_MODEL = "mlx-community/whisper-large-v3-turbo"
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


def run(cmd, **kw):
    print("  $", " ".join(str(c) for c in cmd), file=sys.stderr)
    return subprocess.run(cmd, check=True, **kw)


def ffprobe_dur(p):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nk=1:nw=1", str(p)],
        capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def voice_store(args):
    d = (getattr(args, "voice_dir", None) or os.environ.get("TTS_VOICE_DIR")
         or str(Path.home() / ".local/share/tts/voices"))
    return Path(d).expanduser()


def resolve_proj(args):
    """Pin args.proj to a usable dir (fresh /tmp/tts-XXXX if not given)."""
    if getattr(args, "proj", None):
        p = Path(args.proj).expanduser()
        p.mkdir(parents=True, exist_ok=True)
    else:
        p = Path(tempfile.mkdtemp(prefix="tts-"))
    args.proj = str(p)
    return p


def load_voice(args):
    dest = voice_store(args) / args.voice
    ref, txt = dest / "ref.wav", dest / "ref.txt"
    if not ref.exists() or not txt.exists():
        sys.exit(f"[tts] voice '{args.voice}' not found in {voice_store(args)} "
                 f"— run `prep --voice {args.voice}` first")
    return ref, " ".join(txt.read_text(encoding="utf-8").split())


def gen_one(model, ref_audio, ref_text, text, out_dir, prefix, extra=None):
    cmd = ["mlx_audio.tts.generate", "--model", model,
           "--ref_audio", str(ref_audio), "--ref_text", ref_text,
           "--text", text, "--output_path", str(out_dir), "--file_prefix", prefix]
    if extra:
        cmd += extra
    run(cmd)
    hits = sorted(Path(out_dir).glob(f"{prefix}*.wav"))
    if not hits:
        sys.exit(f"[tts] generation produced no wav for prefix {prefix}")
    if len(hits) == 1:
        return hits[0]
    merged = Path(out_dir) / f"{prefix}_merged.wav"
    _concat(hits, merged)
    return merged


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


def _concat(wavs, out):
    out = Path(out)
    listf = out.with_suffix(".concat.txt")
    listf.write_text("\n".join(f"file '{Path(w).resolve()}'" for w in wavs) + "\n",
                     encoding="utf-8")
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(listf),
         "-ar", "24000", "-ac", "1", "-c:a", "pcm_s16le", str(out)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    listf.unlink(missing_ok=True)


def _normalize(raw, norm, gap):
    run(["ffmpeg", "-y", "-i", str(raw), "-af", NORM_AF.format(gap=gap),
         "-ar", "24000", "-ac", "1", "-c:a", "pcm_s16le", str(norm)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def _deliver(src, out):
    """Copy the finished wav to a user-chosen DEST (dir or *.wav). Returns dest."""
    if not out:
        return None
    dst = Path(out).expanduser()
    dst = dst if dst.suffix.lower() == ".wav" else dst / "output.wav"
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return dst


def _deliver_loudnorm(src, out):
    """Render an edit-ready loudness-normalized copy. Returns dest."""
    if not out:
        return None
    dst = Path(out).expanduser()
    dst = dst if dst.suffix.lower() == ".wav" else dst / "output-loudnorm.wav"
    dst.parent.mkdir(parents=True, exist_ok=True)
    run(["ffmpeg", "-y", "-i", str(src), "-af", EDIT_LOUDNORM_AF,
         "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le", str(dst)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return dst


def _read_text(args):
    if getattr(args, "text", None):
        return args.text
    if getattr(args, "text_file", None):
        return Path(args.text_file).read_text(encoding="utf-8")
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
        print(f"[tts] preptext -> {dst} ({len(segments)} chunks)", file=sys.stderr)
    else:
        sys.stdout.write(out_text)
        print(f"[tts] preptext chunks: {len(segments)}", file=sys.stderr)

    for warning in _preptext_warnings(segments, args.max_chunks, args.max_chars):
        print(f"[tts] WARN: {warning}", file=sys.stderr)

def cmd_prep(args):
    dest = voice_store(args) / args.voice
    dest.mkdir(parents=True, exist_ok=True)
    ref = dest / "ref.wav"
    af = "loudnorm=I=-16:TP=-1.5:LRA=11,aresample=24000"
    cmd = ["ffmpeg", "-y"]
    if args.ss is not None:
        cmd += ["-ss", str(args.ss)]
    cmd += ["-i", str(Path(args.media).expanduser()), "-map", "0:a:0"]
    if args.dur is not None:
        cmd += ["-t", str(args.dur)]
    cmd += ["-af", af, "-ac", "1", "-c:a", "pcm_s16le", str(ref)]
    run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    run(["mlx_whisper", str(ref), "--model", WHISPER_MODEL, "--language", args.lang,
         "--condition-on-previous-text", "False", "--output-format", "txt",
         "--output-dir", str(dest)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    txt = dest / "ref.txt"
    one = " ".join(txt.read_text(encoding="utf-8").split())
    txt.write_text(one + "\n", encoding="utf-8")
    print(f"[tts] voice '{args.voice}' stored: {dest} ({ffprobe_dur(ref):.1f}s)")
    print(f"[tts] ref_text: {one}")


def cmd_voices(args):
    store = voice_store(args)
    if not store.exists():
        print(f"[tts] no voices yet ({store})"); return
    print(f"[tts] voice store: {store}")
    for d in sorted(store.iterdir()):
        if (d / "ref.wav").exists():
            t = (d / "ref.txt").read_text(encoding="utf-8")[:48] if (d / "ref.txt").exists() else ""
            print(f"  {d.name:16} {ffprobe_dur(d/'ref.wav'):5.1f}s  {t}")


def cmd_full(args):
    ref, ref_text = load_voice(args)
    proj = resolve_proj(args)
    out = gen_one(args.model, ref, ref_text, _read_text(args), proj, "output",
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
    ref, ref_text = load_voice(args)
    proj = resolve_proj(args)
    chunks = proj / "chunks"; chunks.mkdir(parents=True, exist_ok=True)
    segs = [ln.strip() for ln in _read_text(args).splitlines() if ln.strip()]
    if not segs:
        sys.exit("[tts] text has no non-empty lines (one sentence per line)")
    gen_extra = gen_extra_from_args(args)
    manifest = {"model": args.model, "voice": args.voice,
                "ref_audio": str(ref.resolve()), "ref_text": ref_text,
                "gap": args.gap, "lang": args.lang, "gen_extra": gen_extra,
                "segments": segs}
    (proj / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    for i, seg in enumerate(segs, 1):
        idx = f"{i:04d}"
        print(f">>> chunk {idx}: {seg[:30]}...")
        raw = gen_one(args.model, ref, ref_text, seg + "\n\n", chunks, f"seg_{idx}",
                      extra=gen_extra)
        _normalize(raw, chunks / f"norm_{idx}.wav", args.gap)
    cmd_join(args)


def cmd_regen(args):
    proj = Path(args.proj).expanduser()
    man = json.loads((proj / "manifest.json").read_text(encoding="utf-8"))
    n = args.seg
    if n < 1 or n > len(man["segments"]):
        sys.exit(f"[tts] --seg out of range (1..{len(man['segments'])})")
    if args.text:
        man["segments"][n - 1] = args.text.strip()
        (proj / "manifest.json").write_text(
            json.dumps(man, ensure_ascii=False, indent=2), encoding="utf-8")
    chunks = proj / "chunks"; idx = f"{n:04d}"; seg = man["segments"][n - 1]
    print(f">>> regen chunk {idx}: {seg[:30]}...")
    gen_extra = gen_extra_from_args(args) or man.get("gen_extra", [])
    if gen_extra != man.get("gen_extra", []):
        man["gen_extra"] = gen_extra
        (proj / "manifest.json").write_text(
            json.dumps(man, ensure_ascii=False, indent=2), encoding="utf-8")
    raw = gen_one(man["model"], man["ref_audio"], man["ref_text"], seg + "\n\n",
                  chunks, f"seg_{idx}", extra=gen_extra)
    _normalize(raw, chunks / f"norm_{idx}.wav", man["gap"])
    cmd_join(args)


def cmd_join(args):
    proj = Path(args.proj).expanduser()
    norms = sorted((proj / "chunks").glob("norm_*.wav"),
                   key=lambda p: int(p.stem.split("_")[1]))
    if not norms:
        sys.exit("[tts] no normalized chunks to join")
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
    proc = subprocess.run(
        ["ffmpeg", "-hide_banner", "-sseof", f"-{tail}", "-i", str(path),
         "-af", "volumedetect", "-f", "null", "-"],
        capture_output=True, text=True)
    text = proc.stderr + proc.stdout
    m = re.search(r"max_volume:\s*(-?\d+(?:\.\d+)?) dB", text)
    return float(m.group(1)) if m else None


def cmd_audit(args):
    proj = Path(args.proj).expanduser()
    chunks = sorted((proj / "chunks").glob("seg_*_000.wav"),
                    key=lambda p: int(p.stem.split("_")[1]))
    if not chunks:
        sys.exit("[tts] no raw chunks to audit")
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


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--voice-dir", dest="voice_dir", help="override voice store")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("prep"); p.add_argument("media")
    p.add_argument("--voice", required=True); p.add_argument("--ss", type=float)
    p.add_argument("--dur", type=float); p.add_argument("--lang", default="ko")
    p.set_defaults(func=cmd_prep)

    p = sub.add_parser("voices"); p.set_defaults(func=cmd_voices)

    p = sub.add_parser("preptext")
    p.add_argument("--text")
    p.add_argument("--text-file", dest="text_file")
    p.add_argument("--out", help="write spoken TTS script to this file")
    p.add_argument("--profile", default="korean-youtube",
                   help="currently informational; default korean-youtube")
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
        p.add_argument("--voice", required=True)
        p.add_argument("--proj", help="work dir (default /tmp/tts-XXXX)")
        p.add_argument("--out", help="also save final to this dir or *.wav path")
        p.add_argument("--loudnorm-out", dest="loudnorm_out",
                       help="also render edit-ready loudnorm copy to this dir or *.wav path")
        p.add_argument("--text"); p.add_argument("--text-file", dest="text_file")
        p.add_argument("--model", default=DEFAULT_MODEL)
        p.add_argument("--gap", type=float, default=0.30)
        p.add_argument("--lang", default="ko")
        add_generation_tuning_args(p)
        p.set_defaults(func=fn)

    p = sub.add_parser("regen"); p.add_argument("--proj", required=True)
    p.add_argument("--seg", type=int, required=True); p.add_argument("--text")
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
