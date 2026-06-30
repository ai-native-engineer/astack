# Image Generation and Notion Asset Sync

> 목차
> - 출처 우선순위 + 웹 검색 이미지 소싱 (소스 티어, tvly+crwl 파이프라인, 검수 게이트)
> - 1. 먼저 구분 (기존 이식 / 새 로컬 / 생성) - S3 URL 만료 vs file:// 보존 정본
>   - 1-실행: Codex 이미지 생성 호출, base64 회수 (런타임 함정)
> - 2. 새 이미지를 노션 본문에 삽입 (ntn api 블록 업로드/PATCH)
> - 3. 반영 후 검증 (삽입 직후 고유 검증; 전체 round-trip은 notion-sync.md 4-3절)
> - 4. 이미지 생성 규칙 (비자명 규칙 + 로고 처리 정본)
> - 5. 프롬프트 템플릿 (브랜드 UI / 기본 Doc Template / 텍스트 적은 개념 / 텍스트 없는 / 한국어 인포그래픽 / 정확한 한글 대체)

새 이미지나 생성 이미지를 강의 자료 Notion 페이지에 넣을 때 쓴다. 이 파일은 받거나 만든 이미지를 Notion이 읽을 수 있는 ref로 만들어 반영하는 절차를 다룬다. 직접 제작(SVG, HTML/CSS 렌더링, 수동 텍스트 오버레이)은 쓰지 않는다(정본 4절).

**핵심 - 100% 대응 이미지를 찾지 않는다**: 이 자료에 딱 맞는 전용 이미지는 세상에 없다. 못 찾았다고 Codex 생성으로 건너뛰지 마라(사용자가 가장 자주 지적한 실수). 그 개념을 흔히 설명하는 관용, 보편 이미지면 충분하고, 사람이 만들어 많이 쓰이는 이미지가 AI 생성보다 낫다(author-intent 판단원칙).

**이미지 출처 우선순위 (정본, 위에서부터 시도)**:

1. **기존 검증 자료 이식** - 원본 `file://` ref와 caption까지 그대로 보존. 최우선. **단 비판적으로 검토한다**: 기존 이미지가 이 우선순위에 안 맞게 쓰였거나(개념을 추상 일러스트로 때움 등), 원본 스크린샷을 AI로 재생성한 흔적(caption 빈 이미지, 원본과 다른 그림)이면 그 이미지를 버리고 **전수 재조사**해 2~3순위로 다시 확보한다. **원본의 실제 스크린샷, 로고, 도식을 AI로 비슷하게 재생성하지 마라**(고객사 A 1회차 실측).
2. **웹 검색 + 크롤로 찾은 실제 이미지** - 공식 문서 화면뿐 아니라 **공식 로고, 서비스 대표 이미지, 정확한 개념 이미지**(튜토리얼 형식이 아니어도 좋다). Codex 생성물보다 정확, 신뢰. 검증된 도구 조합, 티어, 검수 절차는 아래 **"웹 검색 이미지 소싱"** 블록이 정본.
3. **로그인 없는 화면 직접 캡처** - `chrome-devtools`(안 되면 `playwright`), 로그인 불필요한 메인/랜딩 페이지만. **기존 제품 UI 화면도 공식 사이트 검색(2번)이 먼저** - 공식 스크린샷이 없을 때만 캡처(실측: Supabase Table Editor는 공식 스크린샷이 검색으로 잡힘).
4. **Codex 생성** - 위 1~3을 시도해 실패했을 때만. **개념 설명 이미지엔 쓰지 않는다**(관용 이미지가 반드시 있다). 이번 회차에서 만든 산출물 결과 화면, 목업처럼 세상에 실물이 없는 것만.

**무엇을 어디서 구하나 - 종류로 가른다**:
- **개념 설명 이미지**(Git이란, 데이터 흐름, RAG 구조 등): 1~3만. 관용 이미지가 존재하니 검색/이식으로 구하고 Codex 생성(4)은 금지.
- **기존 제품 UI 화면**(Supabase, GitHub 등 이미 있는 도구): 공식 사이트 검색(2)이 먼저, 없으면 캡처(3).
- **이번 회차에서 만든 산출물 화면**(이 강의에서 만든 그 앱): 세상에 없으니 실제 캡처(3) 또는 Codex 생성(4).

