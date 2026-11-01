import io
import json
import sys
import unittest
import urllib.error
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import notify  # noqa: E402


def long_summary() -> str:
    """4096자를 넘기고, 잘리는 자리 근처에 체크리스트 줄이 있는 요약."""
    lines = ["## 요약", ""]
    lines += [f"- **항목 {n}**: " + "가나다라마바사 " * 12 for n in range(40)]
    lines += ["", "## 할 일"] + [f"- [ ] 확인할 일 {n}" for n in range(40)]
    return "\n".join(lines)


def http_error(code: int) -> urllib.error.HTTPError:
    return urllib.error.HTTPError(
        "https://api.telegram.org/bot/sendMessage", code, "error", None, io.BytesIO(b"")
    )


class FitTelegramTests(unittest.TestCase):
    def test_short_text_is_unchanged(self):
        self.assertEqual(notify.fit_telegram("*제목*\n\n짧은 요약"), "*제목*\n\n짧은 요약")

    def test_long_text_is_cut_on_a_line_boundary(self):
        text = "*제목*\n\n" + long_summary()
        fitted = notify.fit_telegram(text)
        self.assertLessEqual(len(fitted.encode("utf-16-le")) // 2, notify.TELEGRAM_LIMIT)
        self.assertTrue(fitted.endswith(notify.TRUNCATED_MARKER))
        body = fitted[: -len(notify.TRUNCATED_MARKER)]
        # 남은 줄은 모두 원문의 완전한 줄이다. 그래서 `- [`나 `**`가 반쯤 남지 않는다.
        self.assertTrue(text.startswith(body + "\n"))
        self.assertEqual(body.count("*") % 2, 0)
        self.assertEqual(body.count("["), body.count("]"))

    def test_limit_counts_utf16_units(self):
        text = "*제목*\n\n" + "\n".join(["🙂" * 100] * 30)
        fitted = notify.fit_telegram(text)
        self.assertLessEqual(len(fitted.encode("utf-16-le")) // 2, notify.TELEGRAM_LIMIT)


class SendTelegramTests(unittest.TestCase):
    def send(self, *responses):
        payloads = []

        def fake_urlopen(request):
            payloads.append(json.loads(request.data))
            response = responses[len(payloads) - 1]
            if isinstance(response, Exception):
                raise response
            return mock.MagicMock()

        stdout = io.StringIO()
        with (
            mock.patch.object(notify.urllib.request, "urlopen", fake_urlopen),
            redirect_stdout(stdout),
        ):
            sent = notify.send_telegram("token", "42", "제목", long_summary())
        return sent, payloads, stdout.getvalue()

    def test_markdown_send_uses_parse_mode_once(self):
        sent, payloads, _ = self.send(None)
        self.assertTrue(sent)
        self.assertEqual([p.get("parse_mode") for p in payloads], ["Markdown"])

    def test_rejected_markdown_is_resent_as_plain_text(self):
        sent, payloads, output = self.send(http_error(400), None)
        self.assertTrue(sent)
        self.assertEqual([p.get("parse_mode") for p in payloads], ["Markdown", None])
        self.assertEqual(payloads[0]["text"], payloads[1]["text"])
        self.assertIn("TelegramMarkdownRejected", output)
        self.assertIn("(plain text)", output)

    def test_other_errors_are_not_retried(self):
        sent, payloads, output = self.send(http_error(500))
        self.assertFalse(sent)
        self.assertEqual(len(payloads), 1)
        self.assertIn("TelegramDeliveryError", output)

    def test_plain_text_failure_is_reported(self):
        sent, payloads, output = self.send(http_error(400), http_error(400))
        self.assertFalse(sent)
        self.assertEqual(len(payloads), 2)
        self.assertIn("TelegramDeliveryError", output)


if __name__ == "__main__":
    unittest.main()
