#!/usr/bin/env python3
"""Chunk planning and cross-chunk speaker joining with local pyannote models.

MOSS runs per chunk and numbers speakers per call (S01, S02, ...), so the same
person can get another number in the next chunk. This driver uses only two
Community-1 submodels, never the full diarization pipeline:

  plan  segmentation model as speech detector -> cut points at long pauses
  join  speaker embedding per MOSS segment -> one global label per person,
        plus the stretches MOSS left empty although there was speech, and one
        voice per person in speakers.json for scripts/voices.py

usage:
  pyannote-chunks.py --check
  pyannote-chunks.py plan <wav> <chunks.json> <speech.json>
  pyannote-chunks.py join <wav> <moss.json> <speech.json> <out-dir>
"""

from __future__ import annotations

import hashlib
from itertools import combinations
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys

MODEL = "pyannote/speaker-diarization-community-1"
RATE = 16000

# Chunks: MOSS stays near 4 GB on 10-minute chunks. A cut moves at most
# SEARCH_SECONDS from the target to land in the longest pause there, and the
# last chunk may grow to 1.5x the target instead of leaving a short tail.
TARGET_SECONDS = 600.0
SEARCH_SECONDS = 90.0
MIN_PAUSE = 0.5

# Embeddings: shorter segments give unstable vectors; longer ones use their middle.
MIN_SEGMENT_SECONDS = 1.0
MAX_SEGMENT_SECONDS = 20.0
# Chunk speakers with less embedded speech than this keep their own label.
MIN_SPEAKER_SECONDS = 5.0
# Cosine similarity at which two chunk speakers are one person. Chosen on three
# long recordings: same-person pairs had median 0.95, different pairs 0.31.
SAME_SPEAKER = 0.62

# A MOSS-free stretch this long that still holds speech is reported as a gap.
MIN_GAP = 10.0


def pauses(speech: list[list[float]], duration: float) -> list[tuple[float, float]]:
    out, previous = [], 0.0
    for start, end in speech:
        if start - previous >= MIN_PAUSE:
            out.append((previous, start))
        previous = max(previous, end)
    if duration - previous >= MIN_PAUSE:
        out.append((previous, duration))
    return out


def plan_chunks(speech: list[list[float]], duration: float,
                target: float = TARGET_SECONDS) -> list[list[float]]:
    gaps = pauses(speech, duration)
    cuts, at = [], 0.0
    while duration - at > target * 1.5:
        want = at + target
        near = [(end - start, (start + end) / 2) for start, end in gaps
                if abs((start + end) / 2 - want) <= SEARCH_SECONDS]
        cut = round(max(near)[1] if near else want, 2)
        cuts.append(cut)
        at = cut
    edges = [0.0] + cuts + [round(duration, 2)]
    return [[start, end] for start, end in zip(edges, edges[1:])]


def unit(vector: list[float]) -> list[float]:
    norm = math.sqrt(sum(v * v for v in vector)) or 1.0
    return [v / norm for v in vector]


