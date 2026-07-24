# HTML Explainer

로컬에서 바로 열 수 있는 단일 HTML 설명 자료를 만드는 shared skill이다. 실행 지침의 정본은 `SKILL.md`와 `references/`이며, 이 문서는 유지보수자를 위한 구조와 출처만 설명한다.

## 구조

- `SKILL.md`: 타입 선택, 생성, 검증 워크플로
- `references/`: 타입별 스택과 작성 규칙
- `assets/template.html`: 시각형 기본 템플릿
- `assets/interactive-template.html`: 인터랙티브형 기본 템플릿
- `assets/01-*.html`부터 `assets/20-*.html`: 용도별 단일 HTML 예시 템플릿
- `assets/AGENTS.md`: 20개 예시 템플릿 카탈로그
- `scripts/verify.sh`: 브라우저 렌더 검증

## 참고 자료와 출처

20개 예시 템플릿은 Anthropic의 [The unreasonable effectiveness of HTML](https://github.com/anthropics/html-effectiveness) 저장소에서 가져왔다. 원본 파일명과 내용을 유지했으며, 가져온 revision은 `58c305be97f47b26b678f2c07dec01d4242268ec`이다.

원본은 MIT License로 배포된다. 저작권과 라이선스 전문은 `assets/html-effectiveness-LICENSE.txt`에 보존한다.

## 유지보수

번호가 붙은 파일은 결과물 유형과 정보 구조를 참고하는 예시다. 실제 생성물은 `SKILL.md`의 타입별 규칙과 검증 절차를 따른다. 업스트림을 갱신할 때는 20개 HTML과 라이선스 고지를 함께 교체하고 skill-manager 검증을 다시 실행한다.
