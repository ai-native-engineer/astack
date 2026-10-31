# Apple SpeechTranscriber capability check

2026-07-22에 macOS 26.5.2, Swift 6.3.3, `ko-KR` 로컬 Voice Memo 한 건으로
임시 빌드를 실행했다. 원본 파일명과 전사문은 기록하지 않았다.

## Source provenance

- 배포 정본: `native/apple-stt.swift`
- 설치 바이너리 SHA-256: `acc95555dc63bb9b43893158ca659076aa73b78acc5088ba19c9369d3024a8ec`
- 기존 평문, timestamp, SRT, legacy JSON 옵션을 유지한다.
- 의도된 차이: context stable dedupe/cap 100, `--vocab-file` replacement,
  `timeIndexedTranscriptionWithAlternatives`, `--analysis-json` 추가.

같은 로컬 입력에서 설치본과 임시 빌드 모두 네 legacy 출력의 구조 검사를
통과했다. preset 변경으로 JSON segment 수는 45에서 204로 세분화됐다. 따라서
`start/end/text` 배열 계약은 호환되지만 segment 경계의 byte-for-byte 호환은
보장하지 않는 의도된 품질 증거 변경이다.

## Real-file result

| Check | Result |
|---|---:|
| duration | 570,217 ms |
| segments | 204 |
| confidence spans | 880 |
| alternatives | 143 |
| segment confidence missing | 0 |
| selected / dropped context | 100 / 511 |

Apple이 이 입력에서 alternatives, `transcriptionConfidence`, result/audio time
range를 모두 반환했다. confidence run의 범위를 원문 UTF-8 byte offset으로 바꾼 뒤
모든 양 끝이 문자 경계이고 원문 길이 안에 있는지 검증했다. 대안의 audio range는
해당 Apple attributed run에서 읽고, 없을 때만 상위 result range를 사용한다.

`tests/fixtures/apple-capability-ko-KR.json`은 첫 result의 시간과 confidence 형태를
유지하되 텍스트, 해시, context를 대체한 비민감 fixture다. 실제 속성은 녹음과 OS에
따라 없을 수 있으므로 schema의 confidence/alternative 값은 항상 optional로 처리한다.

## Gate 1 status

Capability와 legacy 출력 shape는 통과했다. 같은 570,217 ms 입력을 빈 context와
기본 vocab 상위 100개로 각각 실행한 관측 결과는 다음과 같다.

| Measure | No context | Context 100 |
|---|---:|---:|
| segments | 204 | 204 |
| elapsed | 3.04 s | 2.96 s |
| max RSS | 28,327,936 bytes | 28,459,008 bytes |
| selected terms present | 0 | 0 |

두 hypothesis는 동일했다. 그러나 정답 transcript, named-term occurrence, required
phrase annotation이 없어 CER, named-term recall, omission을 계산할 수 없다. 따라서
context value gate는 `insufficient_data`이고 Gate 1 전체는 아직 통과하지 않았다.

2026-10-20에 3분 다화자 녹음 한 건으로 다시 확인했다. 녹음에서 틀리게 나온
제품명 4개(`NotebookLM`, `Claude Code` 등)만 넣은 context와 빈 context의 평문
출력이 바이트 단위로 같았다. 목표 용어도 바로잡히지 않았다. 따라서 Whisper의 초기
프롬프트처럼 녹음별 용어로 인식을 바꾸는 효과는 이 경로에서 기대하지 않는다.

같은 녹음으로 `DictationTranscriber`(`timeIndexedLongDictation`)도 확인했다.

- 용어 context, 맞춤 언어 모델(`SFCustomLanguageModelData`, `.customizedLanguage`)
  모두 출력이 바이트 단위로 같았다. 원본, 16kHz 변환본, 음량 보정본에서 같았다.
- 대화 녹음의 대부분을 버렸다. `SpeechTranscriber`가 528자를 낼 때 37자, 음량 보정
  뒤에도 101자였다. preset, `frequentFinalization`, `.farField`를 바꿔도 같았다.
- 그래서 받아쓰기 엔진을 바꿔 용어 힌트를 얻는 길도 없다. `SFSpeechRecognizer`
  경로는 음성 인식 권한 창이 필요해 확인하지 않았다.

결론: capped common vocab과 evidence contract까지만 검증됐다. 녹음별 context memory,
Claude suggestion, review-mode watcher 설치는 활성화하지 않는다. 6 calibration + 6
evaluation 녹음과 계획의 최소 annotation denominator가 준비된 뒤 같은 benchmark
gate로 다시 판단한다. 기존 설치 바이너리와 watcher 기본 `legacy` mode는 유지한다.
