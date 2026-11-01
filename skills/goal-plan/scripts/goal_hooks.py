#!/usr/bin/env python3
"""Install, list, remove, and fire agent hooks for a goal workspace.

Claude Code (`.claude/settings.json`) and Codex (`.codex/hooks.json`) read the same
hook wire format, so one `add` lands the same group in both files and whichever
runtime drives the loop fires it. `fire` feeds a sample event to the installed
commands, which is how a harness row proves a hook works without opening a session.

    goal_hooks.py add --event PostToolUse --matcher 'Edit|Write' --command 'scripts/lint.sh'
    goal_hooks.py list
    goal_hooks.py fire PostToolUse --tool Edit --file src/x.ts            # lists the commands that would run
    goal_hooks.py fire PostToolUse --tool Edit --file src/x.ts --trust-workspace
    goal_hooks.py remove <id>

Hook groups are identified by a short hash of (event, matcher, command), so the
config files carry no extra metadata. Groups this script did not add (including the
Stop gate from `init_goal_plan.py`) are listed but never rewritten.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

RUNTIME_FILES = (Path(".claude/settings.json"), Path(".codex/hooks.json"))
EVENTS = (
    "SessionStart", "UserPromptSubmit", "PreToolUse", "PostToolUse",
    "SubagentStop", "PreCompact", "Stop", "SessionEnd", "Notification",
)
TOOL_EVENTS = {"PreToolUse", "PostToolUse"}


def fail(message: str) -> int:
    print(f"error: {message}", file=sys.stderr)
    return 2


def inside_root(root: Path, path: Path) -> bool:
    """No symlink between root and path, so a cloned `.codex -> ~/.codex` never receives project hooks."""
    current = root
    for part in path.relative_to(root).parts:
        current = current / part
        if current.is_symlink():
            return False
        if not current.exists():
            return True
    return True


def shown(text: str) -> str:
    """Escape control characters so a command from the config cannot repaint the terminal before the trust decision."""
    return "".join(ch if ch.isprintable() or ch == " " else repr(ch)[1:-1] for ch in text)


def load(path: Path) -> dict:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must hold a JSON object")
    hooks = data.get("hooks", {})
    if not isinstance(hooks, dict):
        raise ValueError(f"{path}: 'hooks' must be an object keyed by event")
    for event, groups in hooks.items():
        if not isinstance(groups, list) or not all(isinstance(g, dict) and isinstance(g.get("hooks"), list) for g in groups):
            raise ValueError(f"{path}: hooks.{shown(str(event))} must be a list of groups with a 'hooks' array")
    return data


def save(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC | os.O_NOFOLLOW, 0o644)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    os.replace(tmp, path)


def group_id(event: str, matcher: str, command: str) -> str:
    return hashlib.sha256(f"{event}\0{matcher}\0{command}".encode()).hexdigest()[:8]


def entries(data: dict) -> list[tuple[str, str, str, dict, dict]]:
    """(id, event, matcher, group, handler) for every command handler in the file."""
    out = []
    for event, groups in data.get("hooks", {}).items():
        for group in groups:
            matcher = str(group.get("matcher", ""))
            for handler in group["hooks"]:
                command = handler.get("command") if isinstance(handler, dict) else None
                if isinstance(command, str):
                    out.append((group_id(event, matcher, command), event, matcher, group, handler))
    return out


def runtime_paths(root: Path) -> list[Path]:
    paths = []
    for rel in RUNTIME_FILES:
        path = root / rel
        if not inside_root(root, path):
            raise ValueError(f"{path} or one of its parents is a symlink; hooks are written only inside the workspace")
        paths.append(path)
    return paths


# ------------------------------------------------------------------ commands

def cmd_add(args: argparse.Namespace, root: Path) -> int:
    if args.event not in EVENTS:
        return fail(f"unknown event {args.event}; one of {', '.join(EVENTS)}")
    if args.matcher and args.event not in TOOL_EVENTS:
        return fail(f"--matcher applies to {', '.join(sorted(TOOL_EVENTS))} only")
    handler: dict = {"type": "command", "command": args.command}
    if args.timeout:
        handler["timeout"] = args.timeout
    group: dict = {"hooks": [handler]}
    if args.matcher:
        group["matcher"] = args.matcher
    new_id = group_id(args.event, args.matcher or "", args.command)
    for path in runtime_paths(root):
        data = load(path)
        if any(e[0] == new_id for e in entries(data)):
            print(f"kept   {new_id} already in {path}")
            continue
        data.setdefault("hooks", {}).setdefault(args.event, []).append(group)
        save(path, data)
        print(f"added  {new_id} to {path}")
    print(new_id)
    return 0


def cmd_list(args: argparse.Namespace, root: Path) -> int:
    seen: dict[str, tuple[str, str, str, set[str]]] = {}
    for path in runtime_paths(root):
        for gid, event, matcher, _group, handler in entries(load(path)):
            record = seen.setdefault(gid, (event, matcher, handler["command"], set()))
            record[3].add(path.parent.name)
    if not seen:
        print("no hooks installed")
        return 0
    for gid, (event, matcher, command, where) in sorted(seen.items(), key=lambda kv: (kv[1][0], kv[0])):
        runtimes = "+".join(sorted(where))
        flag = "" if len(where) == len(RUNTIME_FILES) else "  (one runtime only)"
        print(f"{gid}  {shown(event):<16} {shown(matcher) or '*':<14} {runtimes:<14} {shown(command)}{flag}")
    return 0


def cmd_remove(args: argparse.Namespace, root: Path) -> int:
    removed = 0
    for path in runtime_paths(root):
        data = load(path)
        hooks = data.get("hooks", {})
        changed = False
        for event in list(hooks):
            new_groups = []
            for group in hooks[event]:
                matcher = str(group.get("matcher", ""))
                kept = [h for h in group["hooks"]
                        if not (isinstance(h, dict) and isinstance(h.get("command"), str)
                                and group_id(event, matcher, h["command"]) == args.id)]
                if len(kept) != len(group["hooks"]):
                    changed = True
                    removed += 1
                if kept:
                    new_groups.append({**group, "hooks": kept})
            if new_groups:
                hooks[event] = new_groups
            else:
                hooks.pop(event)
        if changed:
            if not hooks:
                data.pop("hooks", None)
            save(path, data)
            print(f"removed {args.id} from {path}")
    if not removed:
        return fail(f"no hook with id {args.id}; run `goal_hooks.py list`")
    return 0


def sample_payload(args: argparse.Namespace, root: Path) -> dict:
    payload: dict = {
        "session_id": "goal-hooks-fire",
        "transcript_path": str(root / ".goal-hooks-fire.jsonl"),
        "cwd": str(root),
        "hook_event_name": args.event,
    }
    if args.event in TOOL_EVENTS:
        tool = args.tool or "Edit"
        payload["tool_name"] = tool
        tool_input: dict = {}
        if args.file:
            tool_input["file_path"] = str((root / args.file).resolve()) if not Path(args.file).is_absolute() else args.file
        if args.command_text:
            tool_input["command"] = args.command_text
        payload["tool_input"] = tool_input
        if args.event == "PostToolUse":
            payload["tool_response"] = {"success": True}
    if args.event in {"Stop", "SubagentStop"}:
        payload["stop_hook_active"] = False
    if args.event == "UserPromptSubmit":
        payload["prompt"] = args.prompt or "sample prompt"
    if args.event == "SessionStart":
        payload["source"] = "resume"
    if args.event == "PreCompact":
        payload["trigger"] = "auto"
    if args.payload:
        payload.update(json.loads(args.payload))
    return payload


def matcher_hits(matcher: str, tool: str) -> bool:
    if not matcher or matcher == "*":
        return True
    try:
        return re.fullmatch(matcher, tool) is not None or re.search(matcher, tool) is not None
    except re.error:
        return matcher == tool


def cmd_fire(args: argparse.Namespace, root: Path) -> int:
    if args.event not in EVENTS:
        return fail(f"unknown event {args.event}; one of {', '.join(EVENTS)}")
    source = root / RUNTIME_FILES[0] if args.runtime == "claude" else root / RUNTIME_FILES[1]
    if not inside_root(root, source):
        return fail(f"{source} or one of its parents is a symlink")
    data = load(source)
    payload = sample_payload(args, root)
    tool = payload.get("tool_name", "")
    selected = [e for e in entries(data)
                if e[1] == args.event and (args.event not in TOOL_EVENTS or matcher_hits(e[2], tool))
                and (not args.id or e[0] in args.id)]
    if not selected:
        return fail(f"no {args.event} hook matches tool {tool!r} in {source}")
    if not args.trust_workspace:
        # The runtimes run project hooks only after the user trusts the project; this
        # command runs the same shell lines, so it needs the same explicit decision.
        print(f"would run {len(selected)} hook command(s) from {source}:")
        for gid, _event, _matcher, _group, handler in selected:
            print(f"  {gid}  {shown(handler['command'])}")
        return fail("re-run with --trust-workspace after reading these commands (they come from the workspace config)")
    env = {key: os.environ[key] for key in ("PATH", "HOME", "LANG", "LC_ALL", "TMPDIR", "TERM") if key in os.environ}
    env.update(CLAUDE_PROJECT_DIR=str(root), GOAL_HOOKS_FIRE="1")
    ran = 0
    failures = 0
    for gid, _event, _matcher, _group, handler in selected:
        ran += 1
        timeout = handler.get("timeout") if isinstance(handler.get("timeout"), (int, float)) else 60
        try:
            proc = subprocess.run(handler["command"], shell=True, cwd=root, env=env, input=json.dumps(payload),
                                  capture_output=True, text=True, timeout=timeout)
            code = proc.returncode
            out = (proc.stdout + proc.stderr).strip()
        except subprocess.TimeoutExpired:
            code, out = 124, f"timed out after {timeout}s"
        status = "ok  " if code == 0 else "FAIL"
        if code not in (0, 2):
            # Hooks use exit 2 for a deliberate block; anything else is the hook itself breaking.
            failures += 1
        elif code == 2 and not args.expect_block:
            failures += 1
        elif code == 0 and args.expect_block:
            failures += 1
            status = "FAIL"
        print(f"{status} {gid} exit {code}  {shown(handler['command'])}")
        if out:
            for line in out.splitlines()[-args.tail:]:
                print(f"       {shown(line)}")
    print(f"fired {ran} hook(s) for {args.event}; {failures} failed" + ("; expected a block (exit 2)" if args.expect_block else ""))
    return 1 if failures else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", default=".", help="goal workspace root (default: current directory)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    add = sub.add_parser("add", help="install one command hook in both runtime files")
    add.add_argument("--event", required=True, help=", ".join(EVENTS))
    add.add_argument("--matcher", default="", help="tool-name regex for PreToolUse/PostToolUse, e.g. 'Edit|Write'")
    add.add_argument("--command", required=True, help="shell command; reads the event JSON on stdin")
    add.add_argument("--timeout", type=int, default=0, help="seconds before the runtime kills the hook")
    add.set_defaults(func=cmd_add)

    lst = sub.add_parser("list", help="show installed hooks with ids")
    lst.set_defaults(func=cmd_list)

    rm = sub.add_parser("remove", help="remove a hook by id from both runtime files")
    rm.add_argument("id")
    rm.set_defaults(func=cmd_remove)

    fire = sub.add_parser("fire", help="run the installed hooks for one event with a sample payload")
    fire.add_argument("event")
    fire.add_argument("--tool", help="tool name for PreToolUse/PostToolUse (default Edit)")
    fire.add_argument("--file", help="tool_input.file_path for the sample payload")
    fire.add_argument("--command-text", help="tool_input.command for a Bash sample payload")
    fire.add_argument("--prompt", help="prompt text for UserPromptSubmit")
    fire.add_argument("--payload", help="JSON object merged over the sample payload")
    fire.add_argument("--runtime", choices=("claude", "codex"), default="claude", help="which file to read hooks from")
    fire.add_argument("--expect-block", action="store_true", help="pass only when every hook exits 2 (a deliberate block)")
    fire.add_argument("--id", action="append", help="run only this hook id (repeatable)")
    fire.add_argument("--trust-workspace", action="store_true",
                      help="actually run the commands; without it the matching commands are listed and nothing runs")
    fire.add_argument("--tail", type=int, default=5, help="output lines to show per hook")
    fire.set_defaults(func=cmd_fire)

    args = parser.parse_args(argv)
    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        return fail(f"root not found: {root}")
    try:
        return args.func(args, root)
    except (ValueError, json.JSONDecodeError) as exc:
        return fail(str(exc))


if __name__ == "__main__":
    raise SystemExit(main())
