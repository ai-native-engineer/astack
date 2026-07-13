#!/usr/bin/env python3
"""Validate a company-context web package before handoff."""

from __future__ import annotations

import argparse
import csv
import json
import tempfile
from pathlib import Path


REQUIRED_STEPS = {
    "surface_map",
    "public_web_crawl",
    "press_collection",
    "market_data",
    "internal_context",
    "data_profile",
    "source_integrity",
    "viewer_ready",
}
REQUIRED_SECTIONS = {
    "overview",
    "growth",
    "traffic_consumer",
    "research_ip",
    "funding",
    "organization_finance",
    "news",
    "internal_context",
}
REQUIRED_TSV_HEADERS = {
    "source-manifest.tsv": ["source_type", "url_or_path", "title", "saved_path", "date_collected", "note"],
    "press/press-inventory.tsv": ["source", "date", "outlet", "title", "url", "decoded", "queries"],
    "recursive-crawl/crawl-manifest.tsv": ["url", "hop", "origin_host", "status", "saved_path", "note"],
    "recursive-crawl/link-inventory.tsv": ["category", "kind", "signal", "host", "url", "source_page"],
    "recursive-crawl/attachment-candidates.tsv": ["url", "origin_url", "origin_host", "host", "priority"],
    "recursive-crawl/download-report.tsv": ["url", "saved_path", "status", "mime", "note"],
    "recursive-crawl/keep-list-candidates.tsv": ["score", "category", "url", "reason"],
    "recursive-crawl/shortlist.tsv": ["score", "category", "url", "reason"],
}
VIEWER_ARRAY_KEYS = [
    "manifest",
    "financials",
    "searchTrends",
    "employeeTrends",
    "businessStatusRows",
    "procurementRows",
    "supportProgramRows",
    "pressRows",
]
VIEWER_MARKERS = [
    "https://esm.sh/react",
    "recharts",
    "d3-cloud",
    "@tanstack/react-table",
    "data/viewer-data.json",
    "기업개요",
    "종합성장분석",
    "방문자/소비자",
    "연구/특허",
    "투자유치",
    "조직/재무",
    "기업뉴스",
]
AUTH_PARAM_MARKERS = ("accessKey=", "serviceKey=", "crtfc_key=", "clientSecret=", "client_secret=")
AUTH_SCAN_SUFFIXES = {".csv", ".html", ".json", ".md", ".tsv", ".txt"}


def read_json(path: Path, errors: list[str]):
    if not path.exists():
        errors.append(f"missing file: {path}")
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"invalid json: {path}: {exc}")
        return {}


def is_blank(value) -> bool:
    return value is None or (isinstance(value, str) and not value.strip())


def validate_tsv(root: Path, rel: str, headers: list[str], errors: list[str]) -> list[dict[str, str]]:
    path = root / rel
    if not path.exists():
        errors.append(f"missing file: {rel}")
        return []
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        if reader.fieldnames != headers:
            errors.append(f"bad header: {rel}: {reader.fieldnames} != {headers}")
            return []
        return list(reader)


def validate_manifest_paths(root: Path, rows: list[dict[str, str]], errors: list[str]) -> None:
    if not rows:
        errors.append("source-manifest.tsv has no source rows")
        return
    for idx, row in enumerate(rows, start=2):
        saved_path = (row.get("saved_path") or "").strip()
        if not saved_path or saved_path == "-":
            errors.append(f"source-manifest.tsv:{idx} saved_path is blank")
            continue
        path = Path(saved_path)
        if not path.is_absolute():
            path = root / path
        if not path.exists():
            errors.append(f"source-manifest.tsv:{idx} saved_path not found: {saved_path}")


def tsv_row_count(root: Path, rel: str) -> int:
    path = root / rel
    if not path.exists():
        return 0
    with path.open(encoding="utf-8", newline="") as f:
        return sum(1 for _ in csv.DictReader(f, delimiter="\t"))


def validate_status_semantics(root: Path, step_by_id: dict[str, dict], errors: list[str]) -> None:
    blocked_words = ("보류", "미수집", "not collected", "partial")
    for step_id, step in step_by_id.items():
        if step.get("status") == "done":
            notes = (step.get("notes") or "").lower()
            if any(word in notes for word in blocked_words):
                errors.append(f"status step {step_id} is done but notes describe incomplete work")

    crawl = step_by_id.get("public_web_crawl") or {}
    if crawl.get("status") == "done":
        discovered = tsv_row_count(root, "recursive-crawl/link-inventory.tsv")
        shortlisted = tsv_row_count(root, "recursive-crawl/shortlist.tsv")
        if discovered == 0 and shortlisted == 0:
            errors.append("public_web_crawl is done but link-inventory.tsv and shortlist.tsv have no rows")

    market = step_by_id.get("market_data") or {}
    if market.get("status") == "done":
        optional = {
            "Naver DataLab": "official-data/naver-datalab/search-trends.tsv",
            "procurement": "official-data/data-go-kr/procurement/procurement-search.tsv",
            "support programs": "official-data/data-go-kr/support-programs/support-program-search.tsv",
            "NTIS": "official-data/ntis/projects.tsv",
        }
        missing = [name for name, rel in optional.items() if tsv_row_count(root, rel) == 0]
        if missing:
            errors.append(f"market_data is done but optional market sources are empty or missing: {', '.join(missing)}")


