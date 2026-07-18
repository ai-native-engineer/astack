# Caret MCP 보강

Caret은 Claude Code MCP로 노출된 외부 지식·노트 검색 도구. 이 스킬에서 두 가지 시점에 호출한다.

1. **요약/교정 전 사전 보강** (필수) — 전사본의 키워드·인명·프로젝트명을 사전에 검색해 교정 근거와 요약 배경을 확보
2. **메모 찾아줘 워크플로우** — `search.py`(파일 시스템·SQLite 소스)와 병렬로 Caret도 검색해 결과를 합쳐서 제시

Caret MCP는 Claude Code 런타임 안에서만 호출 가능. Python 스크립트(search.py 등)에서는 직접 호출 불가라서 워크플로우 차원에서 LLM이 묶어서 다룬다.

## 사용 도구

| 도구 | 역할 |
|------|------|
| `caret_search_knowledge` | 지식 베이스(문서·아티클) 검색 |
| `caret_search_notes` | 미팅 노트·작업 노트 검색 |
| `caret_get_note` | 검색된 노트의 **전문** 가져오기 (summary로는 부족할 때 필수) |
| `caret_list_notes`, `caret_list_members`, `caret_get_workspace` | 워크스페이스 메타 조회 |
| 보조 스크립트 `scripts/caret_to_md.py` | `caret_get_note` 결과가 10K 토큰을 초과해 파일로 저장됐을 때 JSON → 마크다운 변환 |

## 1) 요약/교정 전 사전 보강

전사본(Voice Memos transcript)을 요약·교정하기 직전에 반드시 다음을 수행한다. Caret에 관련 지식이 없을 때만 생략 가능.

1. `caret_search_knowledge`로 전사본의 주요 키워드·인명·프로젝트명을 검색. 쿼리는 **병렬로 여러 개** 동시 실행.
2. `caret_search_notes`로 관련 미팅 노트를 검색.
3. 검색 결과의 summary만 보고 판단하지 말고, 관련 노트는 `caret_get_note`로 **전문**을 가져온다.
4. 전문이 10K 토큰을 초과해 파일로 저장된 경우:
   ```bash
   python3 scripts/caret_to_md.py <saved_json_path> -o /tmp/caret_note.md
   wc -l /tmp/caret_note.md
   ```
   변환 후 Read 도구로 60줄씩 병렬 읽기 (Voice Memos 전문 읽기와 동일 패턴).
5. 가져온 Caret 지식과 transcript 전문을 함께 보고 교정 근거·요약 배경 정보로 활용한다.

**이 단계를 건너뛰지 않는다.** Caret 검색이 transcript 안의 줄임말·약어·내부 프로젝트명을 풀어주는 핵심 단서다.

## 2) 메모 찾아줘 워크플로우 통합

사용자가 "메모 찾아줘"·"최근 메모"·"X 관련 메모"라고 요청하면 LLM이 두 채널을 함께 호출하고 결과를 합쳐서 제시한다.

```
사용자: "프롬프트 관련 메모 찾아줘"

LLM:
1. python3 scripts/search.py --keyword "프롬프트"
   → Voice Memos transcript + 통화 녹음 + Apple Notes 라벨별 결과
2. caret_search_knowledge(query="프롬프트")
3. caret_search_notes(query="프롬프트")
   → 둘 다 병렬 호출
4. 결과 합쳐서 라벨별로 제시:
   [음성 메모] - Apple Voice Memos
   [에이닷]    - 에이닷 통화 녹음
   [메모]      - Apple Notes (잠긴 메모는 미리보기에 안내)
   [Caret]     - Caret 지식 / 노트
```

라벨 표기를 통일해서 사용자가 어느 소스에서 온 결과인지 한눈에 알 수 있게 한다.

## 호출 가이드

- **쿼리 병렬화**: 키워드 후보가 여러 개면 `caret_search_*` 호출을 같은 메시지에 묶어서 보낸다. 직렬화하면 응답이 느려진다.
- **summary로 판단 금지**: 검색 결과의 `summary` 필드만으로 노트 내용을 단정하지 말고, 관련성이 보이면 `caret_get_note`로 전문을 확인한다.
- **노트 ID 흐름**: `caret_list_notes`/`caret_search_notes`/`caret_get_note` 모두 노트 객체의 `id` 필드를 키로 사용한다.

## 통합 vs 대체

Caret이 모든 소스를 대체하지는 않는다. 역할 구분:

- **Caret**: 외부 지식·미팅 노트·정제된 컨텍스트
- **search.py 소스들**: 원시 음성·통화·개인 메모 (raw transcript/메모)

요약·교정의 정확도를 높이려면 둘 다 본다. 단순 키워드 검색에서 한쪽만 충분하면 한쪽만 본다.
