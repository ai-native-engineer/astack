---
argument-hint: "[image-or-pdf-path]"
name: ocr
description: "Local OCR for images and scanned PDFs using macOS Vision. Use when user asks OCR, 오씨알, 이미지 글자 읽어, 텍스트 추출, 스캔 PDF 읽어, 문서 텍스트화, PDF 텍스트, or image-to-text. Do NOT use for speech/audio transcription, Freeform board extraction, already-text PDFs, handwriting notes in Obsidian, or image generation."
---

# OCR — 이미지/스캔 PDF 텍스트 추출

macOS Vision 프레임워크 기반, 로컬 처리.

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

## 언어 코드 주의 (도구별로 다름)

| 도구 | 한국어 | 영어 | 중국어 |
| --- | --- | --- | --- |
| `ocrmypdf` (Tesseract 스타일) | `kor` | `eng` | — |
| `apple-ocr` (Apple Vision 스타일) | `ko` | `en` | `zh-Hans` |

`jpn`(ocrmypdf) / `ja`(apple-ocr) 등 다른 언어도 같은 규칙으로 매핑.