def validate_viewer_html(root: Path, errors: list[str]) -> None:
    path = root / "index.html"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8", errors="replace")
    for marker in VIEWER_MARKERS:
        if marker not in text:
            errors.append(f"index.html missing viewer marker: {marker}")
    forbidden_fetches = [
        'fetch("./data/company-profile.json"',
        "fetch('./data/company-profile.json'",
        'fetch("./press/press-inventory.tsv"',
        "fetch('./press/press-inventory.tsv'",
        'fetch("./official-data/',
        "fetch('./official-data/",
    ]
    for marker in forbidden_fetches:
        if marker in text:
            errors.append(f"index.html must fetch data/viewer-data.json only, found: {marker}")


def is_raw_layer(root: Path, path: Path) -> bool:
    try:
        return "raw" in path.relative_to(root).parts
    except ValueError:
        return False


def validate_no_auth_params(root: Path, errors: list[str]) -> None:
    candidates = [
        root / "index.html",
        root / "source-manifest.tsv",
        root / "data/company-profile.json",
        root / "data/viewer-data.json",
        root / "data/research-status.json",
    ]
    official_data = root / "official-data"
    if official_data.exists():
        candidates.extend(
            path for path in official_data.rglob("*")
            if path.is_file() and path.suffix.lower() in AUTH_SCAN_SUFFIXES and not is_raw_layer(root, path)
        )
    seen: set[Path] = set()
    for path in candidates:
        if path in seen or not path.exists() or path.is_dir():
            continue
        seen.add(path)
        text = path.read_text(encoding="utf-8", errors="replace")
        marker = next((item for item in AUTH_PARAM_MARKERS if item in text), "")
        if marker:
            errors.append(f"auth parameter marker found outside raw layer: {path.relative_to(root)} contains {marker}")


def validate_workspace(root: Path) -> list[str]:
    errors: list[str] = []
    root = root.resolve()

    for rel in ["index.html", "data/company-profile.json", "data/viewer-data.json", "data/research-status.json"]:
        if not (root / rel).exists():
            errors.append(f"missing file: {rel}")

    profile = read_json(root / "data/company-profile.json", errors)
    viewer = read_json(root / "data/viewer-data.json", errors)
    status = read_json(root / "data/research-status.json", errors)

    if profile.get("schema_version") != "company-context-web-v1":
        errors.append("data/company-profile.json schema_version must be company-context-web-v1")
    if viewer.get("schema_version") != "company-context-viewer-v1":
        errors.append("data/viewer-data.json schema_version must be company-context-viewer-v1")
    if viewer.get("profile", {}).get("schema_version") != "company-context-web-v1":
        errors.append("data/viewer-data.json profile must embed company-context-web-v1")
    if viewer.get("status", {}).get("schema_version") != "company-context-status-v1":
        errors.append("data/viewer-data.json status must embed company-context-status-v1")
    if status.get("schema_version") != "company-context-status-v1":
        errors.append("data/research-status.json schema_version must be company-context-status-v1")
    for key in VIEWER_ARRAY_KEYS:
        if not isinstance(viewer.get(key), list):
            errors.append(f"data/viewer-data.json {key} must be an array")
    validate_viewer_html(root, errors)
    validate_no_auth_params(root, errors)

    target = profile.get("target") or {}
    summary = profile.get("summary") or {}
    surface_map = profile.get("surface_map") or {}
    sections = profile.get("sections") or {}
    if is_blank(target.get("name")):
        errors.append("target.name is required")
    if is_blank(summary.get("one_screen")):
        errors.append("summary.one_screen is required")
    if not (surface_map.get("surfaces") or surface_map.get("contradictions_unresolved_edges")):
        errors.append("surface_map needs surfaces or unresolved edges")
    if not profile.get("sources"):
        errors.append("sources array is required")

    missing_sections = sorted(REQUIRED_SECTIONS - set(sections))
    if missing_sections:
        errors.append(f"missing sections: {', '.join(missing_sections)}")

    steps = status.get("steps") or []
    step_by_id = {step.get("id"): step for step in steps if isinstance(step, dict)}
    missing_steps = sorted(REQUIRED_STEPS - set(step_by_id))
    if missing_steps:
        errors.append(f"missing status steps: {', '.join(missing_steps)}")
    for step_id in sorted(REQUIRED_STEPS & set(step_by_id)):
        step = step_by_id[step_id]
        step_status = step.get("status")
        evidence = step.get("evidence") or []
        notes = (step.get("notes") or "").strip()
        if step_status not in {"done", "skipped", "partial"}:
            errors.append(f"status step {step_id} must be done, partial, or skipped")
        elif step_status == "done" and not evidence:
            errors.append(f"status step {step_id} needs evidence")
        elif step_status in {"partial", "skipped"} and not notes:
            errors.append(f"status step {step_id} {step_status} without notes")
        elif step_status == "partial" and not evidence:
            errors.append(f"status step {step_id} partial without evidence")
    validate_status_semantics(root, step_by_id, errors)

    manifest_rows: list[dict[str, str]] = []
    for rel, headers in REQUIRED_TSV_HEADERS.items():
        rows = validate_tsv(root, rel, headers, errors)
        if rel == "source-manifest.tsv":
            manifest_rows = rows
    validate_manifest_paths(root, manifest_rows, errors)

    return errors


