<!-- lint-skip: env-values (외부 공식문서 미러 - 원문 담당자 연락처 포함) -->
서비스설계서\
(창업진흥원_K-Startup(사업소개,사업공고, 콘텐츠 등)\_조회서비스)

[1. 서비스 명세 [3](#_Toc149144025)](#_Toc149144025)

[**1.1 공공데이터 오픈API 조회 서비스** [3](#_Toc149144026)](#_Toc149144026)

[가. API 서비스 개요 [3](#_Toc149144027)](#_Toc149144027)

[나. 상세기능 목록 [3](#_Toc149144028)](#_Toc149144028)

[다. 상세기능내역 [4](#_Toc149144029)](#_Toc149144029)

[1) \[통합공고 지원사업 정보\] 상세기능명세 [4](#_Toc149144030)](#_Toc149144030)

[2) \[지원사업 공고 정보\] 상세기능명세 8](#_Toc149144031)

[3) \[창업관련 콘텐츠 정보\] 상세기능명세 12](#_Toc149144032)

[4) \[창업관련 통계보고서 정보\] 상세기능명세 14](#_Toc149144033)

[2. OpenAPI 에러 코드정리 17](#_Toc149144034)

<span id="_Toc149144025" class="anchor"></span>**1. 서비스 명세**

<span id="_Toc149144026" class="anchor"></span>**1.1 공공데이터 오픈API 조회 서비스**

<span id="_Toc149144027" class="anchor"></span>가. API 서비스 개요

<table>
<colgroup>
<col style="width: 16%" />
<col style="width: 20%" />
<col style="width: 23%" />
<col style="width: 20%" />
<col style="width: 20%" />
</colgroup>
<thead>
<tr>
<th rowspan="3" style="text-align: center;"><strong>API 서비스 정보</strong></th>
<th style="text-align: center;"><strong>API명(영문)</strong></th>
<th colspan="3">kisedKstartupService01</th>
</tr>
<tr>
<th style="text-align: center;"><strong>API명(국문)</strong></th>
<th colspan="3">창업진흥원_K-Startup(사업소개,사업공고, 콘텐츠 등)_조회서비스</th>
</tr>
<tr>
<th style="text-align: center;"><strong>API 설명</strong></th>
<th colspan="3">중소벤처기업부 및 창업진흥원이 운영하는 창업지원포털(k-startp)의 사업공고, 사업정보, 컨텐츠정보 등을 활용할 수 있는 OPEN API서비스(JSON, XML 제공(기본returnType=JSON))</th>
</tr>
</thead>
<tbody>
<tr>
<td rowspan="5" style="text-align: center;"><p><strong>API 서비스</strong></p>
<p><strong>보안적용</strong></p>
<p><strong>기술 수준</strong></p></td>
<td style="text-align: center;"><strong>서비스 인증/권한</strong></td>
<td colspan="3"><p>[O] serviceKey [ ] 인증서 (GPKI/NPKI)</p>
<p>[ ] Basic (ID/PW) [ ] 없음</p></td>
</tr>
<tr>
<td style="text-align: center;"><p><strong>메시지 레벨</strong></p>
<p><strong>암호화</strong></p></td>
<td colspan="3">[ ] 전자서명 [ ] 암호화 [O] 없음</td>
</tr>
<tr>
<td style="text-align: center;"><strong>전송 레벨 암호화</strong></td>
<td colspan="3">[ ] SSL [O] 없음</td>
</tr>
<tr>
<td style="text-align: center;"><strong>인터페이스 표준</strong></td>
<td colspan="3"><p>[ ] SOAP 1.2</p>
<p>(RPC-Encoded, Document Literal, Document Literal Wrapped)</p>
<p>[O] REST (GET)</p>
<p>[ ] RSS 1.0 [ ] RSS 2.0 [ ] Atom 1.0 [ ] 기타</p></td>
</tr>
<tr>
<td style="text-align: center;"><p><strong>교환 데이터 표준</strong></p>
<p><strong>(중복선택가능)</strong></p></td>
<td colspan="3">[O] XML [O] JSON [ ] MIME [ ] MTOM</td>
</tr>
<tr>
<td rowspan="8" style="text-align: center;"><p><strong>API 서비스</strong></p>
<p><strong>배포정보</strong></p></td>
<td style="text-align: center;"><strong>서비스 URL</strong></td>
<td colspan="3"><a href="https://apis.data.go.kr/B552735/kisedKstartupService01">https://apis.data.go.kr/B552735/kisedKstartupService01</a></td>
</tr>
<tr>
<td style="text-align: center;"><p><strong>서비스 명세 URL</strong></p>
<p><strong>(WSDL 또는 WADL)</strong></p></td>
<td colspan="3">https://apis.data.go.kr/B552735/kisedKstartupService01?_wadl&amp;type=xml</td>
</tr>
<tr>
<td style="text-align: center;"><strong>서비스 버전</strong></td>
<td colspan="3">1.0</td>
</tr>
<tr>
<td style="text-align: center;"><strong>서비스 시작일</strong></td>
<td>2023-12-15</td>
<td style="text-align: center;"><strong>서비스 배포일</strong></td>
<td>2023-12-15</td>
</tr>
<tr>
<td style="text-align: center;"><strong>서비스 이력</strong></td>
<td colspan="3"></td>
</tr>
<tr>
<td style="text-align: center;"><strong>메시지 교환유형</strong></td>
<td colspan="3"><p>[O] Request-Response [ ] Publish-Subscribe</p>
<p>[ ] Fire-and-Forgot [ ] Notification</p></td>
</tr>
<tr>
<td style="text-align: center;"><strong>서비스 제공자</strong></td>
<td colspan="3">윤강준 / 디지털정보실 / 044-410-1658 / ykj8797@kised.or.kr</td>
</tr>
<tr>
<td style="text-align: center;"><strong>데이터 갱신주기</strong></td>
<td colspan="3">일 1회</td>
</tr>
</tbody>
</table>

<span id="_Toc149144028" class="anchor"></span>나. 상세기능 목록

| **번호** | **API명(국문)** | **상세기능명(영문)** | **상세기능명(국문)** |
|:--:|----|:--:|----|
| 1 | 창업진흥원_K-Startup(사업소개,사업공고, 콘텐츠 등)\_조회서비스 | getBusinessInformation | 통합공고 지원사업 정보 |
| 2 | 창업진흥원_K-Startup(사업소개,사업공고, 콘텐츠 등)\_조회서비스 | getAnnouncementInformation | 지원사업 공고 정보 |
| 3 | 창업진흥원_K-Startup(사업소개,사업공고, 콘텐츠 등)\_조회서비스 | getContentInformation | 창업관련 콘텐츠 정보 |
| 4 | 창업진흥원_K-Startup(사업소개,사업공고, 콘텐츠 등)\_조회서비스 | getStatisticalInformation | 창업관련 통계보고서 정보 |

<span id="_Toc149144029" class="anchor"></span>다. 상세기능내역

<span id="_Toc149144030" class="anchor"></span>1) \[통합공고 지원사업 정보\] 상세기능명세

a\) 상세기능정보

<table>
<colgroup>
<col style="width: 25%" />
<col style="width: 25%" />
<col style="width: 25%" />
<col style="width: 25%" />
</colgroup>
<thead>
<tr>
<th style="text-align: center;"><strong>상세기능 번호</strong></th>
<th>1</th>
<th style="text-align: center;"><strong>상세기능 유형</strong></th>
<th>조회 (목록)</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: center;"><strong>상세기능명(국문)</strong></td>
<td colspan="3">통합공고 지원사업 정보</td>
</tr>
<tr>
<td style="text-align: center;"><strong>상세기능 설명</strong></td>
<td colspan="3">창업지원사업 예산, 규모, 수행기관, 사업절차, 문의처 등 사업 소개 정보</td>
</tr>
<tr>
<td style="text-align: center;"><p><strong>Call Back URL</strong></p>
<p><strong>(외부노출URL)</strong></p></td>
<td colspan="3">https://apis.data.go.kr/B552735/kisedKstartupService01/getBusinessInformation01</td>
</tr>
<tr>
<td style="text-align: center;"><strong>END POINT URL</strong></td>
<td colspan="3">https://nidapi.k-startup.go.kr/api/kisedKstartupService/v1/getBusinessInformation/</td>
</tr>
<tr>
<td style="text-align: center;"><strong>최대 메시지 사이즈</strong></td>
<td colspan="3">[4000] byte</td>
</tr>
<tr>
<td style="text-align: center;"><strong>평균 응답 시간</strong></td>
<td>[500] ms</td>
<td style="text-align: center;"><strong>초당 최대 트랙잭션</strong></td>
<td>[30] tps</td>
</tr>
</tbody>
</table>

b\) 요청 메시지 명세

<table>
<colgroup>
<col style="width: 16%" />
<col style="width: 16%" />
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 19%" />
<col style="width: 24%" />
</colgroup>
<thead>
<tr>
<th style="text-align: center;"><strong>항목명(영문)</strong></th>
<th style="text-align: center;"><strong>항목명(국문)</strong></th>
<th style="text-align: center;"><strong>항목크기</strong></th>
<th style="text-align: center;"><strong>항목구분</strong></th>
<th style="text-align: center;"><strong>샘플데이터</strong></th>
<th style="text-align: center;"><strong>항목설명</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;">ServiceKey</td>
<td style="text-align: left;">서비스키</td>
<td style="text-align: left;">100</td>
<td style="text-align: center;">1</td>
<td style="text-align: left;"><p>인증키</p>
<p>(URL Encode)</p></td>
<td style="text-align: left;">공공데이터포털에서 발급받은 인증키</td>
</tr>
<tr>
<td style="text-align: left;">page</td>
<td style="text-align: left;">페이지</td>
<td style="text-align: left;">100</td>
<td style="text-align: center;">0</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">페이지</td>
</tr>
<tr>
<td style="text-align: left;">perPage</td>
<td style="text-align: left;">한 페이지 결과 수</td>
<td style="text-align: left;">100</td>
<td style="text-align: center;">0</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td style="text-align: left;">returnType</td>
<td style="text-align: left;">반환타입</td>
<td style="text-align: left;">50</td>
<td style="text-align: center;">0</td>
<td style="text-align: left;">json</td>
<td style="text-align: left;">json/XML</td>
</tr>
<tr>
<td style="text-align: left;">biz_category_cd</td>
<td style="text-align: left;">사업 구분 코드</td>
<td style="text-align: left;">50</td>
<td style="text-align: center;">0</td>
<td style="text-align: left;">cmrczn_Tab3</td>
<td style="text-align: left;">사업 구분 코드</td>
</tr>
<tr>
<td style="text-align: left;">supt_biz_titl_nm</td>
<td style="text-align: left;">사업 명</td>
<td style="text-align: left;">300</td>
<td style="text-align: center;">0</td>
<td style="text-align: left;">1인 창조기업 활성화 지원사업</td>
<td style="text-align: left;">사업 명</td>
</tr>
<tr>
<td style="text-align: left;">biz_supt_trgt_info</td>
<td style="text-align: left;">지원 대상</td>
<td style="text-align: left;"></td>
<td style="text-align: center;">0</td>
<td style="text-align: left;">「1인 창조기업 육성에 관한 법률」제2조의 (예지) 1인 창조 기업</td>
<td style="text-align: left;">지원 대상</td>
</tr>
<tr>
<td style="text-align: left;">biz_supt_bdgt_info</td>
<td style="text-align: left;">지원예산 및 규모</td>
<td style="text-align: left;"></td>
<td style="text-align: center;">0</td>
<td style="text-align: left;">&gt;(예산현황) 51.1억원, (지원규모) (1인 창조기업 지원센터) 전국 총 47개, (사업화) 160개 내외</td>
<td style="text-align: left;">지원예산 및 규모</td>
</tr>
<tr>
<td style="text-align: left;">biz_supt_ctnt</td>
<td style="text-align: left;">지원 내용</td>
<td style="text-align: left;"></td>
<td style="text-align: center;">0</td>
<td style="text-align: left;">&gt;(지원센터) 입주공간, 전문가 자문, 교육, 멘토링, 네트워킹 등, (사업화) 마케팅 판로·투자 지원 등</td>
<td style="text-align: left;">지원 내용</td>
</tr>
<tr>
<td style="text-align: left;">supt_biz_chrct</td>
<td style="text-align: left;">지원 특징</td>
<td style="text-align: left;"></td>
<td style="text-align: center;">0</td>
<td style="text-align: left;">창의성과 전문성을 갖춘 1인 창조기업의 창업과 성장기반을 조성</td>
<td style="text-align: left;">지원 특징</td>
</tr>
<tr>
<td style="text-align: left;">supt_biz_intrd_info</td>
<td style="text-align: left;">사업 소개 정보</td>
<td style="text-align: left;"></td>
<td style="text-align: center;">0</td>
<td style="text-align: left;">1인 창조기업 창업을 촉진하고 성장기반을 조성하기 위해 사업공간(1인 창조기업 지원센터), 마케팅, 판로개척, 투자유치 등을 지원</td>
<td style="text-align: left;">사업 소개 정보</td>
</tr>
<tr>
<td style="text-align: left;">biz_yr</td>
<td style="text-align: left;">사업 연도</td>
<td style="text-align: left;">4</td>
<td style="text-align: center;">0</td>
<td style="text-align: left;">2023</td>
<td style="text-align: left;">사업 연도</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0)

c\) 응답 메시지 명세

| **항목명(영문)** | **항목명(국문)** | **항목크기** | **항목구분** | **샘플데이터** | **항목설명** |
|:---|:---|:---|:--:|:---|:---|
| biz_category_cd | 사업 구분 코드 | 50 | 1 | cmrczn_Tab3 | 사업 구분 코드 |
| supt_biz_titl_nm | 사업 명 | 300 | 1 | 1인 창조기업 활성화 지원사업 | 사업 명 |
| biz_supt_trgt_info | 지원 대상 |  | 1 | 「1인 창조기업 육성에 관한 법률」제2조의 (예지) 1인 창조 기업 | 지원 대상 |
| biz_supt_bdgt_info | 지원예산 및 규모 |  | 1 | \>(예산현황) 51.1억원, (지원규모) (1인 창조기업 지원센터) 전국 총 47개, (사업화) 160개 내외 | 지원예산 및 규모 |
| biz_supt_ctnt | 지원 내용 |  | 1 | \>(지원센터) 입주공간, 전문가 자문, 교육, 멘토링, 네트워킹 등, (사업화) 마케팅 판로·투자 지원 등 | 지원 내용 |
| supt_biz_chrct | 지원 특징 |  | 1 | 창의성과 전문성을 갖춘 1인 창조기업의 창업과 성장기반을 조성 | 지원 특징 |
| supt_biz_intrd_info | 사업 소개 정보 |  | 1 | 1인 창조기업 창업을 촉진하고 성장기반을 조성하기 위해 사업공간(1인 창조기업 지원센터), 마케팅, 판로개척, 투자유치 등을 지원 | 사업 소개 정보 |
| biz_yr | 사업 연도 | 4 | 1 | 2023 | 사업 연도 |
| Detl_pg_url | 상세페이지 url | 2000 | 1 | https://www.k-startup.go.kr/web/contents/bizpbanc-deadline.do?schM=view&pbancSn=166834 | 상세페이지 url |

※ 항목구분 : 필수(1), 옵션(0)

d\) 요청/응답 메시지 예제

<table style="width:100%;">
<colgroup>
<col style="width: 99%" />
</colgroup>
<thead>
<tr>
<th style="text-align: center;"><strong>요청메시지</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;">https://apis.data.go.kr/B552735/kisedKstartupService01/getBusinessInformation01?ServiceKey=인증키</td>
</tr>
<tr>
<td style="text-align: center;"><strong>응답메시지</strong></td>
</tr>
<tr>
<td style="text-align: left;"><p>&lt;items&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;biz_category_cd&gt;cmrczn_Tab3&lt;/biz_category_cd&gt;</p>
<p>&lt;supt_biz_titl_nm&gt;1인 창조기업 활성화 지원사업&lt;/supt_biz_titl_nm&gt;</p>
<p>&lt;biz_supt_trgt_info&gt;「1인 창조기업 육성에 관한 법률」제2조의 (예지) 1인 창조 기업&lt;/biz_supt_trgt_info&gt;</p>
<p>&lt;biz_supt_bdgt_info&gt;(예산현황) 51.1억원, (지원규모) (1인 창조기업 지원센터) 전국 총 47개, (사업화) 160개 내외&lt;/biz_supt_bdgt_info&gt;</p>
<p>&lt;biz_supt_ctnt&gt;(지원센터) 입주공간, 전문가 자문, 교육, 멘토링, 네트워킹 등, (사업화) 마케팅 판로·투자 지원 등&lt;/biz_supt_ctnt&gt;</p>
<p>&lt;supt_biz_chrct&gt;창의성과 전문성을 갖춘 1인 창조기업의 창업과 성장기반을 조성&lt;/supt_biz_chrct&gt;</p>
<p>&lt;supt_biz_intrd_info&gt;1인 창조기업 창업을 촉진하고 성장기반을 조성하기 위해 사업공간(1인 창조기업 지원센터), 마케팅, 판로개척, 투자유치 등을 지원&lt;/supt_biz_intrd_info&gt;</p>
<p>&lt;biz_yr&gt;2023&lt;/biz_yr&gt;</p>
<p>&lt;detl_pg_url&gt;https://www.k-startup.go.kr/web/contents/bizpbanc-deadline.do?schM=view&amp;pbancSn=166834&lt;/detl_pg_url&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;/items&gt;</p></td>
</tr>
</tbody>
</table>

<span id="_Toc149144031" class="anchor"></span>2) \[지원사업 공고 정보\] 상세기능명세

a\) 상세기능정보

<table>
<colgroup>
<col style="width: 25%" />
<col style="width: 25%" />
<col style="width: 25%" />
<col style="width: 25%" />
</colgroup>
<thead>
<tr>
<th style="text-align: center;"><strong>상세기능 번호</strong></th>
<th>2</th>
<th style="text-align: center;"><strong>상세기능 유형</strong></th>
<th>조회 (상세)</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: center;"><strong>상세기능명(국문)</strong></td>
<td colspan="3">지원사업 공고 정보</td>
</tr>
<tr>
<td style="text-align: center;"><strong>상세기능 설명</strong></td>
<td colspan="3">창업지원사업 공고명, 공고기간, 지원대상, 지원내용 지원방법 등 공고 정보</td>
</tr>
<tr>
<td style="text-align: center;"><p><strong>Call Back URL</strong></p>
<p><strong>(외부노출URL)</strong></p></td>
<td colspan="3">https://apis.data.go.kr/B552735/kisedKstartupService01/getAnnouncementInformation01</td>
</tr>
<tr>
<td style="text-align: center;"><strong>END POINT URL</strong></td>
<td colspan="3">https://nidapi.k-startup.go.kr/api/kisedKstartupService/v1/getAnnouncementInformation/</td>
</tr>
<tr>
<td style="text-align: center;"><strong>최대 메시지 사이즈</strong></td>
<td colspan="3">[4000] byte</td>
</tr>
<tr>
<td style="text-align: center;"><strong>평균 응답 시간</strong></td>
<td>[500] ms</td>
<td style="text-align: center;"><strong>초당 최대 트랙잭션</strong></td>
<td>[30] tps</td>
</tr>
</tbody>
</table>

b\) 요청 메시지 명세

<table>
<colgroup>
<col style="width: 16%" />
<col style="width: 16%" />
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 19%" />
<col style="width: 24%" />
</colgroup>
<thead>
<tr>
<th style="text-align: center;"><strong>항목명(영문)</strong></th>
<th style="text-align: center;"><strong>항목명(국문)</strong></th>
<th style="text-align: center;"><strong>항목크기</strong></th>
<th style="text-align: center;"><strong>항목구분</strong></th>
<th style="text-align: center;"><strong>샘플데이터</strong></th>
<th style="text-align: center;"><strong>항목설명</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;">ServiceKey</td>
<td style="text-align: left;">서비스키</td>
<td style="text-align: left;">100</td>
<td style="text-align: center;">1</td>
<td style="text-align: left;"><p>인증키</p>
<p>(URL Encode)</p></td>
<td style="text-align: left;">공공데이터포털에서 발급받은 인증키</td>
</tr>
<tr>
<td style="text-align: left;">page</td>
<td style="text-align: left;">페이지</td>
<td style="text-align: left;">100</td>
<td style="text-align: center;">0</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">페이지</td>
</tr>
<tr>
<td style="text-align: left;">perPage</td>
<td style="text-align: left;">한 페이지 결과 수</td>
<td style="text-align: left;">100</td>
<td style="text-align: center;">0</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td style="text-align: left;">returnType</td>
<td style="text-align: left;">반환타입</td>
<td style="text-align: left;">50</td>
<td style="text-align: center;">0</td>
<td style="text-align: left;">json</td>
<td style="text-align: left;">json/XML</td>
</tr>
<tr>
<td style="text-align: left;">intg_pbanc_yn</td>
<td style="text-align: left;">통합 공고 여부</td>
<td style="text-align: left;">300</td>
<td style="text-align: center;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">통합 공고 여부</td>
</tr>
<tr>
<td style="text-align: left;">intg_pbanc_biz_nm</td>
<td style="text-align: left;">통합 공고 사업 명</td>
<td style="text-align: left;">　</td>
<td style="text-align: center;">0</td>
<td style="text-align: left;"></td>
<td style="text-align: left;">통합 공고 사업 명</td>
</tr>
<tr>
<td style="text-align: left;">biz_pbanc_nm</td>
<td style="text-align: left;">지원 사업 공고 명</td>
<td style="text-align: left;">50</td>
<td style="text-align: center;">0</td>
<td style="text-align: left;">창업보육센터 입주기업 수출상담회</td>
<td style="text-align: left;">지원 사업 공고 명</td>
</tr>
<tr>
<td style="text-align: left;">supt_biz_clsfc</td>
<td style="text-align: left;">지원 분야</td>
<td style="text-align: left;">　</td>
<td style="text-align: center;">0</td>
<td style="text-align: left;">행사·네트워트</td>
<td style="text-align: left;">지원 분야</td>
</tr>
<tr>
<td style="text-align: left;">aply_trgt_ctnt</td>
<td style="text-align: left;">신청 대상 내용</td>
<td style="text-align: left;">200</td>
<td style="text-align: center;">0</td>
<td style="text-align: left;"></td>
<td style="text-align: left;">신청 대상 내용</td>
</tr>
<tr>
<td style="text-align: left;">supt_regin</td>
<td style="text-align: left;">지역명</td>
<td style="text-align: left;">　</td>
<td style="text-align: center;">0</td>
<td style="text-align: left;">서울특별시</td>
<td style="text-align: left;">지역명</td>
</tr>
<tr>
<td style="text-align: left;">pbanc_rcpt_bgng_dt</td>
<td style="text-align: left;">공고 접수 시작 일시</td>
<td style="text-align: left;">　</td>
<td style="text-align: center;">0</td>
<td style="text-align: left;">20121129</td>
<td style="text-align: left;">공고 접수 시작 일시</td>
</tr>
<tr>
<td style="text-align: left;">pbanc_rcpt_end_dt</td>
<td style="text-align: left;">공고 접수 종료 일시</td>
<td style="text-align: left;"></td>
<td style="text-align: center;">0</td>
<td style="text-align: left;">20121221</td>
<td style="text-align: left;">공고 접수 종료 일시</td>
</tr>
<tr>
<td style="text-align: left;">aply_trgt</td>
<td style="text-align: left;">신청 대상</td>
<td style="text-align: left;">200</td>
<td style="text-align: center;">0</td>
<td style="text-align: left;">청소년,대학생,일반인</td>
<td style="text-align: left;">신청 대상</td>
</tr>
<tr>
<td style="text-align: left;">biz_enyy</td>
<td style="text-align: left;">창업 기간</td>
<td style="text-align: left;">200</td>
<td style="text-align: center;">0</td>
<td style="text-align: left;">7년미만,5년미만,3년미만,2년미만,1년미만,예비창업자</td>
<td style="text-align: left;">창업 기간</td>
</tr>
<tr>
<td style="text-align: left;">biz_trgt_age</td>
<td style="text-align: left;">대상 연령</td>
<td style="text-align: left;">200</td>
<td style="text-align: center;">0</td>
<td style="text-align: left;">만 20세 미만, 만 20세 이상 ~ 만 39세 이하, 만 40세 이상</td>
<td style="text-align: left;">대상 연령</td>
</tr>
<tr>
<td style="text-align: left;">prfn_matr</td>
<td style="text-align: left;">우대 사항</td>
<td style="text-align: left;">200</td>
<td style="text-align: center;">0</td>
<td style="text-align: left;"></td>
<td style="text-align: left;">우대 사항</td>
</tr>
<tr>
<td style="text-align: left;">Rcrt_prgs_yn</td>
<td style="text-align: left;">모집진행여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: center;">0</td>
<td style="text-align: left;">Y</td>
<td style="text-align: left;">모집진행여부</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

c\) 응답 메시지 명세

| **항목명(영문)** | **항목명(국문)** | **항목크기** | **항목구분** | **샘플데이터** | **항목설명** |
|:---|:---|:---|:--:|:---|:---|
| intg_pbanc_yn | 통합 공고 여부 | 1 | 1 | N | 통합 공고 여부 |
| intg_pbanc_biz_nm | 통합 공고 사업 명 | 300 | 1 |  | 통합 공고 사업 명 |
| biz_pbanc_nm | 지원 사업 공고 명 | 300 | 1 | 창업보육센터 입주기업 수출상담회 | 지원 사업 공고 명 |
| pbanc_ctnt | 공고 내용 | 　 | 1 |  | 공고 내용 |
| supt_biz_clsfc | 지원 분야 | 50 | 1 | 행사·네트워트 | 지원 분야 |
| aply_trgt_ctnt | 신청 대상 내용 | 　 | 1 |  | 신청 대상 내용 |
| supt_regin | 지역명 | 200 | 1 | 서울특별시 | 지역명 |
| pbanc_rcpt_bgng_dt | 공고 접수 시작 일시 | 　 | 1 | 2012-11-29 00:00:00 | 공고 접수 시작 일시 |
| pbanc_rcpt_end_dt | 공고 접수 종료 일시 | 　 | 1 | 2012-12-01 00:00:00 | 공고 접수 종료 일시 |
| pbanc_ntrp_nm | 창업 지원 기관명 | 300 | 1 |  | 창업 지원 기관명 |
| sprv_inst | 주관 기관 | 25 | 1 | 공공기관 | 주관 기관 |
| biz_prch_dprt_nm | 사업 담당자 부서명 | 200 | 1 |  | 사업 담당자 부서명 |
| biz_gdnc_url | 사업 안내 URL | 2000 | 1 |  | 담당자 연락처 |
| prch_cnpl_no | 담당자 연락처 | 200 | 1 |  | 사업 안내 URL |
| detl_pg_url | 상세페이지URL | 500 | 1 | www.k-startup.go.kr/web/contents/web/contents/bizpbanc-ongoing.do?schM=view&pbancSn=14212 | 상세페이지URL |
| aply_mthd_vst_rcpt_istc | 신청 방법 방문 접수 설명 | 　 | 1 |  | 신청 방법 방문 접수 설명 |
| aply_mthd_pssr_rcpt_istc | 신청 방법 우편 접수 설명 | 　 | 1 |  | 신청 방법 우편 접수 설명 |
| aply_mthd_fax_rcpt_istc | 신청 방법 팩스 접수 설명 | 　 | 1 |  | 신청 방법 팩스 접수 설명 |
| aply_mthd_eml_rcpt_istc | 신청 방법 이메일 접수 설명 | 　 | 1 |  | 신청 방법 이메일 접수 설명 |
| aply_mthd_onli_rcpt_istc | 신청 방법 온라인 접수 설명 | 　 | 1 |  | 신청 방법 온라인 접수 설명 |
| aply_mthd_etc_istc | 신청 방법 기타 설명 | 　 | 1 |  | 신청 방법 기타 설명 |
| aply_exclt_trgt_ctnt | 신청제외대상내용 | 　 | 1 |  | 신청제외대상내용 |
| aply_trgt | 신청 대상 | 200 | 1 | 청소년,대학생,일반인 | 신청 대상 |
| biz_enyy | 창업 기간 | 200 | 1 | 7년미만,5년미만,3년미만,2년미만,1년미만,예비창업자 | 창업 기간 |
| biz_trgt_age | 대상 연령 | 200 | 1 | 만 20세 미만, 만 20세 이상 ~ 만 39세 이하, 만 40세 이상 | 대상 연령 |
| prfn_matr | 우대 사항 | 200 | 1 |  | 우대 사항 |
| Rcrt_prgs_yn | 모집진행여부 | 1 | 1 | Y | 모집진행여부 |
| pbanc_sn | 공고일련번호 | 32 | 1 | 1234 | 공고 일련번호 |

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

d\) 요청/응답 메시지 예제

<table style="width:100%;">
<colgroup>
<col style="width: 99%" />
</colgroup>
<thead>
<tr>
<th style="text-align: center;"><strong>요청메시지</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;">https://apis.data.go.kr/B552735/kisedKstartupService01/getAnnouncementInformation01?ServiceKey=인증키</td>
</tr>
<tr>
<td style="text-align: center;"><strong>응답메시지</strong></td>
</tr>
<tr>
<td style="text-align: left;"><p>&lt;items&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;intg_pbanc_yn&gt;N&lt;/intg_pbanc_yn&gt;</p>
<p>&lt;intg_pbanc_biz_nm&gt;&lt;/intg_pbanc_biz_nm&gt;</p>
<p>&lt;biz_pbanc_nm&gt;창업보육센터 입주기업 수출상담회&lt;/biz_pbanc_nm&gt;</p>
<p>&lt;pbanc_ctnt&gt;&lt;/pbanc_ctnt&gt;</p>
<p>&lt;supt_biz_clsfc&gt;행사·네트워트&lt;/supt_biz_clsfc&gt;</p>
<p>&lt;aply_trgt_ctnt&gt;&lt;/aply_trgt_ctnt&gt;</p>
<p>&lt;supt_regin&gt;서울특별시&lt;/supt_regin&gt;</p>
<p>&lt;pbanc_rcpt_bgng_dt&gt;2012-11-29 00:00:00&lt;/pbanc_rcpt_bgng_dt&gt;</p>
<p>&lt;pbanc_rcpt_end_dt&gt;2012-12-01 00:00:00&lt;/pbanc_rcpt_end_dt&gt;</p>
<p>&lt;pbanc_ntrp_nm&gt;&lt;/pbanc_ntrp_nm&gt;</p>
<p>&lt;sprv_inst&gt;공공기관&lt;/sprv_inst&gt;</p>
<p>&lt;biz_prch_dprt_nm&gt;&lt;/biz_prch_dprt_nm&gt;</p>
<p>&lt;biz_gdnc_url&gt;&lt;/biz_gdnc_url&gt;</p>
<p>&lt;biz_aply_url&gt;&lt;/biz_aply_url&gt;</p>
<p>&lt;prch_cnpl_no&gt;&lt;/prch_cnpl_no&gt;</p>
<p>&lt;detl_pg_url&gt;www.k-startup.go.kr/web/contents/web/contents/bizpbanc-ongoing.do?schM=view&amp;pbancSn=14212&lt;/detl_pg_url&gt;</p>
<p>&lt;aply_mthd_vst_rcpt_istc&gt;&lt;/aply_mthd_vst_rcpt_istc&gt;</p>
<p>&lt;aply_mthd_pssr_rcpt_istc&gt;&lt;/aply_mthd_pssr_rcpt_istc&gt;</p>
<p>&lt;aply_mthd_fax_rcpt_istc&gt;&lt;/aply_mthd_fax_rcpt_istc&gt;</p>
<p>&lt;aply_mthd_eml_rcpt_istc&gt;&lt;/aply_mthd_eml_rcpt_istc&gt;</p>
<p>&lt;aply_mthd_onli_rcpt_istc&gt;&lt;/aply_mthd_onli_rcpt_istc&gt;</p>
<p>&lt;aply_mthd_etc_istc&gt;&lt;/aply_mthd_etc_istc&gt;</p>
<p>&lt;aply_excl_trgt_ctnt&gt;&lt;/aply_excl_trgt_ctnt&gt;</p>
<p>&lt;aply_trgt&gt;청소년,대학생,일반인&lt;/aply_trgt&gt;</p>
<p>&lt;biz_enyy&gt;7년미만,5년미만,3년미만,2년미만,1년미만,예비창업자&lt;/biz_enyy&gt;</p>
<p>&lt;biz_trgt_age&gt;만 20세 미만, 만 20세 이상 ~ 만 39세 이하, 만 40세 이상&lt;/biz_trgt_age&gt;</p>
<p>&lt;prfn_matr&gt;&lt;/prfn_matr&gt;</p>
<p>&lt;rcrt_prgs_yn&gt;Y&lt;/rcrt_prgs_yn&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;/items&gt;</p></td>
</tr>
</tbody>
</table>

<span id="_Toc149144032" class="anchor"></span>3) \[창업관련 콘텐츠 정보\] 상세기능명세

