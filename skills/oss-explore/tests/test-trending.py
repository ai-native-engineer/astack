#!/usr/bin/env python3
import argparse
import importlib.util
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "trending.py"
SPEC = importlib.util.spec_from_file_location("trending", SCRIPT)
assert SPEC and SPEC.loader
trending = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(trending)

SAMPLE = """
<article class="Box-row">
  <h2><a href="/owner/repo">owner / repo</a></h2>
  <p class="col-9 color-fg-muted my-1 pr-4">Useful &amp; small</p>
  <span itemprop="programmingLanguage">Python</span>
  <a href="/owner/repo/stargazers"><svg></svg>1,234</a>
  <span>55 stars today</span>
</article>
"""

repos = trending.parse(SAMPLE, 1)
assert repos == [{
    "repo": "owner/repo",
    "period_stars": 55,
    "total_stars": 1234,
    "language": "Python",
    "description": "Useful & small",
}]
assert trending.parse(SAMPLE.replace("55 stars today", "1 star today"), 1)[0]["period_stars"] == 1
assert trending.source_url("c++", "weekly") == "https://github.com/trending/c%2B%2B?since=weekly"
assert trending.parse("<p>It looks like we don’t have any trending repositories for your choices.</p>", 5) == []

try:
    trending.parse("<html>changed</html>", 5)
except ValueError:
    pass
else:
    raise AssertionError("changed markup must fail")

for markup in (SAMPLE.replace("55 stars today", ""), SAMPLE.replace(">1,234</a>", "></a>")):
    try:
        trending.parse(markup, 1)
    except ValueError:
        pass
    else:
        raise AssertionError("partial star markup must fail")

for value in ("0", "-1"):
    try:
        trending.positive_int(value)
    except argparse.ArgumentTypeError:
        pass
    else:
        raise AssertionError(f"{value} must be rejected")

print("test_trending: ok")
