---
argument-hint: "[query]"
name: voice-memos
description: "Use for: Apple 음성 메모, 에이닷 통화 녹음, Apple Notes, Tiro 회의 노트를 찾아 전사, 교정, 요약하고 알림과 워처를 진단한다. 일반 음성 파일 전사는 stt."
---

# Voice Memos

음성 메모와 개인 노트를 한 곳에서 다룬다. 로컬 세 소스와 Tiro 회의 노트를 통합하며, 각 소스의 처리 규칙·자동화·필드 경로는 `references/` 아래 별도 문서에 분리되어 있다. 이 SKILL.md는 인덱스 + 공통 워크플로우 역할이다.

전사 -> 검토 대기/요약 -> 알림 파이프라인 코드의 원본도 이 스킬의 `scripts/`다. launchd 워처가 새 녹음을 감지해 `scripts/run.sh`를 자동 실행한다. 설치 기본값은 `legacy`이며 strict `shadow`·`review`는 Gate 1 통과 전까지 활성화하지 않는다. 구성, 진단, 재시작은 `references/watcher.md`를 읽는다.

## 데이터 소스 인덱스

| 라벨 | 소스 | 처리 | 상세 |
|------|------|------|------|
| `[음성 메모]` | Apple Voice Memos (m4a/qta) | 추출·요약·알림 풀 파이프라인 (워처 자동) | `references/voice-memos.md` |
| `[에이닷]` | 에이닷 통화 녹음 (.txt + .m4a) | .txt는 search 인덱싱만(원본 보존), .m4a는 워처가 자동 전사 | `references/call-recordings.md` |
| `[메모]` | Apple Notes (NoteStore.sqlite) | search 인덱싱만 (mode=ro 직접 쿼리). 잠긴 메모는 미리보기에 안내 표시 | `references/apple-notes.md` |
| `[티로]` | Tiro 회의 노트 (클라우드 CLI) | 검색·읽기만. 워처/전사는 타지 않는다 | `references/tiro.md` |

로컬 세 소스는 `search.py`가 인덱싱한다. Tiro는 `scripts/tiro_notes.py`로 따로 조회한 뒤 같은 응답에서 라벨로 붙인다.

## 경로

- 데이터 루트: `VOICE_MEMOS_DATA_DIR`. 미설정 시 `~/Library/Mobile Documents/com~apple~CloudDocs/voice-memos`
- Apple Voice Memos `legacy` 산출물: 데이터 루트의 `transcripts/YYYYMMDD/HHMMSS/transcript.md` + `summary.md`
- Apple Voice Memos strict 산출물: `transcripts/YYYYMMDD/HHMMSS-<recording-id-8>/` 아래 `analysis.json`, `raw.md`, `run.json`; `review`만 `transcript.md`를 추가하고 finalizable일 때 `summary.md`를 만든다.
- 에이닷 `.m4a` 산출물: `legacy`는 원본 옆 `<원본>.transcript.md`/`<원본>.summary.md`; strict는 `<원본>.analysis.json`/`<원본>.run.json`을 추가하고 `review`만 transcript를 쓴다.
- 녹음별 strict context: `~/.config/voice-memos/recordings/<audio-sha256>.json`
- 검토 결정/저장 용어: 로컬 `~/.voice-memos/state/review.sqlite3`
- 워처 로그: `~/.voice-memos/logs/watcher.log`

모든 상대 명령은 현재 로드된 `voice-memos` 스킬 루트를 작업 디렉터리로 삼아 실행한다.

## 공통 검색 명령

`search.py`는 로컬 세 소스를 인덱싱한다. 라벨로 출처를 구분한다. Tiro는 아래 워크플로의 `tiro_notes.py`다.

```bash
python3 scripts/search.py                       # 최근 10개
python3 scripts/search.py --recent 5
python3 scripts/search.py --date 2025-01-15     # YYYY-MM-DD, YYYY-MM, YYYY
python3 scripts/search.py --date today          # today, yesterday, this-week, this-month
python3 scripts/search.py --date 목요일          # 요일(thu, 목요일): 오늘 포함 가장 최근 그 요일
python3 scripts/search.py --keyword "프롬프트"
python3 scripts/search.py --dates                # 녹음/메모 있는 날짜 목록
python3 scripts/search.py --recent 5 --no-preview --count
```

- 음성 메모는 녹음 폴더마다 `transcript.md`, 없으면 화자 분리 결과 `diarized.md`를 보여 준다.
- 산출물이 없는 원본 녹음도 `미전사`로 앱 제목, 길이, 원본 경로와 함께 나온다. 화자 분리나 전사는 그 원본 경로로 실행한다.
- `미전사`가 여러 건 쌓였으면 워처가 멈춘 것이므로 `references/watcher.md`로 진단한다.
- 키워드 검색은 전사본만 읽는다. iCloud에만 있는 파일은 읽으면 멈추므로 빼고 개수를 경고한다.
- 사용자가 "하나 더 있다"고 정정하면 `search.py --recent N --no-preview`와 `python3 scripts/tiro_notes.py list --limit N --no-preview`를 함께 본다. Tiro가 비면 `references/tiro.md` 실패 표를 본다. 한쪽 결과만 보고 "없다"고 단정하지 않는다.

