# 전사 파이프라인 워처 (launchd)

새 녹음(Voice Memos·에이닷 통화)이 생기면 전사→요약→알림을 자동 실행하는 LaunchAgent. "전사가 안 됐어", "알림이 안 와", "워처 확인해줘" 요청 시 이 문서를 따른다. 파이프라인 코드 원본은 이 스킬의 `scripts/`다.

## 구성

- Label: `com.user.voicememos-watcher`
- plist: `~/Library/LaunchAgents/com.user.voicememos-watcher.plist`
- 실행: `/bin/bash <스킬 실제 경로>/scripts/run.sh` (plist는 symlink 아닌 real path 사용)
- WatchPaths (둘 중 하나에 파일이 생기면 트리거):
  - `~/Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings` (Voice Memos)
  - `~/Library/Mobile Documents/com~apple~CloudDocs/녹음` (에이닷 통화)
- 로그: `~/.voice-memos/logs/watcher.log` (1,000줄 초과 시 최근 500줄만 유지)

## run.sh 단계

1. `extract.py --all` — 음성 메모 전사
2. `transcribe_calls.py` — 에이닷 통화 .m4a 전사
3. `summarize.py` — 요약·제목 생성 (`uv run`, `CLAUDECODE` unset)
4. `notify.py` — Discord/Telegram 알림 (`--skip-notify`로 스킵)

처리할 게 없으면 로그에 `변경 없음` 한 줄만 남는다. 단계 실패 시 `[ERROR]` 로그 + Telegram 에러 알림.

## 진단 절차 — "전사가 안 됐어"

1. `tail -30 ~/.voice-memos/logs/watcher.log`로 최근 실행 확인.
2. 새 녹음을 했는데도 `변경 없음` 또는 extract `0/0 처리됨`만 반복되면 **FDA(전체 디스크 접근) 문제**다. launchd 프로세스는 터미널 셸과 달리 FDA가 없으면 TCC 보호 폴더(Recordings)가 0개로 보인다. macOS 업데이트로 FDA가 리셋되면 재발한다.
3. 해결: 시스템 설정 > 개인정보 보호 및 보안 > 전체 디스크 접근에 `/bin/bash`(ProgramArguments[0], TCC 책임 프로세스)와 `/opt/homebrew/bin/python3`(실제 폴더 접근자) **둘 다** 추가하고 토글 ON. 패널 바로 열기:
   ```bash
   open "x-apple.systempreferences:com.apple.preference.security?Privacy_AllFiles"
   ```
4. 검증: `~/.claude/skills/voice-memos/scripts/verify_fda.sh` — 기존 워처 plist를 건드리지 않고 일회성 잡으로 `bash→python3` 체인을 재현해 폴더 파일 개수만 센다(전사·알림 부작용 없음). `count>0`이면 성공.
5. 밀린 분량 수동 처리: `bash ~/.claude/skills/voice-memos/scripts/run.sh --skip-notify`

## 재시작·상태 확인

```bash
launchctl print gui/$(id -u)/com.user.voicememos-watcher        # 상태 확인
launchctl bootout gui/$(id -u)/com.user.voicememos-watcher 2>/dev/null
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.user.voicememos-watcher.plist
launchctl kickstart -k gui/$(id -u)/com.user.voicememos-watcher  # 즉시 1회 실행
```
