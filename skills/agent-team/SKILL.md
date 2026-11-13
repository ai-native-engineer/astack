---
name: agent-team
description: "Use for: Delegate work to subsessions on a user-named or role-default model, and coordinate workers across Claude Code, AGY, Codex, and OMP for team, parallel-agent, Herdr, or cross-harness requests. Not for overlapping edits, lead-only steps (deletion, external sends, merges), or tool explanations."
---

# Agent Team

Lead는 작업 분해, 판단, 통합을 맡고 worker는 한정된 범위를 실행한다. 개발 계획과 검토 기준은 작업에서 선택한 개발 스킬을 따르고, 이 스킬은 위임과 결과 회수를 맡는다.

Hermes가 lead로 Herdr의 Codex/Claude Code worker를 제어할 때도 같은 작업 계약을 쓴다. 기기와 세션 선택, 창 제어, worker 시작과 복구는 공용 `herdr` 스킬을 따르고, Hermes 설정과 배포는 `macmini-ops`가 맡는다.

## 실행 경로

- 대상은 Claude Code, AGY, Codex, OMP다. Grok은 설치 상태와 관계없이 이 스킬의 선택, 실행, 대체 worker 대상에서 제외한다. 설치 제거는 하지 않는다.
- 현재 coordinator의 하네스, 모델, 노출된 팀 도구를 확인한다. 모델 이름으로 하네스를 추정하지 않는다.
- 같은 하네스의 네이티브 팀 도구를 우선 사용한다. 다른 하네스로 위임하거나 관찰 가능한 pane이 필요하면 Herdr를 선택한다.
- 선택한 하네스 지침만 읽는다. 다른 하네스로 위임할 때는 대상 하네스와 Herdr 지침을 함께 읽는다.
- 실행 도구가 없으면 지원되지 않는 경로를 만들지 말고 lead가 직접 처리하거나 필요한 실행 환경을 알린다.
- 사용자가 worker 하네스를 지정했으면 미지원이나 사용량 제한을 이유로 다른 하네스를 조용히 실행하지 않는다. 대체가 필요하면 선택을 확인하고, lead가 진행한 일은 지정 worker의 결과로 보고하지 않는다.

| 조건 | 읽을 것 |
|---|---|
| 모든 worker 위임 | [Worker Model Routing](references/model-routing.md) |
| Claude Code가 lead 또는 worker | [Claude Code](references/claude-code.md) |
| Codex가 lead 또는 worker | [Codex](references/codex.md) |
| OMP가 lead 또는 worker | [OMP](references/omp.md) |
| AGY가 lead 또는 worker | [AGY](references/agy.md) |
| Herdr pane으로 위임 | [Herdr](references/herdr.md) |
| 위임 시작, 결과 회수, 재개, 종료 | [실행 기록과 회수](references/run-lifecycle.md) |

## 작업과 소유권

