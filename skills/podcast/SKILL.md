---
argument-hint: "[기간/주제 또는 publish]"
name: podcast
description: "Podcast episode production and publishing orchestrator from script/news recap to spoken script, TTS audio, GitHub Releases/RSS feed, and Spotify/Apple distribution. Use when user asks 팟캐스트 만들어, 에피소드 제작, 뉴스 팟캐스트, 대본부터 발행, RSS feed, Spotify/Apple podcast publish, or podcast automation. Do NOT use for TTS-only voice generation, AI news recap text only, YouTube production, or generic audio editing."
---

# Podcast — 제작·발행 오케스트레이터

단계를 잇는 라우터다. 각 단계는 **기존 스킬/스크립트를 호출**하고 로직을 복제하지 않는다. 빠진 고리("정리본->구어체 대본")만 이 스킬의 reference로 코드화돼 있다.

## 파이프라인
1. **입력 결정** — 기간(또는 대본 소스)·청중·길이·보이스(기본 `aiden`)·대상 쇼 repo(예: `~/Dev/<your-show>`).
2. **재료 preflight** — 대상 쇼의 `episodes.json` 최신 회차·기간을 먼저 보고, 요청 기간에 새 digest/재료가 없으면 제작하지 말고 "새 재료 없음"으로 종료.
3. **대본 재료** — `ai-news-recap`(digest -> 청중별 정리). digest가 없으면 `daily-digest` 먼저. 뉴스가 아니면 사용자가 준 원문/주제를 재료로.
4. **대본 변환** — `references/script-conversion.md` 규칙대로 구어체 대본 `.txt` 생성(한 줄=한 문장, 마크다운·URL 제거, 한글 음차, 브릿지·인트로/아웃트로). 링크는 쇼노트로 분리.
5. **음성** — `tts` 스킬: `scripts/tts_clone.py chunk --voice <voice> --text-file script.txt --loudnorm-out edit.wav`. 문장 수가 많으면 먼저 줄인다. 발행용 mp3는 원본 청크가 아니라 `--loudnorm-out`이 만든 -16 LUFS 편집본에서 변환한다(44.1k·128k·ID3). 청크 원본은 음량이 작아 그대로 mp3로 만들면 팟캐스트 표준보다 낮게 발행된다.
6. **발행** — `scripts/publish.sh --repo <쇼repo> --audio <mp3> --title "제목" --desc "쇼노트"`: 오디오를 GitHub Releases에 올리고 `episodes.json`·`feed.xml`을 갱신·push하면 Spotify/Apple이 RSS를 자동 수집한다. 제목은 묶음형 `쇼명: 핵심 2~3건 쉼표 나열 (M/D~M/D)`(그 주 빅뉴스 1건이 압도적이면 `핵심 한 줄 | 쇼명 (M/D~M/D)`), 쇼노트는 `references/shownotes-convention.md`를 따른다. 이미 mp3가 있으면 1~5단계 없이 이 단계만으로 발행할 수 있다. **새 쇼면** `references/publish-setup.md`로 1회 셋업(repo·Pages·Spotify 등록) 먼저.

## 결정·기본값
- 청중 미지정이면 물어본다(대중 팟캐스트는 비개발자가 흔한 기본).
- 보이스 기본 `aiden`, 길이 기본 10분 이상. 분량은 꼭지 깊이로 늘리고 천천히 읽어 늘리지 않는다.
- 대상 쇼 repo는 사용자가 지정한다(예: `~/Dev/<your-show>`). 헤드리스/scheduled 실행은 질문하지 않고 지정된 값으로 진행한다.
- 사실 보존: 원문(정리본/digest) 수치·이름만, 추측 금지.

## 검증
- 대본에 URL·마크다운 없는지, 한 줄=한 문장인지 확인 후 음성 생성.
- 음성 생성 전 문장 수와 예상 시간을 확인하고, 긴 대본은 TTS 실행 전에 줄인다.
- 발행 후 피드 HTTP 200, 오디오 `accept-ranges`, `ffprobe` duration, 최종 mp3 `mean_volume`이 -16 LUFS 근처(대략 -17dB 이상)인지 확인.

단계별 세부 동작은 각 스킬의 SKILL.md를 따른다. 이 스킬은 순서·결정·대본 변환만 담는다.
