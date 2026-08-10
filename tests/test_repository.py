#!/usr/bin/env python3
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"


def frontmatter(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    assert match, f"missing YAML frontmatter: {path}"
    return match.group(1)


def main() -> None:
    skill_dirs = sorted(path for path in SKILLS.iterdir() if path.is_dir())
    skill_names = {path.name for path in skill_dirs}

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    readme_names = set(re.findall(r"^\| `([a-z0-9-]+)` \|", readme, re.MULTILINE))
    assert readme_names == skill_names, (
        f"README/skills mismatch: missing={sorted(skill_names - readme_names)}, "
        f"extra={sorted(readme_names - skill_names)}"
    )

    for skill_dir in skill_dirs:
        skill_md = skill_dir / "SKILL.md"
        assert skill_md.is_file(), f"missing SKILL.md: {skill_dir}"
        metadata = frontmatter(skill_md)
        name = re.search(r"^name:\s*[\"']?([^\"'\n]+)", metadata, re.MULTILINE)
        assert name and name.group(1).strip() == skill_dir.name, f"name mismatch: {skill_md}"
        assert re.search(r"^description:\s*\S", metadata, re.MULTILINE), f"missing description: {skill_md}"

    for helper in ("extract_transcript.sh", "srt-to-md.sh"):
        assert (SKILLS / "crawl" / "scripts" / helper).is_file(), f"missing bundled crawl helper: {helper}"

    forbidden_paths = {
        "/Users/": "user-specific absolute path",
        "$HOME/.agents/skills/shared/": "untranslated shared-skill path",
        "~/.agents/skills/shared/": "untranslated shared-skill path",
        "skills/shared/": "working-directory-dependent shared-skill path",
        "$HOME/Dev/": "user-specific development path",
        "~/Dev/": "user-specific development path",
        "~/scripts/": "user-specific scripts path",
        "/opt/homebrew/bin/python3": "hardcoded Python path",
        'Path.home() / ".local/bin/crwl"': "hardcoded crwl path",
    }
    path_violations = []
    for path in SKILLS.rglob("*"):
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for needle, reason in forbidden_paths.items():
            if needle in text:
                path_violations.append(f"{path.relative_to(ROOT)}: {reason} ({needle})")
    assert not path_violations, "non-portable paths:\n" + "\n".join(path_violations)

    tracked = subprocess.check_output(
        ["git", "-C", str(ROOT), "ls-files", "-z"], text=True
    ).split("\0")
    forbidden = []
    for relative in filter(None, tracked):
        path = ROOT / relative
        if path.is_symlink() or path.name in {".env", ".venv", "__pycache__"} or path.suffix == ".pyc":
            forbidden.append(relative)
    assert not forbidden, f"forbidden runtime artifacts: {forbidden}"

    plugin = json.loads((ROOT / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
    marketplace = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
    codex_plugin = json.loads((ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    codex_marketplace = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
    assert plugin["name"] == "astack"
    assert plugin["version"] == codex_plugin["version"] == "0.2.1"
    assert marketplace["name"] == "astack"
    assert any(
        item.get("name") == "astack"
        and item.get("source") == "./"
        and item.get("version") == plugin["version"]
        for item in marketplace["plugins"]
    )
    assert codex_plugin["skills"] == "./skills/"
    assert any(item.get("name") == "astack" for item in codex_marketplace["plugins"])

    print(f"astack repository checks: pass ({len(skill_dirs)} skills)")


if __name__ == "__main__":
    main()
