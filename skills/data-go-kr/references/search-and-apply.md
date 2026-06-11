# API 검색 · 활용신청 · 스키마 추출

> 검색·상세 페이지는 전부 **비로그인 GET** — 크롤로 처리한다 (2026-06 실측). 활용신청만 로그인이 필요해 사용자 몫이다.

## 1. 검색

```bash
curl -sL "https://www.data.go.kr/tcs/dss/selectDataSetList.do?dType=API&keyword=<URL인코딩 키워드>" \
  -A "Mozilla/5.0" -o /tmp/datagokr-search.html
```

- 결과에서 API 상세 링크 추출: `rg -o 'href="/data/[0-9]+/openapi\.do"'` → 숫자가 **publicDataPk**.
- 제목·제공기관·키워드는 링크 주변 HTML에서 함께 추출해 후보를 비교한다. 활용신청 건수가 많은 API가 보통 정본이다.
- 키워드 팁: 데이터명보다 **기관명+업무**(예 "조달청 낙찰", "국민연금 사업장")가 잘 잡힌다. 0건이면 동의어로 2~3회 재시도(예 "입찰"↔"낙찰"↔"계약").

## 2. 상세 페이지 — 스키마가 인라인으로 박혀 있다

```bash
curl -sL "https://www.data.go.kr/data/<publicDataPk>/openapi.do" -A "Mozilla/5.0" -o /tmp/detail.html
```

핵심: 페이지 안에 **Swagger JSON 전문이 인라인**으로 들어 있다 (`var swaggerJson = \`{...}\`;`). 별도 엔드포인트 불필요.

```python
import re, json
html = open('/tmp/detail.html').read()
sw = json.loads(re.search(r'var swaggerJson = `(.*?)`;', html, re.S).group(1))
sw['host']         # 예: apis.data.go.kr/1230000/as/ScsbidInfoService
sw['paths'].keys() # 오퍼레이션 목록
```

- 함정: 요청 파라미터는 오퍼레이션의 `get` 아래가 아니라 **path 레벨** `sw['paths'][op]['parameters']`에 있다 (2026-06 실측 — `get`만 보면 빈 것처럼 보인다). required 여부·한국어 설명까지 여기 다 있다.
- 응답 필드 설명은 인라인 Swagger의 `responses` 스키마에 한국어로 다 있다 — 레시피의 "응답 핵심 필드"는 여기서 뽑는다.
- **인라인 Swagger가 없는 구형 API 폴백**: long-tail에는 Swagger 없이 참고문서(HWP/Word/PDF 첨부)만 있는 API가 상당수다. regex가 안 잡히면 ① 상세 페이지의 "참고문서" 첨부를 내려받아 파라미터 표를 추출하거나 ② 페이지의 샘플 코드/미리보기 영역에서 endpoint·파라미터를 줍거나 ③ 같은 데이터의 표준형("공공데이터개방표준") 후보로 갈아탄다. 셋 다 안 되면 그 API는 "스키마 확보 실패"로 사용자에게 보고한다 — 추측 호출 금지.
- **공식 참고문서 보존 규칙**: 참고문서를 확보하면(사용자 제공 포함) `references/recipes/docs/`에 **원본 그대로 + `YYMMDD_원본파일명` 프리픽스**로 저장하고, `pandoc <원본> -t gfm --wrap=none -o <같은이름>.md`로 변환본을 나란히 둔다. 레시피 헤더의 "심층 문서" 줄로 연결 — 레시피는 요약, 변환본은 전체 정의(전 오퍼레이션·응답 필드·샘플)의 권위 소스가 된다. Swagger보다 참고문서가 상세한 경우(inqryDiv 코드값 등)가 많아 둘 다 확보됐으면 문서가 우선.

## 3. 활용신청 (사용자 몫)

- 미신청 키로 호출하면 에러(call-patterns.md의 코드 표)가 떨어진다. 그때 사용자에게 전달할 것:
  1. 딥링크: `https://www.data.go.kr/data/<publicDataPk>/openapi.do` → 페이지의 **[활용신청]** 버튼
  2. "로그인 → 활용목적 입력 → 동의 → 신청. 개발계정은 **자동승인**, 키 동기화는 즉시~1시간"
- 같은 계정의 **일반 인증키 1개**가 신청한 모든 API에 공용으로 쓰인다 — API마다 키가 늘어나는 게 아니라 신청만 추가되는 구조.
- 신청 후에도 같은 에러면: 동기화 대기 중이거나, 비슷한 이름의 **다른 API에 신청**한 것 — publicDataPk가 일치하는지 확인.

## 4. 후보가 여럿일 때

- 같은 데이터가 "OO서비스"(전통형)와 "OO 공공데이터개방표준서비스"(표준형)로 중복 제공되는 경우가 흔하다. 표준형이 필드가 정규화돼 있지만 운영 공지(조회기간 축소 등)가 붙어 있을 수 있다 — 상세 페이지 상단 공지를 확인하고 선택 근거를 레시피에 남긴다.

> 참고 패턴 출처: NomaDamas/k-skill (활용신청 딥링크·에러 시맨틱 문서화 방식 차용)
