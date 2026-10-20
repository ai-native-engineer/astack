# Provider: ntis.go.kr (NTIS)

국가 R&D 과제, 성과, 연구기관, 연구보고서, 분류/코드, 추천, 통합검색, 연구자정보 조회가 목적이면 ntis.go.kr(NTIS)를 쓴다.

- checked: 2026-06-28
- domain: `ntis.go.kr`
- alias: NTIS
- catalog: 14 services (8 전체용, 6 기관용)
- key env: `NTIS_API_KEY`
- recipes: `references/recipes/ntis/*.md`
- original manuals: `references/recipes/docs/ntis/*.pdf` and `*.txt`

## 언제 쓰나

- 국가연구개발 과제 검색과 과제고유번호 확인
- 논문, 특허, 연구보고서, 연구시설장비 등 R&D 성과 메타데이터 조회
- 수행기관 R&D 현황, 과학기술표준분류/국가중점기술 코드, 연관 콘텐츠 추천
- 기관용 권한이 있는 경우 통합검색, 위탁/공동연구, 출연연 연구자정보 조회

## 키

- 기본 키 이름: `NTIS_API_KEY`
- 서비스별 활용신청과 승인이 필요할 수 있다.
- 호출은 가능하면 `agents-env run NTIS_API_KEY -- <명령>`으로 실행한다.
- recipe, 로그, 보고서에는 실제 승인키를 쓰지 않는다.

## 서비스별 레시피

| apiSn | 구분 | 서비스 | recipe | 원문 PDF |
|---:|---|---|---|---|
| `6605` | 전체용 | 국가R&D 과제검색 서비스(전체용) | [project-search-public](../recipes/ntis/project-search-public.md) | [PDF](../recipes/docs/ntis/6605-project-search-public.pdf) |
| `6427` | 기관용 | 국가R&D 과제검색 서비스(기관용) | [project-search-agency](../recipes/ntis/project-search-agency.md) | [PDF](../recipes/docs/ntis/6427-project-search-agency.pdf) |
| `6614` | 기관용 | 위탁/공동연구 과제검색 서비스(기관용) | [consortium-project-search-agency](../recipes/ntis/consortium-project-search-agency.md) | [PDF](../recipes/docs/ntis/6614-consortium-project-search-agency.pdf) |
| `6606` | 전체용 | 국가R&D 성과검색 서비스(전체용) | [result-search-public](../recipes/ntis/result-search-public.md) | [PDF](../recipes/docs/ntis/6606-result-search-public.pdf) |
| `161` | 기관용 | 국가R&D 성과검색 서비스(기관용) | [result-search-agency](../recipes/ntis/result-search-agency.md) | [PDF](../recipes/docs/ntis/161-result-search-agency.pdf) |
| `6609` | 전체용 | 국가R&D 수행기관 R&D현황조회 서비스(전체용) | [org-rnd-status-public](../recipes/ntis/org-rnd-status-public.md) | [PDF](../recipes/docs/ntis/6609-org-rnd-status-public.pdf) |
| `6607` | 전체용 | 국가R&D 연구보고서 검색 서비스(전체용) | [research-report-search-public](../recipes/ntis/research-report-search-public.md) | [PDF](../recipes/docs/ntis/6607-research-report-search-public.pdf) |
| `6603` | 기관용 | 과학기술표준분류 추천 서비스(기관용) | [science-tech-classification-recommend-agency](../recipes/ntis/science-tech-classification-recommend-agency.md) | [PDF](../recipes/docs/ntis/6603-science-tech-classification-recommend-agency.pdf) |
| `6429` | 전체용 | 이슈로보는R&D 서비스(전체용) | [rnd-issue-public](../recipes/ntis/rnd-issue-public.md) | [PDF](../recipes/docs/ntis/6429-rnd-issue-public.pdf) |
| `6604` | 전체용 | 국가R&D 용어사전 조회 서비스(전체용) | [rnd-dictionary-public](../recipes/ntis/rnd-dictionary-public.md) | [PDF](../recipes/docs/ntis/6604-rnd-dictionary-public.pdf) |
| `6430` | 전체용 | 과학기술표준분류코드/국가중점기술코드 검색 서비스(전체용) | [classification-code-search-public](../recipes/ntis/classification-code-search-public.md) | [PDF](../recipes/docs/ntis/6430-classification-code-search-public.pdf) |
| `6613` | 전체용 | 연관콘텐츠 추천 서비스(전체용) | [related-content-recommend-public](../recipes/ntis/related-content-recommend-public.md) | [PDF](../recipes/docs/ntis/6613-related-content-recommend-public.pdf) |
| `6616` | 기관용 | 국가R&D 통합검색 서비스(기관용) | [integrated-search-agency](../recipes/ntis/integrated-search-agency.md) | [PDF](../recipes/docs/ntis/6616-integrated-search-agency.pdf) |
| `6618` | 기관용 | 출연(연) 연구자정보검색 서비스(기관용) | [researcher-info-search-agency](../recipes/ntis/researcher-info-search-agency.md) | [PDF](../recipes/docs/ntis/6618-researcher-info-search-agency.pdf) |

## 호출 흐름

1. 작업 축을 먼저 고른다: 과제, 성과, 기관, 연구보고서, 분류/코드, 추천, 통합검색, 연구자정보.
2. 위 표에서 recipe를 열어 endpoint, 필수 파라미터, paging, 공식 PDF 원문을 확인한다.
3. 미승인/키 오류가 나오면 `apiSn`과 서비스명을 기준으로 NTIS OpenAPI 활용신청 상태를 확인한다.
4. 기관용 API는 소속기관 권한 제한이 있으므로 대국민 API로 대체 가능한지 먼저 본다.

## 활용신청 메모

- 2026-06-28 기준 14개 서비스 활용신청 제출을 확인했다.
- 승인키가 상세 이력 또는 `NTIS_API_KEY`에 없으면 호출은 공식 오류 `인증키 정보가 없습니다.`로 끝난다.
- 제출/승인 상태는 NTIS 활용신청이력에서 확인하고, 실제 키·쿠키·개인정보·공인 IP는 레시피에 저장하지 않는다.

## 함정

- 기업명/기관명은 법인명, 산학협력단, 캠퍼스, 연구소 표기가 달라 누락될 수 있다.
- 과제 0건과 성과 0건은 의미가 다르다. 과제 조회 후 과제고유번호로 성과 API를 다시 연결한다.
- 대국민/기관용 API는 제공 필드와 이용 가능 범위가 다를 수 있다.
- 연구자정보 API는 개인정보 최소 처리 원칙을 적용한다.
- PDF 원문이 API별 최종 근거다. recipe는 호출에 필요한 핵심만 정리한 캐시다.
