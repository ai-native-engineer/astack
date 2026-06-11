# Report Schema

## Default Tree

```text
company-context/
└── YYYYMMDD-<company-slug>/
    ├── 00-surface-map.md
    ├── 00-target.md
    ├── 01-public-web.md
    ├── 02-public-press.md
    ├── 03-market-data.md
    ├── 04-internal-context.md
    ├── 05-company-brief.md
    ├── source-manifest.tsv
    ├── attachments/
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
    └── public-mirror/             # 인용용 읽기 md (있을 때)
        └── <host>/<path>.md
```

미팅 준비 질문지, 진행 시나리오, 데모 카드 같은 다운스트림 문서는 이 스킬의 산출물이 아니다. 필요하면 작업 세션에서 이 패키지를 근거로 별도 생성한다.

## File Roles

### 00-target.md

- company / primary domain / country / listed status
- research intent
- notes on entity resolution

### 00-surface-map.md

- legal entity
- parent company
- email domain
- local brand / D2C surfaces
- B2B portal
- careers
- IR / investor host
- attachment / CDN host
- contradictions and unresolved edges

### 01-public-web.md

- Site map / navigation summary
- Recursive crawl summary (저장 페이지 수, 카테고리별 링크 수, 새 도메인, 새 첨부, 노이즈 표면)
- High-signal pages reviewed (실제 읽은 페이지/미러 경로)
- Product / customer / industry language
- Attachment inventory summary
- Important quotes / claims
- Gaps

### 02-public-press.md

- Company-authored press releases
- Third-party news coverage
- Timeline of meaningful events
- Why each event matters for outreach
- Gaps

### 03-market-data.md

- KRX lookup result
- DART company profile
- Recent filings
- Finance / audit / capital events
- Risks / anomalies
- Gaps

### 04-internal-context.md

- Prior touchpoints
- Existing stakeholder relationships
- Notes from internal docs / chats / calls
- Confidence by source
- Gaps

### 05-company-brief.md

짧고 강한 최종본. 최소 섹션:

- One-screen summary
- Current deal status
- Champion / buying center
- Participant needs
- Next action / questions for next meeting
- What they do
- Why now
- Buying signals
- Language they use
- Research status / crawl constraints (막힌 표면, 관측 공백)
- Risks / red flags
- Suggested outreach angles
- Open questions

## source-manifest.tsv

헤더:

```tsv
source_type	url_or_path	title	saved_path	date_collected	note
```

중요 규칙:

- `saved_path` 는 **실제로 존재하는 파일/폴더만** 적는다
- 계획/희망/미생성 산출물은 manifest에 적지 않는다
- 전달 전 saved_path가 전부 실존하는지 확인한다. manifest에 없는 파일을 추가하는 것보다, **없는 파일을 적지 않는 것**이 더 중요하다

예:

```tsv
web	https://example.com/about	About	01-public-web.md	2026-06-10	Main company overview
attachment	https://example.com/investor.pdf	Investor Deck	attachments/investor-deck.pdf	2026-06-10	IR attachment
press	https://news.example.com/...	Funding news	02-public-press.md	2026-06-10	Third-party article
```

### recursive-crawl/

분절 표면 회사에서는 선택이 아니라 기본 산출물.

- `crawl-manifest.tsv`: 저장 페이지 목록
- `link-inventory.tsv`: 발견 링크 분류표
- `attachment-candidates.tsv`: 첨부 후보
- `download-report.tsv`: 첨부 다운로드 성공/거절 MIME 로그
- `keep-list-candidates.tsv`: 실제 후속 읽기 대상
- `shortlist.tsv`: 바로 읽을 상위 후보
- `pages/`: 페이지별 md 원본

### press/

- `press-inventory.tsv`: 외부 보도 인벤토리 (`scripts/search_press.py` 산출). 컬럼: `source / date / outlet / title / url / decoded / queries`. 읽을 기사 선별과 원문 미러 규칙은 `references/press-coverage.md`.

### public-mirror/

최종 읽기용 md. raw `pages/`가 아니라 shortlist에서 다시 떨군 읽기 좋은 산출물. 보고서 인용은 이 경로를 쓴다.
