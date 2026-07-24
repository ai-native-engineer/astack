import os
import subprocess
import tempfile
import unittest
from pathlib import Path


RUNNER = Path(__file__).resolve().parents[1] / "scripts" / "run.sh"


class RunnerClaimTest(unittest.TestCase):
    def test_pending_claim_failure_is_named_and_nonzero(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            runtime = root / "runtime"
            pending = runtime / "run-queue" / "pending"
            pending.mkdir(parents=True)

            bin_dir = root / "scripts"
            bin_dir.mkdir()
            fake_mv = bin_dir / "mv"
            fake_mv.write_text(
                """#!/bin/bash
case "$1" in
    */run-queue/pending) exit 73 ;;
esac
exec /bin/mv "$@"
""",
                encoding="utf-8",
            )
            fake_mv.chmod(0o755)

            result = subprocess.run(
                ["/bin/bash", str(RUNNER), "--skip-notify"],
                env={
                    **os.environ,
                    "HOME": str(root),
                    "VOICE_MEMOS_RUNTIME_DIR": str(runtime),
                    "VOICE_MEMOS_PYTHON": "/usr/bin/true",
                    "VOICE_MEMOS_UV": "/usr/bin/true",
                },
                capture_output=True,
                text=True,
                timeout=5,
            )

            log = (runtime / "logs" / "watcher.log").read_text(encoding="utf-8")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("PendingQueueClaimError", log)
            self.assertNotIn(str(runtime), log)
            self.assertTrue(pending.is_dir())


if __name__ == "__main__":
    unittest.main()
