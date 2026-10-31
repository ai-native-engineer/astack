---
argument-hint: "[audio-path]"
name: stt
description: "Use for: Transcribe local audio/video, meetings, lectures, interviews, or selected ranges with optional speaker diarization. Not for TTS, personal Apple Voice Memos workflows, YouTube captions, OCR, or audio editing."
---

# STT - Apple 로컬 전사 + 선택적 화자 분리

## 전사 (음성 -> 텍스트)

기본은 macOS 26+의 `apple-stt`다. 일반 텍스트는 Apple 실패 시 Handy에서 선택한 로컬 모델로 한 번 fallback하고, 구조화 출력은 Apple 결과만 쓴다.

- 일반 텍스트: `bash scripts/stt-fallback.sh 녹음.m4a` - Apple이 오류로 종료할 때만 16kHz mono WAV로 변환해 Handy fallback을 실행한다. 이 스크립트는 읽지 말고 실행한다.
- Apple 직접 실행: `apple-stt 녹음.m4a` - `-t`(타임스탬프), `--srt`, `--json`, `--save`, `-l en-US`
- 분석 증거: `apple-stt --analysis-json 녹음.m4a` - versioned Apple evidence object
- 구간: `ffmpeg -ss <시작초> -to <끝초> -i in.m4a -c copy clip.m4a` 후 `apple-stt clip.m4a`
  - 긴 녹음에 회의 외 이동·잡음이 섞이면 그 구간은 전사·화자분리가 다 깨지니 회의 구간만 잘라 처리.
- 영상 파일(화면 녹화 mp4 등): `apple-stt`는 영상을 직접 받으면 첫 오디오 트랙만 전사해, 다른 트랙에만 있는 발화가 오류 없이 빠진다. 트랙이 여럿이거나 녹화가 아직 끝나지 않은 파일은 `references/recording-files.md`를 먼저 읽는다.
- 고유명사: 이름과 제품명은 `apple-stt --vocab <단어,...>`로 일회성 힌트를 줄 수 있다. 공용 사전보다 먼저 들어간다. 다만 지금까지 Apple 결과가 힌트로 바뀐 관측이 없으므로(`references/apple-capabilities.md`) 오인식 표기 목록을 함께 남긴다. 전역 `~/.config/stt/vocab.txt`는 Voice Memos도 읽는 공용 사전이라 사용자 승인 뒤에만 바꾼다.
- 전사본을 넘길 때 같은 사람이나 제품이 여러 표기로 갈라진 오인식은 목록으로 함께 적는다.
- 정본 소스: `native/apple-stt.swift`. 빌드한 실행 파일은 PATH가 읽는 위치에 설치하고 `command -v apple-stt`로 확인한다.
- 빌드: `swiftc -O -parse-as-library -target arm64-apple-macos26.0 native/apple-stt.swift -o <임시경로>/apple-stt`
- 검증 근거: `references/apple-capabilities.md`. 회귀 비교 계약은 `references/benchmark.md`를 따른다.
- fallback은 성공한 Apple 결과의 품질을 재판정하지 않는다. 자동 품질 비교는 두 엔진을 항상 실행해야 하므로 실제 오류 복구와 분리한다.
- 음성 메모 원본: `~/Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings/*.m4a`

## 화자 분리 (누가 언제 말했나)

화자가 필요하면 MOSS-Transcribe-Diarize가 글과 화자를 함께 만든다. 이 모드의 텍스트 정본은 Apple이 아니라 MOSS다. 화자가 필요 없으면 위의 빠른 전사를 쓴다. 준비, 흐름, 함정은 `references/diarization.md`를 읽는다.

- 실행: `bash scripts/stt_diarize.sh <오디오> [start초] [end초]`
- 출력: `stt/YYMMDD-HHMMSS-PID/`의 `diarized.md`와 확인 화면이 읽는 파일들
- 비용: 모두 로컬에서 돈다. 녹음 길이의 1/7 안팎(1시간 녹음에 약 9분, 3분 녹음에 약 40초)이 걸리고, 메모리는 최대 약 5GB다. 1시간이 넘는 녹음은 실행 전에 걸릴 시간을 알린다.
- 실행 전에 `sysctl vm.swapusage`를 본다. swap 여유가 거의 없으면 조각마다 두세 배 느려지므로 그만큼 늘려 알린다.
- 진행은 로그의 `chunk i/N ... in Ns` 줄로 보고, 남은 조각 수로 남은 시간을 계산해 알린다.
- 긴 녹음은 10분 조각으로 나눠 돌리고, 조각 사이 같은 사람은 목소리 특징으로 잇는다. 목소리가 비슷한 두 사람이 한 사람으로 묶일 수 있다.
- `**[gap]**` 줄은 말소리가 있는데 MOSS가 10초 넘게 비운 곳이다. 전사본을 넘길 때 빠졌을 수 있는 구간으로 함께 알린다.
- 종료 코드 70은 MOSS 단계 실패다. Apple 결과로 대신 채우지 말고 실패를 알린 뒤 빠른 전사를 제안한다.
- 확인 화면: 사용자가 결과를 들으며 확인하거나 화자에게 이름을 붙이려 하면 `python3 scripts/diar_review.py <결과 폴더>`를 백그라운드로 실행하고 출력된 주소를 알린다. 저장한 이름은 그 전사본에 바로 반영되고, "알아보기"를 켜면 다음 녹음에서도 그 목소리를 찾는다.
- `이름?`으로 표시된 추정은 넘길 때 확인 대상으로 적는다. 등록 조건, 대화로 받은 기억 요청, 삭제는 `references/diarization.md`의 확인 화면과 목소리 기억을 따른다.

## TTS (텍스트 → 음성)

음성 합성과 복제는 `tts` 스킬을 쓴다. 이 스킬은 음성에서 텍스트를 만드는 경로만 다룬다.

## 부속

- `ffmpeg`는 구간 자르기, 오디오 트랙 추출, 로컬 preview에만 쓴다.
- 유튜브는 기존 자막이 있으면 STT를 실행하지 않는다.
