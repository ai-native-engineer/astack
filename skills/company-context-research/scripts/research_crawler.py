#!/usr/bin/env python3
"""Unified research crawler and postprocessor for the company-context-research skill.
Supports crawling, rebuilding inventories, page pruning, page mirroring, and multi-domain second-pass expansion,
along with automatic attachment downloading (with JS decryption), dynamic finance charts, and export risk analysis.
"""
import argparse
import csv
import re
import subprocess
import sys
import time
import json
import os
from collections import deque, defaultdict
from pathlib import Path
from urllib.parse import urlparse, urlunparse

# --- Globals and Consts ---
URL_RE = re.compile(r"https?://[^\s\)\]>'\"]+")
ATTACHMENT_EXTS = (".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx", ".csv")
NOISE_EXTS = (".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp", ".css", ".js", ".woff", ".woff2")
ALLOWED_MIMES = (
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.ms-powerpoint",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "text/csv",
)
SOCIAL_HOSTS = {
    "linkedin.com", "www.linkedin.com", "instagram.com", "www.instagram.com",
    "youtube.com", "www.youtube.com", "facebook.com", "www.facebook.com",
    "x.com", "twitter.com", "www.x.com", "www.twitter.com"
}
LOW_SIGNAL_PATH_PARTS = (
    "/products/", "/product/", "/collections/", "/cart", "/checkout", "/account", "/search", "/cdn/", "/membership"
)
HIGH_SIGNAL_PATH_PARTS = (
    "/about", "/strategy", "/history", "/purpose", "/values", "/operations", "/newsroom", "/news", "/press",
    "/media", "/report", "/reports", "/sustainability", "/investor", "/careers", "/career", "/contact",
    "/contacts", "/pages/", "/blogs/", "/who-we-are", "/innovation"
)
LOW_SIGNAL_EXACT_PATHS = {
    "/cookie-policy/", "/privacy-policy/", "/site-terms/", "/accessibility-statement/", "/about-us/strate", "/newsroom/__trashed/"
}
PRUNE_SUBSTRINGS = (
    "/about-us/strate.md", "/sustainability/sustainability/"
)

TARGET_KEYWORDS = []

# --- Helper Functions ---
def base_domain(host: str) -> str:
    host = host.lower().strip(".")
    if host.endswith(".co.kr") or host.endswith(".or.kr") or host.endswith(".go.kr"):
        parts = host.split(".")
        return ".".join(parts[-3:]) if len(parts) >= 3 else host
    parts = host.split(".")
    return ".".join(parts[-2:]) if len(parts) >= 2 else host

def normalize(url: str) -> str:
    p = urlparse(url)
    scheme = "https" if p.scheme in {"http", "https"} else p.scheme
    host = p.netloc.lower()
    if host == "amersports.com":
        host = "www.amersports.com"
    path = p.path or "/"
    path = path.replace("/sustainability/sustainability/", "/sustainability/")
    while "//" in path:
        path = path.replace("//", "/")
    clean = urlunparse((scheme, host, path, "", "", ""))
    return clean.rstrip("#")

def path_slug(url: str) -> Path:
    p = urlparse(url)
    path = p.path.strip("/")
    if not path:
        return Path(p.netloc) / "index.md"
    return Path(p.netloc) / f"{path}.md"

def is_noise(url: str) -> bool:
    p = urlparse(url)
    lower = p.path.lower()
    if any(lower.endswith(ext) for ext in NOISE_EXTS):
        return True
    if p.netloc.lower() in SOCIAL_HOSTS:
        return True
    return False

def is_attachment(url: str) -> bool:
    if "dummy-file-host.com" in url:
        return True
    return urlparse(url).path.lower().endswith(ATTACHMENT_EXTS)

def get_commerce_allow_prefixes(host: str) -> tuple:
    host = host.lower()
    for kw in TARGET_KEYWORDS:
        if kw in host:
            return ("/pages/", "/blogs/")
    for kw in ("salomon", "wilson", "arc'teryx", "atomic"):
        if kw in host:
            return ("/pages/", "/blogs/")
    return ()

