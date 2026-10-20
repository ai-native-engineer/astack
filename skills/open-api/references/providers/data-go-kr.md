# Provider: data.go.kr

공공데이터포털(data.go.kr) API 호출 규칙이다. 작업에서 출발해 레시피를 먼저 찾고, 없으면 검색해서 호출한 뒤 레시피로 적립한다.

## 언제 쓰나

- 공공데이터포털, data.go.kr
- 나라장터 입찰, 낙찰, 계약
- 국민연금 사업장
- 사업자등록 상태
- 건축물대장
- 행정기관, 공공기관 데이터셋

## 워크플로

1. 작업의 도메인 키워드(기관명, 데이터명)로 `rg -il "<키워드>" ${CLAUDE_PLUGIN_ROOT}/skills/open-api/references/recipes/data-go-kr/`를 검색한다.
2. 레시피가 있으면 키를 확인하고 레시피대로 호출한다. 인코딩, 페이징, 에러 처리는 [`data-go-kr-call-patterns.md`](data-go-kr-call-patterns.md)를 읽는다.
3. 레시피가 없으면 [`data-go-kr-search-and-apply.md`](data-go-kr-search-and-apply.md) 절차로 API 검색, 후보 선정, 상세 페이지 스키마 추출, 호출 시도 순서로 진행한다.
    - 미신청 또는 미승인 에러가 나오면 활용신청 딥링크를 사용자에게 전달하고 멈춘다. 절차와 딥링크 형식은 search-and-apply 3절이다.
4. 첫 호출이 성공하면 작업을 끝내기 전에 `references/recipes/data-go-kr/`에 레시피를 저장한다. 형식은 [`recipes/_TEMPLATE.md`](../recipes/_TEMPLATE.md)를 따르되 data.go.kr 레시피는 헤더에 `publicDataPk`(숫자)와 상세 URL `https://www.data.go.kr/data/<publicDataPk>/openapi.do`를 적고, 파일명은 `<기관영문약칭>-<데이터영문키워드>.md`로 짓는다(예: `g2b-scsbid-info.md`).
5. 호출이 레시피대로 안 되면(파라미터 변경, 서비스 개편) 상세 페이지를 다시 떠서 레시피를 고치고 `checked` 날짜를 갱신한다.

## 키

- 기본 키 이름: `DATA_GO_KR_API_KEY`, 쿼리 파라미터 `serviceKey`.
- 키 소스 우선순위:
    1. `agents-env`가 있으면 `agents-env run DATA_GO_KR_API_KEY -- <명령>`으로 주입한다. 레시피 예시의 `$DATA_GO_KR_API_KEY` 자리는 `{{DATA_GO_KR_API_KEY}}`로 바꾼다. 키가 컨텍스트, 명령줄, 출력에 노출되지 않는다. 스토어에 키가 없으면(`agents-env get DATA_GO`) 사용자에게 `agents-env edit`로 추가를 요청한다. 에이전트는 전역 스토어에 쓰지 않는다.
    2. 환경변수 `DATA_GO_KR_API_KEY`.
    3. cwd `.env`.
    4. 셋 다 없으면 발급 안내(data.go.kr 로그인 -> 마이페이지 -> 일반 인증키) 후 멈춘다.
- Decoding 키를 저장하고, 인코딩은 호출 도구(curl `--data-urlencode`)에 맡긴다. 이중 인코딩이 가장 잦은 함정이다.

## 안전선

- 활용신청은 로그인 세션이 필요해 대신할 수 없다. 링크 전달까지가 책임이다.
- 응답의 개인정보(대표자명, 주소 등)는 작업에 필요한 필드만 다룬다.

## 레시피

- 레시피: `references/recipes/data-go-kr/*.md`
- 공식 참고문서 원본과 변환본: `references/recipes/docs/data-go-kr/`
