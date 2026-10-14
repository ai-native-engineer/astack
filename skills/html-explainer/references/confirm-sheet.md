# 확인 시트형

사용자가 영상, 오디오, 이미지, 원문을 직접 보고 항목별로 고르거나 메모한 뒤, 그 결과를 대화로 돌려주는 단일 HTML이다. 설명을 읽히는 페이지가 아니라 **판단을 받아 가는** 페이지라서 다른 타입과 목적이 다르다.

## 구성

- 항목 하나는 질문 한 줄, 판단용 실물, 선택지, 메모 칸 하나다.
- 질문 앞에 `A1`, `A2` 같은 ID를 붙인다. 결과에서 이 ID로 항목을 찾는다.
- 맨 아래에 결과 텍스트 글상자와 복사 버튼을 둔다.
- Vanilla JS 단일 HTML이고 빌드와 CDN이 없다. 항목 구성이 요청마다 달라 시작 템플릿은 두지 않고 맨 아래 골격에서 시작한다.

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
- 항목마다 메모 칸을 하나 둔다. 선택지에 없는 요청은 여기에 적힌다.
- 고르지 않은 항목은 결과에 `미선택`으로 남긴다. 빠지면 "안 봤다"와 "상관없다"를 구분할 수 없다.

## 결과는 복사 텍스트로 돌려받는다

선택이나 메모가 바뀔 때마다 결과 텍스트를 다시 만들어 읽기 전용 글상자에 계속 보여 준다. 사용자는 복사 버튼을 눌러 대화에 붙여 넣는다.

```text
[<시트 제목> 응답]

A1 말 속도를 골라 주세요: 8.5 (지금) (메모: 8.0도 괜찮음)
A2 적용할 항목을 모두 고르세요: 자막, 효과음
A3 PR을 머지할까요: 미선택
```

- 한 줄에 ID, 질문, 선택, 메모가 모두 있어야 한다. 에이전트는 시트 파일을 다시 열지 않고 이 텍스트만으로 처리한다.
- 복사는 `navigator.clipboard.writeText`를 먼저 쓰고, 막히면 글상자를 `select()`한 뒤 `document.execCommand('copy')`를 쓴다. 둘 다 막히면 글상자를 직접 선택해 복사하라고 안내한다. `file://` 페이지에서는 클립보드 API가 막힐 수 있다.
- 저장 창으로 결과를 넘기지 않는다. 파일 선택창(`showSaveFilePicker`, `showOpenFilePicker`), `<a download>`, 다운로드 버튼이 모두 해당한다. 사용자가 창을 끝내지 못하면 결과가 브라우저 안에 갇히고, 에이전트는 사용자 탭의 저장소를 읽을 방법이 없다.
- `localStorage`는 새로고침에 대비한 임시 보관으로만 쓰고 접근을 `try/catch`로 감싼다. 저장했다는 사실을 전달이 끝났다는 뜻으로 말하지 않는다.

## 화면을 대신 움직이지 않는다

- 페이지를 자동으로 스크롤하지 않는다. 재생 위치에 맞춰 현재 줄을 강조하는 데서 멈춘다(`classList.toggle`). `scrollIntoView`나 `scrollTo`로 화면을 옮기면 사용자가 내려 둔 스크롤을 되돌려 항목을 평가할 수 없다.
- 재생 위치를 따라가는 긴 목록이 꼭 필요하면 세 가지를 모두 지킨다.
    - 사용자가 켜는 토글을 두고 기본은 끈다.
    - 목록 컨테이너의 `scrollTop`만 바꾼다. 페이지 전체를 움직이는 `scrollIntoView`는 쓰지 않는다.
    - 사용자가 직접 스크롤하면 일정 시간 따라가기를 멈춘다.
- 줄 위치를 `offsetTop`으로 계산하면 목록 컨테이너에 `position: relative`를 둔다. 없으면 페이지 기준으로 계산돼 목록이 엉뚱한 곳으로 튄다.

## 열고 응답을 받는다

- 페이지를 열었다고 알릴 때 흐름 한 줄을 함께 적는다. 고른 뒤 "응답 복사"를 눌러 결과를 대화에 붙여 넣으면 된다. 재생을 직접 확인하지 못한 항목이 있으면 그 항목을 밝힌다.
- 응답을 받으면 메모가 있는 항목부터 하나씩 답하고, 어디까지 반영했는지(어느 파일, 어느 규칙)를 함께 보고한다. 선택만 처리하고 메모를 놓치면 사용자가 같은 말을 다시 해야 한다.

## 골격

```html
<section data-item="A1">
  <h3>A1 말 속도를 골라 주세요</h3>
  <video controls preload="metadata" src="file:///.../speed-8.5.mp4"></video>
  <label><input type="radio" name="A1" value="8.5 (지금)"> 8.5 (지금)</label> <label><input type="radio" name="A1" value="9.5"> 9.5</label>
  <textarea placeholder="메모"></textarea>
</section>
<!-- 항목 반복 -->
<textarea id="out" readonly rows="8"></textarea>
<button id="copy">응답 복사</button> <span id="msg"></span>
<script>
const TITLE = '<시트 제목>';
const out = document.getElementById('out');
function build() {
  const lines = [...document.querySelectorAll('[data-item]')].map(sec => {
    const picked = [...sec.querySelectorAll('input:checked')].map(i => i.value).join(', ') || '미선택';
    const memo = sec.querySelector('textarea').value.trim();
    return `${sec.querySelector('h3').textContent}: ${picked}` + (memo ? ` (메모: ${memo})` : '');
  });
  out.value = `[${TITLE} 응답]\n\n${lines.join('\n')}`;
}
document.addEventListener('input', build);
build();
document.getElementById('copy').onclick = async () => {
  out.select();
  let ok = false;
  try { await navigator.clipboard.writeText(out.value); ok = true; }
  catch { ok = document.execCommand('copy'); }
  document.getElementById('msg').textContent = ok
    ? '복사했습니다. 대화에 붙여 넣으면 됩니다.'
    : '복사가 막혔습니다. 글상자를 직접 선택해 복사해 주세요.';
};
</script>
```
