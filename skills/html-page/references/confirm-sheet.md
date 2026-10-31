# 확인 시트형

사용자가 영상, 오디오, 이미지, 원문을 직접 보고 항목별로 고르거나 메모한 뒤, 그 결과를 대화로 돌려주는 단일 HTML이다. 설명을 읽히는 페이지가 아니라 **판단을 받아 가는** 페이지라서 다른 타입과 목적이 다르다.

## 목차

- 구성
- 원문에서 확인 시트 생성
- 실물을 항목 안에 넣는다
- 선택과 메모
- 선택 영역 주석
- 결과 미리보기와 회신
- 화면을 대신 움직이지 않는다
- 전달 전 검수
- 열고 응답을 받는다
- 템플릿 수정 계약

## 구성

- Start from `assets/review-template.html` for checks and text annotations. It is one offline Vanilla JS file; preserve its working review interactions while replacing the example content.
- Keep each item focused on one labelled question, visible evidence, and a real answer control. Use a comparison or flow to explain the difference, not a wall of prose.
- 질문 앞에 `A1`, `A2` 같은 ID를 붙인다. 결과에서 이 ID로 항목을 찾는다.
- Keep annotations behind text selection and a collapsed per-item list. Do not add an always-visible annotation toolbar or a separate “add to reply” step.
- In the connected reader, the existing panel owns the right outline, unanswered navigation, floating overall memo, preview, and send. Do not duplicate those controls in the source. Direct file viewing retains a full-question copy fallback, not automatic delivery.

## 원문에서 확인 시트 생성

Markdown 원문을 그대로 검토할 때는 `scripts/build-review.py --help`를 실행한 뒤 생성기를 사용한다. 본문을 다시 쓰거나 스크립트 일부만 추출하지 않는다. 생성기는 완전한 `assets/review-template.html`에서 `#review-document`의 예시 머리말·항목 구간만 교체하고 공용 주석·회신 UI를 보존한다.

```bash
python3 <skill-dir>/scripts/build-review.py --source <source.md> --output <review.html> --title "원문 검토"
```

1. 원문과 출력 경로를 명시한다. 출력 디렉터리는 미리 존재해야 하며, 기존 출력의 교체를 의도한 경우에만 `--force`를 쓴다. 원문·템플릿·연결 미디어나 그 별칭을 출력으로 지정할 수 없다.
2. 필요한 로컬 미디어만 `--media <file> [<file> ...]`로 명시한다. 생성기는 파일 존재와 미디어 확장자를 확인하고 `Path.as_uri()`로 연결한다. Markdown 안의 링크를 따라 읽거나 다운로드하지 않는다. 파일을 내장하거나 재생 가능성을 검증하지 않으므로 전달 전 브라우저에서 확인한다.
3. 울타리 코드 블록 밖의 ATX 레벨 2 제목(`##`)을 항목으로 나눈다. 제목 언어·이름은 제한하지 않는다. 머리말·빈 줄·마지막 텍스트를 보존하며, 레벨 2 제목이 없으면 ‘전체 원문’ 하나로 만든다. 빈 제목·빈 본문은 명시하고, 빈 파일·공백뿐인 파일·잘못된 UTF-8·NUL 문자는 출력 전에 거부한다.
4. 각 항목에서 제목과 원문 행 위치를 확인한다. 복사 대상은 제목 줄을 제외한 본문의 정확한 일반 텍스트이며, 앞뒤 공백·줄바꿈·출처·링크·HTML처럼 보이는 문자열을 해석하거나 줄이지 않는다. 원래 제목 줄도 항목 메타데이터에 보관한다. 복사 실패 시 같은 본문을 직접 선택해 복사하고 주석·체크를 유지한다.
5. 원문 URI와 바이트 SHA-256을 표시한 고정 사본으로 검토한다. 원문 변경은 자동 반영되지 않는다. 원문이 바뀌면 다시 생성하고 연결 회신에도 새 리비전을 등록한다. 항목 ID는 원문 URI·제목·동일 제목의 출현 순서로 안정적으로 생성되지만, 체크·주석 초안은 원문 식별자와 내용 해시별로 격리한다. 이전 저장값을 삭제하거나 새 원문에 적용하지 않는다.
6. 아래 전달 전 검수와 reply-delivery 절차를 따른다. 본문 복사·체크는 승인·게시·회신 전송이 아니며 생성기는 사용자 답을 미리 채우거나 페이지를 열 때 보내지 않는다. 연결 패널이 전체 의견·미리보기·단일 전송을 계속 소유한다.

