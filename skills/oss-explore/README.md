# oss-explore

GitHub 오픈소스를 주제로 발견하고, 후보를 비교한 뒤 필요하면 기여와 회고까지 잇는 `gh` 기반 shared skill입니다. 런타임 계약은 [`SKILL.md`](./SKILL.md), 전체 옵션과 JSON 스키마는 [`references/commands.md`](./references/commands.md)가 정본입니다.

## 역할

- 일반 탐색: 이름/설명과 토픽을 우선하고 후보가 부족할 때 README 검색으로 채웁니다.
- 비교: 검색 근거, 라이선스, 최근 push, 언어를 함께 보여줍니다.
- 기여: 요청할 때만 good first issue/help wanted를 보강합니다.
- 회고: 외부 OSS 머지 PR과 기여 통계를 정리합니다.

star는 인기도 신호로만 사용합니다. 기본 탐색은 관련도 계층을 먼저 적용하고 같은 계층 안에서 star/최근 활동/fork 수로 정렬합니다.

## 구조

- `scripts/explore.sh`: 주제 탐색과 후보 비교
- `scripts/discover.sh`: 기여 이슈 발굴
- `scripts/trending.sh`, `trending.py`: `https://github.com/trending`의 전체/언어별 일간, 주간, 월간 탐색
- `scripts/bootstrap.sh`: fork/clone/브랜치 준비
- `scripts/contributions.sh`, `stats.sh`: 기여 회고
- `scripts/render_html.py`: 탐색/회고 HTML 렌더링
- `tests/test-explore.sh`: 관련도 계층, README fallback, 비라틴 주제 회귀 확인
- `tests/test-operations.sh`: 공개 범위, 조회 실패, 캐시 보존, 검색 상한, 입력 검증 확인
- `tests/test-trending.py`: Trending 정상/빈 결과/부분 마크업 변경 판별 확인

## 설계 출처

- [GitHub repository search](https://docs.github.com/en/search-github/searching-on-github/searching-for-repositories): 이름/설명/README, 토픽, 라이선스, 활동 필터
- [GitHub community profile metrics](https://docs.github.com/en/rest/metrics/community): README, LICENSE, CONTRIBUTING, Code of Conduct 존재 여부
- [GitHub Topics](https://github.com/topics): 분야별 자기분류 신호
- [awesome-for-beginners](https://github.com/MunGell/awesome-for-beginners): 비기너 라벨과 큐레이션 시드
- [up-for-grabs](https://github.com/up-for-grabs/up-for-grabs.net), [goodfirstissue.dev](https://github.com/DeepSourceCorp/good-first-issue): 기여 이슈 발굴 패턴
- [gh-oss-stats](https://github.com/mabd-dev/gh-oss-stats), [RepoSense](https://github.com/reposense/RepoSense): 외부 기여 집계와 identity 아이디어

## 유지보수 우선순위

1. 실제 검색 질 회귀를 먼저 확인합니다. 대표 주제에서 약한 인기 레포가 상위 shortlist를 밀어내지 않아야 합니다.
2. GitHub HTML 구조에 의존하는 Trending 파서를 주기적으로 확인합니다.
3. 깊이 비교 자동화는 README/릴리스/community profile 확인이 반복 비용으로 확인될 때만 추가합니다.

남은 후보는 관련 토픽 확장, 저장된 shortlist diff, 다계정 identity 통합입니다. 별도 모드보다 기존 명령의 작은 옵션으로 해결 가능한지 먼저 봅니다.
