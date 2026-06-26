# 화자 분리 (diarization) 상세

전사(텍스트)와 화자분리(누가 언제)는 분리된 단계다. `apple-stt`/whisper는 텍스트만, 화자 타임라인은 argmax(또는 pyannote)가 따로 만든다. 그 둘을 시간 겹침으로 합쳐 화자 라벨 전사본을 얻는다.

## 기본: 로컬 argmax (`stt_diarize.sh`)

```
~/.claude/skills/stt/scripts/stt_diarize.sh <오디오> <apple|argmax|both> [start초 end초]
```

세 모드 = 정확도/비용 선택. 스크립트가 정렬·병합까지 끝낸 `.md` 뷰만 내므로 **AI는 고른 뷰 하나만 읽으면 된다**(원본 json/rttm 안 읽어도 됨).

| 모드 | 텍스트 | 화자 경계 | 무게 | 언제 |
|---|---|---|---|---|
| `apple` | apple-stt(깨끗) | **굵음** | 가벼움(diarize만) | 평소 — 내용 파악 + 대략 누가 |
| `argmax` | argmax/WhisperKit | **단어단위 정밀** | 632MB 모델 | 빠른 주고받기까지 정확히 |
| `both` | 둘 다 | — | 최고 | 교차검증·정확도 최우선(토큰 최다) |

- **입자 트레이드오프**: apple-stt는 문장 단위 세그먼트(~10초)라 한 세그먼트에 여러 화자가 섞이면 1명으로 뭉개진다(굵은 화자). argmax는 단어 단위라 끼어듦·맞장구까지 분리되지만 텍스트가 거칠다. 깨끗한 텍스트와 정밀 화자를 동시에는 불가 — apple-stt가 단어 단위 타임스탬프를 안 주기 때문(구조적).
- **구간 트림 `[start end]` 중요**: 회의 뒤 이동·지하철·음악이 붙은 녹음은 그 잡음이 **가짜 화자로 군집**돼 화자 수가 부풀려진다(실측: 전체 90분 → 7명, 회의 12.5분만 자르니 → 3명). 회의 구간만 잘라 처리할 것.
- env: `ARGMAX_CLI`(경로), `STT_OUT`(출력 루트), `STT_LANG`(기본 ko).

### argmax-cli (WhisperKit + SpeakerKit)

- 네이티브 Swift/CoreML, ANE 실행. **gated 모델·토큰 불필요**, 모델 자동 다운로드. macOS URLSession이라 대용량도 IPv4로 자동 폴백(아래 whispermlx의 IPv6 함정 없음).
- 빌드: `git clone https://github.com/argmaxinc/argmax-oss-swift && cd argmax-oss-swift && make setup && swift build -c release` → `.build/release/argmax-cli`.
- 화자 타임라인만 필요하면 `argmax-cli diarize`(전사 안 함, 가벼움). 전사+화자는 `argmax-cli transcribe --diarization`. WhisperKit 모델명은 repo별 상이 — `--help`/HF `argmaxinc/whisperkit-coreml` 참조(스크립트 기본값 `large-v3-v20240930_turbo_632MB`).
- 병합 산출 `argmax_view.md`에 가끔 `[?]` — 무음 틈에 걸려 화자 턴과 안 겹친 단어. 거슬리면 `diar_views.py`에서 직전 화자로 흡수 처리.

## 대안: 로컬 whispermlx (pyannote, 단어단위)

argmax보다 출력은 표준(인라인 라벨)이나 셋업이 무겁고 깨지기 쉽다. 같은 turbo 모델이라 전사 정확도는 동급.

- 설치: `uv tool install whispermlx --python 3.12` — 패키지가 `requires_python <3.14`라 시스템이 3.14면 **3.12 핀 필수**(없으면 설치 실패).
- 실행: `whispermlx <오디오> --model mlx-community/whisper-large-v3-turbo --language ko --diarize --condition_on_previous_text False`
- **gated**: `pyannote/speaker-diarization-community-1` 승인 필요 — hf.co 해당 모델 페이지에서 로그인 후 "Agree", `hf auth login`. 안 하면 첫 화자분리에서 403.
- **IPv6/NAT64 함정**: 일부 네트워크에서 HF 대용량(모델 1GB+) 다운로드가 0바이트로 무한 정지(read 타임아웃 없음). Python은 Happy Eyeballs를 안 해 끊긴 IPv6에 갇힌다. 우회: IPv4 강제 `sitecustomize.py`(socket.getaddrinfo를 AF_INET 우선)를 만들어 `PYTHONPATH=<dir> whispermlx ...`. 모델 캐시 후엔 네트워크 안 타므로 불필요.
- 환각: `--condition_on_previous_text False`로 무음 구간 반복 환각 억제(완전 차단은 아님).

## 옵션: 클라우드 (오디오 외부 업로드 — 민감 자료 금지)

키는 agents-env로 주입(평문 노출 없음).

- **OpenAI** `gpt-4o-transcribe-diarize` — `~/.claude/skills/stt/scripts/transcribe-openai.sh <오디오> [OPENAI_API_KEY@태그] [diarized_json|json|text]`. $0.006/분, 30초+ chunking 자동, 문장 세그먼트 단위.
- **ElevenLabs Scribe** — `~/.claude/skills/stt/scripts/transcribe-elevenlabs.sh <오디오> [ELEVENLABS_API_KEY@태그] [language_code]`. ~$0.40/시간, 단어 단위 타임스탬프 + 언어 자동감지.
