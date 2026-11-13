"""Redaction must not leave secrets more readable than it found them."""

from __future__ import annotations

import argparse
import contextlib
import io
import os
import stat
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import session_history as cli  # noqa: E402

SECRET = "sk-" + "A" * 40


def mode(path: Path) -> int:
    return stat.S_IMODE(path.stat().st_mode)


class TestRedactPermissions(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        # the common default; the bug only shows when umask widens new files
        self._umask = os.umask(0o022)
        self.log = self.root / "session.jsonl"
        self.log.write_text(f'{{"text": "key {SECRET}"}}\n', encoding="utf-8")
        self.log.chmod(0o600)
        self.backup = self.root / "state" / "redact.tar.gz"

    def tearDown(self):
        os.umask(self._umask)
        self._tmp.cleanup()

    def redact(self):
        args = argparse.Namespace(
            tool="claude",
            path=[str(self.log)],
            exclude=[],
            apply=True,
            backup=str(self.backup),
        )
        with (
            mock.patch.object(cli, "collect_sources", return_value=[]),
            contextlib.redirect_stdout(io.StringIO()),
            contextlib.redirect_stderr(io.StringIO()),
        ):
            cli.cmd_redact(args)

    def test_rewrite_keeps_the_original_file_mode(self):
        self.redact()
        self.assertNotIn(SECRET, self.log.read_text(encoding="utf-8"))
        self.assertEqual(mode(self.log), 0o600)

    def test_existing_tmp_is_preserved_and_write_stays_private(self):
        self.log.chmod(0o640)
        original = self.log.read_bytes()
        existing_tmp = self.log.with_suffix(self.log.suffix + ".tmp")
        existing_tmp.write_bytes(b"unrelated temporary data")
        existing_tmp.chmod(0o644)
        existing_inode = existing_tmp.stat().st_ino
        real_tempfile = tempfile.NamedTemporaryFile
        real_chmod = os.chmod
        created = []
        write_modes = []

        def observe_tempfile(*args, **kwargs):
            fh = real_tempfile(*args, **kwargs)
            created.append(fh)
            write = fh.write

            def observe_write(text):
                write_modes.append(stat.S_IMODE(os.fstat(fh.fileno()).st_mode))
                result = write(text)
                write_modes.append(stat.S_IMODE(os.fstat(fh.fileno()).st_mode))
                return result

            fh.write = observe_write
            return fh

        def restore_mode(path, permissions):
            self.assertEqual(len(created), 1)
            self.assertTrue(created[0].closed)
            self.assertEqual(mode(path), 0o600)
            self.assertEqual(
                path.read_text(encoding="utf-8"),
                '{"text": "key [REDACTED_API_KEY]"}\n',
            )
            self.assertEqual(self.log.read_bytes(), original)
            real_chmod(path, permissions)

        with (
            mock.patch.object(
                cli.tempfile, "NamedTemporaryFile", side_effect=observe_tempfile
            ),
            mock.patch.object(cli.os, "chmod", side_effect=restore_mode),
        ):
            self.redact()

        self.assertEqual(write_modes, [0o600, 0o600])
        owned_tmp = Path(created[0].name)
        self.assertEqual(owned_tmp.parent.resolve(), self.log.parent.resolve())
        self.assertNotEqual(owned_tmp, existing_tmp)
        self.assertFalse(owned_tmp.exists())
        self.assertEqual(mode(self.log), 0o640)
        self.assertTrue(stat.S_ISREG(self.log.lstat().st_mode))
        self.assertNotIn(SECRET, self.log.read_text(encoding="utf-8"))
        self.assertEqual(existing_tmp.read_bytes(), b"unrelated temporary data")
        self.assertEqual(mode(existing_tmp), 0o644)
        self.assertEqual(existing_tmp.stat().st_ino, existing_inode)
        self.assertEqual(
            set(self.root.iterdir()), {self.log, existing_tmp, self.backup.parent}
        )

    def test_existing_tmp_symlink_and_its_target_are_untouched(self):
        victim = self.root / "unrelated.txt"
        victim.write_bytes(b"unrelated original data")
        victim.chmod(0o644)
        victim_inode = victim.stat().st_ino
        existing_tmp = self.log.with_suffix(self.log.suffix + ".tmp")
        existing_tmp.symlink_to(victim)

        self.redact()

        self.assertTrue(stat.S_ISREG(self.log.lstat().st_mode))
        self.assertNotIn(SECRET, self.log.read_text(encoding="utf-8"))
        self.assertEqual(mode(self.log), 0o600)
        self.assertTrue(existing_tmp.is_symlink())
        self.assertEqual(existing_tmp.readlink(), victim)
        self.assertEqual(victim.read_bytes(), b"unrelated original data")
        self.assertEqual(mode(victim), 0o644)
        self.assertEqual(victim.stat().st_ino, victim_inode)
        self.assertEqual(
            set(self.root.iterdir()),
            {self.log, existing_tmp, victim, self.backup.parent},
        )

    def test_write_failure_preserves_original_and_cleans_only_owned_tmp(self):
        original = self.log.read_bytes()
        original_inode = self.log.stat().st_ino
        existing_tmp = self.log.with_suffix(self.log.suffix + ".tmp")
        existing_tmp.write_bytes(b"unrelated temporary data")
        existing_tmp.chmod(0o644)
        existing_inode = existing_tmp.stat().st_ino
        real_tempfile = tempfile.NamedTemporaryFile
        created = []

        def failing_tempfile(*args, **kwargs):
            fh = real_tempfile(*args, **kwargs)
            created.append(fh)
            write = fh.write

            def fail_write(text):
                write(text[:10])
                fh.flush()
                self.assertEqual(mode(Path(fh.name)), 0o600)
                raise OSError("injected write failure")

            fh.write = fail_write
            return fh

        with (
            mock.patch.object(
                cli.tempfile, "NamedTemporaryFile", side_effect=failing_tempfile
            ),
            self.assertRaisesRegex(OSError, "injected write failure"),
        ):
            self.redact()

        self.assertEqual(len(created), 1)
        self.assertTrue(created[0].closed)
        self.assertFalse(Path(created[0].name).exists())
        self.assertEqual(self.log.read_bytes(), original)
        self.assertEqual(self.log.stat().st_ino, original_inode)
        self.assertEqual(mode(self.log), 0o600)
        self.assertTrue(stat.S_ISREG(self.log.lstat().st_mode))
        self.assertEqual(existing_tmp.read_bytes(), b"unrelated temporary data")
        self.assertEqual(mode(existing_tmp), 0o644)
        self.assertEqual(existing_tmp.stat().st_ino, existing_inode)
        with tarfile.open(self.backup) as tar:
            member = tar.getmember(str(self.log).lstrip("/"))
            self.assertEqual(tar.extractfile(member).read(), original)
        self.assertEqual(
            set(self.root.iterdir()), {self.log, existing_tmp, self.backup.parent}
        )

    def test_replace_failure_preserves_original_and_cleans_only_owned_tmp(self):
        self.log.chmod(0o640)
        original = self.log.read_bytes()
        original_inode = self.log.stat().st_ino
        victim = self.root / "unrelated.txt"
        victim.write_bytes(b"unrelated original data")
        victim.chmod(0o644)
        victim_inode = victim.stat().st_ino
        existing_tmp = self.log.with_suffix(self.log.suffix + ".tmp")
        existing_tmp.symlink_to(victim)
        created = []

        def fail_replace(tmp, destination):
            created.append(tmp)
            self.assertEqual(destination, self.log)
            self.assertEqual(tmp.parent.resolve(), self.log.parent.resolve())
            self.assertNotEqual(tmp, existing_tmp)
            self.assertTrue(stat.S_ISREG(tmp.lstat().st_mode))
            self.assertEqual(mode(tmp), 0o640)
            self.assertEqual(
                tmp.read_text(encoding="utf-8"),
                '{"text": "key [REDACTED_API_KEY]"}\n',
            )
            self.assertEqual(self.log.read_bytes(), original)
            raise OSError("injected replace failure")

        with (
            mock.patch.object(Path, "replace", autospec=True, side_effect=fail_replace),
            self.assertRaisesRegex(OSError, "injected replace failure"),
        ):
            self.redact()

        self.assertEqual(len(created), 1)
        self.assertFalse(created[0].exists())
        self.assertEqual(self.log.read_bytes(), original)
        self.assertEqual(self.log.stat().st_ino, original_inode)
        self.assertEqual(mode(self.log), 0o640)
        self.assertTrue(stat.S_ISREG(self.log.lstat().st_mode))
        self.assertTrue(existing_tmp.is_symlink())
        self.assertEqual(existing_tmp.readlink(), victim)
        self.assertEqual(victim.read_bytes(), b"unrelated original data")
        self.assertEqual(mode(victim), 0o644)
        self.assertEqual(victim.stat().st_ino, victim_inode)
        with tarfile.open(self.backup) as tar:
            member = tar.getmember(str(self.log).lstrip("/"))
            self.assertEqual(tar.extractfile(member).read(), original)
        self.assertEqual(
            set(self.root.iterdir()),
            {self.log, existing_tmp, victim, self.backup.parent},
        )

    def test_backup_of_unmasked_originals_is_owner_only(self):
        self.redact()
        self.assertEqual(mode(self.backup), 0o600)
        self.assertEqual(mode(self.backup.parent), 0o700)
        # the backup exists for rollback, so it must still restore the original
        with tarfile.open(self.backup) as tar:
            member = tar.getmember(str(self.log).lstrip("/"))
            self.assertIn(SECRET, tar.extractfile(member).read().decode("utf-8"))

    def test_existing_backup_is_never_overwritten(self):
        self.backup.parent.mkdir()
        self.backup.write_bytes(b"earlier backup")
        with self.assertRaises(SystemExit):
            self.redact()
        self.assertEqual(self.backup.read_bytes(), b"earlier backup")
        self.assertIn(SECRET, self.log.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
