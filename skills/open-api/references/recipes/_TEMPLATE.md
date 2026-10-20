# <API 공식명>

<!-- 파일명 규칙: <provider>/<english-slug>.md. 한글 파일명 금지 -->

> provider: <data.go.kr | opendart.fss.or.kr | plus.kipris.or.kr | ntis.go.kr>
> official: <공식 문서 또는 상세 페이지 URL>
> checked: <YYYY-MM-DD> · 상태: <실호출 검증됨 | 스키마만 확보 | 신청/승인 필요>

## 언제 쓰나

<이 레시피로 풀리는 작업을 검색 키워드가 풍부하게 1~2문장으로 적는다. 동의어와 기관명을 포함한다.>

## Endpoint

- base: `<base url>`
- operation: `<operation/path>`
- method: `<GET | POST>`

## 키

- env: `<KEY_NAME>`
- 주입 예: `agents-env run <KEY_NAME> -- <명령>`

## 호출 예시

```bash
curl -sG "<endpoint>" \
  --data-urlencode "<key-param>=$<KEY_NAME>" \
  --data-urlencode "<필수파라미터>=<값>"
```

## 필수/주요 파라미터

| 이름 | 의미 | 형식·예 |
|---|---|---|

## 응답 핵심 필드

| 필드 | 의미 |
|---|---|

## 페이징

<pageNo/numOfRows, cursor, limit/offset, totalCount 등. 없으면 "없음".>

## 함정

- <이 API 고유의 날짜 형식, 코드값, 신청 범위, 0건 의미, 인코딩 특이사항>
