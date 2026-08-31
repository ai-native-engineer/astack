---
name: kakaotalk
description: "macOS KakaoTalk chatroom read/search/send automation with shared communication rules before outbound messages. Use when user asks 카톡 보내줘, 카카오톡 메시지, 카톡 읽어줘, 채팅방 확인, 카톡방 찾아줘, 대화 내역, 카톡 검색, 내가 한 말 찾아줘, 이번 달 카톡 정리, or send/read messages via KakaoTalk. Do NOT use for Slack, iMessage/SMS, Gmail/Google Chat, long-form writing, or message drafting without KakaoTalk execution."
---

# KakaoTalk CLI

`katok` CLI 하나로 카카오톡을 읽고, 검색하고, 보낸다.

**읽기, 검색, 발송 모두 `katok`으로 한다.** 접근성 UI 스크래핑, DB 직접 조회, 복호화로 폴백하지 않는다. `katok`이 로컬 DB 접근, 아카이브, 검색 인덱스, 발송 UI 조작을 전부 관리하므로 스킬은 CLI 표면만 다룬다.

## 실행 표면 확인

```bash
katok --help
```

설치본이 문서보다 오래됐을 수 있다. 절차에 나오는 서브커맨드가 `--help` 목록에 없으면 [references/setup-and-permissions.md](references/setup-and-permissions.md)의 업그레이드 절차로 올리고, 올리기 전까지 그 경로를 쓰지 않는다.

## 안전선

- 검색 결과는 snippet, 날짜, 채팅방, chunk ID까지만 보여준다. 원문은 사용자가 그 결과를 열어 달라고 했을 때만 `katok chunk get`으로 가져온다.
- 전체 채팅방 목록이나 전체 chunk 목록을 응답에 그대로 옮기지 않는다. 요청한 범위 밖의 대화가 딸려 나온다.
- 발송은 되돌릴 수 없고 다른 사람에게 도달한다. 보낼 방을 스스로 고르지 않고, 방과 최종 본문을 사용자에게 확인받는다. 사용자가 방과 정확한 최종 본문을 이미 명시 승인한 경우에만 재확인을 생략한다.
- 대상 지정만 검증하면 될 때는 `--dry-run`을 쓴다. 방 창을 여는 것만으로는 아무에게도 알림이 가지 않는다.
- 사람 검토를 남기려면 `--draft`로 입력창에 붙여둔다. 사람이 Enter를 누르기 전까지 전달되지 않는다.
- 대화를 화면에 띄우는 시연에는 합성 데이터를 쓴다. 발표, 녹화, 화면 공유는 대화가 요청자 아닌 사람에게 도달하는 경로다.

## 메시지 작성 의존성

카카오톡으로 보낼 문구를 작성, 수정, 발송할 때는 transport 실행 전에 공통 커뮤니케이션 규칙을 먼저 읽는다.

1. `../communication/references/work-message-contract.md`
2. `../communication/references/style-profiles.md` (저장된 문체를 맞출 때만)
3. `../communication/references/message-templates.md` (요청, 핸드오프, 상태 공유일 때)
4. `../communication/references/channel-overlays/kakaotalk.md`

공통 스킬을 읽을 수 없으면 최소 계약만 따른다: 목적, 수신자, 요청/맥락/액션을 분리하고, 사용자가 승인한 본문은 임의로 재작성하지 않으며, 발송 전 채팅방과 최종 본문을 확인받는다.

## 참조 라우팅

| 언제 | 읽을 것 |
|---|---|
| 메시지를 읽거나 보낸다 (최신성 판단, 단계, 확인 템플릿, 발송 결과 판정) | [references/message-workflows.md](references/message-workflows.md) |
| 검색이 원하는 걸 못 찾는다, 기간이나 발신자로 좁힌다, 내가 한 말을 모은다 | [references/search-and-filtering.md](references/search-and-filtering.md) |
| 보낼 방을 이름으로 특정하지 못한다, 같은 이름이 여럿이다, 오픈채팅이다 | [references/chatroom-lookup.md](references/chatroom-lookup.md) |
| 설치, Full Disk Access, 발송 전제 조건을 점검한다 | [references/setup-and-permissions.md](references/setup-and-permissions.md) |
| 실제 대화 대신 합성 데이터로 시연한다 | [references/demo-mode.md](references/demo-mode.md) |
