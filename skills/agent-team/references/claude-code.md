# Claude Code

공통 계약은 루트 SKILL.md를 따른다. Claude Code가 coordinator이거나 Herdr worker일 때만 읽는다.

## 네이티브 팀

- 현재 세션에 노출된 teammate 또는 subagent 도구를 사용한다. Agent Teams가 없으면 있다고 가정하지 않는다.
- coordinator 모델을 유지한다. `orchestrator`는 현재 lead 세션의 모델을 사용하며 별도 worker alias로 변환하지 않는다. `implementation`은 `sonnet`, `implementation-complex`는 `opus`, `research`는 `pick_worker_model.py --harness claude`가 고른 alias로 변환한다. `Agent`의 `model`(Workflow는 `agent()`의 `model` 옵션)에 명시한 alias가 현재 도구 계약에서 거부되면 같은 역할의 허용 alias를 한 번 시도하고, 없으면 `model`을 생략해 `CLAUDE_CODE_SUBAGENT_MODEL` 또는 lead 모델을 상속한다. 실제 사용값과 fallback을 기록한다.
- 네이티브 팀이 가능하면 in-process 실행을 우선한다. 기본 작업 경로는 lead의 작업용 worktree이며 `isolation: "worktree"`를 일괄 지정하지 않는다.
- 독립 브랜치나 실험이 필요한 경우에만 lead가 격리를 선택한다. 하네스가 만든 경로와 브랜치 이름을 반환값에서 확인하고 실행 기록에 남긴다.
- 수정과 추가 확인은 기존 teammate에게 보낸다. 출력 상한으로 잘린 보고는 재사용 가능한 사실만 회수하고, 남은 범위를 새 worker에 맡긴다.
- `idle_notification`에 보고가 다시 실리면 timestamp, worker, turn을 대조해 중복 결과를 다시 통합하지 않는다.
- worker가 2차 지시를 받기 전에 1차 완료 보고를 보내면 진행이 안 된 것처럼 보인다. 재촉하기 전에 "N번 지시를 받았는지" 먼저 묻는다.
- 보고서 파일을 쓰지 않고 메시지로만 돌려주는 worker가 있다. 산출물이 파일이어야 하면 lead가 메시지 본문을 파일로 옮긴다.
- 브리프가 전제한 필드가 서버 API에 없으면 worker가 우회하기 전에 계약 담당에게 추가시키고 서버를 재시작한다.
- 백그라운드 작업을 기다리는 worker는 깨어나지 못할 수 있다. 브리프에 긴 작업은 foreground로 돌리라고 적고, lead는 기다릴 때마다 `sleep`을 백그라운드로 걸어 자신을 깨운다.

## worker 전달문

Sonnet worker에는 공통 계약 뒤에 다음 문단을 붙인다.

```text
Finish the assigned scope and its relevant checks. Ask only when missing information blocks progress or an action exceeds the allowed side effects.

After the assigned work is complete, report the result. Do not add unrequested features, tests, files, docs, or refactors.
```

## Herdr worker

- `herdr agent start`의 대상 kind는 `claude`다.
- `claude --help`에서 현재 모델 인자를 확인한다. `claude -p`를 관찰 가능한 Herdr pane의 대체 경로로 사용하지 않는다.
- 맨몸 `claude` 명령, alias, 설정, 훅은 바꾸지 않는다. 프록시 경로의 문제는 `~/scripts`의 `claude-proxy` 래퍼 안에서 푼다.
- 종료와 worktree 정리는 lead가 결과와 Git 상태를 확인한 뒤 수행한다. worker에게 merge를 맡기지 않는다. PR, push는 브리프가 명시한 전용 worktree의 단독 worker에게만 맡긴다.
