---
name: kakaotalk
description: "macOS KakaoTalk chatroom read/search/send automation with shared communication rules before outbound messages. Use when user asks 카톡 보내줘, 카카오톡 메시지, 카톡 읽어줘, 채팅방 확인, 카톡방 찾아줘, 대화 내역, 카톡 검색, or send/read messages via KakaoTalk. Do NOT use for Slack, iMessage/SMS, Gmail/Google Chat, long-form writing, or message drafting without KakaoTalk execution."
---

# KakaoTalk CLI

macOS Accessibility API(atomacos)를 통해 카카오톡 메시지를 읽고 보내는 스킬.

**안전선 — 마우스 커서를 옮기지 않는다.** 합성 마우스 클릭(`cliclick`·AppleScript `click at`·Quartz/CGEvent)은 사용자가 컴퓨터를 쓰는 중에 실제 커서를 빼앗는다. UI 조작은 전부 접근성(`.Press()`/`AXUIElementPerformAction`·`AXFocused`)과 키보드(`key code`·클립보드 붙여넣기)·`Raise()`로만 한다.

## 메시지 작성 의존성

카카오톡으로 보낼 문구를 작성·수정·발송할 때는 transport 실행 전에 공통 커뮤니케이션 규칙을 먼저 읽는다.

1. `../communication/references/work-message-contract.md`
2. `../communication/references/style-profiles.md` (저장된 문체를 맞출 때만)
3. `../communication/references/message-templates.md` (요청·핸드오프·상태 공유일 때)
4. `../communication/references/channel-overlays/kakaotalk.md`

공통 스킬을 읽을 수 없으면 최소 계약만 따른다: 목적·수신자·요청/맥락/액션을 분리하고, 사용자가 승인한 본문은 임의로 재작성하지 않으며, 발송 전 채팅방과 최종 본문을 확인받는다.

이 스킬 디렉터리에서 아래 prefix를 사용한다.

```
uv run --project . python scripts/
```

---

## 메시지 발송 워크플로우

### Step 1: 채팅방 열고 대화 내역 읽기

```bash
{prefix}kakao_read.py "대상이름" --json
```

- 대상이 오픈채팅이면 먼저 아래 `오픈채팅 우회 절차`를 참고해 방을 연 뒤 읽기/발송 스크립트를 사용한다.

### Step 2: 맥락 파악 후 메시지 작성

- 배열 끝부분이 최신 메시지 (최근일수록 가치 높음)
- 최근 대화 주제와 자연스럽게 이어지도록 구성
- 위 `메시지 작성 의존성`의 공통 contract와 카카오톡 overlay를 적용

### Step 3: 사용자 확인 (필수)

텍스트로 메시지 내용을 보여준 후 사용자에게 확인:

```
**보낼 메시지:**
받는 사람: {채팅방}
---
{메시지 내용}
---
→ 사용자에게 "이 메시지를 보낼까요?"라고 확인
```

### Step 4: 발송

```bash
{prefix}kakao_send.py "채팅방이름" "메시지"
```

- 사용자 요청 없이 서명이나 에이전트 표기를 추가하지 않는다.
- 발송 직후 `kakao_read.py --limit N`에 방금 보낸 메시지가 안 보여도 즉시 실패로 단정하지 않는다. 이 스크립트는 현재 보이는 메시지 범위를 읽기 때문에 뷰포트가 최신 위치가 아니면 직전 발송분이 빠질 수 있다. `kakao_send.py`의 `"success": true`를 1차 확인값으로 본다.

---

## 메시지 읽기 전용 워크플로우

```bash
{prefix}kakao_read.py "대상이름" --json
```

읽은 후 요약: 최근 대화 주제, 답장 필요 여부.

---

## 권한 문제 진단 (필수)

다음 신호가 보이면 방 이름 문제가 아니라 macOS 접근성 권한 문제다.

- `atomacos`에서 `app.windows()`가 `0`을 반환함
- `kakao_read.py --search ... --debug` 로그에 `main window NOT found after retries`가 찍힘
- `osascript`에서 `보조 접근이 허용되지 않습니다` 오류가 발생함

해결 절차:

1. System Settings > Privacy & Security > Accessibility에서 현재 터미널 앱/Codex 실행 앱을 허용
2. 필요하면 카카오톡과 터미널을 모두 다시 실행
3. 아래 두 명령으로 권한이 실제 반영됐는지 확인

```bash
osascript -e 'tell application "System Events" to tell process "KakaoTalk" to get name of every window'
# 기대값: 카카오톡

uv run --project . python - <<'PY'
import atomacos
app = atomacos.getAppRefByBundleId('com.kakao.KakaoTalkMac')
print('windows', len(app.windows()))
PY
# 기대값: windows 1 이상
```

---

