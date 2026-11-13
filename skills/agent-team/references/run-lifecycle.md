# 실행 기록과 결과 회수

공통 계약은 루트 SKILL.md를 따른다. 위임 전에 읽고 네이티브 팀과 Herdr에 같은 식별 기준을 적용한다.

## 실행 기록

- 작업의 기존 산출물 위치를 우선 사용한다. 일회성 작업이면 OS가 제공하는 임시 디렉터리를 만든다. 새 전역 최상위 폴더나 별도 상태 DB를 만들지 않는다.
- lead는 run 디렉터리와 worker별 결과 디렉터리를 먼저 만든다. worker에게 전달할 결과 경로는 절대 경로다.
- run 기록에는 `run_id`, lead의 하네스/세션, 저장소/작업용 worktree, 시작 기준 commit과 기존 변경, worker별 담당 범위를 적는다.
- worker마다 하네스, 실제 모델, native thread/job/session ID, Herdr 세션/pane/agent 이름, 결과 경로, 생성한 자원, 마지막 turn과 상태를 기록한다. 해당 없는 값은 생략하고 미확인 값은 미확인으로 둔다.
- 기존 worker를 재개하거나 Herdr pane에 다시 지시할 때도 별도의 재개 기록을 남긴다. `pane_id`, 실제 native session/job ID, 전송한 프롬프트, 전송 시각, 수신 근거, 결과 회수 시각, 회수한 결과 경로 또는 화면 근거, 최종 상태를 한 항목에 연결한다.
- 프롬프트 수신이나 `working` 전환만으로 완료를 기록하지 않는다. 결과 회수 뒤 변경 파일·검증 결과·남은 프로세스 중 하나 이상의 완료 근거를 대조하고, 없으면 `settled_unverified` 또는 `in_progress`로 남긴다.
- 기록 파일의 절대 경로를 lead의 세션 인계 요약에 남긴다. 재부팅 이후까지 필요한 작업은 임시 디렉터리에만 두지 않고 기존 프로젝트 보관 위치를 사용한다.
- 시크릿, 전체 환경변수, 인증정보는 실행 기록에 넣지 않는다.

## 결과 형식

worker는 lead가 지정한 `turn-<N>.md`를 한 번 완성해 저장한 뒤 경로를 반환한다. 파일을 읽는 도중 부분 결과를 완료로 오인하지 않도록 같은 디렉터리의 임시 파일에 쓰고 최종 경로로 교체한다.

```text
run_id:
worker_id:
turn_id:
하네스/세션:
담당 범위:
결론:
변경 파일:
검증 명령과 결과:
실제 부수 효과:
남은 실행/프로세스:
Obstacles:
```

native 결과를 파일로 직접 저장할 수 없으면 lead가 실제 반환 내용을 같은 형식으로 보관한다. ID와 경로를 worker가 추측해 채우게 하지 않는다.

## 완료 판정

1. run, worker, turn이 현재 기다리는 과제와 같은지 확인한다. 다른 turn 결과와 중복 알림은 재사용하지 않는다.
2. 결과 파일이 완성됐는지, 반환된 검증 결과가 해당 작업 경로와 변경에 대한 것인지 확인한다.
3. lead는 결정적인 수치, 인용, 변경 파일을 원문과 diff에서 대조한다. worker의 성공 선언이나 exit code 하나로 통합하지 않는다.
4. 담당 밖 변경과 보고되지 않은 부수 효과, 남은 background 작업을 확인한다.
5. lead가 필요한 통합 검사를 수행한 뒤 완료로 기록하고 Git 변경을 처리한다.

- Herdr prompt가 수락되거나 agent가 `working`으로 바뀐 것은 입력 수신·활동 시작 증거일 뿐이다. 같은 run/worker/turn을 계속 관찰하고, 결과 회수와 완료 근거 대조 전에는 완료로 기록하거나 같은 작업을 재전송하지 않는다.
- `agent_prompt_stalled`가 반환되면 입력 미전달로 단정하지 않는다. 먼저 같은 run/worker/turn의 결과 파일과 기록을 확인하고, 완성·일치·검증된 결과가 있으면 재전송 없이 회수한다. 결과가 없거나 부분적이면 기존 session/job의 실제 상태를 확인한 뒤 미해결 범위만 재개한다.
- 최종 보고가 있어도 worker가 소유한 foreground 또는 background 프로세스가 남아 있으면 해당 turn을 완료로 단정하지 않는다. 프로세스의 남은 작업과 의도적 상주 여부를 확인해 기록한다. 완료된 turn을 되살리기 위해 프롬프트를 재전송하지 않는다.

## 하위 세션 잇기와 보관

연관 작업과 후속 작업은 새 worker를 만들지 않고 맥락을 가진 기존 하위 세션에 보낸다. 이전 turn의 결과를 회수한 뒤 보낸다. 확인 근거는 설치된 CLI의 `--help`(`codex`, `herdr`, `agy`)와 Claude Code 공식 문서(sub-agents)다.

