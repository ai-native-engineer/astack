#!/usr/bin/env python3
"""Merge normalized official API outputs into a company-context profile."""

from __future__ import annotations

import argparse
import csv
import json
import tempfile
from datetime import date
from pathlib import Path


MANIFEST_HEADERS = ["source_type", "url_or_path", "title", "saved_path", "date_collected", "note"]


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, str]], headers: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def upsert(rows: list[dict[str, str]], key: str, row: dict[str, str]) -> None:
    for idx, old in enumerate(rows):
        if old.get(key) == row.get(key):
            rows[idx] = {**old, **row}
            return
    rows.append(row)


def add_source(profile: dict, title: str, source_path: str, note: str, url: str = "") -> None:
    sources = profile.setdefault("sources", [])
    row = {"title": title, "source_path": source_path, "note": note}
    if url:
        row["url"] = url
    upsert(sources, "title", row)


def eok(value: object) -> str:
    try:
        text = str(value).strip()
        if not text:
            return "-"
        return f"{int(float(text)) / 100000000:,.1f}억원"
    except Exception:
        return "-"


def latest(rows: list[dict[str, str]], key: str) -> dict[str, str]:
    return sorted((row for row in rows if row.get(key)), key=lambda row: row.get(key, ""))[-1] if rows else {}


def cell(row: dict[str, str], key: str) -> str:
    value = row.get(key)
    return str(value).strip() if value is not None else ""


def signed_result(row: dict[str, str], result_key: str, income_key: str, loss_key: str) -> str:
    result = cell(row, result_key)
    if result:
        return result
    income = cell(row, income_key)
    if income:
        return income
    loss = cell(row, loss_key)
    if not loss:
        return ""
    try:
        loss_float = float(loss)
        signed = loss_float if loss_float < 0 else -loss_float
        return str(int(signed)) if signed.is_integer() else str(signed)
    except Exception:
        return loss if loss.startswith("-") else f"-{loss}"


def financial_item(row: dict[str, str]) -> dict[str, str]:
    operating_result = signed_result(row, "operating_result_krw", "operating_income_krw", "operating_loss_krw")
    net_result = signed_result(row, "net_result_krw", "net_income_krw", "net_loss_krw")
    return {
        "date": row.get("year", ""),
        "title": f"{row.get('year', '')} 감사보고서 재무 요약",
        "value": f"영업수익 {eok(row.get('revenue_krw', ''))}, 영업손익 {eok(operating_result)}, 당기순손익 {eok(net_result)}",
        "summary": f"자산 {eok(row.get('assets_krw', ''))}, 부채 {eok(row.get('liabilities_krw', ''))}, 자본 {eok(row.get('equity_krw', ''))}",
        "source_path": f"official-data/dart/{row.get('source_xml')}" if row.get("source_xml") else "official-data/dart/financial-summary.tsv",
    }


def upsert_metric(section: dict, label: str, value: str, note: str) -> None:
    metrics = section.setdefault("metrics", [])
    upsert(metrics, "label", {"label": label, "value": value, "note": note})


