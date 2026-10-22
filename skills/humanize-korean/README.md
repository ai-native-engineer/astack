# humanize-korean

한글 텍스트의 AI 티를 한 번의 호출로 탐지, 윤문, 자체검증하는 스킬이다. 사람용 설명이고, 에이전트가 따르는 규칙은 `SKILL.md`와 `references/`에 있다.

## 출처

- [epoko77-ai/im-not-ai](https://github.com/epoko77-ai/im-not-ai)(MIT)의 Codex용 한 번 호출 경로(fast path)를 들여왔다. 들여온 룰북은 v2.0이다(`references/quick-rules.md` 제목).
- 분류 체계(`references/ai-tell-taxonomy.md`), 처방(`references/rewriting-playbook.md`), 학술 근거(`references/scholarship.md`)가 원본에서 왔다.
- 원본의 정밀 경로(진단, 겨냥 윤문, 마무리를 나눠 부르는 `--strict`)는 이 스킬에 없다. 필요하면 원본 플러그인을 설치해 쓴다. 이 스킬은 완료, 검토 필요, 부분 처리로 결과 범위를 구분하고 남은 구간과 이유를 사용자에게 보인다.

## 이 저장소의 적용 범위

원본의 분류·예시·학술 출처는 보존한다. 입력 길이, 변경률, 재시도 횟수와 문장 비율을 모델의 처리 한계나 합격 기준으로 삼지는 않는다. 문맥에서 필요한 표현을 남기고 의미·인용·수치·장르·전체 입력 반영 여부를 검증하는 기준으로 조정했다. 실제 행동 지침은 `SKILL.md`와 이에 맞춘 참조 문서가 정본이다.
