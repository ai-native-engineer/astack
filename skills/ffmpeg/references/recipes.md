# ffmpeg 레시피 + 함정

각 작업의 핵심 명령 1~2개와 자주 틀리는 함정. 전체 옵션은 `ffmpeg -h full`.
출력은 항상 새 파일, 작업 후 `ffprobe`로 검증(SKILL.md 안전선).

## 자르기

```bash
# 끝점만 (시작 0) — copy로 무손실·초고속. 끝은 가장 가까운 키프레임에 맞춰짐
ffmpeg -y -i in.mp4 -to 02:53:00 -c copy -movflags +faststart out.mp4

# 중간 구간 — copy, 빠르지만 시작이 키프레임으로 당겨질 수 있음
ffmpeg -y -ss 00:10:00 -to 00:20:00 -i in.mp4 -c copy out.mp4

# 프레임 정확 컷 — 재인코딩(픽셀 단위 정확, 손실·느림)
ffmpeg -y -ss 00:10:00 -to 00:20:00 -i in.mp4 -c:v libx264 -crf 18 -c:a aac out.mp4
```

**함정**
- **정확도는 copy냐 재인코딩이냐가 결정한다 — seeking 위치가 아니다.** `copy`는 픽셀을 디코드하지 않아 **항상 키프레임 단위**로만 잘리고(시작점이 앞 키프레임으로 당겨짐), 프레임 정확 컷은 재인코딩뿐이다.
- `-ss` 위치는 **속도**를 가른다. **입력 앞**(`-ss … -i`)=키프레임으로 점프 후 탐색이라 빠름, **입력 뒤**(`-i … -ss`)=처음부터 디코드라 느림. 현대 ffmpeg는 재인코딩 시 입력 앞 `-ss`도 정확하다. 끝점만 자를 땐 시작이 0이라 무관.
- `+faststart`는 moov atom을 파일 앞으로 옮겨 웹 스트리밍 첫 재생을 빠르게 한다(끝에 두 번째 pass가 붙어도 copy면 여전히 빠름).

## 합치기 (이어붙이기)

```bash
# 같은 코덱·해상도·fps — concat demuxer, copy로 무손실
printf "file '%s'\n" a.mp4 b.mp4 c.mp4 > list.txt
ffmpeg -y -f concat -safe 0 -i list.txt -c copy out.mp4

# 코덱/해상도가 다름 — concat 필터로 재인코딩(통일 필요)
ffmpeg -y -i a.mp4 -i b.mp4 -filter_complex "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]" -map "[v]" -map "[a]" out.mp4
```

**함정**: copy 합치기는 코덱·해상도·fps·픽셀포맷이 **전부 같아야** 깨지지 않는다. 하나라도 다르면 concat 필터(재인코딩). `-safe 0`은 절대경로/특수문자 파일명일 때 필요.

## 압축 (용량 줄이기) — 재인코딩

```bash
ffmpeg -y -i in.mp4 -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 128k out.mp4
```

- `crf`: 18(고화질·큰 용량) ~ 28(저화질·작은 용량), 기본 23. 낮을수록 고화질.
- `preset`: `ultrafast`→`veryslow`. 느릴수록 같은 화질에 더 작은 용량(시간↔용량 트레이드오프).
- 더 작게: `libx265`(HEVC, ~30% 절감, 호환성↓) 또는 해상도 축소 병행.

## 포맷·컨테이너 변환

```bash
# 컨테이너만 변경(mkv→mp4 등) — 코덱이 호환되면 copy로 무손실
ffmpeg -y -i in.mkv -c copy out.mp4

# 코덱 변경(예: webm/vp9) — 재인코딩
ffmpeg -y -i in.mp4 -c:v libvpx-vp9 -crf 30 -b:v 0 -c:a libopus out.webm
```

**함정**: mp4는 일부 코덱(예: PCM 오디오) 미수용 → copy 실패 시 해당 트랙만 재인코딩(`-c:v copy -c:a aac`).

## 오디오 추출 / 변환