def merge_profile(root: Path, profile: dict, data: dict[str, list[dict[str, str]]]) -> dict:
    sections = profile.setdefault("sections", {})
    overview = sections.setdefault("overview", {})
    growth = sections.setdefault("growth", {})
    traffic = sections.setdefault("traffic_consumer", {})
    research = sections.setdefault("research_ip", {})
    funding = sections.setdefault("funding", {})
    finance = sections.setdefault("organization_finance", {})

    financials = data["financials"]
    headcount = data["headcount"]
    business_status = data["business_status"]
    search_trends = data["search_trends"]
    procurement = data["procurement"]
    support_programs = data["support_programs"]
    funding_signals = data["funding_signals"]
    patents = data["patents"]
    trademarks = data["trademarks"]
    keywords = data["keywords"]
    ntis_projects = data["ntis_projects"]

    if financials:
        finance["financials"] = [financial_item(row) for row in financials]
        last = latest(financials, "year")
        operating_result = signed_result(last, "operating_result_krw", "operating_income_krw", "operating_loss_krw")
        net_result = signed_result(last, "net_result_krw", "net_income_krw", "net_loss_krw")
        growth["metrics"] = [
            metric for metric in growth.get("metrics", [])
            if metric.get("label") not in {"최근 영업손실", "최근 순손실"}
        ]
        upsert_metric(overview, "매출액", eok(last.get("revenue_krw", "")), f"{last.get('year', '')} DART")
        upsert_metric(growth, "최근 영업수익", eok(last.get("revenue_krw", "")), f"{last.get('year', '')} DART 감사보고서")
        upsert_metric(growth, "최근 영업손익", eok(operating_result), f"{last.get('year', '')} DART 감사보고서")
        upsert_metric(growth, "최근 순손익", eok(net_result), f"{last.get('year', '')} DART 감사보고서")
        upsert_metric(growth, "최근 자본총계", eok(last.get("equity_krw", "")), f"{last.get('year', '')} DART 감사보고서")
        add_source(profile, "DART 재무 요약", "official-data/dart/financial-summary.tsv", f"정규화 재무 {len(financials)}개 연도")

    if headcount:
        finance["employee_trends"] = headcount
        last = latest(headcount, "dataCrtYm")
        period = f"{last.get('dataCrtYm', '')[:4]}-{last.get('dataCrtYm', '')[4:6]}".strip("-")
        value = f"{last.get('jnngpCnt', '-')}명"
        upsert_metric(overview, "국민연금 가입자수", value, f"{period} 국민연금 사업장")
        finance["headcount"] = [{
            "date": period,
            "title": "국민연금 가입자수",
            "value": value,
            "summary": f"당월 취득 {last.get('nwAcqzrCnt', '-')}명, 상실 {last.get('lssJnngpCnt', '-')}명",
            "source_path": "official-data/data-go-kr/nps-workplace/headcount.tsv",
            "note": "3인 이상 법인사업장 중심의 고용 프록시",
        }]
        add_source(profile, "국민연금 사업장 가입자 추이", "official-data/data-go-kr/nps-workplace/headcount.tsv", f"정규화 월별 가입자 {len(headcount)}건")

    if business_status:
        row = business_status[0]
        profile.setdefault("target", {}).setdefault("identifiers", {})["business_status"] = row
        upsert_metric(overview, "사업자 상태", row.get("b_stt", "-"), "국세청 사업자등록 상태조회")
        facts = overview.setdefault("facts", [])
        upsert(facts, "title", {
            "title": "사업자등록 상태",
            "value": row.get("b_stt", "-"),
            "summary": row.get("tax_type", ""),
            "source_path": "official-data/data-go-kr/nts-business-status/business-status.tsv",
        })
        add_source(profile, "국세청 사업자등록 상태", "official-data/data-go-kr/nts-business-status/business-status.tsv", "정규화 사업자 상태 1건")

    if search_trends:
        traffic["search_trends"] = search_trends
        groups = sorted({row.get("group", "") for row in search_trends if row.get("group")})
        upsert_metric(traffic, "검색 키워드", f"{len(groups)}개", "Naver DataLab 검색 관심도 프록시")
        add_source(profile, "Naver DataLab 검색 관심도", "official-data/naver-datalab/search-trends.tsv", f"정규화 검색 트렌드 {len(search_trends)}건")

    if procurement:
        confirmed = sum(int(row.get("confirmed_matches") or 0) for row in procurement)
        growth["procurement_contracts"] = [{
            "date": date.today().isoformat(),
            "title": "조달/계약 검색",
            "value": f"확정 {confirmed}건",
            "summary": f"나라장터 입찰/계약 키워드 {len(procurement)}개 조합을 확인했다. 검색 후보와 실제 수주 이력은 구분한다.",
            "source_path": "official-data/data-go-kr/procurement/procurement-search.tsv",
        }]
        add_source(profile, "나라장터 조달/계약 검색", "official-data/data-go-kr/procurement/procurement-search.tsv", f"정규화 조달 검색 {len(procurement)}건")

    if support_programs:
        confirmed = sum(int(row.get("confirmed_company_selection") or 0) for row in support_programs)
        funding["support_programs"] = [{
            "date": date.today().isoformat(),
            "title": "정부지원사업 선정 이력 검색",
            "value": f"확정 선정 {confirmed}건",
            "summary": f"기업마당/K-Startup 공고 검색 {len(support_programs)}개 조합을 확인했다. 공고 검색과 수혜 이력은 구분한다.",
            "source_path": "official-data/data-go-kr/support-programs/support-program-search.tsv",
        }]
        add_source(profile, "기업마당/K-Startup 지원사업 검색", "official-data/data-go-kr/support-programs/support-program-search.tsv", f"정규화 지원사업 검색 {len(support_programs)}건")

    if funding_signals:
        funding["official_signals"] = funding_signals
        add_source(profile, "DART 투자/자본 보조 신호", "official-data/dart/funding-signals.tsv", f"정규화 보조 신호 {len(funding_signals)}건")

    if patents:
        research["patents"] = patents
        add_source(profile, "KIPRIS 특허/실용신안 원장", "official-data/kipris/patents.tsv", f"정규화 특허/실용신안 {len(patents)}건")
    if trademarks:
        research["trademarks"] = trademarks
        add_source(profile, "KIPRIS 상표 원장", "official-data/kipris/trademarks.tsv", f"정규화 상표 {len(trademarks)}건")
    if keywords:
        research["keywords"] = [row.get("keyword", "") for row in keywords[:24] if row.get("keyword")]
    if ntis_projects:
        existing = research.get("projects", [])
        seen = {row.get("title") for row in existing if isinstance(row, dict)}
        research["projects"] = existing + [row for row in ntis_projects if row.get("title") not in seen]
        add_source(profile, "NTIS 국가R&D 과제 원장", "official-data/ntis/projects.tsv", f"정규화 국가R&D 과제 {len(ntis_projects)}건")

    metrics = [m for m in research.get("metrics", []) if m.get("label") not in {"KIPRIS 특허/실용신안", "KIPRIS 상표", "NTIS 조회"}]
    if patents:
        metrics.append({"label": "KIPRIS 특허/실용신안", "value": f"{len(patents)}건", "note": "open-api 정규화 TSV"})
    if trademarks:
        metrics.append({"label": "KIPRIS 상표", "value": f"{len(trademarks)}건", "note": "open-api 정규화 TSV"})
    ntis_note = "open-api 정규화 TSV" if ntis_projects else "projects.tsv 0건 또는 키/승인 보류"
    metrics.append({"label": "NTIS 조회", "value": f"{len(ntis_projects)}건" if ntis_projects else "보류", "note": ntis_note})
    research["metrics"] = metrics

    notes = []
    if patents or trademarks:
        notes.append(f"KIPRIS 정규화 원장 기준 특허/실용신안 {len(patents)}건, 상표 {len(trademarks)}건을 반영했다.")
    notes.append(f"NTIS 정규화 과제 {len(ntis_projects)}건을 반영했다." if ntis_projects else "NTIS 정규화 과제는 0건 또는 보류 상태다.")
    if not research.get("analysis"):
        research["analysis"] = " ".join(notes)

    gaps = [gap for gap in profile.get("gaps", []) if "KIPRIS" not in gap and "NTIS" not in gap]
    if not ntis_projects:
        gaps.append("NTIS R&D 과제는 정규화 TSV 0건 또는 키/승인 보류 상태로 남김.")
    profile["gaps"] = gaps
    return profile


