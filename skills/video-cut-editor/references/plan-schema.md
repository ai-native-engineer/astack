# Cut Plan Schema

`video_cut_workflow.py render`가 읽는 계획의 데이터 계약이다. 편집 판단 절차는 `references/workflow.md`를 따른다.

```json
{
  "source": "/absolute/path/input.mp4",
  "output": "/absolute/path/output.mp4",
  "status": "reviewed",
  "silence_policy": {
    "source": "ffmpeg_silencedetect",
    "min_duration": 1.0,
    "padding": 0.3
  },
  "remove_intervals": [
    {
      "start": 12.34,
      "end": 18.9,
      "reason": "full_retake: marker 1 at 18.5s, failed wording before retake"
    },
    {
      "start": 30.3,
      "end": 38.2,
      "reason": "silence",
      "silence_sources": [
        {"start": 30.0, "end": 38.5, "duration": 8.5}
      ]
    }
  ]
}
```

## 계약

- `start`와 `end`는 원본 타임라인의 초 단위이며 `start < end`여야 한다.
- interval은 서로 겹치지 않는다.
- `status`는 `draft` 또는 `reviewed`다. 프로그램이 계획을 변환하면 다시 `draft`로 둔다.
- 빈 `remove_intervals`와 `reviewed` 상태는 원본 전체를 보존하기로 검토한 계획이다.
- `reason`은 삭제 근거를 짧게 남긴다. 마커 기반 발화 컷은 마커 ID와 시간을 포함한다.
- 사용자가 마커 없는 원본 위치를 직접 지정한 발화 컷은 interval에 숫자형 `source_timestamp`를 기록한다.
- 마커나 `source_timestamp` 근거가 없으면 비무음 interval을 만들지 않는다.
- `skip`과 `needs_manual`은 검토 기록에 남기고 `remove_intervals`에는 넣지 않는다.
- 무음 interval은 `silence_policy`와 하나 이상의 `silence_sources`를 가진다.
- 각 `silence_sources`는 검출된 `start`, `end`, `duration`을 기록하고 interval은 padding 적용 후 실제 삭제 범위를 기록한다.
- 화면 보정으로 무음 interval을 나눠도 각 새 interval은 원래 `silence_sources` 안에 있어야 한다.
- 렌더 뒤 생성된 join map은 해당 계획으로 생긴 실제 접합점 QA에 사용한다.

`source_timestamp` 예시:

```json
{"start": 14.2, "end": 15.4, "source_timestamp": 15.0, "reason": "local_correction: user-selected location"}
```