생성기 회귀 검사는 `tests/test_build_review.py`에 있다. 원문 보존·실패 시 무쓰기·원자적 교체 검사와 실제 브라우저의 복사·선택 주석·미디어 검증을 구분한다.

## 실물을 항목 안에 넣는다

경로만 적어 두면 사용자가 항목마다 파일을 찾아 열어야 하고, 그동안 확인이 멈춘다. 판단에 필요한 것을 그 항목 안에서 바로 재생하고 읽게 한다.

| 실물 | 넣는 법 |
|---|---|
| 영상, 오디오 | `<video controls preload="metadata">`, `<audio controls>`에 원본의 `file://` URL |
| 이미지 | `<img>`. 1MB 이하면 data URI로 넣어도 된다 |
| 원문, 로그, 대본 | 항목 안 `<details><pre>`. 요약이나 주장을 확인받는 항목이면 근거 원문을 함께 둔다 |
| A/B 비교 | `<video>` 두 개를 나란히 둔다 |

- 영상과 오디오는 base64로 넣지 않는다. 수십 MB가 되면 열리는 데 오래 걸리고 파일을 고치기도 어렵다. 원본을 한 폴더에 모아 두고 `file://` URL로 가리킨다.
- URL은 `Path(p).resolve().as_uri()`처럼 도구로 만든다. 파일명에 `#`이나 `?`가 있으면 손으로 이어 붙인 URL은 파일명이 잘려 깨진다.
- 생성 스크립트가 `src`가 가리키는 파일이 실제로 있는지 확인한다. 없는 파일은 빈 플레이어로 뜨고 사용자에게는 원인이 보이지 않는다.

## 선택과 메모

- 라디오는 하나 고르기, 체크박스는 여럿 고르기다. 선택지의 `value`는 사용자에게 보이는 말 그대로 둔다. 그대로 결과 텍스트에 들어가므로 코드표를 따로 두지 않는다.
- 실제 입력 요소를 질문 안에 둔다. 설명 문장이나 스크린샷만으로 체크 가능한 질문을 대신하지 않는다.
- 하나의 판단은 고유한 `data-item`과 `fieldset/legend` 또는 연결된 질문 라벨로 구성한다. 그룹을 묶는 컨테이너에 질문 ID를 중복 부여하지 않는다.
- Use selection annotations for comments tied to text. Add an optional labelled item-memo field only when the task needs a comment without a text target; keep it collapsed until requested. A note without an answer remains ‘메모 있음, 선택 필요’, not complete.
- 글 자체가 답인 질문은 `textarea[data-reply-answer]`로 표시한다. 공백을 제외한 값은 선택 결과와 같은 답으로 전달하며, 일반 textarea는 부가 메모다.
- ‘없음’이나 ‘아직 결정하지 않음’도 답일 수 있으면 명시적인 선택지를 둔다. 체크박스의 배타 선택지는 `data-reply-exclusive`로 표시해 다른 체크와 동시 선택되지 않게 한다.
- 고르지 않은 항목은 결과에 `미선택`으로 남긴다. 빠지면 "안 봤다"와 "상관없다"를 구분할 수 없다.
- 연결된 목차는 질문별 완료/미응답과 전체 진행을 표시한다. ‘미응답만’과 ‘미응답 보기’에서 실제 질문으로 이동하며 접힌 details를 열고 입력에 포커스를 둔다.
- 조건부로 숨긴 질문은 현재 진행/회신에서 제외하되 초안 값은 보존한다. 단순히 접은 details 안의 질문은 미응답에 포함한다.
- 체크 해제나 답 지우기는 즉시 미응답으로 돌린다. 부분 응답 전송을 막거나 빈 선택을 동의로 처리하지 않는다.
- Show muted green with an explicit completed label when an answer exists, and muted red with an unanswered label otherwise. Keep the source badges, right outline, and dock consistent. Completion is not correctness or approval; start unchecked unless restoring the user's actual answer.

