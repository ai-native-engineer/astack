# Claude Code

Claude Code에서만 이 파일을 적용한다.

## 모델과 팀

- lead는 지금 세션 모델이 Opus(`opus`)나 Fable(`fable`)이면 그대로 맡는다. 두 계열 모두 판단과 통합을 맡길 수 있으니, 모델 때문에 세션을 다시 시작해 맥락을 잃지 않는다.
- 세션 모델이 Sonnet이나 Haiku면 작업 전에 `/model opus`로 바꾸자고 안내한다.
- worker는 Sonnet(`sonnet`)을 기본으로 사용한다.
- 추출, 분류, 페르소나, 반복 작업은 Sonnet `low` effort를 사용한다.
- 코드 구현과 일반 검토는 Sonnet `medium` effort를 사용한다.
- 복잡한 추론이 명시적으로 필요할 때만 Sonnet `high` effort를 사용한다.
- worker에게도 모호한 설계 판단이나 고위험 검토가 필요할 때만 Opus를 사용한다.
- 네이티브 Agent Teams를 in-process 모드로 사용한다.

## 실행

1. 서로 겹치지 않는 범위로 teammate 2~3명을 만든다.
2. 루트 스킬의 공통 계약으로 각 teammate에게 위임한다. Sonnet teammate에게는 템플릿 뒤에 아래 두 문단을 그대로 붙인다. Sonnet은 `low`, `medium`에서 일을 다 끝내기 전에 확인을 구하며 멈추거나, 요청하지 않은 테스트와 문서를 덧붙이는 경향이 있다.

```text
Keep working until everything the user asked for is done, and only stop to ask when you can't go on without the user or before a risky step.

When the work the user asked for is done and checked, stop and report. Don't add features, tests, files, docs or refactors that weren't asked for. If you think one would help, mention it at the end instead of doing it.
```

3. 같은 작업의 수정과 추가 확인은 기존 teammate에게 보낸다.
4. 통합이 끝날 때까지 teammate를 유지한다.
5. 충돌하거나 근거가 약한 결과는 담당 teammate에게 되돌린다.
6. 통합 후 teammate를 종료한다.
7. 사용한 worker 모델, teammate 수, 검증 결과를 짧게 보고한다.
