---
name: agent-team
description: "Use for: Coordinate independent workers across Claude Code, AGY, Codex, and GJC for explicit team, parallel-agent, Herdr delegation, or cross-harness requests. Not for sequential work, overlapping edits, or tool explanations."
---

# Agent Team

Lead는 작업 분해, 판단, 통합을 맡고 worker는 한정된 범위를 실행한다. 개발 계획과 검토 기준은 작업에서 선택한 개발 스킬을 따르고, 이 스킬은 위임과 결과 회수를 맡는다.

Hermes가 lead로 Herdr의 Codex/Claude Code worker를 제어할 때도 같은 작업 계약을 쓴다. 기기와 세션 선택, 창 제어, worker 시작과 복구는 공용 `herdr` 스킬을 따르고, Hermes 설정과 배포는 `hermes-ops`가 맡는다.

## 실행 경로

- 대상은 Claude Code, AGY, Codex, GJC다. Grok은 설치 상태와 관계없이 이 스킬의 선택, 실행, 대체 worker 대상에서 제외한다. 설치 제거는 하지 않는다.
- 현재 coordinator의 하네스, 모델, 노출된 팀 도구를 확인한다. 모델 이름으로 하네스를 추정하지 않는다.
- 같은 하네스의 네이티브 팀 도구를 우선 사용한다. 다른 하네스로 위임하거나 관찰 가능한 pane이 필요하면 Herdr를 선택한다.
- 선택한 하네스 지침만 읽는다. 다른 하네스로 위임할 때는 대상 하네스와 Herdr 지침을 함께 읽는다.
- 실행 도구가 없으면 지원되지 않는 경로를 만들지 말고 lead가 직접 처리하거나 필요한 실행 환경을 알린다.
- 사용자가 worker 하네스를 지정했으면 미지원이나 사용량 제한을 이유로 다른 하네스를 조용히 실행하지 않는다. 대체가 필요하면 선택을 확인하고, lead가 진행한 일은 지정 worker의 결과로 보고하지 않는다.

| 조건 | 읽을 것 |
|---|---|
| Claude Code가 lead 또는 worker | [Claude Code](references/claude-code.md) |
| Codex가 lead 또는 worker | [Codex](references/codex.md) |
| AGY가 lead 또는 worker | [AGY](references/agy.md) |
| GJC가 lead 또는 worker | [GJC](references/gjc.md) |
| Herdr pane으로 위임 | [Herdr](references/herdr.md) |
| 위임 시작, 결과 회수, 재개, 종료 | [실행 기록과 회수](references/run-lifecycle.md) |

## 작업과 소유권

- 독립 작업이 여러 개이고 전달 비용보다 병렬 실행의 이득이 클 때 팀을 만든다. 작은 수정, 순차 의존 작업, 단순 명령 실행은 lead가 직접 처리한다. 사용자가 특정 worker의 검토를 명시하면 한 건도 위임할 수 있다.
- 기본값은 기존 작업용 worktree 공유다. worker마다 새 worktree를 만들지 않는다. 독립 브랜치나 별도 구현 실험이 필요할 때만 lead가 추가 worktree를 준비한다.
- 읽기 전용 worker는 같은 폴더를 읽는다. 편집 worker는 담당 파일을 나누며, 같은 파일, 생성물, 잠금 파일을 바꾸는 작업은 순차로 처리한다.
- worker는 Git 상태와 diff를 읽을 수 있다. stage, commit, branch 변경, fetch, merge, push와 worktree 생성/제거는 lead가 맡는다.
- 삭제와 휴지통 이동, 외부 발송은 worker에게 맡기지 않는다. worker는 대상과 근거를 보고하고 lead가 사용자 승인 범위 안에서 실행한다.
- worker는 하위 worker를 만들지 않는다. 현재 모델을 유지하고, worker 모델은 해당 런타임에서 실제로 지원하는 모델 중 작업 난도와 비용에 맞춰 고른다.
- lead는 시작 전 기존 변경과 작업 경로를 기록하고, 통합 전 worker의 주장과 실제 diff, 검증 결과를 대조한다.

## 위임 계약

모든 위임에 다음 템플릿을 포함한다. 경로는 절대 경로로 적고 결과 예산은 숫자로 정한다.

```text
목표:
범위:
담당 파일:
작업 경로:
금지 작업: 담당 밖 편집, Git 변경, 삭제, 외부 발송, 하위 worker 생성
허용 부수 효과:
출력 형식:
결과 예산:
완료 조건:
실행 식별: run_id / worker_id / turn_id
결과 경로:
Obstacles:
```

- 결과는 결론, 담당 범위, 변경 파일, 실제 부수 효과, 검증 결과, Obstacles를 포함한다. 긴 원문 로그는 결과 파일에 두고 대화에는 요약과 경로를 반환한다.
- lead는 다른 worker에게 필요한 사실과 쟁점만 전달한다. 검증되지 않은 보고를 확정 사실로 넘기지 않는다.
- 시작은 보통 2~3명으로 제한하고 현재 런타임의 동시 실행 한도를 따른다. 권한 판단이 필요한 변경은 병렬 블록에 묶지 않는다.
- 사용량 제한이나 일시 오류가 반복되면 무한 재시도하지 않는다. 완료분을 보존하고 실제 실행 식별자로 재개한다.
- 결과가 잘렸거나 session이 유실됐으면 남은 범위를 새 worker에 전달한다. 이미 완료된 일을 다시 실행시키지 않는다.
