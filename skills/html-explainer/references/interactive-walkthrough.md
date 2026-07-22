# 인터랙티브형 워크스루

단계를 클릭하며 학습자가 스스로 결론에 도달하는 단계형 설명. 시각형(`stack-guide.md`)과 달리 **읽는 게 아니라 조작한다** — 한 스텝에서 직접 눌러/밀어/골라야 다음이 보인다.

## 멘탈 모델

- **한 스텝 = 한 개념.** 한 화면에 한 가지만. 다음으로 넘어가야 다음 개념.
- **능동 이해.** 각 스텝은 학습자가 *무엇을 해볼지*(버튼/슬라이더/선택)를 준다. 수동으로 읽기만 하는 스텝이 이어지면 슬라이드 PDF와 다를 게 없다.
- **누적 결론.** 앞 스텝의 조작·선택이 뒤 스텝(결과/요약)에 반영되면 "내가 답을 만들었다"는 감각이 생긴다.
- **마지막은 한 줄.** 끝 스텝은 기억할 핵심 한 문장(`.key`).

## 스택과 골격

- React 18 + ReactDOM + Babel standalone, 전부 CDN, **빌드 없는 단일 HTML**.
- 새 파일은 `assets/interactive-template.html`을 복사해 시작한다 — 진행바·dots·키보드 네비·다크/라이트·스텝 애니메이션이 이미 배선돼 있다. 이 엔진(`App`)을 재작성하지 않는다.
- 채우는 곳은 두 군데뿐: `STEP_NAMES` 배열(스텝 이름 = 진행바·dots·카운터의 단일 소스)과 `Steps()`의 `case` 본문.

## 스텝 작성

- 스텝 본문 리듬: `eyebrow`(꼭지 라벨) -> `h1.disp`(제목) -> `body-txt`(한 줄 정의) -> 위젯 1개(있으면).
- **위젯은 정보를 드러내는 조작만.** 버튼으로 결과 공개, 슬라이더로 값 변화, 선택지로 분기. 장식용 위젯 금지(빼도 이해가 안 줄면 뺀다).
- 위젯은 작은 컴포넌트로 분리하고 `useState`로 자체 상태를 갖는다(템플릿 `DemoWidget` 패턴). 입력값을 다음 스텝에 쓰려면 상태를 `App`에서 들고 `Steps`에 내려준다(원본 db-튜토리얼의 `decision` props 패턴).
- 스텝 수는 한 개념씩 쪼개되 과하게 늘리지 않는다. 한 자리 숫자(키보드 1~9 점프) 안쪽이 편하다.

## 인터랙티브 특화 함정

- **in-browser Babel 경고는 정상이다.** `verify.sh` 콘솔에 "precompile your scripts for production"이 `[warn]`으로 뜨는 건 에러가 아니다 — 무시한다.
- **`verify.sh`의 render-check JSON은 `mermaid/echarts/iconify`가 전부 false/0으로 나온다** — 이 타입은 그 스택을 안 쓰니 정상이다. 통과 판정은 **콘솔 에러 0 + 스크린샷 육안**으로 한다(겹침·잘림·첫 스텝 렌더).
- **키보드 핸들러는 `INPUT`/`TEXTAREA`를 건너뛴다.** 안 그러면 입력 중 스페이스/화살표가 스텝을 넘긴다(템플릿에 `입력 보호` 배선됨). Enter 전송은 [dev-frontend의 IME-safe 검증 계약](../../dev-frontend/SKILL.md#ime-safe-enter-submit)을 따른다.
- **스텝 전환 애니메이션은 `key={step}`으로 본문을 remount**해서 낸다(템플릿 배선). 이게 빠지면 fadeUp이 안 돈다.
- 팔레트(`:root` CSS 변수)는 토픽에 맞게 바꾼다. 기본은 따뜻한 에디토리얼 톤이라 대시보드·핀테크엔 어울리지 않는다 — 그럴 땐 변수만 교체한다.

## 공통 철칙

다크/라이트(matchMedia), 긴 한국어 라벨 `<br/>`, CDN 메이저 버전 고정, "애니메이션은 정보 운반만"은 두 타입 공통이라 `SKILL.md` 철칙을 따른다(여기서 반복하지 않는다).

## 완성 예시

- [claude-code-context-timeline.html](../examples/claude-code-context-timeline.html) — Claude Code 세션 시작부터 파일 읽기·서브에이전트·압축까지, 컨텍스트의 생애주기를 시간순으로 보여주는 게이트형 타임라인.
- [chat-context-composition-lab.html](../examples/chat-context-composition-lab.html) — 사용자가 채팅을 이어가며 시스템·사용자·AI 메시지가 다음 요청의 컨텍스트로 누적되는 구성을 직접 확인하는 실험실.
- [claude-directory-explorer.html](../examples/claude-directory-explorer.html) — `.claude` 디렉터리의 파일 트리를 탐색하며 파일별 설명·팁을 보는 2패널 탐색기. 스텝형이 아닌 탐색기형 패턴(트리 + 상세 패널 + URL 해시 딥링크)과 런타임 인라인 오프라인 단일 파일의 예시. 공식 문서 컴포넌트를 포팅한 것이라 CDN 대신 React UMD를 인라인했다.

모두 완성 예시다. 새 파일은 복사하지 말고 `assets/interactive-template.html`에서 시작한다.
