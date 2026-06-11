# Entity Resolution

브랜드 기업, 수입 유통사, 한국 법인, 모회사 구조에서는 "대표 홈페이지 1개" 가정이 자주 깨진다. 이 경우 먼저 public surface를 분해한다.

## Surface Map

최소한 아래 칸을 채운다.

- legal entity
- parent company
- email domain
- local consumer brand site
- B2B portal
- careers / recruiter
- investor relations host
- attachment host / CDN

## Common Patterns

### 1. 법인 홈페이지는 없고 브랜드 사이트만 있는 경우

- footer의 법인명 / 대표 / 사업자등록번호 / 주소를 우선 증거로 쓴다
- 같은 회사가 여러 브랜드 사이트를 운영하면 각 브랜드 footer가 같은 법인으로 수렴하는지 본다

### 2. B2B 포털과 소비자 사이트 정보가 다른 경우

- 둘 다 버리지 말고 "현재 운영" vs "레거시 시스템 흔적" 가설로 분리한다
- 주소, 사업자번호, 신고번호의 일치/불일치를 기록한다

### 3. IR 문서가 별도 호스트에 있는 경우

- q4cdn, 별도 investor 서브도메인, SEC/공시 링크는 first-party attachment 로 취급한다
- same-domain 룰 때문에 빠뜨리면 안 된다

### 4. 채용 사이트가 별도 ATS 인 경우

- recruiter, greenhouse, lever, jobkorea 등 채용 표면도 회사 현재 투자 방향의 근거다
- 403/로그인 차단이면 대체 채용 플랫폼으로 우회하고 공백을 적는다

## Priority

1. 법인 식별 정보
2. 현재 운영 중인 브랜드/채널
3. 재무/IR/공시
4. 채용/운영 시그널
5. 외부 기사와 인터뷰

## Don’ts

- parent portfolio를 local operating scope로 자동 변환하지 않는다
- 한 브랜드 사이트만 보고 전체 법인 구조를 확정하지 않는다
- 이메일 도메인만 보고 공식 public site가 있다고 가정하지 않는다
