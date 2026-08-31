# 발송할 방 특정하기

`--room`은 채팅 목록에 보이는 제목과 정확히 일치해야 한다. 이름이 안 맞거나 여러 방이 같은 이름을 쓸 때 아래 순서로 좁힌다.

## 1. 실제 이름을 목록에서 읽는다

```bash
katok send --list-rooms --limit 40 --json    # 채팅 목록의 방 이름, 최신순
katok send --list-windows --json             # 지금 열려 있는 창 제목
```

둘 다 전달하지 않고 목록만 반환한다. 여기서 읽은 정확한 제목을 `--room`에 그대로 넘긴다.

전체 목록을 사용자 응답에 그대로 옮기지 않는다. 찾던 방과 후보 몇 개만 보여준다.

## 2. 같은 이름이 여럿이면 chat_id로 지정한다

이름은 식별자가 아니다. 여러 방이 한 이름을 공유하면 katok은 추측하지 않고 발송을 거부한다. 이때는 `--chat`을 쓴다.

```bash
katok search keyword "<그 방에서 오간 표현>" --limit 100 --json \
  | jq -r '.[] | [.chat_id, .chat_name, .started_at] | @tsv'

katok send --chat <chat-id> --text "<메시지>" --accept-use-policy --json
```

`chat_id`는 검색 결과와 `katok chunks` 출력에 들어 있다. 이름과 마지막 대화 시각을 함께 보므로 같은 이름이 있어도 맞는 방을 고른다.

## 3. 오픈채팅이 목록에 없을 때

`--list-rooms`는 카카오톡이 **지금 보여주는 탭**의 목록을 읽는다. 일반 채팅 탭에 머물러 있으면 오픈채팅 방은 나오지 않는다.

1. 카카오톡 앱의 오픈채팅 탭 전환을 사용자에게 요청한다. `katok`이 탭 전환을 제공하지 않으므로 접근성/AppleScript로 직접 조작하지 않는다(SKILL.md의 CLI 표면 원칙). 사용자가 자리에 없으면 아래 3번의 아카이브 경로(`chat_id`)로 우회한다.
2. `katok send --list-rooms --limit 40 --json`을 다시 실행한다.
3. 그래도 안 보이면 방이 없다고 결론내기 전에 `katok search`로 그 방의 대화가 아카이브에 있는지 확인한다. 있으면 `chat_id`로 지정한다.

일반 채팅 목록에 없다는 것만으로 방이 없다고 판단하지 않는다.

## 4. 보내기 전 대상 검증

이름을 확정했으면 전달 없이 지정만 확인한다.

```bash
katok send --room "<확정한 제목>" --dry-run --json
```

`success`가 `true`이고 `chat`이 의도한 방이면 그때 실제 발송으로 넘어간다.
