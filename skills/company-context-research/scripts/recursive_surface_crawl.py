#!/usr/bin/env python3
import argparse
import csv
import re
import subprocess
from collections import deque
from pathlib import Path
from urllib.parse import urlparse, urlunparse


URL_RE = re.compile(r"https?://[^\s\)\]>'\"]+")
ATTACHMENT_EXTS = (".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx", ".csv")
NOISE_EXTS = (".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp", ".css", ".js", ".woff", ".woff2")
SOCIAL_HOSTS = {
    "linkedin.com",
    "www.linkedin.com",
    "instagram.com",
    "www.instagram.com",
    "youtube.com",
    "www.youtube.com",
    "facebook.com",
    "www.facebook.com",
    "x.com",
    "twitter.com",
    "www.x.com",
    "www.twitter.com",
}
LOW_SIGNAL_PATH_PARTS = (
    "/products/",
    "/product/",
    "/collections/",
    "/cart",
    "/checkout",
    "/account",
    "/search",
    "/cdn/",
    "/membership",
)
HIGH_SIGNAL_PATH_PARTS = (
    "/about",
    "/strategy",
    "/history",
    "/purpose",
    "/values",
    "/operations",
    "/newsroom",
    "/news",
    "/press",
    "/media",
    "/report",
    "/reports",
    "/sustainability",
    "/investor",
    "/careers",
    "/career",
    "/contact",
    "/contacts",
    "/pages/",
    "/blogs/",
    "/who-we-are",
    "/innovation",
)
LOW_SIGNAL_EXACT_PATHS = {
    "/cookie-policy/",
    "/privacy-policy/",
    "/site-terms/",
    "/accessibility-statement/",
    "/about-us/strate",
    "/newsroom/__trashed/",
}
COMMERCE_HOST_ALLOW_PREFIXES = {
    "salomon.co.kr": ("/pages/", "/blogs/"),
    "kr.wilson.com": ("/pages/", "/blogs/"),
    "www.wilson.com": ("/pages/", "/blogs/"),
}
COMMERCE_HOST_DENY_PREFIXES = {
    "salomon.co.kr": ("/collections/", "/products/", "/account", "/cart", "/checkout", "/search"),
    "kr.wilson.com": ("/collections/", "/products/", "/account", "/cart", "/checkout", "/search"),
    "www.wilson.com": ("/collections/", "/products/", "/account", "/cart", "/checkout", "/search"),
}


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
    host = p.netloc.lower()
    if host in SOCIAL_HOSTS:
        return True
    return False


def is_attachment(url: str) -> bool:
    return urlparse(url).path.lower().endswith(ATTACHMENT_EXTS)


def priority(url: str) -> str:
    path = urlparse(url).path.lower()
    host = urlparse(url).netloc.lower()
    if path in LOW_SIGNAL_EXACT_PATHS:
        return "low"
    if host in COMMERCE_HOST_DENY_PREFIXES and any(path.startswith(prefix) for prefix in COMMERCE_HOST_DENY_PREFIXES[host]):
        return "low"
    if host in COMMERCE_HOST_ALLOW_PREFIXES and path not in ("", "/"):
        if not any(path.startswith(prefix) for prefix in COMMERCE_HOST_ALLOW_PREFIXES[host]):
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
    host = urlparse(url).netloc.lower()
    if host in SOCIAL_HOSTS:
        return "social"
    if "jobkorea" in host or "recruiter" in host or "greenhouse" in host or "lever.co" in host:
        return "careers"
    if "investors." in host or "q4cdn" in host:
        return "ir"
    if "sales.amersports.com" in host:
        return "b2b-portal"
    if "salomon.co.kr" in host:
        return "local-brand"
    if "amersports.com" in host:
        return "parent-corporate"
    if any(x in host for x in ["wilson.com", "atomic.com", "arcteryx.com", "peakperformance.com", "armada.com"]):
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
    host = urlparse(url).netloc.lower()
    cat = category_for(url)
    if cat in {"parent-corporate", "b2b-portal", "careers", "ir"}:
        return True
    if cat == "local-brand":
        path = urlparse(url).path.lower()
        return path in ("", "/") or path.startswith("/pages/") or path.startswith("/blogs/")
    if cat == "brand-related":
        path = urlparse(url).path.lower()
        return path in ("", "/") or path.startswith("/pages/") or path.startswith("/blogs/") or "/our-company" in path
    return signal == "high"


