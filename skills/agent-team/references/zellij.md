# Zellij Worker Transport

사용자가 Zellij를 요청하거나 coordinator와 다른 CLI harness를 worker로 쓸 때만 적용한다. 같은 런타임의 네이티브 팀이 충분하면 해당 런타임 지침을 따른다.

## 도구

`scripts/zdel`을 실행 도구로 사용한다. 먼저 `scripts/zdel --help`만 읽고, 소스는 도구 수정이 필요할 때만 연다.

- Zellij 세션 안이면 그대로 실행한다.
- 세션 밖(백그라운드 잡 등)이면 `zellij list-sessions`로 live 세션을 찾아 `ZELLIJ_SESSION_NAME=<세션명>`을 붙여 외부 제어로 실행한다.
- live 세션이 없으면 `zellij attach -b <세션명>`으로 백그라운드 세션을 만들어 거기에 띄우고, 사용자에게 attach 명령을 안내한다.
- headless 실행(`codex exec` 등)으로 대체하지 않는다. pane 점유가 방해라는 판단으로 강등하지도 않는다 — 관찰 가능한 pane이 이 transport의 목적이다.
- worker마다 별도 pane과 이름을 사용한다.
- codex와 claude worker는 각각 notify와 Stop hook이 turn 결과와 완료 sentinel을 저장한다. 그 외 명령은 `start`와 `send`가 결과 파일 및 sentinel 지시를 prompt에 붙인다. 한 turn의 완료 주체는 둘 중 하나뿐이다.
- `send`는 현재 turn의 sentinel이 생긴 뒤에만 다음 turn을 연다. 먼저 `wait`로 결과를 회수하거나 `status`에서 `done`을 확인한다.
- pane 화면은 진행 진단용이다. 결과 파일과 실제 변경 파일을 정본으로 삼는다.
- 권한 우회 flag는 자동 추가하지 않는다. 사용자가 허용한 harness 명령만 전달한다.

## Workflow

1. 독립 작업을 모두 `start`한 뒤 기다린다.
2. 시작 직후 `peek`으로 두 가지를 점검한다: trust dialog·권한 확인 화면, 그리고 프롬프트가 입력창에 제출되지 않고 남아 있는지. 잔류면 `key <worker> Enter`로 제출한다 — 자동 Enter는 trust dialog를 오승인할 수 있어 zdel이 대신 눌러주지 않는다.
3. worker가 둘 이상이면 `wait-all`로 결과를 한 번에 회수한다.
4. `result`와 실제 변경 파일을 검토한다. 결과 파일이 산출물 전문 대신 요약뿐이면 같은 worker에 해당 turn 파일로 전문 저장을 재요청한다.
5. 수정은 같은 worker에 `send`하고 다시 `wait`한다.
6. 통합이 끝나면 `stop`으로 pane과 임시 상태를 정리한다.

```sh
scripts/zdel start worker-ui "Implement the frozen UI spec" -- agent-cli --model worker-model
scripts/zdel peek worker-ui
scripts/zdel wait-all 1800 worker-ui worker-api
scripts/zdel send worker-ui "Fix the review findings"
scripts/zdel wait worker-ui 1800
scripts/zdel result worker-ui
scripts/zdel stop worker-ui
```

timeout(exit 124)이면 `peek`으로 먼저 확인한다. 작업 중이면 wait 시간을 늘리고, 입력 대기면 `key`로 같은 pane을 복구한다.
