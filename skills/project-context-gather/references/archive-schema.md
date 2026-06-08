# 아카이브 frontmatter 스키마 + 템플릿

`./context/`의 소스 아카이브 `.md`는 맨 위에 아래 YAML frontmatter를 둔다. 이게 메타데이터의 **단일 소스**이고, 재실행 머지(upsert)와 `scripts/context_status.py` 뷰어가 이 값을 읽는다. frontmatter는 **flat key: value만** 쓴다(중첩·리스트 금지 — 스크립트가 의존성 없이 파싱하도록).

## 템플릿

새 아카이브는 스킬의 `templates/archive-template.md`를 복사해 시작한다. 아래는 그 형태:

```markdown
---
project: <프로젝트 폴더명>
source: slack
collected_first: 2026-05-29
collected_last: 2026-06-08
range_start: 2026-04-14
range_end: 2026-06-08
anchor: "1730000000.000000"
items: 23
scope: "general, team-updates"
---

# <프로젝트> — <소스> 맥락 아카이브

## 핵심 인물
| 이름 | 핸들/이메일 | 역할 |

## 주요 결정사항
- <날짜> <결정>

---

## (시간순 원문 전체)
```

## 필드

| 필드 | 의미 | 머지 시 |
|---|---|---|
| `project` | 프로젝트(폴더)명 | 불변 |
| `source` | `slack`/`notion`/`gmail`/`drive`/`calendar`/`obsidian`/`voice`/`call`/`note`/`caret`/`kakaotalk` | 불변 |
| `collected_first` | 최초 수집일(YYYY-MM-DD) | **불변** |
| `collected_last` | 마지막 수집일 | 매 머지에 오늘로 갱신 |
| `range_start` | 가장 오래된 항목 날짜 | 불변(더 옛 항목 발견 시만 당김) |
| `range_end` | 가장 최신 항목 날짜 | 새 최신 항목일로 갱신 |
| `anchor` | 증분 기준점(아래) | 새 마지막 항목 키로 갱신, 없으면 빈 문자열 |
| `items` | 담긴 항목 수 | 갱신 |
| `scope` | 채널/계정/워크스페이스 범위 | 확장 시 갱신 |

## anchor (증분 기준점) — 소스별

재실행 시 "이 값 이후만" 가져와 중복 없이 증분한다. 검색 명령에 그대로 넣는다.

| source | anchor 값 | 증분 검색 |
|---|---|---|
| slack | 마지막 메시지 `ts` | `agent-slack message list ... --oldest <anchor>` |
| gmail | 마지막 메일 날짜 | `gog gmail search "... after:<anchor>"` |
| calendar | 마지막 이벤트 날짜 | 그 이후 이벤트만 |
| notion | 마지막 `last_edited_time` | 그 이후 편집분만 |
| obsidian / voice / note | 날짜(YYYY-MM-DD) | 그 이후 노트·녹음만 |

anchor를 못 구하는 소스는 빈 문자열로 두고, 머지 시 기존 본문 항목과 **dedupe(같은 ts·내용 제외)**로 중복을 거른다.

## 머지 규칙 (재실행 upsert)

기존 파일이 있으면 새로 만들거나 통째로 덮어쓰지 않는다.
1. `anchor`(없으면 `collected_last`) **이후 신규 항목만** 검색.
2. 본문 시간순 제자리에 dedupe해 끼워 넣음. 기존 항목·결정·인물 줄 보존, 충돌하는 옛 결정만 최신으로 교체(옛 값 `→ 변경` 표기).
3. frontmatter 갱신: `collected_last`=오늘, `range_end`=새 최신 항목일, `anchor`=새 마지막 키, `items`=갱신. `collected_first`·`range_start`는 불변.

## 현황 보기

```bash
# 전체 소스 현황 표
python3 ~/.claude/skills/project-context-gather/scripts/context_status.py ./context

# 특정 소스의 anchor만 (재수집 증분 검색에 그대로 사용)
python3 ~/.claude/skills/project-context-gather/scripts/context_status.py ./context --source slack
```

기존(frontmatter 없는) 아카이브는 스크립트가 파일명·본문 헤더에서 best-effort로 파싱해 `*`로 표시한다. 다음 머지 때 위 frontmatter를 얹으면 정식 관리로 전환된다.
