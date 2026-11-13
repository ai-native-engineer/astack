#!/usr/bin/env python3
"""Offline checks for korean-proofread.sh output handling, using a fake omp on PATH."""

from pathlib import Path
import os
import subprocess
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "korean-proofread.sh"
MACHINE_CONFIG = Path.home() / ".agents" / "scripts" / "machine-config.sh"


class KoreanProofreadTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        bin_dir = self.tmp / "bin"
        bin_dir.mkdir()
        self.fake_omp = bin_dir / "omp"
        scripts_dir = self.tmp / "agents" / "scripts"
        scripts_dir.mkdir(parents=True)
        (scripts_dir / "machine-config.sh").symlink_to(MACHINE_CONFIG)
        (self.tmp / "agents" / "machine.env.example").write_text("", encoding="utf-8")
        self.config = self.tmp / "machine.env"
        self.config.write_text("HUMANIZE_KOREAN_PROOFREAD_MODEL=fake/model:medium\n", encoding="utf-8")
        self.env = {
            **os.environ,
            "PATH": f"{bin_dir}:{os.environ['PATH']}",
            "AGENTS_HOME": str(self.tmp / "agents"),
            "AGENTS_MACHINE_CONFIG": str(self.config),
        }

    def write_fake_omp(self, stdout: str, stderr: str = "", code: int = 0):
        self.fake_omp.write_text(
            "#!/usr/bin/env bash\n"
            f"printf %s {self.quote(stdout)}\n"
            f"printf %s {self.quote(stderr)} >&2\n"
            f"exit {code}\n",
            encoding="utf-8",
        )
        self.fake_omp.chmod(0o755)

    @staticmethod
    def quote(text: str) -> str:
        return "$'" + text.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n") + "'"

    def run_script(self, draft: str = "초안입니다.\n"):
        return subprocess.run(
            ["bash", str(SCRIPT)], input=draft, capture_output=True, text=True, env=self.env, timeout=30
        )

    def test_drops_leading_blank_lines_but_keeps_first_line_indent(self):
        self.write_fake_omp("\n\n    code\n본문\n", stderr="Working...\n")
        result = self.run_script()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "    code\n본문\n")

    def test_model_failure_skips_with_empty_stdout(self):
        self.write_fake_omp("부분 출력", stderr="Working...\n429 day limit\n", code=1)
        result = self.run_script()
        self.assertEqual(result.returncode, 3)
        self.assertEqual(result.stdout, "")
        self.assertIn("429 day limit", result.stderr)

    def test_missing_model_key_skips(self):
        self.write_fake_omp("호출되면 안 됨")
        self.config.write_text("", encoding="utf-8")
        result = self.run_script()
        self.assertEqual(result.returncode, 3)
        self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
