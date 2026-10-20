# KIPRIS 특허·실용 서지상세정보

> provider: plus.kipris.or.kr
> official: https://plus.kipris.or.kr/portal/data/service/DBII_000000000000001/view.do?menuNo=200100&kppBCode=&kppMCode=&kppSCode=&subTab=SC001&entYn=N&clasKeyword=
> checked: 2026-06-28 · 상태: 실제 호출 성공

## 언제 쓰나

특허·실용신안의 출원번호로 공개·등록공보 서지상세정보를 조회할 때 쓴다. 출원번호, 공개번호, 등록번호, 발명의 명칭, 출원인, 발명자, IPC/CPC, 패밀리, 청구항, 국가 R&D 정보 확인 작업의 출발점이다.

## Endpoint

- base: `http://plus.kipris.or.kr/kipo-api/kipi`
- serviceId: `patUtiModInfoSearchSevice`
- operation: `getBibliographyDetailInfoSearch`
- method: `GET`
- detail id: `DBII_000000000000001` / `SC002` / `ADI_0000000000002130`

## 키

- env: `KIPRIS_API_KEY`
- query parameter: `ServiceKey`
- 주입 예: `agents-env run KIPRIS_API_KEY -- <명령>`

## 호출 예시

```bash
curl -sG "http://plus.kipris.or.kr/kipo-api/kipi/patUtiModInfoSearchSevice/getBibliographyDetailInfoSearch" \
  --data-urlencode "applicationNumber=1020050050026" \
  --data-urlencode "ServiceKey=$KIPRIS_API_KEY"
```

## 필수/주요 파라미터

| 이름 | 의미 | 형식·예 |
|---|---|---|
| `applicationNumber` | 출원번호 | `1020050050026` |
| `ServiceKey` | KIPRIS Plus 서비스키 | `$KIPRIS_API_KEY` |

## 응답 핵심 필드

| 필드 | 의미 |
|---|---|
| `applicationDate` | 출원일자 |
| `applicationNumber` | 출원번호 |
| `inventionTitle` | 발명의 명칭(한글) |
| `inventionTitleEng` | 발명의 명칭(영문) |
| `openDate` / `openNumber` | 공개일자 / 공개번호 |
| `publicationDate` / `publicationNumber` | 공고일자 / 공고번호 |
| `registerDate` / `registerNumber` / `registerStatus` | 등록일자 / 등록번호 / 등록상태 |
| `ipcInfoArray` | IPC 정보 |
| `applicantInfoArray` | 출원인 정보 |
| `inventorInfoArray` | 발명자 정보 |
| `rndInfoArray` | 국가연구개발사업 정보 |

## 페이징

없음. 출원번호 단건 상세 조회다.

## 함정

- KIPRIS 공개 명세의 예시는 `ServiceKey`를 대문자로 쓴다.
- 호출 권한이 없으면 `resultCode=31`, `resultMsg=DEADLINE_HAS_EXPIRED_ERROR`가 나올 수 있다. 서비스 신청/연장 후 재시도한다.
- 공식 페이지의 serviceId가 `patUtiModInfoSearchSevice`로 표기되어 있다. 철자처럼 보이는 부분을 임의 수정하지 않는다.
