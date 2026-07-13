#!/usr/bin/env python3
import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import tts_clone


def main():
    args = SimpleNamespace(voice="aiden", voice_dir=None)
    ref, ref_text = tts_clone.load_voice(args)
    assert ref == tts_clone.DEFAULT_VOICE_DIR / "aiden/ref.wav"
    assert ref.exists() and ref_text

    segments = tts_clone.prep_spoken_text("Claude Code와 AI를 4주 동안 배웁니다.")
    assert segments == ["클로드 코드와 에이아이를 사 주 동안 배웁니다."]

    original = tts_clone.find_apple_stt
    tts_clone.find_apple_stt = lambda: None
    try:
        missing_stt = SimpleNamespace(
            ref_text=None, ref_text_file=None, voice="sample", voice_dir=None,
            media="/missing.wav", ss=None, dur=None, lang="ko",
        )
        try:
            tts_clone.cmd_prep(missing_stt)
            raise AssertionError("prep should require reference text without apple-stt")
        except SystemExit as exc:
            assert "--ref-text" in str(exc)
    finally:
        tts_clone.find_apple_stt = original
    print("tts self-check: pass")


if __name__ == "__main__":
    main()