def get_commerce_deny_prefixes(host: str) -> tuple:
    host = host.lower()
    for kw in TARGET_KEYWORDS:
        if kw in host:
            return ("/collections/", "/products/", "/product/", "/account", "/cart", "/checkout", "/search")
    for kw in ("salomon", "wilson", "arc'teryx", "atomic"):
        if kw in host:
            return ("/collections/", "/products/", "/product/", "/account", "/cart", "/checkout", "/search")
    return ()

def priority(url: str) -> str:
    if "dummy-file-host.com" in url:
        return "high"
    path = urlparse(url).path.lower()
    host = urlparse(url).netloc.lower()
    if path in LOW_SIGNAL_EXACT_PATHS:
        return "low"
    deny_prefixes = get_commerce_deny_prefixes(host)
    if deny_prefixes and any(path.startswith(prefix) for prefix in deny_prefixes):
        return "low"
    allow_prefixes = get_commerce_allow_prefixes(host)
    if allow_prefixes and path not in ("", "/"):
        if not any(path.startswith(prefix) for prefix in allow_prefixes):
            return "low"
    if any(part in path for part in HIGH_SIGNAL_PATH_PARTS):
        return "high"
    if any(part in path for part in LOW_SIGNAL_PATH_PARTS):
        return "low"
    if path in ("", "/"):
        return "medium"
    return "medium"

def related_host(host: str, origin_host: str, keywords: list[str]) -> bool:
    host = host.lower()
    if host == origin_host.lower():
        return True
    if base_domain(host) == base_domain(origin_host):
        return True
    if any(k in host for k in keywords):
        return True
    return False

def category_for(url: str) -> str:
    if "dummy-file-host.com" in url:
        return "ir"
    host = urlparse(url).netloc.lower()
    if host in SOCIAL_HOSTS:
        return "social"
    if "jobkorea" in host or "recruiter" in host or "greenhouse" in host or "lever.co" in host:
        return "careers"
    if "investors." in host or "q4cdn" in host:
        return "ir"
    if any(k in host for k in TARGET_KEYWORDS):
        if "korea" in host or ".co.kr" in host:
            return "parent-corporate"
        return "brand-related"
    return "other"

def keep_in_inventory(url: str) -> bool:
    if is_noise(url):
        return False
    if is_attachment(url):
        return True
    signal = priority(url)
    if signal == "low":
        return False
    cat = category_for(url)
    if cat in {"parent-corporate", "b2b-portal", "careers", "ir"}:
        return True
    if cat in {"local-brand", "brand-related"}:
        path = urlparse(url).path.lower()
        return path in ("", "/") or path.startswith("/pages/") or path.startswith("/blogs/") or "/about" in path
    return signal == "high"

def keep_reason(url: str) -> str:
    path = urlparse(url).path.lower()
    cat = category_for(url)
    if is_attachment(url):
        return "공식 첨부 후보"
    if cat == "b2b-portal":
        return "B2B 주문/재고 포털"
    if cat == "careers":
        return "채용/조직 확장 시그널"
    if cat == "local-brand" or cat == "brand-related":
        if "/about" in path or "/our-company" in path:
            return "법인/브랜드 소개 정보"
        if "/pages/" in path or "/blogs/" in path:
            return "브랜드 컨텐츠 및 소개 표면"
        return "브랜드 관련 표면"
    if cat == "parent-corporate":
        return "모회사 고신호 표면"
    return "후속 검토 후보"

def include_in_keep_list(row: dict) -> bool:
    cat = row["category"]
    kind = row["kind"]
    signal = row["signal"]
    url = row["url"]
    path = urlparse(url).path.lower()
    if kind == "attachment":
        return True
    if cat == "b2b-portal" or cat == "careers":
        return True
    if cat in {"local-brand", "brand-related"}:
        return any(t in path for t in ("/about", "/our-company", "/pages/", "/blogs/"))
    if cat == "parent-corporate":
        if signal != "high":
            return False
        return any(token in path for token in ("/about", "/overview", "/network", "/investment", "/careers/", "/newsroom/", "/sustainability/"))
    return False

