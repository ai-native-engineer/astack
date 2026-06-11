#!/usr/bin/env python3
import argparse
import csv
import subprocess
import time
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlparse


SCRIPT_DIR = Path(__file__).resolve().parent
RECURSIVE = SCRIPT_DIR / "recursive_surface_crawl.py"
POSTPROCESS = SCRIPT_DIR / "postprocess_recursive_crawl.py"
MIRROR = SCRIPT_DIR / "mirror_selected_pages.py"
DOWNLOAD = SCRIPT_DIR / "download_attachment_candidates.py"
HOST_FIELDS = [
    "host",
    "top_score",
    "has_page_seed",
    "seed_count",
    "seeds",
    "output_dir",
    "crawl_status",
    "crawl_return_code",
    "crawl_duration_seconds",
    "postprocess_status",
    "postprocess_return_code",
    "postprocess_duration_seconds",
    "download_status",
    "download_return_code",
    "download_duration_seconds",
    "mirror_status",
    "mirror_return_code",
    "mirror_duration_seconds",
    "page_count",
    "inventory_rows",
    "attachment_candidate_rows",
    "shortlist_rows",
    "detail",
]


def host_keywords(host: str) -> list[str]:
    host = host.lower()
    parts = [p for p in host.replace("-", ".").split(".") if p and p not in {"www", "com", "co", "kr", "net", "org"}]
    return list(dict.fromkeys(parts))


def run_child(cmd: list[str], timeout_seconds: int) -> tuple[str, str, str, str]:
    started = time.perf_counter()
    try:
        proc = subprocess.run(cmd, check=False, capture_output=True, text=True, timeout=timeout_seconds)
    except subprocess.TimeoutExpired as exc:
        duration = time.perf_counter() - started
        if exc.stdout:
            print(str(exc.stdout).rstrip())
        if exc.stderr:
            print(str(exc.stderr).rstrip())
        return "timeout", "", f"{duration:.3f}", f"timeout after {timeout_seconds}s"
    duration = time.perf_counter() - started
    if proc.stdout:
        print(proc.stdout.rstrip())
    if proc.stderr:
        print(proc.stderr.rstrip())
    return ("ok" if proc.returncode == 0 else "failed"), str(proc.returncode), f"{duration:.3f}", ""


def tsv_data_rows(path: Path) -> int:
    if not path.exists():
        return 0
    with path.open(encoding="utf-8", errors="ignore") as f:
        return max(sum(1 for _ in f) - 1, 0)


def page_count(host_dir: Path) -> int:
    pages_dir = host_dir / "pages"
    if not pages_dir.exists():
        return 0
    return sum(1 for path in pages_dir.rglob("*.md") if path.is_file())


