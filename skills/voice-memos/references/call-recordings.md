# 통화 녹음 소스 (에이닷)

SK텔레콤 에이닷이 통화 녹음을 iCloud Drive에 올리는 소스. 파일이 두 형태다:

- **`.txt`** — 에이닷 자동 전사본. 화자 라벨(`상대방`/`나`)과 자체 요약(`[통화요약]`)이 포함된 완성 텍스트라 추가 처리 없이 search 인덱싱만 한다.
- **`.m4a`** — 통화 원본 오디오. 워처의 `transcribe_calls.py`가 apple-stt로 자동 전사한다(아래 절 참조). 설치 기본값은 `legacy`다.

## 위치

- 디렉터리: `~/Library/Mobile Documents/com~apple~CloudDocs/녹음/`
- 파일명 예시: `<이름>_<전화번호>_<YYYYMMDD>_<HHMMSS>.txt`, `<전화번호>_<YYYYMMDD>_<HHMMSS>.txt`
  - 예: `홍길동님_01012345678_20260407_165111.txt`, `01012345678_20260407_165111.txt`
- `search.py`는 이 디렉터리의 `.txt` 전체와 `.transcript.md`를 에이닷으로 포함하고, 날짜 정렬/필터링은 파일명 끝의 `_YYYYMMDD_HHMMSS` suffix로 처리한다.
- `.m4a` 자동 전사(`transcribe_calls.py`)는 파일명 끝의 `_YYYYMMDD_HHMMSS.m4a` suffix가 있는 통화 녹음을 대상으로 한다.

## .txt 파일 구조

```
에이닷

홍길동님(010-1234-5678) 님과의 통화
2026. 4. 7.(화) 오후 4:51
17분 8초


[통화요약]
* (주제 요약)
  - (소주제)
    • (세부 내용)

[녹음 내용]
상대방 00:01
여보세요

나 00:01
에
...
```

- `[통화요약]` 헤더 직후가 에이닷의 자동 요약. 검색 미리보기에 이걸 그대로 노출한다.
- `[녹음 내용]` 이후가 화자 라벨 + 타임스탬프 포함 본문.

## .m4a 자동 전사 (transcribe_calls.py)

워처 `run.sh`의 2단계. `scripts/transcribe_calls.py`가 통화 .m4a를 apple-stt로 전사한다. Voice Memos와 달리 통화 m4a에는 tsrp atom이 없어 `extract.py`가 못 다루므로 별도 경로다.

- iCloud placeholder(dataless) 파일이면 `brctl download`로 받아 크기 안정화까지 대기 후 전사.
- `legacy` 산출물: 원본 옆 `<원본>.transcript.md` + `<원본>.summary.md`. 전사 파일은 `extract.py`와 동일한 `## 전사 내용` 마커 포맷이다. 제목은 `YYYY-MM-DD HH:MM:SS <상대>님과의 통화`이며 화자 라벨은 없다.
- strict 산출물: 원본 옆 `<원본>.analysis.json`과 `<원본>.run.json`. `shadow`는 transcript를 쓰지 않고, `review`만 `<원본>.transcript.md`를 만든다. strict analysis가 미지원이거나 검증에 실패하면 legacy로 fallback하지 않는다.
- Voice Memos와 같은 SHA-256 recording ID, strict sidecar, context pack, privacy, per-recording lock 계약을 사용한다. sidecar는 `~/.config/voice-memos/recordings/<audio-sha256>.json`에 둔다.
- 이후 `summarize.py`(요약)·`notify.py`(알림)가 그대로 이어받지만 `review_pending`이면 provisional 요약/알림을 만들지 않고, `privacy: local`이면 Claude를 호출하지 않는다.
- strict `shadow`·`review`는 Gate 1 미통과 상태라 설치 launchd에서 활성화하지 않는다.
- 같은 통화에 .txt가 있든 없든 .m4a를 전사한다. 따라서 search 결과에 같은 통화가 `[에이닷]` 원본 .txt와 `[에이닷]` 파생 `.transcript.md`로 중복 노출될 수 있다.

## 통합 원칙

- **iCloud 원본을 변형하지 않는다.** .txt·.m4a 원본은 수정하지 않고, 파생 `.analysis.json`/`.run.json`/`.transcript.md`/`.summary.md`만 같은 `녹음/` 폴더에 둔다.
- `.txt`는 search.py 인덱싱만 한다. 폐기된 `correct.py` 전역 치환은 `.txt`와 파생 transcript 어디에도 적용하지 않는다.
- `search.py` 라벨: `[에이닷]`. 미리보기는 `[통화요약]` 섹션 전체를 들여쓰기로 표시. 섹션이 없으면 `[녹음 내용]` 첫 80자.

## 검색 동작

- `iter_transcript_files()`가 디렉터리를 glob해서 모든 `.txt`와 `.transcript.md`를 포함.
- `call_to_datetime()`이 파일명 끝의 `_YYYYMMDD_HHMMSS` suffix에서 날짜를 파싱.
- `format_result()`에서 suffix를 제거한 prefix를 표시 이름으로 사용하되, prefix 끝의 전화번호 꼬리는 제거.

## 전문 읽기

통화 녹음은 한 줄이 짧고 줄 수가 많아 Read 도구로 직접 열어도 토큰 제한에 잘 걸리지 않는다. Voice Memos 전사본과 달리 `fold` 절차는 보통 불필요.

대용량 통화(예: 1시간 이상)일 때만 같은 fold 패턴을 적용한다.

## 화자 라벨 해석

`상대방`/`나`는 에이닷이 자동으로 단 라벨이라 100% 정확하지 않다. 특히 짧은 발화·동시 발화에서 라벨이 뒤바뀔 수 있다. 의사결정·심리 분석을 할 때는 문맥으로 한 번 더 검증한다. `.m4a` 전사본(apple-stt)에는 화자 라벨이 아예 없다 — Voice Memos와 동일한 화자 분리 한계 규칙(`voice-memos.md` 3절)을 적용한다.
