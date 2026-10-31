# STT maintainer notes

실행 계약은 `SKILL.md`와 `references/diarization.md`에 있다.

화자 분리는 MOSS-Transcribe-Diarize를 mlx-audio로 로컬에서 돌린다. mlx-audio는
버전을 고정한 일회용 `uv run` 환경에서 실행하고, MOSS 출력 파싱은 그 버전에서
확인했다. pyannote Community-1은 전체 화자 분리 파이프라인을 돌리지 않는다. 분할
모델로 자를 위치를 찾고, 화자 특징값 모델로 조각 사이 화자를 잇는 데만 쓴다. 이
부분은 기존 whispermlx Python 환경을 재사용하고 오프라인으로 실행한다. 오디오는
FFmpeg로 PCM으로 디코딩해 전달하므로 선택적 torchcodec 디코더를 사용하지 않는다.

목소리 기억(`scripts/voices.py`)은 화자 잇기 단계가 사람마다 만드는 256차원 평균
특징을 쓴다. 점수 계산은 Alt 앱의 화자 갤러리를 따르되, 샘플의 일관성(cohesion)
가중치는 Alt 네이티브 모듈 안에 있어 옮기지 않았다. 기준값은 Alt 값이 아니라 로컬
녹음에서 다시 쟀다.

확인 화면(`scripts/diar_review.py`, `assets/diar-review.html`)은 표준 라이브러리만
쓰는 로컬 서버와 빌드 없는 단일 HTML이다. 화면 구성(화자 색 칩, 시간, 본문, 화자 이름
바꾸기)은 Alt 앱의 전사 화면을 따랐다. 앱으로 따로 포장하지 않은 이유는 Alt가 이미 같은
화면을 가진 앱이고, 이 스킬의 차이는 에이전트가 돌리는 받아쓰기와 로컬 목소리 기억에
있기 때문이다. 앱이 필요해지면 같은 페이지를 앱 껍데기에 넣는다.

## 근거

- [MOSS-Transcribe-Diarize](https://huggingface.co/OpenMOSS-Team/MOSS-Transcribe-Diarize)
- [mlx-audio](https://github.com/Blaizzy/mlx-audio)
- [Community-1 모델과 Python API](https://huggingface.co/pyannote/speaker-diarization-community-1)
- [pyannote.audio](https://github.com/pyannote/pyannote-audio)
- Alt(altalt.io) 데스크톱 앱의 1인 턴 규칙(쉼 2초, 최대 60초)과 화자 갤러리 점수 계산을 가져왔다.

## 테스트

- `tests/test_diarize.sh`: 가짜 런타임으로 단계 순서, 턴과 빈 곳 표시, 구간 offset,
  잘못된 인자, MOSS 실패 시 중단, 중단 신호 때 작업 파일 정리를 검증한다.
- `tests/test_pyannote_chunks.py`: 자를 위치, 화자 잇기, 빈 곳 판정, 사람별 목소리 특징을 검증한다.
- `tests/test_voices.py`: 임시 저장소로 등록 조건, 기준값, 여유 차이, 삭제를 검증한다.
- `tests/test_diar_review.py`: 가짜 결과 폴더로 확인 화면 서버의 토큰 검사, 구간 재생,
  이름 저장과 전사본 반영, 빈 곳 처리, 잊기를 검증한다.

실제 모델 검증은 별도 로컬 녹음으로 수행하며 개인 녹음이나 전사문을 저장소에 넣지 않는다.