def main() -> None:
    ap = argparse.ArgumentParser(description="Run a second-pass recursive crawl from shortlist hosts")
    ap.add_argument("shortlist", help="shortlist.tsv path")
    ap.add_argument("--out", required=True, help="second-pass output root")
    ap.add_argument("--category", action="append", default=["brand-related"], help="categories to expand")
    ap.add_argument("--max-hosts", type=int, default=3)
    ap.add_argument("--max-seeds-per-host", type=int, default=3)
    ap.add_argument("--max-pages", type=int, default=15)
    ap.add_argument("--max-hops", type=int, default=1)
    ap.add_argument("--mirror-out-root", help="optional public-mirror root for second-pass shortlisted pages")
    ap.add_argument("--mirror-limit", type=int, default=6)
    ap.add_argument("--attachments-dir", help="optional shared attachments dir")
    ap.add_argument("--download-limit", type=int, default=10)
    ap.add_argument("--stage-timeout-seconds", type=int, default=180, help="timeout for each child crawl/download/mirror command")
    args = ap.parse_args()

    shortlist = list(csv.DictReader(Path(args.shortlist).open(encoding="utf-8"), delimiter="\t"))
    buckets: dict[str, list[dict]] = defaultdict(list)
    for row in shortlist:
        if row["category"] not in set(args.category):
            continue
        url = row["url"]
        parsed = urlparse(url)
        host = parsed.netloc.lower()
        if url.lower().endswith((".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx", ".csv")):
            root_seed = f"https://{host}/"
            buckets[host].append({**row, "url": root_seed, "reason": row["reason"] + " -> host root", "_seed_type": "attachment-derived"})
            continue
        buckets[host].append({**row, "_seed_type": "page"})

    scored_hosts = []
    for host, rows in buckets.items():
        top_score = max(int(r.get("score", 0)) for r in rows)
        has_page_seed = any(r.get("_seed_type") == "page" for r in rows)
        scored_hosts.append((1 if has_page_seed else 0, top_score, host, rows))
    scored_hosts.sort(key=lambda x: (-x[0], -x[1], x[2]))
    selected_hosts = scored_hosts[: args.max_hosts]
    out_root = Path(args.out)
    out_root.mkdir(parents=True, exist_ok=True)
    summary_rows = []

    for has_page_seed, top_score, host, rows in selected_hosts:
        seeds = []
        for row in rows[: args.max_seeds_per_host]:
            seeds.append(row["url"])
        host_dir = out_root / host.replace("/", "_")
        host_dir.mkdir(parents=True, exist_ok=True)
        cmd = [
            "python3",
            str(RECURSIVE),
            *seeds,
            "--max-pages",
            str(args.max_pages),
            "--max-hops",
            str(args.max_hops),
            "--out",
            str(host_dir),
        ]
        for keyword in host_keywords(host):
            cmd.extend(["--keyword", keyword])
        crawl_status, crawl_return_code, crawl_duration, crawl_detail = run_child(cmd, args.stage_timeout_seconds)
        postprocess_status, postprocess_return_code, postprocess_duration, postprocess_detail = run_child(
            ["python3", str(POSTPROCESS), str(host_dir)],
            args.stage_timeout_seconds,
        )
        download_status = "skipped"
        download_return_code = "0"
        download_duration = "0.000"
        download_detail = ""
        if args.attachments_dir:
            download_status, download_return_code, download_duration, download_detail = run_child(
                [
                    "python3",
                    str(DOWNLOAD),
                    str(host_dir / "attachment-candidates.tsv"),
                    "--out",
                    str(Path(args.attachments_dir)),
                    "--limit",
                    str(args.download_limit),
                    "--report",
                    str(host_dir / "download-report.tsv"),
                ],
                args.stage_timeout_seconds,
            )
        mirror_status = "skipped"
        mirror_return_code = "0"
        mirror_duration = "0.000"
        mirror_detail = ""
        if args.mirror_out_root:
            mirror_status, mirror_return_code, mirror_duration, mirror_detail = run_child(
                [
                    "python3",
                    str(MIRROR),
                    str(host_dir / "shortlist.tsv"),
                    "--out",
                    str(Path(args.mirror_out_root)),
                    "--limit",
                    str(args.mirror_limit),
                ],
                args.stage_timeout_seconds,
            )
        detail = "; ".join(
            part
            for part in [crawl_detail, postprocess_detail, download_detail, mirror_detail]
            if part
        )
        summary_rows.append(
            {
                "host": host,
                "top_score": str(top_score),
                "has_page_seed": str(bool(has_page_seed)).lower(),
                "seed_count": str(len(seeds)),
                "seeds": " | ".join(seeds),
                "output_dir": str(host_dir),
                "crawl_status": crawl_status,
                "crawl_return_code": crawl_return_code,
                "crawl_duration_seconds": crawl_duration,
                "postprocess_status": postprocess_status,
                "postprocess_return_code": postprocess_return_code,
                "postprocess_duration_seconds": postprocess_duration,
                "download_status": download_status,
                "download_return_code": download_return_code,
                "download_duration_seconds": download_duration,
                "mirror_status": mirror_status,
                "mirror_return_code": mirror_return_code,
                "mirror_duration_seconds": mirror_duration,
                "page_count": str(page_count(host_dir)),
                "inventory_rows": str(tsv_data_rows(host_dir / "link-inventory.tsv")),
                "attachment_candidate_rows": str(tsv_data_rows(host_dir / "attachment-candidates.tsv")),
                "shortlist_rows": str(tsv_data_rows(host_dir / "shortlist.tsv")),
                "detail": detail,
            }
        )
        print(f"{host}\t{host_dir}")

    summary_tsv = out_root / "second-pass-hosts.tsv"
    with summary_tsv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=HOST_FIELDS, delimiter="\t")
        writer.writeheader()
        writer.writerows(summary_rows)

    summary_md = out_root / "second-pass-summary.md"
    lines = ["# Second Pass Summary", ""]
    for row in summary_rows:
        lines.append(f"## {row['host']}")
        lines.append("")
        lines.append(f"- Top score: `{row['top_score']}`")
        lines.append(f"- Has page seed: `{row['has_page_seed']}`")
        lines.append(f"- Output dir: `{row['output_dir']}`")
        lines.append(f"- Crawl status: `{row['crawl_status']}`")
        lines.append(f"- Postprocess status: `{row['postprocess_status']}`")
        lines.append(f"- Download status: `{row['download_status']}`")
        lines.append(f"- Mirror status: `{row['mirror_status']}`")
        lines.append(f"- Pages / inventory / shortlist: `{row['page_count']} / {row['inventory_rows']} / {row['shortlist_rows']}`")
        lines.append("- Seeds:")
        for seed in row["seeds"].split(" | "):
            lines.append(f"  - {seed}")
        if row["detail"]:
            lines.append(f"- Detail: {row['detail']}")
        lines.append("")
    summary_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
