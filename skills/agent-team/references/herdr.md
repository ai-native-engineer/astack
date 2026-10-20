# Herdr Worker Transport

위임 전에 [공용 Herdr 스킬](../../herdr/SKILL.md)을 읽는다. 기기/세션 선택, 일반 조작, worker 시작과 관찰, 복구의 정본은 그 스킬이다. 이 문서는 agent-team의 작업 계약과 Herdr 실행을 연결한다.

## 호출자와 대상

- Herdr 내부의 lead와 외부의 Hermes lead를 모두 지원한다. 외부 호출자는 공용 스킬의 명시적 대상 선택 절차를 따른다. `HERDR_ENV`를 위조하거나 사용자 포커스 창을 기본 대상으로 삼지 않는다.
- worker 하네스, 모델, 작업 경로와 담당 범위는 사용자 요청과 루트 SKILL.md를 따른다. 미지원 종류나 사용량 제한을 다른 하네스로 조용히 대체하지 않는다.
- 공용 helper의 `worker-run`은 Codex와 Claude Code를 지원한다. AGY/GJC는 기존 하네스 지침과 설치된 `herdr agent start --help`에서 실제 지원을 확인한 뒤 네이티브 agent 명령을 사용한다. 다른 kind로 위장하거나 helper의 지원 범위를 확장해 해석하지 않는다.
- SSH 연결, 머신 등록, Hermes 설정 변경은 worker 실행과 분리한다. 현재 연결이 없으면 설치/인증 경계를 지키고 실제 장애를 보고한다.

## 실행과 회수

1. [실행 기록과 회수](run-lifecycle.md)에 따라 run/worker/turn 식별자와 결과 경로를 준비한다.
2. 공용 Herdr 스킬로 실제 대상과 점유 상태를 확인하고, 작업 계약을 담은 task 파일과 worker 실행 기록을 전달한다.
3. `agent prompt --wait`의 제출/활동 확인을 유지한다. timeout이나 stalled 응답은 미전달 증거가 아니므로 같은 기록을 관찰한다.
4. lifecycle 상태와 해당 run/turn의 결과 파일, 변경 파일과 검증을 대조해 lead가 완료를 판정한다. 시작 성공이나 `idle`만으로 과제 완료를 선언하지 않는다.
5. 이전 turn을 회수한 뒤 새 turn을 보낸다. 사용자에게 인계했거나 백그라운드 작업이 남은 자원은 닫지 않는다.
6. 이번 실행이 만든 자원만 결과 보존 후 공용 Herdr 절차로 정리한다. 기존 사용자 pane과 세션은 유지한다.

일반 Herdr 조작은 공용 스킬을 직접 호출할 수 있다. 이 문서나 agent-team을 거쳐야만 transport 계약이 적용되는 구조로 만들지 않는다.
