#!/usr/bin/env python3
"""oss-explore :: render_html
stdin 으로 explore.sh / contributions.sh / stats.sh 의 JSON 을 받아 단일 HTML 리포트를 stdout 으로 출력.
의존성 0 (표준 라이브러리만), 다크/라이트 자동 대응, 인라인 CSS.
"""
import sys
import json
import html as _html


def esc(s):
    return _html.escape(str(s))


def bar_rows(items, label_key, value_key, unit=""):
    if not items:
        return "<p class='muted'>데이터 없음</p>"
    maxv = max((it[value_key] for it in items), default=0) or 1
    out = []
    for it in items:
        pct = round(it[value_key] / maxv * 100)
        out.append(
            f"<div class='bar-row'>"
            f"<span class='bar-label'>{esc(it[label_key])}</span>"
            f"<span class='bar-track'><span class='bar-fill' style='width:{pct}%'></span></span>"
            f"<span class='bar-val'>{esc(it[value_key])}{unit}</span>"
            f"</div>"
        )
    return "\n".join(out)


def render_contributions(d):
    s = d.get("summary", {})
    limit_note = (f"<p class='muted'>GitHub 검색 상한 {s.get('search_limit')}건에 도달해 일부 기여가 빠질 수 있습니다.</p>"
                  if s.get("limit_reached") else "")
    metadata_note = (f"<p class='muted'>레포 메타데이터 조회 실패 {s.get('metadata_lookup_failures')}건: 별 수와 설명 일부를 확인할 수 없습니다.</p>"
                     if s.get("metadata_lookup_failures") else "")
    cards = f"""
    <div class='cards'>
      <div class='card'><div class='num'>{s.get('merged_prs', 0)}</div><div class='lbl'>머지된 PR</div></div>
      <div class='card'><div class='num'>{s.get('external_repos', 0)}</div><div class='lbl'>순수 외부 OSS</div></div>
      <div class='card'><div class='num'>{s.get('org_groups', 0)}</div><div class='lbl'>소속 조직</div></div>
    </div>"""

    ext = d.get("external", [])
    if ext:
        rows = "\n".join(
            f"<tr><td><a href='{esc(r['url'])}' target='_blank'>{esc(r['repo'])}</a></td>"
            f"<td class='c'>{r['prs']}</td>"
            f"<td class='c'><span class='star'>★ {esc('?' if r.get('stars') is None else format(r['stars'], ','))}</span></td>"
            f"<td class='desc'>{esc(r.get('description', ''))}</td></tr>"
            for r in ext
        )
        external = f"""
        <table>
          <thead><tr><th>레포</th><th>머지 PR</th><th>Stars</th><th>설명</th></tr></thead>
          <tbody>{rows}</tbody>
        </table>"""
    else:
        external = "<p class='muted'>순수 외부 OSS 기여 없음</p>"

    orgs = d.get("orgs", [])
    if orgs:
        items = []
        for g in orgs:
            repos = ", ".join(
                f"{esc(r['repo'].split('/')[-1])}<span class='dim'>({r['prs']})</span>"
                for r in g["repos"]
            )
            items.append(
                f"<li><strong>{esc(g['org'])}</strong> "
                f"<span class='dim'>· {g['prs']} PR</span><br><span class='repos'>{repos}</span></li>"
            )
        org_html = f"<ul class='orglist'>{''.join(items)}</ul>"
    else:
        org_html = "<p class='muted'>소속 조직 기여 없음</p>"

    body = f"""
    {cards}
    {limit_note}
    {metadata_note}
    <h2>순수 외부 OSS 기여 <span class='dim'>(star 순)</span></h2>
    {external}
    <h2>소속 조직 <span class='dim'>(팀/회사 프로젝트)</span></h2>
    {org_html}"""
    return f"{esc(d.get('user',''))} — 오픈소스 기여 내역", body