**웹 검색 이미지 소싱** (출처 2번 상세, 실측 검증 2026-06-26 - 개념/설명 이미지)

소스 티어(위에서부터, communication.md 출처 품질 우선순위와 동일):
- 티어 1: AI 벤더 공식 + 공식 튜토리얼/docs. **한 벤더에 묶지 말고 여러 공식 docs를 같이 검색**한다(실측: RAG 최적 다이어그램은 Anthropic이 아니라 AWS 공식). 예: AI 개념은 `docs.aws.amazon.com`, `platform.openai.com`, `docs.anthropic.com`, `cloud.google.com` / 도구는 그 도구 공식(`git-scm.com`, `docs.github.com`, `supabase.com`).
- 티어 2: 공신력 전문기업 자료(IBM, Databricks, Pinecone, Atlassian, Cohere). 티어 1이 빈약할 때만(실측 4사례 전부 티어 1로 충족).
- 티어 3: 일반 블로그. 마지노선, 출처 + 신뢰등급 표기.

도구 파이프라인(실측 순서, 4사례 전부 tvly가 1순위):
1. **tvly로 이미지 직접 검색** - 이미지를 직접 주는 유일한 도구. 티어 도메인 한정. 결과 JSON에 이미지 URL + 페이지 manifest가 같이 와 단독으로 끝나는 경우가 많다.
   ```text
   agents-env run TAVILY_AI_API_KEY@senugw0u -- sh -c 'TAVILY_API_KEY={{TAVILY_AI_API_KEY}} tvly search "<개념> diagram" --include-images --include-image-descriptions --include-domains <티어 도메인 콤마> --max-results 10 --json'
   ```
2. **crwl로 페이지 통째 수확** - tvly 직접 이미지가 빈약하거나 좋은 공식 페이지의 이미지 전부가 필요할 때. 검색이 직접 못 준 다이어그램까지 뽑지만 로고/중복이 섞이니 거른다.
   ```text
   crwl crawl "<찾은 공식 페이지>" -o md | grep -oE '!\[[^]]*\]\([^)]+\)'
   ```
3. **WebSearch/exa 폴백** - tvly가 후보 페이지를 못 줄 때만. 도메인 티어 한정(WebSearch `allowed_domains`는 JSON 배열).

채택 전 검수(생략 금지, 채택을 가르는 단계 - 실측 탈락: 산점도/로고/stale HTML):
- `curl -sL "<url>" -o /tmp/x.<ext>` 후 `file /tmp/x.<ext>`로 진짜 이미지인지 확인(tvly URL이 stale면 PNG 아닌 HTML이 온다).
- 받은 파일을 Read로 직접 열어 개념 다이어그램이 맞는지(산점도/로고/장식/광고 아님), 텍스트 가독성 확인.
- **SVG는 Read로 렌더 안 됨** - `qlmanage -t -s 1600 -o /tmp /tmp/x.svg`로 PNG 변환 후 검수(실측: OpenAI 임베딩 최적 이미지가 SVG).

채택 후: `02-output/assets/<YYMMDD>-<slug>/` 저장 + 티어/도메인을 섹션 하단 북마크 카드로(인라인 출처 금지). 노션 삽입은 2절.

## 1. 먼저 구분

