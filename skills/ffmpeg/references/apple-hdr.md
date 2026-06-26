# Apple HDR → SDR 변환 & HEIC (사이니지·비-Apple 기기 호환)

iPhone/iPad 촬영 미디어를 디지털 사이니지·안드로이드·윈도우에서 재생되게 변환한다.

## 핵심 원리

iPhone은 영상을 **HLG(Hybrid Log-Gamma) / BT.2020** HDR 색공간으로 찍는다. 대부분의 사이니지·비-Apple 기기는 **BT.709(SDR)**만 지원하므로, 이 메타데이터가 남으면 재생 실패하거나 색이 깨진다.

### 절대 하면 안 되는 것: `tonemap` 금지

HLG는 SDR과 역호환되도록 설계돼 톤맵핑이 **필요 없다.** `tonemap=hable` 등을 쓰면 화면이 극도로 어두워진다. 픽셀은 그대로 두고 **메타데이터만 BT.709로 덮어쓰는 것**이 정답이다. HLG 하위 곡선이 표준 감마와 유사해 픽셀 값 자체는 SDR에서도 자연스럽게 표시된다 — 문제는 `color_primaries=bt2020`·`color_transfer=arib-std-b67` 태그가 기기에 "HDR이다"라고 알려 재생을 거부하게 만드는 것뿐이다.

## MOV → MP4 (사이니지 호환)

```bash
# 원본 해상도 유지, 고화질
ffmpeg -y -i input.MOV \
  -c:v libx264 -profile:v high -crf 18 \
  -vf "format=yuv420p,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709" \
  -c:a aac -b:a 128k \
  output.mp4

# 1920x1080 리사이즈 + 압축 (저사양 사이니지)
ffmpeg -y -i input.MOV \
  -c:v libx264 -profile:v main -level 4.1 -crf 23 \
  -vf "scale=1920:1080,format=yuv420p,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709" \
  -c:a aac -b:a 128k \
  output.mp4
```

- `setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709` — HDR 메타데이터를 SDR로 덮어쓰는 **핵심 필터**
- `format=yuv420p` — 호환성 최대화 픽셀 포맷
- `profile:v main -level 4.1` — 저사양 기기 호환. 고화질 필요 시 `high`
- `crf 18` — 고화질(0=무손실, 23=기본, 낮을수록 고화질)

## HEIC → JPG / PNG (macOS 내장 sips)

```bash
sips -s format jpeg -s formatOptions 100 input.HEIC --out output.jpg   # 최대 품질 0~100
sips -s format png input.HEIC --out output.png
```

ffmpeg가 아니라 macOS 내장 `sips` 사용 — 별도 설치 불필요.

## 일괄 변환

```bash
for f in *.MOV *.mov; do
  [ -f "$f" ] || continue
  ffmpeg -y -i "$f" \
    -c:v libx264 -profile:v high -crf 18 \
    -vf "format=yuv420p,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709" \
    -c:a aac -b:a 128k \
    "${f%.*}.mp4"
done

for f in *.HEIC *.heic; do
  [ -f "$f" ] || continue
  sips -s format jpeg -s formatOptions 100 "$f" --out "${f%.*}.jpg"
done
```

## 검증

변환 후 색공간 메타데이터가 BT.709인지 반드시 확인:

```bash
ffprobe -v error -show_entries stream=color_space,color_transfer,color_primaries -of default=noprint_wrappers=1 output.mp4
```

- **정상**: `color_space=bt709` / `color_transfer=bt709` / `color_primaries=bt709`
- **잔존(문제)**: `bt2020nc` / `arib-std-b67` / `bt2020`

## 트러블슈팅

| 증상 | 원인 | 해결 |
|---|---|---|
| 사이니지에서 재생 안 됨 | BT.2020/HLG 메타데이터 잔존 | `setparams`로 BT.709 덮어쓰기 |
| 변환 후 화면이 극도로 어두움 | `tonemap` 필터 사용 | tonemap 제거, `setparams`만 사용 |
| 해상도 관련 재생 실패 | 4K를 사이니지가 미지원 | `scale=1920:1080` 추가 |
| H.264 프로파일 미지원 | High Profile / Level 5.1 | `main -level 4.1`로 변경 |
| `colorspace` 필터 에러 | HLG 입력 파싱 실패 | `colorspace` 대신 `setparams` 사용 |