- 작업은 기본적으로 worker에게 위임한다. lead가 직접 하는 일은 브리프를 쓰기 위한 짧은 읽기, 결과 확인, 삭제, 외부 발송, 머지와 기본적으로 lead가 맡는 Git 변경으로 한정한다. 작은 수정과 순차 의존 작업도 lead가 하지 않고 한 worker에게 이어서 맡긴다.
- worker를 여럿 만드는 조건은 독립 작업이 여러 개이고 전달 비용보다 병렬 실행의 이득이 클 때다. 같은 파일을 겹쳐 고치는 병렬 worker는 두지 않는다.
- 연관 작업과 후속 작업은 맥락을 가진 기존 worker에 잇고, 더 필요 없는 worker는 보관하거나 종료한다. 방법은 [실행 기록과 회수](references/run-lifecycle.md)의 「하위 세션 잇기와 보관」을 따른다.
- 기본값은 기존 작업용 worktree 공유다. worker마다 새 worktree를 만들지 않는다. 독립 브랜치나 별도 구현 실험이 필요할 때만 lead가 추가 worktree를 준비한다.
- 읽기 전용 worker는 같은 폴더를 읽는다. 편집 worker는 담당 파일을 나누며, 같은 파일, 생성물, 잠금 파일을 바꾸는 작업은 순차로 처리한다.
- worker는 Git 상태와 diff를 읽을 수 있다. 기본적으로 stage, commit, branch 변경, fetch, merge, push와 worktree 생성/제거는 lead가 맡는다. 전용 worktree에서 혼자 일하는 worker에게는 브리프에 명시한 경우에만 그 브랜치의 stage, commit, push와 PR 생성을 맡긴다. 머지는 항상 lead가 한다.
- 삭제와 휴지통 이동, 외부 발송은 worker에게 맡기지 않는다. worker는 대상과 근거를 보고하고 lead가 사용자 승인 범위 안에서 실행한다.
- worker가 macOS GUI 앱을 띄울 때는 `open -g`로 실행해 사용자의 포커스를 뺏지 않는다. 반복 실행이 필요하면 lead가 허용 부수 효과에 실행 횟수 상한을 적는다. 맨 앞으로 나오는 앱 창은 사용자의 작업을 끊는다.
- worker는 하위 worker를 만들지 않는다. lead는 현재 모델을 유지한다.
- 사용자가 모델을 말했으면 그 값을 역할 기본값보다 먼저 쓴다. 값은 아래 모델 해석 규칙으로 하네스에 맞춘다.
- worker는 `model`이 아니라 역할을 먼저 배정한다. `orchestrator`는 lead 역할로 존재하며 현재 세션의 모델을 사용한다. `implementation`은 Sonnet, `implementation-complex`는 Opus, `research`는 현재 하네스의 같은 세대 최저가 capable 모델을 기본값으로 삼는다. 세부 변환과 fallback은 `references/model-routing.md`를 따른다.
- 모델 값은 worker를 실행하는 하네스의 현재 도구 스키마에서 해석한다. Claude Code alias를 Codex ID로, Codex ID를 Claude Code alias로 넘기지 않는다.
- 명시한 모델이 provider/catalog 오류로 시작 전에 거부되면 같은 역할의 하네스 호환 모델로 한 번 재시도하고, 호환 override가 없으면 `model`을 생략해 lead 모델 상속으로 한 번 fallback한다. 실제 모델과 fallback 사유를 실행 기록에 남긴다.
- 읽기 전용 `research` worker는 `python3 -I scripts/pick_worker_model.py --harness <하네스>`가 고른 모델을 쓴다. 이 스크립트는 그 하네스가 지금 띄울 수 있는 모델 중 같은 세대에서 가장 싼 것을 models.dev 가격으로 고르므로 지침에 모델 이름을 적지 않는다. effort는 낮추지 않고 하네스 기본값을 둔다.
- lead는 시작 전 기존 변경과 작업 경로를 기록하고, 통합 전 worker의 주장과 실제 diff, 검증 결과를 대조한다.

## 위임 계약

모든 위임에 다음 템플릿을 포함한다. 경로는 절대 경로로 적고 결과 예산은 숫자로 정한다.

```text
목표:
범위:
담당 파일:
작업 경로:
금지 작업: 담당 밖 편집, 브리프가 허용하지 않은 Git 변경, 삭제, 외부 발송, 하위 worker 생성
허용 부수 효과:
출력 형식:
결과 예산:
완료 조건:
실행 식별: run_id / worker_id / turn_id
결과 경로:
Obstacles:
```

- 편집 worker의 브리프에는 worktree 절대 경로를 적고, worker는 모든 편집과 명령에 그 경로를 쓴다. 기본 체크아웃은 실사용 경로이므로 건드리지 않는다.
- 결과는 결론, 담당 범위, 변경 파일, 실제 부수 효과, 검증 결과, Obstacles를 포함한다. 긴 원문 로그는 결과 파일에 두고 대화에는 요약과 경로를 반환한다.
- lead는 다른 worker에게 필요한 사실과 쟁점만 전달한다. 검증되지 않은 보고를 확정 사실로 넘기지 않는다.
- 시작은 보통 2~3명으로 제한하고 현재 런타임의 동시 실행 한도를 따른다. 권한 판단이 필요한 변경은 병렬 블록에 묶지 않는다.
- 사용량 제한이나 일시 오류가 반복되면 무한 재시도하지 않는다. 완료분을 보존하고 실제 실행 식별자로 재개한다.
- 결과가 잘렸거나 session이 유실됐으면 남은 범위를 새 worker에 전달한다. 이미 완료된 일을 다시 실행시키지 않는다.