def write_tsv(path: Path, headers: list[str], rows: list[list[str]] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(headers)
        writer.writerows(rows or [])


def make_fixture(root: Path, complete: bool) -> None:
    (root / "data").mkdir(parents=True)
    viewer_html = """<!doctype html>
<script type="module">
import React from "https://esm.sh/react@18.3.1";
import "https://esm.sh/recharts@2.15.3";
import "https://esm.sh/d3-cloud@1.2.7";
import "https://esm.sh/@tanstack/react-table@8.21.3";
fetch("./data/viewer-data.json");
</script>
기업개요 종합성장분석 방문자/소비자 연구/특허 투자유치 조직/재무 기업뉴스
"""
    (root / "index.html").write_text(viewer_html, encoding="utf-8")
    profile = {
        "schema_version": "company-context-web-v1",
        "target": {"name": "Fixture Co"},
        "summary": {"one_screen": "fixture summary" if complete else ""},
        "surface_map": {"surfaces": [{"type": "home", "url": "https://example.com"}]},
        "sections": {key: {} for key in REQUIRED_SECTIONS},
        "sources": [{"title": "Example", "url": "https://example.com"}] if complete else [],
    }
    status_value = "done" if complete else "pending"
    status = {
        "schema_version": "company-context-status-v1",
        "steps": [
            {"id": step_id, "label": step_id, "status": status_value, "evidence": ["source-manifest.tsv"], "notes": ""}
            for step_id in REQUIRED_STEPS
        ],
    }
    (root / "data/company-profile.json").write_text(json.dumps(profile), encoding="utf-8")
    (root / "data/research-status.json").write_text(json.dumps(status), encoding="utf-8")
    viewer = {
        "schema_version": "company-context-viewer-v1",
        "profile": profile,
        "status": status,
        **{key: [] for key in VIEWER_ARRAY_KEYS},
    }
    (root / "data/viewer-data.json").write_text(json.dumps(viewer), encoding="utf-8")
    for rel, headers in REQUIRED_TSV_HEADERS.items():
        rows = [
            ["web", "https://example.com", "Example", "data/company-profile.json", "2026-01-01", "fixture"],
            ["data", "data/viewer-data.json", "Viewer data bundle", "data/viewer-data.json", "2026-01-01", "fixture"],
        ] if rel == "source-manifest.tsv" and complete else []
        if complete and rel == "recursive-crawl/link-inventory.tsv":
            rows = [["company", "link", "about", "example.com", "https://example.com/about", "https://example.com"]]
        if complete and rel == "recursive-crawl/shortlist.tsv":
            rows = [["10", "about", "https://example.com/about", "fixture"]]
        write_tsv(root / rel, headers, rows)
    if complete:
        write_tsv(root / "official-data/naver-datalab/search-trends.tsv", ["period", "group", "keyword", "ratio", "source_url"], [["2026-01-01", "Fixture", "fixture", "1", "https://openapi.naver.com/v1/datalab/search"]])
        write_tsv(root / "official-data/data-go-kr/procurement/procurement-search.tsv", ["dataset", "query", "confirmed_matches", "note"], [["fixture", "Fixture", "0", "checked"]])
        write_tsv(root / "official-data/data-go-kr/support-programs/support-program-search.tsv", ["dataset", "query", "confirmed_company_selection", "note"], [["fixture", "Fixture", "0", "checked"]])
        write_tsv(root / "official-data/ntis/projects.tsv", ["project_name", "period", "organization", "ministry", "budget", "source_url"], [["No confirmed fixture project", "2026", "Fixture", "-", "0", "https://example.com"]])


def self_test() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        valid = Path(tmp) / "valid"
        invalid = Path(tmp) / "invalid"
        leaky = Path(tmp) / "leaky"
        make_fixture(valid, complete=True)
        make_fixture(invalid, complete=False)
        make_fixture(leaky, complete=True)
        profile = read_json(leaky / "data/company-profile.json", [])
        profile["sources"].append({
            "title": "Leaky call",
            "url": "https://example.com/api?accessKey=$KIPRIS_API_KEY",
            "source_path": "data/company-profile.json",
        })
        (leaky / "data/company-profile.json").write_text(json.dumps(profile), encoding="utf-8")
        valid_errors = validate_workspace(valid)
        invalid_errors = validate_workspace(invalid)
        leaky_errors = validate_workspace(leaky)
        assert not valid_errors, valid_errors
        assert invalid_errors, "invalid fixture unexpectedly passed"
        assert any("auth parameter marker" in error for error in leaky_errors), leaky_errors
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
    errors = validate_workspace(Path(args.workspace))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("validation ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
