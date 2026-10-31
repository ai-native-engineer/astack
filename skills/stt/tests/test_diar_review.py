#!/usr/bin/env python3
"""Checks for scripts/diar_review.py against a fake run (no models needed)."""

import http.client
import json
import os
from pathlib import Path
import sys
import tempfile
import threading
import unittest

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

TRANSCRIPT = {"segments": [
    {"start": 0.0, "end": 2.0, "speaker": "SPEAKER_00", "text": "첫 번째"},
    {"start": 2.1, "end": 4.0, "speaker": "SPEAKER_01", "text": "두 번째"}],
    "gaps": [[4.0, 20.0]]}


class Review(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        os.environ["STT_VOICES"] = str(root / "voices.json")
        import voices
        import diar_review
        voices.STORE = Path(os.environ["STT_VOICES"])
        self.voices = voices
        self.run_dir = root / "run"
        self.run_dir.mkdir()
        self.audio = root / "talk.m4a"
        self.audio.write_bytes(bytes(range(10)))
        (self.run_dir / "transcript.json").write_text(json.dumps(TRANSCRIPT), encoding="utf-8")
        (self.run_dir / "speakers.json").write_text(json.dumps({
            "_recording": "r1",
            "SPEAKER_00": {"seconds": 20.0, "embedding": [1, 0]},
            "SPEAKER_01": {"seconds": 2.0, "embedding": [0, 1]}}), encoding="utf-8")
        (self.run_dir / "run.json").write_text(json.dumps({"audio": str(self.audio), "start": 30.0}),
                                               encoding="utf-8")
        self.server = diar_review.make_server(diar_review.Run(self.run_dir))
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.tmp.cleanup()
        del os.environ["STT_VOICES"]

    def request(self, method, path, body=None, token=True, headers=None):
        conn = http.client.HTTPConnection("127.0.0.1", self.server.server_port)
        query = f"?t={self.server.token}" if token else ""
        hdrs = {"Content-Type": "application/json"} if body is not None else {}
        hdrs.update(headers or {})
        conn.request(method, path + query, json.dumps(body) if body is not None else None, hdrs)
        res = conn.getresponse()
        data = res.read()
        conn.close()
        return res, data

    def state(self, method="GET", path="/api/state", body=None):
        res, data = self.request(method, path, body)
        return res.status, json.loads(data)

    def markdown(self):
        return (self.run_dir / "diarized.md").read_text(encoding="utf-8")

    def test_requests_need_token_and_local_host(self):
        self.assertEqual(self.request("GET", "/api/state", token=False)[0].status, 403)
        self.assertEqual(self.request("GET", "/api/state", headers={"Host": "evil.test"})[0].status, 403)
        self.assertEqual(self.request("GET", "/")[0].status, 200)

    def test_state_uses_source_times(self):
        _, state = self.state()
        self.assertEqual([(r["display"], r["start"]) for r in state["rows"]],
                         [("SPEAKER_00", 30.0), ("SPEAKER_01", 32.1)])
        self.assertTrue(state["audio"])
        self.assertEqual(state["speakers"][0]["sample"], [30.0, 32.0])

    def test_gaps_stay_in_transcript_but_not_in_rows(self):
        self.state("POST", "/api/name", {"label": "SPEAKER_00", "name": "민지", "remember": False})
        _, state = self.state()
        self.assertNotIn("gap", [r["label"] for r in state["rows"]])
        self.assertIn("**[gap]** (00:34~00:50)", self.markdown())

    def test_audio_supports_ranges_for_seeking(self):
        res, data = self.request("GET", "/audio", headers={"Range": "bytes=2-5"})
        self.assertEqual((res.status, data), (206, bytes([2, 3, 4, 5])))
        self.assertEqual(res.getheader("Content-Range"), "bytes 2-5/10")
        self.assertEqual(self.request("GET", "/audio", headers={"Range": "bytes=20-"})[0].status, 416)

    def test_naming_rewrites_transcript_and_remembers(self):
        status, state = self.state("POST", "/api/name", {"label": "SPEAKER_00", "name": "민지", "remember": True})
        self.assertEqual(status, 200)
        self.assertIn("**[민지]** (00:30) 첫 번째", self.markdown())
        self.assertEqual(state["voices"], [{"name": "민지", "count": 1}])
        self.assertEqual((self.run_dir / "names.json").stat().st_mode & 0o777, 0o600)

    def test_short_voice_is_named_here_but_not_remembered(self):
        status, state = self.state("POST", "/api/name", {"label": "SPEAKER_01", "name": "서준", "remember": True})
        self.assertEqual(status, 400)
        self.assertIn("짧아", state["error"])
        status, state = self.state("POST", "/api/name", {"label": "SPEAKER_01", "name": "서준", "remember": False})
        self.assertEqual(status, 200)
        self.assertIn("**[서준]**", self.markdown())
        self.assertEqual(state["voices"], [])
        self.assertFalse(next(s for s in state["speakers"] if s["label"] == "SPEAKER_01")["remember"])

    def test_same_name_merges_rows(self):
        self.state("POST", "/api/name", {"label": "SPEAKER_00", "name": "민지", "remember": False})
        _, state = self.state("POST", "/api/name", {"label": "SPEAKER_01", "name": "민지", "remember": False})
        self.assertEqual([r["text"] for r in state["rows"]], ["첫 번째 두 번째"])

    def test_bad_names_are_refused(self):
        for name in ("", "a]b", "x" * 41):
            status, _ = self.state("POST", "/api/name", {"label": "SPEAKER_00", "name": name})
            self.assertEqual(status, 400, name)
        status, _ = self.state("POST", "/api/name", {"label": "SPEAKER_09", "name": "민지"})
        self.assertEqual(status, 400)

    def test_clear_and_forget(self):
        self.state("POST", "/api/name", {"label": "SPEAKER_00", "name": "민지", "remember": True})
        _, state = self.state("POST", "/api/clear", {"label": "SPEAKER_00"})
        self.assertEqual(state["rows"][0]["display"], "SPEAKER_00")
        self.assertEqual(state["voices"], [{"name": "민지", "count": 1}])
        _, state = self.state("POST", "/api/forget", {"name": "민지"})
        self.assertEqual(state["voices"], [])

    def test_forget_drops_names_found_automatically(self):
        self.voices.enroll(self.run_dir, "SPEAKER_00", "민지")
        (self.run_dir / "names.json").write_text(json.dumps({
            "SPEAKER_00": {"name": "민지", "score": 0.8, "sure": True},
            "SPEAKER_01": {"name": "민지", "sure": True, "manual": True}}), encoding="utf-8")
        _, state = self.state("POST", "/api/forget", {"name": "민지"})
        self.assertEqual([r["display"] for r in state["rows"]], ["SPEAKER_00", "민지"])


if __name__ == "__main__":
    unittest.main()