a\) 상세기능정보

<table>
<colgroup>
<col style="width: 25%" />
<col style="width: 25%" />
<col style="width: 25%" />
<col style="width: 25%" />
</colgroup>
<thead>
<tr>
<th style="text-align: center;"><strong>상세기능 번호</strong></th>
<th>3</th>
<th style="text-align: center;"><strong>상세기능 유형</strong></th>
<th>조회 (상세)</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: center;"><strong>상세기능명(국문)</strong></td>
<td colspan="3">창업관련 콘텐츠 정보</td>
</tr>
<tr>
<td style="text-align: center;"><strong>상세기능 설명</strong></td>
<td colspan="3">정책·규제 정보, 생태계 이슈·동향, 창업우수사례 정보 등 콘텐츠 정보</td>
</tr>
<tr>
<td style="text-align: center;"><p><strong>Call Back URL</strong></p>
<p><strong>(외부노출URL)</strong></p></td>
<td colspan="3">https://apis.data.go.kr/B552735/kisedKstartupService01/getContentInformation01</td>
</tr>
<tr>
<td style="text-align: center;"><strong>END POINT URL</strong></td>
<td colspan="3">https://nidapi.k-startup.go.kr/api/kisedKstartupService/v1/getContentInformation/</td>
</tr>
<tr>
<td style="text-align: center;"><strong>최대 메시지 사이즈</strong></td>
<td colspan="3">[4000] byte</td>
</tr>
<tr>
<td style="text-align: center;"><strong>평균 응답 시간</strong></td>
<td>[500] ms</td>
<td style="text-align: center;"><strong>초당 최대 트랙잭션</strong></td>
<td>[30] tps</td>
</tr>
</tbody>
</table>

