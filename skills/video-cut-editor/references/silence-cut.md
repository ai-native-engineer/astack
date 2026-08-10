# 무음 제거

로컬 영상 파일에서 긴 무음을 제거할 때 쓴다. CapCut draft를 고치는 작업은 `capcut-editor-assistant`로 보낸다.

## 기본 워크플로

1. `scripts/video_silence_cut.py INPUT --dry-run`으로 무음 구간과 예상 출력 길이를 먼저 본다.
2. `--test-duration 60`으로 1분 샘플을 만든다.
3. 샘플 재생이 자연스러우면 같은 설정으로 전체 파일을 새 출력 파일로 만든다.
4. 출력 후 `ffprobe` 구조 비교와 `ffmpeg -v error -f null -` 디코딩 검사를 확인한다.
5. `scripts/audit_visual_joins.py`로 실제 접합점을 전수 계산하고 후보 프레임 스트립을 직접 확인한다.
6. 화면 보정을 했다면 긴 무음을 다시 검출해 정적 대기가 되살아나지 않았는지 확인한다.

마커 제거도 함께 필요하면 3번의 전체 무음 렌더를 최종본으로 쓰지 않는다. 먼저 `marker-cut-plan.reviewed.json`으로 마커 삭제 구간을 확정하고, `scripts/build_mixed_cut_plan.py`로 `silencedetect`가 찾은 긴 무음만 원본 타임라인 좌표에 합친 plan을 만들어 한 번만 렌더한다. VAD 음성 구간의 여집합은 삭제 계획으로 쓰지 않는다.

## UI 강의 보존 모드

무음 중에도 클릭, 노드 설정, 실행, 로딩, 생성 대기, 결과 확인이 학습 내용인 UI 강의와 스크린 녹화에는 기본 워크플로 대신 이 모드를 쓴다.

- `silencedetect`, VAD, STT는 화면 검토할 후보를 찾는 데만 쓴다.
- 화면 근거 없이 무음 구간을 `remove_intervals`에 넣지 않는다.
- 긴 정적 화면이나 로딩 화면은 삭제 근거가 아니다.
- 같은 UI 단계를 온전히 다시 시연한 `full_retake`가 화면과 전사에서 확인될 때만 앞의 중복 take를 삭제한다.
- 삭제할 근거가 없으면 `status: reviewed`와 빈 `remove_intervals`를 기록하고 원본 전체를 보존한다.

이 모드는 말보다 화면이 강의의 진행 단위인 경우에 설정 단계가 조용히 사라지는 것을 막는다.

## 실행

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/video-cut-editor/scripts/video_silence_cut.py in.mp4 --dry-run
python3 ${CLAUDE_PLUGIN_ROOT}/skills/video-cut-editor/scripts/video_silence_cut.py in.mp4 out.sample.mp4 --test-duration 60
python3 ${CLAUDE_PLUGIN_ROOT}/skills/video-cut-editor/scripts/video_silence_cut.py in.mp4 out.silencecut.mp4
```

무음 전용 helper 기본값은 `-35dB`, `0.8초 이상 무음`, `0.15초 padding`이다. 마커와 합치는 최종 plan은 더 보수적으로 `1.0초 이상 무음`, `0.30초 padding`을 사용한다. 말 앞뒤가 잘리면 padding을 먼저 늘린다.

## 원본 형식 보존의 의미

정확한 무음 컷은 `trim`/`concat` 필터를 거치므로 재인코딩이 필요하다. `-c copy`는 빠르고 무손실이지만 컷 지점이 키프레임에 끌려가 말 시작이나 화면 전환이 어긋날 수 있다.

이 스크립트의 보존 기준은 다음이다.

- 원본 파일은 수정하지 않는다.
- 비디오 코덱 계열을 가능한 한 유지한다. 예: HEVC 입력은 HEVC 출력.
- 해상도, fps, 픽셀 포맷, 색공간 메타데이터를 가능한 한 유지한다.
- 오디오 트랙 수를 유지한다.
- AAC 오디오는 AAC로 다시 인코딩하되 sample rate, channels, bitrate를 가능한 한 유지한다.

출력은 비트 단위 무손실이 아니다. 최종 보고에서는 "재인코딩됨"과 검증 결과를 함께 말한다.

## 화면 점프 보정

무음 컷 접합부에서 이전 화면 한 프레임, 앱 간 점프, 화면 역행이 보이면 긴 무음 전체를 복원하지 않는다. `references/visual-join-qa.md`의 절차대로 직접 확인한 순수 `silence` interval만 `scripts/refine_visual_silence_plan.py`로 분할한다.

보정 결과는 `draft` plan이므로 plan audit, dry-run, 샘플 확인 뒤 다시 검토 상태로 올린다. 보정본은 visual join audit과 긴 무음 검출을 모두 다시 통과해야 한다.

## 언제 값을 바꾸나

- 말 끝이 잘리면 `--padding 0.25` 이상으로 늘린다.
- 숨소리나 키보드 소리가 말로 잡히면 `--silence-db -30dB`처럼 덜 엄격하게 올린다.
- 너무 적게 잘리면 `--silence-db -40dB`처럼 더 엄격하게 낮춘다.
- 짧은 쉼까지 잘리면 `--min-duration 1.0` 이상으로 늘린다.
