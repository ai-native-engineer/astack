#!/usr/bin/env python3
import argparse
import csv
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
from recursive_surface_crawl import path_slug  # noqa: E402


def is_attachment(url: str) -> bool:
    return url.lower().endswith((".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx", ".csv"))


def main() -> None:
    ap = argparse.ArgumentParser(description="Mirror selected high-signal pages from shortlist/keep-list")
    ap.add_argument("tsv", help="shortlist.tsv or keep-list-candidates.tsv path")
    ap.add_argument("--out", required=True, help="public-mirror output dir")
    ap.add_argument("--limit", type=int, default=20, help="max pages to mirror")
    args = ap.parse_args()

    rows = list(csv.DictReader(Path(args.tsv).open(encoding="utf-8"), delimiter="\t"))
    out_root = Path(args.out)
    out_root.mkdir(parents=True, exist_ok=True)
    urls = {row["url"] for row in rows}

    mirrored = 0
    for row in rows:
        if mirrored >= args.limit:
            break
        url = row["url"]
        if is_attachment(url):
            continue
        if url.endswith("/en_GB"):
            ko = url[:-5] + "ko_KR"
            if ko in urls:
                continue
        dest = out_root / path_slug(url)
        dest.parent.mkdir(parents=True, exist_ok=True)
        cmd = [
            str(Path.home() / ".local/bin/crwl"),
            "crawl",
            url,
            "-o",
            "md-fit",
            "-O",
            str(dest),
        ]
        subprocess.run(cmd, check=False)
        print(f"{url}\t{dest}")
        mirrored += 1


if __name__ == "__main__":
    main()
