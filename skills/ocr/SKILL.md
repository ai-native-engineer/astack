---
argument-hint: "[image-or-pdf-path]"
name: ocr
description: "Local OCR and table extraction for images and scanned PDFs using macOS Vision. Use when user asks OCR, 오씨알, 이미지 글자 읽어, 텍스트 추출, 표 추출/인식, 테이블을 markdown/CSV로, 스캔 PDF 읽어, 문서 텍스트화, PDF 텍스트, or image-to-text. Do NOT use for speech/audio transcription, Freeform board extraction, already-text PDFs, handwriting notes in Obsidian, or image generation."
---

# OCR — 이미지/스캔 PDF 텍스트 추출

macOS Vision 프레임워크 기반, 로컬 처리.

기본 동작은 PDF에 투명 텍스트 레이어를 넣거나 이미지에서 텍스트를 읽는 것이다. 사용자가 표·테이블·markdown·CSV 추출을 명시할 때만 `extract-tables.py`를 실행한다.

## PDF OCR → `ocrmypdf` + Apple OCR 플러그인 (권장)

```bash
ocrmypdf --plugin ocrmypdf_appleocr -l kor input.pdf output.pdf
```

- 병렬 처리, PDF에 **투명 텍스트 레이어**를 직접 생성 (텍스트 선택/검색 가능).
- `gs`(Ghostscript)가 `git status`로 alias돼 최적화 경고가 뜨지만 OCR 자체는 정상 동작.
- 설치: `uv tool install ocrmypdf --with "ocrmypdf-appleocr @ git+https://github.com/mkyt/OCRmyPDF-AppleOCR.git"`

## 이미지 OCR → `apple-ocr`

```bash
apple-ocr -l ko "이미지.png"
```

- PDF에는 `ocrmypdf`를 사용 (상위 호환).

## 표 구조 추출 → `scripts/extract-tables.py`

표·양식·다단 비교 박스의 행/열 구조가 필요할 때 (일반 텍스트는 위 두 도구로 충분). 표 검출은 img2table, 텍스트 인식은 Apple Vision이라 Tesseract·언어팩 설치가 필요 없다.

```bash
uv run scripts/extract-tables.py input.pdf --pages 1-20   # 설치된 ocr 스킬 루트, PDF (1-based)
uv run scripts/extract-tables.py 표.png --format csv      # 설치된 ocr 스킬 루트, 이미지
```

- 출력: markdown(기본)/html/csv → stdout. 옵션 전체는 `--help`.
- PDF에 내장 텍스트 레이어가 있으면 그걸 쓰고 없으면 Vision OCR로 폴백. 내장 레이어가 띄어쓰기를 뭉갤 때는 `--force-ocr`가 더 깔끔하다.
- 검출 결과는 표 **후보**다 — 다이어그램 박스·표지 문구도 표로 잡히니 내용을 보고 취사선택한다. 선 없는 표는 정확도가 떨어진다.

## 언어 코드 주의 (도구별로 다름)

| 도구 | 한국어 | 영어 | 중국어 |
| --- | --- | --- | --- |
| `ocrmypdf` (Tesseract 스타일) | `kor` | `eng` | — |
| `apple-ocr` (Apple Vision 스타일) | `ko` | `en` | `zh-Hans` |
| `extract-tables.py` (BCP-47, `--lang`) | `ko-KR` | `en-US` | `zh-Hans` |

`jpn`(ocrmypdf) / `ja`(apple-ocr) 등 다른 언어도 같은 규칙으로 매핑.
