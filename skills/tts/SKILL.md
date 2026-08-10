---
name: tts
description: "Local text-to-speech, voice cloning, preset speakers, and voice design with Qwen3-TTS/mlx-audio, full/chunk generation, and partial regeneration. Use when user asks TTS, 텍스트 음성으로, 음성 합성, 음성 복제, voice clone, 내 목소리로, 성우 음성, 목소리 디자인, 더빙, narration, Qwen3-TTS, or 음성 생성. Do NOT use for speech-to-text transcription, podcast publishing workflow, video editing, audio cleanup, or non-voice media conversion."
compatibility: "macOS on Apple Silicon. Requires Python 3, ffmpeg, and mlx-audio; apple-stt is optional for automatic reference transcription."
---

# TTS - 로컬 음성 합성

## 기본 계약

- 기본 엔진은 Qwen3-TTS Base이며, 모델을 받은 뒤 로컬에서 실행한다.
- 음성 레퍼런스는 스킬에 넣지 않고 로컬 `~/.local/share/tts/voices/<name>/ref.wav + ref.txt`에 둔다.
- 기본 음성은 `~/.config/tts/config.json`의 `default_voice`로 정한다. 미설정 별칭은 `default`다.
- `prep --voice <name>`은 새 음성을 로컬 voice store에 저장한다. 같은 이름이 있으면 중단하며, 명시적인 `--replace`에서만 두 레퍼런스 파일을 함께 교체한다. `TTS_VOICE_DIR` 또는 `--voice-dir`로 위치를 바꿀 수 있다.
- 등록 음성 복제는 `--voice`, 프리셋 화자는 `--preset-voice`, 자연어 음성 설계는 `--instruct`를 쓴다. 쓸 수 있는 프리셋 화자 이름은 `full --help`의 `--preset-voice` 설명에서 확인한다.
- 긴 작업은 `chunk`, 짧은 문장은 `full`을 쓴다. `chunk`는 한 줄을 한 청크로 처리한다.
- 같은 대본과 설정으로 `chunk --proj`를 다시 실행하면 완료된 청크를 건너뛰고 중단 지점부터 이어간다. 대본이나 설정이 다르면 새 프로젝트를 쓴다.
- 민감한 대본·전사·음성 지시는 각각 `--text-file`, `--ref-text-file`, `--instruct-file`로 전달한다. 생성 자식 프로세스에는 내용이 표준입력으로 넘어가 프로세스 인자와 실행 로그에 남지 않는다.

음성 등록, 발화 전처리, 튜닝, 복구 작업 전에는 `references/voice-clone.md`를 읽는다.

## 실행 흐름

1. 화면용 표기를 자연스러운 발화문으로 고치고 `preptext`로 청크를 정리한다.
2. 복제·프리셋·음성 설계 중 하나를 고른 뒤 `full` 또는 `chunk`로 생성한다. 별도 지정이 없으면 로컬 기본 음성과 한국어를 사용한다.
3. 긴 결과는 `audit` 후 위험 청크만 `regen`한다.
4. 외부 공유본은 자동 전사와 직접 청취로 문장 누락·고유명사·끝음을 확인한다.

```bash
S="${CLAUDE_PLUGIN_ROOT}/skills/tts/scripts/tts_clone.py"
python3 "$S" chunk --text-file script.txt --out out/raw.wav --loudnorm-out out/edit.wav
python3 "$S" full --preset-voice <preset-name> --instruct-file style.txt --text-file script.txt
python3 "$S" regen --proj /tmp/tts-XXXX --seg 3 --duration-multiplier 1.08
```

전체 명령과 옵션은 `python3 "$S" --help` 및 하위 명령의 `--help`를 따른다.

## 저장 위치

- 음성 자산: `~/.local/share/tts/voices/<name>/ref.wav + ref.txt`(기본값)
- 작업 프로젝트: `--proj`, 기본 `/tmp/tts-XXXX`
- 원본 최종본: `--out`
- 편집용 48kHz mono 정규화본: `--loudnorm-out`

드라이버가 생성·관리하는 음성 폴더와 작업 프로젝트는 `700`, 레퍼런스·manifest·생성 WAV는 `600` 권한으로 저장한다. 입력 미디어·대본·지시 파일은 읽기만 하며 권한을 바꾸지 않는다. `manifest.json`에는 재생성용 대본 청크와 음성 설정이 남으며 외부 서버로 업로드하지 않는다.

빠른 비복제 안내 음성만 필요하면 macOS `say`를 쓴다.
