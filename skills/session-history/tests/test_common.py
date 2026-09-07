"""Unit tests for shared session-history path behavior."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from common import HOME, path_matches


class TestPathMatches(unittest.TestCase):
    def test_matches_same_parent_and_child_paths(self):
        self.assertTrue(path_matches("/tmp/work", "/tmp/work"))
        self.assertTrue(path_matches("/tmp/work/app", "/tmp/work"))
        self.assertTrue(path_matches("/tmp/work", "/tmp/work/app"))

    def test_does_not_prefix_match_sibling_names(self):
        self.assertFalse(path_matches("/tmp/work", "/tmp/work-copy"))
        self.assertFalse(path_matches("/tmp/work-copy", "/tmp/work"))

    def test_excludes_home_project(self):
        self.assertFalse(path_matches(str(HOME), str(HOME / "project")))

    def test_resolves_symlink_aliases(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            actual = root / "actual"
            actual.mkdir()
            alias = root / "alias"
            alias.symlink_to(actual, target_is_directory=True)
            self.assertTrue(path_matches(str(actual), str(alias)))

    def test_rejects_missing_or_relative_values(self):
        self.assertFalse(path_matches("", "/tmp/work"))
        self.assertFalse(path_matches("/tmp/work", "relative/path"))


if __name__ == "__main__":
    unittest.main()
