# 통화 녹음 소스 (에이닷)

SK텔레콤 에이닷이 통화 녹음을 iCloud Drive에 올리는 소스. 파일이 두 형태다:

- **`.txt`** — 에이닷 자동 전사본. 화자 라벨(`상대방`/`나`)과 자체 요약(`[통화요약]`)이 포함된 완성 텍스트라 추가 처리 없이 search 인덱싱만 한다.
- **`.m4a`** — 통화 원본 오디오. 워처의 `transcribe_calls.py`가 apple-stt로 자동 전사한다(아래 절 참조).

## 위치

- 디렉터리: `~/Library/Mobile Documents/com~apple~CloudDocs/녹음/`
- 파일명 규약: `<이름>_<휴대폰번호>_<YYYYMMDD>_<HHMMSS>.{txt,m4a}`
  - 예: `홍길동님_01012345678_20260407_165111.txt`
- 정규식 (search.py): `^(.+?)_(\d{10,11})_(\d{8})_(\d{6})\.txt$`

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
- 산출물: `~/.voice-memos/transcripts/YYYYMMDD/HHMMSS/transcript.md` — `extract.py`와 동일한 `## 전사 내용` 마커 포맷. 제목은 `YYYY-MM-DD HH:MM:SS <상대>님과의 통화`, 화자 라벨 없음.
- 이후 `summarize.py`(요약)·`notify.py`(알림)가 그대로 이어받는다.
- 같은 통화에 .txt가 있든 없든 .m4a를 전사한다. 따라서 search 결과에 같은 통화가 `[에이닷]`(.txt)과 `[음성 메모]`(transcripts 산출물) 양쪽 라벨로 중복 노출될 수 있다 — transcripts 쪽 제목의 `~님과의 통화`로 구분.

## 통합 원칙

- **iCloud 원본을 변형하지 않는다.** .txt·.m4a 모두 수정하면 다른 기기에 전파된다. 전사 산출물은 `~/.voice-memos/` 아래에만 생긴다.
- .txt에는 `correct.py`(단어장 교정)를 적용하지 않고 search.py 인덱싱만 한다.
- `search.py` 라벨: `[에이닷]`. 미리보기는 `[통화요약]` 섹션 전체를 들여쓰기로 표시. 섹션이 없으면 `[녹음 내용]` 첫 80자.

## 검색 동작

- `iter_transcript_files()`가 디렉터리를 glob해서 정규식에 맞는 .txt만 포함.
- `call_to_datetime()`이 파일명에서 `YYYYMMDD_HHMMSS` 파싱.
- `format_result()`에서 연락처(`홍길동님`)를 표시 이름으로 사용.

## 전문 읽기

통화 녹음은 한 줄이 짧고 줄 수가 많아 Read 도구로 직접 열어도 토큰 제한에 잘 걸리지 않는다. Voice Memos 전사본과 달리 `fold` 절차는 보통 불필요.

대용량 통화(예: 1시간 이상)일 때만 같은 fold 패턴을 적용한다.

## 화자 라벨 해석

`상대방`/`나`는 에이닷이 자동으로 단 라벨이라 100% 정확하지 않다. 특히 짧은 발화·동시 발화에서 라벨이 뒤바뀔 수 있다. 의사결정·심리 분석을 할 때는 문맥으로 한 번 더 검증한다. `.m4a` 전사본(apple-stt)에는 화자 라벨이 아예 없다 — Voice Memos와 동일한 화자 분리 한계 규칙(`voice-memos.md` §3)을 적용한다.
