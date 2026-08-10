---
argument-hint: "[url]"
name: crawl
description: "Free local web/documentation crawler that converts URLs and sites to markdown without API keys, accounts, credits, or quotas. Use when user gives a URL to read/save/analyze, asks 크롤링/crawl/웹페이지 읽어/사이트 긁어/문서 크롤링, or needs local markdown extraction from pages/docs. Do NOT use for broad web search/ranking, paid API research, local files, Google Workspace/Notion data, or Korean public-data APIs."
---

# Crawl

PATH에서 확인되는 공식 `crwl` CLI(crawl4ai) + 이 스킬의 `scripts/`로 웹페이지·문서를 마크다운으로 변환.
**권위 소스: `crwl crawl --help`, `crwl examples`, 각 스크립트 `--help`.** 여기엔 모드 선택과 비자명한 함정만 둔다. 스크립트 작성·crawl4ai API는 주제별 reference:
- `references/crawl4ai-api.md` — 코어(CLI·발견/추출 분리·deep-crawl·seeding·마크다운·캡처·정제·실측 함정)
- `references/crawl4ai-robustness.md` — 안 되는 사이트 대응(봇 차단·동적/무한스크롤·Shadow DOM·로그인 세션·프록시·지역위장·동시성)

## 모드 선택 — crwl CLI 우선, 스크립트는 CLI가 못 하는 것만

기본은 공식 `crwl` CLI. CLI로 안 되는 것(페이지별 파일 미러링, deep-crawl URL 범위 제한, 본문 셀렉터 자동선택·크롬 정화·이미지)일 때만 `scripts/`의 특화 스크립트를 쓴다. CLI 전체 옵션은 `crwl crawl --help`.

| 작업 | 도구 |
|---|---|
| 한 페이지 → md | `crwl crawl <url> -o md` (stdout, 저장은 `-O f.md`) |
| 섹션 deep-crawl → **한 파일 합본** | `crwl crawl <url> -o md --deep-crawl bfs --max-pages N`. 페이지가 `# <URL>` 구분선으로 이어 붙는다(읽기·grep용). 단 인라인 `--deep-crawl`은 URL 범위가 안 막혀 도메인 전역으로 샌다 → 범위 제한은 `-C cfg.json`(아래 "CLI deep-crawl 범위 제한" 절) |
| 섹션 → **페이지별 파일** 미러 + 크롬 정화(+`--assets` 이미지) | `scripts/crawl-mirror.py`. AI에 먹일/사람이 볼 깔끔한 문서 아카이브용 ⬇ 주력 |
| 미러의 소유 호스트 PDF 원본 수집 | `scripts/pdf-mirror.py` (`--host` 필수, 100MB 초과 로컬 보관은 `--oversize-dir`) |
| 대형 생성 Markdown을 순서 보존 조각으로 분할 | `scripts/split-markdown.py` |
| 저장된 미러의 자막 fold·대용량 문서 검증 | `scripts/verify-mirror.py` |

⚠ `crwl crawl`의 기본 출력은 마크다운이 **아니다** — `-o`를 빼면 stdout이든 `-O` 파일이든 html 포함 JSON 덤프가 나온다(`.md` 확장자도 무시됨). `-O`는 경로만 정하고 포맷은 `-o`가 정한다. 마크다운은 항상 `-o md`(본문만은 `-o md-fit`)로 명시한다. (`crawl-mirror.py`는 포맷을 자체 처리하므로 예외.)

## 문서 사이트 -> URL 경로 미러링 (주력)

**출력 경로: 항상 현재 디렉토리(`.`)** — 사용자가 명시하지 않으면 `--out`을 별도 지정하지 않는다. 두 모드:

```bash
# 전체 크롤: --pattern이 따라갈 URL 범위(= prefix). 여러 페이지를 페이지별 파일로 미러
scripts/crawl-mirror.py <seed-url> --pattern "*<host>/<path>*" --lang en [--assets]
# 단일 페이지: 그 URL 1장만 (deep-crawl, cross-page 정제 없음)
scripts/crawl-mirror.py <url> --single [--assets]
# -> ./<host>/<path>/<page>.md  (URL 경로 = 파일 경로, 페이지당 1파일, source 주석 포함)
```