미리보기 출력 중 iCloud 파일이 `Resource deadlock avoided`를 내면 `--no-preview`로 목록만 확인한다. 본문이 필요하면 해당 파일을 `brctl download`로 내려받고 `/tmp`로 복사한 뒤 읽는다(자세한 절차는 `references/voice-memos.md`의 전문 읽기 절).

## 워크플로우

사용자 요청 패턴별 진입 절차. 자세한 명령·옵션은 해당 references 파일에서.

### "음성 메모 처리해줘"

워처가 보통 이미 기본 `legacy`로 자동 처리했다. `search.py --recent`로 transcript/summary 존재부터 확인한다. 수동 처리가 필요할 때:

1. `bash scripts/run.sh --skip-notify` - 음성 메모와 통화 녹음을 순차 처리한다. 개별 실행은 `references/voice-memos.md` 1절, 3절을 읽는다.
2. LLM이 직접 요약할 때는 `references/voice-memos.md` 3절 템플릿으로 `summary.md`를 저장한다.

### "화자 분리해줘" / "누가 말한 건지 알고 싶어"

`search.py`가 보여 준 원본 경로로 실행한다. 전사본이 없는 녹음도 된다.

```bash
bash scripts/diarize.sh <audio.m4a> [transcript_dir|-] [start] [end]
```

- 결과 폴더를 생략하거나 `-`로 두면 파이프라인이 그 녹음에 쓰는 transcript 폴더에 둔다. 구간만 자를 때는 `-`를 넣고 `start`, `end`를 준다.
- 결과 폴더에는 `diarized.md`와 확인 화면이 읽는 `transcript.json`, `diar.rttm`, `speakers.json`, `names.json`, `run.json`이 함께 생긴다. 다시 실행하면 이 파일들을 덮어쓴다.
- 실행 전에 걸릴 시간을 `stt` 스킬 기준으로 알린다. 여러 녹음은 메모리 때문에 하나씩 차례로 돌린다.
- 글과 화자는 `stt` 스킬의 화자 분리 모드(MOSS)가 함께 만들므로, `diarized.md`의 글은 Apple 전사본과 다를 수 있다. 턴 묶기, 빈 곳(`**[gap]**`), 확인 화면은 `stt` 스킬의 `references/diarization.md`를 따른다.

### "전사만 해줘"

`python3 scripts/extract.py` — `apple-stt`(macOS SpeechAnalyzer)로 오디오 직접 전사. 옵션은 `references/voice-memos.md` 1절.

### "메모 찾아줘" / "최근 메모" / "X 관련 메모"

로컬 `search.py`와 Tiro `tiro_notes.py`를 함께 돌리고 결과를 라벨별로 제시한다.

1. 요청에 맞춰 `search.py --keyword <키워드>`, `--date <날짜>`, `--recent <N>` 중 하나를 실행한다.
2. 같은 조건으로 `python3 scripts/tiro_notes.py list` 또는 `search`를 실행한다. 옵션·인증은 `references/tiro.md`.
3. 결과를 라벨별로 묶어서 보여준다.
   - `[음성 메모]` — Apple Voice Memos
   - `[에이닷]` — 에이닷 통화 녹음
   - `[메모]` — Apple Notes (잠긴 메모는 미리보기 자리에 안내 표시)
   - `[티로]` — Tiro 회의 노트
4. 사용자가 특정 항목을 선택하면 로컬 파일은 Read로, Apple Notes는 `scripts/vm_notes.py`의 `note_body()`로, Tiro는 `tiro_notes.py transcript <guid>`가 저장한 경로를 접어서 읽는다.

### "이 날짜 녹음 다시 확인해줘" / "voice-memos 재검토해줘"

특정 날짜를 다시 볼 때는 하나만 찍지 말고 같은 날짜의 전체 후보를 먼저 확인한다.

1. `search.py --date <날짜> --no-preview --count`로 후보 수를 확인한 뒤 `--no-preview` 목록을 본다.
2. 날짜 결과 전체를 후보로 두고, 요청 키워드와 바로 맞는 항목만 고르지 않는다.
3. 각 후보의 `summary.md`를 먼저 읽고, 사용자 발화·결정·맥락 판단이 필요하면 같은 폴더의 `transcript.md`까지 읽는다.
4. 답변에는 포함·제외·보류한 후보와 파일 경로, 판단 근거를 짧게 남긴다.

### "전문 가져와줘" / "메모 내용 읽어줘"

전사본은 한 줄이 길어 Read 도구의 토큰 제한에 걸린다. `references/voice-memos.md` 4절의 fold + Read 병렬 패턴을 따른다. 단:

