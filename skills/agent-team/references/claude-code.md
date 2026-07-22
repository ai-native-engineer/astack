# Claude Code

Claude Code에서만 이 파일을 적용한다.

## 모델과 팀

- lead는 Fable을 사용한다.
- worker는 Sonnet을 기본으로 사용한다.
- 추출, 분류, 페르소나, 반복 작업은 Sonnet `low` effort를 사용한다.
- 코드 구현과 일반 검토는 Sonnet `medium` effort를 사용한다.
- 복잡한 추론이 명시적으로 필요할 때만 Sonnet `high` effort를 사용한다.
- worker에게도 모호한 설계 판단이나 고위험 검토가 필요할 때만 Opus를 사용한다.
- 네이티브 Agent Teams를 in-process 모드로 사용한다.
- lead가 Fable이 아니면 작업 전에 `claude-team`으로 다시 시작하라고 안내한다.

## 실행

1. 서로 겹치지 않는 범위로 teammate 2~3명을 만든다.
2. 루트 스킬의 공통 계약으로 각 teammate에게 위임한다.
3. 같은 작업의 수정과 추가 확인은 기존 teammate에게 보낸다.
4. 통합이 끝날 때까지 teammate를 유지한다.
5. 충돌하거나 근거가 약한 결과는 담당 teammate에게 되돌린다.
6. 통합 후 teammate를 종료한다.
7. 사용한 worker 모델, teammate 수, 검증 결과를 짧게 보고한다.
