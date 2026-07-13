# 국민연금공단_국민연금 가입 사업장 내역 상세설명

> publicDataPk: 3046071 · 상세: https://www.data.go.kr/data/3046071/openapi.do
> checked: 2026-06-28 · 상태: 실호출 검증됨
> 심층 문서: docs/260628-nps-workplace-guide-v2.0.md · 원본: docs/260628-nps-workplace-guide-v2.0.docx

## 언제 쓰나

국민연금 가입 사업장, 사업장 가입자수, 국민연금 고지금액, 월별 취득자·상실자, 회사 고용 현황을 조회할 때 쓴다. 기업명으로 사업장 기본 목록을 찾고, 각 월별 `seq`로 상세·기간별 현황을 이어서 조회한다.

## Endpoint

- host: `apis.data.go.kr/B552015/NpsBplcInfoInqireServiceV2`

| 오퍼레이션 | 용도 |
|---|---|
| `/getBassInfoSearchV2` | 사업장명으로 기본정보와 월별 `seq` 조회 |
| `/getDetailInfoSearchV2` | `seq` 기준 가입자수·고지금액·등록일·업종 조회 |
| `/getPdAcctoSttusInfoSearchV2` | `seq` 기준 월별 취득자수·상실자수 조회 |

## 키

- env: `DATA_GO_KR_API_KEY`
- query parameter: `serviceKey`
- 주입 예: `agents-env run DATA_GO_KR_API_KEY -- <명령>`

## 호출 예시

```bash
agents-env run DATA_GO_KR_API_KEY -- curl -sG "https://apis.data.go.kr/B552015/NpsBplcInfoInqireServiceV2/getBassInfoSearchV2" \
  --data-urlencode "serviceKey={{DATA_GO_KR_API_KEY}}" \
  --data-urlencode "wkplNm=채널코퍼레이션" \
  --data-urlencode "pageNo=1" \
  --data-urlencode "numOfRows=100" \
  --data-urlencode "dataType=json"
```

```bash
agents-env run DATA_GO_KR_API_KEY -- curl -sG "https://apis.data.go.kr/B552015/NpsBplcInfoInqireServiceV2/getDetailInfoSearchV2" \
  --data-urlencode "serviceKey={{DATA_GO_KR_API_KEY}}" \
  --data-urlencode "seq=6733098" \
  --data-urlencode "pageNo=1" \
  --data-urlencode "numOfRows=100" \
  --data-urlencode "dataType=json"
```

```bash
agents-env run DATA_GO_KR_API_KEY -- curl -sG "https://apis.data.go.kr/B552015/NpsBplcInfoInqireServiceV2/getPdAcctoSttusInfoSearchV2" \
  --data-urlencode "serviceKey={{DATA_GO_KR_API_KEY}}" \
  --data-urlencode "seq=6733098" \
  --data-urlencode "pageNo=1" \
  --data-urlencode "numOfRows=100" \
  --data-urlencode "dataType=json"
```

## 필수/주요 파라미터

| 이름 | 의미 | 형식·예 |
|---|---|---|
| `serviceKey` | 공공데이터포털 일반 인증키 | Decoding 키를 환경변수에 두고 `--data-urlencode` 사용 |
| `dataType` | 응답 형식 | `json` |
| `pageNo` | 페이지 번호 | `1`부터 |
| `numOfRows` | 페이지 크기 | 예: `100` |
| `wkplNm` | 사업장명 | 기본정보 조회 필수 |
| `bzowrRgstNo` | 사업자등록번호 앞 6자리 | 선택 |
| `ldongAddrMgplDgCd` | 시도 법정동 코드 | 선택 |
| `ldongAddrMgplSgguCd` | 시군구 법정동 코드 | 선택 |
| `ldongAddrMgplSgguEmdCd` | 읍면동 법정동 코드 | 선택 |
| `seq` | 사업장 월별 식별번호 | 상세·기간별 조회 필수 |
| `dataCrtYm` | 자료생성년월 | `yyyymm`, 기간별 현황 선택 |

## 응답 핵심 필드

| 필드 | 의미 |
|---|---|
| `response.header.resultCode` | `00`이면 정상 |
| `response.body.totalCount` | 전체 결과 수 |
| `body.items.item[].seq` | 상세·기간별 조회에 쓰는 식별번호 |
| `body.items.item[].dataCrtYm` | 자료생성년월 |
| `body.items.item[].wkplNm` | 사업장명 |
| `body.items.item[].wkplJnngStcd` | 가입상태, `1`: 등록, `2`: 탈퇴 |
| `body.items.item[].wkplStylDvcd` | 사업장 형태, `1`: 법인, `2`: 개인 |
| `body.items.item[].wkplRoadNmDtlAddr` | 사업장 도로명 상세주소 |
| `body.items.item[].adptDt` | 사업장 등록일 |
| `body.items.item[].scsnDt` | 사업장 탈퇴일 |
| `body.items.item[].jnngpCnt` | 가입자수 |
| `body.items.item[].crrmmNtcAmt` | 당월 고지금액 |
| `body.items.item[].nwAcqzrCnt` | 월별 취득자수 |
| `body.items.item[].lssJnngpCnt` | 월별 상실자수 |

## 페이징

- `pageNo`와 `numOfRows`를 사용한다.
- `response.body.totalCount`로 전체 건수를 확인하고 `body.items.item[]`을 페이지별로 합친다.
- 회사 1곳도 월별 `seq`가 여러 건 나올 수 있으므로 기본정보 조회 결과의 각 `seq`에 대해 상세·기간별 조회를 반복한다.

## 함정

- `type=json`이 아니라 `dataType=json`이다.
- `/getBassInfoSearchV2`는 회사 1곳도 월별 `seq`가 여러 건 나온다. 고용 추이는 기본 목록의 각 `seq`로 상세·기간별 조회를 반복해서 만든다.
- 공식 가이드 v2.0 기준 2025-05-07부터 요청/응답 표기가 스네이크 케이스에서 카멜 케이스로 바뀌었고, 응답 구조는 `items.item[]`다.
- 공식 가이드는 과부하 이슈로 제공 시점 기준 1년치 데이터만 제공된다고 안내한다.
- 데이터는 매월 15일 이후 제공 기준이며, 오픈API 데이터는 통계자료로 활용할 수 없다고 안내되어 있다.
- 공식 가이드의 오퍼레이션 목록에는 `getPdAcctoSttuInfoSearchV2`로 보이는 오탈자가 있으나, 상세 명세·샘플·data.go.kr Swagger·실호출 기준 정식 경로는 `getPdAcctoSttusInfoSearchV2`다.
- 사업자등록번호는 앞 6자리만 마스킹된 형태로 반환된다. 불필요하면 저장·표시하지 않는다.
- 문서상 3인 이상 법인사업장 정보가 중심이며, `wkpl_styl_dvcd` 요청 파라미터는 삭제된 것으로 안내되어 있다.
