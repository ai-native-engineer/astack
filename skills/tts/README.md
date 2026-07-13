# tts (maintainer notes)

로컬 음성 합성·복제 스킬. 기본 엔진 Qwen3-TTS(mlx-audio), 한국어 발화 전처리(preptext), full/chunk 모드 + 청크 부분 재생성.

## 출처·근거
- 런타임: [mlx-audio](https://github.com/Blaizzy/mlx-audio) (`mlx_audio.tts.generate`).
- 모델: [Qwen3-TTS](https://github.com/QwenLM/Qwen3-TTS) (MLX 변환본 `mlx-community/Qwen3-TTS-12Hz-1.7B-Base-bf16`). 대안 [VoxCPM2](https://huggingface.co/openbmb/VoxCPM2).
- 끝음 페이드+패딩·concat 포맷일치·줄바꿈 분리·zsh `LINES` 함정은 2026-06-14 실측 세션에서 도출. 메모리 `reference_qwen3_tts_mlx_generation.md`와 동일 노하우.

## 구조
- `SKILL.md` — 라우팅·모드·빠른 사용(항상 로드).
- `references/voice-clone.md` — 셋업·레퍼런스 준비·함정·튜닝·대안 엔진(작업 시 로드).
- `scripts/tts_clone.py` — stdlib 전용 드라이버. `preptext`로 한국어 발화용 텍스트를 만들고, mlx_audio/ffmpeg를 PATH로, apple-stt를 `~/scripts/apple-stt`로 호출(전사). 모델은 `--model`로 교체 가능(범용).
- `voices/aiden/` — 패키지에 포함되는 기본 음성 레퍼런스(`ref.wav` + `ref.txt`).

## 분리 이력
`stt` 스킬에 있던 빈약한 TTS 섹션(`say -v Yuna`, STT 왕복 테스트용)을 이 스킬로 이관. `stt`는 STT 전용으로 좁히고 TTS 라우팅 키워드 제거 → 두 스킬 라우팅 중복 방지.
