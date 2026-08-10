# Official API Enrichment

이 문서는 `company-context-research` 산출물을 혁신의 숲형 탭 데이터로 보강할 때 읽는다. API 호출 절차가 아니라, 이미 수집된 공식 데이터의 **정규화 파일 계약과 병합 규칙**만 다룬다.

## 목차

- Ownership Boundary
- Principles
- Normalized Inputs
- Funding Data Boundary
- Merge
- Naver News
- Naver DataLab
- Final Check

## Ownership Boundary

- `$open-api`가 DART, data.go.kr, KIPRIS, NTIS의 provider 선택, 키 주입, endpoint 확정, 호출, 페이징, retry, raw 저장, 레시피 적립을 담당한다.
- `company-context-research`는 회사별 workspace, 정규화 데이터 패키지, HTML 뷰어, `data/company-profile.json` 병합, `data/viewer-data.json` 빌드를 담당한다.
- 이 스킬에는 DART/data.go.kr/KIPRIS/NTIS API 키 이름, curl 샘플, endpoint 조립, provider별 에러 처리 절차를 두지 않는다.
- Naver News는 보도 인벤토리 수집이고, Naver DataLab은 검색 관심도 프록시다. 둘은 DART/data.go.kr/KIPRIS/NTIS 위임 범위와 분리한다.

## Principles

- HTML은 외부 API를 직접 호출하지 않는다.
- 화면은 `official-data/`를 직접 조합하지 않고 `data/viewer-data.json`만 fetch한다.
- API raw 응답은 `$open-api` 또는 해당 collector가 `official-data/<provider>/raw/`에 남긴다.
- 정규화 결과는 `official-data/<provider>/*.tsv` 또는 `*.json`으로 둔다.
- 정규화 결과, canonical JSON, manifest, viewer에는 인증 파라미터가 포함된 호출 URL을 남기지 않는다.
- `source_url`이 필요하면 공개 상세 페이지 또는 provider label을 넣고, `accessKey`, `serviceKey`, `crtfc_key` 같은 키 파라미터는 raw 계층에만 둔다.
- 병합 스크립트는 정규화 파일만 읽고 API 호출을 하지 않는다.
- 뉴스 원문과 공식 페이지는 화면에서 `원문` 링크로 열고, 로컬 `public-mirror/*.md` 경로는 노출하지 않는다.

## Normalized Inputs

`$open-api`가 호출한 공식 데이터는 아래 이름으로 정규화하면 `company-context-research`가 안정적으로 병합할 수 있다.

| 입력 파일 | 주요 컬럼 | 병합 위치 |
|---|---|---|
| `official-data/dart/financial-summary.tsv` | `year`, `revenue_krw`, `operating_income_krw`, `operating_loss_krw`, `operating_result_krw`, `net_income_krw`, `net_loss_krw`, `net_result_krw`, `assets_krw`, `liabilities_krw`, `equity_krw`, `source_xml` | `sections.organization_finance.financials`, `sections.growth.metrics`, `sections.overview.metrics` |
| `official-data/dart/funding-signals.tsv` | `date`, `title`, `value`, `summary`, `source_path`, `note` | `sections.funding.official_signals` |
| `official-data/naver-datalab/search-trends.tsv` | `group`, `period`, `ratio` | `sections.traffic_consumer.search_trends`, `sections.traffic_consumer.metrics` |
| `official-data/data-go-kr/nps-workplace/headcount.tsv` | `dataCrtYm`, `jnngpCnt`, `nwAcqzrCnt`, `lssJnngpCnt`, `crrmmNtcAmt` | `sections.organization_finance.employee_trends`, `sections.organization_finance.headcount`, `sections.overview.metrics` |
| `official-data/data-go-kr/nts-business-status/business-status.tsv` | `b_no`, `b_stt`, `tax_type` | `target.identifiers.business_status`, `sections.overview.facts`, `sections.overview.metrics` |
| `official-data/data-go-kr/procurement/procurement-search.tsv` | `dataset`, `query`, `confirmed_matches`, `note` | `sections.growth.procurement_contracts` |
| `official-data/data-go-kr/support-programs/support-program-search.tsv` | `dataset`, `query`, `confirmed_company_selection`, `note` | `sections.funding.support_programs` |
| `official-data/kipris/patents.tsv` | `title`, `application_no`, `application_date`, `applicant`, `status`, `source_url` | `sections.research_ip.patents` |
| `official-data/kipris/trademarks.tsv` | `title`, `application_no`, `application_date`, `applicant`, `status`, `source_url` | `sections.research_ip.trademarks` |
| `official-data/kipris/keywords.tsv` | `keyword`, `count`, `source` | `sections.research_ip.keywords` |
| `official-data/ntis/projects.tsv` | `project_name`, `period`, `organization`, `ministry`, `budget`, `source_url` | `sections.research_ip.projects`, `sections.funding.support_programs` |