def keep_score(url: str, category: str) -> int:
    path = urlparse(url).path.lower()
    score = 0
    if is_attachment(url):
        score += 40
    if category == "b2b-portal":
        score += 35
    elif category == "local-brand":
        score += 30
    elif category == "brand-related":
        score += 24
    elif category == "careers":
        score += 18
    elif category == "parent-corporate":
        score += 12

    if any(token in path for token in ["/about-us/strategy", "/about-us/operations", "/about-us/history", "/about", "/overview", "/network"]):
        score += 10
    if any(token in path for token in ["/responsible-procurement", "/supply-chain-transparency", "major_finished_goods_suppliers", "modern-slavery", "transparency-act"]):
        score += 10
    if any(token in path for token in ["/our-company", "/about-us", "/about"]):
        score += 8
    if any(token in path for token in ["/careers/open-positions", "/open-positions"]):
        score += 8
    if any(k in path for k in TARGET_KEYWORDS):
        score += 6
    if "cookie-policy" in path or "privacy-policy" in path:
        score -= 20
    return score

def extract_urls(md_path: Path) -> list[str]:
    try:
        text = md_path.read_text(encoding="utf-8", errors="ignore")
        urls = [normalize(m.group(0).rstrip(".,:;")) for m in URL_RE.finditer(text)]
        js_download_re = re.compile(r"(?:fnDownload|downloadFile|fnDownloadFile|download_file)\((['\"])(.*?)\1\)")
        for m in js_download_re.finditer(text):
            enc_data = m.group(2)
            urls.append(f"https://dummy-file-host.com/download?encData={enc_data}.pdf")
        return list(dict.fromkeys(urls))
    except Exception:
        return []

# --- Attachment Downloader Logic ---
def filename_for(url: str) -> str:
    text = re.sub(r"[^A-Za-z0-9._-]+", "-", Path(urlparse(url).path).name or "attachment")
    return re.sub(r"-{2,}", "-", text).strip("-") or "attachment"

def download_attachments(tsv_path: Path, out_dir: Path, limit: int = 20, report_path: Path = None):
    out_dir.mkdir(parents=True, exist_ok=True)
    report_file = report_path or out_dir / "download-report.tsv"
    if not tsv_path.exists():
        print(f"Attachment candidate TSV {tsv_path} does not exist. Skipping.")
        return
    rows = list(csv.DictReader(tsv_path.open(encoding="utf-8"), delimiter="\t"))
    seen = set()
    count = 0
    report_rows = []
    
    for row in rows:
        if count >= limit:
            break
        url = row["url"]
        origin_url = row.get("origin_url", "")
        origin_host = row.get("origin_host", "") or row.get("host", "")
        if url in seen:
            continue
        seen.add(url)

        target_urls = []
        if "dummy-file-host.com" in url:
            match = re.search(r"encData=([^&]+)", url)
            if match:
                enc_data = match.group(1)
                if enc_data.endswith(".pdf"):
                    enc_data = enc_data[:-4]
                host = origin_host if origin_host else urlparse(url).netloc
                target_urls = [
                    f"https://{host}/investment/download.php?file={enc_data}",
                    f"https://{host}/common/download.php?file={enc_data}",
                    f"https://{host}/download.php?file={enc_data}",
                    f"https://{host}/api/common/files/download?encData={enc_data}",
                    f"https://{host}/download?encData={enc_data}",
                ]
        else:
            target_urls = [url]

        target = out_dir / filename_for(url)
        downloaded = False
        mime = ""
        for target_url in target_urls:
            cmd = ["curl", "-L", "-s", "-H", f"Referer: {origin_url}", target_url, "-o", str(target)]
            subprocess.run(cmd, check=False)
            if target.exists() and target.stat().st_size > 0:
                file_proc = subprocess.run(["file", "-I", str(target)], capture_output=True, text=True, check=False)
                if ": " in file_proc.stdout:
                    mime = file_proc.stdout.split(": ", 1)[1].strip()
                if any(mime.startswith(prefix) for prefix in ALLOWED_MIMES):
                    downloaded = True
                    break
                else:
                    target.unlink(missing_ok=True)
            else:
                target.unlink(missing_ok=True)
                
        status = "ok" if downloaded else "rejected"
        note = "" if downloaded else "failed to download valid mime"
        report_rows.append({"url": url, "saved_path": str(target) if downloaded else "", "status": status, "mime": mime, "note": note})
        count += 1
        print(f"Download {status}\t{mime}\t{url}\t{target if downloaded else 'NONE'}")

    with report_file.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["url", "saved_path", "status", "mime", "note"], delimiter="\t")
        w.writeheader()
        w.writerows(report_rows)

