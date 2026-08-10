# 메시지 읽기와 발송 워크플로

## 목차

- 최신성 확인 - 타임스탬프로 판단한다
- 읽기 워크플로
- 발송 워크플로

## 최신성 확인 - 타임스탬프로 판단한다

```bash
katok doctor --json
```

`freshness.recommendation.sync_before_search`는 최신성 지표가 아니다. 아카이브가 한 번이라도 완료됐으면 계속 `false`로 나오므로, 며칠 밀린 아카이브에서도 `false`다. 그 값 대신 **`freshness.last_sync.completed_at`과 현재 시각의 차이**로 판단한다.

- 요청이 최근 대화에 걸리면(오늘, 이번 주, 이번 달, 방금 온 메시지) 차이를 확인하고 필요하면 sync한다.
- 오래된 대화만 찾으면 sync 없이 진행한다.

```bash
katok sync --source macos --json
```

sync를 돌리기 전에 두 가지를 사용자에게 알린다.

- 아카이브 규모에 따라 수십 분이 걸린다.
- 도는 동안 아카이브가 잠겨 **검색과 읽기도 함께 막힌다**. sync 중 조회는 `database is locked`로 실패하므로 끝날 때까지 기다린다.

## 읽기 워크플로

1. 위 최신성 확인을 거친다.
2. 검색으로 후보를 찾는다. 방식 선택, limit, 기간 및 발신자 좁히기는 [search-and-filtering.md](search-and-filtering.md)를 읽는다.
3. 결과를 snippet, 날짜, 채팅방, chunk ID로 먼저 요약한다.
4. 사용자가 특정 결과나 특정 방을 읽어 달라고 한 경우에만 본문을 가져온다.

```bash
katok chunk get <chunk-id> --json
katok chunk context <chunk-id> --json
```

특정 방의 최근 대화를 읽을 때는 정확한 `chat_id`를 고른 뒤 chunk 목록의 최신 항목을 골라 `chunk get`으로 본문을 받는다. `chunks` 출력 자체에는 본문이 없다.

```bash
katok source chats --source macos --json \
  | jq --arg name "<채팅방 이름>" '[.[] | select(.chat_name | contains($name))]'
katok chunks --chat <chat-id> --json | jq '.[-5:]'
```

읽은 뒤에는 최근 대화 주제와 답장 필요 여부를 요약한다.

## 발송 워크플로

### 1. 맥락과 대상 확인

- 맥락이 필요하면 위 읽기 워크플로를 쓴다.
- 방을 이름으로 특정하지 못하면 [chatroom-lookup.md](chatroom-lookup.md)를 읽는다.

### 2. 메시지 작성

- `started_at`이 가장 최근인 chunk를 우선해 대화 흐름에 잇는다.
- SKILL.md `메시지 작성 의존성`의 공통 계약과 카카오톡 overlay를 적용한다.

### 3. 사용자 확인

보낼 방과 본문을 텍스트로 보여주고 확인받는다.

```
**보낼 메시지:**
받는 사람: {채팅방}
---
{메시지 내용}
---
```

### 4. 대상 검증

전달 없이 방 지정만 확인한다. 방 창을 여는 것으로는 상대에게 알림이 가지 않는다.

```bash
katok send --room "<채팅방 이름>" --dry-run --json
```

### 5. 발송

```bash
katok send --room "<채팅방 이름>" --text "<메시지>" --accept-use-policy --json
```

- `--accept-use-policy`는 텍스트, 이미지, draft 모드에 필요하다. 없으면 실행 전에 거부된다.
- 이름이 여러 방과 겹치면 katok이 추측하지 않고 거부한다. 이때는 `--chat <chat-id>`로 지정한다. `chat_id`는 검색 결과와 `chunks` 출력에 있다.
- 사람이 최종 확인하고 보내야 하면 `--text` 대신 `--draft`로 입력창에 남긴다.
- 이미지는 `--image <경로>`로 보낸다. `--text`와 함께 쓰지 않는다.
- 화면을 건드리면 안 되는 자동화에는 `--no-open`을 준다. 닫힌 방을 열면 카카오톡 창이 잠깐 앞으로 나온다.
- 아무도 키보드 앞에 없으면 `--take-focus-now`로 즉시 포커스를 가져온다. 기본값은 사용자의 타이핑이 멈추기를 기다린다.

### 6. 결과 판정

종료 코드가 `0`이고 JSON의 `success`가 `true`이며 `chat`이 요청한 그 방일 때 완료로 본다. 셋 중 하나라도 어긋나면 보내지 못한 것으로 보고한다.

사용자가 발송 확인을 요청하면 `katok sync --source macos --json` 후 보낸 문구를 keyword 검색한다.
