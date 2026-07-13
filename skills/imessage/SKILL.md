---
argument-hint: "[search|read|recent|send] [contact] [message]"
name: imessage
description: "macOS iMessage/SMS/RCS read/search/send automation without MCP, using readonly chat.db for lookup and Messages.app for sending. Use when user asks 아이메시지, iMessage, 문자 검색, 메시지 읽어, 최근 메시지, 누구랑 대화 찾아줘, 문자 보내, iMessage send, or chat.db. Do NOT use for KakaoTalk, Slack, Gmail/Google Chat, voice memos/call recordings, or generic message writing without iMessage execution."
allowed-tools: Bash
---

# iMessage (MCP-free)

macOS Messages를 MCP 서버 없이 다룬다. 상시 폴링 프로세스도, `claude --channels` 플래그도 필요 없다.

- **읽기·검색**: `~/Library/Messages/chat.db`를 readonly SQLite로 직접 조회. 최신 macOS가 본문을 넣는 `attributedBody`(typedstream)도 디코딩한다.
- **이름 ↔ 번호**: 연락처(`AddressBook-v22.abcddb`)를 조회해 "홍길동" 같은 이름으로 바로 검색·전송한다.
- **전송**: `osascript`로 Messages.app에 발신 (창 안 띄우고 백그라운드). chat.db에 직접 쓰지 않는다 — DB INSERT는 실제 전송이 안 되고 DB만 손상시킨다.

## 요건 (한 번만)

1. **전체 디스크 접근(FDA)** — chat.db는 TCC 보호. 시스템 설정 → 개인정보 보호 및 보안 → 전체 디스크 접근 → 터미널(또는 호출하는 앱) 추가. 없으면 `read`/`search`가 권한 에러로 종료.
2. **Automation 권한** — 첫 `send` 때 "Terminal이 Messages를 제어" 프롬프트 1회. 허용하면 이후 무프롬프트.

## 사용법

스크립트: `scripts/imsg.py` (Python stdlib만, 설치 의존성 0).

```bash
PY=/opt/homebrew/bin/python3
SK="$HOME/.claude/skills/imessage/scripts/imsg.py"

# 연락처/본문 키워드 검색 → 이름·번호·매칭 메시지
"$PY" "$SK" search 홍길동

# 특정 상대와의 대화 읽기 (이름·번호·이메일 모두 가능)
"$PY" "$SK" read 홍길동 --limit 30
"$PY" "$SK" read +821012345678
"$PY" "$SK" read someone@icloud.com

# 최근 대화방 목록
"$PY" "$SK" recent --limit 20

# 전송 — 기본은 DRY-RUN(미리보기). 실제 발송은 --yes
"$PY" "$SK" send 홍길동 "홍길동님, 최종본 전달드립니다."          # 미리보기만
"$PY" "$SK" send 홍길동 "홍길동님, 최종본 전달드립니다." --yes     # 실제 발송
```

## 전송 안전 규칙 (에이전트용)

- **`send --yes`는 사용자 명시 승인 없이 실행 금지.** 먼저 `--yes` 없이 돌려 받는 사람·chat guid·본문을 미리보기로 보여주고, 사용자가 확인하면 그때 `--yes`로 발송한다.
- 보낼 문구는 사용자가 준 그대로. 서명("Sent by Claude" 등) 자동 추가 안 함.
- 받는 사람이 의도와 맞는지(동명이인·잘못된 번호) 미리보기에서 반드시 확인.

## 한계

- **본문 키워드 검색은 `text` 컬럼만** 매칭한다. 최신 메시지는 본문이 `attributedBody`(BLOB)라 키워드로 안 걸릴 수 있다 — 그땐 상대를 `read`로 직접 열어 훑는다.
- **전송은 텍스트만.** 첨부·tapback·편집·스레드 답장은 Apple 비공개 API 영역이라 osascript로 안 된다.
- 기존 1:1 대화가 없는 새 상대에게는 guid 전송이 안 될 수 있다 — Messages.app에서 먼저 한 번 보내 대화를 만든 뒤 사용.

## 출처

[anthropics/claude-plugins-official — external_plugins/imessage](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/imessage) (Apache-2.0)를 참고했다. 원본은 `chat.db`를 1초마다 폴링하는 **MCP 채널 서버**(인바운드 자동응답 봇)다. 이 스킬은 거기서 MCP 의존성을 걷어내고 읽기·검색·전송만 남긴 **on-demand CLI**로 재구성한 것이다.

- `attributedBody`(typedstream) 디코딩과 osascript 발신 스크립트는 원본 `server.ts`를 참고했다.
- 단, 원본의 길이 파서(`0x81`→1바이트, `0x82`→2바이트)는 255바이트 넘는 한글 본문에서 잘려, 정확한 인코딩인 `0x81`→2바이트 / `0x82`→4바이트로 정정했다.
