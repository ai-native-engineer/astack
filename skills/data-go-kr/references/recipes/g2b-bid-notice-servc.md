# 조달청_나라장터 입찰공고정보서비스 (용역)

> publicDataPk: 15129394 · 상세: https://www.data.go.kr/data/15129394/openapi.do
> checked: 2026-06-16 · 상태: **실호출 검증됨** (getBidPblancListInfoServcPPSSrch, 건설사업관리 키워드 검색 138건 HTTP 200 확인)
> 활용기간: 2026-06-10 ~ 2028-06-10 · 일일 1000건/오퍼레이션

## 언제 쓰나

나라장터 용역 입찰공고 목록 조회, 건설사업관리·감리·설계 용역 공고 검색, 공고명 키워드 검색, 발주기관별 공고 조회, 특정 기간 공고 목록 추출.

## Endpoint

- host: `apis.data.go.kr/1230000/ad/BidPublicInfoService`
- 용역 목록(기간조회): `/getBidPblancListInfoServc`
- 용역 목록(검색조건): `/getBidPblancListInfoServcPPSSrch` ← **키워드 검색은 이것**
- 용역 기초금액: `/getBidPblancListInfoServcBsisAmount`

> ⚠️ `/ad/` 경로 필수. 기존에 시도한 `/1230000/BidPublicInfoService`(ad 없음)는 500 반환.

## 호출 예시 (키워드 검색)

```bash
agents-env run DATA_GO_KR_API_KEY -- curl -sG \
  "https://apis.data.go.kr/1230000/ad/BidPublicInfoService/getBidPblancListInfoServcPPSSrch" \
  --data-urlencode "serviceKey={{DATA_GO_KR_API_KEY}}" \
  --data-urlencode "pageNo=1" \
  --data-urlencode "numOfRows=10" \
  --data-urlencode "inqryDiv=1" \
  --data-urlencode "inqryBgnDt=202606010000" \
  --data-urlencode "inqryEndDt=202606302359" \
  --data-urlencode "bidNtceNm=건설사업관리" \
  --data-urlencode "type=json"
```

## 필수/주요 파라미터

| 이름 | 의미 | 비고 |
|---|---|---|
| serviceKey | 인증키 | required, Decoding 키 사용 |
| pageNo / numOfRows | 페이지 | required |
| inqryDiv | 조회구분 | **1=등록일시, 2=공고일시, 4=공고번호** |
| inqryBgnDt / inqryEndDt | 조회 시작/종료 | 형식 `YYYYMMDDHHMM` |
| bidNtceNm | 공고명 키워드 | PPSSrch 전용 |
| ntceInsttNm | 공고기관명 | PPSSrch 전용 |
| type | 응답형식 | `json` |

## 응답 핵심 필드

| 필드 | 의미 |
|---|---|
| bidNtceNm | 공고명 |
| ntceInsttNm | 발주기관명 |
| bidNtceNo | 입찰공고번호 |
| bidNtceDt | 공고일시 |
| bidClseDt | 입찰마감일시 |
| presmptPrce | 예정금액 |
| cntrctMthdNm | 계약방법명 |
| dminsttNm | 수요기관명 |

## 함정

- **`/ad/` 경로 누락 시 500** — 낙찰정보서비스(`/as/`)와 다른 경로. 혼동 주의.
- JSON `items`는 바로 배열 (`response.body.items[]`). 단건이면 dict로 옴 → `isinstance` 분기 필요.
- 공고문 **전문(본문 텍스트)**은 이 API로 못 가져옴. 상세 내용은 나라장터 웹(g2b.go.kr) 직접 접근 필요.
- 낙찰정보서비스 레시피: `g2b-scsbid-info.md`
