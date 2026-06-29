# 컷 마커 효과음 검출

컷편집용 효과음은 스킬에 포함된 `assets/triple-pulse.wav`를 쓴다. 영상에서 편집점 후보를 찾으라고 하면 먼저 이 스크립트를 실행한다.

```bash
python3 ~/.agents/skills/shared/ffmpeg/scripts/detect_cut_markers.py VIDEO.mp4
```

기본값:

- marker: `assets/triple-pulse.wav`
- threshold: `0.90`
- output: 시간·정확도 Markdown 테이블

정확도는 fullband envelope와 8-19 kHz highband envelope를 결합한 normalized correlation score다. `0.90`은 90% 이상만 편집점 후보로 인정한다는 뜻이다.

임계값을 바꿔 재검출할 때:

```bash
python3 ~/.agents/skills/shared/ffmpeg/scripts/detect_cut_markers.py VIDEO.mp4 --threshold 0.95
```

이 스크립트는 검출만 한다. 실제 컷 편집은 검출 시간을 확인한 뒤 `recipes.md`의 자르기/합치기 원칙을 따른다.