def update_status(root: Path, notes: str) -> None:
    path = root / "data/research-status.json"
    if not path.exists():
        return
    status = read_json(path)
    evidence_candidates = [
        "official-data/dart/financial-summary.tsv",
        "official-data/dart/funding-signals.tsv",
        "official-data/naver-datalab/search-trends.tsv",
        "official-data/data-go-kr/nps-workplace/headcount.tsv",
        "official-data/data-go-kr/nts-business-status/business-status.tsv",
        "official-data/data-go-kr/procurement/procurement-search.tsv",
        "official-data/data-go-kr/support-programs/support-program-search.tsv",
        "official-data/kipris/patents.tsv",
        "official-data/kipris/trademarks.tsv",
        "official-data/kipris/keywords.tsv",
        "official-data/ntis/projects.tsv",
    ]
    full_market_rels = [
        "official-data/naver-datalab/search-trends.tsv",
        "official-data/data-go-kr/procurement/procurement-search.tsv",
        "official-data/data-go-kr/support-programs/support-program-search.tsv",
        "official-data/ntis/projects.tsv",
    ]
    for step in status.get("steps", []):
        if step.get("id") == "market_data":
            evidence = step.setdefault("evidence", [])
            for rel in evidence_candidates:
                if (root / rel).exists() and rel not in evidence:
                    evidence.append(rel)
            missing = [rel for rel in full_market_rels if len(read_tsv(root / rel)) == 0]
            if evidence and missing and step.get("status") != "skipped":
                step["status"] = "partial"
                step["notes"] = f"{notes}; missing_or_empty={','.join(missing)}"
            elif evidence and not missing and step.get("status") in {"pending", "partial", ""}:
                step["status"] = "done"
                step["notes"] = notes
            else:
                step["notes"] = notes
        if step.get("id") == "source_integrity":
            evidence = step.setdefault("evidence", [])
            for rel in ["official-data/kipris/", "official-data/ntis/"]:
                if (root / rel).exists() and rel not in evidence:
                    evidence.append(rel)
    write_json(path, status)


