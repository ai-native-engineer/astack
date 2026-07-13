# 조달청_나라장터 계약정보서비스

> publicDataPk: 15129427 · 상세: https://www.data.go.kr/data/15129427/openapi.do
> checked: 2026-06-28 · 상태: **실호출 검증됨** (`getCntrctInfoListServc`의 `YYYYMMDDHHMM`, `getCntrctInfoListServcPPSSrch`의 `YYYYMMDD` 모두 HTTP 200, `resultCode=00` 확인)
> 참고문서: `docs/260628-g2b-contract-info-reference-1.0.docx`

## 언제 쓰나

나라장터 계약현황, 계약체결 이력, 계약상세, 변경이력, 삭제이력, 물품·공사·용역·외자 계약 조회. 특정 기관·공고번호·요청번호·확정계약번호·통합계약번호 기준으로 조달 계약 정보를 확인할 때 쓴다.

## Endpoint

- host: `apis.data.go.kr/1230000/ao/CntrctInfoService`
- 기본/변경/삭제 조회는 등록·변경·삭제일시 또는 `untyCntrctNo` 기준
- `*PPSSrch`는 나라장터 검색조건 기준: 계약체결일자, 확정계약번호, 요청번호, 공고번호, 기관명, 품명/계약명, 계약방법 등

| 구분 | 오퍼레이션 | 용도 |
|---|---|---|
| 물품 | `/getCntrctInfoListThng` | 계약현황 |
| 물품 | `/getCntrctInfoListThngDetail` | 물품세부 |
| 물품 | `/getCntrctInfoListThngPPSSrch` | 나라장터 검색조건 |
| 물품 | `/getCntrctInfoListThngChgHstry` | 변경이력 |
| 물품 | `/getCntrctInfoListThngDltHstry` | 삭제이력 |
| 공사 | `/getCntrctInfoListCnstwk` | 계약현황 |
| 공사 | `/getCntrctInfoListCnstwkServcInfo` | 공사서비스정보 |
| 공사 | `/getCntrctInfoListCnstwkPPSSrch` | 나라장터 검색조건 |
| 공사 | `/getCntrctInfoListCnstwkChgHstry` | 변경이력 |
| 공사 | `/getCntrctInfoListCnstwkDltHstry` | 삭제이력 |
| 용역 | `/getCntrctInfoListServc` | 계약현황 |
| 용역 | `/getCntrctInfoListGnrlServcServcInfo` | 일반용역서비스정보 |
| 용역 | `/getCntrctInfoListTechServcServcInfo` | 기술용역서비스정보 |
| 용역 | `/getCntrctInfoListServcPPSSrch` | 나라장터 검색조건 |
| 용역 | `/getCntrctInfoListServcChgHstry` | 변경이력 |
| 용역 | `/getCntrctInfoListServcDltHstry` | 삭제이력 |
| 외자 | `/getCntrctInfoListFrgcpt` | 계약현황 |
| 외자 | `/getCntrctInfoListFrgcptDetail` | 외자세부 |
| 외자 | `/getCntrctInfoListFrgcptPPSSrch` | 나라장터 검색조건 |
| 외자 | `/getCntrctInfoListFrgcptChgHstry` | 변경이력 |
| 외자 | `/getCntrctInfoListFrgcptDltHstry` | 삭제이력 |

## 키

- env: `DATA_GO_KR_API_KEY`
- query parameter: `serviceKey`
- 주입 예: `agents-env run DATA_GO_KR_API_KEY -- <명령>`

## 호출 예시

```bash
agents-env run DATA_GO_KR_API_KEY -- curl -sG \
  "https://apis.data.go.kr/1230000/ao/CntrctInfoService/getCntrctInfoListServc" \
  --data-urlencode "serviceKey={{DATA_GO_KR_API_KEY}}" \
  --data-urlencode "pageNo=1" \
  --data-urlencode "numOfRows=10" \
  --data-urlencode "inqryDiv=1" \
  --data-urlencode "inqryBgnDt=202606010000" \
  --data-urlencode "inqryEndDt=202606012359" \
  --data-urlencode "type=json"
```

