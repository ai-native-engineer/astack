# Style Profiles

Use this reference when a message should match a specific person, team, or organization voice.

## Routing

- First apply `references/work-message-contract.md`; style never overrides factual clarity or send/edit safety.
- Read profiles from `$HOME/.config/communication/styles/`; shared skill files contain no personal or organization profile.
- Use `default.md` for "내 말투" and `<slug>.md` for a named person, team, or organization.
- If a matching local profile exists, read it after the common communication rules.
- If no matching profile exists and the user wants reusable tone matching, create a new profile from `templates/style.md` with `scripts/create-style-profile.py`.
- Do not edit `templates/style.md` for one person's preferences. Put person/team-specific choices in the local profile directory.
- If no profile exists, use the common contract and current-message instructions; do not invent personal preferences.
- One-off rewrites do not need a generated profile. Generate only when the user asks for reuse or a named profile.

## Create A Profile

Run the generator from the skill root:

```bash
python3 scripts/create-style-profile.py --name "Person or Team" --slug "person-or-team"
```

Useful optional fields:

```bash
python3 scripts/create-style-profile.py \
  --name "Person or Team" \
  --slug "person-or-team" \
  --description "When to use this profile" \
  --voice "Direct, concise work handoff tone" \
  --default-ending "~입니다" \
  --sentence-pattern "결론은 [X]입니다. 근거는 [Y]입니다. 그래서 [Z]로 가겠습니다." \
  --avoid "Repeated softeners"
```

The script writes `$HOME/.config/communication/styles/<slug>.md`. Use `--dry-run` to preview and `--force` to replace an existing generated profile. Use `--output` only when the user explicitly chose another local path.

## Profile Authoring Rules

- Capture observable writing behavior, not personality guesses.
- Keep it operational: voice, default endings, sentence patterns, structure preferences, mention rules, avoid list.
- Include weak/better examples if the profile is easy to misuse.
- Keep reusable team rules in `work-message-contract.md`; keep only person/team-specific preferences in the style profile.
- If a profile conflicts with the user's explicit instruction for the current message, follow the current instruction.