b\) 요청 메시지 명세

<table>
<colgroup>
<col style="width: 16%" />
<col style="width: 16%" />
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 19%" />
<col style="width: 24%" />
</colgroup>
<thead>
<tr>
<th style="text-align: center;"><strong>항목명(영문)</strong></th>
<th style="text-align: center;"><strong>항목명(국문)</strong></th>
<th style="text-align: center;"><strong>항목크기</strong></th>
<th style="text-align: center;"><strong>항목구분</strong></th>
<th style="text-align: center;"><strong>샘플데이터</strong></th>
<th style="text-align: center;"><strong>항목설명</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;">ServiceKey</td>
<td style="text-align: left;">서비스키</td>
<td style="text-align: left;">100</td>
<td style="text-align: center;">1</td>
<td style="text-align: left;"><p>인증키</p>
<p>(URL Encode)</p></td>
<td style="text-align: left;">공공데이터포털에서 발급받은 인증키</td>
</tr>
<tr>
<td style="text-align: left;">page</td>
<td style="text-align: left;">페이지</td>
<td style="text-align: left;">100</td>
<td style="text-align: center;">0</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">페이지</td>
</tr>
<tr>
<td style="text-align: left;">perPage</td>
<td style="text-align: left;">한 페이지 결과 수</td>
<td style="text-align: left;">100</td>
<td style="text-align: center;">0</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td style="text-align: left;">returnType</td>
<td style="text-align: left;">반환타입</td>
<td style="text-align: left;">50</td>
<td style="text-align: center;">0</td>
<td style="text-align: left;">json</td>
<td style="text-align: left;">json/XML</td>
</tr>
<tr>
<td style="text-align: left;">clss_cd</td>
<td style="text-align: left;">콘텐츠 구분 코드</td>
<td style="text-align: left;">50</td>
<td style="text-align: center;">0</td>
<td style="text-align: left;">notice_matr</td>
<td style="text-align: left;">콘텐츠 구분 코드</td>
</tr>
<tr>
<td style="text-align: left;">titl_nm</td>
<td style="text-align: left;">제목</td>
<td style="text-align: left;">300</td>
<td style="text-align: center;">0</td>
<td style="text-align: left;">2023년 창업에듀 영상 콘텐츠 공모전 선정결과 안내</td>
<td style="text-align: left;">제목</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