- 통화 녹음 .txt는 줄이 짧아 보통 Read 직접 가능 (`references/call-recordings.md`)
- Apple Notes는 가상 Path(`apple-note:<Z_PK>`)라 Read 불가. `search.py`가 미리보기를 보여주므로 보통 충분. 전문이 필요하면 `scripts/vm_notes.py`의 `note_body()`로 읽는다 — NoteStore.sqlite를 raw로 직접 쿼리하면 본문이 zlib+protobuf로 압축돼 있어 Traceback난다(`references/apple-notes.md`).

### "텔레그램으로 보내줘" / "디스코드로 보내줘"

명시 요청에만 반응. `references/voice-memos.md` 5절.

```bash
python3 scripts/notify.py --file <path.md>
python3 scripts/notify.py
```

### "전사가 안 됐어" / "알림이 안 와" / 워처 점검

launchd 워처 구성·로그 판독·FDA 권한 진단·재시작 절차는 `references/watcher.md`.
Telegram 에러 알림을 붙여주면 마지막 `[ERROR]` 단계부터 본다. 전사 단계의 `RecordingsUnreadable`은 워처의 FDA가 빠진 것이다(`references/watcher.md` A). `processed=0`은 새 대상 없음일 수 있으므로, 요약 단계에 오류가 있으면 먼저 model/SDK/CLI 경로를 확인한다.

### "음성 메모 제목 바꿔줘" / "앱 안 이름 바꿔줘"

Voice Memos 앱 안에서 보이는 표시 이름만 변경 (원본 .m4a 파일명은 그대로). `references/voice-memos.md` 7절의 AX 접근성 절차를 따른다.

### "녹음 합쳐줘" / "이어붙여줘"

앱에는 합치기가 없다. 원본은 덮어쓰지 않고 복사본을 이어 새 파일을 만든다. 절차·함정은 `references/voice-memos.md` 8절. 일반 mp4/오디오 이어붙이기는 `ffmpeg` 스킬.

## 공통 원칙

- **응답 언어**: 한국어. 영어·일본어 원문 인용은 원문 유지.
- **화자 분리 한계**: Voice Memos 전사본에는 화자 라벨이 없다. 사용자의 발언·의사결정·심리를 추론·요약하기 전에 어느 발언이 본인 것인지 사용자에게 먼저 확인한다. 알려진 사용자 호칭이 등장해도 그 문장이 사용자의 **발화**인지 사용자**에 대한 언급**인지 구분한다. 상세 절차는 `references/voice-memos.md` 3절.
- **원본 보존**: Voice Memos 원본, 에이닷 통화 녹음(.txt/.m4a), Apple Notes, Tiro 클라우드 노트는 변형하지 않는다. 파생 위치는 소스별로 다르다. Voice Memos 산출물은 `voice-memos/transcripts/`, 에이닷 `.m4a` 산출물은 원본 옆 `.analysis.json`/`.run.json`/`.transcript.md`/`.summary.md`, Notes는 `mode=ro` 직접 쿼리, Tiro 전사는 `~/.voice-memos/tiro/`. 합친 뒤 소스 녹음을 목록에서 빼라는 명시 요청만 예외이며 절차는 `references/voice-memos.md` 8절.

## scripts/ 인덱스

| 스크립트 | 역할 | 상세 |
|----------|------|------|
| `run.sh` | 워처 진입점: 전사 -> 통화 전사 -> 요약 -> 알림. review pending은 요약·최종 알림을 보류 | `references/watcher.md` |
| `extract.py` | apple-stt로 음성 메모 evidence/transcript 생성 | `references/voice-memos.md` 1절 |
| `transcribe_calls.py` | 에이닷 통화 .m4a 전사 | `references/call-recordings.md` |
| `correct.py` | 전역 치환을 거부하고 review 명령을 안내하는 호환 shim | `references/voice-memos.md` 2절 |
| `review.py` | context metadata, 불확실 구간 검토, SQLite decision/term event | `references/voice-memos.md` 2절 |
| `summarize.py` | claude-agent-sdk 요약·제목 생성 | `references/voice-memos.md` 3절 |
| `notify.py` | Discord/Telegram 전송 | `references/voice-memos.md` 5절 |
| `config.py` | 파이프라인 공통 경로 정의 | — |
| `search.py` | 로컬 3개 소스 통합 검색 | 본 문서 "공통 검색 명령" |
| `vm_notes.py` | Apple Notes 저수준 모듈 (search.py가 사용) | `references/apple-notes.md` |
| `tiro_notes.py` | Tiro 회의 노트 검색·전사 파일 저장 | `references/tiro.md` |
| `check_fda.py`, `verify_fda.sh` | 워처 FDA 권한 진단 | `references/watcher.md` |
| `trigger_tsrp.sh`, `transcribe_visible.swift`, `click_transcription.swift`, `stt_fallback.swift` | 비실행 legacy reference. runner/문서 명령에서 호출 금지 | `references/voice-memos.md` 6절 |
