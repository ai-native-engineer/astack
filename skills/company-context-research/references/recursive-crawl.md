# Recursive Crawl

표면이 분절된 회사는 사람이 surface map을 먼저 만들더라도 놓치는 도메인이 생긴다. 따라서 이런 회사는 `재귀 확장 -> 로컬 아카이브 -> 인벤토리 후처리` 순서로 간다.

## When to use

아래 중 2개 이상이면 기본값으로 쓴다.

- 브랜드 사이트와 법인 사이트가 분리됨
- B2B portal 이 따로 있음
- IR 호스트가 별도임
- CDN / q4cdn / wp-content 첨부가 많음
- 글로벌 parent 와 로컬 brand 가 섞여 있음
- Shopify / commerce surface 가 보임

## First pass

`00-surface-map.md`에 적은 표면들에서 시드 URL을 뽑아 직접 돌린다.

```bash
python3 scripts/recursive_surface_crawl.py <seed-url...> \
  --keyword <kw1> --keyword <kw2> \
  --out <recursive-crawl-dir>
```

`--keyword`는 host 확장 판정 키워드(회사명, 브랜드명, 모회사명 등)다. 이 단계가 만드는 원본 5종:

- `crawl-manifest.tsv` — 실제 저장된 페이지 목록
- `link-inventory.tsv` — 발견 링크를 category/kind/signal 기준으로 분류
- `attachment-candidates.tsv` — 첨부 후보만 추출
- `keep-list-candidates.tsv` — 후속으로 실제 읽을 가치가 있는 URL만 추림
- `shortlist.tsv` — 바로 읽을 상위 후보 20개

이 단계 전에는 페이지를 감으로 고르지 않는다. 403/404로 막힌 시드는 같은 방식으로 재시도하지 말고, 우회 경로(corporate 사이트 경유 IR, 이메일 도메인 루트 등)를 모델이 직접 찾아 `01-public-web.md`에 공백/우회 내역으로 남긴다.

## If the crawl is interrupted

`pages/` 가 이미 일부라도 저장돼 있으면 처음부터 다시 돌리지 않는다.

```bash
python3 scripts/postprocess_recursive_crawl.py <recursive-crawl-dir>
```

이 스크립트가 저장된 `pages/`만 읽어 원본 5종을 재생성한다. 즉, `crawl` 과 `postprocess` 를 분리해서 생각한다.

## If the archive contains broken pages

오타 슬러그, 중복 경로(`sustainability/sustainability`), 명백한 저신호 페이지가 남아 있으면:

```bash
python3 scripts/prune_recursive_crawl_pages.py <recursive-crawl/pages>
python3 scripts/postprocess_recursive_crawl.py <recursive-crawl-dir>
```

즉, `prune -> postprocess` 를 한 세트로 본다.

## How to read the outputs

### `crawl-manifest.tsv`

무엇이 실제로 저장됐는지 본다. hop 0 = 시드, hop 1+ = 연관 도메인/페이지 확장. 여기서 새 도메인, 새 브랜드 표면, 새 섹션을 찾는다.

### `link-inventory.tsv`

링크를 모두 분류한 원장이다. 전체를 다 읽는 용도가 아니라 `parent-corporate` / `local-brand` / `brand-related` / `b2b-portal` / `careers` / `ir` 각 카테고리 수와 대표 링크만 보는 용도다.

### `attachment-candidates.tsv`

PDF/DOC/PPT/XLS 후보 전용. 먼저 여기서 공식 첨부를 다운로드하고, 그 뒤 본문 요약에 반영한다.

주의: JS 위젯으로 첨부를 로드하는 IR 페이지(q4cdn 등)는 md 크롤 원문에 PDF 링크가 아예 안 잡힐 수 있다(실측: amersports.com/investors → 후보 0건). 이때 "첨부 후보 0개"를 "첨부 없음"으로 읽지 않는다 — 모델이 IR/CDN 호스트의 직링크를 브라우저 도구·사이트맵·검색으로 직접 찾아 회수하고 `source-manifest.tsv`에 기록한다.

