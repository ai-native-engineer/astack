#!/usr/bin/env python3
"""Runnable checks for goal_worker.py: a local bare repo and a recorded `gh` stand-in, no network."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_goal_scripts import GIT_ENV, INIT, SKILL_ROOT, commit_all, git, run  # noqa: E402

GOAL_WORKER = SKILL_ROOT / "scripts" / "goal_worker.py"
GOAL_LOG = SKILL_ROOT / "scripts" / "goal_log.py"

# A `gh` that logs every call. `pr view ... --jq .state` answers from $FAKE_GH/merged_state (what GitHub
# reports after the push); every other `pr view` answers with the JSON file the test wrote.
FAKE_GH = r'''#!/bin/sh
printf '%s\n' "$*" >> "$FAKE_GH/calls.log"
case "$*" in
  "repo view --json nameWithOwner --jq .nameWithOwner") echo "octo/demo" ;;
  "repo view --json defaultBranchRef"*) cat "$FAKE_GH/default_branch" ;;
  "pr view "*"--jq .state"*) cat "$FAKE_GH/merged_state" ;;
  "pr view "*) cat "$FAKE_GH/pr.json" ;;
  "issue close "*) ;;
  *) echo "unexpected gh call: $*" >&2; exit 9 ;;
esac
'''


class Fixture:
    """origin (bare) + goal workspace on goal/demo with row 1 (issue #12) ready for a worker."""

    def __init__(self, tmp: Path) -> None:
        self.tmp = tmp
        self.fake = tmp / "fake-gh"
        self.fake.mkdir()
        (self.fake / "gh").write_text(FAKE_GH, encoding="utf-8")
        (self.fake / "gh").chmod(0o755)
        (self.fake / "merged_state").write_text("MERGED\n", encoding="utf-8")
        (self.fake / "default_branch").write_text("main\n", encoding="utf-8")
        self.env = {**GIT_ENV, "PATH": f"{self.fake}:{GIT_ENV['PATH']}", "FAKE_GH": str(self.fake),
                    "GOAL_WORKER_CONFIRM_DELAY": "0"}
        self.origin = tmp / "origin.git"
        run("git", "init", "-q", "--bare", "--initial-branch=main", str(self.origin), cwd=tmp)
        (tmp / "work").mkdir()
        self.ws = tmp / "work" / "goal"
        run("git", "clone", "-q", str(self.origin), str(self.ws), cwd=tmp)
        git("checkout", "-q", "-b", "main", cwd=self.ws)
        (self.ws / "README.md").write_text("# demo\n", encoding="utf-8")
        commit_all(self.ws, "chore: init")
        git("push", "-q", "-u", "origin", "main", cwd=self.ws)
        git("checkout", "-q", "-b", "goal/demo", cwd=self.ws)
        subprocess.run([sys.executable, str(INIT), str(self.ws), "--goal", "demo", "--proof-command", "true"],
                       capture_output=True, text=True, check=True)
        goal = self.ws / "GOAL.md"
        goal.write_text(goal.read_text(encoding="utf-8").replace(
            "tracking issue: TBD (`#N` or none)", "tracking issue: #40", 1), encoding="utf-8")
        self.log("add", "--task", "build x", "--issue", "12")
        commit_all(self.ws, "chore(goal): plan (#40)")
        git("push", "-q", "-u", "origin", "goal/demo", cwd=self.ws)

    def log(self, *args: str) -> subprocess.CompletedProcess[str]:
        return run(sys.executable, str(GOAL_LOG), *args, cwd=self.ws)

    def worker(self, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, str(GOAL_WORKER), *args], cwd=self.ws,
                              capture_output=True, text=True, check=check, env=self.env)

    def row(self, row_id: str) -> dict[str, str]:
        lines = (self.ws / "progress.tsv").read_text(encoding="utf-8").splitlines()
        header = lines[0].split("\t")
        for line in lines[1:]:
            cells = dict(zip(header, line.split("\t")))
            if cells["id"] == row_id:
                return cells
        raise AssertionError(f"no row {row_id}")

    def start_and_push_work(self) -> tuple[str, Path]:
        """`start` row 1, commit a file in the worker worktree, push it, and write the PR JSON."""
        self.worker("start", "1", "--worker", "w1", "--type", "feat", "--desc", "build-x")
        branch, wt = self.row("1")["branch"], Path(self.row("1")["worktree"])
        (wt / "x.txt").write_text("x\n", encoding="utf-8")
        commit_all(wt, "feat(x): build x (#12)")
        git("push", "-q", "-u", "origin", branch, cwd=wt)
        self.head = git("rev-parse", "HEAD", cwd=wt)
        self.write_pr(branch, self.head)
        return branch, wt

    def write_pr(self, branch: str, oid: str, *, state: str = "OPEN", base: str = "goal/demo",
                 title: str = "feat(x): build x (#12)") -> None:
        (self.fake / "pr.json").write_text(json.dumps(
            {"state": state, "baseRefName": base, "headRefName": branch, "headRefOid": oid, "title": title}),
            encoding="utf-8")

    def calls(self) -> list[str]:
        path = self.fake / "calls.log"
        return path.read_text(encoding="utf-8").splitlines() if path.exists() else []

    def snapshot(self) -> tuple[str, str, str]:
        return (git("rev-parse", "HEAD", cwd=self.ws), (self.ws / "progress.tsv").read_text(encoding="utf-8"),
                git("branch", "--list", cwd=self.ws))


