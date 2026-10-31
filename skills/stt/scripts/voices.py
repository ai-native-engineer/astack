#!/usr/bin/env python3
"""Remember named voices and find them in later recordings.

A voice is stored only when the user names a speaker. Each enrolment keeps one
pyannote speaker embedding from one recording; a name can hold several.

usage:
  voices.py enroll <run-dir> <SPEAKER_xx> <name>
  voices.py match <run-dir>           # writes <run-dir>/names.json
  voices.py list
  voices.py forget <name>

The store is STT_VOICES or ~/.local/share/stt/voices.json, readable only by
the owner. run-dir is a stt_diarize.sh output folder with speakers.json.
"""

from __future__ import annotations

import json
import math
import os
from datetime import date
from pathlib import Path
import sys
import tempfile

STORE = Path(os.environ.get("STT_VOICES") or Path.home() / ".local/share/stt/voices.json")
# Scoring follows Alt's speaker gallery (top 3 exemplars weighted by speech
# length, 0.1 margin over the next name). The cut-offs come from 12 local
# recordings: different people in one recording reached 0.58, and one person
# across 11 recordings scored 0.80-0.92. See references/diarization.md.
NAME_THRESHOLD = 0.70
SUGGEST_THRESHOLD = 0.60
MATCH_MARGIN = 0.1
TOP_K = 3
DURATION_WEIGHT_CAP_SECONDS = 60.0
MIN_ENROLL_SECONDS = 3.0
MIN_MATCH_SECONDS = 3.0
MAX_EXEMPLARS = 15


def write_private(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    out = tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent,
                                      prefix=f".{path.name}.", suffix=".tmp", delete=False)
    tmp = Path(out.name)
    try:
        with out:
            os.fchmod(out.fileno(), 0o600)
            json.dump(data, out, ensure_ascii=False, indent=1)
        os.replace(tmp, path)
    except BaseException:
        tmp.unlink(missing_ok=True)
        raise


def load_store() -> dict:
    if not STORE.exists():
        return {"version": 1, "voices": []}
    return json.loads(STORE.read_text(encoding="utf-8"))


def load_speakers(run_dir: Path) -> dict:
    path = run_dir / "speakers.json"
    if not path.is_file():
        raise SystemExit(f"{path} not found; run stt_diarize.sh again to record speaker voices")
    return json.loads(path.read_text(encoding="utf-8"))


def cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb) if na and nb else -1.0


def score(probe: list[float], exemplars: list[dict]) -> float:
    scored = sorted(((cosine(probe, e["embedding"]),
                      min(e["seconds"], DURATION_WEIGHT_CAP_SECONDS) / DURATION_WEIGHT_CAP_SECONDS)
                     for e in exemplars), reverse=True)[:TOP_K]
    total = sum(weight for _, weight in scored)
    return sum(value * weight for value, weight in scored) / total if total else -1.0


def enroll(run_dir: Path, speaker: str, name: str) -> int:
    speakers = load_speakers(run_dir)
    if speaker.startswith("_") or speaker not in speakers:
        labels = ", ".join(sorted(k for k in speakers if not k.startswith("_")))
        raise SystemExit(f"unknown speaker {speaker}; choose one of {labels}")
    voice = speakers[speaker]
    if voice["seconds"] < MIN_ENROLL_SECONDS or not any(voice["embedding"]):
        raise SystemExit(f"{speaker} has {voice['seconds']:.1f}s of speech; "
                         f"need {MIN_ENROLL_SECONDS:.0f}s or more")
    store = load_store()
    recording = speakers.get("_recording", run_dir.name)
    store["voices"] = [v for v in store["voices"]
                       if not (v["recording"] == recording and v["speaker"] == speaker)]
    store["voices"].append({"name": name, "recording": recording, "speaker": speaker,
                            "seconds": round(voice["seconds"], 1), "added": date.today().isoformat(),
                            "embedding": voice["embedding"]})
    mine = [v for v in store["voices"] if v["name"] == name]
    if len(mine) > MAX_EXEMPLARS:
        store["voices"].remove(min(mine, key=lambda v: (v["seconds"], v["added"])))
    write_private(STORE, store)
    print(f"remembered {name} from {speaker} ({voice['seconds']:.0f}s); "
          f"{min(len(mine), MAX_EXEMPLARS)} sample(s) for this name")
    return 0


def match(run_dir: Path) -> int:
    speakers = {k: v for k, v in load_speakers(run_dir).items() if not k.startswith("_")}
    by_name: dict[str, list[dict]] = {}
    for voice in load_store()["voices"]:
        by_name.setdefault(voice["name"], []).append(voice)
    pairs = sorted(((score(v["embedding"], exemplars), spk, name)
                    for spk, v in speakers.items()
                    if v["seconds"] >= MIN_MATCH_SECONDS and any(v["embedding"])
                    for name, exemplars in by_name.items()), reverse=True)
    names: dict[str, dict] = {}
    used: set[str] = set()
    for value, spk, name in pairs:
        if value < SUGGEST_THRESHOLD:
            break
        if spk in names or name in used:
            continue
        runner = next((v for v, s, n in pairs if s == spk and n != name and n not in used), None)
        if runner is not None and value - runner < MATCH_MARGIN:
            continue
        names[spk] = {"name": name, "score": round(value, 3), "sure": value >= NAME_THRESHOLD}
        used.add(name)
    write_private(run_dir / "names.json", names)
    for spk, hit in sorted(names.items()):
        mark = "" if hit["sure"] else " (suggestion)"
        print(f"{spk} -> {hit['name']} {hit['score']:.2f}{mark}", file=sys.stderr)
    return 0


def sample_counts() -> dict[str, int]:
    counts: dict[str, int] = {}
    for voice in load_store()["voices"]:
        counts[voice["name"]] = counts.get(voice["name"], 0) + 1
    return counts


def forget(name: str) -> int:
    """Remove every sample of name; returns how many were removed."""
    store = load_store()
    before = len(store["voices"])
    store["voices"] = [v for v in store["voices"] if v["name"] != name]
    if len(store["voices"]) != before:
        write_private(STORE, store)
    return before - len(store["voices"])


def main(argv: list[str]) -> int:
    if argv[1:] == ["list"]:
        for name, count in sorted(sample_counts().items()):
            print(f"{name}\t{count} recording(s)")
        return 0
    if len(argv) == 3 and argv[1] == "forget":
        removed = forget(argv[2])
        if not removed:
            print(f"no voice named {argv[2]}", file=sys.stderr)
            return 1
        print(f"forgot {removed} sample(s) of {argv[2]}")
        return 0
    if len(argv) == 5 and argv[1] == "enroll":
        return enroll(Path(argv[2]), argv[3], argv[4])
    if len(argv) == 3 and argv[1] == "match":
        return match(Path(argv[2]))
    print(__doc__, file=sys.stderr)
    return 64


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
