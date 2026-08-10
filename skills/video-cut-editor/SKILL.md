---
argument-hint: "[video-path]"
name: video-cut-editor
description: "Local video cut editing and silence removal workflow for lecture/screen recording cleanup: remove long silence with padding, detect triple-pulse edit markers, find speech boundaries with VAD, inspect marker/STT evidence, create reviewable cut plans, render once from the original timeline, run PTS-normalized frame and waveform QA at actual joins, merge reviewed outputs, and clean artifacts. Use for 무음 제거, 무음 컷, 컷편집, 말실수 제거, 편집점 마커, 프레임 검수, 음파 검수, triple-pulse, retake cleanup, final merge, QA report, browser listening review, HTML review editor, human approval, or cleanup. Do NOT use for ordinary ffmpeg conversion, standalone ffmpeg/media operations, CapCut draft editing, pure STT, or YouTube planning."
---

# Video Cut Editor

무음 제거와 마커 기반 컷편집 워크플로우를 다룬다. 목표는 원본 타임라인에서 증거를 만들고, 필요한 경우 검토된 `cut-plan.json`만 최종 렌더하는 것이다.

## Mental Model

- Marker/VAD와 `silencedetect`는 컷 후보를 찾는 증거이며, 자동 삭제 명령이 아니다.
- 무음 제거는 최종 plan 그대로 만든 샘플로 padding을 먼저 확인한다.
- STT는 앞뒤 내용 판단을 위한 증거로만 쓴다.
- UI 강의나 스크린 녹화에서 무음에도 설정, 실행, 로딩, 결과 확인이 남을 수 있으면 화면 검토 전에는 `remove_intervals: []` 보존 계획을 유지한다.
- 자동 분석과 의미 판단을 분리한다.
- `join-map`은 렌더 뒤 파형과 화면 연속성을 검사할 실제 접합점의 원장이다.
- 무음 제거와 마커 제거를 함께 요청받으면 마커 판단을 먼저 끝낸 뒤 남는 타임라인에서 무음을 잡고, 하나의 최종 `cut-plan.json`으로 원본에서 한 번만 렌더한다.
- 고급 ffmpeg 인코딩·필터·stream copy 판단이 필요하면 `$ffmpeg`를 보조 스킬로 사용하고, 컷 판단과 `cut-plan.json`은 이 스킬에서 유지한다.

## Workflow

| 작업 | 읽을 것 |
|---|---|
| 무음 제거·무음 컷·padding 샘플 테스트 | `references/silence-cut.md` |
| 말실수·retake·편집점 마커 기반 컷편집 | `references/workflow.md` |
| 렌더 뒤 프레임 접합부 전수 검사·화면 점프 보정 | `references/visual-join-qa.md` |
| `cut-plan.json` 필드·검토 상태 확인 | `references/plan-schema.md` |
| 최종 사람 청취·HTML 검수 에디터·승인 JSON | `references/workflow.md#human-listening-review` |

마커 기반 컷편집은 `scripts/video_cut_workflow.py analyze INPUT.mp4`로 `review.md`와 `cut-plan.json` 템플릿을 만든 뒤, marker 전후 STT/VAD evidence를 읽고 `remove_intervals`를 채운다.

렌더 전에는 `scripts/audit_cut_plan.py PLAN.json`과 `render --dry-run`으로 플랜을 확인한다. 최종 영상은 요청한 출력 경로에 두고, 기본 생성되는 render log, join map, visual/waveform join QA, merge QA 같은 부산물은 `<output-stem>.video-cut-artifacts/`에 모은다. 최종 렌더 뒤 이 artifact 폴더의 증거와 `ffprobe`/decode 검증 결과를 보고한다.

## Scripts

