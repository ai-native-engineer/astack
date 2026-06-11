# Press Coverage

외부 보도(수집 축 ④) 수집 규칙. 자사 뉴스룸은 crawl-first 재귀 크롤(축 ③)에 잡히므로, 이 문서는 **제3자 보도**를 다룬다.

## Layer 1: search_press.py (네이버 뉴스 API + Google News RSS)

수집의 기본. 두 소스를 한 번에 돌려 `press/press-inventory.tsv`를 만든다.

```bash
agents-env run NAVER_CLIENT_ID NAVER_CLIENT_SECRET -- \
  python3 scripts/search_press.py "<회사명>" ["<회사명> <대표명>" ...] --out <workspace>/press
```

- 쿼리는 회사명 1개로 시작한다. naver `total`이 1,100을 넘으면(스크립트가 경고) "회사명+대표명", "회사명+브랜드/제품명" 식 변형 쿼리를 추가해 인덱스를 쪼갠다.
- 한국 보도가 기대되지 않는 회사는 `--sources gnews`로 네이버를 빼고 돌리고, 그 시장 언어의 쿼리와 tavily 보강에 무게를 둔다. 네이버 레이어는 한국 시장 인스턴스일 뿐 이 단계의 전제가 아니다.
- 네이버: 한국 보도 본진. 검색제휴 수백 개사(지역지·업계지 포함)가 잡힌다. 날짜 범위 파라미터가 없고 쿼리당 최대 ~1,100건(start≤1000) — 쿼리 분할이 유일한 우회책이다.
- Google News RSS: 피드당 ~100건 캡을 `--years-back` 연 단위 `after:`/`before:` 윈도우로 우회한다. en 로케일(`gnews-en`)이 글로벌 모회사의 영문 보도를 잡는다.
- gnews 원문 URL 디코딩은 비공식 내부 API라 언제든 깨질 수 있다. 실패 항목은 `decoded=no`로 인코딩 URL이 보존된다 — 버리지 말고 제목/언론사/날짜는 그대로 근거로 쓴다.

키: `NAVER_CLIENT_ID` / `NAVER_CLIENT_SECRET` — agents-env에 저장(`agents-env get naver`로 확인). 없으면 developers.naver.com 앱 등록(즉시 발급, 심사 없음, 검색 API 일 25,000회)을 사용자에게 요청한다.

## Layer 2: tavily-cli (영문/글로벌 보강)

한국 토종 매체 커버리지가 보장되지 않으므로 **네이버 대체가 아니라 보강**이다. 글로벌 모회사, 해외 시장 반응, 실적 발표 해석 기사를 잡는 용도.

```bash
agents-env run TAVILY_AI_API_KEY[@tag] -- env TAVILY_API_KEY={{TAVILY_AI_API_KEY}} \
  tvly search "<영문 회사명> <키워드>" --topic news --time-range year --max-results 20 --json
```

- 과거 기간은 `--start-date` / `--end-date`(YYYY-MM-DD)로 지정한다.
- 무인증도 동작하지만 rate-cap이 있다. 캡에 걸리면 위처럼 키를 주입한다.

## Layer 3: 빅카인즈 웹 UI (깊은 과거 폴백)

2018년 이전의 깊은 과거나 날짜·언론사 정밀 필터가 필요할 때만. Open API는 신청-승인 게이트(셀프서브 아님)라 스킬에 넣지 않는다 — bigkinds.or.kr 웹 검색 + 엑셀 다운로드를 수동 경로로 안내한다(본문 200자 컷, 원문은 URL 재크롤).

## Selection → 본문 확보

- TSV 전부를 읽지 않는다. 모델이 영업 의도와의 관련성, 사건성(펀딩·파트너십·실적·소송·임원 변화), 언론사 다양성 기준으로 읽을 기사를 고른다.
- **인용할 기사는 원문 URL을 `crwl`로 미러**해 `public-mirror/`에 둔다 — API의 description/snippet은 요약일 뿐 인용 근거가 아니다. crawl-first 원칙은 보도에도 적용된다.
- 수집·인용한 기사는 `source-manifest.tsv`에 기록한다.

## Failure Rules

- naver `pubDate`는 "기사가 네이버에 제공된 시각"이라 실제 보도일과 어긋날 수 있다 — 본문 날짜와 충돌하면 본문을 따른다.
- gnews의 과거 연도 윈도우는 전수 아카이브가 아니라 대표 샘플이다. "그 해 보도 N건"처럼 말하지 않는다.
- 막다른 길이므로 시도하지 않는다: 카카오 검색 API(뉴스 엔드포인트 자체가 없음), GDELT DOC API(검색 윈도우가 최근 3개월).
- 수집 0건이어도 "보도 없음"으로 단정하지 않는다 — 쿼리 변형과 사명 변경 이력을 먼저 확인하고, 그래도 없으면 관측 공백으로 적는다.
