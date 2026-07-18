---
argument-hint: "[video-path]"
name: video-cut-editor
description: "Local video cut editing and silence removal workflow for lecture/screen recording cleanup: remove long silence with padding, detect triple-pulse edit markers, find speech boundaries with VAD, inspect marker/STT evidence, create reviewable cut plans, render once from the original timeline, write join maps, run waveform join QA, merge reviewed outputs, and clean artifacts. Use for 무음 제거, 무음 컷, 컷편집, 말실수 제거, 편집점 마커, 음파 검수, triple-pulse, retake cleanup, final merge, QA report, or cleanup. Do NOT use for ordinary ffmpeg conversion, standalone ffmpeg/media operations, CapCut draft editing, pure STT, or YouTube planning."
---

# Video Cut Editor

무음 제거와 마커 기반 컷편집 워크플로우를 다룬다. 목표는 원본 타임라인에서 증거를 만들고, 필요한 경우 검토된 `cut-plan.json`만 최종 렌더하는 것이다.

## Mental Model

- Marker/VAD가 타임라인을 잡는다.
- 무음 제거는 dry-run과 1분 샘플로 padding을 먼저 확인한다.
- STT는 앞뒤 내용 판단을 위한 증거로만 쓴다.
- 자동 분석과 의미 판단을 분리한다.
- 무음 제거와 마커 제거를 함께 요청받으면 마커 판단을 먼저 끝낸 뒤 남는 타임라인에서 무음을 잡고, 하나의 최종 `cut-plan.json`으로 원본에서 한 번만 렌더한다.
- 고급 ffmpeg 인코딩·필터·stream copy 판단이 필요하면 `$ffmpeg`를 보조 스킬로 사용하고, 컷 판단과 `cut-plan.json`은 이 스킬에서 유지한다.

## Workflow

| 작업 | 읽을 것 |
|---|---|
| 무음 제거·무음 컷·padding 샘플 테스트 | `references/silence-cut.md` |
| 말실수·retake·편집점 마커 기반 컷편집 | `references/workflow.md` |
| `cut-plan.json` 필드·검토 상태 확인 | `references/plan-schema.md` |

마커 기반 컷편집은 `scripts/video_cut_workflow.py analyze INPUT.mp4`로 `review.md`와 `cut-plan.json` 템플릿을 만든 뒤, marker 전후 STT/VAD evidence를 읽고 `remove_intervals`를 채운다.

렌더 전에는 `scripts/audit_cut_plan.py PLAN.json`과 `render --dry-run`으로 플랜을 확인한다. 최종 영상은 요청한 출력 경로에 두고, 기본 생성되는 render log, join map, waveform join QA, merge QA 같은 부산물은 `<output-stem>.video-cut-artifacts/`에 모은다. 최종 렌더 뒤 이 artifact 폴더의 증거와 `ffprobe`/decode 검증 결과를 보고한다.

## Scripts

- `scripts/video_cut_workflow.py` — analyze/render 오케스트레이터. 먼저 `--help`를 보고 실행한다.
- `scripts/detect_cut_markers.py` — bundled `assets/triple-pulse.wav` 편집점 검출.
- `scripts/audit_cut_plan.py` — broad marker cut, no-retake marker, tail cut 같은 위험 플랜을 렌더 전에 탐지한다.
- `scripts/audit_waveform_joins.py` — 최종본 전체 파형이 아니라 `*.join-map.json`의 실제 접합점만 PCM 파형으로 검사한다.
- `scripts/build_mixed_cut_plan.py` — reviewed marker plan과 speech evidence를 합쳐 최종 무음+마커 plan을 만든다.
- `scripts/merge_reviewed_outputs.py` — spot-check와 decode 검증을 통과한 edited 파일만 최종 병합한다.
- `scripts/cleanup_artifacts.py` — 원본·edited·merged 영상은 보존하고 생성 evidence/log/workspace만 정리한다.
- `scripts/video_speech_cut.py` — frame-level VAD 기반 음성 구간 분석과 speech cut 렌더.
- `scripts/video_silence_cut.py` — 로컬 영상 파일 무음 제거와 speech/VAD 경계 분석 helper.

## Critical Rules

- 검토 전 marker 기반 자동 렌더를 하지 않는다.
- 모든 마커를 일괄 `cut_before_marker`로 처리하지 않는다.
- `cut_before_marker`는 뒤에서 전체 clause/sentence retake가 확인될 때만 쓴다.
- local correction은 실패한 단어·구만 자르고, 직전 VAD segment 전체를 삭제하지 않는다.
- 뒤에 retake가 없는 tail marker는 `skip` 또는 짧은 trailing trim으로 처리한다.
- 컷 구간은 원본 타임라인 초 단위로 기록한다.
- 무음 제거와 마커 제거가 모두 필요하면 마커 컷을 먼저 확정하고, 그 뒤 남는 구간의 무음만 원본 타임라인 좌표로 합쳐 한 번 렌더한다.
- 긴 렌더는 기본 render log를 남기고, 중단 판단 전 로그·프로세스·출력 파일 크기 증가를 확인한다.
- 마커 컷이 있는 최종본은 대표 위험 구간을 STT 또는 직접 재생으로 spot-check한다.
- 파형 QA는 `join-map`의 접합점만 검사한다. 전체 오디오 스캔은 정상 발화 강세를 컷 후보로 오검출한다.
- 여러 edited 파일을 합칠 때는 개별 spot-check와 decode 검증을 통과한 파일만 merge한다.
- 최종 QA는 input preflight, marker spot-check, merge warning, duration/decode 결과를 한 보고서로 남긴다.
- 증거·로그·QA 부산물은 기본적으로 `<output-stem>.video-cut-artifacts/`에 모으고, 원본·edited·merged 영상과 섞어 두지 않는다.
- cleanup은 dry-run 후보 확인 뒤 실행하고 원본·edited·merged 영상은 보존한다.
- 기존 산출물은 덮어쓰지 말고 archive 폴더로 치운다.
- 정확 컷은 재인코딩이므로 bitstream 무손실이라고 말하지 않는다.
