# Web Package Schema

## 목차

- Default Tree
- File Roles
- `data/company-profile.json`
- `data/research-status.json`
- `source-manifest.tsv`

## Default Tree

```text
company-context/
└── YYYYMMDD-<company-slug>/
    ├── index.html
    ├── data/
    │   ├── company-profile.json
    │   ├── viewer-data.json
    │   └── research-status.json
    ├── source-manifest.tsv
    ├── attachments/
    ├── official-data/
    │   ├── dart/
    │   ├── naver-datalab/
    │   ├── data-go-kr/
    │   ├── kipris/
    │   └── ntis/
    ├── press/
    │   └── press-inventory.tsv
    ├── recursive-crawl/
    │   ├── crawl-manifest.tsv
    │   ├── link-inventory.tsv
    │   ├── attachment-candidates.tsv
    │   ├── download-report.tsv
    │   ├── keep-list-candidates.tsv
    │   ├── shortlist.tsv
    │   └── pages/
    ├── recursive-crawl-v2/        # 2차 이후 라운드 (있을 때)
    │   └── <host>/
    └── public-mirror/             # 인용용 읽기 사본
        └── <host>/<path>.md
```

Markdown 보고서는 기본 산출물이 아니다. 수집 중 판독 노트가 필요하면 임시로 만들 수 있지만, 최종 전달 기준은 `data/company-profile.json`과 `index.html`이다.

## File Roles

### `index.html`

- 외부 빌드 없이 동작하는 정적 HTML 뷰어
- `data/viewer-data.json` 하나만 fetch해서 탭 UI로 렌더링
- 기본 템플릿은 React/CDN, Recharts, d3-cloud, TanStack Table을 사용한다.
- UI 탭은 기업개요, 종합성장분석, 방문자/소비자, 연구/특허, 투자유치, 조직/재무, 기업뉴스를 유지한다.
- `official-data/`, `press/`, `recursive-crawl/` 파일은 직접 fetch하지 않는다.
- 브라우저 확인은 로컬 정적 서버 URL로 한다. `file://index.html`은 `fetch()` 보안 제한 때문에 실패한다.

### `data/company-profile.json`

canonical 데이터. 사람이 읽는 prose가 아니라, 화면과 후속 자동화가 재사용할 구조화 데이터다.

최상위 필수 키:

```json
{
  "schema_version": "company-context-web-v1",
  "generated_at": "YYYY-MM-DD",
  "target": {},
  "summary": {},
  "surface_map": {},
  "sections": {},
  "gaps": [],
  "sources": []
}
```

#### `target`

- `name`
- `primary_domain`
- `country`
- `listed_status`
- `research_intent`
- `entity_resolution_notes`
- `identifiers`: 사업자번호, 법인등록번호, 사업자 상태 같은 공식 식별자

#### `summary`

- `one_screen`
- `deal_status`
- `champion_buying_center`
- `participant_needs`
- `what_they_do`
- `why_now`
- `buying_signals`
- `language_they_use`
- `risks_red_flags`
- `open_questions`

#### `surface_map`

- `legal_entity`
- `parent_company`
- `email_domains`
- `surfaces`: `{ "type", "name", "url", "host", "evidence" }`
- `contradictions_unresolved_edges`

#### `sections`

혁신의 숲형 탐색 탭에 대응한다.

- `overview`: `metrics`, `facts`, `notes`
- `growth`: `metrics`, `timeline`, `procurement_contracts`, `analysis`
- `traffic_consumer`: `metrics`, `segments`, `search_trends`, `analysis`
- `research_ip`: `projects`, `patents`, `trademarks`, `keywords`, `metrics`, `analysis`
- `funding`: `rounds`, `official_signals`, `support_programs`, `analysis`
- `organization_finance`: `headcount`, `employee_trends`, `financials`, `analysis`
- `news`: `items`, `analysis`
- `internal_context`: `touchpoints`, `stakeholders`, `analysis`

공통 item은 가능하면 아래 형태를 쓴다.

```json
{
  "title": "string",
  "date": "YYYY-MM-DD",
  "value": "string",
  "summary": "string",
  "url": "https://...",
  "source_path": "public-mirror/example.md",
  "note": "string"
}
```

### `data/viewer-data.json`

화면이 읽는 단일 데이터 번들이다. `scripts/build_viewer_data.py <workspace>`로 생성한다.

필수 키:

```json
{
  "schema_version": "company-context-viewer-v1",
  "generated_at": "YYYY-MM-DD",
  "profile": {},
  "status": {},
  "manifest": [],
  "financials": [],
  "searchTrends": [],
  "employeeTrends": [],
  "businessStatusRows": [],
  "procurementRows": [],
  "supportProgramRows": [],
  "pressRows": []
}
```

규칙:

- `profile`은 `data/company-profile.json`을 그대로 담는다.
- `status`는 `data/research-status.json`을 그대로 담는다.
- `manifest`는 `source-manifest.tsv`를 row 객체로 담는다.
- `financials`, `searchTrends`, `employeeTrends`, `businessStatusRows`, `procurementRows`, `supportProgramRows`, `pressRows`는 표준 TSV를 JSON row로 합친다.
- `index.html`은 이 파일만 읽고, 원본·TSV 파일 조합은 빌더가 담당한다.

