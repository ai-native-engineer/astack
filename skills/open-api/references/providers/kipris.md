# Provider: plus.kipris.or.kr (KIPRIS)

특허·상표·디자인·실용신안 등 지식재산권 조회가 목적이면 plus.kipris.or.kr(KIPRIS Plus)를 쓴다.

- checked: 2026-06-28
- domain: `plus.kipris.or.kr`
- alias: KIPRIS/키프리스
- key env: `KIPRIS_API_KEY`
- recipes: `references/recipes/kipris/*.md`

## 목차

- 언제 쓰나
- 키
- 흐름
- 공개 카탈로그
- 활용신청 확인
- 통합명세 추출
- Operation Index
- Endpoint 패턴
- 함정

## 언제 쓰나

- 특허, 실용신안, 상표, 디자인
- 출원인·권리자·발명자 기준 검색
- 출원번호, 공개번호, 등록번호 조회
- 회사의 기술 포트폴리오, 브랜드 상표 보유 여부 확인

## 키

- 기본 키 이름: `KIPRIS_API_KEY`
- 서비스별 신청·승인이 나뉠 수 있으므로 미승인 응답이면 신청할 서비스명을 확인한다.

## 흐름

1. 권리 유형을 먼저 고른다: 특허/실용신안, 상표, 디자인.
2. 레시피를 검색한다. 없으면 `kipris-operation-index.json`에서 서비스와 operation을 고른다.
3. 기본 후보는 `deprecated=false` operation으로 제한한다.
4. 출원인명·권리자명 표기를 여러 형태로 검색한다.
5. 번호 조회는 번호 종류를 구분한다: 출원번호, 공개번호, 등록번호.
6. 결과에는 상태, 출원일, 공개일, 등록일, 명칭, 출원인/권리자를 함께 남긴다.

## 공개 카탈로그

서비스 목록은 로그인 없이 읽힌다.

```text
https://plus.kipris.or.kr/portal/data/service/List.do?subTab=SC001&entYn=N&menuNo=200100
```

- 목록 HTML 안의 `var data = [...]`가 서비스 카탈로그다.
- 페이지네이션은 `pageIndex`로 돈다. 2026-06-28 확인 기준 5페이지, 50개 API 서비스.
- 보존할 필드: `bCode`, `serviceNm`, `kppBCodenm`, `kppMCodenm`, `kppSCodenm`, `provideOzanm`, `updateCycle`, `opUseYn`, `buUseYn`, `frUseYn`, `licenseYn`, `opStatusYn`.
- 상세 URL 형식: `https://plus.kipris.or.kr/portal/data/service/<bCode>/view.do?menuNo=200100&kppBCode=&kppMCode=&kppSCode=&subTab=SC001&entYn=N&clasKeyword=`

## 활용신청 확인

로그인된 세션에서 신청/활성 상태를 확인한다.

```text
https://plus.kipris.or.kr/portal/data/request/apiFsmtmList.do?menuNo=290005
https://plus.kipris.or.kr/portal/mypage/prclsMng.do?menuNo=200035
```

| 용도 | method | endpoint |
|---|---|---|
| 장바구니 중복/가능 여부 확인 | POST | `/api/data/request/checkKplusDataSpbskt.do` |
| 장바구니 등록 | POST | `/portal/data/request/fsmtmCart.do` |
| 구매내역 상세 팝업 | GET | `/popup/portal/prclsMngPopup.do?prclsSeq=<주문번호>` |

장바구니 POST에는 `list=<bCode JSON array>`와 `kplusDataTpcd=KP051`을 보낸다.
무료 신청은 장바구니에서 `무료(월 1,000건 호출 제한)`을 선택하고 최종 수수료가 `0`인지 확인한 뒤 제출한다.
유료, 결제, 비영(0)원 수수료가 보이면 제출하지 않는다.

2026-06-28 로그인 계정 확인 기준:

- Open API 카탈로그 50개 중 48개는 구매내역 상세에서 같은 `bCode`로 `사용중`이었다.
- `법적 상태 이력(특허·실용(ST.27), 상표, 디자인(ST.87))`와 `권리자 변동 이력`은 신청 시 하위 API 5개로 풀려 등록됐다.
- 해당 신청 주문은 `KI202606280906460001`, 결제금액 `0`, 상태 `사용중`이었다.

## 통합명세 추출

전체 operation과 입출력 파라미터는 "API 통합설명서(명세서)" 페이지의 공개 AJAX를 쓰는 쪽이 안정적이다.

```text
https://plus.kipris.or.kr/portal/main/contents.do?menuNo=210165
```

| 용도 | method | endpoint |
|---|---|---|
| 서비스 검색 | POST | `https://plus.kipris.or.kr/portal/data/request/serviceSearch.do` |
| operation 검색 | POST | `https://plus.kipris.or.kr/portal/data/request/apiSearch.do` |
| 선택 operation 입출력 row | POST | `https://plus.kipris.or.kr/portal/popup/data/request/apiDescriptionAllSearch.do` |
| operation 단건 설명 팝업 | GET | `https://plus.kipris.or.kr/portal/popup/<bCode>/<scode>/<apiDetailSeq>/apiDescriptionSearch.do` |