## 필수/주요 파라미터

| 이름 | 의미 | 형식·예 |
|---|---|---|
| serviceKey | 인증키 | Decoding 키를 `--data-urlencode`로 전달. 문서 표기는 `ServiceKey`지만 실호출은 `serviceKey` 확인 |
| pageNo / numOfRows | 페이지 | `pageNo=1`, `numOfRows=10` |
| type | 응답 형식 | JSON은 `type=json` |
| inqryDiv | 조회구분 | 기본/변경/삭제: `1=일시`, `2=통합계약번호`. PPSSrch: `1=계약체결일자`, `2=확정계약번호`, `3=요청번호`, `4=공고번호` |
| inqryBgnDt / inqryEndDt | 시작/종료 일시 | 기본·변경·삭제 조회. `YYYYMMDDHHMM` |
| inqryBgnDate / inqryEndDate | 시작/종료 일자 | PPSSrch 조회. `YYYYMMDD` |
| untyCntrctNo | 통합계약번호 | `inqryDiv=2`일 때 필수 |
| dcsnCntrctNo | 확정계약번호 | PPSSrch `inqryDiv=2`일 때 필수 |
| reqNo | 요청번호 | PPSSrch `inqryDiv=3`일 때 필수 |
| ntceNo | 공고번호 | PPSSrch `inqryDiv=4`일 때 필수 |
| insttDivCd / insttNm / insttCd | 기관 조건 | PPSSrch에서 계약기관/수요기관 필터 |
| prdctClsfcNoNm | 품명 | 물품·외자 PPSSrch |
| cntrctNm | 계약명 | 용역 PPSSrch |
| cntrctMthdCd | 계약방법코드 | `1=일반경쟁`, `2=제한경쟁`, `3=지명경쟁`, `4=수의계약` |

## 응답 핵심 필드

| 필드 | 의미 |
|---|---|
| untyCntrctNo | 통합계약번호 |
| bsnsDivNm | 업무구분명: 물품, 일반용역, 기술용역, 공사, 외자 |
| dcsnCntrctNo / cntrctRefNo | 확정계약번호 / 계약참조번호 |
| cntrctNm | 계약명 |
| cntrctCnclsDate / cntrctDate | 계약체결일자 / 계약일자 |
| totCntrctAmt / thtmCntrctAmt | 총계약금액 / 금차계약금액 |
| cntrctInsttNm / dminsttList | 계약기관명 / 수요기관목록 |
| corpList | 업체목록 |
| reqNo / ntceNo | 요청번호 / 공고번호 |
| cntrctDtlInfoUrl | 계약상세정보URL |
| rgstDt / chgDt | 등록일시 / 변경일시 |

## 페이징

- `pageNo`와 `numOfRows`를 사용한다.
- `response.body.totalCount`로 전체 건수를 확인하고 `items`를 페이지별로 합친다.
- 계약 데이터는 기간 범위가 넓으면 급격히 커지므로 날짜 구간을 좁게 나눠 수집한다.

## 함정

- 날짜 파라미터가 둘로 갈린다. 기본·변경·삭제 조회는 `inqryBgnDt`/`inqryEndDt`(`YYYYMMDDHHMM`), `*PPSSrch`는 `inqryBgnDate`/`inqryEndDate`(`YYYYMMDD`)다.
- 서비스 URL은 문서에 `http`로 나오지만 `https://apis.data.go.kr/1230000/ao/CntrctInfoService` 호출이 정상 동작한다.
- JSON 응답의 `items`는 배열이다. `response.body.items[]`로 처리한다.
- `corpList`, `dminsttList`는 `^`와 `,`로 묶인 문자열 목록이다. 구조화가 필요하면 별도 파싱한다.
- 업체명으로 직접 검색하는 전용 파라미터는 없다. 업체 기준 분석은 기간/기관/공고번호로 수집한 뒤 `corpList`에서 후처리한다.
