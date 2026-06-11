# Voice Memos 소스 처리

Apple Voice Memos 앱이 만든 `.m4a`/`.qta` 녹음 파일을 `apple-stt`(macOS SpeechAnalyzer)로 전사하고, 요약·제목 생성·알림까지 다루는 풀 파이프라인. 이 스킬에서 가장 비중이 큰 소스다.

평소에는 launchd 워처가 새 녹음을 감지해 아래 §1·§3·§5를 자동 실행한다(`watcher.md`). 아래 명령들은 수동 재실행·부분 실행용.

## 위치

- 원본: `~/Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings/*.{m4a,qta}`
- 산출물: `~/.voice-memos/transcripts/YYYYMMDD/HHMMSS/transcript.md` + `summary.md`
- 단어장: `~/.voice-memos/corrections.json`

전사본 한 줄이 수만 자로 매우 길어서 Read 도구로 직접 열면 토큰 제한에 걸린다. 전문 읽기는 아래 "전문 읽기" 절차를 따른다.

## 1. 전사 추출 (extract)

`apple-stt`(macOS SpeechAnalyzer)로 오디오를 직접 전사해 `YYYYMMDD/HHMMSS/transcript.md`로 저장. Apple 기본 전사(tsrp atom)나 UI 트리거에 의존하지 않는다.

```bash
# 새 파일만 추출
python3 ~/.claude/skills/voice-memos/scripts/extract.py

# 전체 재추출
python3 ~/.claude/skills/voice-memos/scripts/extract.py --all --force

# 특정 파일만
python3 ~/.claude/skills/voice-memos/scripts/extract.py --file <path.m4a>
```

- `wait_until_settled()`로 파일 크기가 안정될 때까지 대기 → 녹음 중 미완성 파일 전사 방지
- `.qta`(Apple Watch·타기기 동기화 = QuickTime 컨테이너)는 `ffmpeg`로 오디오만 m4a 추출 후 전사
- 파일명은 정규식으로 `YYYYMMDD HHMMSS` 추출 → 앱에서 한글로 이름 바꾼 녹음도 폴더가 안 깨짐
- vocab은 `--vocab-file`로 `~/.config/stt/vocab.txt` 전달

## 2. 교정 (correct) — 수동 도구

`corrections.json` 단어장으로 음성인식 오류를 일괄 치환하는 수동 도구. **`run.sh` 자동 파이프라인에는 포함되지 않는다** (교정은 §3 summarize가 LLM으로 함께 수행). 단어장 기반 일괄 치환이 따로 필요할 때만 실행한다.

```bash
python3 ~/.claude/skills/voice-memos/scripts/correct.py
python3 ~/.claude/skills/voice-memos/scripts/correct.py --all --force
```

새 단어를 추가할 때는 `~/.voice-memos/corrections.json`을 직접 편집:

```json
{ "잘못된단어": "올바른단어" }
```

## 3. 요약 (summarize)

전사본을 claude-agent-sdk(`claude-sonnet-4-6[1m]`)로 요약. 결과는 같은 디렉터리의 `summary.md`에 저장. 요약과 함께 `## 제목`을 생성해 `transcript.md`의 frontmatter(`- **제목**:`)와 H1 헤딩에 주입한다(멱등).

주의: claude-agent-sdk에는 WebSearch 도구가 없다. `allowed_tools=["WebSearch"]`를 주면 max_turns를 소진하고 빈 응답을 반환하므로 추가하지 말 것.

claude-agent-sdk 의존이라 스킬 디렉터리의 uv venv로 실행하고, Claude Code 세션 안에서는 `CLAUDECODE`를 unset한다 (run.sh와 동일).

```bash
cd ~/.claude/skills/voice-memos && unset CLAUDECODE
uv run python scripts/summarize.py            # 미요약만
uv run python scripts/summarize.py --all --force
uv run python scripts/summarize.py --recent 5
uv run python scripts/summarize.py --file <path/transcript.md>
```

