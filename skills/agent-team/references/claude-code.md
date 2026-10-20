# Claude Code

공통 계약은 루트 SKILL.md를 따른다. Claude Code가 coordinator이거나 Herdr worker일 때만 읽는다.

## 네이티브 팀

- 현재 세션에 노출된 teammate 또는 subagent 도구를 사용한다. Agent Teams가 없으면 있다고 가정하지 않는다.
- coordinator 모델을 유지한다. worker는 현재 지원되는 모델과 effort 설정을 확인해 선택하고, 모델 계열 때문에 세션을 다시 시작하거나 전역 설정을 바꾸지 않는다.
- 네이티브 팀이 가능하면 in-process 실행을 우선한다. 기본 작업 경로는 lead의 작업용 worktree이며 `isolation: "worktree"`를 일괄 지정하지 않는다.
- 독립 브랜치나 실험이 필요한 경우에만 lead가 격리를 선택한다. 하네스가 만든 경로와 브랜치 이름을 반환값에서 확인하고 실행 기록에 남긴다.
- 수정과 추가 확인은 기존 teammate에게 보낸다. 출력 상한으로 잘린 보고는 재사용 가능한 사실만 회수하고, 남은 범위를 새 worker에 맡긴다.
- `idle_notification`에 보고가 다시 실리면 timestamp, worker, turn을 대조해 중복 결과를 다시 통합하지 않는다.

## worker 전달문

Sonnet worker에는 공통 계약 뒤에 다음 문단을 붙인다.

```text
Finish the assigned scope and its relevant checks. Ask only when missing information blocks progress or an action exceeds the allowed side effects.

After the assigned work is complete, report the result. Do not add unrequested features, tests, files, docs, or refactors.
```

## Herdr worker

- `herdr agent start`의 대상 kind는 `claude`다.
- `claude --help`에서 현재 모델 인자를 확인한다. `claude -p`를 관찰 가능한 Herdr pane의 대체 경로로 사용하지 않는다.
- 종료와 worktree 정리는 lead가 결과와 Git 상태를 확인한 뒤 수행한다. worker에게 PR, push, merge를 맡기지 않는다.
