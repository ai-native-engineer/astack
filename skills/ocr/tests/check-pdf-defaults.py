"""Run native PDF inspection checks and optional real OCR using the documented default command."""

import argparse
import hashlib
import json
import re
import shlex
import subprocess
import tempfile
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--output-dir", type=Path, required=True)
parser.add_argument(
    "--ocr",
    action="store_true",
    help="Also run the installed OCRmyPDF/AppleOCR pipeline",
)
parser.add_argument(
    "--baseline-skill",
    type=Path,
    help="Compare a previous SKILL.md default on the same fixture",
)
args = parser.parse_args()
args.output_dir.mkdir(parents=True, exist_ok=True)
run = Path(tempfile.mkdtemp(prefix="pdf-defaults-", dir=args.output_dir))
skill = Path(__file__).resolve().parents[1]
probe = run / "inspect-pdf-text"
subprocess.run(
    ["swiftc", str(skill / "scripts/inspect-pdf-text.swift"), "-o", str(probe)],
    check=True,
)
subprocess.run(
    ["swift", str(skill / "tests/make-fixtures.swift"), str(run)], check=True
)
results = {}


def inspect(name, filename, options, expected_failure=None):
    process = subprocess.run(
        [str(probe), str(run / filename), *options],
        text=True,
        capture_output=True,
        check=False,
    )
    (run / (name + ".json")).write_text(process.stdout, encoding="utf-8")
    report = json.loads(process.stdout)
    if expected_failure:
        assert process.returncode == 2 and expected_failure in report["failures"], (
            report
        )
    else:
        assert process.returncode == 0 and not report["failures"], report
    results[name] = {"exit": process.returncode, "failures": report["failures"]}
    return report


phrases = ["도서관에서 책을 읽습니다", "Deep learning helps us study"]
expect = [item for phrase in phrases for item in ("--expect", phrase)]
inspect("bad-spacing-rejected", "spaced.pdf", expect, "expected_phrase_missing")
inspect(
    "reading-order-rejected",
    "reordered.pdf",
    ["--source", str(run / "reference.pdf"), "--preserve-text", "--pages", "all"],
    "non_whitespace_text_or_order_changed",
)
inspect(
    "geometry-change-rejected",
    "resized.pdf",
    ["--source", str(run / "reference.pdf")],
    "page_geometry_changed",
)
inspect("image-only-rejected", "scan.pdf", [], "no_extractable_text")
inspect(
    "valid-reference",
    "reference.pdf",
    expect
    + ["--source", str(run / "reference.pdf"), "--preserve-text", "--pages", "all"],
)


def ocr_command(skill_file, output):
    code = re.search(
        r"```bash\n(.*?)```", skill_file.read_text(encoding="utf-8"), re.DOTALL
    ).group(1)
    command = shlex.split(code.replace("\\\n", " "), comments=True)
    assert command[0] == "ocrmypdf"
    command[-2:] = [str(run / "scan.pdf"), str(output)]
    return command


if args.ocr:
    source_hash = hashlib.sha256((run / "scan.pdf").read_bytes()).hexdigest()
    output = run / "accurate_ocr.pdf"
    command = ocr_command(skill / "SKILL.md", output)
    with (run / "ocr.log").open("w") as log:
        subprocess.run(command, check=True, stdout=log, stderr=subprocess.STDOUT)
    assert hashlib.sha256((run / "scan.pdf").read_bytes()).hexdigest() == source_hash
    inspect(
        "actual-ocr-default",
        output.name,
        expect + ["--source", str(run / "scan.pdf"), "--pages", "all"],
    )
    poppler = subprocess.run(
        ["pdftotext", str(output), "-"], check=True, text=True, capture_output=True
    ).stdout
    (run / "poppler.txt").write_text(poppler, encoding="utf-8")
    assert all(phrase in poppler for phrase in phrases), poppler
    results["poppler-phrase-search"] = True
    for filename, prefix in [(run / "scan.pdf", "source"), (output, "output")]:
        subprocess.run(
            ["pdftoppm", "-r", "72", str(filename), str(run / prefix)], check=True
        )
    before = sorted(run.glob("source-*.ppm"))
    after = sorted(run.glob("output-*.ppm"))
    assert len(before) == len(after) == 2
    assert all(
        a.read_bytes() == b.read_bytes() for a, b in zip(before, after, strict=True)
    )
    results["rendered-pixels-unchanged"] = {"pages": 2, "dpi": 72}
    output_hash = hashlib.sha256(output.read_bytes()).hexdigest()
    with (run / "overwrite-refusal.log").open("w") as log:
        repeated = subprocess.run(
            command, check=False, stdout=log, stderr=subprocess.STDOUT
        )
    assert (
        repeated.returncode != 0
        and hashlib.sha256(output.read_bytes()).hexdigest() == output_hash
    )
    results["overwrite-refused"] = True
    if args.baseline_skill:
        baseline = run / "baseline.pdf"
        with (run / "baseline-ocr.log").open("w") as log:
            subprocess.run(
                ocr_command(args.baseline_skill, baseline),
                check=True,
                stdout=log,
                stderr=subprocess.STDOUT,
            )
        process = subprocess.run(
            [str(probe), str(baseline), "--pages", "all", *expect],
            text=True,
            capture_output=True,
            check=False,
        )
        report = json.loads(process.stdout)
        (run / "baseline-inspection.json").write_text(process.stdout, encoding="utf-8")
        results["baseline"] = {
            "exit": process.returncode,
            "failures": report["failures"],
            "missing_phrases": report["expected_phrases_missing"],
        }

(run / "results.json").write_text(
    json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
)
print(
    json.dumps({"output": str(run), "results": results}, ensure_ascii=False, indent=2)
)
