---
argument-hint: "[audio-path]"
name: stt
description: "Local speech-to-text transcription and optional speaker diarization for audio/video files, meetings, lectures, interviews, and selected time ranges. Use when user asks STT, 전사, 받아쓰기, 오디오/녹음/회의록/강의/인터뷰 전사, 화자 분리, speaker diarization, or 누가 말했는지. Do NOT use for text-to-speech, Apple Voice Memos personal workflow, YouTube caption extraction, OCR, or audio editing."
---

# STT - Apple 로컬 전사 + 선택적 화자 분리

## 전사 (음성 -> 텍스트)

기본은 macOS 26+의 `apple-stt`다. 일반 텍스트는 Apple 실패 시 Handy에서 선택한 로컬 모델로 한 번 fallback하고, 구조화 출력은 Apple 결과만 쓴다.

- 일반 텍스트: `bash scripts/stt-fallback.sh 녹음.m4a` - Apple이 오류로 종료할 때만 16kHz mono WAV로 변환해 Handy fallback을 실행한다. 이 스크립트는 읽지 말고 실행한다.
- Apple 직접 실행: `apple-stt 녹음.m4a` - `-t`(타임스탬프), `--srt`, `--json`, `--save`, `-l en-US`
- 분석 증거: `apple-stt --analysis-json 녹음.m4a` - versioned Apple evidence object
- 구간: `ffmpeg -ss <시작초> -to <끝초> -i in.m4a -c copy clip.m4a` 후 `apple-stt clip.m4a`
  - 긴 녹음에 회의 외 이동·잡음이 섞이면 그 구간은 전사·화자분리가 다 깨지니 회의 구간만 잘라 처리.
- 정본 소스: `native/apple-stt.swift`. 빌드한 실행 파일은 PATH가 읽는 위치에 설치하고 `command -v apple-stt`로 확인한다.
- 빌드: `swiftc -O -parse-as-library -target arm64-apple-macos26.0 native/apple-stt.swift -o <임시경로>/apple-stt`
- 검증 근거: `references/apple-capabilities.md`. 회귀 비교 계약은 `references/benchmark.md`를 따른다.
- fallback은 성공한 Apple 결과의 품질을 재판정하지 않는다. 자동 품질 비교는 두 엔진을 항상 실행해야 하므로 실제 오류 복구와 분리한다.
- 음성 메모 원본: `~/Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings/*.m4a`

## 화자 분리 (누가 언제 말했나)

`apple-stt`가 텍스트의 유일한 정본이다. 화자 라벨이 필요할 때만 Argmax `diarize`로 RTTM을 만들고 Apple 시간 범위에 결합한다. 세부 계약은 `references/diarization.md`를 읽는다.

- 실행: `bash scripts/stt_diarize.sh <오디오> [start초] [end초]`
- 출력: `stt/YYMMDD-HHMMSS-PID/diarized.md`, `diar.rttm`
- 한 Apple 범위에 여러 화자가 겹치면 `mixed`로 둔다. Argmax 텍스트를 생성하거나 Apple 텍스트를 교체하지 않는다.

## TTS (텍스트 → 음성)

음성 합성과 복제는 `tts` 스킬을 쓴다. 이 스킬은 음성에서 텍스트를 만드는 경로만 다룬다.

## 부속

- `ffmpeg`는 구간 자르기와 로컬 preview에만 쓴다.
- 유튜브는 기존 자막이 있으면 STT를 실행하지 않는다.
