---
name: data-go-kr
description: 한국 공공데이터포털(data.go.kr)의 임의 API를 작업 단위로 검색→활용신청 안내→호출하는 범용 스킬. API당 고정 스킬이 아니라 long-tail 전체를 온디맨드로 다루고, 성공한 호출은 레시피로 캐시해 다음부터 직행. 호출은 사용자 키(DATA_GO_KR_API_KEY) 직접, 프록시 없음. Use when user says "공공데이터", "공공 API", "data.go.kr", "나라장터"(입찰/낙찰/계약 조회), "국민연금 사업장", "사업자등록 상태조회", "건축물대장", or any task needing Korean government open APIs.
argument-hint: "[할 작업]"
license: MIT
---

# data-go-kr — 공공데이터포털 범용 호출

인자(또는 대화 맥락)는 **할 작업**이다 (예: "○○회사 나라장터 낙찰 이력 조회"). API 이름이 아니라 작업에서 출발해, 아래 루프로 푼다.

## 멘탈 모델

**레시피 캐시 우선, 없으면 검색→호출→레시피 적립.** 한 번 성공한 API는 `references/recipes/`에 호출 레시피로 남겨, 같은 작업의 두 번째부터는 파라미터 파악 비용 없이 직행한다. 쓸수록 큐레이션이 쌓이는 구조.

## 워크플로

레시피 검색·저장의 정본 경로는 `~/.agents/skills/shared/data-go-kr/references/recipes/` (심볼릭 링크 말고 이 원본 기준).

1. **레시피 탐색** — 작업의 도메인 키워드(기관·데이터명)로 `rg -il "<키워드>" ~/.agents/skills/shared/data-go-kr/references/recipes/` 검색.
2. **레시피 있음** → 키 확인 후 레시피대로 호출. 인코딩·에러 처리는 `references/call-patterns.md`.
3. **레시피 없음** → `references/search-and-apply.md` 절차로 API 검색 → 후보 선정 → 상세 페이지에서 스키마 추출 → 호출 시도.
   - **미신청/미승인 에러**가 떨어지면 활용신청 딥링크를 사용자에게 전달하고 멈춘다 (절차·딥링크 형식은 search-and-apply.md §3).
4. **첫 호출 성공 시 레시피 저장** — 위 정본 경로에 `_TEMPLATE.md` 형식으로, 작업을 끝내기 전에 반드시. 다음 사용자가 곧 나다.

## 키 규칙 (불변)

- 키 소스 우선순위: ① **`agents-env`가 설치돼 있으면 주입 호출** — `agents-env run DATA_GO_KR_API_KEY -- <명령>` 형태로 실행하고, 레시피 예시의 `$DATA_GO_KR_API_KEY` 자리를 `{{DATA_GO_KR_API_KEY}}`로 바꾼다. 키가 컨텍스트·명령줄·출력에 노출되지 않는다(주입 동작 검증 2026-06-11). 스토어에 키가 없으면(`agents-env get DATA_GO`) 사용자에게 `agents-env edit`로 추가를 요청한다 — 에이전트는 전역 스토어에 쓸 수 없다. ② 환경변수 `DATA_GO_KR_API_KEY` ③ cwd `.env`. 셋 다 없으면 발급 안내(data.go.kr 로그인 → 마이페이지 → 일반 인증키) 후 멈춘다.
- **Decoding 키 기준**으로 저장·사용한다. 호출 시 인코딩은 도구(curl `--data-urlencode`)에 맡긴다 — 이중 인코딩이 최다 빈도 함정.
- 키 평문을 출력·레시피·로그에 적지 않는다. 항상 `$DATA_GO_KR_API_KEY`(또는 `{{DATA_GO_KR_API_KEY}}`) 표기로.

## 안전선

- 활용신청을 대신 해줄 수 없다(로그인 세션 필요) — 링크 전달까지가 스킬의 책임.
- "검색 결과 없음"을 "API 없음"으로 단정하지 않는다 — 키워드를 바꿔 2~3회 재검색 후에 없다고 보고한다.
- 응답의 개인정보(대표자명·주소 등)는 작업에 필요한 필드만 다룬다.

## References

| 언제 | 읽을 것 |
|---|---|
| API 검색·활용신청·스키마 추출 | `references/search-and-apply.md` |
| 호출 직전 (인코딩·페이징·에러코드) | `references/call-patterns.md` |
| 레시피 작성·갱신 | `references/recipes/_TEMPLATE.md` |