def dot(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def speaker_vectors(segments: list[dict]) -> dict[str, tuple[float, list[float]]]:
    """Duration-weighted mean direction per chunk speaker, from embedded segments."""
    acc: dict[str, tuple[float, list[float]]] = {}
    for seg in segments:
        vector = seg.get("embedding")
        if not vector:
            continue
        seconds = seg["end"] - seg["start"]
        weighted = [seconds * v for v in unit(vector)]
        total, summed = acc.get(seg["key"], (0.0, [0.0] * len(weighted)))
        acc[seg["key"]] = (total + seconds, [a + b for a, b in zip(summed, weighted)])
    return {key: (seconds, unit(summed)) for key, (seconds, summed) in acc.items()}


def cluster(vectors: dict[str, tuple[float, list[float]]],
            threshold: float = SAME_SPEAKER) -> list[list[str]]:
    """Average-linkage merge of chunk speakers above the similarity threshold.

    Two speakers of the same chunk may merge too: MOSS sometimes gives one
    person two labels inside a chunk, and listening confirmed such a pair.
    """
    keys = sorted(k for k, (seconds, _) in vectors.items() if seconds >= MIN_SPEAKER_SECONDS)
    sim = {(a, b): dot(vectors[a][1], vectors[b][1]) for a in keys for b in keys}
    groups = [[key] for key in keys]
    while True:
        best, pair = threshold, None
        for i, j in combinations(range(len(groups)), 2):
            value = sum(sim[(a, b)] for a in groups[i] for b in groups[j]) / (len(groups[i]) * len(groups[j]))
            if value >= best:
                best, pair = value, (i, j)
        if pair is None:
            return groups
        i, j = pair
        groups[i] += groups.pop(j)


def global_labels(segments: list[dict], groups: list[list[str]]) -> dict[str, str]:
    """SPEAKER_00 is the person who talked longest. Unjoined chunk speakers stay separate."""
    seconds: dict[str, float] = {}
    for seg in segments:
        seconds[seg["key"]] = seconds.get(seg["key"], 0.0) + seg["end"] - seg["start"]
    grouped = {key for group in groups for key in group}
    people = groups + [[key] for key in sorted(seconds) if key not in grouped]
    people.sort(key=lambda group: (-sum(seconds.get(k, 0.0) for k in group), group[0]))
    return {key: f"SPEAKER_{n:02d}" for n, group in enumerate(people) for key in group}


def speaker_profiles(segments: list[dict], labels: dict[str, str]) -> dict[str, dict]:
    """Speech seconds and mean voice direction per global speaker (empty when never embedded)."""
    by_label: dict[str, list[dict]] = {}
    for seg in segments:
        by_label.setdefault(labels[seg["key"]], []).append(dict(seg, key=labels[seg["key"]]))
    profiles = {}
    for label, rows in sorted(by_label.items()):
        voice = speaker_vectors(rows).get(label)
        profiles[label] = {"seconds": round(sum(r["end"] - r["start"] for r in rows), 2),
                           "embedding": [round(v, 5) for v in voice[1]] if voice else []}
    return profiles


def empty_stretches(segments: list[dict], speech: list[list[float]],
                    duration: float) -> list[list[float]]:
    """Stretches of MIN_GAP or more with no MOSS segment but with detected speech."""
    stretches, covered = [], 0.0
    for start, end in sorted((s["start"], s["end"]) for s in segments):
        if start - covered >= MIN_GAP:
            stretches.append((covered, start))
        covered = max(covered, end)
    if duration - covered >= MIN_GAP:
        stretches.append((covered, duration))
    return [[round(a, 2), round(b, 2)] for a, b in stretches
            if any(s < b and e > a for s, e in speech)]


def load_samples(wav: Path):
    import numpy as np

    pcm = subprocess.run(
        ["ffmpeg", "-nostdin", "-v", "error", "-i", str(wav), "-ar", str(RATE), "-ac", "1",
         "-f", "s16le", "pipe:1"], check=True, capture_output=True).stdout
    samples = np.frombuffer(pcm, dtype="<i2").astype("float32") / 32768
    if not len(samples):
        raise RuntimeError("audio decoded to zero samples")
    return samples


def load_pipeline():
    import torch
    from huggingface_hub import snapshot_download
    from pyannote.audio import Pipeline

    device = os.environ.get("PYANNOTE_DEVICE", "auto")
    if device == "auto":
        device = "mps" if torch.backends.mps.is_available() else "cpu"
    if device not in ("mps", "cpu"):
        raise RuntimeError("PYANNOTE_DEVICE must be auto, mps or cpu")
    if device == "mps" and not torch.backends.mps.is_available():
        raise RuntimeError("MPS requested but unavailable")
    print(f"pyannote Community-1 device={device} offline=true", file=sys.stderr)
    pipeline = Pipeline.from_pretrained(snapshot_download(MODEL, local_files_only=True))
    pipeline.to(torch.device(device))
    return pipeline, torch.device(device)


def write_private(path: Path, text: str) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as out:
        out.write(text)


def check() -> None:
    import importlib.util

    for package in ("torch", "numpy", "pyannote.audio", "huggingface_hub"):
        if importlib.util.find_spec(package) is None:
            raise RuntimeError(f"missing {package}; use the whispermlx Python environment")
    if not shutil.which("ffmpeg"):
        raise RuntimeError("ffmpeg not found in PATH")
    from huggingface_hub import snapshot_download

    model_path = Path(snapshot_download(MODEL, local_files_only=True))
    for name in ("config.yaml", "segmentation/pytorch_model.bin", "embedding/pytorch_model.bin"):
        if not (model_path / name).is_file():
            raise RuntimeError(f"incomplete model cache: {name}")


def plan(wav: Path, chunks_path: Path, speech_path: Path) -> None:
    import torch
    from pyannote.audio.pipelines import VoiceActivityDetection

    samples = load_samples(wav)
    pipeline, device = load_pipeline()
    vad = VoiceActivityDetection(segmentation=pipeline._segmentation.model, device=device)
    vad.instantiate({"min_duration_on": 0.0, "min_duration_off": 0.0})
    found = vad({"waveform": torch.from_numpy(samples).unsqueeze(0), "sample_rate": RATE})
    speech = [[round(s.start, 2), round(s.end, 2)] for s in found.get_timeline().support()]
    duration = len(samples) / RATE
    chunks = plan_chunks(speech, duration)
    write_private(speech_path, json.dumps({"duration": round(duration, 2), "speech": speech}))
    write_private(chunks_path, json.dumps(chunks))
    print(f"chunks={len(chunks)} speech_share="
          f"{sum(b - a for a, b in speech) / duration:.2f}", file=sys.stderr)


def join(wav: Path, moss_path: Path, speech_path: Path, out_dir: Path) -> None:
    import numpy as np
    import torch

    moss = json.loads(moss_path.read_text(encoding="utf-8"))
    detected = json.loads(speech_path.read_text(encoding="utf-8"))
    segments = [dict(seg, key=f"{seg['chunk']:02d}-{seg['local']}") for seg in moss["segments"]]
    samples = load_samples(wav)
    pipeline, _ = load_pipeline()
    embed = pipeline._embedding
    for seg in segments:
        length = seg["end"] - seg["start"]
        if length < MIN_SEGMENT_SECONDS:
            continue
        middle, half = (seg["start"] + seg["end"]) / 2, min(length, MAX_SEGMENT_SECONDS) / 2
        wave = samples[int((middle - half) * RATE):int((middle + half) * RATE)]
        vector = embed(torch.from_numpy(wave.copy())[None, None, :])[0]
        if np.all(np.isfinite(vector)):
            seg["embedding"] = [float(v) for v in vector]
    groups = cluster(speaker_vectors(segments))
    labels = global_labels(segments, groups)
    rows = [{"start": round(s["start"], 2), "end": round(s["end"], 2), "speaker": labels[s["key"]],
             "chunk": s["chunk"], "local": s["local"], "text": s["text"]}
            for s in sorted(segments, key=lambda s: (s["start"], s["end"]))]
    gaps = empty_stretches(segments, detected["speech"], detected["duration"])
    transcript = {"engine": moss.get("model"), "chunks": moss.get("chunks", []),
                  "segments": rows, "gaps": gaps}
    write_private(out_dir / "transcript.json", json.dumps(transcript, ensure_ascii=False, indent=1))
    write_private(out_dir / "diar.rttm", "".join(
        f"SPEAKER audio 1 {r['start']:.3f} {max(r['end'] - r['start'], 0.001):.3f} <NA> <NA> "
        f"{r['speaker']} <NA> <NA>\n" for r in rows))
    digest = hashlib.sha256()
    with wav.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            digest.update(block)
    speakers = {"_recording": digest.hexdigest()[:16], **speaker_profiles(segments, labels)}
    write_private(out_dir / "speakers.json", json.dumps(speakers))
    print(f"speakers={len(set(labels.values()))} gaps={len(gaps)}", file=sys.stderr)


def main(argv: list[str]) -> int:
    # Inference stays offline, including the submodels the pipeline loads.
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
    if argv[1:] == ["--check"]:
        try:
            check()
        except Exception as exc:
            print(f"pyannote runtime not ready: {exc}", file=sys.stderr)
            print(f"Prepare the runtime and cached model first: hf download {MODEL}", file=sys.stderr)
            return 69
        return 0
    steps = {("plan", 5): plan, ("join", 6): join}
    step = steps.get((argv[1] if len(argv) > 1 else "", len(argv)))
    if step is None:
        print(__doc__, file=sys.stderr)
        return 64
    try:
        step(*map(Path, argv[2:]))
    except Exception as exc:
        print(f"pyannote {argv[1]} failed: {exc}", file=sys.stderr)
        return 70
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