def render_stats(d):
    s = d.get("summary", {})
    limit_note = (f"<p class='muted'>GitHub 검색 상한 {s.get('search_limit')}건에 도달해 통계가 일부 기간만 반영될 수 있습니다.</p>"
                  if s.get("limit_reached") else "")
    language_note = (f"<p class='muted'>언어 조회 실패 {s.get('language_lookup_failures')}건은 언어별 분포에서 제외했습니다.</p>"
                     if s.get("language_lookup_failures") else "")
    cards = f"""
    <div class='cards'>
      <div class='card'><div class='num'>{s.get('total_prs', 0)}</div><div class='lbl'>전체 PR</div></div>
      <div class='card'><div class='num'>{s.get('merged_prs', 0)}</div><div class='lbl'>머지된 PR</div></div>
      <div class='card'><div class='num'>{'계산 불가' if s.get('merge_rate') is None else str(s.get('merge_rate', 0)) + '%'}</div><div class='lbl'>머지율</div></div>
    </div>"""
    years = bar_rows(d.get("years", []), "year", "prs")
    months = bar_rows([{**m, "label": m["month"] + "월"} for m in d.get("months", [])], "label", "prs")
    weekdays = d.get("weekdays", [])
    langs = bar_rows(d.get("languages", []), "name", "repos")
    weekday_section = ""
    if weekdays:
        wd = bar_rows(weekdays, "day", "prs")
        weekday_section = f"<h2>요일별 <span class='dim'>(머지 PR)</span></h2>\n<div class='chart'>{wd}</div>"
    body = f"""
    {cards}
    {limit_note}
    {language_note}
    <h2>연도별 <span class='dim'>(머지 PR)</span></h2>
    <div class='chart'>{years}</div>
    <h2>월별 <span class='dim'>(머지 PR)</span></h2>
    <div class='chart'>{months}</div>
    {weekday_section}
    <h2>언어별 <span class='dim'>(머지 PR이 닿은 레포 수)</span></h2>
    <div class='chart'>{langs}</div>"""
    return f"{esc(d.get('user',''))} — 기여 통계", body


def render_explore(d):
    q = d.get("query", {})
    repos = d.get("repos", [])
    with_issues = q.get("with_issues", False)
    issue_failures = d.get("issue_lookup_failures", 0)
    contributable = [r for r in repos if (r.get("gfi") or 0) > 0 or (r.get("hw") or 0) > 0]
    total_gfi = sum(r.get("gfi") or 0 for r in repos)

    def issue_cell(value, emphasize=False):
        if value is None:
            return "?"
        return f"<strong>{value}</strong>" if emphasize and value > 0 else str(value)

    cards = [f"<div class='card'><div class='num'>{len(repos)}</div><div class='lbl'>발견된 레포</div></div>"]
    if with_issues:
        cards.append(f"<div class='card'><div class='num'>{len(contributable)}</div><div class='lbl'>기여 가능 레포</div></div>")
        cards.append(f"<div class='card'><div class='num'>{total_gfi}</div><div class='lbl'>확인된 good first issue 합계</div></div>")
    cards_html = f"<div class='cards'>{''.join(cards)}</div>"

    if repos:
        if with_issues:
            head = "<tr><th>레포</th><th>★</th><th>언어</th><th>최근푸시</th><th>라이선스</th><th>검색 근거</th><th>GFI</th><th>HW</th><th>설명</th></tr>"
            rows = "\n".join(
                f"<tr><td><a href='{esc(r['url'])}' target='_blank'>{esc(r['repo'])}</a></td>"
                f"<td class='c'><span class='star'>★ {r['stars']:,}</span></td>"
                f"<td class='c'>{esc(r['language'])}</td>"
                f"<td class='c'>{esc(r['pushed'])}</td>"
                f"<td class='c'>{esc(r.get('license', 'unknown'))}</td>"
                f"<td class='c'>{esc(', '.join(r.get('matched_by', [])))}</td>"
                f"<td class='c'>{issue_cell(r.get('gfi'), True)}</td>"
                f"<td class='c'>{issue_cell(r.get('hw'))}</td>"
                f"<td class='desc'>{esc(r.get('description', ''))}</td></tr>"
                for r in repos
            )
        else:
            head = "<tr><th>레포</th><th>★</th><th>언어</th><th>최근푸시</th><th>라이선스</th><th>검색 근거</th><th>설명</th></tr>"
            rows = "\n".join(
                f"<tr><td><a href='{esc(r['url'])}' target='_blank'>{esc(r['repo'])}</a></td>"
                f"<td class='c'><span class='star'>★ {r['stars']:,}</span></td>"
                f"<td class='c'>{esc(r['language'])}</td>"
                f"<td class='c'>{esc(r['pushed'])}</td>"
                f"<td class='c'>{esc(r.get('license', 'unknown'))}</td>"
                f"<td class='c'>{esc(', '.join(r.get('matched_by', [])))}</td>"
                f"<td class='desc'>{esc(r.get('description', ''))}</td></tr>"
                for r in repos
            )
        table = f"<table><thead>{head}</thead><tbody>{rows}</tbody></table>"
    else:
        table = "<p class='muted'>해당 주제로 발견된 레포가 없습니다.</p>"

    meta = []
    if q.get("language"):
        meta.append(f"lang={esc(q['language'])}")
    if q.get("license"):
        meta.append(f"license={esc(q['license'])}")
    if q.get("min_stars"):
        meta.append(f"★≥{q['min_stars']}")
    meta.append(f"sort={esc(q.get('sort', 'stars'))}")
    hint = ""
    if with_issues:
        failure_note = (f" 조회 실패 {issue_failures}곳은 ?로 표시했습니다." if issue_failures else "")
        hint = ("<p class='muted'>GFI=good first issue · HW=help wanted (레포/라벨별 최대 50건 조회). "
                f"굵은 GFI = 지금 기여 진입점이 있는 레포.{failure_note}</p>")
    body = f"""
    {cards_html}
    <p class='gen'>{' · '.join(meta)}</p>
    {hint}
    <h2>발견된 레포 <span class='dim'>(관련도 우선, {esc(q.get('sort', 'stars'))} 보조 정렬)</span></h2>
    {table}"""
    return f"\"{esc(q.get('topic', ''))}\" — 오픈소스 발견", body


