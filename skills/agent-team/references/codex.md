# Codex

Codex가 coordinator일 때 적용한다. 다른 coordinator가 Codex를 worker harness로 쓸 때는 아래 모델 절만 참조한다.

## 모델과 팀

- lead는 Sol을 사용한다.
- worker는 Terra를 사용한다.
- 모델 인자: Sol=`gpt-5.6-sol`, Terra=`gpt-5.6-terra`. codex CLI는 Sol/Terra라는 별칭을 해석하지 못하므로 `-m`에는 이 인자를 쓴다.
- 네이티브 subagent thread를 사용한다.
- lead가 Sol이 아니면 작업 전에 `codex-team`으로 다시 시작하라고 안내한다.

## 실행

1. 서로 겹치지 않는 범위로 subagent 2~3명을 만든다.
2. 루트 스킬의 공통 계약으로 각 subagent에게 위임한다.
3. 같은 작업의 수정과 추가 확인은 기존 subagent에게 보낸다.
4. 통합이 끝날 때까지 subagent thread를 유지한다.
5. 충돌하거나 근거가 약한 결과는 담당 subagent에게 되돌린다.
6. 통합 후 subagent를 종료한다.
7. 사용한 worker 모델, subagent 수, 검증 결과를 짧게 보고한다.
