#!/usr/bin/env python3
"""Generate a podcast RSS feed (Apple/Spotify-compatible) from JSON config.

Reads <repo>/show.json and <repo>/episodes.json, writes <repo>/feed.xml.
stdlib only. Config is JSON (no PyYAML dependency).

show.json:
  {
    "title": "...", "description": "...", "author": "...",
    "owner_name": "...", "email": "...",        # email shows in feed (Spotify verification)
    "link": "https://owner.github.io/repo/",    # show website (GitHub Pages)
    "image": "https://owner.github.io/repo/cover.jpg",  # square 1400-3000px
    "language": "ko", "category": "Technology", "subcategory": "Tech News",
    "explicit": false, "type": "episodic"
  }
episodes.json: list of
  { "title","description","audio_url","length","duration","pubDate","guid","episode" }
  (newest first or any order; sorted by pubDate desc here)
"""
import json, sys
from pathlib import Path
from xml.sax.saxutils import escape


def x(s):
    return escape(str(s or ""))


def build(show, eps):
    eps = sorted(eps, key=lambda e: e.get("pubDate", ""), reverse=True)
    L = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd"'
         ' xmlns:content="http://purl.org/rss/1.0/modules/content/">', '<channel>']
    L += [f"<title>{x(show['title'])}</title>",
          f"<link>{x(show.get('link',''))}</link>",
          f"<language>{x(show.get('language','ko'))}</language>",
          f"<description>{x(show['description'])}</description>",
          f"<itunes:author>{x(show.get('author',''))}</itunes:author>",
          f"<itunes:summary>{x(show['description'])}</itunes:summary>",
          f'<itunes:image href="{x(show.get("image",""))}"/>',
          f"<itunes:explicit>{'true' if show.get('explicit') else 'false'}</itunes:explicit>",
          f"<itunes:type>{x(show.get('type','episodic'))}</itunes:type>",
          "<itunes:owner>",
          f"<itunes:name>{x(show.get('owner_name', show.get('author','')))}</itunes:name>",
          f"<itunes:email>{x(show['email'])}</itunes:email>", "</itunes:owner>"]
    cat = show.get("category")
    if cat:
        sub = show.get("subcategory")
        if sub:
            L.append(f'<itunes:category text="{x(cat)}"><itunes:category text="{x(sub)}"/></itunes:category>')
        else:
            L.append(f'<itunes:category text="{x(cat)}"/>')
    if show.get("image"):
        L += ["<image>", f"<url>{x(show['image'])}</url>",
              f"<title>{x(show['title'])}</title>",
              f"<link>{x(show.get('link',''))}</link>", "</image>"]
    for e in eps:
        L += ["<item>",
              f"<title>{x(e['title'])}</title>",
              f"<description><![CDATA[{e.get('description','')}]]></description>",
              f'<enclosure url="{x(e["audio_url"])}" length="{int(e.get("length",0))}" type="audio/mpeg"/>',
              f'<guid isPermaLink="false">{x(e.get("guid", e["audio_url"]))}</guid>',
              f"<pubDate>{x(e['pubDate'])}</pubDate>",
              f"<itunes:duration>{int(e.get('duration',0))}</itunes:duration>",
              f"<itunes:explicit>{'true' if e.get('explicit', show.get('explicit')) else 'false'}</itunes:explicit>"]
        if e.get("episode"):
            L.append(f"<itunes:episode>{int(e['episode'])}</itunes:episode>")
        L.append("</item>")
    L += ["</channel>", "</rss>", ""]
    return "\n".join(L)


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True, help="show repo dir (has show.json, episodes.json)")
    a = ap.parse_args()
    repo = Path(a.repo).expanduser()
    show = json.loads((repo / "show.json").read_text(encoding="utf-8"))
    epf = repo / "episodes.json"
    eps = json.loads(epf.read_text(encoding="utf-8")) if epf.exists() else []
    (repo / "feed.xml").write_text(build(show, eps), encoding="utf-8")
    print(f"[feed] wrote {repo/'feed.xml'} ({len(eps)} episodes)")


if __name__ == "__main__":
    main()
