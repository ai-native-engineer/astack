# 합성 데이터로 시연하기

발표, 녹화, 화면 공유처럼 대화가 요청자 아닌 사람에게 보이는 자리에서는 실제 아카이브를 열지 않는다. 합성 fixture로 별도 인덱스를 만들어 같은 명령을 그대로 시연한다.

## 별도 인덱스 만들기

`katok`은 `--data-dir`로 아카이브 위치를 바꾸고, `fixture` 소스로 JSONL을 그대로 읽는다. 실제 아카이브와 파일이 분리되므로 시연 중 실수로 실제 대화를 열 수 없다.

```bash
DEMO="$HOME/Library/Application Support/katok-demo"
katok --data-dir "$DEMO" sync demo.jsonl --source fixture --json
katok --data-dir "$DEMO" search keyword "<표현>" --limit 1000 --json
```

시연 중 실행하는 모든 명령에 `--data-dir`을 붙인다. 하나라도 빠지면 그 명령은 실제 아카이브를 연다.

## fixture 형식

한 줄에 메시지 하나인 JSONL이다. 필드 구성은 katok 저장소의 fixture 타입이 정본이므로, 형식이 안 맞으면 그쪽을 확인한다.

```json
{"account_hash":"acct-demo","chat_id":"2001","chat_name":"<방 이름>","chat_type":"group","message_id":"demo-0001","sender_id":"u-100","sender_nickname":"<보낸 사람>","timestamp":"2026-08-02T01:20:00Z","text":"<본문>","message_type":"text","reply_to_message_id":null}
```

`chat_type`은 `group` 또는 `direct`다. 같은 발신자가 짧은 간격으로 연달아 보낸 메시지는 하나의 chunk로 묶이므로, 여러 줄짜리 발화를 보여주려면 `\n`을 넣거나 같은 발신자로 연속 배치한다.

## 데이터 설계

검색이 실제로 일해야 정답이 나오도록 만든다. 답이 한 방에 다 모여 있으면 시연이 무엇을 증명하는지 보이지 않는다.

- 찾을 대상을 여러 방에 흩어 놓는다. 한 방만 읽으면 놓치게 한다.
- 다른 사람도 같은 표현을 쓰게 한다. 발신자 필터가 있어야 답이 맞게 된다.
- 지난 기간의 항목을 섞는다. 기간 필터가 있어야 답이 맞게 된다.
- 잡담을 대상보다 많이 둔다. 검색어가 노이즈를 걸러야 하는 상황을 만든다.

## 이름 충돌 확인

지어낸 한국어 이름은 생각보다 자주 실제 연락처와 겹친다. 시연 화면이나 공개 저장소에서 자기 이름을 발견하는 상황을 피한다.

```bash
katok source chats --source macos --json | jq -r '.[].chat_name' > "${TMPDIR:-/tmp}/roomnames.txt"
grep -c "<지어낸 이름>" "${TMPDIR:-/tmp}/roomnames.txt"   # 0이어야 한다
```

생성한 fixture 파일은 커밋하지 않는다. 생성 스크립트를 정본으로 두고 매번 다시 만든다. `.jsonl`은 실제 카카오톡 유래 데이터가 취하는 형식이라 저장소에서 통째로 무시되는 경우가 많다.
