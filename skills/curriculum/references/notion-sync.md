# 강의 자료 수정, Notion 반영 (Phase 6 - 선택적)

프로젝트가 발행 채널로 Notion을 선언했을 때만 적용한다. 공통 CLI, 인증, 승인, 삭제 규칙은 `notion` 스킬의 `references/ntn-cli.md`가 정본이다. 해당 스킬이나 `ntn`이 없으면 Phase 6을 실행하지 않는다. workspace id, token tag, page/database/data-source id는 프로젝트 `AGENTS.md`에 둔다.

## 목차

- 4-R. 베이스 선택 라우터
- 4-0. 쓰기 전 안전 전제
- 4-1. 발산 게이트
- 4-2. 신규/의도적 전체교체
- 4-S. 성숙 페이지 surgical 반영
- 4-3. round-trip 검증
- 4-4. 선택적 2차 리뷰

## 원칙

- 프로젝트가 published pages의 정본을 Notion으로 선언한 경우에만 발행된 페이지를 SoT로 본다.
- Notion을 쓰지 않거나 로컬 정본을 선언한 프로젝트는 Phase 6을 생략한다.
- 기존 페이지의 사용자 편집을 보존한다. 로컬과 Notion이 갈리면 자동 우선순위를 적용하지 말고 사용자에게 기준을 묻는다.
- 기본 반영 방식은 surgical이다. 전체교체는 신규 페이지나 사용자가 승인한 전체 재작성에만 쓴다.

## 4-R. 베이스 선택 라우터

직접 REST로 페이지 정체성, `last_edited_by`, `last_edited_time`을 확인한 뒤 베이스와 방식을 정한다.

| 상황 | 베이스 | 방식 |
|---|---|---|
| 페이지 없음 | 검수 완료 로컬 작성본 | 신규 전체 반영 1회 |
| 페이지 있음, 로컬과 동일 | 현재 Notion 본문 | 승인된 변경만 surgical |
| 페이지 있음, 사용자 직접 편집 신호 | 현재 Notion 본문 | 발산 게이트 뒤 surgical |
| 편집자/최신본이 모호함 | 미정 | 멈추고 사용자에게 질문 |

## 4-0. 쓰기 전 안전 전제

1. 공통 notion 쓰기 안전선으로 workspace, page id, 제목, 부모, 총 개수, 실행 명령을 확인하고 승인을 받는다.
2. 직접 REST로 제목과 첫 섹션이 의도한 회차인지 확인한다.
3. 원문 Markdown 백업을 만든다. unknown/synced block이나 surgical 반영이면 raw block JSON도 함께 보관한다. `notion_reflect.py`는 전체교체 직전 임시 Markdown 백업 경로를 출력한다.
4. `gate-candidates`, `review-draft`, `gate-review`, 필요한 `verify-media`를 통과한다.
5. 이미지/GIF, 북마크, child_page, unknown/synced block 보존 방식을 정한다.
6. 본문 옆 `.fidelity.json`에 이식 원본을 선언한다. 호스트 훅이 없으면 같은 검사를 수동으로 수행한다.
7. 성숙 페이지는 변경 diff를 먼저 보여주고 별도 승인을 받는다.

사이드카 형식:

```json
{"sources": ["../01-context/검증된-원본.md"]}
```

대응 이식 원본이 없는 네이티브/골드 교안만 `{"native": true}`를 명시한다. `native`와 `sources`를 함께 쓰지 않으며, 검사 임계값은 사이드카에서 낮출 수 없다.

## 4-1. 발산 게이트

1. 직접 REST로 얻은 Notion 기준본과 직전 동기화본/로컬을 정규화해 비교한다.
2. Notion에만 있는 추가/삭제와 사용자 편집 신호를 분리한다.
3. 기준이 갈리면 멈추고 `Notion vs 로컬 중 어느 것이 최신인가`를 묻는다.
4. Notion이 기준이면 그 본문에 이번 승인 변경만 재적용하고 로컬 작업본도 같은 결과로 정렬한다.
5. 변경 문자열은 적용 전 정확히 한 곳에만 존재하는지 검증한다.

## 4-2. 신규/의도적 전체교체

전체교체 전 자산을 다음처럼 처리한다.

