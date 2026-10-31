#!/usr/bin/env python3
"""Checks for scripts/voices.py with a throwaway store (no models needed)."""

import contextlib
import importlib.util
import io
import json
import math
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "voices.py"


def unit(angle: float) -> list[float]:
    """A 2-D voice whose cosine with unit(0) is cos(angle)."""
    return [math.cos(angle), math.sin(angle)]


def at(similarity: float) -> list[float]:
    return unit(math.acos(similarity))


class Voices(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        with mock.patch.dict(os.environ, {"STT_VOICES": str(self.root / "store" / "voices.json")}):
            spec = importlib.util.spec_from_file_location("voices", SCRIPT)
            self.v = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(self.v)

    def run_dir(self, name: str, speakers: dict) -> Path:
        path = self.root / name
        path.mkdir()
        data = {"_recording": name}
        data.update({label: {"seconds": seconds, "embedding": emb}
                     for label, (seconds, emb) in speakers.items()})
        (path / "speakers.json").write_text(json.dumps(data), encoding="utf-8")
        return path

    def call(self, *args) -> int:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return self.v.main(["voices.py", *map(str, args)])

    def names(self, run: Path) -> dict:
        return json.loads((run / "names.json").read_text(encoding="utf-8"))

    def test_write_private_new_and_replaced_files_stay_private(self):
        path = self.root / "output" / "names.json"
        staged = []
        dump = json.dump

        def check_dump(data, out, **kwargs):
            temporary = Path(out.name)
            self.assertEqual(temporary.parent, path.parent)
            self.assertNotEqual(temporary, path.with_name(path.name + ".tmp"))
            self.assertNotIn(temporary, staged)
            staged.append(temporary)
            self.assertEqual(os.fstat(out.fileno()).st_mode & 0o777, 0o600)
            dump(data, out, **kwargs)
            out.flush()
            self.assertEqual(temporary.stat().st_mode & 0o777, 0o600)
            self.assertEqual(json.loads(temporary.read_text(encoding="utf-8")), data)

        with mock.patch.object(self.v.json, "dump", side_effect=check_dump):
            for name in ("민지", "서준"):
                with self.subTest(name=name):
                    if path.exists():
                        path.chmod(0o644)
                    data = {"name": name}
                    self.v.write_private(path, data)
                    self.assertEqual(json.loads(path.read_text(encoding="utf-8")), data)
                    self.assertEqual(path.stat().st_mode & 0o777, 0o600)
                    self.assertEqual(set(path.parent.iterdir()), {path})
        self.assertEqual(len(staged), 2)

    def test_write_private_leaves_preexisting_public_tmp_untouched(self):
        path = self.root / "names.json"
        fixed = path.with_name(path.name + ".tmp")
        fixed.write_bytes(b"unrelated temporary data\n")
        fixed.chmod(0o644)
        inode = fixed.stat().st_ino

        self.v.write_private(path, {"name": "민지"})

        self.assertTrue(fixed.is_file(), "Unrelated fixed temporary file must remain")
        self.assertEqual(fixed.read_bytes(), b"unrelated temporary data\n")
        self.assertEqual(fixed.stat().st_mode & 0o777, 0o644)
        self.assertEqual(fixed.stat().st_ino, inode)
        self.assertEqual(json.loads(path.read_text(encoding="utf-8")), {"name": "민지"})
        self.assertEqual(path.stat().st_mode & 0o777, 0o600)
        self.assertEqual(set(self.root.iterdir()), {path, fixed})

    def test_write_private_does_not_follow_fixed_tmp_symlink(self):
        path = self.root / "names.json"
        fixed = path.with_name(path.name + ".tmp")
        victim = self.root / "victim.json"
        victim.write_bytes(b"unrelated target data\n")
        victim.chmod(0o644)
        inode = victim.stat().st_ino
        fixed.symlink_to(victim)

        self.v.write_private(path, {"name": "민지"})

        self.assertTrue(fixed.is_symlink())
        self.assertEqual(fixed.readlink(), victim)
        self.assertEqual(victim.read_bytes(), b"unrelated target data\n")
        self.assertEqual(victim.stat().st_mode & 0o777, 0o644)
        self.assertEqual(victim.stat().st_ino, inode)
        self.assertEqual(json.loads(path.read_text(encoding="utf-8")), {"name": "민지"})
        self.assertEqual(path.stat().st_mode & 0o777, 0o600)
        self.assertEqual(set(self.root.iterdir()), {path, fixed, victim})

    def test_write_private_failures_preserve_original_and_unrelated_files(self):
        make_temp = tempfile.NamedTemporaryFile
        for stage in ("serialization", "write", "close", "replace"):
            for fixed_kind in ("file", "symlink"):
                with self.subTest(stage=stage, fixed_kind=fixed_kind):
                    parent = self.root / f"{stage}-{fixed_kind}"
                    parent.mkdir()
                    path = parent / "names.json"
                    path.write_bytes(b"original data\n")
                    path.chmod(0o644)
                    original_inode = path.stat().st_ino
                    fixed = path.with_name(path.name + ".tmp")
                    unrelated = fixed if fixed_kind == "file" else parent / "victim.json"
                    unrelated.write_bytes(b"unrelated data\n")
                    unrelated.chmod(0o644)
                    unrelated_inode = unrelated.stat().st_ino
                    if fixed_kind == "symlink":
                        fixed.symlink_to(unrelated)
                    before = set(parent.iterdir())
                    staged = []
                    handles = []

                    def open_temp(*args, **kwargs):
                        out = make_temp(*args, **kwargs)
                        staged.append(Path(out.name))
                        handles.append(out)
                        if stage == "write":
                            write = out.write

                            def fail_write(text):
                                write(text)
                                out.flush()
                                self.assertTrue(Path(out.name).read_bytes())
                                self.assertEqual(os.fstat(out.fileno()).st_mode & 0o777, 0o600)
                                raise OSError("write failed")

                            out.write = fail_write
                        elif stage == "close":
                            class CloseFailure:
                                def __getattr__(self, name):
                                    return getattr(out, name)

                                def __enter__(self):
                                    out.__enter__()
                                    return self

                                def __exit__(self, *exc):
                                    out.__exit__(*exc)
                                    raise OSError("close failed")

                            return CloseFailure()
                        return out

                    data = {"name": "민지"}
                    if stage == "serialization":
                        data["unsupported"] = object()
                    error = TypeError if stage == "serialization" else OSError
                    message = "not JSON serializable" if stage == "serialization" else f"{stage} failed"
                    with contextlib.ExitStack() as stack:
                        stack.enter_context(mock.patch.object(self.v.tempfile, "NamedTemporaryFile",
                                                              side_effect=open_temp))
                        if stage == "replace":
                            stack.enter_context(mock.patch.object(self.v.os, "replace",
                                                                  side_effect=OSError(message)))
                        with self.assertRaisesRegex(error, message):
                            self.v.write_private(path, data)

                    self.assertEqual(len(staged), 1)
                    self.assertFalse(staged[0].exists())
                    self.assertTrue(handles[0].closed)
                    self.assertEqual(set(parent.iterdir()), before)
                    self.assertEqual(path.read_bytes(), b"original data\n")
                    self.assertEqual(path.stat().st_mode & 0o777, 0o644)
                    self.assertEqual(path.stat().st_ino, original_inode)
                    self.assertEqual(unrelated.read_bytes(), b"unrelated data\n")
                    self.assertEqual(unrelated.stat().st_mode & 0o777, 0o644)
                    self.assertEqual(unrelated.stat().st_ino, unrelated_inode)
                    if fixed_kind == "symlink":
                        self.assertTrue(fixed.is_symlink())
                        self.assertEqual(fixed.readlink(), unrelated)

    def test_match_writes_and_replaces_private_names(self):
        self.call("enroll", self.run_dir("r1", {"SPEAKER_00": (60, unit(0))}), "SPEAKER_00", "민지")
        run = self.run_dir("p", {"SPEAKER_00": (30, unit(0))})
        path = run / "names.json"
        for existing in (False, True):
            with self.subTest(existing=existing):
                if existing:
                    path.write_text("{}", encoding="utf-8")
                    path.chmod(0o644)
                with contextlib.redirect_stderr(io.StringIO()):
                    self.assertEqual(self.v.match(run), 0)
                self.assertEqual(self.names(run), {"SPEAKER_00": {"name": "민지", "score": 1.0, "sure": True}})
                self.assertEqual(path.stat().st_mode & 0o777, 0o600)
                self.assertEqual(set(run.iterdir()), {run / "speakers.json", path})

    def test_only_named_speakers_are_stored_privately(self):
        run = self.run_dir("r1", {"SPEAKER_00": (20, unit(0)), "SPEAKER_01": (20, unit(1.5))})
        self.assertEqual(self.call("enroll", run, "SPEAKER_00", "민지"), 0)
        store = json.loads(self.v.STORE.read_text(encoding="utf-8"))
        self.assertEqual([(s["name"], s["speaker"]) for s in store["voices"]], [("민지", "SPEAKER_00")])
        self.assertEqual(self.v.STORE.stat().st_mode & 0o777, 0o600)

    def test_short_speech_is_not_enrolled(self):
        run = self.run_dir("r1", {"SPEAKER_00": (2, unit(0))})
        with self.assertRaises(SystemExit):
            self.call("enroll", run, "SPEAKER_00", "민지")
        self.assertFalse(self.v.STORE.exists())

    def test_thresholds_name_suggest_or_leave(self):
        self.call("enroll", self.run_dir("r1", {"SPEAKER_00": (60, unit(0))}), "SPEAKER_00", "민지")
        for similarity, expected in ((0.75, True), (0.65, False), (0.55, None)):
            run = self.run_dir(f"p{similarity}", {"SPEAKER_00": (30, at(similarity))})
            self.call("match", run)
            hit = self.names(run).get("SPEAKER_00")
            self.assertEqual(hit and hit["sure"], expected, similarity)

    def test_close_second_name_blocks_the_match(self):
        self.call("enroll", self.run_dir("r1", {"SPEAKER_00": (60, unit(0))}), "SPEAKER_00", "민지")
        self.call("enroll", self.run_dir("r2", {"SPEAKER_00": (60, unit(0.2))}), "SPEAKER_00", "서준")
        run = self.run_dir("p", {"SPEAKER_00": (30, unit(0.1))})
        self.call("match", run)
        self.assertEqual(self.names(run), {})

    def test_one_name_per_speaker(self):
        self.call("enroll", self.run_dir("r1", {"SPEAKER_00": (60, unit(0))}), "SPEAKER_00", "민지")
        run = self.run_dir("p", {"SPEAKER_00": (30, unit(0.05)), "SPEAKER_01": (30, unit(0.1))})
        self.call("match", run)
        self.assertEqual({k: v["name"] for k, v in self.names(run).items()}, {"SPEAKER_00": "민지"})

    def test_samples_per_name_are_capped(self):
        for index in range(self.v.MAX_EXEMPLARS + 2):
            run = self.run_dir(f"r{index}", {"SPEAKER_00": (10 + index, unit(0))})
            self.call("enroll", run, "SPEAKER_00", "민지")
        store = json.loads(self.v.STORE.read_text(encoding="utf-8"))
        self.assertEqual(len(store["voices"]), self.v.MAX_EXEMPLARS)
        self.assertNotIn(10, [s["seconds"] for s in store["voices"]])

    def test_forget_removes_every_sample(self):
        for index in range(2):
            self.call("enroll", self.run_dir(f"r{index}", {"SPEAKER_00": (20, unit(0))}), "SPEAKER_00", "민지")
        self.assertEqual(self.call("forget", "민지"), 0)
        self.assertEqual(json.loads(self.v.STORE.read_text(encoding="utf-8"))["voices"], [])
        self.assertEqual(self.call("forget", "민지"), 1)


if __name__ == "__main__":
    unittest.main()
