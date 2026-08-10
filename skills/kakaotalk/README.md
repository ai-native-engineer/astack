# KakaoTalk skill

## Source

- [NomaDamas/katok](https://github.com/NomaDamas/katok)

## Integrated boundary

- Reading, search, and sending all go through the `katok` CLI. The skill duplicates none of its
  database access, decryption, room matching, or Accessibility handling.
- Sending previously lived in a local Python Accessibility transport shipped with this skill.
  `katok send` replaced it: the CLI refuses ambiguous room names instead of guessing, matches
  rooms by member set rather than by string, and offers `--dry-run` and `--draft` so targeting
  and wording can be checked without delivering anything.

## Behavior rules

AI behavior rules live in `SKILL.md` and `references/`. This file is background for people.
