#!/usr/bin/env python3
import argparse
import csv
import re
import subprocess
from pathlib import Path
from urllib.parse import urlparse

ALLOWED_PREFIXES = (
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.ms-powerpoint",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "text/csv",
)


def slugify(text: str) -> str:
    text = re.sub(r"[^A-Za-z0-9._-]+", "-", text)
    text = re.sub(r"-{2,}", "-", text).strip("-")
    return text or "attachment"


def filename_for(url: str) -> str:
    p = urlparse(url)
    name = Path(p.path).name or "attachment"
    return slugify(name)


def main() -> None:
    ap = argparse.ArgumentParser(description="Download attachment candidates from TSV")
    ap.add_argument("tsv", help="attachment-candidates.tsv path")
    ap.add_argument("--out", required=True, help="download directory")
    ap.add_argument("--limit", type=int, default=20, help="max files to download")
    ap.add_argument("--report", help="optional report tsv path; default <out>/download-report.tsv")
    args = ap.parse_args()

    tsv_path = Path(args.tsv)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    report_path = Path(args.report) if args.report else out_dir / "download-report.tsv"

    rows = list(csv.DictReader(tsv_path.open(encoding="utf-8"), delimiter="\t"))
    seen = set()
    count = 0
    report_rows = []
    for row in rows:
        if count >= args.limit:
            break
        url = row["url"]
        if url in seen:
            continue
        seen.add(url)
        target = out_dir / filename_for(url)
        cmd = ["curl", "-L", "-s", url, "-o", str(target)]
        subprocess.run(cmd, check=False)
        file_proc = subprocess.run(["file", "-I", str(target)], capture_output=True, text=True, check=False)
        mime = ""
        if ": " in file_proc.stdout:
            mime = file_proc.stdout.split(": ", 1)[1].strip()
        status = "ok"
        note = ""
        if not any(mime.startswith(prefix) for prefix in ALLOWED_PREFIXES):
            status = "rejected"
            note = "unexpected mime"
            target.unlink(missing_ok=True)
        report_rows.append(
            {
                "url": url,
                "saved_path": str(target),
                "status": status,
                "mime": mime,
                "note": note,
            }
        )
        count += 1
        print(f"{status}\t{mime}\t{url}\t{target}")

    with report_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["url", "saved_path", "status", "mime", "note"], delimiter="\t")
        w.writeheader()
        w.writerows(report_rows)


if __name__ == "__main__":
    main()
