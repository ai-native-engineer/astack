# podcast (maintainer notes)

팟캐스트 **제작과 발행** 오케스트레이터. 제작 단계는 기존 스킬을 호출하고, 발행은 이 스킬이 직접 한다.

## 체인
`daily-digest`/`ai-news-recap`(대본 재료) -> **이 스킬의 대본 변환**(`references/script-conversion.md`) -> `tts`(AI 음성) -> **이 스킬의 발행**(`scripts/publish.sh`, GitHub Releases+Pages로 공개 RSS, Spotify/Apple 자동 수집).

## 역할(거버넌스: orchestrator + 발행 transport 흡수)
- 이 스킬이 코드화한 것: 정리본을 구어체 대본으로 바꾸는 규칙, 쇼노트 컨벤션, 발행 스크립트.
- 제작 단계(뉴스 정리, 음성)는 `ai-news-recap`, `tts`를 호출만 한다.
- 발행은 옛 `podcast-publish`를 별도 스킬로 두지 않고 흡수했다(직접 사용 실적이 없고 podcast가 유일 호출자라 분리가 인지 부담만 줬다. 2026-06 병합).

## 구조
- `SKILL.md` — 파이프라인, 결정, 검증.
- `references/script-conversion.md` — 듣기용 대본 변환 규칙.
- `references/shownotes-convention.md` — 에피소드 설명(쇼노트) 컨벤션.
- `references/publishing.md` — dry-run, 발행, 실패 복구, 공개 검증.
- `references/publish-setup.md` — 새 쇼 최초 1회 셋업(repo, Pages, Spotify).
- `scripts/publish.sh`, `scripts/gen_feed.py` — 발행과 RSS 피드 생성.
- `scripts/chapter_ts.py` — tts chunk 산출물에서 챕터 타임스탬프(hh:mm:ss) 계산.
- `tests/test_podcast.py` — RSS 정렬/쇼노트와 publish dry-run 회귀 테스트.
- `templates/show.json` — 쇼 설정 템플릿.