## 선택 영역 주석

- Selecting text within one item reveals a comment icon at the selection's upper-right, clamped inside the viewport. Clicking it opens the compact editor; no persistent reading-position toolbar is needed.
- Freeze the item ID, stable anchor, original quotation, and optional `data-comment-context` when writing begins. Scrolling or changing comparison conditions must not retarget a draft. Context is explanatory text, not an inferred live session state.
- Typing automatically updates that item's memo carrier. Closing or pressing Escape preserves nonempty drafts; IME composition must not close the editor. The per-item list supports location, edit, and delete.
- Reject selections crossing item boundaries or controls. Keep the template's quote, message, note-count, and packet limits. An over-limit edit stays recoverable with the persistent message ‘전송에서 제외됨, 내용을 줄여 주세요’; exclude that entire note from the outgoing memo instead of sending its previous text or truncating the draft.
- Preserve notes and checked answers across reload. The connected panel owns form persistence; direct-file mode uses pathname-scoped storage, additionally keyed by source identity and content revision for generated source reviews. Neither storage nor annotation entry sends a response.

## 결과 미리보기와 회신

선택이나 메모가 바뀔 때마다 응답 미리보기에 자동으로 반영한다. 별도 포함 체크를 요구하지 않는다. 항목별 메모와 전체 추가 메모를 구분한다. For a connected return path, follow the compact Markdown/XML protocol in the reply-delivery workflow routed by `SKILL.md`. The user sends the composed response once. A copy alone does not prove delivery.

```text
[<시트 제목> 응답]

A1 말 속도를 골라 주세요: 8.5 (지금) (메모: 8.0도 괜찮음)
A2 적용할 항목을 모두 고르세요: 자막, 효과음
A3 PR을 머지할까요: 미선택
```

- For a file-only copy fallback, include each ID, question, choice, and note so the text stands alone. The connected compact protocol uses registered item IDs; unfamiliar IDs must be resolved through the helper's inspection command.
- Try `navigator.clipboard.writeText` first. If access is blocked, keep the complete response visible in the read-only text field and give manual-selection instructions without clearing the memo editor or the reader's selection. `file://` clipboard permissions vary; do not claim success from a button click alone.
- 저장 창으로 결과를 넘기지 않는다. 파일 선택창(`showSaveFilePicker`, `showOpenFilePicker`), `<a download>`, 다운로드 버튼이 모두 해당한다. 사용자가 창을 끝내지 못하면 결과가 브라우저 안에 갇히고, 에이전트는 사용자 탭의 저장소를 읽을 방법이 없다.
- `localStorage`는 새로고침에 대비한 임시 보관으로만 쓰고 접근을 `try/catch`로 감싼다. 저장했다는 사실을 전달이 끝났다는 뜻으로 말하지 않는다.

## 화면을 대신 움직이지 않는다

- 페이지를 자동으로 스크롤하지 않는다. 재생 위치에 맞춰 현재 줄을 강조하는 데서 멈춘다(`classList.toggle`). `scrollIntoView`나 `scrollTo`로 화면을 옮기면 사용자가 내려 둔 스크롤을 되돌려 항목을 평가할 수 없다.
- 재생 위치를 따라가는 긴 목록이 꼭 필요하면 세 가지를 모두 지킨다.
    - 사용자가 켜는 토글을 두고 기본은 끈다.
    - 목록 컨테이너의 `scrollTop`만 바꾼다. 페이지 전체를 움직이는 `scrollIntoView`는 쓰지 않는다.
    - 사용자가 직접 스크롤하면 일정 시간 따라가기를 멈춘다.
- 줄 위치를 `offsetTop`으로 계산하면 목록 컨테이너에 `position: relative`를 둔다. 없으면 페이지 기준으로 계산돼 목록이 엉뚱한 곳으로 튄다.

## 전달 전 검수