# --- Inventory Tables Writer ---
def write_tables(root: Path, manifest_rows, attachment_rows, link_inventory_rows):
    manifest_path = root / "crawl-manifest.tsv"
    attachment_path = root / "attachment-candidates.tsv"
    link_inventory_path = root / "link-inventory.tsv"
    keep_list_path = root / "keep-list-candidates.tsv"
    shortlist_path = root / "shortlist.tsv"

    with manifest_path.open("w", encoding="utf-8", newline="") as f:
        csv.DictWriter(f, fieldnames=["url", "hop", "origin_host", "status", "saved_path", "note"], delimiter="\t").writeheader()
        csv.DictWriter(f, fieldnames=["url", "hop", "origin_host", "status", "saved_path", "note"], delimiter="\t").writerows(manifest_rows)

    with attachment_path.open("w", encoding="utf-8", newline="") as f:
        csv.DictWriter(f, fieldnames=["url", "origin_url", "origin_host", "host", "priority"], delimiter="\t").writeheader()
        csv.DictWriter(f, fieldnames=["url", "origin_url", "origin_host", "host", "priority"], delimiter="\t").writerows(attachment_rows)

    seen_links = set()
    deduped_rows = []
    for row in link_inventory_rows:
        normalized = normalize(row["url"])
        row = {**row, "url": normalized, "host": urlparse(normalized).netloc.lower(), "signal": priority(normalized), "category": category_for(normalized)}
        if row["url"] not in seen_links:
            seen_links.add(row["url"])
            deduped_rows.append(row)

    with link_inventory_path.open("w", encoding="utf-8", newline="") as f:
        csv.DictWriter(f, fieldnames=["category", "kind", "signal", "host", "url", "source_page"], delimiter="\t").writeheader()
        csv.DictWriter(f, fieldnames=["category", "kind", "signal", "host", "url", "source_page"], delimiter="\t").writerows(deduped_rows)

    seen_keep = set()
    keep_rows = []
    all_urls = {row["url"] for row in deduped_rows}
    for row in deduped_rows:
        if not include_in_keep_list(row):
            continue
        url = row["url"]
        if url.endswith("/en_GB") and (url[:-5] + "ko_KR") in all_urls:
            continue
        if url not in seen_keep:
            seen_keep.add(url)
            keep_rows.append({"category": row["category"], "url": url, "reason": keep_reason(url)})

    scored_keep_rows = [{"score": keep_score(r["url"], r["category"]), **r} for r in keep_rows]
    scored_keep_rows.sort(key=lambda r: (-r["score"], r["category"], r["url"]))
    with keep_list_path.open("w", encoding="utf-8", newline="") as f:
        csv.DictWriter(f, fieldnames=["score", "category", "url", "reason"], delimiter="\t").writeheader()
        csv.DictWriter(f, fieldnames=["score", "category", "url", "reason"], delimiter="\t").writerows(scored_keep_rows)

    shortlist_rows = scored_keep_rows[:20]
    with shortlist_path.open("w", encoding="utf-8", newline="") as f:
        csv.DictWriter(f, fieldnames=["score", "category", "url", "reason"], delimiter="\t").writeheader()
        csv.DictWriter(f, fieldnames=["score", "category", "url", "reason"], delimiter="\t").writerows(shortlist_rows)

    return len(deduped_rows), len(scored_keep_rows)

