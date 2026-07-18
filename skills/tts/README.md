# TTS

Qwen3-TTS와 mlx-audio 기반의 로컬 음성 합성·복제 스킬이다. 배포본에는 개인 음성을 포함하지 않으며, `prep`으로 등록한 음성은 로컬 데이터 디렉터리에 보관한다.

## 구조

- `SKILL.md`: 항상 로드되는 실행 계약
- `references/voice-clone.md`: 셋업, 음성 등록, 품질 복구, 튜닝
- `scripts/tts_clone.py`: 결정론적 전처리·생성 드라이버
- `tests/test_tts_clone.py`: 외부 모델 없이 실행하는 최소 회귀 검사
- `~/.local/share/tts/voices/`: 사용자별 음성 레퍼런스(패키지 외부)

사람의 음성·전사문은 개인 데이터이므로 shared 스킬이나 플러그인 repo에 추가하지 않는다.