1. **기존 Notion 이미지 이식 (같은/다른 워크스페이스)**
   - 원본 본문의 `file://` attachment ref(`source=attachment:…:spaceId:…`)를 그대로 본문에 넣어 `pages create/update`하면 노션이 그 파일을 대상 워크스페이스로 **복제/보존**한다 - 원본이 다른 워크스페이스여도 연동 봇이 그 워크스페이스에 접근 가능하면 복제된다(실증 2026-06-17 워크스페이스 간 26개)
   - 깨지는 건 `pages get`이 내보낸 **만료 presigned S3 URL**(`?X-Amz-…`)을 본문에 도로 넣을 때뿐 - get 출력 S3 URL은 로컬 .md에 박지 말고 원본 `file://` ref를 유지한다
   - 원본 `file://` ref가 없고 get S3 URL밖에 못 구할 때만 원본 이미지를 내려받아 2절의 업로드 + `ntn api` 블록 삽입으로 넣는다
   - ⚠️ **다른 워크스페이스 ref(워크스페이스 간)는 매 `update`마다 재복제된다**(중복 attachment 생성). 원본 워크스페이스가 살아있으면 작동하지만, **원본 워크스페이스 의존을 끊고 대상 워크스페이스 자립**시키려면: get S3 URL이나 spaceId만 바꾼 ref로는 불가(후자는 `500 Cross-cell memcached` - permissionRecord의 block id가 원본 워크스페이스 것이라 불일치) - 이미지를 내려받아 2절 `ntn files create`로 대상 워크스페이스에 영구 업로드 후 file_upload 블록으로 박는다. 그러면 그 이미지는 .md 마크다운 밖(노션 authoritative)이 되어 이후 .md `update`마다 2절로 재삽입해야 하므로, **자립화는 자료 추림, 확정 후 최종본에서 1회**가 효율적(실증 2026-06-17)
   - 페이지 전체 일괄 복사 금지, PRD 설명처럼 섹션 이해에 필요한 핵심 이미지는 누락하지 않기

2. **새로 만든 로컬 이미지 추가**
   - 새로 만든 로컬 이미지는 아직 노션 attachment ref가 없다 - 로컬 절대경로, 외부 URL을 본문 .md에 넣어 `pages update`하면 노션이 못 읽어 빈 이미지 `![]()`로 깨진다
   - 새 이미지는 2절의 `ntn files create` + `ntn api` 블록 삽입으로 넣는다

3. **이미지 생성**
   - 생성 결과는 임시 다운로드 폴더에 두지 말고 프로젝트 `02-output/assets/<YYMMDD>-<slug>/`에 최종본 저장
   - 디자인, 로고 레퍼런스, 한국어 프롬프트, SVG 금지, 한글 검수 등 생성 규칙은 4절 정본을 따른다. 런타임 호출, 결과 회수 함정은 아래 1-실행.

### 1-실행: Codex 이미지 생성 호출, 회수 (이 런타임 함정)

새 이미지는 `codex exec`의 네이티브 이미지 생성으로 만든다. 이 환경에서 비자명한 3가지:

1. **호출**: `codex exec -s workspace-write -i <레퍼런스로고>.png < prompt.txt`. 프롬프트는 **stdin으로** 준다 - `-i`가 가변인자라 위치 인자 프롬프트를 삼킨다. 로고를 `-i`로 넘기면 실제로 반영된다(공식 로고 정확 재현 실증 2026-06-18).
2. **코드 드로잉 차단**: 프롬프트에 "PIL, matplotlib, SVG, HTML, 코드로 그리지 말고 image_gen으로만 생성"이라고 **명시하지 않으면 codex가 코드(PIL)로 도식을 그린다** - 이 스킬이 금지한 수동 제작이 된다. 명시해야 image_gen 모델을 쓴다.
3. **결과 회수 - 파일로 안 떨어진다**: image_gen 결과가 `$CODEX_HOME/generated_images/`에 저장되지 않는 경우가 많다(내장 저장 헬퍼가 `OPENAI_API_KEY` 필요). 그땐 **최신 세션 jsonl에서 base64를 추출**한다 - `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl`에서 `payload.type=="image_generation_call"` 레코드의 `result`(base64 PNG)를 디코드해 `02-output/assets/<YYMMDD>-<slug>/`에 저장(대상 세션은 `image_generation_call` 개수로 식별). 한 세션에서 여러 장을 생성해 한 번에 추출할 수 있다.

회수한 PNG를 열어 한글을 확대 검수한다(gpt-image 한글 정확도는 양호). 틀리면 텍스트를 줄여 재생성.

## 2. 새 이미지를 노션 본문에 삽입 (`ntn api` 블록 삽입)

만료 S3 URL vs `file://` ref 보존 규칙은 1절 정본 참조. 갈림길: 원본 attachment `file://` ref가 손에 있으면 1절(마크다운 그대로 이식). **새로 만든 로컬 이미지**(노션 attachment가 아직 없음)거나 **get이 내보낸 S3 URL밖에 없는 경우**는 마크다운 `pages update`로 못 넣어(빈 이미지 `![]()`로 깨짐) 아래 2절처럼 **`ntn api`로 이미지 블록을 직접 삽입**한다.