def update_manifest(root: Path, data: dict[str, list[dict[str, str]]]) -> None:
    manifest = read_tsv(root / "source-manifest.tsv")
    today = date.today().isoformat()
    rows = [
        ("dart", "official-data/dart/financial-summary.tsv", "DART financial summary normalized", f"{len(data['financials'])} rows"),
        ("dart", "official-data/dart/funding-signals.tsv", "DART funding signals normalized", f"{len(data['funding_signals'])} rows"),
        ("naver-datalab", "official-data/naver-datalab/search-trends.tsv", "Naver DataLab search trends normalized", f"{len(data['search_trends'])} rows"),
        ("data-go-kr", "official-data/data-go-kr/nps-workplace/headcount.tsv", "NPS workplace headcount normalized", f"{len(data['headcount'])} rows"),
        ("data-go-kr", "official-data/data-go-kr/nts-business-status/business-status.tsv", "NTS business status normalized", f"{len(data['business_status'])} rows"),
        ("data-go-kr", "official-data/data-go-kr/procurement/procurement-search.tsv", "Procurement search normalized", f"{len(data['procurement'])} rows"),
        ("data-go-kr", "official-data/data-go-kr/support-programs/support-program-search.tsv", "Support program search normalized", f"{len(data['support_programs'])} rows"),
        ("kipris", "official-data/kipris/patents.tsv", "KIPRIS patents normalized", f"{len(data['patents'])} rows"),
        ("kipris", "official-data/kipris/trademarks.tsv", "KIPRIS trademarks normalized", f"{len(data['trademarks'])} rows"),
        ("kipris", "official-data/kipris/keywords.tsv", "KIPRIS keywords normalized", f"{len(data['keywords'])} rows"),
        ("ntis", "official-data/ntis/projects.tsv", "NTIS projects normalized", f"{len(data['ntis_projects'])} rows"),
    ]
    for source_type, rel, title, note in rows:
        if (root / rel).exists():
            upsert(manifest, "saved_path", {
                "source_type": source_type,
                "url_or_path": rel,
                "title": title,
                "saved_path": rel,
                "date_collected": today,
                "note": note,
            })
    write_tsv(root / "source-manifest.tsv", manifest, MANIFEST_HEADERS)


def merge(root: Path) -> dict[str, int]:
    root = root.resolve()
    data = {
        "financials": read_tsv(root / "official-data/dart/financial-summary.tsv"),
        "funding_signals": read_tsv(root / "official-data/dart/funding-signals.tsv"),
        "search_trends": read_tsv(root / "official-data/naver-datalab/search-trends.tsv"),
        "headcount": read_tsv(root / "official-data/data-go-kr/nps-workplace/headcount.tsv"),
        "business_status": read_tsv(root / "official-data/data-go-kr/nts-business-status/business-status.tsv"),
        "procurement": read_tsv(root / "official-data/data-go-kr/procurement/procurement-search.tsv"),
        "support_programs": read_tsv(root / "official-data/data-go-kr/support-programs/support-program-search.tsv"),
        "patents": read_tsv(root / "official-data/kipris/patents.tsv"),
        "trademarks": read_tsv(root / "official-data/kipris/trademarks.tsv"),
        "keywords": read_tsv(root / "official-data/kipris/keywords.tsv"),
        "ntis_projects": read_tsv(root / "official-data/ntis/projects.tsv"),
    }
    profile_path = root / "data/company-profile.json"
    profile = merge_profile(root, read_json(profile_path), data)
    write_json(profile_path, profile)
    notes = (
        f"DART financials={len(data['financials'])}, funding_signals={len(data['funding_signals'])}; "
        f"data.go.kr headcount={len(data['headcount'])}, business_status={len(data['business_status'])}, "
        f"procurement={len(data['procurement'])}, support={len(data['support_programs'])}; "
        f"Naver DataLab={len(data['search_trends'])}; "
        f"KIPRIS patents={len(data['patents'])}, trademarks={len(data['trademarks'])}; "
        f"NTIS projects={len(data['ntis_projects'])}"
    )
    update_status(root, notes)
    update_manifest(root, data)
    return {key: len(value) for key, value in data.items()}


