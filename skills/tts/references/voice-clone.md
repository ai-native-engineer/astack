# Voice clone — 상세 (Qwen3-TTS / mlx-audio)

레이어 구분: 실행 프로그램(`mlx-audio`, `mlx_whisper`) = uv tool / 모델 가중치 = HF 캐시(`~/.cache/huggingface`). `hf`는 가중치 다운로드 도구지 프로그램 설치 도구가 아니다.

## 셋업 (최초 1회)
```bash
uv tool install mlx-audio                      # 런타임 (mlx_audio.tts.generate)
uv tool install huggingface_hub                # 가중치 다운로드 (hf)
# ffmpeg: brew install ffmpeg
```
- 가중치는 첫 실행 시 repo id로 자동 다운로드된다. 미리 받으려면: `hf download mlx-community/Qwen3-TTS-12Hz-1.7B-Base-bf16`.
- 전사용 whisper(`mlx-community/whisper-large-v3-turbo`)는 stt 스킬과 캐시 공유.

## 저장 위치 (영구 vs 휘발)
- **레퍼런스(원본 목소리)**: 영구 보관함 `~/.local/share/tts/voices/<name>/ref.wav + ref.txt`. env `TTS_VOICE_DIR` 또는 `--voice-dir`로 변경. 개인 음성이라 /tmp·git에 두지 않는다. `voices`로 목록 확인.
- **프로젝트(작업 폴더)**: `--proj` 미지정 시 `tempfile.mkdtemp`로 `/tmp/tts-XXXX` 자동 생성. `manifest.json`이 레퍼런스 절대경로를 기록하므로, 보관함 voice가 있으면 /tmp 프로젝트가 날아가도 `prep` 없이 다시 생성 가능.
- **최종본 보관**: `--out <폴더|*.wav>`로 완성된 `output.wav`를 원하는 위치에 복사(작업 폴더와 별개). full/chunk/regen/join 모두 지원. `--proj`와 `--out`을 함께 쓴다.
- **편집용 정규화본 보관**: `--loudnorm-out <폴더|*.wav>`로 원본과 별개인 편집용 WAV를 만든다. 필터는 `loudnorm=I=-16:TP=-1.5:LRA=11`, 출력은 48kHz mono `pcm_s16le`. CapCut/유튜브 나레이션에 바로 넣을 때는 이 파일을 우선 사용하고, 원본 `output.wav`는 재처리용으로 남긴다.

## 1) 레퍼런스 준비 (prep)
좋은 클론은 레퍼런스가 9할. 조건: **단일 화자, 클린(무음악·저잡음), 자연 발화 10~30초**.
- 배경음악 깔린 구간 금지 — 클론에 음악이 섞인다. `ffmpeg ... silencedetect=noise=-30dB:d=0.4`로 무음이 거의 없으면 음악 베드이므로 다른 구간을 쓴다.
- `prep`이 클립 추출(loudnorm·24k·mono) + `mlx_whisper` 전사로 보관함에 `ref.wav`/`ref.txt`를 만든다. **ref_text(전사)를 같이 줘야 클론 품질이 오른다.**
- 미디어에서 특정 구간만: `prep <file> --voice <name> --ss <시작초> --dur <길이>`. 이미 깨끗한 wav면 `--ss/--dur` 생략.

## 2) 생성 — full vs chunk
- **full**: `--join_audio`로 1패스. 짧은 글에 빠르다. 단 긴 글은 중간에 "튕김"이 나면 통째로 못 쓴다.
- **chunk**: 한 줄=한 문장으로 쪼개 각각 생성 → 끝 페이드(~60ms)+무음 패딩 → concat. `manifest.json`에 모델·ref·문장 리스트를 저장.
  - 장점: 한 청크만 망가져도 `regen`으로 그것만 교체. 품질 최상.
  - 단점: 세그먼트 독립 샘플링이라 톤 일관성이 약간 흔들릴 수 있다(아래 튜닝으로 완화).

### 한국어 발화용 텍스트 전처리
TTS에는 화면용 표기보다 **귀로 들었을 때 자연스러운 발화문**을 넣는다. 이 스킬은 최종 발화용 대본을 만드는 쪽이므로 원문/녹음용 파일을 강제로 분리하지 않는다.

