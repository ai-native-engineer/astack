# GJC

공통 계약은 루트 SKILL.md를 따른다. GJC가 coordinator 또는 worker일 때만 읽는다.

## 네이티브 task

- 현재 세션의 `task` 도구를 사용한다. 실행 전에 실제 스키마와 사용 가능한 agent 정의를 확인한다.
- `task`는 agent와 독립 과제 목록을 받는다. 각 과제의 ID, 설명, assignment에 공통 계약을 담고, 반환된 job/session/artifact 식별자를 기록한다.
- 기본값은 같은 작업용 worktree다. 스키마가 제공하는 `isolated`를 생략하고, 독립 브랜치나 실험이 필요할 때만 격리를 선택한다.
- 격리가 patch 반환, 자동 적용, 자동 commit 중 어떤 동작을 하는지 현재 설정에서 확인한다. lead의 Git 소유권과 맞지 않으면 lead가 준비한 worktree에서 실행한다.
- 현재 provider와 모델 역할 설정을 사용한다. 모델을 지정해야 하면 GJC가 지원하는 provider-qualified ID를 확인한다.
- async 응답은 완료가 아니다. 반환된 job 식별자로 현재 제공되는 상태 조회/결과 회수 도구를 사용한다. 실제 지원되는 message/resume 경로만 재사용한다.
- repository binding은 현재 세션의 작업 경로와 같아야 한다. 다른 저장소 경로를 task 인자에 넣어 권한이나 작업 범위를 넓히지 않는다.

## Herdr 경계

- 설치된 `herdr agent start --help`에 `gjc`가 없으면 `--kind gjc`를 만들거나 다른 kind로 위장하지 않는다.
- 이 경우 다른 하네스에서 GJC를 Herdr worker로 실행하는 경로는 미지원으로 보고한다. GJC coordinator 자체의 네이티브 task와는 다른 상황이다. 다른 하네스에서 GJC task를 호출할 수 있다고 가정하지 않는다.
- 사용자가 GJC를 지정했으면 허용된 다른 하네스를 제안하고 선택을 기다린다. lead가 가능한 일을 진행해도 GJC 위임이 끝났다고 보고하지 않는다.
- GJC를 다른 하네스로 바꾸는 것은 같은 모델을 쓴다는 이유만으로 결정하지 않는다.

## 발견과 검증

`gjc skills discover --source user --query agent-team --json`으로 이름뿐 아니라 source와 실제 경로를 확인한다. 발견 성공을 명시 호출이나 결과 회수 성공으로 확대하지 않는다.
