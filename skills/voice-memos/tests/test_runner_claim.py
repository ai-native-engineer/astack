import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock


RUNNER = Path(__file__).resolve().parents[1] / "scripts" / "run.sh"


def failing_runtime(root: Path) -> Path:
    """run.sh가 pending 큐 claim에서 실패하도록 준비하고 runtime 경로를 준다."""
    runtime = root / "runtime"
    (runtime / "run-queue" / "pending").mkdir(parents=True)

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
    return runtime


def quiet_env(root: Path, runtime: Path, **extra) -> dict:
    """run.sh의 실패 알림 경로를 막은 환경. cleanup 은 --skip-notify 와 무관하게
    종료 코드가 0이 아니면 Telegram 으로 발송하고, 게이트는 아래 두 변수뿐이다."""
    return {
        **os.environ,
        "HOME": str(root),
        "VOICE_MEMOS_CONFIG_FILE": str(root / "absent.env"),
        "TELEGRAM_BOT_TOKEN": "",
        "TELEGRAM_CHAT_ID": "",
        "VOICE_MEMOS_RUNTIME_DIR": str(runtime),
        "VOICE_MEMOS_PYTHON": "/usr/bin/true",
        "VOICE_MEMOS_UV": "/usr/bin/true",
        **extra,
    }


class RunnerClaimTest(unittest.TestCase):
    def test_pending_claim_failure_is_named_and_nonzero(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            runtime = failing_runtime(root)

            result = subprocess.run(
                ["/bin/bash", str(RUNNER), "--skip-notify"],
                env=quiet_env(root, runtime),
                capture_output=True,
                text=True,
                timeout=5,
            )

            log = (runtime / "logs" / "watcher.log").read_text(encoding="utf-8")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("PendingQueueClaimError", log)
            self.assertNotIn(str(runtime), log)
            self.assertTrue((runtime / "run-queue" / "pending").is_dir())

    def test_inherited_telegram_tokens_do_not_trigger_a_real_send(self):
        """토큰이 셸에 export 돼 있어도 테스트 환경이 발송을 막는지 고정한다.

        막지 못하면 테스트가 깨질 때마다 사용자 채팅으로 실제 알림이 나간다.
        """
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            runtime = failing_runtime(root)

            calls = root / "curl-calls"
            fake_curl = root / "fake-curl"
            fake_curl.write_text(
                f'#!/bin/bash\necho "$@" >> {calls}\n', encoding="utf-8"
            )
            fake_curl.chmod(0o755)

            # 부모 셸에 진짜 토큰이 있는 상황을 흉내낸 뒤, 하네스 조합이 이를 덮는지 본다.
            with mock.patch.dict(
                os.environ,
                {"TELEGRAM_BOT_TOKEN": "inherited", "TELEGRAM_CHAT_ID": "42"},
                clear=False,
            ):
                result = subprocess.run(
                    ["/bin/bash", str(RUNNER), "--skip-notify"],
                    env=quiet_env(root, runtime, VOICE_MEMOS_CURL=str(fake_curl)),
                    capture_output=True,
                    text=True,
                    timeout=5,
                )

            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(calls.exists(), f"outbound call attempted: {calls}")


if __name__ == "__main__":
    unittest.main()
