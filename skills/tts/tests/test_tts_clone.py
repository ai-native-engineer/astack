#!/usr/bin/env python3
import json
import os
import stat
import subprocess
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import tts_clone


def main():
    with tempfile.TemporaryDirectory() as tmp:
        voice_dir = Path(tmp)
        sample = voice_dir / "sample"
        sample.mkdir()
        (sample / "ref.wav").write_bytes(b"RIFF")
        (sample / "ref.txt").write_text("sample reference", encoding="utf-8")
        args = SimpleNamespace(voice="sample", voice_dir=str(voice_dir))
        ref, ref_text = tts_clone.load_voice(args)
        assert ref == sample / "ref.wav"
        assert ref.exists() and ref_text == "sample reference"
        assert stat.S_IMODE(sample.stat().st_mode) == 0o700
        assert stat.S_IMODE(ref.stat().st_mode) == 0o600
        assert stat.S_IMODE((sample / "ref.txt").stat().st_mode) == 0o600

        bad = SimpleNamespace(voice="../escape", voice_dir=str(voice_dir))
        try:
            tts_clone.load_voice(bad)
            raise AssertionError("voice paths should be rejected")
        except SystemExit as exc:
            assert "invalid voice name" in str(exc)

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

    with tempfile.TemporaryDirectory() as tmp:
        out_dir = Path(tmp)
        (out_dir / "seg_0001_old.wav").write_bytes(b"stale")
        ref = out_dir / "ref.wav"
        ref_text = out_dir / "ref.txt"
        ref.write_bytes(b"RIFF")
        ref_text.write_text("private reference", encoding="utf-8")
        launcher = out_dir / "mlx_audio.tts.generate"
        launcher.write_text(f"#!{sys.executable}\n", encoding="utf-8")
        original_run = tts_clone.run
        original_launcher = tts_clone.MLX_GENERATE
        seen = {}

        def fake_generate(cmd, **kwargs):
            payload = json.loads(kwargs["input"])
            seen.update(cmd=cmd, display=kwargs["display"], payload=payload)
            generated = Path(payload[payload.index("--output_path") + 1])
            prefix = payload[payload.index("--file_prefix") + 1]
            (generated / f"{prefix}_000.wav").write_bytes(b"fresh")

        tts_clone.run = fake_generate
        tts_clone.MLX_GENERATE = str(launcher)
        try:
            result = tts_clone.gen_one(
                "model",
                {"mode": "clone", "ref_audio": str(ref),
                 "ref_text_file": str(ref_text)},
                "private target text", out_dir, "seg_0001",
            )
            assert result == out_dir / "seg_0001_000.wav"
            assert result.read_bytes() == b"fresh"
            assert stat.S_IMODE(result.stat().st_mode) == 0o600
            assert "private target text" not in " ".join(seen["cmd"])
            assert "private reference" not in " ".join(seen["cmd"])
            assert "private target text" not in " ".join(seen["display"])
            assert seen["payload"][seen["payload"].index("--text") + 1] == "private target text"
        finally:
            tts_clone.run = original_run
            tts_clone.MLX_GENERATE = original_launcher

    preset = SimpleNamespace(
        voice=None, preset_voice="Aiden", instruct="calm and warm",
        instruct_file=None, model=None,
    )
    preset_source = tts_clone.generation_source(preset)
    assert preset_source == {
        "mode": "preset", "preset_voice": "Aiden", "instruct": "calm and warm"
    }
    assert tts_clone.model_for_source(preset, preset_source) == tts_clone.DEFAULT_CUSTOM_MODEL
    assert tts_clone.source_cli_args(preset_source) == [
        "--voice", "Aiden", "--instruct", "calm and warm"
    ]

    try:
        tts_clone.generation_source(SimpleNamespace(
            voice="sample", preset_voice=None, instruct="calm",
            instruct_file=None,
        ))
        raise AssertionError("local clone and instruction should not be mixed")
    except SystemExit as exc:
        assert "--preset-voice" in str(exc)

    try:
        tts_clone._python_from_launcher("/missing/mlx_audio.tts.generate")
        raise AssertionError("missing mlx-audio launcher should have an actionable error")
    except SystemExit as exc:
        assert "uv tool install mlx-audio" in str(exc)

    with tempfile.TemporaryDirectory() as tmp:
        instruction = Path(tmp) / "instruction.txt"
        instruction.write_text("차분한 30대 남성 목소리", encoding="utf-8")
        design = SimpleNamespace(
            voice=None, preset_voice=None, instruct=None,
            instruct_file=str(instruction), model=None,
        )
        design_source = tts_clone.generation_source(design)
        assert design_source == {"mode": "design", "instruct": "차분한 30대 남성 목소리"}
        assert tts_clone.model_for_source(design, design_source) == tts_clone.DEFAULT_DESIGN_MODEL
        assert tts_clone.source_cli_args(design_source) == [
            "--instruct", "차분한 30대 남성 목소리"
        ]

    with tempfile.TemporaryDirectory() as tmp:
        proj = Path(tmp)
        (proj / "chunks").mkdir()
        manifest = {
            "model": "model", "ref_audio": "ref.wav", "ref_text": "reference",
            "gap": 0.3, "segments": ["문장입니다."],
            "gen_extra": ["--lang_code", "ko", "--top_p", "0.8"],
        }
        (proj / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        seen = {}
        original_gen = tts_clone.gen_one
        original_normalize = tts_clone._normalize
        original_join = tts_clone.cmd_join
        tts_clone.gen_one = lambda *args, **kwargs: (
            seen.setdefault("extra", kwargs["extra"]), proj / "raw.wav"
        )[1]
        tts_clone._normalize = lambda *args, **kwargs: None
        tts_clone.cmd_join = lambda args: None
        try:
            regen = SimpleNamespace(
                proj=tmp, seg=1, text=None, text_file=None, duration_multiplier=1.08,
                speed=None, ddpm_steps=None, temperature=None, top_p=0.7,
                top_k=None, repetition_penalty=None,
            )
            tts_clone.cmd_regen(regen)
            assert seen["extra"] == [
                "--lang_code", "ko", "--top_p", "0.7",
                "--duration_multiplier", "1.08",
            ]
            saved = json.loads((proj / "manifest.json").read_text(encoding="utf-8"))
            assert saved["gen_extra"] == ["--lang_code", "ko", "--top_p", "0.8"]
        finally:
            tts_clone.gen_one = original_gen
            tts_clone._normalize = original_normalize
            tts_clone.cmd_join = original_join

    with tempfile.TemporaryDirectory() as tmp:
        voice = Path(tmp) / "voices" / "sample"
        voice.mkdir(parents=True)
        (voice / "ref.wav").write_bytes(b"RIFF")
        (voice / "ref.txt").write_text("reference\n", encoding="utf-8")
        proj = Path(tmp) / "project"
        proj.mkdir()
        (proj / "manifest.json").write_text(
            json.dumps({"segments": ["old"]}), encoding="utf-8"
        )
        chunk = SimpleNamespace(
            voice="sample", voice_dir=str(voice.parent), proj=str(proj),
            preset_voice=None, instruct=None, instruct_file=None,
            text="new", text_file=None, model="model", gap=0.3, lang="ko",
            duration_multiplier=None, speed=None, ddpm_steps=None,
            temperature=None, top_p=None, top_k=None, repetition_penalty=None,
        )
        try:
            tts_clone.cmd_chunk(chunk)
            raise AssertionError("chunk should not reuse an existing project")
        except SystemExit as exc:
            assert "use regen/join or a new --proj" in str(exc)

    with tempfile.TemporaryDirectory() as tmp:
        proj = Path(tmp)
        chunks = proj / "chunks"
        chunks.mkdir()
        for i in range(1, 4):
            (chunks / f"norm_{i:04d}.wav").write_bytes(b"RIFF")
        (proj / "manifest.json").write_text(
            json.dumps({"segments": ["one", "two"]}), encoding="utf-8"
        )
        seen = {}
        original_concat, original_dur = tts_clone._concat, tts_clone.ffprobe_dur
        tts_clone._concat = lambda wavs, out: seen.setdefault(
            "wavs", [Path(w).name for w in wavs]
        )
        tts_clone.ffprobe_dur = lambda path: 1.0
        try:
            tts_clone.cmd_join(SimpleNamespace(proj=tmp, out=None, loudnorm_out=None))
            assert seen["wavs"] == ["norm_0001.wav", "norm_0002.wav"]
        finally:
            tts_clone._concat, tts_clone.ffprobe_dur = original_concat, original_dur

    with tempfile.TemporaryDirectory() as tmp:
        voice = Path(tmp) / "sample"
        voice.mkdir()
        old_ref, old_txt = voice / "ref.wav", voice / "ref.txt"
        old_ref.write_bytes(b"old audio")
        old_txt.write_text("old text\n", encoding="utf-8")
        original_run = tts_clone.run
        tts_clone.run = lambda *args, **kwargs: (_ for _ in ()).throw(
            subprocess.CalledProcessError(1, args[0])
        )
        try:
            prep = SimpleNamespace(
                ref_text="new text", ref_text_file=None, voice="sample",
                voice_dir=tmp, media="missing.wav", ss=None, dur=None, lang="ko",
            )
            try:
                tts_clone.cmd_prep(prep)
                raise AssertionError("prep should propagate ffmpeg failure")
            except subprocess.CalledProcessError:
                pass
            assert old_ref.read_bytes() == b"old audio"
            assert old_txt.read_text(encoding="utf-8") == "old text\n"
        finally:
            tts_clone.run = original_run

    with tempfile.TemporaryDirectory() as tmp:
        proj = Path(tmp) / "private-project"
        args = SimpleNamespace(proj=str(proj))
        tts_clone.resolve_proj(args)
        manifest = {
            "model": "model",
            "source": {"mode": "clone", "ref_audio": "/voice/ref.wav",
                       "ref_text_file": "/voice/ref.txt"},
            "segments": ["private script"],
        }
        tts_clone.write_manifest(proj, manifest)
        saved = json.loads((proj / "manifest.json").read_text(encoding="utf-8"))
        assert "ref_text" not in saved["source"]
        assert stat.S_IMODE(proj.stat().st_mode) == 0o700
        assert stat.S_IMODE((proj / "manifest.json").stat().st_mode) == 0o600

    old_path = os.environ.get("PATH")
    try:
        os.environ["PATH"] = "/usr/bin:/bin"
        local_launcher = Path("~/.local/bin/mlx_audio.tts.generate").expanduser()
        if local_launcher.exists():
            assert tts_clone._tool("mlx_audio.tts.generate") == str(local_launcher)
    finally:
        if old_path is None:
            os.environ.pop("PATH", None)
        else:
            os.environ["PATH"] = old_path
    print("tts self-check: pass")


if __name__ == "__main__":
    main()
