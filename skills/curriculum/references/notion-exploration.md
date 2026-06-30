# 노션 탐색 절차 (읽기 전용, 좌표 찾기 전용)

ntn CLI로 노션에서 **"무엇이 어디에 있는지"(page-id, 경로, DB 구조)만** 찾는 절차. curriculum 딥 탐색의 좌표 찾기, 4-R 베이스 라우터 진입 전 page-id 정체성 + `last_edited` 신호 수집에 쓴다. **좌표만 찾고 내용은 판정하지 않는다** - 검수/사실 검증/품질 비평/개선은 review.md 검수 하네스 몫이고, 이 절차로 하면 안 된다(탐색 전용이라 그럴듯한 오정정을 낸다).

이 reference는 두 런타임이 공유한다. Claude Code는 `notion-explorer` 서브에이전트(조직 플러그인 `agents/`, 도구 격리 haiku)가 이 절차를 따른다. Codex는 아래 "Codex에서 실행"으로 같은 절차를 돈다.

## 인증 - 첫 호출부터 성공시키는 순서

워크스페이스 UUID (전체를 그대로 넣는다. **prefix, 축약은 매칭 실패**):

| 축약 | 워크스페이스 | UUID |
| --- | --- | --- |
| `<lecture-ws-token>` | 강의자료 워크스페이스 | `<lecture-workspace-id>` |
| `<org-ws-token>` | 조직 워크스페이스 | `<org-workspace-id>` |
| `me` | 개인 Space | `<my-workspace-id>` |

**1차 (기본)**: keychain 토큰으로 호출.
```bash
NOTION_WORKSPACE_ID=<lecture-workspace-id> ntn api /v1/search -d '{"query":"키워드","page_size":10,"sort":{"direction":"descending","timestamp":"last_edited_time"}}'
```

**2차 (1차가 `Failed to fetch token from keychain`)**: 화면 잠금 등으로 keychain이 막힌 헤드리스 상황. `NOTION_API_TOKEN` env로 주입한다. curriculum 강의자료는 lecture-ws=`<lecture-ws-token>`, org-ws=프로젝트 지정 조직 워크스페이스 토큰를 쓴다. `<company-ws-token>` 토큰은 회사 데이터용이라 curriculum 강의자료 탐색, 반영에 쓰지 않는다. integration 토큰은 연결된 페이지, DB만 보이므로 404면 태그나 공유 범위가 틀린 것이다.
```bash
agents-env run NOTION_API_KEY@<lecture-ws-token> -- sh -c 'NOTION_API_TOKEN={{NOTION_API_KEY}} NOTION_WORKSPACE_ID=<lecture-workspace-id> ntn api /v1/search -d '"'"'{"query":"키워드","page_size":10}'"'"''
```

`No auth token found`는 미인증이 아니라 UUID prefix 오류 신호 - `ntn login` 시키지 말고 전체 UUID부터 확인한다.

**워크스페이스 검증**: 어디에 붙었는지 의심되면 `NOTION_WORKSPACE_ID=<uuid> ntn api /v1/users/me`로 `workspace_name`을 본다. `ntn doctor`는 `NOTION_WORKSPACE_ID`를 무시하고 config 기본값만 보니 전환 검증엔 쓰지 않는다.

## 탐색 절차

1. **search**: `/v1/search`로 후보 page/DB를 최신 수정순 10개. 키워드는 띄어쓰기 변형도 한 번 더(`MBTI 테스트`/`MBTI테스트`). `/v1/search`는 페이지/DB **제목** 위주라 DB 안의 개별 행(항목)은 안 잡힐 수 있다 - 특정 DB의 행을 찾는 거면 search 0건을 "없음"으로 단정 말고 3번 datasources query로 전수한다.
2. **read**: 후보의 본문은 `ntn pages get <id>`(Markdown round-trip). 하위 블록 트리는 `ntn api /v1/blocks/<id>/children`.
   - **반영 진입 신호(요청받았을 때만)**: 메인이 베이스(로컬 vs 노션)를 정하려면 후보마다 `ntn pages get <id> --json`(또는 search 응답)의 `last_edited_time`과 `last_edited_by.id`가 필요하다. **봇/사람은 여기서 단정하지 말고 id를 raw로 넘긴다** - `/v1/users/<id>`로 임의 유저의 type을 조회하면 403(PAT는 자기 자신만)이라 봇/사람을 못 가리고, 연동 봇이 여러 개라 "내 봇 id와 다르면 사람"도 틀린다. 최종 판정은 자기 반영 봇 id를 아는 메인이 한다. 단순 좌표 찾기면 생략한다.
