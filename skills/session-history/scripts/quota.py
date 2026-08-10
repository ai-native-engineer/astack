"""Live subscription quota snapshots (Claude OAuth + Codex wham).

Reads local CLI credential files only; never prints tokens.
Grok has no stable public quota endpoint here — returns unsupported.
"""

from __future__ import annotations

import json
import subprocess
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

HOME = Path.home()
CLAUDE_CREDENTIALS = HOME / ".claude" / ".credentials.json"
CODEX_AUTH = HOME / ".codex" / "auth.json"

TIMEOUT_SEC = 12


def _http_json(url: str, headers: dict[str, str]) -> tuple[int, Any]:
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_SEC) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            try:
                return resp.status, json.loads(body)
            except json.JSONDecodeError:
                return resp.status, {"_raw": body[:500]}
    except urllib.error.HTTPError as exc:
        try:
            body = exc.read().decode("utf-8", errors="replace")
            data = json.loads(body)
        except Exception:
            data = {"error": str(exc)}
        return exc.code, data
    except Exception as exc:  # noqa: BLE001 — surface network/DNS as error field
        return 0, {"error": str(exc)}


def _claude_access_token() -> str | None:
    if CLAUDE_CREDENTIALS.exists():
        try:
            data = json.loads(CLAUDE_CREDENTIALS.read_text(encoding="utf-8"))
            oauth = data.get("claudeAiOauth") or {}
            token = oauth.get("accessToken")
            if isinstance(token, str) and token.strip():
                return token.strip()
        except (OSError, json.JSONDecodeError):
            pass
    # macOS Keychain fallback (Claude Code stores credentials there)
    try:
        raw = subprocess.run(
            ["security", "find-generic-password", "-s", "Claude Code-credentials", "-w"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        if raw.returncode == 0 and raw.stdout.strip():
            data = json.loads(raw.stdout.strip())
            oauth = data.get("claudeAiOauth") or {}
            token = oauth.get("accessToken")
            if isinstance(token, str) and token.strip():
                return token.strip()
    except (OSError, json.JSONDecodeError, subprocess.TimeoutExpired):
        pass
    return None


def _codex_tokens() -> tuple[str | None, str | None]:
    if not CODEX_AUTH.exists():
        return None, None
    try:
        data = json.loads(CODEX_AUTH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None, None
    tokens = data.get("tokens") or {}
    access = tokens.get("access_token") or tokens.get("accessToken")
    account = tokens.get("account_id") or tokens.get("accountId")
    if not access:
        access = data.get("access_token") or data.get("OPENAI_API_KEY")
    return (
        access.strip() if isinstance(access, str) and access.strip() else None,
        account.strip() if isinstance(account, str) and account.strip() else None,
    )


def fetch_claude_quota() -> dict[str, Any]:
    token = _claude_access_token()
    if not token:
        return {
            "tool": "claude",
            "ok": False,
            "error": "no Claude OAuth access token (~/.claude/.credentials.json)",
            "windows": [],
        }
    status, data = _http_json(
        "https://api.anthropic.com/api/oauth/usage",
        {
            "Authorization": f"Bearer {token}",
            "User-Agent": "session-history-quota",
            "Accept": "application/json",
            "anthropic-version": "2023-06-01",
            "anthropic-beta": "oauth-2025-04-20",
        },
    )
    if status != 200 or not isinstance(data, dict):
        err = data.get("error") if isinstance(data, dict) else data
        if isinstance(err, dict):
            err = err.get("message") or err
        return {
            "tool": "claude",
            "ok": False,
            "error": f"HTTP {status}: {err}",
            "windows": [],
        }
    windows = []
    for key, label in (
        ("five_hour", "5h"),
        ("seven_day", "Week"),
        ("seven_day_opus", "Opus week"),
        ("seven_day_sonnet", "Sonnet week"),
    ):
        block = data.get(key) or {}
        if not isinstance(block, dict):
            continue
        util = block.get("utilization")
        if util is None:
            continue
        windows.append({
            "label": label,
            "used_percent": float(util),
            "resets_at": block.get("resets_at"),
        })
    return {
        "tool": "claude",
        "ok": True,
        "plan": data.get("plan") or data.get("plan_type") or "",
        "windows": windows,
        "raw_keys": sorted(data.keys()),
    }


def fetch_codex_quota() -> dict[str, Any]:
    token, account_id = _codex_tokens()
    if not token:
        return {
            "tool": "codex",
            "ok": False,
            "error": "no Codex access token (~/.codex/auth.json)",
            "windows": [],
        }
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "session-history-quota",
        "Accept": "application/json",
    }
    if account_id:
        headers["ChatGPT-Account-Id"] = account_id
    status, data = _http_json("https://chatgpt.com/backend-api/wham/usage", headers)
    if status in (401, 403):
        return {
            "tool": "codex",
            "ok": False,
            "error": "token expired or forbidden",
            "windows": [],
        }
    if status != 200 or not isinstance(data, dict):
        return {
            "tool": "codex",
            "ok": False,
            "error": f"HTTP {status}: {data if not isinstance(data, dict) else data.get('error')}",
            "windows": [],
        }
    windows = []
    rate = data.get("rate_limit") or {}
    primary = rate.get("primary_window") or {}
    secondary = rate.get("secondary_window") or {}
    def _window_label(seconds: int | float | None, fallback_seconds: int) -> str:
        hours = round((seconds or fallback_seconds) / 3600)
        if hours >= 24 * 6:
            return "Week"
        if hours >= 24:
            return "Day" if hours <= 30 else f"{hours}h"
        return f"{hours}h"

    if primary:
        windows.append({
            "label": _window_label(primary.get("limit_window_seconds"), 10800),
            "used_percent": float(primary.get("used_percent") or 0),
            "resets_at": primary.get("reset_at"),
        })
    if secondary:
        windows.append({
            "label": _window_label(secondary.get("limit_window_seconds"), 86400),
            "used_percent": float(secondary.get("used_percent") or 0),
            "resets_at": secondary.get("reset_at"),
        })
    credits = data.get("credits") or {}
    balance = credits.get("balance")
    plan = data.get("plan_type") or ""
    if balance is not None:
        try:
            plan = f"{plan} (credits ${float(balance):.2f})".strip()
        except (TypeError, ValueError):
            pass
    return {
        "tool": "codex",
        "ok": True,
        "plan": plan,
        "windows": windows,
    }


def fetch_grok_quota() -> dict[str, Any]:
    return {
        "tool": "grok",
        "ok": False,
        "error": "unsupported (no stable public quota API in this skill)",
        "windows": [],
    }


def fetch_quotas(tool_filter: str = "all") -> list[dict[str, Any]]:
    out = []
    if tool_filter in ("all", "claude"):
        out.append(fetch_claude_quota())
    if tool_filter in ("all", "codex"):
        out.append(fetch_codex_quota())
    if tool_filter in ("all", "grok"):
        out.append(fetch_grok_quota())
    return out