**외부 공개 URL은 image 블록 `external` 타입으로 바로 박지 말 것** - 노션이 `app.notion.com/image` 프록시로 캐시만 하고 원본 CDN에 의존한다(원본이 죽거나 URL 정책이 바뀌면 깨짐). 웹/CDN 이미지도 다운로드해 `file_upload`로 노션에 영구 저장한다(블록 url이 `prod-files-secure.s3`면 노션 보관 = 영구, 실증 2026-06-26 anthropic CDN 84장 영구 업로드).

1. 백업: `NOTION_WORKSPACE_ID=<ws> ntn pages get <page-id> > /tmp/orig-<page-id>.md`
2. 이미지 업로드 -> file_upload id는 출력 **첫 컬럼** (`--json`을 붙이면 pretty 여러 줄 출력이라 `splitlines()[-1]`이 아니라 출력 전체를 파싱해 `id`를 꺼낸다)

```text
NOTION_WORKSPACE_ID=<ws> ntn files create --filename <name>.png --content-type image/png < <path>.png
```

3. 삽입 위치 앵커 block id - 이미지 **바로 앞에 올 블록의 텍스트**로 찾는다

```text
NOTION_WORKSPACE_ID=<ws> ntn api "/v1/blocks/<page-id>/children?page_size=100" 2>&1 | head -c 40000
```

   - ⚠️ **`timeout` 명령으로 감싸지 말 것** - ntn 출력이 통째로 막혀 빈 응답이 된다(실측). hang이 **출력 시작 후**면 `| head -c N`의 SIGPIPE로 끊는다. hang이 **0바이트(출력 전)**면 직전 auto-background된 ntn이 키체인 락을 점유한 것 - `pkill -f "ntn api"`(+필요시 `ntn doctor`) 후 **foreground로** 재시도한다. blocks GET을 background로 돌리지 말 것(락 연쇄로 영구 hang).
   - 파싱: 앵커 텍스트를 찾고 **그 텍스트 뒤 2번째 `"id"`가 그 블록 id**다(1번째는 `created_by.id`). 응답이 잘려 JSON이 깨지면 그 구간만 정규식으로 뽑는다.

4. 이미지 블록을 앵커 **뒤(`after_block`)**에 삽입 - body는 stdin(셸 mangling 회피)

```text
{"children":[{"object":"block","type":"image","image":{"type":"file_upload","file_upload":{"id":"<upload-id>"}}}],"position":{"type":"after_block","after_block":{"id":"<anchor-id>"}}}
```
```text
NOTION_WORKSPACE_ID=<ws> ntn api --method PATCH "/v1/blocks/<page-id>/children" < body.json
```

   - `position`: `{"type":"after_block","after_block":{"id":…}}` / `{"type":"start"}` / `{"type":"end"}`. 옛 `after` 키는 400(2026-03-11 스펙에서 `position`으로 바뀜).

5. 정리: 옛 staging 페이지, `<page url=...>` 링크가 본문에 남지 않게.

## 3. 반영 후 검증

```text
NOTION_WORKSPACE_ID=<ws> ntn pages get <page-id> > /tmp/after-<page-id>.md
```

삽입 직후 고유 검증(이 절, `/tmp/after-<page-id>.md`로 확인):
- 이미지가 의도한 앵커 **다음 위치**에 있는지
- 기대한 신규 이미지 개수만큼 이미지 블록 증가 (이미지가 `![](https://prod-files-secure…)` S3 URL로 보이는 건 정상 - 노션엔 실제 이미지 블록이 박혀 있음)
- 유실 시 2절로 재삽입하거나 이미지 주변만 `ntn api` 블록 PATCH로 수정 (만료 S3 URL vs `file://` 보존은 1절 참조)

반영 후 전체 round-trip 검증(빈 이미지 `![]()` 0, `<page url=>` 0, 기존 이미지/GIF/첨부 보존, frontmatter/중복 H1/출처 aside 누출 없음, 로컬 교안 파일 동기화)은 notion-sync.md 4-3절.

