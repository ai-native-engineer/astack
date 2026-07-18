---
name: tts
description: "Local text-to-speech and voice cloning with Qwen3-TTS/mlx-audio, locally registered voices, full/chunk generation, and partial regeneration. Use when user asks TTS, 텍스트 음성으로, 음성 합성, 음성 복제, voice clone, 내 목소리로, 성우 음성, 더빙, narration, Qwen3-TTS, or 음성 생성. Do NOT use for speech-to-text transcription, podcast publishing workflow, video editing, audio cleanup, or non-voice media conversion."
compatibility: "macOS on Apple Silicon. Requires Python 3, ffmpeg, and mlx-audio; apple-stt is optional for automatic reference transcription."
---

# TTS - 로컬 음성 합성·복제

## 기본 계약

- 기본 엔진은 Qwen3-TTS Base이며, 모델을 받은 뒤 로컬에서 실행한다.
- 음성 레퍼런스는 스킬에 넣지 않고 로컬 `~/.local/share/tts/voices/<name>/ref.wav + ref.txt`에 둔다.
- 기본 음성은 `~/.config/tts/config.json`의 `default_voice`로 정한다. 미설정 별칭은 `default`다.
- `prep --voice <name>`은 새 음성을 로컬 voice store에 저장한다. `TTS_VOICE_DIR` 또는 `--voice-dir`로 위치를 바꿀 수 있다.
- 긴 작업은 `chunk`, 짧은 문장은 `full`을 쓴다. `chunk`는 한 줄을 한 청크로 처리한다.

음성 등록, 발화 전처리, 튜닝, 복구 작업 전에는 `references/voice-clone.md`를 읽는다.

## 실행 흐름

1. 화면용 표기를 자연스러운 발화문으로 고치고 `preptext`로 청크를 정리한다.
2. `full` 또는 `chunk`로 생성한다. 별도 지정이 없으면 로컬 기본 음성과 한국어를 사용한다.
3. 긴 결과는 `audit` 후 위험 청크만 `regen`한다.
4. 외부 공유본은 자동 전사와 직접 청취로 문장 누락·고유명사·끝음을 확인한다.

```bash
S="scripts/tts_clone.py"  # 설치된 tts 스킬 루트에서 실행
python3 "$S" chunk --text-file script.txt --out out/raw.wav --loudnorm-out out/edit.wav
python3 "$S" regen --proj /tmp/tts-XXXX --seg 3 --duration-multiplier 1.08
```

전체 명령과 옵션은 `python3 "$S" --help` 및 하위 명령의 `--help`를 따른다.

## 저장 위치

- 음성 자산: `~/.local/share/tts/voices/<name>/ref.wav + ref.txt`(기본값)
- 작업 프로젝트: `--proj`, 기본 `/tmp/tts-XXXX`
- 원본 최종본: `--out`
- 편집용 48kHz mono 정규화본: `--loudnorm-out`

빠른 비복제 안내 음성만 필요하면 macOS `say`를 쓴다.
