# OCR 스킬 유지보수

PDF 생성 기본값과 실행 규칙은 [SKILL.md](SKILL.md), 결과 검증과 기존 레이어 처리는 [품질 절차](references/pdf-text-quality.md)가 정본이다.

## 설계 근거

- 인식 모드를 명시해 OS에 따른 기본값 차이를 제거한다. 가로쓰기 문서에 `accurate`를 기본으로 두고, 세로쓰기는 별도 샘플로 판단한다.
- 공백 교정은 정상적인 단어 경계를 보존하는 작업이다. 문자 전체에서 공백을 지우는 검색용 정규화와 구분한다.
- 화면이 같아도 추출 순서는 달라질 수 있으므로 텍스트 레이어 생성과 검증을 함께 취급한다.
- 검사 도구의 문구 일치, 텍스트 존재, 페이지 구조 검사는 한정된 assertion이다. 전체 인식 정확도나 픽셀 동일성을 보장하지 않는다.

## 출처

- [AppleOCR 모드와 렌더러](https://github.com/mkyt/OCRmyPDF-AppleOCR): 기본 모드, 세로쓰기 지원 차이, 언어 보정, 렌더러 제약.
- [OCRmyPDF cookbook](https://ocrmypdf.readthedocs.io/en/latest/cookbook.html): 일반 PDF 출력, 기존 OCR 교체, 원본 외형 보존.
- [PDF의 논리적 읽는 순서](https://pdfa.org/techniques-for-accessible-pdf/content-order-correctly-set/UA1_Tpdf-G4_01/): 보이는 위치와 논리 구조의 구분.

## 검증 도구

[check-pdf-defaults.py](tests/check-pdf-defaults.py)는 [합성 PDF 생성기](tests/make-fixtures.swift)로 잘못된 공백, 순서 변경, 크기 변경, 텍스트 없는 PDF와 정상 PDF를 검사한다. `--output-dir`로 결과 위치를 지정한다. `--ocr`는 설치된 OCRmyPDF를 사용해 SKILL.md의 기본 명령을 실제 실행하고, PDFKit/Poppler의 문구 검색과 합성 페이지의 렌더링 동일성을 확인한다. `--baseline-skill`을 함께 주면 같은 입력에서 이전 기본 명령의 결과도 기록한다. Swift/PDFKit과 Poppler가 필요하며 테스트에는 개인 책이나 원격 모델을 사용하지 않는다.
