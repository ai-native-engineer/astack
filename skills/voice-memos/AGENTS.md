# AGENTS.md

## Project Rules

- **이 디렉터리가 파이프라인 코드의 원본(single source of truth)이다.** launchd 워처 plist(`~/Library/LaunchAgents/com.user.voicememos-watcher.plist`)가 이곳의 `scripts/run.sh`를 real path로 직접 실행하므로, 스크립트 이동·이름 변경 시 plist 재지정 + `launchctl bootout/bootstrap`이 필요하다.
- 모든 파일은 UTF-8 인코딩으로 작성하고, 수정 후 `file -I`로 확인한다.
- Voice Memos 전사는 `apple-stt`(macOS SpeechAnalyzer, 음성 메모와 동일 엔진)로 오디오를 직접 전사한다. Apple 기본 전사(`tsrp` atom)나 UI 전사 버튼 트리거에 의존하지 않는다.
- `apple-stt`는 vocab을 `~/.config/apple-stt/vocab.txt`에서 자동 로드하지만, 이 프로젝트의 실제 vocab은 `~/.config/stt/vocab.txt`에 있으므로 `extract.py`가 `--vocab-file`로 명시 전달한다 (config.py `VOCAB_FILE`이 단일 소스).
- `summarize.py`는 claude-agent-sdk 의존이라 이 디렉터리의 uv venv로 실행한다(`uv run`). claude-agent-sdk에는 WebSearch 도구가 없다 — `allowed_tools=["WebSearch"]`를 주면 max_turns를 소진하고 빈 응답을 반환하므로 절대 추가하지 말 것.
- Voice Memos UI 자동화는 접근성 트리의 안정적인 식별자(`PlaybackView/TranscriptionButton`)를 우선 사용한다.

## Historical Notes

- 2026-06-11: 파이프라인 코드 원본을 `~/dev/3-tool/voice-memos`에서 이 스킬 디렉터리로 이전했다. 배경: 스킬에 남아 있던 파이프라인 사본(extract 등 4종)이 구버전(tsrp)으로 갈라져 문서와 불일치했고, 사용자가 원본을 스킬 쪽에 두기로 결정. 최신 스크립트(config/run.sh/transcribe_calls/check_fda/verify_fda 포함)를 가져오고 워처 plist를 이곳 `run.sh`로 재지정했다. `references/watcher.md`(워처 운영·FDA 진단) 신설, 에이닷 .m4a 자동 전사를 `call-recordings.md`에 반영. 옛 repo는 deprecated 안내만 남김.

- 2026-05-30: tsrp atom 파싱 + UI 전사 버튼 트리거 방식을 폐기하고 `apple-stt` 직접 전사로 전환했다. 사유: (1) tsrp는 Apple OS 백그라운드 전사가 끝나야 생겨서 `run.sh`에 `sleep 10` 타이밍 도박이 필요했고 긴 녹음은 누락될 수 있었다, (2) apple-stt는 오디오를 직접 전사해 길이·타이밍 무관하게 항상 결과가 나온다, (3) vocab(고유명사) 제어가 가능하다. `extract.py`를 apple-stt 호출로 재작성, `run.sh`의 `sleep 10` → `sleep 2`로 축소. tsrp/UI 트리거 스크립트(`trigger_tsrp.sh`, `transcribe_visible.swift`, `click_transcription.swift`, `stt_fallback.swift`)는 삭제하지 않고 폴백용으로 보관. 화자 분리 미지원은 그대로(회의는 Plaud 사용).
- 2026-04-08: 전사 기반 bulk rename를 실제로 돌리면서 `재개` / `완료`가 보이는 편집·녹음 계열 화면으로 진입할 수 있다는 실패 모드를 확인했고, `SKILL.md`의 rename 절차에 `RecordingsList`/제목 필드 재검증과 해당 화면 즉시 중단 규칙을 추가했다.
- 2026-04-08: Voice Memos 앱 표시 이름 변경 경로를 직접 검증했고, `RecordingsList` 행 선택 뒤 제목 `AXTextField`의 값을 설정하고 `Return`을 보내야 목록 이름까지 실제로 커밋된다는 점을 `SKILL.md`에 반영했다.
- 2026-04-08: `scripts/click_transcription.swift`와 `scripts/trigger_tsrp.sh`를 추가해 Voice Memos의 `전사문` 버튼을 UI 자동화로 눌러 Apple 원본 전사를 트리거할 수 있게 했다.
- 2026-04-08: `SKILL.md`에 Voice Memos 목록 순회, `전사문` 버튼 식별 기준, 스크롤 반복, 재추출 확인 절차를 추가해 AI가 문서만 보고도 Apple 전사 트리거를 수행할 수 있게 했다.
- 2026-04-08: `scripts/transcribe_visible.swift`를 추가해 현재 보이는 목록만 Swift 접근성으로 안전하게 전사하고, `오디오를 전사할 수 없음` 상태를 전사 불가로 감지하도록 보강했다.
- 2026-04-08: `SKILL.md`의 Apple 전사 섹션을 전면 보강해 `swift` 우선, `180초` 대기, `오디오를 전사할 수 없음`의 터미널 처리, 현재 보이는 목록 단위 처리, 스크롤 실패 시 중단 기준을 명시했다.
