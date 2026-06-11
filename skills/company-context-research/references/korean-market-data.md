# Korean Market Data

한국 법인 조사일 때 읽는다. 외부 프록시 의존 없음 — DART는 공식 API 직접 호출, 나머지는 `data-go-kr` 스킬 위임(사용자 키 직접)으로만 동작한다.

## Layer 1: 상장 확인 + 시세 snapshot (data-go-kr)

`data-go-kr` 스킬로 공공데이터포털의 주식 API(금융위원회 주식시세정보 등)를 발굴·호출한다. 검색→활용신청→호출→레시피 캐시 절차는 그 스킬이 권위 소스다.

- 역할: 상장 여부 확인, 시장 구분, 종목코드, 기본정보, 일별 시세 snapshot
- 종목명 검색으로 회사명/종목코드를 먼저 좁힌 뒤 시세로 들어간다
- 이 레이어는 **상장 여부를 확인하는 용도**다. 한국 법인 전체를 포괄하지 않는다.

최소 수집 항목:

- 시장 (`KOSPI` / `KOSDAQ` / `KONEX`)
- 종목코드
- 기준일
- 종가
- 등락률
- 거래량
- 시가총액
- 필요 시 상장일 / 상장주식수 / 액면가

주의:

- 실시간 호가/체결처럼 말하지 않는다
- 휴장일이면 최근 영업일 snapshot 으로 재시도한다

## Layer 2: DART filings (직접 호출)

DART OpenAPI(`https://opendart.fss.or.kr/api/`)를 직접 호출한다. endpoint 카탈로그는 DART 공식 개발가이드(opendart.fss.or.kr)가 권위 소스다.

- 역할: 공시검색, 기업개황, 재무제표, 배당, 감사의견, 증자/감자, 전환사채, 소송, 직원 현황 등
- `API_K_DART` 키 필요. 이 환경에서는 셸 환경변수가 아니라 `agents-env`에 저장돼 있다 — 값을 보지 않고 그대로 쓴다:
  - 존재 확인: `agents-env get API_K_DART`
  - 호출: `agents-env run API_K_DART -- curl -s "https://opendart.fss.or.kr/api/list.json?crtfc_key={{API_K_DART}}&bgn_de=<YYYYMMDD>&end_de=<YYYYMMDD>"` (파라미터 이름은 `crtfc_key`)
  - 셸에 `API_K_DART` 환경변수가 이미 있으면 그걸 써도 된다
- 대부분의 endpoint 는 `corp_code`(8자리)가 먼저 필요하다 — `corpCode.xml` endpoint를 받으면 zip 안에 전체 법인 목록(CORPCODE.xml)이 오고, 거기서 회사명으로 `corp_code`를 찾는다.
- 이 레이어는 **한국 법인 여부가 보이면 listed 여부와 별개로 시도**한다.

### Minimum DART coverage

한국 법인 조사 시 가능하면 아래를 확보한다.

- 최근 공시 목록
- 기업개황
- 최근 사업보고서 또는 최신 분기/반기 재무
- 배당 관련 정보
- 감사의견
- 증자/감자 또는 전환사채 등 자본조달 이벤트
- 소송/주요사항 보고서 (관련 있을 때)
- 직원 현황

## Layer 3: 공공데이터 보강 (data-go-kr)

DART가 얇은 법인(비상장사 대부분)은 `data-go-kr` 스킬에 위임해 공공데이터포털 API로 보강한다. 키·활용신청·호출 절차는 그 스킬이 권위 소스다.

업종 무관 기본 시도 2개:

- **국민연금 사업장** — 직원 수·가입 추이. 비상장사의 성장/축소를 보여주는 가장 강한 공개 신호
- **사업자등록 상태조회** — 휴폐업 여부. entity resolution 단계에서도 유용

그 외 레이어(나라장터 입찰/계약, 건축물대장 등)는 회사 성격에 따라 data-go-kr 검색으로 온디맨드 발굴한다 — 특정 업종을 전제하지 않는다.

## Output Rules

`03-market-data.md` 에는 아래를 구분해서 적는다.

- 상장 확인 + 시세 snapshot
- DART company profile
- DART recent filings
- DART finance / audit / capital events
- 공공데이터 보강 (직원 수 추이, 사업자 상태 등)
- 해석 메모
- 관측 공백

## Failure Rules

- 키가 어디에도 없으면(`agents-env get API_K_DART` 기준) DART 레이어를 생략하지 말고 "키 없음" 공백으로 적는다
- listed 여부가 불명확하면 먼저 Layer 1 시세 API에서 종목명 검색으로 확인한다
- 시세 API에 안 나온다고 DART를 자동 스킵하지 않는다
- DART가 얇다고 ②축을 끝내지 않는다 — Layer 3 공공데이터를 시도한 뒤 공백을 적는다
- 한국 법인성이 약하면 DART 미적용 사유를 적고 종료한다
