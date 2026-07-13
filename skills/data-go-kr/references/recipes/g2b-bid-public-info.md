# 조달청_나라장터 입찰공고정보서비스

> publicDataPk: 15129394 · 상세: https://www.data.go.kr/data/15129394/openapi.do
> checked: 2026-06-28 · 상태: **실호출 검증됨** (getBidPblancListInfoServcPPSSrch, AI 키워드 검색 HTTP 200·resultCode 00·554건 확인)
> 심층 문서: `docs/260628-g2b-bid-public-info-reference-1.2.md` (원본 .docx 동봉, v1.2)
> 활용기간: 2026-06-10 ~ 2028-06-10 · 일일 1000건/오퍼레이션

## 언제 쓰나

나라장터 입찰공고 목록 조회, 공고명 키워드 검색, 발주기관·수요기관별 공고 조회, 공사·용역·물품·외자 공고 검색, 기초금액·면허제한·참가가능지역·구매대상물품·첨부파일 조회.

## Endpoint

- host: `apis.data.go.kr/1230000/ad/BidPublicInfoService`
- 목록 조회: `/getBidPblancListInfo{Cnstwk|Servc|Frgcpt|Thng}` — 공사·용역·외자·물품
- 나라장터 검색조건 조회: `/getBidPblancListInfo{Cnstwk|Servc|Frgcpt|Thng}PPSSrch` — 공고명/기관명/참조번호 등 키워드 검색
- 기초금액: `/getBidPblancListInfo{Thng|Cnstwk|Servc}BsisAmount`
- 변경이력: `/getBidPblancListInfoChgHstry{Thng|Cnstwk|Servc}`
- 부가정보: `/getBidPblancListInfoLicenseLimit`, `/getBidPblancListInfoPrtcptPsblRgn`, `/getBidPblancListInfo{Thng|Servc|Frgcpt}PurchsObjPrdct`, `/getBidPblancListInfoEorderAtchFileInfo`
- 기타/특수: `/getBidPblancListInfoEtc`, `/getBidPblancListInfoEtcPPSSrch`, `/getBidPblancListPPIFnlRfpIssAtchFileInfo`, `/getBidPblancListBidPrceCalclAInfo`, `/getBidPblancListEvaluationIndstrytyMfrcInfo`

## 키

- env: `DATA_GO_KR_API_KEY`
- query parameter: `serviceKey`
- 주입 예: `agents-env run DATA_GO_KR_API_KEY -- <명령>`

## 호출 예시

```bash
agents-env run DATA_GO_KR_API_KEY -- curl -sG \
  "https://apis.data.go.kr/1230000/ad/BidPublicInfoService/getBidPblancListInfoServcPPSSrch" \
  --data-urlencode "serviceKey={{DATA_GO_KR_API_KEY}}" \
  --data-urlencode "pageNo=1" \
  --data-urlencode "numOfRows=10" \
  --data-urlencode "inqryDiv=1" \
  --data-urlencode "inqryBgnDt=202606010000" \
  --data-urlencode "inqryEndDt=202606282359" \
  --data-urlencode "bidNtceNm=AI" \
  --data-urlencode "type=json"
```

## 필수/주요 파라미터

| 이름 | 의미 | 형식·예 |
|---|---|---|
| serviceKey | 인증키 | required, Decoding 키를 `--data-urlencode`로 전달 |
| pageNo / numOfRows | 페이지 | required, `1` / `10` |
| type | 응답형식 | `json` 지정 시 JSON |
| inqryDiv | 조회구분 | 일반 목록: `1=등록일시, 2=입찰공고번호, 3=변경일시`; PPSSrch: `1=공고게시일시, 2=개찰일시` |
| inqryBgnDt / inqryEndDt | 조회 시작/종료 | `YYYYMMDDHHMM`; 날짜 조회 시 필수 |
| bidNtceNo | 입찰공고번호 | 일반 목록에서 `inqryDiv=2`일 때 필수 |
| bidNtceOrd | 입찰공고차수 | 면허제한·참가가능지역·구매대상물품·첨부파일 등 상세성 조회에 자주 필요 |
| bidNtceNm | 입찰공고명 | PPSSrch 계열, 일부 입력 조회 가능 |
| ntceInsttNm / dminsttNm | 공고기관명 / 수요기관명 | PPSSrch 계열, 일부 입력 조회 가능 |
| refNo | 참조번호 | PPSSrch 계열 |

## 응답 핵심 필드

| 필드 | 의미 |
|---|---|
| bidNtceNo / bidNtceOrd | 입찰공고번호 / 차수 |
| bidNtceNm | 입찰공고명 |
| bidNtceDt / bidClseDt / opengDt | 공고일시 / 입찰마감일시 / 개찰일시 |
| ntceInsttNm / dminsttNm | 공고기관명 / 수요기관명 |
| cntrctCnclsMthdNm / bidMethdNm | 계약체결방법명 / 입찰방식명 |
| asignBdgtAmt / presmptPrce / rsrvtnPrceRngBgnRate | 배정예산금액 / 추정가격·예정가격 계열 / 예비가격범위시작율 |
| techAbltEvlRt / bidPrceEvlRt | 기술능력평가비율 / 입찰가격평가비율 |
| sucsfbidMthdAppStd | 낙찰방법적용기준(v1.2 추가) |
| bidNtceDtlUrl / bidNtceUrl | 공고 상세 URL 계열 |

## 페이징

- `pageNo`와 `numOfRows`는 필수다.
- `response.body.totalCount`로 전체 건수를 확인하고 `items`를 페이지별로 합친다.
- `items`는 0건이면 빈 값, 단건이면 객체, 복수건이면 배열로 올 수 있으므로 항상 배열로 정규화한다.

## 함정

- `/ad/` 경로 필수. `/1230000/BidPublicInfoService`처럼 `ad`를 빼면 실패한다.
- 공식 문서 샘플 URL에는 `//ad`, 경로 중간 공백, 파라미터 붙음 같은 오타가 섞여 있다. 위 endpoint 형태로 정규화해서 호출한다.
- `inqryDiv` 의미가 일반 목록과 `PPSSrch`에서 다르다. 키워드 검색은 보통 `PPSSrch + inqryDiv=1 + 공고게시일시 범위`가 맞다.
- JSON `items`는 배열로 온다. 0건은 빈 값, 일부 API/상황은 단건 객체 가능성이 있어 파서에서 배열/객체를 모두 처리한다.
- 공고문 전문 본문은 이 API 응답에 없다. 상세 문서는 응답 URL 또는 나라장터 웹 접근이 필요하다.