def keep_reason(url: str) -> str:
    host = urlparse(url).netloc.lower()
    path = urlparse(url).path.lower()
    cat = category_for(url)
    if is_attachment(url):
        if "sustainability_report" in path or "sustainability-report" in path:
            return "핵심 지속가능성 보고서"
        if "supplier" in path or "suppliers" in path:
            return "공급망/제조 파트너 구조"
        if "modern-slavery" in path or "human-trafficking" in path:
            return "인권/조달 가드레일"
        if "transparency" in path:
            return "법규 대응 투명성"
        if "impact-statement" in path:
            return "브랜드 연관 도메인에서 파생된 공식 PDF"
        return "공식 첨부 후보"
    if cat == "b2b-portal":
        return "B2B 주문/재고 포털"
    if cat == "careers":
        return "채용/조직 확장 시그널"
    if cat == "local-brand":
        if "/about-us" in path or "/our-company" in path:
            return "한국 법인 정보 확인"
        if "/pages/" in path:
            return "브랜드 소개/운영 표면"
        return "로컬 브랜드 표면"
    if cat == "brand-related":
        if "/our-company" in path:
            return "연관 브랜드 법인/브랜드 소개"
        if "/blogs/" in path or "/pages/blogs" in path:
            return "연관 브랜드 컨텐츠 표면"
        return "연관 브랜드 표면"
    if cat == "parent-corporate":
        if "/about-us/strategy" in path:
            return "그룹 전략"
        if "/about-us/operations" in path:
            return "운영/공급망 관련 전략"
        if "/about-us/history" in path:
            return "브랜드 편입 이력과 상장 이력"
        if "/about-us" in path:
            return "글로벌 모회사 규모와 포트폴리오"
        if "/careers/" in path:
            return "글로벌 채용/조직 확장 시그널"
        if "/newsroom/" in path:
            return "브랜드/운영 관련 공식 발표"
        if "/sustainability/" in path:
            return "지속가능성/공급망 관련 표면"
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
    if cat == "b2b-portal":
        return True
    if cat == "local-brand":
        return "/about-us" in path or "/our-company" in path
    if cat == "brand-related":
        return "/our-company" in path or "/pages/blogs" in path or "/blogs/" in path
    if cat == "careers":
        return True
    if cat == "parent-corporate":
        if signal != "high":
            return False
        return any(
            token in path
            for token in (
                "/about-us/",
                "/about-us",
                "/careers/",
                "/newsroom/",
                "/sustainability/",
            )
        )
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

    if any(token in path for token in ["/about-us/strategy", "/about-us/operations", "/about-us/history"]):
        score += 10
    if any(token in path for token in ["/responsible-procurement", "/supply-chain-transparency", "major_finished_goods_suppliers", "modern-slavery", "transparency-act"]):
        score += 10
    if any(token in path for token in ["/our-company", "/about-us"]):
        score += 8
    if any(token in path for token in ["/careers/open-positions", "/open-positions"]):
        score += 8
    if any(token in path for token in ["salomon", "wilson", "atomic"]):
        score += 6
    if any(token in path for token in ["retail", "supply-chain", "warehouse", "factory", "binding"]):
        score += 5
    if "cookie-policy" in path or "privacy-policy" in path:
        score -= 20
    return score


def dedupe_link_rows(rows: list[dict]) -> list[dict]:
    deduped_rows = []
    seen_links = set()
    for row in rows:
        normalized = normalize(row["url"])
        row = {**row, "url": normalized, "host": urlparse(normalized).netloc.lower(), "signal": priority(normalized), "category": category_for(normalized)}
        key = row["url"]
        if key in seen_links:
            continue
        seen_links.add(key)
        deduped_rows.append(row)
    return deduped_rows


def build_keep_rows(deduped_rows: list[dict]) -> list[dict]:
    keep_rows = []
    seen_keep = set()
    all_urls = {row["url"] for row in deduped_rows}
    for row in deduped_rows:
        if not include_in_keep_list(row):
            continue
        url = row["url"]
        if url.endswith("/en_GB"):
            ko = url[:-5] + "ko_KR"
            if ko in all_urls:
                continue
        if url in seen_keep:
            continue
        seen_keep.add(url)
        keep_rows.append(
            {
                "category": row["category"],
                "url": url,
                "reason": keep_reason(url),
            }
        )
    return keep_rows


def write_tables(
    manifest_path: Path,
    attachment_path: Path,
    link_inventory_path: Path,
    keep_list_path: Path,
    shortlist_path: Path,
    manifest_rows: list[dict],
    attachment_rows: list[dict],
    link_inventory_rows: list[dict],
) -> tuple[int, int]:
    with manifest_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["url", "hop", "origin_host", "status", "saved_path", "note"],
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(manifest_rows)

    with attachment_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["url", "origin_url", "origin_host", "host", "priority"],
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(attachment_rows)

    deduped_rows = dedupe_link_rows(link_inventory_rows)
    with link_inventory_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["category", "kind", "signal", "host", "url", "source_page"],
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(deduped_rows)

    keep_rows = build_keep_rows(deduped_rows)
    scored_keep_rows = []
    for row in keep_rows:
        scored_keep_rows.append(
            {
                "score": keep_score(row["url"], row["category"]),
                **row,
            }
        )
    scored_keep_rows.sort(key=lambda r: (-r["score"], r["category"], r["url"]))
    with keep_list_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["score", "category", "url", "reason"],
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(scored_keep_rows)

    shortlist_rows = scored_keep_rows[:20]
    with shortlist_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["score", "category", "url", "reason"],
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(shortlist_rows)

    return len(deduped_rows), len(scored_keep_rows)


