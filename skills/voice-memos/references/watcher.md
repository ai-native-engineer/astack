# 전사 파이프라인 워처 (launchd)

새 녹음(Voice Memos·에이닷 통화)이 생기면 전사 -> 요약 -> 알림을 자동 실행하는 LaunchAgent. 설치 기본값은 `VOICE_MEMOS_STT_MODE=legacy`다. "전사가 안 됐어", "알림이 안 와", "워처 확인해줘" 요청 시 이 문서를 따른다. 파이프라인 코드 원본은 이 스킬의 `scripts/`다.

## 구성

- Label과 plist 이름은 설치 환경에서 정한다. 진단 전에 기존 plist와 Label을 찾는다.
- 실행: `/bin/bash` + 현재 로드된 스킬 루트의 `scripts/run.sh` real path
- WatchPaths (둘 중 하나에 파일이 생기면 트리거):
  - `~/Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings` (Voice Memos)
  - `~/Library/Mobile Documents/com~apple~CloudDocs/녹음` (에이닷 통화)
- 로그: `~/.voice-memos/logs/watcher.log` (**로컬**, 1,000줄 초과 시 최근 500줄만 유지)
- durable queue scaffold: `~/.voice-memos/run-queue/`. plist의 `QueueDirectories` 등록은 Gate 1과 retry/crash E2E가 끝난 뒤에만 한다. 현재 설치 plist는 변경하지 않는다.

```bash
WATCHER_PLIST="$(find "$HOME/Library/LaunchAgents" -maxdepth 1 -type f -name '*.plist' -exec grep -l 'voice-memos/scripts/run.sh' {} + | head -n 1)"
test -n "$WATCHER_PLIST" || { echo "voice-memos watcher plist not found" >&2; exit 1; }
WATCHER_LABEL="$(/usr/libexec/PlistBuddy -c 'Print :Label' "$WATCHER_PLIST")"
```

**경로 분리 규칙 (중요)**: 전사 산출물은 `VOICE_MEMOS_DATA_DIR`에 둔다. 미설정 기본값은 `~/Library/Mobile Documents/com~apple~CloudDocs/voice-memos/`다. strict context는 `~/.config/voice-memos/recordings/`, 검토 DB·lock·queue·로그는 로컬 `~/.voice-memos/`에 둔다. 알림 자격증명은 `~/.config/voice-memos/.env`(`VOICE_MEMOS_CONFIG_FILE`로 재지정 가능)다. plist의 `StandardOutPath`/`StandardErrorPath`와 run.sh의 `LOG_DIR`을 iCloud Drive에 두면 잡이 `EX_CONFIG`로 실행조차 못 한다(진단 B). 데이터 루트나 설정 파일을 바꾸면 plist의 `EnvironmentVariables`에도 같은 값을 설정한다.

## run.sh 단계

1. `extract.py --all` — 음성 메모 전사
2. `transcribe_calls.py` — 에이닷 통화 .m4a 전사
3. `summarize.py` — 요약·제목 생성 (`uv run`, `CLAUDECODE` unset)
4. `notify.py` — Discord/Telegram 알림 (`--skip-notify`로 스킵)

`extract.py --all`은 Voice Memos DB에서 최근 삭제된 항목과 로컬 오디오가 아직 내려오지 않은 iCloud 동기화 대기 항목을 제외한다. 동기화가 끝나 `ZLOCALDURATION`이 생기면 자동으로 다시 처리 대상이 된다.

`review_pending`이면 3단계가 Claude 호출을 건너뛴다. 새 summary가 없으므로 4단계도 transcript 전문을 provisional 본문으로 보내지 않는다. `privacy: local`도 Claude 호출을 건너뛴다. 처리할 게 없으면 로그에 `no changes` 한 줄만 남는다. 단계 실패 시 redacted `[ERROR]` 로그 + Telegram 에러 알림을 보낸다.

### 모드와 활성화 상태