# --- Feature A: Finance Chart Visualizer ---
def generate_finance_charts(market_data_path: Path):
    # Placeholder. Engagement-specific hardcoded financials were removed for public release.
    # Reimplement generically (parse figures from the market-data file) before use.
    print("Finance visualization not implemented in this build.")
    return

# --- Feature B: Export Risk Scanner ---
def scan_export_risk(market_data_path: Path, brief_path: Path):
    # Placeholder. Engagement-specific export-risk template was removed for public release.
    # Reimplement generically before use.
    print("Export risk scan not implemented in this build.")
    return

# --- Core Modes Execution ---
def crawl_mode(seeds, keywords, max_pages, max_hops, out_root, download=False, download_limit=20):
    pages_dir = out_root / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)
    
    queue = deque((normalize(u), 0, urlparse(normalize(u)).netloc.lower()) for u in seeds)
    seen_pages: set[str] = set()
    seen_attachments: set[str] = set()
    manifest_rows = []
    attachment_rows = []
    link_inventory_rows = []
    
    global TARGET_KEYWORDS
    TARGET_KEYWORDS = [k.lower() for k in keywords]

    while queue and len(seen_pages) < max_pages:
        url, hop, origin_host = queue.popleft()
        if url in seen_pages:
            continue
        seen_pages.add(url)
        out_file = pages_dir / path_slug(url)
        out_file.parent.mkdir(parents=True, exist_ok=True)
        
        cmd = [str(Path.home() / ".local/bin/crwl"), "crawl", url, "-o", "md-fit", "-O", str(out_file)]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        ok = proc.returncode == 0
        note = (proc.stderr or proc.stdout).strip()
        
        manifest_rows.append({
            "url": url, "hop": hop, "origin_host": origin_host,
            "status": "ok" if ok else "failed",
            "saved_path": str(out_file.relative_to(out_root)) if ok else "",
            "note": note[:500]
        })
        if not ok or not out_file.exists():
            continue

        for found in extract_urls(out_file):
            if keep_in_inventory(found):
                link_inventory_rows.append({
                    "category": category_for(found),
                    "kind": "attachment" if is_attachment(found) else "page",
                    "signal": priority(found),
                    "host": urlparse(found).netloc.lower(),
                    "url": found,
                    "source_page": str(out_file.relative_to(pages_dir))
                })
            if is_noise(found):
                continue
            host = urlparse(found).netloc.lower()
            if is_attachment(found):
                if found not in seen_attachments and related_host(host, origin_host, TARGET_KEYWORDS):
                    seen_attachments.add(found)
                    attachment_rows.append({"url": found, "origin_url": url, "origin_host": origin_host, "host": host, "priority": priority(found)})
                continue

            if hop >= max_hops:
                continue
            if not related_host(host, origin_host, TARGET_KEYWORDS):
                continue
            if priority(found) == "low":
                continue
            queue.append((found, hop + 1, origin_host))
            
        write_tables(out_root, manifest_rows, attachment_rows, link_inventory_rows)

    inv, keep = write_tables(out_root, manifest_rows, attachment_rows, link_inventory_rows)
    print(f"Crawl completed. pages: {len(manifest_rows)}, inventory: {inv}, keep_list: {keep}")
    
    if download:
        download_attachments(out_root / "attachment-candidates.tsv", out_root / "attachments", limit=download_limit)

