#!/usr/bin/env python3
"""Offline regression checks for YouTube channel date backfill."""

import importlib.util
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "youtube-channels.py"
SPEC = importlib.util.spec_from_file_location("youtube_channels", SCRIPT)
youtube_channels = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(youtube_channels)

VIDEO_ID = "abcdefghijk"
CACHE_CONTENT = f"---\ntitle: Example\nyoutube_id: {VIDEO_ID}\n---\n\nNo captions.\n"


class BackfillDateTests(unittest.TestCase):
    def test_cookie_setting_controls_argv_and_preserves_date_backfill(self) -> None:
        cases = (
            (None, ["--cookies-from-browser", "chrome"]),
            ("", []),
            ("firefox", ["--cookies-from-browser", "firefox"]),
            ("firefox:Profile With Spaces", ["--cookies-from-browser", "firefox:Profile With Spaces"]),
        )
        for browser, cookie_args in cases:
            with self.subTest(browser=browser), tempfile.TemporaryDirectory() as tmp:
                cache_fp = Path(tmp) / f"{VIDEO_ID}.md"
                cache_fp.write_text(CACHE_CONTENT, encoding="utf-8")
                meta = {"title": "Example", "youtube_id": VIDEO_ID}
                env = {} if browser is None else {"YT_COOKIES_FROM_BROWSER": browser}
                response = subprocess.CompletedProcess([], 0, stdout="20261026\n", stderr="")

                with patch.dict(os.environ, env, clear=True), patch.object(
                    youtube_channels.subprocess, "run", return_value=response,
                ) as run:
                    youtube_channels.backfill_date(VIDEO_ID, meta, cache_fp)

                run.assert_called_once_with(
                    ["yt-dlp", "--print", "%(upload_date)s", "--skip-download", *cookie_args,
                     f"https://www.youtube.com/watch?v={VIDEO_ID}"],
                    stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=60,
                )
                self.assertEqual(meta, {"title": "Example", "youtube_id": VIDEO_ID, "date": "2026-10-26"})
                self.assertEqual(
                    cache_fp.read_text(encoding="utf-8"),
                    CACHE_CONTENT.replace("\nyoutube_id:", "\ndate: 2026-10-26\nyoutube_id:", 1),
                )

    def test_existing_date_does_not_call_subprocess_or_change_cache(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cache_fp = Path(tmp) / f"{VIDEO_ID}.md"
            content = CACHE_CONTENT.replace("\nyoutube_id:", "\ndate: 2025-01-02\nyoutube_id:", 1)
            cache_fp.write_text(content, encoding="utf-8")
            meta = {"title": "Example", "date": "2025-01-02"}

            with patch.object(youtube_channels.subprocess, "run", side_effect=AssertionError("unexpected fetch")) as run:
                youtube_channels.backfill_date(VIDEO_ID, meta, cache_fp)

            run.assert_not_called()
            self.assertEqual(meta, {"title": "Example", "date": "2025-01-02"})
            self.assertEqual(cache_fp.read_text(encoding="utf-8"), content)

    def test_failed_date_lookup_preserves_metadata_and_cache(self) -> None:
        for output in ("", "NA\n", "2026-10-26\n"):
            with self.subTest(output=output), tempfile.TemporaryDirectory() as tmp:
                cache_fp = Path(tmp) / f"{VIDEO_ID}.md"
                cache_fp.write_text(CACHE_CONTENT, encoding="utf-8")
                meta = {"title": "Example", "youtube_id": VIDEO_ID}
                response = subprocess.CompletedProcess([], 1, stdout=output, stderr="lookup failed")

                with patch.object(youtube_channels.subprocess, "run", return_value=response) as run:
                    youtube_channels.backfill_date(VIDEO_ID, meta, cache_fp)

                run.assert_called_once()
                self.assertEqual(meta, {"title": "Example", "youtube_id": VIDEO_ID})
                self.assertEqual(cache_fp.read_text(encoding="utf-8"), CACHE_CONTENT)


if __name__ == "__main__":
    unittest.main()
