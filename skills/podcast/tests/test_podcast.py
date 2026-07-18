#!/usr/bin/env python3

import importlib.util
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree


SKILL = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("gen_feed", SKILL / "scripts/gen_feed.py")
GEN_FEED = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GEN_FEED)


class PodcastTest(unittest.TestCase):
    def setUp(self):
        self.show = {
            "title": "Test Show",
            "description": "Test description",
            "email": "podcast@example.com",
        }

    def episode(self, number, date, description="Summary"):
        return {
            "title": f"Episode {number}",
            "description": description,
            "audio_url": f"https://example.com/ep{number}.mp3",
            "length": 10,
            "duration": 1,
            "pubDate": date,
            "guid": f"tag:example.com,2026:episode:{number}",
            "episode": number,
        }

    def test_feed_sorts_dates_and_formats_show_notes(self):
        notes = (
            "Opening summary\n\n이번 주 다룬 이야기\n[01:05] Topic\n\n"
            "참고 링크\nSource: https://example.com/a?x=1&y=2\n\nSafe ]]> text"
        )
        feed = GEN_FEED.build(
            self.show,
            [
                self.episode(1, "Tue, 23 Jun 2026 15:11:30 +0900"),
                self.episode(2, "Mon, 29 Jun 2026 09:24:28 +0900", notes),
            ],
        )
        self.assertLess(feed.index("Episode 2"), feed.index("Episode 1"))
        self.assertIn("<li>00:01:05 Topic</li>", feed)
        self.assertIn('<a href="https://example.com/a?x=1&amp;y=2">Source</a>', feed)
        self.assertIn("<content:encoded>", feed)
        ElementTree.fromstring(feed)

    @unittest.skipUnless(
        shutil.which("ffmpeg") and shutil.which("ffprobe"),
        "requires ffmpeg and ffprobe",
    )
    def test_chapter_ts_accumulates_chunk_starts(self):
        with tempfile.TemporaryDirectory() as directory:
            chunks = Path(directory) / "chunks"
            chunks.mkdir()
            for index in (1, 2, 3):
                subprocess.run(
                    [
                        "ffmpeg", "-loglevel", "error", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
                        "-t", "1", str(chunks / f"norm_{index:04d}.wav"),
                    ],
                    check=True,
                )
            result = subprocess.run(
                [
                    "python3", str(SKILL / "scripts/chapter_ts.py"),
                    "--proj", directory, "--lines", "1,3",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertIn("00:00:00 line 1", result.stdout)
            self.assertIn("00:00:02 line 3", result.stdout)
            self.assertIn("total 00:00:03", result.stdout)

    @unittest.skipUnless(
        shutil.which("ffmpeg") and shutil.which("ffprobe") and shutil.which("git"),
        "requires ffmpeg, ffprobe, and git",
    )
    def test_publish_dry_run_uses_max_episode_without_changes(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            (repo / "show.json").write_text(json.dumps(self.show), encoding="utf-8")
            episodes = [self.episode(4, "Mon, 29 Jun 2026 09:24:28 +0900")]
            (repo / "episodes.json").write_text(json.dumps(episodes), encoding="utf-8")
            (repo / "feed.xml").write_text("old feed\n", encoding="utf-8")
            audio = repo / "audio.mp3"
            subprocess.run(
                [
                    "ffmpeg", "-loglevel", "error", "-f", "lavfi", "-i", "anullsrc",
                    "-t", "0.1", "-codec:a", "libmp3lame", str(audio),
                ],
                check=True,
            )
            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            subprocess.run(["git", "-C", str(repo), "config", "user.email", "test@example.com"], check=True)
            subprocess.run(["git", "-C", str(repo), "config", "user.name", "Test"], check=True)
            subprocess.run(
                ["git", "-C", str(repo), "remote", "add", "origin", "https://github.com/example/show.git"],
                check=True,
            )
            subprocess.run(["git", "-C", str(repo), "add", "show.json", "episodes.json", "feed.xml"], check=True)
            subprocess.run(["git", "-C", str(repo), "commit", "-q", "-m", "initial"], check=True)

            result = subprocess.run(
                [
                    str(SKILL / "scripts/publish.sh"), "--repo", str(repo), "--audio", str(audio),
                    "--title", "New episode", "--desc", "Notes", "--dry-run",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertIn("ep5", result.stdout)
            self.assertEqual(json.loads((repo / "episodes.json").read_text()), episodes)
            self.assertEqual((repo / "feed.xml").read_text(), "old feed\n")


if __name__ == "__main__":
    unittest.main()
