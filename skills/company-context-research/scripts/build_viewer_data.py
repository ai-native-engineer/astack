#!/usr/bin/env python3
"""Build the single JSON payload consumed by index.html."""

from __future__ import annotations

import argparse
import csv
import json
import tempfile
import shutil
from datetime import date
from pathlib import Path


MANIFEST_HEADERS = ["source_type", "url_or_path", "title", "saved_path", "date_collected", "note"]

STANDARD_TABLES = {
    "financials": "official-data/dart/financial-summary.tsv",
    "searchTrends": "official-data/naver-datalab/search-trends.tsv",
    "employeeTrends": "official-data/data-go-kr/nps-workplace/headcount.tsv",
    "businessStatusRows": "official-data/data-go-kr/nts-business-status/business-status.tsv",
    "procurementRows": "official-data/data-go-kr/procurement/procurement-search.tsv",
    "supportProgramRows": "official-data/data-go-kr/support-programs/support-program-search.tsv",
    "pressRows": "press/press-inventory.tsv",
}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=MANIFEST_HEADERS, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def upsert_viewer_manifest(root: Path) -> list[dict[str, str]]:
    path = root / "source-manifest.tsv"
    rows = read_tsv(path)
    row = {
        "source_type": "data",
        "url_or_path": "data/viewer-data.json",
        "title": "Viewer data bundle",
        "saved_path": "data/viewer-data.json",
        "date_collected": date.today().isoformat(),
        "note": "Single JSON payload consumed by index.html",
    }
    for idx, existing in enumerate(rows):
        if existing.get("saved_path") == "data/viewer-data.json":
            rows[idx] = {**existing, **row}
            break
    else:
        rows.append(row)
    write_tsv(path, rows)
    return rows


def sync_viewer_template(root: Path) -> None:
    template = Path(__file__).resolve().parents[1] / "templates/company-viewer.html"
    if template.exists():
        shutil.copyfile(template, root / "index.html")


def build(root: Path) -> Path:
    root = root.resolve()
    sync_viewer_template(root)
    profile = read_json(root / "data/company-profile.json")
    status = read_json(root / "data/research-status.json")
    manifest = upsert_viewer_manifest(root)
    payload = {
        "schema_version": "company-context-viewer-v1",
        "generated_at": date.today().isoformat(),
        "profile": profile,
        "status": status,
        "manifest": manifest,
    }
    for key, rel in STANDARD_TABLES.items():
        payload[key] = read_tsv(root / rel)
    out = root / "data/viewer-data.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return out


def self_test() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "data").mkdir()
        (root / "official-data/dart").mkdir(parents=True)
        (root / "press").mkdir()
        (root / "data/company-profile.json").write_text('{"schema_version":"company-context-web-v1"}', encoding="utf-8")
        (root / "data/research-status.json").write_text('{"schema_version":"company-context-status-v1"}', encoding="utf-8")
        write_tsv(root / "source-manifest.tsv", [])
        (root / "official-data/dart/financial-summary.tsv").write_text("year\trevenue_krw\n2026\t1\n", encoding="utf-8")
        (root / "official-data/naver-datalab").mkdir(parents=True)
        (root / "official-data/naver-datalab/search-trends.tsv").write_text("group\tperiod\tratio\nx\t2026-01-01\t1\n", encoding="utf-8")
        (root / "official-data/data-go-kr/nps-workplace").mkdir(parents=True)
        (root / "official-data/data-go-kr/nps-workplace/headcount.tsv").write_text("dataCrtYm\tjnngpCnt\n202601\t10\n", encoding="utf-8")
        (root / "press/press-inventory.tsv").write_text("source\tdate\toutlet\ttitle\turl\tdecoded\tqueries\nnaver\t2026-01-01\tx\tt\thttps://x\t-\tq\n", encoding="utf-8")
        out = build(root)
        data = read_json(out)
        assert (root / "index.html").exists()
        assert data["schema_version"] == "company-context-viewer-v1"
        assert len(data["financials"]) == 1
        assert len(data["searchTrends"]) == 1
        assert len(data["employeeTrends"]) == 1
        assert len(data["pressRows"]) == 1
        assert any(row["saved_path"] == "data/viewer-data.json" for row in read_tsv(root / "source-manifest.tsv"))
    print("self-test ok")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("workspace", nargs="?", help="company-context workspace path")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        self_test()
        return 0
    if not args.workspace:
        ap.error("workspace is required unless --self-test is used")
    print(build(Path(args.workspace)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
