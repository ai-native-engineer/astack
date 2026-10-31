import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from test_reply_bridge import bridge


class HttpTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.store = bridge.Store(self.root / "state")
        media = self.root / "clip.mp4"
        media.write_bytes(b"0123456789")
        page = self.root / "page.html"
        page.write_text(f'<html><body><video src="{media.as_uri()}"></video></body></html>')
        self.artifact = self.store.register(page, "Test", "codex", "conversation", "test-server")
        self.process = None
        self.start()

    def start(self):
        self.process = subprocess.Popen([sys.executable, str(bridge.Path(bridge.__file__)), "--state-dir", str(self.store.root), "serve", "--preview"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(50):
            info = bridge.running(self.store)
            if info and info["pid"] == self.process.pid:
                self.origin = f'http://127.0.0.1:{info["port"]}'
                break
            time.sleep(0.05)
        else:
            self.fail("service did not start")
        with urlopen(self.origin + "/artifact/" + self.artifact["id"]) as response:
            page = response.read().decode()
        self.meta = json.loads(re.search(r'<script id="reply-meta" type="application/json">(.*?)</script>', page, re.S)[1])

    def tearDown(self):
        if self.process:
            self.process.terminate()
            self.process.wait(timeout=5)
        self.temp.cleanup()

    def post(self, body, origin=None, csrf=True, path="reply"):
        headers = {"Content-Type": "application/json", "Origin": origin or self.origin}
        if csrf:
            headers["X-Reply-CSRF"] = self.meta["csrf"]
        req = Request(self.origin + "/artifact/" + self.artifact["id"] + "/" + path, data=json.dumps(body).encode(), headers=headers)
        with urlopen(req) as response:
            return json.load(response)

    def test_cross_origin_and_missing_csrf_cannot_enqueue(self):
        body = dict(id="reply-http-one", text="hello")
        for options in [dict(origin="null"), dict(origin="https://example.invalid"), dict(csrf=False)]:
            with self.assertRaises(HTTPError) as caught:
                self.post(body, **options)
            self.assertEqual(caught.exception.code, 403)
            caught.exception.close()
        self.assertEqual(self.store.pending(), [])

    def test_preview_is_read_only_and_matches_the_delivered_packet(self):
        body = dict(id="reply-preview-one", text="추가 메모", items=[dict(id="R1", label="원문 질문", values=["우선 참고"])])
        preview = self.post(body, path="preview")
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM replies").fetchone()[0], 0)
        self.post(body)
        with self.store.connect() as db:
            row = db.execute("SELECT * FROM replies WHERE id=?", (body["id"],)).fetchone()
        self.assertEqual(preview["message"], bridge.reply_text(self.artifact, row))
        self.assertEqual(preview["characters"], len(preview["message"]))

    def test_connection_does_not_claim_preview_is_a_live_receiver(self):
        with urlopen(self.origin + "/artifact/" + self.artifact["id"] + "/connection") as response:
            info = json.load(response)
        self.assertEqual(info["state"], "preview")

    def test_focus_requires_post_origin_csrf_and_is_disabled_in_preview(self):
        for options in [dict(origin="null"), dict(origin="https://example.invalid"), dict(csrf=False)]:
            with self.assertRaises(HTTPError) as caught:
                self.post({}, path="focus", **options)
            self.assertEqual(caught.exception.code, 403)
            caught.exception.close()
        with self.assertRaises(HTTPError) as caught:
            self.post({}, path="focus")
        self.assertEqual(caught.exception.code, 409)
        caught.exception.close()
        with self.assertRaises(HTTPError) as caught:
            urlopen(self.origin + "/artifact/" + self.artifact["id"] + "/focus")
        self.assertEqual(caught.exception.code, 404)
        caught.exception.close()
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM replies").fetchone()[0], 0)

    def test_reply_survives_restart_at_same_url_and_duplicate_is_not_recreated(self):
        body = dict(id="reply-http-one", text="한국어 의견")
        self.assertEqual(self.post(body)["state"], "held")
        origin = self.origin
        self.process.terminate(); self.process.wait(timeout=5)
        self.start()
        self.assertEqual(self.origin, origin)
        self.assertEqual(self.post(body)["id"], "reply-http-one")
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM replies").fetchone()[0], 1)

    def test_media_seeking_and_arbitrary_paths(self):
        key = next(iter(json.loads(self.artifact["media"])))
        req = Request(self.origin + f'/media/{self.artifact["id"]}/{key}', headers={"Range": "bytes=2-5"})
        with urlopen(req) as response:
            self.assertEqual(response.status, 206)
            self.assertEqual(response.read(), b"2345")
        with self.assertRaises(HTTPError) as caught:
            urlopen(self.origin + f'/media/{self.artifact["id"]}/not-registered')
        caught.exception.close()

    def test_stop_targets_recorded_process_and_retains_replies(self):
        self.post(dict(id="reply-http-stop", text="retain this"))
        result = subprocess.run([sys.executable, str(bridge.Path(bridge.__file__)), "--state-dir", str(self.store.root), "stop"], capture_output=True, text=True, check=True)
        self.assertTrue(json.loads(result.stdout)["stop_requested"])
        self.process.wait(timeout=5)
        self.process = None
        self.assertEqual(self.store.reply("reply-http-stop", self.artifact["id"])["state"], "held")


if __name__ == "__main__":
    unittest.main()