c\) 응답 메시지 명세

| **항목명(영문)** | **항목명(국문)** | **항목크기** | **항목구분** | **샘플데이터** | **항목설명** |
|:---|:---|:---|:--:|:---|:---|
| clss_cd | 콘텐츠 구분 코드 | 50 | 1 | notice_matr | 콘텐츠 구분 코드 |
| titl_nm | 제목 | 300 | 1 | 2023년 창업에듀 영상 콘텐츠 공모전 선정결과 안내 | 제목 |
| fstm_reg_dt | 등록 일시 | 　 | 1 | 2023-10-31 17:45:34 | 등록 일시 |
| view_cnt | 조회 수 | 7 | 1 | 38 | 조회 수 |
| detl_pg_url | 상세페이지 URL | 500 | 1 | www.k-startup.go.kr/web/contents/webNotice_MATR.do?id=160721&schM=view | 상세페이지 URL |
| file_nm | 파일 명 | 300 | 1 | 2023년 창업에듀 영상 콘텐츠 공모전 선정결과 안내.pdf | 파일 명 |

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

d\) 요청/응답 메시지 예제

<table style="width:100%;">
<colgroup>
<col style="width: 99%" />
</colgroup>
<thead>
<tr>
<th style="text-align: center;"><strong>요청메시지</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;">https://apis.data.go.kr/B552735/kisedKstartupService01/getContentInformation01?ServiceKey=인증키</td>
</tr>
<tr>
<td style="text-align: center;"><strong>응답메시지</strong></td>
</tr>
<tr>
<td style="text-align: left;"><p>&lt;items&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;clss_cd&gt;notice_matr&lt;/clss_cd&gt;</p>
<p>&lt;titl_nm&gt;2023년 창업에듀 영상 콘텐츠 공모전 선정결과 안내&lt;/titl_nm&gt;</p>
<p>&lt;fstm_reg_dt&gt;2023-10-31 17:45:34&lt;/fstm_reg_dt&gt;</p>
<p>&lt;view_cnt&gt;38&lt;/view_cnt&gt;</p>
<p>&lt;detl_pg_url&gt;www.k-startup.go.kr/web/contents/webNotice_MATR.do?id=160721&amp;schM=view&lt;/detl_pg_url&gt;</p>
<p>&lt;file_nm&gt;2023년 창업에듀 영상 콘텐츠 공모전 선정결과 안내.pdf&lt;/file_nm&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;/items&gt;</p></td>
</tr>
</tbody>
</table>