### `data/research-status.json`

마지막에 스킬이 제대로 돌았는지 검증하기 위한 상태 파일이다. 모든 필수 step은 `done`, `partial`, 근거 있는 `skipped` 중 하나여야 한다.

필수 step:

- `surface_map`
- `public_web_crawl`
- `press_collection`
- `market_data`
- `internal_context`
- `data_profile`
- `source_integrity`
- `viewer_ready`

형식:

```json
{
  "schema_version": "company-context-status-v1",
  "steps": [
    {
      "id": "surface_map",
      "label": "Surface map",
      "status": "done",
      "evidence": ["data/company-profile.json", "source-manifest.tsv"],
      "notes": ""
    }
  ]
}
```

상태 규칙:

- `done`: 실제 row/evidence가 있고, notes가 보류나 미수집을 말하지 않을 때만 쓴다.
- `partial`: 일부 산출물은 있으나 DataLab, NTIS, 조달/계약, 지원사업, 재귀 확장 등 명시한 수집 축이 빠졌을 때 쓴다.
- `skipped`: 대상 비해당 또는 접근권한 없음처럼 실행하지 않는 것이 맞을 때 쓴다.

`partial`과 `skipped`는 `notes`에 왜 완결되지 않았는지 적어야 한다. 예: 비상장 해외 법인이라 DART/KRX 비대상, 내부 CRM 접근권한 없음, Naver DataLab 키 미보유.

### `source-manifest.tsv`

헤더:

```tsv
source_type	url_or_path	title	saved_path	date_collected	note
```

중요 규칙:

- `saved_path`는 실제 존재하는 파일/폴더만 적는다.
- placeholder `-`, 빈 문자열, 계획/희망/미생성 산출물은 적지 않는다.
- 웹 URL만 보고 근거로 쓴 경우에도 최소한 `source-manifest.tsv`에 원 URL과 수집일을 남긴다.
- 전달 전 `python3 scripts/validate_company_workspace.py <workspace>`로 saved_path 실존 여부를 확인한다.

예:

```tsv
web	https://example.com/about	About	public-mirror/example.com/about.md	2026-06-28	Main company overview
attachment	https://example.com/investor.pdf	Investor Deck	attachments/investor-deck.pdf	2026-06-28	IR attachment
press	https://news.example.com/...	Funding news	public-mirror/news.example.com/funding.md	2026-06-28	Third-party article
data	data/company-profile.json	Normalized profile	data/company-profile.json	2026-06-28	Canonical web data
```

### `official-data/`

공식 API raw 응답과 정규화 파일을 보관한다. 화면은 이 폴더를 직접 읽지 않는다. 핵심 요약은 `data/company-profile.json`에 병합하고, 화면 테이블에 필요한 정규화 row는 `data/viewer-data.json`에 복사한다.

- `dart/`: DART corp code, filings, financial summary
- `naver-datalab/`: 검색 관심도 raw JSON과 normalized TSV
- `data-go-kr/`: `$open-api` 레시피로 호출한 국민연금, 사업자등록, 나라장터, 지원사업 데이터
- `kipris/`: 특허 목록과 키워드 원장
- `ntis/`: R&D 과제 목록

data.go.kr 계열은 이 스킬에서 새 호출 규약을 만들지 않고 `$open-api` 레시피를 따른다.

정규화 계층 규칙:

- raw API 응답과 호출 흔적은 `official-data/<provider>/raw/`에 둔다.
- normalized TSV/JSON, `source-manifest.tsv`, `data/company-profile.json`, `data/viewer-data.json`, `index.html`에는 인증 파라미터가 포함된 호출 URL을 남기지 않는다.
- DART 재무 손익은 `operating_result_krw`, `net_result_krw`를 canonical로 쓴다. 흑자는 양수, 적자는 음수다.
- 국민연금 사업장 가입자수는 고용보험 가입자수와 구분해서 표기한다.

### `recursive-crawl/`

분절 표면 회사에서는 선택이 아니라 기본 산출물.

- `crawl-manifest.tsv`: 저장 페이지 목록
- `link-inventory.tsv`: 발견 링크 분류표
- `attachment-candidates.tsv`: 첨부 후보
- `download-report.tsv`: 첨부 다운로드 성공/거절 MIME 로그
- `keep-list-candidates.tsv`: 실제 후속 읽기 대상
- `shortlist.tsv`: 바로 읽을 상위 후보
- `pages/`: 페이지별 md 원본

`public_web_crawl`을 `done`으로 두려면 `link-inventory.tsv` 또는 `shortlist.tsv`에 실제 row가 있어야 한다. 헤더만 있는 인벤토리는 `partial`이며, blockers를 `research-status` notes와 `gaps`에 적는다.

### `press/`

- `press-inventory.tsv`: 외부 보도 인벤토리 (`scripts/research_press_tuner.py` 산출). 컬럼: `source / date / outlet / title / url / decoded / queries`.

### `public-mirror/`

최종 인용용 읽기 사본. raw `recursive-crawl/pages/`가 아니라 shortlist 또는 중요 기사에서 다시 떨군 읽기 좋은 산출물이다.