def self_test() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "data").mkdir()
        (root / "official-data/dart").mkdir(parents=True)
        (root / "official-data/naver-datalab").mkdir(parents=True)
        (root / "official-data/data-go-kr/nps-workplace").mkdir(parents=True)
        (root / "official-data/data-go-kr/nts-business-status").mkdir(parents=True)
        (root / "official-data/data-go-kr/procurement").mkdir(parents=True)
        (root / "official-data/data-go-kr/support-programs").mkdir(parents=True)
        (root / "official-data/kipris").mkdir(parents=True)
        (root / "official-data/ntis").mkdir(parents=True)
        write_json(root / "data/company-profile.json", {"schema_version": "company-context-web-v1", "target": {"identifiers": {}}, "sections": {"research_ip": {}}, "gaps": [], "sources": []})
        write_json(root / "data/research-status.json", {"schema_version": "company-context-status-v1", "steps": [{"id": "market_data", "status": "done", "evidence": []}, {"id": "source_integrity", "status": "done", "evidence": []}]})
        write_tsv(root / "source-manifest.tsv", [], MANIFEST_HEADERS)
        write_tsv(
            root / "official-data/dart/financial-summary.tsv",
            [{
                "year": "2025",
                "revenue_krw": "100000000",
                "operating_income_krw": "",
                "operating_loss_krw": "20000000",
                "operating_result_krw": "-20000000",
                "net_income_krw": "30000000",
                "net_loss_krw": "",
                "net_result_krw": "30000000",
                "assets_krw": "40000000",
                "liabilities_krw": "50000000",
                "equity_krw": "-10000000",
                "source_xml": "report.xml",
            }],
            [
                "year",
                "revenue_krw",
                "operating_income_krw",
                "operating_loss_krw",
                "operating_result_krw",
                "net_income_krw",
                "net_loss_krw",
                "net_result_krw",
                "assets_krw",
                "liabilities_krw",
                "equity_krw",
                "source_xml",
            ],
        )
        write_tsv(root / "official-data/dart/funding-signals.tsv", [{"date": "2025-01-01", "title": "유상증자", "value": "10억원", "summary": "요약", "source_path": "official-data/dart/report.xml"}], ["date", "title", "value", "summary", "source_path"])
        write_tsv(root / "official-data/naver-datalab/search-trends.tsv", [{"group": "브랜드", "period": "2025-01-01", "ratio": "10"}], ["group", "period", "ratio"])
        write_tsv(root / "official-data/data-go-kr/nps-workplace/headcount.tsv", [{"dataCrtYm": "202501", "jnngpCnt": "10", "nwAcqzrCnt": "1", "lssJnngpCnt": "2"}], ["dataCrtYm", "jnngpCnt", "nwAcqzrCnt", "lssJnngpCnt"])
        write_tsv(root / "official-data/data-go-kr/nts-business-status/business-status.tsv", [{"b_no": "0000000000", "b_stt": "계속사업자", "tax_type": "일반과세자"}], ["b_no", "b_stt", "tax_type"])
        write_tsv(root / "official-data/data-go-kr/procurement/procurement-search.tsv", [{"confirmed_matches": "0"}], ["confirmed_matches"])
        write_tsv(root / "official-data/data-go-kr/support-programs/support-program-search.tsv", [{"confirmed_company_selection": "0"}], ["confirmed_company_selection"])
        write_tsv(root / "official-data/kipris/patents.tsv", [{"date": "2026-01-01", "title": "특허", "summary": "요약"}], ["date", "title", "summary"])
        write_tsv(root / "official-data/kipris/trademarks.tsv", [{"date": "2026-01-01", "title": "상표", "summary": "요약"}], ["date", "title", "summary"])
        write_tsv(root / "official-data/kipris/keywords.tsv", [{"keyword": "AI", "weight": "10", "source": "test"}], ["keyword", "weight", "source"])
        result = merge(root)
        profile = read_json(root / "data/company-profile.json")
        assert result["patents"] == 1
        assert result["financials"] == 1
        assert profile["sections"]["funding"]["official_signals"][0]["title"] == "유상증자"
        assert profile["sections"]["overview"]["metrics"][0]["label"] == "매출액"
        assert "영업손익 -0.2억원" in profile["sections"]["organization_finance"]["financials"][0]["value"]
        assert "당기순손익 0.3억원" in profile["sections"]["organization_finance"]["financials"][0]["value"]
        assert any(metric["label"] == "최근 순손익" for metric in profile["sections"]["growth"]["metrics"])
        assert profile["sections"]["research_ip"]["metrics"][0]["value"] == "1건"
    print("self-test ok")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace", nargs="?")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0
    if not args.workspace:
        parser.error("workspace is required unless --self-test is used")
    print(json.dumps(merge(Path(args.workspace)), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