또는 LLM이 직접 전사본을 읽고 아래 템플릿으로 요약을 만들어 `summary.md`에 저장한다.

```markdown
## 교정 사항

| 원문 | 교정 | 근거 |
|------|------|------|
| (오류) | (교정) | (문맥/검색 근거) |

## 요약

### 핵심 내용
- (3-5개 문장, 구체적 수치/이름/날짜 포함)

### 주요 논의 사항
- (주제별로 구조화)

### 결정 사항
- (누가, 왜, 무엇을 결정)

### 액션 아이템
- [ ] 할 일 — 담당자 (기한)
```

### 요약 규칙

- 전사본 유형(독백·1:1·다자 회의)과 전체 맥락을 먼저 파악
- 확신이 높을 때만 교정. 애매하면 원문 유지. 고유명사는 vocab 사전·문맥으로 검증 (WebSearch 사용 불가)
- 전사본에 없는 내용 추가 금지(hallucination 금지). 의미 있는 디테일은 보존
- 구어체 → 문어체로 다듬되 의미·뉘앙스 보존. 불필요한 반복·필러만 제거
- 해당 내용이 없는 섹션은 생략

### [필수] 화자 분리 한계

Voice Memos 전사본에는 화자 라벨이 없다. 다자 대화·미팅을 요약할 때:

1. 전사본에 등장하는 이름·닉네임(참석자들의 이름 등)을 기계적으로 특정 발화자에게 매핑하지 않는다.
2. 사용자의 관점·의견·결정을 추론·요약하기 전에 "이 녹음에서 당신은 어느 발언을 했는지" 사용자에게 먼저 묻는다. 특히 다음 상황은 필수:
   - 사용자의 의사결정·심리·평가를 요약할 때
   - 특정 인물의 발언을 사용자에게 귀속시킬 때
   - 발언 주체에 따라 결론이 달라질 때
3. 사용자 호칭(본인 이름·닉네임)이 전사본에 등장하면 사용자를 지칭할 가능성이 높지만, 그 문장이 사용자의 **발화**인지 사용자**에 대한 언급**인지 반드시 구분한다.
4. 추측으로 화자를 특정해 요약하지 말고, 불확실하면 묻고 답을 받은 뒤 요약을 확정한다.

### [필수] Caret MCP 사전 보강

요약/교정에 들어가기 전에 반드시 Caret MCP로 외부 컨텍스트를 모은다. 절차는 `references/caret.md`.

## 4. 전문 읽기 (read)

전사본은 줄 수는 적지만 한 줄이 수만 자라 Read 도구의 10K 토큰 제한을 초과한다. "전문 가져와줘"·"메모 내용 읽어줘" 요청 시:

```bash
# 1) 200자 단위로 분할
fold -s -w 200 ~/.voice-memos/transcripts/YYYYMMDD/HHMMSS/transcript.md > /tmp/transcript_folded.md

# 2) 줄 수 확인
wc -l /tmp/transcript_folded.md
```

3) Read 도구로 60줄씩 병렬 읽기 (350줄 기준 예시):

```
Read /tmp/transcript_folded.md offset=1   limit=60
Read /tmp/transcript_folded.md offset=61  limit=60
Read /tmp/transcript_folded.md offset=121 limit=60
Read /tmp/transcript_folded.md offset=181 limit=60
Read /tmp/transcript_folded.md offset=241 limit=60
Read /tmp/transcript_folded.md offset=301 limit=50
```

- 가능한 한 병렬 호출
- `cat`/Bash 출력도 같은 토큰 제한이라 사용하지 않는다
- 임시 파일은 별도 삭제 불필요

## 5. 알림 전송 (notify)

명시 요청 시에만 실행. `.env`에 Discord/Telegram 설정 필요.

```bash
python3 ~/.claude/skills/voice-memos/scripts/notify.py --file <path.md>
python3 ~/.claude/skills/voice-memos/scripts/notify.py   # 미전송 일괄
```