def rebuild_mode(out_root, keywords):
    pages_dir = out_root / "pages"
    if not pages_dir.exists():
        print(f"Pages directory {pages_dir} does not exist.")
        return
        
    global TARGET_KEYWORDS
    TARGET_KEYWORDS = [k.lower() for k in keywords]
    manifest_rows = []
    attachment_rows = []
    link_inventory_rows = []

    for page in sorted(pages_dir.rglob("*.md")):
        rel = page.relative_to(out_root)
        manifest_rows.append({
            "url": "", "hop": "", "origin_host": "", "status": "ok",
            "saved_path": str(rel), "note": "rebuilt from existing page archive"
        })
        source_page = str(page.relative_to(pages_dir))
        for found in extract_urls(page):
            if keep_in_inventory(found):
                link_inventory_rows.append({
                    "category": category_for(found),
                    "kind": "attachment" if is_attachment(found) else "page",
                    "signal": priority(found),
                    "host": urlparse(found).netloc.lower(),
                    "url": found,
                    "source_page": source_page
                })
            if is_attachment(found):
                attachment_rows.append({"url": found, "origin_url": "", "origin_host": "", "host": urlparse(found).netloc.lower(), "priority": priority(found)})

    inv, keep = write_tables(out_root, manifest_rows, attachment_rows, link_inventory_rows)
    print(f"Rebuild completed. pages: {len(manifest_rows)}, inventory: {inv}, keep_list: {keep}")

def prune_mode(pages_dir_path: Path):
    removed = []
    for page in pages_dir_path.rglob("*.md"):
        posix = page.as_posix()
        if any(token in posix for token in PRUNE_SUBSTRINGS):
            removed.append(page)
    for page in removed:
        page.unlink(missing_ok=True)
        print(f"Pruned: {page}")
    print(f"Removed total: {len(removed)}")

def mirror_mode(tsv_path: Path, out_root: Path, limit: int = 20):
    if not tsv_path.exists():
        print(f"TSV {tsv_path} not found.")
        return
    rows = list(csv.DictReader(tsv_path.open(encoding="utf-8"), delimiter="\t"))
    out_root.mkdir(parents=True, exist_ok=True)
    urls = {row["url"] for row in rows}

    mirrored = 0
    for row in rows:
        if mirrored >= limit:
            break
        url = row["url"]
        if is_attachment(url):
            continue
        if url.endswith("/en_GB") and (url[:-5] + "ko_KR") in urls:
            continue
        dest = out_root / path_slug(url)
        dest.parent.mkdir(parents=True, exist_ok=True)
        cmd = [str(Path.home() / ".local/bin/crwl"), "crawl", url, "-o", "md-fit", "-O", str(dest)]
        subprocess.run(cmd, check=False)
        print(f"Mirrored {url} -> {dest}")
        mirrored += 1

def second_pass_mode(shortlist_path: Path, out_root: Path, categories, max_hosts, max_seeds_per_host, max_pages, max_hops, mirror_dir=None, attachments_dir=None, download_limit=10):
    if not shortlist_path.exists():
        print(f"Shortlist file {shortlist_path} not found.")
        return
    shortlist = list(csv.DictReader(shortlist_path.open(encoding="utf-8"), delimiter="\t"))
    buckets = defaultdict(list)
    for row in shortlist:
        if row["category"] not in set(categories):
            continue
        url = row["url"]
        host = urlparse(url).netloc.lower()
        if is_attachment(url):
            root_seed = f"https://{host}/"
            buckets[host].append({**row, "url": root_seed, "reason": row["reason"] + " -> host root", "_seed_type": "attachment-derived"})
        else:
            buckets[host].append({**row, "_seed_type": "page"})

    scored_hosts = []
    for host, rows in buckets.items():
        top_score = max(int(r.get("score", 0)) for r in rows)
        has_page_seed = any(r.get("_seed_type") == "page" for r in rows)
        scored_hosts.append((1 if has_page_seed else 0, top_score, host, rows))
    scored_hosts.sort(key=lambda x: (-x[0], -x[1], x[2]))
    
    selected_hosts = scored_hosts[:max_hosts]
    out_root.mkdir(parents=True, exist_ok=True)
    
    for _, _, host, rows in selected_hosts:
        seeds = [row["url"] for row in rows[:max_seeds_per_host]]
        host_dir = out_root / host.replace("/", "_")
        print(f"Running second-pass for host {host} with seeds: {seeds}")
        
        # Calculate keywords based on host parts
        keywords = [p for p in host.replace("-", ".").split(".") if p and p not in {"www", "com", "co", "kr", "net", "org"}]
        crawl_mode(seeds, keywords, max_pages, max_hops, host_dir, download=(attachments_dir is not None), download_limit=download_limit)
        
        if mirror_dir:
            mirror_mode(host_dir / "shortlist.tsv", Path(mirror_dir))

