---
argument-hint: "[audio-path]"
name: stt
description: "Local speech-to-text transcription and optional speaker diarization for audio/video files, meetings, lectures, interviews, and selected time ranges. Use when user asks STT, 전사, 받아쓰기, 오디오/녹음/회의록/강의/인터뷰 전사, 화자 분리, speaker diarization, or 누가 말했는지. Do NOT use for text-to-speech, Apple Voice Memos personal workflow, YouTube caption extraction, OCR, or audio editing."
---

# STT — 로컬 음성 전사 + 화자 분리

## 전사 (음성 → 텍스트)

기본 `apple-stt`(로컬·빠름, 4배속+). **전체 전사가 기본**, 일부만 필요하면 구간 전사.

- 전체: `apple-stt 녹음.m4a` — `-t`(타임스탬프) · `--srt` · `--json` · `--save` · `-l en-US`
- 구간: 먼저 잘라서 전사 — `ffmpeg -ss <시작초> -to <끝초> -i in.m4a -c copy clip.m4a` → `apple-stt clip.m4a`
  - 긴 녹음에 회의 외 이동·잡음이 섞이면 그 구간은 전사·화자분리가 다 깨지니 회의 구간만 잘라 처리.
- 바이너리 `~/scripts/apple-stt` (소스/빌드 `~/Dev/1-project/stt/`: `swiftc -O -parse-as-library -target arm64-apple-macos26.0 apple-stt.swift -o apple-stt`). **macOS 26+ 전용**.
- 음성 메모 원본: `~/Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings/*.m4a`

## 화자 분리 (누가 언제 말했나)

`apple-stt`는 전사만 한다 — 화자 라벨은 별도 단계. **기본은 로컬 argmax.** 모드별 입자 트레이드오프·구간 트림·whispermlx 셋업·클라우드 상세는 `references/diarization.md`.

- **기본(로컬)**: `~/.claude/skills/stt/scripts/stt_diarize.sh <오디오> <apple|argmax|both> [start초 end초]` (diarize/transcribe 스크립트는 스킬 내부 경로 — `apple-stt`만 `~/scripts/`의 별도 빌드 바이너리다. `scripts/`만 적어 `~/scripts/`로 오해하면 `exit 127`)
  - `apple` = apple-stt 텍스트 + argmax 화자(가벼움, 화자 경계 굵음)
  - `argmax` = argmax 텍스트 + 단어단위 정밀 화자(632MB 모델)
  - `both` = 둘 다(정확도 최고·토큰 최다)
  - 출력: `stt/YYMMDD-HHMM/transcript.md`(전사본), `diarized.md`(화자분리전사본). 필요한 것 하나만 읽으면 됨(토큰 절약).
  - 이동·잡음 구간은 가짜 화자로 잡히니 `[start end]`로 회의 구간만 자를 것.
- **대안(로컬)**: `whispermlx` (pyannote, 단어단위 인라인 라벨) — gated 승인·IPv6 다운로드 함정은 `references/diarization.md`.
- **옵션(클라우드, 오디오 외부 업로드 — 민감 자료 금지)**: OpenAI `~/.claude/skills/stt/scripts/transcribe-openai.sh`, ElevenLabs `~/.claude/skills/stt/scripts/transcribe-elevenlabs.sh`. 키는 agents-env 주입.

## TTS (텍스트 → 음성)

음성 합성·복제는 `tts` 스킬 (기본 Qwen3-TTS). 이 스킬은 음성→텍스트 전용.

## 부속

- `brew install ffmpeg` (전처리·구간 자르기), `uv tool install yt-dlp` (다운로드).
- 유튜브 자막/음원은 [[youtube]] 스킬 — 자막 있으면 STT 불필요.
