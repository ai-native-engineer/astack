# 헤드리스 Chrome 직접 호출 함정

`chrome-devtools` 데몬을 거치지 않고 `Google Chrome --headless=new`를 직접 불러 정적 HTML을 찍거나 DOM을 덤프할 때 읽는다. CDP 수준 제어나 QA는 데몬 CLI나 gstack `/browse`를 쓴다.

## 종료와 폭

- `--screenshot=...`은 PNG를 쓴 뒤에도 프로세스가 끝나지 않아 Bash가 300초 타임아웃에 걸린다(2026-09-30 실측). `perl -e 'alarm 25; exec @ARGV' "<Chrome>" --headless=new --no-first-run --user-data-dir=<임시 폴더> --window-size=<폭>,<높이> --screenshot=<png> file://...` 뒤에 `pkill -f <임시 폴더>`를 붙인다.
- `--window-size=420,...`은 레이아웃이 약 500px 폭으로 잡히고 캡처만 420px로 잘려 모바일 폭 검사로 쓸 수 없다. 폭은 600px 이상으로 잡는다.
- `#한글-앵커` 조각을 붙이면 빈 화면이 찍힌다. 특정 절은 그 부분만 잘라 `<base href>`를 넣은 임시 HTML로 찍는다.

## 폰 폭 확인

- 창을 줄이지 않는다. `<iframe style="width:390px;height:844px" src="file://...">`(320, 360, 390px)를 여러 개 담은 빈 페이지를 넓은 창(1700px 등)으로 찍으면 iframe 안은 정확히 그 폭으로 배치된다. 언어와 테마 조합을 한 장에 나란히 놓으면 사람에게 보여 줄 비교 화면도 된다.
- 넘침은 같은 페이지에 iframe의 `contentDocument`를 읽는 스크립트를 넣어 `--dump-dom`으로 잰다(가로 스크롤 `scrollWidth - clientWidth`, 잘린 글자 `el.scrollWidth > el.clientWidth`, 두 줄로 넘친 줄 `getBoundingClientRect().height`). `file://` 안의 iframe을 읽으려면 `--allow-file-access-from-files`를 준다.

## 프로필 재사용

같은 `--user-data-dir`를 여러 실행에 쓰면 localStorage가 이어진다. 측정 실행에서 테마 버튼처럼 값을 저장하는 요소를 누르면 다음 스크린샷이 그 값으로 찍힌다(`data-theme="light"`로 고정한 사본도 어둡게 나왔다). 클릭이 들어간 측정과 스크린샷은 실행마다 새 폴더를 쓴다.

## 헤드리스 영상 재생

Claude Code 샌드박스에서 띄운 `--headless=new`는 `<video>`, `<audio>`, HyperFrames 플레이어가 `paused=false`인데 `currentTime`이 0초에서 움직이지 않는다(2026-10-07 실측, readyState 4, 오류 없음). 오디오 출력 장치를 못 잡아 미디어 시계가 서는 것으로 보이며 `--disable-audio-output`(가짜 출력)을 주면 정상으로 흐른다. 재생 QA에서 시각이 안 가면 앱 버그로 단정하기 전에 이 플래그로 다시 확인한다.

## 가상 시간 한계

`--dump-dom --virtual-time-budget=<ms>`에서는 `document.startViewTransition` 콜백이 불리지 않아 Astro ClientRouter 이동이 `astro:after-preparation`에서 멈추고, `video.play()` 약속도 끝나지 않아 결과를 쓰기 전에 DOM이 출력된다(2026-10-14 실측). 가상 시간은 레이아웃 측정(폭 넘침)까지만 쓴다. 이동이나 재생을 재려면 가상 시간을 빼고, 측정 페이지에 로컬 서버가 결과를 받을 때까지 응답을 붙잡는 `<img src="/__wait">`를 넣어 load를 늦춘 뒤 결과를 `fetch` POST로 받는다. 전환 효과를 지워 우회하면 버그가 나는 경로까지 함께 빠지니 우회하지 않는다.
