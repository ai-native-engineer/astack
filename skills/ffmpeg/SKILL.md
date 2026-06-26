---
name: ffmpeg
description: "Local ffmpeg/ffprobe media operations for cutting, joining, compressing, converting, extracting tracks, resizing, changing FPS, rotating, GIFs, subtitles, thumbnails, audio normalization, HDR-to-SDR, and HEIC conversion. Use when user asks 영상 잘라/합쳐/압축/변환, MP4/MOV/webm, 오디오 추출, mp3, GIF, 자막 입혀, 프레임/썸네일, ffmpeg, ffprobe, HDR 제거, or HEIC 변환. Do NOT use for speech-to-text, text-to-speech, CapCut draft editing, YouTube strategy, or image generation."
---

# ffmpeg

영상·오디오·이미지 변환의 단일 스킬. `ffmpeg`/`ffprobe`(+ macOS 내장 `sips`)로 자르기·합치기·압축·추출·포맷변환·HDR 색공간 변환을 다룬다.

## 멘탈 모델: copy 먼저, 재인코딩은 최후

ffmpeg 작업은 두 모드뿐이다. 어느 쪽인지부터 정한다.

- **stream copy (`-c copy`)** — 비트스트림을 그대로 복사. **무손실·초고속**(8시간 영상도 1~2초). 자르기, 컨테이너 변경(mkv↔mp4), 트랙 추출처럼 **픽셀을 바꾸지 않는** 작업.
- **재인코딩 (`-c:v libx264 -crf …` 등)** — 픽셀을 디코드→인코드. **화질 손실 + 느림.** 압축, 해상도/프레임레이트/코덱/색공간 변경처럼 **픽셀을 바꿔야 할 때만.**

판단: **픽셀을 바꿀 필요가 없으면 무조건 copy.** 자를 때 끝점만 지정(`-to`)하면 시작이 0이라 copy로도 깔끔하다. 중간 구간 정밀 컷·합치기엔 함정이 있다 → `recipes.md`.

## 불변 안전선

1. **원본 보존** — 출력은 항상 새 파일명. 입력을 덮어쓰지 않는다(in-place 요청이면 임시파일 생성 후 교체).
2. **작업 후 `ffprobe` 검증·보고** — 출력의 duration·codec·해상도를 확인한다. copy면 코덱이 입력과 **동일**해야 무손실이 보증된다.
   ```bash
   ffprobe -v error -show_entries format=duration:stream=codec_name,width,height -of default=noprint_wrappers=1 OUT
   ```
3. **"무손실"은 copy일 때만 주장한다.** 재인코딩이면 "재인코딩됨(crf N)"이라고 명시한다. 비트레이트 수치 차이는 구간별 평균 차이일 뿐 손실이 아니다 — copy면 코덱 동일 = 무손실.

## 라우팅 — 작업별 reference

| 작업 | 읽을 것 |
|---|---|
| 자르기·합치기·압축·추출·포맷변환·해상도/fps·회전·GIF·자막·썸네일/프레임·배속·볼륨/정규화 | `references/recipes.md` |
| Apple HDR(HLG/BT.2020)→SDR, 사이니지/안드로이드 호환, HEIC→JPG/PNG | `references/apple-hdr.md` |

기본 명령은 해당 reference의 레시피를 베끼고, 전체 옵션은 `ffmpeg -h full` / https://ffmpeg.org/ffmpeg.html 에 위임한다.
