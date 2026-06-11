---
argument-hint: "[query]"
name: voice-memos
description: >
  Apple Voice Memos·에이닷 통화 녹음·Apple Notes·Caret MCP를 통합해 음성 메모와
  개인 노트를 추출, 교정, 검색, 요약, 전문 읽기, 알림 전송한다. 전사 자동화
  워처(launchd)의 진단·재시작도 다룬다.
  "음성 메모", "voice memo", "전사", "메모 검색", "메모 찾아줘", "녹음 내용",
  "메모 추출", "메모 교정", "전문 가져와줘", "메모 내용 읽어줘",
  "텔레그램으로 보내줘", "최근 메모", "오늘 메모", "전사가 안 됐어",
  "알림이 안 와" 요청에 사용.
---

# Voice Memos

음성 메모와 개인 노트를 한 곳에서 다룬다. 네 종류의 소스를 통합하며, 각 소스의 처리 규칙·자동화·필드 경로는 `references/` 아래 별도 문서에 분리되어 있다. 이 SKILL.md는 인덱스 + 공통 워크플로우 역할이다.

전사→요약→알림 파이프라인 코드의 원본도 이 스킬의 `scripts/`다. launchd 워처가 새 녹음을 감지해 `scripts/run.sh`를 자동 실행한다 — 구성·진단·재시작은 `references/watcher.md`.

## 데이터 소스 인덱스

| 라벨 | 소스 | 처리 | 상세 |
|------|------|------|------|
| `[음성 메모]` | Apple Voice Memos (m4a/qta) | 추출·요약·알림 풀 파이프라인 (워처 자동) | `references/voice-memos.md` |
| `[에이닷]` | 에이닷 통화 녹음 (.txt + .m4a) | .txt는 search 인덱싱만(원본 보존), .m4a는 워처가 자동 전사 | `references/call-recordings.md` |
| `[메모]` | Apple Notes (NoteStore.sqlite) | search 인덱싱만 (mode=ro 직접 쿼리). 잠긴 메모는 미리보기에 안내 표시 | `references/apple-notes.md` |
| `[Caret]` | Caret MCP (외부 지식·노트) | 요약 사전 보강 + 검색 병렬 호출 | `references/caret.md` |

세 종류의 raw 소스는 `search.py`가 통합 인덱싱한다. Caret은 MCP 도구라 `search.py` 안에서는 호출 불가능하고, LLM이 워크플로우 차원에서 같이 호출한다.

## 경로

- 산출물(transcript/summary): `~/.voice-memos/transcripts/YYYYMMDD/HHMMSS/transcript.md` + `summary.md`
- 단어장: `~/.voice-memos/corrections.json`
- 워처 로그: `~/.voice-memos/logs/watcher.log`
- 스크립트: `~/.claude/skills/voice-memos/scripts/`
- 소스별 상세 문서: `~/.claude/skills/voice-memos/references/`

## 공통 검색 명령

`search.py`는 세 종류의 raw 소스를 동시에 인덱싱한다. 라벨로 출처를 구분한다.

```bash
python3 ~/.claude/skills/voice-memos/scripts/search.py                       # 최근 10개
python3 ~/.claude/skills/voice-memos/scripts/search.py --recent 5
python3 ~/.claude/skills/voice-memos/scripts/search.py --date 2026-05-07     # YYYY-MM-DD, YYYY-MM, YYYY
python3 ~/.claude/skills/voice-memos/scripts/search.py --date today          # today, yesterday, this-week, this-month
python3 ~/.claude/skills/voice-memos/scripts/search.py --keyword "프롬프트"
python3 ~/.claude/skills/voice-memos/scripts/search.py --dates                # 녹음/메모 있는 날짜 목록
python3 ~/.claude/skills/voice-memos/scripts/search.py --recent 5 --no-preview --count
```

## 워크플로우

사용자 요청 패턴별 진입 절차. 자세한 명령·옵션은 해당 references 파일에서.

### "음성 메모 처리해줘"

워처가 보통 이미 자동 처리했다 — `search.py --recent`로 transcript/summary 존재부터 확인한다. 수동 처리가 필요할 때:

1. `bash ~/.claude/skills/voice-memos/scripts/run.sh --skip-notify` — 전사(음성 메모+통화)→요약 일괄. 개별 실행은 `references/voice-memos.md` §1·§3
2. LLM이 직접 요약할 때: **Caret MCP 사전 보강** — `caret_search_knowledge` / `caret_search_notes` 병렬 호출 후 `caret_get_note`로 관련 노트 전문 확보 (`references/caret.md`) → `references/voice-memos.md` §3 템플릿으로 `summary.md` 저장

### "전사만 해줘"

`python3 ~/.claude/skills/voice-memos/scripts/extract.py` — `apple-stt`(macOS SpeechAnalyzer)로 오디오 직접 전사. 옵션은 `references/voice-memos.md` §1.

### "메모 찾아줘" / "최근 메모" / "X 관련 메모"