컬럼이 더 많아도 된다. 화면에 필요한 핵심 컬럼은 위 이름을 유지한다.

`official-data/data-go-kr/nps-workplace/headcount.tsv`는 국민연금 사업장 가입자수다. 화면과 prose에서 고용보험 가입자수로 부르지 않는다.

DART 손익 컬럼 규칙:

- `operating_result_krw`와 `net_result_krw`는 흑자 양수, 적자 음수의 signed 값이다.
- `operating_income_krw`와 `net_income_krw`는 흑자 금액을 보존하는 보조 컬럼이다.
- `operating_loss_krw`와 `net_loss_krw`는 손실 금액을 보존하는 보조 컬럼이다.
- 손실 전용 TSV를 받은 경우 병합 스크립트가 `*_loss_krw`를 음수 `*_result_krw`로 하위호환 변환한다.
- 표·차트·prose는 손익 기준으로 표시한다. 흑자 연도를 빈 손실값 때문에 0억원으로 표시하지 않는다.

## Funding Data Boundary

투자유치 라운드 원장은 기본적으로 공식 API에서 완전하게 나오지 않는다.

- `sections.funding.rounds`는 기업 홈페이지, 공식 뉴스룸, 보도자료, 신뢰 가능한 언론 원문을 우선 근거로 채운다.
- DART는 유상증자, 전환사채, 감사보고서 주석 같은 공시 신호를 보강할 수 있지만 스타트업 투자 라운드 전체를 대체하지 않는다.
- data.go.kr/K-Startup/기업마당은 지원사업 공고 또는 공공지원 신호다. 선정·수혜가 확인되지 않으면 투자유치 이력처럼 쓰지 않는다.
- KVIC 공개 API는 펀드 단위 데이터 보강에는 유용하지만 개별 스타트업 라운드 원장으로 단정하지 않는다.
- IPO·상장준비·공시 보도는 `official_signals`나 `news`에 둔다. 날짜·투자자·금액·라운드가 확정되지 않으면 `rounds`에 넣지 않는다.
- 투자자명, 금액, 라운드, 날짜가 보도/홈페이지에서 확인되지 않으면 `gaps`에 관측 공백으로 남긴다.

## Merge

정규화 파일을 받은 뒤에는 병합과 화면 번들을 다시 만든다.

```bash
python3 scripts/merge_official_data.py "$workspace"
python3 scripts/build_viewer_data.py "$workspace"
python3 scripts/validate_company_workspace.py "$workspace"
```

`merge_official_data.py`는 위 표준 정규화 파일을 `data/company-profile.json`에 병합한다. 화면은 이후 `build_viewer_data.py`가 만든 `data/viewer-data.json`만 읽는다.

## Naver News

Naver News는 검색 관심도 데이터가 아니라 보도 인벤토리다.

```bash
agents-env run NAVER_CLIENT_ID NAVER_CLIENT_SECRET TAVILY_API_KEY -- \
  python3 scripts/research_press_tuner.py "<회사명>" "<브랜드명>" --out "$workspace/press"
```

네이버 API가 지연되거나 키가 없으면 Tavily News Search로 폴백한다. 실패한 소스는 숨기지 말고 `data/research-status.json`의 해당 step notes에 남긴다.

## Naver DataLab

Naver DataLab은 검색 관심도 프록시다. 실제 방문자 수나 소비자 수로 쓰지 않는다.

국내 소비자 브랜드, 여행·커머스·콘텐츠·앱 서비스처럼 검색 수요가 의미 있는 회사는 Naver DataLab을 우선 보강한다. 키가 없거나 기간/키워드 한도 때문에 못 수집하면 `market_data`를 `partial` 또는 `skipped`로 두고 사유를 notes에 적는다.

권장 정규화 파일:

```text
official-data/naver-datalab/raw/search-trends.json
official-data/naver-datalab/search-trends.tsv
```

권장 컬럼:

```text
period	group	keyword	ratio	source_url
```

병합 위치:

```text
sections.traffic_consumer.search_trends
sections.traffic_consumer.metrics
```

## Final Check

공식 데이터 보강 후에는 아래 조건을 만족해야 한다.

- `source-manifest.tsv`에 원 URL, 공식 API 상세 페이지, 또는 정규화 파일 경로가 남아 있다.
- `data/research-status.json`에 성공·부분 성공·실패·미신청·미승인 상태가 숨겨지지 않는다.
- `data/company-profile.json`에 병합한 값은 raw 또는 normalized 파일에서 역추적 가능하다.
- 화면에는 `원문`, `DART`, `DATA`, `KIPRIS`, `NTIS`처럼 짧은 출처만 보인다.
- normalized TSV와 canonical JSON에는 인증 파라미터가 포함된 API 호출 URL이 남아 있지 않다.
