# 무음 제거

로컬 영상 파일에서 긴 무음을 제거할 때 쓴다. CapCut draft를 고치는 작업은 `capcut-editor-assistant`로 보낸다.

## 기본 워크플로

1. `scripts/video_silence_cut.py INPUT --dry-run`으로 무음 구간과 예상 출력 길이를 먼저 본다.
2. `--test-duration 60`으로 1분 샘플을 만든다.
3. 샘플 재생이 자연스러우면 전체 파일을 새 출력 파일로 만든다.
4. 출력 후 `ffprobe` 구조 비교와 `ffmpeg -v error -f null -` 디코딩 검사를 확인한다.

마커 제거도 함께 필요하면 3번의 전체 무음 렌더를 최종본으로 쓰지 않는다. 먼저 `marker-cut-plan.reviewed.json`으로 마커 삭제 구간을 확정하고, `scripts/build_mixed_cut_plan.py`로 남는 구간의 무음만 원본 타임라인 좌표에 합친 plan을 만들어 한 번만 렌더한다.

## 실행

```bash
python3 ~/.agents/skills/shared/video-cut-editor/scripts/video_silence_cut.py in.mp4 --dry-run
python3 ~/.agents/skills/shared/video-cut-editor/scripts/video_silence_cut.py in.mp4 out.sample.mp4 --test-duration 60
python3 ~/.agents/skills/shared/video-cut-editor/scripts/video_silence_cut.py in.mp4 out.silencecut.mp4
```

기본값은 `-35dB`, `0.8초 이상 무음`, `0.15초 padding`이다. 말 앞뒤가 잘리면 padding을 먼저 늘린다.

## 원본 형식 보존의 의미

정확한 무음 컷은 `trim`/`concat` 필터를 거치므로 재인코딩이 필요하다. `-c copy`는 빠르고 무손실이지만 컷 지점이 키프레임에 끌려가 말 시작이나 화면 전환이 어긋날 수 있다.

이 스크립트의 보존 기준은 다음이다.

- 원본 파일은 수정하지 않는다.
- 비디오 코덱 계열을 가능한 한 유지한다. 예: HEVC 입력은 HEVC 출력.
- 해상도, fps, 픽셀 포맷, 색공간 메타데이터를 가능한 한 유지한다.
- 오디오 트랙 수를 유지한다.
- AAC 오디오는 AAC로 다시 인코딩하되 sample rate, channels, bitrate를 가능한 한 유지한다.

출력은 비트 단위 무손실이 아니다. 최종 보고에서는 "재인코딩됨"과 검증 결과를 함께 말한다.

## 언제 값을 바꾸나

- 말 끝이 잘리면 `--padding 0.25` 이상으로 늘린다.
- 숨소리나 키보드 소리가 말로 잡히면 `--silence-db -30dB`처럼 덜 엄격하게 올린다.
- 너무 적게 잘리면 `--silence-db -40dB`처럼 더 엄격하게 낮춘다.
- 짧은 쉼까지 잘리면 `--min-duration 1.0` 이상으로 늘린다.
