# Public Sweep Checklist

## Discovery Order

1. surface map
2. 분절 표면이면 recursive crawl 원본 4종 생성
3. corporate / brand / portal / careers / IR 각 표면 확인
4. 각 표면의 sitemap / robots / navigation
5. 회사 소개와 제품 구조
6. 고객 사례 / 산업별 페이지
7. docs / blog / newsroom / careers
8. IR / governance / investor pages
9. first-party linked attachments
10. external press and third-party coverage

## High-Signal Page Types

우선순위가 높은 섹션:

- `about`
- `product`
- `solutions`
- `industries`
- `customers`
- `case studies`
- `docs`
- `blog`
- `newsroom` / `press`
- `careers`
- `IR`
- `governance`
- `pricing`
- `partners`

존재하지 않는 섹션은 억지로 만들지 말고, 존재하는 섹션은 빠뜨리지 않는다.

## Attachment Coverage

기본적으로 찾는 파일:

- `.pdf`
- `.docx`
- `.pptx`
- `.xlsx`
- `.csv`

특히 우선 수집:

- 회사 소개서
- 제품 브로슈어
- 투자자 자료
- annual report / sustainability report
- whitepaper
- pricing / rate card
- case study PDF

same-domain만 보지 않는다. 아래도 first-party attachment 로 본다.

- investor host
- q4cdn
- Shopify CDN
- media kit CDN
- 공식 press release / report 파일 링크

## Crawl Budget

무한 크롤 금지. 기본 예산:

- 일반 기업 사이트: 핵심 페이지 최대 25개 + 관련 첨부 전부
- 대형 엔터프라이즈 / 문서 사이트: 핵심 페이지 최대 50개 + 고신호 첨부 전부

문서 사이트가 거대하면 샘플링이 아니라 "고신호 우선 전수" 방식으로 간다.

분절 표면 회사에서 recursive crawl을 쓰면:

- 저장 페이지 예산: 20~40
- 사람이 다시 읽는 keep-list: 10~20

## What to capture from each page

- 회사가 스스로 정의한 사업 설명
- 반복되는 고객/산업 언어
- 도입 효과 수치
- 레퍼런스 고객 / 파트너
- 최근 출시 / 방향 전환
- 채용 포지션으로 보이는 투자 방향

각 surface마다 최소 1개 이상은 아래를 남긴다.

- 실제 URL
- 한 줄 핵심 해석
- 직접 근거 문장 또는 수치

## External Coverage

반드시 나눠서 본다.

- 회사가 직접 발행한 뉴스룸 / 보도자료
- 제3자 기사 / 인터뷰 / 분석

핵심 토픽:

- 펀딩
- 파트너십
- 고객 확보
- 주요 계약
- 신제품 / 전략 변화
- 소송 / 규제
- 경영진 변화
- 채용 확대 / 축소

회사 전용 newsroom이 없으면 아래 대체 경로를 본다.

- brand site news/blog
- investor release
- 업계지
- 채용 플랫폼

## Observability Gaps

다음은 숨기지 말고 기록한다.

- surface map이 일부만 확인됨
- 뉴스룸 없음
- sitemap 없음
- 첨부파일 다운로드 차단
- 동적 렌더링으로 본문 확보 실패
- paywall
- 관련 회사가 너무 많아 entity ambiguity 존재
