# TTS

Qwen3-TTS와 mlx-audio 기반의 로컬 음성 합성·복제 스킬이다. `aiden` 음성을 기본 제공하고, `prep`으로 등록한 음성을 `voices/<name>/`에 함께 보관한다.

## 구조

- `SKILL.md`: 항상 로드되는 실행 계약
- `references/voice-clone.md`: 셋업, 음성 등록, 품질 복구, 튜닝
- `scripts/tts_clone.py`: 결정론적 전처리·생성 드라이버
- `scripts/test_tts_clone.py`: 외부 모델 없이 실행하는 최소 회귀 검사
- `voices/`: 패키지에 포함되는 음성 레퍼런스

`voices/`의 파일은 astack 공개 배포에 포함될 수 있으므로 재배포 동의를 받은 음성만 추가한다.