## 채팅방 못 찾았을 때 — 자가 피드백 (필수)

스크립트가 키워드 분리 재시도 + 열린 창 검증을 자동 수행함.
그래도 실패하면 아래 단계를 직접 수행:

1. **`--search "키워드"` 사용** — 가장 고유한 키워드 하나로 검색 결과 확인
2. **키워드 변형** — 순서 다름("A X B" → "B X A"), 구분자 다름("X" vs "_"), 약칭 가능성
3. **`--list` 사용** — 전체 채팅 목록에서 유사한 이름 찾기
4. **엉뚱한 방 진입 금지** — 스크립트가 열린 창 제목을 검증하여 불일치 시 자동 닫음

---

## 오픈채팅 우회 절차

기본 `kakao_read.py --search` / `--list`는 현재 선택된 탭 기준으로만 보일 수 있다. 일반 채팅 탭에 머문 상태에서는 오픈채팅 방 이름이 검색되지 않을 수 있으므로 아래 순서로 우회한다.

### 1. 카카오톡 메인 창 확인

```bash
open -a KakaoTalk

uv run --project . python - <<'PY'
import atomacos
app = atomacos.getAppRefByBundleId('com.kakao.KakaoTalkMac')
print('windows', len(app.windows()))
for i, win in enumerate(app.windows(), 1):
    print(i, getattr(win, 'AXTitle', None))
PY
```

### 2. 오픈채팅 버튼 존재 확인

```bash
osascript -e 'tell application "System Events" to tell process "KakaoTalk" to get description of every button of window 1'
# 기대값에 "오픈채팅" 포함
```

### 3. 필요하면 오픈채팅 탭을 접근성 Press로 전환

오픈채팅 버튼을 **접근성 AXPress로 누른다 — 마우스 커서를 옮기지 않는다.** 합성 마우스 클릭(Quartz/CGEvent·`cliclick`·`click at`)은 사용자가 컴퓨터를 쓰는 중에 실제 커서를 빼앗으므로 이 스킬에서는 쓰지 않는다. `atomacos`의 `.Press()`가 안 먹으면 raw `AXUIElementPerformAction`으로 폴백한다.

```bash
uv run --project . python - <<'PY'
import atomacos
from ApplicationServices import AXUIElementPerformAction

app = atomacos.getAppRefByBundleId('com.kakao.KakaoTalkMac')
win = app.windows()[0]

for child in getattr(win, 'AXChildren', []) or []:
    if getattr(child, 'AXRole', None) == 'AXButton' and getattr(child, 'AXDescription', None) == '오픈채팅':
        try:
            child.Press()                                  # 접근성 Press (커서 안 움직임)
        except Exception:
            AXUIElementPerformAction(child.ref, 'AXPress')  # raw AXPress 폴백
        print('pressed 오픈채팅')
        break
PY
```

### 4. 오픈채팅 목록에서 실제 행 텍스트 확인

```bash
uv run --project . python - <<'PY'
import subprocess
for i in range(1, 21):
    script = (
        'tell application "System Events" to tell process "KakaoTalk" '
        f'to get value of every static text of every UI element of row {i} '
        'of table 1 of scroll area 1 of window 1'
    )
    out = subprocess.run(['osascript', '-e', script], capture_output=True, text=True).stdout.strip()
    print(f'{i}\t{out}')
PY
```

예시 출력:

```text
3	프로젝트 공지, 1676, 11:32
6	프로젝트 공지/운영자, 3월 23일
```

### 5. 원하는 행 선택 후 Enter로 입장

```bash
osascript \
  -e 'tell application "System Events" to tell process "KakaoTalk" to select row 3 of table 1 of scroll area 1 of window 1' \
  -e 'tell application "System Events" to key code 36'
```

입장 후에는 일반 채팅과 동일하게 처리한다.

```bash
{prefix}kakao_read.py "프로젝트 공지" --json
{prefix}kakao_send.py "프로젝트 공지" "메시지"
```

### 6. 같은 이름의 일반 채팅/오픈채팅이 함께 있을 때

- `프로젝트 공지`와 `프로젝트 공지/운영자`처럼 유사한 이름이 같이 보일 수 있으니, 행 텍스트 전체를 읽고 정확한 row index를 고른다.
- `--search`가 0건이어도 오픈채팅 목록 행에는 존재할 수 있으므로, 검색 실패만으로 방이 없다고 결론내리지 않는다.

---

전체 플래그는 `kakao_read.py --help` / `kakao_send.py --help` 참조.

---

## 요구사항

1. **의존성**: 이 스킬 디렉터리에서 `uv sync`
2. **Accessibility 권한**: System Settings > Privacy & Security > Accessibility에서 Terminal 허용
3. **카카오톡 실행 중**: macOS용 카카오톡 앱