<span id="_Toc149144033" class="anchor"></span>4) \[창업관련 통계보고서 정보\] 상세기능명세

a\) 상세기능정보

<table>
<colgroup>
<col style="width: 25%" />
<col style="width: 25%" />
<col style="width: 25%" />
<col style="width: 25%" />
</colgroup>
<thead>
<tr>
<th style="text-align: center;"><strong>상세기능 번호</strong></th>
<th>4</th>
<th style="text-align: center;"><strong>상세기능 유형</strong></th>
<th>조회 (상세)</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: center;"><strong>상세기능명(국문)</strong></td>
<td colspan="3">창업관련 통계보고서 정보</td>
</tr>
<tr>
<td style="text-align: center;"><strong>상세기능 설명</strong></td>
<td colspan="3">창업기업 업력, 형태, 분야, 해외진출 여부 등 통계보고서 정보</td>
</tr>
<tr>
<td style="text-align: center;"><p><strong>Call Back URL</strong></p>
<p><strong>(외부노출URL)</strong></p></td>
<td colspan="3">https://apis.data.go.kr/B552735/kisedKstartupService01/getStatisticalInformation01</td>
</tr>
<tr>
<td style="text-align: center;"><strong>END POINT URL</strong></td>
<td colspan="3">https://nidapi.k-startup.go.kr/api/kisedKstartupService/v1/getStatisticalInformation/</td>
</tr>
<tr>
<td style="text-align: center;"><strong>최대 메시지 사이즈</strong></td>
<td colspan="3">[4000] byte</td>
</tr>
<tr>
<td style="text-align: center;"><strong>평균 응답 시간</strong></td>
<td>[500] ms</td>
<td style="text-align: center;"><strong>초당 최대 트랙잭션</strong></td>
<td>[30] tps</td>
</tr>
</tbody>
</table>

