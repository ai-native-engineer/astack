# Strategic Account & Entity Resolution Guidelines

본 문서는 `company-context-research` 스킬 실행 시 영업적 관점(Account Priority) 및 법인 구조 식별(Entity Resolution)을 포함한 전략적 리서치 가이드를 제공합니다.

---

## 1. Account Priority (계정 우선 모드 판단)

영업 실무에서는 관계에 따른 조사의 목적이 중요하므로 아래 두 모드를 명확히 분리하여 실행합니다.

* **`account-first`**: 이미 관계가 있는 계정, 기존 프로젝트/폴더에 context가 존재하는 경우.
* **`cold research`**: 처음 마주하는 신규 영업 타깃.

### 💡 account-first 모드 핵심 체크리스트
이 모드에서는 일반적인 회사 소개가 우선이 아닙니다. 아래 6대 질문에 우선 답변해야 합니다:
1. 지금 **딜(Deal) 단계**가 어디인가?
2. 내부 **챔피언(Champion / Buying Center)**이 누구인가?
3. **다음 미팅에서 확인할 질문**이 무엇인가?
4. **참가자별 실무 니즈**가 어떻게 나뉘는가?
5. **리스크 및 블로커(Red Flags)**가 무엇인가?
6. 공개 웹 정보가 위 1~5를 어떻게 뒷받침하거나 기여할 수 있는가?

### `data/company-profile.json.summary` 우선 입력 순서
1. `deal_status`: 현재 딜 상태
2. `champion_buying_center`: 내부 챔피언 / buying center
3. `participant_needs`: 참가자별 니즈
4. `open_questions`: 다음 미팅에서 확인할 질문
5. `buying_signals`: 공개 웹 / 보도 / 재무 보강
6. `what_they_do`: 일반적인 회사 소개 및 정보

### 🏢 모회사 우선 규칙 (Parent-company rule)
글로벌/그룹 모회사 정보는 아래 경우에만 전면에 배치하고, 그 외에는 Supporting note로 내립니다:
* 예산 책정 및 최종 결재 라인을 암시할 때
* 브랜드 제품 범위나 사업 영역을 규정할 때
* 현지 법인 구조의 불일치나 혼동을 해소할 때

---

## 2. Entity Resolution (분절된 법인 표면 매핑)

브랜드 기업, 수입 유통사, 한국 법인, 모회사 구조에서는 홈페이지 1개 가정이 깨집니다. 이 경우 먼저 `data/company-profile.json.surface_map`을 구성합니다.

### 🌐 Surface Map 구성 요소
* **legal entity**: 공식 법인명 및 등록 정보
* **parent company**: 모회사 및 계열 구조
* **email domain**: 실제 도메인 주소
* **local consumer brand site**: 국내 소비자 타깃 브랜드/D2C 몰
* **B2B portal**: 도매, 대리점, 파트너 전용 시스템
* **careers / recruiter**: 인재 채용 플랫폼 (JobKorea, Greenhouse, Lever 등)
* **investor relations host**: 주주 및 IR 전용 페이지 (q4cdn 등)
* **attachment host / CDN**: 실제 첨부파일 업로드 경로

### 🔎 중복 법인명 및 데이터 없음(013) 처리 규칙 (DART)
한국 법인 조사 시 `corpCode.xml`에서 이름이 중복되는 법인이 발견되거나 공시 데이터 조회 실패 시 다음 규칙을 적용합니다:
* **`stock_code` 필드 대조**: 상장법인만 stock_code가 존재하므로 최우선 판별자로 사용합니다.
* **`corp_cls` 필드**: `Y`=상장, `K`=코스닥, `N`=코넥스, `E`=기타(비상장). 상장법인을 찾으려면 `Y`나 `K`를 우선합니다.
* **`bizr_no`(사업자번호) 및 `est_dt`(설립일)**: 법인의 분할 및 변경 이력이 있는 경우 사업자번호를 통해 대조합니다.
* **DART 013 (데이터 없음) 발생 시**:
  1. 합병 피흡수(인수법인으로의 이관) 또는 분할, 상장폐지를 의심하고 footer 및 뉴스룸에서 개편 키워드를 확인합니다.
  2. 공시 매핑 지연일 경우, 즉시 **웹 쿼리 보강(Web Financial Fallback)**을 수행하여 매출액/영업이익/당기순이익 실적 데이터를 채웁니다.

---

## 3. Source & Research Patterns (수집 Heuristics)

### 🎯 Actionable Sales Intel 수집 항목
1. 회사가 실제로 해결하고 있는 업계 문제 및 사업 모델
2. 최근 뉴스와 파트너십 이벤트
3. 채용 및 조직 확장 추이 (구매, R&D, 물류 부서 성장 시그널)
4. 핵심 의사결정권자 및 인물 정보
5. **왜 지금 접촉해야 하는지 (Buying Signal)**
6. 미팅 오프너로 활용할 수 있는 추천 접근 화법

### 💡 Sales Seminar Heuristic
* 회사가 자사 채널에서 자주 반복하여 사용하는 **특유의 언어, 전략적 헤드카피, proof point 수치, 고객 피드백 주장**을 누락 없이 발췌하여 제안서 문구나 질문으로 연계되도록 보존합니다.

### 🚫 주의 및 회피 사항 (Don'ts)
* 디자인이나 트렌디한 문구만 보고 회사의 실제 비즈니스 모델이나 ICP를 넘겨짚지 않습니다.
* 모회사와 자회사의 실제 사업 범위와 예산 구조를 명확히 구분하고 명시적 근거 없이 묶어 취급하지 않습니다.
* 오래된 주가 시세나 과거 공시를 현재 기업 가치인 것처럼 설명하지 않습니다.