# --- Feature C: Report Merger & Workspace Cleaner ---
def merge_report_mode(workspace: Path):
    print(f"Starting merge-report mode for workspace: {workspace}")
    
    # Ordered markdown files for unified business narrative
    ordered_files = [
        ("00-target.md", "## 1. Target Profile"),
        ("00-surface-map.md", "## 2. Surface Map"),
        ("05-company-brief.md", "## 3. Executive Brief & Deal Context"),
        ("03-market-data.md", "## 4. Market & Financial Data"),
        ("01-public-web.md", "## 5. Public Web Insights"),
        ("02-public-press.md", "## 6. Press & Public Timeline"),
        ("04-internal-context.md", "## 7. Internal Context & Stakeholders")
    ]
    
    merged_lines = []
    # Title
    corp_name = workspace.name.split("-")[-1].replace("_", " ").title()
    merged_lines.append(f"# Company Research Master Brief - {corp_name}")
    merged_lines.append("")
    merged_lines.append("## Table of Contents")
    for _, title in ordered_files:
        anchor = title.lower().replace(".", "").replace(" ", "-").replace("&", "").replace("(", "").replace(")", "")
        merged_lines.append(f"- [{title[3:]}](#{anchor})")
    merged_lines.append("")
    merged_lines.append("---")
    merged_lines.append("")
    
    found_any = False
    for filename, title in ordered_files:
        filepath = workspace / filename
        if not filepath.exists():
            print(f"Warning: {filename} not found in workspace. Skipping section.")
            continue
        found_any = True
        merged_lines.append(title)
        merged_lines.append("")
        
        # Read content and adjust headers
        content = filepath.read_text(encoding="utf-8")
        adjusted_lines = []
        for line in content.splitlines():
            # Skip the main title of each sub-file
            if line.startswith("# ") and not line.startswith("## "):
                continue
            # Demote headers to fit hierarchy
            if line.startswith("###### "):
                line = "###### " + line[7:]
            elif line.startswith("##### "):
                line = "###### " + line[6:]
            elif line.startswith("#### "):
                line = "##### " + line[5:]
            elif line.startswith("### "):
                line = "#### " + line[4:]
            elif line.startswith("## "):
                line = "### " + line[3:]
            adjusted_lines.append(line)
            
        merged_lines.extend(adjusted_lines)
        merged_lines.append("")
        merged_lines.append("---")
        merged_lines.append("")
        
    if not found_any:
        print("Error: No markdown files found to merge.")
        return
        
    if merged_lines and merged_lines[-2] == "---":
        merged_lines = merged_lines[:-3]
        
    output_brief_path = workspace / "company-research-brief.md"
    output_brief_path.write_text("\n".join(merged_lines) + "\n", encoding="utf-8")
    print(f"Master brief generated successfully at: {output_brief_path}")
    
    # Delete original sub-files safely
    for filename, _ in ordered_files:
        filepath = workspace / filename
        filepath.unlink(missing_ok=True)
        print(f"Deleted sub-file: {filename}")
        
    # Rename/move directories into .research-cache hidden directory
    cache_dir = workspace / ".research-cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    import shutil
    # Move recursive-crawl
    crawl_dir = workspace / "recursive-crawl"
    if crawl_dir.exists():
        target_crawl = cache_dir / "recursive-crawl"
        if target_crawl.exists():
            shutil.rmtree(target_crawl)
        shutil.move(str(crawl_dir), str(cache_dir))
        print("Moved 'recursive-crawl' to hidden cache '.research-cache/recursive-crawl'")
        
    # Move press
    press_dir = workspace / "press"
    if press_dir.exists():
        target_press = cache_dir / "press"
        if target_press.exists():
            shutil.rmtree(target_press)
        shutil.move(str(press_dir), str(cache_dir))
        print("Moved 'press' to hidden cache '.research-cache/press'")
        
    # Move public-mirror
    mirror_dir = workspace / "public-mirror"
    if mirror_dir.exists():
        target_mirror = cache_dir / "public-mirror"
        if target_mirror.exists():
            shutil.rmtree(target_mirror)
        shutil.move(str(mirror_dir), str(cache_dir))
        print("Moved 'public-mirror' to hidden cache '.research-cache/public-mirror'")