b\) 요청 메시지 명세

<table>
<colgroup>
<col style="width: 16%" />
<col style="width: 16%" />
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 19%" />
<col style="width: 24%" />
</colgroup>
<thead>
<tr>
<th style="text-align: center;"><strong>항목명(영문)</strong></th>
<th style="text-align: center;"><strong>항목명(국문)</strong></th>
<th style="text-align: center;"><strong>항목크기</strong></th>
<th style="text-align: center;"><strong>항목구분</strong></th>
<th style="text-align: center;"><strong>샘플데이터</strong></th>
<th style="text-align: center;"><strong>항목설명</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;">ServiceKey</td>
<td style="text-align: left;">서비스키</td>
<td style="text-align: left;">100</td>
<td style="text-align: center;">1</td>
<td style="text-align: left;"><p>인증키</p>
<p>(URL Encode)</p></td>
<td style="text-align: left;">공공데이터포털에서 발급받은 인증키</td>
</tr>
<tr>
<td style="text-align: left;">page</td>
<td style="text-align: left;">페이지</td>
<td style="text-align: left;">100</td>
<td style="text-align: center;">0</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">페이지</td>
</tr>
<tr>
<td style="text-align: left;">perPage</td>
<td style="text-align: left;">한 페이지 결과 수</td>
<td style="text-align: left;">100</td>
<td style="text-align: center;">0</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td style="text-align: left;">returnType</td>
<td style="text-align: left;">반환타입</td>
<td style="text-align: left;">50</td>
<td style="text-align: center;">0</td>
<td style="text-align: left;">json</td>
<td style="text-align: left;">json/XML</td>
</tr>
<tr>
<td style="text-align: left;">titl_nm</td>
<td style="text-align: left;">통계 자료 명</td>
<td style="text-align: left;">300</td>
<td style="text-align: center;">0</td>
<td style="text-align: left;">중소기업청 창업진흥원 창업기업 실태조사 보고서(2013)</td>
<td style="text-align: left;">통계 자료 명</td>
</tr>
<tr>
<td style="text-align: left;">file_nm</td>
<td style="text-align: left;">통계 자료 내용</td>
<td style="text-align: left;">1000</td>
<td style="text-align: center;">0</td>
<td style="text-align: left;">2023년 창업기업 실태조사&lt;p&gt;&lt;br&gt;&lt;/p&gt;&lt;p&gt;이 보고서는 중소기업청이 주관하고 창업진흥원이 수행하여 그 결과를 수록한 것입니다</td>
<td style="text-align: left;">통계 자료 내용</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

