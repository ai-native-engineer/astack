# Apple Notes 소스

macOS Notes.app의 메모를 search 인덱싱에 통합. NoteStore.sqlite를 `mode=ro`로 직접 쿼리하고, 본문은 zlib + protobuf naive 파싱으로 디코딩한다. 외부 의존성 0.

## 위치

- 데이터베이스: `~/Library/Group Containers/group.com.apple.notes/NoteStore.sqlite`
- WAL/SHM: 같은 경로의 `NoteStore.sqlite-wal`, `NoteStore.sqlite-shm`

## 핵심 규칙

- **임시 복사본을 만들지 않는다.** WAL 모드 SQLite는 reader가 writer를 막지 않아서 `mode=ro` URI로 원본을 직접 열어도 안전하다. 사본을 만들면 디스크 낭비 + 동기화 지연만 생긴다.
- 원본을 절대 쓰지 않는다. `sqlite3.connect(f"file:{path}?mode=ro", uri=True)` 사용.
- Notes.app 본문은 SQLite + zlib + protobuf로 저장되며 평문이 아니다. 단순 grep으로는 안 잡힌다.
- **조회 전 Notes.app 실행 보장.** macOS Notes는 앱이 실행 중일 때만 iCloud 동기화를 한다. 앱이 꺼져 있던 동안 iPhone 등 다른 기기에서 쓴 메모는 로컬 NoteStore.sqlite에 아예 없어서 직쿼리로 절대 잡히지 않는다 (2026-06-11 실측: 9일치 메모 누락). `vm_notes._ensure_notes_synced()`가 `refresh_notes_meta()` 진입 시 자동 처리한다 — 앱이 안 떠 있으면 `open -gja Notes`로 숨김 실행 후 DB/WAL mtime 변화를 폴링(첫 변화 최대 15초 대기, 변화 후 2초 안정화)하고 진행. 띄운 앱은 종료하지 않으므로 대기 비용은 세션당 1회. WAL 가독성 자체는 문제없음(shm rw 접근 가능 확인).

## 디코딩 경로

```
ZICCLOUDSYNCINGOBJECT  (메타: ZTITLE1, ZMODIFICATIONDATE1, ZFOLDER, ZCRYPTOINITIALIZATIONVECTOR)
  ↓ JOIN ZICNOTEDATA ON ZICNOTEDATA.ZNOTE = ZICCLOUDSYNCINGOBJECT.Z_PK
ZICNOTEDATA.ZDATA       (BLOB: gzip 또는 raw zlib)
  ↓ decompress
NoteStoreProto
  ↓ field 2 (length-delimited)
Document
  ↓ field 3 (length-delimited)
Note
  ↓ field 2 (length-delimited string)
note_text  ← 본문
```

본문 첫 줄은 보통 제목과 동일(Notes.app이 첫 줄을 자동 제목으로 사용). 미리보기 만들 때 두 번째 줄부터 표시.

## search.py 통합

- 가상 Path 표현: `apple-note:<Z_PK>`. 다른 소스(Voice Memos transcript, 통화 녹음 .txt)와 동일한 `list[Path]` 인터페이스를 유지하기 위한 어댑터.
- 라벨: `[메모]`. 잠금 여부와 무관하게 동일 라벨을 쓰고, 잠긴 메모는 미리보기 영역에 `(잠긴 메모 — 본문 검색 제외)` 안내로 구분한다.
- 구현: `scripts/vm_notes.py` 모듈이 메타 캐시·디코딩을 전담하고, search.py는 공개 함수만 쓴다 — `refresh_notes_meta()`(캐시 갱신), `all_note_paths()`, `is_note()`, `note_meta()`, `note_body()`(본문, lazy 디코딩), `note_haystack()`(제목+본문, 키워드 검색용).

## 잠긴 메모

`ZICCLOUDSYNCINGOBJECT.ZCRYPTOINITIALIZATIONVECTOR != NULL`이면 AES 암호화된 메모. 비밀번호 없이는 복호화 불가.

- 라벨은 일반 메모와 동일하게 `[메모]`로 표시
- 미리보기 영역에 `(잠긴 메모 — 본문 검색 제외)` 안내가 나타나서 구분된다
- 본문 검색 대상에서 제외 (제목만 검색)

## 폴더 정보

폴더 row와 메모 row는 같은 `ZICCLOUDSYNCINGOBJECT` 테이블을 공유한다.

- 메모 row: `ZTITLE1` 사용 (메모 제목)
- 폴더 row: `ZTITLE2` 사용 (폴더 이름)
- 메모의 `ZFOLDER`가 폴더 row의 `Z_PK`를 가리킴

`search.py`는 시작 시 폴더 맵을 만들어 메타에 폴더 이름을 채워 넣는다.

## 전체 export (선택)

여러 메모를 마크다운 파일로 일괄 뽑고 싶을 때 사용하는 일회성 스크립트 예시.

```bash
python3 /tmp/notes-export/export_all.py \
  "$HOME/Library/Group Containers/group.com.apple.notes/NoteStore.sqlite" \
  /tmp/notes-export/notes
```

- 출력: `<폴더명>/<YYMMDD>-<제목>.md` (`folder`, `modified` 프론트매터 + 본문)
- 잠긴 메모는 placeholder만 생성

스킬 자체에 필요한 기능이 아니라 임시 도구. search 인덱싱에는 영향 없다.

## 한계

- **서식 손실**: 단순 protobuf field 추출이라 굵게·기울임·체크박스·표·NSAttributedString 속성은 빠진다. 본문 텍스트만 잡힌다.
- **첨부 손실**: 이미지·PDF 등은 별도 테이블·디렉터리에 있어 export 대상에서 빠진다.
- **계정 분리 손실**: 여러 iCloud 계정에 동명 폴더(`Notes`)가 있으면 export 시 한 디렉터리에 합쳐진다.

이 한계는 search 인덱싱 용도에서는 문제 없다(키워드·날짜·제목 검색에 필요한 정보는 모두 잡힘).