## 6. (폐기) Apple 전사 트리거 (trigger-tsrp)

> 2026-05-30 폐기. 현재는 §1 `apple-stt`로 직접 전사하므로 이 절차는 불필요하다. `trigger_tsrp.sh`/`transcribe_visible.swift`/`stt_fallback.swift`는 폴백용으로만 보관한다. 아래는 구버전 기록.

(구버전) Voice Memos가 녹음을 연 뒤 상단 `전사문` 버튼을 눌러야 Apple 원본 전사(`tsrp`)가 생기던 경우.

```bash
# 현재 선택된 녹음 하나만 처리
~/.claude/skills/voice-memos/scripts/trigger_tsrp.sh

# 현재 보이는 목록의 미전사 항목을 안전 처리. 결과: transcribed / unavailable / timeout
~/.claude/skills/voice-memos/scripts/transcribe_visible.swift --timeout 180
```

규칙:

- `swift` 기반 접근성 자동화를 `osascript`보다 우선 사용. `osascript`는 창을 강제로 띄울 때만.
- 버튼 클릭은 접근성 식별자 `PlaybackView/TranscriptionButton`만 사용한다. `RecordingView/TranscriptionButton`이 보이거나 `완료`/`일시 정지` 같은 녹음 UI가 보이면 자동화를 즉시 중단한다(녹음 중이라는 의미).
- 목록 설명에 `전사문을 사용할 수 있음`이 있으면 이미 완료된 항목이라 다시 누르지 않는다.
- Apple 전사 대기 시간은 기본 `180초`. 장시간 녹음은 실제로 그 정도 걸린다.
- `오디오를 전사할 수 없음`이 보이면 Apple 전사 불가 상태(`unavailable`). 같은 항목을 반복 클릭하지 않는다. 사용자가 결과를 꼭 원하면 `scripts/stt_fallback.swift`로 넘긴다.
- `timeout`과 `unavailable`은 다르다. `timeout`은 아직 처리 중일 수 있어 한두 번 재시도 가능, `unavailable`은 같은 방식으로는 영영 안 된다.
- 일반적인 `AXButton` 전체 탐색이나 `description=전사문`만 본 채로 누르면 잘못된 버튼(녹음 버튼 등)을 누를 위험이 있다. 반드시 식별자 기반.

자동화 흐름:

1. Voice Memos가 꺼져 있거나 창이 없으면 `swift`/AppKit으로 먼저 앱을 실행한다(`NSWorkspace.shared.openApplication(...)`). 접근성 트리에 창이 안 잡힐 때만 `osascript -e 'tell application id "com.apple.VoiceMemos" to activate'`.
2. 단일 녹음 처리: `trigger_tsrp.sh`. 현재 보이는 목록 일괄: `transcribe_visible.swift --timeout 180`.
3. 여러 메모를 훑어야 하면 왼쪽 목록 `AXButton`들을 순회한다. 항목 설명은 `녹음 25, 어제` 또는 `JAX 소통, 2026. 4. 1., 전사문을 사용할 수 있음` 같은 형태.
4. 각 항목을 클릭해 상세를 연 뒤 상단 툴바의 `전사문` 버튼만 누른다. 다른 툴바 버튼·하단 컨트롤은 절대 누르지 않는다.
5. 버튼을 누른 뒤 최대 `180초` 폴링. 다음 중 하나면 종료:
   - 목록 설명에 `전사문을 사용할 수 있음`이 생김 → `transcribed`
   - 상세 패널에 전사 텍스트가 채워짐 → `transcribed`
   - 상세 패널에 `오디오를 전사할 수 없음` → `unavailable`
   - `180초` 초과 → `timeout`
6. 미전사 항목 전체를 돌릴 때는 "현재 보이는 목록"만 처리하고, 페이지가 실제로 바뀌었는지(보이는 항목 set 비교) 확인한 뒤 다음 페이지로 넘어간다. Voice Memos 목록은 가상화돼 있어 스크롤 명령이 항상 먹지는 않는다. 안 바뀌면 그 자리에서 멈추고 사용자에게 스크롤 요청.
7. 처리 후 `extract.py --file <m4a|qta>`로 tsrp가 실제로 생겼는지 확인.

