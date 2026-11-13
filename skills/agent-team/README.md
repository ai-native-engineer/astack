# Agent Team

Claude Code, AGY, Codex, OMP의 작업 위임과 결과 회수를 관리하는 공용 스킬이다. 개발 계획과 품질 기준은 선택한 개발 스킬에 두고, 이 스킬은 worker의 범위, 실행 경로, 결과, 종료를 연결한다.

## 구성

- `SKILL.md`: 대상 하네스, 공유 worktree, 파일 소유권, lead의 Git 책임, 위임 계약.
- `references/herdr.md`: 시작 확인, 병렬 prompt wait, 재전송 판단, 소유한 pane만 종료.
- `references/run-lifecycle.md`: run/worker/turn 식별, 결과 파일, 재개와 정리.
- [경량 평가 케이스](tests/eval-cases.json): 공유 폴더, 시작/완료 구분, 재전송, 하네스 선택, 자원 소유권, worker 모델 선택의 회귀 사례.

## 검증

정적 검사는 skill-manager의 portable schema, authoring, description, reference 검사를 사용한다.

경량 평가는 eval-cases의 prompt를 새 컨텍스트에 주고 행동 계획만 받는다. 실제 worker, Git 변경, pane 제어는 실행하지 않는다. 같은 대표 사례를 기존 스킬, 새 스킬, 스킬 없는 조건에서 비교하고 각 결과에 추측한 지점을 포함한다. 각 하네스에서 수행한 범위를 구분한다.

- 지침을 제공한 시나리오 평가: 판단과 라우팅 문구 확인.
- 스킬 발견과 명시/자동 호출: 각 CLI의 실제 사용자 스킬 경로에서 별도 확인.
- 실제 위임: worker 시작, 결과 회수, 종료를 해당 transport에서 직접 확인.

앞선 단계의 성공을 뒤 단계의 증거로 쓰지 않는다. 상세 실행 결과는 PR 검증 기록에 남긴다.

## 근거

- [Herdr agent automation](https://herdr.dev/docs/agent-automation/): start의 준비 확인, prompt wait의 활동 확인, 독립 wait의 즉시 반환 가능성, timeout 이후 중복 제출 방지.
- [Herdr agents](https://herdr.dev/docs/agents/): 지원 agent, 상태 감지 한계, idle 이후 남을 수 있는 background 작업.
- 설치된 `agy --help`, `agy agent --help`, `agy models`: agent 목록 조회와 모델 선택을 worker 생성과 구분.
- 초기 역할 분리 참고: [Tmux + Fable](https://www.youtube.com/watch?v=wCSPgHpcxdc), [open-agent-teams](https://github.com/AI-Builder-Club/skills/tree/main/skills/open-agent-teams).
- worker 전달문 참고: [Prompting Claude Sonnet](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5).

모델의 고정 가격 비율이나 특정 버전이 더 우수하다는 문구를 실행 정책에 넣지 않는다. 모델은 실제 런타임에서 확인하고, Zellij 등 은퇴한 실행 어댑터는 Git 이력으로 보존한다.

worker 모델 선택 기준의 근거: 이 환경의 세션 로그 집계에서 조사성 위임의 절반이 `model` 미지정으로 lead 모델(opus)을 상속했고, 가장 싼 모델을 명시한 경우는 7%였다. 스크립트는 "같은 세대 안에서 가장 싼 모델"을 고른다. 세대 판정은 계열별 최신 출시와 공급자 최신 출시 대비 180일이며, 두 세대 전 소형 모델은 싸도 후보에서 뺀다. 무료 티어와 프론티어 랩 밖 모델은 품질을 가격으로 판단할 수 없어 기본 제외한다.
