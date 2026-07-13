#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 1 ] || [ "$#" -gt 2 ]; then
  echo "Usage: init_company_workspace.sh <company-or-domain> [base-dir]" >&2
  exit 2
fi

raw_target="$1"
if [ "$#" -ge 2 ]; then
  base_dir="$2"
else
  if [ -d "01-context" ]; then
    base_dir="./01-context/company"
  else
    base_dir="./company-context"
  fi
fi
stamp="$(date +%Y%m%d)"
slug="$(printf '%s' "$raw_target" | tr '[:space:]' '-' | sed -E 's#/+#-#g; s/-+/-/g; s/^-|-$//g')"

if [ -z "$slug" ]; then
  slug="company"
fi

root="${base_dir%/}/${stamp}-${slug}"
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
template_path="$script_dir/../templates/company-viewer.html"
target_json="$(python3 -c 'import json,sys; print(json.dumps(sys.argv[1], ensure_ascii=False))' "$raw_target")"

mkdir -p "$root/data"
mkdir -p "$root/attachments"
mkdir -p "$root/official-data/dart"
mkdir -p "$root/official-data/naver-datalab/raw"
mkdir -p "$root/official-data/data-go-kr/nps-workplace/raw"
mkdir -p "$root/official-data/data-go-kr/nts-business-status/raw"
mkdir -p "$root/official-data/data-go-kr/procurement/raw"
mkdir -p "$root/official-data/data-go-kr/support-programs/raw"
mkdir -p "$root/official-data/kipris/raw"
mkdir -p "$root/official-data/ntis/raw"
mkdir -p "$root/press"
mkdir -p "$root/recursive-crawl/pages"
mkdir -p "$root/public-mirror"

if [ ! -f "$template_path" ]; then
  echo "Missing viewer template: $template_path" >&2
  exit 1
fi
cp "$template_path" "$root/index.html"

cat >"$root/data/company-profile.json" <<EOF
{
  "schema_version": "company-context-web-v1",
  "generated_at": "",
  "target": {
    "name": $target_json,
    "primary_domain": "",
    "country": "",
    "listed_status": "",
    "research_intent": "",
    "entity_resolution_notes": [],
    "identifiers": {}
  },
  "summary": {
    "one_screen": "",
    "deal_status": "",
    "champion_buying_center": [],
    "participant_needs": [],
    "what_they_do": "",
    "why_now": "",
    "buying_signals": [],
    "language_they_use": [],
    "risks_red_flags": [],
    "open_questions": []
  },
  "surface_map": {
    "legal_entity": "",
    "parent_company": "",
    "email_domains": [],
    "surfaces": [],
    "contradictions_unresolved_edges": []
  },
  "sections": {
    "overview": {"metrics": [], "facts": [], "notes": ""},
    "growth": {"metrics": [], "timeline": [], "procurement_contracts": [], "analysis": ""},
    "traffic_consumer": {"metrics": [], "segments": [], "search_trends": [], "analysis": ""},
    "research_ip": {"projects": [], "patents": [], "trademarks": [], "keywords": [], "metrics": [], "analysis": ""},
    "funding": {"rounds": [], "official_signals": [], "support_programs": [], "analysis": ""},
    "organization_finance": {"headcount": [], "employee_trends": [], "financials": [], "analysis": ""},
    "news": {"items": [], "analysis": ""},
    "internal_context": {"touchpoints": [], "stakeholders": [], "analysis": ""}
  },
  "gaps": [],
  "sources": []
}
EOF

cat >"$root/data/research-status.json" <<EOF
{
  "schema_version": "company-context-status-v1",
  "steps": [
    {"id": "surface_map", "label": "Surface map", "status": "pending", "evidence": [], "notes": ""},
    {"id": "public_web_crawl", "label": "Public web crawl", "status": "pending", "evidence": [], "notes": ""},
    {"id": "press_collection", "label": "Press collection", "status": "pending", "evidence": [], "notes": ""},
    {"id": "market_data", "label": "Official market data", "status": "pending", "evidence": [], "notes": ""},
    {"id": "internal_context", "label": "Internal context", "status": "pending", "evidence": [], "notes": ""},
    {"id": "data_profile", "label": "Normalized data profile", "status": "pending", "evidence": [], "notes": ""},
    {"id": "source_integrity", "label": "Source integrity", "status": "pending", "evidence": [], "notes": ""},
    {"id": "viewer_ready", "label": "HTML viewer", "status": "pending", "evidence": [], "notes": ""}
  ]
}
EOF

cat >"$root/source-manifest.tsv" <<EOF
source_type	url_or_path	title	saved_path	date_collected	note
EOF

cat >"$root/press/press-inventory.tsv" <<EOF
source	date	outlet	title	url	decoded	queries
EOF

cat >"$root/recursive-crawl/crawl-manifest.tsv" <<EOF
url	hop	origin_host	status	saved_path	note
EOF

cat >"$root/recursive-crawl/link-inventory.tsv" <<EOF
category	kind	signal	host	url	source_page
EOF

cat >"$root/recursive-crawl/attachment-candidates.tsv" <<EOF
url	origin_url	origin_host	host	priority
EOF

cat >"$root/recursive-crawl/download-report.tsv" <<EOF
url	saved_path	status	mime	note
EOF

cat >"$root/recursive-crawl/keep-list-candidates.tsv" <<EOF
score	category	url	reason
EOF

cat >"$root/recursive-crawl/shortlist.tsv" <<EOF
score	category	url	reason
EOF

printf '%s\n' "$root"
