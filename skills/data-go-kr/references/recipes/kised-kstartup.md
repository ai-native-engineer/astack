# 창업진흥원_K-Startup(사업소개,사업공고,콘텐츠 등)_조회서비스

> publicDataPk: 15125364 · 상세: https://www.data.go.kr/data/15125364/openapi.do
> checked: 2026-06-28 · 상태: **실호출 검증됨** (4개 operation 모두 `page=1&perPage=1&returnType=json` HTTP 200·JSON 확인)
> 활용기간: 2026-06-28 ~ 2028-06-28 · 일일 10000건/오퍼레이션
> 심층 문서: `docs/260628-kised-kstartup-reference-v2.0.md` (원본 .docx 동봉) · 코드표: `docs/260628-kised-kstartup-codes.xlsx`

## 언제 쓰나

K-Startup 창업지원사업 공고, 모집중인 지원사업, 지역·대상·창업기간별 사업공고, 창업지원 사업소개, 창업 관련 콘텐츠·정책·우수사례, 창업 통계보고서 조회.

## Endpoint

- host: `apis.data.go.kr/B552735/kisedKstartupService01`

| 오퍼레이션 | 용도 |
|---|---|
| `/getAnnouncementInformation01` | 지원사업 공고 정보 |
| `/getBusinessInformation01` | 통합공고 지원사업/사업소개 정보 |
| `/getContentInformation01` | 창업관련 콘텐츠 정보 |
| `/getStatisticalInformation01` | 창업관련 통계보고서 정보 |

## 키

- env: `DATA_GO_KR_API_KEY`
- query parameter: `serviceKey`
- 주입 예: `agents-env run DATA_GO_KR_API_KEY -- <명령>`

## 호출 예시

```bash
agents-env run DATA_GO_KR_API_KEY -- curl -sG \
  "https://apis.data.go.kr/B552735/kisedKstartupService01/getAnnouncementInformation01" \
  --data-urlencode "serviceKey={{DATA_GO_KR_API_KEY}}" \
  --data-urlencode "page=1" \
  --data-urlencode "perPage=10" \
  --data-urlencode "returnType=json" \
  --data-urlencode "cond[rcrt_prgs_yn::EQ]=Y" \
  --data-urlencode "cond[biz_pbanc_nm::LIKE]=창업"
```

## 필수/주요 파라미터

| 이름 | 의미 | 형식·예 |
|---|---|---|
| serviceKey | 인증키 | required, Decoding 키 사용 |
| page / perPage | 페이지 | `page=1`, `perPage=10` |
| returnType | 응답 형식 | `json` 권장. 명시하지 않으면 문서별 기본값 설명이 엇갈림 |
| cond[field::LIKE] | 부분일치 필터 | `cond[biz_pbanc_nm::LIKE]=창업`, `cond[supt_regin::LIKE]=서울` |
| cond[field::EQ] | 정확일치 필터 | `cond[rcrt_prgs_yn::EQ]=Y`, `cond[biz_yr::EQ]=2026` |
| cond[pbanc_rcpt_bgng_dt::GTE] | 공고 접수 시작일 이상 | `YYYYMMDD`, 공고 조회 전용 |
| cond[pbanc_rcpt_end_dt::LTE] | 공고 접수 종료일 이하 | `YYYYMMDD`, 공고 조회 전용 |

### 주요 필터

| 오퍼레이션 | 필터 |
|---|---|
| getAnnouncementInformation01 | `cond[intg_pbanc_yn::EQ]`, `cond[intg_pbanc_biz_nm::LIKE]`, `cond[biz_pbanc_nm::LIKE]`, `cond[supt_biz_clsfc::LIKE]`, `cond[aply_trgt_ctnt::LIKE]`, `cond[supt_regin::LIKE]`, `cond[pbanc_rcpt_bgng_dt::GTE]`, `cond[pbanc_rcpt_end_dt::LTE]`, `cond[aply_trgt::LIKE]`, `cond[biz_enyy::LIKE]`, `cond[biz_trgt_age::LIKE]`, `cond[prfn_matr::LIKE]`, `cond[rcrt_prgs_yn::EQ]` |
| getBusinessInformation01 | `cond[biz_category_cd::EQ]`, `cond[supt_biz_titl_nm::LIKE]`, `cond[biz_supt_trgt_info::LIKE]`, `cond[biz_supt_bdgt_info::LIKE]`, `cond[biz_supt_ctnt::LIKE]`, `cond[supt_biz_chrct::LIKE]`, `cond[supt_biz_intrd_info::LIKE]`, `cond[biz_yr::EQ]` |
| getContentInformation01 | `cond[clss_cd::EQ]`, `cond[titl_nm::LIKE]` |
| getStatisticalInformation01 | `cond[titl_nm::LIKE]`, `cond[file_nm::LIKE]` |

