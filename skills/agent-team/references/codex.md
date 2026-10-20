# Codex

공통 계약은 루트 SKILL.md를 따른다. Codex가 coordinator이거나 Herdr worker일 때만 읽는다.

## 네이티브 팀

- 현재 세션에 노출된 subagent 생성, 메시지, 대기 도구와 스키마를 사용한다. CLI 버전이나 모델 이름만 보고 팀 도구가 있다고 가정하지 않는다.
- coordinator 모델을 유지한다. worker 모델을 지정할 수 있으면 현재 도구가 허용하는 실제 ID를 사용하고, 허용되지 않으면 상속된 모델을 기록한다.
- 컨텍스트를 상속하지 않는 worker에는 목표, 파일, 근거, 금지 작업을 빠짐없이 전달한다. 컨텍스트 상속 여부와 모델 변경 조건은 현재 생성 도구의 제약을 따른다.
- 기본 작업 경로는 lead의 작업용 worktree다. worker에게 자동 worktree 생성이나 Git 변경을 맡기지 않는다.
- 수정과 추가 확인은 기존 worker 식별자로 보낸다. 반환된 thread/session ID와 결과 경로를 실행 기록에 남긴다.
- 도구에 종료 기능이 없으면 종료됐다고 보고하지 않는다. 실행 중인 작업이 끝났는지 확인하고 세션 상태를 기록한다.

## Herdr worker

- `herdr agent start`의 대상 kind는 `codex`다.
- `codex --help`에서 현재 모델과 작업 경로 인자를 확인하고, 허용된 인자만 Herdr의 `--` 뒤에 전달한다.
- `codex exec`를 관찰 가능한 Herdr pane의 대체 경로로 사용하지 않는다.
