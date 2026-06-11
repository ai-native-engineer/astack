# <API 공식명>

<!-- 파일명 규칙: <기관영문약칭>-<데이터영문키워드>.md (예: g2b-scsbid-info.md, nps-workplace.md). 한글 파일명 금지 -->

> publicDataPk: <숫자> · 상세: https://www.data.go.kr/data/<publicDataPk>/openapi.do
> checked: <YYYY-MM-DD> · 상태: <실호출 검증됨 | 스키마만 확보(실호출 미검증)>

## 언제 쓰나

<이 레시피로 풀리는 작업을 검색 키워드가 풍부하게 1~2문장. 레시피 탐색이 rg 기반이므로 동의어를 포함: 예) 낙찰·개찰·입찰결과·수주이력>

## Endpoint

- host: `<apis.data.go.kr/... 또는 api.odcloud.kr/...>`
- 주요 오퍼레이션: `<경로>` — <용도 1줄> (여러 개면 표로)

## 호출 예시

```bash
curl -sG "https://<host>/<operation>" \
  --data-urlencode "serviceKey=$DATA_GO_KR_API_KEY" \
  --data-urlencode "<필수파라미터>=<값>" \
  --data-urlencode "type=json"
```

## 필수/주요 파라미터

| 이름 | 의미 | 형식·예 |
|---|---|---|

## 응답 핵심 필드

| 필드 | 의미 |
|---|---|

## 함정

- <이 API 고유의 함정: 날짜 형식, 조회기간 제한, 인코딩 특이사항 등. 없으면 섹션 삭제>
