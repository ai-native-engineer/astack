---
argument-hint: "[mode]"
name: tts
description: "Local/offline text-to-speech and voice cloning with Qwen3-TTS/mlx-audio, sample voice registration, full/chunk generation, and partial regeneration. Use when user asks TTS, 텍스트 음성으로, 음성 합성, 음성 복제, voice clone, 내 목소리로, 성우 음성, 더빙, narration, Qwen3-TTS, or 음성 생성. Do NOT use for speech-to-text transcription, podcast publishing workflow, video editing, audio cleanup, or non-voice media conversion."
---

# TTS — 로컬 음성 합성·복제

## 기본 동작
- **기본 엔진 = Qwen3-TTS**(mlx-audio, 로컬·오픈웨이트·완전 오프라인). 주 용도는 음성 복제.
- **기본 클론 음성 = `aiden`**. `full`·`chunk`에서 `--voice`를 생략하면 사용하며, 다른 등록 음성은 `--voice <이름>`으로 고른다.
- **드라이버**: `scripts/tts_clone.py` — `prep` → (`full` | `chunk`) → (`regen`). 외부 전송 없음.
- **빠른 비복제 음성**(파이프라인 테스트·간단 안내): macOS `say -v Yuna -o out.aiff "한국어 문장"`. 클론이 필요 없을 때만.

세부 명령·함정·튜닝·대안 엔진은 작업 직전 `references/voice-clone.md`를 읽는다.

## 두 모드
| 모드 | 방식 | 쓸 때 |
|---|---|---|
| `full` | 텍스트 전체를 1패스로 생성 | 짧은 문장, 빠르게 한 방 |
| `chunk` | 한 줄=한 문장 단위로 따로 생성 → 이어붙임. `manifest.json`으로 부분 재생성 | 긴 글·최고 품질. 한 청크가 망가져도 그 청크만 다시 뽑음 |

- `chunk`가 품질은 가장 좋지만, 세그먼트가 독립 샘플링이라 **톤 일관성이 약간 떨어질 수 있다**.
- 문장 구분은 **줄바꿈**(한 줄=한 문장)으로 — 모델이 줄바꿈에서 텀을 둔다. 청크 **끝음 잘림**은 드라이버가 페이드+패딩으로 보정하되, 실제 마지막 음절이 생성 단계에서 짧게 나오면 `audit` → `regen --duration-multiplier 1.08` 순서로 재생성한다.

## 한국어 발화 최적화
- TTS에 넣을 텍스트는 **표기용 대본이 아니라 발화용 대본**으로 먼저 다듬는다. 원문 파일을 별도로 보존하는 절차는 필수 아님.
- 영어·약어·도구명은 모델이 자연스럽게 읽도록 음차한다. 예: `Claude Code` → `클로드 코드`, `AI` → `에이아이`, `OS` → `오에스`, `PDF` → `피디에프`, `CTA` → `씨티에이` 또는 `콜투액션`.
- 화면용 표기와 발화가 다르면 발화를 우선한다. 예: 코드 `GRANTER`는 음성에서 `코드 그랜터`처럼 읽히게 쓴다.
- 한국어 생성은 `--lang ko`를 명시한다. 드라이버가 이를 `mlx_audio.tts.generate --lang_code ko`로 전달해야 하며, 실행 로그의 `Language: ko`를 확인한다.
- 고유명사는 ASR·TTS가 흔들릴 수 있으므로 발화용 띄어쓰기나 음차 힌트를 쓴다. 예: `대모산개발단`이 불안하면 `대모산 개발단`처럼 분리한다.
- 청크용 줄바꿈은 너무 잘게 쪼개지 않는다. **쉼표나 연결 어미로 끝나는 줄 금지**. 한 줄은 완성 문장 또는 완성된 호흡 단위로 둔다.
- 긴 나레이션에서 `audit` 위험 청크가 많이 나오면 개별 `regen`보다 먼저 줄바꿈 구조를 고친다. 2분 내외 대본은 대략 15~25청크를 우선 목표로 한다.
- `audit`는 원본 청크 꼬리 음량 기준의 보수적 신호다. 최종 실패 판정은 자동 전사(`apple-stt`)와 직접 청취로 문장 누락·고유명사 오류를 확인한다.

## 저장 위치 (둘을 분리)
- **원본 목소리(레퍼런스)** = 재사용 자산 → 스킬 내부 `voices/<이름>/ref.wav + ref.txt`. 기본 `aiden` 음성은 패키지에 포함하며, 다른 저장소가 필요할 때만 `TTS_VOICE_DIR` 또는 `--voice-dir`로 바꾼다.
- **작업 폴더** = `--proj`(생략 시 `/tmp/tts-XXXX` 자동 생성, 휘발성). 청크·manifest·중간물이 여기 쌓인다.
- **최종본 보관** = `--out <폴더|*.wav>`. 완성된 `output.wav`를 원하는 위치에 함께 복사. → `--proj`(작업)와 `--out`(보관)을 같이 쓴다.
- **편집용 정규화본** = `--loudnorm-out <폴더|*.wav>`. 원본을 보존하면서 `loudnorm=I=-16:TP=-1.5:LRA=11`, 48kHz mono WAV로 한 번 더 렌더한다. CapCut/유튜브 나레이션에 넣을 파일은 보통 이 버전이 더 적합하다.

## 빠른 사용
```bash
S=~/.agents/skills/shared/tts/scripts/tts_clone.py
python3 "$S" prep  <영상/음성파일> --voice aiden [--ss 9.6 --dur 14]  # 목소리 1회 등록(스킬 내부)
python3 "$S" voices                                                   # 등록된 목소리 목록
python3 "$S" preptext --text-file script.md --out script-tts.txt      # 한국어 발화/음차/청크 전처리
python3 "$S" chunk --text-file script.txt --lang ko      # → /tmp/tts-XXXX/output.wav
python3 "$S" chunk --text-file script.txt --lang ko --out ~/Desktop/intro.wav  # 보관 위치 지정
python3 "$S" chunk --text-file script.txt --lang ko --out out/raw.wav --loudnorm-out out/edit.wav  # 원본+편집용
python3 "$S" audit --proj /tmp/tts-XXXX                              # 끝음 잘림 의심 청크 찾기
python3 "$S" regen --proj /tmp/tts-XXXX --seg 3 --duration-multiplier 1.08  # 끝음 여유 있게 재생성
python3 "$S" regen --proj /tmp/tts-XXXX --seg 3 [--text "고친 문장"]   # 청크 3만 재생성
python3 "$S" join  --proj /tmp/tts-XXXX --loudnorm-out ~/Desktop/edit.wav  # 기존 청크를 편집용으로 다시 출력
python3 "$S" full  --text-file script.txt                              # 한 방 생성
```
- 다른 엔진(예: VoxCPM2)은 `--model <repo>`로 교체. 기본값은 Qwen3-TTS Base.

## 셋업 (최초 1회)
`mlx-audio`(런타임)·`hf`(가중치)·`ffmpeg` 필요. 설치·모델 다운로드·대안 엔진은 `references/voice-clone.md` 참조.