### 코드값

| 코드 | 값 |
|---|---|
| `biz_category_cd` | `cmrczn_Tab1` 사업화, `cmrczn_Tab2` 창업교육, `cmrczn_Tab3` 시설·공간·보육, `cmrczn_Tab4` 멘토링·컨설팅, `cmrczn_Tab5` 행사·네트워크, `cmrczn_Tab6` 기술개발 R&D, `cmrczn_Tab7` 융자, `cmrczn_Tab8` 인력, `cmrczn_Tab9` 글로벌 |
| `clss_cd` | `notice_matr` 정책 및 규제정보/공지사항, `fnd_scs_case` 창업우수사례, `kstartup_isse_trd` 생태계 이슈·동향 |

## 응답 핵심 필드

JSON 루트는 `currentCount`, `matchCount`, `page`, `perPage`, `totalCount`, `data[]`.

| 오퍼레이션 | 주요 필드 |
|---|---|
| getAnnouncementInformation01 | `biz_pbanc_nm`, `pbanc_ctnt`, `supt_biz_clsfc`, `supt_regin`, `pbanc_rcpt_bgng_dt`, `pbanc_rcpt_end_dt`, `pbanc_ntrp_nm`, `sprv_inst`, `biz_aply_url`, `detl_pg_url`, `rcrt_prgs_yn`, `pbanc_sn` |
| getBusinessInformation01 | `biz_category_cd`, `supt_biz_titl_nm`, `biz_supt_trgt_info`, `biz_supt_bdgt_info`, `biz_supt_ctnt`, `supt_biz_chrct`, `supt_biz_intrd_info`, `biz_yr`, `detl_pg_url` |
| getContentInformation01 | `clss_cd`, `titl_nm`, `fstm_reg_dt`, `view_cnt`, `detl_pg_url`, `file_nm` |
| getStatisticalInformation01 | `titl_nm`, `ctnt`, `fstm_reg_dt`, `last_mdfcn_dt`, `detl_pg_url`, `file_nm` |

## 페이징

- 전통형 `pageNo`/`numOfRows`가 아니라 `page`와 `perPage`를 쓴다.
- JSON 루트의 `currentCount`, `matchCount`, `totalCount`, `data[]`를 기준으로 페이지를 이어 붙인다.
- 필터를 쓰면 `matchCount`가 필터 결과 수이고, `totalCount`는 전체 건수를 유지할 수 있다.

## 함정

- 공식 첨부문서에는 `ServiceKey`로 쓰여 있지만 상세 페이지 Swagger와 실호출 기준은 `serviceKey`.
- `returnType=json`을 항상 명시한다. 공식 문서에는 기본 JSON, Swagger에는 기본 XML로 엇갈리게 표기돼 있다.
- `biz_category_cd`는 대소문자 민감. 코드표의 `cmrczn_tab1` 표기는 그대로 쓰면 필터 결과가 0건이고, 실제 값은 `cmrczn_Tab1`처럼 `Tab`의 `T`가 대문자다.
- 필터 사용 시 `matchCount`가 필터 결과 수다. `totalCount`는 전체 건수를 유지할 수 있다.
- JSON은 전통형 `response.body.items`가 아니라 루트 `data[]` 배열이다.
- 일부 `detl_pg_url` 값은 `www.k-startup.go.kr/...`처럼 scheme이 빠져 온다. 링크로 쓸 때 `https://` 보정이 필요하다.
