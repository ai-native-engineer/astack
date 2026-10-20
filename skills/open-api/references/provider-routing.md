# Provider Routing

작업에서 출발해 provider를 고른다. 애매하면 레시피 검색을 먼저 하고, provider 후보를 1~2개만 비교한다.

## 빠른 선택

| 작업 단서 | API domain/provider |
|---|---|
| 공공데이터포털, 나라장터, 국민연금 사업장, 사업자등록 상태, 건축물대장, 행정기관 데이터셋 | data.go.kr |
| 기업 공시, 사업보고서, 감사보고서, 재무제표, 상장/비상장 법인 공시 | opendart.fss.or.kr (DART) |
| 특허, 실용신안, 상표, 디자인, 출원인, 등록번호, 지식재산권 | plus.kipris.or.kr (KIPRIS) |
| 국가 R&D 과제, 연구개발 성과, 연구기관, 과제 참여 기업, 정부 연구비 | ntis.go.kr (NTIS) |

## Provider Coverage

| API domain/provider | key env | 신청·권한 | 레시피·근거 위치 | 현재 커버리지 |
|---|---|---|---|---|
| data.go.kr | `DATA_GO_KR_API_KEY` | API별 활용신청. 신청은 사용자가 하고, 미승인 시 딥링크 안내 | `providers/data-go-kr.md`, `recipes/data-go-kr/*.md`, `recipes/docs/data-go-kr/*` | 나라장터·국민연금·국세청·K-Startup·기업마당 레시피 8개와 원문 참고문서 |
| opendart.fss.or.kr (DART) | `API_K_DART` | DART Open API 키 필요. 서비스별 신청은 보통 없음 | `providers/dart.md`, `recipes/dart/*.md` | corp code, 기업개황, 공시목록, 단일회사 주요계정 |
| plus.kipris.or.kr (KIPRIS) | `KIPRIS_API_KEY` | KIPRIS Plus 서비스별 신청·승인 필요 | `providers/kipris.md`, `providers/kipris-operation-index.json`, `recipes/kipris/*.md` | 공개 카탈로그 50개, operation index 579개, 대표 특허·상표·법적상태·권리자 레시피 |
| ntis.go.kr (NTIS) | `NTIS_API_KEY` | NTIS 서비스별 활용신청·승인 필요. 기관용은 권한 제한 가능 | `providers/ntis.md`, `recipes/ntis/*.md`, `recipes/docs/ntis/*` | 14개 서비스 recipe와 원문 PDF/TXT 보관 |

## 조합 조회

- 회사 1곳을 깊게 볼 때: opendart.fss.or.kr → plus.kipris.or.kr → ntis.go.kr 순서가 보통 빠르다.
- 정부지원·조달 맥락이 있으면: data.go.kr을 먼저 보고, 필요하면 ntis.go.kr을 붙인다.
- 기술 보유 여부는 plus.kipris.or.kr 단독으로 단정하지 않는다. 출원인 표기 변형과 계열사명을 같이 본다.

## 없다고 말하기 전

- 기관명·업무명·동의어로 2~3회 재검색한다.
- 법인명은 띄어쓰기, 주식회사 표기, 영문명, 옛 이름을 바꿔 본다.
- API가 없으면 공식 웹 검색/다운로드만 가능한지 구분해서 보고한다.