## 4. 이미지 생성 규칙

모델이 이미 아는 일반 디자인 상식은 생략한다. 아래는 이 맥락의 비자명한 규칙만.

**톤, 워크플로**
- 별도 지시가 없으면 강의 자료 이미지는 **Notion Doc Template 톤**으로 만든다.
- 이미지 톤 후보를 여러 개 만들지 않는다. 기존 Notion 이미지가 있으면 먼저 이식하고, 없으면 기본 톤으로 바로 제작한다.
- 이미지 생성 프롬프트는 기본 한국어로 작성한다. 영어 템플릿은 참고 구조로만 쓰고, 실제 생성 요청은 한국어 강의 자료 맥락과 수강생이 보는 UI 행동에 맞게 바꾼다.
- 새로 **만드는** 이미지(원자료에 실물이 없는 산출물 목업, 추상 개념 도식)는 Codex 자체 이미지 생성 기능으로 만든다 - 공식 문서, 원자료에 실제 이미지가 있으면 그걸 web검색으로 가져오는 게 먼저다(출처 우선순위 intro).

**로고 처리 (정본)** - 브랜드 UI 프롬프트(5절)도 이 절차를 따른다.
- 서비스, 회사, 제품과 관련된 강의 이미지는 브랜드 맥락을 먼저 확인한다. 공식 로고/브랜드 자산/신뢰 가능한 투명 배경 로고를 찾아 로컬 자산으로 보관한다. Codex 이미지 생성 도구가 명시적 이미지 입력을 지원하면 그 로고 파일을 실제 레퍼런스로 전달하고, 명시적 입력이 없으면 로고 파일을 먼저 열어 시각 컨텍스트에 올린 뒤 프롬프트에 공식 로고의 형태/색/금지사항을 명시한다.
- 로고는 사실성을 높이는 기준 자산이다. 기억으로 재현하거나 유사 로고를 새로 만들지 않는다. 생성 결과를 확대 검수하기 전에는 로고 레퍼런스 반영을 완료로 보지 않는다. 로고 파일을 확실히 확보하지 못하거나 결과에서 로고 반영을 검증할 수 없으면 브랜드 로고 없이 실제 UI 관계성이 보이는 화면, 대시보드, 데이터 테이블, 설정 패널 중심으로 만든다.
- 서비스 로고와 실제 UI 관계가 중요한 장면은 추상 아이콘 카드보다 제품 화면 맥락을 우선한다. 예: Base44 자료는 Base44 로고 레퍼런스와 앱 빌더 화면, Dashboard Data, Preview, Users/Permissions 설정처럼 수강생이 실제로 찾을 UI 위치가 보이게 만든다.

**금지, 한글 검수**
- SVG, HTML/CSS 렌더링, 수동 텍스트 오버레이, 직접 도식 제작을 대체 경로로 쓰지 않는다.
- 생성 이미지 안의 한글은 확대해서 직접 읽고, 한 글자라도 틀리면 폐기한 뒤 Codex 이미지 생성으로 다시 만든다.
- 이미지 안 텍스트는 허용된다. 다만 긴 문장보다 짧은 제목, 라벨, 핵심 문장을 우선하고, 필요한 경우 더 짧은 문구로 다시 생성한다.

**배치, 캡션, 출처**
- 이미지를 넣는 구간은 이미지 블록을 먼저 두고, 그 다음 본문 설명을 이어간다.
- **여러 페이지에 걸친 누적 자료(허브/시리즈)는 같은 이미지를 여러 페이지에 배치해도 정상** - 페이지를 독립적으로 보기 때문이다. 이미지 url별 전역 dedup으로 한 페이지에만 남기면 다수 페이지가 이미지를 잃어 소극적이 된다(실증 2026-06-26: dedup으로 절반이 빠져 사용자가 "이미지가 소극적"이라 지적 -> 완화 후 39->84장). 같은 페이지 내 같은 이미지 중복만 제외하고, 페이지 간 중복은 허용한다.
- `흐름도로 다시 보기` 같은 후행 이미지 섹션을 새로 만들지 않는다.
- 이미지 아래에 "이 이미지는..." 식 설명 문단이나 캡션을 붙이지 않는다. 이미지는 주변 본문 이해를 돕는 시각 자료이고, 설명은 본문 흐름 안에서 이어간다.
- 이미지를 넣은 섹션의 본문이 이미지 내용을 다시 설명해야 한다. 이미지만으로 핵심 개념을 전달하게 두지 않는다.
- **공식 문서/공식 사이트에서 가져온 설명 이미지는 그 출처를 섹션 하단에 북마크 카드로 단다**(notion-sync.md 4-2절). 캡션 금지는 "이 이미지는…" 식 설명 문단을 막는 것이지 출처 북마크를 막는 게 아니다. 본문에 `[출처: URL]` 텍스트는 박지 않는다(anti-patterns.md 2절).

