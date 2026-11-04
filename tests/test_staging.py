#!/usr/bin/env python3
"""플러그인 staging을 임시 fixture로 검사한다. 실제 정본은 읽지 않는다."""

import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
STAGER = ROOT / "scripts" / "stage-skills.sh"


class StagingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="astack-staging-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "source with spaces"
        self.stage = self.root / "stage with spaces"
        self.source.mkdir()
        self.stage.mkdir()
        self.write("sample/SKILL.md", "~/.agents/skills/shared/sample/\n")

    def write(self, relative, content="fixture\n"):
        path = self.source / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def run_stage(self, *skills, stage=None):
        return subprocess.run(
            ["bash", str(STAGER), str(self.source), str(stage or self.stage), *skills],
            capture_output=True,
            text=True,
            timeout=20,
        )

    def assert_ok(self, result):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_normalizes_only_skill_and_reference_markdown(self):
        original = "$HOME/.agents/skills/shared/other/\n"
        self.write("sample/references/nested/usage.md", original)
        self.write("sample/README.md", original)
        script = self.write("sample/scripts/tool.sh", "#!/bin/sh\n")
        script.chmod(0o755)
        self.write("sample/data.bin", "binary fixture")
        self.assert_ok(self.run_stage("sample"))
        self.assertEqual(
            (self.stage / "sample/SKILL.md").read_text(),
            "${CLAUDE_PLUGIN_ROOT}/skills/sample/\n",
        )
        self.assertEqual(
            (self.stage / "sample/references/nested/usage.md").read_text(),
            "${CLAUDE_PLUGIN_ROOT}/skills/other/\n",
        )
        self.assertEqual((self.stage / "sample/README.md").read_text(), original)
        self.assertTrue(os.access(self.stage / "sample/scripts/tool.sh", os.X_OK))
        self.assertEqual(script.read_text(), "#!/bin/sh\n")
        self.assertEqual(list(self.stage.rglob("*.bak")), [])

    def test_excludes_runtime_and_personal_files(self):
        excluded = (
            ".env", ".venv/config", ".git/config", ".cache/data",
            "node_modules/pkg/index.js", "__pycache__/module.pyc", "module.pyc",
            ".pytest_cache/v/cache", ".ruff_cache/data", ".DS_Store",
            ".omc/state", "prompts/log.json", "work/recording.wav",
            "references/transcripts/raw.txt", "references/corrections.json",
        )
        for relative in excluded:
            self.write("sample/" + relative)
        self.write("sample/.env.example", "CONFIG_FILE=<path>\n")
        self.write("sample/assets/retained.txt")
        self.assert_ok(self.run_stage("sample"))
        for relative in excluded:
            self.assertFalse((self.stage / "sample" / relative).exists(), relative)
        self.assertTrue((self.stage / "sample/.env.example").is_file())
        self.assertTrue((self.stage / "sample/assets/retained.txt").is_file())

    def test_bundles_crawl_helpers_only_when_crawl_is_selected(self):
        self.write("crawl/SKILL.md", "crawl\n")
        self.write("crawl/scripts/transcribe_ids.py")
        for name in ("captions.py", "fetch-subs.sh"):
            self.write("youtube/scripts/" + name, name + "\n")
        self.assert_ok(self.run_stage("crawl"))
        for name in ("captions.py", "fetch-subs.sh", "transcribe_ids.py"):
            self.assertTrue((self.stage / "crawl/scripts" / name).is_file())
        second = self.root / "other stage"
        second.mkdir()
        self.assert_ok(self.run_stage("sample", stage=second))
        self.assertFalse((second / "crawl").exists())

    def test_missing_source_or_helper_fails_without_partial_copy(self):
        result = self.run_stage("sample", "missing")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(list(self.stage.iterdir()), [])
        self.write("crawl/SKILL.md")
        result = self.run_stage("crawl")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("helper", result.stderr)
        self.assertEqual(list(self.stage.iterdir()), [])

    def test_rejects_unsafe_skill_names(self):
        for skill in ("../outside", "/absolute", "", "sample/name"):
            with self.subTest(skill=skill):
                self.assertNotEqual(self.run_stage(skill).returncode, 0)
        self.assertEqual(list(self.stage.iterdir()), [])

    def test_rejects_nonempty_or_symlink_stage(self):
        retained = self.stage / "retained"
        retained.write_text("do not change\n")
        self.assertNotEqual(self.run_stage("sample").returncode, 0)
        self.assertEqual(retained.read_text(), "do not change\n")
        alias = self.root / "alias"
        alias.symlink_to(self.source, target_is_directory=True)
        self.assertNotEqual(self.run_stage("sample", stage=alias).returncode, 0)
        self.assertTrue((self.source / "sample/SKILL.md").exists())

    def test_repeatable_for_independent_empty_stages(self):
        self.assert_ok(self.run_stage("sample"))
        second = self.root / "second"
        second.mkdir()
        self.assert_ok(self.run_stage("sample", stage=second))
        self.assertEqual(
            (self.stage / "sample/SKILL.md").read_bytes(),
            (second / "sample/SKILL.md").read_bytes(),
        )

    def test_rsync_failure_is_not_reported_as_success(self):
        fake_bin = self.root / "bin"
        fake_bin.mkdir()
        rsync = fake_bin / "rsync"
        rsync.write_text("#!/bin/sh\nexit 23\n")
        rsync.chmod(0o755)
        env = dict(os.environ, PATH=str(fake_bin) + os.pathsep + os.environ["PATH"])
        result = subprocess.run(
            ["bash", str(STAGER), str(self.source), str(self.stage), "sample"],
            env=env, capture_output=True, text=True, timeout=20,
        )
        self.assertEqual(result.returncode, 23, result.stderr)


class SyncIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="astack-sync-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.plugin = self.root / "plugin"
        self.shared = self.root / "agents/skills/shared"
        scripts = self.plugin / "scripts"
        scripts.mkdir(parents=True)
        for name in ("sync.sh", "stage-skills.sh"):
            shutil.copyfile(ROOT / "scripts" / name, scripts / name)
        sync = (scripts / "sync.sh").read_text()
        skills = re.search(r"SKILLS=\((.*?)\)", sync, re.DOTALL).group(1).split()
        for skill in skills:
            path = self.shared / skill / "SKILL.md"
            path.parent.mkdir(parents=True)
            path.write_text("~/.agents/skills/shared/sample/\n")
        crawl_scripts = self.shared / "crawl/scripts"
        crawl_scripts.mkdir(parents=True)
        (crawl_scripts / "transcribe_ids.py").write_text("fixture\n")
        helpers = self.shared / "youtube/scripts"
        helpers.mkdir(parents=True)
        for name in ("captions.py", "fetch-subs.sh"):
            (helpers / name).write_text("fixture\n")
        self.validators = self.shared / "skill-manager/scripts"
        self.validators.mkdir(parents=True)
        for name in ("quick_validate.py", "lint_skill_authoring.py"):
            (self.validators / name).write_text("raise SystemExit(0)\n")
        tests = self.plugin / "tests"
        tests.mkdir()
        (tests / "test_repository.py").write_text("print('fixture repository check')\n")
        self.env = dict(os.environ, AGENTS_ROOT=str(self.root / "agents"))

    def run_sync(self):
        return subprocess.run(
            ["bash", str(self.plugin / "scripts/sync.sh")],
            env=self.env, capture_output=True, text=True, timeout=45,
        )

    def test_sync_uses_stager_and_repeated_run_is_content_stable(self):
        first = self.run_sync()
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        path = self.plugin / "skills/agent-team/SKILL.md"
        expected = b"${CLAUDE_PLUGIN_ROOT}/skills/sample/\n"
        self.assertEqual(path.read_bytes(), expected)
        second = self.run_sync()
        self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
        self.assertEqual(path.read_bytes(), expected)
        self.assertIn("fixture repository check", second.stdout)

    def assert_preserved_on_failure(self):
        destination = self.plugin / "skills"
        destination.mkdir()
        retained = destination / "retained"
        retained.write_text("existing distribution\n")
        result = self.run_sync()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertEqual(retained.read_text(), "existing distribution\n")
        self.assertEqual(list(destination.iterdir()), [retained])

    def test_stage_failure_does_not_replace_distribution(self):
        (self.plugin / "scripts/stage-skills.sh").write_text("#!/bin/sh\nexit 23\n")
        self.assert_preserved_on_failure()

    def test_validation_failure_does_not_replace_distribution(self):
        (self.validators / "quick_validate.py").write_text("raise SystemExit(1)\n")
        self.assert_preserved_on_failure()


if __name__ == "__main__":
    unittest.main(verbosity=2)