**추출 파이프라인**(nav/footer 제거 + 이미지 보존): `target_elements`로 본문 위주 추출(발견은 전체 DOM 유지) -> 전체 크롤이면 **cross-page 반복 제거**(여러 페이지 공통 줄 = nav/footer, 이미지 줄은 페이지 고유라 보존) -> `strip_chrome`(Mintlify 패턴). 이미지는 `--assets`로 로컬 다운로드 + 상대경로 치환. `https://host/a/b` -> `host/a/b.md`(디렉토리이자 페이지인 경로는 `a.md`와 `a/`가 공존).

## 문서 사이트 함정 (crawl-mirror.py 기본값에 반영됨)

모르고 `crwl -C`로 통째 긁으면 수천 페이지·잡음 범벅이 된다. 직접 크롤 스크립트를 짤 때도 이 5가지를 챙긴다:

- **로케일 폭발**: devsite/구글 문서는 footer에 `?hl=<언어>` 변형 링크가 있어 deep-crawl이 ~20배로 불어난다(실측: 문서 198개 → 2913페이지). → `*hl=*` 링크를 안 따라가고 언어는 Accept-Language(`--lang`)로 고정한다. bare URL은 브라우저 로케일을 따르므로 영어 원문은 `--lang en`.
- **발견과 추출 분리 — 본문 한정은 `target_elements`로(`css_selector` 아님)**: `css_selector`는 "entire extraction process"에 영향을 줘 셀렉터 밖 nav 링크까지 잘리고, nav가 본문 밖인 사이트(MkDocs 등)에서 deep-crawl 발견이 무너진다(실측: docs.crawl4ai.com `css_selector='main'` 24개 vs `target_elements` 118개 발견). `crawl-mirror.py`는 본문 후보(devsite `.devsite-article-body`/Mintlify `#content-area`/`main`/`article`)를 `target_elements` 리스트로 한 번에 넘긴다 — 추출만 본문에 한정하고 링크 발견은 전체 DOM 유지, 미매칭 시 전체 페이지로 graceful degrade라 셀렉터 자동승격·폴백이 불필요. nav/footer는 본문 밖이라 추출에서 자동 제외된다(`excluded_tags`로 nav를 지우면 그 안 링크까지 사라져 발견이 다시 막히므로 쓰지 않는다). 새 플랫폼이어도 보통 `--selector` 없이 된다.
- **끊긴/오타 링크(404)**: deep-crawl에 스퓨리어스 URL이 섞인다(예 `.../articl`, 존재하지 않는 별칭). → 추출 본문 길이 게이트(`--min-len`)로 버린다.
- **Mintlify 마크다운 크롬**: 헤딩이 `## `+제로폭 앵커 링크+텍스트 3줄로 쪼개지고, `Copy page` 버튼·`Was this page helpful?` 푸터·제목 위 eyebrow가 박힌다. → `crawl-mirror.py`가 저장 전 자동 제거(`strip_chrome`, 패턴 없으면 no-op).
- **이미지는 기본 미다운로드**: raw_markdown은 원격 이미지 URL 참조만 남긴다(CDN 링크라 나중에 깨질 수 있음). 사람이 볼 자료·오프라인 보존엔 `crawl-mirror.py --assets`로 페이지 옆 `<page>.assets/`에 받아 상대경로로 치환한다. AI에 먹일 용도면 불필요.

## CLI deep-crawl 범위 제한 (`-C` 라우트)

`crwl` 플래그로는 deep-crawl을 URL 프리픽스로 못 막는다. 인라인 `--deep-crawl`은 빈 FilterChain + `max_depth=3` 고정이라 도메인 전역으로 샌다(`-c`는 스칼라만, `-f`는 본문 필터). 범위 제한은 `FilterChain(URLPatternFilter)`를 담은 `-C` config로만 되고, `scripts/gen-deep-config.py`가 그 config를 만든다.

## 그 외

- 출력이 길면 stdout 대신 `-o md -O f.md`로 저장 후 Read (폭주 방지).
- 봇/JS 차단·로그인: `-b headless=...` 조정, 인증은 프로필(`crwl profiles`로 생성 후 `-p`).
