#!/usr/bin/env python3
"""Create a local communication style profile from templates/style.md."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TEMPLATE = SKILL_ROOT / "templates" / "style.md"
DEFAULT_OUTPUT_DIR = Path.home() / ".config" / "communication" / "styles"


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9._-]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-._")
    return value


def bullet_block(items: list[str], fallback: str) -> str:
    if not items:
        return f"- TODO: {fallback}"
    return "\n".join(f"- {item.strip()}" for item in items if item.strip())


def code_bullet_block(items: list[str], fallback: str) -> str:
    if not items:
        return f"- `TODO: {fallback}`"
    lines: list[str] = []
    for item in items:
        item = item.strip()
        if not item:
            continue
        if item.startswith("`") and item.endswith("`"):
            lines.append(f"- {item}")
        else:
            lines.append(f"- `{item}`")
    return "\n".join(lines)


def render(template: str, replacements: dict[str, str]) -> str:
    rendered = template
    for key, value in replacements.items():
        rendered = rendered.replace("{{" + key + "}}", value)
    return rendered


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a local style profile from templates/style.md."
    )
    parser.add_argument("--name", required=True, help="Profile display name.")
    parser.add_argument(
        "--slug",
        help="ASCII file slug. Required when --name cannot produce an ASCII slug.",
    )
    parser.add_argument(
        "--description",
        default="this person/team voice should be matched in outbound work messages",
        help="When agents should use this profile.",
    )
    parser.add_argument("--owner", help="Profile owner. Defaults to --name.")
    parser.add_argument("--voice", action="append", default=[], help="Voice rule.")
    parser.add_argument(
        "--work-default",
        action="append",
        default=[],
        help="Operational writing default.",
    )
    parser.add_argument(
        "--default-ending",
        action="append",
        default=[],
        help="Preferred sentence ending, e.g. '~입니다'.",
    )
    parser.add_argument(
        "--sentence-pattern",
        action="append",
        default=[],
        help="Reusable sentence pattern.",
    )
    parser.add_argument("--avoid", action="append", default=[], help="Avoid rule.")
    parser.add_argument(
        "--mention-rule",
        action="append",
        default=[],
        help="Mention or naming rule.",
    )
    parser.add_argument(
        "--weak-example",
        default="[weak example to avoid]",
        help="Weak style example.",
    )
    parser.add_argument(
        "--better-example",
        default="[better version in this profile's voice]",
        help="Better style example.",
    )
    parser.add_argument(
        "--template",
        default=str(DEFAULT_TEMPLATE),
        help="Template path. Defaults to templates/style.md.",
    )
    parser.add_argument(
        "--output",
        help="Output path. Defaults to ~/.config/communication/styles/<slug>.md.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the generated profile instead of writing it.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing output file.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    slug = args.slug or slugify(args.name)
    if not slug:
        print("error: --slug is required when --name has no ASCII slug", file=sys.stderr)
        return 2

    template_path = Path(args.template).expanduser()
    if not template_path.is_absolute():
        template_path = SKILL_ROOT / template_path
    if not template_path.exists():
        print(f"error: template not found: {template_path}", file=sys.stderr)
        return 2

    output_path = (
        Path(args.output).expanduser()
        if args.output
        else DEFAULT_OUTPUT_DIR / f"{slug}.md"
    )
    if not output_path.is_absolute():
        output_path = SKILL_ROOT / output_path

    replacements = {
        "PROFILE_NAME": args.name,
        "PROFILE_SLUG": slug,
        "PROFILE_DESCRIPTION": args.description,
        "PROFILE_OWNER": args.owner or args.name,
        "VOICE_BULLETS": bullet_block(args.voice, "describe the voice in observable terms"),
        "WORK_DEFAULTS": bullet_block(args.work_default, "describe operational defaults"),
        "DEFAULT_ENDINGS": code_bullet_block(args.default_ending, "preferred endings"),
        "SENTENCE_PATTERNS": code_bullet_block(args.sentence_pattern, "sentence pattern"),
        "AVOID_BULLETS": bullet_block(args.avoid, "phrasing or behavior to avoid"),
        "MENTION_RULES": bullet_block(args.mention_rule, "mention and naming preferences"),
        "WEAK_EXAMPLE": args.weak_example,
        "BETTER_EXAMPLE": args.better_example,
    }

    content = render(template_path.read_text(encoding="utf-8"), replacements)

    if args.dry_run:
        print(content)
        return 0

    if output_path.exists() and not args.force:
        print(f"error: output exists, pass --force to replace: {output_path}", file=sys.stderr)
        return 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
