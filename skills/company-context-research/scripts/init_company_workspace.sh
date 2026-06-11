#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 1 ] || [ "$#" -gt 2 ]; then
  echo "Usage: init_company_workspace.sh <company-or-domain> [base-dir]" >&2
  exit 2
fi

raw_target="$1"
base_dir="${2:-./company-context}"
stamp="$(date +%Y%m%d)"
slug="$(printf '%s' "$raw_target" | tr '[:space:]' '-' | sed -E 's#/+#-#g; s/-+/-/g; s/^-|-$//g')"

if [ -z "$slug" ]; then
  slug="company"
fi

root="${base_dir%/}/${stamp}-${slug}"
mkdir -p "$root/attachments"
mkdir -p "$root/recursive-crawl/pages"

cat >"$root/00-surface-map.md" <<EOF
# Surface Map

## Legal entity

## Parent company

## Email domain

## Local brand / D2C surfaces

## B2B portal

## Careers

## IR / investor host

## Attachment / CDN host

## Contradictions and unresolved edges
EOF

cat >"$root/00-target.md" <<EOF
# Target

- Company:
- Primary domain:
- Country:
- Listed status:
- Research intent:
- Entity resolution notes:
EOF

cat >"$root/01-public-web.md" <<EOF
# Public Web

## Coverage

## Product and company language

## Attachments reviewed

## Important quotes and claims

## Gaps
EOF

cat >"$root/02-public-press.md" <<EOF
# Public Press

## Company-authored releases

## Third-party coverage

## Timeline

## Why it matters

## Gaps
EOF

cat >"$root/03-market-data.md" <<EOF
# Market Data

## KRX layer

## DART layer

## Finance and capital events

## Risks and anomalies

## Gaps
EOF

cat >"$root/04-internal-context.md" <<EOF
# Internal Context

## Prior touchpoints

## Stakeholders

## Notes and transcripts

## Confidence

## Gaps
EOF

cat >"$root/05-company-brief.md" <<EOF
# Company Brief

## One-screen summary

## Current deal status

## Champion / buying center

## Participant needs

## Next action / questions for next meeting

## What they do

## Why now

## Buying signals

## Language they use

## Risks and red flags

## Suggested outreach angles

## Open questions
EOF

cat >"$root/source-manifest.tsv" <<EOF
source_type	url_or_path	title	saved_path	date_collected	note
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

cat >"$root/recursive-crawl/keep-list-candidates.tsv" <<EOF
score	category	url	reason
EOF

cat >"$root/recursive-crawl/shortlist.tsv" <<EOF
score	category	url	reason
EOF

printf '%s\n' "$root"
