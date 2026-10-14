#!/usr/bin/env python3
"""Produce local Community-1 RTTM from audio, using an existing model cache."""

from __future__ import annotations

import argparse
import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import sys

MODEL = "pyannote/speaker-diarization-community-1"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--audio-path", type=Path)
    parser.add_argument("--rttm-path", type=Path)
    args = parser.parse_args()
    if not args.check and (args.audio_path is None or args.rttm_path is None):
        parser.error("--audio-path and --rttm-path are required")

    # Both the preflight and inference must remain offline, including submodels.
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
    try:
        for package in ("torch", "numpy", "pyannote.audio", "huggingface_hub"):
            if importlib.util.find_spec(package) is None:
                raise RuntimeError(f"missing {package}; use the whispermlx Python environment")
        ffmpeg = shutil.which("ffmpeg")
        if not ffmpeg:
            raise RuntimeError("ffmpeg not found in PATH")
        from huggingface_hub import snapshot_download

        model_path = Path(snapshot_download(MODEL, local_files_only=True))
        for name in ("config.yaml", "segmentation/pytorch_model.bin",
                     "embedding/pytorch_model.bin", "plda/plda.npz",
                     "plda/xvec_transform.npz"):
            if not (model_path / name).is_file():
                raise RuntimeError(f"incomplete model cache: {name}")
        if args.check:
            return 0
        if not args.audio_path.is_file():
            raise RuntimeError("audio file not found")
        if args.rttm_path.exists():
            raise RuntimeError("RTTM output already exists; choose a new path")

        import numpy as np
        import torch
        from pyannote.audio import Pipeline

        device = os.environ.get("PYANNOTE_DEVICE", "auto")
        if device == "auto":
            device = "mps" if torch.backends.mps.is_available() else "cpu"
        if device not in ("mps", "cpu"):
            raise RuntimeError("PYANNOTE_DEVICE must be auto, mps or cpu")
        if device == "mps" and not torch.backends.mps.is_available():
            raise RuntimeError("MPS requested but unavailable")
        print(f"pyannote Community-1 device={device} offline=true", file=sys.stderr)
        # Supplying decoded PCM avoids the optional torchcodec decoder dependency.
        pcm = subprocess.run(
            [ffmpeg, "-v", "error", "-i", str(args.audio_path.resolve()),
             "-ar", "16000", "-ac", "1", "-f", "s16le", "pipe:1"],
            check=True, capture_output=True,
        ).stdout
        samples = np.frombuffer(pcm, dtype="<i2").astype("float32") / 32768
        if not len(samples):
            raise RuntimeError("audio decoded to zero samples")
        pipeline = Pipeline.from_pretrained(str(model_path))
        pipeline.to(torch.device(device))
        result = pipeline({"waveform": torch.from_numpy(samples).unsqueeze(0),
                           "sample_rate": 16000})
        # Preserve overlap; exclusive diarization would conceal mixed speakers.
        annotation = result.speaker_diarization
        args.rttm_path.parent.mkdir(parents=True, exist_ok=True)
        fd = os.open(args.rttm_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as out:
            annotation.write_rttm(out)
        print(f"speakers={len(annotation.labels())}", file=sys.stderr)
        return 0
    except Exception as exc:
        print(f"pyannote diarization failed: {exc}", file=sys.stderr)
        print(f"Prepare the runtime and cached model first: hf download {MODEL}",
              file=sys.stderr)
        return 69


if __name__ == "__main__":
    raise SystemExit(main())
