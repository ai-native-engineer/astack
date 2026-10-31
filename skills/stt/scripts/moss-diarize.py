#!/usr/bin/env python3
"""Transcribe and diarize each chunk with MOSS-Transcribe-Diarize through mlx-audio.

The model is loaded once and run per chunk. Segment times are shifted to the
whole recording; speaker ids stay local to their chunk (pyannote-chunks.py
joins them afterwards).

usage:
  moss-diarize.py --check
  moss-diarize.py <wav-16k-mono> <chunks.json> <moss.json>
Run inside the pinned mlx-audio environment (see stt_diarize.sh).
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import re
import sys
import tempfile
import time
import wave

MODEL = os.environ.get("MOSS_MODEL", "OpenMOSS-Team/MOSS-Transcribe-Diarize")
# A 15-minute chunk needs well under this; reaching it means the output was cut off.
MAX_TOKENS = 32768
SPEAKER_PREFIX = re.compile(r"^\[S\d+\]\s*")


def check() -> None:
    from huggingface_hub import snapshot_download
    import mlx_audio.stt.utils  # noqa: F401

    snapshot_download(MODEL, local_files_only=True)


def write_slice(source: wave.Wave_read, start: float, end: float, target: Path) -> None:
    rate = source.getframerate()
    source.setpos(min(int(start * rate), source.getnframes()))
    frames = source.readframes(max(0, int(end * rate) - int(start * rate)))
    with wave.open(str(target), "wb") as out:
        out.setnchannels(source.getnchannels())
        out.setsampwidth(source.getsampwidth())
        out.setframerate(rate)
        out.writeframes(frames)


def run(wav: Path, chunks_path: Path, out_path: Path) -> None:
    import mlx.core as mx
    from mlx_audio.stt.utils import load_model

    chunks = json.loads(chunks_path.read_text(encoding="utf-8"))
    began = time.perf_counter()
    model = load_model(MODEL)
    print(f"MOSS model={MODEL} load={time.perf_counter() - began:.1f}s", file=sys.stderr)
    segments, runs = [], []
    with wave.open(str(wav), "rb") as source, tempfile.TemporaryDirectory(dir=out_path.parent) as tmp:
        for index, (start, end) in enumerate(chunks, 1):
            clip = Path(tmp) / f"{index:02d}.wav"
            write_slice(source, start, end, clip)
            mx.reset_peak_memory()
            began = time.perf_counter()
            result = model.generate(str(clip), max_tokens=MAX_TOKENS)
            clip.unlink()
            if result.generation_tokens >= MAX_TOKENS:
                raise RuntimeError(f"chunk {index} hit the {MAX_TOKENS}-token limit; output is cut off")
            seconds = time.perf_counter() - began
            peak = mx.get_peak_memory() / 1e9
            runs.append({"start": start, "end": end, "seconds": round(seconds, 1), "peak_gb": round(peak, 2),
                         "generation_tokens": result.generation_tokens})
            for seg in result.segments or []:
                text = SPEAKER_PREFIX.sub("", seg["text"]).strip()
                if text:
                    segments.append({"start": round(seg["start"] + start, 2), "end": round(seg["end"] + start, 2),
                                     "chunk": index, "local": seg.get("speaker_id") or "?", "text": text})
            print(f"chunk {index}/{len(chunks)} {end - start:.0f}s audio in {seconds:.0f}s, "
                  f"peak {peak:.1f} GB", file=sys.stderr)
    fd = os.open(out_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as out:
        json.dump({"model": MODEL, "chunks": runs, "segments": segments}, out, ensure_ascii=False)


def main(argv: list[str]) -> int:
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
    if argv[1:] == ["--check"]:
        try:
            check()
        except Exception as exc:
            print(f"MOSS runtime not ready: {exc}", file=sys.stderr)
            print(f"Prepare the cached model first: hf download {MODEL}", file=sys.stderr)
            return 69
        return 0
    if len(argv) != 4:
        print(__doc__, file=sys.stderr)
        return 64
    try:
        run(Path(argv[1]), Path(argv[2]), Path(argv[3]))
    except Exception as exc:
        print(f"MOSS failed: {exc}", file=sys.stderr)
        return 70
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