검색 POST의 기본 form은 아래처럼 비워 전체를 받는다.

```text
dataType=KP051
kppBCode=
kppMCode=
kppSCode=
apiBCode=
apiSCode=
apiGCode=
clasKeyword=
clasKeyword1=
clasKeyword2=
clasKeyword5=
clasKeyword6=
```

`apiDescriptionAllSearch`는 선택한 operation 배열을 JSON 문자열로 보낸다.

```text
bCodeList=["DBII_..."]
scodeList=["SC002"]
apiDetailIdList=["ADI_..."]
```

응답은 JSON 배열이 아니라 JSON 문자열로 감싼 배열일 수 있다. 한 번 파싱한 값이 문자열이면 다시 `JSON.parse`한다.

2026-06-28 공개 표면 확인값:

- `serviceSearch`: 50개 서비스.
- `apiSearch`: 579개 operation.
- `apiDescriptionAllSearch`: 10,281개 입출력 파라미터 row.
- `scodeNm`: 확인된 operation은 모두 REST.

## Operation Index

전체 operation inventory는 이 파일 옆의 `kipris-operation-index.json`에 둔다.

- 2026-06-28 추출 기준: 전체 579개, 정상 후보 549개, 폐기예정 30개.
- 각 항목은 `serviceNm`, `groupName`, `displayName`, `operation`, `serviceId`, `apiDetailSeq`, `deprecated`, `inputParameterNames`, `popupUrl`을 가진다.
- `deprecated=true`는 공식 표시명에 `폐기예정`이 들어간 operation이다.
- operation을 고를 때는 먼저 `deprecated=false`에서 찾는다.
- 사용자가 폐기예정 operation을 직접 지정했거나 대체 operation이 없을 때만 `deprecated=true`를 쓰고, 응답에 폐기예정임을 밝힌다.
- `inferredRequestUrlPattern`은 추정값이다. 실제 호출 URL은 `popupUrl`의 "입력값 예시(Request Sample)"를 우선한다.

예시:

```bash
jq -r '.operations[]
  | select(.serviceNm=="특허·실용 공개·등록공보" and .deprecated==false)
  | [.groupName,.displayName,.operation,.serviceId,(.inputParameterNames|join(","))]
  | @tsv' ${CLAUDE_PLUGIN_ROOT}/skills/open-api/references/providers/kipris-operation-index.json
```

## Endpoint 패턴

단건 팝업의 "입력값 예시(Request Sample)"에서 실제 호출 패턴을 확인한다. operation별로 base URL과 키 파라미터명이 다를 수 있으므로 다른 operation의 패턴을 옮겨 쓰지 않는다.

```text
http://plus.kipris.or.kr/kipo-api/kipi/<serviceId>/<operation>?<params>&ServiceKey=<서비스키>
http://plus.kipris.or.kr/openapi/rest/<serviceId>/<operation>?<params>&accessKey=<서비스키>
```

예: `특허·실용 공개·등록공보`의 서지상세정보.

```text
http://plus.kipris.or.kr/kipo-api/kipi/patUtiModInfoSearchSevice/getBibliographyDetailInfoSearch?applicationNumber=1020050050026&ServiceKey=서비스키
```

예: 같은 서비스의 출원번호 검색.

```text
http://plus.kipris.or.kr/openapi/rest/patUtiModInfoSearchSevice/applicationNumberSearchInfo?applicationNumber=1020050050026&docsStart=1&accessKey=서비스키
```

상세 페이지의 operation link에는 `setServiceNm('<serviceId>','<operation>')`가 들어 있다. `apiSearch` 결과에 `serviceId`가 없으면 상세 페이지에서 `apiDetailSeq`와 `scode`로 매칭한다.

## 함정

- 회사명 표기가 조금만 달라도 결과가 갈린다.
- 계열사·공동출원은 별도 후보로 분리한다.
- 검색 0건은 권리 없음이 아니라 검색식 불일치일 수 있다.
- `단어(폐기예정)`, `번호(폐기예정)`처럼 목록 앞에 보이는 operation이 대표 후보가 아닐 수 있다. 전체 index에서 같은 서비스의 비폐기 operation을 먼저 찾는다.
- `ServiceKey` 파라미터는 대소문자를 그대로 둔다.
- 일부 operation은 `accessKey`를 쓴다. 키 파라미터명은 operation 팝업의 Request Sample을 따른다.
- 공개 명세 추출과 실제 API 활용신청은 다르다. 호출 권한이 없으면 서비스명을 기준으로 활용신청/승인 상태를 확인하고, 사용자가 신청까지 요청한 경우 공식 절차로 제출한다.
- 일부 신청 항목은 카탈로그 `bCode` 그대로가 아니라 하위 서비스 여러 개로 등록된다. 구매내역 상세의 `serviceNm`, `licenseYn`, `dataMotnProcStnm`으로 최종 활성 서비스를 확인한다.
- 단건 `ajaxOperation.do`는 폼 컨텍스트 없이 직접 호출하면 빈 grid를 줄 수 있다. 전체 입출력 row는 통합명세의 `apiDescriptionAllSearch`를 우선한다.