## 5. 프롬프트 템플릿

### 브랜드/서비스 UI 기반 강의 이미지

서비스, 회사, 제품이 직접 등장하는 자료에 우선 사용한다. 로고 처리(확보/명시적 입력 전달/미지원 시 먼저 열기/확대 검수/검증 불가 시 대체)는 4절을 따른다. 로고 이미지는 `02-output/assets/<YYMMDD>-<slug>/`에 저장한다.

```text
레퍼런스 처리:
- 명시적 이미지 입력 지원 시: [공식/신뢰 가능한 투명 배경 로고 이미지]를 실제 레퍼런스로 사용
- 명시적 이미지 입력이 없을 시: 먼저 열어 확인한 공식 로고의 형태/색/금지사항을 아래에 적고, 생성 후 결과를 확대 검수
- 로고 반영을 검증할 수 없으면 로고 없는 현실적인 UI 장면으로 생성

강의 자료용 16:9 이미지를 만들어주세요.

주제:
[서비스/도구]에서 [수강생이 확인해야 하는 UI/개념/절차]

목표:
수강생이 실제 제품 화면에서 어디를 보고 무엇을 검수해야 하는지 바로 이해하게 합니다.

반드시 포함할 것:
- 검증 가능한 경우에만 공식 로고를 기반으로 한 실제적인 브랜드 맥락
- [도구명]의 현실적인 앱 빌더/대시보드/설정 화면 느낌
- 본문 섹션과 직접 연결되는 UI 영역: [예: Preview, Dashboard Data, Users, Permissions, Publish]
- 추상 아이콘 카드보다 실제 화면과 작업 위치가 보이는 구성

텍스트:
- 긴 문장 금지
- 필요하면 짧은 UI 라벨 수준만 사용
- 한글이 들어가면 철자를 정확히 유지

스타일:
- Notion 강의 자료에 들어갈 현실적인 제품 UI 스크린샷형 이미지
- 밝은 배경
- 깔끔한 SaaS 대시보드 톤
- 과장된 마케팅 배너나 장식용 일러스트 금지

금지:
- 가짜 로고 invent
- 실제 로고와 다른 유사 로고
- 무관한 브랜드 로고
- 추상 배경만 있는 이미지
- 캡션/설명 문단이 이미지 안에 들어간 구성
```

### 기본: Notion Doc Template 강의 이미지

강의 자료에 새 이미지를 만들 때 기본으로 사용한다. 노션 본문과 자연스럽게 붙는 문서형 이미지다. 설명 이미지가 필요할 때 별도 스타일 후보를 만들지 말고 이 톤으로 바로 제작한다.

```text
Use case: Korean educational infographic
Asset type: Notion document template style image for course material

Primary request:
Create a 16:9 Korean course image in a clean Notion document / worksheet template tone.
It should feel like a premium Notion lesson page preview, not a generic slide and not a decorative illustration.

Audience:
Korean non-developer professionals learning [강의 주제].

Subject:
[주제/개념/절차]

Text:
Title: "[제목]"
Subtitle: "[한 줄 정의]"
Labels:
- "[라벨 1]"
- "[라벨 2]"
- "[라벨 3]"
- "[라벨 4]"
Bottom note: "[핵심 문장]"

Visual structure:
- Looks like a clean Notion-style page section.
- Use a title block, definition block, and compact process or comparison blocks.
- Use minimal icons, callout boxes, subtle dividers, and clean table-like rows.
- Keep the layout calm, modular, and practical.
- Korean text must be large enough to read at Notion page width.

Color / mood:
- Off-white or white background.
- Graphite navy text.
- Muted teal highlights.
- Sage green support color.
- Soft yellow callout for the key takeaway.
- Mature B2B course material, not playful.

Constraints:
- Do not add extra words.
- Do not translate the Korean.
- Do not invent labels.
- Keep all Korean spelling exact.
- No fake Notion UI labels.
- No unreadable placeholder text.

Avoid:
- generic PowerPoint slide look
- classroom worksheet look
- cartoon people
- bright childish colors
- heavy shadows
- dense tutorial checklist
- random English or Korean text
```

