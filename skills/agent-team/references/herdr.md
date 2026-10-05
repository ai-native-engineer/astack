# herdr Worker Transport

사용자가 herdr pane을 요청하거나 coordinator와 다른 CLI harness를 worker로 쓸 때만 적용한다. 같은 런타임의 네이티브 팀이 충분하면 해당 런타임 지침을 따른다.

## 전제

- `test "${HERDR_ENV:-}" = 1`로 herdr 관리 pane 안인지 먼저 확인한다. 아니면 herdr 밖이라고 알리고 네이티브 팀으로 진행한다. 밖에서 herdr를 조작하면 사용자가 보고 있는 세션을 건드린다.
- 명령 문법은 설치된 `herdr agent`, `herdr pane`의 `--help`를 정본으로 삼는다. 응답은 JSON이므로 pane ID와 상태는 응답에서 읽는다.
- `herdr` 인자 없이 실행하지 않는다. TUI가 뜬다.
- headless 실행(`codex exec`, `claude -p`)으로 대체하지 않는다. 관찰 가능한 pane이 이 transport의 목적이다.
- 권한 우회 flag는 자동 추가하지 않는다. 사용자가 허용한 harness 인자만 `--` 뒤에 전달한다.

## 결과 계약

herdr 상태는 turn이 끝났다는 신호일 뿐 성공 신호가 아니다. worker가 오류로 멈춰도 `idle`로 돌아온다.

1. lead가 `mktemp -d`로 run 디렉터리를 만든다.
2. 모든 위임 프롬프트 끝에 "결과 전문을 `<run-dir>/<worker>/turn-<N>.md`에 저장하라"를 붙인다.
3. 결과 파일과 실제 변경 파일을 정본으로 삼는다. pane 화면은 진단용이다.
4. 결과 파일이 없으면 `herdr agent read <worker>`로 화면을 보고 원인을 판단한다.

## Workflow

1. 호출자 pane을 `herdr pane layout --pane "$HERDR_PANE_ID"`로 보고, 넓으면 `right`, 좁으면 `down`으로 나눈다.
2. worker마다 `herdr pane split --current --direction <dir> --cwd "$PWD" --no-focus`로 pane을 만든다.
3. `herdr agent start <worker> --kind <claude|codex|...> --pane <pane-id> -- <harness 인자>`로 worker를 띄운다. 모델은 harness 인자로 지정한다(예: `-- --model sonnet`, `-- -m <codex-model>`).
4. `herdr agent prompt <worker> "<계약 템플릿 + 결과 파일 지시>" --wait --timeout <ms>`로 위임한다. worker가 둘 이상이면 각각 `--wait` 없이 보낸 뒤 `herdr agent wait <worker>`로 하나씩 회수한다.
5. 결과 파일을 검토한다. 수정은 같은 worker에 다음 turn 번호로 `agent prompt`한다.
6. 통합이 끝나면 `herdr pane close <pane-id>`로 worker pane을 닫는다.

## 상태별 대응

| 신호 | 대응 |
|---|---|
| `agent_pane_busy` (split 직후 start) | 셸 초기화 중이다. 2~3초 뒤 같은 pane에 다시 start한다 |
| `agent_prompt_stalled` (start 직후 첫 prompt) | harness가 입력을 받기 전이라 프롬프트가 버려진다. `agent read`로 입력창이 비었는지 보고 한 번 다시 보낸다 |
| `blocked` 또는 `agent_blocked` | 권한·질문 화면이다. `agent read`로 확인하고 사용자에게 묻는다. 대신 승인하지 않는다 |
| `unknown` | 완료 증거가 아니다. 결과 파일과 화면으로 판단한다 |
| `timeout` | `agent read`로 작업 중인지 본다. 작업 중이면 기다리고, 입력 대기면 `agent send-keys`로 복구한다 |
| `idle`/`done`인데 결과 파일 없음 | worker 오류다. 화면의 오류를 Obstacles로 기록하고 재시도 또는 lead가 직접 수행한다 |