- `scripts/video_cut_workflow.py` — analyze/render 오케스트레이터. 먼저 `--help`를 보고 실행한다.
- `scripts/detect_cut_markers.py` — bundled `assets/triple-pulse.wav` 편집점 검출.
- `scripts/audit_cut_plan.py` — broad marker cut, no-retake marker, tail cut 같은 위험 플랜을 렌더 전에 탐지한다.
- `scripts/audit_visual_joins.py` — 모든 실제 접합점의 양쪽 프레임을 PTS 정규화해 비교하고 검토 후보 스트립을 만든다.
- `scripts/audit_waveform_joins.py` — 최종본 전체 파형이 아니라 `*.join-map.json`의 실제 접합점만 PCM 파형으로 검사한다.
- `scripts/build_mixed_cut_plan.py` — reviewed marker plan과 명시적인 긴 무음 evidence를 합쳐 최종 plan을 만든다.
- `scripts/refine_visual_silence_plan.py` — 직접 확인한 화면 위험 `silence` 구간만 장면 변화 주변으로 쪼개 새 draft plan을 만든다.
- `scripts/merge_reviewed_outputs.py` — 검토된 edited 파일만 병합하고 재인코딩 시 트랙별 입력 비트레이트와 최종 출력 품질을 검증한다.
- `scripts/build-listening-review.py` — 최종 join map의 마커/파일 연결부를 2배속으로 승인·반려하고 JSON을 내보내는 HTML 검수 에디터를 만든다. `--transcript`로 접합부 전후 발화를, edit join 카드에는 고칠 원본 좌표를 함께 싣는다.
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
- VAD `speech_segments`의 여집합을 자동 삭제하지 않는다. 조용한 음절과 짧은 호흡이 음성 밖으로 분류될 수 있기 때문이다.
- 자동 무음 컷은 기본적으로 1.0초 이상 검출된 무음에서 양쪽 0.30초를 보존한다.
- 샘플과 최종본은 같은 `cut-plan.json`을 사용하고, 기술 QA와 사람의 청취 승인을 구분해 보고한다.
- 긴 렌더는 기본 render log를 남기고, 중단 판단 전 로그·프로세스·출력 파일 크기 증가를 확인한다.
- 긴 렌더의 호출 래퍼가 끝났다는 표시만으로 QA를 시작하지 않고, 대상 `ffmpeg` 프로세스 종료와 출력 파일 close를 확인한 뒤 검사한다.
- 마커 컷이 있는 최종본은 대표 위험 구간을 STT 또는 직접 재생으로 spot-check한다.
- 마커 evidence가 있는 최종본은 원본과 같은 threshold로 잔존 마커를 다시 검사하고, 하나라도 남으면 전달하지 않는다.
- 화면 QA는 `join-map`의 모든 접합점을 비교하고 낮은 SSIM 후보의 프레임 스트립을 직접 본다. SSIM은 후보 순위일 뿐 편집 승인값이 아니다.
- 화면 점프가 난 긴 무음은 전체 구간을 복원하지 않고, 직접 확인한 `silence` 구간만 장면 변화 주변으로 분할한 draft plan을 다시 검토한다.
- 화면 보정 뒤에는 프레임 접합부와 긴 무음을 모두 다시 검사한다. 화면을 살리면서 정적 대기를 되살릴 수 있기 때문이다.
- 파형 QA는 `join-map`의 접합점만 검사한다. 전체 오디오 스캔은 정상 발화 강세를 컷 후보로 오검출한다.
- 파형 QA의 트랙은 `0:a:0`, `0:a:1` 같은 FFmpeg stream specifier로 지정하고 실제 오디오 트랙을 모두 검사한다.
- 파형의 `listen` 판정은 STT가 자연스러워도 사람 청취 전까지 미해결로 보고한다.
- 여러 edited 파일을 합칠 때는 개별 spot-check와 decode 검증을 통과한 파일만 merge한다.
- 최종 QA는 input preflight, marker spot-check, merge warning, duration/decode 결과를 한 보고서로 남긴다.
- 최종 합본이 다시 생성되면 이전 QA를 무효화하고 수락할 파일에서 decode, 모든 오디오 트랙, 마커, 화면 접합부, 긴 무음을 다시 검사한다.
- 기술 QA 뒤에는 위험 접합점과 그 구간 전사를 함께 실은 2배속 HTML 검수 에디터를 열고, 승인 JSON이 나오기 전까지 산출물과 검수 증거를 보존한다. 중복·잘린 문장은 귀보다 눈으로 먼저 잡힌다.
- 증거·로그·QA 부산물은 기본적으로 `<output-stem>.video-cut-artifacts/`에 모으고, 원본·edited·merged 영상과 섞어 두지 않는다.
- cleanup은 dry-run 후보 확인 뒤 실행하고 원본·edited·merged 영상은 보존한다.
- work 디렉토리를 통째로 지우기 전에 reviewed cut plan을 artifacts로 옮긴다. 최종본을 원본에서 다시 만드는 유일한 기록인데 cleanup 후보에는 안 잡힌다.
- 기존 산출물은 원본, 검토 plan, 길이와 패킷을 비교해 호환성이 확인되기 전까지 그대로 보존하고, 이름이 충돌하면 별도 candidate를 만든다.
- 범퍼나 외부 클립을 붙일 때는 stream shape가 같아 보여도 전체 디코드로 결합 호환성을 확인하고, 실패하면 최종 결합본을 재인코딩한다.
- 정확 컷은 재인코딩이므로 bitstream 무손실이라고 말하지 않는다.
