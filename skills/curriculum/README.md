# Curriculum 스킬 (maintainer README)

> 플러그인 배포 루트: `${CLAUDE_PLUGIN_ROOT}/skills/curriculum/` (canonical의 sanitize 미러).
> 편집 착수 시 `skill-manager`(update 모드) + `authoring-principles.md` 선독 절차를 따른다.
> 이 파일은 사람(maintainer)용이다. 사고 기록, 설계 근거, 출처는 여기에 둔다 - SKILL.md와 코드는 AI가 읽는 파일이라 출처/사고 정보를 넣지 않는다(skill-manager 규칙).

## 설계 의도

결정론적 검사는 산문보다 **스크립트/exit-code**로 강제한다. 판단과 프로젝트별 선택만 문서 지침으로 둔다.

게이트는 반복 가능한 누락과 구조 오류만 검사하고, 품질 판단은 검수 하네스와 사용자 승인에 남긴다.

## 구조 개요

- **6 Phase**: 설계 -> 맥락수집 -> 자료조사 -> 자료생성 -> 검수/개선 -> 노션반영 (어느 단계부터든 진입). Notion을 발행 채널로 쓰지 않는 프로젝트는 Phase 6을 생략한다. 절 번호(`3-x`, `4-x`)는 교차 인용 안정 앵커라 Phase 번호와 독립.
- **게이트 스크립트** `scripts/curriculum_gate.py`: 서브커맨드 `explore` / `gate-candidates` / `verify-pages` / `verify-media` / `review-draft` / `gate-review` / `status`.
- **반영 스크립트** `scripts/notion_reflect.py`: 검수 게이트를 재실행하고, 로컬 이미지 upload-id 계약을 확보하지 못하면 본문 update 전에 fail-closed한다.
- **선택적 호스트 훅**: 지원하는 런타임에서는 Notion 쓰기 전 충실도 검사를 추가한다. 훅 유무와 무관하게 본문 옆 fidelity sidecar 검사는 작업 절차로 유지한다.
- **보조 스크립트**: `format_scan.py`(2형태 원칙 lint), `fidelity_lint.py`(충실도 수동 검사), `self_check.py`(게이트 회귀 자가 점검 - maintainer용).
- **references** 15개 + `templates/` 1개.

## 게이트 원장 (왜 각 게이트가 있나)

SKILL.md 본문은 거시 라우팅만 둔다. 각 게이트가 막는 실패모드는 여기에 둔다.

| 게이트 | 막는 실패모드 | 성공 기준 |
|---|---|---|
| `explore` | 기존 검증 자료를 안 보고 새로 지어냄 | 프로젝트가 선언한 모듈 DB/Notion/로컬 소스를 함께 탐색. 기본 후보 10개, 범위에 따라 명시적으로 조정 |
| `gate-candidates` | 검색 파일만 만들고 원문을 안 본 채 제작 시작 | `[x]` 체크 + 근거 + 최선 후보를 요구 |
| `verify-pages` | page-id를 추정해 단정/반영 | 401(토큰 무효), 403(권한/capability), 404(없음 또는 미공유)를 구분 |
| `verify-media` | 텍스트만 이식하고 이미지/첨부를 빠뜨림 | 원본 작업본 vs 교안 미디어 ref 대조 |
| `review-draft` | 신호 없는 섹션, 이미지 없는 산출물 섹션, dense-prose, AI slop 표기 | 고신호(HIGH) 0이면 exit 0. 표기/구조 검출은 HIGH(frontmatter, aside, 비표준색)와 warn(소수 번호, 콜아웃 이모지)으로 나뉜다 |
| `gate-review` | 다른 작업의 후보/리포트를 재사용하거나 기계 위반을 남김 | 현재 교안·후보 binding + 리포트 형식 + 고신호 0 + `format_scan` 0을 반영 전제로 |
| `status` | 현재 산출물과 다음 검사를 놓침 | archives 제외 산출물과 다음 실행할 게이트 가시화. Phase 통과 판정은 하지 않음 |
| `notion_reflect` 내장 게이트 | 잘못된 페이지나 stale 페이지에 미검수 교안을 반영 | 단일 page/md pair + 기대 title/parent/last-edited + 현재 candidates/report binding을 필수 검증. 우회 없음 |
| 충실도 검사 | 소스에 없는 net-new 블록을 Notion에 씀 | `.fidelity.json` sources 선언 + `scripts/fidelity_lint.py`. 임계값 재정의는 허용하지 않음 |

공통 규칙: 게이트 통과는 exit 0 + 응답에 실행 명령, exit code, 핵심 출력 라인 인용으로만 인정한다.

## 향후 스크립트화 후보 (산문인데 기계 강제 가능, 미구현)

- **빈 이미지/staging-link 검사** (중간): notion-sync 4-3 round-trip의 빈 이미지 `![]()`와 테스트 링크 `<page url=`를 review-draft 패턴으로 추가.
- **module-bank 적재 검증 게이트화** (중간): "적재했다 단정 금지, data-source query로 행 실재 + 속성값 확인" + "원본 미디어 ref 전수 보존"을 verify-media 재사용 또는 전용 게이트로.
- **코드펜스 한글 비-text 검출** (낮음, 추정): 복붙 펜스가 한글인데 언어가 text 아니면 노션이 오하이라이팅. 휴리스틱 가능성 검토.

## 미착수 설계 항목

- **리서치/검수 서브에이전트 역할 경계 명문화**: 스크립트(결정, 전수 대조) vs 서브에이전트(판단, 비평) 경계를 references에 더 구체화. 대부분 이미 분리됨(notion-explorer는 좌표, curriculum-reviewer는 검수).
- **노션 템플릿 감독 가드**: 템플릿 골격은 자동화하지 않고 사용자가 직접 감독한다. 유형은 고정 목록 없이 프로젝트별 사용자 지시로 받는다(AI 미감 재구성 금지).
