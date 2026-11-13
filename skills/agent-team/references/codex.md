# Codex

공통 계약은 루트 SKILL.md를 따른다. Codex가 coordinator이거나 Herdr worker일 때만 읽는다.

## 네이티브 팀

- 현재 세션에 노출된 subagent 생성, 메시지, 대기 도구와 스키마를 사용한다. CLI 버전이나 모델 이름만 보고 팀 도구가 있다고 가정하지 않는다.
- coordinator 모델을 유지한다. `orchestrator`는 현재 lead 세션의 모델을 사용하며 별도 worker ID로 변환하지 않는다. `implementation`은 현재 계정의 중간 코딩 모델, `implementation-complex`는 고성능 모델, `research`는 `pick_worker_model.py --harness codex`가 고른 모델로 변환한다. `spawn_agent` 설명이 나열한 override 목록에 없는 ID는 사용하지 않는다. `reasoning_effort`는 비워 기본값을 쓴다. 프록시 프로필처럼 계정 캐시와 다른 카탈로그로 띄운 세션에서는 설명의 override ID를 `--available`로 넘긴다. 스크립트는 `CODEX_MODEL_CATALOG_JSON`이 가리키는 카탈로그가 있으면 그것을 우선 읽는다. 지정 모델이 provider/catalog 오류로 거부되면 같은 역할의 현재 허용 ID를 한 번 시도하고, 없으면 `model`을 생략해 상속 fallback을 한 번 수행하며 실제 사용 모델과 사유를 기록한다.
- 컨텍스트를 상속하지 않는 worker에는 목표, 파일, 근거, 금지 작업을 빠짐없이 전달한다. 컨텍스트 상속 여부와 모델 변경 조건은 현재 생성 도구의 제약을 따른다.
- 기본 작업 경로는 lead의 작업용 worktree다. worker에게 자동 worktree 생성을 맡기지 않는다. Git 변경은 브리프가 명시한 전용 worktree의 단독 worker에게만 맡긴다.
- 수정과 추가 확인은 기존 worker 식별자로 보낸다. 반환된 thread/session ID와 결과 경로를 실행 기록에 남긴다.
- 도구에 종료 기능이 없으면 종료됐다고 보고하지 않는다. 실행 중인 작업이 끝났는지 확인하고 세션 상태를 기록한다.

## Herdr worker

- `herdr agent start`의 대상 kind는 `codex`다.
- `codex --help`에서 현재 모델과 작업 경로 인자를 확인하고, 허용된 인자만 Herdr의 `--` 뒤에 전달한다.
- `codex exec`를 관찰 가능한 Herdr pane의 대체 경로로 사용하지 않는다.
- 맨몸 `codex` 명령, alias, 설정, 훅은 바꾸지 않는다. 프록시 경로의 문제는 `~/scripts`의 `codex-proxy` 래퍼 안에서 푼다.

## 교차검증 (보안, 배포 감사)

- 적용 범위는 보안 감사, 배포 감사, 사용자가 교차검증을 명시한 점검뿐이다. 그 밖의 점검에서 교차검증이 도움이 될 것 같으면 실행하지 않고 제안만 한다.
- 영역별 하위 세션 N개와 `codex exec -s read-only --skip-git-repo-check -C <dir> -o <out.md> < <prompt.txt>` 2개(backend/frontend)를 함께 돌린다. read-only 샌드박스는 권한 프롬프트가 뜨지 않아 병렬 실행 중 연쇄 취소 위험이 없다.
- 프롬프트에는 `file:line` 근거, 추정 표시, 거짓양성 회피, TOP 5 우선순위를 요구한다.
- 양쪽이 합의한 발견은 high-confidence로 표시하고 dedup해 단일 리포트로 합친다. 독립 엔진 교차검증은 한쪽이 놓친 발견을 잡아 주므로(실측: Codex가 Claude 쪽이 놓친 무인증 API와 낡은 색인을 잡았다) 이 범위에서는 생략하지 않는다.

## codex exec 호출 함정

- Python 등에서 `codex`를 subprocess로 부를 때는 `stdin=DEVNULL`을 준다. 빠지면 멈춘다. 다른 도구도 같은 패턴이다.
- 동시 호출은 3개 이하로 한다. 6개를 동시에 부르면 간헐적으로 시간 초과가 난다.
- 이미지 생성 프롬프트에는 "파일 시스템 검색 금지, 한 번 생성 후 종료"를 적는다. 없으면 Codex가 자기 출력물을 `find`로 찾다가 320초 시간 초과가 난다.
