# Notion 탐색 절차 (읽기 전용 좌표 찾기)

Notion에서 page-id, 경로, DB 구조, `last_edited` 신호만 찾는다. 내용 검수, 사실 판정, 품질 비평, 수정은 [`review.md`](review.md) 하네스가 맡는다.

## 준비

- workspace id와 token tag는 프로젝트 `AGENTS.md`에서 읽는다.
- 인증, workspace 전환, keychain fallback은 `notion` 스킬의 `references/ntn-cli.md`를 따른다. 해당 스킬이나 `ntn`이 없으면 Notion 탐색을 실행하지 않는다.
- 전체 UUID를 사용하고 `/v1/users/me`로 실제 workspace를 확인한다.
- 좌표를 찾는 동안 create/update/trash/PATCH를 실행하지 않는다.

## 탐색 절차

1. **search**: `/v1/search`로 후보 page/DB를 최근 수정순으로 찾는다. 기본 `page_size`는 10이며 결과가 부족하거나 넓으면 범위에 맞게 조정한다.
2. **read**: 후보 본문은 `ntn pages get <id>`, 하위 블록은 `/v1/blocks/<id>/children`으로 읽는다.
3. **DB 전수**: DB 안의 행을 찾을 때는 `datasources resolve`로 data-source id를 얻고 pagination이 끝날 때까지 query한다.
4. **중첩 확인**: 토글, 콜아웃, synced block은 `has_children`을 따라 재귀 조회한다.
5. **정체성 확인**: 실제 read가 성공한 id만 후보로 반환한다. 401(토큰 무효), 403(권한/capability), 404(없음 또는 미공유)를 구분한다.
6. **반영 신호**: 요청받은 경우에만 `last_edited_time`과 `last_edited_by.id`를 raw로 반환한다. 봇/사람 판정은 호출자가 한다.

## 반환 형식

```text
workspace: <프로젝트 workspace 이름/id>
목표: <받은 목표 요약>
auth: <성공한 인증 방식, secret 값 제외>
found:
  - title: <페이지 제목>
    id: <하이픈 포함 전체 page-id>
    type: <page|database>
    path: <상위 페이지/DB 경로>
    last_edited: <요청받은 경우 raw time + editor id>
    note: <목표 관점 한 줄>
구조: <필요한 경우 들여쓰기 트리>
miss: <못 찾은 것>
denied: <401 토큰 무효 / 403 권한 부족 / 404 없음 또는 미공유>
```

본문 전체를 반환하지 않는다. 원문이 필요하면 호출자가 page-id로 직접 읽게 한다.

## 딥 탐색 explore와의 경계

`curriculum_gate.py explore --notion-hits`에는 요약 좌표가 아니라 `/search` 결과 JSON이 필요하다. 딥 탐색에서는 pagination을 끝까지 따라가 `has_more=false`를 확인한 완전한 결과를 프로젝트가 선언한 workspace별 파일로 저장해 넘긴다. Notion 소스를 쓰지 않으면 `--no-notion`을 명시한다.

## 에이전트 실행

사용 가능한 읽기 전용 서브에이전트가 있으면 이 절차와 반환 형식을 그대로 위임한다. 별도 서브에이전트가 없으면 메인 에이전트가 같은 read-only 절차를 실행한다. 런타임 내부 세션이나 중첩 CLI 실행에 의존하지 않는다.

## 하지 않는 것

- create/update/trash/PATCH
- 자료 검수, 사실 검증, 품질 비평, 개선
- 본문 원문 덤프
- search 0건만 보고 DB 행이 없다고 단정
- 축약 workspace id나 작은 `--limit`으로 전수 여부 단정