def crawl_page(url: str, out_file: Path) -> tuple[bool, str]:
    out_file.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        str(Path.home() / ".local/bin/crwl"),
        "crawl",
        url,
        "-o",
        "md-fit",
        "-O",
        str(out_file),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc.returncode == 0, (proc.stderr or proc.stdout).strip()


def extract_urls(md_path: Path) -> list[str]:
    text = md_path.read_text(encoding="utf-8", errors="ignore")
    urls = [normalize(m.group(0).rstrip(".,:;")) for m in URL_RE.finditer(text)]
    return list(dict.fromkeys(urls))


def main() -> None:
    ap = argparse.ArgumentParser(description="Recursive cross-domain surface crawler")
    ap.add_argument("seed", nargs="+", help="Seed URLs")
    ap.add_argument("--keyword", action="append", default=[], help="Host matching keyword")
    ap.add_argument("--max-hops", type=int, default=2)
    ap.add_argument("--max-pages", type=int, default=40)
    ap.add_argument("--out", required=True, help="Output directory")
    args = ap.parse_args()

    out_root = Path(args.out)
    pages_dir = out_root / "pages"
    manifest_path = out_root / "crawl-manifest.tsv"
    attachment_path = out_root / "attachment-candidates.tsv"
    link_inventory_path = out_root / "link-inventory.tsv"
    keep_list_path = out_root / "keep-list-candidates.tsv"
    shortlist_path = out_root / "shortlist.tsv"
    pages_dir.mkdir(parents=True, exist_ok=True)

    queue = deque((normalize(u), 0, urlparse(normalize(u)).netloc.lower()) for u in args.seed)
    seen_pages: set[str] = set()
    seen_attachments: set[str] = set()
    manifest_rows = []
    attachment_rows = []
    link_inventory_rows = []

    keywords = [k.lower() for k in args.keyword]

    while queue and len(seen_pages) < args.max_pages:
        url, hop, origin_host = queue.popleft()
        if url in seen_pages:
            continue
        seen_pages.add(url)
        out_file = pages_dir / path_slug(url)
        ok, note = crawl_page(url, out_file)
        manifest_rows.append(
            {
                "url": url,
                "hop": hop,
                "origin_host": origin_host,
                "status": "ok" if ok else "failed",
                "saved_path": str(out_file.relative_to(out_root)) if ok else "",
                "note": note[:500],
            }
        )
        if not ok or not out_file.exists():
            continue

        for found in extract_urls(out_file):
            if keep_in_inventory(found):
                link_inventory_rows.append(
                    {
                        "category": category_for(found),
                        "kind": "attachment" if is_attachment(found) else "page",
                        "signal": priority(found),
                        "host": urlparse(found).netloc.lower(),
                        "url": found,
                        "source_page": str(out_file.relative_to(pages_dir)),
                    }
                )
            if is_noise(found):
                continue
            host = urlparse(found).netloc.lower()
            if is_attachment(found):
                if found not in seen_attachments and related_host(host, origin_host, keywords):
                    seen_attachments.add(found)
                    attachment_rows.append(
                        {
                            "url": found,
                            "origin_url": url,
                            "origin_host": origin_host,
                            "host": host,
                            "priority": priority(found),
                        }
                    )
                continue

            if hop >= args.max_hops:
                continue
            if not related_host(host, origin_host, keywords):
                continue
            if priority(found) == "low":
                continue
            queue.append((found, hop + 1, origin_host))
        inventory_count, keep_count = write_tables(
            manifest_path,
            attachment_path,
            link_inventory_path,
            keep_list_path,
            shortlist_path,
            manifest_rows,
            attachment_rows,
            link_inventory_rows,
        )

    inventory_count, keep_count = write_tables(
        manifest_path,
        attachment_path,
        link_inventory_path,
        keep_list_path,
        shortlist_path,
        manifest_rows,
        attachment_rows,
        link_inventory_rows,
    )
    print(f"pages: {len(manifest_rows)}")
    print(f"attachments: {len(attachment_rows)}")
    print(f"inventory: {inventory_count}")
    print(f"keep_list: {keep_count}")
    print(f"out: {out_root}")


if __name__ == "__main__":
    main()
