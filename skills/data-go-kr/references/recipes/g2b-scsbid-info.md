# 조달청_나라장터 낙찰정보서비스

> publicDataPk: 15129397 · 상세: https://www.data.go.kr/data/15129397/openapi.do
> checked: 2026-06-10 · 상태: **실호출 검증됨** (getScsbidListSttusServc, inqryDiv=1+YYYYMMDDHHMM+type=json으로 HTTP 200·resultCode 00 확인. 활용신청 승인 2026-06-10, 일일 1000건/오퍼레이션)
> 심층 문서: `docs/260610_조달청_OpenAPI참고자료_나라장터_낙찰정보서비스_1.1.md` (원본 .docx 동봉 — 전체 오퍼레이션 23종·응답 필드 정의·샘플 URL)

## 언제 쓰나

특정 회사의 관급 수주 이력, 나라장터 낙찰·개찰 결과, 입찰 결과 조회, 최종낙찰업체·낙찰금액·낙찰률 확인, 수요기관별 발주 이력 역추적.

## Endpoint

- host: `apis.data.go.kr/1230000/as/ScsbidInfoService`
- 낙찰목록(업무별 4종): `/getScsbidListSttusThng`(물품) `/getScsbidListSttusCnstwk`(공사) `/getScsbidListSttusServc`(용역 — 감리·CM·설계 용역은 여기) `/getScsbidListSttusFrgcpt`(외자)
- 개찰결과: `/getOpengResultListInfo{Thng|Cnstwk|Servc|Frgcpt}` (+ `Rebid` 재입찰, `Failing` 유찰, `*PreparPcDetail` 복수예비가격)
- `*PPSSrch` 접미 변형: 검색조건 확장판 — 필요 시 상세 페이지에서 파라미터 비교

## 호출 예시

```bash
curl -sG "https://apis.data.go.kr/1230000/as/ScsbidInfoService/getScsbidListSttusServc" \
  --data-urlencode "serviceKey=$DATA_GO_KR_API_KEY" \
  --data-urlencode "pageNo=1" --data-urlencode "numOfRows=999" \
  --data-urlencode "inqryDiv=1" \
  --data-urlencode "inqryBgnDt=202501010000" --data-urlencode "inqryEndDt=202506302359" \
  --data-urlencode "type=json"
```

## 필수/주요 파라미터 (공식 참고문서 v1.1 확정)

| 이름 | 의미 | 비고 |
|---|---|---|
| serviceKey · pageNo · numOfRows | 공통 | required |
| inqryDiv | 조회구분 | required. **1=등록일시, 2=공고일시, 3=개찰일시, 4=입찰공고번호** |
| inqryBgnDt / inqryEndDt | 조회 시작/종료 일시 | 형식 `YYYYMMDDHHMM`. inqryDiv 1·2·3일 때 필수 |
| bidNtceNo | 입찰공고번호 | inqryDiv=4일 때 필수 |
| type | 응답 형식 | `json` |

조회기간 상한은 참고문서에 명시 없음. PPSSrch 변형은 공고기관·수요기관·업종코드·추정가격 범위 등 검색조건 확장(낙찰업체명 검색은 여전히 없음) — 전체 파라미터는 심층 문서 참조.

## 응답 핵심 필드

| 필드 | 의미 |
|---|---|
| bidwinnrNm / bidwinnrBizno / bidwinnrCeoNm | 최종낙찰업체명 / 사업자등록번호 / 대표자명 |
| sucsfbidAmt / sucsfbidRate | 최종낙찰금액 / 낙찰률 |
| bidNtceNo / bidNtceNm | 입찰공고번호 / 공고명 |
| dminsttNm | 수요기관명 (발주처) |
| rlOpengDt / fnlSucsfDate | 실개찰일시 / 최종낙찰일자 |
| prtcptCnum | 참가업체수 (경쟁 강도) |

## 함정

- **업체명으로 직접 검색하는 파라미터가 없다.** 특정 회사의 수주 이력은 기간 순회 → `bidwinnrBizno`(사업자번호)로 클라이언트 필터. 업체 기준 검색이 급하면 "조달청_나라장터 공공데이터개방표준서비스"(별도 신청) 쪽을 검토.
- 회사 필터는 업체명 문자열이 아니라 **사업자등록번호로** — 동명 법인 혼입 방지.
- **JSON 응답의 `items`는 바로 배열**(`response.body.items[]`) — Swagger·참고문서의 `items.item` 중첩은 XML 기준이라 JSON 파싱 코드에 그대로 쓰면 깨진다 (2026-06-10 실측).
- 응답 일시 형식은 요청(`YYYYMMDDHHMM`)과 달리 `YYYY-MM-DD HH:MM:SS`.
- 활용신청 승인 → 키 동기화 실측 약 10~20분 (그 전엔 HTTP 403 평문 Forbidden).