권장 변환:
- `Claude Code` → `클로드 코드`
- `AI` → `에이아이`
- `OS` → `오에스`
- `PDF` → `피디에프`
- `CTA` → `씨티에이` 또는 문맥상 `콜투액션`
- `URL`, `MCP`, 제품 코드, 쿠폰 코드처럼 그대로 읽으면 어색한 표기는 한국어 발화로 바꾼다. 예: `NOVA` → `코드 노바`.
- 숫자는 기계적으로 모두 한글화하지 않는다. 발음이 불안정하거나 영상에서 중요한 숫자만 발화 기준으로 고친다. 예: `44일` → `사십사 일`, `73억` → `칠십삼억`.
- 고유명사는 붙여 쓰면 TTS·ASR이 흔들릴 수 있다. 발음이 중요한 이름은 발화용 띄어쓰기를 둔다. 예: `코드스쿨` → `코드 스쿨`.

줄바꿈/청크 기준:
- 한 줄이 곧 한 청크다. 빈 줄은 무시된다.
- 쉼표, `그리고`, `-고`, `-서`, `-면`처럼 다음 절을 기다리는 형태로 줄을 끝내지 않는다.
- 너무 짧은 청크가 많으면 끝음 잘림 위험과 톤 불일치가 늘어난다.
- 반대로 한 청크가 너무 길면 발음이 뭉개질 수 있다. 2분 내외 한국어 나레이션은 대략 15~25청크를 1차 목표로 잡는다.
- `audit`에서 RISK가 전체 청크의 20~30% 이상이면 먼저 텍스트 줄바꿈을 다시 잡고 재생성한다. 일부 청크만 RISK면 해당 청크를 `regen --duration-multiplier 1.08`로 재생성한다.

전처리 명령:
```bash
python3 tts_clone.py preptext --text-file script.md --out script-tts.txt
python3 tts_clone.py preptext --text "Claude Code와 AI OS를 4주 동안 만듭니다."
```
`preptext`는 음차, 일부 숫자+단위 발화 변환, 줄바꿈 청크 정리를 수행한다. 결과는 바로 `chunk --text-file`에 넣는 것을 목표로 한다.

## 3) 부분 재생성 (regen)
```bash
python3 tts_clone.py regen --proj DIR --seg 3              # 청크 3 다시 뽑기(같은 텍스트)
python3 tts_clone.py regen --proj DIR --seg 3 --text "..." # 텍스트도 교체
python3 tts_clone.py regen --proj DIR --seg 3 --duration-multiplier 1.08 # 끝음 여유 있게 재생성
python3 tts_clone.py join  --proj DIR                      # 수동 편집 후 재이어붙이기
python3 tts_clone.py join  --proj DIR --loudnorm-out edit.wav # 편집용 loudnorm 파일만 다시 출력
```
`regen`은 `manifest.json` 기준으로 해당 청크만 재생성하고 `output.wav`를 다시 만든다.

## 최종 음량 정규화 (편집용)
TTS 원본은 문장별 음량이 조금 작거나 편차가 있을 수 있다. 긴 나레이션을 영상 편집에 넣을 때는 원본과 편집용 파일을 둘 다 남긴다.

```bash
python3 tts_clone.py chunk --voice myvoice --text-file script.txt --lang ko \
  --out out/raw.wav \
  --loudnorm-out out/edit.wav
```

- `--out`: 원본 보존용. 24kHz mono 출력이며, 필요하면 다시 정규화하거나 청크 재생성 기준으로 쓴다.
- `--loudnorm-out`: 편집 투입용. 48kHz mono, 평균 음량 목표 `-16 LUFS`, true peak `-1.5 dB`.
- 배경음악과 섞을 최종본이면 `--loudnorm-out` 파일을 먼저 타임라인에 넣고, 필요 시 CapCut에서 -1~-3dB 정도만 미세 조정한다.

