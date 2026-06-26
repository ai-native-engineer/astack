# 최초 1회 셋업 (쇼당 한 번)

전제: `gh`(로그인됨), `ffprobe`(ffmpeg), `python3`. 오디오는 GitHub Releases(무료·CDN·스트리밍 byte-range 지원), RSS는 GitHub Pages(무료)로 서빙.

## 1) 쇼 repo 생성
```bash
gh repo create OWNER/REPO --public --clone   # 공개여야 Pages 무료
```
공개 repo의 Releases 자산 URL이 곧 오디오 호스팅 주소가 된다.

## 2) 쇼 구성 파일
repo 루트에 다음을 둔다(`templates/show.json` 복사·수정):
- `show.json` — 제목·작성자·**email**(Spotify 인증코드 수신 주소)·`link`/`image`(아래 Pages URL)·category.
- `episodes.json` — `[]` (빈 배열로 시작).
- `cover.jpg` — **정사각 1400~3000px**, JPG/PNG. (Spotify/Apple 필수)
- `.nojekyll` — 빈 파일. GitHub Pages가 Jekyll 처리 없이 파일을 그대로 서빙하게 한다.

`link`/`image`는 `https://OWNER.github.io/REPO/` 형식. commit/push.

## 3) GitHub Pages 활성화
```bash
gh api -X POST repos/OWNER/REPO/pages -f 'source[branch]=main' -f 'source[path]=/'
```
- 피드 URL: `https://OWNER.github.io/REPO/feed.xml`
- 커버 URL: `https://OWNER.github.io/REPO/cover.jpg` (show.json `image`와 일치시킬 것)

## 4) 1화 발행
```bash
scripts/publish.sh --repo <repo경로> --audio ep1.mp3 \
  --title "1화 제목" --desc "에피소드 설명/쇼노트"
```
오디오를 릴리스에 올리고, `episodes.json`·`feed.xml`을 갱신해 push한다.

## 5) Spotify 등록 (1회, 사람이)
Spotify for Podcasters(=Spotify for Creators) 로그인 -> **기존 팟캐스트 추가** -> 호스팅 위치 **"다른 곳(Somewhere else)"** -> **피드 URL 붙여넣기** -> `show.json`의 email로 온 **인증코드** 입력 -> 제출. 몇 분~수 시간 내 게시.
- Apple Podcasts Connect도 동일하게 같은 RSS URL 제출.

## 함정·주의
- **Spotify 직접 업로드 쇼와 외부 RSS는 한 쇼에서 양립 불가.** 자동화(외부 RSS)로 갈 거면 Spotify에 직접 mp3 올리는 쇼는 쓰지 않는다(새 쇼를 RSS로 등록).
- `gen_feed.py`는 `episodes.json` **전체로 feed를 재생성**(증분 아님) — 과거 회차도 episodes.json에 계속 남겨둔다.
- 오디오 URL은 릴리스 자산(`/releases/download/epN/epN.mp3`). 태그를 지우면 링크가 깨지니 회차 태그는 보존한다.
- 커버를 바꾸면 캐시 때문에 반영이 늦을 수 있다(파일명을 바꾸거나 시간 두기).