1. 생성한 최종 HTML은 `reply-bridge.py publish`가 문법 검사(`scripts/verify.sh --syntax`)와 디자인 검사(`scripts/check-design.py`)를 먼저 돌린다. Python 생성기의 문법 검사나 `open` 성공으로 대신하지 않는다. 문자열 안의 줄바꿈이나 따옴표는 HTML로 나온 뒤에 깨질 수 있다.
2. Verify actual pointer selection, upper-right icon placement, editor focus/caret, automatic item-note inclusion, unselected IDs, and the overall memo. Check/uncheck an actual item and compare source, outline, and dock colors in both themes. For connected replies, compare the Markdown/XML preview with an isolated delivered packet; for file-only copies, preserve the full question text.
3. 복사 버튼이 화면에 표시된 응답문을 그대로 클립보드 호출에 넘기는지 확인한다. 기본 복사가 막히는 경우의 대체 복사와 수동 선택 안내도 확인한다.
4. Verify reload, note edit/delete/location, rejected-draft recovery, cross-item selection rejection, narrow/short viewports, and frozen pending replies while the next draft changes. Use `tests/review-template-browser.py` when changing the reusable template; never submit a test reply to the user's live conversation.
5. 문법 통과, DOM 동작, 실제 브라우저의 복사와 미디어 재생은 구분해 기록한다. 문법 검사만 한 결과를 페이지 전체 검수로 보고하지 않는다.

`--syntax`는 인라인 JavaScript를 임시 파일에 추출해 Node.js로 검사하며 브라우저나 네트워크를 쓰지 않는다. 외부 스크립트, 지원하지 않는 script 타입이나 검사할 JavaScript가 없으면 미검증으로 종료한다. 실제 브라우저 검수는 기존 브라우저 스킬을 따르고, CDP 실행은 이 스킬의 명시 요청 경계를 유지한다.

## 열고 응답을 받는다

- 페이지는 `reply-bridge.py publish`로 연다. exit 0이면 패널의 단일 전송으로 원래 대화에 돌아오고, exit 3이면 파일만 열린 미연결 상태라 사용자가 회신 복사로 이 대화에 붙여 넣어야 한다. 어느 쪽인지와 재생을 확인하지 못한 미디어를 밝힌다.
- 응답을 받으면 메모가 있는 항목부터 하나씩 답하고, 어디까지 반영했는지(어느 파일, 어느 규칙)를 함께 보고한다. 선택만 처리하고 메모를 놓치면 사용자가 같은 말을 다시 해야 한다.

## 템플릿 수정 계약

Copy the complete `assets/review-template.html`, then replace its title, context summary, questions, and evidence. Do not copy private research IDs, paths, source screenshots, or answers into the starter. The runtime discovers item IDs rather than relying on the three sample IDs. Within `#review-document`, adapt a complete item together:

```html
<section data-item="A1" id="comparison" data-comment-anchor="comparison"
  data-comment-title="전달 방식 비교">
  <h2>A1 전달 방식 비교</h2>
  <fieldset class="review-row" data-review-state="unanswered">
    <legend>전달 방식 확인</legend>
    <label><input id="check-A1" name="A1" type="checkbox"
      value="두 전달 방식의 차이를 확인했습니다">두 전달 방식의 차이를 확인했습니다</label>
    <span class="review-state" data-reply-state>미확인</span>
  </fieldset>
  <p>검토할 실제 비교 설명과 근거를 이 위치에 넣습니다.</p>
  <details class="section-notes" id="notes-A1" hidden>
    <summary id="notes-count-A1">주석 0</summary>
    <div id="notes-list-A1"></div>
  </details>
  <div class="annotation-wire" inert>
    <textarea id="memo-A1" data-reply-notes aria-label="A1에 연결된 주석"></textarea>
  </div>
</section>
```

- Match the item, form, notes-list, and memo IDs when renaming or adding an item. Keep element IDs unique; each `data-comment-anchor` equals its element ID. Use either a whole-item anchor or separate non-nested explanation anchors. Optional context belongs on the selected anchor.
- Keep the note carrier visually clipped and inert, but not `hidden`, `display:none`, `aria-hidden`, `disabled`, or `readonly`: it must remain in the existing item-memo collector. Do not put user-editable fields inside that inert carrier.
- Preserve the template's hidden `ANNOTATION_STATE` section and `#selection-state`, selection editor, and shared script. That reserved state is recovery data, not a question or an outgoing answer.
- 연결은 `reply-bridge.py publish`가 한다. 원본 파일은 단독으로 열리게 유지하고 전송 코드를 복제하거나 인라인하지 않는다.