c\) 응답 메시지 명세

| **항목명(영문)** | **항목명(국문)** | **항목크기** | **항목구분** | **샘플데이터** | **항목설명** |
|:---|:---|:---|:--:|:---|:---|
| titl_nm | 통계 자료 명 | 300 | 1 | 중소기업청 창업진흥원 창업기업 실태조사 보고서(2013) | 통계 자료 명 |
| ctnt | 통계 자료 내용 | 　 | 1 | 2023년 창업기업 실태조사\<p\>\<br\>\</p\>\<p\>이 보고서는 중소기업청이 주관하고 창업진흥원이 수행하여 그 결과를 수록한 것입니다 | 통계 자료 내용 |
| fstm_reg_dt | 등록 일시 | 　 | 1 | 2016-05-24 09:22:58 | 등록 일시 |
| last_mdfcn_dt | 수정 일시 | 　 | 1 | 2022-04-04 14:18:41 | 수정 일시 |
| detl_pg_url | 상세페이지 URL | 500 | 1 | www.k-startup.go.kr/web/contents/webFND_STATS_RSCH_DATA.do?id=75403&schM=view | 상세페이지 URL |
| file_nm | 다운로드 파일 명 | 1000 | 1 | 2013년 창업기업 실태조사.pdf | 다운로드 파일 명 |

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

