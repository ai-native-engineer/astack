---
name: open-api
description: "Use for: Route Korean official APIs including data.go.kr, DART, KIPRIS, and NTIS for disclosures, patents, trademarks, R&D, procurement, and registries. Not for OpenAPI specifications, non-Korean APIs, Snowflake, or crawling."
argument-hint: "[할 작업]"
license: MIT
---

# open-api — 한국 공식/공공 API 라우터

인자(또는 대화 맥락)는 **할 작업**이다. API 이름부터 고정하지 말고, 작업에서 출발해 provider와 레시피를 좁힌다.

## 멘탈 모델

**레시피 캐시 우선, 없으면 provider 선택 → 공식 문서/신청 → 호출 → 레시피 적립.** 이 스킬은 data.go.kr, opendart.fss.or.kr, plus.kipris.or.kr, ntis.go.kr을 한 작업 단위로 라우팅한다.

## 워크플로

1. **레시피 탐색** — 작업 키워드로 `${CLAUDE_PLUGIN_ROOT}/skills/open-api/references/recipes/`를 먼저 검색한다.
2. **provider 선택** — 애매하면 `references/provider-routing.md`를 읽고 provider 후보를 1~2개로 줄인다.
3. **provider 세부 로드** — 선택한 provider 파일과 `references/call-patterns.md`를 읽고 키·인코딩·페이징·에러를 맞춘다.
4. **레시피 없음** — `references/search-and-apply.md`로 공식 API 검색, 신청 상태 확인, 스키마 추출, 첫 호출을 진행한다.
5. **첫 성공 호출 저장** — 새 레시피는 아래 표의 `recipe dir`에 `_TEMPLATE.md` 형식으로 저장한다. 기존 레시피를 고쳐 성공시킨 경우에는 그 파일을 갱신한다.

## 키 규칙

| domain/provider | recipe dir | 기본 키 이름 |
|---|---|---|
| data.go.kr | `data-go-kr` | `DATA_GO_KR_API_KEY` |
| opendart.fss.or.kr (DART) | `dart` | `API_K_DART` |
| plus.kipris.or.kr (KIPRIS) | `kipris` | `KIPRIS_API_KEY` |
| ntis.go.kr (NTIS) | `ntis` | `NTIS_API_KEY` |

- 키는 provider별로 분리한다.
- 호출은 가능하면 `agents-env run <KEY_NAME> -- <명령>`으로 주입한다.
- 키 평문은 출력·레시피·로그에 남기지 않는다.
- 레시피 예시는 `$KEY_NAME` 또는 `{{KEY_NAME}}` placeholder만 쓴다.

## 안전선

- "검색 결과 없음"을 "API 없음"으로 단정하지 않는다. provider와 키워드를 바꿔 2~3회 재검색한 뒤 한계로 보고한다.
- 개인정보·민감정보는 작업에 필요한 필드만 다룬다.

## References

| 언제 | 읽을 것 |
|---|---|
| provider 선택 | `references/provider-routing.md` |
| 호출 직전 공통 규칙 | `references/call-patterns.md` |
| 신규 API 검색·신청·스키마 추출 | `references/search-and-apply.md` |
| data.go.kr | `references/providers/data-go-kr.md` |
| data.go.kr 호출 직전 (인코딩·페이징·에러코드) | `references/providers/data-go-kr-call-patterns.md` |
| data.go.kr 신규 API 검색·활용신청·스키마 추출 | `references/providers/data-go-kr-search-and-apply.md` |
| opendart.fss.or.kr / DART | `references/providers/dart.md` |
| plus.kipris.or.kr / KIPRIS | `references/providers/kipris.md` |
| ntis.go.kr / NTIS | `references/providers/ntis.md` |
| 레시피 작성·갱신 | `references/recipes/_TEMPLATE.md` |
