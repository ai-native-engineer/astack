# Tiro 소스

Tiro는 이미 클라우드에서 전사가 끝난 회의 노트다. voice-memos에서는 검색·읽기만 한다. 워처, apple-stt, 요약 파이프라인, 원본 업로드는 쓰지 않는다.

인증은 `agents-env`의 `TIRO_TOKEN`(계정 API 키 `id.secret`)이다. `tiro auth login` OAuth는 쓰지 않는다. 루프백 콜백이 만료되어 로그인에 실패한다.

## 조회

스킬 루트에서:

```bash
python3 scripts/tiro_notes.py list --limit 10
python3 scripts/tiro_notes.py list --date today
python3 scripts/tiro_notes.py search "키워드"
python3 scripts/tiro_notes.py get <guid>
python3 scripts/tiro_notes.py transcript <guid>
```

`list`/`search`는 `[티로]` 라벨과 guid만 보여 준다. 전사는 항상 `--output`으로 파일에 쓴다. 한 회의가 수십만 자라서 stdout에 본문을 풀면 세션이 죽는다. `--output`을 생략하면 `~/.voice-memos/tiro/<guid>.md`에 저장하고 경로만 출력한다. 그 파일을 접어서 읽는다.

## 워크스페이스

계정 API 키는 워크스페이스에 묶여 있지 않다. `--workspace`가 없으면 CLI가 전체 워크스페이스를 훑고 경고를 낸다. `tiro_notes.py`가 guid를 이렇게 고른다.

1. `TIRO_WORKSPACE`
2. `~/.config/voice-memos/tiro.json`의 `workspace`
3. `tiro wiki workspaces` 결과가 하나면 그 guid를 설정 파일에 저장

여러 개면 설정 파일에 guid를 넣게 안내하고 중단한다. 스킬 문서에 실제 guid를 적지 않는다.

```json
{"workspace": "<guid>"}
```

## 한계

- 원본 음성, 실시간 녹음, 파일 업로드, 노트 제목 수정은 CLI 조회 범위 밖이다.
- `tiro notes search`의 `documents`(원페이지)는 비어 있을 수 있다. 본문이 필요하면 `transcript`를 쓴다.
- 위키 명령은 워크스페이스에 위키가 켜져 있어야 한다. 꺼져 있으면 402다. 회의 노트 검색은 wiki가 아니다.
- MCP는 쓰지 않는다.

## 실패

| 증상 | 다음 동작 |
|------|-----------|
| `TIRO_TOKEN` 없음 / Not authenticated | `agents-env ls`로 키 이름을 확인하고, 없으면 `agents-env edit`로 `TIRO_TOKEN`을 넣는다. 값은 대화에 붙이지 않는다. |
| `tiro` 없음 | `pnpm add -g @theplato/tiro-cli` |
| 워크스페이스 여러 개 | `tiro.json` 또는 `TIRO_WORKSPACE` |
| 목록이 비었다 | 앱에서 노트가 완료 상태인지 본다. 로컬 `search.py` 결과와 섞지 말고 `[티로]`만 비었다고 말한다. |
