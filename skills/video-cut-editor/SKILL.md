---
argument-hint: "[video-path]"
name: video-cut-editor
description: "Edits local lecture and screen recordings from retake markers and reviewed long-silence evidence. Use for 컷편집, 말실수·retake 정리, 편집점 마커, 긴 무음 제거, 접합부 QA, 최종 청취 검수, 영상 병합, or editing-artifact cleanup. Preserves unmarked speech and renders one reviewed plan from the original timeline. Do NOT use for ordinary ffmpeg conversion, CapCut project editing, pure STT, or YouTube planning."
---

# Video Cut Editor

원본 좌표에서 편집 근거와 삭제 계획을 분리하고, 검토된 계획 하나만 렌더한다.

## 핵심 원칙

- 마커, VAD, STT, 무음 검출은 후보를 찾는 증거다. 자동 분석만으로 삭제를 확정하지 않는다.
- 발화 삭제는 검출된 마커나 사용자가 지정한 원본 위치에 한정한다. 표시되지 않은 반복과 말실수는 보존한다.
- 무음은 화면 맥락을 확인한 명확한 장기 구간만 제거한다. 짧은 쉼, 문장 경계, 조용한 UI 조작은 보존한다.
- 모든 삭제 구간은 원본 타임라인의 하나의 계획으로 합치고 원본에서 한 번 렌더한다.
- 렌더 전후 모든 실제 접합점에서 종결 어미, 첫 음절, 문장 의미, 화면 연속성을 확인한다.
- 기술 QA와 사람의 청취 승인을 구분한다. 승인 전까지 원본, 계획, 산출물, 검수 근거를 보존한다.

## 작업 흐름

1. 사용자가 지정한 원본과 출력 범위를 확정하고 분석 근거를 만든다.
2. 마커 판단을 먼저 끝내고, 필요한 경우 검토한 장기 무음을 더해 원본 좌표의 계획을 만든다.
3. 계획을 검증하고 모든 예정 접합점을 미리 확인한 뒤 원본에서 렌더한다.
4. 실제 접합점 기술 QA와 최종 사람 청취를 통과한 파일만 전달하고, 승인 뒤 부산물을 정리한다.

## 참조 라우팅

| 작업 | 읽을 것 |
|---|---|
| 마커 판단, 렌더, 병합, 사람 승인, 정리 | `references/workflow.md` |
| 장기 무음 판단과 화면 맥락 보존 | `references/silence-cut.md` |
| 계획 데이터 계약 | `references/plan-schema.md` |
| 화면 접합부 검사와 보정 | `references/visual-join-qa.md` |

실행 도구는 `scripts/video_cut_workflow.py`를 진입점으로 삼고, 작업별 옵션은 각 스크립트의 `--help`를 따른다.

## 완료 조건

- 수락할 미디어와 QA·승인 근거가 같은 파일을 가리킨다.
- 계획된 발화 접합부와 렌더된 실제 접합부를 모두 검토했다.
- 최종 사람 승인이 기록됐고 요청한 출력 위치에 전달본이 있다.
- 원본은 보존됐으며 cleanup은 생성 부산물 후보를 확인한 뒤 수행했다.
