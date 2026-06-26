# 전사 파이프라인 워처 (launchd)

새 녹음(Voice Memos·에이닷 통화)이 생기면 전사→요약→알림을 자동 실행하는 LaunchAgent. "전사가 안 됐어", "알림이 안 와", "워처 확인해줘" 요청 시 이 문서를 따른다. 파이프라인 코드 원본은 이 스킬의 `scripts/`다.

## 구성

- Label: `com.user.voicememos-watcher`
- plist: `~/Library/LaunchAgents/com.user.voicememos-watcher.plist`
- 실행: `/bin/bash ~/.claude/skills/voice-memos/scripts/run.sh` (plist는 symlink 아닌 real path 사용)
- WatchPaths (둘 중 하나에 파일이 생기면 트리거):
  - `~/Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings` (Voice Memos)
  - `~/Library/Mobile Documents/com~apple~CloudDocs/녹음` (에이닷 통화)
- 로그: `~/.voice-memos/logs/watcher.log` (**로컬**, 1,000줄 초과 시 최근 500줄만 유지)

**경로 분리 규칙 (중요)**: 전사 산출물(`transcripts/`·`corrections.json`)은 iCloud(`~/.voice-memos/`)에 두되, **로그와 plist의 `StandardOutPath`/`StandardErrorPath`, run.sh의 `LOG_DIR`은 반드시 로컬(`~/.voice-memos/logs/`)**이어야 한다. launchd는 iCloud Drive 동기화 폴더에 파일을 쓰지 못해, 로그를 거기 두면 잡이 `EX_CONFIG`로 실행조차 못 한다(진단 B).

## run.sh 단계

1. `extract.py --all` — 음성 메모 전사
2. `transcribe_calls.py` — 에이닷 통화 .m4a 전사
3. `summarize.py` — 요약·제목 생성 (`uv run`, `CLAUDECODE` unset)
4. `notify.py` — Discord/Telegram 알림 (`--skip-notify`로 스킵)

처리할 게 없으면 로그에 `변경 없음` 한 줄만 남는다. 단계 실패 시 `[ERROR]` 로그 + Telegram 에러 알림.

## 진단 절차

먼저 `launchctl print gui/$(id -u)/com.user.voicememos-watcher | grep -E "state|last exit"`와 `tail -30 ~/.voice-memos/logs/watcher.log`로 **워처는 도는데 처리를 못 하는지(A)** vs **아예 실행이 안 되는지(B)**를 가른다.

Telegram 에러 알림을 받은 경우는 전달된 로그의 **마지막 실패 단계**를 먼저 본다. `1/4 음성 메모 전사`에서 `0/N 처리됨`이나
`결과 없음(무음/인식 실패)`가 같이 보여도, `3/4 요약 생성`에 `Fatal error in message reader`가 있으면 전사 실패가 아니라 요약 단계가 원인이다.
이때 `scripts/summarize.py`의 모델이 `[1m]`로 돌아갔는지, claude CLI/SDK 호출이 바뀌었는지부터 확인한다.

### A. 워처는 도는데 전사가 안 됨 — FDA 부재

새 녹음을 해도 watcher.log에 `변경 없음`/extract `0/0 처리됨`만 반복. WatchPaths 트리거는 정상이나 run.sh의 python3가 TCC 보호 폴더(Recordings)를 0개로 본다(터미널/Claude 셸은 FDA가 있어 같은 스크립트가 정상). macOS 업데이트로 FDA가 리셋되면 재발.

해결: 시스템 설정 > 개인정보 보호 및 보안 > 전체 디스크 접근에 `/bin/bash`(ProgramArguments[0], TCC 책임 프로세스)와 `/opt/homebrew/bin/python3`(실제 접근자) **둘 다** 추가+토글 ON. 패널 바로 열기:

```bash
open "x-apple.systempreferences:com.apple.preference.security?Privacy_AllFiles"
```

검증: `bash ~/.claude/skills/voice-memos/scripts/verify_fda.sh` — 워처 plist를 안 건드리고 일회성 잡으로 `bash→python3` 체인을 재현해 폴더 개수만 센다(부작용 없음). `count>0`이면 성공.

### B. 워처가 아예 실행 안 됨 — 로그가 iCloud 경로 (EX_CONFIG)

`launchctl print`에 `last exit code = 78: EX_CONFIG`, kickstart해도 watcher.log에 새 줄이 안 찍히고 `runs`만 증가. 원인: plist `StandardOutPath`/`StandardErrorPath`(또는 run.sh `LOG_DIR`)가 iCloud(`Mobile Documents`) 경로다 → launchd가 못 써서 잡이 spawn 전에 죽는다. 해결: 위 **경로 분리 규칙**대로 로그 경로를 로컬 `~/.voice-memos/logs`로 되돌리고, plist 변경은 `bootout`→`bootstrap`으로 재로드(아래).

### 밀린 분량 처리

직접 `extract.py`를 돌리지 말고 **워처가 처리하게** `launchctl kickstart -k gui/$(id -u)/com.user.voicememos-watcher`. run.sh의 `extract.py --all`은 `--force`가 없어 기존 transcript는 스킵 → 중복 전사가 없다(summary도 처리 마커로 스킵). 알림 없이 돌리려면 `bash ~/.claude/skills/voice-memos/scripts/run.sh --skip-notify`.

## 재시작·상태 확인

```bash
launchctl print gui/$(id -u)/com.user.voicememos-watcher        # 상태 확인
launchctl bootout gui/$(id -u)/com.user.voicememos-watcher 2>/dev/null
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.user.voicememos-watcher.plist
launchctl kickstart -k gui/$(id -u)/com.user.voicememos-watcher  # 즉시 1회 실행
```