## 끝음 잘림 (실측 함정)
모델이 마지막 음절을 EOS로 일찍 잘라먹는다. 청크 꼬리 120ms의 max 음량이 -13dB대로 크면 끊긴 것(자연 감쇠는 -20dB대).
- 드라이버가 **끝 ~60ms 페이드아웃 + 무음 패딩**(`afade`+`apad`)으로 보정한다.
- 생성 텍스트에는 드라이버가 청크마다 줄바꿈 두 줄을 붙여 EOS 여백을 준다.
- 의심 청크 찾기: `python3 tts_clone.py audit --proj DIR`. 원본 `seg_NN_000.wav`의 마지막 120ms max volume이 기본 `-18 dB`보다 크면 `RISK`로 표시한다.
- `audit`는 원본 청크 꼬리 음량을 보는 보수적 휴리스틱이라 오탐이 있다. 특히 정규화본은 페이드와 패딩이 적용되므로, `RISK`가 있어도 자동 전사와 직접 청취에서 문장 끝이 보존되면 사용 가능하다.
- 1차 재생성: `python3 tts_clone.py regen --proj DIR --seg N --duration-multiplier 1.08`. 그래도 짧으면 `1.12`까지 올린다. 말이 너무 늘어지면 `1.05`로 낮춘다.
- 2차 재생성: 해당 문장을 더 짧게 쪼개거나 마지막 표현을 바꾼다. 예: `확인해주세요.`가 잘리면 `확인해 주세요.`처럼 띄어 쓰거나, `확인해주시면 됩니다.`처럼 종결을 바꾼다.
- `--gap`/무음 패딩은 끊김을 숨길 뿐 마지막 음절을 복구하지 못한다. 실제 끝음이 짧게 생성된 경우에는 `duration_multiplier` 또는 문장 재작성으로 다시 뽑는 것이 맞다.

## 생성 후 검증
- 한국어 생성 로그에서 `Language: ko`가 찍히는지 확인한다. `tts_clone.py --lang ko`는 내부에서 `mlx_audio.tts.generate --lang_code ko`로 전달되어야 한다.
- 긴 결과물이나 외부 공유용 음성은 `mlx_whisper <final.wav> --language ko`로 자동 전사를 뽑아 대본과 대조한다.
- `mlx_whisper`는 기본적으로 현재 폴더에 같은 이름의 `.txt`를 만들 수 있으므로, 임시 전사 파일은 산출물 폴더로 옮기거나 검증 후 정리한다.

## concat 함정
`ffmpeg -f concat` demuxer는 입력 포맷(코덱·SR·채널·sample_fmt)이 다르면 **첫 파일 뒤에서 조용히 멈춘다**(무음 파일 불일치로 N개 중 1개만 합쳐지는 사고). → 드라이버는 모든 세그먼트를 동일 포맷(24kHz/mono/`pcm_s16le`)으로 정규화한 뒤 concat한다. 직접 셸로 짤 때도 동일 포맷을 보장할 것. (zsh에서 `LINES=(...)` 배열 할당은 특수변수 충돌로 실패 — 다른 이름을 쓴다.)

## 튜닝 (mlx_audio.tts.generate 플래그)
전체 플래그는 `mlx_audio.tts.generate --help`. 자주 쓰는 것:
- 품질↑: `--ddpm_steps 30~50`(디퓨전 스텝, 느려짐).
- 청크 간 일관성↑: `--temperature` 낮추기, `--top_p`/`--top_k` 조이기(샘플링 변동 축소).
- 끝음/속도: `--duration_multiplier`(꼬리 여유, 단 발화 속도 변함), `--speed`.
- 드라이버 옵션: `--duration-multiplier`, `--speed`, `--ddpm-steps`, `--temperature`, `--top-p`, `--top-k`, `--repetition-penalty`를 `full`/`chunk`/`regen`에서 그대로 넘길 수 있다.

## 모드(음성 종류) & 대안 엔진
같은 `mlx_audio.tts.generate`로 다른 모델/모드를 쓴다 (`--model`로 교체):
- **Qwen3-TTS** (기본): `...-Base`(3초 클론) / `...-CustomVoice`(프리셋 보이스, `--voice Chelsie|Ethan|Vivian…`) / `...-VoiceDesign`(자연어 설계, `--instruct "차분한 30대 남성"`).
- **VoxCPM2** (OpenBMB): `mlx-community/VoxCPM2-8bit` 등. Apache 2.0(상업 OK)·48kHz·한국어 O. 같은 레퍼런스로 A/B 비교 가능.
- 참고: Voxtral(Mistral)은 오픈웨이트로는 커스텀 클론 불가(프리셋만)·한국어 미지원이라 로컬 한국어 클론엔 부적합.

## 산출물 레이아웃
```
~/.local/share/tts/voices/<name>/ref.wav  ref.txt   # 영구 보관함
/tmp/tts-XXXX/manifest.json  output.wav             # 휘발 프로젝트
/tmp/tts-XXXX/chunks/seg_NN_000.wav                 # 원본 청크
/tmp/tts-XXXX/chunks/norm_NN.wav                    # 페이드+패딩 적용본(concat 대상)
out/edit.wav                                        # --loudnorm-out 편집용 최종본(선택)
```
