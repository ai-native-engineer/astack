---
argument-hint: "[query]"
name: voice-memos
description: "Apple Voice Memos, 에이닷 통화 녹음, Apple Notes, Caret MCP 개인 노트를 추출, 전사, 교정, 검색, 요약, 전문 읽기, 알림 전송, launchd watcher 진단/재시작으로 처리. Use when user asks 음성 메모, voice memo, 전사, 녹음 내용, 메모 찾아줘, 최근/오늘 메모, 전문 가져와줘, 텔레그램으로 보내줘, 전사가 안 됐어, 알림이 안 와. Do NOT use for YouTube 자막, 회의록 작성 only from text, 일반 파일 검색, or non-personal audio production."
---

# Voice Memos

음성 메모와 개인 노트를 한 곳에서 다룬다. 네 종류의 소스를 통합하며, 각 소스의 처리 규칙·자동화·필드 경로는 `references/` 아래 별도 문서에 분리되어 있다. 이 SKILL.md는 인덱스 + 공통 워크플로우 역할이다.

전사 -> 검토 대기/요약 -> 알림 파이프라인 코드의 원본도 이 스킬의 `scripts/`다. launchd 워처가 새 녹음을 감지해 `scripts/run.sh`를 자동 실행한다. 설치 기본값은 `legacy`이며 strict `shadow`·`review`는 Gate 1 통과 전까지 활성화하지 않는다. 구성, 진단, 재시작은 `references/watcher.md`를 읽는다.

## 데이터 소스 인덱스

| 라벨 | 소스 | 처리 | 상세 |
|------|------|------|------|
| `[음성 메모]` | Apple Voice Memos (m4a/qta) | 추출·요약·알림 풀 파이프라인 (워처 자동) | `references/voice-memos.md` |
| `[에이닷]` | 에이닷 통화 녹음 (.txt + .m4a) | .txt는 search 인덱싱만(원본 보존), .m4a는 워처가 자동 전사 | `references/call-recordings.md` |
| `[메모]` | Apple Notes (NoteStore.sqlite) | search 인덱싱만 (mode=ro 직접 쿼리). 잠긴 메모는 미리보기에 안내 표시 | `references/apple-notes.md` |
| `[Caret]` | Caret MCP (외부 지식·노트) | 요약 사전 보강 + 검색 병렬 호출 | `references/caret.md` |

세 종류의 raw 소스는 `search.py`가 통합 인덱싱한다. Caret은 MCP 도구라 `search.py` 안에서는 호출 불가능하고, LLM이 워크플로우 차원에서 같이 호출한다.

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

`search.py`는 세 종류의 raw 소스를 동시에 인덱싱한다. 라벨로 출처를 구분한다.

```bash
python3 scripts/search.py                       # 최근 10개
python3 scripts/search.py --recent 5
python3 scripts/search.py --date 2025-01-15     # YYYY-MM-DD, YYYY-MM, YYYY
python3 scripts/search.py --date today          # today, yesterday, this-week, this-month
python3 scripts/search.py --keyword "프롬프트"
python3 scripts/search.py --dates                # 녹음/메모 있는 날짜 목록
python3 scripts/search.py --recent 5 --no-preview --count
```

`search.py`는 **이미 전사/인덱싱된 산출물 기준**이다. "최근 N건 요약"에서 사용자가 "하나 더 있다"고 정정하거나 앱에는 보이는데 검색 결과가 부족하면, 먼저 `search.py --recent N --no-preview`로 전사 산출물 상태를 확인한 뒤 `extract.py --all` / `verify_fda.sh`로 원본 접근·워처 권한 문제를 진단한다. 전사 산출물만 보고 "없다"고 단정하지 않는다.

미리보기 출력 중 iCloud 파일이 `Resource deadlock avoided`를 내면 `--no-preview`로 목록만 확인한다. 본문이 필요하면 해당 파일을 `brctl download`로 내려받고 `/tmp`로 복사한 뒤 읽는다(자세한 절차는 `references/voice-memos.md`의 전문 읽기 절).

## 워크플로우

사용자 요청 패턴별 진입 절차. 자세한 명령·옵션은 해당 references 파일에서.

### "음성 메모 처리해줘"

워처가 보통 이미 기본 `legacy`로 자동 처리했다. `search.py --recent`로 transcript/summary 존재부터 확인한다. 수동 처리가 필요할 때:

1. `bash scripts/run.sh --skip-notify` - 음성 메모와 통화 녹음을 순차 처리한다. 개별 실행은 `references/voice-memos.md` 1절, 3절을 읽는다.
2. LLM이 직접 요약할 때는 `caret_search_knowledge` / `caret_search_notes`를 병렬 호출하고 `caret_get_note`로 관련 노트 전문을 확보한 뒤 `references/voice-memos.md` 3절 템플릿으로 `summary.md`를 저장한다.

### "화자 분리해줘" / "누가 말한 건지 알고 싶어"

해당 음성 메모의 transcript 디렉토리를 확인한 뒤 실행한다.

```bash
bash scripts/diarize.sh <audio.m4a> <transcript_dir> [start] [end]
```

출력은 `transcript_dir/diarized.md`다. Apple 텍스트가 정본이고 Argmax는 `diarize`만 실행한다. 여러 화자가 한 Apple 범위에 겹치면 `mixed`로 둔다.

### "전사만 해줘"

`python3 scripts/extract.py` — `apple-stt`(macOS SpeechAnalyzer)로 오디오 직접 전사. 옵션은 `references/voice-memos.md` 1절.

### "메모 찾아줘" / "최근 메모" / "X 관련 메모"

세 채널을 병렬로 호출하고 결과를 합쳐 라벨별로 제시한다.

1. `search.py --keyword <키워드>` 또는 `--date <날짜>` 또는 `--recent <N>` 실행
2. **같은 메시지에서** `caret_search_knowledge` + `caret_search_notes` 병렬 호출 (`references/caret.md` 2절)
3. 결과를 라벨별로 묶어서 보여줌:
   - `[음성 메모]` — Apple Voice Memos
   - `[에이닷]` — 에이닷 통화 녹음
   - `[메모]` — Apple Notes (잠긴 메모는 미리보기 자리에 안내 표시)
   - `[Caret]` — Caret 지식 / 노트
4. 사용자가 특정 항목을 선택하면 Read(파일) 또는 `caret_get_note`(Caret)로 본문을 가져온다

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
Telegram 에러 알림을 붙여주면 마지막 `[ERROR]` 단계부터 본다. 전사 단계의 `processed=0`은 새 대상 없음일 수 있으므로, 요약 단계에 오류가 있으면 먼저 model/SDK/CLI 경로를 확인한다.

### "음성 메모 제목 바꿔줘" / "앱 안 이름 바꿔줘"

Voice Memos 앱 안에서 보이는 표시 이름만 변경 (원본 .m4a 파일명은 그대로). `references/voice-memos.md` 7절의 AX 접근성 절차를 따른다.

## 공통 원칙

- **응답 언어**: 한국어. 영어·일본어 원문 인용은 원문 유지.
- **화자 분리 한계**: Voice Memos 전사본에는 화자 라벨이 없다. 사용자의 발언·의사결정·심리를 추론·요약하기 전에 어느 발언이 본인 것인지 사용자에게 먼저 확인한다. 알려진 사용자 호칭이 등장해도 그 문장이 사용자의 **발화**인지 사용자**에 대한 언급**인지 구분한다. 상세 절차는 `references/voice-memos.md` 3절.
- **원본 보존**: Voice Memos 원본, 에이닷 통화 녹음(.txt/.m4a), Apple Notes는 변형하지 않는다. 파생 위치는 소스별로 다르다. Voice Memos 산출물은 `voice-memos/transcripts/`, 에이닷 `.m4a` 산출물은 원본 옆 `.analysis.json`/`.run.json`/`.transcript.md`/`.summary.md`, Notes는 `mode=ro` 직접 쿼리.
- **Caret 사전 보강 필수**: LLM이 채팅에서 직접 요약·검토할 때 Caret MCP 검색을 건너뛰지 않는다. 자동 `summarize.py`는 Caret을 호출하지 않는다. 관련 지식이 없는 경우에만 생략 가능하며, 검색 결과의 `summary` 필드만으로 판단하지 말고 `caret_get_note`로 전문을 확보한다.

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
| `search.py` | 3개 raw 소스 통합 검색 | 본 문서 "공통 검색 명령" |
| `vm_notes.py` | Apple Notes 저수준 모듈 (search.py가 사용) | `references/apple-notes.md` |
| `caret_to_md.py` | Caret get_note 결과 (>10K) JSON -> md | `references/caret.md` |
| `check_fda.py`, `verify_fda.sh` | 워처 FDA 권한 진단 | `references/watcher.md` |
| `trigger_tsrp.sh`, `transcribe_visible.swift`, `click_transcription.swift`, `stt_fallback.swift` | 비실행 legacy reference. runner/문서 명령에서 호출 금지 | `references/voice-memos.md` 6절 |
