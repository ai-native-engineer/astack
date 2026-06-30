# 강의 자료 수정, 노션 반영 (Phase 4 - ntn 전용)

curriculum 스킬의 Phase 4 세부. 발산 게이트 다음 ntn 안전 동기화, 그다음 round-trip 검증.

**원칙 - 노션이 강의자료 정본(SoT)/버전 보관소.** 발행된 회차 페이지의 원본은 노션이고 버전 히스토리도 노션이 갖는다. 반영은 "로컬 -> 노션 전체교체" 한 방향으로 고정하지 않는다 - 로컬에서 작업한 경우와 노션에서 직접 편집한 경우 둘 다 정상 흐름이라, 작업 시작 시 **4-R 라우터**로 베이스(어디가 최신이냐)와 방식(surgical 부분 반영 / 전체교체)을 먼저 정한다. 로컬 `.md`는 정본이 아니라 **게이트 입력용 작업 파생물**이다(케이스 2,3은 노션을 직접 API로 떠서 시작) - `02-output/`엔 최신 작업본만 둔다(옛 버전/백업을 쌓지 않는다). 로컬 옛 버전/백업 정리(삭제)는 4-1절로 노션이 로컬보다 앞서는지 확인한 뒤 앞설 때만, 확인 불가(접근 안 됨/trash)면 보존.

## 4-R. 베이스 선택 라우터 (반영 시작 전 첫 단계)

반영을 한 방향으로 고정하지 않는다. 직접 API로 노션 상태를 확인해 **베이스**(어디가 최신/정본이냐)와 **방식**(surgical 부분 반영 / 전체교체)을 먼저 정한다.

| 상황 | 베이스 | 방식 | 절차 |
|---|---|---|---|
| 1) 노션에 페이지 없음(신규 첫 빌드) | 로컬 작성본 | 전체 push 1회 | 4-2 표준 절차 + `notion_reflect.py`(이미지 삽입) |
| 2) 페이지 있음, 마지막 편집 = 연동 봇 | 로컬 작업본 | surgical 부분 반영 | 노션 fetch -> 변경 블록만 직접 API(4-0 성숙 페이지) |
| 3) 페이지 있음, 마지막 편집 = 사람(직접 편집) | **노션 현재본** | surgical 부분 반영 | 4-1 발산 게이트(노션 베이스에 변경만 재적용) |

- **판정** - `GET /v1/pages/<id>`(4-0 신뢰 채널)의 `last_edited_by`(연동 봇 vs 사람) + `last_edited_time`. 봇이 마지막이면 케이스 2, 사람이 마지막이면 케이스 3, 애매하면 멈추고 사용자에게 묻는다.
- **기본 = surgical.** 전체교체(`ntn pages update`)는 케이스 1(신규), 의도적 전체 재작성에서만 쓴다 - 전체교체는 file:// 접근/제목 변경/자산 유실 위험을 동반한다(4-2). 성숙 페이지는 변경 블록만 직접 API로 고치고 사전 diff 승인(4-0).
- **게이트 입력 = 작업 파생물.** 케이스 2,3은 작업 시작 시 노션을 직접 API로 떠 `/tmp/orig-<id>.md`로 만들고(4-0 신뢰 채널, 4-2 백업과 동일 파일 - ntn get은 크로스 오염 가능) 그 위에서 변경분 계산 + 게이트(verify-media/review-draft/gate-review) 실행 -> surgical 반영. 로컬 .md를 노션에서 재생성해 발산 자체를 줄인다.

## 4-0. 안전 전제 (파괴적 쓰기 전 필수)

`ntn pages update`는 전체 교체 = 파괴적. 그 전에 넷을 지킨다:

- **신뢰 채널** - ntn 읽기는 hang/0바이트/**크로스 오염**(다른 페이지 내용이 섞여 나옴)이 실측됐다(2026-06-19). 오염된 읽기 위에서 비교/검증하면 거짓 통과한다. 파괴적 쓰기 전/후의 상태 확인/발산 게이트/round-trip은 **직접 Notion REST API**로 한다: `agents-env run NOTION_API_KEY@<tag> -- python3/curl`(토큰을 child에만 주입, `GET /v1/pages/<id>`, `/v1/blocks/<id>/children`; 이미지 삽입은 `POST /v1/file_uploads` 후 image 블록 `after_block` PATCH). page-id 실존 확인은 `curriculum_gate.py verify-pages`가 이 채널을 쓴다(토큰 태그는 4-2절). ntn hang/timeout/0바이트가 보이면 즉시 직접 API로 폴백.
- **페이지 정체성** - AGENTS의 page-id 매핑은 stale일 수 있다. 쓰기 전 직접 API로 `title`과 본문 첫 섹션이 의도한 회차와 맞는지 확인한다(예: "4회차"라 적힌 id가 실제 "3회차" 페이지일 수 있음).
- **성숙 페이지 = surgical** - 이미 발행됐거나 사용자가 직접 발전시킨 페이지는 전체교체 금지. 변경 블록만 직접 API로 고치고, **무엇이 바뀌는지 diff를 먼저 사용자에게 보여 승인**받은 뒤 반영한다. "추가"는 추가만 - 최소 diff.
- **충실도 사이드카 (외부 훅, 우회 불가)** - `notion_reflect.py` 쓰기는 PreToolUse 훅 `~/.claude/hook-utils/curriculum-write-gate.py`가 가로채 본문 옆 `<본문>.fidelity.json`(이식 원본을 `sources`로 선언)을 요구한다. 소스에 없는 net-new(발명) 블록 비율이 한도를 넘으면 쓰기를 차단한다(`--skip-gate`로 못 뚫음 - gate-review와 별개 훅). 반영 전에 사이드카로 기존 자료 소스를 선언하고 본문을 그 흐름/구조 그대로 이식한다.

## 4-1. 발산 게이트 (케이스 3 노션 직접 편집 - 베이스를 노션으로)

노션 직접 편집은 막을 사고가 아니라 "정본이 노션으로 갔다"는 정상 신호다(4-R 케이스 3). 다만 전체교체(`ntn pages update`)로 로컬을 올리면 그 편집이 사라지므로, 케이스 3이면 **로컬이 아니라 노션을 베이스로** 삼아 이번 변경만 재적용한다(surgical). **반영 전 항상** (비교 입력은 4-0절 신뢰 채널 읽기로 - 오염된 ntn 읽기 위 비교는 거짓 통과):

> 실증: 사용자가 노션에서 의도적으로 지운 표가 로컬엔 남아 덮을 뻔 - 베이스라인 대조로 잡아 노션 기준 재적용.

1. **베이스라인 diff (주 신호)** - 4-2절의 `/tmp/orig-<id>.md`를 직전 동기화본/로컬과 정규화 diff(프론트매터/코드블록 탭 차이 무시). 노션에만 있는 추가/삭제 = 직접 편집 후보.
2. **타임스탬프 교차확인 (보조 - diff가 모호하거나 직접편집이 의심될 때만)** - `ntn pages get <id> --json`의 `last_edited_time`(KST), `last_edited_by`를 직전 반영 기록(프로젝트 AGENTS.md 동기화 로그)과 비교. 노션이 더 최근이고 편집자가 연동 봇이 아니면 직접 편집 신호.
3. **갈라졌으면 멈추고 사용자에게 묻는다** - "노션 vs 로컬, 어느 게 최신/정답이냐". **자동 진행 금지.** 우선순위 기본값: **기존 로컬 < 노션(사용자 직접 편집) < 이번 AI 편집.**
4. **노션이 기준이면 베이스 교체** - 로컬을 베이스로 쓰지 말고 **노션 베이스라인에 이번 변경만 재적용**(변경마다 `body.count(old)==1` 단언 후 replace, 그다음 push). 로컬 `.md`도 그 결과로 정렬해 이후 동기 유지.
5. **역동기화 diff는 노이즈 제거 후** - 사용자 노션 편집을 로컬로 가져올 때, `ntn pages get` 출력은 round-trip 노이즈 탓에 raw diff로는 편집을 못 가린다. 정규화 후 비교: 1. 맨 위 `---title---` frontmatter 제거 2. `permissionRecord`의 block `id`(업로드마다 재생성) 마스킹 3. `\[`, `\~` 이스케이프 해제 4. `<colgroup>` 제거 5. 행 들여쓰기 무시. 남는 차이가 실제 사용자 편집이다(실증 2026-06-10: raw 239줄에서 실제 편집 2건으로 좁혀짐).

## 4-2. ntn 동기화 (전체교체 - 케이스 1 신규 빌드/의도적 전체 재작성용)

**워크스페이스 지정**: 모든 `ntn` 명령 앞에 `NOTION_WORKSPACE_ID=<workspace-id>`를 붙인다. ID는 `강의자료 워크스페이스=<lecture-workspace-id>`, `조직 워크스페이스=<org-workspace-id>`, `me=<my-workspace-id>`. 검증은 `NOTION_WORKSPACE_ID=<workspace-id> ntn api /v1/users/me`의 `workspace_name`. 직접 REST(verify-pages 등)용 토큰 태그는 `agents-env ls | rg -i notion`으로 고른다(워크스페이스별로 다름) - 토큰의 실제 워크스페이스는 `/v1/users/me`의 `bot.workspace_name`으로 검증한다.

**AI 에이전트/백그라운드는 ntn 명령도 keychain 대신 환경변수 토큰으로 감싼다** - keychain은 헤드리스, 화면잠금에서 `Failed to fetch token from keychain`으로 막힌다(토큰 등록돼도 못 읽음). `agents-env run NOTION_API_KEY@<tag> -- sh -c 'NOTION_API_TOKEN={{NOTION_API_KEY}} NOTION_WORKSPACE_ID=<id> ntn ...'`로 감싸면 작동하고, 아래 4-2절 '키체인 락' hang도 사라진다. curriculum 강의자료는 lecture-ws=`<lecture-ws-token>`, org-ws=프로젝트 지정 조직 워크스페이스 토큰를 쓴다. `<company-ws-token>` 토큰은 회사 데이터용이라 강의자료 반영에 쓰지 않는다. integration 토큰이라 연결된 페이지, DB만 접근(404면 태그나 공유 범위가 틀린 것). 정본: notion `references/ntn-cli.md`, auto-memory `reference_ntn_agent_auth`(토큰 태그 매핑).

**전체교체 프리플라이트 - 로컬 .md에 없는 노션 자산은 날아간다:**

| 자산 | 추출 | 처리 |
|---|---|---|
| 이미지/GIF | `get`은 만료 presigned S3 URL `![](…?X-Amz-…)`로 내보냄 | **전체교체 보존/유실 조건만**: 본문에 원본 `file://` attachment ref(`source=attachment:…`)가 있으면 `update` 후 노션이 복제/보존, **ref를 빼거나 get S3 URL로 갈아끼우면 유실**. file:// ref 없는 새 로컬 PNG만 `ntn api` 블록 삽입. 워크스페이스 간 복제/자립화 등 상세/함정은 `image-generation-notion-assets.md` 1절, 2절이 정본. **여러 페이지 배치 update 금지** - 한 페이지씩 |
| 북마크 카드 | `<unknown url=… alt="bookmark"/>` | **실제 발동하는 보존 규칙** - 본문에 이 ref가 있으면 그대로 두면 보존된다(실증: day5 opengraph/보안 페이지 code.claude.com 북마크). ref 없으면 update가 날린다. update로 **신규 생성은 불가**(400)라, 새 카드는 `PATCH /v1/blocks/<parent>/children` body `{"children":[{"type":"bookmark","bookmark":{"url":"…"}}]}`(직접 REST/`ntn api`, `position`으로 위치 지정). 사이트 링크를 화면 캡처 대신 북마크로 넣을 때 쓴다(실증 2026-06-21 1회차 다운로드 링크) |
| child_page | 별도 페이지 | update는 안 건드린다(`--allow-deleting-content` 안 씀이 기본). **신규 child_page 생성은 update로 불가, Notion API(`POST /v1/pages`, `parent`에 회차 페이지 id)로 생성** |
| unknown 블록 | `<unknown …/>` (`external_object_instance` 등) | 본문에 있으면 그대로 보존. 빼고 update하면 유실, 새로 만들면 400. 보존/이동만 |

**표준 절차:**
```text
NOTION_WORKSPACE_ID=<workspace-id> ntn datasources resolve <db-id>                    # (1) DB->data-source
NOTION_WORKSPACE_ID=<workspace-id> ntn datasources query <ds-id> --limit 1000         #     전수(기본/100은 컷)
NOTION_WORKSPACE_ID=<workspace-id> ntn pages get <page-id> > /tmp/orig-<page-id>.md    # (2) 백업 + 4-1절 게이트 입력
NOTION_WORKSPACE_ID=<workspace-id> ntn pages get <page-id> --json > /tmp/orig-<page-id>.json   #   last_edited_time, 진단
# (4) 4-1절 발산 게이트 통과 + 위 자산 4종 병합
NOTION_WORKSPACE_ID=<workspace-id> ntn pages update <page-id> < page.md               # (5) stdin 권장(--content 공백 구문은 ---, # 시작 시 플래그 오인)
# (6) 4-3절 검증
```

**이미지 보존 두 방식** (전체교체 시 로컬 .md에 없는 이미지는 유실 - 둘 중 하나로 보존):
1. **file:// 보존** - 기존 노션 이미지를 그대로 유지(재업로드 안 함). 로컬 .md에 원본 `file://` attachment ref가 있을 때만. 텍스트만 바뀐 surgical 수정에 적합(위 표 이미지 행).
2. **로컬 재업로드** - 로컬 .md가 이미지를 **로컬 경로**(`![](../assets/x.png)`)로 참조하거나 출처를 `[[bookmark: URL]]` 디렉티브로 둘 때(리폼/재생성 클립). `scripts/notion_reflect.py --candidates curriculum-candidates-*.md --report <검수.md> <page_id> <local.md> [...]`: 이미지/북마크 디렉티브를 strip한 텍스트로 `update`(본문 전체교체, **properties 보존**) -> 로컬 PNG는 `files create`로 재업로드해 image 블록, `[[bookmark: URL]]`은 bookmark 블록을 직전 '실텍스트' 블록(역방향 탐색, 콜아웃/표/펜스/구분선/태그 건너뜀) 뒤 `after_block` 삽입 -> round-trip로 image/bookmark 블록 수==로컬 확인(exit 0). 로컬+PNG가 입력 기준이라 노션 상태 의존이 없어 robust(케이스 1 전체교체 경로 한정). **반영 전 검수 게이트 내장** - `--candidates`와 `--report`로 받은 후보 검토 산출물/검수 리포트/교안을 `gate-review`로 재검사해 source evidence 없는 반영, 리포트 없는 반영, 고신호 교안 반영을 거부한다. 의도적 우회만 `--skip-gate`. **출처 표기는 인라인 `[출처:]` 금지(authoring 3-3)** - 반영 전 인라인 출처를 섹션 하단 `[[bookmark: URL]]`로 변환한다(고유 URL을 섹션마다, 코드펜스 안/`---` 구분선 뒤가 아니라 섹션 마지막 실텍스트 뒤). **함정**:
   - 같은 앵커를 공유하는 연속 이미지/북마크는 직전 삽입 블록 뒤로 체이닝(순서 보존)
   - flatten은 `callout`까지 재귀해야 콜아웃 뒤 자산 앵커가 잡힌다
   - ntn 호출 `stdin=DEVNULL`(EOF 대기 hang 방지)
   - child_page/database 있는 페이지엔 금지(update가 본문을 지움)
   - 동시 ntn 다중 실행 금지(키체인 락)
   - `---` 구분선은 텍스트가 없어 앵커 불가 - 북마크는 구분선 앞(섹션 실텍스트 뒤)에 둔다 (실증 2026-06-22 Part4 27클립 반영, 앵커 체이닝+구분선 스킵 후 실패 0.)

**STEP 토글 변환**: `# STEP N.` 헤딩 끝에 ` {toggle="true"}`, 다음 top-level `---`/다음 `# ` 전까지 본문 라인마다 탭 1개. 코드펜스 내부 `---`는 divider 오인 금지(fence 상태 추적).

**함정**:
- `--limit` 컷 - 전수 1000+/페이지네이션, 생성 전 `Counter`로 중복 확인.
- 삭제 판정은 `in_trash:true`(not `archived`). `ntn pages trash`는 `--yes`(공유 워크스페이스 삭제는 명시 승인 후).
- **ntn 백그라운드 금지** - hang 시 키체인 락 연쇄. zsh 반복은 `for id in ${(f)IDS}`.
- **`ntn pages update`가 본문뿐 아니라 제목 property를 바꿀 수 있다**(실측 2026-06-19) - 반영 후 직접 API로 제목 확인/복구.
- 원본 노트는 `<details><summary>📝 원본 작업 노트</summary>…</details>`로 보존.

**프로젝트 AGENTS.md = 결정 원장**: 날짜별 변경/근거/page id 매핑/재현 스크립트 경로/"되돌리지 말 것" 라벨을 누적해 세션 간 컨텍스트 소실과 의도치 않은 롤백을 막는다.

## 4-S. 직접 블록 API surgical 함정 (전체교체, 재업로드 아닌 블록 단위 편집)

성숙 페이지를 변경 블록만 직접 REST로 고칠 때(4-0)의 비자명 함정. 이미지 보존이 필요한 대량 부분 편집은 `ntn pages update`(전체교체)도 `notion_reflect.py`(재업로드)도 아니라, 블록을 직접 `PATCH /v1/blocks/<id>` / `PATCH /v1/blocks/<parent>/children`로 고친다. 자작 변환, 적용 스크립트는 아래를 지킨다(실증 2026-06-26 <company-ws-token> Claude Code 허브 51p surgical 반영).

- **인라인 마크다운은 segment 보존 PATCH** - 블록 rich_text를 통째 평문으로 갈면 굵게/코드/링크 annotation이 날아간다. `**굵게**`, `` `코드` ``, `[텍스트](url)`만 파싱해 rich_text로(나머지 평문). 코드블록은 평문 rich_text로 넣고 마크다운 파싱 금지(코드 안 백틱/별표가 깨짐). PATCH 전 `html.unescape` - 워크플로/JSON 직렬화가 `>`를 `&gt;`로 바꿔 그대로 들어간다.
- **append `after`는 실제 부모를 조회** - `after`로 준 블록이 synced_block, column, toggle 안에 중첩이면 parent를 페이지로 주면 400. `GET /v1/blocks/<after>`의 `parent.block_id`를 실제 부모로 쓴다. after가 `table_row`면 table엔 비-row 자식을 못 넣으니, table 블록 전체 **다음**에 삽입한다(table의 부모 + after=table id).
- **synced_block은 편집이 다른 페이지로 동기화된다** - 참조본(reference)을 편집하면 원본(다른 페이지)도, 원본을 편집하면 모든 참조본도 바뀐다(노션은 참조본 children GET 시 원본 block_id를 반환하므로 그 id PATCH = 전 위치 반영). 편집, 이미지 삽입 전 `GET /v1/blocks/<sb>`의 `synced_block.synced_from`으로 original(null)/reference를 판정하고, 동기화로 영향받는 다른 페이지를 사용자에게 알린다. dump는 synced_block을 재귀해야 내부 블록을 놓치지 않는다.
- **block_id는 적용 전 실존 검증** - 변경 스펙을 LLM(서브에이전트)이 만들면 block_id를 환각, 추정한다(실측 95% 정확, 5%는 가짜). 적용 전 페이지 실제 블록 id 집합과 대조해 없는 id는 버린다. 타입도 대조 - table_row 편집은 실제 table_row만, 스펙의 type이 실제와 다르면 실제 타입으로 PATCH.
- **마크다운 표는 직접 블록 변환이 안 됨** - 자작 `md→blocks`는 `| a | b |` 표 문법을 paragraph로 깨거나 누락한다. append 본문에 표가 필요하면 불릿 리스트로 풀거나 table 블록을 명시 구성한다.
- **retry는 idempotent하게, 두 번 돌리지 말 것** - append 재시도의 "이미 있으면 skip"이 식별 문구 매칭으로 빗나가면 같은 블록이 2~3개 중복 삽입된다. 재시도 후 인접 동일 `(type, text)` 블록을 dedup으로 정리하고, round-trip으로 append 문구 출현 횟수==1을 확인한다.

## 4-3. 검증 (반영 직후 필수 - round-trip)

반영 직후 페이지를 떠와 점검한다. 읽기는 4-0절 신뢰 채널(직접 API 재귀, `GET /v1/blocks/<id>/children`) 우선 - `ntn pages get`은 크로스 오염 가능. (ntn get 예: `NOTION_WORKSPACE_ID=<workspace-id> ntn pages get <page-id> > /tmp/after.md`)
- [ ] frontmatter 본문 누출 없음(맨 위가 첫 콘텐츠 블록)
- [ ] `<callout>`, `<table>`, `toggle=`, `<details>` 여닫 개수 일치
- [ ] 이미지 블록 보존(로컬 .md에 원본 `file://` ref가 있으면 `update`로 복제/보존됨 / get이 준 S3 URL을 박았거나 ref를 빼면 유실), 북마크/unknown 블록 보존
- [ ] 빈 이미지 `![]()` 없음, 테스트용 `<page url=...>` 링크 없음
- [ ] 새 이미지는 관련 섹션 중간에 여러 장 배치, 이미지가 설명보다 먼저 나옴, 캡션식 설명 문단 없음
- [ ] 생성 이미지는 Codex 자체 생성 결과만(SVG/HTML/CSS 렌더링 없음), 로고 레퍼런스/한글 검수 규칙 충족(image-generation-notion-assets.md 4절)
- [ ] **산출물 시각자료**: 이번 회차 핵심 산출물/새 대표 예시/새 도메인의 목업/흐름/결과 화면 이미지를 **새로 생성**(타 도메인 기존 개념 이미지 재사용으로 때우지 않음 - authoring.md 3-0절 3.)
- [ ] **콜아웃 예산**: 콜아웃 용도/개수/밀도 기준 충족(authoring.md 3-3절)
- [ ] 코드펜스 짝수(중첩 0), 빈 펜스의 `javascript` 0, 코드블록 언어가 내용과 일치(JSON=`json`, 코드=`javascript`, 프롬프트=`markdown`), 노드/프로세스 흐름은 `mermaid` 블록(`text` 블록 안 ASCII 화살표 흐름 0)
- [ ] 섹션 번호 정수 연속(복습 `# 0` 허용), 목차 칸 명사구
- [ ] 인라인 `[출처:]` 표기 0 (출처는 섹션 하단 북마크 카드로 - authoring 3-3, review-draft가 강제)
- [ ] 위험/보안 우회 명령 없음 / 용어 풀이/개인 목표 1개/시간 현실성/내부 모순 없음
- [ ] 새 이미지/생성 이미지는 프로젝트 `02-output/assets/...`에 최종본 보관. 로컬 .md엔 원본 `file://` ref를 유지(get이 내보낸 만료 S3 URL은 박지 말 것), file:// ref 없는 새 PNG만 슬롯 위치 기록 후 `ntn api`로 삽입

## 4-4. 2차 리뷰 (선택, 권장)

외부 모델(예 codex)로 read-only 검증 - 1. 도메인 미스매치 2. 시간 과부하 3. 입문자 눈높이 점프/용어 4. 내부 모순 5. 보안. **외부 의견은 추천이지 결정이 아니다** - 사용자 지시와 충돌하면 항목별로 확인.