# --- Main CLI ---
def main():
    ap = argparse.ArgumentParser(description="Unified Research Crawler CLI")
    ap.add_argument("--mode", required=True, choices=["crawl", "rebuild", "prune", "mirror", "second-pass", "visualize", "scan-risk", "merge-report"])
    ap.add_argument("seeds_or_dir", nargs="*", help="Seed URLs or directory paths depending on the mode")
    ap.add_argument("--keyword", action="append", default=[], help="Keywords for matching hosts")
    ap.add_argument("--max-pages", type=int, default=40)
    ap.add_argument("--max-hops", type=int, default=2)
    ap.add_argument("--out", help="Output directory path")
    ap.add_argument("--download", action="store_true", help="Auto-download attachments after crawl")
    ap.add_argument("--download-limit", type=int, default=20)
    ap.add_argument("--limit", type=int, default=20, help="Limit for mirror or download modes")
    ap.add_argument("--category", action="append", default=["brand-related"], help="Categories for second-pass")
    
    # Paths for analysis helper
    ap.add_argument("--market-data-path", help="Path to 03-market-data.md for visualization/scanning")
    ap.add_argument("--brief-path", help="Path to 05-company-brief.md for risk warning injection")
    args = ap.parse_args()

    if args.mode == "crawl":
        if not args.out:
            print("Error: --out is required in crawl mode.")
            sys.exit(1)
        if not args.seeds_or_dir:
            print("Error: seed URLs required in crawl mode.")
            sys.exit(1)
        crawl_mode(args.seeds_or_dir, args.keyword, args.max_pages, args.max_hops, Path(args.out), download=args.download, download_limit=args.download_limit)
        
    elif args.mode == "rebuild":
        if not args.out:
            print("Error: --out is required in rebuild mode.")
            sys.exit(1)
        rebuild_mode(Path(args.out), args.keyword)
        
    elif args.mode == "prune":
        if not args.seeds_or_dir:
            print("Error: pages directory required in prune mode.")
            sys.exit(1)
        prune_mode(Path(args.seeds_or_dir[0]))
        
    elif args.mode == "mirror":
        if not args.out:
            print("Error: --out is required in mirror mode.")
            sys.exit(1)
        if not args.seeds_or_dir:
            print("Error: shortlist TSV path required in mirror mode.")
            sys.exit(1)
        mirror_mode(Path(args.seeds_or_dir[0]), Path(args.out), limit=args.limit)
        
    elif args.mode == "second-pass":
        if not args.out:
            print("Error: --out is required in second-pass mode.")
            sys.exit(1)
        if not args.seeds_or_dir:
            print("Error: shortlist.tsv path required in second-pass mode.")
            sys.exit(1)
        second_pass_mode(Path(args.seeds_or_dir[0]), Path(args.out), args.category, max_hosts=3, max_seeds_per_host=3, max_pages=15, max_hops=1, attachments_dir=args.out if args.download else None, download_limit=args.download_limit)
        
    elif args.mode == "visualize":
        path = Path(args.market_data_path) if args.market_data_path else Path("./03-market-data.md")
        generate_finance_charts(path)
        
    elif args.mode == "scan-risk":
        m_path = Path(args.market_data_path) if args.market_data_path else Path("./03-market-data.md")
        b_path = Path(args.brief_path) if args.brief_path else Path("./05-company-brief.md")
        scan_export_risk(m_path, b_path)
        
    elif args.mode == "merge-report":
        workspace_dir = Path(args.out) if args.out else Path(".")
        merge_report_mode(workspace_dir)

if __name__ == "__main__":
    main()
