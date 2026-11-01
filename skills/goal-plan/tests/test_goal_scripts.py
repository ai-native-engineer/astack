#!/usr/bin/env python3
"""Runnable checks for goal-plan scaffold options, the /goal condition line, and the result PR script."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parent.parent
INIT = SKILL_ROOT / "scripts" / "init_goal_plan.py"
GOAL_LOG = SKILL_ROOT / "scripts" / "goal_log.py"
GOAL_PR = SKILL_ROOT / "scripts" / "goal_pr.py"
GIT_ENV = {
    "GIT_AUTHOR_NAME": "goal-plan tests", "GIT_AUTHOR_EMAIL": "tests@example.invalid",
    "GIT_COMMITTER_NAME": "goal-plan tests", "GIT_COMMITTER_EMAIL": "tests@example.invalid",
    "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_NOSYSTEM": "1", "HOME": "/nonexistent", "PATH": "/usr/bin:/bin:/opt/homebrew/bin:/usr/local/bin",
}


def run(*cmd: str, cwd: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(list(cmd), cwd=cwd, capture_output=True, text=True, check=check, env=GIT_ENV)


def git(*args: str, cwd: Path) -> str:
    return run("git", *args, cwd=cwd).stdout.strip()


def commit_all(cwd: Path, message: str) -> None:
    git("add", "-A", cwd=cwd)
    git("commit", "-q", "-m", message, cwd=cwd)


class ScaffoldOptionTests(unittest.TestCase):
    def test_goal_contains_harness_sections_and_issue(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "goal"
            result = subprocess.run(
                [sys.executable, str(INIT), str(target), "--goal", "ship it", "--issue", "42"],
                capture_output=True, text=True, check=True,
            )
            goal = (target / "GOAL.md").read_text(encoding="utf-8")
            for section in ("## Environment", "## Verification Layers", "## GitHub Flow"):
                self.assertIn(section, goal)
            self.assertIn("tracking issue: #42.", goal)
            self.assertNotIn("{{", goal)
            self.assertIn("condition", result.stdout)
            self.assertNotIn("/goal @GOAL.md", result.stdout)

    def test_issue_must_be_a_number(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [sys.executable, str(INIT), str(Path(tmp) / "goal"), "--goal", "ship it", "--issue", "later"],
                capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("--issue must be an issue number", result.stderr)


def fill_goal(goal_path: Path, *, bounds: str = "stop after 20 turns", decisions: str | None = None,
              criteria: str | None = None) -> None:
    """Replace every template TBD with an answer, the way a finished interview would."""
    lines = []
    section = ""
    for line in goal_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            section = line[3:].strip()
        if line.startswith("TBD"):
            line = {"Bounds": bounds}.get(section, "none")
        if line.startswith("| ") and "TBD" in line:
            line = line.replace("TBD", "exists", 1).replace("TBD", "`true`")
        if line.startswith("- <axis>"):
            continue
        if line.startswith("- AC-"):
            continue
        if line.startswith("- cannot start here: TBD"):
            line = "- cannot start here: nothing"
        if line.startswith("- row issues: TBD"):
            line = "- row issues: sub-issues of the tracking issue, one per row"
        if line.startswith("- result PR: base branch TBD"):
            line = "- result PR: base branch main"
        if line.startswith("- tracking issue: TBD"):
            line = "- tracking issue: #7."
        lines.append(line)
    text = "\n".join(lines) + "\n"
    text = text.replace("## Decisions\n\nnone\n",
                        "## Decisions\n\n" + (decisions or '- Proof (2026-01-01): "pytest면 충분". Unit suite only.') + "\n", 1)
    text = text.replace("## Acceptance Criteria\n\nnone\n",
                        "## Acceptance Criteria\n\n" + (criteria or "Covered by Proof.") + "\n", 1)
    goal_path.write_text(text, encoding="utf-8")


class ConditionTests(unittest.TestCase):
    def test_condition_refuses_tbd_and_prints_goal_line(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "goal"
            subprocess.run([sys.executable, str(INIT), str(target), "--goal", "all tests pass"],
                           capture_output=True, text=True, check=True)
            refused = subprocess.run([sys.executable, str(GOAL_LOG), "condition"],
                                     cwd=target, capture_output=True, text=True)
            self.assertEqual(refused.returncode, 2)
            self.assertIn("fill ## Goal and ## Proof", refused.stderr)

            subprocess.run([sys.executable, str(INIT), str(target), "--goal", "all tests pass",
                            "--proof-command", "pytest -q"],
                           capture_output=True, text=True, check=True)
            goal_path = target / "GOAL.md"
            unfinished = subprocess.run([sys.executable, str(GOAL_LOG), "condition"],
                                        cwd=target, capture_output=True, text=True)
            self.assertEqual(unfinished.returncode, 2)
            self.assertIn("not ready for an unattended loop", unfinished.stderr)
            self.assertIn("## Environment still says TBD", unfinished.stderr)
            self.assertIn("## Decisions has no recorded interview answer", unfinished.stderr)
            self.assertNotIn("/goal", unfinished.stdout)

            fill_goal(goal_path)
            printed = subprocess.run([sys.executable, str(GOAL_LOG), "condition"],
                                     cwd=target, capture_output=True, text=True, check=True)
            line = printed.stdout.strip()
            self.assertTrue(line.startswith("/goal all tests pass."))
            self.assertIn("Proof: run `pytest -q` and show its output.", line)
            self.assertIn("Follow GOAL.md end to end", line)
            self.assertIn("Bounds: stop after 20 turns", line)
            self.assertLess(len(line), 4000)

    def test_condition_checks_only_emptiness(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "goal"
            subprocess.run([sys.executable, str(INIT), str(target), "--goal", "all tests pass",
                            "--proof-command", "pytest -q"],
                           capture_output=True, text=True, check=True)
            goal_path = target / "GOAL.md"

            fill_goal(goal_path, criteria="- AC-1: WHEN pytest runs THE SUITE SHALL pass.\n"
                                          "- AC-2: WHEN lint runs THE TREE SHALL be clean. Proof: `biome check .` exits 0.")
            missing_proof = subprocess.run([sys.executable, str(GOAL_LOG), "condition"],
                                           cwd=target, capture_output=True, text=True)
            self.assertEqual(missing_proof.returncode, 2)
            self.assertIn("- AC-1 has no 'Proof:'", missing_proof.stderr)
            self.assertNotIn("AC-2", missing_proof.stderr)

            subprocess.run([sys.executable, str(INIT), str(target), "--goal", "all tests pass",
                            "--proof-command", "pytest -q"],
                           capture_output=True, text=True, check=True)  # fresh template again
            fill_goal(goal_path, decisions="- Scope (2026-01-01): accepted default. Only src/.",
                      criteria="- AC-1: WHEN pytest runs THE SUITE SHALL pass. Proof: `pytest -q` exits 0.")
            text = goal_path.read_text(encoding="utf-8").replace("## Bounds\n\nstop after 20 turns",
                                                                 "## Bounds\n\nnone", 1)
            goal_path.write_text(text, encoding="utf-8")
            ok = subprocess.run([sys.executable, str(GOAL_LOG), "condition"],
                                cwd=target, capture_output=True, text=True, check=True)
            self.assertTrue(ok.stdout.startswith("/goal all tests pass."))
            self.assertNotIn("Bounds:", ok.stdout)


class ResultPrTests(unittest.TestCase):
    def make_repo(self, tmp: Path) -> tuple[Path, Path]:
        origin = tmp / "origin.git"
        run("git", "init", "-q", "--bare", "--initial-branch=main", str(origin), cwd=tmp)
        repo = tmp / "repo"
        run("git", "clone", "-q", str(origin), str(repo), cwd=tmp)
        git("checkout", "-q", "-b", "main", cwd=repo)
        (repo / "README.md").write_text("# demo\n", encoding="utf-8")
        commit_all(repo, "chore: init")
        git("push", "-q", "-u", "origin", "main", cwd=repo)
        git("remote", "set-head", "origin", "main", cwd=repo)
        git("checkout", "-q", "-b", "goal/demo", cwd=repo)
        subprocess.run([sys.executable, str(INIT), str(repo), "--goal", "demo", "--proof-command", "true"],
                       capture_output=True, text=True, check=True)
        commit_all(repo, "chore(goal): plan")
        (repo / "src").mkdir()
        (repo / "src" / "app.py").write_text("print('hi')\n", encoding="utf-8")
        (repo / "progress.tsv").write_text(
            (repo / "progress.tsv").read_text(encoding="utf-8") + "1\tdone\tkeep\tapp\tprints\tabc\tok\t-\t-\n",
            encoding="utf-8")
        commit_all(repo, "feat(app): print hi (row 1 keep)")
        return origin, repo

    def test_dry_run_builds_branch_without_scaffold(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            origin, repo = self.make_repo(Path(tmp))
            result = run(sys.executable, str(GOAL_PR), "--branch", "feat/demo-result", "--dry-run", cwd=repo)
            self.assertIn("dry run", result.stdout)
            files = git("ls-tree", "-r", "--name-only", "feat/demo-result", cwd=repo).splitlines()
            self.assertIn("src/app.py", files)
            self.assertIn("README.md", files)
            for scaffold in ("GOAL.md", "progress.tsv", ".claude/settings.json", ".codex/hooks.json"):
                self.assertNotIn(scaffold, files)
            self.assertEqual(git("branch", "--show-current", cwd=repo), "goal/demo")
            self.assertEqual(git("ls-remote", "--heads", "origin", "feat/demo-result", cwd=repo), "")
            self.assertEqual(git("worktree", "list", "--porcelain", cwd=repo).count("worktree "), 1)
            self.assertIn("src/app.py", result.stdout)

    def test_warns_on_commits_without_issue_number_and_numbers_scaffold_commit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            origin, repo = self.make_repo(Path(tmp))
            unnumbered = run(sys.executable, str(GOAL_PR), "--branch", "feat/demo-a", "--dry-run", cwd=repo)
            self.assertIn("warning: commit without an issue number", unnumbered.stderr)
            self.assertIn("feat(app): print hi (row 1 keep)", unnumbered.stderr)
            self.assertNotIn("remove goal scaffold", unnumbered.stderr)

            goal_path = repo / "GOAL.md"
            goal_path.write_text(goal_path.read_text(encoding="utf-8").replace(
                "tracking issue: TBD (`#N` or none)", "tracking issue: #42", 1), encoding="utf-8")
            (repo / "src" / "app.py").write_text("print('hi #42')\n", encoding="utf-8")
            commit_all(repo, "feat(app): greet (#42, row 2 keep)")
            numbered = run(sys.executable, str(GOAL_PR), "--branch", "feat/demo-b", "--dry-run", cwd=repo)
            self.assertNotIn("greet (#42", numbered.stderr)
            self.assertIn("print hi (row 1 keep)", numbered.stderr)
            subject = git("log", "-1", "--format=%s", "feat/demo-b", cwd=repo)
            self.assertEqual(subject, "chore(goal): remove goal scaffold from result branch (#42)")

    def test_push_without_pr_and_include(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            origin, repo = self.make_repo(Path(tmp))
            run(sys.executable, str(GOAL_PR), "--branch", "feat/demo-result", "--no-pr",
                "--include", "GOAL.md", cwd=repo)
            self.assertIn("feat/demo-result", git("ls-remote", "--heads", "origin", cwd=repo))
            files = git("ls-tree", "-r", "--name-only", "origin/feat/demo-result", cwd=repo).splitlines()
            self.assertIn("GOAL.md", files)
            self.assertNotIn("progress.tsv", files)
            self.assertIn("remove goal scaffold", git("log", "-1", "--format=%s", "feat/demo-result", cwd=repo))

    def test_rejects_bad_branch_dirty_tree_and_missing_pr_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            origin, repo = self.make_repo(Path(tmp))
            bad = run(sys.executable, str(GOAL_PR), "--branch", "main", "--dry-run", cwd=repo, check=False)
            self.assertEqual(bad.returncode, 2)
            self.assertIn("<type>/<description>", bad.stderr)

            no_inputs = run(sys.executable, str(GOAL_PR), "--branch", "feat/x", cwd=repo, check=False)
            self.assertEqual(no_inputs.returncode, 2)
            self.assertIn("--title and --body-file", no_inputs.stderr)

            (repo / "src" / "app.py").write_text("print('changed')\n", encoding="utf-8")
            dirty = run(sys.executable, str(GOAL_PR), "--branch", "feat/x", "--dry-run", cwd=repo, check=False)
            self.assertEqual(dirty.returncode, 2)
            self.assertIn("uncommitted changes", dirty.stderr)


if __name__ == "__main__":
    unittest.main()