3. **DB 전수**: data_source 안 항목을 빠짐없이 봐야 하면 먼저 `ntn datasources resolve <db-id>`로 DB의 data_source id를 얻고(database id와 data_source id는 다른 객체), `ntn datasources query <ds> --limit 1000`. **`--limit`은 그 수에서 자른다** - 작게 주면 "없음"으로 오판하니 존재 여부 판단엔 크게(1000) 주거나 `--start-cursor`로 끝까지. 제목이 같아도 다른 DB가 공존하니(같은 워크스페이스에 "기존"/"리뉴얼" 동명 DB 등) resolve한 data_source id를 섞지 않는다. 0건/404면 빈 DB로 단정 말고 id 종류, 워크스페이스 일치부터 의심.
4. 목표에 닿는 것만 추린다. 무관 페이지(키워드 부분일치 오탐, 일반 지식 페이지, 빈 페이지)는 버린다.

## 반환 형식 (좌표만 - 본문 덤프 금지)

```
workspace: <lecture|org|my>
목표: <받은 목표 요약>
auth: <1차 keychain / 2차 agents-env@tag 중 무엇으로 성공했는지>
found:
  - title: <페이지 제목>
    id: <page-id (하이픈 포함 전체)>
    type: <page|database>
    path: <상위 페이지/DB 경로 알면>
    last_edited: <last_edited_time + last_edited_by.id (raw, 봇/사람 단정 말 것) - 반영 신호 요청 안 받았으면 생략>
    note: <목표 관점에서 한 줄 - 무엇이 들어있는지>
구조: <DB, 하위 페이지 트리가 목표면 들여쓰기 트리로>
miss: <못 찾은 것 / 비어있던 것>
denied: <접근 막힌 page-id - 404=존재 안 함/환각, 401/403=미공유(다른 tag면 보일 수 있음)로 구분해 적는다>
```

찾은 page-id는 **하이픈 포함 전체**로 준다(메인이 그대로 read/update에 씀). 이 page-id는 ntn search 기반 **후보**다 - 메인이 파괴적 쓰기 전엔 직접 REST(`verify-pages`)로 실존을 재확인하는 전제로 넘긴다(ntn 읽기는 크로스 오염 실측이 있다). 본문 전체가 필요하면 "본문은 `ntn pages get <id>`로 메인에서 받으세요"라고만 안내하고 여기 붙이지 않는다 - 컨텍스트 절약이 이 탐색의 목적이다.

## 오판 방지 (탐색 함정)

- **토글/콜아웃 안쪽은 재귀로 본다.** `ntn pages get`은 평면 마크다운으로 내보내지만 노션엔 토글/콜아웃의 자식 블록이 중첩으로 있다. 블록/이미지 개수나 "이 내용이 있나"를 top-level만 보고 판단하면 누락한다(실측: 토글 안 10장을 못 세 "7장 누락" 오판). 개수, 존재 판단은 토글 경계 안쪽까지.
- **같은 내용이 여러 페이지에 보이면 synced_block일 수 있다** - 중복이 아니라 한 원본을 여러 페이지가 공유하는 것. 블록 `synced_from`으로 원본/참조본을 가른다.
- **DB가 보여도 개별 행 페이지는 404일 수 있다**(DB 공유는 행 공유가 아님, 또는 integration tag 미연결). page-id는 `ntn pages get`이 실제로 성공한 것만 "존재"로 확정해 반환한다. 404면 추측 id를 주지 말고 `miss`에 정직하게 적는다.

## 딥 탐색 explore 게이트와의 경계

curriculum 딥 탐색 게이트(authoring 3-0 / review 0절)의 노션 전수는 **raw search JSON**(`ntn api /search > notion-search-*.json`)을 `curriculum_gate.py explore --notion-hits`에 넘기는 구조다. 이 절차(요약 좌표 반환)와 인터페이스가 다르니, explore 게이트엔 이 탐색을 쓰지 않고 `ntn /search`로 직접 떠 넘긴다.

## Codex에서 실행

Codex CLI엔 Claude Code 서브에이전트가 없으니, `codex exec -s read-only`로 이 절차를 돈다(read-only 샌드박스가 쓰기를 막아 도구 격리를 대신한다). 프롬프트에 이 reference 경로를 읽혀 위 인증/탐색 절차를 따르게 하고, 반환은 같은 좌표 형식으로 받는다. ntn 인증은 위 1차/2차 동일.

## 하지 않는 것

- create / update / trash / PATCH 등 모든 쓰기. 좌표만 넘기고 편집은 호출자가 한다.
- 자료 검수, 사실 검증, 품질 비평, 개선, 내용 요약. 좌표를 찾을 뿐 내용은 판정하지 않는다(검수는 review.md 하네스).
- 본문 원문을 그대로 반환 (요약, 경로, 구조만).
- `ntn --help` / `ntn doctor` / 광범위한 `find ~/.config` 로 시작 (위 검색/읽기 명령부터 바로 쓴다).