CSS = """
:root { --bg:#fff; --fg:#1a1a1a; --muted:#666; --card:#f5f5f7; --border:#e2e2e6;
        --accent:#2563eb; --star:#d97706; --fill:#2563eb; --track:#e2e2e6; }
@media (prefers-color-scheme: dark) {
  :root { --bg:#0d1117; --fg:#e6edf3; --muted:#8b949e; --card:#161b22; --border:#30363d;
          --accent:#58a6ff; --star:#e3b341; --fill:#388bfd; --track:#21262d; } }
* { box-sizing:border-box; }
body { margin:0; padding:2.5rem 1.5rem; background:var(--bg); color:var(--fg);
       font:15px/1.6 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif; }
.wrap { max-width:860px; margin:0 auto; }
h1 { font-size:1.6rem; margin:0 0 .25rem; }
h2 { font-size:1.15rem; margin:2rem 0 .75rem; }
.gen { color:var(--muted); font-size:.85rem; margin-bottom:1.5rem; }
.dim { color:var(--muted); font-weight:400; font-size:.85em; }
.muted { color:var(--muted); }
.cards { display:flex; gap:1rem; flex-wrap:wrap; }
.card { flex:1; min-width:140px; background:var(--card); border:1px solid var(--border);
        border-radius:12px; padding:1.1rem 1.2rem; }
.card .num { font-size:2rem; font-weight:700; color:var(--accent); }
.card .lbl { color:var(--muted); font-size:.85rem; }
table { width:100%; border-collapse:collapse; font-size:.9rem; }
th,td { text-align:left; padding:.55rem .6rem; border-bottom:1px solid var(--border); }
th { color:var(--muted); font-weight:600; }
td.c { text-align:center; white-space:nowrap; }
td.desc { color:var(--muted); }
a { color:var(--accent); text-decoration:none; }
a:hover { text-decoration:underline; }
.star { color:var(--star); white-space:nowrap; }
.orglist { list-style:none; padding:0; margin:0; }
.orglist li { padding:.6rem 0; border-bottom:1px solid var(--border); }
.repos { color:var(--muted); font-size:.88rem; }
.chart { display:flex; flex-direction:column; gap:.4rem; }
.bar-row { display:flex; align-items:center; gap:.6rem; }
.bar-label { width:130px; text-align:right; font-size:.85rem; color:var(--muted);
             overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.bar-track { flex:1; height:14px; background:var(--track); border-radius:7px; overflow:hidden; }
.bar-fill { display:block; height:100%; background:var(--fill); border-radius:7px; }
.bar-val { width:48px; font-size:.85rem; }
footer { margin-top:2.5rem; color:var(--muted); font-size:.8rem;
         border-top:1px solid var(--border); padding-top:1rem; }
"""


def main():
    raw = sys.stdin.read()
    d = json.loads(raw)
    t = d.get("type")
    if t == "explore":
        title, body = render_explore(d)
    elif t == "stats":
        title, body = render_stats(d)
    else:
        title, body = render_contributions(d)
    html_out = f"""<!doctype html>
<html lang='ko'><head><meta charset='utf-8'>
<meta name='viewport' content='width=device-width, initial-scale=1'>
<title>{title}</title><style>{CSS}</style></head>
<body><div class='wrap'>
<h1>{title}</h1>
<div class='gen'>생성: {esc(d.get('generated', ''))} · gh CLI 기준</div>
{body}
<footer>oss-explore · GitHub CLI 기반 · 오픈소스 발견 → 비교 → 기여/회고</footer>
</div></body></html>"""
    sys.stdout.write(html_out)


if __name__ == "__main__":
    main()
