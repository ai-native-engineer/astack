# 화자 분리

전사 텍스트와 화자 타임라인은 분리한다. Apple `SpeechTranscriber`가 텍스트의
유일한 정본이고, pyannote Community-1은 사용자가 요청할 때 로컬에서 RTTM만 만든다.

## 실행

설치된 `stt` 스킬 루트에서 실행한다.

```sh
bash scripts/stt_diarize.sh <오디오> [start초] [end초]
```

결과는 `stt/YYMMDD-HHMMSS-PID/diarized.md`와 원본 `diar.rttm`이다. 실제
다화자 품질 gate 전에는 이름 mapping을 만들지 않고 raw RTTM을 함께 보존한다.
구간 시작값을 주면 `diarized.md` 타임스탬프는 원본 녹음 기준으로 표시하고,
raw RTTM은 잘린 clip 기준 시간을 그대로 보존한다.
실행은 `scripts/pyannote-diarize.py`를 통해 설치된 `whispermlx`의 Python 환경을 재사용한다. MPS를 사용할 수 있으면 MPS, 아니면 CPU를 쓰며 선택한 장치를 stderr에 출력한다.

- `PYANNOTE_PYTHON`: 다른 환경을 명시할 때의 Python 실행 파일 경로
- `PYANNOTE_DEVICE`: `auto`(기본), `mps`, `cpu` 중 선택
- `STT_OUT`: 출력 루트

`APPLE_STT_BIN`은 테스트나 설치 전 smoke test에서만 별도 Apple 바이너리를
지정한다. 일반 실행은 PATH의 `apple-stt`를 쓴다.

모델은 Hugging Face의 기존 `pyannote/speaker-diarization-community-1` 캐시만 읽는다. 없으면 전사를 시작하기 전에 중단한다. 모델 접근 승인과 인증은 Hugging Face 공식 절차로 준비하고, 다운로드는 `hf download pyannote/speaker-diarization-community-1`로 별도 수행한다. 실행 중에는 모델 다운로드나 오디오 외부 전송을 하지 않는다.

## 결합 규칙

- Apple segment와 RTTM turn의 시간 겹침만 사용한다.
- 한 Apple range가 정확히 한 화자와 겹치면 그 익명 label을 붙인다.
- 두 명 이상과 겹치면 `mixed`로 둔다. 텍스트를 임의로 쪼개거나 dominant speaker에게 넘기지 않는다.
- 겹치는 RTTM turn이 없으면 `?`로 둔다.
- 화자 이름은 녹음별 명시적 mapping만 허용한다. 음성 embedding과 녹음 간 생체 identity는 저장하지 않는다.

Apple timing이 너무 거칠어 다화자 fixture 대부분이 `mixed`라면 이름 mapping을
진행하지 않는다. 이 경우 Apple transcript와 optional raw RTTM만 유지한다.

## 구간 선택

회의 뒤 이동, 음악, 긴 잡음이 붙은 녹음은 가짜 화자 수를 늘린다. 회의 범위를
알면 `[start초] [end초]`로 잘라 diarization 입력만 제한한다. 두 값은 원본 녹음의
절대 위치이며 `end초`는 구간 길이가 아니다. 원본은 바꾸지 않는다.