```bash
ffmpeg -y -i in.mp4 -vn -c:a copy out.m4a       # 무손실 추출(원본이 aac면 m4a)
ffmpeg -y -i in.mp4 -vn -c:a libmp3lame -q:a 2 out.mp3   # mp3 변환(재인코딩)
ffmpeg -y -i in.mp4 -vn -c:a pcm_s16le out.wav  # wav(무압축)
```

`-vn`=비디오 제외. 무손실로 빼려면 원본 오디오 코덱에 맞는 컨테이너 선택.

## 해상도 / 프레임레이트 — 재인코딩

```bash
ffmpeg -y -i in.mp4 -vf "scale=1280:-2" -c:a copy out.mp4   # 가로 1280, 세로 자동(2의 배수)
ffmpeg -y -i in.mp4 -r 30 -c:a copy out.mp4                  # 30fps로
```

**함정**: scale에서 한 축을 `-2`로 두면 종횡비 유지 + libx264 요구사항(짝수)을 만족. `-1` 대신 `-2`를 쓴다.

## 회전

```bash
# 메타데이터만 회전(무손실·즉시, 플레이어가 메타 무시하면 안 돌아감)
ffmpeg -y -i in.mp4 -metadata:s:v rotate=90 -c copy out.mp4

# 픽셀 실제 회전(재인코딩, 어디서나 적용됨)
ffmpeg -y -i in.mp4 -vf "transpose=1" out.mp4   # 1=시계90, 2=반시계90, transpose 두 번=180
```

## GIF — 재인코딩 (팔레트 2-pass로 화질 확보)

```bash
ffmpeg -y -i in.mp4 -vf "fps=12,scale=480:-1:flags=lanczos,palettegen" -y palette.png
ffmpeg -y -i in.mp4 -i palette.png -lavfi "fps=12,scale=480:-1:flags=lanczos[x];[x][1:v]paletteuse" out.gif
```

**함정**: 팔레트 없이 바로 GIF면 색이 뭉개진다. fps·scale을 낮춰 용량 관리.

## 자막

```bash
# 소프트섭(트랙으로 삽입, 끄고 켤 수 있음) — mkv 권장, copy 가능
ffmpeg -y -i in.mp4 -i sub.srt -c copy -c:s mov_text out.mp4

# 하드섭(영상에 태워 넣음, 항상 보임) — 재인코딩
ffmpeg -y -i in.mp4 -vf "subtitles=sub.srt" -c:a copy out.mp4
```

**함정**: mp4의 자막 코덱은 `mov_text`. mkv는 `srt`/`ass` 그대로 copy. 하드섭은 폰트·스타일을 ass로 제어.

## 프레임 / 썸네일 추출

```bash
ffmpeg -y -ss 00:01:30 -i in.mp4 -frames:v 1 -q:v 2 thumb.jpg   # 특정 시점 1장
ffmpeg -y -i in.mp4 -vf "fps=1/10" frame_%04d.jpg              # 10초마다 1장
```

`-ss`를 `-i` 앞에 둬 빠르게 점프. `-q:v 2`=고화질 JPG(2~5 권장).

## 속도 변경 (배속) — 재인코딩

```bash
# 2배속(영상+오디오)
ffmpeg -y -i in.mp4 -filter_complex "[0:v]setpts=0.5*PTS[v];[0:a]atempo=2.0[a]" -map "[v]" -map "[a]" out.mp4
```

**함정**: `setpts` 계수는 배속의 **역수**(2배=0.5, 0.5배=2.0). `atempo`는 0.5~2.0만 받아 더 크면 체이닝(`atempo=2.0,atempo=2.0`=4배).

## 볼륨 / 오디오 정규화

```bash
ffmpeg -y -i in.mp4 -af "volume=2.0" -c:v copy out.mp4                       # 단순 2배(클리핑 주의)
ffmpeg -y -i in.mp4 -af "loudnorm=I=-16:TP=-1.5:LRA=11" -c:v copy out.mp4    # EBU R128 정규화
```

**함정**: 들쭉날쭉한 음량은 단순 `volume` 곱으로 못 고친다 — `loudnorm`이 강의·팟캐스트를 방송 표준(-16 LUFS)으로 고르게 맞춘다. 영상은 `-c:v copy`로 안 건드림.
