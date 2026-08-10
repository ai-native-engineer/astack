# 화면 접합부 QA

렌더나 병합 뒤 실제 접합점의 화면 연속성을 확인할 때 읽는다. 구조·디코딩 검증은 프레임 내용의 자연스러움을 승인하지 않는다.

## 검사

`join-map`의 모든 접합점을 검사한다.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/video-cut-editor/scripts/audit_visual_joins.py OUTPUT.mp4 OUTPUT.video-cut-artifacts/OUTPUT.join-map.json
```

도구는 접합점 전후 프레임의 PTS를 각각 0부터 다시 시작하게 한 뒤 SSIM을 계산한다. 기본값은 접합점 양쪽 `0.10초`, 폭 `640`, 후보 기준 `0.95`다.

- 생성된 `*.visual-audit.json`과 `*.visual-audit.md`에서 전수 검사 개수를 확인한다.
- `visual-review/`의 후보 스트립을 직접 보고 앱 전환, 이전 화면 한 프레임 노출, 역행, 깜빡임을 판정한다.
- merge join과 이전 실패 지점은 점수가 높아도 표본으로 직접 확인한다.
- SSIM은 변화량 순위를 위한 휴리스틱이다. 낮은 점수는 자동 실패가 아니고 높은 점수도 의미상 연속성을 보장하지 않는다.
- 임계값과 프레임 간격은 녹화 해상도·UI 변화량에 맞춰 조정하고, 최종 판정 근거를 보고서에 남긴다.

## 무음 컷이 화면 점프를 만든 경우

문제가 `reason: silence`인 접합부에서 생겼다면 해당 원본 plan의 정확한 `start`/`end`만 JSON 배열로 기록한다. 마커나 merge join은 이 보정 경로에 넣지 않는다.

```json
[
  {"start": 12.34, "end": 18.9}
]
```

긴 무음 전체를 복원하지 말고 장면 변화 주변만 보존하는 draft plan을 만든다.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/video-cut-editor/scripts/refine_visual_silence_plan.py \
  cut-plan.reviewed.json reviewed-visual-silences.json \
  --output-plan cut-plan.visual-safe.json \
  --output-media OUTPUT.visual-safe.mp4 \
  --report visual-silence-report.json
```

- 입력 interval은 명시적인 `silencedetect` evidence가 있는 순수 `silence`여야 한다.
- 도구는 짧은 구간을 보존하고, 긴 구간은 감지한 장면 변화 앞뒤의 보존 창으로 분할한다.
- 장면 감지는 화면 녹화에 맞춘 휴리스틱이므로 `--scene-threshold`와 보존 창은 샘플을 보고 조정한다.
- 출력 plan은 `draft`다. `audit_cut_plan.py`, dry-run, 그 plan의 샘플 검토 뒤에만 `reviewed`로 바꾼다.
- 보정본을 원본에서 한 번 렌더한 뒤 visual join audit과 `silencedetect`를 다시 실행한다.
- 장시간 정적 무음이 다시 생겼다면 화면 연속성만 좋아졌어도 보정을 통과시키지 않는다.

## 완료 판정

- 모든 실제 접합점이 점수 계산 대상에 포함됐다.
- 모든 후보 스트립을 직접 판정했다.
- 보정 뒤 후보와 장시간 정적 무음을 다시 검사했다.
- 파형 `listen` 지점은 사람 청취 전까지 별도 미해결 항목으로 남겼다.
