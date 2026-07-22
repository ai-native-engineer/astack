---
name: agent-team
description: "Orchestrates independent work with a strong lead and lower-cost persistent workers in Claude Code, Codex, or observable Zellij panes. Use when users invoke agent-team or say 에이전트 팀, 팀으로 해줘, 병렬로 맡겨, Zellij로 위임, or 상위 모델이 하위 모델에 위임. Do NOT use for routine, sequential, same-file, or single-step tasks."
argument-hint: "[task]"
---

# Agent Team

강한 모델은 판단과 통합을 맡고, 저렴한 모델은 독립 실행을 맡긴다. 현재 요청과 호출 인자를 팀의 목표로 사용한다.

## 런타임 라우팅

1. 위임 전에 현재 coordinator 런타임을 확인한다.
2. Claude Code에서는 [Claude Code 지침](references/claude-code.md)만 읽는다.
3. Codex에서는 [Codex 지침](references/codex.md)만 읽는다.
4. 다른 런타임의 reference는 읽지 않는다. 모델명과 팀 도구가 섞이면 잘못된 실행 표면을 선택한다.
5. 예외: 사용자가 Zellij를 요청하거나 현재 런타임에 없는 worker 모델명·harness를 지정하면 cross-harness 위임이다 — 모르는 모델명을 "없는 모델"로 단정하기 전에 다른 harness reference의 모델 절에서 확인하고, 해당 reference와 [Zellij 지침](references/zellij.md)을 읽는다.

## 공통 계약

- 서로 독립적으로 진행할 작업이 2개 이상일 때만 팀을 만든다.
- 순차 의존, 같은 파일 편집, 작은 수정은 lead가 직접 처리한다.
- 팀을 쓰지 않으면 이유를 한 줄로 알리고 작업을 계속한다.
- lead가 요구사항 해석, 작업 분해, 결과 통합, 테스트, 최종 diff 검증을 직접 수행한다.
- worker에게 하위 worker 생성을 허용하지 않는다.
- 모든 위임 프롬프트에 다음 템플릿을 그대로 포함한다.

```text
목표:
범위:
출력 형식:
결과 예산:
완료 조건:
담당 파일:
Obstacles:
```

- worker는 원문 로그 대신 결론, 변경 파일, 검증 결과, Obstacles를 반환한다.
- lead는 worker 결과를 다른 worker에게 전달할 때 원문 대신 필요한 사실과 쟁점만 요약한다.