세 채널을 병렬로 호출하고 결과를 합쳐 라벨별로 제시한다.

1. `search.py --keyword <키워드>` 또는 `--date <날짜>` 또는 `--recent <N>` 실행
2. **같은 메시지에서** `caret_search_knowledge` + `caret_search_notes` 병렬 호출 (`references/caret.md` §2)
3. 결과를 라벨별로 묶어서 보여줌:
   - `[음성 메모]` — Apple Voice Memos
   - `[에이닷]` — 에이닷 통화 녹음
   - `[메모]` — Apple Notes (잠긴 메모는 미리보기 자리에 안내 표시)
   - `[Caret]` — Caret 지식 / 노트
4. 사용자가 특정 항목을 선택하면 Read(파일) 또는 `caret_get_note`(Caret)로 본문을 가져온다

### "전문 가져와줘" / "메모 내용 읽어줘"

전사본은 한 줄이 길어 Read 도구의 토큰 제한에 걸린다. `references/voice-memos.md` §4의 fold + Read 병렬 패턴을 따른다. 단:

- 통화 녹음 .txt는 줄이 짧아 보통 Read 직접 가능 (`references/call-recordings.md`)
- Apple Notes는 가상 Path(`apple-note:<Z_PK>`)라 Read 불가. `search.py`가 미리보기를 보여주므로 보통 충분. 전문이 필요하면 `scripts/vm_notes.py`의 `note_body()`로 읽거나 sqlite 직접 쿼리 (`references/apple-notes.md`).

### "텔레그램으로 보내줘" / "디스코드로 보내줘"

명시 요청에만 반응. `references/voice-memos.md` §5.

```bash
python3 ~/.claude/skills/voice-memos/scripts/notify.py --file <path.md>
python3 ~/.claude/skills/voice-memos/scripts/notify.py
```

### "전사가 안 됐어" / "알림이 안 와" / 워처 점검

launchd 워처 구성·로그 판독·FDA 권한 진단·재시작 절차는 `references/watcher.md`.

### "음성 메모 제목 바꿔줘" / "앱 안 이름 바꿔줘"

Voice Memos 앱 안에서 보이는 표시 이름만 변경 (원본 .m4a 파일명은 그대로). `references/voice-memos.md` §7의 AX 접근성 절차를 따른다.

## 공통 원칙

- **응답 언어**: 한국어. 영어·일본어 원문 인용은 원문 유지.
- **화자 분리 한계**: Voice Memos 전사본에는 화자 라벨이 없다. 사용자의 발언·의사결정·심리를 추론·요약하기 전에 어느 발언이 본인 것인지 사용자에게 먼저 확인한다. 사용자 호칭(본인 이름·닉네임)이 등장해도 그 문장이 사용자의 **발화**인지 사용자**에 대한 언급**인지 구분한다. 상세 절차는 `references/voice-memos.md` §3.
- **iCloud 원본 보존**: 통화 녹음(.txt/.m4a)과 Apple Notes는 원본을 변형하지 않는다 (산출물은 `~/.voice-memos/`에만, Notes는 `mode=ro` 직접 쿼리).
- **Caret 사전 보강 필수**: 요약·교정에 들어가기 전에 Caret MCP 검색을 건너뛰지 않는다. 관련 지식이 없는 경우에만 생략 가능. 검색 결과의 `summary` 필드만으로 판단하지 말고 `caret_get_note`로 전문을 확보한다.

## scripts/ 인덱스

| 스크립트 | 역할 | 상세 |
|----------|------|------|
| `run.sh` | 워처 진입점: 전사→통화 전사→요약→알림 순차 실행 | `references/watcher.md` |
| `extract.py` | apple-stt로 음성 메모 전사 → transcript.md | `references/voice-memos.md` §1 |
| `transcribe_calls.py` | 에이닷 통화 .m4a 전사 | `references/call-recordings.md` |
| `correct.py` | 단어장 일괄 치환 (수동 도구, 파이프라인 미포함) | `references/voice-memos.md` §2 |
| `summarize.py` | claude-agent-sdk 요약·제목 생성 | `references/voice-memos.md` §3 |
| `notify.py` | Discord/Telegram 전송 | `references/voice-memos.md` §5 |
| `config.py` | 파이프라인 공통 경로 정의 | — |
| `search.py` | 3개 raw 소스 통합 검색 | 본 문서 "공통 검색 명령" |
| `vm_notes.py` | Apple Notes 저수준 모듈 (search.py가 사용) | `references/apple-notes.md` |
| `caret_to_md.py` | Caret get_note 결과 (>10K) JSON→md | `references/caret.md` |
| `check_fda.py`, `verify_fda.sh` | 워처 FDA 권한 진단 | `references/watcher.md` |
| `trigger_tsrp.sh`, `transcribe_visible.swift`, `click_transcription.swift`, `stt_fallback.swift` | (폐기, 폴백 보관) 구 tsrp/UI 전사 | `references/voice-memos.md` §6 |
