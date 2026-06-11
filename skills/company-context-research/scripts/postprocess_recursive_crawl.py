#!/usr/bin/env python3
import argparse
from pathlib import Path
from urllib.parse import urlparse

from recursive_surface_crawl import (
    category_for,
    extract_urls,
    include_in_keep_list,
    is_attachment,
    keep_reason,
    keep_in_inventory,
    priority,
    write_tables,
)


def main() -> None:
    ap = argparse.ArgumentParser(description="Rebuild recursive crawl inventories from saved pages/")
    ap.add_argument("root", help="recursive-crawl directory")
    args = ap.parse_args()

    root = Path(args.root)
    pages_dir = root / "pages"
    manifest_path = root / "crawl-manifest.tsv"
    attachment_path = root / "attachment-candidates.tsv"
    link_inventory_path = root / "link-inventory.tsv"
    keep_list_path = root / "keep-list-candidates.tsv"
    shortlist_path = root / "shortlist.tsv"

    manifest_rows = []
    attachment_rows = []
    link_inventory_rows = []

    for page in sorted(pages_dir.rglob("*.md")):
        rel = page.relative_to(root)
        manifest_rows.append(
            {
                "url": "",
                "hop": "",
                "origin_host": "",
                "status": "ok",
                "saved_path": str(rel),
                "note": "rebuilt from existing page archive",
            }
        )
        source_page = str(page.relative_to(pages_dir))
        for found in extract_urls(page):
            if keep_in_inventory(found):
                link_inventory_rows.append(
                    {
                        "category": category_for(found),
                        "kind": "attachment" if is_attachment(found) else "page",
                        "signal": priority(found),
                        "host": urlparse(found).netloc.lower(),
                        "url": found,
                        "source_page": source_page,
                    }
                )
            if is_attachment(found):
                attachment_rows.append(
                    {
                        "url": found,
                        "origin_url": "",
                        "origin_host": "",
                        "host": urlparse(found).netloc.lower(),
                        "priority": priority(found),
                    }
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
    print(f"out: {root}")


if __name__ == "__main__":
    main()