문제 대응:

- 같은 항목에 대해 `전사문` 버튼을 반복 클릭하지 않는다. `unavailable`이 떴다면 `stt_fallback.swift`로 우회.
- 앱이 켜졌는데 창이 0개면 접근성 자동화 대상이 없다. Swift `NSRunningApplication.activate(options: [.activateAllWindows])`로 먼저 창을 띄운다.
- 보이는 미전사 항목이 0인데 작업이 끝나지 않았다면 자동 스크롤이 실패한 것. 사용자가 수동 스크롤한 뒤 `transcribe_visible.swift` 재실행.
- 접근성 버튼 탐색이 불안정할 때 일반 버튼 탐색으로 범위를 넓히지 않는다. 위험.

## 7. 앱 표시 이름 변경 (rename-title)

Voice Memos 앱 안에서 보이는 메모 제목만 바꾼다. 이 작업은 앱 표시 이름만 변경하며 원본 `.m4a` 파일명은 그대로다.

접근성 경로:

- 왼쪽 목록은 `AXIdentifier=RecordingsList` 아래의 `AXButton` 행
- 행 `description`에 `녹음 2, 어제, 전사문을 사용할 수 있음` 같은 문자열
- 항목을 선택하면 상세 패널에 제목용 `AXTextField`가 나타남
- 같은 화면의 검색 필드도 `AXTextField`이고 값이 `.`인 경우가 있어 제목 필드로 착각하면 안 됨

절차:

1. Voice Memos를 전면에 띄우고 녹음 UI가 아닌지 확인. `RecordingView/TranscriptionButton`·`완료`/`일시 정지`가 보이면 즉시 중단.
2. `RecordingsList`에서 대상 행 버튼 선택.
3. 창 전체에서 `AXTextField`를 찾되 값이 비어 있지 않고 `.`이 아닌 필드를 제목 필드로 사용.
4. `kAXValueAttribute`에 새 제목을 설정.
5. `Return` 키(`CGKeyCode 36`)로 편집 확정. 안 보내면 목록 이름이 커밋되지 않을 수 있다.
6. 목록 행 `description` prefix가 새 제목으로 바뀌었는지 검증.

규칙:

- 메뉴 탐색·더블클릭보다 `행 선택 → 제목 필드 값 설정 → Return` 경로 우선.
- 현재 보이는 목록만 대상. 안 보이는 항목까지 억지로 찾지 않는다.
- 테스트성 변경은 즉시 원복.
- `Return`은 제목 필드가 실제로 잡힌 상태에서만. 이전 항목 값이 남아 있거나 아직 갱신되지 않았으면 기다린다.
- 각 항목 처리 전후로 `RecordingsList`와 제목 `AXTextField`가 살아 있는지 다시 확인. 하나라도 사라지면 중단.
- 아래 상태면 즉시 중단(녹음 편집 UI일 가능성): 하단에 `재개`+`완료`가 함께 보임, 큰 파형 편집 화면, `RecordingsList`가 사라지고 단일 녹음 편집 UI만 보임. `Return`이나 추가 클릭을 보내지 않는다.

전사 기반 일괄 이름 변경:

1. transcript/summary가 있는 항목만 대상.
2. 사용자가 명시적으로 컨벤션 통일을 원할 때만 `YYMMDD-주제` 형식 적용.
3. 날짜 접두사는 transcript의 `녹음일시` 기준 `YYMMDD`.
4. 본문 2-4개 핵심 키워드로 짧게: `260407-AI-API-서빙-플랫폼`.
5. 항목별로 `선택 → 제목 필드가 해당 항목명으로 바뀐 것 확인 → 값 설정 → Return → 목록 prefix 검증` 순서를 반복.