class StartTests(unittest.TestCase):
    def test_start_derives_branch_and_worktree_and_records_the_ledger(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fx = Fixture(Path(tmp))
            before = git("rev-parse", "HEAD", cwd=fx.ws)
            result = fx.worker("start", "1", "--worker", "w1", "--type", "feat", "--desc", "build-x")
            wt = fx.tmp / "work" / "feat-12-build-x"
            self.assertIn("branch: feat/12-build-x", result.stdout)
            self.assertIn(f"worktree: {wt.resolve()}", result.stdout)
            self.assertTrue(wt.is_dir())
            self.assertEqual(git("rev-parse", "--abbrev-ref", "HEAD", cwd=wt), "feat/12-build-x")
            self.assertEqual(git("rev-parse", "HEAD", cwd=wt), before)
            row = fx.row("1")
            self.assertEqual((row["status"], row["worker"], row["branch"]), ("doing", "w1", "feat/12-build-x"))
            self.assertEqual(Path(row["worktree"]).resolve(), wt.resolve())
            self.assertEqual(git("rev-parse", "HEAD", cwd=fx.ws), before)  # no commit

    def test_start_falls_back_to_the_tracking_issue_and_honors_worktree(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fx = Fixture(Path(tmp))
            fx.log("set", "1", "--col", "task", "--value", "no issue prefix")
            target = fx.tmp / "elsewhere"
            result = fx.worker("start", "1", "--worker", "w1", "--type", "fix", "--desc", "y",
                               "--worktree", str(target))
            self.assertIn("branch: fix/40-y", result.stdout)
            self.assertTrue(target.is_dir())

    def test_start_refuses_a_row_that_is_not_todo_and_bad_names(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fx = Fixture(Path(tmp))
            bad = fx.worker("start", "1", "--worker", "w", "--type", "wip", "--desc", "x", check=False)
            self.assertEqual(bad.returncode, 2)
            bad = fx.worker("start", "1", "--worker", "w", "--type", "feat", "--desc", "Not Kebab", check=False)
            self.assertEqual(bad.returncode, 2)
            fx.worker("start", "1", "--worker", "w", "--type", "feat", "--desc", "x")
            again = fx.worker("start", "1", "--worker", "w", "--type", "feat", "--desc", "x", check=False)
            self.assertEqual(again.returncode, 2)
            self.assertIn("only a todo row", again.stderr)


class IntegrateTests(unittest.TestCase):
    def test_happy_path_is_one_first_parent_commit_with_work_and_ledger(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fx = Fixture(Path(tmp))
            branch, wt = fx.start_and_push_work()
            result = fx.worker("integrate", "1", "--pr", "5", "--artifact", "x.txt exists", "--head", fx.head)
            self.assertEqual(result.returncode, 0, result.stderr)
            parents = git("log", "--first-parent", "--format=%s", "origin/goal/demo~1..HEAD", cwd=fx.ws)
            self.assertEqual(parents, "feat(x): build x (#12)")
            self.assertEqual(git("rev-list", "--parents", "-n", "1", "HEAD", cwd=fx.ws).count(" "), 2)
            self.assertTrue((fx.ws / "x.txt").is_file())
            row = fx.row("1")
            self.assertEqual((row["status"], row["decision"], row["artifact"]), ("done", "keep", "x.txt exists"))
            self.assertIn("progress.tsv", git("show", "--name-only", "--format=", "HEAD", cwd=fx.ws))
            self.assertEqual(git("status", "--porcelain", cwd=fx.ws), "")
            self.assertEqual(git("rev-parse", "HEAD", cwd=fx.ws), git("rev-parse", "origin/goal/demo", cwd=fx.ws))
            self.assertFalse(wt.exists())
            self.assertEqual(git("branch", "--list", branch, cwd=fx.ws), "")
            self.assertEqual(git("ls-remote", "--heads", "origin", branch, cwd=fx.ws), "")
            self.assertIn("issue close 12 --reason completed --comment x.txt exists (PR #5) --repo octo/demo",
                          fx.calls())

    def test_keep_issue_leaves_the_issue_open(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fx = Fixture(Path(tmp))
            fx.start_and_push_work()
            result = fx.worker("integrate", "1", "--pr", "5", "--artifact", "ok", "--head", fx.head, "--keep-issue")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse([c for c in fx.calls() if c.startswith("issue close")])

    def refuses(self, fx: Fixture, expected: str, *extra: str) -> None:
        before = fx.snapshot()
        remote_before = git("ls-remote", "--heads", "origin", cwd=fx.ws)
        result = fx.worker("integrate", "1", "--pr", "5", "--artifact", "ok", "--head", fx.head, *extra, check=False)
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn(expected, result.stderr)
        self.assertEqual(fx.snapshot(), before)
        self.assertEqual(git("ls-remote", "--heads", "origin", cwd=fx.ws), remote_before)
        self.assertFalse([c for c in fx.calls() if c.startswith("issue close")])
        self.assertFalse((fx.ws / ".git" / "MERGE_HEAD").exists())

    def test_refuses_a_pr_that_is_not_open_or_targets_the_wrong_base_or_head(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fx = Fixture(Path(tmp))
            branch, wt = fx.start_and_push_work()
            oid = git("rev-parse", "HEAD", cwd=wt)
            fx.write_pr(branch, oid, state="CLOSED")
            self.refuses(fx, "not OPEN")
            fx.write_pr(branch, oid, base="main")
            self.refuses(fx, "not the goal branch")
            fx.write_pr("feat/other", oid)
            self.refuses(fx, "not the row branch")
            self.assertTrue(wt.is_dir())

    def test_refuses_when_the_pr_head_differs_from_the_remote_branch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fx = Fixture(Path(tmp))
            branch, wt = fx.start_and_push_work()
            fx.write_pr(branch, "0" * 40)
            self.refuses(fx, "differs from origin")

    def test_refuses_local_commits_not_pushed_and_a_dirty_worker_worktree(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fx = Fixture(Path(tmp))
            branch, wt = fx.start_and_push_work()
            (wt / "y.txt").write_text("y\n", encoding="utf-8")
            self.refuses(fx, "is not clean")
            commit_all(wt, "feat(x): unpushed (#12)")
            self.refuses(fx, "has commits not on origin")

    def test_refuses_rows_that_are_deferred_or_have_no_branch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fx = Fixture(Path(tmp))
            fx.start_and_push_work()
            fx.log("defer", "1", "--reason", "waiting for the user")
            self.refuses(fx, "row 1 is deferred")
            fx.log("add", "--task", "no worker yet")
            result = fx.worker("integrate", "2", "--pr", "5", "--artifact", "ok", "--head", fx.head, check=False)
            self.assertEqual(result.returncode, 2)
            self.assertIn("has no branch", result.stderr)

    def test_refuses_a_dirty_file_other_than_progress_tsv(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fx = Fixture(Path(tmp))
            fx.start_and_push_work()
            (fx.ws / "README.md").write_text("changed\n", encoding="utf-8")
            result = fx.worker("integrate", "1", "--pr", "5", "--artifact", "ok", "--head", fx.head, check=False)
            self.assertEqual(result.returncode, 2)
            self.assertIn("README.md", result.stderr)
            self.assertIn("besides progress.tsv: README.md", result.stderr)

    def test_a_dirty_progress_tsv_is_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fx = Fixture(Path(tmp))
            fx.start_and_push_work()  # start left assign/start uncommitted in progress.tsv
            self.assertIn("progress.tsv", git("status", "--porcelain", cwd=fx.ws))
            self.assertEqual(fx.worker("integrate", "1", "--pr", "5", "--artifact", "ok", "--head", fx.head).returncode, 0)

    def test_conflict_aborts_the_merge_and_changes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fx = Fixture(Path(tmp))
            branch, wt = fx.start_and_push_work()
            (fx.ws / "x.txt").write_text("goal side\n", encoding="utf-8")
            commit_all(fx.ws, "feat(x): conflicting (#12)")
            git("push", "-q", "origin", "goal/demo", cwd=fx.ws)
            before = fx.snapshot()
            result = fx.worker("integrate", "1", "--pr", "5", "--artifact", "ok", "--head", fx.head, check=False)
            self.assertEqual(result.returncode, 1)
            self.assertIn("merge aborted", result.stderr)
            self.assertEqual(fx.snapshot(), before)
            self.assertFalse((fx.ws / ".git" / "MERGE_HEAD").exists())
            self.assertTrue(wt.is_dir())
            self.assertNotEqual(git("ls-remote", "--heads", "origin", branch, cwd=fx.ws), "")

    def test_unconfirmed_merged_state_deletes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fx = Fixture(Path(tmp))
            branch, wt = fx.start_and_push_work()
            (fx.fake / "merged_state").write_text("OPEN\n", encoding="utf-8")
            result = fx.worker("integrate", "1", "--pr", "5", "--artifact", "ok", "--head", fx.head, check=False)
            self.assertEqual(result.returncode, 1)
            self.assertIn("not MERGED", result.stderr)
            self.assertTrue(wt.is_dir())
            self.assertNotEqual(git("branch", "--list", branch, cwd=fx.ws), "")
            self.assertNotEqual(git("ls-remote", "--heads", "origin", branch, cwd=fx.ws), "")
            self.assertFalse([c for c in fx.calls() if c.startswith("issue close")])

    def test_rejected_push_stops_without_deleting_or_forcing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fx = Fixture(Path(tmp))
            branch, wt = fx.start_and_push_work()
            other = fx.tmp / "other"
            run("git", "clone", "-q", "-b", "goal/demo", str(fx.origin), str(other), cwd=fx.tmp)
            (other / "z.txt").write_text("z\n", encoding="utf-8")
            commit_all(other, "feat(z): elsewhere (#12)")
            git("push", "-q", "origin", "goal/demo", cwd=other)
            result = fx.worker("integrate", "1", "--pr", "5", "--artifact", "ok", "--head", fx.head, check=False)
            self.assertEqual(result.returncode, 1)
            self.assertIn("push rejected", result.stderr)
            self.assertIn("never force", result.stderr)
            self.assertTrue(wt.is_dir())
            self.assertNotEqual(git("ls-remote", "--heads", "origin", branch, cwd=fx.ws), "")


class SecurityTests(unittest.TestCase):
    """The merge is bound to the reviewed commit, orchestrator files are off limits, destructive steps are validated."""

    def integrate(self, fx: Fixture, *extra: str, head: str | None = None, check: bool = False):
        return fx.worker("integrate", "1", "--pr", "5", "--artifact", "ok", "--head", head or fx.head, *extra,
                         check=check)

    def test_head_is_required(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fx = Fixture(Path(tmp))
            fx.start_and_push_work()
            result = fx.worker("integrate", "1", "--pr", "5", "--artifact", "ok", check=False)
            self.assertEqual(result.returncode, 2)
            self.assertIn("--head", result.stderr)

    def test_head_must_equal_the_pr_head_and_the_remote_branch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fx = Fixture(Path(tmp))
            branch, wt = fx.start_and_push_work()
            reviewed = fx.head
            before = fx.snapshot()
            wrong = self.integrate(fx, head="1" * 40)
            self.assertEqual(wrong.returncode, 2)
            self.assertIn("--head", wrong.stderr)
            short = self.integrate(fx, head=reviewed[:10])
            self.assertEqual(short.returncode, 2)
            self.assertEqual(fx.snapshot(), before)
            # the worker pushes another commit after review; the PR and the remote moved, --head did not
            (wt / "late.txt").write_text("late\n", encoding="utf-8")
            commit_all(wt, "feat(x): late change (#12)")
            git("push", "-q", "origin", branch, cwd=wt)
            fx.write_pr(branch, git("rev-parse", "HEAD", cwd=wt))
            moved = self.integrate(fx, head=reviewed)
            self.assertEqual(moved.returncode, 2)
            self.assertIn("--head", moved.stderr)
            self.assertEqual(fx.snapshot(), before)
            self.assertFalse((fx.ws / "late.txt").exists())

    def test_the_merge_parent_is_exactly_the_reviewed_head(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fx = Fixture(Path(tmp))
            fx.start_and_push_work()
            self.assertEqual(self.integrate(fx).returncode, 0)
            self.assertEqual(git("rev-parse", "HEAD^2", cwd=fx.ws), fx.head)

    def test_remote_branch_is_deleted_with_a_lease_on_the_reviewed_head(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fx = Fixture(Path(tmp))
            branch, _ = fx.start_and_push_work()
            trace = fx.tmp / "git-trace.log"
            fx.env["GIT_TRACE"] = str(trace)
            self.assertEqual(self.integrate(fx).returncode, 0)
            text = trace.read_text(encoding="utf-8")
            self.assertIn(f"--force-with-lease=refs/heads/{branch}:{fx.head}", text)
            self.assertIn("--delete", text)
            self.assertEqual(git("ls-remote", "--heads", "origin", branch, cwd=fx.ws), "")

    def refused_for_files(self, fx: Fixture, wt: Path, names: list[str]) -> None:
        for name in names:
            path = wt / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("changed by the worker\n", encoding="utf-8")
        commit_all(wt, "feat(x): touch owned files (#12)")
        branch = git("rev-parse", "--abbrev-ref", "HEAD", cwd=wt)
        git("push", "-q", "origin", branch, cwd=wt)
        head = git("rev-parse", "HEAD", cwd=wt)
        fx.write_pr(branch, head)
        before = fx.snapshot()
        result = self.integrate(fx, head=head)
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        for name in names:
            self.assertIn(name, result.stderr)
        self.assertEqual(fx.snapshot(), before)
        self.assertFalse((fx.ws / ".git" / "MERGE_HEAD").exists())
        self.assertTrue(wt.is_dir())

    def test_a_worker_diff_touching_orchestrator_files_is_refused(self) -> None:
        for name in ("GOAL.md", "progress.tsv", ".claude/settings.json", ".codex/hooks.json"):
            with self.subTest(name), tempfile.TemporaryDirectory() as tmp:
                fx = Fixture(Path(tmp))
                _, wt = fx.start_and_push_work()
                self.refused_for_files(fx, wt, [name])

    def test_row_branch_must_be_a_plain_non_protected_work_branch(self) -> None:
        cases = {"main": "main", "goal/demo": "goal/demo", "feat/main": "feat/main", "weird": "weird",
                 "feat/trunk": "feat/trunk"}
        for value in cases:
            with self.subTest(value), tempfile.TemporaryDirectory() as tmp:
                fx = Fixture(Path(tmp))
                fx.start_and_push_work()
                git("push", "-q", "origin", "main:refs/heads/feat/trunk", cwd=fx.ws)
                git("remote", "set-head", "origin", "feat/trunk", cwd=fx.ws)  # the repository default branch
                fx.log("set", "1", "--col", "branch", "--value", value)
                before = fx.snapshot()
                result = self.integrate(fx)
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                self.assertIn(f"row branch {value}", result.stderr)
                self.assertEqual(fx.snapshot(), before)
                self.assertFalse([c for c in fx.calls() if c.startswith("pr view")])

    def test_an_unregistered_worktree_path_is_kept_and_reported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fx = Fixture(Path(tmp))
            branch, wt = fx.start_and_push_work()
            decoy = fx.tmp / "decoy"
            decoy.mkdir()
            (decoy / "precious.txt").write_text("keep me\n", encoding="utf-8")
            fx.log("set", "1", "--col", "worktree", "--value", str(decoy))
            result = self.integrate(fx)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("not registered", result.stderr)
            self.assertTrue((decoy / "precious.txt").is_file())
            self.assertTrue(wt.is_dir())
            self.assertEqual(git("ls-remote", "--heads", "origin", branch, cwd=fx.ws), "")  # merge stands



class CommitFailureTests(unittest.TestCase):
    """A failing commit (hook) or ledger update leaves the goal workspace exactly as it was."""

    def setup_failing(self, tmp: str):
        fx = Fixture(Path(tmp))
        branch, wt = fx.start_and_push_work()
        fx.log("add", "--task", "other row")
        fx.log("start", "2")  # an uncommitted `doing` entry for another row must survive
        return fx, branch, wt

    def assert_untouched(self, fx: Fixture, ledger: bytes, head: str, remote: str, branch: str, wt: Path) -> None:
        self.assertFalse((fx.ws / ".git" / "MERGE_HEAD").exists())
        self.assertEqual(git("diff", "--cached", "--name-only", cwd=fx.ws), "")
        self.assertFalse((fx.ws / "x.txt").exists())
        self.assertEqual((fx.ws / "progress.tsv").read_bytes(), ledger)
        self.assertEqual(git("rev-parse", "HEAD", cwd=fx.ws), head)
        self.assertEqual(git("ls-remote", "--heads", "origin", "goal/demo", cwd=fx.ws), remote)
        self.assertNotEqual(git("ls-remote", "--heads", "origin", branch, cwd=fx.ws), "")
        self.assertNotEqual(git("branch", "--list", branch, cwd=fx.ws), "")
        self.assertTrue(wt.is_dir())

    def test_failing_pre_commit_hook_aborts_the_merge_and_a_retry_succeeds(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fx, branch, wt = self.setup_failing(tmp)
            ledger = (fx.ws / "progress.tsv").read_bytes()
            head = git("rev-parse", "HEAD", cwd=fx.ws)
            remote = git("ls-remote", "--heads", "origin", "goal/demo", cwd=fx.ws)
            hook = fx.ws / ".git" / "hooks" / "pre-commit"
            hook.write_text("#!/bin/sh\necho 'hook says no' >&2\nexit 1\n", encoding="utf-8")
            hook.chmod(0o755)
            failed = fx.worker("integrate", "1", "--pr", "5", "--artifact", "ok", "--head", fx.head, check=False)
            self.assertEqual(failed.returncode, 1, failed.stdout + failed.stderr)
            self.assertIn("hook says no", failed.stderr)
            self.assert_untouched(fx, ledger, head, remote, branch, wt)
            hook.unlink()
            retry = fx.worker("integrate", "1", "--pr", "5", "--artifact", "ok", "--head", fx.head, check=False)
            self.assertEqual(retry.returncode, 0, retry.stdout + retry.stderr)
            self.assertEqual(git("rev-list", "--first-parent", "--count", f"{head}..HEAD", cwd=fx.ws), "1")
            self.assertEqual(fx.row("1")["status"], "done")
            self.assertEqual(fx.row("2")["status"], "doing")
            self.assertFalse(wt.exists())

    def test_failing_ledger_update_restores_the_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fx, branch, wt = self.setup_failing(tmp)
            ledger = (fx.ws / "progress.tsv").read_bytes()
            head = git("rev-parse", "HEAD", cwd=fx.ws)
            remote = git("ls-remote", "--heads", "origin", "goal/demo", cwd=fx.ws)
            failed = fx.worker("integrate", "1", "--pr", "5", "--artifact", "-", "--head", fx.head, check=False)
            self.assertEqual(failed.returncode, 1, failed.stdout + failed.stderr)
            self.assertIn("ledger update failed", failed.stderr)
            self.assert_untouched(fx, ledger, head, remote, branch, wt)


if __name__ == "__main__":
    unittest.main()