d\) 요청/응답 메시지 예제

<table style="width:100%;">
<colgroup>
<col style="width: 99%" />
</colgroup>
<thead>
<tr>
<th style="text-align: center;"><strong>요청메시지</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;">https://apis.data.go.kr/B552735/kisedKstartupService01/getStatisticalInformation01?ServiceKey=인증키</td>
</tr>
<tr>
<td style="text-align: center;"><strong>응답메시지</strong></td>
</tr>
<tr>
<td style="text-align: left;"><p>&lt;items&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;titl_nm&gt;중소기업청 창업진흥원 창업기업 실태조사 보고서(2013)&lt;/titl_nm&gt;</p>
<p>&lt;ctnt&gt;2023년 창업기업 실태조사&lt;p&gt;&lt;br&gt;&lt;/p&gt;&lt;p&gt;이 보고서는 중소기업청이 주관하고 창업진흥원이 수행하여 그 결과를 수록한 것입니다.&lt;/p&gt;&lt;/ctnt&gt;</p>
<p>&lt;fstm_reg_dt&gt;2016-05-24 09:22:58&lt;/fstm_reg_dt&gt;</p>
<p>&lt;last_mdfcn_dt&gt;2022-04-04 14:18:41&lt;/last_mdfcn_dt&gt;</p>
<p>&lt;detl_pg_url&gt;www.k-startup.go.kr/web/contents/webFND_STATS_RSCH_DATA.do?id=75403&amp;schM=view&lt;/detl_pg_url&gt;</p>
<p>&lt;file_nm&gt;2013년 창업기업 실태조사.pdf&lt;/file_nm&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;/items&gt;</p></td>
</tr>
</tbody>
</table>

<span id="_Toc149144034" class="anchor"></span>**2. OpenAPI 에러 코드정리**

| **에러코드** | **에러메시지** | **설명** |
|:--:|:---|:---|
| 1 | APPLICATION_ERROR | 어플리케이션 에러 |
| 10 | INVALID_REQUEST_PARAMETER_ERROR | 잘못된 요청 파라메터 에러 |
| 12 | NO_OPENAPI_SERVICE_ERROR | 해당 오픈API서비스가 없거나 폐기됨 |
| 20 | SERVICE_ACCESS_DENIED_ERROR | 서비스 접근거부 |
| 22 | LIMITED_NUMBER_OF_SERVICE_REQUESTS_EXCEEDS_ERROR | 서비스 요청제한횟수 초과에러 |
| 30 | SERVICE_KEY_IS_NOT_REGISTERED_ERROR | 등록되지 않은 서비스키 |
| 31 | DEADLINE_HAS_EXPIRED_ERROR | 기한만료된 서비스키 |
| 32 | UNREGISTERED_IP_ERROR | 등록되지 않은 IP |
| 99 | UNKNOWN_ERROR | 기타에러 |
