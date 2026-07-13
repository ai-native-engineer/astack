---
argument-hint: "[draft|render|publish] [기간/주제]"
name: podcast
description: "Podcast episode drafting, voice rendering, and explicit publishing from a script or news recap to TTS audio, formatted show notes, GitHub Releases, RSS, Spotify, and Apple Podcasts. Use when user asks 팟캐스트 만들어, 에피소드 제작, 뉴스 팟캐스트, 대본, 쇼노트, RSS feed, Spotify/Apple publish, or podcast automation. Do NOT use for TTS-only generation, news recap text only, YouTube production, or generic audio editing."
---

# Podcast

대본부터 RSS 발행까지 잇는 orchestrator다. 기존 `ai-news-recap`과 `tts`를 호출하고, 이 스킬은 대본 변환, 쇼노트, 발행 순서를 관리한다.

## 모드 게이트

- `draft`: 재료를 구어체 대본과 쇼노트로 바꾸고 멈춘다.
- `render`: draft 결과를 `tts`의 기본 voice로 렌더링하고 발행 전 파일에서 멈춘다.
- `publish`: 사용자가 발행을 명시했을 때만 Release 변경과 git push를 실행한다. 모드가 불명확하면 `render`까지 진행한다.

## 워크플로

1. `show.json`이 있는 현재 repo 또는 사용자가 지정한 쇼 repo를 선택한다. 헤드리스 실행은 `PODCAST_REPO`를 사용한다.
2. `episodes.json`과 요청 기간을 비교한다. 새 재료가 없으면 제작하지 않는다.
3. 뉴스는 `ai-news-recap`, 필요하면 `daily-digest`로 재료를 준비한다. 일반 주제는 사용자가 준 원문을 쓴다.
4. `references/script-conversion.md`에 따라 URL과 마크다운이 없는 한 줄 한 문장 대본을 만든다.
5. `references/shownotes-convention.md`에 따라 요약, 챕터, 링크를 분리한다.
6. `tts`로 기본 voice를 사용해 음성을 만들고, loudnorm 편집본을 44.1kHz 128kbps MP3로 변환한다.
7. publish 모드에서는 `references/publishing.md`를 읽고 dry-run을 통과한 뒤 발행한다. 새 쇼는 `references/publish-setup.md`를 먼저 따른다.

## 기본값과 검증

- 청중과 목표 길이는 `show.json`의 `audience`, `target_minutes`를 우선하고, 없으면 비개발자와 8분을 쓴다.
- 원문에 없는 수치와 이름을 추가하지 않는다.
- 최종 MP3 loudness는 `mean_volume`이 아니라 EBU R128 integrated LUFS로 확인한다.
- 발행 후 Release 제목, RSS 회차 순서, XML 파싱, enclosure byte-range와 크기, 공개 피드 반영을 확인한다.
