#!/usr/bin/env python3
"""publish의 Herdr 대화 자동 감지 회귀 검사: 가짜 herdr CLI로 세션·에이전트·대화 ID를 읽고, 식별 실패는 ValueError로 끝난다."""
import importlib.util
import os
import stat
import sys
import tempfile
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("reply_bridge", SKILL / "scripts" / "reply-bridge.py")
bridge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bridge)

FAKE = r'''#!/usr/bin/env bash
# 가짜 herdr: session list 표와 pane get JSON만 흉내 낸다.
if [ "$1" = "session" ]; then
  printf 'name status directory socket\n'
  printf 'default running /x /sock/herdr.sock\n'
  printf 'qa running /x/sessions/qa /sock/sessions/qa/herdr.sock\n'
  exit 0
fi
# herdr --session <name> pane get <id>
name="$2"; pane="$5"
case "$pane" in
  wX:p1) printf '{"result":{"pane":{"pane_id":"wX:p1","agent":"claude","agent_session":{"agent":"claude","kind":"id","source":"herdr:claude","value":"conv-claude-1"}}}}\n' ;;
  wX:p2) printf '{"result":{"pane":{"pane_id":"wX:p2","agent":"codex","agent_session":{"agent":"codex","kind":"id","source":"herdr:codex","value":"conv-codex-2"}}}}\n' ;;
  wX:p3) printf '{"result":{"pane":{"pane_id":"wX:p3","agent":"claude"}}}\n' ;;
  *) printf '{"error":{"code":"pane_not_found"}}\n'; exit 1 ;;
esac
'''


def demo():
    with tempfile.TemporaryDirectory(prefix="publish-detect-") as folder:
        fake = Path(folder) / "herdr"
        fake.write_text(FAKE, encoding="utf-8")
        fake.chmod(fake.stat().st_mode | stat.S_IXUSR)
        base = {"HERDR_BIN_PATH": str(fake), "PATH": os.environ.get("PATH", "")}

        origin = bridge.detect_origin({**base, "HERDR_PANE_ID": "wX:p1", "HERDR_SOCKET_PATH": "/sock/herdr.sock"})
        assert origin == {"endpoint": "default", "agent": "claude", "conversation": "conv-claude-1", "pane": "wX:p1"}, origin
        origin = bridge.detect_origin({**base, "HERDR_PANE_ID": "wX:p2", "HERDR_SOCKET_PATH": "/sock/sessions/qa/herdr.sock"})
        assert origin["endpoint"] == "qa" and origin["agent"] == "codex" and origin["conversation"] == "conv-codex-2", origin

        failures = {
            "no pane env": {**base},
            "unknown socket": {**base, "HERDR_PANE_ID": "wX:p1", "HERDR_SOCKET_PATH": "/sock/nope.sock"},
            "no conversation yet": {**base, "HERDR_PANE_ID": "wX:p3", "HERDR_SOCKET_PATH": "/sock/herdr.sock"},
            "missing pane": {**base, "HERDR_PANE_ID": "wX:p9", "HERDR_SOCKET_PATH": "/sock/herdr.sock"},
        }
        for label, env in failures.items():
            try:
                bridge.detect_origin(env)
            except ValueError:
                continue
            raise AssertionError(f"{label}: must raise ValueError")
    print("ok: publish-detect")


if __name__ == "__main__":
    demo()