| 런타임 | 잇기 | 보관과 종료 |
|---|---|---|
| Claude Code | `SendMessage`의 `to`에 이름 또는 agent ID를 넣는다. 끝난 하위 세션도 새 `Agent` 호출 없이 이력을 유지한 채 백그라운드로 재개된다. 이름을 새 agent가 가져갔으면 거부되므로 ID를 쓴다. Explore와 Plan은 agent ID를 돌려주지 않아 잇지 못한다. | 보관 기능은 없다. 끝난 하위 세션의 행은 30초 뒤 `/tasks`에서 사라지고 transcript는 `cleanupPeriodDays`(기본 30일) 뒤 지워진다. 최종 보고 뒤에도 하위 세션이 띄운 백그라운드 명령이 남아 대기 상태일 수 있으므로 `TaskStop`으로 멈춘다. `TaskStop`으로 멈춘 세션은 실행이 끝나면 `SendMessage`로 다시 잇는다. 사용자가 `/tasks`에서 `x`로 멈춘 세션은 자동 재개되지 않는다. |
| Codex | 네이티브 도구는 현재 스키마의 메시지 도구에 기존 worker 식별자를 넣는다. CLI는 `codex resume <세션 ID 또는 이름> [프롬프트]`와 `codex queue --thread <ID 또는 이름> --message <텍스트> [--resume]`다. | `codex archive <세션 ID 또는 이름>`으로 보관하고 `codex unarchive`로 되돌린다. `codex delete`는 영구 삭제라 승인 없이 쓰지 않는다. 네이티브 하위 worker 스레드에 `archive`가 적용되는지는 미확인이다. |
| Herdr | 이전 turn을 회수한 뒤 같은 agent에 `herdr agent prompt <대상> <텍스트> --wait`를 보낸다. pane 안 하네스의 세션 복원은 [Herdr](herdr.md)와 공용 `herdr` 스킬의 recovery를 따른다. | 보관 개념은 없고 `herdr pane close <pane_id>`만 있다. 이번 실행이 만든 pane만 결과를 보존한 뒤 닫는다. 닫은 뒤 pane 안 대화가 어떻게 남는지는 미확인이다. |
| AGY | CLI 세션은 `agy --continue`나 `agy --conversation <ID>`로 잇는다. 네이티브 하위 세션 이어쓰기는 미확인이다. | 보관 개념은 `--help`에 없다. |

- 런타임에 보관 개념이 없으면 보관했다고 보고하지 않는다. 결과를 회수하고 background 작업이 없는 상태를 확인한 뒤 사용자에게 인계한 세션이 아닌 것만 종료한다.
- 이을 수 없는 세션(식별자 유실, 거부, 미지원)은 완료분을 보존하고 남은 범위만 새 worker에 전달한다. 아래 재개 규칙과 같다.

## 재개와 종료

- 재개할 때 기록의 실제 session/job ID로 상태를 다시 확인하고, 재개 기록에 프롬프트 전달과 결과 회수를 순서대로 갱신한다. runtime이 resume/message를 지원하지 않으면 완료분을 보존하고 남은 범위만 새 worker에 전달한다.
- 명시한 모델이 worker 시작 전에 provider/catalog 오류로 거부되면 같은 역할의 현재 하네스 모델로 한 번만 fallback한다. 호환 override가 없으면 `model`을 생략해 lead 모델을 상속할 수 있으며, 요청 모델, 실제 모델, provider와 fallback 사유를 실행 기록에 남긴다.
- 같은 turn의 실행 여부가 불명확하면 재전송보다 관측을 우선한다. 모델/provider를 바꿔 같은 작업을 중복 실행하지 않는다.
- 사용자에게 인계했거나 실행이 남은 자원은 닫지 않는다. 이번 실행이 만들었고 결과가 회수된 자원만 lead가 종료한다.
- worker의 PR을 머지하고 그 worktree와 브랜치를 지우기 전에 그 worker를 먼저 멈춘다(`TaskStop`). 최종 보고 뒤에도 백그라운드 push 재시도가 남을 수 있어, 대상이 사라지면 재시도가 끝나지 않고 사용자 화면에는 계속 실행 중으로 보인다. `ListAgents`의 completed 표시만 믿지 말고 실행 중인 작업을 확인한다. 하네스가 잠근 worker worktree를 `git worktree unlock`으로 풀기 전에도 같다.
- 추가 worktree는 미커밋, 미추적, 무시된 산출물과 반영된 변경을 확인한 뒤 정리한다. worker가 만든 내용이 남으면 보존 경로를 먼저 확보한다.
- 최종 보고에는 사용한 하네스/모델, 완료 범위, 검증 종류, 결과 경로, 남은 자원을 구분한다. 발견/설정/명시 호출/실제 위임은 각각 확인한 수준까지만 보고한다.
