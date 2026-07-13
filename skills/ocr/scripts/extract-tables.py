# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "img2table",
#     "pandas",
#     "tabulate",
#     "pyobjc-framework-Vision",
#     "pyobjc-framework-Cocoa",
# ]
# ///
"""스캔 PDF/이미지에서 표 구조(행·열)를 추출해 markdown/html/csv로 출력.

표 검출은 img2table(OpenCV), 텍스트 인식은 macOS Vision(Apple OCR).
실행: uv run extract-tables.py <input.pdf|image> [--pages 1-20] [--format md]
"""

from __future__ import annotations

import argparse
import os
import sys
import tempfile
from pathlib import Path

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".tiff", ".tif", ".webp", ".bmp"}


class AppleVisionOCR:
    """img2table OCRInstance 규격의 macOS Vision 래퍼."""

    def __init__(self, lang: list[str], recognition_level: str = "accurate") -> None:
        self.lang = lang
        self.recognition_level = recognition_level

    def of(self, document):
        import Cocoa
        import cv2
        import objc
        import Vision

        records = {}
        for page, image in enumerate(document.images):
            height, width = image.shape[:2]
            fd, tmp_path = tempfile.mkstemp(suffix=".png")
            os.close(fd)
            # document.images는 RGB, cv2.imwrite는 BGR을 기대
            cv2.imwrite(tmp_path, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
            try:
                with objc.autorelease_pool():
                    req = Vision.VNRecognizeTextRequest.alloc().init()
                    level = (
                        Vision.VNRequestTextRecognitionLevelAccurate
                        if self.recognition_level == "accurate"
                        else Vision.VNRequestTextRecognitionLevelFast
                    )
                    req.setRecognitionLevel_(level)
                    req.setAutomaticallyDetectsLanguage_(False)
                    req.setRecognitionLanguages_(self.lang)
                    req.setUsesLanguageCorrection_(True)

                    handler = Vision.VNImageRequestHandler.alloc().initWithURL_options_(
                        Cocoa.NSURL.fileURLWithPath_(tmp_path), None
                    )
                    _, error = handler.performRequests_error_([req], None)
                    if error:
                        raise RuntimeError(f"VNRecognizeTextRequest error: {error}")

                    for idx, obs in enumerate(req.results()):
                        candidate = obs.topCandidates_(1)[0]
                        bb = obs.boundingBox()  # normalized, bottom-left origin
                        word_id = f"word_{page + 1}_{idx + 1}"
                        records.setdefault(page, []).append(
                            {
                                "id": word_id,
                                "parent": word_id,
                                "value": candidate.string(),
                                "confidence": round(candidate.confidence() * 100),
                                "x1": round(bb.origin.x * width),
                                "y1": round((1 - bb.origin.y - bb.size.height) * height),
                                "x2": round((bb.origin.x + bb.size.width) * width),
                                "y2": round((1 - bb.origin.y) * height),
                            }
                        )
            finally:
                Path(tmp_path).unlink(missing_ok=True)

        from img2table.ocr._types import OCRData

        return OCRData(records=records) if records else None


def parse_pages(spec: str) -> list[int]:
    """1-based 페이지 스펙("3", "1-20", "1,5,9-12")을 0-based 목록으로."""
    pages: set[int] = set()
    for part in spec.split(","):
        if "-" in part:
            a, b = part.split("-", 1)
            pages.update(range(int(a) - 1, int(b)))
        else:
            pages.add(int(part) - 1)
    return sorted(pages)


def render(df, fmt: str) -> str:
    if fmt == "md":
        return df.to_markdown(index=False)
    if fmt == "html":
        return df.to_html(index=False)
    return df.to_csv(index=False)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input", help="PDF 또는 이미지 경로")
    ap.add_argument("--pages", help="1-based 페이지 스펙 (예: 1-20 / 3,7,9-12). PDF 전용, 생략 시 전체")
    ap.add_argument("--format", choices=["md", "html", "csv"], default="md")
    ap.add_argument("--lang", default="ko-KR,en-US", help="Vision BCP-47 언어 코드, 쉼표 구분")
    ap.add_argument("--force-ocr", action="store_true",
                    help="PDF 내장 텍스트 레이어를 무시하고 항상 Vision OCR 사용")
    ap.add_argument("--min-confidence", type=int, default=50)
    args = ap.parse_args()

    src = Path(args.input).expanduser()
    if not src.is_file():
        sys.exit(f"파일 없음: {src}")

    ocr = AppleVisionOCR(lang=args.lang.split(","))
    kwargs = dict(ocr=ocr, implicit_rows=True, borderless_tables=True,
                  min_confidence=args.min_confidence)

    if src.suffix.lower() in IMAGE_EXTS:
        from img2table.document import Image

        tables = {0: Image(src=str(src)).extract_tables(**kwargs)}
    else:
        from img2table.document import PDF

        doc = PDF(
            src=str(src),
            pages=parse_pages(args.pages) if args.pages else None,
            pdf_text_extraction=not args.force_ocr,
        )
        tables = doc.extract_tables(**kwargs)

    found = 0
    for page, tbls in sorted(tables.items()):
        for i, t in enumerate(tbls):
            found += 1
            print(f"\n## page {page + 1} - table {i + 1}\n")
            print(render(t.df, args.format))
    if not found:
        print("표 없음", file=sys.stderr)


if __name__ == "__main__":
    main()
