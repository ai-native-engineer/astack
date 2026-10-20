---
name: ocr
description: "Local OCR, searchable PDF text-layer creation/repair, and table extraction. Use for OCR, 이미지 글자 읽기, 스캔 PDF 텍스트화, OCR 레이어 교체, 문자 사이 공백 문제, or 표를 Markdown/CSV로 추출. Do NOT use for speech transcription, routine reading or keyword search in searchable PDFs, Freeform boards, Obsidian handwriting notes, or image generation."
compatibility: "macOS; OCRmyPDF with AppleOCR for PDF OCR. Swift/PDFKit and Poppler for PDF text-layer verification."
metadata:
  requires:
    - tool: ocrmypdf
      check: command -v ocrmypdf
      install: uv tool install ocrmypdf --with "ocrmypdf-appleocr @ git+https://github.com/mkyt/OCRmyPDF-AppleOCR.git"
    - tool: gs
      check: command -v gs
      install: brew install ghostscript
---

# OCR - 이미지와 스캔 PDF 텍스트 추출

macOS Vision을 사용해 로컬에서 처리한다. 정상적인 단어 간 띄어쓰기는 보존하고, 글자마다 끼는 불필요한 공백을 피한다. 문법을 다시 쓰거나 모든 공백을 삭제하는 작업은 기본 범위가 아니다.

이미 검색 가능한 PDF에서 단어가 나오는 페이지를 찾는 요청은 이 스킬의 실행 대상이 아니다. 기존 텍스트를 검색한다.

## PDF 텍스트 레이어

생성하거나 교체하기 전에 [텍스트 레이어 품질 절차](references/pdf-text-quality.md)를 읽고 적용한다. 가로쓰기 PDF는 인식 모드와 렌더러를 명시한다. 모드를 생략하면 환경에 따라 LiveText가 선택돼 글자 단위 조각 사이에 공백이 생길 수 있다.

```bash
ocrmypdf --ocr-engine appleocr --appleocr-recognition-mode accurate \
  --pdf-renderer sandwich --output-type pdf --optimize 0 \
  --no-overwrite -l kor input.pdf output_ocr.pdf
```

- 언어는 문서에 맞게 선택한다. 세로쓰기는 기본 모드로 품질을 보장하지 않으며, 품질 절차의 예외 분기를 따른다.
- 원본을 보존하고 별도 `_ocr.pdf`로 저장한다. 기존 OCR 레이어 교체는 새 사본에 `--redo-ocr`를 사용한 뒤 검증한다.
- 생성 성공이나 텍스트 존재만으로 완료하지 않는다. 공백, 검색 가능한 문구, 읽는 순서와 페이지 외형을 확인한다.
- [inspect-pdf-text.swift](scripts/inspect-pdf-text.swift)는 실행 도구다. 실제 스킬 경로에서 `swift`로 실행하며 사용법은 `--help`로 확인한다.
- 설치: `uv tool install ocrmypdf --with "ocrmypdf-appleocr @ git+https://github.com/mkyt/OCRmyPDF-AppleOCR.git"`
- AppleOCR는 자동 등록되므로 `--plugin ocrmypdf_appleocr`를 중복으로 추가하지 않는다.
- Ghostscript가 필요한 처리에서 `gs`가 없으면 `brew install ghostscript` 후 `command -v gs`로 확인한다.

## 이미지 텍스트 추출

```bash
apple-ocr -l ko "이미지.png"
```

PDF에는 위 PDF 텍스트 레이어 절차를 사용한다.

## 표 구조 추출

표, 테이블, Markdown/CSV 추출을 요청한 경우에만 [extract-tables.py](scripts/extract-tables.py)를 실행한다. 표 검출은 img2table, 인식은 macOS Vision이다.

```bash
uv run scripts/extract-tables.py input.pdf --pages 1-20
uv run scripts/extract-tables.py 표.png --format csv
```

- 위 스크립트 경로는 실제 OCR 스킬 경로로 해석한다. 출력 형식과 옵션은 `--help`로 확인한다.
- 내장 텍스트를 먼저 쓰고 없으면 Vision OCR로 폴백한다. 내장 레이어 때문에 표 분석이 잘못되면 이 스크립트의 `--force-ocr`로 내장 텍스트를 우회한다. 이는 PDF 페이지를 재래스터화하는 OCRmyPDF의 동명 옵션과 다르다.
- 결과는 표 후보이므로 원본과 대조한다. 선 없는 표, 다이어그램, 목차는 오인식할 수 있다.

## 언어 코드

| 도구 | 한국어 | 영어 | 중국어 |
| --- | --- | --- | --- |
| `ocrmypdf` | `kor` | `eng` | `chi_sim` / `chi_tra` |
| `apple-ocr` | `ko` | `en` | `zh-Hans` |
| `extract-tables.py` | `ko-KR` | `en-US` | `zh-Hans` |

일본어는 각각 `jpn`, `ja`, `ja-JP`를 사용한다. AppleOCR의 자동 언어 감지가 필요하면 `accurate`에서 `-l und`를 사용하고, 여러 언어 코드를 `+`로 묶지 않는다.
