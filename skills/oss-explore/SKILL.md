---
argument-hint: "[주제] [username]"
name: oss-explore
description: "GitHub open-source discovery, contribution entry-point finding, trending exploration, fork/clone/branch bootstrap, and contribution portfolio/stat reports using gh. Use when user asks 오픈소스 찾아줘, X 관련 OSS, good first issue, where to contribute, trending repos, 내 오픈소스 기여, contribution stats, or OSS portfolio. Do NOT use for private repo code review, generic GitHub issue triage, package docs lookup, or non-GitHub research."
---

# oss-explore

## Overview

`gh` CLI 위에 오픈소스 **발견 → 기여 → 회고**를 한 진입점으로 묶은 범용 툴킷. 출발점은 "기여 진입점"이 아니라 **분야 자체**다 — "마케팅 오픈소스 찾아줘" 같은 요청에 그 분야 레포를 찾고, 평가하고, 거기서 기여할 만한 곳까지 자동으로 보여준다.

주제·언어·기간·star 하한은 **전부 사용자 인자**이며 특정 분야/조직을 하드코딩하지 않는다 — 누구나 그대로 쓸 수 있다. 기여 집계는 **머지된 PR을 단일 기준**으로 삼는다(`gh search commits`는 `repository`를 `null`로 반환해 신뢰 불가).

스크립트는 모두 `scripts/`에 있고, 터미널 출력이 기본이며 `--json`(원시)·`--html`(리포트) 옵션을 가진다.
설치된 `oss-explore` 스킬 루트에서 `SC=scripts`로 두고 실행한다.

## 6가지 모드 (발견 → 기여 → 회고)

### 1. 주제로 발견 — `explore.sh "<주제>" [옵션]`
분야/키워드로 오픈소스를 **발견**한다. **키워드 검색**(이름/설명/README)과 **토픽 검색**(GitHub 토픽)을 둘 다 돌려 fullName 기준 병합·dedup → star/활성도/언어로 평가. **기본으로 각 레포의 기여 가능성(good first issue/help wanted 열린 이슈 수)을 자동 보강**해 "발견과 동시에 어디에 기여할 수 있는지"를 한 표에 보여준다(`--no-issues`로 끄면 빠른 발견 모드).
```bash
"$SC/explore.sh" "marketing" --min-stars 500          # 마케팅 OSS, star 500↑, 기여 가능성 포함
"$SC/explore.sh" "vector database" --language python  # 파이썬 벡터DB
"$SC/explore.sh" "음악" --sort updated --no-issues     # 최근 활성 순, 빠르게
"$SC/explore.sh" "legal" --html                        # HTML 리포트
```

### 2. 이슈 단위 기여 진입점 발굴 — `discover.sh [옵션]`
비기너 친화 라벨 동의어 **~10종**(good first issue / help wanted / first-timers-only / easy / beginner / starter ...)을 OR로 검색. **기여자 관점 기본값**: PR 연결된 이슈 제외(`--include-linked`로 포함), 1년 넘거나 blocked/wontfix/stale 제외(`--max-age`/`--stale-ok`), 상위 20건(`--top`). 💬 댓글수(🆕0=아직 아무도 안 집음). `--min-stars`로 양산/이벤트성 제거+star순. **`--curated`**는 awesome-for-beginners 검증 레포만, **`--hot`**은 "good first issue ≥5개인 활성 레포"를 star순, **`--summary`**는 언어별 집계.
```bash
"$SC/discover.sh" --language python                 # 비기너 라벨 전체·PR미연결·최근 1년
"$SC/discover.sh" --topic cli --sort comments-asc   # 아직 아무도 안 집은 이슈 우선
"$SC/discover.sh" --curated --language python       # 사람이 검증한 레포만(노이즈 최소)
```

### 3. 트렌딩 탐색 — `trending.sh [language] [옵션]`
github.com/trending 파싱. `--highlight`로 관심 키워드 강조(🔖), `--issues`로 각 레포의 good first issue/help wanted 수를 병렬 조회해 "트렌딩 ∩ 기여 가능" 확인.
```bash
"$SC/trending.sh" rust --since weekly
"$SC/trending.sh" typescript --issues                       # 기여 가능성 컬럼
```

### 4. 기여 워크플로 부트스트랩 — `bootstrap.sh <owner/repo> [branch] [옵션]`
fork → clone → 기여 브랜치 생성(upstream remote는 gh가 자동 설정). `--dry`로 명령만 미리보기.
```bash
"$SC/bootstrap.sh" owner/repo --dry      # 먼저 확인
"$SC/bootstrap.sh" owner/repo fix/typo   # 실제 실행
```
PR 생성은 자동화하지 않는다(레포별 규약이 다름). 부트스트랩 후: `git push -u origin <branch>` → `gh pr create --web`. 커밋/브랜치 규약은 `dev` 스킬의 git-convention 참고.

### 5. 기여 내역 정리 (회고) — `contributions.sh [username] [옵션]`
머지 PR을 "본인 소유가 아닌" 레포별로 집계 → **소속 조직 vs 순수 외부 OSS**로 분류 → 외부는 star 내림차순. username 생략/`@me`면 현재 로그인.
```bash
"$SC/contributions.sh"                 # 내 기여
"$SC/contributions.sh" --emit-markdown # 프로필 README/이력서용 shields.io 배지 테이블(외부 OSS만)
```

### 6. 기여 통계 (회고) — `stats.sh [username] [옵션]`
전체 PR 대비 머지율, **연도별·월별·요일별** 추이, 언어별 분포. HTML은 막대 차트. 레포별 언어 조회로 다소 느릴 수 있다.

각 스크립트의 전체 플래그·기본값은 `references/commands.md`의 "스크립트 옵션" 절(또는 `<script> --help` 미지원 시 그 표)을 참조한다.

## 핵심 함정 (스크립트에 이미 반영)

- `gh search repos`는 star 필드가 **`stargazersCount`**(s 있음), `gh repo view`는 **`stargazerCount`**(s 없음) — 헷갈리면 빈 값
- explore는 키워드+토픽을 **둘 다** 돌려 병합한다(키워드만 쓰면 자기태깅 토픽 레포를, 토픽만 쓰면 이름/설명 매치 레포를 놓침). 토픽은 소문자-하이픈 슬러그로 변환
- 머지 PR 검색은 `gh search prs --author=U --merged` — `--state=merged`는 잘못된 플래그(jq parse error 유발)
- **본인 vs 타인 조직 분류**: 조회 대상이 현재 로그인이면 `user/orgs`(비공개 포함), 타인이면 `users/<u>/orgs`(공개만) → 타인은 비공개 조직이 "외부"로 오분류될 수 있음(API 한계)
- 병렬 보강은 짧은 helper script를 `xargs -P 10 -n 1`로 호출한다. macOS BSD `xargs -I {}`는 명령 255바이트 제한이 있어 긴 인라인 명령에서 깨진다.
- 트렌딩은 공식 API가 없어 HTML 파싱(`trending.py`). 페이지 구조가 바뀌면 정규식 갱신 필요
- `gh search issues`는 query가 `-`로 시작하면 플래그로 오인 → discover는 `created:>=`를 항상 맨 앞에 둬 차단. `--stale-ok` created 하한은 `2008-01-01`(1926년은 GitHub이 0건 반환)

## 더 보기

- `README.md` — 관련 도구 카탈로그(발견·기여 흡수 출처)와 개선 백로그
- `references/commands.md` — 사용한 `gh` 서브커맨드, jq 레시피, 함정 전체, JSON 스키마. 옵션 권위 소스는 항상 `gh <cmd> --help`.