| 자산 | 처리 |
|---|---|
| 기존 Notion 이미지/GIF | 원본 `file://` attachment ref를 보존한다. 만료 S3 URL을 재사용하지 않는다. |
| 새 로컬 이미지 | 본문 update 전에 업로드 ID를 얻을 수 있는 도구 계약이 있는지 확인한다. 없으면 전체교체를 중단하고 수동/surgical 삽입으로 전환한다. |
| 북마크 | 실제 `bookmark.url`을 blocks API로 확인한다. 자기참조 `app.notion.com/p/...#...` 앵커는 반영하지 않는다. |
| child_page/database | 전체교체 대상에서 제외한다. 새 child_page는 공통 notion 페이지 생성 절차를 쓴다. |
| unknown/synced block | 보존 가능 여부와 다른 페이지 영향 범위를 먼저 확인한다. |

표준 순서:

```text
직접 REST 정체성 확인 -> 백업 -> 발산/검수/미디어 게이트 -> 자산 preflight -> 사용자 승인 -> 한 페이지 반영 -> round-trip
```

`notion_reflect.py`는 한 번에 page/md pair 하나만 받고 직전 REST에서 확인한 title, parent, `last_edited_time`과 현재 후보/검수 리포트를 모두 검증한다. 아래 변수는 승인 직전 조회값으로 채운다.

```text
NOTION_WORKSPACE_ID="$WORKSPACE_ID" \
  python3 "${CLAUDE_PLUGIN_ROOT}/skills/curriculum/scripts/notion_reflect.py" \
  --expected-title "$PAGE_TITLE" \
  --expected-parent-id "$PARENT_ID" \
  --expected-last-edited-time "$LAST_EDITED_TIME" \
  --candidates "$CANDIDATES_MD" --report "$REVIEW_MD" \
  "$PAGE_ID" "$LOCAL_MD"
```

로컬 이미지가 있으면 **업로드 ID 계약을 본문 update 전에 검증**한다. 현재 `ntn` 출력에서 upload id를 얻지 못하면 fail-closed로 반영을 거부한다. 이 경우 업로드 ID를 보장하는 도구를 쓰거나, 이미지를 수동 업로드한 뒤 block API로 surgical 삽입한다. 스크립트가 이미지를 자동 업로드한다고 가정하지 않는다.

여러 페이지를 한 명령으로 반영하지 않는다. 한 페이지마다 승인, 반영, round-trip을 닫는다. 기대 title/parent/last-edited와 candidates/report에는 해당 페이지와 교안에 대응하는 값만 준다.

## 4-S. 성숙 페이지 surgical 반영

- 텍스트는 가능하면 공통 notion reference의 Markdown `update_content`처럼 기존 문자열이 한 곳에만 있을 때 성공하는 API를 우선한다.
- rich_text를 직접 PATCH할 때는 굵게, 코드, 링크 annotation을 보존한다.
- append 위치는 대상 블록의 실제 부모를 조회해 정한다. table_row 뒤 삽입은 table 블록 다음 위치를 쓴다.
- synced_block은 다른 페이지에도 반영되므로 원본/참조본과 영향 페이지를 확인해 사용자에게 알린다.
- 변경 스펙의 block id와 block type은 적용 직전 실제 페이지 블록 집합과 대조한다.
- retry 전에 이미 적용됐는지 확인하고, 반영 후 동일 블록 출현 횟수가 1인지 확인한다.
- 직접 API 경로에서도 draft와 fidelity sidecar로 검수/충실도 게이트를 수동 재현한다.

## 4-3. round-trip 검증

반영 직후 직접 API를 우선해 다시 읽고 확인한다.

- [ ] 제목, 부모, 첫 섹션이 반영 전과 일치
- [ ] 승인된 변경만 적용되고 사용자 편집 보존
- [ ] callout/table/toggle/details 여닫 개수 일치
- [ ] 이미지/GIF, 북마크, child_page, unknown/synced block 보존
- [ ] 북마크 URL별 출현 횟수 1
- [ ] 빈 이미지와 staging/test 링크 0
- [ ] frontmatter 본문 누출 0
- [ ] 코드펜스와 섹션 번호 규칙 통과
- [ ] 인라인 `[출처:]` 0
- [ ] 위험/보안 우회 명령, 시간 과부하, 내부 모순 0
- [ ] 목표가 최소완료/선택확장으로 구분됨
- [ ] 새 생성 이미지는 net-new 산출물 결과 화면/목업에만 사용됨

프로젝트 `AGENTS.md`에는 page-id, 승인된 변경, round-trip 결과, 복구 경로만 기록한다.

## 4-4. 선택적 2차 리뷰

필요하면 외부 검수기로 도메인 미스매치, 시간 과부하, 입문자 눈높이, 내부 모순, 보안을 read-only 검토한다. 외부 의견은 추천이며 사용자 지시와 충돌하면 항목별로 확인한다.
