# Codex

Codex가 coordinator일 때 적용한다. 다른 coordinator가 Codex를 worker harness로 쓸 때는 아래 모델 절만 참조한다.

## 모델과 팀

- 현재 coordinator의 모델을 유지한다. 특정 모델이 아니라 작업의 품질·비용·지연 요구로 역할을 고른다.
- `gpt-6-astra`는 복잡한 통합, 높은 위험, 깊은 검토에 쓴다.
- `gpt-6-sol`은 일반적인 코딩, 조사, 판단이 필요한 worker에 쓴다.
- `gpt-6-luna`는 범위가 좁고 반복적이며 비용·지연에 민감한 worker에 쓴다.
- 모델을 지정할 때는 Codex가 해석하는 실제 모델 ID를 `-m`에 전달한다. `gpt-6-astra`, `gpt-6-sol`, `gpt-6-luna`를 사용한다.
- coordinator가 Astra가 아니라는 이유만으로 세션을 재시작하지 않는다.
- 네이티브 subagent thread를 사용한다.

## 실행

1. 서로 겹치지 않는 범위로 subagent 2~3명을 만든다.
2. 루트 스킬의 공통 계약으로 각 subagent에게 위임한다.
3. 같은 작업의 수정과 추가 확인은 기존 subagent에게 보낸다.
4. 통합이 끝날 때까지 subagent thread를 유지한다.
5. 충돌하거나 근거가 약한 결과는 담당 subagent에게 되돌린다.
6. 통합 후 subagent를 종료한다.
7. 사용한 worker 모델, subagent 수, 검증 결과를 짧게 보고한다.