### 텍스트가 적은 개념 이미지

한글 정확도가 중요하거나 문장이 길면, 이미지 안 텍스트를 짧은 제목, 라벨 중심으로 줄이고 본문에서 설명한다. 텍스트 없는 배경을 만든 뒤 별도 렌더링으로 글자를 올리는 방식은 쓰지 않는다.

```text
Create a 16:9 Notion document template style course image.
Use no readable text except the exact short Korean title below.

Topic:
[주제]

Show this structure:
1. [짧은 제목 영역]
2. [핵심 개념/흐름을 보여주는 문서형 블록]
3. [하단 핵심 메시지를 암시하는 callout 영역]

Visual style:
- clean Notion-style page section
- off-white background
- modular document blocks
- subtle dividers
- muted teal and sage highlights
- soft yellow callout area
- minimal icons only
- do not leave space for later text overlay
```

### 텍스트 없는 개념 설명 이미지

```text
Use case: educational course material
Asset type: Notion lesson concept image
Audience: non-developer business learners

Create a clean 16:9 educational diagram that explains [개념] in the context of [업무/수업 주제].

Scene:
- Show [현재 상태/문제] on the left.
- Show [중간 과정/전환] in the center.
- Show [목표 상태/결과] on the right.

Visual style:
- Modern flat editorial illustration
- Clear hierarchy, generous spacing, realistic work-tool details
- Restrained palette with navy, teal, green, and warm accent colors
- White or very light background

Text:
- No readable text, no labels, no fake UI copy
- Use icons, shapes, arrows, and layout to communicate the flow

Avoid:
- Decorative gradient blobs, stock-photo atmosphere, vague abstract art
- Tiny unreadable UI
- Random English or Korean text
```

### 한국어 인포그래픽 이미지

```text
Use case: Korean educational infographic
Asset type: Notion lesson infographic
Audience: non-developer business learners

Create a polished 16:9 Korean infographic about [주제].

Text must be exactly:
Title: "[제목]"
Subtitle: "[한 줄 정의]"
Section 1: "[섹션명]"
- "[짧은 문장 1]"
- "[짧은 문장 2]"
Section 2: "[섹션명]"
- "[짧은 문장 1]"
- "[짧은 문장 2]"

Visual structure:
- Large title at top
- 3 to 5 clearly separated blocks
- Simple icons and arrows
- High contrast Korean text, large enough to read in Notion

Constraints:
- Do not add extra words.
- Do not translate the Korean.
- Do not invent labels.
- Keep all Korean spelling exact.
- If the Korean text is wrong in the generated result, shorten the text and regenerate with Codex image generation.
```

### 정확한 한글이 필수일 때의 대체 프롬프트

```text
Codex 이미지 생성으로 강의 자료용 16:9 이미지를 만들어주세요.
한글 문구는 아래 짧은 제목만 넣고, 나머지는 아이콘, 문서 블록, 흐름 구조로 표현하세요.

주제:
[주제]

보여줄 흐름:
1. [왼쪽 장면]
2. [가운데 장면]
3. [오른쪽 장면]

스타일:
- 강의 자료용 16:9 도식
- 밝은 배경
- 업무 도구 화면, 문서, 화살표, 체크 표시 중심
- 한글 제목 외 읽을 수 있는 문자는 넣지 않기
```

한글 오탈자, 왜곡이 있으면 폐기하고 Codex 이미지 생성으로 다시 만든다. SVG, HTML/CSS 렌더링, 수동 텍스트 오버레이로 보정하지 않는다.
