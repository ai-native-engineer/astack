# STT maintainer notes

실행 계약은 `SKILL.md`와 `references/diarization.md`에 있다.

화자 분리는 기존 whispermlx Python 환경의 pyannote Community-1을 재사용한다.
드라이버는 캐시가 준비됐는지 먼저 검사하고 오프라인으로 실행한다.
오디오는 FFmpeg로 PCM으로 디코딩해 전달하므로 선택적 torchcodec 디코더를
사용하지 않는다. 겹침을 보존한 RTTM과 Apple 전사 범위를 결합한다.

## 근거

- [Community-1 모델과 Python API](https://huggingface.co/pyannote/speaker-diarization-community-1)
- [pyannote.audio](https://github.com/pyannote/pyannote-audio)

`tests/test_diarize.sh`는 전사·화자 분리 결합, 구간 offset, 잘못된 구간,
중단 시 임시 전사 정리를 검증한다. 실제 모델 검증은 별도 로컬 녹음으로
수행하며 개인 녹음이나 전사문을 저장소에 넣지 않는다.
