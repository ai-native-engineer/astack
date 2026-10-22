import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/verify.sh"

@unittest.skipUnless(shutil.which("node"), "Node.js is needed for syntax checks")
class SyntaxModeTests(unittest.TestCase):
    def check_html(self, text):
        with tempfile.TemporaryDirectory() as folder:
            page = Path(folder) / "sheet with spaces.html"
            page.write_text(text, encoding="utf-8")
            run = subprocess.run(["/bin/bash", str(SCRIPT), "--syntax", str(page)], capture_output=True, text=True, check=False)
            return run.returncode, json.loads(run.stdout)

    def test_broken_embedded_newline_is_rejected(self):
        code, report = self.check_html("<script>const out='line one\nline two';</script>")
        self.assertEqual(code, 1)
        self.assertFalse(report["ok"])
        self.assertIn("SyntaxError", report["errors"][0]["message"])

    def test_escaped_newline_and_module_are_accepted_without_runtime_claim(self):
        code, report = self.check_html(r"<script type>const out='one\ntwo';</script><script type='module'>export const ok=true;</script>")
        self.assertEqual(code, 0)
        self.assertEqual(report["checked"], 2)
        self.assertEqual(report["runtime"], "not-checked")

    def test_external_dependency_is_not_silently_passed(self):
        code, report = self.check_html("<script src='https://example.invalid/private.js'></script><script>const x=1;</script>")
        self.assertEqual(code, 2)
        self.assertFalse(report["ok"])

    def test_no_javascript_is_unverified(self):
        code, report = self.check_html('<script type="application/json">{"a":1}</script><p>static</p>')
        self.assertEqual(code, 2)
        self.assertFalse(report["ok"])

if __name__ == "__main__":
    unittest.main()
