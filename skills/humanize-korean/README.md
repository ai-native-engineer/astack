# humanize-korean

한글 텍스트의 AI 티를 한 번의 호출로 탐지, 윤문, 자체검증하는 스킬이다. 사람용 설명이고, 에이전트가 따르는 규칙은 `SKILL.md`와 `references/`에 있다.

## 출처

- [epoko77-ai/im-not-ai](https://github.com/epoko77-ai/im-not-ai)(MIT)의 Codex용 한 번 호출 경로(fast path)를 들여왔다. 들여온 룰북은 v2.0이다(`references/quick-rules.md` 제목).
- 분류 체계(`references/ai-tell-taxonomy.md`), 처방(`references/rewriting-playbook.md`), 학술 근거(`references/scholarship.md`)가 원본에서 왔다.
- 원본의 정밀 경로(진단, 겨냥 윤문, 마무리를 나눠 부르는 `--strict`)는 이 스킬에 없다. 필요하면 원본 플러그인을 설치해 쓴다. 그래서 등급 C/D 안내는 정밀 모드를 권하지 않고 남은 구간을 사용자에게 보인다.
