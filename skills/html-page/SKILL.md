---
name: html-page
description: "Use for: 로컬 HTML 페이지 한 장으로 설명, 비교, 인터랙티브 walkthrough, 용어집, 확인 시트, 회의록, 정리본, 프로토타입을 만들고 Herdr 패널로 바로 회신받는다. 편집형 도식 파일은 diagram, 제품 UI는 dev-frontend."
argument-hint: "[visual|interactive|wiki|sheet] [topic]"
---

# HTML Page

로컬 HTML 하나로 설명하거나 판단을 받고, 그 페이지를 원래 대화의 Herdr 패널에서 바로 회신할 수 있게 연결한다. 만들기, 보내기, 고정의 세 단계다. 답은 사용자 언어로 쓴다.

## 1. 만들기

- 시작점은 둘이다. 설명, 도표, 차트는 `assets/template.html`, 보고 고르거나 메모를 받는 확인 시트는 `assets/review-template.html`을 복사한다. 두 파일 다 `assets/design.css`의 토큰 블록을 인라인하고 있다.
- 색은 토큰 이름으로만 쓴다(`--paper`, `--ink`, `--muted`, `--line`, `--action`, `--complete`, `--pending`, 범주색 `--teal`, `--amber`). 새 색을 정하지 않는다. 한 벌이어야 패널, 완료 표시, 다크 모드가 같은 규칙으로 보인다.
- 저장 위치는 수명으로 정한다. 이 턴의 답이나 선택을 받으면 끝나는 페이지(선택지, 설명 한 번, 확인 시트)는 `$TMPDIR/html-pages/<name>.html`에 둔다. 나중에 다시 열어 볼 내용(회의록, 정리본, 조사 보고, 서비스 프로토타입)은 `~/.agents/artifacts/YYMMDD-<harness>-<native-session-id>-<name>.html`에 둔다. 애매하면 임시에 두고 사용자가 남기자고 하면 아티팩트로 옮긴다.
- 임시 폴더는 `mkdir -m 700`으로 만든다. 공용 `/tmp`에는 두지 않는다(`$TMPDIR`이 없으면 `~/.cache/html-pages`). 회신 서비스는 등록 시점의 페이지 스냅샷을 따로 보관하므로 보낸 응답과 그 페이지는 남는다. 세션 ID는 실제 값을 쓴다(Herdr 패널이면 `herdr agent list`). 저장소 소유 산출물은 그 저장소 위치를 따른다.
- 구조와 작성 규칙은 작업에 맞는 reference를 읽는다.

| 작업 | 읽을 것 |
|---|---|
| 관계, 구조, 차트 | [stack-guide](references/stack-guide.md) |
| 실제 과정, 인터랙티브 설명 | [interactive-walkthrough](references/interactive-walkthrough.md) |
| 검색, 용어집, 참조 조회 | [wiki-knowledge-base](references/wiki-knowledge-base.md) |
| 보고 고르기, 메모, 확인 시트 | [confirm-sheet](references/confirm-sheet.md) (템플릿 수정 계약 포함) |
| Markdown 원문을 그대로 검토 | `scripts/build-review.py --help` 실행 뒤 생성 |
| 새 컨트롤이나 화면 | [ui-polish](references/ui-polish.md) |
| 이전 산출물 재사용 | [reference-selection](references/reference-selection.md) |

## 2. 보내기

```bash
python3 <skill-dir>/scripts/reply-bridge.py --state-dir ~/.agents/artifacts/.html-page-replies publish <file.html> --conversation-label "<작업 이름>"
```

- 이 명령 하나가 문법 검사, 디자인 검사, 현재 Herdr 패널의 대화 식별, 회신 서비스 기동, 등록, 브라우저 열기를 한다. 파일을 `open`으로 직접 열지 않는다. 열어만 두면 사용자가 복사해 붙여 넣어야 한다.
- exit 0: 출력 JSON의 `url`과 `log`를 사용자에게 알린다. 서비스는 턴이 끝나도 남으며 멈추는 명령은 같은 스크립트의 `stop`이다.
- exit 1: 검사 실패. 출력의 `errors`를 고친 뒤 다시 실행한다.
- exit 3: Herdr 패널 밖이거나 대화를 식별하지 못했다. 파일은 열린 상태다. "미연결"이라고 명시하고 `reason`을 보고한다. 대화를 알면 `--session`, `--agent`, `--conversation`을 셋 다 지정한다.
- 회신이 오면 메모 있는 항목부터 처리하고 어디까지 반영했는지 보고한다. 미선택은 동의가 아니다. 회신 상태, Codex `receive`, fallback은 [reply-delivery](references/reply-delivery.md)를 읽는다.

## 3. 고정

- `scripts/check-design.py`가 darkreader-lock, color-scheme, 다크 모드 블록, 토큰 정의, CDN 버전 고정, Mermaid `flowchart`를 검사한다. publish가 먼저 실행하므로 통과하지 못한 페이지는 보내지지 않는다.
- `scripts/publish-gate.sh`는 Claude Code Stop 훅이다. 이 세션이 `$TMPDIR/html-pages/`나 `~/.agents/artifacts/`에 만든 HTML이 현재 내용으로 등록되지 않았으면 턴을 막고 publish를 요구한다. 등록은 `settings.json`의 Stop 훅에 한다.
- 보고에서는 검사 통과, 브라우저에서 실제 동작 확인(aside-browser로 입력과 상태 변화), 사용자의 전송을 구분한다. 검사만 한 결과를 전체 검수로 쓰지 않는다.

## 불변

- 파일 하나로 열리게 유지한다. 외부 스크립트는 버전을 고정한 CDN만 쓰고 미디어는 base64 대신 `file://` 경로로 가리킨다.
- 페이지를 자동으로 스크롤하지 않는다. 키보드 입력, 텍스트 선택, 스크롤 위치, 감소된 모션 설정을 보존한다.
- 공개 게시는 요청받았을 때만 사용자가 고른 호스팅으로 한다. 로컬 원본은 그대로 둔다.