- `legacy`(기본): 기존 `HHMMSS/transcript.md`를 유지하고 요약·알림까지 실행한다.
- `shadow`: strict `analysis.json`/`run.json` evidence만 만들며 transcript를 덮어쓰지 않는다. Voice Memo에는 `raw.md`도 보존한다. analysis 미지원·검증 실패 시 legacy fallback 없이 실패한다.
- `review`: content hash 기반 `HHMMSS-<id8>` artifact와 review state를 만든다. 후보가 있으면 `review_pending`으로 멈춘다.
- `shadow`·`review`는 Gate 1 미통과 상태라 설치 launchd에서 활성화하지 않는다. 수동 검증이 아닌데 plist에 `VOICE_MEMOS_STT_MODE`가 있으면 제거해 기본 `legacy`로 되돌린다.
- `QueueDirectories`도 아직 설치하지 않는다. persistent failure 재실행과 review 종료 후 `RecordingBusy` handoff가 E2E로 닫히기 전에는 운영 계약이 아니다.

run.sh는 boot identity + PID start identity를 검증하는 단일 전역 lock을 사용한다. contender는 실패하지 않고 pending marker를 남기며, owner는 현재 pass 뒤 queue를 drain한다. stale lock은 owner identity가 맞지 않을 때만 복구한다.

## 진단 절차

먼저 `launchctl print "gui/$(id -u)/$WATCHER_LABEL" | grep -E "state|last exit"`와 `tail -30 ~/.voice-memos/logs/watcher.log`로 **워처는 도는데 처리를 못 하는지(A)** vs **아예 실행이 안 되는지(B)**를 가른다.

Telegram 에러 알림을 받은 경우는 전달된 로그의 **마지막 실패 단계**를 먼저 본다. `1/4 voice memo transcription`의 `processed=0`만 보고 전사 실패로 단정하지 않는다. `3/4 summary`에 `Fatal error in message reader`가 있으면 요약 단계가 원인이다.
이때 `scripts/summarize.py`의 model, claude CLI/SDK 인증, `tools=[]` 옵션이 바뀌었는지부터 확인한다.

### A. 워처는 도는데 전사가 안 됨 — FDA 부재

새 녹음을 해도 watcher.log에 `no changes`/extract `processed=0`만 반복한다. WatchPaths 트리거는 정상이나 run.sh의 python3가 TCC 보호 폴더(Recordings)를 0개로 본다(터미널/Claude 셸은 FDA가 있어 같은 스크립트가 정상). macOS 업데이트로 FDA가 리셋되면 재발.

해결: 시스템 설정 > 개인정보 보호 및 보안 > 전체 디스크 접근에 `/bin/bash`(ProgramArguments[0], TCC 책임 프로세스)와 `command -v "${VOICE_MEMOS_PYTHON:-python3}"`가 출력한 실제 Python 실행 파일 **둘 다** 추가+토글 ON. 패널 바로 열기:

```bash
open "x-apple.systempreferences:com.apple.preference.security?Privacy_AllFiles"
```

검증: `bash scripts/verify_fda.sh` — 워처 plist를 안 건드리고 일회성 잡으로 `bash→python3` 체인을 재현해 폴더 개수만 센다(부작용 없음). `count>0`이면 성공.

### B. 워처가 아예 실행 안 됨 — 로그가 iCloud 경로 (EX_CONFIG)

`launchctl print`에 `last exit code = 78: EX_CONFIG`, kickstart해도 watcher.log에 새 줄이 안 찍히고 `runs`만 증가. 원인: plist `StandardOutPath`/`StandardErrorPath`(또는 run.sh `LOG_DIR`)가 iCloud(`Mobile Documents`) 경로다 → launchd가 못 써서 잡이 spawn 전에 죽는다. 해결: 위 **경로 분리 규칙**대로 로그 경로를 로컬 `~/.voice-memos/logs`로 되돌리고, plist 변경은 `bootout`→`bootstrap`으로 재로드(아래).

### 밀린 분량 처리

직접 `extract.py`를 돌리지 말고 **워처가 처리하게** `launchctl kickstart -k "gui/$(id -u)/$WATCHER_LABEL"`. 기본 `legacy`는 기존 transcript를, strict 모드는 source/engine/context fingerprint가 맞는 evidence를 스킵한다. 알림 없이 돌리려면 `bash scripts/run.sh --skip-notify`.

## 재시작·상태 확인

```bash
launchctl print "gui/$(id -u)/$WATCHER_LABEL"        # 상태 확인
launchctl bootout "gui/$(id -u)/$WATCHER_LABEL" 2>/dev/null
launchctl bootstrap "gui/$(id -u)" "$WATCHER_PLIST"
launchctl kickstart -k "gui/$(id -u)/$WATCHER_LABEL" # 즉시 1회 실행
```