```bash
python3 scripts/download_attachment_candidates.py <recursive-crawl/attachment-candidates.tsv> --out <attachments-dir>
```

기본으로 `download-report.tsv` 를 같이 남겨 MIME 검증 결과를 기록한다.

### `keep-list-candidates.tsv`

실제 후속 읽기 대상을 여기서만 고른다. recursive crawl 이후 사람이 다시 읽는 범위를 축소하는 장치다.

### `shortlist.tsv`

`keep-list` 가 그래도 넓을 때, 바로 읽을 우선순위 상위 20개다. `attachment` > `b2b-portal` > `local-brand` > `brand-related` > 핵심 `parent-corporate` 순으로 점수를 준다.

## Mirror the shortlisted pages

raw archive는 증거 보존용이고, 최종 읽기용은 별도로 깔끔하게 떨구는 편이 낫다.

```bash
python3 scripts/mirror_selected_pages.py <recursive-crawl/shortlist.tsv> --out <public-mirror-dir>
```

- attachment는 건너뜀
- shortlist/keep-list의 page URL만 다시 저장
- `public-mirror/<host>/<path>.md` 구조를 유지
- 보고서에서 직접 인용하는 페이지는 raw `pages/`가 아니라 이 `public-mirror/` 경로를 source-manifest에 적는다

## Second pass

1차 재귀에서 새 브랜드 도메인이 드러나면 거기서 끝내지 않는다.

```bash
python3 scripts/second_pass_from_shortlist.py <recursive-crawl/shortlist.tsv> \
  --out <second-pass-dir> \
  --mirror-out-root <public-mirror-dir> \
  --attachments-dir <attachments-dir>
```

- `brand-related` 호스트를 실제로 다시 팜 (`--category`로 조정)
- `local-brand` 호스트에서 `/pages/`, `/blogs/`, `/our-company` 계열만 재귀
- 1차에서 글로벌 index만 잡힌 경우 로컬 도메인(`kr.<brand>.com` 등)을 별도 아카이브로 확보
- host 우선순위는 **page seed가 있는 host > attachment만 있는 host**
- 후속 패스에서 새로 발견한 첨부도 `--attachments-dir`로 자동 다운로드

## Further rounds

2차 패스 후에도 팔 가치가 있는 host가 남으면, **그 host의 URL을 시드로 `recursive_surface_crawl.py`를 다시 돌리는 방식으로 반복**한다. 별도 자동 루프는 없다 — 더 갈지/멈출지는 모델이 직접 판단한다:

- 계속 파기: 법인/브랜드 콘텐츠 표면(`about-us`, `who-we-are`, `history` 계열)이 계속 열림
- 멈추기: root/첨부만 있고 실제 확장성이 약함, 또는 같은 카테고리 페이지만 반복됨

각 라운드의 산출물 디렉토리는 `recursive-crawl-v2`, `-v3`처럼 구분하고, 어떤 host를 왜 더 팠는지/멈췄는지는 `01-public-web.md`에 적는다.

## Commerce noise rule

Shopify / D2C surface는 상품/컬렉션 노이즈가 크다. `products/`, `collections/`, `cart`, `checkout`, `account`, `membership` 계열은 기본적으로 읽기 대상에서 제외한다. 허용 표면은 보통 `/pages/`, `/blogs/`, `/our-company`, `/about-us`.

## What success looks like

- 브랜드/법인/모회사 구조가 surface map에 더 선명해짐
- 연관 도메인이 새로 드러남
- first-party 첨부가 추가로 확보됨
- 본문 조사 범위가 오히려 줄어듦

## What failure looks like

- recursive crawl을 했는데도 `keep-list` 없이 전체 md를 다시 훑음
- `shortlist` 없이 keep-list 50개 이상을 그대로 읽기 시작함
- Shopify collections/products가 분석의 대부분을 차지함
- 새 도메인과 새 첨부를 정리하지 않음
- 결과 요약에 `몇 페이지 저장`, `무슨 새 표면 발견`, `무슨 첨부 추가 확보`가 없음
