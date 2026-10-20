# AGY

공통 계약은 루트 SKILL.md를 따른다. AGY가 coordinator이거나 Herdr worker일 때만 읽는다.

## 네이티브 팀

- 현재 세션이 실제로 제공하는 subagent 도구가 있으면 그 스키마를 사용한다. 이름이 비슷한 다른 CLI의 팀 도구를 가져오지 않는다.
- `agy agent`와 `agy agents`는 사용 가능한 agent 목록 조회다. worker 생성이나 메시지 전송 명령으로 사용하지 않는다.
- 네이티브 팀 도구가 없고 Herdr 안에서 실행 중이면 Herdr 경로를 사용한다. 둘 다 없으면 lead가 직접 처리하고 제한을 보고한다.
- 모델 ID는 필요할 때 `agy models`로 확인한다. Codex나 Claude의 모델 ID를 그대로 넘기지 않는다.
- effort와 권한 모드는 기존 사용자 설정을 유지한다. worker 실행을 위해 전역 설정을 바꾸거나 권한 우회 인자를 추가하지 않는다.

## Herdr worker

- `herdr agent start`의 대상 kind는 `agy`다. 설치된 명령에서 지원 여부를 확인한 뒤 pane을 만든다. 지원 여부가 미확인이면 생성 단계로 넘어가지 않는다.
- `agy --help`에서 모델과 effort 인자를 확인한 뒤 허용된 인자만 Herdr의 `--` 뒤에 전달한다.
- AGY가 입력 대기로 돌아와도 background task가 실행 중일 수 있다. 해당 turn의 결과와 남은 작업을 함께 확인한다.
- `agy --print`를 관찰 가능한 pane의 대체 경로로 사용하지 않는다.

## 발견과 검증

설치 파일의 존재, AGY의 스킬 발견, 명시 호출, 자동 선택은 따로 확인한다. 다른 CLI의 공유 스킬 링크만 보고 AGY에서도 로드된다고 보고하지 않는다.
