#!/usr/bin/env python3
"""Generate a validated podcast RSS feed from show.json and episodes.json."""

import argparse
import html
import json
import re
from email.utils import parsedate_to_datetime
from pathlib import Path
from xml.etree import ElementTree
from xml.sax.saxutils import escape


TIMESTAMP_RE = re.compile(r"^\[?(\d{1,2}):(\d{2})(?::(\d{2}))?\]?\s+(.+)$")
LINK_RE = re.compile(r"^(.+?):\s+(https?://\S+)$")


def x(value):
    return escape(str(value or ""), {'"': "&quot;"})


def cdata(value):
    return str(value or "").replace("]]>", "]]]]><![CDATA[>")


def timestamp(line):
    match = TIMESTAMP_RE.match(line.strip())
    if not match:
        return None
    first, second, third, title = match.groups()
    if third is None:
        hours, minutes, seconds = 0, int(first), int(second)
    else:
        hours, minutes, seconds = int(first), int(second), int(third)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d} {title}"


def link(line):
    match = LINK_RE.match(line.strip())
    return match.groups() if match else None


def summary(text):
    """Keep the preview concise; full formatted notes live in content:encoded."""
    blocks = []
    for block in re.split(r"\n\s*\n", str(text or "").strip()):
        lines = block.splitlines()
        if any(timestamp(line) or link(line) for line in lines):
            break
        blocks.append(" ".join(line.strip() for line in lines))
        if len(blocks) == 2:
            break
    return "\n\n".join(blocks) or str(text or "").strip()


def show_notes_html(text):
    """Convert the plain show-notes convention to portable, basic HTML."""
    lines = str(text or "").splitlines()
    parts = []
    index = 0
    while index < len(lines):
        line_text = lines[index].strip()
        if not line_text:
            index += 1
            continue

        stamp = timestamp(line_text)
        if stamp:
            items = []
            while index < len(lines) and (stamp := timestamp(lines[index])):
                items.append(f"<li>{html.escape(stamp)}</li>")
                index += 1
            parts.append("<ul>" + "".join(items) + "</ul>")
            continue

        found_link = link(line_text)
        if found_link:
            items = []
            while index < len(lines) and (found_link := link(lines[index])):
                label, url = found_link
                items.append(
                    f'<li><a href="{html.escape(url, quote=True)}">'
                    f"{html.escape(label)}</a></li>"
                )
                index += 1
            parts.append("<ul>" + "".join(items) + "</ul>")
            continue

        next_line = lines[index + 1] if index + 1 < len(lines) else ""
        if timestamp(next_line) or link(next_line):
            parts.append(f"<p><strong>{html.escape(line_text)}</strong></p>")
        else:
            parts.append(f"<p>{html.escape(line_text)}</p>")
        index += 1
    return "".join(parts)


def validated_episodes(show, episodes):
    for key in ("title", "description", "email"):
        if not show.get(key):
            raise ValueError(f"show.json: missing required field '{key}'")
    if not isinstance(episodes, list):
        raise ValueError("episodes.json: expected a JSON list")

    seen = {"episode": set(), "guid": set(), "audio_url": set()}
    dated = []
    for index, episode in enumerate(episodes, 1):
        where = f"episodes.json item {index}"
        for key in ("title", "audio_url", "pubDate", "guid", "episode"):
            if episode.get(key) in (None, ""):
                raise ValueError(f"{where}: missing required field '{key}'")
        try:
            published = parsedate_to_datetime(episode["pubDate"])
        except (TypeError, ValueError) as error:
            raise ValueError(f"{where}: invalid RFC 2822 pubDate") from error
        if published.utcoffset() is None:
            raise ValueError(f"{where}: pubDate must include a timezone")
        for key in seen:
            value = episode[key]
            if value in seen[key]:
                raise ValueError(f"{where}: duplicate {key} '{value}'")
            seen[key].add(value)
        dated.append((published, episode))
    return [episode for _, episode in sorted(dated, reverse=True, key=lambda item: item[0])]


def build(show, episodes):
    episodes = validated_episodes(show, episodes)
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd"'
        ' xmlns:content="http://purl.org/rss/1.0/modules/content/">',
        "<channel>",
        f"<title>{x(show['title'])}</title>",
        f"<link>{x(show.get('link', ''))}</link>",
        f"<language>{x(show.get('language', 'ko'))}</language>",
        f"<description>{x(show['description'])}</description>",
        f"<itunes:author>{x(show.get('author', ''))}</itunes:author>",
        f"<itunes:summary>{x(show['description'])}</itunes:summary>",
        f'<itunes:image href="{x(show.get("image", ""))}"/>',
        f"<itunes:explicit>{'true' if show.get('explicit') else 'false'}</itunes:explicit>",
        f"<itunes:type>{x(show.get('type', 'episodic'))}</itunes:type>",
        "<itunes:owner>",
        f"<itunes:name>{x(show.get('owner_name', show.get('author', '')))}</itunes:name>",
        f"<itunes:email>{x(show['email'])}</itunes:email>",
        "</itunes:owner>",
    ]
    category = show.get("category")
    if category:
        subcategory = show.get("subcategory")
        if subcategory:
            lines.append(
                f'<itunes:category text="{x(category)}"><itunes:category '
                f'text="{x(subcategory)}"/></itunes:category>'
            )
        else:
            lines.append(f'<itunes:category text="{x(category)}"/>')
    if show.get("image"):
        lines += [
            "<image>",
            f"<url>{x(show['image'])}</url>",
            f"<title>{x(show['title'])}</title>",
            f"<link>{x(show.get('link', ''))}</link>",
            "</image>",
        ]
    for episode in episodes:
        description = episode.get("description", "")
        lines += [
            "<item>",
            f"<title>{x(episode['title'])}</title>",
            f"<description>{x(summary(description))}</description>",
            f"<content:encoded><![CDATA[{cdata(show_notes_html(description))}]]></content:encoded>",
            f'<enclosure url="{x(episode["audio_url"])}" '
            f'length="{int(episode.get("length", 0))}" type="audio/mpeg"/>',
            f'<guid isPermaLink="false">{x(episode["guid"])}</guid>',
            f"<pubDate>{x(episode['pubDate'])}</pubDate>",
            f"<itunes:duration>{int(episode.get('duration', 0))}</itunes:duration>",
            f"<itunes:explicit>{'true' if episode.get('explicit', show.get('explicit')) else 'false'}</itunes:explicit>",
            f"<itunes:episode>{int(episode['episode'])}</itunes:episode>",
            "</item>",
        ]
    lines += ["</channel>", "</rss>", ""]
    feed = "\n".join(lines)
    ElementTree.fromstring(feed)
    return feed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, help="show repo dir")
    args = parser.parse_args()
    repo = Path(args.repo).expanduser()
    show = json.loads((repo / "show.json").read_text(encoding="utf-8"))
    episode_file = repo / "episodes.json"
    episodes = json.loads(episode_file.read_text(encoding="utf-8")) if episode_file.exists() else []
    feed_file = repo / "feed.xml"
    feed_file.write_text(build(show, episodes), encoding="utf-8")
    print(f"[feed] wrote {feed_file} ({len(episodes)} episodes)")


if __name__ == "__main__":
    main()
