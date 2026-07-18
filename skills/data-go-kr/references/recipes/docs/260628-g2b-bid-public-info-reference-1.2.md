<!-- lint-skip: env-values (외부 공식문서 미러 - 원문 담당자 연락처 포함) -->
조달청 공공데이터 개방

OpenAPI 참고자료

**나라장터검색조건에 의한 입찰공고공사조회**

[1. 서비스 명세 [5](#_Toc466461848)](#_Toc466461848)

[1.1 나라장터 입찰공고정보서비스 [5](#나라장터-입찰공고정보서비스)](#나라장터-입찰공고정보서비스)

[가. 서비스 개요 [5](#서비스-개요)](#서비스-개요)

[나. 오퍼레이션 목록 [7](#오퍼레이션-목록)](#오퍼레이션-목록)

<span id="_Toc466461848" class="anchor"></span>**개정 이력**

<table style="width:97%;">
<colgroup>
<col style="width: 11%" />
<col style="width: 15%" />
<col style="width: 17%" />
<col style="width: 52%" />
</colgroup>
<tbody>
<tr>
<td>버 전</td>
<td>변경일</td>
<td>변경 구분</td>
<td>변경사유</td>
</tr>
<tr>
<td style="text-align: left;">1.0</td>
<td style="text-align: left;">2025. 1. 6.</td>
<td style="text-align: left;">제정</td>
<td style="text-align: left;">제정</td>
</tr>
<tr>
<td style="text-align: left;"></td>
<td style="text-align: left;"></td>
<td style="text-align: left;"></td>
<td style="text-align: left;"></td>
</tr>
<tr>
<td style="text-align: left;"></td>
<td style="text-align: left;"></td>
<td style="text-align: left;"></td>
<td><ul>
<li></li>
</ul></td>
</tr>
<tr>
<td style="text-align: left;"></td>
<td style="text-align: left;"></td>
<td style="text-align: left;"></td>
<td><ul>
<li></li>
</ul></td>
</tr>
<tr>
<td style="text-align: left;"></td>
<td style="text-align: left;"></td>
<td style="text-align: left;"></td>
<td><ul>
<li></li>
</ul></td>
</tr>
<tr>
<td style="text-align: left;"></td>
<td style="text-align: left;"></td>
<td style="text-align: left;"></td>
<td><ul>
<li></li>
</ul></td>
</tr>
</tbody>
</table>

**변경 사항**

<table style="width:97%;">
<colgroup>
<col style="width: 11%" />
<col style="width: 15%" />
<col style="width: 17%" />
<col style="width: 52%" />
</colgroup>
<tbody>
<tr>
<td>버 전</td>
<td>변경일</td>
<td>변경 사유</td>
<td>상세</td>
</tr>
<tr>
<td style="text-align: left;">1.0</td>
<td style="text-align: left;">2025. 1. 6.</td>
<td style="text-align: left;">제정</td>
<td style="text-align: left;">제정</td>
</tr>
<tr>
<td style="text-align: left;">1.0</td>
<td style="text-align: left;">2025. 1. 17.</td>
<td style="text-align: left;">일부 항목 데이터 크기 및 설명 변경</td>
<td style="text-align: left;"><p>[공통]</p>
<p>-업종코드(indstrytyCd) 크기 변경(100→4)</p>
<p>-낙찰방법코드(sucsfbidMthdCd) 크기 변경(10→9), 코드 형식 변경 (한글 1자리+숫자6자리)</p>
<p>-공동수급방식코드(cmmnSpldmdMethdCd) 크기 변경(1→15), ), 코드 형식 변경 (한글 1자리+숫자6자리)</p>
<p>[입찰공고목록 정보에 대한 평가대상 주력분야 조회]</p>
<p>-응답 메시지 낙찰자선정적용기준코드(BidwinrSlctnBssCd), 건설업역구분코드(CnstrtWkrarDivCd) 항목의 데이터 크기 변경(1→9), 코드 형식 변경 (한글 1자리+숫자6자리)</p></td>
</tr>
<tr>
<td>1.0</td>
<td style="text-align: left;">2025. 2. 7.</td>
<td style="text-align: left;">일부 항목 샘플데이터 및 설명 변경</td>
<td><p>[공통]</p>
<p>-공고종류명(ntceKindNm) 샘플데이터 및 설명 변경</p>
<p>-참가제한지역코드(prtcptLmtRgnCd) 항목 설명 변경</p>
<p>-참가제한지역명(prtcptLmtRgnNm) 항목 설명 변경</p>
<p>[입찰공고목록 정보에 대한 공사조회], [나라장터검색조건에 의한 입찰공고공사조회]</p>
<p>-적용기준내용(aplBssCntnts) 크기 변경 (30→500)</p></td>
</tr>
<tr>
<td style="text-align: left;">1.1</td>
<td style="text-align: left;">2025.09.28</td>
<td style="text-align: left;">항목추가</td>
<td style="text-align: left;"><blockquote>
<p>- 지방자치단체 입찰시 낙찰자 결정 기준 개정 관련 표준시장단가금액(smkpAmt),표준시장단가금액A적용여부(smkpAmtYn) 항목 추가</p>
</blockquote>
<p>대상오퍼레이션</p>
<p>* 입찰공고목록 정보에 대한 공사기초금액조회</p>
<p>* 입찰공고목록 정보에 대한 입찰가격산식A정보조회</p>
<blockquote>
<p>- 공공데이터 활용신청 기술능력평가비율(techAbltEvlRt), 입찰가격평가비율(bidPrceEvlRt) 항목추가</p>
</blockquote>
<p>* 입찰공고목록 정보에 대한 용역조회</p>
<p>* 입찰공고목록 정보에 대한 외자조회</p>
<p>* 입찰공고목록 정보에 대한 물품조회</p>
<p>* 나라장터검색조건에 의한 입찰공고용역조회</p>
<p>* 나라장터검색조건에 의한 입찰공고외자조회</p>
<p>* 나라장터검색조건에 의한 입찰공고물품조회</p></td>
</tr>
<tr>
<td style="text-align: left;">1.2</td>
<td style="text-align: left;">2026.04.10</td>
<td style="text-align: left;">항목추가</td>
<td style="text-align: left;"><blockquote>
<p>- 공공데이터 활용신청 낙찰방법적용기준 (sucsfbidMthdAppStd) 항목추가</p>
</blockquote>
<p>* 입찰공고목록 정보에 대한 용역조회</p>
<p>* 입찰공고목록 정보에 대한 외자조회</p>
<p>* 입찰공고목록 정보에 대한 물품조회</p>
<p>* 나라장터검색조건에 의한 입찰공고용역조회</p>
<p>* 나라장터검색조건에 의한 입찰공고외자조회</p>
<p>* 나라장터검색조건에 의한 입찰공고물품조회</p></td>
</tr>
<tr>
<td style="text-align: left;"></td>
<td style="text-align: left;"></td>
<td style="text-align: left;"></td>
<td><ul>
<li></li>
</ul></td>
</tr>
</tbody>
</table>

# 1. 서비스 명세

## 1.1 나라장터 입찰공고정보서비스

### 서비스 개요

<table style="width:100%;">
<colgroup>
<col style="width: 20%" />
<col style="width: 8%" />
<col style="width: 9%" />
<col style="width: 19%" />
<col style="width: 0%" />
<col style="width: 9%" />
<col style="width: 3%" />
<col style="width: 8%" />
<col style="width: 20%" />
</colgroup>
<tbody>
<tr>
<td rowspan="4">서비스 정보</td>
<td colspan="2">서비스 ID</td>
<td colspan="6">BidPublicInfoService</td>
</tr>
<tr>
<td colspan="2">서비스명(국문)</td>
<td colspan="6">나라장터 입찰공고정보서비스</td>
</tr>
<tr>
<td colspan="2">서비스명(영문)</td>
<td colspan="6">BidPublicInfoService</td>
</tr>
<tr>
<td colspan="2">서비스 설명</td>
<td colspan="6"><p>조달청의 나라장터에서 제공하는 물품, 용역, 공사, 외자 입찰공고목록, 입찰공고상세정보, 기초금액정보, 면허제한정보, 참가가능지역정보, 입찰공고 변경이력를 제공하며 나라장터 입찰공고 검색조건으로도 업무별 입찰공고 정보를 제공하는 나라장터 입찰공고정보서비스</p>
<p>. 조달청의 입찰공고 정보 또한 제공</p></td>
</tr>
<tr>
<td rowspan="3">서비스 보안</td>
<td colspan="2">서비스 인증/권한</td>
<td colspan="5"><p>[O] 서비스 Key[ ] 인증서 (GPKI)</p>
<p>[] Basic (ID/PW) [ ] 없음</p></td>
<td rowspan="2">[ ]WS-Security</td>
</tr>
<tr>
<td colspan="2">메시지 레벨 암호화</td>
<td colspan="5">[ ] 전자서명 [ ] 암호화 [O] 없음</td>
</tr>
<tr>
<td colspan="2">전송 레벨 암호화</td>
<td colspan="6">[ ] SSL [ O] 없음</td>
</tr>
<tr>
<td rowspan="2">적용 기술 수준</td>
<td colspan="2">인터페이스 표준</td>
<td colspan="6"><p>[ ] SOAP 1.2</p>
<p>(RPC-Encoded, Document Literal, Document Literal Wrapped)</p>
<p>[ O ] REST (GET)</p>
<p>[ ] RSS 1.0 [ ] RSS 2.0 [ ] Atom 1.0 [ ] 기타</p></td>
</tr>
<tr>
<td colspan="2">교환 데이터 표준</td>
<td colspan="6">[ O ] XML [ O ] JSON [ ] MIME [ ] MTOM</td>
</tr>
<tr>
<td rowspan="2">서비스 URL</td>
<td colspan="2">개발환경</td>
<td colspan="6">http://apis.data.go.kr/1230000/ad/BidPublicInfoService</td>
</tr>
<tr>
<td colspan="2">운영환경</td>
<td colspan="6">http://apis.data.go.kr/1230000/ad/BidPublicInfoService</td>
</tr>
<tr>
<td rowspan="2">서비스 WADL</td>
<td colspan="2">개발환경</td>
<td colspan="6">N/A</td>
</tr>
<tr>
<td colspan="2">운영환경</td>
<td colspan="6">N/A</td>
</tr>
<tr>
<td rowspan="3">서비스 배포 정보</td>
<td colspan="2">서비스 버전</td>
<td colspan="6">3.1</td>
</tr>
<tr>
<td colspan="2">서비스 시작일</td>
<td colspan="2">2025-01-06</td>
<td colspan="2">배포 일자</td>
<td colspan="2">2025-01-06</td>
</tr>
<tr>
<td colspan="2">서비스 이력</td>
<td colspan="6">N/A</td>
</tr>
<tr>
<td>메시지 교환 유형</td>
<td colspan="8"><p>[O] Request-Response [ ] Publish-Subscribe</p>
<p>[ ] Fire-and-Forgot [ ] Notification</p></td>
</tr>
<tr>
<td>메시지 로깅 수준</td>
<td>성공</td>
<td colspan="2">[O] Header [ ] Body</td>
<td colspan="2">실패</td>
<td colspan="3">[O] Header [O} Body</td>
</tr>
<tr>
<td>사용 제약 사항 (비고)</td>
<td colspan="8">N/A</td>
</tr>
<tr>
<td>서비스 제공자</td>
<td colspan="8">안정우 / 조달청 조달데이터관리팀 / 042-724-7685 / eureka3112@korea.kr</td>
</tr>
<tr>
<td>데이터 갱신주기</td>
<td colspan="8">수시</td>
</tr>
</tbody>
</table>

### 오퍼레이션 목록

<table>
<colgroup>
<col style="width: 10%" />
<col style="width: 16%" />
<col style="width: 31%" />
<col style="width: 31%" />
<col style="width: 9%" />
</colgroup>
<tbody>
<tr>
<td>일련번호</td>
<td>서비스명(국문)</td>
<td>오퍼레이션명(영문)</td>
<td>오퍼레이션명(국문)</td>
<td>메시지명(영문)</td>
</tr>
<tr>
<td>1</td>
<td rowspan="24" style="text-align: center;">나라장터 입찰공고정보서비스</td>
<td style="text-align: left;">getBidPblancListInfoCnstwk</td>
<td>입찰공고목록 정보에 대한 공사조회</td>
<td>N/A</td>
</tr>
<tr>
<td>2</td>
<td>getBidPblancListInfoServc</td>
<td>입찰공고목록 정보에 대한 용역조회</td>
<td>N/A</td>
</tr>
<tr>
<td>3</td>
<td>getBidPblancListInfoFrgcpt</td>
<td>입찰공고목록 정보에 대한 외자조회</td>
<td>N/A</td>
</tr>
<tr>
<td>4</td>
<td>getBidPblancListInfoThng</td>
<td>입찰공고목록 정보에 대한 물품조회</td>
<td>N/A</td>
</tr>
<tr>
<td>5</td>
<td>getBidPblancListInfoThngBsisAmount</td>
<td>입찰공고목록 정보에 대한 물품기초금액조회</td>
<td>N/A</td>
</tr>
<tr>
<td>6</td>
<td>getBidPblancListInfoCnstwkBsisAmount</td>
<td>입찰공고목록 정보에 대한 공사기초금액조회</td>
<td>N/A</td>
</tr>
<tr>
<td>7</td>
<td>getBidPblancListInfoServcBsisAmount</td>
<td>입찰공고목록 정보에 대한 용역기초금액조회</td>
<td>N/A</td>
</tr>
<tr>
<td>8</td>
<td>getBidPblancListInfoChgHstryThng</td>
<td>입찰공고목록 정보에 대한 물품변경이력조회</td>
<td>N/A</td>
</tr>
<tr>
<td>9</td>
<td>getBidPblancListInfoChgHstryCnstwk</td>
<td>입찰공고목록 정보에 대한 공사변경이력조회</td>
<td>N/A</td>
</tr>
<tr>
<td>10</td>
<td>getBidPblancListInfoChgHstryServc</td>
<td>입찰공고목록 정보에 대한 용역변경이력조회</td>
<td>N/A</td>
</tr>
<tr>
<td>11</td>
<td style="text-align: left;">getBidPblancListInfoCnstwkPPSSrch</td>
<td>나라장터검색조건에 의한 입찰공고공사조회</td>
<td>N/A</td>
</tr>
<tr>
<td>12</td>
<td>getBidPblancListInfoServcPPSSrch</td>
<td>나라장터검색조건에 의한 입찰공고용역조회</td>
<td>N/A</td>
</tr>
<tr>
<td>13</td>
<td>getBidPblancListInfoFrgcptPPSSrch</td>
<td>나라장터검색조건에 의한 입찰공고외자조회</td>
<td>N/A</td>
</tr>
<tr>
<td>14</td>
<td>getBidPblancListInfoThngPPSSrch</td>
<td>나라장터검색조건에 의한 입찰공고물품조회</td>
<td>N/A</td>
</tr>
<tr>
<td>15</td>
<td>getBidPblancListInfoLicenseLimit</td>
<td>입찰공고목록 정보에 대한 면허제한정보조회</td>
<td>N/A</td>
</tr>
<tr>
<td>16</td>
<td>getBidPblancListInfoPrtcptPsblRgn</td>
<td>입찰공고목록 정보에 대한 참가가능지역정보조회</td>
<td>N/A</td>
</tr>
<tr>
<td>17</td>
<td>getBidPblancListInfoThngPurchsObjPrdct</td>
<td>입찰공고목록 정보에 대한 물품 구매대상물품조회</td>
<td>N/A</td>
</tr>
<tr>
<td>18</td>
<td>getBidPblancListInfoServcPurchsObjPrdct</td>
<td>입찰공고목록 정보에 대한 용역 구매대상물품조회</td>
<td>N/A</td>
</tr>
<tr>
<td>19</td>
<td>getBidPblancListInfoFrgcptPurchsObjPrdct</td>
<td style="text-align: left;">입찰공고목록 정보에 대한 외자 구매대상물품조회</td>
<td>N/A</td>
</tr>
<tr>
<td>20</td>
<td>getBidPblancListInfoEorderAtchFileInfo</td>
<td style="text-align: left;">입찰공고목록 정보에 대한 e발주 첨부파일정보조회</td>
<td>N/A</td>
</tr>
<tr>
<td>21</td>
<td style="text-align: left;">getBidPblancListInfoEtc</td>
<td>입찰공고목록 정보에 대한 기타공고조회</td>
<td>N/A</td>
</tr>
<tr>
<td>22</td>
<td>getBidPblancListInfoEtcPPSSrch</td>
<td>나라장터검색조건에 의한 입찰공고기타조회</td>
<td>N/A</td>
</tr>
<tr>
<td>23</td>
<td>getBidPblancListPPIFnlRfpIssAtchFileInfo</td>
<td>입찰공고목록 정보에 대한 혁신장터 최종제안요청서 교부 첨부파일정보조회</td>
<td>N/A</td>
</tr>
<tr>
<td>24</td>
<td>getBidPblancListBidPrceCalclAInfo</td>
<td>입찰공고목록 정보에 대한 입찰가격산식A정보조회</td>
<td>N/A</td>
</tr>
<tr>
<td>25</td>
<td></td>
<td>getBidPblancListEvaluationIndstrytyMfrcInfo</td>
<td>입찰공고목록 정보에 대한 평가대상주력분야 조회</td>
<td>N/A</td>
</tr>
</tbody>
</table>

#### \
\[입찰공고목록 정보에 대한 공사조회\] 오퍼레이션 명세

<table>
<colgroup>
<col style="width: 4%" />
<col style="width: 21%" />
<col style="width: 17%" />
<col style="width: 21%" />
<col style="width: 2%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr>
<td rowspan="6">오퍼레이션 정보</td>
<td>오퍼레이션 번호</td>
<td>1</td>
<td>오퍼레이션명(국문)</td>
<td colspan="2">입찰공고목록 정보에 대한 공사조회</td>
</tr>
<tr>
<td>오퍼레이션 유형</td>
<td>조회(목록)</td>
<td>오퍼레이션명(영문)</td>
<td colspan="2">getBidPblancListInfoCnstwk</td>
</tr>
<tr>
<td>오퍼레이션 설명</td>
<td colspan="4">검색조건에 등록일시, 입찰공고번호, 변경일시를 입력하여 나라장터의 입찰공고번호, 공고명, 발주기관, 수요기관, 계약체결방법명 등 공사부분의 입찰공고정보를 조회함</td>
</tr>
<tr>
<td>Call Back URL</td>
<td colspan="4">N/A</td>
</tr>
<tr>
<td>최대 메시지 사이즈</td>
<td colspan="4">[ 4000bytes]</td>
</tr>
<tr>
<td>평균 응답 시간</td>
<td>[ 500 ms]</td>
<td colspan="2">초당 최대 트랜잭션</td>
<td>[ 30 tps]</td>
</tr>
</tbody>
</table>

##### 요청 메시지 명세

<table>
<colgroup>
<col style="width: 19%" />
<col style="width: 19%" />
<col style="width: 13%" />
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 21%" />
</colgroup>
<tbody>
<tr>
<td>항목명(영문)</td>
<td>항목명(국문)</td>
<td>항목크기</td>
<td>항목구분</td>
<td>샘플데이터</td>
<td>항목설명</td>
</tr>
<tr>
<td style="text-align: left;">numOfRows</td>
<td style="text-align: left;">한 페이지 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td style="text-align: left;">pageNo</td>
<td style="text-align: left;">페이지 번호</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">페이지 번호</td>
</tr>
<tr>
<td style="text-align: left;">ServiceKey</td>
<td style="text-align: left;">서비스키</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">공공데이터포탈에서 받은 인증키</td>
<td style="text-align: left;">공공데이터포탈에서 받은 인증키</td>
</tr>
<tr>
<td style="text-align: left;">type</td>
<td style="text-align: left;">타입</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">0</td>
<td>json</td>
<td>오픈API 리턴 타입을 JSON으로 받고 싶을 경우 'json' 으로 지정</td>
</tr>
<tr>
<td style="text-align: left;">inqryDiv</td>
<td style="text-align: left;">조회구분</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">검색하고자하는 조회구분<br />
1:등록일시 , 2.입찰공고번호 , 3.변경일시</td>
</tr>
<tr>
<td style="text-align: left;">inqryBgnDt</td>
<td style="text-align: left;">조회시작일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">202507010000</td>
<td style="text-align: left;">검색하고자하는 등록일시 또는 변경일시 조회시작일시 "YYYYMMDDHHMM"<br />
(조회구분 '1', '3' 선택시 필수)</td>
</tr>
<tr>
<td style="text-align: left;">inqryEndDt</td>
<td style="text-align: left;">조회종료일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">202507012359</td>
<td style="text-align: left;">검색하고자하는 등록일시 또는 변경일시 조회종료일시 "YYYYMMDDHHMM"<br />
(조회구분 '1', '3' 선택시 필수)</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNo</td>
<td style="text-align: left;">입찰공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25BK00932003</td>
<td style="text-align: left;">검색하고자 하는 입찰공고번호<br />
(조회구분 '2' 선택시 필수)</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 응답 메시지 명세

<table>
<colgroup>
<col style="width: 20%" />
<col style="width: 18%" />
<col style="width: 14%" />
<col style="width: 13%" />
<col style="width: 13%" />
<col style="width: 19%" />
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
<td style="text-align: left;">resultCode</td>
<td style="text-align: left;">결과코드</td>
<td style="text-align: left;">2</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">00</td>
<td style="text-align: left;">결과코드</td>
</tr>
<tr>
<td style="text-align: left;">resultMsg</td>
<td style="text-align: left;">결과메세지</td>
<td style="text-align: left;">50</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">정상</td>
<td style="text-align: left;">결과메세지</td>
</tr>
<tr>
<td style="text-align: left;">numOfRows</td>
<td style="text-align: left;">한 페이지 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td style="text-align: left;">pageNo</td>
<td style="text-align: left;">페이지 번호</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">페이지 번호</td>
</tr>
<tr>
<td style="text-align: left;">totalCount</td>
<td style="text-align: left;">전체 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">입찰공고 관리번입찰공고 관리번호이며 조달청나라장터 공고건의 형식은 년도(4)+월(2)+순번(5)이며 자체전자조달시스템 보유기관은 각 기관별 형식 별도 사용</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNo</td>
<td style="text-align: left;">입찰공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">R25BK00932003</td>
<td style="text-align: left;"><p>입찰공고 관리번입찰공고 관리번호이며 조달청나라장터 공고건의 형식은 년도(4)+월(2)+순번(5)이며 자체전자조달시스템 보유기관은 각 기관별 형식 별도 사용</p>
<p>*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성</p>
<p>-단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</p></td>
</tr>
<tr>
<td style="text-align: left;">bidNtceOrd</td>
<td style="text-align: left;">입찰공고차수</td>
<td style="text-align: left;">3</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">000</td>
<td style="text-align: left;">입찰공고차수는 해당 입찰공고에 대한 재공고 및 재입찰 등이 발생되었을 경우 증가되는 수</td>
</tr>
<tr>
<td style="text-align: left;">reNtceYn</td>
<td style="text-align: left;">재공고여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">본 입찰공고의 재공고 여부(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">rgstTyNm</td>
<td style="text-align: left;">등록유형명</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">조달청 또는 나라장터 자체 공고건</td>
<td style="text-align: left;">입찰공고가 "조달청 또는 나라장터 자체 공고건","'나라장터 기타 공고건"</td>
</tr>
<tr>
<td style="text-align: left;">ntceKindNm</td>
<td style="text-align: left;">공고종류명</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">등록공고</td>
<td style="text-align: left;">공고의 공고상태명으로 등록공고, 변경공고, 취소공고, 재공고 구분</td>
</tr>
<tr>
<td style="text-align: left;">intrbidYn</td>
<td style="text-align: left;">국제입찰여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">국제입찰대상인지의 여부를 나타내며 국제입찰 대상은 내외국인 또는 외국인을 대상으로 하여 물품, 공사 및 용역을 조달하기 위하여 행하는 입찰을 말하며 수의계약을 포함한다. 국가계약법 제4조에 의해 추정가격이 고시금액(국제입찰 적용 대상 기준금액으로 기획재정부장관 및 행정자치부장관이 매 2년마다 고시한 금액을 말하며 WTO 또는 양자간(FTA) 정부조달협정에 따르면 국제입찰 대상 기준 금액이 SDR(Special Drawing Rights:특별인출권) 통화단위로 되어 있어 주무부 장관이 이를 2년마다 원화로 환산하여 고시) 이상일 경우 국제입찰대상이 됨(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceDt</td>
<td style="text-align: left;">입찰공고일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-01 06:23:47</td>
<td style="text-align: left;">입찰공고서를 공고한 일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">refNo</td>
<td style="text-align: left;">참조번호</td>
<td style="text-align: left;">105</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">문성고등학교 공고 제2025-51호</td>
<td style="text-align: left;">조달청 입찰공고의 경우 참조공고번호는 자체 전자조달시스템에서 관리하는 공고번호를 의미하며 자체전자조달시스템의 경우 참조공고번호는 나라장터(G2B) 입찰공고번호를 의미함</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNm</td>
<td style="text-align: left;">입찰공고명</td>
<td style="text-align: left;">1000</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">문성고등학교 비탈면공사 수의계약 안내공고</td>
<td style="text-align: left;">공사명 또는 사업명이라고도 하며 입찰공고 내용을 요약한 이름</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttCd</td>
<td style="text-align: left;">공고기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">7380065</td>
<td style="text-align: left;">공고를 하는 기관의 코드로 행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드가 행자부코드가 없는 경우 조달청에서 부여한 공고기관 코드가 표기됨</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttNm</td>
<td style="text-align: left;">공고기관명</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">광주광역시교육청 문성고등학교</td>
<td style="text-align: left;">수요기관의 의뢰를 받아 공고하는 기관의 명</td>
</tr>
<tr>
<td style="text-align: left;">dminsttCd</td>
<td style="text-align: left;">수요기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">7380065</td>
<td style="text-align: left;">실제 수요기관의 코드로 행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드가 행자부코드가 없는 경우 조달청에서 부여한 수요기관 코드가 표기됨</td>
</tr>
<tr>
<td style="text-align: left;">dminsttNm</td>
<td style="text-align: left;">수요기관명</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">광주광역시교육청 문성고등학교</td>
<td style="text-align: left;">중앙조달인 경우 조달사업에 관한 법률 제2조(정의)에 따라 수요물자의 구매 공급 또는 시설공사 계약의 체결을 조달청장에게 요청할 수 있도록 조달청장이 인정하여 등록한 기관 또는 자체전자조달시스템을 이용하는 기관인 경우 계약을 의뢰한 기관의 명으로 공고기관과 수요기관이 동일할 수 있음</td>
</tr>
<tr>
<td style="text-align: left;">bidMethdNm</td>
<td style="text-align: left;">입찰방식명</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">전자입찰</td>
<td style="text-align: left;">공고의 입찰방식명 직찰<br />
전자입찰,전자입찰/직찰,전자/직찰/우편/상시,직찰/우편/상시,우편/상시,전자시담,복수견적(역경매),직찰/우편,전자시담(다자간)</td>
</tr>
<tr>
<td style="text-align: left;">cntrctCnclsMthdNm</td>
<td style="text-align: left;">계약체결방법명</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">전자입찰</td>
<td style="text-align: left;">계약체결의 방법을 구분하는 명<br />
*일반경쟁계약은 계약 대상 물품의 규격 및 시방서와 계약조건 등을 널리 공고하여 일정한 자격을 가진 불특정 다수인의 입찰희망자를 모두 경쟁 입찰하는 계약방법<br />
*제한경쟁계약은 일반·지명경쟁계약제도의 단점을 보완하기 위해 실적제한, 기술보유제한, 특정물품제한, 지역제한 등을 두는 계약방법<br />
*지명경쟁계약은 계약상대자의 신용과 실적 등에 있어 적당하다고 인정하는 특정 다수의 경쟁 참가자를 지명하여 계약 상대방을 결정하는 계약방법<br />
*수의계약은 계약상대자를 결정함에 있어 경쟁방법에 의하지 않고 특정인을 선정하여 계약하는 계약방법</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttOfclNm</td>
<td style="text-align: left;">공고기관담당자명</td>
<td style="text-align: left;">35</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">이건구</td>
<td style="text-align: left;">공고기관의 공고를 담당하는 담당자의 명</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttOfclTelNo</td>
<td style="text-align: left;">공고기관담당자전화번호</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">062-670-7502</td>
<td style="text-align: left;">공고기관의 공고를 담당하는 담당자의 전화번호</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttOfclEmailAdrs</td>
<td style="text-align: left;">공고기관담당자이메일주소</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">lkk7394@naver.com</td>
<td style="text-align: left;">공고기관의 공고를 담당하는 담당자의 이메일주소</td>
</tr>
<tr>
<td style="text-align: left;">exctvNm</td>
<td style="text-align: left;">집행관명</td>
<td style="text-align: left;">35</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">이건구</td>
<td style="text-align: left;">공고의 집행관명</td>
</tr>
<tr>
<td style="text-align: left;">bidQlfctRgstDt</td>
<td style="text-align: left;">입찰참가자격등록마감일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-07 18:00</td>
<td style="text-align: left;">입찰참가등록이란 입찰사무를 효과적으로 집행하기 위하여 사전에 입찰참가자격등록을 해두었다가 필요 시 입찰에 참여하는 제도로 해당 공고에 대한 입찰참가자격의 등록이 완료되어야 하는 시점을 의미함 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">cmmnSpldmdAgrmntRcptdocMethd</td>
<td style="text-align: left;">공동수급협정서접수방식</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">없음</td>
<td style="text-align: left;">공동수급협정서의 접수방식"전자","수기","없음","공고서참고"</td>
</tr>
<tr>
<td style="text-align: left;">cmmnSpldmdAgrmntClseDt</td>
<td style="text-align: left;">공동수급협정마감일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-09-24 17:00:00</td>
<td style="text-align: left;">공동계약이 허용된 공고에 대해 공동수급체를 구성하여 입찰에 참여하고자 할 경우 구성원이 일정 분담내용에 따라 나누어 공동으로 이행하는 약속을 한 공동수급협정서를 작성하여야 하며 이때 공동수급협정서의 등록(작성) 마감 시점을 의미함”YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">cmmnSpldmdCorpRgnLmtYn</td>
<td style="text-align: left;">공동수급업체지역제한여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">공동수급협정시 구성원의 지역제한을 적용할지 여부. 지역제한인경우 협정 구성업체가 참가제한지역에 포함되어야 함.(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">bidBeginDt</td>
<td style="text-align: left;">입찰개시일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-01 14:00:00</td>
<td style="text-align: left;">입찰서의 제출을 개시하는 일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">bidClseDt</td>
<td style="text-align: left;">입찰마감일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-08 10:00:00</td>
<td style="text-align: left;">입찰서의 제출을 마감하는 일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">opengDt</td>
<td style="text-align: left;">개찰일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-08 11:00:00</td>
<td style="text-align: left;">집행관이 개찰을 수행할 수 있는 시작일시이며<br />
개찰일시 이후에 개찰이 가능함<br />
실제 개찰을 수행한 시간을 의미하지 않음 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl1</td>
<td style="text-align: left;">공고규격서URL1</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00932003&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=1&amp;prcmBsneSeCd=07</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl2</td>
<td style="text-align: left;">공고규격서URL2</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00932003&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=2&amp;prcmBsneSeCd=07</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl3</td>
<td style="text-align: left;">공고규격서URL3</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00932003&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=3&amp;prcmBsneSeCd=07</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl4</td>
<td style="text-align: left;">공고규격서URL4</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00932003&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=4&amp;prcmBsneSeCd=07</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl5</td>
<td style="text-align: left;">공고규격서URL5</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00932003&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=5&amp;prcmBsneSeCd=07</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl6</td>
<td style="text-align: left;">공고규격서URL6</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00932003&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=6&amp;prcmBsneSeCd=07</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl7</td>
<td style="text-align: left;">공고규격서URL7</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00932003&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=7&amp;prcmBsneSeCd=07</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl8</td>
<td style="text-align: left;">공고규격서URL8</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00932003&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=8&amp;prcmBsneSeCd=07</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl9</td>
<td style="text-align: left;">공고규격서URL9</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00932003&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=9&amp;prcmBsneSeCd=07</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl10</td>
<td style="text-align: left;">공고규격서URL10</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00932003&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=10&amp;prcmBsneSeCd=07</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm1</td>
<td style="text-align: left;">공고규격파일명1</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">문성고등학교비탈면공사수의계약안내공고.hwp</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm2</td>
<td style="text-align: left;">공고규격파일명2</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">공내역서(비탈면공사).xlsx</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm3</td>
<td style="text-align: left;">공고규격파일명3</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">20160430911-02_1462145881670_3. 설계설명서.hwp</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm4</td>
<td style="text-align: left;">공고규격파일명4</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">20160430911-02_1462145881672_4. 공내역서.xlsx</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm5</td>
<td style="text-align: left;">공고규격파일명5</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">20160530911-02_1462145881663_1. (변경)공고문.hwp</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm6</td>
<td style="text-align: left;">공고규격파일명6</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">20160530911-02_1462145881668_2. 시방서.hwp</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm7</td>
<td style="text-align: left;">공고규격파일명7</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">20160530911-02_1462145881670_3. 설계설명서.hwp</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm8</td>
<td style="text-align: left;">공고규격파일명8</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">20160530911-02_1462145881672_4. 공내역서.xlsx</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm9</td>
<td style="text-align: left;">공고규격파일명9</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">20120901436-01_공고2002-18호.hwp</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm10</td>
<td style="text-align: left;">공고규격파일명10</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">20120901436-01_공고2002-18호.hwp</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">rbidPermsnYn</td>
<td style="text-align: left;">재입찰허용여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">Y</td>
<td style="text-align: left;">입찰이 유찰되는 경우 재공고 없이 다시 입찰(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">pqApplDocRcptMthdNm</td>
<td style="text-align: left;">PQ신청서접수방법명</td>
<td style="text-align: left;">30</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">없음</td>
<td style="text-align: left;">PQ대상공고에서 PQ심사신청서를 어떻게 받을지에 대한 코드명</td>
</tr>
<tr>
<td style="text-align: left;">pqApplDocRcptDt</td>
<td style="text-align: left;">PQ신청서접수일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-09-18 10:00:00</td>
<td style="text-align: left;">PQ심사신청서 접수 마감일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">arsltApplDocRcptMthdNm</td>
<td style="text-align: left;">실적신청서접수방법명</td>
<td style="text-align: left;">50</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">없음</td>
<td style="text-align: left;">공고의 실적신청서접수방법명</td>
</tr>
<tr>
<td style="text-align: left;">arsltApplDocRcptDt</td>
<td style="text-align: left;">실적신청서접수일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-09-18 10:00:00</td>
<td style="text-align: left;">실적심사신청서 접수마감일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">jntcontrctDutyRgnNm1</td>
<td style="text-align: left;">공동도급의무지역명1</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">서울특별시</td>
<td style="text-align: left;">공고의 공동도급의무지역명</td>
</tr>
<tr>
<td style="text-align: left;">jntcontrctDutyRgnNm2</td>
<td style="text-align: left;">공동도급의무지역명2</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">서울특별시</td>
<td style="text-align: left;">공고의 공동도급의무지역명</td>
</tr>
<tr>
<td style="text-align: left;">jntcontrctDutyRgnNm3</td>
<td style="text-align: left;">공동도급의무지역명3</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">서울특별시</td>
<td style="text-align: left;">공고의 공동도급의무지역명</td>
</tr>
<tr>
<td style="text-align: left;">rgnDutyJntcontrctRt</td>
<td style="text-align: left;">지역의무공동도급비율</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">지역의무공동동급시 3개지역의 공동도급합산 하한 비율(%)</td>
</tr>
<tr>
<td style="text-align: left;">dtlsBidYn</td>
<td style="text-align: left;">내역입찰여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">내역입찰인지는 나타내는 항목으로 내역입찰일 경우 투찰시 내역서를 첨부해야함(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">bidPrtcptLmtYn</td>
<td style="text-align: left;">입찰참가제한여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">공고의 입찰참가제한여부(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">prearngPrceDcsnMthdNm</td>
<td style="text-align: left;">예정가격결정방법명</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">복수예가</td>
<td style="text-align: left;">예정가격의 결정을 위해 복수예정가격방식으로 산정하는지 단일 예정가격으로 산정하는지를 구분하는 명</td>
</tr>
<tr>
<td style="text-align: left;">totPrdprcNum</td>
<td style="text-align: left;">총예가건수</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">15</td>
<td style="text-align: left;">공고의 총예가건수</td>
</tr>
<tr>
<td style="text-align: left;">drwtPrdprcNum</td>
<td style="text-align: left;">추첨예가건수</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">공고의 추첨예가건수</td>
</tr>
<tr>
<td style="text-align: left;">bdgtAmt</td>
<td style="text-align: left;">예산금액</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">55330000</td>
<td style="text-align: left;">공고의 예산금액(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">presmptPrce</td>
<td style="text-align: left;">추정가격</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">55330000</td>
<td style="text-align: left;">물품/공사/용역 등의 조달 계약을 체결함에 있어 국제입찰 대상여부를 판단하는 기준 등으로 삼기 위하여 예정가격이 결정되기 전에 예산에 계상된 금액 등을 기준으로 하여 부가가치세 및 조달 수수료를 제외한 금액(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">govsplyAmt</td>
<td style="text-align: left;">관급금액</td>
<td style="text-align: left;">21</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">공고의 관급금액(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">aplBssCntnts</td>
<td style="text-align: left;">적용기준내용</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">행자부</td>
<td style="text-align: left;">공고의 적용기준내용</td>
</tr>
<tr>
<td style="text-align: left;">indstrytyEvlRt</td>
<td style="text-align: left;">업종평가비율</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">69.79</td>
<td style="text-align: left;">적격심사에서 사용하는 업종평가비율(%)</td>
</tr>
<tr>
<td style="text-align: left;">mainCnsttyNm</td>
<td style="text-align: left;">주공종명</td>
<td style="text-align: left;">300</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">상.하수도설비공사업</td>
<td style="text-align: left;">공고의 주공종명</td>
</tr>
<tr>
<td style="text-align: left;">mainCnsttyCnstwkPrearngAmt</td>
<td style="text-align: left;">주공종공사예정금액</td>
<td style="text-align: left;">21</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">681790000</td>
<td style="text-align: left;">적격심사시 주공종추정금액(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">incntvRgnNm1</td>
<td style="text-align: left;">가산지역명1</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">경상남도</td>
<td style="text-align: left;">적격심사를 실시할 경우 해당 지역 업체의 경우 가산점을 얻을 수 있는 지역명</td>
</tr>
<tr>
<td style="text-align: left;">incntvRgnNm2</td>
<td style="text-align: left;">가산지역명2</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">경기도</td>
<td style="text-align: left;">적격심사를 실시할 경우 해당 지역 업체의 경우 가산점을 얻을 수 있는 지역명</td>
</tr>
<tr>
<td style="text-align: left;">incntvRgnNm3</td>
<td style="text-align: left;">가산지역명3</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">서울특별시</td>
<td style="text-align: left;">적격심사를 실시할 경우 해당 지역 업체의 경우 가산점을 얻을 수 있는 지역명</td>
</tr>
<tr>
<td style="text-align: left;">incntvRgnNm4</td>
<td style="text-align: left;">가산지역명4</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">서울특별시</td>
<td style="text-align: left;">적격심사를 실시할 경우 해당 지역 업체의 경우 가산점을 얻을 수 있는 지역명</td>
</tr>
<tr>
<td style="text-align: left;">opengPlce</td>
<td style="text-align: left;">개찰장소</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">국가종합전자조달시스템(나라장터)</td>
<td style="text-align: left;">집행관이 개찰을 하는 장소</td>
</tr>
<tr>
<td style="text-align: left;">dcmtgOprtnDt</td>
<td style="text-align: left;">설명회실시일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-09-13 09:00:00</td>
<td style="text-align: left;">해당 공고에 대한 현장/입찰/과업 설명회를 실시하는 일시”YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">dcmtgOprtnPlce</td>
<td style="text-align: left;">설명회실시장소</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">우리청 관리과</td>
<td style="text-align: left;">해당 공고에 대한 설명회를 실시하는 경우 현장/입찰/과업 설명회를 실시하는 장소</td>
</tr>
<tr>
<td style="text-align: left;">contrctrcnstrtnGovsplyMtrlAmt</td>
<td style="text-align: left;">도급자설치관급자재금액</td>
<td style="text-align: left;">21</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">공고의 도급자설치관급자재금액(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">govcnstrtnGovsplyMtrlAmt</td>
<td style="text-align: left;">관급자설치관급자재금액</td>
<td style="text-align: left;">21</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">128822000</td>
<td style="text-align: left;">공고의 관급자설치관급자재금액(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceDtlUrl</td>
<td style="text-align: left;">입찰공고상세URL</td>
<td style="text-align: left;">512</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/link/PNPE027_01/single/?bidPbancNo=R25BK00932003&amp;bidPbancOrd=000</td>
<td style="text-align: left;">나라장터시스템의 입찰공고 상세화면 링크</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceUrl</td>
<td style="text-align: left;">입찰공고URL</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/link/PNPE027_01/single/?bidPbancNo=R25BK00932003&amp;bidPbancOrd=000</td>
<td style="text-align: left;">해당 입찰공고를 인터넷상에서 확인할 수 있는 URL주소</td>
</tr>
<tr>
<td style="text-align: left;">bidPrtcptFeePaymntYn</td>
<td style="text-align: left;">입찰참가수수료납부여부</td>
<td style="text-align: left;">30</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">전자납부</td>
<td style="text-align: left;">입찰참가 의사가 있는 자가 납부하여야하는 수수료의 유무 및 납부방법을 표기하는 것으로 "전자납부, 수기 및 전자납부, 수기, 없음"으로 표기</td>
</tr>
<tr>
<td style="text-align: left;">bidPrtcptFee</td>
<td style="text-align: left;">입찰참가수수료</td>
<td style="text-align: left;">21</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">10000</td>
<td style="text-align: left;">입찰에 참가하기위해 납부하는 수수료(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">bidGrntymnyPaymntYn</td>
<td style="text-align: left;">입찰보증금납부여부</td>
<td style="text-align: left;">30</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">불허</td>
<td style="text-align: left;">입찰보증금을 나라장터에서 전자로 납부가능하게 할지 여부 “전자납부허용”,”불허’으로 표기</td>
</tr>
<tr>
<td style="text-align: left;">crdtrNm</td>
<td style="text-align: left;">채권자명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">문성고등학교장</td>
<td style="text-align: left;">입찰보증금 항목의 "보증채권자명"으로 전자입찰보증 접수시 사용</td>
</tr>
<tr>
<td style="text-align: left;">cmmnSpldmdCnum</td>
<td style="text-align: left;">공동수급업체수</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">공고서에 의함</td>
<td style="text-align: left;">공고의 공동수급업체수</td>
</tr>
<tr>
<td style="text-align: left;">untyNtceNo</td>
<td style="text-align: left;">통합공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25BM00300431</td>
<td style="text-align: left;">입찰공고를 구분하는 번호로 입찰공고번호이며 형식은 년도(4)+월(2)+순번(5)<br />
*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성<br />
- 단계구분: BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격), BK(통합입찰)</td>
</tr>
<tr>
<td style="text-align: left;">sptDscrptDocUrl1</td>
<td style="text-align: left;">현장설명서URL1</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00932003&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=1&amp;prcmBsneSeCd=07</td>
<td style="text-align: left;">공고의 현장설명서URL</td>
</tr>
<tr>
<td style="text-align: left;">sptDscrptDocUrl2</td>
<td style="text-align: left;">현장설명서URL2</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00932003&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=2&amp;prcmBsneSeCd=07</td>
<td style="text-align: left;">공고의 현장설명서URL</td>
</tr>
<tr>
<td style="text-align: left;">sptDscrptDocUrl3</td>
<td style="text-align: left;">현장설명서URL3</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00932003&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=3&amp;prcmBsneSeCd=07</td>
<td style="text-align: left;">공고의 현장설명서URL</td>
</tr>
<tr>
<td style="text-align: left;">sptDscrptDocUrl4</td>
<td style="text-align: left;">현장설명서URL4</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00932003&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=4&amp;prcmBsneSeCd=07</td>
<td style="text-align: left;">공고의 현장설명서URL</td>
</tr>
<tr>
<td style="text-align: left;">sptDscrptDocUrl5</td>
<td style="text-align: left;">현장설명서URL5</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00932003&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=5&amp;prcmBsneSeCd=07</td>
<td style="text-align: left;">공고의 현장설명서URL</td>
</tr>
<tr>
<td style="text-align: left;">subsiCnsttyNm1</td>
<td style="text-align: left;">부대공종명1</td>
<td style="text-align: left;">300</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">토목공사업</td>
<td style="text-align: left;">공고의 부대공종명</td>
</tr>
<tr>
<td style="text-align: left;">subsiCnsttyNm2</td>
<td style="text-align: left;">부대공종명2</td>
<td style="text-align: left;">300</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">건축공사업</td>
<td style="text-align: left;">공고의 부대공종명</td>
</tr>
<tr>
<td style="text-align: left;">subsiCnsttyNm3</td>
<td style="text-align: left;">부대공종명3</td>
<td style="text-align: left;">300</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">기계설비공사업</td>
<td style="text-align: left;">공고의 부대공종명</td>
</tr>
<tr>
<td style="text-align: left;">subsiCnsttyNm4</td>
<td style="text-align: left;">부대공종명4</td>
<td style="text-align: left;">300</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">상.하수도설비공사업</td>
<td style="text-align: left;">공고의 부대공종명</td>
</tr>
<tr>
<td style="text-align: left;">subsiCnsttyNm5</td>
<td style="text-align: left;">부대공종명5</td>
<td style="text-align: left;">300</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">조경식재공사업</td>
<td style="text-align: left;">공고의 부대공종명</td>
</tr>
<tr>
<td style="text-align: left;">subsiCnsttyNm6</td>
<td style="text-align: left;">부대공종명6</td>
<td style="text-align: left;">300</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">시설물유지관리업</td>
<td style="text-align: left;">공고의 부대공종명</td>
</tr>
<tr>
<td style="text-align: left;">subsiCnsttyNm7</td>
<td style="text-align: left;">부대공종명7</td>
<td style="text-align: left;">300</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">일반소방시설공사업(기계)</td>
<td style="text-align: left;">공고의 부대공종명</td>
</tr>
<tr>
<td style="text-align: left;">subsiCnsttyNm8</td>
<td style="text-align: left;">부대공종명8</td>
<td style="text-align: left;">300</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">일반소방시설공사업(전기)</td>
<td style="text-align: left;">공고의 부대공종명</td>
</tr>
<tr>
<td style="text-align: left;">subsiCnsttyNm9</td>
<td style="text-align: left;">부대공종명9</td>
<td style="text-align: left;">300</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">산업.환경설비공사업</td>
<td style="text-align: left;">공고의 부대공종명</td>
</tr>
<tr>
<td style="text-align: left;">subsiCnsttyIndstrytyEvlRt1</td>
<td style="text-align: left;">부공종업종평가비율1</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">33</td>
<td style="text-align: left;">공고의 부공종업종평가비율(%)</td>
</tr>
<tr>
<td style="text-align: left;">subsiCnsttyIndstrytyEvlRt2</td>
<td style="text-align: left;">부공종업종평가비율2</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">37.51</td>
<td style="text-align: left;">공고의 부공종업종평가비율(%)</td>
</tr>
<tr>
<td style="text-align: left;">subsiCnsttyIndstrytyEvlRt3</td>
<td style="text-align: left;">부공종업종평가비율3</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">32.75</td>
<td style="text-align: left;">공고의 부공종업종평가비율(%)</td>
</tr>
<tr>
<td style="text-align: left;">subsiCnsttyIndstrytyEvlRt4</td>
<td style="text-align: left;">부공종업종평가비율4</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">39.7</td>
<td style="text-align: left;">공고의 부공종업종평가비율(%)</td>
</tr>
<tr>
<td style="text-align: left;">subsiCnsttyIndstrytyEvlRt5</td>
<td style="text-align: left;">부공종업종평가비율5</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">30</td>
<td style="text-align: left;">공고의 부공종업종평가비율(%)</td>
</tr>
<tr>
<td style="text-align: left;">subsiCnsttyIndstrytyEvlRt6</td>
<td style="text-align: left;">부공종업종평가비율6</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">24.94</td>
<td style="text-align: left;">공고의 부공종업종평가비율(%)</td>
</tr>
<tr>
<td style="text-align: left;">subsiCnsttyIndstrytyEvlRt7</td>
<td style="text-align: left;">부공종업종평가비율7</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">33</td>
<td style="text-align: left;">공고의 부공종업종평가비율(%)</td>
</tr>
<tr>
<td style="text-align: left;">subsiCnsttyIndstrytyEvlRt8</td>
<td style="text-align: left;">부공종업종평가비율8</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">27</td>
<td style="text-align: left;">공고의 부공종업종평가비율(%)</td>
</tr>
<tr>
<td style="text-align: left;">subsiCnsttyIndstrytyEvlRt9</td>
<td style="text-align: left;">부공종업종평가비율9</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">32</td>
<td style="text-align: left;">공고의 부공종업종평가비율(%)</td>
</tr>
<tr>
<td style="text-align: left;">cmmnSpldmdMethdCd</td>
<td style="text-align: left;">공동수급방식코드</td>
<td style="text-align: left;">15</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">공500004</td>
<td style="text-align: left;">공동수급이라 함은 구성원을 2인 이상으로 하여 수급인이 해당계약을 공동으로 수행하기 위하여 잠정적으로 결성한 실체를 의미하며 공동수급체가도급을 받아 이행하는 방식을 구분하는 코드로<br />
공500001 : 공동이행<br />
공500002 : 분담이행<br />
공500003 : 주계약자관리방식<br />
공500004 : 단독계약<br />
공500005 : 혼합방식<br />
공500006 : 공동이행 또는 분담이행<br />
공500007 : 혼합_단독<br />
공500008 : 혼합_공동<br />
공500012 : 해당없음으로 구분됨</td>
</tr>
<tr>
<td style="text-align: left;">cmmnSpldmdMethdNm</td>
<td style="text-align: left;">공동수급방식명</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">공동수급불허</td>
<td style="text-align: left;">공동수급이라 함은 구성원을 2인 이상으로 하여 수급인이 해당계약을 공동으로 수행하기 위하여 잠정적으로 결성한 실체를 의미하며 공동수급체가도급을 받아 이행하는 방식을 구분하는 명임</td>
</tr>
<tr>
<td style="text-align: left;">stdNtceDocUrl</td>
<td style="text-align: left;">표준공고서URL</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00932003&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=1&amp;prcmBsneSeCd=07</td>
<td style="text-align: left;">공고의 표준공고문URL</td>
</tr>
<tr>
<td style="text-align: left;">brffcBidprcPermsnYn</td>
<td style="text-align: left;">지사투찰허용여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">지역제한 공고에 한해서 지사 투찰을 허용할지 여부. 투찰제어시 사용(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">cnsttyAccotShreRateList</td>
<td style="text-align: left;">공종별지분율목록</td>
<td style="text-align: left;">4000</td>
<td style="text-align: left;">0..n</td>
<td style="text-align: left;">[전기공사업^100],</td>
<td style="text-align: left;">공고의 공종별지분율 목록<br />
[부업종코드명^부업종평가비율(%)],[부업종코드명^부업종평가비율(%)]</td>
</tr>
<tr>
<td style="text-align: left;">cnstrtnAbltyEvlAmtList</td>
<td style="text-align: left;">시공능력평가금액목록</td>
<td style="text-align: left;">4000</td>
<td style="text-align: left;">0..n</td>
<td style="text-align: left;">[1^토목공사업^0001^7400000000],</td>
<td style="text-align: left;">공고의 시공능력평가금액목록 [제한그룹번호^면허지역통합코드명^면허지역통합코드^시공능력평가금액],[제한그룹번호^면허지역통합코드명^면허지역통합코드^시공능력평가금액]</td>
</tr>
<tr>
<td style="text-align: left;">dsgntCmptYn</td>
<td style="text-align: left;">지명경쟁여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">공고의 지명경쟁여부(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">arsltCmptYn</td>
<td style="text-align: left;">실적경쟁여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">공고의 실적경쟁여부(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">pqEvalYn</td>
<td style="text-align: left;">PQ심사여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">공고의 PQ심사여부(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">ntceDscrptYn</td>
<td style="text-align: left;">공고설명여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">공고의 공고설명여부(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">rsrvtnPrceReMkngMthdNm</td>
<td style="text-align: left;">예비가격재작성방법명</td>
<td style="text-align: left;">50</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">재입찰시 기존 예비가격을 사용하여 예정가격이 산정됩니다.</td>
<td style="text-align: left;">공고의 예비가격재작성방법명</td>
</tr>
<tr>
<td style="text-align: left;">mainCnsttyPresmptPrce</td>
<td style="text-align: left;">주공종추정가격</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">5000</td>
<td style="text-align: left;">주공종에 대한 추정가격(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">orderPlanUntyNo</td>
<td style="text-align: left;">발주계획통합번호</td>
<td style="text-align: left;">35</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25DD20312897</td>
<td style="text-align: left;">*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성<br />
- 단계구분: BK(입찰)<br />
TA(계약)<br />
DD:(발주계획)<br />
BD(사전규격),<br />
BK(통합입찰)</td>
</tr>
<tr>
<td style="text-align: left;">sucsfbidLwltRate</td>
<td style="text-align: left;">낙찰하한율</td>
<td style="text-align: left;">22</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">89.745</td>
<td style="text-align: left;">개찰시 사용하는 낙찰하한율(%)</td>
</tr>
<tr>
<td style="text-align: left;">rgstDt</td>
<td style="text-align: left;">등록일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">2025-07-01 06:23:47</td>
<td style="text-align: left;">공고의 등록일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">bfSpecRgstNo</td>
<td style="text-align: left;">사전규격등록번호</td>
<td style="text-align: left;">17</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25BD00085140</td>
<td style="text-align: left;"><p>*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성</p>
<p>- 단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</p></td>
</tr>
<tr>
<td style="text-align: left;">sucsfbidMthdCd</td>
<td style="text-align: left;">낙찰방법코드</td>
<td style="text-align: left;">9</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">낙030022</td>
<td style="text-align: left;">낙찰방법명에 대한 코드 (한글 1자리 + 숫자 6자리)</td>
</tr>
<tr>
<td style="text-align: left;">sucsfbidMthdNm</td>
<td style="text-align: left;">낙찰방법명</td>
<td style="text-align: left;">700</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">소액수의견적(2인 이상 견적 제출)-국민연금보험료 등 합산액 감액 적용</td>
<td style="text-align: left;">낙찰자를 결정하는 방법-낙찰방법 세부기준</td>
</tr>
<tr>
<td style="text-align: left;">chgDt</td>
<td style="text-align: left;">변경일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-03 06:23:47</td>
<td style="text-align: left;">공고의 변경일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">dminsttOfclEmailAdrs</td>
<td style="text-align: left;">수요기관담당자이메일주소</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">nskk22@kywa.or.kr</td>
<td style="text-align: left;">수요기관 담당자의 이메일주소</td>
</tr>
<tr>
<td style="text-align: left;">indstrytyLmtYn</td>
<td style="text-align: left;">업종제한여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">Y</td>
<td style="text-align: left;">해당 공고 입찰 시 업종(면허)제한을 두는지의 여부<br />
예시)Y</td>
</tr>
<tr>
<td style="text-align: left;">cnstrtsiteRgnNm</td>
<td style="text-align: left;">공사현장지역명</td>
<td style="text-align: left;">256</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">광주광역시 남구</td>
<td style="text-align: left;"><p>공사현장의 지역명</p>
<p>나라장터 화면에서 “공사현장”</p></td>
</tr>
<tr>
<td style="text-align: left;">rgnDutyJntcontrctYn</td>
<td style="text-align: left;">지역의무공동도급여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">지역업체 참여가 일정 지분율 이상일 경우에만 입창이 가능한 공고 여부 ( Y:해당 N:공고서에의함)</td>
</tr>
<tr>
<td style="text-align: left;">chgNtceRsn</td>
<td style="text-align: left;">변경공고사유</td>
<td style="text-align: left;">4000</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">지역제한(강원도)으로 변경</td>
<td style="text-align: left;"><p>공고종류명(공고의 공고상태명) 이 변경일 경우 변경공고사유 , 취소일 경우 취소공고사유</p>
<p>(연계공고건는 제외)</p></td>
</tr>
<tr>
<td style="text-align: left;">rbidOpengDt</td>
<td style="text-align: left;">재입찰개찰일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-08 11:00:00</td>
<td style="text-align: left;">공고종류명이 ‘재입찰’ 일 경우 재입찰공고의 개찰을 수행할 수 있는 시작일시<br />
“YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">ciblAplYn</td>
<td style="text-align: left;">건설산업법적용대상여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">Y</td>
<td style="text-align: left;">건설산업기본법 적용 대상인지에 대한 여부</td>
</tr>
<tr>
<td style="text-align: left;">mtltyAdvcPsblYn</td>
<td style="text-align: left;">상호시장진출허용여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">건설업역(종합공사,전문공사)에 상호 진출 가능한지에 대한 여부</td>
</tr>
<tr>
<td style="text-align: left;">mtltyAdvcPsblYnCnstwkNm</td>
<td style="text-align: left;">건설산업법적용대상공사명</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">전문공사-유지보수공사</td>
<td style="text-align: left;">건설산업법 적용대상 공사명</td>
</tr>
<tr>
<td style="text-align: left;">VAT</td>
<td style="text-align: left;">부가가치세</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">5030000</td>
<td style="text-align: left;">부가가치세</td>
</tr>
<tr>
<td style="text-align: left;">indutyVAT</td>
<td style="text-align: left;">주공종부가가치세</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">주공종부가가치세</td>
</tr>
<tr>
<td style="text-align: left;">indstrytyMfrcFldEvlYn</td>
<td style="text-align: left;">주력분야평가여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">업종 주력분야 평가 대상 여부</td>
</tr>
<tr>
<td style="text-align: left;">bidWgrnteeRcptClseDt</td>
<td style="text-align: left;">입찰보증서접수마감일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-09-18 10:00:00</td>
<td style="text-align: left;">입찰보증서접수마감일시</td>
</tr>
<tr>
<td style="text-align: left;">rgnLmtBidLocplcJdgmBssCd</td>
<td style="text-align: left;">지역제한입찰소재지판단기준코드</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">지역제한입찰소재지판단기준코드</td>
</tr>
<tr>
<td style="text-align: left;">rgnLmtBidLocplcJdgmBssNm</td>
<td style="text-align: left;">지역제한입찰소재지판단기준명</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">본사또는참여지사소재지</td>
<td style="text-align: left;">지역제한입찰소재지판단기준명</td>
</tr>
<tr>
<td style="text-align: left;">sucsfbidMthdAppStd</td>
<td style="text-align: left;">낙찰방법적용기준</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">조달청 시설공사 적격심사세부기준</td>
<td style="text-align: left;"><p>낙찰자를 결정하</p>
<p>방법 적용기준</p></td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 요청 / 응답 메시지 예제

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr>
<td style="text-align: center;"><strong>REST(URI)</strong></td>
</tr>
<tr>
<td style="text-align: left;">http://apis.data.go.kr/1230000//ad/BidPublicInfoService/getBidPblancListInfoCnstwk?inqryDiv=2&amp;pageNo=1&amp;serviceKey=&amp;numOfRows=10bidNtceNo=R25BK00932003&amp;ServiceKey=인증키</td>
</tr>
<tr>
<td style="text-align: center;"><strong>응답 메시지</strong></td>
</tr>
<tr>
<td style="text-align: center;"><p>&lt;response&gt;</p>
<p>    &lt;header&gt;</p>
<p>        &lt;resultCode&gt;00&lt;/resultCode&gt;</p>
<p>        &lt;resultMsg&gt;정상&lt;/resultMsg&gt;</p>
<p>    &lt;/header&gt;</p>
<p>    &lt;body&gt;</p>
<p>        &lt;items&gt;</p>
<p>            &lt;item&gt;</p>
<p>                &lt;bidNtceNo&gt;R25BK00932003&lt;/bidNtceNo&gt;</p>
<p>                &lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>                &lt;reNtceYn&gt;N&lt;/reNtceYn&gt;</p>
<p>                &lt;rgstTyNm&gt;조달청 또는 나라장터 자체 공고건&lt;/rgstTyNm&gt;</p>
<p>                &lt;ntceKindNm&gt;등록공고&lt;/ntceKindNm&gt;</p>
<p>                &lt;intrbidYn&gt;N&lt;/intrbidYn&gt;</p>
<p>                &lt;bidNtceDt&gt;2025-07-01 06:23:47&lt;/bidNtceDt&gt;</p>
<p>                &lt;refNo&gt;문성고등학교 공고 제2025-51호&lt;/refNo&gt;</p>
<p>                &lt;bidNtceNm&gt;문성고등학교 비탈면공사 수의계약 안내공고&lt;/bidNtceNm&gt;</p>
<p>                &lt;ntceInsttCd&gt;7380065&lt;/ntceInsttCd&gt;</p>
<p>                &lt;ntceInsttNm&gt;광주광역시교육청 문성고등학교&lt;/ntceInsttNm&gt;</p>
<p>                &lt;dminsttCd&gt;7380065&lt;/dminsttCd&gt;</p>
<p>                &lt;dminsttNm&gt;광주광역시교육청 문성고등학교&lt;/dminsttNm&gt;</p>
<p>                &lt;bidMethdNm&gt;전자입찰&lt;/bidMethdNm&gt;</p>
<p>                &lt;cntrctCnclsMthdNm&gt;수의계약&lt;/cntrctCnclsMthdNm&gt;</p>
<p>                &lt;ntceInsttOfclNm&gt;이건구&lt;/ntceInsttOfclNm&gt;</p>
<p>                &lt;ntceInsttOfclTelNo&gt;062-670-7502&lt;/ntceInsttOfclTelNo&gt;</p>
<p>                &lt;ntceInsttOfclEmailAdrs&gt;lkk7394@naver.com&lt;/ntceInsttOfclEmailAdrs&gt;</p>
<p>                &lt;exctvNm&gt;이건구&lt;/exctvNm&gt;</p>
<p>                &lt;bidQlfctRgstDt&gt;2025-07-07 18:00&lt;/bidQlfctRgstDt&gt;</p>
<p>                &lt;cmmnSpldmdAgrmntRcptdocMethd&gt;없음&lt;/cmmnSpldmdAgrmntRcptdocMethd&gt;</p>
<p>                &lt;cmmnSpldmdAgrmntClseDt&gt;&lt;/cmmnSpldmdAgrmntClseDt&gt;</p>
<p>                &lt;cmmnSpldmdCorpRgnLmtYn&gt;&lt;/cmmnSpldmdCorpRgnLmtYn&gt;</p>
<p>                &lt;bidBeginDt&gt;2025-07-01 14:00:00&lt;/bidBeginDt&gt;</p>
<p>                &lt;bidClseDt&gt;2025-07-08 10:00:00&lt;/bidClseDt&gt;</p>
<p>                &lt;opengDt&gt;2025-07-08 11:00:00&lt;/opengDt&gt;</p>
<p>                &lt;ntceSpecDocUrl1&gt;https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00932003&amp;amp;bidPbancOrd=000&amp;amp;fileType=&amp;amp;fileSeq=1&amp;prcmBsneSeCd=07&lt;/ntceSpecDocUrl1&gt;</p>
<p>                &lt;ntceSpecDocUrl2&gt;https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00932003&amp;amp;bidPbancOrd=000&amp;amp;fileType=&amp;amp;fileSeq=2&amp;prcmBsneSeCd=07&lt;/ntceSpecDocUrl2&gt;</p>
<p>                &lt;ntceSpecDocUrl3&gt;&lt;/ntceSpecDocUrl3&gt;</p>
<p>                &lt;ntceSpecDocUrl4&gt;&lt;/ntceSpecDocUrl4&gt;</p>
<p>                &lt;ntceSpecDocUrl5&gt;&lt;/ntceSpecDocUrl5&gt;</p>
<p>                &lt;ntceSpecDocUrl6&gt;&lt;/ntceSpecDocUrl6&gt;</p>
<p>                &lt;ntceSpecDocUrl7&gt;&lt;/ntceSpecDocUrl7&gt;</p>
<p>                &lt;ntceSpecDocUrl8&gt;&lt;/ntceSpecDocUrl8&gt;</p>
<p>                &lt;ntceSpecDocUrl9&gt;&lt;/ntceSpecDocUrl9&gt;</p>
<p>                &lt;ntceSpecDocUrl10&gt;&lt;/ntceSpecDocUrl10&gt;</p>
<p>                &lt;ntceSpecFileNm1&gt;문성고등학교비탈면공사수의계약안내공고.hwp&lt;/ntceSpecFileNm1&gt;</p>
<p>                &lt;ntceSpecFileNm2&gt;공내역서(비탈면공사).xlsx&lt;/ntceSpecFileNm2&gt;</p>
<p>                &lt;ntceSpecFileNm3&gt;&lt;/ntceSpecFileNm3&gt;</p>
<p>                &lt;ntceSpecFileNm4&gt;&lt;/ntceSpecFileNm4&gt;</p>
<p>                &lt;ntceSpecFileNm5&gt;&lt;/ntceSpecFileNm5&gt;</p>
<p>                &lt;ntceSpecFileNm6&gt;&lt;/ntceSpecFileNm6&gt;</p>
<p>                &lt;ntceSpecFileNm7&gt;&lt;/ntceSpecFileNm7&gt;</p>
<p>                &lt;ntceSpecFileNm8&gt;&lt;/ntceSpecFileNm8&gt;</p>
<p>                &lt;ntceSpecFileNm9&gt;&lt;/ntceSpecFileNm9&gt;</p>
<p>                &lt;ntceSpecFileNm10&gt;&lt;/ntceSpecFileNm10&gt;</p>
<p>                &lt;rbidPermsnYn&gt;Y&lt;/rbidPermsnYn&gt;</p>
<p>                &lt;pqApplDocRcptMthdNm&gt;&lt;/pqApplDocRcptMthdNm&gt;</p>
<p>                &lt;pqApplDocRcptDt&gt;&lt;/pqApplDocRcptDt&gt;</p>
<p>                &lt;arsltApplDocRcptMthdNm&gt;&lt;/arsltApplDocRcptMthdNm&gt;</p>
<p>                &lt;arsltApplDocRcptDt&gt;&lt;/arsltApplDocRcptDt&gt;</p>
<p>                &lt;jntcontrctDutyRgnNm1&gt;&lt;/jntcontrctDutyRgnNm1&gt;</p>
<p>                &lt;jntcontrctDutyRgnNm2&gt;&lt;/jntcontrctDutyRgnNm2&gt;</p>
<p>                &lt;jntcontrctDutyRgnNm3&gt;&lt;/jntcontrctDutyRgnNm3&gt;</p>
<p>                &lt;rgnDutyJntcontrctRt&gt;&lt;/rgnDutyJntcontrctRt&gt;</p>
<p>                &lt;dtlsBidYn&gt;N&lt;/dtlsBidYn&gt;</p>
<p>                &lt;bidPrtcptLmtYn&gt;N&lt;/bidPrtcptLmtYn&gt;</p>
<p>                &lt;prearngPrceDcsnMthdNm&gt;복수예가&lt;/prearngPrceDcsnMthdNm&gt;</p>
<p>                &lt;totPrdprcNum&gt;15&lt;/totPrdprcNum&gt;</p>
<p>                &lt;drwtPrdprcNum&gt;4&lt;/drwtPrdprcNum&gt;</p>
<p>                &lt;bdgtAmt&gt;55330000&lt;/bdgtAmt&gt;</p>
<p>                &lt;presmptPrce&gt;50300000&lt;/presmptPrce&gt;</p>
<p>                &lt;govsplyAmt&gt;0&lt;/govsplyAmt&gt;</p>
<p>                &lt;aplBssCntnts&gt;행자부&lt;/aplBssCntnts&gt;</p>
<p>                &lt;indstrytyEvlRt&gt;&lt;/indstrytyEvlRt&gt;</p>
<p>                &lt;mainCnsttyNm&gt;&lt;/mainCnsttyNm&gt;</p>
<p>                &lt;mainCnsttyCnstwkPrearngAmt&gt;&lt;/mainCnsttyCnstwkPrearngAmt&gt;</p>
<p>                &lt;incntvRgnNm1&gt;&lt;/incntvRgnNm1&gt;</p>
<p>                &lt;incntvRgnNm2&gt;&lt;/incntvRgnNm2&gt;</p>
<p>                &lt;incntvRgnNm3&gt;&lt;/incntvRgnNm3&gt;</p>
<p>                &lt;incntvRgnNm4&gt;&lt;/incntvRgnNm4&gt;</p>
<p>                &lt;opengPlce&gt;국가종합전자조달시스템(나라장터)&lt;/opengPlce&gt;</p>
<p>                &lt;dcmtgOprtnDt&gt;&lt;/dcmtgOprtnDt&gt;</p>
<p>                &lt;dcmtgOprtnPlce&gt;&lt;/dcmtgOprtnPlce&gt;</p>
<p>                &lt;contrctrcnstrtnGovsplyMtrlAmt&gt;0&lt;/contrctrcnstrtnGovsplyMtrlAmt&gt;</p>
<p>                &lt;govcnstrtnGovsplyMtrlAmt&gt;0&lt;/govcnstrtnGovsplyMtrlAmt&gt;</p>
<p>                &lt;bidNtceDtlUrl&gt;https://www.g2b.go.kr/link/PNPE027_01/single/?bidPbancNo=R25BK00932003&amp;bidPbancOrd=000&lt;/bidNtceDtlUrl&gt;</p>
<p>                &lt;bidNtceUrl&gt;https://www.g2b.go.kr/link/PNPE027_01/single/?bidPbancNo=R25BK00932003&amp;bidPbancOrd=000&lt;/bidNtceUrl&gt;</p>
<p>                &lt;bidPrtcptFeePaymntYn&gt;&lt;/bidPrtcptFeePaymntYn&gt;</p>
<p>                &lt;bidPrtcptFee&gt;&lt;/bidPrtcptFee&gt;</p>
<p>                &lt;bidGrntymnyPaymntYn&gt;&lt;/bidGrntymnyPaymntYn&gt;</p>
<p>                &lt;crdtrNm&gt;문성고등학교장&lt;/crdtrNm&gt;</p>
<p>                &lt;cmmnSpldmdCnum&gt;공고서에 의함&lt;/cmmnSpldmdCnum&gt;</p>
<p>                &lt;untyNtceNo&gt;R25BM00300431&lt;/untyNtceNo&gt;</p>
<p>                &lt;sptDscrptDocUrl1&gt;&lt;/sptDscrptDocUrl1&gt;</p>
<p>                &lt;sptDscrptDocUrl2&gt;&lt;/sptDscrptDocUrl2&gt;</p>
<p>                &lt;sptDscrptDocUrl3&gt;&lt;/sptDscrptDocUrl3&gt;</p>
<p>                &lt;sptDscrptDocUrl4&gt;&lt;/sptDscrptDocUrl4&gt;</p>
<p>                &lt;sptDscrptDocUrl5&gt;&lt;/sptDscrptDocUrl5&gt;</p>
<p>                &lt;subsiCnsttyNm1&gt;&lt;/subsiCnsttyNm1&gt;</p>
<p>                &lt;subsiCnsttyNm2&gt;&lt;/subsiCnsttyNm2&gt;</p>
<p>                &lt;subsiCnsttyNm3&gt;&lt;/subsiCnsttyNm3&gt;</p>
<p>                &lt;subsiCnsttyNm4&gt;&lt;/subsiCnsttyNm4&gt;</p>
<p>                &lt;subsiCnsttyNm5&gt;&lt;/subsiCnsttyNm5&gt;</p>
<p>                &lt;subsiCnsttyNm6&gt;&lt;/subsiCnsttyNm6&gt;</p>
<p>                &lt;subsiCnsttyNm7&gt;&lt;/subsiCnsttyNm7&gt;</p>
<p>                &lt;subsiCnsttyNm8&gt;&lt;/subsiCnsttyNm8&gt;</p>
<p>                &lt;subsiCnsttyNm9&gt;&lt;/subsiCnsttyNm9&gt;</p>
<p>                &lt;subsiCnsttyIndstrytyEvlRt1&gt;&lt;/subsiCnsttyIndstrytyEvlRt1&gt;</p>
<p>                &lt;subsiCnsttyIndstrytyEvlRt2&gt;&lt;/subsiCnsttyIndstrytyEvlRt2&gt;</p>
<p>                &lt;subsiCnsttyIndstrytyEvlRt3&gt;&lt;/subsiCnsttyIndstrytyEvlRt3&gt;</p>
<p>                &lt;subsiCnsttyIndstrytyEvlRt4&gt;&lt;/subsiCnsttyIndstrytyEvlRt4&gt;</p>
<p>                &lt;subsiCnsttyIndstrytyEvlRt5&gt;&lt;/subsiCnsttyIndstrytyEvlRt5&gt;</p>
<p>                &lt;subsiCnsttyIndstrytyEvlRt6&gt;&lt;/subsiCnsttyIndstrytyEvlRt6&gt;</p>
<p>                &lt;subsiCnsttyIndstrytyEvlRt7&gt;&lt;/subsiCnsttyIndstrytyEvlRt7&gt;</p>
<p>                &lt;subsiCnsttyIndstrytyEvlRt8&gt;&lt;/subsiCnsttyIndstrytyEvlRt8&gt;</p>
<p>                &lt;subsiCnsttyIndstrytyEvlRt9&gt;&lt;/subsiCnsttyIndstrytyEvlRt9&gt;</p>
<p>                &lt;cmmnSpldmdMethdCd&gt;&lt;/cmmnSpldmdMethdCd&gt;</p>
<p>                &lt;cmmnSpldmdMethdNm&gt;(없음)공동수급불허&lt;/cmmnSpldmdMethdNm&gt;</p>
<p>                &lt;stdNtceDocUrl&gt;https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00932003&amp;amp;bidPbancOrd=000&amp;amp;fileType=&amp;amp;fileSeq=1&amp;prcmBsneSeCd=07&lt;/stdNtceDocUrl&gt;</p>
<p>                &lt;brffcBidprcPermsnYn&gt;&lt;/brffcBidprcPermsnYn&gt;</p>
<p>                &lt;cnsttyAccotShreRateList&gt;&lt;/cnsttyAccotShreRateList&gt;</p>
<p>                &lt;cnstrtnAbltyEvlAmtList&gt;&lt;/cnstrtnAbltyEvlAmtList&gt;</p>
<p>                &lt;dsgntCmptYn&gt;N&lt;/dsgntCmptYn&gt;</p>
<p>                &lt;arsltCmptYn&gt;N&lt;/arsltCmptYn&gt;</p>
<p>                &lt;pqEvalYn&gt;&lt;/pqEvalYn&gt;</p>
<p>                &lt;ntceDscrptYn&gt;&lt;/ntceDscrptYn&gt;</p>
<p>                &lt;rsrvtnPrceReMkngMthdNm&gt;재입찰시 예비가격을 다시 생성하여 예정가격이 산정됩니다.&lt;/rsrvtnPrceReMkngMthdNm&gt;</p>
<p>                &lt;mainCnsttyPresmptPrce&gt;&lt;/mainCnsttyPresmptPrce&gt;</p>
<p>                &lt;orderPlanUntyNo&gt;&lt;/orderPlanUntyNo&gt;</p>
<p>                &lt;sucsfbidLwltRate&gt;89.745&lt;/sucsfbidLwltRate&gt;</p>
<p>                &lt;rgstDt&gt;2025-07-01 06:23:47&lt;/rgstDt&gt;</p>
<p>                &lt;bfSpecRgstNo&gt;&lt;/bfSpecRgstNo&gt;</p>
<p>                &lt;sucsfbidMthdCd&gt;낙030029&lt;/sucsfbidMthdCd&gt;</p>
<p>                &lt;sucsfbidMthdNm&gt;소액수의견적(2인 이상 견적 제출)-국민연금보험료 등 합산액 감액 적용&lt;/sucsfbidMthdNm&gt;</p>
<p>                &lt;chgDt&gt;&lt;/chgDt&gt;</p>
<p>                &lt;dminsttOfclEmailAdrs&gt;&lt;/dminsttOfclEmailAdrs&gt;</p>
<p>                &lt;indstrytyLmtYn&gt;Y&lt;/indstrytyLmtYn&gt;</p>
<p>                &lt;cnstrtsiteRgnNm&gt;광주광역시 남구&lt;/cnstrtsiteRgnNm&gt;</p>
<p>                &lt;rgnDutyJntcontrctYn&gt;N&lt;/rgnDutyJntcontrctYn&gt;</p>
<p>                &lt;chgNtceRsn&gt;&lt;/chgNtceRsn&gt;</p>
<p>                &lt;rbidOpengDt&gt;2025-07-08 11:00:00&lt;/rbidOpengDt&gt;</p>
<p>                &lt;ciblAplYn&gt;Y&lt;/ciblAplYn&gt;</p>
<p>                &lt;mtltyAdvcPsblYn&gt;N&lt;/mtltyAdvcPsblYn&gt;</p>
<p>                &lt;mtltyAdvcPsblYnCnstwkNm&gt;전문공사-유지보수공사&lt;/mtltyAdvcPsblYnCnstwkNm&gt;</p>
<p>                &lt;VAT&gt;5030000&lt;/VAT&gt;</p>
<p>                &lt;indutyVAT&gt;&lt;/indutyVAT&gt;</p>
<p>                &lt;indstrytyMfrcFldEvlYn&gt;N&lt;/indstrytyMfrcFldEvlYn&gt;</p>
<p>                &lt;bidWgrnteeRcptClseDt&gt;&lt;/bidWgrnteeRcptClseDt&gt;</p>
<p>                &lt;rgnLmtBidLocplcJdgmBssCd&gt;N&lt;/rgnLmtBidLocplcJdgmBssCd&gt;</p>
<p>                &lt;rgnLmtBidLocplcJdgmBssNm&gt;본사또는참여지사소재지&lt;/rgnLmtBidLocplcJdgmBssNm&gt;</p>
<p>&lt;sucsfbidMthdAppStd&gt;&lt;/sucsfbidMthdAppStd&gt;</p>
<p>            &lt;/item&gt;</p>
<p>        &lt;/items&gt;</p>
<p>        &lt;numOfRows&gt;10&lt;/numOfRows&gt;</p>
<p>        &lt;pageNo&gt;1&lt;/pageNo&gt;</p>
<p>        &lt;totalCount&gt;1&lt;/totalCount&gt;</p>
<p>    &lt;/body&gt;</p>
<p>&lt;/response&gt;</p></td>
</tr>
</tbody>
</table>

#### \[입찰공고목록 정보에 대한 용역조회\] 오퍼레이션 명세

<table>
<colgroup>
<col style="width: 4%" />
<col style="width: 21%" />
<col style="width: 17%" />
<col style="width: 21%" />
<col style="width: 2%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr>
<td rowspan="6">오퍼레이션 정보</td>
<td>오퍼레이션 번호</td>
<td>2</td>
<td>오퍼레이션명(국문)</td>
<td colspan="2">입찰공고목록 정보에 대한 용역조회</td>
</tr>
<tr>
<td>오퍼레이션 유형</td>
<td>조회(목록)</td>
<td>오퍼레이션명(영문)</td>
<td colspan="2">getBidPblancListInfoServc</td>
</tr>
<tr>
<td>오퍼레이션 설명</td>
<td colspan="4">검색조건에 등록일시, 입찰공고번호, 변경일시를 입력하여 나라장터의 입찰공고번호, 공고명, 발주기관, 수요기관, 계약체결방법명 등 용역부분의 입찰공고정보를 조회함</td>
</tr>
<tr>
<td>Call Back URL</td>
<td colspan="4">N/A</td>
</tr>
<tr>
<td>최대 메시지 사이즈</td>
<td colspan="4">[ 4000bytes]</td>
</tr>
<tr>
<td>평균 응답 시간</td>
<td>[ 500 ms]</td>
<td colspan="2">초당 최대 트랜잭션</td>
<td>[ 30 tps]</td>
</tr>
</tbody>
</table>

##### 요청 메시지 명세

<table>
<colgroup>
<col style="width: 19%" />
<col style="width: 19%" />
<col style="width: 13%" />
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 21%" />
</colgroup>
<tbody>
<tr>
<td>항목명(영문)</td>
<td>항목명(국문)</td>
<td>항목크기</td>
<td>항목구분</td>
<td>샘플데이터</td>
<td>항목설명</td>
</tr>
<tr>
<td style="text-align: left;">numOfRows</td>
<td style="text-align: left;">한 페이지 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td style="text-align: left;">pageNo</td>
<td style="text-align: left;">페이지 번호</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">페이지 번호</td>
</tr>
<tr>
<td style="text-align: left;">ServiceKey</td>
<td style="text-align: left;">서비스키</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">공공데이터포탈에서 받은 인증키</td>
<td style="text-align: left;">공공데이터포탈에서 받은 인증키</td>
</tr>
<tr>
<td style="text-align: left;">type</td>
<td style="text-align: left;">타입</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">0</td>
<td>json</td>
<td>오픈API 리턴 타입을 JSON으로 받고 싶을 경우 'json' 으로 지정</td>
</tr>
<tr>
<td style="text-align: left;">inqryDiv</td>
<td style="text-align: left;">조회구분</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">검색하고자하는 조회구분<br />
1:등록일시 , 2.입찰공고번호 , 3.변경일시</td>
</tr>
<tr>
<td style="text-align: left;">inqryBgnDt</td>
<td style="text-align: left;">조회시작일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">202507010000</td>
<td style="text-align: left;">검색하고자하는 등록일시 또는 변경일시 조회시작일시 "YYYYMMDDHHMM"<br />
(조회구분 '1', '3' 선택시 필수)</td>
</tr>
<tr>
<td style="text-align: left;">inqryEndDt</td>
<td style="text-align: left;">조회종료일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">202507012359</td>
<td style="text-align: left;">검색하고자하는 등록일시 또는 변경일시 조회종료일시 "YYYYMMDDHHMM"<br />
(조회구분 '1', '3' 선택시 필수)</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNo</td>
<td style="text-align: left;">입찰공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25BK00934017</td>
<td style="text-align: left;">검색하고자 하는 입찰공고번호<br />
(조회구분 '2' 선택시 필수)</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 응답 메시지 명세

<table style="width:98%;">
<colgroup>
<col style="width: 16%" />
<col style="width: 19%" />
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 14%" />
<col style="width: 23%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;">항목명(영문)</th>
<th style="text-align: left;">항목명(국문)</th>
<th style="text-align: left;">항목크기</th>
<th style="text-align: left;">항목구분</th>
<th style="text-align: left;">샘플데이터</th>
<th style="text-align: left;">항목설명</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;">resultCode</td>
<td style="text-align: left;">결과코드</td>
<td style="text-align: left;">2</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">00</td>
<td style="text-align: left;">결과코드</td>
</tr>
<tr>
<td style="text-align: left;">resultMsg</td>
<td style="text-align: left;">결과메세지</td>
<td style="text-align: left;">50</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">정상.</td>
<td style="text-align: left;">결과메세지</td>
</tr>
<tr>
<td style="text-align: left;">numOfRows</td>
<td style="text-align: left;">한 페이지 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td style="text-align: left;">pageNo</td>
<td style="text-align: left;">페이지 번호</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">페이지 수</td>
</tr>
<tr>
<td style="text-align: left;">totalCount</td>
<td style="text-align: left;">전체 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">전체 결과 수</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNo</td>
<td style="text-align: left;">입찰공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">R25BK00934017</td>
<td style="text-align: left;"><p>입찰공고 관리번입찰공고 관리번호이며 조달청나라장터 공고건의 형식은 년도(4)+월(2)+순번(5)이며 자체전자조달시스템 보유기관은 각 기관별 형식 별도 사용</p>
<p>*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성</p>
<p>-단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</p></td>
</tr>
<tr>
<td style="text-align: left;">bidNtceOrd</td>
<td style="text-align: left;">입찰공고차수</td>
<td style="text-align: left;">3</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">000</td>
<td style="text-align: left;">입찰공고차수는 해당 입찰공고에 대한 재공고 및 재입찰 등이 발생되었을 경우 증가되는 수</td>
</tr>
<tr>
<td style="text-align: left;">reNtceYn</td>
<td style="text-align: left;">재공고여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">Y</td>
<td style="text-align: left;">본 입찰공고의 재공고 여부(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">rgstTyNm</td>
<td style="text-align: left;">등록유형명</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">조달청 또는 나라장터 자체 공고건</td>
<td style="text-align: left;">입찰공고가 "조달청 또는 나라장터 자체 공고건","'나라장터 기타 공고건"</td>
</tr>
<tr>
<td style="text-align: left;">ntceKindNm</td>
<td style="text-align: left;">공고종류명</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">등록공고</td>
<td style="text-align: left;">공고의 공고상태명으로 등록공고, 변경공고, 취소공고, 재공고 구분</td>
</tr>
<tr>
<td style="text-align: left;">intrbidYn</td>
<td style="text-align: left;">국제입찰여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">국제입찰대상인지의 여부를 나타내며 국제입찰 대상은 내외국인 또는 외국인을 대상으로 하여 물품, 공사 및 용역을 조달하기 위하여 행하는 입찰을 말하며 수의계약을 포함한다. 국가계약법 제4조에 의해 추정가격이 고시금액(국제입찰 적용 대상 기준금액으로 기획재정부장관 및 행정자치부장관이 매 2년마다 고시한 금액을 말하며 WTO 또는 양자간(FTA) 정부조달협정에 따르면 국제입찰 대상 기준 금액이 SDR(Special Drawing Rights:특별인출권) 통화단위로 되어 있어 주무부 장관이 이를 2년마다 원화로 환산하여 고시) 이상일 경우 국제입찰대상이 됨(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceDt</td>
<td style="text-align: left;">입찰공고일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-01 13:21:14</td>
<td style="text-align: left;">입찰공고서를 공고한 일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">refNo</td>
<td style="text-align: left;">참조번호</td>
<td style="text-align: left;">105</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">서울특별시 재무공고 제2025-1698호</td>
<td style="text-align: left;">조달청 입찰공고의 경우 참조공고번호는 자체 전자조달시스템에서 관리하는 공고번호를 의미하며 자체전자조달시스템의 경우 참조공고번호는 나라장터(G2B) 입찰공고번호를 의미함</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNm</td>
<td style="text-align: left;">입찰공고명</td>
<td style="text-align: left;">1000</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">2025년 남부 관내 상수도 긴급누수복구공사장 건설폐기물 처리용역(장기계속)</td>
<td style="text-align: left;">공사명 또는 사업명이라고도 하며 입찰공고 내용을 요약한 이름</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttCd</td>
<td style="text-align: left;">공고기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">6110000</td>
<td style="text-align: left;">공고를 하는 기관의 코드로 행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드가 행자부코드가 없는 경우 조달청에서 부여한 공고기관 코드가 표기됨</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttNm</td>
<td style="text-align: left;">공고기관명</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">서울특별시</td>
<td style="text-align: left;">수요기관의 의뢰를 받아 공고하는 기관의 명</td>
</tr>
<tr>
<td style="text-align: left;">dminsttCd</td>
<td style="text-align: left;">수요기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">6114454</td>
<td style="text-align: left;">실제 수요기관의 코드로 행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드가 행자부코드가 없는 경우 조달청에서 부여한 수요기관 코드가 표기됨</td>
</tr>
<tr>
<td style="text-align: left;">dminsttNm</td>
<td style="text-align: left;">수요기관명</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">서울특별시 서울아리수본부 남부수도사업소</td>
<td style="text-align: left;">중앙조달인 경우 조달사업에 관한 법률 제2조(정의)에 따라 수요물자의 구매 공급 또는 시설공사 계약의 체결을 조달청장에게 요청할 수 있도록 조달청장이 인정하여 등록한 기관 또는 자체전자조달시스템을 이용하는 기관인 경우 계약을 의뢰한 기관의 명으로 공고기관과 수요기관이 동일할 수 있음</td>
</tr>
<tr>
<td style="text-align: left;">bidMethdNm</td>
<td style="text-align: left;">입찰방식명</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">전자입찰</td>
<td style="text-align: left;">공고의 입찰방식명 직찰<br />
전자입찰,전자입찰/직찰,전자/직찰/우편/상시,직찰/우편/상시,우편/상시,전자시담,복수견적(역경매),직찰/우편,전자시담(다자간)</td>
</tr>
<tr>
<td style="text-align: left;">cntrctCnclsMthdNm</td>
<td style="text-align: left;">계약체결방법명</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">제한경쟁</td>
<td style="text-align: left;">계약체결의 방법을 구분하는 명<br />
*일반경쟁계약은 계약 대상 물품의 규격 및 시방서와 계약조건 등을 널리 공고하여 일정한 자격을 가진 불특정 다수인의 입찰희망자를 모두 경쟁 입찰하는 계약방법<br />
*제한경쟁계약은 일반·지명경쟁계약제도의 단점을 보완하기 위해 실적제한, 기술보유제한, 특정물품제한, 지역제한 등을 두는 계약방법<br />
*지명경쟁계약은 계약상대자의 신용과 실적 등에 있어 적당하다고 인정하는 특정 다수의 경쟁 참가자를 지명하여 계약 상대방을 결정하는 계약방법<br />
*수의계약은 계약상대자를 결정함에 있어 경쟁방법에 의하지 않고 특정인을 선정하여 계약하는 계약방법</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttOfclNm</td>
<td style="text-align: left;">공고기관담당자명</td>
<td style="text-align: left;">35</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">김희정</td>
<td style="text-align: left;">공고기관의 공고를 담당하는 담당자의 명</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttOfclTelNo</td>
<td style="text-align: left;">공고기관담당자전화번호</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">02-2133-3251</td>
<td style="text-align: left;">공고기관의 공고를 담당하는 담당자의 전화번호</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttOfclEmailAdrs</td>
<td style="text-align: left;">공고기관담당자이메일주소</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">angelro@korea.kr</td>
<td style="text-align: left;">공고기관의 공고를 담당하는 담당자의 이메일주소</td>
</tr>
<tr>
<td style="text-align: left;">exctvNm</td>
<td style="text-align: left;">집행관명</td>
<td style="text-align: left;">35</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">김희정</td>
<td style="text-align: left;">공고의 집행관명</td>
</tr>
<tr>
<td style="text-align: left;">bidQlfctRgstDt</td>
<td style="text-align: left;">입찰참가자격등록마감일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-07 18:00</td>
<td style="text-align: left;">입찰참가등록이란 입찰사무를 효과적으로 집행하기 위하여 사전에 입찰참가자격등록을 해두었다가 필요 시 입찰에 참여하는 제도로 해당 공고에 대한 입찰참가자격의 등록이 완료되어야 하는 시점을 의미함 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">cmmnSpldmdAgrmntRcptdocMethd</td>
<td style="text-align: left;">공동수급협정서접수방식</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">전자문서</td>
<td style="text-align: left;">공동수급협정서의 접수방식"전자","수기","없음","공고서참고"</td>
</tr>
<tr>
<td style="text-align: left;">cmmnSpldmdAgrmntClseDt</td>
<td style="text-align: left;">공동수급협정마감일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-07 18:00:00</td>
<td style="text-align: left;">공동계약이 허용된 공고에 대해 공동수급체를 구성하여 입찰에 참여하고자 할 경우 구성원이 일정 분담내용에 따라 나누어 공동으로 이행하는 약속을 한 공동수급협정서를 작성하여야 하며 이때 공동수급협정서의 등록(작성) 마감 시점을 의미함”YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">cmmnSpldmdCorpRgnLmtYn</td>
<td style="text-align: left;">공동수급업체지역제한여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">Y</td>
<td style="text-align: left;">공동수급협정시 구성원의 지역제한을 적용할지 여부. 지역제한인경우 협정 구성업체가 참가제한지역에 포함되어야 함.(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">bidBeginDt</td>
<td style="text-align: left;">입찰개시일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-04 10:00:00</td>
<td style="text-align: left;">입찰서의 제출을 개시하는 일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">bidClseDt</td>
<td style="text-align: left;">입찰마감일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-08 14:00:00</td>
<td style="text-align: left;">입찰서의 제출을 마감하는 일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">opengDt</td>
<td style="text-align: left;">개찰일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-08 15:00:00</td>
<td style="text-align: left;">집행관이 개찰을 수행할 수 있는 시작일시이며<br />
개찰일시 이후에 개찰이 가능함<br />
실제 개찰을 수행한 시간을 의미하지 않음 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl1</td>
<td style="text-align: left;">공고규격서URL1</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00934017&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=1 &amp;prcmBsneSeCd=03</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl2</td>
<td style="text-align: left;">공고규격서URL2</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00934017&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=2 &amp;prcmBsneSeCd=03</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl3</td>
<td style="text-align: left;">공고규격서URL3</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00934017&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=3 &amp;prcmBsneSeCd=03</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl4</td>
<td style="text-align: left;">공고규격서URL4</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00934017&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=4 &amp;prcmBsneSeCd=03</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl5</td>
<td style="text-align: left;">공고규격서URL5</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00934017&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=5 &amp;prcmBsneSeCd=03</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl6</td>
<td style="text-align: left;">공고규격서URL6</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00934017&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=6 &amp;prcmBsneSeCd=03</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl7</td>
<td style="text-align: left;">공고규격서URL7</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00934017&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=7 &amp;prcmBsneSeCd=03</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl8</td>
<td style="text-align: left;">공고규격서URL8</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00934017&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=8 &amp;prcmBsneSeCd=03</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl9</td>
<td style="text-align: left;">공고규격서URL9</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00934017&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=9 &amp;prcmBsneSeCd=03</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl10</td>
<td style="text-align: left;">공고규격서URL10</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00934017&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=10 &amp;prcmBsneSeCd=03</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm1</td>
<td style="text-align: left;">공고규격파일명1</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">입찰공고문_2025년 남부 관내 상수도 긴급누수복구공사장 건설폐기물 처리용역(장기계속).hwpx</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm2</td>
<td style="text-align: left;">공고규격파일명2</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2.용역설명서.hwpx</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm3</td>
<td style="text-align: left;">공고규격파일명3</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">3.과업내용서.hwpx</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm4</td>
<td style="text-align: left;">공고규격파일명4</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">4.용역계약특수조건.hwpx</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm5</td>
<td style="text-align: left;">공고규격파일명5</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">5.특별과업내용서.hwpx</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm6</td>
<td style="text-align: left;">공고규격파일명6</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">6.물량내역서.xlsx</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm7</td>
<td style="text-align: left;">공고규격파일명7</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">7.사업수행능력평가서 작성안내서.hwp</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm8</td>
<td style="text-align: left;">공고규격파일명8</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">8.사업수행능력평가서 작성안내서.hwp</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm9</td>
<td style="text-align: left;">공고규격파일명9</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">9.사업수행능력평가서 작성안내서.hwp</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm10</td>
<td style="text-align: left;">공고규격파일명10</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">10.사업수행능력평가서 작성안내서.hwp</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">rbidPermsnYn</td>
<td style="text-align: left;">재입찰허용여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">입찰이 유찰되는 경우 재공고 없이 다시 입찰(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">pqApplDocRcptMthdNm</td>
<td style="text-align: left;">PQ신청서접수방법명</td>
<td style="text-align: left;">30</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">없음</td>
<td style="text-align: left;">PQ대상공고에서 PQ심사신청서를 어떻게 받을지에 대한 코드명</td>
</tr>
<tr>
<td style="text-align: left;">pqApplDocRcptDt</td>
<td style="text-align: left;">PQ신청서접수일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-01 14:00:00</td>
<td style="text-align: left;">PQ심사신청서 접수 마감일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">tpEvalApplMthdNm</td>
<td style="text-align: left;">TP심사신청방법명</td>
<td style="text-align: left;">30</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">없음</td>
<td style="text-align: left;">공고의 TP심사신청방법명</td>
</tr>
<tr>
<td style="text-align: left;">tpEvalApplClseDt</td>
<td style="text-align: left;">TP심사신청마감일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-01 14:00:00</td>
<td style="text-align: left;">공고의 TP심사신청마감일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">jntcontrctDutyRgnNm1</td>
<td style="text-align: left;">공동도급의무지역명1</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">서울특별시</td>
<td style="text-align: left;">공고의 공동도급의무지역명</td>
</tr>
<tr>
<td style="text-align: left;">jntcontrctDutyRgnNm2</td>
<td style="text-align: left;">공동도급의무지역명2</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">서울특별시</td>
<td style="text-align: left;">공고의 공동도급의무지역명</td>
</tr>
<tr>
<td style="text-align: left;">jntcontrctDutyRgnNm3</td>
<td style="text-align: left;">공동도급의무지역명3</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">서울특별시</td>
<td style="text-align: left;">공고의 공동도급의무지역명</td>
</tr>
<tr>
<td style="text-align: left;">rgnDutyJntcontrctRt</td>
<td style="text-align: left;">지역의무공동도급비율</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">지역의무공동동급시 3개지역의 공동도급합산 하한 비율(%)</td>
</tr>
<tr>
<td style="text-align: left;">dtlsBidYn</td>
<td style="text-align: left;">내역입찰여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">내역입찰인지는 나타내는 항목으로 내역입찰일 경우 투찰시 내역서를 첨부해야함(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">bidPrtcptLmtYn</td>
<td style="text-align: left;">입찰참가제한여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">공고의 입찰참가제한여부(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">prearngPrceDcsnMthdNm</td>
<td style="text-align: left;">예정가격결정방법명</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">복수예가</td>
<td style="text-align: left;">예정가격의 결정을 위해 복수예정가격방식으로 산정하는지 단일 예정가격으로 산정하는지를 구분하는 명</td>
</tr>
<tr>
<td style="text-align: left;">totPrdprcNum</td>
<td style="text-align: left;">총예가건수</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">15</td>
<td style="text-align: left;">공고의 총예가건수</td>
</tr>
<tr>
<td style="text-align: left;">drwtPrdprcNum</td>
<td style="text-align: left;">추첨예가건수</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">공고의 추첨예가건수</td>
</tr>
<tr>
<td style="text-align: left;">asignBdgtAmt</td>
<td style="text-align: left;">배정예산금액</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">142817400</td>
<td style="text-align: left;">사업목적물을 달성하기 위하여 배정된 예산액 또는 설계금액(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">presmptPrce</td>
<td style="text-align: left;">추정가격</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">129834000</td>
<td style="text-align: left;">물품/공사/용역 등의 조달 계약을 체결함에 있어 국제입찰 대상여부를 판단하는 기준 등으로 삼기 위하여 예정가격이 결정되기 전에 예산에 계상된 금액 등을 기준으로 하여 부가가치세 및 조달 수수료를 제외한 금액(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">opengPlce</td>
<td style="text-align: left;">개찰장소</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">국가종합전자조달시스템(나라장터)</td>
<td style="text-align: left;">집행관이 개찰을 하는 장소</td>
</tr>
<tr>
<td style="text-align: left;">dcmtgOprtnDt</td>
<td style="text-align: left;">설명회실시일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-01 14:00:00</td>
<td style="text-align: left;">해당 공고에 대한 현장/입찰/과업 설명회를 실시하는 일시”YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">dcmtgOprtnPlce</td>
<td style="text-align: left;">설명회실시장소</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">우리청 관리과</td>
<td style="text-align: left;">해당 공고에 대한 설명회를 실시하는 경우 현장/입찰/과업 설명회를 실시하는 장소</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceDtlUrl</td>
<td style="text-align: left;">입찰공고상세URL</td>
<td style="text-align: left;">512</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/link/PNPE027_01/single/?bidPbancNo=R25BK00934017&amp;bidPbancOrd=000</td>
<td style="text-align: left;">나라장터시스템의 입찰공고 상세화면 링크</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceUrl</td>
<td style="text-align: left;">입찰공고URL</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/link/PNPE027_01/single/?bidPbancNo=R25BK00934017&amp;bidPbancOrd=000</td>
<td style="text-align: left;">해당 입찰공고를 인터넷상에서 확인할 수 있는 URL주소</td>
</tr>
<tr>
<td style="text-align: left;">bidPrtcptFeePaymntYn</td>
<td style="text-align: left;">입찰참가수수료납부여부</td>
<td style="text-align: left;">30</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">없음</td>
<td style="text-align: left;">입찰참가 의사가 있는 자가 납부하여야하는 수수료의 유무 및 납부방법을 표기하는 것으로 "전자납부, 수기 및 전자납부, 수기, 없음"으로 표기</td>
</tr>
<tr>
<td style="text-align: left;">bidPrtcptFee</td>
<td style="text-align: left;">입찰참가수수료</td>
<td style="text-align: left;">21</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">입찰에 참가하기위해 납부하는 수수료(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">bidGrntymnyPaymntYn</td>
<td style="text-align: left;">입찰보증금납부여부</td>
<td style="text-align: left;">30</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">불허</td>
<td style="text-align: left;">입찰보증금을 나라장터에서 전자로 납부가능하게 할지 여부 “전자납부허용”,”불허’으로 표기</td>
</tr>
<tr>
<td style="text-align: left;">crdtrNm</td>
<td style="text-align: left;">채권자명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">서울특별시장</td>
<td style="text-align: left;">입찰보증금 항목의 "보증채권자명"으로 전자입찰보증 접수시 사용</td>
</tr>
<tr>
<td style="text-align: left;">ppswGnrlSrvceYn</td>
<td style="text-align: left;">조달청일반용역여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">공고의 조달청일반용역여부(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">srvceDivNm</td>
<td style="text-align: left;">용역구분명</td>
<td style="text-align: left;">30</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">일반용역</td>
<td style="text-align: left;">공고의 용역구분명으로 일반용역/기술용역으로 구분</td>
</tr>
<tr>
<td style="text-align: left;">prdctClsfcLmtYn</td>
<td style="text-align: left;">물품분류제한여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">물품공고의 경우 물품분류번호로 제한할 경우 Y, 물품분류번호 제한없으면 N</td>
</tr>
<tr>
<td style="text-align: left;">mnfctYn</td>
<td style="text-align: left;">제조여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">물품분류로 투찰제한시 제조물품으로 제한할 지 여부. "Y"일 경우 투찰시 업체의 경쟁입찰참가자격등록증에 공고서상 물품분류가 제조물품으로 등록되어 있어야 투찰가능(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">purchsObjPrdctList</td>
<td style="text-align: left;">구매대상물품목록</td>
<td style="text-align: left;">4000</td>
<td style="text-align: left;">0..n</td>
<td style="text-align: left;">[1^7612159801^건설폐기물처리서비스],</td>
<td style="text-align: left;">공고의 구매대상물품목록으로 [입찰분류번호^세부품명번호(세부물품분류번호)^세부품명(세부물품분류명)],[입찰분류번호^세부품명번호(세부물품분류번호)^세부품명(세부물품분류명)]</td>
</tr>
<tr>
<td style="text-align: left;">untyNtceNo</td>
<td style="text-align: left;">통합공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25BM00300902</td>
<td style="text-align: left;"><p>입찰공고 관리번입찰공고 관리번호이며 조달청나라장터 공고건의 형식은 년도(4)+월(2)+순번(5)이며 자체전자조달시스템 보유기관은 각 기관별 형식 별도 사용</p>
<p>*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성</p>
<p>-단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</p></td>
</tr>
<tr>
<td style="text-align: left;">cmmnSpldmdMethdCd</td>
<td style="text-align: left;">공동수급방식코드</td>
<td style="text-align: left;">15</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">공500002</td>
<td style="text-align: left;">공동수급이라 함은 구성원을 2인 이상으로 하여 수급인이 해당계약을 공동으로 수행하기 위하여 잠정적으로 결성한 실체를 의미하며 공동수급체가도급을 받아 이행하는 방식을 구분하는 코드로<br />
공500001 : 공동이행<br />
공500002 : 분담이행<br />
공500003 : 주계약자관리방식<br />
공500004 : 단독계약<br />
공500005 : 혼합방식<br />
공500006 : 공동이행 또는 분담이행<br />
공500007 : 혼합_단독<br />
공500008 : 혼합_공동<br />
공500012 : 해당없음으로 구분됨</td>
</tr>
<tr>
<td style="text-align: left;">cmmnSpldmdMethdNm</td>
<td style="text-align: left;">공동수급구성방식명</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">(전자)분담이행</td>
<td style="text-align: left;">공고의 공동수급구성방식명</td>
</tr>
<tr>
<td style="text-align: left;">stdNtceDocUrl</td>
<td style="text-align: left;">표준공고서URL</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00934017&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=1 &amp;prcmBsneSeCd=03</td>
<td style="text-align: left;">공고의 표준공고문URL</td>
</tr>
<tr>
<td style="text-align: left;">brffcBidprcPermsnYn</td>
<td style="text-align: left;">지사투찰허용여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">지역제한 공고에 한해서 지사 투찰을 허용할지 여부. 투찰제어시 사용(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">dsgntCmptYn</td>
<td style="text-align: left;">지명경쟁여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">공고의 지명경쟁여부(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">arsltCmptYn</td>
<td style="text-align: left;">실적경쟁여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">공고의 실적경쟁여부(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">pqEvalYn</td>
<td style="text-align: left;">PQ심사여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">공고의 PQ심사여부(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">tpEvalYn</td>
<td style="text-align: left;">TP심사여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">공고의 물품규격명(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">ntceDscrptYn</td>
<td style="text-align: left;">공고설명여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">공고의 공고설명여부(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">rsrvtnPrceReMkngMthdNm</td>
<td style="text-align: left;">예비가격재작성방법명</td>
<td style="text-align: left;">50</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">재입찰시 기존 예비가격을 사용하여 예정가격이 산정됩니다.</td>
<td style="text-align: left;">공고의 예비가격재작성방법명</td>
</tr>
<tr>
<td style="text-align: left;">arsltApplDocRcptMthdNm</td>
<td style="text-align: left;">실적신청서접수방법명</td>
<td style="text-align: left;">50</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">전자문서</td>
<td style="text-align: left;">공고의 실적신청서접수방법명</td>
</tr>
<tr>
<td style="text-align: left;">arsltReqstdocRcptDt</td>
<td style="text-align: left;">실적신청서접수일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-08 15:00:00</td>
<td style="text-align: left;">실적심사신청서 접수마감일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">orderPlanUntyNo</td>
<td style="text-align: left;">발주계획통합번호</td>
<td style="text-align: left;">35</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25DD20306522</td>
<td style="text-align: left;">*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성<br />
- 단계구분: BK(입찰)<br />
TA(계약)<br />
DD:(발주계획)<br />
BD(사전규격),<br />
BK(통합입찰)</td>
</tr>
<tr>
<td style="text-align: left;">sucsfbidLwltRate</td>
<td style="text-align: left;">낙찰하한율</td>
<td style="text-align: left;">22</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">87.745</td>
<td style="text-align: left;">개찰시 사용하는 낙찰하한율(%)</td>
</tr>
<tr>
<td style="text-align: left;">rgstDt</td>
<td style="text-align: left;">등록일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">2025-07-01 13:21:14</td>
<td style="text-align: left;">공고의 등록일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">bfSpecRgstNo</td>
<td style="text-align: left;">사전규격등록번호</td>
<td style="text-align: left;">17</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25BD20306522</td>
<td style="text-align: left;"><p>*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성</p>
<p>- 단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</p></td>
</tr>
<tr>
<td style="text-align: left;">infoBizYn</td>
<td style="text-align: left;">정보화사업여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">정보화사업여부<br />
Y/N</td>
</tr>
<tr>
<td style="text-align: left;">sucsfbidMthdCd</td>
<td style="text-align: left;">낙찰방법코드</td>
<td style="text-align: left;">9</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">낙030001</td>
<td style="text-align: left;">낙찰방법명에 대한 코드 (한글 1자리 + 숫자 6자리)</td>
</tr>
<tr>
<td style="text-align: left;">sucsfbidMthdNm</td>
<td style="text-align: left;">낙찰방법명</td>
<td style="text-align: left;">700</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">적격심사제-추정가격 2억원 미만인 용역</td>
<td style="text-align: left;">낙찰자를 결정하는 방법-낙찰방법 세부기준</td>
</tr>
<tr>
<td style="text-align: left;">chgDt</td>
<td style="text-align: left;">변경일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-01 13:21:14</td>
<td style="text-align: left;">공고의 변경일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">dminsttOfclEmailAdrs</td>
<td style="text-align: left;">수요기관담당자이메일주소</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">nskk22@kywa.or.kr</td>
<td style="text-align: left;">수요기관 담당자의 이메일주소</td>
</tr>
<tr>
<td style="text-align: left;">indstrytyLmtYn</td>
<td style="text-align: left;">업종제한여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">Y</td>
<td style="text-align: left;">해당 공고 입찰 시 업종(면허)제한을 두는지의 여부<br />
예시)Y</td>
</tr>
<tr>
<td style="text-align: left;">chgNtceRsn</td>
<td style="text-align: left;">변경공고사유</td>
<td style="text-align: left;">4000</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">공동수급협정서 접수 여부 변경</td>
<td style="text-align: left;">공고종류명(공고의 공고상태명) 이 변경일 경우 변경공고사유 , 취소일 경우 취소공고사유</td>
</tr>
<tr>
<td style="text-align: left;">rbidOpengDt</td>
<td style="text-align: left;">재입찰개찰일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-08 15:00:00</td>
<td style="text-align: left;">공고종류명이 ‘재입찰’ 일 경우 재입찰공고의 개찰을 수행할 수 있는 시작일시<br />
“YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">VAT</td>
<td style="text-align: left;">부가가치세</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">12983400</td>
<td style="text-align: left;">부가가치세</td>
</tr>
<tr>
<td style="text-align: left;">indutyVAT</td>
<td style="text-align: left;">주공종부가가치세</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">주공종부가가치세</td>
</tr>
<tr>
<td style="text-align: left;">rgnLmtBidLocplcJdgmBssCd</td>
<td style="text-align: left;">지역제한입찰소재지판단기준코드</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">지역제한입찰소재지판단기준코드</td>
</tr>
<tr>
<td style="text-align: left;">rgnLmtBidLocplcJdgmBssNm</td>
<td style="text-align: left;">지역제한입찰소재지판단기준명</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">본사또는참여지사소재지</td>
<td style="text-align: left;">지역제한입찰소재지판단기준명</td>
</tr>
<tr>
<td style="text-align: left;">pubPrcrmntLrgclsfcNm</td>
<td style="text-align: left;">공공조달대분류명</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">폐기물 처리 및 재활용서비스</td>
<td style="text-align: left;">나라장터에서의 사업분류체계의 공공조달분류번호의 대분류에 해당되는 명</td>
</tr>
<tr>
<td style="text-align: left;">pubPrcrmntMidclsfcNm</td>
<td style="text-align: left;">공공조달중분류명</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">폐기물 처리</td>
<td style="text-align: left;">나라장터에서의 사업분류체계의 공공조달분류번호의 중분류에 해당되는 명</td>
</tr>
<tr>
<td style="text-align: left;">pubPrcrmntClsfcNo</td>
<td style="text-align: left;">공공조달분류번호</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">76121598</td>
<td style="text-align: left;">나라장터에서의 사업분류체계의 공공조달분류번호</td>
</tr>
<tr>
<td style="text-align: left;">pubPrcrmntClsfcNm</td>
<td style="text-align: left;">공공조달분류명</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">건설폐기물처리서비스</td>
<td style="text-align: left;">나라장터에서의 사업분류체계의 공공조달분류번호명</td>
</tr>
<tr>
<td style="text-align: left;">techAbltEvlRt</td>
<td style="text-align: left;">기술능력평가비율</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">80</td>
<td style="text-align: left;">협상에 의한 낙찰자 결정의 경우 기술능력 평가 비율</td>
</tr>
<tr>
<td style="text-align: left;">bidPrceEvlRt</td>
<td style="text-align: left;">입찰가격평가비율</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">협상에 의한 낙찰자 결정의 경우 기술능력 입찰가격 평가 비율</td>
</tr>
<tr>
<td style="text-align: left;">sucsfbidMthdAppStd</td>
<td style="text-align: left;">낙찰방법적용기준</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">조달청 시설공사 적격심사세부기준</td>
<td style="text-align: left;"><p>낙찰자를 결정하</p>
<p>방법 적용기준</p></td>
</tr>
</tbody>
</table>

##### 요청 / 응답 메시지 예제

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr>
<td style="text-align: center;"><strong>REST(URI)</strong></td>
</tr>
<tr>
<td style="text-align: center;">http://apis.data.go.kr/1230000/ad/BidPublicInfoService/getBidPblancListInfoServc?inqryDiv=2 &amp;bidNtceNo=R25BK00934017&amp;pageNo=1&amp;numOfRows=10&amp;ServiceKey=인증키</td>
</tr>
<tr>
<td style="text-align: center;"><strong>응답 메시지</strong></td>
</tr>
<tr>
<td style="text-align: center;"><p>&lt;response&gt;</p>
<p>&lt;header&gt;</p>
<p>&lt;resultCode&gt;00&lt;/resultCode&gt;</p>
<p>&lt;resultMsg&gt;정상&lt;/resultMsg&gt;</p>
<p>&lt;/header&gt;</p>
<p>&lt;body&gt;</p>
<p>&lt;items&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00934017&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;reNtceYn&gt;Y&lt;/reNtceYn&gt;</p>
<p>&lt;rgstTyNm&gt;조달청 또는 나라장터 자체 공고건&lt;/rgstTyNm&gt;</p>
<p>&lt;ntceKindNm&gt;등록공고&lt;/ntceKindNm&gt;</p>
<p>&lt;intrbidYn&gt;N&lt;/intrbidYn&gt;</p>
<p>&lt;bidNtceDt&gt;2025-07-01 13:21:14&lt;/bidNtceDt&gt;</p>
<p>&lt;refNo&gt;서울특별시 재무공고 제2025-1698호&lt;/refNo&gt;</p>
<p>&lt;bidNtceNm&gt;2025년 남부 관내 상수도 긴급누수복구공사장 건설폐기물 처리용역(장기계속)&lt;/bidNtceNm&gt;</p>
<p>&lt;ntceInsttCd&gt;6110000&lt;/ntceInsttCd&gt;</p>
<p>&lt;ntceInsttNm&gt;서울특별시&lt;/ntceInsttNm&gt;</p>
<p>&lt;dminsttCd&gt;6114454&lt;/dminsttCd&gt;</p>
<p>&lt;dminsttNm&gt;서울특별시 서울아리수본부 남부수도사업소&lt;/dminsttNm&gt;</p>
<p>&lt;bidMethdNm&gt;전자입찰&lt;/bidMethdNm&gt;</p>
<p>&lt;cntrctCnclsMthdNm&gt;제한경쟁&lt;/cntrctCnclsMthdNm&gt;</p>
<p>&lt;ntceInsttOfclNm&gt;김희정&lt;/ntceInsttOfclNm&gt;</p>
<p>&lt;ntceInsttOfclTelNo&gt;02-2133-3251&lt;/ntceInsttOfclTelNo&gt;</p>
<p>&lt;ntceInsttOfclEmailAdrs&gt;&lt;/ntceInsttOfclEmailAdrs&gt;</p>
<p>&lt;exctvNm&gt;김희정&lt;/exctvNm&gt;</p>
<p>&lt;bidQlfctRgstDt&gt;2025-07-07 18:00&lt;/bidQlfctRgstDt&gt;</p>
<p>&lt;cmmnSpldmdAgrmntRcptdocMethd&gt;전자&lt;/cmmnSpldmdAgrmntRcptdocMethd&gt;</p>
<p>&lt;cmmnSpldmdAgrmntClseDt&gt;2025-07-07 18:00:00&lt;/cmmnSpldmdAgrmntClseDt&gt;</p>
<p>&lt;cmmnSpldmdCorpRgnLmtYn&gt;Y&lt;/cmmnSpldmdCorpRgnLmtYn&gt;</p>
<p>&lt;bidBeginDt&gt;2025-07-04 10:00:00&lt;/bidBeginDt&gt;</p>
<p>&lt;bidClseDt&gt;2025-07-08 14:00:00&lt;/bidClseDt&gt;</p>
<p>&lt;opengDt&gt;2025-07-08 15:00:00&lt;/opengDt&gt;</p>
<p>&lt;ntceSpecDocUrl1&gt;https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00934017&amp;amp;bidPbancOrd=000&amp;amp;fileType=&amp;amp;fileSeq=1 &amp;prcmBsneSeCd=03&lt;/ntceSpecDocUrl1&gt;</p>
<p>&lt;ntceSpecDocUrl2&gt;https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00934017&amp;amp;bidPbancOrd=000&amp;amp;fileType=&amp;amp;fileSeq=2 &amp;prcmBsneSeCd=03&lt;/ntceSpecDocUrl2&gt;</p>
<p>&lt;ntceSpecDocUrl3&gt;https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00934017&amp;amp;bidPbancOrd=000&amp;amp;fileType=&amp;amp;fileSeq=3 &amp;prcmBsneSeCd=03&lt;/ntceSpecDocUrl3&gt;</p>
<p>&lt;ntceSpecDocUrl4&gt;https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00934017&amp;amp;bidPbancOrd=000&amp;amp;fileType=&amp;amp;fileSeq=4 &amp;prcmBsneSeCd=03&lt;/ntceSpecDocUrl4&gt;</p>
<p>&lt;ntceSpecDocUrl5&gt;https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00934017&amp;amp;bidPbancOrd=000&amp;amp;fileType=&amp;amp;fileSeq=5 &amp;prcmBsneSeCd=03&lt;/ntceSpecDocUrl5&gt;</p>
<p>&lt;ntceSpecDocUrl6&gt;https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00934017&amp;amp;bidPbancOrd=000&amp;amp;fileType=&amp;amp;fileSeq=6 &amp;prcmBsneSeCd=03&lt;/ntceSpecDocUrl6&gt;</p>
<p>&lt;ntceSpecDocUrl7&gt;&lt;/ntceSpecDocUrl7&gt;</p>
<p>&lt;ntceSpecDocUrl8&gt;&lt;/ntceSpecDocUrl8&gt;</p>
<p>&lt;ntceSpecDocUrl9&gt;&lt;/ntceSpecDocUrl9&gt;</p>
<p>&lt;ntceSpecDocUrl10&gt;&lt;/ntceSpecDocUrl10&gt;</p>
<p>&lt;ntceSpecFileNm1&gt;입찰공고문_2025년 남부 관내 상수도 긴급누수복구공사장 건설폐기물 처리용역(장기계속).hwpx&lt;/ntceSpecFileNm1&gt;</p>
<p>&lt;ntceSpecFileNm2&gt;2. 용역설명서.hwpx&lt;/ntceSpecFileNm2&gt;</p>
<p>&lt;ntceSpecFileNm3&gt;3. 과업내용서.hwpx&lt;/ntceSpecFileNm3&gt;</p>
<p>&lt;ntceSpecFileNm4&gt;4. 용역계약특수조건.hwpx&lt;/ntceSpecFileNm4&gt;</p>
<p>&lt;ntceSpecFileNm5&gt;5. 특별과업내용서.hwpx&lt;/ntceSpecFileNm5&gt;</p>
<p>&lt;ntceSpecFileNm6&gt;6. 물량내역서.xlsx&lt;/ntceSpecFileNm6&gt;</p>
<p>&lt;ntceSpecFileNm7&gt;&lt;/ntceSpecFileNm7&gt;</p>
<p>&lt;ntceSpecFileNm8&gt;&lt;/ntceSpecFileNm8&gt;</p>
<p>&lt;ntceSpecFileNm9&gt;&lt;/ntceSpecFileNm9&gt;</p>
<p>&lt;ntceSpecFileNm10&gt;&lt;/ntceSpecFileNm10&gt;</p>
<p>&lt;rbidPermsnYn&gt;N&lt;/rbidPermsnYn&gt;</p>
<p>&lt;pqApplDocRcptMthdNm&gt;&lt;/pqApplDocRcptMthdNm&gt;</p>
<p>&lt;pqApplDocRcptDt&gt;&lt;/pqApplDocRcptDt&gt;</p>
<p>&lt;tpEvalApplMthdNm&gt;&lt;/tpEvalApplMthdNm&gt;</p>
<p>&lt;tpEvalApplClseDt&gt;&lt;/tpEvalApplClseDt&gt;</p>
<p>&lt;jntcontrctDutyRgnNm1&gt;&lt;/jntcontrctDutyRgnNm1&gt;</p>
<p>&lt;jntcontrctDutyRgnNm2&gt;&lt;/jntcontrctDutyRgnNm2&gt;</p>
<p>&lt;jntcontrctDutyRgnNm3&gt;&lt;/jntcontrctDutyRgnNm3&gt;</p>
<p>&lt;rgnDutyJntcontrctRt&gt;&lt;/rgnDutyJntcontrctRt&gt;</p>
<p>&lt;dtlsBidYn&gt;&lt;/dtlsBidYn&gt;</p>
<p>&lt;bidPrtcptLmtYn&gt;N&lt;/bidPrtcptLmtYn&gt;</p>
<p>&lt;prearngPrceDcsnMthdNm&gt;복수예가&lt;/prearngPrceDcsnMthdNm&gt;</p>
<p>&lt;totPrdprcNum&gt;15&lt;/totPrdprcNum&gt;</p>
<p>&lt;drwtPrdprcNum&gt;4&lt;/drwtPrdprcNum&gt;</p>
<p>&lt;asignBdgtAmt&gt;142817400&lt;/asignBdgtAmt&gt;</p>
<p>&lt;presmptPrce&gt;129834000&lt;/presmptPrce&gt;</p>
<p>&lt;opengPlce&gt;국가종합전자조달시스템(나라장터)&lt;/opengPlce&gt;</p>
<p>&lt;dcmtgOprtnDt&gt;&lt;/dcmtgOprtnDt&gt;</p>
<p>&lt;dcmtgOprtnPlce&gt;&lt;/dcmtgOprtnPlce&gt;</p>
<p>&lt;bidNtceDtlUrl&gt;https://www.g2b.go.kr/link/PNPE027_01/single/?bidPbancNo=R25BK00934017&amp;amp;bidPbancOrd=000&lt;/bidNtceDtlUrl&gt;</p>
<p>&lt;bidNtceUrl&gt; https://www.g2b.go.kr/link/PNPE027_01/single/?bidPbancNo=R25BK00934017&amp;amp;bidPbancOrd=000&lt;/bidNtceUrl&gt;</p>
<p>&lt;bidPrtcptFeePaymntYn&gt;&lt;/bidPrtcptFeePaymntYn&gt;</p>
<p>&lt;bidPrtcptFee&gt;0&lt;/bidPrtcptFee&gt;</p>
<p>&lt;bidGrntymnyPaymntYn&gt;&lt;/bidGrntymnyPaymntYn&gt;</p>
<p>&lt;crdtrNm&gt;서울특별시장&lt;/crdtrNm&gt;</p>
<p>&lt;ppswGnrlSrvceYn&gt;N&lt;/ppswGnrlSrvceYn&gt;</p>
<p>&lt;srvceDivNm&gt;일반용역&lt;/srvceDivNm&gt;</p>
<p>&lt;prdctClsfcLmtYn&gt;&lt;/prdctClsfcLmtYn&gt;</p>
<p>&lt;mnfctYn&gt;&lt;/mnfctYn&gt;</p>
<p>&lt;purchsObjPrdctList&gt;&lt;/purchsObjPrdctList&gt;</p>
<p>&lt;untyNtceNo&gt;R25BM00300902&lt;/untyNtceNo&gt;</p>
<p>&lt;cmmnSpldmdMethdCd&gt;공500002&lt;/cmmnSpldmdMethdCd&gt;</p>
<p>&lt;cmmnSpldmdMethdNm&gt;(전자)분담이행&lt;/cmmnSpldmdMethdNm&gt;</p>
<p>&lt;stdNtceDocUrl&gt;https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00934017&amp;amp;bidPbancOrd=000&amp;amp;fileType=&amp;amp;fileSeq=1 &amp;prcmBsneSeCd=03&lt;/stdNtceDocUrl&gt;</p>
<p>&lt;brffcBidprcPermsnYn&gt;&lt;/brffcBidprcPermsnYn&gt;</p>
<p>&lt;dsgntCmptYn&gt;N&lt;/dsgntCmptYn&gt;</p>
<p>&lt;arsltCmptYn&gt;N&lt;/arsltCmptYn&gt;</p>
<p>&lt;pqEvalYn&gt;&lt;/pqEvalYn&gt;</p>
<p>&lt;tpEvalYn&gt;N&lt;/tpEvalYn&gt;</p>
<p>&lt;ntceDscrptYn&gt;&lt;/ntceDscrptYn&gt;</p>
<p>&lt;rsrvtnPrceReMkngMthdNm&gt;&lt;/rsrvtnPrceReMkngMthdNm&gt;</p>
<p>&lt;arsltApplDocRcptMthdNm&gt;&lt;/arsltApplDocRcptMthdNm&gt;</p>
<p>&lt;arsltReqstdocRcptDt&gt;&lt;/arsltReqstdocRcptDt&gt;</p>
<p>&lt;orderPlanUntyNo&gt;R25DD20306522&lt;/orderPlanUntyNo&gt;</p>
<p>&lt;sucsfbidLwltRate&gt;87.745&lt;/sucsfbidLwltRate&gt;</p>
<p>&lt;rgstDt&gt;2025-07-01 13:21:14&lt;/rgstDt&gt;</p>
<p>&lt;bfSpecRgstNo&gt;&lt;/bfSpecRgstNo&gt;</p>
<p>&lt;infoBizYn&gt;&lt;/infoBizYn&gt;</p>
<p>&lt;sucsfbidMthdCd&gt;낙030001&lt;/sucsfbidMthdCd&gt;</p>
<p>&lt;sucsfbidMthdNm&gt;적격심사제-추정가격 2억원 미만인 용역&lt;/sucsfbidMthdNm&gt;</p>
<p>&lt;chgDt&gt;&lt;/chgDt&gt;</p>
<p>&lt;dminsttOfclEmailAdrs&gt;&lt;/dminsttOfclEmailAdrs&gt;</p>
<p>&lt;indstrytyLmtYn&gt;Y&lt;/indstrytyLmtYn&gt;</p>
<p>&lt;chgNtceRsn&gt;&lt;/chgNtceRsn&gt;</p>
<p>&lt;rbidOpengDt&gt;2025-07-08 15:00:00&lt;/rbidOpengDt&gt;</p>
<p>&lt;VAT&gt;12983400&lt;/VAT&gt;</p>
<p>&lt;indutyVAT&gt;&lt;/indutyVAT&gt;</p>
<p>&lt;rgnLmtBidLocplcJdgmBssCd&gt;&lt;/rgnLmtBidLocplcJdgmBssCd&gt;</p>
<p>&lt;rgnLmtBidLocplcJdgmBssNm&gt;&lt;/rgnLmtBidLocplcJdgmBssNm&gt;</p>
<p>&lt;pubPrcrmntLrgClsfcNm&gt;폐기물 처리 및 재활용서비스&lt;/pubPrcrmntLrgClsfcNm&gt;</p>
<p>&lt;pubPrcrmntMidClsfcNm&gt; 폐기물 처리 &lt;/pubPrcrmntMidClsfcNm&gt;</p>
<p>&lt;pubPrcrmntClsfcNo&gt;76121598&lt;/pubPrcrmntClsfcNo&gt;</p>
<p>&lt;pubPrcrmntClsfcNm&gt;건설폐기물처리서비스&lt;/pubPrcrmntClsfcNm&gt;</p>
<p>&lt;techAbltEvlRt&gt;&lt;/techAbltEvlRt&gt;</p>
<p>&lt;bidPrceEvlRt&gt;&lt;/bidPrceEvlRt&gt;</p>
<p>&lt;sucsfbidMthdAppStd&gt;&lt;/sucsfbidMthdAppStd&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;/items&gt;</p>
<p>&lt;numOfRows&gt;10&lt;/numOfRows&gt;</p></td>
</tr>
</tbody>
</table>

#### \[입찰공고목록 정보에 대한 외자조회\] 오퍼레이션 명세

<table>
<colgroup>
<col style="width: 4%" />
<col style="width: 21%" />
<col style="width: 17%" />
<col style="width: 21%" />
<col style="width: 2%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr>
<td rowspan="6">오퍼레이션 정보</td>
<td>오퍼레이션 번호</td>
<td>3</td>
<td>오퍼레이션명(국문)</td>
<td colspan="2">입찰공고목록 정보에 대한 외자조회</td>
</tr>
<tr>
<td>오퍼레이션 유형</td>
<td>조회(목록)</td>
<td>오퍼레이션명(영문)</td>
<td colspan="2">getBidPblancListInfoFrgcpt</td>
</tr>
<tr>
<td>오퍼레이션 설명</td>
<td colspan="4">검색조건에 등록일시, 입찰공고번호, 변경일시를 입력하여 나라장터의 입찰공고번호, 공고명, 발주기관, 수요기관, 계약체결방법명 등 외자 부분의 입찰공고정보를 조회함</td>
</tr>
<tr>
<td>Call Back URL</td>
<td colspan="4">N/A</td>
</tr>
<tr>
<td>최대 메시지 사이즈</td>
<td colspan="4">[ 4000bytes]</td>
</tr>
<tr>
<td>평균 응답 시간</td>
<td>[ 500 ms]</td>
<td colspan="2">초당 최대 트랜잭션</td>
<td>[ 30 tps]</td>
</tr>
</tbody>
</table>

##### 요청 메시지 명세

<table>
<colgroup>
<col style="width: 16%" />
<col style="width: 20%" />
<col style="width: 14%" />
<col style="width: 11%" />
<col style="width: 16%" />
<col style="width: 21%" />
</colgroup>
<tbody>
<tr>
<td>항목명(영문)</td>
<td>항목명(국문)</td>
<td>항목크기</td>
<td>항목구분</td>
<td>샘플데이터</td>
<td>항목설명</td>
</tr>
<tr>
<td style="text-align: left;">numOfRows</td>
<td style="text-align: left;">한 페이지 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td style="text-align: left;">pageNo</td>
<td style="text-align: left;">페이지 번호</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">페이지 번호</td>
</tr>
<tr>
<td style="text-align: left;">ServiceKey</td>
<td style="text-align: left;">서비스키</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">공공데이터포탈에서 받은 인증키</td>
<td style="text-align: left;">공공데이터포탈에서 받은 인증키</td>
</tr>
<tr>
<td style="text-align: left;">type</td>
<td style="text-align: left;">타입</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">0</td>
<td>json</td>
<td>오픈API 리턴 타입을 JSON으로 받고 싶을 경우 'json' 으로 지정</td>
</tr>
<tr>
<td style="text-align: left;">inqryDiv</td>
<td style="text-align: left;">조회구분</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">검색하고자하는 조회구분<br />
1:등록일시 , 2.입찰공고번호 , 3.변경일시</td>
</tr>
<tr>
<td style="text-align: left;">inqryBgnDt</td>
<td style="text-align: left;">조회시작일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">202507010000</td>
<td style="text-align: left;">검색하고자하는 등록일시 또는 변경일시 조회시작일시 "YYYYMMDDHHMM"<br />
(조회구분 '1', '3' 선택시 필수)</td>
</tr>
<tr>
<td style="text-align: left;">inqryEndDt</td>
<td style="text-align: left;">조회종료일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">202507012359</td>
<td style="text-align: left;">검색하고자하는 등록일시 또는 변경일시 조회종료일시 "YYYYMMDDHHMM"<br />
(조회구분 '1', '3' 선택시 필수)</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNo</td>
<td style="text-align: left;">입찰공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25BK00963966</td>
<td style="text-align: left;">검색하고자 하는 입찰공고번호<br />
(조회구분 '2' 선택시 필수)</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 응답 메시지 명세

<table>
<colgroup>
<col style="width: 20%" />
<col style="width: 18%" />
<col style="width: 14%" />
<col style="width: 11%" />
<col style="width: 14%" />
<col style="width: 19%" />
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
<td style="text-align: left;">resultCode</td>
<td style="text-align: left;">결과코드</td>
<td style="text-align: left;">2</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">00</td>
<td style="text-align: left;">결과코드</td>
</tr>
<tr>
<td style="text-align: left;">resultMsg</td>
<td style="text-align: left;">결과메세지</td>
<td style="text-align: left;">50</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">정상.</td>
<td style="text-align: left;">결과메세지</td>
</tr>
<tr>
<td style="text-align: left;">numOfRows</td>
<td style="text-align: left;">한 페이지 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td style="text-align: left;">pageNo</td>
<td style="text-align: left;">페이지 번호</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">페이지 수</td>
</tr>
<tr>
<td style="text-align: left;">totalCount</td>
<td style="text-align: left;">데이터 총 개수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">17</td>
<td style="text-align: left;">데이터 총개수</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNo</td>
<td style="text-align: left;">입찰공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">R25BK00963966</td>
<td style="text-align: left;"><p>입찰공고 관리번입찰공고 관리번호이며 조달청나라장터 공고건의 형식은 년도(4)+월(2)+순번(5)이며 자체전자조달시스템 보유기관은 각 기관별 형식 별도 사용</p>
<p>*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성</p>
<p>-단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</p></td>
</tr>
<tr>
<td style="text-align: left;">bidNtceOrd</td>
<td style="text-align: left;">입찰공고차수</td>
<td style="text-align: left;">3</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">000</td>
<td style="text-align: left;">입찰공고차수는 해당 입찰공고에 대한 재공고 및 재입찰 등이 발생되었을 경우 증가되는 수</td>
</tr>
<tr>
<td style="text-align: left;">reNtceYn</td>
<td style="text-align: left;">재공고여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">본 입찰공고의 재공고 여부(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">rgstTyNm</td>
<td style="text-align: left;">등록유형명</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">조달청 또는 나라장터 자체 공고건</td>
<td style="text-align: left;">입찰공고가 "조달청 또는 나라장터 자체 공고건","'나라장터 기타 공고건"</td>
</tr>
<tr>
<td style="text-align: left;">ntceKindNm</td>
<td style="text-align: left;">공고종류명</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">등록공고</td>
<td style="text-align: left;">공고의 공고상태명으로 등록공고, 변경공고, 취소공고, 재공고 구분</td>
</tr>
<tr>
<td style="text-align: left;">intrbidYn</td>
<td style="text-align: left;">국제입찰여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">Y</td>
<td style="text-align: left;">국제입찰대상인지의 여부를 나타내며 국제입찰 대상은 내외국인 또는 외국인을 대상으로 하여 물품, 공사 및 용역을 조달하기 위하여 행하는 입찰을 말하며 수의계약을 포함한다. 국가계약법 제4조에 의해 추정가격이 고시금액(국제입찰 적용 대상 기준금액으로 기획재정부장관 및 행정자치부장관이 매 2년마다 고시한 금액을 말하며 WTO 또는 양자간(FTA) 정부조달협정에 따르면 국제입찰 대상 기준 금액이 SDR(Special Drawing Rights:특별인출권) 통화단위로 되어 있어 주무부 장관이 이를 2년마다 원화로 환산하여 고시) 이상일 경우 국제입찰대상이 됨(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceDt</td>
<td style="text-align: left;">입찰공고일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">2025-07-17 16:19:29</td>
<td style="text-align: left;">입찰공고서를 공고한 일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">refNo</td>
<td style="text-align: left;">참조번호</td>
<td style="text-align: left;">105</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25DC00076604</td>
<td style="text-align: left;">조달청 입찰공고의 경우 참조공고번호는 자체 전자조달시스템에서 관리하는 공고번호를 의미하며 자체전자조달시스템의 경우 참조공고번호는 나라장터(G2B) 입찰공고번호를 의미함</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNm</td>
<td style="text-align: left;">입찰공고명</td>
<td style="text-align: left;">1000</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">전기 회전제어시스템용 복합환경 성능평가 시스템</td>
<td style="text-align: left;">공사명 또는 사업명이라고도 하며 입찰공고 내용을 요약한 이름</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttCd</td>
<td style="text-align: left;">공고기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">1230000</td>
<td style="text-align: left;">공고를 하는 기관의 코드로 행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드가 행자부코드가 없는 경우 조달청에서 부여한 공고기관 코드가 표기됨</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttNm</td>
<td style="text-align: left;">공고기관명</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">조달청</td>
<td style="text-align: left;">수요기관의 의뢰를 받아 공고하는 기관의 명</td>
</tr>
<tr>
<td style="text-align: left;">dminsttCd</td>
<td style="text-align: left;">수요기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">Z005460</td>
<td style="text-align: left;">실제 수요기관의 코드로 행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드가 행자부코드가 없는 경우 조달청에서 부여한 수요기관 코드가 표기됨</td>
</tr>
<tr>
<td style="text-align: left;">dminsttNm</td>
<td style="text-align: left;">수요기관명</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">한국자동차연구원</td>
<td style="text-align: left;">중앙조달인 경우 조달사업에 관한 법률 제2조(정의)에 따라 수요물자의 구매 공급 또는 시설공사 계약의 체결을 조달청장에게 요청할 수 있도록 조달청장이 인정하여 등록한 기관 또는 자체전자조달시스템을 이용하는 기관인 경우 계약을 의뢰한 기관의 명으로 공고기관과 수요기관이 동일할 수 있음</td>
</tr>
<tr>
<td style="text-align: left;">bidMethdNm</td>
<td style="text-align: left;">입찰방식명</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">전자입찰</td>
<td style="text-align: left;">공고의 입찰방식명 직찰<br />
전자입찰,전자입찰/직찰,전자/직찰/우편/상시,직찰/우편/상시,우편/상시,전자시담,복수견적(역경매),직찰/우편,전자시담(다자간)</td>
</tr>
<tr>
<td style="text-align: left;">cntrctCnclsMthdNm</td>
<td style="text-align: left;">계약체결방법명</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">일반경쟁</td>
<td style="text-align: left;">계약체결의 방법을 구분하는 명<br />
*일반경쟁계약은 계약 대상 물품의 규격 및 시방서와 계약조건 등을 널리 공고하여 일정한 자격을 가진 불특정 다수인의 입찰희망자를 모두 경쟁 입찰하는 계약방법<br />
*제한경쟁계약은 일반·지명경쟁계약제도의 단점을 보완하기 위해 실적제한, 기술보유제한, 특정물품제한, 지역제한 등을 두는 계약방법<br />
*지명경쟁계약은 계약상대자의 신용과 실적 등에 있어 적당하다고 인정하는 특정 다수의 경쟁 참가자를 지명하여 계약 상대방을 결정하는 계약방법<br />
*수의계약은 계약상대자를 결정함에 있어 경쟁방법에 의하지 않고 특정인을 선정하여 계약하는 계약방법</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttOfclNm</td>
<td style="text-align: left;">공고기관담당자명</td>
<td style="text-align: left;">35</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">김하연</td>
<td style="text-align: left;">공고기관의 공고를 담당하는 담당자의 명</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttOfclTelNo</td>
<td style="text-align: left;">공고기관담당자전화번호</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">042-724-7540</td>
<td style="text-align: left;">공고기관의 공고를 담당하는 담당자의 전화번호</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttOfclEmailAdrs</td>
<td style="text-align: left;">공고기관담당자이메일주소</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">hypps@korea.kr</td>
<td style="text-align: left;">공고기관의 공고를 담당하는 담당자의 이메일주소</td>
</tr>
<tr>
<td style="text-align: left;">exctvNm</td>
<td style="text-align: left;">집행관명</td>
<td style="text-align: left;">35</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">김하연</td>
<td style="text-align: left;">공고의 집행관명</td>
</tr>
<tr>
<td style="text-align: left;">bidQlfctRgstDt</td>
<td style="text-align: left;">입찰참가자격등록마감일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-08-11 18:00</td>
<td style="text-align: left;">입찰참가등록이란 입찰사무를 효과적으로 집행하기 위하여 사전에 입찰참가자격등록을 해두었다가 필요 시 입찰에 참여하는 제도로 해당 공고에 대한 입찰참가자격의 등록이 완료되어야 하는 시점을 의미함 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">cmmnSpldmdAgrmntRcptdocMethd</td>
<td style="text-align: left;">공동수급협정서접수방식</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">공고서참조</td>
<td style="text-align: left;">공동수급협정서의 접수방식"전자","수기","없음","공고서참고"</td>
</tr>
<tr>
<td style="text-align: left;">cmmnSpldmdAgrmntClseDt</td>
<td style="text-align: left;">공동수급협정마감일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-08-11 18:00</td>
<td style="text-align: left;">공동계약이 허용된 공고에 대해 공동수급체를 구성하여 입찰에 참여하고자 할 경우 구성원이 일정 분담내용에 따라 나누어 공동으로 이행하는 약속을 한 공동수급협정서를 작성하여야 하며 이때 공동수급협정서의 등록(작성) 마감 시점을 의미함”YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">cmmnSpldmdCorpRgnLmtYn</td>
<td style="text-align: left;">공동수급업체지역제한여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">공동수급협정시 구성원의 지역제한을 적용할지 여부. 지역제한인경우 협정 구성업체가 참가제한지역에 포함되어야 함.(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">bidBeginDt</td>
<td style="text-align: left;">입찰개시일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-18 13:00:00</td>
<td style="text-align: left;">입찰서의 제출을 개시하는 일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">bidClseDt</td>
<td style="text-align: left;">입찰마감일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-08-12 10:00:00</td>
<td style="text-align: left;">입찰서의 제출을 마감하는 일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">opengDt</td>
<td style="text-align: left;">개찰일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-08-12 15:00:00</td>
<td style="text-align: left;">집행관이 개찰을 수행할 수 있는 시작일시이며<br />
개찰일시 이후에 개찰이 가능함<br />
실제 개찰을 수행한 시간을 의미하지 않음 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl1</td>
<td style="text-align: left;">공고규격서URL1</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00964371&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=1 &amp;prcmBsneSeCd=02</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl2</td>
<td style="text-align: left;">공고규격서URL2</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00964371&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=2 &amp;prcmBsneSeCd=02</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl3</td>
<td style="text-align: left;">공고규격서URL3</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00964371&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=3 &amp;prcmBsneSeCd=02</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl4</td>
<td style="text-align: left;">공고규격서URL4</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00964371&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=4 &amp;prcmBsneSeCd=02</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl5</td>
<td style="text-align: left;">공고규격서URL5</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00964371&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=5 &amp;prcmBsneSeCd=02</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl6</td>
<td style="text-align: left;">공고규격서URL6</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00964371&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=6 &amp;prcmBsneSeCd=02</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl7</td>
<td style="text-align: left;">공고규격서URL7</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00964371&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=7 &amp;prcmBsneSeCd=02</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl8</td>
<td style="text-align: left;">공고규격서URL8</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00964371&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=8 &amp;prcmBsneSeCd=02</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl9</td>
<td style="text-align: left;">공고규격서URL9</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00964371&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=9 &amp;prcmBsneSeCd=02</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl10</td>
<td style="text-align: left;">공고규격서URL10</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00964371&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=10 &amp;prcmBsneSeCd=02</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm1</td>
<td style="text-align: left;">공고규격파일명1</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">공급자증명서 양식 및 작성요령.hwp</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm2</td>
<td style="text-align: left;">공고규격파일명2</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">해외공급자 계약서 서명권한 위임장(양식).hwp</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm3</td>
<td style="text-align: left;">공고규격파일명3</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">구매규격서.hwp</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm4</td>
<td style="text-align: left;">공고규격파일명4</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">제안요청서.hwp</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm5</td>
<td style="text-align: left;">공고규격파일명5</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25BK00964371-000_20250717143009_외자공고서_D02.htm</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm6</td>
<td style="text-align: left;">공고규격파일명6</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25BK00964371-000_20250717143009_SUMMARY_OF_BIDDING_D03.htm</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm7</td>
<td style="text-align: left;">공고규격파일명7</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">구매규격서7.hwp</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm8</td>
<td style="text-align: left;">공고규격파일명8</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">구매규격서8.hwp</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm9</td>
<td style="text-align: left;">공고규격파일명9</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">구매규격서8.hwp</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm10</td>
<td style="text-align: left;">공고규격파일명10</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">구매규격서10.hwp</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">rbidPermsnYn</td>
<td style="text-align: left;">재입찰허용여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">입찰이 유찰되는 경우 재공고 없이 다시 입찰(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">prdctClsfcLmtYn</td>
<td style="text-align: left;">물품분류제한여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">Y</td>
<td style="text-align: left;">물품공고의 경우 물품분류번호로 제한할 경우 Y, 물품분류번호 제한없으면 N</td>
</tr>
<tr>
<td style="text-align: left;">mnfctYn</td>
<td style="text-align: left;">제조여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">물품분류로 투찰제한시 제조물품으로 제한할 지 여부. "Y"일 경우 투찰시 업체의 경쟁입찰참가자격등록증에 공고서상 물품분류가 제조물품으로 등록되어 있어야 투찰가능(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">prearngPrceDcsnMthdNm</td>
<td style="text-align: left;">예정가격결정방법명</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">비예가</td>
<td style="text-align: left;">예정가격의 결정을 위해 복수예정가격방식으로 산정하는지 단일 예정가격으로 산정하는지를 구분하는 명</td>
</tr>
<tr>
<td style="text-align: left;">totPrdprcNum</td>
<td style="text-align: left;">총예가건수</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">15</td>
<td style="text-align: left;">공고의 총예가건수</td>
</tr>
<tr>
<td style="text-align: left;">drwtPrdprcNum</td>
<td style="text-align: left;">추첨예가건수</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">공고의 추첨예가건수</td>
</tr>
<tr>
<td style="text-align: left;">asignBdgtAmt</td>
<td style="text-align: left;">배정예산금액</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">50000000</td>
<td style="text-align: left;">사업목적물을 달성하기 위하여 배정된 예산액 또는 설계금액(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">presmptPrce</td>
<td style="text-align: left;">추정가격</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">75833</td>
<td style="text-align: left;">물품/공사/용역 등의 조달 계약을 체결함에 있어 국제입찰 대상여부를 판단하는 기준 등으로 삼기 위하여 예정가격이 결정되기 전에 예산에 계상된 금액 등을 기준으로 하여 부가가치세 및 조달 수수료를 제외한 금액(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">opengPlce</td>
<td style="text-align: left;">개찰장소</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">국가종합전자조달시스템(나라장터)</td>
<td style="text-align: left;">집행관이 개찰을 하는 장소</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceDtlUrl</td>
<td style="text-align: left;">입찰공고상세URL</td>
<td style="text-align: left;">512</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/link/PNPE027_01/single/?bidPbancNo=R25BK00964371&amp;bidPbancOrd=000</td>
<td style="text-align: left;">나라장터시스템의 입찰공고 상세화면 링크</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceUrl</td>
<td style="text-align: left;">입찰공고URL</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/link/PNPE027_01/single/?bidPbancNo=R25BK00964371&amp;bidPbancOrd=000</td>
<td style="text-align: left;">해당 입찰공고를 인터넷상에서 확인할 수 있는 URL주소</td>
</tr>
<tr>
<td style="text-align: left;">bidPrtcptFeePaymntYn</td>
<td style="text-align: left;">입찰참가수수료납부여부</td>
<td style="text-align: left;">30</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">전자납부허용</td>
<td style="text-align: left;">입찰참가 의사가 있는 자가 납부하여야하는 수수료의 유무 및 납부방법을 표기하는 것으로 "전자납부, 수기 및 전자납부, 수기, 없음"으로 표기</td>
</tr>
<tr>
<td style="text-align: left;">bidPrtcptFee</td>
<td style="text-align: left;">입찰참가수수료</td>
<td style="text-align: left;">21</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">10000</td>
<td style="text-align: left;">입찰에 참가하기위해 납부하는 수수료(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">bidGrntymnyPaymntYn</td>
<td style="text-align: left;">입찰보증금납부여부</td>
<td style="text-align: left;">30</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">전자납부허용</td>
<td style="text-align: left;">입찰보증금을 나라장터에서 전자로 납부가능하게 할지 여부 “전자납부허용”,”불허’으로 표기</td>
</tr>
<tr>
<td style="text-align: left;">crdtrNm</td>
<td style="text-align: left;">채권자명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">조달청장</td>
<td style="text-align: left;">입찰보증금 항목의 "보증채권자명"으로 전자입찰보증 접수시 사용</td>
</tr>
<tr>
<td style="text-align: left;">prdctSno</td>
<td style="text-align: left;">물품순번</td>
<td style="text-align: left;">6</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">공고의 물품목록순번</td>
</tr>
<tr>
<td style="text-align: left;">dtilPrdctClsfcNo</td>
<td style="text-align: left;">세부품명번호</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">4111450101</td>
<td style="text-align: left;">물품분류번호(8자리) + 물품식별번호(앞2자리) [물품목록정보의 관리 및 이용에 관한 규정 제12조]</td>
</tr>
<tr>
<td style="text-align: left;">dtilPrdctClsfcNoNm</td>
<td style="text-align: left;">세부품명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">동력계</td>
<td style="text-align: left;">세부품명번호 10자리에 대한 한글명</td>
</tr>
<tr>
<td style="text-align: left;">prdctSpecNm</td>
<td style="text-align: left;">물품규격명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">동력계</td>
<td style="text-align: left;">공고의 물품규격명</td>
</tr>
<tr>
<td style="text-align: left;">prdctQty</td>
<td style="text-align: left;">물품수량</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">공고의 물품수량</td>
</tr>
<tr>
<td style="text-align: left;">prdctUnit</td>
<td style="text-align: left;">물품단위</td>
<td style="text-align: left;">30</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">SET</td>
<td style="text-align: left;">공고의 물품단위</td>
</tr>
<tr>
<td style="text-align: left;">prdctUprc</td>
<td style="text-align: left;">물품단가</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">공고의 물품단가</td>
</tr>
<tr>
<td style="text-align: left;">dlvrTmlmtDt</td>
<td style="text-align: left;">납품기한일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-11-02 12:14:58</td>
<td style="text-align: left;">공고의 납품기한일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">dlvrDaynum</td>
<td style="text-align: left;">납품일수</td>
<td style="text-align: left;">5</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">30</td>
<td style="text-align: left;">공고의 납품일수</td>
</tr>
<tr>
<td style="text-align: left;">dlvryCndtnNm</td>
<td style="text-align: left;">인도조건명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">FCA</td>
<td style="text-align: left;">인도 받을 장소</td>
</tr>
<tr>
<td style="text-align: left;">purchsObjPrdctList</td>
<td style="text-align: left;">구매대상물품목록</td>
<td style="text-align: left;">4000</td>
<td style="text-align: left;">0..n</td>
<td style="text-align: left;">[1^4111450101^동력계]</td>
<td style="text-align: left;">공고의 구매대상물품목록으로 [입찰분류번호^세부품명번호(세부물품분류번호)^세부품명(세부물품분류명)],[입찰분류번호^세부품명번호(세부물품분류번호)^세부품명(세부물품분류명)] 제공</td>
</tr>
<tr>
<td style="text-align: left;">untyNtceNo</td>
<td style="text-align: left;">통합공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25BM00325017</td>
<td style="text-align: left;">입찰공고를 구분하는 번호로 입찰공고번호이며 형식은 년도(4)+월(2)+순번(5)<br />
*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성<br />
- 단계구분: BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격), BK(통합입찰)</td>
</tr>
<tr>
<td style="text-align: left;">cmmnSpldmdMethdCd</td>
<td style="text-align: left;">공동수급방식코드</td>
<td style="text-align: left;">15</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">공500004</td>
<td style="text-align: left;">공동수급이라 함은 구성원을 2인 이상으로 하여 수급인이 해당계약을 공동으로 수행하기 위하여 잠정적으로 결성한 실체를 의미하며 공동수급체가도급을 받아 이행하는 방식을 구분하는 코드로<br />
공500001 : 공동이행<br />
공500002 : 분담이행<br />
공500003 : 주계약자관리방식<br />
공500004 : 단독계약<br />
공500005 : 혼합방식<br />
공500006 : 공동이행 또는 분담이행<br />
공500007 : 혼합_단독<br />
공500008 : 혼합_공동<br />
공500012 : 해당없음으로 구분됨</td>
</tr>
<tr>
<td style="text-align: left;">cmmnSpldmdMethdNm</td>
<td style="text-align: left;">공동수급방식명</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">()공동수급불허</td>
<td style="text-align: left;">공동수급이라 함은 구성원을 2인 이상으로 하여 수급인이 해당계약을 공동으로 수행하기 위하여 잠정적으로 결성한 실체를 의미하며 공동수급체가도급을 받아 이행하는 방식을 구분하는 명임</td>
</tr>
<tr>
<td style="text-align: left;">stdNtceDocUrl</td>
<td style="text-align: left;">표준공고서URL</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00964371&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=5 &amp;prcmBsneSeCd=02</td>
<td style="text-align: left;">공고의 표준공고문URL</td>
</tr>
<tr>
<td style="text-align: left;">brffcBidprcPermsnYn</td>
<td style="text-align: left;">지사투찰허용여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">지역제한 공고에 한해서 지사 투찰을 허용할지 여부. 투찰제어시 사용(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">dsgntCmptYn</td>
<td style="text-align: left;">지명경쟁여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">공고의 지명경쟁여부(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">rsrvtnPrceReMkngMthdNm</td>
<td style="text-align: left;">예비가격재작성방법명</td>
<td style="text-align: left;">50</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">재입찰시 기존 예비가격을 사용하여 예정가격이 산정됩니다.</td>
<td style="text-align: left;">공고의 예비가격재작성방법명</td>
</tr>
<tr>
<td style="text-align: left;">arsltApplDocRcptMthdNm</td>
<td style="text-align: left;">실적신청서접수방법명</td>
<td style="text-align: left;">50</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">전자문서</td>
<td style="text-align: left;">공고의 실적신청서접수방법명</td>
</tr>
<tr>
<td style="text-align: left;">arsltApplDocRcptDt</td>
<td style="text-align: left;">실적신청서접수일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-17 16:19:29</td>
<td style="text-align: left;">실적심사신청서 접수마감일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">orderPlanUntyNo</td>
<td style="text-align: left;">발주계획통합번호</td>
<td style="text-align: left;">35</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25DD20301690</td>
<td style="text-align: left;">*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성<br />
- 단계구분: BK(입찰)<br />
TA(계약)<br />
DD:(발주계획)<br />
BD(사전규격),<br />
BK(통합입찰)</td>
</tr>
<tr>
<td style="text-align: left;">sucsfbidLwltRate</td>
<td style="text-align: left;">낙찰하한율</td>
<td style="text-align: left;">22</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">87.745</td>
<td style="text-align: left;">개찰시 사용하는 낙찰하한율(%)</td>
</tr>
<tr>
<td style="text-align: left;">rgstDt</td>
<td style="text-align: left;">등록일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">2025-07-17 16:19:29</td>
<td style="text-align: left;">공고의 등록일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">bfSpecRgstNo</td>
<td style="text-align: left;">사전규격등록번호</td>
<td style="text-align: left;">17</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25BD00089809</td>
<td style="text-align: left;">*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성<br />
- 단계구분: BK(입찰)<br />
TA(계약)<br />
DD:(발주계획)<br />
BD(사전규격),<br />
BK(통합입찰)</td>
</tr>
<tr>
<td style="text-align: left;">sucsfbidMthdCd</td>
<td style="text-align: left;">낙찰방법코드</td>
<td style="text-align: left;">9</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">낙030021</td>
<td style="text-align: left;">낙찰방법명에 대한 코드 (한글 1자리 + 숫자 6자리)</td>
</tr>
<tr>
<td style="text-align: left;">sucsfbidMthdNm</td>
<td style="text-align: left;">낙찰방법명</td>
<td style="text-align: left;">700</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">협상에의한계약</td>
<td style="text-align: left;">낙찰자를 결정하는 방법-낙찰방법 세부기준</td>
</tr>
<tr>
<td style="text-align: left;">chgDt</td>
<td style="text-align: left;">변경일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-20 16:19:29</td>
<td style="text-align: left;">공고의 변경일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">dminsttOfclEmailAdrs</td>
<td style="text-align: left;">수요기관담당자이메일주소</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">@</td>
<td style="text-align: left;">수요기관 담당자의 이메일주소</td>
</tr>
<tr>
<td style="text-align: left;">indstrytyLmtYn</td>
<td style="text-align: left;">업종제한여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">Y</td>
<td style="text-align: left;">해당 공고 입찰 시 업종(면허)제한을 두는지의 여부<br />
예시)Y</td>
</tr>
<tr>
<td style="text-align: left;">chgNtceRsn</td>
<td style="text-align: left;">변경공고사유</td>
<td style="text-align: left;">4000</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">원화금액 수정</td>
<td style="text-align: left;">공고종류명(공고의 공고상태명) 이 변경일 경우 변경공고사유 , 취소일 경우 취소공고사유</td>
</tr>
<tr>
<td style="text-align: left;">rbidOpengDt</td>
<td style="text-align: left;">재입찰개찰일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-08-12 15:00:00</td>
<td style="text-align: left;">공고종류명이 ‘재입찰’ 일 경우 재입찰공고의 개찰을 수행할 수 있는 시작일시<br />
“YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">bidWgrnteeRcptClseDt</td>
<td style="text-align: left;">입찰보증서접수마감일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-08-11 10:00:00</td>
<td style="text-align: left;">입찰보증서접수마감일시</td>
</tr>
<tr>
<td style="text-align: left;">techAbltEvlRt</td>
<td style="text-align: left;">기술능력평가비율</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">80</td>
<td style="text-align: left;">협상에 의한 낙찰자 결정의 경우 기술능력 평가 비율</td>
</tr>
<tr>
<td style="text-align: left;">bidPrceEvlRt</td>
<td style="text-align: left;">입찰가격평가비율</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">협상에 의한 낙찰자 결정의 경우 기술능력 입찰가격 평가 비율</td>
</tr>
<tr>
<td style="text-align: left;">sucsfbidMthdAppStd</td>
<td style="text-align: left;">낙찰방법적용기준</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">조달청 시설공사 적격심사세부기준</td>
<td style="text-align: left;"><p>낙찰자를 결정하</p>
<p>방법 적용기준</p></td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 요청 / 응답 메시지 예제

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr>
<td style="text-align: center;"><strong>REST(URI)</strong></td>
</tr>
<tr>
<td style="text-align: center;">http://apis.data.go.kr/1230000/ad/BidPublicInfoService/getBidPblancListInfoFrgcpt/ad/BidPublicInfoService/getBidPblancListInfoFrgcpt?type=&amp;inqryDiv=2&amp;numOfRows=10&amp;pageNo=1&amp;bidNtceNo=R25BK00964371&amp;ServiceKey=인증키</td>
</tr>
<tr>
<td style="text-align: center;"><strong>응답 메시지</strong></td>
</tr>
<tr>
<td style="text-align: left;"><p>&lt;response&gt;</p>
<p>&lt;header&gt;</p>
<p>&lt;resultCode&gt;00&lt;/resultCode&gt;</p>
<p>&lt;resultMsg&gt;정상&lt;/resultMsg&gt;</p>
<p>&lt;/header&gt;</p>
<p>&lt;body&gt;</p>
<p>&lt;items&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00963966&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;reNtceYn&gt;N&lt;/reNtceYn&gt;</p>
<p>&lt;rgstTyNm&gt;조달청 또는 나라장터 자체 공고건&lt;/rgstTyNm&gt;</p>
<p>&lt;ntceKindNm&gt;등록공고&lt;/ntceKindNm&gt;</p>
<p>&lt;intrbidYn&gt;Y&lt;/intrbidYn&gt;</p>
<p>&lt;bidNtceDt&gt;2025-07-16 20:12:30&lt;/bidNtceDt&gt;</p>
<p>&lt;refNo&gt;한국공항공사 본사 제2025-87호&lt;/refNo&gt;</p>
<p>&lt;bidNtceNm&gt;엑스선검색장비(소형)&lt;/bidNtceNm&gt;</p>
<p>&lt;ntceInsttCd&gt;B551178&lt;/ntceInsttCd&gt;</p>
<p>&lt;ntceInsttNm&gt;한국공항공사&lt;/ntceInsttNm&gt;</p>
<p>&lt;dminsttCd&gt;B551178&lt;/dminsttCd&gt;</p>
<p>&lt;dminsttNm&gt;한국공항공사&lt;/dminsttNm&gt;</p>
<p>&lt;bidMethdNm&gt;전자입찰&lt;/bidMethdNm&gt;</p>
<p>&lt;cntrctCnclsMthdNm&gt;일반경쟁&lt;/cntrctCnclsMthdNm&gt;</p>
<p>&lt;ntceInsttOfclNm&gt;정재우&lt;/ntceInsttOfclNm&gt;</p>
<p>&lt;ntceInsttOfclTelNo&gt;02-2660-2433&lt;/ntceInsttOfclTelNo&gt;</p>
<p>&lt;ntceInsttOfclEmailAdrs&gt;jaywoo@airport.co.kr&lt;/ntceInsttOfclEmailAdrs&gt;</p>
<p>&lt;exctvNm&gt;정재우&lt;/exctvNm&gt;</p>
<p>&lt;bidQlfctRgstDt&gt;2025-08-08 18:00&lt;/bidQlfctRgstDt&gt;</p>
<p>&lt;cmmnSpldmdAgrmntRcptdocMethd&gt;공고서참고&lt;/cmmnSpldmdAgrmntRcptdocMethd&gt;</p>
<p>&lt;cmmnSpldmdAgrmntClseDt&gt;&lt;/cmmnSpldmdAgrmntClseDt&gt;</p>
<p>&lt;cmmnSpldmdCorpRgnLmtYn&gt;&lt;/cmmnSpldmdCorpRgnLmtYn&gt;</p>
<p>&lt;bidBeginDt&gt;2025-08-07 10:00:00&lt;/bidBeginDt&gt;</p>
<p>&lt;bidClseDt&gt;2025-08-11 10:00:00&lt;/bidClseDt&gt;</p>
<p>&lt;opengDt&gt;2025-08-11 11:00:00&lt;/opengDt&gt;</p>
<p>&lt;ntceSpecDocUrl1&gt;https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00963966&amp;amp;bidPbancOrd=000&amp;amp;fileType=&amp;amp;fileSeq=1 &amp;prcmBsneSeCd=02&lt;/ntceSpecDocUrl1&gt;</p>
<p>&lt;ntceSpecDocUrl2&gt;https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00963966&amp;amp;bidPbancOrd=000&amp;amp;fileType=&amp;amp;fileSeq=2 &amp;prcmBsneSeCd=02&lt;/ntceSpecDocUrl2&gt;</p>
<p>&lt;ntceSpecDocUrl3&gt;https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00963966&amp;amp;bidPbancOrd=000&amp;amp;fileType=&amp;amp;fileSeq=3 &amp;prcmBsneSeCd=02&lt;/ntceSpecDocUrl3&gt;</p>
<p>&lt;ntceSpecDocUrl4&gt;https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00963966&amp;amp;bidPbancOrd=000&amp;amp;fileType=&amp;amp;fileSeq=4 &amp;prcmBsneSeCd=02&lt;/ntceSpecDocUrl4&gt;</p>
<p>&lt;ntceSpecDocUrl5&gt;https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00963966&amp;amp;bidPbancOrd=000&amp;amp;fileType=&amp;amp;fileSeq=5 &amp;prcmBsneSeCd=02&lt;/ntceSpecDocUrl5&gt;</p>
<p>&lt;ntceSpecDocUrl6&gt;&lt;/ntceSpecDocUrl6&gt;</p>
<p>&lt;ntceSpecDocUrl7&gt;&lt;/ntceSpecDocUrl7&gt;</p>
<p>&lt;ntceSpecDocUrl8&gt;&lt;/ntceSpecDocUrl8&gt;</p>
<p>&lt;ntceSpecDocUrl9&gt;&lt;/ntceSpecDocUrl9&gt;</p>
<p>&lt;ntceSpecDocUrl10&gt;&lt;/ntceSpecDocUrl10&gt;</p>
<p>&lt;ntceSpecFileNm1&gt;(2025-87)_English_Summary.docx&lt;/ntceSpecFileNm1&gt;</p>
<p>&lt;ntceSpecFileNm2&gt;(2025-87)입찰공고문(2025년 엑스선 검색장비(소형) 통합구매).hwp&lt;/ntceSpecFileNm2&gt;</p>
<p>&lt;ntceSpecFileNm3&gt;붙임3. 입찰안내서(2025년 엑스선 검색장비(소형) 통합구매).hwp&lt;/ntceSpecFileNm3&gt;</p>
<p>&lt;ntceSpecFileNm4&gt;붙임4. 2025년 엑스선 검색장비(소형) 제안요청서.hwp&lt;/ntceSpecFileNm4&gt;</p>
<p>&lt;ntceSpecFileNm5&gt;붙임5. 도급사업 안전보건 수준평가 평가기준(엑스선 검색장비_소형).hwp&lt;/ntceSpecFileNm5&gt;</p>
<p>&lt;ntceSpecFileNm6&gt;&lt;/ntceSpecFileNm6&gt;</p>
<p>&lt;ntceSpecFileNm7&gt;&lt;/ntceSpecFileNm7&gt;</p>
<p>&lt;ntceSpecFileNm8&gt;&lt;/ntceSpecFileNm8&gt;</p>
<p>&lt;ntceSpecFileNm9&gt;&lt;/ntceSpecFileNm9&gt;</p>
<p>&lt;ntceSpecFileNm10&gt;&lt;/ntceSpecFileNm10&gt;</p>
<p>&lt;rbidPermsnYn&gt;N&lt;/rbidPermsnYn&gt;</p>
<p>&lt;prdctClsfcLmtYn&gt;Y&lt;/prdctClsfcLmtYn&gt;</p>
<p>&lt;mnfctYn&gt;&lt;/mnfctYn&gt;</p>
<p>&lt;prearngPrceDcsnMthdNm&gt;비예가&lt;/prearngPrceDcsnMthdNm&gt;</p>
<p>&lt;totPrdprcNum&gt;&lt;/totPrdprcNum&gt;</p>
<p>&lt;drwtPrdprcNum&gt;&lt;/drwtPrdprcNum&gt;</p>
<p>&lt;asignBdgtAmt&gt;&lt;/asignBdgtAmt&gt;</p>
<p>&lt;presmptPrce&gt;&lt;/presmptPrce&gt;</p>
<p>&lt;opengPlce&gt;국가종합전자조달시스템(나라장터)&lt;/opengPlce&gt;</p>
<p>&lt;bidNtceDtlUrl&gt;https://www.g2b.go.kr/link/PNPE027_01/single/?bidPbancNo=R25BK00963966&amp;bidPbancOrd=000&lt;/bidNtceDtlUrl&gt;</p>
<p>&lt;bidNtceUrl&gt; https://www.g2b.go.kr/link/PNPE027_01/single/?bidPbancNo=R25BK00963966&amp;bidPbancOrd=000&lt;/bidNtceUrl&gt;</p>
<p>&lt;bidPrtcptFeePaymntYn&gt;&lt;/bidPrtcptFeePaymntYn&gt;</p>
<p>&lt;bidPrtcptFee&gt;&lt;/bidPrtcptFee&gt;</p>
<p>&lt;bidGrntymnyPaymntYn&gt;전자납부허용&lt;/bidGrntymnyPaymntYn&gt;</p>
<p>&lt;crdtrNm&gt;한국공항공사 사장&lt;/crdtrNm&gt;</p>
<p>&lt;prdctSno&gt;1&lt;/prdctSno&gt;</p>
<p>&lt;dtilPrdctClsfcNo&gt;4617162401&lt;/dtilPrdctClsfcNo&gt;</p>
<p>&lt;dtilPrdctClsfcNoNm&gt;엑스레이화물검색기&lt;/dtilPrdctClsfcNoNm&gt;</p>
<p>&lt;prdctSpecNm&gt;&lt;/prdctSpecNm&gt;</p>
<p>&lt;prdctQty&gt;8&lt;/prdctQty&gt;</p>
<p>&lt;prdctUnit&gt;EA&lt;/prdctUnit&gt;</p>
<p>&lt;prdctUprc&gt;1262140000&lt;/prdctUprc&gt;</p>
<p>&lt;dlvrTmlmtDt&gt;&lt;/dlvrTmlmtDt&gt;</p>
<p>&lt;dlvrDaynum&gt;&lt;/dlvrDaynum&gt;</p>
<p>&lt;dlvryCndtnNm&gt;&lt;/dlvryCndtnNm&gt;</p>
<p>&lt;purchsObjPrdctList&gt;[1^4617162401^엑스레이화물검색기]&lt;/purchsObjPrdctList&gt;</p>
<p>&lt;untyNtceNo&gt;R25BM00323571&lt;/untyNtceNo&gt;</p>
<p>&lt;cmmnSpldmdMethdCd&gt;&lt;/cmmnSpldmdMethdCd&gt;</p>
<p>&lt;cmmnSpldmdMethdNm&gt;()공동수급불허&lt;/cmmnSpldmdMethdNm&gt;</p>
<p>&lt;stdNtceDocUrl&gt;https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00963966&amp;amp;bidPbancOrd=000&amp;amp;fileType=&amp;amp;fileSeq=2 &amp;prcmBsneSeCd=02&lt;/stdNtceDocUrl&gt;</p>
<p>&lt;brffcBidprcPermsnYn&gt;&lt;/brffcBidprcPermsnYn&gt;</p>
<p>&lt;dsgntCmptYn&gt;N&lt;/dsgntCmptYn&gt;</p>
<p>&lt;rsrvtnPrceReMkngMthdNm&gt;&lt;/rsrvtnPrceReMkngMthdNm&gt;</p>
<p>&lt;arsltApplDocRcptMthdNm&gt;&lt;/arsltApplDocRcptMthdNm&gt;</p>
<p>&lt;arsltApplDocRcptDt&gt;&lt;/arsltApplDocRcptDt&gt;</p>
<p>&lt;orderPlanUntyNo&gt;R25DD20329612&lt;/orderPlanUntyNo&gt;</p>
<p>&lt;sucsfbidLwltRate&gt;&lt;/sucsfbidLwltRate&gt;</p>
<p>&lt;rgstDt&gt;2025-07-16 20:12:30&lt;/rgstDt&gt;</p>
<p>&lt;bfSpecRgstNo&gt;R25BD00076155&lt;/bfSpecRgstNo&gt;</p>
<p>&lt;sucsfbidMthdCd&gt;낙030005&lt;/sucsfbidMthdCd&gt;</p>
<p>&lt;sucsfbidMthdNm&gt;협상에의한계약&lt;/sucsfbidMthdNm&gt;</p>
<p>&lt;chgDt&gt;&lt;/chgDt&gt;</p>
<p>&lt;dminsttOfclEmailAdrs&gt;&lt;/dminsttOfclEmailAdrs&gt;</p>
<p>&lt;indstrytyLmtYn&gt;&lt;/indstrytyLmtYn&gt;</p>
<p>&lt;chgNtceRsn&gt;&lt;/chgNtceRsn&gt;</p>
<p>&lt;rbidOpengDt&gt;2025-08-11 11:00:00&lt;/rbidOpengDt&gt;</p>
<p>&lt;bidWgrnteeRcptClseDt&gt;2025-08-11 10:00:00&lt;/bidWgrnteeRcptClseDt&gt;</p>
<p>&lt;techAbltEvlRt&gt;90&lt;/techAbltEvlRt&gt;</p>
<p>&lt;bidPrceEvlRt&gt;10&lt;/bidPrceEvlRt&gt;</p>
<p>&lt;sucsfbidMthdAppStd&gt;&lt;/sucsfbidMthdAppStd&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;/items&gt;</p>
<p>&lt;numOfRows&gt;999&lt;/numOfRows&gt;</p>
<p>&lt;pageNo&gt;1&lt;/pageNo&gt;</p>
<p>&lt;totalCount&gt;1&lt;/totalCount&gt;</p>
<p>&lt;/body&gt;</p>
<p>&lt;/response&gt;</p></td>
</tr>
</tbody>
</table>

#### \
\[입찰공고목록 정보에 대한 물품조회\] 오퍼레이션 명세

<table>
<colgroup>
<col style="width: 4%" />
<col style="width: 21%" />
<col style="width: 17%" />
<col style="width: 21%" />
<col style="width: 2%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr>
<td rowspan="6">오퍼레이션 정보</td>
<td>오퍼레이션 번호</td>
<td>4</td>
<td>오퍼레이션명(국문)</td>
<td colspan="2">입찰공고목록 정보에 대한 물품조회</td>
</tr>
<tr>
<td>오퍼레이션 유형</td>
<td>조회(목록)</td>
<td>오퍼레이션명(영문)</td>
<td colspan="2">getBidPblancListInfoThng</td>
</tr>
<tr>
<td>오퍼레이션 설명</td>
<td colspan="4">검색조건에 등록일시, 입찰공고번호, 변경일시를 입력하여 나라장터의 입찰공고번호, 공고명, 발주기관, 수요기관, 계약체결방법명 등 물품부분의 입찰공고정보를 조회함</td>
</tr>
<tr>
<td>Call Back URL</td>
<td colspan="4">N/A</td>
</tr>
<tr>
<td>최대 메시지 사이즈</td>
<td colspan="4">[ 4000bytes]</td>
</tr>
<tr>
<td>평균 응답 시간</td>
<td>[ 500 ms]</td>
<td colspan="2">초당 최대 트랜잭션</td>
<td>[ 30 tps]</td>
</tr>
</tbody>
</table>

##### 요청 메시지 명세

<table>
<colgroup>
<col style="width: 19%" />
<col style="width: 19%" />
<col style="width: 13%" />
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 21%" />
</colgroup>
<tbody>
<tr>
<td>항목명(영문)</td>
<td>항목명(국문)</td>
<td>항목크기</td>
<td>항목구분</td>
<td>샘플데이터</td>
<td>항목설명</td>
</tr>
<tr>
<td style="text-align: left;">numOfRows</td>
<td style="text-align: left;">한 페이지 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td style="text-align: left;">pageNo</td>
<td style="text-align: left;">페이지 번호</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">페이지 번호</td>
</tr>
<tr>
<td style="text-align: left;">ServiceKey</td>
<td style="text-align: left;">서비스키</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">공공데이터포탈에서 받은 인증키</td>
<td style="text-align: left;">공공데이터포탈에서 받은 인증키</td>
</tr>
<tr>
<td style="text-align: left;">type</td>
<td style="text-align: left;">타입</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">0</td>
<td>json</td>
<td>오픈API 리턴 타입을 JSON으로 받고 싶을 경우 'json' 으로 지정</td>
</tr>
<tr>
<td style="text-align: left;">inqryDiv</td>
<td style="text-align: left;">조회구분</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">검색하고자하는 조회구분<br />
1:등록일시 , 2.입찰공고번호 , 3.변경일시</td>
</tr>
<tr>
<td style="text-align: left;">inqryBgnDt</td>
<td style="text-align: left;">조회시작일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">202507010000</td>
<td style="text-align: left;">검색하고자하는 등록일시 또는 변경일시 조회시작일시 "YYYYMMDDHHMM"<br />
(조회구분 '1', '3' 선택시 필수)</td>
</tr>
<tr>
<td style="text-align: left;">inqryEndDt</td>
<td style="text-align: left;">조회종료일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">202507012359</td>
<td style="text-align: left;">검색하고자하는 등록일시 또는 변경일시 조회종료일시 "YYYYMMDDHHMM"<br />
(조회구분 '1', '3' 선택시 필수)</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNo</td>
<td style="text-align: left;">입찰공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25BK00940072</td>
<td style="text-align: left;">검색하고자 하는 입찰공고번호<br />
(조회구분 '2' 선택시 필수)</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 응답 메시지 명세

<table>
<colgroup>
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 13%" />
<col style="width: 11%" />
<col style="width: 14%" />
<col style="width: 19%" />
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
<td style="text-align: left;">resultCode</td>
<td style="text-align: left;">결과코드</td>
<td style="text-align: left;">2</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">00</td>
<td style="text-align: left;">결과코드</td>
</tr>
<tr>
<td style="text-align: left;">resultMsg</td>
<td style="text-align: left;">결과메세지</td>
<td style="text-align: left;">50</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">정상.</td>
<td style="text-align: left;">결과메세지</td>
</tr>
<tr>
<td style="text-align: left;">numOfRows</td>
<td style="text-align: left;">한 페이지 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td style="text-align: left;">pageNo</td>
<td style="text-align: left;">페이지 번호</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">페이지 수</td>
</tr>
<tr>
<td style="text-align: left;">totalCount</td>
<td style="text-align: left;">데이터 총 개수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">17</td>
<td style="text-align: left;">데이터 총개수</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNo</td>
<td style="text-align: left;">입찰공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">R25BK00940072</td>
<td style="text-align: left;"><p>입찰공고 관리번호이며 조달청나라장터 공고건의 형식은 년도(4)+월(2)+순번(5)이며 자체전자조달시스템 보유기관은 각 기관별 형식 별도 사용<br />
*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성<br />
- 단계구분: BK(입찰),</p>
<p>TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</p></td>
</tr>
<tr>
<td style="text-align: left;">bidNtceOrd</td>
<td style="text-align: left;">입찰공고차수</td>
<td style="text-align: left;">3</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">000</td>
<td style="text-align: left;">입찰공고차수는 해당 입찰공고에 대한 재공고 및 재입찰 등이 발생되었을 경우 증가되는 수</td>
</tr>
<tr>
<td style="text-align: left;">reNtceYn</td>
<td style="text-align: left;">재공고여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">본 입찰공고의 재공고 여부(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">rgstTyNm</td>
<td style="text-align: left;">등록유형명</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">조달청 또는 나라장터 자체 공고건</td>
<td style="text-align: left;">입찰공고가 "조달청 또는 나라장터 자체 공고건","'나라장터 기타 공고건"</td>
</tr>
<tr>
<td style="text-align: left;">ntceKindNm</td>
<td style="text-align: left;">공고종류명</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">등록공고</td>
<td style="text-align: left;">공고의 공고상태명으로 등록공고, 변경공고, 취소공고, 재공고 구분</td>
</tr>
<tr>
<td style="text-align: left;">intrbidYn</td>
<td style="text-align: left;">국제입찰여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">국제입찰대상인지의 여부를 나타내며 국제입찰 대상은 내외국인 또는 외국인을 대상으로 하여 물품, 공사 및 용역을 조달하기 위하여 행하는 입찰을 말하며 수의계약을 포함한다. 국가계약법 제4조에 의해 추정가격이 고시금액(국제입찰 적용 대상 기준금액으로 기획재정부장관 및 행정자치부장관이 매 2년마다 고시한 금액을 말하며 WTO 또는 양자간(FTA) 정부조달협정에 따르면 국제입찰 대상 기준 금액이 SDR(Special Drawing Rights:특별인출권) 통화단위로 되어 있어 주무부 장관이 이를 2년마다 원화로 환산하여 고시) 이상일 경우 국제입찰대상이 됨(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceDt</td>
<td style="text-align: left;">입찰공고일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-04 11:12:46</td>
<td style="text-align: left;">입찰공고서를 공고한 일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">refNo</td>
<td style="text-align: left;">참조번호</td>
<td style="text-align: left;">105</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">스키장 고객용 전자 물품보관함_2025</td>
<td style="text-align: left;">조달청 입찰공고의 경우 참조공고번호는 자체 전자조달시스템에서 관리하는 공고번호를 의미하며 자체전자조달시스템의 경우 참조공고번호는 나라장터(G2B) 입찰공고번호를 의미함</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNm</td>
<td style="text-align: left;">입찰공고명</td>
<td style="text-align: left;">1000</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">스키장 고객용 전자 물품보관함 구매</td>
<td style="text-align: left;">공사명 또는 사업명이라고도 하며 입찰공고 내용을 요약한 이름</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttCd</td>
<td style="text-align: left;">공고기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">1230145</td>
<td style="text-align: left;">공고를 하는 기관의 코드로 행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드가 행자부코드가 없는 경우 조달청에서 부여한 공고기관 코드가 표기됨</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttNm</td>
<td style="text-align: left;">공고기관명</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">조달청 강원지방조달청</td>
<td style="text-align: left;">수요기관의 의뢰를 받아 공고하는 기관의 명</td>
</tr>
<tr>
<td style="text-align: left;">dminsttCd</td>
<td style="text-align: left;">수요기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">Z003620</td>
<td style="text-align: left;">실제 수요기관의 코드로 행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드가 행자부코드가 없는 경우 조달청에서 부여한 수요기관 코드가 표기됨</td>
</tr>
<tr>
<td style="text-align: left;">dminsttNm</td>
<td style="text-align: left;">수요기관명</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">(주)강원랜드</td>
<td style="text-align: left;">중앙조달인 경우 조달사업에 관한 법률 제2조(정의)에 따라 수요물자의 구매 공급 또는 시설공사 계약의 체결을 조달청장에게 요청할 수 있도록 조달청장이 인정하여 등록한 기관 또는 자체전자조달시스템을 이용하는 기관인 경우 계약을 의뢰한 기관의 명으로 공고기관과 수요기관이 동일할 수 있음</td>
</tr>
<tr>
<td style="text-align: left;">bidMethdNm</td>
<td style="text-align: left;">입찰방식명</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">전자입찰</td>
<td style="text-align: left;">공고의 입찰방식명 직찰<br />
전자입찰,전자입찰/직찰,전자/직찰/우편/상시,직찰/우편/상시,우편/상시,전자시담,복수견적(역경매),직찰/우편,전자시담(다자간)</td>
</tr>
<tr>
<td style="text-align: left;">cntrctCnclsMthdNm</td>
<td style="text-align: left;">계약체결방법명</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">제한경쟁</td>
<td style="text-align: left;">계약체결의 방법을 구분하는 명<br />
*일반경쟁계약은 계약 대상 물품의 규격 및 시방서와 계약조건 등을 널리 공고하여 일정한 자격을 가진 불특정 다수인의 입찰희망자를 모두 경쟁 입찰하는 계약방법<br />
*제한경쟁계약은 일반·지명경쟁계약제도의 단점을 보완하기 위해 실적제한, 기술보유제한, 특정물품제한, 지역제한 등을 두는 계약방법<br />
*지명경쟁계약은 계약상대자의 신용과 실적 등에 있어 적당하다고 인정하는 특정 다수의 경쟁 참가자를 지명하여 계약 상대방을 결정하는 계약방법<br />
*수의계약은 계약상대자를 결정함에 있어 경쟁방법에 의하지 않고 특정인을 선정하여 계약하는 계약방법</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttOfclNm</td>
<td style="text-align: left;">공고기관담당자명</td>
<td style="text-align: left;">35</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">윤순제</td>
<td style="text-align: left;">공고기관의 공고를 담당하는 담당자의 명</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttOfclTelNo</td>
<td style="text-align: left;">공고기관담당자전화번호</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">070-4056-8424</td>
<td style="text-align: left;">공고기관의 공고를 담당하는 담당자의 전화번호</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttOfclEmailAdrs</td>
<td style="text-align: left;">공고기관담당자이메일주소</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">soongde@korea.kr</td>
<td style="text-align: left;">공고기관의 공고를 담당하는 담당자의 이메일주소</td>
</tr>
<tr>
<td style="text-align: left;">exctvNm</td>
<td style="text-align: left;">집행관명</td>
<td style="text-align: left;">35</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">이병규</td>
<td style="text-align: left;">공고의 집행관명</td>
</tr>
<tr>
<td style="text-align: left;">bidQlfctRgstDt</td>
<td style="text-align: left;">입찰참가자격등록마감일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-14 18:00</td>
<td style="text-align: left;">입찰참가등록이란 입찰사무를 효과적으로 집행하기 위하여 사전에 입찰참가자격등록을 해두었다가 필요 시 입찰에 참여하는 제도로 해당 공고에 대한 입찰참가자격의 등록이 완료되어야 하는 시점을 의미함 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">cmmnSpldmdAgrmntRcptdocMethd</td>
<td style="text-align: left;">공동수급협정서접수방식</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">없음</td>
<td style="text-align: left;">공동수급협정서의 접수방식"전자","수기","없음","공고서참고"</td>
</tr>
<tr>
<td style="text-align: left;">cmmnSpldmdAgrmntClseDt</td>
<td style="text-align: left;">공동수급협정마감일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-11 14:00:00</td>
<td style="text-align: left;">공동계약이 허용된 공고에 대해 공동수급체를 구성하여 입찰에 참여하고자 할 경우 구성원이 일정 분담내용에 따라 나누어 공동으로 이행하는 약속을 한 공동수급협정서를 작성하여야 하며 이때 공동수급협정서의 등록(작성) 마감 시점을 의미함”YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">cmmnSpldmdCorpRgnLmtYn</td>
<td style="text-align: left;">공동수급업체지역제한여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">공동수급협정시 구성원의 지역제한을 적용할지 여부. 지역제한인경우 협정 구성업체가 참가제한지역에 포함되어야 함.(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">bidBeginDt</td>
<td style="text-align: left;">입찰개시일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-11 14:00:00</td>
<td style="text-align: left;">입찰서의 제출을 개시하는 일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">bidClseDt</td>
<td style="text-align: left;">입찰마감일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-15 14:00:00</td>
<td style="text-align: left;">입찰서의 제출을 마감하는 일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">opengDt</td>
<td style="text-align: left;">개찰일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-15 15:00:00</td>
<td style="text-align: left;">집행관이 개찰을 수행할 수 있는 시작일시이며<br />
개찰일시 이후에 개찰이 가능함<br />
실제 개찰을 수행한 시간을 의미하지 않음 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl1</td>
<td style="text-align: left;">공고규격서URL1</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00940072&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=1&amp;prcmBsneSeCd=01</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl2</td>
<td style="text-align: left;">공고규격서URL2</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00940072&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=2&amp;prcmBsneSeCd=01</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl3</td>
<td style="text-align: left;">공고규격서URL3</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00940072&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=3&amp;prcmBsneSeCd=01</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl4</td>
<td style="text-align: left;">공고규격서URL4</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00940072&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=4&amp;prcmBsneSeCd=01</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl5</td>
<td style="text-align: left;">공고규격서URL5</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00940072&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=5&amp;prcmBsneSeCd=01</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl6</td>
<td style="text-align: left;">공고규격서URL6</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00940072&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=6&amp;prcmBsneSeCd=01</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl7</td>
<td style="text-align: left;">공고규격서URL7</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00940072&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=7&amp;prcmBsneSeCd=01</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl8</td>
<td style="text-align: left;">공고규격서URL8</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00940072&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=8&amp;prcmBsneSeCd=01</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl9</td>
<td style="text-align: left;">공고규격서URL9</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00940072&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=9&amp;prcmBsneSeCd=01</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl10</td>
<td style="text-align: left;">공고규격서URL10</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00940072&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=10&amp;prcmBsneSeCd=01</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm1</td>
<td style="text-align: left;">공고규격파일명1</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">사양서 등.zip</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm2</td>
<td style="text-align: left;">공고규격파일명2</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">공고서_R25BK00940072(국가, 중기간, 계약이행, 고시금액 미만).hwpx</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm3</td>
<td style="text-align: left;">공고규격파일명3</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">공고서_R25BK00940072(국가, 중기간, 계약이행, 고시금액 미만).hwpx</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm4</td>
<td style="text-align: left;">공고규격파일명4</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">공고서_R25BK00940072(국가, 중기간, 계약이행, 고시금액 미만).hwpx</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm5</td>
<td style="text-align: left;">공고규격파일명5</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">공고서_R25BK00940072(국가, 중기간, 계약이행, 고시금액 미만).hwpx</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm6</td>
<td style="text-align: left;">공고규격파일명6</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">공고서_R25BK00940072(국가, 중기간, 계약이행, 고시금액 미만).hwpx</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm7</td>
<td style="text-align: left;">공고규격파일명7</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">공고서_R25BK00940072(국가, 중기간, 계약이행, 고시금액 미만).hwpx</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm8</td>
<td style="text-align: left;">공고규격파일명8</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">공고서_R25BK00940072(국가, 중기간, 계약이행, 고시금액 미만).hwpx</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm9</td>
<td style="text-align: left;">공고규격파일명9</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">공고서_R25BK00940072(국가, 중기간, 계약이행, 고시금액 미만).hwpx</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm10</td>
<td style="text-align: left;">공고규격파일명10</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">공고서_R25BK00940072(국가, 중기간, 계약이행, 고시금액 미만).hwpx</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">rbidPermsnYn</td>
<td style="text-align: left;">재입찰허용여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">Y</td>
<td style="text-align: left;">입찰이 유찰되는 경우 재공고 없이 다시 입찰(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">prdctClsfcLmtYn</td>
<td style="text-align: left;">물품분류제한여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">Y</td>
<td style="text-align: left;">물품공고의 경우 물품분류번호로 제한할 경우 Y, 물품분류번호 제한없으면 N</td>
</tr>
<tr>
<td style="text-align: left;">mnfctYn</td>
<td style="text-align: left;">제조여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">Y</td>
<td style="text-align: left;">물품분류로 투찰제한시 제조물품으로 제한할 지 여부. "Y"일 경우 투찰시 업체의 경쟁입찰참가자격등록증에 공고서상 물품분류가 제조물품으로 등록되어 있어야 투찰가능(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">prearngPrceDcsnMthdNm</td>
<td style="text-align: left;">예정가격결정방법명</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">복수예가</td>
<td style="text-align: left;">예정가격의 결정을 위해 복수예정가격방식으로 산정하는지 단일 예정가격으로 산정하는지를 구분하는 명</td>
</tr>
<tr>
<td style="text-align: left;">totPrdprcNum</td>
<td style="text-align: left;">총예가건수</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">15</td>
<td style="text-align: left;">공고의 총예가건수</td>
</tr>
<tr>
<td style="text-align: left;">drwtPrdprcNum</td>
<td style="text-align: left;">추첨예가건수</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">공고의 추첨예가건수</td>
</tr>
<tr>
<td style="text-align: left;">asignBdgtAmt</td>
<td style="text-align: left;">배정예산금액</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">227930550</td>
<td style="text-align: left;">사업목적물을 달성하기 위하여 배정된 예산액 또는 설계금액(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">presmptPrce</td>
<td style="text-align: left;">추정가격</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">205550000</td>
<td style="text-align: left;">물품/공사/용역 등의 조달 계약을 체결함에 있어 국제입찰 대상여부를 판단하는 기준 등으로 삼기 위하여 예정가격이 결정되기 전에 예산에 계상된 금액 등을 기준으로 하여 부가가치세 및 조달 수수료를 제외한 금액(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">opengPlce</td>
<td style="text-align: left;">개찰장소</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">국가종합전자조달시스템(나라장터))</td>
<td style="text-align: left;">집행관이 개찰을 하는 장소</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceDtlUrl</td>
<td style="text-align: left;">입찰공고상세URL</td>
<td style="text-align: left;">512</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/link/PNPE027_01/single/?bidPbancNo=R25BK00940072&amp;bidPbancOrd=000</td>
<td style="text-align: left;">나라장터시스템의 입찰공고 상세화면 링크</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceUrl</td>
<td style="text-align: left;">입찰공고URL</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/link/PNPE027_01/single/?bidPbancNo=R25BK00940072&amp;bidPbancOrd=000</td>
<td style="text-align: left;">해당 입찰공고를 인터넷상에서 확인할 수 있는 URL주소</td>
</tr>
<tr>
<td style="text-align: left;">bidPrtcptFeePaymntYn</td>
<td style="text-align: left;">입찰참가수수료납부여부</td>
<td style="text-align: left;">30</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">없음</td>
<td style="text-align: left;">입찰참가 의사가 있는 자가 납부하여야하는 수수료의 유무 및 납부방법을 표기하는 것으로 "전자납부, 수기 및 전자납부, 수기, 없음"으로 표기</td>
</tr>
<tr>
<td style="text-align: left;">bidPrtcptFee</td>
<td style="text-align: left;">입찰참가수수료</td>
<td style="text-align: left;">21</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">1825550</td>
<td style="text-align: left;">입찰에 참가하기위해 납부하는 수수료(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">bidGrntymnyPaymntYn</td>
<td style="text-align: left;">입찰보증금납부여부</td>
<td style="text-align: left;">30</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">불허</td>
<td style="text-align: left;">입찰보증금을 나라장터에서 전자로 납부가능하게 할지 여부 “전자납부허용”,”불허’으로 표기</td>
</tr>
<tr>
<td style="text-align: left;">crdtrNm</td>
<td style="text-align: left;">채권자명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">대한민국정부강원지방조달청장</td>
<td style="text-align: left;">입찰보증금 항목의 "보증채권자명"으로 전자입찰보증 접수시 사용</td>
</tr>
<tr>
<td style="text-align: left;">dtilPrdctClsfcNo</td>
<td style="text-align: left;">세부품명번호</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">5610152001</td>
<td style="text-align: left;">물품분류번호(8자리) + 물품식별번호(앞2자리) [물품목록정보의 관리 및 이용에 관한 규정 제12조]</td>
</tr>
<tr>
<td style="text-align: left;">dtilPrdctClsfcNoNm</td>
<td style="text-align: left;">세부품명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">사물함</td>
<td style="text-align: left;">세부품명번호 10자리에 대한 한글명</td>
</tr>
<tr>
<td style="text-align: left;">prdctSpecNm</td>
<td style="text-align: left;">물품규격명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">사물함, 기타물품포함, 수요기관규격 참조</td>
<td style="text-align: left;">공고의 물품규격명</td>
</tr>
<tr>
<td style="text-align: left;">prdctQty</td>
<td style="text-align: left;">물품수량</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">공고의 물품수량</td>
</tr>
<tr>
<td style="text-align: left;">prdctUnit</td>
<td style="text-align: left;">물품단위</td>
<td style="text-align: left;">30</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">식</td>
<td style="text-align: left;">공고의 물품단위</td>
</tr>
<tr>
<td style="text-align: left;">prdctUprc</td>
<td style="text-align: left;">물품단가</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">226105000</td>
<td style="text-align: left;">공고의 물품단가</td>
</tr>
<tr>
<td style="text-align: left;">dlvrTmlmtDt</td>
<td style="text-align: left;">납품기한일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-10-15 15:00:0</td>
<td style="text-align: left;">공고의 납품기한일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">dlvrDaynum</td>
<td style="text-align: left;">납품일수</td>
<td style="text-align: left;">5</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">90</td>
<td style="text-align: left;">공고의 납품일수</td>
</tr>
<tr>
<td style="text-align: left;">dlvryCndtnNm</td>
<td style="text-align: left;">인도조건명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">수요기관희망장소입고도</td>
<td style="text-align: left;">인도 받을 장소</td>
</tr>
<tr>
<td style="text-align: left;">purchsObjPrdctList</td>
<td style="text-align: left;">구매대상물품목록</td>
<td style="text-align: left;">4000</td>
<td style="text-align: left;">0..n</td>
<td style="text-align: left;">1^5610152001^사물함]</td>
<td style="text-align: left;">공고의 구매대상물품목록으로 [입찰분류번호^세부품명번호(세부물품분류번호)^세부품명(세부물품분류명)],[입찰분류번호^세부품명번호(세부물품분류번호)^세부품명(세부물품분류명)] 제공</td>
</tr>
<tr>
<td style="text-align: left;">untyNtceNo</td>
<td style="text-align: left;">통합공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25BM00306572</td>
<td style="text-align: left;">입찰공고를 구분하는 번호로 입찰공고번호이며 형식은 년도(4)+월(2)+순번(5)<br />
*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성<br />
- 단계구분: BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격), BK(통합입찰)</td>
</tr>
<tr>
<td style="text-align: left;">cmmnSpldmdMethdCd</td>
<td style="text-align: left;">공동수급방식코드</td>
<td style="text-align: left;">15</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">공500004</td>
<td style="text-align: left;">공동수급이라 함은 구성원을 2인 이상으로 하여 수급인이 해당계약을 공동으로 수행하기 위하여 잠정적으로 결성한 실체를 의미하며 공동수급체가도급을 받아 이행하는 방식을 구분하는 코드로<br />
공500001 : 공동이행<br />
공500002 : 분담이행<br />
공500003 : 주계약자관리방식<br />
공500004 : 단독계약<br />
공500005 : 혼합방식<br />
공500006 : 공동이행 또는 분담이행<br />
공500007 : 혼합_단독<br />
공500008 : 혼합_공동<br />
공500012 : 해당없음으로 구분됨</td>
</tr>
<tr>
<td style="text-align: left;">cmmnSpldmdMethdNm</td>
<td style="text-align: left;">공동수급방식명</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">(없음)공동수급불허</td>
<td style="text-align: left;">공동수급이라 함은 구성원을 2인 이상으로 하여 수급인이 해당계약을 공동으로 수행하기 위하여 잠정적으로 결성한 실체를 의미하며 공동수급체가도급을 받아 이행하는 방식을 구분하는 명임</td>
</tr>
<tr>
<td style="text-align: left;">stdNtceDocUrl</td>
<td style="text-align: left;">표준공고서URL</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00940072&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=2&amp;prcmBsneSeCd=01</td>
<td style="text-align: left;">공고의 표준공고문URL</td>
</tr>
<tr>
<td style="text-align: left;">brffcBidprcPermsnYn</td>
<td style="text-align: left;">지사투찰허용여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">지역제한 공고에 한해서 지사 투찰을 허용할지 여부. 투찰제어시 사용(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">dsgntCmptYn</td>
<td style="text-align: left;">지명경쟁여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">공고의 지명경쟁여부(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">rsrvtnPrceReMkngMthdNm</td>
<td style="text-align: left;">예비가격재작성방법명</td>
<td style="text-align: left;">50</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">재입찰시 기존 예비가격을 사용하여 예정가격이 산정됩니다.</td>
<td style="text-align: left;">공고의 예비가격재작성방법명</td>
</tr>
<tr>
<td style="text-align: left;">arsltApplDocRcptMthdNm</td>
<td style="text-align: left;">실적신청서접수방법명</td>
<td style="text-align: left;">50</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">전자문서</td>
<td style="text-align: left;">공고의 실적신청서접수방법명</td>
</tr>
<tr>
<td style="text-align: left;">arsltApplDocRcptDt</td>
<td style="text-align: left;">실적신청서접수일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-15 14:00:00</td>
<td style="text-align: left;">실적심사신청서 접수마감일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">orderPlanUntyNo</td>
<td style="text-align: left;">발주계획통합번호</td>
<td style="text-align: left;">35</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25DD20260187</td>
<td style="text-align: left;">*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성<br />
- 단계구분: BK(입찰)<br />
TA(계약)<br />
DD:(발주계획)<br />
BD(사전규격),<br />
BK(통합입찰)</td>
</tr>
<tr>
<td style="text-align: left;">sucsfbidLwltRate</td>
<td style="text-align: left;">낙찰하한율</td>
<td style="text-align: left;">22</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">87.995</td>
<td style="text-align: left;">개찰시 사용하는 낙찰하한율(%)</td>
</tr>
<tr>
<td style="text-align: left;">rgstDt</td>
<td style="text-align: left;">등록일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">2002-09-18 10:00:00</td>
<td style="text-align: left;">공고의 등록일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">bfSpecRgstNo</td>
<td style="text-align: left;">사전규격등록번호</td>
<td style="text-align: left;">17</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25BD00083579</td>
<td style="text-align: left;"><p>*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성</p>
<p>- 단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</p></td>
</tr>
<tr>
<td style="text-align: left;">infoBizYn</td>
<td style="text-align: left;">정보화사업여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">정보화사업여부<br />
Y/N</td>
</tr>
<tr>
<td style="text-align: left;">sucsfbidMthdCd</td>
<td style="text-align: left;">낙찰방법코드</td>
<td style="text-align: left;">9</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">낙030001</td>
<td style="text-align: left;">낙찰방법명에 대한 코드 (한글 1자리 + 숫자 6자리)</td>
</tr>
<tr>
<td style="text-align: left;">sucsfbidMthdNm</td>
<td style="text-align: left;">낙찰방법명</td>
<td style="text-align: left;">700</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">조달청 중소기업자간 경쟁물품에 대한 계약이행능력심사 세부기준 - 추정가격이 고시금액 미만인 중소기업자간 경쟁물품</td>
<td style="text-align: left;">낙찰자를 결정하는 방법-낙찰방법 세부기준</td>
</tr>
<tr>
<td style="text-align: left;">chgDt</td>
<td style="text-align: left;">변경일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-04 11:12:46</td>
<td style="text-align: left;">공고의 변경일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">dminsttOfclEmailAdrs</td>
<td style="text-align: left;">수요기관담당자이메일주소</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">ddd@kywa.or.kr</td>
<td style="text-align: left;">수요기관 담당자의 이메일주소</td>
</tr>
<tr>
<td style="text-align: left;">indstrytyLmtYn</td>
<td style="text-align: left;">업종제한여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">해당 공고 입찰 시 업종(면허)제한을 두는지의 여부<br />
예시)Y</td>
</tr>
<tr>
<td style="text-align: left;">chgNtceRsn</td>
<td style="text-align: left;">변경공고사유</td>
<td style="text-align: left;">4000</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">입찰기간 부족</td>
<td style="text-align: left;">공고종류명(공고의 공고상태명) 이 변경일 경우 변경공고사유 , 취소일 경우 취소공고사유</td>
</tr>
<tr>
<td style="text-align: left;">rbidOpengDt</td>
<td style="text-align: left;">재입찰개찰일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-15 15:00:00</td>
<td style="text-align: left;">공고종류명이 ‘재입찰’ 일 경우 재입찰공고의 개찰을 수행할 수 있는 시작일시<br />
“YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">VAT</td>
<td style="text-align: left;">부가가치세</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">20555000</td>
<td style="text-align: left;">부가가치세</td>
</tr>
<tr>
<td style="text-align: left;">indutyVAT</td>
<td style="text-align: left;">주공종부가가치세</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">주공종부가가치세</td>
</tr>
<tr>
<td style="text-align: left;">bidWgrnteeRcptClseDt</td>
<td style="text-align: left;">입찰보증서접수마감일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-09-18 10:00:00</td>
<td style="text-align: left;">입찰보증서접수마감일시</td>
</tr>
<tr>
<td style="text-align: left;">rgnLmtBidLocplcJdgmBssCd</td>
<td style="text-align: left;">지역제한입찰소재지판단기준코드</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">지역제한입찰소재지판단기준코드</td>
</tr>
<tr>
<td style="text-align: left;">rgnLmtBidLocplcJdgmBssNm</td>
<td style="text-align: left;">지역제한입찰소재지판단기준명</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">본사또는참여지사소재지</td>
<td style="text-align: left;">지역제한입찰소재지판단기준명</td>
</tr>
<tr>
<td style="text-align: left;">techAbltEvlRt</td>
<td style="text-align: left;">기술능력평가비율</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">80</td>
<td style="text-align: left;">협상에 의한 낙찰자 결정의 경우 기술능력 평가 비율</td>
</tr>
<tr>
<td style="text-align: left;">bidPrceEvlRt</td>
<td style="text-align: left;">입찰가격평가비율</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">협상에 의한 낙찰자 결정의 경우 기술능력 입찰가격 평가 비율</td>
</tr>
<tr>
<td style="text-align: left;">sucsfbidMthdAppStd</td>
<td style="text-align: left;">낙찰방법적용기준</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">조달청 시설공사 적격심사세부기준</td>
<td style="text-align: left;"><p>낙찰자를 결정하</p>
<p>방법 적용기준</p></td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 요청 / 응답 메시지 예제

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr>
<td style="text-align: center;"><strong>REST(URI)</strong></td>
</tr>
<tr>
<td style="text-align: center;">http://apis.data.go.kr/1230000/ad/BidPublicInfoService/getBidPblancListInfoThng?type=&amp;inqryDiv=2&amp;numOfRows=10&amp;pageNo=1&amp;bidNtceNo=R25BK00940072&amp;ServiceKey=인증키</td>
</tr>
<tr>
<td style="text-align: center;"><strong>응답 메시지</strong></td>
</tr>
<tr>
<td style="text-align: center;"><p>&lt;response&gt;</p>
<p>&lt;header&gt;</p>
<p>&lt;resultCode&gt;00&lt;/resultCode&gt;</p>
<p>&lt;resultMsg&gt;정상&lt;/resultMsg&gt;</p>
<p>&lt;/header&gt;</p>
<p>&lt;body&gt;</p>
<p>&lt;items&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00940072&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;reNtceYn&gt;N&lt;/reNtceYn&gt;</p>
<p>&lt;rgstTyNm&gt;조달청 또는 나라장터 자체 공고건&lt;/rgstTyNm&gt;</p>
<p>&lt;ntceKindNm&gt;등록공고&lt;/ntceKindNm&gt;</p>
<p>&lt;intrbidYn&gt;N&lt;/intrbidYn&gt;</p>
<p>&lt;bidNtceDt&gt;2025-07-04 11:12:46&lt;/bidNtceDt&gt;</p>
<p>&lt;refNo&gt;&lt;/refNo&gt;</p>
<p>&lt;bidNtceNm&gt;스키장 고객용 전자 물품보관함 구매&lt;/bidNtceNm&gt;</p>
<p>&lt;ntceInsttCd&gt;1230145&lt;/ntceInsttCd&gt;</p>
<p>&lt;ntceInsttNm&gt;조달청 강원지방조달청&lt;/ntceInsttNm&gt;</p>
<p>&lt;dminsttCd&gt;Z003620&lt;/dminsttCd&gt;</p>
<p>&lt;dminsttNm&gt;(주)강원랜드&lt;/dminsttNm&gt;</p>
<p>&lt;bidMethdNm&gt;전자입찰&lt;/bidMethdNm&gt;</p>
<p>&lt;cntrctCnclsMthdNm&gt;제한경쟁&lt;/cntrctCnclsMthdNm&gt;</p>
<p>&lt;ntceInsttOfclNm&gt;윤순제&lt;/ntceInsttOfclNm&gt;</p>
<p>&lt;ntceInsttOfclTelNo&gt;070-4056-8424&lt;/ntceInsttOfclTelNo&gt;</p>
<p>&lt;ntceInsttOfclEmailAdrs&gt;soongdae@korea.kr&lt;/ntceInsttOfclEmailAdrs&gt;</p>
<p>&lt;exctvNm&gt;이병규&lt;/exctvNm&gt;</p>
<p>&lt;bidQlfctRgstDt&gt;2025-07-14 18:00&lt;/bidQlfctRgstDt&gt;</p>
<p>&lt;cmmnSpldmdAgrmntRcptdocMethd&gt;없음&lt;/cmmnSpldmdAgrmntRcptdocMethd&gt;</p>
<p>&lt;cmmnSpldmdAgrmntClseDt&gt;&lt;/cmmnSpldmdAgrmntClseDt&gt;</p>
<p>&lt;cmmnSpldmdCorpRgnLmtYn&gt;&lt;/cmmnSpldmdCorpRgnLmtYn&gt;</p>
<p>&lt;bidBeginDt&gt;2025-07-11 14:00:00&lt;/bidBeginDt&gt;</p>
<p>&lt;bidClseDt&gt;2025-07-15 14:00:00&lt;/bidClseDt&gt;</p>
<p>&lt;opengDt&gt;2025-07-15 15:00:00&lt;/opengDt&gt;</p>
<p>&lt;ntceSpecDocUrl1&gt;https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00940072&amp;amp;bidPbancOrd=000&amp;amp;fileType=&amp;amp;fileSeq=1&amp;prcmBsneSeCd=01&lt;/ntceSpecDocUrl1&gt;</p>
<p>&lt;ntceSpecDocUrl2&gt;https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00940072&amp;amp;bidPbancOrd=000&amp;amp;fileType=&amp;amp;fileSeq=2&amp;prcmBsneSeCd=01&lt;/ntceSpecDocUrl2&gt;</p>
<p>&lt;ntceSpecDocUrl3&gt;&lt;/ntceSpecDocUrl3&gt;</p>
<p>&lt;ntceSpecDocUrl4&gt;&lt;/ntceSpecDocUrl4&gt;</p>
<p>&lt;ntceSpecDocUrl5&gt;&lt;/ntceSpecDocUrl5&gt;</p>
<p>&lt;ntceSpecDocUrl6&gt;&lt;/ntceSpecDocUrl6&gt;</p>
<p>&lt;ntceSpecDocUrl7&gt;&lt;/ntceSpecDocUrl7&gt;</p>
<p>&lt;ntceSpecDocUrl8&gt;&lt;/ntceSpecDocUrl8&gt;</p>
<p>&lt;ntceSpecDocUrl9&gt;&lt;/ntceSpecDocUrl9&gt;</p>
<p>&lt;ntceSpecDocUrl10&gt;&lt;/ntceSpecDocUrl10&gt;</p>
<p>&lt;ntceSpecFileNm1&gt;사양서 등.zip&lt;/ntceSpecFileNm1&gt;</p>
<p>&lt;ntceSpecFileNm2&gt;공고서_R25BK00940072(국가, 중기간, 계약이행, 고시금액 미만).hwpx&lt;/ntceSpecFileNm2&gt;</p>
<p>&lt;ntceSpecFileNm3&gt;&lt;/ntceSpecFileNm3&gt;</p>
<p>&lt;ntceSpecFileNm4&gt;&lt;/ntceSpecFileNm4&gt;</p>
<p>&lt;ntceSpecFileNm5&gt;&lt;/ntceSpecFileNm5&gt;</p>
<p>&lt;ntceSpecFileNm6&gt;&lt;/ntceSpecFileNm6&gt;</p>
<p>&lt;ntceSpecFileNm7&gt;&lt;/ntceSpecFileNm7&gt;</p>
<p>&lt;ntceSpecFileNm8&gt;&lt;/ntceSpecFileNm8&gt;</p>
<p>&lt;ntceSpecFileNm9&gt;&lt;/ntceSpecFileNm9&gt;</p>
<p>&lt;ntceSpecFileNm10&gt;&lt;/ntceSpecFileNm10&gt;</p>
<p>&lt;rbidPermsnYn&gt;Y&lt;/rbidPermsnYn&gt;</p>
<p>&lt;prdctClsfcLmtYn&gt;Y&lt;/prdctClsfcLmtYn&gt;</p>
<p>&lt;mnfctYn&gt;Y&lt;/mnfctYn&gt;</p>
<p>&lt;prearngPrceDcsnMthdNm&gt;복수예가&lt;/prearngPrceDcsnMthdNm&gt;</p>
<p>&lt;totPrdprcNum&gt;15&lt;/totPrdprcNum&gt;</p>
<p>&lt;drwtPrdprcNum&gt;4&lt;/drwtPrdprcNum&gt;</p>
<p>&lt;asignBdgtAmt&gt;227930550&lt;/asignBdgtAmt&gt;</p>
<p>&lt;presmptPrce&gt;205550000&lt;/presmptPrce&gt;</p>
<p>&lt;opengPlce&gt;&lt;/opengPlce&gt;</p>
<p>&lt;bidNtceDtlUrl&gt;https://www.g2b.go.kr/link/PNPE027_01/single/?bidPbancNo=R25BK00940072&amp;amp;bidPbancOrd=000&lt;/bidNtceDtlUrl&gt;</p>
<p>&lt;bidNtceUrl&gt; https://www.g2b.go.kr/link/PNPE027_01/single/?bidPbancNo=R25BK00940072&amp;amp;bidPbancOrd=000&lt;/bidNtceUrl&gt;</p>
<p>&lt;bidPrtcptFeePaymntYn&gt;&lt;/bidPrtcptFeePaymntYn&gt;</p>
<p>&lt;bidPrtcptFee&gt;1825550&lt;/bidPrtcptFee&gt;</p>
<p>&lt;bidGrntymnyPaymntYn&gt;&lt;/bidGrntymnyPaymntYn&gt;</p>
<p>&lt;crdtrNm&gt;대한민국정부강원지방조달청장&lt;/crdtrNm&gt;</p>
<p>&lt;dtilPrdctClsfcNo&gt;5610152001&lt;/dtilPrdctClsfcNo&gt;</p>
<p>&lt;dtilPrdctClsfcNoNm&gt;사물함&lt;/dtilPrdctClsfcNoNm&gt;</p>
<p>&lt;prdctSpecNm&gt;사물함, 기타물품포함, 수요기관규격&lt;/prdctSpecNm&gt;</p>
<p>&lt;prdctQty&gt;1&lt;/prdctQty&gt;</p>
<p>&lt;prdctUnit&gt;식&lt;/prdctUnit&gt;</p>
<p>&lt;prdctUprc&gt;226105000&lt;/prdctUprc&gt;</p>
<p>&lt;dlvrTmlmtDt&gt;&lt;/dlvrTmlmtDt&gt;</p>
<p>&lt;dlvrDaynum&gt;90&lt;/dlvrDaynum&gt;</p>
<p>&lt;dlvryCndtnNm&gt;수요기관희망장소입고도&lt;/dlvryCndtnNm&gt;</p>
<p>&lt;purchsObjPrdctList&gt;[1^5610152001^사물함]&lt;/purchsObjPrdctList&gt;</p>
<p>&lt;untyNtceNo&gt;R25BM00306572&lt;/untyNtceNo&gt;</p>
<p>&lt;cmmnSpldmdMethdCd&gt;&lt;/cmmnSpldmdMethdCd&gt;</p>
<p>&lt;cmmnSpldmdMethdNm&gt;(없음)공동수급불허&lt;/cmmnSpldmdMethdNm&gt;</p>
<p>&lt;stdNtceDocUrl&gt;https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00940072&amp;amp;bidPbancOrd=000&amp;amp;fileType=&amp;amp;fileSeq=2&lt;/stdNtceDocUrl&gt;</p>
<p>&lt;brffcBidprcPermsnYn&gt;&lt;/brffcBidprcPermsnYn&gt;</p>
<p>&lt;dsgntCmptYn&gt;N&lt;/dsgntCmptYn&gt;</p>
<p>&lt;rsrvtnPrceReMkngMthdNm&gt;재입찰시 예비가격을 다시 생성하여 예정가격이 산정됩니다.&lt;/rsrvtnPrceReMkngMthdNm&gt;</p>
<p>&lt;arsltApplDocRcptMthdNm&gt;&lt;/arsltApplDocRcptMthdNm&gt;</p>
<p>&lt;arsltApplDocRcptDt&gt;&lt;/arsltApplDocRcptDt&gt;</p>
<p>&lt;orderPlanUntyNo&gt;R25DD20260187&lt;/orderPlanUntyNo&gt;</p>
<p>&lt;sucsfbidLwltRate&gt;87.995&lt;/sucsfbidLwltRate&gt;</p>
<p>&lt;rgstDt&gt;2025-07-04 11:12:46&lt;/rgstDt&gt;</p>
<p>&lt;bfSpecRgstNo&gt;R25BD00083579&lt;/bfSpecRgstNo&gt;</p>
<p>&lt;infoBizYn&gt;N&lt;/infoBizYn&gt;</p>
<p>&lt;sucsfbidMthdCd&gt;낙030001&lt;/sucsfbidMthdCd&gt;</p>
<p>&lt;sucsfbidMthdNm&gt;조달청 중소기업자간 경쟁물품에 대한 계약이행능력심사 세부기준 - 추정가격이 고시금액 미만인 중소기업자간 경쟁물품&lt;/sucsfbidMthdNm&gt;</p>
<p>&lt;chgDt&gt;&lt;/chgDt&gt;</p>
<p>&lt;dminsttOfclEmailAdrs&gt;&lt;/dminsttOfclEmailAdrs&gt;</p>
<p>&lt;indstrytyLmtYn&gt;&lt;/indstrytyLmtYn&gt;</p>
<p>&lt;chgNtceRsn&gt;&lt;/chgNtceRsn&gt;</p>
<p>&lt;rbidOpengDt&gt;2025-07-15 15:00:00&lt;/rbidOpengDt&gt;</p>
<p>&lt;VAT&gt;20555000&lt;/VAT&gt;</p>
<p>&lt;indutyVAT&gt;&lt;/indutyVAT&gt;</p>
<p>&lt;bidWgrnteeRcptClseDt&gt;2025-07-14 18:00:00&lt;/bidWgrnteeRcptClseDt&gt;</p>
<p>&lt;rgnLmtBidLocplcJdgmBssCd&gt;&lt;/rgnLmtBidLocplcJdgmBssCd&gt;</p>
<p>&lt;rgnLmtBidLocplcJdgmBssNm&gt;&lt;/rgnLmtBidLocplcJdgmBssNm&gt;</p>
<p>&lt;techAbltEvlRt&gt;&lt;/techAbltEvlRt&gt;</p>
<p>&lt;bidPrceEvlRt&gt;&lt;/bidPrceEvlRt&gt;</p>
<p>&lt;sucsfbidMthdAppStd&gt;&lt;/sucsfbidMthdAppStd&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;/items&gt;</p>
<p>&lt;numOfRows&gt;10&lt;/numOfRows&gt;</p>
<p>&lt;pageNo&gt;1&lt;/pageNo&gt;</p>
<p>&lt;totalCount&gt;1&lt;/totalCount&gt;</p>
<p>&lt;/body&gt;</p>
<p>&lt;/response&gt;</p></td>
</tr>
</tbody>
</table>

#### \[입찰공고목록 정보에 대한 물품기초금액조회\] 오퍼레이션 명세

<table>
<colgroup>
<col style="width: 4%" />
<col style="width: 21%" />
<col style="width: 17%" />
<col style="width: 21%" />
<col style="width: 2%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr>
<td rowspan="6">오퍼레이션 정보</td>
<td>오퍼레이션 번호</td>
<td>5</td>
<td>오퍼레이션명(국문)</td>
<td colspan="2">입찰공고목록 정보에 대한 물품기초금액조회</td>
</tr>
<tr>
<td>오퍼레이션 유형</td>
<td>조회(목록)</td>
<td>오퍼레이션명(영문)</td>
<td colspan="2">getBidPblancListInfoThngBsisAmount</td>
</tr>
<tr>
<td>오퍼레이션 설명</td>
<td colspan="4">검색조건에 기초금액 등록일시, 입찰공고번호를 입력하여 입찰공고번호, 입찰공고명, 기초금액, 기초금액공개일시, 예비가격범위시작율, 평가기준금액, 난이도계수, 기타경비기준율 등 물품의 기초금액정보 조회</td>
</tr>
<tr>
<td>Call Back URL</td>
<td colspan="4">N/A</td>
</tr>
<tr>
<td>최대 메시지 사이즈</td>
<td colspan="4">[ 4000bytes]</td>
</tr>
<tr>
<td>평균 응답 시간</td>
<td>[ 500 ms]</td>
<td colspan="2">초당 최대 트랜잭션</td>
<td>[ 30 tps]</td>
</tr>
</tbody>
</table>

##### 요청 메시지 명세

<table>
<colgroup>
<col style="width: 19%" />
<col style="width: 19%" />
<col style="width: 13%" />
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 21%" />
</colgroup>
<tbody>
<tr>
<td>항목명(영문)</td>
<td>항목명(국문)</td>
<td>항목크기</td>
<td>항목구분</td>
<td>샘플데이터</td>
<td>항목설명</td>
</tr>
<tr>
<td style="text-align: left;">numOfRows</td>
<td style="text-align: left;">한 페이지 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td style="text-align: left;">pageNo</td>
<td style="text-align: left;">페이지 번호</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">페이지 번호</td>
</tr>
<tr>
<td style="text-align: left;">ServiceKey</td>
<td style="text-align: left;">서비스키</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">공공데이터포탈에서 받은 인증키</td>
<td style="text-align: left;">공공데이터포탈에서 받은 인증키</td>
</tr>
<tr>
<td style="text-align: left;">type</td>
<td style="text-align: left;">타입</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">0</td>
<td>json</td>
<td>오픈API 리턴 타입을 JSON으로 받고 싶을 경우 'json' 으로 지정</td>
</tr>
<tr>
<td style="text-align: left;">inqryDiv</td>
<td style="text-align: left;">조회구분</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">검색하고자하는 조회구분<br />
1:입력일시 , 2.입찰공고번호</td>
</tr>
<tr>
<td style="text-align: left;">inqryBgnDt</td>
<td style="text-align: left;">조회시작일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">202507010000</td>
<td style="text-align: left;">검색하고자하는 조회시작일시 "YYYYMMDDHHMM"<br />
(조회구분 '1' 선택시 필수)</td>
</tr>
<tr>
<td style="text-align: left;">inqryEndDt</td>
<td style="text-align: left;">조회종료일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">202507012359</td>
<td style="text-align: left;">검색하고자하는 조회종료일시 "YYYYMMDDHHMM"<br />
(조회구분 '1' 선택시 필수)</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNo</td>
<td style="text-align: left;">입찰공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25BK00940072</td>
<td style="text-align: left;">검색하고자 하는 입찰공고번호<br />
(조회구분 '2' 선택시 필수)</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 응답 메시지 명세

<table style="width:98%;">
<colgroup>
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 13%" />
<col style="width: 11%" />
<col style="width: 13%" />
<col style="width: 18%" />
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
<td style="text-align: left;">resultCode</td>
<td style="text-align: left;">결과코드</td>
<td style="text-align: left;">2</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">00</td>
<td style="text-align: left;">결과코드</td>
</tr>
<tr>
<td style="text-align: left;">resultMsg</td>
<td style="text-align: left;">결과메세지</td>
<td style="text-align: left;">50</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">정상.</td>
<td style="text-align: left;">결과메세지</td>
</tr>
<tr>
<td style="text-align: left;">numOfRows</td>
<td style="text-align: left;">한 페이지 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td style="text-align: left;">pageNo</td>
<td style="text-align: left;">페이지 번호</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">페이지 번호</td>
</tr>
<tr>
<td style="text-align: left;">totalCount</td>
<td style="text-align: left;">데이터 총 개수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">데이터 총개수</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNo</td>
<td style="text-align: left;">입찰공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">R25BK00940072</td>
<td style="text-align: left;"><p>입찰공고 관리번입찰공고 관리번호이며 조달청나라장터 공고건의 형식은 년도(4)+월(2)+순번(5)이며 자체전자조달시스템 보유기관은 각 기관별 형식 별도 사용</p>
<p>*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성</p>
<p>- 단계구분: BK(입찰)<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</p></td>
</tr>
<tr>
<td style="text-align: left;">bidNtceOrd</td>
<td style="text-align: left;">입찰공고차수</td>
<td style="text-align: left;">3</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">000</td>
<td style="text-align: left;">입찰공고차수는 해당 입찰공고에 대한 재공고 및 재입찰 등이 발생되었을 경우 증가되는 수</td>
</tr>
<tr>
<td style="text-align: left;">bidClsfcNo</td>
<td style="text-align: left;">입찰분류번호</td>
<td style="text-align: left;">5</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">공고의 입찰분류번호</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNm</td>
<td style="text-align: left;">입찰공고명</td>
<td style="text-align: left;">1000</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">스키장 고객용 전자 물품보관함 구매</td>
<td style="text-align: left;">공사명 또는 사업명이라고도 하며 입찰공고 내용을 요약한 이름</td>
</tr>
<tr>
<td style="text-align: left;">bssamt</td>
<td style="text-align: left;">기초금액</td>
<td style="text-align: left;">21</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">221500000</td>
<td style="text-align: left;">예정가격 작성 과정에서 거래실례가격, 원가계산가격 등에 의하여 조사한 가격이나 설계가격에 대하여 계약담당공무원이 그 적정여부를 검토조정한 가격(기초금액)(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">bssamtOpenDt</td>
<td style="text-align: left;">기초금액공개일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-09 16:02:24</td>
<td style="text-align: left;">기초금액공개일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">rsrvtnPrceRngBgnRate</td>
<td style="text-align: left;">예비가격범위시작률</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">-2</td>
<td style="text-align: left;">예비가격범위시작율(%)</td>
</tr>
<tr>
<td style="text-align: left;">rsrvtnPrceRngEndRate</td>
<td style="text-align: left;">예비가격범위종료율</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">+2</td>
<td style="text-align: left;">예비가격범위종료율(%)</td>
</tr>
<tr>
<td style="text-align: left;">evlBssAmt</td>
<td style="text-align: left;">평가기준금액</td>
<td style="text-align: left;">21</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N/A</td>
<td style="text-align: left;">적정성 평가를 위한 평가기준금액(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">dfcltydgrCfcnt</td>
<td style="text-align: left;">난이도계수</td>
<td style="text-align: left;">5</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N/A</td>
<td style="text-align: left;">적정성 평가를 위한 난이도계수</td>
</tr>
<tr>
<td style="text-align: left;">etcGnrlexpnsBssRate</td>
<td style="text-align: left;">기타경비기준율</td>
<td style="text-align: left;">8</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N/A</td>
<td style="text-align: left;">기타경비기준율(%)</td>
</tr>
<tr>
<td style="text-align: left;">gnrlMngcstBssRate</td>
<td style="text-align: left;">일반관리비기준율</td>
<td style="text-align: left;">8</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N/A</td>
<td style="text-align: left;">일반관리비기준율(%)</td>
</tr>
<tr>
<td style="text-align: left;">prftBssRate</td>
<td style="text-align: left;">이윤기준율</td>
<td style="text-align: left;">8</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N/A</td>
<td style="text-align: left;">이윤기준율(%)</td>
</tr>
<tr>
<td style="text-align: left;">lbrcstBssRate</td>
<td style="text-align: left;">노무비기준율</td>
<td style="text-align: left;">8</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N/A</td>
<td style="text-align: left;">노무비기준율(%)</td>
</tr>
<tr>
<td style="text-align: left;">industSftyHelthMngcst</td>
<td style="text-align: left;">산업안전보건관리비</td>
<td style="text-align: left;">17</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N/A</td>
<td style="text-align: left;">산업안전보건관리비(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">rtrfundNon</td>
<td style="text-align: left;">퇴직공제부금비</td>
<td style="text-align: left;">17</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N/A</td>
<td style="text-align: left;">퇴직공제부금비(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">envCnsrvcst</td>
<td style="text-align: left;">환경보전비</td>
<td style="text-align: left;">15</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N/A</td>
<td style="text-align: left;">환경보전비(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">scontrctPayprcePayGrntyFee</td>
<td style="text-align: left;">하도급대금지급보증수수료</td>
<td style="text-align: left;">21</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N/A</td>
<td style="text-align: left;">하도급대금지급보증수수료(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">mrfnHealthInsrprm</td>
<td style="text-align: left;">국민건강보험료</td>
<td style="text-align: left;">18</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N/A</td>
<td style="text-align: left;">국민건강보험료(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">npnInsrprm</td>
<td style="text-align: left;">국민연금보험료</td>
<td style="text-align: left;">18</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N/A</td>
<td style="text-align: left;">국민연금보험료(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">rmrk1</td>
<td style="text-align: left;">비고1</td>
<td style="text-align: left;">1000</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">기초금액은 부가세 포함 가격임.</td>
<td style="text-align: left;">기초금액 공개시 업체에게 전달할 메세지사항1</td>
</tr>
<tr>
<td style="text-align: left;">rmrk2</td>
<td style="text-align: left;">비고2</td>
<td style="text-align: left;">1000</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">규격서 참조(엔드밀 외 29종)</td>
<td style="text-align: left;">기초금액 공개시 업체에게 전달할 메세지사항2</td>
</tr>
<tr>
<td style="text-align: left;">usefulAmt</td>
<td style="text-align: left;">가용금액</td>
<td style="text-align: left;">21</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">226105000</td>
<td style="text-align: left;">수요기관 예산에서 수수료를 제외한 금액(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">inptDt</td>
<td style="text-align: left;">입력일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">2025-07-09 16:02:24</td>
<td style="text-align: left;">공고를 저장한 일시 (YYYY-MM-DD HH24:MM:SS)</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 요청 / 응답 메시지 예제

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr>
<td style="text-align: center;"><strong>REST(URI)</strong></td>
</tr>
<tr>
<td style="text-align: center;">http://apis.data.go.kr/1230000/ad/BidPublicInfoService/getBidPblancListInfoThngBsisAmount?type=xml&amp;inqryDiv=2&amp;numOfRows=10&amp;pageNo=1&amp;bidNtceNo=R25BK00940072&amp;ServiceKey=인증키</td>
</tr>
<tr>
<td style="text-align: center;"><strong>응답 메시지</strong></td>
</tr>
<tr>
<td style="text-align: center;"><p>&lt;response&gt;</p>
<p>&lt;header&gt;</p>
<p>&lt;resultCode&gt;00&lt;/resultCode&gt;</p>
<p>&lt;resultMsg&gt;정상&lt;/resultMsg&gt;</p>
<p>&lt;/header&gt;</p>
<p>&lt;body&gt;</p>
<p>&lt;items&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00940072&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;1&lt;/bidClsfcNo&gt;</p>
<p>&lt;bidNtceNm&gt;스키장 고객용 전자 물품보관함 구매&lt;/bidNtceNm&gt;</p>
<p>&lt;bssamt&gt;221500000&lt;/bssamt&gt;</p>
<p>&lt;bssamtOpenDt&gt;2025-07-09 16:02:24&lt;/bssamtOpenDt&gt;</p>
<p>&lt;rsrvtnPrceRngBgnRate&gt;-2&lt;/rsrvtnPrceRngBgnRate&gt;</p>
<p>&lt;rsrvtnPrceRngEndRate&gt;+2&lt;/rsrvtnPrceRngEndRate&gt;</p>
<p>&lt;evlBssAmt&gt;&lt;/evlBssAmt&gt;</p>
<p>&lt;dfcltydgrCfcnt&gt;&lt;/dfcltydgrCfcnt&gt;</p>
<p>&lt;etcGnrlexpnsBssRate&gt;&lt;/etcGnrlexpnsBssRate&gt;</p>
<p>&lt;gnrlMngcstBssRate&gt;&lt;/gnrlMngcstBssRate&gt;</p>
<p>&lt;prftBssRate&gt;&lt;/prftBssRate&gt;</p>
<p>&lt;lbrcstBssRate&gt;&lt;/lbrcstBssRate&gt;</p>
<p>&lt;industSftyHelthMngcst&gt;&lt;/industSftyHelthMngcst&gt;</p>
<p>&lt;rtrfundNon&gt;&lt;/rtrfundNon&gt;</p>
<p>&lt;envCnsrvcst&gt;&lt;/envCnsrvcst&gt;</p>
<p>&lt;scontrctPayprcePayGrntyFee&gt;&lt;/scontrctPayprcePayGrntyFee&gt;</p>
<p>&lt;mrfnHealthInsrprm&gt;&lt;/mrfnHealthInsrprm&gt;</p>
<p>&lt;npnInsrprm&gt;&lt;/npnInsrprm&gt;</p>
<p>&lt;rmrk1&gt;&lt;/rmrk1&gt;</p>
<p>&lt;rmrk2&gt;&lt;/rmrk2&gt;</p>
<p>&lt;usefulAmt&gt;226105000&lt;/usefulAmt&gt;</p>
<p>&lt;inptDt&gt;2025-07-09 16:02:24&lt;/inptDt&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;/items&gt;</p>
<p>&lt;numOfRows&gt;999&lt;/numOfRows&gt;</p>
<p>&lt;pageNo&gt;1&lt;/pageNo&gt;</p>
<p>&lt;totalCount&gt;1&lt;/totalCount&gt;</p>
<p>&lt;/body&gt;</p>
<p>&lt;/response&gt;</p></td>
</tr>
</tbody>
</table>

#### \
\[입찰공고목록 정보에 대한 공사기초금액조회\] 오퍼레이션 명세

<table>
<colgroup>
<col style="width: 4%" />
<col style="width: 21%" />
<col style="width: 17%" />
<col style="width: 21%" />
<col style="width: 2%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr>
<td rowspan="6">오퍼레이션 정보</td>
<td>오퍼레이션 번호</td>
<td>6</td>
<td>오퍼레이션명(국문)</td>
<td colspan="2">입찰공고목록 정보에 대한 공사기초금액조회</td>
</tr>
<tr>
<td>오퍼레이션 유형</td>
<td>조회(목록)</td>
<td>오퍼레이션명(영문)</td>
<td colspan="2">getBidPblancListInfoCnstwkBsisAmount</td>
</tr>
<tr>
<td>오퍼레이션 설명</td>
<td colspan="4">검색조건에 기초금액 등록일시, 입찰공고번호를 입력하여 입찰공고번호, 입찰공고명, 기초금액, 기초금액공개일시, 예비가격범위시작율, 평가기준금액, 난이도계수, 기타경비기준율 등의 공사의 기초금액정보 조회</td>
</tr>
<tr>
<td>Call Back URL</td>
<td colspan="4">N/A</td>
</tr>
<tr>
<td>최대 메시지 사이즈</td>
<td colspan="4">[ 4000bytes]</td>
</tr>
<tr>
<td>평균 응답 시간</td>
<td>[ 500 ms]</td>
<td colspan="2">초당 최대 트랜잭션</td>
<td>[ 30 tps]</td>
</tr>
</tbody>
</table>

##### 요청 메시지 명세

<table>
<colgroup>
<col style="width: 19%" />
<col style="width: 19%" />
<col style="width: 13%" />
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 21%" />
</colgroup>
<tbody>
<tr>
<td>항목명(영문)</td>
<td>항목명(국문)</td>
<td>항목크기</td>
<td>항목구분</td>
<td>샘플데이터</td>
<td>항목설명</td>
</tr>
<tr>
<td style="text-align: left;">numOfRows</td>
<td style="text-align: left;">한 페이지 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td style="text-align: left;">pageNo</td>
<td style="text-align: left;">페이지 번호</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">페이지 번호</td>
</tr>
<tr>
<td style="text-align: left;">ServiceKey</td>
<td style="text-align: left;">서비스키</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">공공데이터포탈에서 받은 인증키</td>
<td style="text-align: left;">공공데이터포탈에서 받은 인증키</td>
</tr>
<tr>
<td style="text-align: left;">type</td>
<td style="text-align: left;">타입</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">0</td>
<td>json</td>
<td>오픈API 리턴 타입을 JSON으로 받고 싶을 경우 'json' 으로 지정</td>
</tr>
<tr>
<td style="text-align: left;">inqryDiv</td>
<td style="text-align: left;">조회구분</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">검색하고자하는 조회구분<br />
1:입력일시 , 2.입찰공고번호</td>
</tr>
<tr>
<td style="text-align: left;">inqryBgnDt</td>
<td style="text-align: left;">조회시작일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">202509230000</td>
<td style="text-align: left;">검색하고자하는 조회시작일시 "YYYYMMDDHHMM"<br />
(조회구분 '1' 선택시 필수)</td>
</tr>
<tr>
<td style="text-align: left;">inqryEndDt</td>
<td style="text-align: left;">조회종료일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">202509232359</td>
<td style="text-align: left;">검색하고자하는 조회종료일시 "YYYYMMDDHHMM"<br />
(조회구분 '1' 선택시 필수)</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNo</td>
<td style="text-align: left;">입찰공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25BK01035950</td>
<td style="text-align: left;">검색하고자 하는 입찰공고번호<br />
(조회구분 '2' 선택시 필수)</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 응답 메시지 명세

<table>
<colgroup>
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 13%" />
<col style="width: 13%" />
<col style="width: 13%" />
<col style="width: 19%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;">항목명(영문)</th>
<th style="text-align: left;">항목명(국문)</th>
<th style="text-align: left;">항목크기</th>
<th style="text-align: left;">항목구분</th>
<th style="text-align: left;">샘플데이터</th>
<th style="text-align: left;">항목설명</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;">resultCode</td>
<td style="text-align: left;">결과코드</td>
<td style="text-align: left;">2</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">00</td>
<td style="text-align: left;">결과코드</td>
</tr>
<tr>
<td style="text-align: left;">resultMsg</td>
<td style="text-align: left;">결과메세지</td>
<td style="text-align: left;">50</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">정상.</td>
<td style="text-align: left;">결과메세지</td>
</tr>
<tr>
<td style="text-align: left;">numOfRows</td>
<td style="text-align: left;">한 페이지 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td style="text-align: left;">pageNo</td>
<td style="text-align: left;">페이지 번호</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">페이지 번호</td>
</tr>
<tr>
<td style="text-align: left;">totalCount</td>
<td style="text-align: left;">데이터 총 개수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">데이터 총개수</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNo</td>
<td style="text-align: left;">입찰공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">R25BK01035950</td>
<td style="text-align: left;"><p>입찰공고 관리번입찰공고 관리번호이며 조달청나라장터 공고건의 형식은 년도(4)+월(2)+순번(5)이며 자체전자조달시스템 보유기관은 각 기관별 형식 별도 사용</p>
<p>*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성</p>
<p>-단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</p></td>
</tr>
<tr>
<td style="text-align: left;">bidNtceOrd</td>
<td style="text-align: left;">입찰공고차수</td>
<td style="text-align: left;">3</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">000</td>
<td style="text-align: left;">입찰공고차수는 해당 입찰공고에 대한 재공고 및 재입찰 등이 발생되었을 경우 증가되는 수</td>
</tr>
<tr>
<td style="text-align: left;">bidClsfcNo</td>
<td style="text-align: left;">입찰분류번호</td>
<td style="text-align: left;">5</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">공고의 입찰분류번호</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNm</td>
<td style="text-align: left;">입찰공고명</td>
<td style="text-align: left;">1000</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">진주 상상리메이크센터 건립 공사(건축)</td>
<td style="text-align: left;">공사명 또는 사업명이라고도 하며 입찰공고 내용을 요약한 이름</td>
</tr>
<tr>
<td style="text-align: left;">bssamt</td>
<td style="text-align: left;">기초금액</td>
<td style="text-align: left;">21</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">13827624000</td>
<td style="text-align: left;">예정가격 작성 과정에서 거래실례가격, 원가계산가격 등에 의하여 조사한 가격이나 설계가격에 대하여 계약담당공무원이 그 적정여부를 검토조정한 가격(기초금액)(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">bssamtOpenDt</td>
<td style="text-align: left;">기초금액공개일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-09-23 10:58:42</td>
<td style="text-align: left;">기초금액공개일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">rsrvtnPrceRngBgnRate</td>
<td style="text-align: left;">예비가격범위시작률</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">-3</td>
<td style="text-align: left;">예비가격범위시작율(%)</td>
</tr>
<tr>
<td style="text-align: left;">rsrvtnPrceRngEndRate</td>
<td style="text-align: left;">예비가격범위종료율</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">+3</td>
<td style="text-align: left;">예비가격범위종료율(%)</td>
</tr>
<tr>
<td style="text-align: left;">evlBssAmt</td>
<td style="text-align: left;">평가기준금액</td>
<td style="text-align: left;">21</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">적정성 평가를 위한 평가기준금액(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">dfcltydgrCfcnt</td>
<td style="text-align: left;">난이도계수</td>
<td style="text-align: left;">5</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0.9</td>
<td style="text-align: left;">적정성 평가를 위한 난이도계수</td>
</tr>
<tr>
<td style="text-align: left;">etcGnrlexpnsBssRate</td>
<td style="text-align: left;">기타경비기준율</td>
<td style="text-align: left;">8</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">3.5</td>
<td style="text-align: left;">기타경비기준율(%)</td>
</tr>
<tr>
<td style="text-align: left;">gnrlMngcstBssRate</td>
<td style="text-align: left;">일반관리비기준율</td>
<td style="text-align: left;">8</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">5.13</td>
<td style="text-align: left;">일반관리비기준율(%)</td>
</tr>
<tr>
<td style="text-align: left;">prftBssRate</td>
<td style="text-align: left;">이윤기준율</td>
<td style="text-align: left;">8</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">6.78</td>
<td style="text-align: left;">이윤기준율(%)</td>
</tr>
<tr>
<td style="text-align: left;">lbrcstBssRate</td>
<td style="text-align: left;">노무비기준율</td>
<td style="text-align: left;">8</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">36.01</td>
<td style="text-align: left;">노무비기준율(%)</td>
</tr>
<tr>
<td style="text-align: left;">sftyMngcst</td>
<td style="text-align: left;">산업안전보건관리비</td>
<td style="text-align: left;">17</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">237064891</td>
<td style="text-align: left;">산업안전보건관리비 (원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">rtrfundNon</td>
<td style="text-align: left;">퇴직공제부금비</td>
<td style="text-align: left;">17</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">101751069</td>
<td style="text-align: left;">퇴직공제부금비(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">envCnsrvcst</td>
<td style="text-align: left;">환경보전비</td>
<td style="text-align: left;">15</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">환경보전비(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">scontrctPayprcePayGrntyFee</td>
<td style="text-align: left;">하도급대금지급보증수수료</td>
<td style="text-align: left;">21</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">하도급대금지급보증수수료(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">mrfnHealthInsrprm</td>
<td style="text-align: left;">국민건강보험료</td>
<td style="text-align: left;">18</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">156829366</td>
<td style="text-align: left;">국민건강보험료(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">npnInsrprm</td>
<td style="text-align: left;">국민연금보험료</td>
<td style="text-align: left;">18</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">199078180</td>
<td style="text-align: left;">국민연금보험료(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">rmrk1</td>
<td style="text-align: left;">비고1</td>
<td style="text-align: left;">1000</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N/A.</td>
<td style="text-align: left;">기초금액 공개시 업체에게 전달할 메세지사항1</td>
</tr>
<tr>
<td style="text-align: left;">rmrk2</td>
<td style="text-align: left;">비고2</td>
<td style="text-align: left;">1000</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N/A</td>
<td style="text-align: left;">기초금액 공개시 업체에게 전달할 메세지사항2</td>
</tr>
<tr>
<td style="text-align: left;">odsnLngtrmrcprInsrprm</td>
<td style="text-align: left;">노인장기요양보험료</td>
<td style="text-align: left;">18</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">20309402</td>
<td style="text-align: left;">노인장기요양보험료(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">usefulAmt</td>
<td style="text-align: left;">가용금액</td>
<td style="text-align: left;">21</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">수요기관 예산에서 수수료를 제외한 금액(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">inptDt</td>
<td style="text-align: left;">입력일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">2025-09-23 10:58:42</td>
<td style="text-align: left;">공고를 저장한 일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">sftyChckMngcst</td>
<td style="text-align: left;">안전관리비</td>
<td style="text-align: left;">17</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">20309402</td>
<td style="text-align: left;">안전관리비 (원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">bidPrceCalclAYn</td>
<td style="text-align: left;">입찰가격산식A여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">Y</td>
<td style="text-align: left;">나라장터 화면의 입찰공고의 A값 표시여부</td>
</tr>
<tr>
<td style="text-align: left;">bssAmtPurcnstcst</td>
<td style="text-align: left;">기초금액순공사비</td>
<td style="text-align: left;">22</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">기초금액 중 순공사원가 (재료비,노무비,경비,및 이에 대한 부가가치세 합산금액)</td>
</tr>
<tr>
<td style="text-align: left;">qltyMngcst</td>
<td style="text-align: left;">품질관리비</td>
<td style="text-align: left;">22</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">55225988</td>
<td style="text-align: left;">건설공사의 시설물 안전 및 유지관리에 관한 품질시험비(품질시험에 필요한 재료비, 노무비, 경비)와 품질관리활동비(품질시험비 외 품질관리활동에 필요한 비용)에 소요되는 비용</td>
</tr>
<tr>
<td style="text-align: left;">qltyMngcstAObjYn</td>
<td style="text-align: left;">품질관리비A적용대상여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">Y</td>
<td style="text-align: left;">품질관리비가 A값의 합산에 포함히 되는지 적용여부</td>
</tr>
<tr>
<td style="text-align: left;">smkpAmt</td>
<td style="text-align: left;">표준시장단가금액</td>
<td style="text-align: left;">22</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">55225988</td>
<td style="text-align: left;">표준시장단가금액 (원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">smkpAmtYn</td>
<td style="text-align: left;">표준시장단가금액A적용대상여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">표준시장단가금액이 A값의 합산에 포함히 되는지 적용여부</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 요청 / 응답 메시지 예제

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr>
<td style="text-align: center;"><strong>REST(URI)</strong></td>
</tr>
<tr>
<td style="text-align: center;">http://apis.data.go.kr/1230000/ad/BidPublicInfoService/getBidPblancListInfoCnstwkBsisAmount?type=xml&amp;inqryDiv=2&amp;numOfRows=10&amp;pageNo=1&amp;bidNtceNo=R25BK01035950&amp;ServiceKey=인증키</td>
</tr>
<tr>
<td style="text-align: center;"><strong>응답 메시지</strong></td>
</tr>
<tr>
<td style="text-align: center;"><p>&lt;response&gt;</p>
<p>&lt;header&gt;</p>
<p>&lt;resultCode&gt;00&lt;/resultCode&gt;</p>
<p>&lt;resultMsg&gt;정상&lt;/resultMsg&gt;</p>
<p>&lt;/header&gt;</p>
<p>&lt;body&gt;</p>
<p>&lt;items&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK01035950&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;0&lt;/bidClsfcNo&gt;</p>
<p>&lt;bidNtceNm&gt;진주 상상리메이크센터 건립 공사(건축)&lt;/bidNtceNm&gt;</p>
<p>&lt;bssamt&gt;13827624000&lt;/bssamt&gt;</p>
<p>&lt;bssamtOpenDt&gt;2025-09-23 10:58:42&lt;/bssamtOpenDt&gt;</p>
<p>&lt;rsrvtnPrceRngBgnRate&gt;-3&lt;/rsrvtnPrceRngBgnRate&gt;</p>
<p>&lt;rsrvtnPrceRngEndRate&gt;+3&lt;/rsrvtnPrceRngEndRate&gt;</p>
<p>&lt;evlBssAmt&gt;0&lt;/evlBssAmt&gt;</p>
<p>&lt;dfcltydgrCfcnt&gt;0.9&lt;/dfcltydgrCfcnt&gt;</p>
<p>&lt;etcGnrlexpnsBssRate&gt;3.5&lt;/etcGnrlexpnsBssRate&gt;</p>
<p>&lt;gnrlMngcstBssRate&gt;5.13&lt;/gnrlMngcstBssRate&gt;</p>
<p>&lt;prftBssRate&gt;6.78&lt;/prftBssRate&gt;</p>
<p>&lt;lbrcstBssRate&gt;36.01&lt;/lbrcstBssRate&gt;</p>
<p>&lt;sftyMngcst&gt;237064891&lt;/sftyMngcst&gt;</p>
<p>&lt;sftyChckMngcst&gt;102872000&lt;/sftyChckMngcst&gt;</p>
<p>&lt;rtrfundNon&gt;101751069&lt;/rtrfundNon&gt;</p>
<p>&lt;envCnsrvcst&gt;0&lt;/envCnsrvcst&gt;</p>
<p>&lt;scontrctPayprcePayGrntyFee&gt;0&lt;/scontrctPayprcePayGrntyFee&gt;</p>
<p>&lt;mrfnHealthInsrprm&gt;156829366&lt;/mrfnHealthInsrprm&gt;</p>
<p>&lt;npnInsrprm&gt;199078180&lt;/npnInsrprm&gt;</p>
<p>&lt;rmrk1&gt;&lt;/rmrk1&gt;</p>
<p>&lt;rmrk2&gt;&lt;/rmrk2&gt;</p>
<p>&lt;odsnLngtrmrcprInsrprm&gt;20309402&lt;/odsnLngtrmrcprInsrprm&gt;</p>
<p>&lt;usefulAmt&gt;0&lt;/usefulAmt&gt;</p>
<p>&lt;inptDt&gt;2025-09-23 10:58:42&lt;/inptDt&gt;</p>
<p>&lt;bidPrceCalclAYn&gt;Y&lt;/bidPrceCalclAYn&gt;</p>
<p>&lt;bssAmtPurcnstcst&gt;&lt;/bssAmtPurcnstcst&gt;</p>
<p>&lt;qltyMngcst&gt;55225988&lt;/qltyMngcst&gt;</p>
<p>&lt;qltyMngcstAObjYn&gt;Y&lt;/qltyMngcstAObjYn&gt;</p>
<p>&lt;smkpAmt&gt;1513896031&lt;/smkpAmt&gt;</p>
<p>&lt;smkpAmtYn&gt;Y&lt;/smkpAmtYn&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;/items&gt;</p>
<p>&lt;numOfRows&gt;10&lt;/numOfRows&gt;</p>
<p>&lt;pageNo&gt;1&lt;/pageNo&gt;</p>
<p>&lt;totalCount&gt;1&lt;/totalCount&gt;</p>
<p>&lt;/body&gt;</p>
<p>&lt;/response&gt;</p></td>
</tr>
</tbody>
</table>

#### \
\[입찰공고목록 정보에 대한 용역기초금액조회\] 오퍼레이션 명세

<table>
<colgroup>
<col style="width: 4%" />
<col style="width: 21%" />
<col style="width: 17%" />
<col style="width: 21%" />
<col style="width: 2%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr>
<td rowspan="6">오퍼레이션 정보</td>
<td>오퍼레이션 번호</td>
<td>7</td>
<td>오퍼레이션명(국문)</td>
<td colspan="2">입찰공고목록 정보에 대한 용역기초금액조회</td>
</tr>
<tr>
<td>오퍼레이션 유형</td>
<td>조회(목록)</td>
<td>오퍼레이션명(영문)</td>
<td colspan="2">getBidPblancListInfoServcBsisAmount</td>
</tr>
<tr>
<td>오퍼레이션 설명</td>
<td colspan="4">검색조건에 기초금액 등록일시, 입찰공고번호를 입력하여 입찰공고번호, 입찰공고명, 기초금액, 기초금액공개일시, 예비가격범위시작율, 평가기준금액, 난이도계수, 기타경비기준율 등의 용역의 기초금액정보 조회</td>
</tr>
<tr>
<td>Call Back URL</td>
<td colspan="4">N/A</td>
</tr>
<tr>
<td>최대 메시지 사이즈</td>
<td colspan="4">[ 4000bytes]</td>
</tr>
<tr>
<td>평균 응답 시간</td>
<td>[ 500 ms]</td>
<td colspan="2">초당 최대 트랜잭션</td>
<td>[ 30 tps]</td>
</tr>
</tbody>
</table>

##### 요청 메시지 명세

<table>
<colgroup>
<col style="width: 19%" />
<col style="width: 19%" />
<col style="width: 13%" />
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 21%" />
</colgroup>
<tbody>
<tr>
<td>항목명(영문)</td>
<td>항목명(국문)</td>
<td>항목크기</td>
<td>항목구분</td>
<td>샘플데이터</td>
<td>항목설명</td>
</tr>
<tr>
<td style="text-align: left;">numOfRows</td>
<td style="text-align: left;">한 페이지 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td style="text-align: left;">pageNo</td>
<td style="text-align: left;">페이지 번호</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">페이지 번호</td>
</tr>
<tr>
<td style="text-align: left;">ServiceKey</td>
<td style="text-align: left;">서비스키</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">공공데이터포탈에서 받은 인증키</td>
<td style="text-align: left;">공공데이터포탈에서 받은 인증키</td>
</tr>
<tr>
<td style="text-align: left;">type</td>
<td style="text-align: left;">타입</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">0</td>
<td>json</td>
<td>오픈API 리턴 타입을 JSON으로 받고 싶을 경우 'json' 으로 지정</td>
</tr>
<tr>
<td style="text-align: left;">inqryDiv</td>
<td style="text-align: left;">조회구분</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">검색하고자하는 조회구분<br />
1:입력일시 , 2.입찰공고번호</td>
</tr>
<tr>
<td style="text-align: left;">inqryBgnDt</td>
<td style="text-align: left;">조회시작일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">202509230000</td>
<td style="text-align: left;">검색하고자하는 조회시작일시 "YYYYMMDDHHMM"<br />
(조회구분 '1' 선택시 필수)</td>
</tr>
<tr>
<td style="text-align: left;">inqryEndDt</td>
<td style="text-align: left;">조회종료일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">202509232359</td>
<td style="text-align: left;">검색하고자하는 조회종료일시 "YYYYMMDDHHMM"<br />
(조회구분 '1' 선택시 필수)</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNo</td>
<td style="text-align: left;">입찰공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25BK01057292</td>
<td style="text-align: left;">검색하고자 하는 입찰공고번호<br />
(조회구분 '2' 선택시 필수)</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 응답 메시지 명세

<table>
<colgroup>
<col style="width: 20%" />
<col style="width: 18%" />
<col style="width: 14%" />
<col style="width: 13%" />
<col style="width: 13%" />
<col style="width: 19%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;">항목명(영문)</th>
<th style="text-align: center;"><strong>항목명(국문)</strong></th>
<th style="text-align: center;"><strong>항목크기</strong></th>
<th style="text-align: center;"><strong>항목구분</strong></th>
<th style="text-align: center;"><strong>샘플데이터</strong></th>
<th style="text-align: center;"><strong>항목설명</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;">resultCode</td>
<td style="text-align: left;">결과코드</td>
<td style="text-align: left;">2</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">00</td>
<td style="text-align: left;">결과코드</td>
</tr>
<tr>
<td style="text-align: left;">resultMsg</td>
<td style="text-align: left;">결과메세지</td>
<td style="text-align: left;">50</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">정상.</td>
<td style="text-align: left;">결과메세지</td>
</tr>
<tr>
<td style="text-align: left;">numOfRows</td>
<td style="text-align: left;">한 페이지 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td style="text-align: left;">pageNo</td>
<td style="text-align: left;">페이지 번호</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">페이지 번호</td>
</tr>
<tr>
<td style="text-align: left;">totalCount</td>
<td style="text-align: left;">데이터 총 개수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">17</td>
<td style="text-align: left;">데이터 총개수</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNo</td>
<td style="text-align: left;">입찰공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">R25BK01057292</td>
<td style="text-align: left;"><p>입찰공고 관리번입찰공고 관리번호이며 조달청나라장터 공고건의 형식은 년도(4)+월(2)+순번(5)이며 자체전자조달시스템 보유기관은 각 기관별 형식 별도 사용</p>
<p>*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성</p>
<p>-단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</p></td>
</tr>
<tr>
<td style="text-align: left;">bidNtceOrd</td>
<td style="text-align: left;">입찰공고차수</td>
<td style="text-align: left;">3</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">000</td>
<td style="text-align: left;">입찰공고차수는 해당 입찰공고에 대한 재공고 및 재입찰 등이 발생되었을 경우 증가되는 수</td>
</tr>
<tr>
<td style="text-align: left;">bidClsfcNo</td>
<td style="text-align: left;">입찰분류번호</td>
<td style="text-align: left;">5</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">공고의 입찰분류번호</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNm</td>
<td style="text-align: left;">입찰공고명</td>
<td style="text-align: left;">1000</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">2025년 교직원 인플루엔자 예방접종 지원사업 위탁 용역</td>
<td style="text-align: left;">공사명 또는 사업명이라고도 하며 입찰공고 내용을 요약한 이름</td>
</tr>
<tr>
<td style="text-align: left;">bssamt</td>
<td style="text-align: left;">기초금액</td>
<td style="text-align: left;">21</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">109352720</td>
<td style="text-align: left;">예정가격 작성 과정에서 거래실례가격, 원가계산가격 등에 의하여 조사한 가격이나 설계가격에 대하여 계약담당공무원이 그 적정여부를 검토조정한 가격(기초금액)(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">bssamtOpenDt</td>
<td style="text-align: left;">기초금액공개일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-09-23 09:41:50</td>
<td style="text-align: left;">기초금액공개일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">rsrvtnPrceRngBgnRate</td>
<td style="text-align: left;">예비가격범위시작률</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">-3</td>
<td style="text-align: left;">예비가격범위시작율(%)</td>
</tr>
<tr>
<td style="text-align: left;">rsrvtnPrceRngEndRate</td>
<td style="text-align: left;">예비가격범위종료율</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">+3</td>
<td style="text-align: left;">예비가격범위종료율(%)</td>
</tr>
<tr>
<td style="text-align: left;">evlBssAmt</td>
<td style="text-align: left;">평가기준금액</td>
<td style="text-align: left;">21</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">적정성 평가를 위한 평가기준금액(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">dfcltydgrCfcnt</td>
<td style="text-align: left;">난이도계수</td>
<td style="text-align: left;">5</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N/A</td>
<td style="text-align: left;">적정성 평가를 위한 난이도계수</td>
</tr>
<tr>
<td style="text-align: left;">etcGnrlexpnsBssRate</td>
<td style="text-align: left;">기타경비기준율</td>
<td style="text-align: left;">8</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N/A</td>
<td style="text-align: left;">기타경비기준율(%)</td>
</tr>
<tr>
<td style="text-align: left;">gnrlMngcstBssRate</td>
<td style="text-align: left;">일반관리비기준율</td>
<td style="text-align: left;">8</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N/A</td>
<td style="text-align: left;">일반관리비기준율(%)</td>
</tr>
<tr>
<td style="text-align: left;">prftBssRate</td>
<td style="text-align: left;">이윤기준율</td>
<td style="text-align: left;">8</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N/A</td>
<td style="text-align: left;">이윤기준율(%)</td>
</tr>
<tr>
<td style="text-align: left;">lbrcstBssRate</td>
<td style="text-align: left;">노무비기준율</td>
<td style="text-align: left;">8</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N/A</td>
<td style="text-align: left;">노무비기준율(%)</td>
</tr>
<tr>
<td style="text-align: left;">sftyMngcst</td>
<td style="text-align: left;">산업안전보건관리비</td>
<td style="text-align: left;">17</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">산업안전보건관리비 (원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">rtrfundNon</td>
<td style="text-align: left;">퇴직공제부금비</td>
<td style="text-align: left;">17</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">퇴직공제부금비(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">envCnsrvcst</td>
<td style="text-align: left;">환경보전비</td>
<td style="text-align: left;">15</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">환경보전비(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">scontrctPayprcePayGrntyFee</td>
<td style="text-align: left;">하도급대금지급보증수수료</td>
<td style="text-align: left;">21</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">하도급대금지급보증수수료(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">mrfnHealthInsrprm</td>
<td style="text-align: left;">국민건강보험료</td>
<td style="text-align: left;">18</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">국민건강보험료(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">npnInsrprm</td>
<td style="text-align: left;">국민연금보험료</td>
<td style="text-align: left;">18</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">국민연금보험료(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">rmrk1</td>
<td style="text-align: left;">비고1</td>
<td style="text-align: left;">1000</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">기초금액은 부가세 포함 가격임.</td>
<td style="text-align: left;">기초금액 공개시 업체에게 전달할 메세지사항1</td>
</tr>
<tr>
<td style="text-align: left;">rmrk2</td>
<td style="text-align: left;">비고2</td>
<td style="text-align: left;">1000</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">규격서 참조(엔드밀 외 29종)</td>
<td style="text-align: left;">기초금액 공개시 업체에게 전달할 메세지사항2</td>
</tr>
<tr>
<td style="text-align: left;">odsnLngtrmrcprInsrprm</td>
<td style="text-align: left;">노인장기요양보험료</td>
<td style="text-align: left;">18</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">노인장기요양보험료(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">usefulAmt</td>
<td style="text-align: left;">가용금액</td>
<td style="text-align: left;">21</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">수요기관 예산에서 수수료를 제외한 금액(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">inptDt</td>
<td style="text-align: left;">입력일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">2025-09-23 09:41:50</td>
<td style="text-align: left;">공고를 저장한 일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">sftyChckMngcst</td>
<td style="text-align: left;">안전관리비</td>
<td style="text-align: left;">17</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">안전관리비 (원화,원)</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 요청 / 응답 메시지 예제

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr>
<td style="text-align: center;"><strong>REST(URI)</strong></td>
</tr>
<tr>
<td style="text-align: center;">http://apis.data.go.kr/1230000/ad/BidPublicInfoService/getBidPblancListInfoServcBsisAmount?type=xml&amp;inqryDiv=2&amp;numOfRows=10&amp;pageNo=1&amp;bidNtceNo=R25BK01057292&amp;ServiceKey=인증키</td>
</tr>
<tr>
<td style="text-align: center;"><strong>응답 메시지</strong></td>
</tr>
<tr>
<td style="text-align: center;"><p>&lt;response&gt;</p>
<p>&lt;header&gt;</p>
<p>&lt;resultCode&gt;00&lt;/resultCode&gt;</p>
<p>&lt;resultMsg&gt;정상&lt;/resultMsg&gt;</p>
<p>&lt;/header&gt;</p>
<p>&lt;body&gt;</p>
<p>&lt;items&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK01057292&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;0&lt;/bidClsfcNo&gt;</p>
<p>&lt;bidNtceNm&gt;2025년 교직원 인플루엔자 예방접종 지원사업 위탁 용역&lt;/bidNtceNm&gt;</p>
<p>&lt;bssamt&gt;109352720&lt;/bssamt&gt;</p>
<p>&lt;bssamtOpenDt&gt;2025-09-23 09:41:50&lt;/bssamtOpenDt&gt;</p>
<p>&lt;rsrvtnPrceRngBgnRate&gt;-3&lt;/rsrvtnPrceRngBgnRate&gt;</p>
<p>&lt;rsrvtnPrceRngEndRate&gt;+3&lt;/rsrvtnPrceRngEndRate&gt;</p>
<p>&lt;evlBssAmt&gt;0&lt;/evlBssAmt&gt;</p>
<p>&lt;dfcltydgrCfcnt&gt;&lt;/dfcltydgrCfcnt&gt;</p>
<p>&lt;etcGnrlexpnsBssRate&gt;&lt;/etcGnrlexpnsBssRate&gt;</p>
<p>&lt;gnrlMngcstBssRate&gt;&lt;/gnrlMngcstBssRate&gt;</p>
<p>&lt;prftBssRate&gt;&lt;/prftBssRate&gt;</p>
<p>&lt;lbrcstBssRate&gt;&lt;/lbrcstBssRate&gt;</p>
<p>&lt;sftyMngcst&gt;0&lt;/sftyMngcst&gt;</p>
<p>&lt;sftyChckMngcst&gt;0&lt;/sftyChckMngcst&gt;</p>
<p>&lt;rtrfundNon&gt;0&lt;/rtrfundNon&gt;</p>
<p>&lt;envCnsrvcst&gt;0&lt;/envCnsrvcst&gt;</p>
<p>&lt;scontrctPayprcePayGrntyFee&gt;0&lt;/scontrctPayprcePayGrntyFee&gt;</p>
<p>&lt;mrfnHealthInsrprm&gt;0&lt;/mrfnHealthInsrprm&gt;</p>
<p>&lt;npnInsrprm&gt;0&lt;/npnInsrprm&gt;</p>
<p>&lt;rmrk1&gt;&lt;/rmrk1&gt;</p>
<p>&lt;rmrk2&gt;&lt;/rmrk2&gt;</p>
<p>&lt;odsnLngtrmrcprInsrprm&gt;0&lt;/odsnLngtrmrcprInsrprm&gt;</p>
<p>&lt;usefulAmt&gt;0&lt;/usefulAmt&gt;</p>
<p>&lt;inptDt&gt;2025-09-23 09:41:50&lt;/inptDt&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;/items&gt;</p>
<p>&lt;numOfRows&gt;999&lt;/numOfRows&gt;</p>
<p>&lt;pageNo&gt;1&lt;/pageNo&gt;</p>
<p>&lt;totalCount&gt;1&lt;/totalCount&gt;</p>
<p>&lt;/body&gt;</p>
<p>&lt;/response&gt;</p></td>
</tr>
</tbody>
</table>

#### \
\[입찰공고목록 정보에 대한 물품변경이력조회\] 오퍼레이션 명세

<table>
<colgroup>
<col style="width: 4%" />
<col style="width: 21%" />
<col style="width: 17%" />
<col style="width: 21%" />
<col style="width: 2%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr>
<td rowspan="6">오퍼레이션 정보</td>
<td>오퍼레이션 번호</td>
<td>8</td>
<td>오퍼레이션명(국문)</td>
<td colspan="2">입찰공고목록 정보에 대한 물품변경이력조회</td>
</tr>
<tr>
<td>오퍼레이션 유형</td>
<td>조회(목록)</td>
<td>오퍼레이션명(영문)</td>
<td colspan="2">getBidPblancListInfoChgHstryThng</td>
</tr>
<tr>
<td>오퍼레이션 설명</td>
<td colspan="4"><p>검색조건에 변경일시, 입찰공고번호를 입력하여 변경된 입찰공고번호, 입찰공고차수, 입찰분류번호, 재입찰번호, 변경항목명, 변경전후값 등 물품 입찰공고변경 데이터 조회</p>
<p>※ 변경이력 추출 대상 항목</p>
<p>PQ신청서접수일시, 물품분류제한여부, 제조여부, 입찰서개시일시, 입찰서마감일시, 개찰일시, 입찰자격등록일시, 공동수급협정서마감일시, PQ신청서접수방법명, 참가가능지역, 면허제한코드, 설명회실시일시, 입찰참가제한여부, 공고서, 규격서, 공고규격화일, 공동수급구성방식코드, 입찰계약방법코드, 공동수급구성방식,실적신청서접수일시, 공고명, 재입찰허용여부, 실적신청서접수방법코드,예가방법구분코드, 집행관코드, 추첨복수예가개수, 배정예산금액,총예가개수, 추정가격, 내역입찰여부, 지사투찰허용여부</p></td>
</tr>
<tr>
<td>Call Back URL</td>
<td colspan="4">N/A</td>
</tr>
<tr>
<td>최대 메시지 사이즈</td>
<td colspan="4">[ 4000bytes]</td>
</tr>
<tr>
<td>평균 응답 시간</td>
<td>[ 500 ms]</td>
<td colspan="2">초당 최대 트랜잭션</td>
<td>[ 30 tps]</td>
</tr>
</tbody>
</table>

##### 요청 메시지 명세

<table>
<colgroup>
<col style="width: 19%" />
<col style="width: 19%" />
<col style="width: 13%" />
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 21%" />
</colgroup>
<tbody>
<tr>
<td>항목명(영문)</td>
<td>항목명(국문)</td>
<td>항목크기</td>
<td>항목구분</td>
<td>샘플데이터</td>
<td>항목설명</td>
</tr>
<tr>
<td style="text-align: left;">numOfRows</td>
<td style="text-align: left;">한 페이지 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td style="text-align: left;">pageNo</td>
<td style="text-align: left;">페이지 번호</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">페이지 번호</td>
</tr>
<tr>
<td style="text-align: left;">ServiceKey</td>
<td style="text-align: left;">서비스키</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">공공데이터포탈에서 받은 인증키</td>
<td style="text-align: left;">공공데이터포탈에서 받은 인증키</td>
</tr>
<tr>
<td style="text-align: left;">type</td>
<td style="text-align: left;">타입</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">0</td>
<td>json</td>
<td>오픈API 리턴 타입을 JSON으로 받고 싶을 경우 'json' 으로 지정</td>
</tr>
<tr>
<td style="text-align: left;">inqryDiv</td>
<td style="text-align: left;">조회구분</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">검색하고자하는 조회구분<br />
1:변경일시 , 2.입찰공고번호</td>
</tr>
<tr>
<td style="text-align: left;">inqryBgnDt</td>
<td style="text-align: left;">조회시작일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">202509010000</td>
<td style="text-align: left;">검색하고자하는 변경일시시작 'YYYYMMDDHHMM'<br />
조회구분이 1일 경우 필수</td>
</tr>
<tr>
<td style="text-align: left;">inqryEndDt</td>
<td style="text-align: left;">조회종료일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">202509012359</td>
<td style="text-align: left;">검색하고자하는 변경일시종료 'YYYYMMDDHHMM'<br />
조회구분이 1일 경우 필수</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNo</td>
<td style="text-align: left;">입찰공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25BK01016776</td>
<td style="text-align: left;">검색하고자하는 입찰공고번호<br />
조회구분이 2일 경우 필수</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 응답 메시지 명세

<table>
<colgroup>
<col style="width: 20%" />
<col style="width: 18%" />
<col style="width: 14%" />
<col style="width: 13%" />
<col style="width: 13%" />
<col style="width: 19%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;">항목명(영문)</th>
<th style="text-align: center;"><strong>항목명(국문)</strong></th>
<th style="text-align: center;"><strong>항목크기</strong></th>
<th style="text-align: center;"><strong>항목구분</strong></th>
<th style="text-align: center;"><strong>샘플데이터</strong></th>
<th style="text-align: center;"><strong>항목설명</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;">resultCode</td>
<td style="text-align: left;">결과코드</td>
<td style="text-align: left;">2</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">00</td>
<td style="text-align: left;">결과코드</td>
</tr>
<tr>
<td style="text-align: left;">resultMsg</td>
<td style="text-align: left;">결과메세지</td>
<td style="text-align: left;">50</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">정상.</td>
<td style="text-align: left;">결과메세지</td>
</tr>
<tr>
<td style="text-align: left;">numOfRows</td>
<td style="text-align: left;">한 페이지 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td style="text-align: left;">pageNo</td>
<td style="text-align: left;">페이지 번호</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">페이지 번호</td>
</tr>
<tr>
<td style="text-align: left;">totalCount</td>
<td style="text-align: left;">데이터 총 개수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">17</td>
<td style="text-align: left;">데이터 총개수</td>
</tr>
<tr>
<td style="text-align: left;">bsnsDivNm</td>
<td style="text-align: left;">업무구분명</td>
<td style="text-align: left;">30</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">물품</td>
<td style="text-align: left;">입찰업무를 구분하는 명으로 물품, 용역, 공사, 외자로 구분함</td>
</tr>
<tr>
<td style="text-align: left;">chgDataDivNm</td>
<td style="text-align: left;">변경데이터구분명</td>
<td style="text-align: left;">30</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">개찰결과</td>
<td style="text-align: left;">"입찰공고"또는 "개찰결과"로 표기됨</td>
</tr>
<tr>
<td style="text-align: left;">chgDt</td>
<td style="text-align: left;">변경일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">2025-09-01 14:12:41</td>
<td style="text-align: left;">입찰공고 내역이 변경된 일시</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNo</td>
<td style="text-align: left;">입찰공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">R25BK01016776</td>
<td style="text-align: left;"><p>입찰공고 관리번입찰공고 관리번호이며 조달청나라장터 공고건의 형식은 년도(4)+월(2)+순번(5)이며 자체전자조달시스템 보유기관은 각 기관별 형식 별도 사용</p>
<p>*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성</p>
<p>-단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</p></td>
</tr>
<tr>
<td style="text-align: left;">bidNtceOrd</td>
<td style="text-align: left;">입찰공고차수</td>
<td style="text-align: left;">3</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">000</td>
<td style="text-align: left;">입찰공고차수는 해당 입찰공고에 대한 재공고 및 재입찰 등이 발생되었을 경우 증가되는 수</td>
</tr>
<tr>
<td style="text-align: left;">bidClsfcNo</td>
<td style="text-align: left;">입찰분류번호</td>
<td style="text-align: left;">5</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">공고의 입찰분류번호</td>
</tr>
<tr>
<td style="text-align: left;">rbidNo</td>
<td style="text-align: left;">재입찰번호</td>
<td style="text-align: left;">11</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">000</td>
<td style="text-align: left;">재입찰번호</td>
</tr>
<tr>
<td style="text-align: left;">chgItemNm</td>
<td style="text-align: left;">변경항목명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">개찰일시</td>
<td style="text-align: left;">입찰공고 내역이 변경된 항목의 명으로 대상항목은 PQ신청서접수일시, 물품분류제한여부, 제조여부, 입찰서개시일시, 입찰서마감일시, 개찰일시, 입찰자격등록일시, 공동수급협정서마감일시, PQ신청서접수방법명, 참가가능지역, 면허제한코드, 설명회실시일시, 입찰참가제한여부, 공고서, 규격서, 공고규격화일, 공동수급구성방식코드, 입찰계약방법코드, 공동수급구성방식,실적신청서접수일시, 공고명, 재입찰허용여부, 실적신청서접수방법코드,예가방법구분코드, 집행관코드, 추첨복수예가개수, 배정예산금액,총예가개수, 추정가격, 내역입찰여부, 지사투찰허용여부</td>
</tr>
<tr>
<td style="text-align: left;">bfchgVal</td>
<td style="text-align: left;">변경전값</td>
<td style="text-align: left;">2000</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025/09/03 12:00</td>
<td style="text-align: left;">변경항목명에 해당하는 변경전 값<br />
예) 변경항목명이 입찰서개시일시일 경우 변경전값이 2015-05-04 09:00</td>
</tr>
<tr>
<td style="text-align: left;">afchgVal</td>
<td style="text-align: left;">변경후값</td>
<td style="text-align: left;">2000</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">202509011500</td>
<td style="text-align: left;">변경항목명에 해당하는 변경후값<br />
예) 변경항목명이 입찰서개시일시일 경우 변경후값이 2015-05-04 13:00</td>
</tr>
<tr>
<td style="text-align: left;">lcnsLmtCdRgstList</td>
<td style="text-align: left;">면허제한코드등록목록</td>
<td style="text-align: left;">4000</td>
<td style="text-align: left;">0..n</td>
<td style="text-align: left;">N/A</td>
<td style="text-align: left;">입찰공고 면허제한코드 등록목록</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 요청 / 응답 메시지 예제

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr>
<td style="text-align: center;"><strong>REST(URI)</strong></td>
</tr>
<tr>
<td style="text-align: center;">http://apis.data.go.kr/1230000/ad/BidPublicInfoService/getBidPblancListInfoChgHstryThng?type=xml&amp;inqryDiv=2&amp;numOfRows=10&amp;pageNo=1&amp;bidNtceNo=R25BK01016776&amp;ServiceKey=인증키</td>
</tr>
<tr>
<td style="text-align: center;"><strong>응답 메시지</strong></td>
</tr>
<tr>
<td style="text-align: center;"><p>&lt;response&gt;</p>
<p>&lt;header&gt;</p>
<p>&lt;resultCode&gt;00&lt;/resultCode&gt;</p>
<p>&lt;resultMsg&gt;정상&lt;/resultMsg&gt;</p>
<p>&lt;/header&gt;</p>
<p>&lt;body&gt;</p>
<p>&lt;items&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bsnsDivNm&gt;물품&lt;/bsnsDivNm&gt;</p>
<p>&lt;chgDataDivNm&gt;개찰결과&lt;/chgDataDivNm&gt;</p>
<p>&lt;chgDt&gt;2025-09-01 14:12:41&lt;/chgDt&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK01016776&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;1&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;chgItemNm&gt;개찰일시&lt;/chgItemNm&gt;</p>
<p>&lt;bfchgVal&gt;2025/09/03 12:00&lt;/bfchgVal&gt;</p>
<p>&lt;afchgVal&gt;202509011500&lt;/afchgVal&gt;</p>
<p>&lt;lcnsLmtCdRgstList&gt;&lt;/lcnsLmtCdRgstList&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;/items&gt;</p>
<p>&lt;numOfRows&gt;10&lt;/numOfRows&gt;</p>
<p>&lt;pageNo&gt;1&lt;/pageNo&gt;</p>
<p>&lt;totalCount&gt;1&lt;/totalCount&gt;</p>
<p>&lt;/body&gt;</p>
<p>&lt;/response&gt;</p></td>
</tr>
</tbody>
</table>

#### \[입찰공고목록 정보에 대한 공사변경이력조회\] 오퍼레이션 명세

<table style="width:96%;">
<colgroup>
<col style="width: 4%" />
<col style="width: 21%" />
<col style="width: 18%" />
<col style="width: 22%" />
<col style="width: 2%" />
<col style="width: 27%" />
</colgroup>
<tbody>
<tr>
<td rowspan="6">오퍼레이션 정보</td>
<td>오퍼레이션 번호</td>
<td>9</td>
<td>오퍼레이션명(국문)</td>
<td colspan="2">입찰공고목록 정보에 대한 공사변경이력조회</td>
</tr>
<tr>
<td>오퍼레이션 유형</td>
<td>조회(목록)</td>
<td>오퍼레이션명(영문)</td>
<td colspan="2">getBidPblancListInfoChgHstryCnstwk</td>
</tr>
<tr>
<td>오퍼레이션 설명</td>
<td colspan="4"><p>검색조건에 변경일시, 입찰공고번호를 입력하여 변경된 입찰공고번호, 입찰공고차수, 입찰분류번호, 재입찰번호, 변경항목명, 변경전후값 등 공사 입찰공고변경 데이터 조회</p>
<p>※ 변경이력 추출 대상 항목</p>
<p>PQ신청서접수일시, 물품분류제한여부, 제조여부, 입찰서개시일시, 입찰서마감일시, 개찰일시, 입찰자격등록일시, 공동수급협정서마감일시, PQ신청서접수방법명, 참가가능지역, 면허제한코드, 설명회실시일시, 입찰참가제한여부, 공고서, 규격서, 공고규격화일, 공동수급구성방식코드, 입찰계약방법코드, 공동수급구성방식,실적신청서접수일시, 공고명, 재입찰허용여부, 실적신청서접수방법코드,예가방법구분코드, 집행관코드, 추첨복수예가개수, 배정예산금액,총예가개수, 추정가격, 내역입찰여부, 지사투찰허용여부</p></td>
</tr>
<tr>
<td>Call Back URL</td>
<td colspan="4">N/A</td>
</tr>
<tr>
<td>최대 메시지 사이즈</td>
<td colspan="4">[ 4000bytes]</td>
</tr>
<tr>
<td>평균 응답 시간</td>
<td>[ 500 ms]</td>
<td colspan="2">초당 최대 트랜잭션</td>
<td>[ 30 tps]</td>
</tr>
</tbody>
</table>

##### 요청 메시지 명세

<table style="width:98%;">
<colgroup>
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 13%" />
<col style="width: 12%" />
<col style="width: 13%" />
<col style="width: 17%" />
</colgroup>
<tbody>
<tr>
<td style="text-align: left;">항목명(영문)</td>
<td style="text-align: left;">항목명(국문)</td>
<td style="text-align: left;">항목크기</td>
<td style="text-align: left;">항목구분</td>
<td style="text-align: left;">샘플데이터</td>
<td style="text-align: left;">항목설명</td>
</tr>
<tr>
<td style="text-align: left;">numOfRows</td>
<td style="text-align: left;">한 페이지 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td style="text-align: left;">pageNo</td>
<td style="text-align: left;">페이지 번호</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">페이지 번호</td>
</tr>
<tr>
<td style="text-align: left;">ServiceKey</td>
<td style="text-align: left;">서비스키</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">공공데이터포탈에서 받은 인증키</td>
<td style="text-align: left;">공공데이터포탈에서 받은 인증키</td>
</tr>
<tr>
<td style="text-align: left;">type</td>
<td style="text-align: left;">타입</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">json</td>
<td style="text-align: left;">오픈API 리턴 타입을 JSON으로 받고 싶을 경우 'json' 으로 지정</td>
</tr>
<tr>
<td style="text-align: left;">inqryDiv</td>
<td style="text-align: left;">조회구분</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">검색하고자하는 조회구분<br />
1:변경일시 , 2.입찰공고번호</td>
</tr>
<tr>
<td style="text-align: left;">inqryBgnDt</td>
<td style="text-align: left;">조회시작일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">202509230000</td>
<td style="text-align: left;">검색하고자하는 변경일시시작 'YYYYMMDDHHMM'<br />
조회구분이 1일 경우 필수</td>
</tr>
<tr>
<td style="text-align: left;">inqryEndDt</td>
<td style="text-align: left;">조회종료일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">202509232359</td>
<td style="text-align: left;">검색하고자하는 변경일시종료 'YYYYMMDDHHMM'<br />
조회구분이 1일 경우 필수</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNo</td>
<td style="text-align: left;">입찰공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25BK00979664</td>
<td style="text-align: left;">검색하고자하는 입찰공고번호<br />
조회구분이 2일 경우 필수</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 응답 메시지 명세

<table style="width:98%;">
<colgroup>
<col style="width: 21%" />
<col style="width: 18%" />
<col style="width: 14%" />
<col style="width: 13%" />
<col style="width: 13%" />
<col style="width: 16%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;">항목명(영문)</th>
<th style="text-align: left;"><strong>항목명(국문)</strong></th>
<th style="text-align: left;"><strong>항목크기</strong></th>
<th style="text-align: left;"><strong>항목구분</strong></th>
<th style="text-align: left;"><strong>샘플데이터</strong></th>
<th style="text-align: left;"><strong>항목설명</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;">resultCode</td>
<td style="text-align: left;">결과코드</td>
<td style="text-align: left;">2</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">00</td>
<td style="text-align: left;">결과코드</td>
</tr>
<tr>
<td style="text-align: left;">resultMsg</td>
<td style="text-align: left;">결과메세지</td>
<td style="text-align: left;">50</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">정상.</td>
<td style="text-align: left;">결과메세지</td>
</tr>
<tr>
<td style="text-align: left;">numOfRows</td>
<td style="text-align: left;">한 페이지 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td style="text-align: left;">pageNo</td>
<td style="text-align: left;">페이지 번호</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">페이지 번호</td>
</tr>
<tr>
<td style="text-align: left;">totalCount</td>
<td style="text-align: left;">데이터 총 개수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">17</td>
<td style="text-align: left;">데이터 총개수</td>
</tr>
<tr>
<td style="text-align: left;">bsnsDivNm</td>
<td style="text-align: left;">업무구분명</td>
<td style="text-align: left;">30</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">공사</td>
<td style="text-align: left;">입찰업무를 구분하는 명으로 물품, 용역, 공사, 외자로 구분함</td>
</tr>
<tr>
<td style="text-align: left;">chgDataDivNm</td>
<td style="text-align: left;">변경데이터구분명</td>
<td style="text-align: left;">30</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">개찰결과</td>
<td style="text-align: left;">"입찰공고"또는 "개찰결과"로 표기됨</td>
</tr>
<tr>
<td style="text-align: left;">chgDt</td>
<td style="text-align: left;">변경일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">2025-08-19 13:26:19</td>
<td style="text-align: left;">입찰공고 내역이 변경된 일시</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNo</td>
<td style="text-align: left;">입찰공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">R25BK00979664</td>
<td style="text-align: left;"><p>입찰공고 관리번입찰공고 관리번호이며 조달청나라장터 공고건의 형식은 년도(4)+월(2)+순번(5)이며 자체전자조달시스템 보유기관은 각 기관별 형식 별도 사용</p>
<p>*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성</p>
<p>-단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</p></td>
</tr>
<tr>
<td style="text-align: left;">bidNtceOrd</td>
<td style="text-align: left;">입찰공고차수</td>
<td style="text-align: left;">3</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">000</td>
<td style="text-align: left;">입찰공고차수는 해당 입찰공고에 대한 재공고 및 재입찰 등이 발생되었을 경우 증가되는 수</td>
</tr>
<tr>
<td style="text-align: left;">bidClsfcNo</td>
<td style="text-align: left;">입찰분류번호</td>
<td style="text-align: left;">5</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">공고의 입찰분류번호</td>
</tr>
<tr>
<td style="text-align: left;">rbidNo</td>
<td style="text-align: left;">재입찰번호</td>
<td style="text-align: left;">11</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">000</td>
<td style="text-align: left;">재입찰번호</td>
</tr>
<tr>
<td style="text-align: left;">chgItemNm</td>
<td style="text-align: left;">변경항목명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">입찰자격등록일시</td>
<td style="text-align: left;">입찰공고 내역이 변경된 항목의 명으로 대상항목은 PQ신청서접수일시, 물품분류제한여부, 제조여부, 입찰서개시일시, 입찰서마감일시, 개찰일시, 입찰자격등록일시, 공동수급협정서마감일시, PQ신청서접수방법명, 참가가능지역, 면허제한코드, 설명회실시일시, 입찰참가제한여부, 공고서, 규격서, 공고규격화일, 공동수급구성방식코드, 입찰계약방법코드, 공동수급구성방식,실적신청서접수일시, 공고명, 재입찰허용여부, 실적신청서접수방법코드,예가방법구분코드, 집행관코드, 추첨복수예가개수, 배정예산금액,총예가개수, 추정가격, 내역입찰여부, 지사투찰허용여부</td>
</tr>
<tr>
<td style="text-align: left;">bfchgVal</td>
<td style="text-align: left;">변경전값</td>
<td style="text-align: left;">2000</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">20260126 18:00</td>
<td style="text-align: left;">변경항목명에 해당하는 변경전 값<br />
예) 변경항목명이 입찰서마감일시일 경우 변경전값이 '201605061000</td>
</tr>
<tr>
<td style="text-align: left;">afchgVal</td>
<td style="text-align: left;">변경후값</td>
<td style="text-align: left;">2000</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025/08/19 13:26</td>
<td style="text-align: left;">변경항목명에 해당하는 변경후 값<br />
예) 변경항목명이 입찰서마감일시일 경우 변경후값이 201605091000</td>
</tr>
<tr>
<td style="text-align: left;">lcnsLmtCdRgstList</td>
<td style="text-align: left;">면허제한코드변경후목록</td>
<td style="text-align: left;">4000</td>
<td style="text-align: left;">0..n</td>
<td style="text-align: left;">N/A</td>
<td style="text-align: left;">입찰공고 면허제한코드 변경후 목록</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 요청 / 응답 메시지 예제

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr>
<td style="text-align: center;"><strong>REST(URI)</strong></td>
</tr>
<tr>
<td style="text-align: center;">http://apis.data.go.kr/1230000/ad/BidPublicInfoService/getBidPblancListInfoChgHstryCnstwk?type=xml&amp;inqryDiv=2&amp;numOfRows=10&amp;pageNo=1&amp;bidNtceNo=R25BK00979664&amp;ServiceKey=인증키</td>
</tr>
<tr>
<td style="text-align: center;"><strong>응답 메시지</strong></td>
</tr>
<tr>
<td style="text-align: center;"><p>&lt;response&gt;</p>
<p>&lt;header&gt;</p>
<p>&lt;resultCode&gt;00&lt;/resultCode&gt;</p>
<p>&lt;resultMsg&gt;정상&lt;/resultMsg&gt;</p>
<p>&lt;/header&gt;</p>
<p>&lt;body&gt;</p>
<p>&lt;items&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bsnsDivNm&gt;공사&lt;/bsnsDivNm&gt;</p>
<p>&lt;chgDataDivNm&gt;개찰결과&lt;/chgDataDivNm&gt;</p>
<p>&lt;chgDt&gt;2025-08-19 13:26:19&lt;/chgDt&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00979664&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;0&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;chgItemNm&gt;입찰자격등록일시&lt;/chgItemNm&gt;</p>
<p>&lt;bfchgVal&gt;20260126 18:00&lt;/bfchgVal&gt;</p>
<p>&lt;afchgVal&gt;2025/08/19 13:26&lt;/afchgVal&gt;</p>
<p>&lt;lcnsLmtCdRgstList&gt;&lt;/lcnsLmtCdRgstList&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;/items&gt;</p>
<p>&lt;numOfRows&gt;10&lt;/numOfRows&gt;</p>
<p>&lt;pageNo&gt;1&lt;/pageNo&gt;</p>
<p>&lt;totalCount&gt;1&lt;/totalCount&gt;</p>
<p>&lt;/body&gt;</p>
<p>&lt;/response&gt;</p></td>
</tr>
</tbody>
</table>

####  \[입찰공고목록 정보에 대한 용역변경이력조회\] 오퍼레이션 명세

<table style="width:99%;">
<colgroup>
<col style="width: 4%" />
<col style="width: 21%" />
<col style="width: 18%" />
<col style="width: 22%" />
<col style="width: 2%" />
<col style="width: 30%" />
</colgroup>
<tbody>
<tr>
<td rowspan="6">오퍼레이션 정보</td>
<td>오퍼레이션 번호</td>
<td>10</td>
<td>오퍼레이션명(국문)</td>
<td colspan="2">입찰공고목록 정보에 대한 용역변경이력조회</td>
</tr>
<tr>
<td>오퍼레이션 유형</td>
<td>조회(목록)</td>
<td>오퍼레이션명(영문)</td>
<td colspan="2">getBidPblancListInfoChgHstryServc</td>
</tr>
<tr>
<td>오퍼레이션 설명</td>
<td colspan="4"><p>검색조건에 변경일시, 입찰공고번호를 입력하여 변경된 입찰공고번호, 입찰공고차수, 입찰분류번호, 재입찰번호, 변경항목명, 변경전후값 등 용역 입찰공고변경 데이터 조회</p>
<p>※ 변경이력 추출 대상 항목</p>
<p>PQ신청서접수일시, 물품분류제한여부, 제조여부, 입찰서개시일시, 입찰서마감일시, 개찰일시, 입찰자격등록일시, 공동수급협정서마감일시, PQ신청서접수방법명, 참가가능지역, 면허제한코드, 설명회실시일시, 입찰참가제한여부, 공고서, 규격서, 공고규격화일, 공동수급구성방식코드, 입찰계약방법코드, 공동수급구성방식,실적신청서접수일시, 공고명, 재입찰허용여부, 실적신청서접수방법코드,예가방법구분코드, 집행관코드, 추첨복수예가개수, 배정예산금액,총예가개수, 추정가격, 내역입찰여부, 지사투찰허용여부</p></td>
</tr>
<tr>
<td>Call Back URL</td>
<td colspan="4">N/A</td>
</tr>
<tr>
<td>최대 메시지 사이즈</td>
<td colspan="4">[ 4000bytes]</td>
</tr>
<tr>
<td>평균 응답 시간</td>
<td>[ 500 ms]</td>
<td colspan="2">초당 최대 트랜잭션</td>
<td>[ 30 tps]</td>
</tr>
</tbody>
</table>

##### 요청 메시지 명세

<table style="width:99%;">
<colgroup>
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 13%" />
<col style="width: 12%" />
<col style="width: 13%" />
<col style="width: 19%" />
</colgroup>
<tbody>
<tr>
<td style="text-align: left;">항목명(영문)</td>
<td style="text-align: left;">항목명(국문)</td>
<td style="text-align: left;">항목크기</td>
<td style="text-align: left;">항목구분</td>
<td style="text-align: left;">샘플데이터</td>
<td style="text-align: left;">항목설명</td>
</tr>
<tr>
<td style="text-align: left;">numOfRows</td>
<td style="text-align: left;">한 페이지 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td style="text-align: left;">pageNo</td>
<td style="text-align: left;">페이지 번호</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">페이지 번호</td>
</tr>
<tr>
<td style="text-align: left;">type</td>
<td style="text-align: left;">타입</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">json</td>
<td style="text-align: left;">오픈API 리턴 타입을 JSON으로 받고 싶을 경우 'json' 으로 지정</td>
</tr>
<tr>
<td style="text-align: left;">ServiceKey</td>
<td style="text-align: left;">서비스키</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">공공데이터포탈에서 받은 인증키</td>
<td style="text-align: left;">공공데이터포탈에서 받은 인증키</td>
</tr>
<tr>
<td style="text-align: left;">type</td>
<td style="text-align: left;">타입</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">json</td>
<td style="text-align: left;">오픈API 리턴 타입을 JSON으로 받고 싶을 경우 'json' 으로 지정</td>
</tr>
<tr>
<td style="text-align: left;">inqryDiv</td>
<td style="text-align: left;">조회구분</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">검색하고자하는 조회구분<br />
1:변경일시 , 2.입찰공고번호</td>
</tr>
<tr>
<td style="text-align: left;">inqryBgnDt</td>
<td style="text-align: left;">조회시작일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">202509230000</td>
<td style="text-align: left;">검색하고자하는 변경일시시작 'YYYYMMDDHHMM'<br />
조회구분이 1일 경우 필수</td>
</tr>
<tr>
<td style="text-align: left;">inqryEndDt</td>
<td style="text-align: left;">조회종료일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">202509232359</td>
<td style="text-align: left;">검색하고자하는 변경일시종료 'YYYYMMDDHHMM'<br />
조회구분이 1일 경우 필수</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNo</td>
<td style="text-align: left;">입찰공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25BK00664024</td>
<td style="text-align: left;">검색하고자하는 입찰공고번호<br />
조회구분이 2일 경우 필수</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 응답 메시지 명세

<table style="width:98%;">
<colgroup>
<col style="width: 21%" />
<col style="width: 18%" />
<col style="width: 14%" />
<col style="width: 13%" />
<col style="width: 13%" />
<col style="width: 16%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;">항목명(영문)</th>
<th style="text-align: center;"><strong>항목명(국문)</strong></th>
<th style="text-align: center;"><strong>항목크기</strong></th>
<th style="text-align: center;"><strong>항목구분</strong></th>
<th style="text-align: center;"><strong>샘플데이터</strong></th>
<th style="text-align: center;"><strong>항목설명</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;">resultCode</td>
<td style="text-align: left;">결과코드</td>
<td style="text-align: left;">2</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">00</td>
<td style="text-align: left;">결과코드</td>
</tr>
<tr>
<td style="text-align: left;">resultMsg</td>
<td style="text-align: left;">결과메세지</td>
<td style="text-align: left;">50</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">정상.</td>
<td style="text-align: left;">결과메세지</td>
</tr>
<tr>
<td style="text-align: left;">numOfRows</td>
<td style="text-align: left;">한 페이지 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td style="text-align: left;">pageNo</td>
<td style="text-align: left;">페이지 번호</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">페이지 번호</td>
</tr>
<tr>
<td style="text-align: left;">totalCount</td>
<td style="text-align: left;">데이터 총 개수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">17</td>
<td style="text-align: left;">데이터 총개수</td>
</tr>
<tr>
<td style="text-align: left;">bsnsDivNm</td>
<td style="text-align: left;">업무구분명</td>
<td style="text-align: left;">30</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">용역</td>
<td style="text-align: left;">입찰업무를 구분하는 명으로 물품, 용역, 공사, 외자로 구분함</td>
</tr>
<tr>
<td style="text-align: left;">chgDataDivNm</td>
<td style="text-align: left;">변경데이터구분명</td>
<td style="text-align: left;">30</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">개찰결과</td>
<td style="text-align: left;">"입찰공고"또는 "개찰결과"로 표기됨</td>
</tr>
<tr>
<td style="text-align: left;">chgDt</td>
<td style="text-align: left;">변경일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">2025-02-25 11:52:33</td>
<td style="text-align: left;">입찰공고 내역이 변경된 일시</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNo</td>
<td style="text-align: left;">입찰공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">R25BK00664024</td>
<td style="text-align: left;"><p>입찰공고 관리번입찰공고 관리번호이며 조달청나라장터 공고건의 형식은 년도(4)+월(2)+순번(5)이며 자체전자조달시스템 보유기관은 각 기관별 형식 별도 사용</p>
<p>*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성</p>
<p>-단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</p></td>
</tr>
<tr>
<td style="text-align: left;">bidNtceOrd</td>
<td style="text-align: left;">입찰공고차수</td>
<td style="text-align: left;">3</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">000</td>
<td style="text-align: left;">입찰공고차수는 해당 입찰공고에 대한 재공고 및 재입찰 등이 발생되었을 경우 증가되는 수</td>
</tr>
<tr>
<td style="text-align: left;">bidClsfcNo</td>
<td style="text-align: left;">입찰분류번호</td>
<td style="text-align: left;">5</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">공고의 입찰분류번호</td>
</tr>
<tr>
<td style="text-align: left;">rbidNo</td>
<td style="text-align: left;">재입찰번호</td>
<td style="text-align: left;">11</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">000</td>
<td style="text-align: left;">재입찰번호</td>
</tr>
<tr>
<td style="text-align: left;">chgItemNm</td>
<td style="text-align: left;">변경항목명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">입찰자격등록일시</td>
<td style="text-align: left;">입찰공고 내역이 변경된 항목의 명으로 대상항목은 PQ신청서접수일시, 물품분류제한여부, 제조여부, 입찰서개시일시, 입찰서마감일시, 개찰일시, 입찰자격등록일시, 공동수급협정서마감일시, PQ신청서접수방법명, 참가가능지역, 면허제한코드, 설명회실시일시, 입찰참가제한여부, 공고서, 규격서, 공고규격화일, 공동수급구성방식코드, 입찰계약방법코드, 공동수급구성방식,실적신청서접수일시, 공고명, 재입찰허용여부, 실적신청서접수방법코드,예가방법구분코드, 집행관코드, 추첨복수예가개수, 배정예산금액,총예가개수, 추정가격, 내역입찰여부, 지사투찰허용여부</td>
</tr>
<tr>
<td style="text-align: left;">bfchgVal</td>
<td style="text-align: left;">변경전값</td>
<td style="text-align: left;">2000</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">20250303 18:00</td>
<td style="text-align: left;">변경항목명에 해당하는 변경전 값<br />
예) 변경항목명이 입찰서마감일시일 경우 변경전값이 '201605061000</td>
</tr>
<tr>
<td style="text-align: left;">afchgVal</td>
<td style="text-align: left;">변경후값</td>
<td style="text-align: left;">2000</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025/02/25 11:52</td>
<td style="text-align: left;">변경항목명에 해당하는 변경후 값<br />
예) 변경항목명이 입찰서마감일시일 경우 변경후값이 201605091000</td>
</tr>
<tr>
<td style="text-align: left;">lcnsLmtCdRgstList</td>
<td style="text-align: left;">면허제한코드변경후목록</td>
<td style="text-align: left;">4000</td>
<td style="text-align: left;">0..n</td>
<td style="text-align: left;">N/A</td>
<td style="text-align: left;">입찰공고 면허제한코드 변경후 목록</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 요청 / 응답 메시지 예제

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr>
<td style="text-align: center;"><strong>REST(URI)</strong></td>
</tr>
<tr>
<td style="text-align: center;">http://apis.data.go.kr/1230000/ad/BidPublicInfoService/getBidPblancListInfoChgHstryCnstwk?type=xml&amp;inqryDiv=2&amp;numOfRows=10&amp;pageNo=1&amp;bidNtceNo=R25BK00664024&amp;ServiceKey=인증키</td>
</tr>
<tr>
<td style="text-align: center;"><strong>응답 메시지</strong></td>
</tr>
<tr>
<td style="text-align: center;"><p>&lt;response&gt;</p>
<p>&lt;header&gt;</p>
<p>&lt;resultCode&gt;00&lt;/resultCode&gt;</p>
<p>&lt;resultMsg&gt;정상&lt;/resultMsg&gt;</p>
<p>&lt;/header&gt;</p>
<p>&lt;body&gt;</p>
<p>&lt;items&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bsnsDivNm&gt;용역&lt;/bsnsDivNm&gt;</p>
<p>&lt;chgDataDivNm&gt;개찰결과&lt;/chgDataDivNm&gt;</p>
<p>&lt;chgDt&gt;2025-02-25 11:52:33&lt;/chgDt&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00664024&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;0&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;chgItemNm&gt;입찰자격등록일시&lt;/chgItemNm&gt;</p>
<p>&lt;bfchgVal&gt;20250303 18:00&lt;/bfchgVal&gt;</p>
<p>&lt;afchgVal&gt;2025/02/25 11:52&lt;/afchgVal&gt;</p>
<p>&lt;lcnsLmtCdRgstList&gt;&lt;/lcnsLmtCdRgstList&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;/items&gt;</p>
<p>&lt;numOfRows&gt;10&lt;/numOfRows&gt;</p>
<p>&lt;pageNo&gt;1&lt;/pageNo&gt;</p>
<p>&lt;totalCount&gt;1&lt;/totalCount&gt;</p>
<p>&lt;/body&gt;</p>
<p>&lt;/response&gt;</p></td>
</tr>
</tbody>
</table>

#### \[나라장터검색조건에 의한 입찰공고공사조회\] 오퍼레이션 명세

<table style="width:99%;">
<colgroup>
<col style="width: 4%" />
<col style="width: 21%" />
<col style="width: 18%" />
<col style="width: 22%" />
<col style="width: 2%" />
<col style="width: 30%" />
</colgroup>
<tbody>
<tr>
<td rowspan="6">오퍼레이션 정보</td>
<td>오퍼레이션 번호</td>
<td>11</td>
<td>오퍼레이션명(국문)</td>
<td colspan="2">나라장터검색조건에 의한 입찰공고공사조회</td>
</tr>
<tr>
<td>오퍼레이션 유형</td>
<td>조회(목록)</td>
<td>오퍼레이션명(영문)</td>
<td colspan="2">getBidPblancListInfoCnstwkPPSSrch</td>
</tr>
<tr>
<td>오퍼레이션 설명</td>
<td colspan="4">검색조건에 공고게시일시, 개찰일시 범위, 공고기관, 수요기관, 참조번호 등을 입력하여 나라장터의 입찰공고번호, 공고명, 발주기관, 수요기관, 계약체결방법명 등 공사부분의 입찰공고정보를 조회함</td>
</tr>
<tr>
<td>Call Back URL</td>
<td colspan="4">N/A</td>
</tr>
<tr>
<td>최대 메시지 사이즈</td>
<td colspan="4">[ 4000bytes]</td>
</tr>
<tr>
<td>평균 응답 시간</td>
<td>[ 500 ms]</td>
<td colspan="2">초당 최대 트랜잭션</td>
<td>[ 30 tps]</td>
</tr>
</tbody>
</table>

##### 요청 메시지 명세

<table>
<colgroup>
<col style="width: 19%" />
<col style="width: 19%" />
<col style="width: 13%" />
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 21%" />
</colgroup>
<tbody>
<tr>
<td style="text-align: left;">항목명(영문)</td>
<td style="text-align: left;">항목명(국문)</td>
<td style="text-align: left;">항목크기</td>
<td style="text-align: left;">항목구분</td>
<td style="text-align: left;">샘플데이터</td>
<td style="text-align: left;">항목설명</td>
</tr>
<tr>
<td style="text-align: left;">numOfRows</td>
<td style="text-align: left;">한 페이지 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td style="text-align: left;">pageNo</td>
<td style="text-align: left;">페이지 번호</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">페이지 번호</td>
</tr>
<tr>
<td style="text-align: left;">ServiceKey</td>
<td style="text-align: left;">서비스키</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">공공데이터포탈에서 받은 인증키</td>
<td style="text-align: left;">공공데이터포탈에서 받은 인증키</td>
</tr>
<tr>
<td style="text-align: left;">type</td>
<td style="text-align: left;">타입</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">json</td>
<td style="text-align: left;">오픈API 리턴 타입을 JSON으로 받고 싶을 경우 'json' 으로 지정</td>
</tr>
<tr>
<td style="text-align: left;">inqryDiv</td>
<td style="text-align: left;">조회구분</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">검색하고자하는 조회구분<br />
1:공고게시일시, 2:개찰일시<br />
1. 공고게시일시 : 공고일자(pblancDate)<br />
2. 개찰일시 : 개찰일시(opengDt)</td>
</tr>
<tr>
<td style="text-align: left;">inqryBgnDt</td>
<td style="text-align: left;">조회시작일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">202507010000</td>
<td style="text-align: left;">검색하고자 하는 조회시작일시 "YYYYMMDDHHMM"<br />
조회구분이 '1'인 경우 공고게시일시 필수, '2'인 경우 개찰일시 필수</td>
</tr>
<tr>
<td style="text-align: left;">inqryEndDt</td>
<td style="text-align: left;">조회종료일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">202507012359</td>
<td style="text-align: left;">검색하고자 하는 조회종료일시 "YYYYMMDDHHMM"<br />
조회구분이 '1'인 경우 공고게시일시 필수, '2'인 경우 개찰일시 필수</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNm</td>
<td style="text-align: left;">입찰공고명</td>
<td style="text-align: left;">1000</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025년 인천글로벌캠퍼스 지원센터 변유량 냉수펌프 제어판넬 개선 공사 전자견적제출 안내공고</td>
<td style="text-align: left;">검색하고자하는 공고명<br />
※ 공고명 일부 입력시에도 조회 가능</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttCd</td>
<td style="text-align: left;">공고기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">Z023597</td>
<td style="text-align: left;">검색하고자하는 공고기관코드</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttNm</td>
<td style="text-align: left;">공고기관명</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">인천글로벌캠퍼스운영 재단법인</td>
<td style="text-align: left;">검색하고자하는 공고기관명<br />
※ 공고기관명 일부 입력시에도 조회 가능</td>
</tr>
<tr>
<td style="text-align: left;">dminsttCd</td>
<td style="text-align: left;">수요기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">Z023597</td>
<td style="text-align: left;">검색하고자하는 수요기관코드<br />
행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드 입력<br />
행자부코드가 없는 경우 조달청에서 부여한 수요기관 코드 입력</td>
</tr>
<tr>
<td style="text-align: left;">dminsttNm</td>
<td style="text-align: left;">수요기관명</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">인천글로벌캠퍼스운영 재단법인</td>
<td style="text-align: left;">검색하고자하는 수요기관명<br />
※ 수요기관명 일부 입력시에도 조회 가능</td>
</tr>
<tr>
<td style="text-align: left;">refNo</td>
<td style="text-align: left;">참조번호</td>
<td style="text-align: left;">105</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-44</td>
<td style="text-align: left;">검색하고자하는 참조번호</td>
</tr>
<tr>
<td style="text-align: left;">prtcptLmtRgnCd</td>
<td style="text-align: left;">참가제한지역코드</td>
<td style="text-align: left;">2</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">28</td>
<td style="text-align: left;">검색하고자하는 참가제한지역코드<br />
11 : 서울특별시<br />
26 : 부산광역시<br />
27 : 대구광역시<br />
28 : 인천광역시<br />
29 : 광주광역시<br />
30 : 대전광역시<br />
31 : 울산광역시<br />
36 : 세종특별자치시<br />
41 : 경기도<br />
42 : 강원도<br />
43 : 충청북도<br />
44 : 충청남도<br />
45 : 전라북도<br />
46 : 전라남도<br />
47 : 경상북도<br />
48 : 경상남도<br />
50 : 제주도<br />
51 : 강원특별자치도<br />
52 : 전북특별자치도<br />
99 : 기타<br />
00: 전국<br />
*전국 : 지역제한을 설정하지 않은 공고</td>
</tr>
<tr>
<td style="text-align: left;">prtcptLmtRgnNm</td>
<td style="text-align: left;">참가제한지역명</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">인천광역시</td>
<td style="text-align: left;">검색하고자하는 참가제한지역명<br />
※ 참가제한지역명 일부 입력시에도 조회 가능<br />
*전국 : 지역제한을 설정하지 않은 공고</td>
</tr>
<tr>
<td style="text-align: left;">indstrytyCd</td>
<td style="text-align: left;">업종코드</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">6202</td>
<td style="text-align: left;">검색하고자하는 업종코드</td>
</tr>
<tr>
<td style="text-align: left;">indstrytyNm</td>
<td style="text-align: left;">업종명</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">기계설비ㆍ가스공사업</td>
<td style="text-align: left;">검색하고자하는 업종명<br />
※ 업종명 일부 입력시에도 조회 가능</td>
</tr>
<tr>
<td style="text-align: left;">presmptPrceBgn</td>
<td style="text-align: left;">추정가격시작</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">180645355</td>
<td style="text-align: left;">검색하고자하는 추정가격범위시작금액이상(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">presmptPrceEnd</td>
<td style="text-align: left;">추정가격종료</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">180645555</td>
<td style="text-align: left;">검색하고자하는 추정가격범위종료금액이하(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">dtilPrdctClsfcNo</td>
<td style="text-align: left;">세부품명번호</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0000000000</td>
<td style="text-align: left;">검색하고자하는 세부품명번호<br />
(공사업무의 경우 해당 컬럼 검색 불가)</td>
</tr>
<tr>
<td style="text-align: left;">masYn</td>
<td style="text-align: left;">다수공급경쟁자여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">검색하고자하는 다수공급경쟁자여부<br />
(공사업무의 경우 해당 컬럼 검색 불가)</td>
</tr>
<tr>
<td style="text-align: left;">prcrmntReqNo</td>
<td style="text-align: left;">조달요청번호</td>
<td style="text-align: left;">17</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25DC00049909</td>
<td style="text-align: left;">검색하고자하는 조달요청번호</td>
</tr>
<tr>
<td style="text-align: left;">bidClseExcpYn</td>
<td style="text-align: left;">입찰마감제외여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">검색하고자하는 입찰마감제외여부</td>
</tr>
<tr>
<td style="text-align: left;">intrntnlDivCd</td>
<td style="text-align: left;">국제입찰구분코드</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">검색하고자하는 국제구분코드<br />
국내: 1, 국제: 2<br />
국내/시설 입찰 공고일 경우 : 1<br />
국외 입찰 공고일 경우 : 2</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 응답 메시지 명세

<table>
<colgroup>
<col style="width: 16%" />
<col style="width: 16%" />
<col style="width: 16%" />
<col style="width: 16%" />
<col style="width: 16%" />
<col style="width: 19%" />
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
<td style="text-align: left;">resultCode</td>
<td style="text-align: left;">결과코드</td>
<td style="text-align: left;">2</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">00</td>
<td style="text-align: left;">결과코드</td>
</tr>
<tr>
<td style="text-align: left;">resultMsg</td>
<td style="text-align: left;">결과메세지</td>
<td style="text-align: left;">50</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">정상</td>
<td style="text-align: left;">결과메세지</td>
</tr>
<tr>
<td style="text-align: left;">numOfRows</td>
<td style="text-align: left;">한 페이지 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td style="text-align: left;">pageNo</td>
<td style="text-align: left;">페이지 번호</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">페이지 번호</td>
</tr>
<tr>
<td style="text-align: left;">totalCount</td>
<td style="text-align: left;">전체 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">전체 결과 수</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNo</td>
<td style="text-align: left;">입찰공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">R25BK00930755</td>
<td style="text-align: left;"><p>입찰공고 관리번입찰공고 관리번호이며 조달청나라장터 공고건의 형식은 년도(4)+월(2)+순번(5)이며 자체전자조달시스템 보유기관은 각 기관별 형식 별도 사용</p>
<p>*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성</p>
<p>-단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</p></td>
</tr>
<tr>
<td style="text-align: left;">bidNtceOrd</td>
<td style="text-align: left;">입찰공고차수</td>
<td style="text-align: left;">3</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">000</td>
<td style="text-align: left;">입찰공고차수는 해당 입찰공고에 대한 재공고 및 재입찰 등이 발생되었을 경우 증가되는 수</td>
</tr>
<tr>
<td style="text-align: left;">reNtceYn</td>
<td style="text-align: left;">재공고여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">본 입찰공고의 재공고 여부(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">rgstTyNm</td>
<td style="text-align: left;">등록유형명</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">조달청 또는 나라장터 자체 공고건</td>
<td style="text-align: left;">입찰공고가 "조달청 또는 나라장터 자체 공고건","'나라장터 기타 공고건"</td>
</tr>
<tr>
<td style="text-align: left;">ntceKindNm</td>
<td style="text-align: left;">공고종류명</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">등록공고</td>
<td style="text-align: left;">공고의 공고상태명으로 등록공고, 변경공고, 취소공고, 재공고 구분</td>
</tr>
<tr>
<td style="text-align: left;">intrbidYn</td>
<td style="text-align: left;">국제입찰여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">국제입찰대상인지의 여부를 나타내며 국제입찰 대상은 내외국인 또는 외국인을 대상으로 하여 물품, 공사 및 용역을 조달하기 위하여 행하는 입찰을 말하며 수의계약을 포함한다. 국가계약법 제4조에 의해 추정가격이 고시금액(국제입찰 적용 대상 기준금액으로 기획재정부장관 및 행정자치부장관이 매 2년마다 고시한 금액을 말하며 WTO 또는 양자간(FTA) 정부조달협정에 따르면 국제입찰 대상 기준 금액이 SDR(Special Drawing Rights:특별인출권) 통화단위로 되어 있어 주무부 장관이 이를 2년마다 원화로 환산하여 고시) 이상일 경우 국제입찰대상이 됨(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceDt</td>
<td style="text-align: left;">입찰공고일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-01 09:17:24</td>
<td style="text-align: left;">입찰공고서를 공고한 일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">refNo</td>
<td style="text-align: left;">참조번호</td>
<td style="text-align: left;">105</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-44</td>
<td style="text-align: left;">조달청 입찰공고의 경우 참조공고번호는 자체 전자조달시스템에서 관리하는 공고번호를 의미하며 자체전자조달시스템의 경우 참조공고번호는 나라장터(G2B) 입찰공고번호를 의미함</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNm</td>
<td style="text-align: left;">입찰공고명</td>
<td style="text-align: left;">1000</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">2025년 인천글로벌캠퍼스 지원센터 변유량 냉수펌프 제어판넬 개선 공사 전자견적제출 안내공고</td>
<td style="text-align: left;">공사명 또는 사업명이라고도 하며 입찰공고 내용을 요약한 이름</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttCd</td>
<td style="text-align: left;">공고기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">Z023597</td>
<td style="text-align: left;">공고를 하는 기관의 코드로 행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드가 행자부코드가 없는 경우 조달청에서 부여한 공고기관 코드가 표기됨</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttNm</td>
<td style="text-align: left;">공고기관명</td>
<td style="text-align: left;">400400400400400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">인천글로벌캠퍼스운영 재단법인</td>
<td style="text-align: left;">수요기관의 의뢰를 받아 공고하는 기관의 명</td>
</tr>
<tr>
<td style="text-align: left;">dminsttCd</td>
<td style="text-align: left;">수요기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">Z023597</td>
<td style="text-align: left;">실제 수요기관의 코드로 행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드가 행자부코드가 없는 경우 조달청에서 부여한 수요기관 코드가 표기됨</td>
</tr>
<tr>
<td style="text-align: left;">dminsttNm</td>
<td style="text-align: left;">수요기관명</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">인천글로벌캠퍼스운영 재단법인</td>
<td style="text-align: left;">중앙조달인 경우 조달사업에 관한 법률 제2조(정의)에 따라 수요물자의 구매 공급 또는 시설공사 계약의 체결을 조달청장에게 요청할 수 있도록 조달청장이 인정하여 등록한 기관 또는 자체전자조달시스템을 이용하는 기관인 경우 계약을 의뢰한 기관의 명으로 공고기관과 수요기관이 동일할 수 있음</td>
</tr>
<tr>
<td style="text-align: left;">bidMethdNm</td>
<td style="text-align: left;">입찰방식명</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">전자입찰</td>
<td style="text-align: left;">공고의 입찰방식명 직찰<br />
전자입찰,전자입찰/직찰,전자/직찰/우편/상시,직찰/우편/상시,우편/상시,전자시담,복수견적(역경매),직찰/우편,전자시담(다자간)</td>
</tr>
<tr>
<td style="text-align: left;">cntrctCnclsMthdNm</td>
<td style="text-align: left;">계약체결방법명</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">수의계약</td>
<td style="text-align: left;">계약체결의 방법을 구분하는 명<br />
*일반경쟁계약은 계약 대상 물품의 규격 및 시방서와 계약조건 등을 널리 공고하여 일정한 자격을 가진 불특정 다수인의 입찰희망자를 모두 경쟁 입찰하는 계약방법<br />
*제한경쟁계약은 일반·지명경쟁계약제도의 단점을 보완하기 위해 실적제한, 기술보유제한, 특정물품제한, 지역제한 등을 두는 계약방법<br />
*지명경쟁계약은 계약상대자의 신용과 실적 등에 있어 적당하다고 인정하는 특정 다수의 경쟁 참가자를 지명하여 계약 상대방을 결정하는 계약방법<br />
*수의계약은 계약상대자를 결정함에 있어 경쟁방법에 의하지 않고 특정인을 선정하여 계약하는 계약방법</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttOfclNm</td>
<td style="text-align: left;">공고기관담당자명</td>
<td style="text-align: left;">35</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">김정호</td>
<td style="text-align: left;">공고기관의 공고를 담당하는 담당자의 명</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttOfclTelNo</td>
<td style="text-align: left;">공고기관담당자전화번호</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">031-000-1720</td>
<td style="text-align: left;">공고기관의 공고를 담당하는 담당자의 전화번호</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttOfclEmailAdrs</td>
<td style="text-align: left;">공고기관담당자이메일주소</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">jhkim@igc.or.kr</td>
<td style="text-align: left;">공고기관의 공고를 담당하는 담당자의 이메일주소</td>
</tr>
<tr>
<td style="text-align: left;">exctvNm</td>
<td style="text-align: left;">집행관명</td>
<td style="text-align: left;">35</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">김정호</td>
<td style="text-align: left;">공고의 집행관명</td>
</tr>
<tr>
<td style="text-align: left;">bidQlfctRgstDt</td>
<td style="text-align: left;">입찰참가자격등록마감일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-03 18:00</td>
<td style="text-align: left;">입찰참가등록이란 입찰사무를 효과적으로 집행하기 위하여 사전에 입찰참가자격등록을 해두었다가 필요 시 입찰에 참여하는 제도로 해당 공고에 대한 입찰참가자격의 등록이 완료되어야 하는 시점을 의미함 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">cmmnSpldmdAgrmntRcptdocMethd</td>
<td style="text-align: left;">공동수급협정서접수방식</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">없음</td>
<td style="text-align: left;">공동수급협정서의 접수방식"전자","수기","없음","공고서참고"</td>
</tr>
<tr>
<td style="text-align: left;">cmmnSpldmdAgrmntClseDt</td>
<td style="text-align: left;">공동수급협정마감일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-03 18:00</td>
<td style="text-align: left;">공동계약이 허용된 공고에 대해 공동수급체를 구성하여 입찰에 참여하고자 할 경우 구성원이 일정 분담내용에 따라 나누어 공동으로 이행하는 약속을 한 공동수급협정서를 작성하여야 하며 이때 공동수급협정서의 등록(작성) 마감 시점을 의미함”YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">cmmnSpldmdCorpRgnLmtYn</td>
<td style="text-align: left;">공동수급업체지역제한여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N/A</td>
<td style="text-align: left;">공동수급협정시 구성원의 지역제한을 적용할지 여부. 지역제한인경우 협정 구성업체가 참가제한지역에 포함되어야 함.(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">bidBeginDt</td>
<td style="text-align: left;">입찰개시일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-02 09:00:00</td>
<td style="text-align: left;">입찰서의 제출을 개시하는 일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">bidClseDt</td>
<td style="text-align: left;">입찰마감일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-02 09:00:00</td>
<td style="text-align: left;">입찰서의 제출을 마감하는 일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">opengDt</td>
<td style="text-align: left;">개찰일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-07 09:00:00</td>
<td style="text-align: left;">집행관이 개찰을 수행할 수 있는 시작일시이며<br />
개찰일시 이후에 개찰이 가능함<br />
실제 개찰을 수행한 시간을 의미하지 않음 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl1</td>
<td style="text-align: left;">공고규격서URL1</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00930755&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=3&amp;prcmBsneSeCd=07</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl2</td>
<td style="text-align: left;">공고규격서URL2</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00930755&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=5&amp;prcmBsneSeCd=07</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl3</td>
<td style="text-align: left;">공고규격서URL3</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00930755&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=6&amp;prcmBsneSeCd=07</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl4</td>
<td style="text-align: left;">공고규격서URL4</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00930755&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=7&amp;prcmBsneSeCd=07</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl5</td>
<td style="text-align: left;">공고규격서URL5</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00930755&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=8&amp;prcmBsneSeCd=07</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl6</td>
<td style="text-align: left;">공고규격서URL6</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00930755&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=9&amp;prcmBsneSeCd=07</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl7</td>
<td style="text-align: left;">공고규격서URL7</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00930755&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=10&amp;prcmBsneSeCd=07</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl8</td>
<td style="text-align: left;">공고규격서URL8</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00930755&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=11&amp;prcmBsneSeCd=07</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl9</td>
<td style="text-align: left;">공고규격서URL9</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00930755&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=12&amp;prcmBsneSeCd=07</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl10</td>
<td style="text-align: left;">공고규격서URL10</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00930755&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=13&amp;prcmBsneSeCd=07</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm1</td>
<td style="text-align: left;">공고규격파일명1</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">시방서.pdf</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm2</td>
<td style="text-align: left;">공고규격파일명2</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">의견서.pdf</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm3</td>
<td style="text-align: left;">공고규격파일명3</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">안전보건관리서약서.hwpx</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm4</td>
<td style="text-align: left;">공고규격파일명4</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">수급업체 안전보건수준평가 세부기준.hwpx</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm5</td>
<td style="text-align: left;">공고규격파일명5</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">안전보건관리계획서.hwpx</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm6</td>
<td style="text-align: left;">공고규격파일명6</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">공내역서.xlsx</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm7</td>
<td style="text-align: left;">공고규격파일명7</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">공고문_최종본.pdf</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm8</td>
<td style="text-align: left;">공고규격파일명8</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">공고문_최종본.pdf</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm9</td>
<td style="text-align: left;">공고규격파일명9</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">공고문_최종본.pdf</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm10</td>
<td style="text-align: left;">공고규격파일명10</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">공고문_최종본.pdf</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">rbidPermsnYn</td>
<td style="text-align: left;">재입찰허용여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">입찰이 유찰되는 경우 재공고 없이 다시 입찰(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">pqApplDocRcptMthdNm</td>
<td style="text-align: left;">PQ신청서접수방법명</td>
<td style="text-align: left;">30</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">없음</td>
<td style="text-align: left;">PQ대상공고에서 PQ심사신청서를 어떻게 받을지에 대한 코드명</td>
</tr>
<tr>
<td style="text-align: left;">pqApplDocRcptDt</td>
<td style="text-align: left;">PQ신청서접수일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-03 18:00</td>
<td style="text-align: left;">PQ심사신청서 접수 마감일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">arsltApplDocRcptMthdNm</td>
<td style="text-align: left;">실적신청서접수방법명</td>
<td style="text-align: left;">50</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">없음</td>
<td style="text-align: left;">공고의 실적신청서접수방법명</td>
</tr>
<tr>
<td style="text-align: left;">arsltApplDocRcptDt</td>
<td style="text-align: left;">실적신청서접수일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-03 18:00</td>
<td style="text-align: left;">실적심사신청서 접수마감일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">jntcontrctDutyRgnNm1</td>
<td style="text-align: left;">공동도급의무지역명1</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">서울특별시</td>
<td style="text-align: left;">공고의 공동도급의무지역명</td>
</tr>
<tr>
<td style="text-align: left;">jntcontrctDutyRgnNm2</td>
<td style="text-align: left;">공동도급의무지역명2</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">서울특별시</td>
<td style="text-align: left;">공고의 공동도급의무지역명</td>
</tr>
<tr>
<td style="text-align: left;">jntcontrctDutyRgnNm3</td>
<td style="text-align: left;">공동도급의무지역명3</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">서울특별시</td>
<td style="text-align: left;">공고의 공동도급의무지역명</td>
</tr>
<tr>
<td style="text-align: left;">rgnDutyJntcontrctRt</td>
<td style="text-align: left;">지역의무공동도급비율</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">지역의무공동동급시 3개지역의 공동도급합산 하한 비율(%)</td>
</tr>
<tr>
<td style="text-align: left;">dtlsBidYn</td>
<td style="text-align: left;">내역입찰여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">내역입찰인지는 나타내는 항목으로 내역입찰일 경우 투찰시 내역서를 첨부해야함(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">bidPrtcptLmtYn</td>
<td style="text-align: left;">입찰참가제한여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">공고의 입찰참가제한여부(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">prearngPrceDcsnMthdNm</td>
<td style="text-align: left;">예정가격결정방법명</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">복수예가</td>
<td style="text-align: left;">예정가격의 결정을 위해 복수예정가격방식으로 산정하는지 단일 예정가격으로 산정하는지를 구분하는 명</td>
</tr>
<tr>
<td style="text-align: left;">totPrdprcNum</td>
<td style="text-align: left;">총예가건수</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">15</td>
<td style="text-align: left;">공고의 총예가건수</td>
</tr>
<tr>
<td style="text-align: left;">drwtPrdprcNum</td>
<td style="text-align: left;">추첨예가건수</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">공고의 추첨예가건수</td>
</tr>
<tr>
<td style="text-align: left;">bdgtAmt</td>
<td style="text-align: left;">예산금액</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">198710000</td>
<td style="text-align: left;">공고의 예산금액(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">presmptPrce</td>
<td style="text-align: left;">추정가격</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">180645455</td>
<td style="text-align: left;">물품/공사/용역 등의 조달 계약을 체결함에 있어 국제입찰 대상여부를 판단하는 기준 등으로 삼기 위하여 예정가격이 결정되기 전에 예산에 계상된 금액 등을 기준으로 하여 부가가치세 및 조달 수수료를 제외한 금액(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">govsplyAmt</td>
<td style="text-align: left;">관급금액</td>
<td style="text-align: left;">21</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">공고의 관급금액(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">aplBssCntnts</td>
<td style="text-align: left;">적용기준내용</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">행자부</td>
<td style="text-align: left;">공고의 적용기준내용</td>
</tr>
<tr>
<td style="text-align: left;">indstrytyEvlRt</td>
<td style="text-align: left;">업종평가비율</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">적격심사에서 사용하는 업종평가비율(%)</td>
</tr>
<tr>
<td style="text-align: left;">mainCnsttyNm</td>
<td style="text-align: left;">주공종명</td>
<td style="text-align: left;">300</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">토목공사업</td>
<td style="text-align: left;">공고의 주공종명</td>
</tr>
<tr>
<td style="text-align: left;">mainCnsttyCnstwkPrearngAmt</td>
<td style="text-align: left;">주공종공사예정금액</td>
<td style="text-align: left;">21</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">18064540</td>
<td style="text-align: left;">적격심사시 주공종추정금액(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">incntvRgnNm1</td>
<td style="text-align: left;">가산지역명1</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">경상남도</td>
<td style="text-align: left;">적격심사를 실시할 경우 해당 지역 업체의 경우 가산점을 얻을 수 있는 지역명</td>
</tr>
<tr>
<td style="text-align: left;">incntvRgnNm2</td>
<td style="text-align: left;">가산지역명2</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">경기도</td>
<td style="text-align: left;">적격심사를 실시할 경우 해당 지역 업체의 경우 가산점을 얻을 수 있는 지역명</td>
</tr>
<tr>
<td style="text-align: left;">incntvRgnNm3</td>
<td style="text-align: left;">가산지역명3</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">서울특별시</td>
<td style="text-align: left;">적격심사를 실시할 경우 해당 지역 업체의 경우 가산점을 얻을 수 있는 지역명</td>
</tr>
<tr>
<td style="text-align: left;">incntvRgnNm4</td>
<td style="text-align: left;">가산지역명4</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">서울특별시</td>
<td style="text-align: left;">적격심사를 실시할 경우 해당 지역 업체의 경우 가산점을 얻을 수 있는 지역명</td>
</tr>
<tr>
<td style="text-align: left;">opengPlce</td>
<td style="text-align: left;">개찰장소</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">국가종합전자조달시스템(나라장터)</td>
<td style="text-align: left;">집행관이 개찰을 하는 장소</td>
</tr>
<tr>
<td style="text-align: left;">dcmtgOprtnDt</td>
<td style="text-align: left;">설명회실시일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-03 18:00</td>
<td style="text-align: left;">해당 공고에 대한 현장/입찰/과업 설명회를 실시하는 일시”YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">dcmtgOprtnPlce</td>
<td style="text-align: left;">설명회실시장소</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">우리청 관리과</td>
<td style="text-align: left;">해당 공고에 대한 설명회를 실시하는 경우 현장/입찰/과업 설명회를 실시하는 장소</td>
</tr>
<tr>
<td style="text-align: left;">contrctrcnstrtnGovsplyMtrlAmt</td>
<td style="text-align: left;">도급자설치관급자재금액</td>
<td style="text-align: left;">21</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">공고의 도급자설치관급자재금액(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">govcnstrtnGovsplyMtrlAmt</td>
<td style="text-align: left;">관급자설치관급자재금액</td>
<td style="text-align: left;">21</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">공고의 관급자설치관급자재금액(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceDtlUrl</td>
<td style="text-align: left;">입찰공고상세URL</td>
<td style="text-align: left;">512</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/link/PNPE027_01/single/?bidPbancNo=R25BK00930755&amp;bidPbancOrd=000</td>
<td style="text-align: left;">나라장터시스템의 입찰공고 상세화면 링크</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceUrl</td>
<td style="text-align: left;">입찰공고URL</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/link/PNPE027_01/single/?bidPbancNo=R25BK00930755&amp;bidPbancOrd=000</td>
<td style="text-align: left;">해당 입찰공고를 인터넷상에서 확인할 수 있는 URL주소</td>
</tr>
<tr>
<td style="text-align: left;">bidPrtcptFeePaymntYn</td>
<td style="text-align: left;">입찰참가수수료납부여부</td>
<td style="text-align: left;">30</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">전자납부</td>
<td style="text-align: left;">입찰참가 의사가 있는 자가 납부하여야하는 수수료의 유무 및 납부방법을 표기하는 것으로 "전자납부, 수기 및 전자납부, 수기, 없음"으로 표기</td>
</tr>
<tr>
<td style="text-align: left;">bidPrtcptFee</td>
<td style="text-align: left;">입찰참가수수료</td>
<td style="text-align: left;">21</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">입찰에 참가하기위해 납부하는 수수료(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">bidGrntymnyPaymntYn</td>
<td style="text-align: left;">입찰보증금납부여부</td>
<td style="text-align: left;">30</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">불허</td>
<td style="text-align: left;">입찰보증금을 나라장터에서 전자로 납부가능하게 할지 여부 “전자납부허용”,”불허’으로 표기</td>
</tr>
<tr>
<td style="text-align: left;">crdtrNm</td>
<td style="text-align: left;">채권자명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">인천글로벌캠퍼스운영재단법인대표이사</td>
<td style="text-align: left;">입찰보증금 항목의 "보증채권자명"으로 전자입찰보증 접수시 사용</td>
</tr>
<tr>
<td style="text-align: left;">cmmnSpldmdCnum</td>
<td style="text-align: left;">공동수급업체수</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">공고서에 의함</td>
<td style="text-align: left;">공고의 공동수급업체수</td>
</tr>
<tr>
<td style="text-align: left;">untyNtceNo</td>
<td style="text-align: left;">통합공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25BM00300511</td>
<td style="text-align: left;">입찰공고를 구분하는 번호로 입찰공고번호이며 형식은 년도(4)+월(2)+순번(5)<br />
*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성<br />
- 단계구분: BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격), BK(통합입찰)</td>
</tr>
<tr>
<td style="text-align: left;">sptDscrptDocUrl1</td>
<td style="text-align: left;">현장설명서URL1</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo= R25BK00930755&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=11&amp;prcmBsneSeCd=07</td>
<td style="text-align: left;">공고의 현장설명서URL</td>
</tr>
<tr>
<td style="text-align: left;">sptDscrptDocUrl2</td>
<td style="text-align: left;">현장설명서URL2</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo= R25BK00930755&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=12&amp;prcmBsneSeCd=07</td>
<td style="text-align: left;">공고의 현장설명서URL</td>
</tr>
<tr>
<td style="text-align: left;">sptDscrptDocUrl3</td>
<td style="text-align: left;">현장설명서URL3</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo= R25BK00930755&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=13&amp;prcmBsneSeCd=07</td>
<td style="text-align: left;">공고의 현장설명서URL</td>
</tr>
<tr>
<td style="text-align: left;">sptDscrptDocUrl4</td>
<td style="text-align: left;">현장설명서URL4</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo= R25BK00930755&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=14&amp;prcmBsneSeCd=07</td>
<td style="text-align: left;">공고의 현장설명서URL</td>
</tr>
<tr>
<td style="text-align: left;">sptDscrptDocUrl5</td>
<td style="text-align: left;">현장설명서URL5</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo= R25BK00930755&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=15&amp;prcmBsneSeCd=07</td>
<td style="text-align: left;">공고의 현장설명서URL</td>
</tr>
<tr>
<td style="text-align: left;">subsiCnsttyNm1</td>
<td style="text-align: left;">부대공종명1</td>
<td style="text-align: left;">300</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">토목공사업</td>
<td style="text-align: left;">공고의 부대공종명</td>
</tr>
<tr>
<td style="text-align: left;">subsiCnsttyNm2</td>
<td style="text-align: left;">부대공종명2</td>
<td style="text-align: left;">300</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">건축공사업</td>
<td style="text-align: left;">공고의 부대공종명</td>
</tr>
<tr>
<td style="text-align: left;">subsiCnsttyNm3</td>
<td style="text-align: left;">부대공종명3</td>
<td style="text-align: left;">300</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">기계설비공사업</td>
<td style="text-align: left;">공고의 부대공종명</td>
</tr>
<tr>
<td style="text-align: left;">subsiCnsttyNm4</td>
<td style="text-align: left;">부대공종명4</td>
<td style="text-align: left;">300</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">상.하수도설비공사업</td>
<td style="text-align: left;">공고의 부대공종명</td>
</tr>
<tr>
<td style="text-align: left;">subsiCnsttyNm5</td>
<td style="text-align: left;">부대공종명5</td>
<td style="text-align: left;">300</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">조경식재공사업</td>
<td style="text-align: left;">공고의 부대공종명</td>
</tr>
<tr>
<td style="text-align: left;">subsiCnsttyNm6</td>
<td style="text-align: left;">부대공종명6</td>
<td style="text-align: left;">300</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">시설물유지관리업</td>
<td style="text-align: left;">공고의 부대공종명</td>
</tr>
<tr>
<td style="text-align: left;">subsiCnsttyNm7</td>
<td style="text-align: left;">부대공종명7</td>
<td style="text-align: left;">300</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">일반소방시설공사업(기계)</td>
<td style="text-align: left;">공고의 부대공종명</td>
</tr>
<tr>
<td style="text-align: left;">subsiCnsttyNm8</td>
<td style="text-align: left;">부대공종명8</td>
<td style="text-align: left;">300</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">일반소방시설공사업(전기)</td>
<td style="text-align: left;">공고의 부대공종명</td>
</tr>
<tr>
<td style="text-align: left;">subsiCnsttyNm9</td>
<td style="text-align: left;">부대공종명9</td>
<td style="text-align: left;">300</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">산업.환경설비공사업</td>
<td style="text-align: left;">공고의 부대공종명</td>
</tr>
<tr>
<td style="text-align: left;">subsiCnsttyIndstrytyEvlRt1</td>
<td style="text-align: left;">부공종업종평가비율1</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">33</td>
<td style="text-align: left;">공고의 부공종업종평가비율(%)</td>
</tr>
<tr>
<td style="text-align: left;">subsiCnsttyIndstrytyEvlRt2</td>
<td style="text-align: left;">부공종업종평가비율2</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">37.51</td>
<td style="text-align: left;">공고의 부공종업종평가비율(%)</td>
</tr>
<tr>
<td style="text-align: left;">subsiCnsttyIndstrytyEvlRt3</td>
<td style="text-align: left;">부공종업종평가비율3</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">32.75</td>
<td style="text-align: left;">공고의 부공종업종평가비율(%)</td>
</tr>
<tr>
<td style="text-align: left;">subsiCnsttyIndstrytyEvlRt4</td>
<td style="text-align: left;">부공종업종평가비율4</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">39.7</td>
<td style="text-align: left;">공고의 부공종업종평가비율(%)</td>
</tr>
<tr>
<td style="text-align: left;">subsiCnsttyIndstrytyEvlRt5</td>
<td style="text-align: left;">부공종업종평가비율5</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">30</td>
<td style="text-align: left;">공고의 부공종업종평가비율(%)</td>
</tr>
<tr>
<td style="text-align: left;">subsiCnsttyIndstrytyEvlRt6</td>
<td style="text-align: left;">부공종업종평가비율6</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">24.94</td>
<td style="text-align: left;">공고의 부공종업종평가비율(%)</td>
</tr>
<tr>
<td style="text-align: left;">subsiCnsttyIndstrytyEvlRt7</td>
<td style="text-align: left;">부공종업종평가비율7</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">33</td>
<td style="text-align: left;">공고의 부공종업종평가비율(%)</td>
</tr>
<tr>
<td style="text-align: left;">subsiCnsttyIndstrytyEvlRt8</td>
<td style="text-align: left;">부공종업종평가비율8</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">27</td>
<td style="text-align: left;">공고의 부공종업종평가비율(%)</td>
</tr>
<tr>
<td style="text-align: left;">subsiCnsttyIndstrytyEvlRt9</td>
<td style="text-align: left;">부공종업종평가비율9</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">32</td>
<td style="text-align: left;">공고의 부공종업종평가비율(%)</td>
</tr>
<tr>
<td style="text-align: left;">cmmnSpldmdMethdCd</td>
<td style="text-align: left;">공동수급방식코드</td>
<td style="text-align: left;">15</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">공500012</td>
<td style="text-align: left;">공동수급이라 함은 구성원을 2인 이상으로 하여 수급인이 해당계약을 공동으로 수행하기 위하여 잠정적으로 결성한 실체를 의미하며 공동수급체가도급을 받아 이행하는 방식을 구분하는 코드로<br />
공500001 : 공동이행<br />
공500002 : 분담이행<br />
공500003 : 주계약자관리방식<br />
공500004 : 단독계약<br />
공500005 : 혼합방식<br />
공500006 : 공동이행 또는 분담이행<br />
공500007 : 혼합_단독<br />
공500008 : 혼합_공동<br />
공500012 : 해당없음으로 구분됨</td>
</tr>
<tr>
<td style="text-align: left;">cmmnSpldmdMethdNm</td>
<td style="text-align: left;">공동수급방식명</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">(없음)공동수급불허</td>
<td style="text-align: left;">공동수급이라 함은 구성원을 2인 이상으로 하여 수급인이 해당계약을 공동으로 수행하기 위하여 잠정적으로 결성한 실체를 의미하며 공동수급체가도급을 받아 이행하는 방식을 구분하는 명임</td>
</tr>
<tr>
<td style="text-align: left;">stdNtceDocUrl</td>
<td style="text-align: left;">표준공고서URL</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00930755&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=10&amp;prcmBsneSeCd=07</td>
<td style="text-align: left;">공고의 표준공고문URL</td>
</tr>
<tr>
<td style="text-align: left;">brffcBidprcPermsnYn</td>
<td style="text-align: left;">지사투찰허용여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">지역제한 공고에 한해서 지사 투찰을 허용할지 여부. 투찰제어시 사용(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">cnsttyAccotShreRateList</td>
<td style="text-align: left;">공종별지분율목록</td>
<td style="text-align: left;">4000</td>
<td style="text-align: left;">0..n</td>
<td style="text-align: left;">[전기공사업^100],</td>
<td style="text-align: left;">공고의 공종별지분율 목록<br />
[부업종코드명^부업종평가비율(%)],[부업종코드명^부업종평가비율(%)]</td>
</tr>
<tr>
<td style="text-align: left;">cnstrtnAbltyEvlAmtList</td>
<td style="text-align: left;">시공능력평가금액목록</td>
<td style="text-align: left;">4000</td>
<td style="text-align: left;">0..n</td>
<td style="text-align: left;">[1^토목공사업^0001^7400000000],</td>
<td style="text-align: left;">공고의 시공능력평가금액목록 [제한그룹번호^면허지역통합코드명^면허지역통합코드^시공능력평가금액],[제한그룹번호^면허지역통합코드명^면허지역통합코드^시공능력평가금액]</td>
</tr>
<tr>
<td style="text-align: left;">dsgntCmptYn</td>
<td style="text-align: left;">지명경쟁여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">공고의 지명경쟁여부(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">arsltCmptYn</td>
<td style="text-align: left;">실적경쟁여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">공고의 실적경쟁여부(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">pqEvalYn</td>
<td style="text-align: left;">PQ심사여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">공고의 PQ심사여부(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">ntceDscrptYn</td>
<td style="text-align: left;">공고설명여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">공고의 공고설명여부(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">rsrvtnPrceReMkngMthdNm</td>
<td style="text-align: left;">예비가격재작성방법명</td>
<td style="text-align: left;">50</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">재입찰시 기존 예비가격을 사용하여 예정가격이 산정됩니다.</td>
<td style="text-align: left;">공고의 예비가격재작성방법명</td>
</tr>
<tr>
<td style="text-align: left;">mainCnsttyPresmptPrce</td>
<td style="text-align: left;">주공종추정가격</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">5000</td>
<td style="text-align: left;">주공종에 대한 추정가격(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">orderPlanUntyNo</td>
<td style="text-align: left;">발주계획통합번호</td>
<td style="text-align: left;">35</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25DD20311262</td>
<td style="text-align: left;">*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성<br />
- 단계구분: BK(입찰)<br />
TA(계약)<br />
DD:(발주계획)<br />
BD(사전규격),<br />
BK(통합입찰)</td>
</tr>
<tr>
<td style="text-align: left;">sucsfbidLwltRate</td>
<td style="text-align: left;">낙찰하한율</td>
<td style="text-align: left;">22</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">86.745</td>
<td style="text-align: left;">개찰시 사용하는 낙찰하한율(%)</td>
</tr>
<tr>
<td style="text-align: left;">rgstDt</td>
<td style="text-align: left;">등록일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">2025-07-01 09:17:24</td>
<td style="text-align: left;">공고의 등록일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">bfSpecRgstNo</td>
<td style="text-align: left;">사전규격등록번호</td>
<td style="text-align: left;">17</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25BD20311262</td>
<td style="text-align: left;"><p>*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성</p>
<p>- 단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</p></td>
</tr>
<tr>
<td style="text-align: left;">sucsfbidMthdCd</td>
<td style="text-align: left;">낙찰방법코드</td>
<td style="text-align: left;">9</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">낙030021</td>
<td style="text-align: left;">낙찰방법명에 대한 코드 (한글 1자리 + 숫자 6자리)</td>
</tr>
<tr>
<td style="text-align: left;">sucsfbidMthdNm</td>
<td style="text-align: left;">낙찰방법명</td>
<td style="text-align: left;">700</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">소액수의견적(2인 이상 견적 제출)-국민연금보험료 등 합산액 감액 적용</td>
<td style="text-align: left;">낙찰자를 결정하는 방법-낙찰방법 세부기준</td>
</tr>
<tr>
<td style="text-align: left;">chgDt</td>
<td style="text-align: left;">변경일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-01 09:17:24</td>
<td style="text-align: left;">공고의 변경일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">dminsttOfclEmailAdrs</td>
<td style="text-align: left;">수요기관담당자이메일주소</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">nskk22@kywa.or.kr</td>
<td style="text-align: left;">수요기관 담당자의 이메일주소</td>
</tr>
<tr>
<td style="text-align: left;">indstrytyLmtYn</td>
<td style="text-align: left;">업종제한여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">Y</td>
<td style="text-align: left;">해당 공고 입찰 시 업종(면허)제한을 두는지의 여부<br />
예시)Y</td>
</tr>
<tr>
<td style="text-align: left;">cnstrtsiteRgnNm</td>
<td style="text-align: left;">공사현장지역명</td>
<td style="text-align: left;">256</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">인천광역시 연수구</td>
<td style="text-align: left;"><p>공사현장의 지역명</p>
<p>나라장터 화면에서 “공사현장”</p></td>
</tr>
<tr>
<td style="text-align: left;">rgnDutyJntcontrctYn</td>
<td style="text-align: left;">지역의무공동도급여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">지역업체 참여가 일정 지분율 이상일 경우에만 입창이 가능한 공고 여부 ( Y:해당 N:공고서에의함)</td>
</tr>
<tr>
<td style="text-align: left;">chgNtceRsn</td>
<td style="text-align: left;">변경공고사유</td>
<td style="text-align: left;">4000</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">지역제한(강원도)으로 변경</td>
<td style="text-align: left;">공고종류명(공고의 공고상태명) 이 변경일 경우 변경공고사유 , 취소일 경우 취소공고사유</td>
</tr>
<tr>
<td style="text-align: left;">rbidOpengDt</td>
<td style="text-align: left;">재입찰개찰일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-07 09:00:00</td>
<td style="text-align: left;">공고종류명이 ‘재입찰’ 일 경우 재입찰공고의 개찰을 수행할 수 있는 시작일시<br />
“YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">ciblAplYn</td>
<td style="text-align: left;">건설산업법적용대상여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">Y</td>
<td style="text-align: left;">건설산업기본법 적용 대상인지에 대한 여부</td>
</tr>
<tr>
<td style="text-align: left;">mtltyAdvcPsblYn</td>
<td style="text-align: left;">상호시장진출허용여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">건설업역(종합공사,전문공사)에 상호 진출 가능한지에 대한 여부</td>
</tr>
<tr>
<td style="text-align: left;">mtltyAdvcPsblYnCnstwkNm</td>
<td style="text-align: left;">건설산업법적용대상공사명</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">전문공사-유지보수공사</td>
<td style="text-align: left;">건설산업법 적용대상 공사명</td>
</tr>
<tr>
<td style="text-align: left;">VAT</td>
<td style="text-align: left;">부가가치세</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">18064545</td>
<td style="text-align: left;">부가가치세</td>
</tr>
<tr>
<td style="text-align: left;">indutyVAT</td>
<td style="text-align: left;">주공종부가가치세</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">주공종부가가치세</td>
</tr>
<tr>
<td style="text-align: left;">indstrytyMfrcFldEvlYn</td>
<td style="text-align: left;">주력분야평가여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">업종 주력분야 평가 대상 여부</td>
</tr>
<tr>
<td style="text-align: left;">bidWgrnteeRcptClseDt</td>
<td style="text-align: left;">입찰보증서접수마감일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-09-18 10:00:00</td>
<td style="text-align: left;">입찰보증서접수마감일시</td>
</tr>
<tr>
<td style="text-align: left;">rgnLmtBidLocplcJdgmBssCd</td>
<td style="text-align: left;">지역제한입찰소재지판단기준코드</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">지역제한입찰소재지판단기준코드</td>
</tr>
<tr>
<td style="text-align: left;">rgnLmtBidLocplcJdgmBssNm</td>
<td style="text-align: left;">지역제한입찰소재지판단기준명</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">본사또는참여지사소재지</td>
<td style="text-align: left;">지역제한입찰소재지판단기준명</td>
</tr>
<tr>
<td style="text-align: left;">sucsfbidMthdAppStd</td>
<td style="text-align: left;">낙찰방법적용기준</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">조달청 시설공사 적격심사세부기준</td>
<td style="text-align: left;"><p>낙찰자를 결정하</p>
<p>방법 적용기준</p></td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 요청 / 응답 메시지 예제

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr>
<td style="text-align: center;"><strong>REST(URI)</strong></td>
</tr>
<tr>
<td style="text-align: center;">http://apis.data.go.kr/1230000/ad/BidPublicInfoService/getBidPblancListInfoCnstwkPPSSrch?type=xml&amp;inqryDiv=1&amp;inqryBgnDt=202507010000&amp;inqryEndDt=202507012359&amp;numOfRows=10&amp;pageNo=1&amp;bidNtceNm=2025년 인천글로벌캠퍼스 지원센터 변유량 냉수펌프 제어판넬 개선 공사 전자견적제출 안내공고&amp;ServiceKey=인증키</td>
</tr>
<tr>
<td style="text-align: center;"><strong>응답 메시지</strong></td>
</tr>
<tr>
<td style="text-align: left;"><p>&lt;response&gt;</p>
<p>&lt;header&gt;</p>
<p>&lt;resultCode&gt;00&lt;/resultCode&gt;</p>
<p>&lt;resultMsg&gt;정상&lt;/resultMsg&gt;</p>
<p>&lt;/header&gt;</p>
<p>&lt;body&gt;</p>
<p>&lt;items&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00930755&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;reNtceYn&gt;N&lt;/reNtceYn&gt;</p>
<p>&lt;rgstTyNm&gt;조달청 또는 나라장터 자체 공고건&lt;/rgstTyNm&gt;</p>
<p>&lt;ntceKindNm&gt;등록공고&lt;/ntceKindNm&gt;</p>
<p>&lt;intrbidYn&gt;N&lt;/intrbidYn&gt;</p>
<p>&lt;bidNtceDt&gt;2025-07-01 09:17:24&lt;/bidNtceDt&gt;</p>
<p>&lt;refNo&gt;2025-44&lt;/refNo&gt;</p>
<p>&lt;bidNtceNm&gt;2025년 인천글로벌캠퍼스 지원센터 변유량 냉수펌프 제어판넬 개선 공사 전자견적제출 안내공고&lt;/bidNtceNm&gt;</p>
<p>&lt;ntceInsttCd&gt;Z023597&lt;/ntceInsttCd&gt;</p>
<p>&lt;ntceInsttNm&gt;인천글로벌캠퍼스운영 재단법인&lt;/ntceInsttNm&gt;</p>
<p>&lt;dminsttCd&gt;Z023597&lt;/dminsttCd&gt;</p>
<p>&lt;dminsttNm&gt;인천글로벌캠퍼스운영 재단법인&lt;/dminsttNm&gt;</p>
<p>&lt;bidMethdNm&gt;전자입찰&lt;/bidMethdNm&gt;</p>
<p>&lt;cntrctCnclsMthdNm&gt;수의계약&lt;/cntrctCnclsMthdNm&gt;</p>
<p>&lt;ntceInsttOfclNm&gt;김정호&lt;/ntceInsttOfclNm&gt;</p>
<p>&lt;ntceInsttOfclTelNo&gt;&lt;/ntceInsttOfclTelNo&gt;</p>
<p>&lt;ntceInsttOfclEmailAdrs&gt;jhkim@igc.or.kr&lt;/ntceInsttOfclEmailAdrs&gt;</p>
<p>&lt;exctvNm&gt;김정호&lt;/exctvNm&gt;</p>
<p>&lt;bidQlfctRgstDt&gt;2025-07-03 18:00&lt;/bidQlfctRgstDt&gt;</p>
<p>&lt;cmmnSpldmdAgrmntRcptdocMethd&gt;없음&lt;/cmmnSpldmdAgrmntRcptdocMethd&gt;</p>
<p>&lt;cmmnSpldmdAgrmntClseDt&gt;&lt;/cmmnSpldmdAgrmntClseDt&gt;</p>
<p>&lt;cmmnSpldmdCorpRgnLmtYn&gt;&lt;/cmmnSpldmdCorpRgnLmtYn&gt;</p>
<p>&lt;bidBeginDt&gt;2025-07-02 09:00:00&lt;/bidBeginDt&gt;</p>
<p>&lt;bidClseDt&gt;2025-07-04 17:00:00&lt;/bidClseDt&gt;</p>
<p>&lt;opengDt&gt;2025-07-07 09:00:00&lt;/opengDt&gt;</p>
<p>&lt;ntceSpecDocUrl1&gt;https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00930755&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=3&lt;/ntceSpecDocUrl1&gt;</p>
<p>&lt;ntceSpecDocUrl2&gt;https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00930755&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=5&lt;/ntceSpecDocUrl2&gt;</p>
<p>&lt;ntceSpecDocUrl3&gt;https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00930755&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=6&lt;/ntceSpecDocUrl3&gt;</p>
<p>&lt;ntceSpecDocUrl4&gt;https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00930755&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=7&lt;/ntceSpecDocUrl4&gt;</p>
<p>&lt;ntceSpecDocUrl5&gt;https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00930755&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=8&lt;/ntceSpecDocUrl5&gt;</p>
<p>&lt;ntceSpecDocUrl6&gt;https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00930755&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=9&lt;/ntceSpecDocUrl6&gt;</p>
<p>&lt;ntceSpecDocUrl7&gt;https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00930755&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=10&lt;/ntceSpecDocUrl7&gt;</p>
<p>&lt;ntceSpecDocUrl8&gt;&lt;/ntceSpecDocUrl8&gt;</p>
<p>&lt;ntceSpecDocUrl9&gt;&lt;/ntceSpecDocUrl9&gt;</p>
<p>&lt;ntceSpecDocUrl10&gt;&lt;/ntceSpecDocUrl10&gt;</p>
<p>&lt;ntceSpecFileNm1&gt;시방서.pdf&lt;/ntceSpecFileNm1&gt;</p>
<p>&lt;ntceSpecFileNm2&gt;의견서.pdf&lt;/ntceSpecFileNm2&gt;</p>
<p>&lt;ntceSpecFileNm3&gt;안전보건관리서약서.hwpx&lt;/ntceSpecFileNm3&gt;</p>
<p>&lt;ntceSpecFileNm4&gt;수급업체 안전보건수준평가 세부기준.hwpx&lt;/ntceSpecFileNm4&gt;</p>
<p>&lt;ntceSpecFileNm5&gt;안전보건관리계획서.hwpx&lt;/ntceSpecFileNm5&gt;</p>
<p>&lt;ntceSpecFileNm6&gt;공내역서.xlsx&lt;/ntceSpecFileNm6&gt;</p>
<p>&lt;ntceSpecFileNm7&gt;공고문_최종본.pdf&lt;/ntceSpecFileNm7&gt;</p>
<p>&lt;ntceSpecFileNm8&gt;&lt;/ntceSpecFileNm8&gt;</p>
<p>&lt;ntceSpecFileNm9&gt;&lt;/ntceSpecFileNm9&gt;</p>
<p>&lt;ntceSpecFileNm10&gt;&lt;/ntceSpecFileNm10&gt;</p>
<p>&lt;rbidPermsnYn&gt;N&lt;/rbidPermsnYn&gt;</p>
<p>&lt;pqApplDocRcptMthdNm&gt;&lt;/pqApplDocRcptMthdNm&gt;</p>
<p>&lt;pqApplDocRcptDt&gt;&lt;/pqApplDocRcptDt&gt;</p>
<p>&lt;arsltApplDocRcptMthdNm&gt;&lt;/arsltApplDocRcptMthdNm&gt;</p>
<p>&lt;arsltApplDocRcptDt&gt;&lt;/arsltApplDocRcptDt&gt;</p>
<p>&lt;jntcontrctDutyRgnNm1&gt;&lt;/jntcontrctDutyRgnNm1&gt;</p>
<p>&lt;jntcontrctDutyRgnNm2&gt;&lt;/jntcontrctDutyRgnNm2&gt;</p>
<p>&lt;jntcontrctDutyRgnNm3&gt;&lt;/jntcontrctDutyRgnNm3&gt;</p>
<p>&lt;rgnDutyJntcontrctRt&gt;&lt;/rgnDutyJntcontrctRt&gt;</p>
<p>&lt;dtlsBidYn&gt;N&lt;/dtlsBidYn&gt;</p>
<p>&lt;bidPrtcptLmtYn&gt;N&lt;/bidPrtcptLmtYn&gt;</p>
<p>&lt;prearngPrceDcsnMthdNm&gt;복수예가&lt;/prearngPrceDcsnMthdNm&gt;</p>
<p>&lt;totPrdprcNum&gt;15&lt;/totPrdprcNum&gt;</p>
<p>&lt;drwtPrdprcNum&gt;4&lt;/drwtPrdprcNum&gt;</p>
<p>&lt;bdgtAmt&gt;198710000&lt;/bdgtAmt&gt;</p>
<p>&lt;presmptPrce&gt;180645455&lt;/presmptPrce&gt;</p>
<p>&lt;govsplyAmt&gt;0&lt;/govsplyAmt&gt;</p>
<p>&lt;aplBssCntnts&gt;행자부&lt;/aplBssCntnts&gt;</p>
<p>&lt;indstrytyEvlRt&gt;&lt;/indstrytyEvlRt&gt;</p>
<p>&lt;mainCnsttyNm&gt;&lt;/mainCnsttyNm&gt;</p>
<p>&lt;mainCnsttyCnstwkPrearngAmt&gt;&lt;/mainCnsttyCnstwkPrearngAmt&gt;</p>
<p>&lt;incntvRgnNm1&gt;&lt;/incntvRgnNm1&gt;</p>
<p>&lt;incntvRgnNm2&gt;&lt;/incntvRgnNm2&gt;</p>
<p>&lt;incntvRgnNm3&gt;&lt;/incntvRgnNm3&gt;</p>
<p>&lt;incntvRgnNm4&gt;&lt;/incntvRgnNm4&gt;</p>
<p>&lt;opengPlce&gt;국가종합전자조달시스템(나라장터)&lt;/opengPlce&gt;</p>
<p>&lt;dcmtgOprtnDt&gt;&lt;/dcmtgOprtnDt&gt;</p>
<p>&lt;dcmtgOprtnPlce&gt;&lt;/dcmtgOprtnPlce&gt;</p>
<p>&lt;contrctrcnstrtnGovsplyMtrlAmt&gt;0&lt;/contrctrcnstrtnGovsplyMtrlAmt&gt;</p>
<p>&lt;govcnstrtnGovsplyMtrlAmt&gt;0&lt;/govcnstrtnGovsplyMtrlAmt&gt;</p>
<p>&lt;bidNtceDtlUrl&gt;https://www.g2b.go.kr/link/PNPE027_01/single/?bidPbancNo=R25BK00930755&amp;bidPbancOrd=000&lt;/bidNtceDtlUrl&gt;</p>
<p>&lt;bidNtceUrl&gt; https://www.g2b.go.kr/link/PNPE027_01/single/?bidPbancNo=R25BK00930755&amp;bidPbancOrd=000&lt;/bidNtceUrl&gt;</p>
<p>&lt;bidPrtcptFeePaymntYn&gt;&lt;/bidPrtcptFeePaymntYn&gt;</p>
<p>&lt;bidPrtcptFee&gt;&lt;/bidPrtcptFee&gt;</p>
<p>&lt;bidGrntymnyPaymntYn&gt;&lt;/bidGrntymnyPaymntYn&gt;</p>
<p>&lt;crdtrNm&gt;인천글로벌캠퍼스운영재단법인대표이사&lt;/crdtrNm&gt;</p>
<p>&lt;cmmnSpldmdCnum&gt;공고서에 의함&lt;/cmmnSpldmdCnum&gt;</p>
<p>&lt;untyNtceNo&gt;R25BM00300511&lt;/untyNtceNo&gt;</p>
<p>&lt;sptDscrptDocUrl1&gt;&lt;/sptDscrptDocUrl1&gt;</p>
<p>&lt;sptDscrptDocUrl2&gt;&lt;/sptDscrptDocUrl2&gt;</p>
<p>&lt;sptDscrptDocUrl3&gt;&lt;/sptDscrptDocUrl3&gt;</p>
<p>&lt;sptDscrptDocUrl4&gt;&lt;/sptDscrptDocUrl4&gt;</p>
<p>&lt;sptDscrptDocUrl5&gt;&lt;/sptDscrptDocUrl5&gt;</p>
<p>&lt;subsiCnsttyNm1&gt;&lt;/subsiCnsttyNm1&gt;</p>
<p>&lt;subsiCnsttyNm2&gt;&lt;/subsiCnsttyNm2&gt;</p>
<p>&lt;subsiCnsttyNm3&gt;&lt;/subsiCnsttyNm3&gt;</p>
<p>&lt;subsiCnsttyNm4&gt;&lt;/subsiCnsttyNm4&gt;</p>
<p>&lt;subsiCnsttyNm5&gt;&lt;/subsiCnsttyNm5&gt;</p>
<p>&lt;subsiCnsttyNm6&gt;&lt;/subsiCnsttyNm6&gt;</p>
<p>&lt;subsiCnsttyNm7&gt;&lt;/subsiCnsttyNm7&gt;</p>
<p>&lt;subsiCnsttyNm8&gt;&lt;/subsiCnsttyNm8&gt;</p>
<p>&lt;subsiCnsttyNm9&gt;&lt;/subsiCnsttyNm9&gt;</p>
<p>&lt;subsiCnsttyIndstrytyEvlRt1&gt;&lt;/subsiCnsttyIndstrytyEvlRt1&gt;</p>
<p>&lt;subsiCnsttyIndstrytyEvlRt2&gt;&lt;/subsiCnsttyIndstrytyEvlRt2&gt;</p>
<p>&lt;subsiCnsttyIndstrytyEvlRt3&gt;&lt;/subsiCnsttyIndstrytyEvlRt3&gt;</p>
<p>&lt;subsiCnsttyIndstrytyEvlRt4&gt;&lt;/subsiCnsttyIndstrytyEvlRt4&gt;</p>
<p>&lt;subsiCnsttyIndstrytyEvlRt5&gt;&lt;/subsiCnsttyIndstrytyEvlRt5&gt;</p>
<p>&lt;subsiCnsttyIndstrytyEvlRt6&gt;&lt;/subsiCnsttyIndstrytyEvlRt6&gt;</p>
<p>&lt;subsiCnsttyIndstrytyEvlRt7&gt;&lt;/subsiCnsttyIndstrytyEvlRt7&gt;</p>
<p>&lt;subsiCnsttyIndstrytyEvlRt8&gt;&lt;/subsiCnsttyIndstrytyEvlRt8&gt;</p>
<p>&lt;subsiCnsttyIndstrytyEvlRt9&gt;&lt;/subsiCnsttyIndstrytyEvlRt9&gt;</p>
<p>&lt;cmmnSpldmdMethdCd&gt;&lt;/cmmnSpldmdMethdCd&gt;</p>
<p>&lt;cmmnSpldmdMethdNm&gt;(없음)공동수급불허&lt;/cmmnSpldmdMethdNm&gt;</p>
<p>&lt;stdNtceDocUrl&gt;https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00930755&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=10&lt;/stdNtceDocUrl&gt;</p>
<p>&lt;brffcBidprcPermsnYn&gt;&lt;/brffcBidprcPermsnYn&gt;</p>
<p>&lt;cnsttyAccotShreRateList&gt;&lt;/cnsttyAccotShreRateList&gt;</p>
<p>&lt;cnstrtnAbltyEvlAmtList&gt;&lt;/cnstrtnAbltyEvlAmtList&gt;</p>
<p>&lt;dsgntCmptYn&gt;N&lt;/dsgntCmptYn&gt;</p>
<p>&lt;arsltCmptYn&gt;N&lt;/arsltCmptYn&gt;</p>
<p>&lt;pqEvalYn&gt;&lt;/pqEvalYn&gt;</p>
<p>&lt;ntceDscrptYn&gt;&lt;/ntceDscrptYn&gt;</p>
<p>&lt;rsrvtnPrceReMkngMthdNm&gt;&lt;/rsrvtnPrceReMkngMthdNm&gt;</p>
<p>&lt;mainCnsttyPresmptPrce&gt;&lt;/mainCnsttyPresmptPrce&gt;</p>
<p>&lt;orderPlanUntyNo&gt;R25DD20311262&lt;/orderPlanUntyNo&gt;</p>
<p>&lt;sucsfbidLwltRate&gt;89.745&lt;/sucsfbidLwltRate&gt;</p>
<p>&lt;rgstDt&gt;2025-07-01 09:17:24&lt;/rgstDt&gt;</p>
<p>&lt;bfSpecRgstNo&gt;&lt;/bfSpecRgstNo&gt;</p>
<p>&lt;sucsfbidMthdCd&gt;낙030029&lt;/sucsfbidMthdCd&gt;</p>
<p>&lt;sucsfbidMthdNm&gt;소액수의견적(2인 이상 견적 제출)-국민연금보험료 등 합산액 감액 적용&lt;/sucsfbidMthdNm&gt;</p>
<p>&lt;chgDt&gt;&lt;/chgDt&gt;</p>
<p>&lt;dminsttOfclEmailAdrs&gt;&lt;/dminsttOfclEmailAdrs&gt;</p>
<p>&lt;indstrytyLmtYn&gt;Y&lt;/indstrytyLmtYn&gt;</p>
<p>&lt;cnstrtsiteRgnNm&gt;인천광역시 연수구&lt;/cnstrtsiteRgnNm&gt;</p>
<p>&lt;rgnDutyJntcontrctYn&gt;N&lt;/rgnDutyJntcontrctYn&gt;</p>
<p>&lt;chgNtceRsn&gt;&lt;/chgNtceRsn&gt;</p>
<p>&lt;rbidOpengDt&gt;2025-07-07 09:00:00&lt;/rbidOpengDt&gt;</p>
<p>&lt;ciblAplYn&gt;Y&lt;/ciblAplYn&gt;</p>
<p>&lt;mtltyAdvcPsblYn&gt;N&lt;/mtltyAdvcPsblYn&gt;</p>
<p>&lt;mtltyAdvcPsblYnCnstwkNm&gt;전문공사-유지보수공사&lt;/mtltyAdvcPsblYnCnstwkNm&gt;</p>
<p>&lt;VAT&gt;18064545&lt;/VAT&gt;</p>
<p>&lt;indutyVAT&gt;&lt;/indutyVAT&gt;</p>
<p>&lt;indstrytyMfrcFldEvlYn&gt;N&lt;/indstrytyMfrcFldEvlYn&gt;</p>
<p>&lt;bidWgrnteeRcptClseDt&gt;&lt;/bidWgrnteeRcptClseDt&gt;</p>
<p>&lt;rgnLmtBidLocplcJdgmBssCd&gt;N&lt;/rgnLmtBidLocplcJdgmBssCd&gt; &lt;rgnLmtBidLocplcJdgmBssNm&gt;본사또는참여지사소재지&lt;/rgnLmtBidLocplcJdgmBssNm&gt;</p>
<p>&lt;sucsfbidMthdAppStd&gt;&lt;/sucsfbidMthdAppStd&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;/items&gt;</p>
<p>&lt;numOfRows&gt;10&lt;/numOfRows&gt;</p>
<p>&lt;pageNo&gt;1&lt;/pageNo&gt;</p>
<p>&lt;totalCount&gt;1&lt;/totalCount&gt;</p>
<p>&lt;/body&gt;</p>
<p>&lt;/response&gt;</p></td>
</tr>
</tbody>
</table>

#### \[나라장터검색조건에 의한 입찰공고용역조회\] 오퍼레이션 명세

<table style="width:99%;">
<colgroup>
<col style="width: 4%" />
<col style="width: 21%" />
<col style="width: 18%" />
<col style="width: 22%" />
<col style="width: 2%" />
<col style="width: 30%" />
</colgroup>
<tbody>
<tr>
<td rowspan="6">오퍼레이션 정보</td>
<td>오퍼레이션 번호</td>
<td>12</td>
<td>오퍼레이션명(국문)</td>
<td colspan="2">나라장터검색조건에 의한 입찰공고용역조회</td>
</tr>
<tr>
<td>오퍼레이션 유형</td>
<td>조회(목록)</td>
<td>오퍼레이션명(영문)</td>
<td colspan="2">getBidPblancListInfoServcPPSSrch</td>
</tr>
<tr>
<td>오퍼레이션 설명</td>
<td colspan="4">검색조건에 공고게시일시, 개찰일시 범위, 공고기관, 수요기관, 참조번호 등을 입력하여 나라장터의 입찰공고번호, 공고명, 발주기관, 수요기관, 계약체결방법명 등 용역부분의 입찰공고정보를 조회함</td>
</tr>
<tr>
<td>Call Back URL</td>
<td colspan="4">N/A</td>
</tr>
<tr>
<td>최대 메시지 사이즈</td>
<td colspan="4">[ 4000bytes]</td>
</tr>
<tr>
<td>평균 응답 시간</td>
<td>[ 500 ms]</td>
<td colspan="2">초당 최대 트랜잭션</td>
<td>[ 30 tps]</td>
</tr>
</tbody>
</table>

##### 요청 메시지 명세

<table style="width:99%;">
<colgroup>
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 13%" />
<col style="width: 12%" />
<col style="width: 13%" />
<col style="width: 19%" />
</colgroup>
<tbody>
<tr>
<td style="text-align: left;">항목명(영문)</td>
<td style="text-align: left;">항목명(국문)</td>
<td style="text-align: left;">항목크기</td>
<td style="text-align: left;">항목구분</td>
<td style="text-align: left;">샘플데이터</td>
<td style="text-align: left;">항목설명</td>
</tr>
<tr>
<td style="text-align: left;">numOfRows</td>
<td style="text-align: left;">한 페이지 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td style="text-align: left;">pageNo</td>
<td style="text-align: left;">페이지 번호</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">페이지 번호</td>
</tr>
<tr>
<td style="text-align: left;">ServiceKey</td>
<td style="text-align: left;">서비스키</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">공공데이터포탈에서 받은 인증키</td>
<td style="text-align: left;">공공데이터포탈에서 받은 인증키</td>
</tr>
<tr>
<td style="text-align: left;">type</td>
<td style="text-align: left;">타입</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">json</td>
<td style="text-align: left;">오픈API 리턴 타입을 JSON으로 받고 싶을 경우 'json' 으로 지정</td>
</tr>
<tr>
<td style="text-align: left;">inqryDiv</td>
<td style="text-align: left;">조회구분</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">검색하고자하는 조회구분<br />
1:공고게시일시, 2:개찰일시<br />
1. 공고게시일시 : 공고일자(pblancDate)<br />
2. 개찰일시 : 개찰일시(opengDt)</td>
</tr>
<tr>
<td style="text-align: left;">inqryBgnDt</td>
<td style="text-align: left;">조회시작일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">202507010000</td>
<td style="text-align: left;">검색하고자 하는 조회시작일시 "YYYYMMDDHHMM"<br />
조회구분이 '1'인 경우 공고게시일시 필수, '2'인 경우 개찰일시 필수</td>
</tr>
<tr>
<td style="text-align: left;">inqryEndDt</td>
<td style="text-align: left;">조회종료일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">202507012359</td>
<td style="text-align: left;">검색하고자 하는 조회종료일시 "YYYYMMDDHHMM"<br />
조회구분이 '1'인 경우 공고게시일시 필수, '2'인 경우 개찰일시 필수</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNm</td>
<td style="text-align: left;">입찰공고명</td>
<td style="text-align: left;">1000</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">AI 기반 탄소 데이터 정제 알고리즘 개발 용역</td>
<td style="text-align: left;">검색하고자하는 공고명<br />
※ 공고명 일부 입력시에도 조회 가능</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttCd</td>
<td style="text-align: left;">공고기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">B090021</td>
<td style="text-align: left;">검색하고자하는 공고기관코드</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttNm</td>
<td style="text-align: left;">공고기관명</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">한국생산기술연구원</td>
<td style="text-align: left;">검색하고자하는 공고기관명<br />
※ 공고기관명 일부 입력시에도 조회 가능</td>
</tr>
<tr>
<td style="text-align: left;">dminsttCd</td>
<td style="text-align: left;">수요기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">B090021</td>
<td style="text-align: left;"><p>검색하고자하는 수요기관코드</p>
<p>행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드 입력</p>
<p>행자부코드가 없는 경우 조달청에서 부여한 수요기관 코드 입력</p></td>
</tr>
<tr>
<td style="text-align: left;">dminsttNm</td>
<td style="text-align: left;">수요기관명</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">한국생산기술연구원</td>
<td style="text-align: left;">검색하고자하는 수요기관명<br />
※ 수요기관명 일부 입력시에도 조회 가능</td>
</tr>
<tr>
<td style="text-align: left;">refNo</td>
<td style="text-align: left;">참조번호</td>
<td style="text-align: left;">105</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">P81202500407</td>
<td style="text-align: left;">검색하고자하는 참조번호</td>
</tr>
<tr>
<td style="text-align: left;">prtcptLmtRgnCd</td>
<td style="text-align: left;">참가제한지역코드</td>
<td style="text-align: left;">2</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">00</td>
<td style="text-align: left;">검색하고자하는 참가제한지역코드<br />
11 : 서울특별시<br />
26 : 부산광역시<br />
27 : 대구광역시<br />
28 : 인천광역시<br />
29 : 광주광역시<br />
30 : 대전광역시<br />
31 : 울산광역시<br />
36 : 세종특별자치시<br />
41 : 경기도<br />
42 : 강원도<br />
43 : 충청북도<br />
44 : 충청남도<br />
45 : 전라북도<br />
46 : 전라남도<br />
47 : 경상북도<br />
48 : 경상남도<br />
50 : 제주도<br />
51 : 강원특별자치도<br />
52 : 전북특별자치도<br />
99 : 기타<br />
00: 전국<br />
*전국 : 지역제한을 설정하지 않은 공고</td>
</tr>
<tr>
<td style="text-align: left;">prtcptLmtRgnNm</td>
<td style="text-align: left;">참가제한지역명</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">전국</td>
<td style="text-align: left;">검색하고자하는 참가제한지역명<br />
※ 참가제한지역명 일부 입력시에도 조회 가능<br />
*전국 : 지역제한을 설정하지 않은 공고</td>
</tr>
<tr>
<td style="text-align: left;">indstrytyCd</td>
<td style="text-align: left;">업종코드</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">1494</td>
<td style="text-align: left;">검색하고자하는 업종코드</td>
</tr>
<tr>
<td style="text-align: left;">indstrytyNm</td>
<td style="text-align: left;">업종명</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">일반소방공사감리업(전기)</td>
<td style="text-align: left;">검색하고자하는 업종명<br />
※ 업종명 일부 입력시에도 조회 가능</td>
</tr>
<tr>
<td style="text-align: left;">presmptPrceBgn</td>
<td style="text-align: left;">추정가격시작</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">46363000</td>
<td style="text-align: left;">검색하고자하는 추정가격범위시작금액이상(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">presmptPrceEnd</td>
<td style="text-align: left;">추정가격종료</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">46364000</td>
<td style="text-align: left;">검색하고자하는 추정가격범위종료금액이하(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">dtilPrdctClsfcNo</td>
<td style="text-align: left;">세부품명번호</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">7611170100</td>
<td style="text-align: left;">검색하고자하는 세부품명번호</td>
</tr>
<tr>
<td style="text-align: left;">masYn</td>
<td style="text-align: left;">다수공급경쟁자여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">검색하고자하는 다수공급경쟁자여부 (용역업무의 경우 해당 컬럼 검색 불가)</td>
</tr>
<tr>
<td style="text-align: left;">prcrmntReqNo</td>
<td style="text-align: left;">조달요청번호</td>
<td style="text-align: left;">17</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">209700700</td>
<td style="text-align: left;">검색하고자하는 조달요청번호</td>
</tr>
<tr>
<td style="text-align: left;">bidClseExcpYn</td>
<td style="text-align: left;">입찰마감제외여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">검색하고자하는 입찰마감제외여부</td>
</tr>
<tr>
<td style="text-align: left;">intrntnlDivCd</td>
<td style="text-align: left;">국제구분코드</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">검색하고자하는 국제구분코드<br />
국내:1, 국제:2<br />
<br />
국내/시설 입찰 공고일 경우 : 1<br />
국외 입찰 공고일 경우 : 2</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 응답 메시지 명세

<table>
<colgroup>
<col style="width: 14%" />
<col style="width: 22%" />
<col style="width: 11%" />
<col style="width: 14%" />
<col style="width: 16%" />
<col style="width: 20%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;">항목명(영문)</th>
<th style="text-align: left;">항목명(국문)</th>
<th style="text-align: left;">항목크기</th>
<th style="text-align: left;">항목구분</th>
<th style="text-align: left;">샘플데이터</th>
<th style="text-align: left;">항목설명</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;">resultCode</td>
<td style="text-align: left;">결과코드</td>
<td style="text-align: left;">2</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">00</td>
<td style="text-align: left;">결과코드</td>
</tr>
<tr>
<td style="text-align: left;">resultMsg</td>
<td style="text-align: left;">결과메세지</td>
<td style="text-align: left;">50</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">정상.</td>
<td style="text-align: left;">결과메세지</td>
</tr>
<tr>
<td style="text-align: left;">numOfRows</td>
<td style="text-align: left;">한 페이지 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td style="text-align: left;">pageNo</td>
<td style="text-align: left;">페이지 번호</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">페이지 수</td>
</tr>
<tr>
<td style="text-align: left;">totalCount</td>
<td style="text-align: left;">데이터 총 개수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">17</td>
<td style="text-align: left;">데이터 총개수</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNo</td>
<td style="text-align: left;">입찰공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">R25BK00933736</td>
<td style="text-align: left;"><p>입찰공고 관리번입찰공고 관리번호이며 조달청나라장터 공고건의 형식은 년도(4)+월(2)+순번(5)이며 자체전자조달시스템 보유기관은 각 기관별 형식 별도 사용</p>
<p>*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성</p>
<p>-단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</p></td>
</tr>
<tr>
<td style="text-align: left;">bidNtceOrd</td>
<td style="text-align: left;">입찰공고차수</td>
<td style="text-align: left;">3</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">000</td>
<td style="text-align: left;">입찰공고차수는 해당 입찰공고에 대한 재공고 및 재입찰 등이 발생되었을 경우 증가되는 수</td>
</tr>
<tr>
<td style="text-align: left;">reNtceYn</td>
<td style="text-align: left;">재공고여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">본 입찰공고의 재공고 여부(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">rgstTyNm</td>
<td style="text-align: left;">등록유형명</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">조달청 또는 나라장터 자체 공고건</td>
<td style="text-align: left;">입찰공고가 "조달청 또는 나라장터 자체 공고건","'나라장터 기타 공고건"</td>
</tr>
<tr>
<td style="text-align: left;">ntceKindNm</td>
<td style="text-align: left;">공고종류명</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">등록공고</td>
<td style="text-align: left;">공고의 공고상태명으로 등록공고, 변경공고, 취소공고, 재공고 구분</td>
</tr>
<tr>
<td style="text-align: left;">intrbidYn</td>
<td style="text-align: left;">국제입찰여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">국제입찰대상인지의 여부를 나타내며 국제입찰 대상은 내외국인 또는 외국인을 대상으로 하여 물품, 공사 및 용역을 조달하기 위하여 행하는 입찰을 말하며 수의계약을 포함한다. 국가계약법 제4조에 의해 추정가격이 고시금액(국제입찰 적용 대상 기준금액으로 기획재정부장관 및 행정자치부장관이 매 2년마다 고시한 금액을 말하며 WTO 또는 양자간(FTA) 정부조달협정에 따르면 국제입찰 대상 기준 금액이 SDR(Special Drawing Rights:특별인출권) 통화단위로 되어 있어 주무부 장관이 이를 2년마다 원화로 환산하여 고시) 이상일 경우 국제입찰대상이 됨(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceDt</td>
<td style="text-align: left;">입찰공고일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-01 09:28:14</td>
<td style="text-align: left;">입찰공고서를 공고한 일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">refNo</td>
<td style="text-align: left;">참조번호</td>
<td style="text-align: left;">105</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">P81202500407</td>
<td style="text-align: left;">조달청 입찰공고의 경우 참조공고번호는 자체 전자조달시스템에서 관리하는 공고번호를 의미하며 자체전자조달시스템의 경우 참조공고번호는 나라장터(G2B) 입찰공고번호를 의미함</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNm</td>
<td style="text-align: left;">입찰공고명</td>
<td style="text-align: left;">1000</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">AI 기반 탄소 데이터 정제 알고리즘 개발 용역</td>
<td style="text-align: left;">공사명 또는 사업명이라고도 하며 입찰공고 내용을 요약한 이름</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttCd</td>
<td style="text-align: left;">공고기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">B090021</td>
<td style="text-align: left;">공고를 하는 기관의 코드로 행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드가 행자부코드가 없는 경우 조달청에서 부여한 공고기관 코드가 표기됨</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttNm</td>
<td style="text-align: left;">공고기관명</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">한국생산기술연구원</td>
<td style="text-align: left;">수요기관의 의뢰를 받아 공고하는 기관의 명</td>
</tr>
<tr>
<td style="text-align: left;">dminsttCd</td>
<td style="text-align: left;">수요기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">B090021</td>
<td style="text-align: left;">실제 수요기관의 코드로 행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드가 행자부코드가 없는 경우 조달청에서 부여한 수요기관 코드가 표기됨</td>
</tr>
<tr>
<td style="text-align: left;">dminsttNm</td>
<td style="text-align: left;">수요기관명</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">한국생산기술연구원</td>
<td style="text-align: left;">중앙조달인 경우 조달사업에 관한 법률 제2조(정의)에 따라 수요물자의 구매 공급 또는 시설공사 계약의 체결을 조달청장에게 요청할 수 있도록 조달청장이 인정하여 등록한 기관 또는 자체전자조달시스템을 이용하는 기관인 경우 계약을 의뢰한 기관의 명으로 공고기관과 수요기관이 동일할 수 있음</td>
</tr>
<tr>
<td style="text-align: left;">bidMethdNm</td>
<td style="text-align: left;">입찰방식명</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">전자입찰</td>
<td style="text-align: left;">공고의 입찰방식명 직찰<br />
전자입찰,전자입찰/직찰,전자/직찰/우편/상시,직찰/우편/상시,우편/상시,전자시담,복수견적(역경매),직찰/우편,전자시담(다자간)</td>
</tr>
<tr>
<td style="text-align: left;">cntrctCnclsMthdNm</td>
<td style="text-align: left;">계약체결방법명</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">제한경쟁</td>
<td style="text-align: left;">계약체결의 방법을 구분하는 명<br />
*일반경쟁계약은 계약 대상 물품의 규격 및 시방서와 계약조건 등을 널리 공고하여 일정한 자격을 가진 불특정 다수인의 입찰희망자를 모두 경쟁 입찰하는 계약방법<br />
*제한경쟁계약은 일반·지명경쟁계약제도의 단점을 보완하기 위해 실적제한, 기술보유제한, 특정물품제한, 지역제한 등을 두는 계약방법<br />
*지명경쟁계약은 계약상대자의 신용과 실적 등에 있어 적당하다고 인정하는 특정 다수의 경쟁 참가자를 지명하여 계약 상대방을 결정하는 계약방법<br />
*수의계약은 계약상대자를 결정함에 있어 경쟁방법에 의하지 않고 특정인을 선정하여 계약하는 계약방법</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttOfclNm</td>
<td style="text-align: left;">공고기관담당자명</td>
<td style="text-align: left;">35</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">권세운</td>
<td style="text-align: left;">공고기관의 공고를 담당하는 담당자의 명</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttOfclTelNo</td>
<td style="text-align: left;">공고기관담당자전화번호</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">041-589-8532</td>
<td style="text-align: left;">공고기관의 공고를 담당하는 담당자의 전화번호</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttOfclEmailAdrs</td>
<td style="text-align: left;">공고기관담당자이메일주소</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">940584@korea.kr</td>
<td style="text-align: left;">공고기관의 공고를 담당하는 담당자의 이메일주소</td>
</tr>
<tr>
<td style="text-align: left;">exctvNm</td>
<td style="text-align: left;">집행관명</td>
<td style="text-align: left;">35</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">권세운</td>
<td style="text-align: left;">공고의 집행관명</td>
</tr>
<tr>
<td style="text-align: left;">bidQlfctRgstDt</td>
<td style="text-align: left;">입찰참가자격등록마감일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-14 18:00</td>
<td style="text-align: left;">입찰참가등록이란 입찰사무를 효과적으로 집행하기 위하여 사전에 입찰참가자격등록을 해두었다가 필요 시 입찰에 참여하는 제도로 해당 공고에 대한 입찰참가자격의 등록이 완료되어야 하는 시점을 의미함 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">cmmnSpldmdAgrmntRcptdocMethd</td>
<td style="text-align: left;">공동수급협정서접수방식</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">없음</td>
<td style="text-align: left;">공동수급협정서의 접수방식"전자","수기","없음","공고서참고"</td>
</tr>
<tr>
<td style="text-align: left;">cmmnSpldmdAgrmntClseDt</td>
<td style="text-align: left;">공동수급협정마감일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-14 18:00</td>
<td style="text-align: left;">공동계약이 허용된 공고에 대해 공동수급체를 구성하여 입찰에 참여하고자 할 경우 구성원이 일정 분담내용에 따라 나누어 공동으로 이행하는 약속을 한 공동수급협정서를 작성하여야 하며 이때 공동수급협정서의 등록(작성) 마감 시점을 의미함”YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">cmmnSpldmdCorpRgnLmtYn</td>
<td style="text-align: left;">공동수급업체지역제한여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">공동수급협정시 구성원의 지역제한을 적용할지 여부. 지역제한인경우 협정 구성업체가 참가제한지역에 포함되어야 함.(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">bidBeginDt</td>
<td style="text-align: left;">입찰개시일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-02 09:00:00</td>
<td style="text-align: left;">입찰서의 제출을 개시하는 일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">bidClseDt</td>
<td style="text-align: left;">입찰마감일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-15 10:00:00</td>
<td style="text-align: left;">입찰서의 제출을 마감하는 일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">opengDt</td>
<td style="text-align: left;">개찰일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-15 11:00:00</td>
<td style="text-align: left;">집행관이 개찰을 수행할 수 있는 시작일시이며<br />
개찰일시 이후에 개찰이 가능함<br />
실제 개찰을 수행한 시간을 의미하지 않음 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl1</td>
<td style="text-align: left;">공고규격서URL1</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00933736&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=1&amp;prcmBsneSeCd=03</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl2</td>
<td style="text-align: left;">공고규격서URL2</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00933736&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=2&amp;prcmBsneSeCd=03</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl3</td>
<td style="text-align: left;">공고규격서URL3</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00933736&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=3&amp;prcmBsneSeCd=03</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl4</td>
<td style="text-align: left;">공고규격서URL4</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00933736&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=4&amp;prcmBsneSeCd=03</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl5</td>
<td style="text-align: left;">공고규격서URL5</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00933736&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=5&amp;prcmBsneSeCd=03</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl6</td>
<td style="text-align: left;">공고규격서URL6</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00933736&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=6&amp;prcmBsneSeCd=03</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl7</td>
<td style="text-align: left;">공고규격서URL7</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00933736&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=7&amp;prcmBsneSeCd=03</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl8</td>
<td style="text-align: left;">공고규격서URL8</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00933736&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=8&amp;prcmBsneSeCd=03</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl9</td>
<td style="text-align: left;">공고규격서URL9</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00933736&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=9&amp;prcmBsneSeCd=03</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl10</td>
<td style="text-align: left;">공고규격서URL10</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00933736&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=10&amp;prcmBsneSeCd=03</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm1</td>
<td style="text-align: left;">공고규격파일명1</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">과업지시서.hwp</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm2</td>
<td style="text-align: left;">공고규격파일명2</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">공고서.pdf</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm3</td>
<td style="text-align: left;">공고규격파일명3</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">세부과업지시서.hwp</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm4</td>
<td style="text-align: left;">공고규격파일명4</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">사업수행능력평가서 작성안내서_1.hwp</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm5</td>
<td style="text-align: left;">공고규격파일명5</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">사업수행능력평가서 작성안내서_2.hwp</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm6</td>
<td style="text-align: left;">공고규격파일명6</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">사업수행능력평가서 작성안내서_3.hwp</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm7</td>
<td style="text-align: left;">공고규격파일명7</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">사업수행능력평가서 작성안내서_4.hwp</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm8</td>
<td style="text-align: left;">공고규격파일명8</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">사업수행능력평가서 작성안내서_5.hwp</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm9</td>
<td style="text-align: left;">공고규격파일명9</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">사업수행능력평가서 작성안내서_6.hwp</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm10</td>
<td style="text-align: left;">공고규격파일명10</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">사업수행능력평가서 작성안내서_7.hwp</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">rbidPermsnYn</td>
<td style="text-align: left;">재입찰허용여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">입찰이 유찰되는 경우 재공고 없이 다시 입찰(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">pqApplDocRcptMthdNm</td>
<td style="text-align: left;">PQ신청서접수방법명</td>
<td style="text-align: left;">30</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">없음</td>
<td style="text-align: left;">PQ대상공고에서 PQ심사신청서를 어떻게 받을지에 대한 코드명</td>
</tr>
<tr>
<td style="text-align: left;">pqApplDocRcptDt</td>
<td style="text-align: left;">PQ신청서접수일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-14 18:00</td>
<td style="text-align: left;">PQ심사신청서 접수 마감일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">tpEvalApplMthdNm</td>
<td style="text-align: left;">TP심사신청방법명</td>
<td style="text-align: left;">30</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">없음</td>
<td style="text-align: left;">공고의 TP심사신청방법명</td>
</tr>
<tr>
<td style="text-align: left;">tpEvalApplClseDt</td>
<td style="text-align: left;">TP심사신청마감일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-14 18:00</td>
<td style="text-align: left;">공고의 TP심사신청마감일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">jntcontrctDutyRgnNm1</td>
<td style="text-align: left;">공동도급의무지역명1</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">서울특별시</td>
<td style="text-align: left;">공고의 공동도급의무지역명</td>
</tr>
<tr>
<td style="text-align: left;">jntcontrctDutyRgnNm2</td>
<td style="text-align: left;">공동도급의무지역명2</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">서울특별시</td>
<td style="text-align: left;">공고의 공동도급의무지역명</td>
</tr>
<tr>
<td style="text-align: left;">jntcontrctDutyRgnNm3</td>
<td style="text-align: left;">공동도급의무지역명3</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">서울특별시</td>
<td style="text-align: left;">공고의 공동도급의무지역명</td>
</tr>
<tr>
<td style="text-align: left;">rgnDutyJntcontrctRt</td>
<td style="text-align: left;">지역의무공동도급비율</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">지역의무공동동급시 3개지역의 공동도급합산 하한 비율(%)</td>
</tr>
<tr>
<td style="text-align: left;">dtlsBidYn</td>
<td style="text-align: left;">내역입찰여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">내역입찰인지는 나타내는 항목으로 내역입찰일 경우 투찰시 내역서를 첨부해야함(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">bidPrtcptLmtYn</td>
<td style="text-align: left;">입찰참가제한여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">공고의 입찰참가제한여부(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">prearngPrceDcsnMthdNm</td>
<td style="text-align: left;">예정가격결정방법명</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">복수예가</td>
<td style="text-align: left;">예정가격의 결정을 위해 복수예정가격방식으로 산정하는지 단일 예정가격으로 산정하는지를 구분하는 명</td>
</tr>
<tr>
<td style="text-align: left;">totPrdprcNum</td>
<td style="text-align: left;">총예가건수</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">15</td>
<td style="text-align: left;">공고의 총예가건수</td>
</tr>
<tr>
<td style="text-align: left;">drwtPrdprcNum</td>
<td style="text-align: left;">추첨예가건수</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">공고의 추첨예가건수</td>
</tr>
<tr>
<td style="text-align: left;">asignBdgtAmt</td>
<td style="text-align: left;">배정예산금액</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">51000000</td>
<td style="text-align: left;">사업목적물을 달성하기 위하여 배정된 예산액 또는 설계금액(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">presmptPrce</td>
<td style="text-align: left;">추정가격</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">46363636</td>
<td style="text-align: left;">물품/공사/용역 등의 조달 계약을 체결함에 있어 국제입찰 대상여부를 판단하는 기준 등으로 삼기 위하여 예정가격이 결정되기 전에 예산에 계상된 금액 등을 기준으로 하여 부가가치세 및 조달 수수료를 제외한 금액(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">opengPlce</td>
<td style="text-align: left;">개찰장소</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">우리 원 구매자산실 입찰집행관 PC</td>
<td style="text-align: left;">집행관이 개찰을 하는 장소</td>
</tr>
<tr>
<td style="text-align: left;">dcmtgOprtnDt</td>
<td style="text-align: left;">설명회실시일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-14 18:00</td>
<td style="text-align: left;">해당 공고에 대한 현장/입찰/과업 설명회를 실시하는 일시”YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">dcmtgOprtnPlce</td>
<td style="text-align: left;">설명회실시장소</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">우리청 관리과</td>
<td style="text-align: left;">해당 공고에 대한 설명회를 실시하는 경우 현장/입찰/과업 설명회를 실시하는 장소</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceDtlUrl</td>
<td style="text-align: left;">입찰공고상세URL</td>
<td style="text-align: left;">512</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/link/PNPE027_01/single/?bidPbancNo=R25BK00933736&amp;bidPbancOrd=000</td>
<td style="text-align: left;">나라장터시스템의 입찰공고 상세화면 링크</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceUrl</td>
<td style="text-align: left;">입찰공고URL</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/link/PNPE027_01/single/?bidPbancNo=R25BK00933736&amp;bidPbancOrd=000</td>
<td style="text-align: left;">해당 입찰공고를 인터넷상에서 확인할 수 있는 URL주소</td>
</tr>
<tr>
<td style="text-align: left;">bidPrtcptFeePaymntYn</td>
<td style="text-align: left;">입찰참가수수료납부여부</td>
<td style="text-align: left;">30</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">없음</td>
<td style="text-align: left;">입찰참가 의사가 있는 자가 납부하여야하는 수수료의 유무 및 납부방법을 표기하는 것으로 "전자납부, 수기 및 전자납부, 수기, 없음"으로 표기</td>
</tr>
<tr>
<td style="text-align: left;">bidPrtcptFee</td>
<td style="text-align: left;">입찰참가수수료</td>
<td style="text-align: left;">21</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">입찰에 참가하기위해 납부하는 수수료(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">bidGrntymnyPaymntYn</td>
<td style="text-align: left;">입찰보증금납부여부</td>
<td style="text-align: left;">30</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">불허</td>
<td style="text-align: left;">입찰보증금을 나라장터에서 전자로 납부가능하게 할지 여부 “전자납부허용”,”불허’으로 표기</td>
</tr>
<tr>
<td style="text-align: left;">crdtrNm</td>
<td style="text-align: left;">채권자명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">한국생산기술연구원장</td>
<td style="text-align: left;">입찰보증금 항목의 "보증채권자명"으로 전자입찰보증 접수시 사용</td>
</tr>
<tr>
<td style="text-align: left;">ppswGnrlSrvceYn</td>
<td style="text-align: left;">조달청일반용역여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">공고의 조달청일반용역여부(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">srvceDivNm</td>
<td style="text-align: left;">용역구분명</td>
<td style="text-align: left;">30</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">일반용역</td>
<td style="text-align: left;">공고의 용역구분명으로 일반용역/기술용역으로 구분</td>
</tr>
<tr>
<td style="text-align: left;">prdctClsfcLmtYn</td>
<td style="text-align: left;">물품분류제한여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">물품공고의 경우 물품분류번호로 제한할 경우 Y, 물품분류번호 제한없으면 N</td>
</tr>
<tr>
<td style="text-align: left;">mnfctYn</td>
<td style="text-align: left;">제조여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">물품분류로 투찰제한시 제조물품으로 제한할 지 여부. "Y"일 경우 투찰시 업체의 경쟁입찰참가자격등록증에 공고서상 물품분류가 제조물품으로 등록되어 있어야 투찰가능(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">purchsObjPrdctList</td>
<td style="text-align: left;">구매대상물품목록</td>
<td style="text-align: left;">4000</td>
<td style="text-align: left;">0..n</td>
<td style="text-align: left;">[1^7611170100^건설현장청소용역]</td>
<td style="text-align: left;">공고의 구매대상물품목록으로 [입찰분류번호^세부품명번호(세부물품분류번호)^세부품명(세부물품분류명)],[입찰분류번호^세부품명번호(세부물품분류번호)^세부품명(세부물품분류명)] 제공</td>
</tr>
<tr>
<td style="text-align: left;">untyNtceNo</td>
<td style="text-align: left;">통합공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25BM00300528</td>
<td style="text-align: left;">입찰공고를 구분하는 번호로 입찰공고번호이며 형식은 년도(4)+월(2)+순번(5)<br />
*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성<br />
- 단계구분: BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격), BK(통합입찰)</td>
</tr>
<tr>
<td style="text-align: left;">cmmnSpldmdMethdCd</td>
<td style="text-align: left;">공동수급방식코드</td>
<td style="text-align: left;">15</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">공500004</td>
<td style="text-align: left;">공동수급이라 함은 구성원을 2인 이상으로 하여 수급인이 해당계약을 공동으로 수행하기 위하여 잠정적으로 결성한 실체를 의미하며 공동수급체가도급을 받아 이행하는 방식을 구분하는 코드로<br />
공500001 : 공동이행<br />
공500002 : 분담이행<br />
공500003 : 주계약자관리방식<br />
공500004 : 단독계약<br />
공500005 : 혼합방식<br />
공500006 : 공동이행 또는 분담이행<br />
공500007 : 혼합_단독<br />
공500008 : 혼합_공동<br />
공500012 : 해당없음으로 구분됨</td>
</tr>
<tr>
<td style="text-align: left;">cmmnSpldmdMethdNm</td>
<td style="text-align: left;">공동수급방식명</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">(없음)공동수급불허</td>
<td style="text-align: left;">공고의 공동수급구성방식명</td>
</tr>
<tr>
<td style="text-align: left;">stdNtceDocUrl</td>
<td style="text-align: left;">표준공고서URL</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00933736&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=2</td>
<td style="text-align: left;">공고의 표준공고문URL</td>
</tr>
<tr>
<td style="text-align: left;">brffcBidprcPermsnYn</td>
<td style="text-align: left;">지사투찰허용여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">지역제한 공고에 한해서 지사 투찰을 허용할지 여부. 투찰제어시 사용(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">dsgntCmptYn</td>
<td style="text-align: left;">지명경쟁여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">공고의 지명경쟁여부(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">arsltCmptYn</td>
<td style="text-align: left;">실적경쟁여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">공고의 실적경쟁여부(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">pqEvalYn</td>
<td style="text-align: left;">PQ심사여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">공고의 PQ심사여부(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">tpEvalYn</td>
<td style="text-align: left;">TP심사여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">공고의 물품규격명(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">ntceDscrptYn</td>
<td style="text-align: left;">공고설명여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">공고의 공고설명여부(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">rsrvtnPrceReMkngMthdNm</td>
<td style="text-align: left;">예비가격재작성방법명</td>
<td style="text-align: left;">50</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">재입찰시 기존 예비가격을 사용하여 예정가격이 산정됩니다.</td>
<td style="text-align: left;">공고의 예비가격재작성방법명</td>
</tr>
<tr>
<td style="text-align: left;">arsltApplDocRcptMthdNm</td>
<td style="text-align: left;">실적신청서접수방법명</td>
<td style="text-align: left;">50</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">전자문서</td>
<td style="text-align: left;">공고의 실적신청서접수방법명</td>
</tr>
<tr>
<td style="text-align: left;">arsltReqstdocRcptDt</td>
<td style="text-align: left;">실적신청서접수일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-14 18:00</td>
<td style="text-align: left;">실적심사신청서 접수마감일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">orderPlanUntyNo</td>
<td style="text-align: left;">발주계획통합번호</td>
<td style="text-align: left;">35</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25DD20312981</td>
<td style="text-align: left;">*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성<br />
- 단계구분: BK(입찰)<br />
TA(계약)<br />
DD:(발주계획)<br />
BD(사전규격),<br />
BK(통합입찰)</td>
</tr>
<tr>
<td style="text-align: left;">sucsfbidLwltRate</td>
<td style="text-align: left;">낙찰하한율</td>
<td style="text-align: left;">22</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">87.745</td>
<td style="text-align: left;">개찰시 사용하는 낙찰하한율(%)</td>
</tr>
<tr>
<td style="text-align: left;">rgstDt</td>
<td style="text-align: left;">등록일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">2025-07-01 09:28:14</td>
<td style="text-align: left;">공고의 등록일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">bfSpecRgstNo</td>
<td style="text-align: left;">사전규격등록번호</td>
<td style="text-align: left;">17</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25BD00084695</td>
<td style="text-align: left;"><p>*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성</p>
<p>- 단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</p></td>
</tr>
<tr>
<td style="text-align: left;">infoBizYn</td>
<td style="text-align: left;">정보화사업여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">정보화사업여부<br />
Y/N</td>
</tr>
<tr>
<td style="text-align: left;">sucsfbidMthdCd</td>
<td style="text-align: left;">낙찰방법코드</td>
<td style="text-align: left;">9</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">낙030005</td>
<td style="text-align: left;">낙찰방법명에 대한 코드 (한글 1자리 + 숫자 6자리)</td>
</tr>
<tr>
<td style="text-align: left;">sucsfbidMthdNm</td>
<td style="text-align: left;">낙찰방법명</td>
<td style="text-align: left;">700</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">협상에의한계약</td>
<td style="text-align: left;">낙찰자를 결정하는 방법-낙찰방법 세부기준</td>
</tr>
<tr>
<td style="text-align: left;">chgDt</td>
<td style="text-align: left;">변경일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-01 09:28:14</td>
<td style="text-align: left;">공고의 변경일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">dminsttOfclEmailAdrs</td>
<td style="text-align: left;">수요기관담당자이메일주소</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">nskk22@kywa.or.kr</td>
<td style="text-align: left;">수요기관 담당자의 이메일주소</td>
</tr>
<tr>
<td style="text-align: left;">indstrytyLmtYn</td>
<td style="text-align: left;">업종제한여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">Y</td>
<td style="text-align: left;">해당 공고 입찰 시 업종(면허)제한을 두는지의 여부<br />
예시)Y</td>
</tr>
<tr>
<td style="text-align: left;">chgNtceRsn</td>
<td style="text-align: left;">변경공고사유</td>
<td style="text-align: left;">4000</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">공동수급협정서 접수 여부 변경</td>
<td style="text-align: left;"><p>공고종류명(공고의 공고상태명) 이 변경일 경우 변경공고사유 , 취소일 경우 취소공고사유</p>
<p>(연계공고건는 제외)</p></td>
</tr>
<tr>
<td style="text-align: left;">rbidOpengDt</td>
<td style="text-align: left;">재입찰개찰일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-15 11:00:00</td>
<td style="text-align: left;">공고종류명이 ‘재입찰’ 일 경우 재입찰공고의 개찰을 수행할 수 있는 시작일시<br />
“YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">VAT</td>
<td style="text-align: left;">부가가치세</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">4636364</td>
<td style="text-align: left;">부가가치세</td>
</tr>
<tr>
<td style="text-align: left;">indutyVAT</td>
<td style="text-align: left;">주공종부가가치세</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">주공종부가가치세</td>
</tr>
<tr>
<td style="text-align: left;">rgnLmtBidLocplcJdgmBssCd</td>
<td style="text-align: left;">지역제한입찰소재지판단기준코드</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">지역제한입찰소재지판단기준코드</td>
</tr>
<tr>
<td style="text-align: left;">rgnLmtBidLocplcJdgmBssNm</td>
<td style="text-align: left;">지역제한입찰소재지판단기준명</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">본사또는참여지사소재지</td>
<td style="text-align: left;">지역제한입찰소재지판단기준명</td>
</tr>
<tr>
<td style="text-align: left;">pubPrcrmntLrgclsfcNm</td>
<td style="text-align: left;">공공조달대분류명</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">ICT 서비스</td>
<td style="text-align: left;">나라장터에서의 사업분류체계의 공공조달분류번호의 대분류에 해당되는 명</td>
</tr>
<tr>
<td style="text-align: left;">pubPrcrmntMidclsfcNm</td>
<td style="text-align: left;">공공조달중분류명</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">DB구축 및 자료입력</td>
<td style="text-align: left;">나라장터에서의 사업분류체계의 공공조달분류번호의 중분류에 해당되는 명</td>
</tr>
<tr>
<td style="text-align: left;">pubPrcrmntClsfcNo</td>
<td style="text-align: left;">공공조달분류번호</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">81112002</td>
<td style="text-align: left;">나라장터에서의 사업분류체계의 공공조달분류번호</td>
</tr>
<tr>
<td style="text-align: left;">techAbltEvlRt</td>
<td style="text-align: left;">기술능력평가비율</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">80</td>
<td style="text-align: left;">협상에 의한 낙찰자 결정의 경우 기술능력 평가 비율</td>
</tr>
<tr>
<td style="text-align: left;">bidPrceEvlRt</td>
<td style="text-align: left;">입찰가격평가비율</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">협상에 의한 낙찰자 결정의 경우 기술능력 입찰가격 평가 비율</td>
</tr>
<tr>
<td style="text-align: left;">sucsfbidMthdAppStd</td>
<td style="text-align: left;">낙찰방법적용기준</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">조달청 시설공사 적격심사세부기준</td>
<td style="text-align: left;"><p>낙찰자를 결정하</p>
<p>방법 적용기준</p></td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 요청 / 응답 메시지 예제

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr>
<td style="text-align: center;"><strong>REST(URI)</strong></td>
</tr>
<tr>
<td style="text-align: left;">http://apis.data.go.kr/1230000/ad/BidPublicInfoService/ getBidPblancListInfoServcPPSSrch?type=xml&amp;inqryDiv=1&amp;inqryBgnDt=202507010000&amp;inqryEndDt=202507012359&amp;numOfRows=10&amp;pageNo=1&amp;bidNtceNm= AI 기반 탄소 데이터 정제 알고리즘 개발 용역&amp;ServiceKey=인증키</td>
</tr>
<tr>
<td style="text-align: center;"><strong>응답 메시지</strong></td>
</tr>
<tr>
<td style="text-align: left;"><p>&lt;response&gt;</p>
<p>&lt;header&gt;</p>
<p>&lt;resultCode&gt;00&lt;/resultCode&gt;</p>
<p>&lt;resultMsg&gt;정상&lt;/resultMsg&gt;</p>
<p>&lt;/header&gt;</p>
<p>&lt;body&gt;</p>
<p>&lt;items&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00933736&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;reNtceYn&gt;N&lt;/reNtceYn&gt;</p>
<p>&lt;rgstTyNm&gt;조달청 또는 나라장터 자체 공고건&lt;/rgstTyNm&gt;</p>
<p>&lt;ntceKindNm&gt;등록공고&lt;/ntceKindNm&gt;</p>
<p>&lt;intrbidYn&gt;N&lt;/intrbidYn&gt;</p>
<p>&lt;bidNtceDt&gt;2025-07-01 09:28:14&lt;/bidNtceDt&gt;</p>
<p>&lt;refNo&gt;P81202500407&lt;/refNo&gt;</p>
<p>&lt;bidNtceNm&gt;AI 기반 탄소 데이터 정제 알고리즘 개발 용역&lt;/bidNtceNm&gt;</p>
<p>&lt;ntceInsttCd&gt;B090021&lt;/ntceInsttCd&gt;</p>
<p>&lt;ntceInsttNm&gt;한국생산기술연구원&lt;/ntceInsttNm&gt;</p>
<p>&lt;dminsttCd&gt;B090021&lt;/dminsttCd&gt;</p>
<p>&lt;dminsttNm&gt;한국생산기술연구원&lt;/dminsttNm&gt;</p>
<p>&lt;bidMethdNm&gt;전자입찰&lt;/bidMethdNm&gt;</p>
<p>&lt;cntrctCnclsMthdNm&gt;제한경쟁&lt;/cntrctCnclsMthdNm&gt;</p>
<p>&lt;ntceInsttOfclNm&gt;권세운&lt;/ntceInsttOfclNm&gt;</p>
<p>&lt;ntceInsttOfclTelNo&gt;041-589-8532&lt;/ntceInsttOfclTelNo&gt;</p>
<p>&lt;ntceInsttOfclEmailAdrs&gt;&lt;/ntceInsttOfclEmailAdrs&gt;</p>
<p>&lt;exctvNm&gt;권세운&lt;/exctvNm&gt;</p>
<p>&lt;bidQlfctRgstDt&gt;2025-07-14 18:00&lt;/bidQlfctRgstDt&gt;</p>
<p>&lt;cmmnSpldmdAgrmntRcptdocMethd&gt;없음&lt;/cmmnSpldmdAgrmntRcptdocMethd&gt;</p>
<p>&lt;cmmnSpldmdAgrmntClseDt&gt;&lt;/cmmnSpldmdAgrmntClseDt&gt;</p>
<p>&lt;cmmnSpldmdCorpRgnLmtYn&gt;&lt;/cmmnSpldmdCorpRgnLmtYn&gt;</p>
<p>&lt;bidBeginDt&gt;2025-07-02 09:00:00&lt;/bidBeginDt&gt;</p>
<p>&lt;bidClseDt&gt;2025-07-15 10:00:00&lt;/bidClseDt&gt;</p>
<p>&lt;opengDt&gt;2025-07-15 11:00:00&lt;/opengDt&gt;</p>
<p>&lt;ntceSpecDocUrl1&gt;https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00933736&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=1&amp;prcmBsneSeCd=03&lt;/ntceSpecDocUrl1&gt;</p>
<p>&lt;ntceSpecDocUrl2&gt;https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00933736&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=2&amp;prcmBsneSeCd=03&lt;/ntceSpecDocUrl2&gt;</p>
<p>&lt;ntceSpecDocUrl3&gt;&lt;/ntceSpecDocUrl3&gt;</p>
<p>&lt;ntceSpecDocUrl4&gt;&lt;/ntceSpecDocUrl4&gt;</p>
<p>&lt;ntceSpecDocUrl5&gt;&lt;/ntceSpecDocUrl5&gt;</p>
<p>&lt;ntceSpecDocUrl6&gt;&lt;/ntceSpecDocUrl6&gt;</p>
<p>&lt;ntceSpecDocUrl7&gt;&lt;/ntceSpecDocUrl7&gt;</p>
<p>&lt;ntceSpecDocUrl8&gt;&lt;/ntceSpecDocUrl8&gt;</p>
<p>&lt;ntceSpecDocUrl9&gt;&lt;/ntceSpecDocUrl9&gt;</p>
<p>&lt;ntceSpecDocUrl10&gt;&lt;/ntceSpecDocUrl10&gt;</p>
<p>&lt;ntceSpecFileNm1&gt;과업지시서.hwp&lt;/ntceSpecFileNm1&gt;</p>
<p>&lt;ntceSpecFileNm2&gt;공고서.pdf&lt;/ntceSpecFileNm2&gt;</p>
<p>&lt;ntceSpecFileNm3&gt;&lt;/ntceSpecFileNm3&gt;</p>
<p>&lt;ntceSpecFileNm4&gt;&lt;/ntceSpecFileNm4&gt;</p>
<p>&lt;ntceSpecFileNm5&gt;&lt;/ntceSpecFileNm5&gt;</p>
<p>&lt;ntceSpecFileNm6&gt;&lt;/ntceSpecFileNm6&gt;</p>
<p>&lt;ntceSpecFileNm7&gt;&lt;/ntceSpecFileNm7&gt;</p>
<p>&lt;ntceSpecFileNm8&gt;&lt;/ntceSpecFileNm8&gt;</p>
<p>&lt;ntceSpecFileNm9&gt;&lt;/ntceSpecFileNm9&gt;</p>
<p>&lt;ntceSpecFileNm10&gt;&lt;/ntceSpecFileNm10&gt;</p>
<p>&lt;rbidPermsnYn&gt;N&lt;/rbidPermsnYn&gt;</p>
<p>&lt;pqApplDocRcptMthdNm&gt;&lt;/pqApplDocRcptMthdNm&gt;</p>
<p>&lt;pqApplDocRcptDt&gt;&lt;/pqApplDocRcptDt&gt;</p>
<p>&lt;tpEvalApplMthdNm&gt;&lt;/tpEvalApplMthdNm&gt;</p>
<p>&lt;tpEvalApplClseDt&gt;&lt;/tpEvalApplClseDt&gt;</p>
<p>&lt;jntcontrctDutyRgnNm1&gt;&lt;/jntcontrctDutyRgnNm1&gt;</p>
<p>&lt;jntcontrctDutyRgnNm2&gt;&lt;/jntcontrctDutyRgnNm2&gt;</p>
<p>&lt;jntcontrctDutyRgnNm3&gt;&lt;/jntcontrctDutyRgnNm3&gt;</p>
<p>&lt;rgnDutyJntcontrctRt&gt;&lt;/rgnDutyJntcontrctRt&gt;</p>
<p>&lt;dtlsBidYn&gt;&lt;/dtlsBidYn&gt;</p>
<p>&lt;bidPrtcptLmtYn&gt;N&lt;/bidPrtcptLmtYn&gt;</p>
<p>&lt;prearngPrceDcsnMthdNm&gt;복수예가&lt;/prearngPrceDcsnMthdNm&gt;</p>
<p>&lt;totPrdprcNum&gt;15&lt;/totPrdprcNum&gt;</p>
<p>&lt;drwtPrdprcNum&gt;4&lt;/drwtPrdprcNum&gt;</p>
<p>&lt;asignBdgtAmt&gt;51000000&lt;/asignBdgtAmt&gt;</p>
<p>&lt;presmptPrce&gt;46363636&lt;/presmptPrce&gt;</p>
<p>&lt;opengPlce&gt;우리 원 구매자산실 입찰집행관 PC&lt;/opengPlce&gt;</p>
<p>&lt;dcmtgOprtnDt&gt;&lt;/dcmtgOprtnDt&gt;</p>
<p>&lt;dcmtgOprtnPlce&gt;&lt;/dcmtgOprtnPlce&gt;</p>
<p>&lt;bidNtceDtlUrl&gt;https://www.g2b.go.kr/link/PNPE027_01/single/?bidPbancNo=R25BK00933736&amp;bidPbancOrd=000&lt;/bidNtceDtlUrl&gt;</p>
<p>&lt;bidNtceUrl&gt; https://www.g2b.go.kr/link/PNPE027_01/single/?bidPbancNo=R25BK00933736&amp;bidPbancOrd=000&lt;/bidNtceUrl&gt;</p>
<p>&lt;bidPrtcptFeePaymntYn&gt;&lt;/bidPrtcptFeePaymntYn&gt;</p>
<p>&lt;bidPrtcptFee&gt;0&lt;/bidPrtcptFee&gt;</p>
<p>&lt;bidGrntymnyPaymntYn&gt;&lt;/bidGrntymnyPaymntYn&gt;</p>
<p>&lt;crdtrNm&gt;한국생산기술연구원장&lt;/crdtrNm&gt;</p>
<p>&lt;ppswGnrlSrvceYn&gt;N&lt;/ppswGnrlSrvceYn&gt;</p>
<p>&lt;srvceDivNm&gt;일반용역&lt;/srvceDivNm&gt;</p>
<p>&lt;prdctClsfcLmtYn&gt;&lt;/prdctClsfcLmtYn&gt;</p>
<p>&lt;mnfctYn&gt;&lt;/mnfctYn&gt;</p>
<p>&lt;purchsObjPrdctList&gt;&lt;/purchsObjPrdctList&gt;</p>
<p>&lt;untyNtceNo&gt;R25BM00300528&lt;/untyNtceNo&gt;</p>
<p>&lt;cmmnSpldmdMethdCd&gt;&lt;/cmmnSpldmdMethdCd&gt;</p>
<p>&lt;cmmnSpldmdMethdNm&gt;(없음)공동수급불허&lt;/cmmnSpldmdMethdNm&gt;</p>
<p>&lt;stdNtceDocUrl&gt;https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00933736&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=2&amp;prcmBsneSeCd=03&lt;/stdNtceDocUrl&gt;</p>
<p>&lt;brffcBidprcPermsnYn&gt;&lt;/brffcBidprcPermsnYn&gt;</p>
<p>&lt;dsgntCmptYn&gt;N&lt;/dsgntCmptYn&gt;</p>
<p>&lt;arsltCmptYn&gt;N&lt;/arsltCmptYn&gt;</p>
<p>&lt;pqEvalYn&gt;&lt;/pqEvalYn&gt;</p>
<p>&lt;tpEvalYn&gt;N&lt;/tpEvalYn&gt;</p>
<p>&lt;ntceDscrptYn&gt;&lt;/ntceDscrptYn&gt;</p>
<p>&lt;rsrvtnPrceReMkngMthdNm&gt;&lt;/rsrvtnPrceReMkngMthdNm&gt;</p>
<p>&lt;arsltApplDocRcptMthdNm&gt;&lt;/arsltApplDocRcptMthdNm&gt;</p>
<p>&lt;arsltReqstdocRcptDt&gt;&lt;/arsltReqstdocRcptDt&gt;</p>
<p>&lt;orderPlanUntyNo&gt;R25DD20312981&lt;/orderPlanUntyNo&gt;</p>
<p>&lt;sucsfbidLwltRate&gt;&lt;/sucsfbidLwltRate&gt;</p>
<p>&lt;rgstDt&gt;2025-07-01 09:28:14&lt;/rgstDt&gt;</p>
<p>&lt;bfSpecRgstNo&gt;R25BD00084695&lt;/bfSpecRgstNo&gt;</p>
<p>&lt;infoBizYn&gt;&lt;/infoBizYn&gt;</p>
<p>&lt;sucsfbidMthdCd&gt;낙030005&lt;/sucsfbidMthdCd&gt;</p>
<p>&lt;sucsfbidMthdNm&gt;협상에의한계약&lt;/sucsfbidMthdNm&gt;</p>
<p>&lt;chgDt&gt;&lt;/chgDt&gt;</p>
<p>&lt;dminsttOfclEmailAdrs&gt;&lt;/dminsttOfclEmailAdrs&gt;</p>
<p>&lt;indstrytyLmtYn&gt;N&lt;/indstrytyLmtYn&gt;</p>
<p>&lt;chgNtceRsn&gt;&lt;/chgNtceRsn&gt;</p>
<p>&lt;rbidOpengDt&gt;2025-07-15 11:00:00&lt;/rbidOpengDt&gt;</p>
<p>&lt;VAT&gt;4636364&lt;/VAT&gt;</p>
<p>&lt;indutyVAT&gt;&lt;/indutyVAT&gt;</p>
<p>&lt;rgnLmtBidLocplcJdgmBssCd&gt;&lt;/rgnLmtBidLocplcJdgmBssCd&gt;</p>
<p>&lt;rgnLmtBidLocplcJdgmBssNm&gt;&lt;/rgnLmtBidLocplcJdgmBssNm&gt;</p>
<p>&lt;pubPrcrmntLrgClsfcNm&gt;ICT 서비스&lt;/pubPrcrmntLrgClsfcNm&gt;</p>
<p>&lt;pubPrcrmntMidClsfcNm&gt;DB구축 및 자료입력&lt;/pubPrcrmntMidClsfcNm&gt;</p>
<p>&lt;pubPrcrmntClsfcNo&gt;81112002&lt;/pubPrcrmntClsfcNo&gt;</p>
<p>&lt;pubPrcrmntClsfcNm&gt;데이터서비스&lt;/pubPrcrmntClsfcNm&gt;</p>
<p>&lt;techAbltEvlRt&gt;80&lt;/techAbltEvlRt&gt;</p>
<p>&lt;bidPrceEvlRt&gt;20&lt;/bidPrceEvlRt&gt;</p>
<p>&lt;sucsfbidMthdAppStd&gt;&lt;/sucsfbidMthdAppStd&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;/items&gt;</p>
<p>&lt;numOfRows&gt;999&lt;/numOfRows&gt;</p>
<p>&lt;pageNo&gt;1&lt;/pageNo&gt;</p>
<p>&lt;totalCount&gt;1&lt;/totalCount&gt;</p>
<p>&lt;/body&gt;</p>
<p>&lt;/response&gt;</p></td>
</tr>
</tbody>
</table>

#### \
\[나라장터검색조건에 의한 입찰공고외자조회\] 오퍼레이션 명세

<table>
<colgroup>
<col style="width: 4%" />
<col style="width: 21%" />
<col style="width: 17%" />
<col style="width: 21%" />
<col style="width: 2%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr>
<td rowspan="6">오퍼레이션 정보</td>
<td>오퍼레이션 번호</td>
<td>13</td>
<td>오퍼레이션명(국문)</td>
<td colspan="2">나라장터검색조건에 의한 입찰공고외자조회</td>
</tr>
<tr>
<td>오퍼레이션 유형</td>
<td>조회(목록)</td>
<td>오퍼레이션명(영문)</td>
<td colspan="2">getBidPblancListInfoFrgcptPPSSrch</td>
</tr>
<tr>
<td>오퍼레이션 설명</td>
<td colspan="4">검색조건에 공고게시일시, 개찰일시 범위, 공고기관, 수요기관, 참조번호 등을 입력하여 나라장터의 입찰공고번호, 공고명, 발주기관, 수요기관, 계약체결방법명 등 외자부분의 입찰공고정보를 조회함</td>
</tr>
<tr>
<td>Call Back URL</td>
<td colspan="4">N/A</td>
</tr>
<tr>
<td>최대 메시지 사이즈</td>
<td colspan="4">[ 4000bytes]</td>
</tr>
<tr>
<td>평균 응답 시간</td>
<td>[ 500 ms]</td>
<td colspan="2">초당 최대 트랜잭션</td>
<td>[ 30 tps]</td>
</tr>
</tbody>
</table>

##### 요청 메시지 명세

<table>
<colgroup>
<col style="width: 19%" />
<col style="width: 19%" />
<col style="width: 13%" />
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 21%" />
</colgroup>
<tbody>
<tr>
<td>항목명(영문)</td>
<td>항목명(국문)</td>
<td>항목크기</td>
<td>항목구분</td>
<td>샘플데이터</td>
<td>항목설명</td>
</tr>
<tr>
<td style="text-align: left;">numOfRows</td>
<td style="text-align: left;">한 페이지 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td style="text-align: left;">pageNo</td>
<td style="text-align: left;">페이지 번호</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">페이지 번호</td>
</tr>
<tr>
<td style="text-align: left;">ServiceKey</td>
<td style="text-align: left;">서비스키</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">공공데이터포탈에서 받은 인증키</td>
<td style="text-align: left;">공공데이터포탈에서 받은 인증키</td>
</tr>
<tr>
<td style="text-align: left;">type</td>
<td style="text-align: left;">타입</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">0</td>
<td>json</td>
<td style="text-align: left;">오픈API 리턴 타입을 JSON으로 받고 싶을 경우 'json' 으로 지정</td>
</tr>
<tr>
<td style="text-align: left;">inqryDiv</td>
<td style="text-align: left;">조회구분</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">검색하고자하는 조회구분<br />
1:공고게시일시, 2:개찰일시<br />
1. 공고게시일시 : 공고일자(pblancDate)<br />
2. 개찰일시 : 개찰일시(opengDt)</td>
</tr>
<tr>
<td style="text-align: left;">inqryBgnDt</td>
<td style="text-align: left;">조회시작일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">202507010000</td>
<td style="text-align: left;">검색하고자 하는 조회시작일시 "YYYYMMDDHHMM"<br />
조회구분이 '1'인 경우 공고게시일시 필수, '2'인 경우 개찰일시 필수</td>
</tr>
<tr>
<td style="text-align: left;">inqryEndDt</td>
<td style="text-align: left;">조회종료일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">202507012359</td>
<td style="text-align: left;">검색하고자 하는 조회종료일시 "YYYYMMDDHHMM"<br />
조회구분이 '1'인 경우 공고게시일시 필수, '2'인 경우 개찰일시 필수</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNm</td>
<td style="text-align: left;">입찰공고명</td>
<td style="text-align: left;">1000</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">라만 분광기</td>
<td style="text-align: left;">검색하고자하는 공고명<br />
※ 공고명 일부 입력시에도 조회 가능</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttCd</td>
<td style="text-align: left;">공고기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">1230000</td>
<td style="text-align: left;">검색하고자하는 공고기관코드</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttNm</td>
<td style="text-align: left;">공고기관명</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">조달청</td>
<td style="text-align: left;">검색하고자하는 공고기관명<br />
※ 공고기관명 일부 입력시에도 조회 가능</td>
</tr>
<tr>
<td style="text-align: left;">dminsttCd</td>
<td style="text-align: left;">수요기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">B551184</td>
<td style="text-align: left;"><p>검색하고자하는 수요기관코드</p>
<p>행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드 입력</p>
<p>행자부코드가 없는 경우 조달청에서 부여한 수요기관 코드 입력</p></td>
</tr>
<tr>
<td style="text-align: left;">dminsttNm</td>
<td style="text-align: left;">수요기관명</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">한국에너지기술연구원</td>
<td style="text-align: left;">검색하고자하는 수요기관명<br />
※ 수요기관명 일부 입력시에도 조회 가능</td>
</tr>
<tr>
<td style="text-align: left;">refNo</td>
<td style="text-align: left;">참조번호</td>
<td style="text-align: left;">105</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25DC00068938</td>
<td style="text-align: left;">검색하고자하는 참조번호</td>
</tr>
<tr>
<td style="text-align: left;">prtcptLmtRgnCd</td>
<td style="text-align: left;">참가제한지역코드</td>
<td style="text-align: left;">2</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">00</td>
<td style="text-align: left;">검색하고자하는 참가제한지역코드<br />
11 : 서울특별시<br />
26 : 부산광역시<br />
27 : 대구광역시<br />
28 : 인천광역시<br />
29 : 광주광역시<br />
30 : 대전광역시<br />
31 : 울산광역시36 : 세종특별자치시<br />
41 : 경기도<br />
42 : 강원도<br />
43 : 충청북도<br />
44 : 충청남도<br />
45 : 전라북도<br />
46 : 전라남도<br />
47 : 경상북도<br />
48 : 경상남도<br />
50 : 제주도<br />
51 : 강원특별자치도<br />
52 : 전북특별자치도<br />
99 : 기타<br />
00: 전국<br />
*전국 : 지역제한을 설정하지 않은 공고</td>
</tr>
<tr>
<td style="text-align: left;">prtcptLmtRgnNm</td>
<td style="text-align: left;">참가제한지역명</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">전국</td>
<td style="text-align: left;">검색하고자하는 참가제한지역명<br />
※ 참가제한지역명 일부 입력시에도 조회 가능<br />
*전국 : 지역제한을 설정하지 않은 공고</td>
</tr>
<tr>
<td style="text-align: left;">indstrytyCd</td>
<td style="text-align: left;">업종코드</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0003</td>
<td style="text-align: left;">검색하고자하는 업종코드</td>
</tr>
<tr>
<td style="text-align: left;">indstrytyNm</td>
<td style="text-align: left;">업종명</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">토목공사업</td>
<td style="text-align: left;">검색하고자하는 업종명<br />
※ 업종명 일부 입력시에도 조회 가능</td>
</tr>
<tr>
<td style="text-align: left;">presmptPrceBgn</td>
<td style="text-align: left;">추정가격시작</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">검색하고자하는 추정가격범위시작금액이상(원화,원) (외자 업무의 경우 해당 컬럼 검색 불가)</td>
</tr>
<tr>
<td style="text-align: left;">presmptPrceEnd</td>
<td style="text-align: left;">추정가격종료</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">검색하고자하는 추정가격범위종료금액이하(원화,원) (외자 업무의 경우 해당 컬럼 검색 불가)</td>
</tr>
<tr>
<td style="text-align: left;">dtilPrdctClsfcNo</td>
<td style="text-align: left;">세부품명번호</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">4111540601</td>
<td style="text-align: left;">검색하고자하는 세부품명번호</td>
</tr>
<tr>
<td style="text-align: left;">masYn</td>
<td style="text-align: left;">다수공급경쟁자여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">검색하고자하는 다수공급경쟁자여부</td>
</tr>
<tr>
<td style="text-align: left;">prcrmntReqNo</td>
<td style="text-align: left;">조달요청번호</td>
<td style="text-align: left;">17</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25DC00068938</td>
<td style="text-align: left;">검색하고자하는 조달요청번호</td>
</tr>
<tr>
<td style="text-align: left;">bidClseExcpYn</td>
<td style="text-align: left;">입찰마감제외여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">검색하고자하는 입찰마감제외여부</td>
</tr>
<tr>
<td style="text-align: left;">intrntnlDivCd</td>
<td style="text-align: left;">국제구분코드</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">검색하고자하는 국제구분코드<br />
국내:1, 국제:2<br />
국내/시설 입찰 공고일 경우 : 1<br />
국외 입찰 공고일 경우 : 2</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 응답 메시지 명세

<table>
<colgroup>
<col style="width: 20%" />
<col style="width: 18%" />
<col style="width: 14%" />
<col style="width: 11%" />
<col style="width: 14%" />
<col style="width: 19%" />
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
<td style="text-align: left;">resultCode</td>
<td style="text-align: left;">결과코드</td>
<td style="text-align: left;">2</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">00</td>
<td style="text-align: left;">결과코드</td>
</tr>
<tr>
<td style="text-align: left;">resultMsg</td>
<td style="text-align: left;">결과메세지</td>
<td style="text-align: left;">50</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">정상.</td>
<td style="text-align: left;">결과메세지</td>
</tr>
<tr>
<td style="text-align: left;">numOfRows</td>
<td style="text-align: left;">한 페이지 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td style="text-align: left;">pageNo</td>
<td style="text-align: left;">페이지 번호</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">페이지 수</td>
</tr>
<tr>
<td style="text-align: left;">totalCount</td>
<td style="text-align: left;">데이터 총 개수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">17</td>
<td style="text-align: left;">데이터 총개수</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNo</td>
<td style="text-align: left;">입찰공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">R25BK00935313</td>
<td style="text-align: left;"><p>입찰공고 관리번입찰공고 관리번호이며 조달청나라장터 공고건의 형식은 년도(4)+월(2)+순번(5)이며 자체전자조달시스템 보유기관은 각 기관별 형식 별도 사용</p>
<p>*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성</p>
<p>-단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</p></td>
</tr>
<tr>
<td style="text-align: left;">bidNtceOrd</td>
<td style="text-align: left;">입찰공고차수</td>
<td style="text-align: left;">3</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">000</td>
<td style="text-align: left;">입찰공고차수는 해당 입찰공고에 대한 재공고 및 재입찰 등이 발생되었을 경우 증가되는 수</td>
</tr>
<tr>
<td style="text-align: left;">reNtceYn</td>
<td style="text-align: left;">재공고여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">Y</td>
<td style="text-align: left;">본 입찰공고의 재공고 여부(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">rgstTyNm</td>
<td style="text-align: left;">등록유형명</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">조달청 또는 나라장터 자체 공고건</td>
<td style="text-align: left;">입찰공고가 "조달청 또는 나라장터 자체 공고건","'나라장터 기타 공고건"</td>
</tr>
<tr>
<td style="text-align: left;">ntceKindNm</td>
<td style="text-align: left;">공고종류명</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">등록공고</td>
<td style="text-align: left;">공고의 공고상태명으로 등록공고, 변경공고, 취소공고, 재공고 구분</td>
</tr>
<tr>
<td style="text-align: left;">intrbidYn</td>
<td style="text-align: left;">국제입찰여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">Y</td>
<td style="text-align: left;">국제입찰대상인지의 여부를 나타내며 국제입찰 대상은 내외국인 또는 외국인을 대상으로 하여 물품, 공사 및 용역을 조달하기 위하여 행하는 입찰을 말하며 수의계약을 포함한다. 국가계약법 제4조에 의해 추정가격이 고시금액(국제입찰 적용 대상 기준금액으로 기획재정부장관 및 행정자치부장관이 매 2년마다 고시한 금액을 말하며 WTO 또는 양자간(FTA) 정부조달협정에 따르면 국제입찰 대상 기준 금액이 SDR(Special Drawing Rights:특별인출권) 통화단위로 되어 있어 주무부 장관이 이를 2년마다 원화로 환산하여 고시) 이상일 경우 국제입찰대상이 됨(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceDt</td>
<td style="text-align: left;">입찰공고일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">2025-07-01 14:38:38</td>
<td style="text-align: left;">입찰공고서를 공고한 일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">refNo</td>
<td style="text-align: left;">참조번호</td>
<td style="text-align: left;">105</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25DC00068938</td>
<td style="text-align: left;">조달청 입찰공고의 경우 참조공고번호는 자체 전자조달시스템에서 관리하는 공고번호를 의미하며 자체전자조달시스템의 경우 참조공고번호는 나라장터(G2B) 입찰공고번호를 의미함</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNm</td>
<td style="text-align: left;">입찰공고명</td>
<td style="text-align: left;">1000</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">라만 분광기</td>
<td style="text-align: left;">공사명 또는 사업명이라고도 하며 입찰공고 내용을 요약한 이름</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttCd</td>
<td style="text-align: left;">공고기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">1230000</td>
<td style="text-align: left;">공고를 하는 기관의 코드로 행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드가 행자부코드가 없는 경우 조달청에서 부여한 공고기관 코드가 표기됨</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttNm</td>
<td style="text-align: left;">공고기관명</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">조달청</td>
<td style="text-align: left;">수요기관의 의뢰를 받아 공고하는 기관의 명</td>
</tr>
<tr>
<td style="text-align: left;">dminsttCd</td>
<td style="text-align: left;">수요기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">B551184</td>
<td style="text-align: left;">실제 수요기관의 코드로 행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드가 행자부코드가 없는 경우 조달청에서 부여한 수요기관 코드가 표기됨</td>
</tr>
<tr>
<td style="text-align: left;">dminsttNm</td>
<td style="text-align: left;">수요기관명</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">한국에너지기술연구원</td>
<td style="text-align: left;">중앙조달인 경우 조달사업에 관한 법률 제2조(정의)에 따라 수요물자의 구매 공급 또는 시설공사 계약의 체결을 조달청장에게 요청할 수 있도록 조달청장이 인정하여 등록한 기관 또는 자체전자조달시스템을 이용하는 기관인 경우 계약을 의뢰한 기관의 명으로 공고기관과 수요기관이 동일할 수 있음</td>
</tr>
<tr>
<td style="text-align: left;">bidMethdNm</td>
<td style="text-align: left;">입찰방식명</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">전자입찰</td>
<td style="text-align: left;">공고의 입찰방식명 직찰<br />
전자입찰,전자입찰/직찰,전자/직찰/우편/상시,직찰/우편/상시,우편/상시,전자시담,복수견적(역경매),직찰/우편,전자시담(다자간)</td>
</tr>
<tr>
<td style="text-align: left;">cntrctCnclsMthdNm</td>
<td style="text-align: left;">계약체결방법명</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">일반경쟁</td>
<td style="text-align: left;">계약체결의 방법을 구분하는 명<br />
*일반경쟁계약은 계약 대상 물품의 규격 및 시방서와 계약조건 등을 널리 공고하여 일정한 자격을 가진 불특정 다수인의 입찰희망자를 모두 경쟁 입찰하는 계약방법<br />
*제한경쟁계약은 일반·지명경쟁계약제도의 단점을 보완하기 위해 실적제한, 기술보유제한, 특정물품제한, 지역제한 등을 두는 계약방법<br />
*지명경쟁계약은 계약상대자의 신용과 실적 등에 있어 적당하다고 인정하는 특정 다수의 경쟁 참가자를 지명하여 계약 상대방을 결정하는 계약방법<br />
*수의계약은 계약상대자를 결정함에 있어 경쟁방법에 의하지 않고 특정인을 선정하여 계약하는 계약방법</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttOfclNm</td>
<td style="text-align: left;">공고기관담당자명</td>
<td style="text-align: left;">35</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">이승미</td>
<td style="text-align: left;">공고기관의 공고를 담당하는 담당자의 명</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttOfclTelNo</td>
<td style="text-align: left;">공고기관담당자전화번호</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">042-724-7329</td>
<td style="text-align: left;">공고기관의 공고를 담당하는 담당자의 전화번호</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttOfclEmailAdrs</td>
<td style="text-align: left;">공고기관담당자이메일주소</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">pps007@korea.kr</td>
<td style="text-align: left;">공고기관의 공고를 담당하는 담당자의 이메일주소</td>
</tr>
<tr>
<td style="text-align: left;">exctvNm</td>
<td style="text-align: left;">집행관명</td>
<td style="text-align: left;">35</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">이승미</td>
<td style="text-align: left;">공고의 집행관명</td>
</tr>
<tr>
<td style="text-align: left;">bidQlfctRgstDt</td>
<td style="text-align: left;">입찰참가자격등록마감일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-16 18:00</td>
<td style="text-align: left;">입찰참가등록이란 입찰사무를 효과적으로 집행하기 위하여 사전에 입찰참가자격등록을 해두었다가 필요 시 입찰에 참여하는 제도로 해당 공고에 대한 입찰참가자격의 등록이 완료되어야 하는 시점을 의미함 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">cmmnSpldmdAgrmntRcptdocMethd</td>
<td style="text-align: left;">공동수급협정서접수방식</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">공고서참조</td>
<td style="text-align: left;">공동수급협정서의 접수방식"전자","수기","없음","공고서참고"</td>
</tr>
<tr>
<td style="text-align: left;">cmmnSpldmdAgrmntClseDt</td>
<td style="text-align: left;">공동수급협정마감일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-16 18:00</td>
<td style="text-align: left;">공동계약이 허용된 공고에 대해 공동수급체를 구성하여 입찰에 참여하고자 할 경우 구성원이 일정 분담내용에 따라 나누어 공동으로 이행하는 약속을 한 공동수급협정서를 작성하여야 하며 이때 공동수급협정서의 등록(작성) 마감 시점을 의미함”YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">cmmnSpldmdCorpRgnLmtYn</td>
<td style="text-align: left;">공동수급업체지역제한여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">공동수급협정시 구성원의 지역제한을 적용할지 여부. 지역제한인경우 협정 구성업체가 참가제한지역에 포함되어야 함.(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">bidBeginDt</td>
<td style="text-align: left;">입찰개시일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-03 00:00:00</td>
<td style="text-align: left;">입찰서의 제출을 개시하는 일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">bidClseDt</td>
<td style="text-align: left;">입찰마감일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-17 12:00:00</td>
<td style="text-align: left;">입찰서의 제출을 마감하는 일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">opengDt</td>
<td style="text-align: left;">개찰일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-17 13:00:00</td>
<td style="text-align: left;">집행관이 개찰을 수행할 수 있는 시작일시이며<br />
개찰일시 이후에 개찰이 가능함<br />
실제 개찰을 수행한 시간을 의미하지 않음 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl1</td>
<td style="text-align: left;">공고규격서URL1</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00935313&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=1&amp;prcmBsneSeCd=02</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl2</td>
<td style="text-align: left;">공고규격서URL2</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00935313&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=2&amp;prcmBsneSeCd=02</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl3</td>
<td style="text-align: left;">공고규격서URL3</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00935313&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=3&amp;prcmBsneSeCd=02</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl4</td>
<td style="text-align: left;">공고규격서URL4</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00935313&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=4&amp;prcmBsneSeCd=02</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl5</td>
<td style="text-align: left;">공고규격서URL5</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00935313&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=5&amp;prcmBsneSeCd=02</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl6</td>
<td style="text-align: left;">공고규격서URL6</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00935313&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=6&amp;prcmBsneSeCd=02</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl7</td>
<td style="text-align: left;">공고규격서URL7</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00935313&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=7&amp;prcmBsneSeCd=02</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl8</td>
<td style="text-align: left;">공고규격서URL8</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00935313&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=8&amp;prcmBsneSeCd=02</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl9</td>
<td style="text-align: left;">공고규격서URL9</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00935313&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=9&amp;prcmBsneSeCd=02</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl10</td>
<td style="text-align: left;">공고규격서URL10</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00935313&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=10&amp;prcmBsneSeCd=02</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm1</td>
<td style="text-align: left;">공고규격파일명1</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">구매규격서.hwp</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm2</td>
<td style="text-align: left;">공고규격파일명2</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">해외공급자_계약서_서명권한_위임장_(양식).hwp</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm3</td>
<td style="text-align: left;">공고규격파일명3</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">공급자증명서(양식).hwp</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm4</td>
<td style="text-align: left;">공고규격파일명4</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25BK00935313-000_20250701104615_외자공고서_D02.htm</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm5</td>
<td style="text-align: left;">공고규격파일명5</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25BK00935313-000_20250701104615_SUMMARY_OF_BIDDING_D03.htm</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm6</td>
<td style="text-align: left;">공고규격파일명6</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25BK00935313-000_20250701104615_SUMMARY_OF_BIDDING_D03.htm</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm7</td>
<td style="text-align: left;">공고규격파일명7</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25BK00935313-000_20250701104615_SUMMARY_OF_BIDDING_D03.htm</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm8</td>
<td style="text-align: left;">공고규격파일명8</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25BK00935313-000_20250701104615_SUMMARY_OF_BIDDING_D03.htm</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm9</td>
<td style="text-align: left;">공고규격파일명9</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25BK00935313-000_20250701104615_SUMMARY_OF_BIDDING_D03.htm</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm10</td>
<td style="text-align: left;">공고규격파일명10</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25BK00935313-000_20250701104615_SUMMARY_OF_BIDDING_D03.htm</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">rbidPermsnYn</td>
<td style="text-align: left;">재입찰허용여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">입찰이 유찰되는 경우 재공고 없이 다시 입찰(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">prdctClsfcLmtYn</td>
<td style="text-align: left;">물품분류제한여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">Y</td>
<td style="text-align: left;">물품공고의 경우 물품분류번호로 제한할 경우 Y, 물품분류번호 제한없으면 N</td>
</tr>
<tr>
<td style="text-align: left;">mnfctYn</td>
<td style="text-align: left;">제조여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">물품분류로 투찰제한시 제조물품으로 제한할 지 여부. "Y"일 경우 투찰시 업체의 경쟁입찰참가자격등록증에 공고서상 물품분류가 제조물품으로 등록되어 있어야 투찰가능(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">prearngPrceDcsnMthdNm</td>
<td style="text-align: left;">예정가격결정방법명</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">비예가</td>
<td style="text-align: left;">예정가격의 결정을 위해 복수예정가격방식으로 산정하는지 단일 예정가격으로 산정하는지를 구분하는 명</td>
</tr>
<tr>
<td style="text-align: left;">totPrdprcNum</td>
<td style="text-align: left;">총예가건수</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N/A</td>
<td style="text-align: left;">공고의 총예가건수</td>
</tr>
<tr>
<td style="text-align: left;">drwtPrdprcNum</td>
<td style="text-align: left;">추첨예가건수</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N/A</td>
<td style="text-align: left;">공고의 추첨예가건수</td>
</tr>
<tr>
<td style="text-align: left;">asignBdgtAmt</td>
<td style="text-align: left;">배정예산금액</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">사업목적물을 달성하기 위하여 배정된 예산액 또는 설계금액(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">presmptPrce</td>
<td style="text-align: left;">추정가격</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">물품/공사/용역 등의 조달 계약을 체결함에 있어 국제입찰 대상여부를 판단하는 기준 등으로 삼기 위하여 예정가격이 결정되기 전에 예산에 계상된 금액 등을 기준으로 하여 부가가치세 및 조달 수수료를 제외한 금액(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">opengPlce</td>
<td style="text-align: left;">개찰장소</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">국가종합전자조달시스템(나라장터)</td>
<td style="text-align: left;">집행관이 개찰을 하는 장소</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceDtlUrl</td>
<td style="text-align: left;">입찰공고상세URL</td>
<td style="text-align: left;">512</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/link/PNPE027_01/single/?bidPbancNo=R25BK00935313&amp;bidPbancOrd=000</td>
<td style="text-align: left;">나라장터시스템의 입찰공고 상세화면 링크</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceUrl</td>
<td style="text-align: left;">입찰공고URL</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/link/PNPE027_01/single/?bidPbancNo=R25BK00935313&amp;bidPbancOrd=000</td>
<td style="text-align: left;">해당 입찰공고를 인터넷상에서 확인할 수 있는 URL주소</td>
</tr>
<tr>
<td style="text-align: left;">bidPrtcptFeePaymntYn</td>
<td style="text-align: left;">입찰참가수수료납부여부</td>
<td style="text-align: left;">30</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">없음</td>
<td style="text-align: left;">입찰참가 의사가 있는 자가 납부하여야하는 수수료의 유무 및 납부방법을 표기하는 것으로 "전자납부, 수기 및 전자납부, 수기, 없음"으로 표기</td>
</tr>
<tr>
<td style="text-align: left;">bidPrtcptFee</td>
<td style="text-align: left;">입찰참가수수료</td>
<td style="text-align: left;">21</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">입찰에 참가하기위해 납부하는 수수료(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">bidGrntymnyPaymntYn</td>
<td style="text-align: left;">입찰보증금납부여부</td>
<td style="text-align: left;">30</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">전자납부허용</td>
<td style="text-align: left;">입찰보증금을 나라장터에서 전자로 납부가능하게 할지 여부 “전자납부허용”,”불허’으로 표기</td>
</tr>
<tr>
<td style="text-align: left;">crdtrNm</td>
<td style="text-align: left;">채권자명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">조달청장</td>
<td style="text-align: left;">입찰보증금 항목의 "보증채권자명"으로 전자입찰보증 접수시 사용</td>
</tr>
<tr>
<td style="text-align: left;">prdctSno</td>
<td style="text-align: left;">물품순번</td>
<td style="text-align: left;">6</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">공고의 물품목록순번</td>
</tr>
<tr>
<td style="text-align: left;">dtilPrdctClsfcNo</td>
<td style="text-align: left;">세부품명번호</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">4111540601</td>
<td style="text-align: left;">물품분류번호(8자리) + 물품식별번호(앞2자리) [물품목록정보의 관리 및 이용에 관한 규정 제12조]</td>
</tr>
<tr>
<td style="text-align: left;">dtilPrdctClsfcNoNm</td>
<td style="text-align: left;">세부품명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">자외-가시선분광광도계</td>
<td style="text-align: left;">세부품명번호 10자리에 대한 한글명</td>
</tr>
<tr>
<td style="text-align: left;">prdctSpecNm</td>
<td style="text-align: left;">물품규격명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">자외-가시선분광광도계</td>
<td style="text-align: left;">공고의 물품규격명</td>
</tr>
<tr>
<td style="text-align: left;">prdctQty</td>
<td style="text-align: left;">물품수량</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">공고의 물품수량</td>
</tr>
<tr>
<td style="text-align: left;">prdctUnit</td>
<td style="text-align: left;">물품단위</td>
<td style="text-align: left;">30</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">SET</td>
<td style="text-align: left;">공고의 물품단위</td>
</tr>
<tr>
<td style="text-align: left;">prdctUprc</td>
<td style="text-align: left;">물품단가</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">38090</td>
<td style="text-align: left;">공고의 물품단가</td>
</tr>
<tr>
<td style="text-align: left;">dlvrTmlmtDt</td>
<td style="text-align: left;">납품기한일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-11-02 12:14:58</td>
<td style="text-align: left;">공고의 납품기한일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">dlvrDaynum</td>
<td style="text-align: left;">납품일수</td>
<td style="text-align: left;">5</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">공고의 납품일수</td>
</tr>
<tr>
<td style="text-align: left;">dlvryCndtnNm</td>
<td style="text-align: left;">인도조건명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">FCA</td>
<td style="text-align: left;">인도 받을 장소</td>
</tr>
<tr>
<td style="text-align: left;">purchsObjPrdctList</td>
<td style="text-align: left;">구매대상물품목록</td>
<td style="text-align: left;">4000</td>
<td style="text-align: left;">0..n</td>
<td style="text-align: left;">1^4111540601^자외-가시선분광광도계]</td>
<td style="text-align: left;">공고의 구매대상물품목록으로 [입찰분류번호^세부품명번호(세부물품분류번호)^세부품명(세부물품분류명)],[입찰분류번호^세부품명번호(세부물품분류번호)^세부품명(세부물품분류명)] 제공</td>
</tr>
<tr>
<td style="text-align: left;">untyNtceNo</td>
<td style="text-align: left;">통합공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25BM00301112</td>
<td style="text-align: left;">입찰공고를 구분하는 번호로 입찰공고번호이며 형식은 년도(4)+월(2)+순번(5)<br />
*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성<br />
- 단계구분: BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격), BK(통합입찰)</td>
</tr>
<tr>
<td style="text-align: left;">cmmnSpldmdMethdCd</td>
<td style="text-align: left;">공동수급방식코드</td>
<td style="text-align: left;">15</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">공500012</td>
<td style="text-align: left;">공동수급이라 함은 구성원을 2인 이상으로 하여 수급인이 해당계약을 공동으로 수행하기 위하여 잠정적으로 결성한 실체를 의미하며 공동수급체가도급을 받아 이행하는 방식을 구분하는 코드로<br />
공500001 : 공동이행<br />
공500002 : 분담이행<br />
공500003 : 주계약자관리방식<br />
공500004 : 단독계약<br />
공500005 : 혼합방식<br />
공500006 : 공동이행 또는 분담이행<br />
공500007 : 혼합_단독<br />
공500008 : 혼합_공동<br />
공500012 : 해당없음으로 구분됨</td>
</tr>
<tr>
<td style="text-align: left;">cmmnSpldmdMethdNm</td>
<td style="text-align: left;">공동수급방식명</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">()공동수급불허</td>
<td style="text-align: left;">공동수급이라 함은 구성원을 2인 이상으로 하여 수급인이 해당계약을 공동으로 수행하기 위하여 잠정적으로 결성한 실체를 의미하며 공동수급체가도급을 받아 이행하는 방식을 구분하는 명임</td>
</tr>
<tr>
<td style="text-align: left;">stdNtceDocUrl</td>
<td style="text-align: left;">표준공고서URL</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00935313&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=4&amp;prcmBsneSeCd=02</td>
<td style="text-align: left;">공고의 표준공고문URL</td>
</tr>
<tr>
<td style="text-align: left;">brffcBidprcPermsnYn</td>
<td style="text-align: left;">지사투찰허용여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">지역제한 공고에 한해서 지사 투찰을 허용할지 여부. 투찰제어시 사용(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">dsgntCmptYn</td>
<td style="text-align: left;">지명경쟁여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">공고의 지명경쟁여부(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">rsrvtnPrceReMkngMthdNm</td>
<td style="text-align: left;">예비가격재작성방법명</td>
<td style="text-align: left;">50</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">재입찰시 기존 예비가격을 사용하여 예정가격이 산정됩니다.</td>
<td style="text-align: left;">공고의 예비가격재작성방법명</td>
</tr>
<tr>
<td style="text-align: left;">arsltApplDocRcptMthdNm</td>
<td style="text-align: left;">실적신청서접수방법명</td>
<td style="text-align: left;">50</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">전자문서</td>
<td style="text-align: left;">공고의 실적신청서접수방법명</td>
</tr>
<tr>
<td style="text-align: left;">arsltApplDocRcptDt</td>
<td style="text-align: left;">실적신청서접수일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-01 14:38:38</td>
<td style="text-align: left;">실적심사신청서 접수마감일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">orderPlanUntyNo</td>
<td style="text-align: left;">발주계획통합번호</td>
<td style="text-align: left;">35</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25DD20281306</td>
<td style="text-align: left;">*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성<br />
- 단계구분: BK(입찰)<br />
TA(계약)<br />
DD:(발주계획)<br />
BD(사전규격),<br />
BK(통합입찰)</td>
</tr>
<tr>
<td style="text-align: left;">sucsfbidLwltRate</td>
<td style="text-align: left;">낙찰하한율</td>
<td style="text-align: left;">22</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">개찰시 사용하는 낙찰하한율(%)</td>
</tr>
<tr>
<td style="text-align: left;">rgstDt</td>
<td style="text-align: left;">등록일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">2025-07-01 14:38:38</td>
<td style="text-align: left;">공고의 등록일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">bfSpecRgstNo</td>
<td style="text-align: left;">사전규격등록번호</td>
<td style="text-align: left;">17</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25BD00084751</td>
<td style="text-align: left;"><p>*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성</p>
<p>- 단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</p></td>
</tr>
<tr>
<td style="text-align: left;">sucsfbidMthdCd</td>
<td style="text-align: left;">낙찰방법코드</td>
<td style="text-align: left;">9</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">낙030018</td>
<td style="text-align: left;">낙찰방법명에 대한 코드 (한글 1자리 + 숫자 6자리)</td>
</tr>
<tr>
<td style="text-align: left;">sucsfbidMthdNm</td>
<td style="text-align: left;">낙찰방법명</td>
<td style="text-align: left;">700</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">규격적합자중 최저가</td>
<td style="text-align: left;">낙찰자를 결정하는 방법-낙찰방법 세부기준</td>
</tr>
<tr>
<td style="text-align: left;">chgDt</td>
<td style="text-align: left;">변경일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">2025-07-01 14:38:38</td>
<td style="text-align: left;">공고의 변경일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">dminsttOfclEmailAdrs</td>
<td style="text-align: left;">수요기관담당자이메일주소</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">nskk22@kywa.or.kr</td>
<td style="text-align: left;">수요기관 담당자의 이메일주소</td>
</tr>
<tr>
<td style="text-align: left;">indstrytyLmtYn</td>
<td style="text-align: left;">업종제한여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">해당 공고 입찰 시 업종(면허)제한을 두는지의 여부<br />
예시)Y</td>
</tr>
<tr>
<td style="text-align: left;">chgNtceRsn</td>
<td style="text-align: left;">변경공고사유</td>
<td style="text-align: left;">4000</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">원화금액 수정</td>
<td style="text-align: left;"><p>공고종류명(공고의 공고상태명) 이 변경일 경우 변경공고사유 , 취소일 경우 취소공고사유</p>
<p>(연계공고건는 제외)</p></td>
</tr>
<tr>
<td style="text-align: left;">rbidOpengDt</td>
<td style="text-align: left;">재입찰개찰일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-17 13:00:00</td>
<td style="text-align: left;">공고종류명이 ‘재입찰’ 일 경우 재입찰공고의 개찰을 수행할 수 있는 시작일시<br />
“YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">bidWgrnteeRcptClseDt</td>
<td style="text-align: left;">입찰보증서접수마감일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-08-11 10:00:00</td>
<td style="text-align: left;">입찰보증서접수마감일시</td>
</tr>
<tr>
<td style="text-align: left;">techAbltEvlRt</td>
<td style="text-align: left;">기술능력평가비율</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">80</td>
<td style="text-align: left;">협상에 의한 낙찰자 결정의 경우 기술능력 평가 비율</td>
</tr>
<tr>
<td style="text-align: left;">bidPrceEvlRt</td>
<td style="text-align: left;">입찰가격평가비율</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">협상에 의한 낙찰자 결정의 경우 기술능력 입찰가격 평가 비율</td>
</tr>
<tr>
<td style="text-align: left;">sucsfbidMthdAppStd</td>
<td style="text-align: left;">낙찰방법적용기준</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">조달청 시설공사 적격심사세부기준</td>
<td style="text-align: left;"><p>낙찰자를 결정하</p>
<p>방법 적용기준</p></td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 요청 / 응답 메시지 예제

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr>
<td style="text-align: center;"><strong>REST(URI)</strong></td>
</tr>
<tr>
<td style="text-align: center;">http://apis.data.go.kr/1230000/ad/BidPublicInfoService/ getBidPblancListInfoFrgcptPPSSrch?type=xml&amp;inqryDiv=1&amp;inqryBgnDt=202507010000&amp;inqryEndDt=202507012359&amp;numOfRows=10&amp;pageNo=1&amp;bidNtceNm=라만 분광기&amp;ServiceKey=인증키</td>
</tr>
<tr>
<td style="text-align: center;"><strong>응답 메시지</strong></td>
</tr>
<tr>
<td style="text-align: left;"><p>&lt;response&gt;</p>
<p>&lt;header&gt;</p>
<p>&lt;resultCode&gt;00&lt;/resultCode&gt;</p>
<p>&lt;resultMsg&gt;정상&lt;/resultMsg&gt;</p>
<p>&lt;/header&gt;</p>
<p>&lt;body&gt;</p>
<p>&lt;items&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00935313&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;reNtceYn&gt;N&lt;/reNtceYn&gt;</p>
<p>&lt;rgstTyNm&gt;조달청 또는 나라장터 자체 공고건&lt;/rgstTyNm&gt;</p>
<p>&lt;ntceKindNm&gt;등록공고&lt;/ntceKindNm&gt;</p>
<p>&lt;intrbidYn&gt;Y&lt;/intrbidYn&gt;</p>
<p>&lt;bidNtceDt&gt;2025-07-01 14:38:38&lt;/bidNtceDt&gt;</p>
<p>&lt;refNo&gt;R25DC00068938&lt;/refNo&gt;</p>
<p>&lt;bidNtceNm&gt;라만 분광기&lt;/bidNtceNm&gt;</p>
<p>&lt;ntceInsttCd&gt;1230000&lt;/ntceInsttCd&gt;</p>
<p>&lt;ntceInsttNm&gt;조달청&lt;/ntceInsttNm&gt;</p>
<p>&lt;dminsttCd&gt;B551184&lt;/dminsttCd&gt;</p>
<p>&lt;dminsttNm&gt;한국에너지기술연구원&lt;/dminsttNm&gt;</p>
<p>&lt;bidMethdNm&gt;전자입찰&lt;/bidMethdNm&gt;</p>
<p>&lt;cntrctCnclsMthdNm&gt;일반경쟁&lt;/cntrctCnclsMthdNm&gt;</p>
<p>&lt;ntceInsttOfclNm&gt;이승미&lt;/ntceInsttOfclNm&gt;</p>
<p>&lt;ntceInsttOfclTelNo&gt;042-724-7329&lt;/ntceInsttOfclTelNo&gt;</p>
<p>&lt;ntceInsttOfclEmailAdrs&gt;pps007@korea.kr&lt;/ntceInsttOfclEmailAdrs&gt;</p>
<p>&lt;exctvNm&gt;이승미&lt;/exctvNm&gt;</p>
<p>&lt;bidQlfctRgstDt&gt;2025-07-16 18:00&lt;/bidQlfctRgstDt&gt;</p>
<p>&lt;cmmnSpldmdAgrmntRcptdocMethd&gt;공고서참고&lt;/cmmnSpldmdAgrmntRcptdocMethd&gt;</p>
<p>&lt;cmmnSpldmdAgrmntClseDt&gt;&lt;/cmmnSpldmdAgrmntClseDt&gt;</p>
<p>&lt;cmmnSpldmdCorpRgnLmtYn&gt;&lt;/cmmnSpldmdCorpRgnLmtYn&gt;</p>
<p>&lt;bidBeginDt&gt;2025-07-03 00:00:00&lt;/bidBeginDt&gt;</p>
<p>&lt;bidClseDt&gt;2025-07-17 12:00:00&lt;/bidClseDt&gt;</p>
<p>&lt;opengDt&gt;2025-07-17 13:00:00&lt;/opengDt&gt;</p>
<p>&lt;ntceSpecDocUrl1&gt;https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00935313&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=1&amp;prcmBsneSeCd=02&lt;/ntceSpecDocUrl1&gt;</p>
<p>&lt;ntceSpecDocUrl2&gt;https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00935313&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=2&amp;prcmBsneSeCd=02&lt;/ntceSpecDocUrl2&gt;</p>
<p>&lt;ntceSpecDocUrl3&gt;https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00935313&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=3&amp;prcmBsneSeCd=02&lt;/ntceSpecDocUrl3&gt;</p>
<p>&lt;ntceSpecDocUrl4&gt;https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00935313&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=4&amp;prcmBsneSeCd=02&lt;/ntceSpecDocUrl4&gt;</p>
<p>&lt;ntceSpecDocUrl5&gt;https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00935313&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=5&amp;prcmBsneSeCd=02&lt;/ntceSpecDocUrl5&gt;</p>
<p>&lt;ntceSpecDocUrl6&gt;&lt;/ntceSpecDocUrl6&gt;</p>
<p>&lt;ntceSpecDocUrl7&gt;&lt;/ntceSpecDocUrl7&gt;</p>
<p>&lt;ntceSpecDocUrl8&gt;&lt;/ntceSpecDocUrl8&gt;</p>
<p>&lt;ntceSpecDocUrl9&gt;&lt;/ntceSpecDocUrl9&gt;</p>
<p>&lt;ntceSpecDocUrl10&gt;&lt;/ntceSpecDocUrl10&gt;</p>
<p>&lt;ntceSpecFileNm1&gt;구매규격서.hwp&lt;/ntceSpecFileNm1&gt;</p>
<p>&lt;ntceSpecFileNm2&gt;해외공급자_계약서_서명권한_위임장_(양식).hwp&lt;/ntceSpecFileNm2&gt;</p>
<p>&lt;ntceSpecFileNm3&gt;공급자증명서(양식).hwp&lt;/ntceSpecFileNm3&gt;</p>
<p>&lt;ntceSpecFileNm4&gt;R25BK00935313-000_20250701104615_외자공고서_D02.htm&lt;/ntceSpecFileNm4&gt;</p>
<p>&lt;ntceSpecFileNm5&gt;R25BK00935313-000_20250701104615_SUMMARY_OF_BIDDING_D03.htm&lt;/ntceSpecFileNm5&gt;</p>
<p>&lt;ntceSpecFileNm6&gt;&lt;/ntceSpecFileNm6&gt;</p>
<p>&lt;ntceSpecFileNm7&gt;&lt;/ntceSpecFileNm7&gt;</p>
<p>&lt;ntceSpecFileNm8&gt;&lt;/ntceSpecFileNm8&gt;</p>
<p>&lt;ntceSpecFileNm9&gt;&lt;/ntceSpecFileNm9&gt;</p>
<p>&lt;ntceSpecFileNm10&gt;&lt;/ntceSpecFileNm10&gt;</p>
<p>&lt;rbidPermsnYn&gt;N&lt;/rbidPermsnYn&gt;</p>
<p>&lt;prdctClsfcLmtYn&gt;Y&lt;/prdctClsfcLmtYn&gt;</p>
<p>&lt;mnfctYn&gt;&lt;/mnfctYn&gt;</p>
<p>&lt;prearngPrceDcsnMthdNm&gt;비예가&lt;/prearngPrceDcsnMthdNm&gt;</p>
<p>&lt;totPrdprcNum&gt;&lt;/totPrdprcNum&gt;</p>
<p>&lt;drwtPrdprcNum&gt;&lt;/drwtPrdprcNum&gt;</p>
<p>&lt;asignBdgtAmt&gt;&lt;/asignBdgtAmt&gt;</p>
<p>&lt;presmptPrce&gt;0&lt;/presmptPrce&gt;</p>
<p>&lt;opengPlce&gt;국가종합전자조달시스템(나라장터)&lt;/opengPlce&gt;</p>
<p>&lt;bidNtceDtlUrl&gt;https://www.g2b.go.kr/link/PNPE027_01/single/?bidPbancNo=R25BK00935313&amp;bidPbancOrd=000&lt;/bidNtceDtlUrl&gt;</p>
<p>&lt;bidNtceUrl&gt;https://www.g2b.go.kr/link/PNPE027_01/single/?bidPbancNo=R25BK00935313&amp;bidPbancOrd=000&lt;/bidNtceUrl&gt;</p>
<p>&lt;bidPrtcptFeePaymntYn&gt;&lt;/bidPrtcptFeePaymntYn&gt;</p>
<p>&lt;bidPrtcptFee&gt;&lt;/bidPrtcptFee&gt;</p>
<p>&lt;bidGrntymnyPaymntYn&gt;전자납부허용&lt;/bidGrntymnyPaymntYn&gt;</p>
<p>&lt;crdtrNm&gt;조달청장&lt;/crdtrNm&gt;</p>
<p>&lt;prdctSno&gt;1&lt;/prdctSno&gt;</p>
<p>&lt;dtilPrdctClsfcNo&gt;4111540601&lt;/dtilPrdctClsfcNo&gt;</p>
<p>&lt;dtilPrdctClsfcNoNm&gt;자외-가시선분광광도계&lt;/dtilPrdctClsfcNoNm&gt;</p>
<p>&lt;prdctSpecNm&gt;&lt;/prdctSpecNm&gt;</p>
<p>&lt;prdctQty&gt;1&lt;/prdctQty&gt;</p>
<p>&lt;prdctUnit&gt;SET&lt;/prdctUnit&gt;</p>
<p>&lt;prdctUprc&gt;0&lt;/prdctUprc&gt;</p>
<p>&lt;dlvrTmlmtDt&gt;&lt;/dlvrTmlmtDt&gt;</p>
<p>&lt;dlvrDaynum&gt;0&lt;/dlvrDaynum&gt;</p>
<p>&lt;dlvryCndtnNm&gt;&lt;/dlvryCndtnNm&gt;</p>
<p>&lt;purchsObjPrdctList&gt;[1^4111540601^자외-가시선분광광도계]&lt;/purchsObjPrdctList&gt;</p>
<p>&lt;untyNtceNo&gt;R25BM00301112&lt;/untyNtceNo&gt;</p>
<p>&lt;cmmnSpldmdMethdCd&gt;&lt;/cmmnSpldmdMethdCd&gt;</p>
<p>&lt;cmmnSpldmdMethdNm&gt;()공동수급불허&lt;/cmmnSpldmdMethdNm&gt;</p>
<p>&lt;stdNtceDocUrl&gt;https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00935313&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=4&amp;prcmBsneSeCd=02&lt;/stdNtceDocUrl&gt;</p>
<p>&lt;brffcBidprcPermsnYn&gt;&lt;/brffcBidprcPermsnYn&gt;</p>
<p>&lt;dsgntCmptYn&gt;N&lt;/dsgntCmptYn&gt;</p>
<p>&lt;rsrvtnPrceReMkngMthdNm&gt;&lt;/rsrvtnPrceReMkngMthdNm&gt;</p>
<p>&lt;arsltApplDocRcptMthdNm&gt;&lt;/arsltApplDocRcptMthdNm&gt;</p>
<p>&lt;arsltApplDocRcptDt&gt;&lt;/arsltApplDocRcptDt&gt;</p>
<p>&lt;orderPlanUntyNo&gt;R25DD20281306&lt;/orderPlanUntyNo&gt;</p>
<p>&lt;sucsfbidLwltRate&gt;&lt;/sucsfbidLwltRate&gt;</p>
<p>&lt;rgstDt&gt;2025-07-01 14:38:38&lt;/rgstDt&gt;</p>
<p>&lt;bfSpecRgstNo&gt;R25BD00084751&lt;/bfSpecRgstNo&gt;</p>
<p>&lt;sucsfbidMthdCd&gt;낙030018&lt;/sucsfbidMthdCd&gt;</p>
<p>&lt;sucsfbidMthdNm&gt;규격적합자중 최저가&lt;/sucsfbidMthdNm&gt;</p>
<p>&lt;chgDt&gt;&lt;/chgDt&gt;</p>
<p>&lt;dminsttOfclEmailAdrs&gt;&lt;/dminsttOfclEmailAdrs&gt;</p>
<p>&lt;indstrytyLmtYn&gt;&lt;/indstrytyLmtYn&gt;</p>
<p>&lt;chgNtceRsn&gt;&lt;/chgNtceRsn&gt;</p>
<p>&lt;rbidOpengDt&gt;2025-07-17 13:00:00&lt;/rbidOpengDt&gt;</p>
<p>&lt;bidWgrnteeRcptClseDt&gt;&lt;/bidWgrnteeRcptClseDt&gt;</p>
<p>&lt;techAbltEvlRt&gt;&lt;/techAbltEvlRt&gt;</p>
<p>&lt;bidPrceEvlRt&gt;&lt;/bidPrceEvlRt&gt;</p>
<p>&lt;sucsfbidMthdAppStd&gt;&lt;/sucsfbidMthdAppStd&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;/items&gt;</p>
<p>&lt;numOfRows&gt;10&lt;/numOfRows&gt;</p>
<p>&lt;pageNo&gt;1&lt;/pageNo&gt;</p>
<p>&lt;totalCount&gt;1&lt;/totalCount&gt;</p>
<p>&lt;/body&gt;</p>
<p>&lt;/response&gt;</p></td>
</tr>
</tbody>
</table>

#### \
\[나라장터검색조건에 의한 입찰공고물품조회\] 오퍼레이션 명세

<table>
<colgroup>
<col style="width: 4%" />
<col style="width: 21%" />
<col style="width: 17%" />
<col style="width: 21%" />
<col style="width: 2%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr>
<td rowspan="6">오퍼레이션 정보</td>
<td>오퍼레이션 번호</td>
<td>14</td>
<td>오퍼레이션명(국문)</td>
<td colspan="2">나라장터검색조건에 의한 입찰공고물품조회</td>
</tr>
<tr>
<td>오퍼레이션 유형</td>
<td>조회(목록)</td>
<td>오퍼레이션명(영문)</td>
<td colspan="2">getBidPblancListInfoThngPPSSrch</td>
</tr>
<tr>
<td>오퍼레이션 설명</td>
<td colspan="4">검색조건에 공고게시일시, 개찰일시 범위, 공고기관, 수요기관, 참조번호 등을 입력하여 나라장터의 입찰공고번호, 공고명, 발주기관, 수요기관, 계약체결방법명 등 물품부분의 입찰공고정보를 조회함</td>
</tr>
<tr>
<td>Call Back URL</td>
<td colspan="4">N/A</td>
</tr>
<tr>
<td>최대 메시지 사이즈</td>
<td colspan="4">[ 4000bytes]</td>
</tr>
<tr>
<td>평균 응답 시간</td>
<td>[ 500 ms]</td>
<td colspan="2">초당 최대 트랜잭션</td>
<td>[ 30 tps]</td>
</tr>
</tbody>
</table>

##### 요청 메시지 명세

<table>
<colgroup>
<col style="width: 19%" />
<col style="width: 19%" />
<col style="width: 13%" />
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 21%" />
</colgroup>
<tbody>
<tr>
<td>항목명(영문)</td>
<td>항목명(국문)</td>
<td>항목크기</td>
<td>항목구분</td>
<td>샘플데이터</td>
<td>항목설명</td>
</tr>
<tr>
<td style="text-align: left;">numOfRows</td>
<td style="text-align: left;">한 페이지 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td style="text-align: left;">pageNo</td>
<td style="text-align: left;">페이지 번호</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">페이지 번호</td>
</tr>
<tr>
<td style="text-align: left;">ServiceKey</td>
<td style="text-align: left;">서비스키</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">공공데이터포탈에서 받은 인증키</td>
<td style="text-align: left;">공공데이터포탈에서 받은 인증키</td>
</tr>
<tr>
<td style="text-align: left;">type</td>
<td style="text-align: left;">타입</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">0</td>
<td>json</td>
<td style="text-align: left;">오픈API 리턴 타입을 JSON으로 받고 싶을 경우 'json' 으로 지정</td>
</tr>
<tr>
<td style="text-align: left;">inqryDiv</td>
<td style="text-align: left;">조회구분</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">검색하고자하는 조회구분<br />
1:공고게시일시, 2:개찰일시<br />
1. 공고게시일시 : 공고일자(pblancDate)<br />
2. 개찰일시 : 개찰일시(opengDt)</td>
</tr>
<tr>
<td style="text-align: left;">inqryBgnDt</td>
<td style="text-align: left;">조회시작일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">202507010000</td>
<td style="text-align: left;">검색하고자 하는 조회시작일시"YYYYMMDDHHMM"<br />
조회구분이 '1'인 경우 공고게시일시 필수, '2'인 경우 개찰일시 필수</td>
</tr>
<tr>
<td style="text-align: left;">inqryEndDt</td>
<td style="text-align: left;">조회종료일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">202507012359</td>
<td style="text-align: left;">검색하고자 하는 조회종료일시"YYYYMMDDHHMM"<br />
조회구분이 '1'인 경우 공고게시일시 필수, '2'인 경우 개찰일시 필수</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNm</td>
<td style="text-align: left;">입찰공고명</td>
<td style="text-align: left;">1000</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">모션캡쳐시스템 업그레이드</td>
<td style="text-align: left;">검색하고자하는 공고명<br />
※ 공고명 일부 입력시에도 조회 가능</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttCd</td>
<td style="text-align: left;">공고기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">Z001351</td>
<td style="text-align: left;">검색하고자하는 공고기관코드</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttNm</td>
<td style="text-align: left;">공고기관명</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">재단법인부산테크노파크</td>
<td style="text-align: left;">검색하고자하는 공고기관명<br />
※ 공고기관명 일부 입력시에도 조회 가능</td>
</tr>
<tr>
<td style="text-align: left;">dminsttCd</td>
<td style="text-align: left;">수요기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">Z001351</td>
<td style="text-align: left;"><p>검색하고자하는 수요기관코드</p>
<p>행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드 입력</p>
<p>행자부코드가 없는 경우 조달청에서 부여한 수요기관 코드 입력</p></td>
</tr>
<tr>
<td style="text-align: left;">dminsttNm</td>
<td style="text-align: left;">수요기관명</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">각 재단법인부산테크노파크</td>
<td style="text-align: left;">검색하고자하는 수요기관명<br />
※ 수요기관명 일부 입력시에도 조회 가능</td>
</tr>
<tr>
<td style="text-align: left;">refNo</td>
<td style="text-align: left;">참조번호</td>
<td style="text-align: left;">105</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">물품25-49</td>
<td style="text-align: left;">검색하고자하는 참조번호</td>
</tr>
<tr>
<td style="text-align: left;">prtcptLmtRgnCd</td>
<td style="text-align: left;">참가제한지역코드</td>
<td style="text-align: left;">2</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">00</td>
<td style="text-align: left;">검색하고자하는 참가제한지역코드<br />
11 : 서울특별시<br />
26 : 부산광역시<br />
27 : 대구광역시<br />
28 : 인천광역시<br />
29 : 광주광역시<br />
30 : 대전광역시<br />
31 : 울산광역시<br />
36 : 세종특별자치시<br />
41 : 경기도<br />
42 : 강원도<br />
43 : 충청북도<br />
44 : 충청남도<br />
45 : 전라북도<br />
46 : 전라남도<br />
47 : 경상북도<br />
48 : 경상남도<br />
50 : 제주도<br />
51 : 강원특별자치도<br />
52 : 전북특별자치도<br />
99 : 기타<br />
00: 전국<br />
*전국 : 지역제한을 설정하지 않은 공고</td>
</tr>
<tr>
<td style="text-align: left;">prtcptLmtRgnNm</td>
<td style="text-align: left;">참가제한지역명</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">전국</td>
<td style="text-align: left;">검색하고자하는 참가제한지역명<br />
※ 참가제한지역명 일부 입력시에도 조회 가능<br />
*전국 : 지역제한을 설정하지 않은 공고</td>
</tr>
<tr>
<td style="text-align: left;">indstrytyCd</td>
<td style="text-align: left;">업종코드</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0003</td>
<td style="text-align: left;">검색하고자하는 업종코드</td>
</tr>
<tr>
<td style="text-align: left;">indstrytyNm</td>
<td style="text-align: left;">업종명</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">토목공사업</td>
<td style="text-align: left;">검색하고자하는 업종명<br />
※ 업종명 일부 입력시에도 조회 가능</td>
</tr>
<tr>
<td style="text-align: left;">presmptPrceBgn</td>
<td style="text-align: left;">추정가격시작</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">81818100</td>
<td style="text-align: left;">검색하고자하는 추정가격범위시작금액이상(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">presmptPrceEnd</td>
<td style="text-align: left;">추정가격종료</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">81818200</td>
<td style="text-align: left;">검색하고자하는 추정가격범위종료금액이하(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">dtilPrdctClsfcNo</td>
<td style="text-align: left;">세부품명번호</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">4921181901</td>
<td style="text-align: left;">검색하고자하는 세부품명번호</td>
</tr>
<tr>
<td style="text-align: left;">masYn</td>
<td style="text-align: left;">다수공급경쟁자여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">검색하고자하는 다수공급경쟁자여부</td>
</tr>
<tr>
<td style="text-align: left;">prcrmntReqNo</td>
<td style="text-align: left;">조달요청번호</td>
<td style="text-align: left;">13</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25DC00066664</td>
<td style="text-align: left;">검색하고자하는 조달요청번호</td>
</tr>
<tr>
<td style="text-align: left;">bidClseExcpYn</td>
<td style="text-align: left;">입찰마감제외여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">검색하고자하는 입찰마감제외여부</td>
</tr>
<tr>
<td style="text-align: left;">intrntnlDivCd</td>
<td style="text-align: left;">국제구분코드</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">검색하고자하는 국제구분코드<br />
국내:1, 국제:2<br />
<br />
국내/시설 입찰 공고일 경우 : 1<br />
국외 입찰 공고일 경우 : 2</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 응답 메시지 명세

<table>
<colgroup>
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 13%" />
<col style="width: 11%" />
<col style="width: 14%" />
<col style="width: 19%" />
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
<td style="text-align: left;">resultCode</td>
<td style="text-align: left;">결과코드</td>
<td style="text-align: left;">2</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">00</td>
<td style="text-align: left;">결과코드</td>
</tr>
<tr>
<td style="text-align: left;">resultMsg</td>
<td style="text-align: left;">결과메세지</td>
<td style="text-align: left;">50</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">정상.</td>
<td style="text-align: left;">결과메세지</td>
</tr>
<tr>
<td style="text-align: left;">numOfRows</td>
<td style="text-align: left;">한 페이지 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td style="text-align: left;">pageNo</td>
<td style="text-align: left;">페이지 번호</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">페이지 수</td>
</tr>
<tr>
<td style="text-align: left;">totalCount</td>
<td style="text-align: left;">데이터 총 개수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">17</td>
<td style="text-align: left;">데이터 총개수</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNo</td>
<td style="text-align: left;">입찰공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">R25BK00934850</td>
<td style="text-align: left;"><p>입찰공고 관리번입찰공고 관리번호이며 조달청나라장터 공고건의 형식은 년도(4)+월(2)+순번(5)이며 자체전자조달시스템 보유기관은 각 기관별 형식 별도 사용</p>
<p>*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성</p>
<p>-단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</p></td>
</tr>
<tr>
<td style="text-align: left;">bidNtceOrd</td>
<td style="text-align: left;">입찰공고차수</td>
<td style="text-align: left;">3</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">000</td>
<td style="text-align: left;">입찰공고차수는 해당 입찰공고에 대한 재공고 및 재입찰 등이 발생되었을 경우 증가되는 수</td>
</tr>
<tr>
<td style="text-align: left;">reNtceYn</td>
<td style="text-align: left;">재공고여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">본 입찰공고의 재공고 여부(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">rgstTyNm</td>
<td style="text-align: left;">등록유형명</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">조달청 또는 나라장터 자체 공고건</td>
<td style="text-align: left;">입찰공고가 "조달청 또는 나라장터 자체 공고건","'나라장터 기타 공고건"</td>
</tr>
<tr>
<td style="text-align: left;">ntceKindNm</td>
<td style="text-align: left;">공고종류명</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">등록공고</td>
<td style="text-align: left;">공고의 공고상태명으로 등록공고, 변경공고, 취소공고, 재공고 구분</td>
</tr>
<tr>
<td style="text-align: left;">intrbidYn</td>
<td style="text-align: left;">국제입찰여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">국제입찰대상인지의 여부를 나타내며 국제입찰 대상은 내외국인 또는 외국인을 대상으로 하여 물품, 공사 및 용역을 조달하기 위하여 행하는 입찰을 말하며 수의계약을 포함한다. 국가계약법 제4조에 의해 추정가격이 고시금액(국제입찰 적용 대상 기준금액으로 기획재정부장관 및 행정자치부장관이 매 2년마다 고시한 금액을 말하며 WTO 또는 양자간(FTA) 정부조달협정에 따르면 국제입찰 대상 기준 금액이 SDR(Special Drawing Rights:특별인출권) 통화단위로 되어 있어 주무부 장관이 이를 2년마다 원화로 환산하여 고시) 이상일 경우 국제입찰대상이 됨(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceDt</td>
<td style="text-align: left;">입찰공고일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-01 07:54:07</td>
<td style="text-align: left;">입찰공고서를 공고한 일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">refNo</td>
<td style="text-align: left;">참조번호</td>
<td style="text-align: left;">105</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">물품25-49</td>
<td style="text-align: left;">조달청 입찰공고의 경우 참조공고번호는 자체 전자조달시스템에서 관리하는 공고번호를 의미하며 자체전자조달시스템의 경우 참조공고번호는 나라장터(G2B) 입찰공고번호를 의미함</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNm</td>
<td style="text-align: left;">입찰공고명</td>
<td style="text-align: left;">1000</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">모션캡쳐시스템 업그레이드</td>
<td style="text-align: left;">공사명 또는 사업명이라고도 하며 입찰공고 내용을 요약한 이름</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttCd</td>
<td style="text-align: left;">공고기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">Z001351</td>
<td style="text-align: left;">공고를 하는 기관의 코드로 행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드가 행자부코드가 없는 경우 조달청에서 부여한 공고기관 코드가 표기됨</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttNm</td>
<td style="text-align: left;">공고기관명</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">재단법인부산테크노파크</td>
<td style="text-align: left;">수요기관의 의뢰를 받아 공고하는 기관의 명</td>
</tr>
<tr>
<td style="text-align: left;">dminsttCd</td>
<td style="text-align: left;">수요기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">Z001351</td>
<td style="text-align: left;">실제 수요기관의 코드로 행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드가 행자부코드가 없는 경우 조달청에서 부여한 수요기관 코드가 표기됨</td>
</tr>
<tr>
<td style="text-align: left;">dminsttNm</td>
<td style="text-align: left;">수요기관명</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">재단법인부산테크노파크</td>
<td style="text-align: left;">중앙조달인 경우 조달사업에 관한 법률 제2조(정의)에 따라 수요물자의 구매 공급 또는 시설공사 계약의 체결을 조달청장에게 요청할 수 있도록 조달청장이 인정하여 등록한 기관 또는 자체전자조달시스템을 이용하는 기관인 경우 계약을 의뢰한 기관의 명으로 공고기관과 수요기관이 동일할 수 있음</td>
</tr>
<tr>
<td style="text-align: left;">bidMethdNm</td>
<td style="text-align: left;">입찰방식명</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">전자입찰</td>
<td style="text-align: left;">공고의 입찰방식명 직찰<br />
전자입찰,전자입찰/직찰,전자/직찰/우편/상시,직찰/우편/상시,우편/상시,전자시담,복수견적(역경매),직찰/우편,전자시담(다자간)</td>
</tr>
<tr>
<td style="text-align: left;">cntrctCnclsMthdNm</td>
<td style="text-align: left;">계약체결방법명</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">제한경쟁</td>
<td style="text-align: left;">계약체결의 방법을 구분하는 명<br />
*일반경쟁계약은 계약 대상 물품의 규격 및 시방서와 계약조건 등을 널리 공고하여 일정한 자격을 가진 불특정 다수인의 입찰희망자를 모두 경쟁 입찰하는 계약방법<br />
*제한경쟁계약은 일반·지명경쟁계약제도의 단점을 보완하기 위해 실적제한, 기술보유제한, 특정물품제한, 지역제한 등을 두는 계약방법<br />
*지명경쟁계약은 계약상대자의 신용과 실적 등에 있어 적당하다고 인정하는 특정 다수의 경쟁 참가자를 지명하여 계약 상대방을 결정하는 계약방법<br />
*수의계약은 계약상대자를 결정함에 있어 경쟁방법에 의하지 않고 특정인을 선정하여 계약하는 계약방법</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttOfclNm</td>
<td style="text-align: left;">공고기관담당자명</td>
<td style="text-align: left;">35</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">주혜련</td>
<td style="text-align: left;">공고기관의 공고를 담당하는 담당자의 명</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttOfclTelNo</td>
<td style="text-align: left;">공고기관담당자전화번호</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">051-974-9019</td>
<td style="text-align: left;">공고기관의 공고를 담당하는 담당자의 전화번호</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttOfclEmailAdrs</td>
<td style="text-align: left;">공고기관담당자이메일주소</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">ksinichi@btp.or.kr</td>
<td style="text-align: left;">공고기관의 공고를 담당하는 담당자의 이메일주소</td>
</tr>
<tr>
<td style="text-align: left;">exctvNm</td>
<td style="text-align: left;">집행관명</td>
<td style="text-align: left;">35</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">주혜련</td>
<td style="text-align: left;">공고의 집행관명</td>
</tr>
<tr>
<td style="text-align: left;">bidQlfctRgstDt</td>
<td style="text-align: left;">입찰참가자격등록마감일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-13 18:00</td>
<td style="text-align: left;">입찰참가등록이란 입찰사무를 효과적으로 집행하기 위하여 사전에 입찰참가자격등록을 해두었다가 필요 시 입찰에 참여하는 제도로 해당 공고에 대한 입찰참가자격의 등록이 완료되어야 하는 시점을 의미함 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">cmmnSpldmdAgrmntRcptdocMethd</td>
<td style="text-align: left;">공동수급협정서접수방식</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">없음</td>
<td style="text-align: left;">공동수급협정서의 접수방식"전자","수기","없음","공고서참고"</td>
</tr>
<tr>
<td style="text-align: left;">cmmnSpldmdAgrmntClseDt</td>
<td style="text-align: left;">공동수급협정마감일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-13 18:00</td>
<td style="text-align: left;">공동계약이 허용된 공고에 대해 공동수급체를 구성하여 입찰에 참여하고자 할 경우 구성원이 일정 분담내용에 따라 나누어 공동으로 이행하는 약속을 한 공동수급협정서를 작성하여야 하며 이때 공동수급협정서의 등록(작성) 마감 시점을 의미함”YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">cmmnSpldmdCorpRgnLmtYn</td>
<td style="text-align: left;">공동수급업체지역제한여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">공동수급협정시 구성원의 지역제한을 적용할지 여부. 지역제한인경우 협정 구성업체가 참가제한지역에 포함되어야 함.(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">bidBeginDt</td>
<td style="text-align: left;">입찰개시일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-01 10:00:00</td>
<td style="text-align: left;">입찰서의 제출을 개시하는 일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">bidClseDt</td>
<td style="text-align: left;">입찰마감일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-14 10:00:00</td>
<td style="text-align: left;">입찰서의 제출을 마감하는 일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">opengDt</td>
<td style="text-align: left;">개찰일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-14 11:00:00</td>
<td style="text-align: left;">집행관이 개찰을 수행할 수 있는 시작일시이며<br />
개찰일시 이후에 개찰이 가능함<br />
실제 개찰을 수행한 시간을 의미하지 않음 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl1</td>
<td style="text-align: left;">공고규격서URL1</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00934850&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=1&amp;prcmBsneSeCd=01</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl2</td>
<td style="text-align: left;">공고규격서URL2</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00934850&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=2&amp;prcmBsneSeCd=01</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl3</td>
<td style="text-align: left;">공고규격서URL3</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00934850&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=3&amp;prcmBsneSeCd=01</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl4</td>
<td style="text-align: left;">공고규격서URL4</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00934850&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=4&amp;prcmBsneSeCd=01</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl5</td>
<td style="text-align: left;">공고규격서URL5</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00934850&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=5&amp;prcmBsneSeCd=01</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl6</td>
<td style="text-align: left;">공고규격서URL6</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00934850&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=6&amp;prcmBsneSeCd=01</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl7</td>
<td style="text-align: left;">공고규격서URL7</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00934850&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=7&amp;prcmBsneSeCd=01</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl8</td>
<td style="text-align: left;">공고규격서URL8</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00934850&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=8&amp;prcmBsneSeCd=01</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl9</td>
<td style="text-align: left;">공고규격서URL9</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00934850&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=9&amp;prcmBsneSeCd=01</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl10</td>
<td style="text-align: left;">공고규격서URL10</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00934850&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=10&amp;prcmBsneSeCd=01</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm1</td>
<td style="text-align: left;">공고규격파일명1</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">붙임2. 입찰공고문(규가동시)_물품.hwp</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm2</td>
<td style="text-align: left;">공고규격파일명2</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">붙임3. 제안요청서.hwp</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm3</td>
<td style="text-align: left;">공고규격파일명3</td>
<td style="text-align: left;">256400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">붙임2-1. 물품규격서.hwp</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm4</td>
<td style="text-align: left;">공고규격파일명4</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">붙임2-2. 물품규격서.hwp</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm5</td>
<td style="text-align: left;">공고규격파일명5</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">붙임2-3. 물품규격서.hwp</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm6</td>
<td style="text-align: left;">공고규격파일명6</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">붙임2-4. 물품규격서.hwp</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm7</td>
<td style="text-align: left;">공고규격파일명7</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">붙임2-5. 물품규격서.hwp</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm8</td>
<td style="text-align: left;">공고규격파일명8</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">붙임2-6. 물품규격서.hwp</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm9</td>
<td style="text-align: left;">공고규격파일명9</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">붙임2-7. 물품규격서.hwp</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm10</td>
<td style="text-align: left;">공고규격파일명10</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">붙임2-8. 물품규격서.hwp</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">rbidPermsnYn</td>
<td style="text-align: left;">재입찰허용여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">Y</td>
<td style="text-align: left;">입찰이 유찰되는 경우 재공고 없이 다시 입찰(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">prdctClsfcLmtYn</td>
<td style="text-align: left;">물품분류제한여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">Y</td>
<td style="text-align: left;">물품공고의 경우 물품분류번호로 제한할 경우 Y, 물품분류번호 제한없으면 N</td>
</tr>
<tr>
<td style="text-align: left;">mnfctYn</td>
<td style="text-align: left;">제조여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">물품분류로 투찰제한시 제조물품으로 제한할 지 여부. "Y"일 경우 투찰시 업체의 경쟁입찰참가자격등록증에 공고서상 물품분류가 제조물품으로 등록되어 있어야 투찰가능(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">prearngPrceDcsnMthdNm</td>
<td style="text-align: left;">예정가격결정방법명</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">복수예가</td>
<td style="text-align: left;">예정가격의 결정을 위해 복수예정가격방식으로 산정하는지 단일 예정가격으로 산정하는지를 구분하는 명</td>
</tr>
<tr>
<td style="text-align: left;">totPrdprcNum</td>
<td style="text-align: left;">총예가건수</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">15</td>
<td style="text-align: left;">공고의 총예가건수</td>
</tr>
<tr>
<td style="text-align: left;">drwtPrdprcNum</td>
<td style="text-align: left;">추첨예가건수</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">공고의 추첨예가건수</td>
</tr>
<tr>
<td style="text-align: left;">asignBdgtAmt</td>
<td style="text-align: left;">배정예산금액</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">90000000</td>
<td style="text-align: left;">사업목적물을 달성하기 위하여 배정된 예산액 또는 설계금액(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">presmptPrce</td>
<td style="text-align: left;">추정가격</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">81818182</td>
<td style="text-align: left;">물품/공사/용역 등의 조달 계약을 체결함에 있어 국제입찰 대상여부를 판단하는 기준 등으로 삼기 위하여 예정가격이 결정되기 전에 예산에 계상된 금액 등을 기준으로 하여 부가가치세 및 조달 수수료를 제외한 금액(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">opengPlce</td>
<td style="text-align: left;">개찰장소</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">국가종합전자조달시스템(나라장터)</td>
<td style="text-align: left;">집행관이 개찰을 하는 장소</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceDtlUrl</td>
<td style="text-align: left;">입찰공고상세URL</td>
<td style="text-align: left;">512</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/link/PNPE027_01/single/?bidPbancNo=R25BK00934850&amp;bidPbancOrd=000</td>
<td style="text-align: left;">나라장터시스템의 입찰공고 상세화면 링크</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceUrl</td>
<td style="text-align: left;">입찰공고URL</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/link/PNPE027_01/single/?bidPbancNo=R25BK00934850&amp;bidPbancOrd=000&lt;</td>
<td style="text-align: left;">해당 입찰공고를 인터넷상에서 확인할 수 있는 URL주소</td>
</tr>
<tr>
<td style="text-align: left;">bidPrtcptFeePaymntYn</td>
<td style="text-align: left;">입찰참가수수료납부여부</td>
<td style="text-align: left;">30</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">업음</td>
<td style="text-align: left;">입찰참가 의사가 있는 자가 납부하여야하는 수수료의 유무 및 납부방법을 표기하는 것으로 "전자납부, 수기 및 전자납부, 수기, 없음"으로 표기</td>
</tr>
<tr>
<td style="text-align: left;">bidPrtcptFee</td>
<td style="text-align: left;">입찰참가수수료</td>
<td style="text-align: left;">21</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">입찰에 참가하기위해 납부하는 수수료(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">bidGrntymnyPaymntYn</td>
<td style="text-align: left;">입찰보증금납부여부</td>
<td style="text-align: left;">30</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">불허</td>
<td style="text-align: left;">입찰보증금을 나라장터에서 전자로 납부가능하게 할지 여부 “전자납부허용”,”불허’으로 표기</td>
</tr>
<tr>
<td style="text-align: left;">crdtrNm</td>
<td style="text-align: left;">채권자명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">원장</td>
<td style="text-align: left;">입찰보증금 항목의 "보증채권자명"으로 전자입찰보증 접수시 사용</td>
</tr>
<tr>
<td style="text-align: left;">dtilPrdctClsfcNo</td>
<td style="text-align: left;">세부품명번호</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">4921181901</td>
<td style="text-align: left;">물품분류번호(8자리) + 물품식별번호(앞2자리) [물품목록정보의 관리 및 이용에 관한 규정 제12조]</td>
</tr>
<tr>
<td style="text-align: left;">dtilPrdctClsfcNoNm</td>
<td style="text-align: left;">세부품명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">동작분석기</td>
<td style="text-align: left;">세부품명번호 10자리에 대한 한글명</td>
</tr>
<tr>
<td style="text-align: left;">prdctSpecNm</td>
<td style="text-align: left;">물품규격명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">규격서에 따름</td>
<td style="text-align: left;">공고의 물품규격명</td>
</tr>
<tr>
<td style="text-align: left;">prdctQty</td>
<td style="text-align: left;">물품수량</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">공고의 물품수량</td>
</tr>
<tr>
<td style="text-align: left;">prdctUnit</td>
<td style="text-align: left;">물품단위</td>
<td style="text-align: left;">30</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">SET</td>
<td style="text-align: left;">공고의 물품단위</td>
</tr>
<tr>
<td style="text-align: left;">prdctUprc</td>
<td style="text-align: left;">물품단가</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">90000000</td>
<td style="text-align: left;">공고의 물품단가</td>
</tr>
<tr>
<td style="text-align: left;">dlvrTmlmtDt</td>
<td style="text-align: left;">납품기한일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-12-30 00:00</td>
<td style="text-align: left;">공고의 납품기한일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">dlvrDaynum</td>
<td style="text-align: left;">납품일수</td>
<td style="text-align: left;">5</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">90</td>
<td style="text-align: left;">공고의 납품일수</td>
</tr>
<tr>
<td style="text-align: left;">dlvryCndtnNm</td>
<td style="text-align: left;">인도조건명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">납품장소차상도</td>
<td style="text-align: left;">인도 받을 장소</td>
</tr>
<tr>
<td style="text-align: left;">purchsObjPrdctList</td>
<td style="text-align: left;">구매대상물품목록</td>
<td style="text-align: left;">4000</td>
<td style="text-align: left;">0..n</td>
<td style="text-align: left;">[1^4921181901^동작분석기]</td>
<td style="text-align: left;">공고의 구매대상물품목록으로 [입찰분류번호^세부품명번호(세부물품분류번호)^세부품명(세부물품분류명)],[입찰분류번호^세부품명번호(세부물품분류번호)^세부품명(세부물품분류명)] 제공</td>
</tr>
<tr>
<td style="text-align: left;">untyNtceNo</td>
<td style="text-align: left;">통합공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25BM00300438</td>
<td style="text-align: left;">입찰공고를 구분하는 번호로 입찰공고번호이며 형식은 년도(4)+월(2)+순번(5)<br />
*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성<br />
- 단계구분: BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격), BK(통합입찰)</td>
</tr>
<tr>
<td style="text-align: left;">cmmnSpldmdMethdCd</td>
<td style="text-align: left;">공동수급방식코드</td>
<td style="text-align: left;">15</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">공500012</td>
<td style="text-align: left;">공동수급이라 함은 구성원을 2인 이상으로 하여 수급인이 해당계약을 공동으로 수행하기 위하여 잠정적으로 결성한 실체를 의미하며 공동수급체가도급을 받아 이행하는 방식을 구분하는 코드로<br />
공500001 : 공동이행<br />
공500002 : 분담이행<br />
공500003 : 주계약자관리방식<br />
공500004 : 단독계약<br />
공500005 : 혼합방식<br />
공500006 : 공동이행 또는 분담이행<br />
공500007 : 혼합_단독<br />
공500008 : 혼합_공동<br />
공500012 : 해당없음으로 구분됨</td>
</tr>
<tr>
<td style="text-align: left;">cmmnSpldmdMethdNm</td>
<td style="text-align: left;">공동수급방식명</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">(없음)공동수급불허</td>
<td style="text-align: left;">공동수급이라 함은 구성원을 2인 이상으로 하여 수급인이 해당계약을 공동으로 수행하기 위하여 잠정적으로 결성한 실체를 의미하며 공동수급체가도급을 받아 이행하는 방식을 구분하는 명임</td>
</tr>
<tr>
<td style="text-align: left;">stdNtceDocUrl</td>
<td style="text-align: left;">표준공고서URL</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00934850&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=1&amp;prcmBsneSeCd=01</td>
<td style="text-align: left;">공고의 표준공고문URL</td>
</tr>
<tr>
<td style="text-align: left;">brffcBidprcPermsnYn</td>
<td style="text-align: left;">지사투찰허용여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">지역제한 공고에 한해서 지사 투찰을 허용할지 여부. 투찰제어시 사용(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">dsgntCmptYn</td>
<td style="text-align: left;">지명경쟁여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">공고의 지명경쟁여부(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">rsrvtnPrceReMkngMthdNm</td>
<td style="text-align: left;">예비가격재작성방법명</td>
<td style="text-align: left;">50</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">재입찰시 기존 예비가격을 사용하여 예정가격이 산정됩니다.</td>
<td style="text-align: left;">공고의 예비가격재작성방법명</td>
</tr>
<tr>
<td style="text-align: left;">arsltApplDocRcptMthdNm</td>
<td style="text-align: left;">실적신청서접수방법명</td>
<td style="text-align: left;">50</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">전자문서</td>
<td style="text-align: left;">공고의 실적신청서접수방법명</td>
</tr>
<tr>
<td style="text-align: left;">arsltApplDocRcptDt</td>
<td style="text-align: left;">실적신청서접수일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-13 18:00</td>
<td style="text-align: left;">실적심사신청서 접수마감일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">orderPlanUntyNo</td>
<td style="text-align: left;">발주계획통합번호</td>
<td style="text-align: left;">35</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25DD20290101</td>
<td style="text-align: left;"><p>*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성</p>
<p>- 단계구분: BK(입찰)</p>
<p>TA(계약)</p>
<p>DD:(발주계획)</p>
<p>BD(사전규격),</p>
<p>BK(통합입찰)</p></td>
</tr>
<tr>
<td style="text-align: left;">sucsfbidLwltRate</td>
<td style="text-align: left;">낙찰하한율</td>
<td style="text-align: left;">22</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">87.745</td>
<td style="text-align: left;">개찰시 사용하는 낙찰하한율(%)</td>
</tr>
<tr>
<td style="text-align: left;">rgstDt</td>
<td style="text-align: left;">등록일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">2025-07-01 07:54:07</td>
<td style="text-align: left;">공고의 등록일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">bfSpecRgstNo</td>
<td style="text-align: left;">사전규격등록번호</td>
<td style="text-align: left;">17</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25BD00078286</td>
<td style="text-align: left;"><p>*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성</p>
<p>- 단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</p></td>
</tr>
<tr>
<td style="text-align: left;">infoBizYn</td>
<td style="text-align: left;">정보화사업여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">정보화사업여부<br />
Y/N</td>
</tr>
<tr>
<td style="text-align: left;">sucsfbidMthdCd</td>
<td style="text-align: left;">낙찰방법코드</td>
<td style="text-align: left;">9</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">낙030002</td>
<td style="text-align: left;">낙찰방법명에 대한 코드 (한글 1자리 + 숫자 6자리)</td>
</tr>
<tr>
<td style="text-align: left;">sucsfbidMthdNm</td>
<td style="text-align: left;">낙찰방법명</td>
<td style="text-align: left;">700</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">제안적격자 중 예가 내 최저가 투찰자</td>
<td style="text-align: left;">낙찰자를 결정하는 방법-낙찰방법 세부기준</td>
</tr>
<tr>
<td style="text-align: left;">chgDt</td>
<td style="text-align: left;">변경일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-01 07:54:07</td>
<td style="text-align: left;">공고의 변경일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">dminsttOfclEmailAdrs</td>
<td style="text-align: left;">수요기관담당자이메일주소</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">nskk@kywa.or.kr</td>
<td style="text-align: left;">수요기관 담당자의 이메일주소</td>
</tr>
<tr>
<td style="text-align: left;">indstrytyLmtYn</td>
<td style="text-align: left;">업종제한여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">Y</td>
<td style="text-align: left;">해당 공고 입찰 시 업종(면허)제한을 두는지의 여부<br />
예시)Y</td>
</tr>
<tr>
<td style="text-align: left;">chgNtceRsn</td>
<td style="text-align: left;">변경공고사유</td>
<td style="text-align: left;">4000</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">입찰기간 부족</td>
<td style="text-align: left;"><p>공고종류명(공고의 공고상태명) 이 변경일 경우 변경공고사유 , 취소일 경우 취소공고사유</p>
<p>(연계공고건는 제외)</p></td>
</tr>
<tr>
<td style="text-align: left;">rbidOpengDt</td>
<td style="text-align: left;">재입찰개찰일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-14 11:00:00</td>
<td style="text-align: left;">공고종류명이 ‘재입찰’ 일 경우 재입찰공고의 개찰을 수행할 수 있는 시작일시<br />
“YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">VAT</td>
<td style="text-align: left;">부가가치세</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">8181818</td>
<td style="text-align: left;">부가가치세</td>
</tr>
<tr>
<td style="text-align: left;">indutyVAT</td>
<td style="text-align: left;">주공종부가가치세</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">주공종부가가치세</td>
</tr>
<tr>
<td style="text-align: left;">bidWgrnteeRcptClseDt</td>
<td style="text-align: left;">입찰보증서접수마감일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-09-18 10:00:00</td>
<td style="text-align: left;">입찰보증서접수마감일시</td>
</tr>
<tr>
<td style="text-align: left;">rgnLmtBidLocplcJdgmBssCd</td>
<td style="text-align: left;">지역제한입찰소재지판단기준코드</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">지역제한입찰소재지판단기준코드</td>
</tr>
<tr>
<td style="text-align: left;">rgnLmtBidLocplcJdgmBssNm</td>
<td style="text-align: left;">지역제한입찰소재지판단기준명</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">본사또는참여지사소재지</td>
<td style="text-align: left;">지역제한입찰소재지판단기준명</td>
</tr>
<tr>
<td style="text-align: left;">techAbltEvlRt</td>
<td style="text-align: left;">기술능력평가비율</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">80</td>
<td style="text-align: left;">협상에 의한 낙찰자 결정의 경우 기술능력 평가 비율</td>
</tr>
<tr>
<td style="text-align: left;">bidPrceEvlRt</td>
<td style="text-align: left;">입찰가격평가비율</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">협상에 의한 낙찰자 결정의 경우 기술능력 입찰가격 평가 비율</td>
</tr>
<tr>
<td style="text-align: left;">sucsfbidMthdAppStd</td>
<td style="text-align: left;">낙찰방법적용기준</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">조달청 시설공사 적격심사세부기준</td>
<td style="text-align: left;"><p>낙찰자를 결정하</p>
<p>방법 적용기준</p></td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 요청 / 응답 메시지 예제

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr>
<td style="text-align: center;"><strong>REST(URI)</strong></td>
</tr>
<tr>
<td style="text-align: center;">http://apis.data.go.kr/1230000/ad/BidPublicInfoService/ getBidPblancListInfoThngPPSSrch?type=xml&amp;inqryDiv=1&amp;inqryBgnDt=202507010000&amp;inqryEndDt=202507012359&amp;numOfRows=10&amp;pageNo=1&amp;bidNtceNm=모션캡쳐시스템 업그레이드&amp;ServiceKey=인증키</td>
</tr>
<tr>
<td style="text-align: center;"><strong>응답 메시지</strong></td>
</tr>
<tr>
<td style="text-align: left;"><p>&lt;response&gt;</p>
<p>&lt;header&gt;</p>
<p>&lt;resultCode&gt;00&lt;/resultCode&gt;</p>
<p>&lt;resultMsg&gt;정상&lt;/resultMsg&gt;</p>
<p>&lt;/header&gt;</p>
<p>&lt;body&gt;</p>
<p>&lt;items&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00934850&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;reNtceYn&gt;N&lt;/reNtceYn&gt;</p>
<p>&lt;rgstTyNm&gt;조달청 또는 나라장터 자체 공고건&lt;/rgstTyNm&gt;</p>
<p>&lt;ntceKindNm&gt;등록공고&lt;/ntceKindNm&gt;</p>
<p>&lt;intrbidYn&gt;N&lt;/intrbidYn&gt;</p>
<p>&lt;bidNtceDt&gt;2025-07-01 07:54:07&lt;/bidNtceDt&gt;</p>
<p>&lt;refNo&gt;물품25-49&lt;/refNo&gt;</p>
<p>&lt;bidNtceNm&gt;모션캡쳐시스템 업그레이드&lt;/bidNtceNm&gt;</p>
<p>&lt;ntceInsttCd&gt;Z001351&lt;/ntceInsttCd&gt;</p>
<p>&lt;ntceInsttNm&gt;재단법인부산테크노파크&lt;/ntceInsttNm&gt;</p>
<p>&lt;dminsttCd&gt;Z001351&lt;/dminsttCd&gt;</p>
<p>&lt;dminsttNm&gt;재단법인부산테크노파크&lt;/dminsttNm&gt;</p>
<p>&lt;bidMethdNm&gt;전자입찰&lt;/bidMethdNm&gt;</p>
<p>&lt;cntrctCnclsMthdNm&gt;제한경쟁&lt;/cntrctCnclsMthdNm&gt;</p>
<p>&lt;ntceInsttOfclNm&gt;주혜련&lt;/ntceInsttOfclNm&gt;</p>
<p>&lt;ntceInsttOfclTelNo&gt;051-974-9019&lt;/ntceInsttOfclTelNo&gt;</p>
<p>&lt;ntceInsttOfclEmailAdrs&gt;ksinichi@btp.or.kr&lt;/ntceInsttOfclEmailAdrs&gt;</p>
<p>&lt;exctvNm&gt;주혜련&lt;/exctvNm&gt;</p>
<p>&lt;bidQlfctRgstDt&gt;2025-07-13 18:00&lt;/bidQlfctRgstDt&gt;</p>
<p>&lt;cmmnSpldmdAgrmntRcptdocMethd&gt;없음&lt;/cmmnSpldmdAgrmntRcptdocMethd&gt;</p>
<p>&lt;cmmnSpldmdAgrmntClseDt&gt;&lt;/cmmnSpldmdAgrmntClseDt&gt;</p>
<p>&lt;cmmnSpldmdCorpRgnLmtYn&gt;&lt;/cmmnSpldmdCorpRgnLmtYn&gt;</p>
<p>&lt;bidBeginDt&gt;2025-07-01 10:00:00&lt;/bidBeginDt&gt;</p>
<p>&lt;bidClseDt&gt;2025-07-14 10:00:00&lt;/bidClseDt&gt;</p>
<p>&lt;opengDt&gt;2025-07-14 11:00:00&lt;/opengDt&gt;</p>
<p>&lt;ntceSpecDocUrl1&gt;https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00934850&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=1&amp;prcmBsneSeCd=01&lt;/ntceSpecDocUrl1&gt;</p>
<p>&lt;ntceSpecDocUrl2&gt;https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00934850&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=2&amp;prcmBsneSeCd=01&lt;/ntceSpecDocUrl2&gt;</p>
<p>&lt;ntceSpecDocUrl3&gt;https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00934850&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=3&amp;prcmBsneSeCd=01&lt;/ntceSpecDocUrl3&gt;</p>
<p>&lt;ntceSpecDocUrl4&gt;&lt;/ntceSpecDocUrl4&gt;</p>
<p>&lt;ntceSpecDocUrl5&gt;&lt;/ntceSpecDocUrl5&gt;</p>
<p>&lt;ntceSpecDocUrl6&gt;&lt;/ntceSpecDocUrl6&gt;</p>
<p>&lt;ntceSpecDocUrl7&gt;&lt;/ntceSpecDocUrl7&gt;</p>
<p>&lt;ntceSpecDocUrl8&gt;&lt;/ntceSpecDocUrl8&gt;</p>
<p>&lt;ntceSpecDocUrl9&gt;&lt;/ntceSpecDocUrl9&gt;</p>
<p>&lt;ntceSpecDocUrl10&gt;&lt;/ntceSpecDocUrl10&gt;</p>
<p>&lt;ntceSpecFileNm1&gt;붙임2. 입찰공고문(규가동시)_물품.hwp&lt;/ntceSpecFileNm1&gt;</p>
<p>&lt;ntceSpecFileNm2&gt;붙임3. 제안요청서.hwp&lt;/ntceSpecFileNm2&gt;</p>
<p>&lt;ntceSpecFileNm3&gt;붙임2-1. 물품규격서.hwp&lt;/ntceSpecFileNm3&gt;</p>
<p>&lt;ntceSpecFileNm4&gt;&lt;/ntceSpecFileNm4&gt;</p>
<p>&lt;ntceSpecFileNm5&gt;&lt;/ntceSpecFileNm5&gt;</p>
<p>&lt;ntceSpecFileNm6&gt;&lt;/ntceSpecFileNm6&gt;</p>
<p>&lt;ntceSpecFileNm7&gt;&lt;/ntceSpecFileNm7&gt;</p>
<p>&lt;ntceSpecFileNm8&gt;&lt;/ntceSpecFileNm8&gt;</p>
<p>&lt;ntceSpecFileNm9&gt;&lt;/ntceSpecFileNm9&gt;</p>
<p>&lt;ntceSpecFileNm10&gt;&lt;/ntceSpecFileNm10&gt;</p>
<p>&lt;rbidPermsnYn&gt;Y&lt;/rbidPermsnYn&gt;</p>
<p>&lt;prdctClsfcLmtYn&gt;Y&lt;/prdctClsfcLmtYn&gt;</p>
<p>&lt;mnfctYn&gt;N&lt;/mnfctYn&gt;</p>
<p>&lt;prearngPrceDcsnMthdNm&gt;복수예가&lt;/prearngPrceDcsnMthdNm&gt;</p>
<p>&lt;totPrdprcNum&gt;15&lt;/totPrdprcNum&gt;</p>
<p>&lt;drwtPrdprcNum&gt;4&lt;/drwtPrdprcNum&gt;</p>
<p>&lt;asignBdgtAmt&gt;90000000&lt;/asignBdgtAmt&gt;</p>
<p>&lt;presmptPrce&gt;81818182&lt;/presmptPrce&gt;</p>
<p>&lt;opengPlce&gt;국가종합전자조달시스템(나라장터)&lt;/opengPlce&gt;</p>
<p>&lt;bidNtceDtlUrl&gt;https://www.g2b.go.kr/link/PNPE027_01/single/?bidPbancNo=R25BK00934850&amp;bidPbancOrd=000&lt;/bidNtceDtlUrl&gt;</p>
<p>&lt;bidNtceUrl&gt;https://www.g2b.go.kr/link/PNPE027_01/single/?bidPbancNo=R25BK00934850&amp;bidPbancOrd=000&lt;/bidNtceUrl&gt;</p>
<p>&lt;bidPrtcptFeePaymntYn&gt;&lt;/bidPrtcptFeePaymntYn&gt;</p>
<p>&lt;bidPrtcptFee&gt;0&lt;/bidPrtcptFee&gt;</p>
<p>&lt;bidGrntymnyPaymntYn&gt;&lt;/bidGrntymnyPaymntYn&gt;</p>
<p>&lt;crdtrNm&gt;원장&lt;/crdtrNm&gt;</p>
<p>&lt;dtilPrdctClsfcNo&gt;4921181901&lt;/dtilPrdctClsfcNo&gt;</p>
<p>&lt;dtilPrdctClsfcNoNm&gt;동작분석기&lt;/dtilPrdctClsfcNoNm&gt;</p>
<p>&lt;prdctSpecNm&gt;규격서에 따름&lt;/prdctSpecNm&gt;</p>
<p>&lt;prdctQty&gt;1&lt;/prdctQty&gt;</p>
<p>&lt;prdctUnit&gt;SET&lt;/prdctUnit&gt;</p>
<p>&lt;prdctUprc&gt;90000000&lt;/prdctUprc&gt;</p>
<p>&lt;dlvrTmlmtDt&gt;&lt;/dlvrTmlmtDt&gt;</p>
<p>&lt;dlvrDaynum&gt;90&lt;/dlvrDaynum&gt;</p>
<p>&lt;dlvryCndtnNm&gt;&lt;/dlvryCndtnNm&gt;</p>
<p>&lt;purchsObjPrdctList&gt;[1^4921181901^동작분석기]&lt;/purchsObjPrdctList&gt;</p>
<p>&lt;untyNtceNo&gt;R25BM00300438&lt;/untyNtceNo&gt;</p>
<p>&lt;cmmnSpldmdMethdCd&gt;&lt;/cmmnSpldmdMethdCd&gt;</p>
<p>&lt;cmmnSpldmdMethdNm&gt;(없음)공동수급불허&lt;/cmmnSpldmdMethdNm&gt;</p>
<p>&lt;stdNtceDocUrl&gt;https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00934850&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=1&amp;prcmBsneSeCd=01&lt;/stdNtceDocUrl&gt;</p>
<p>&lt;brffcBidprcPermsnYn&gt;&lt;/brffcBidprcPermsnYn&gt;</p>
<p>&lt;dsgntCmptYn&gt;N&lt;/dsgntCmptYn&gt;</p>
<p>&lt;rsrvtnPrceReMkngMthdNm&gt;재입찰시 예비가격을 다시 생성하여 예정가격이 산정됩니다.&lt;/rsrvtnPrceReMkngMthdNm&gt;</p>
<p>&lt;arsltApplDocRcptMthdNm&gt;&lt;/arsltApplDocRcptMthdNm&gt;</p>
<p>&lt;arsltApplDocRcptDt&gt;&lt;/arsltApplDocRcptDt&gt;</p>
<p>&lt;orderPlanUntyNo&gt;R25DD20290101&lt;/orderPlanUntyNo&gt;</p>
<p>&lt;sucsfbidLwltRate&gt;&lt;/sucsfbidLwltRate&gt;</p>
<p>&lt;rgstDt&gt;2025-07-01 07:54:07&lt;/rgstDt&gt;</p>
<p>&lt;bfSpecRgstNo&gt;R25BD00078286&lt;/bfSpecRgstNo&gt;</p>
<p>&lt;infoBizYn&gt;&lt;/infoBizYn&gt;</p>
<p>&lt;sucsfbidMthdCd&gt;낙030002&lt;/sucsfbidMthdCd&gt;</p>
<p>&lt;sucsfbidMthdNm&gt;제안적격자 중 예가 내 최저가 투찰자&lt;/sucsfbidMthdNm&gt;</p>
<p>&lt;chgDt&gt;&lt;/chgDt&gt;</p>
<p>&lt;dminsttOfclEmailAdrs&gt;&lt;/dminsttOfclEmailAdrs&gt;</p>
<p>&lt;indstrytyLmtYn&gt;&lt;/indstrytyLmtYn&gt;</p>
<p>&lt;chgNtceRsn&gt;&lt;/chgNtceRsn&gt;</p>
<p>&lt;rbidOpengDt&gt;2025-07-14 11:00:00&lt;/rbidOpengDt&gt;</p>
<p>&lt;VAT&gt;8181818&lt;/VAT&gt;</p>
<p>&lt;indutyVAT&gt;&lt;/indutyVAT&gt;</p>
<p>&lt;bidWgrnteeRcptClseDt&gt;&lt;/bidWgrnteeRcptClseDt&gt;</p>
<p>&lt;rgnLmtBidLocplcJdgmBssCd&gt;&lt;/rgnLmtBidLocplcJdgmBssCd&gt;</p>
<p>&lt;rgnLmtBidLocplcJdgmBssNm&gt;&lt;/rgnLmtBidLocplcJdgmBssNm&gt;</p>
<p>&lt;techAbltEvlRt&gt;&lt;/techAbltEvlRt&gt;</p>
<p>&lt;bidPrceEvlRt&gt;&lt;/bidPrceEvlRt&gt;</p>
<p>&lt;sucsfbidMthdAppStd&gt;&lt;/sucsfbidMthdAppStd&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;/items&gt;</p>
<p>&lt;numOfRows&gt;10&lt;/numOfRows&gt;</p>
<p>&lt;pageNo&gt;1&lt;/pageNo&gt;</p>
<p>&lt;totalCount&gt;1&lt;/totalCount&gt;</p>
<p>&lt;/body&gt;</p>
<p>&lt;/response&gt;</p></td>
</tr>
</tbody>
</table>

#### \[입찰공고목록 정보에 대한 면허제한정보조회\] 오퍼레이션 명세

<table>
<colgroup>
<col style="width: 4%" />
<col style="width: 21%" />
<col style="width: 17%" />
<col style="width: 21%" />
<col style="width: 2%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr>
<td rowspan="6">오퍼레이션 정보</td>
<td>오퍼레이션 번호</td>
<td>15</td>
<td>오퍼레이션명(국문)</td>
<td colspan="2">입찰공고목록 정보에 대한 면허제한정보조회</td>
</tr>
<tr>
<td>오퍼레이션 유형</td>
<td>조회(목록)</td>
<td>오퍼레이션명(영문)</td>
<td colspan="2">getBidPblancListInfoLicenseLimit</td>
</tr>
<tr>
<td>오퍼레이션 설명</td>
<td colspan="4">검색조건에 등록일시범위(통합입찰공고)와 입찰공고번호를 입력하여 입찰공고번호, 입찰공고차수, 제한그룹번호, 제한순번, 면허제한명, 허용업종목록, 등록일시를 포함한 면허제한정보 조회</td>
</tr>
<tr>
<td>Call Back URL</td>
<td colspan="4">N/A</td>
</tr>
<tr>
<td>최대 메시지 사이즈</td>
<td colspan="4">[ 4000bytes]</td>
</tr>
<tr>
<td>평균 응답 시간</td>
<td>[ 500 ms]</td>
<td colspan="2">초당 최대 트랜잭션</td>
<td>[ 30 tps]</td>
</tr>
</tbody>
</table>

##### 요청 메시지 명세

<table>
<colgroup>
<col style="width: 19%" />
<col style="width: 19%" />
<col style="width: 13%" />
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 21%" />
</colgroup>
<tbody>
<tr>
<td style="text-align: left;">항목명(영문)</td>
<td style="text-align: left;">항목명(국문)</td>
<td style="text-align: left;">항목크기</td>
<td style="text-align: left;">항목구분</td>
<td style="text-align: left;">샘플데이터</td>
<td style="text-align: left;">항목설명</td>
</tr>
<tr>
<td style="text-align: left;">numOfRows</td>
<td style="text-align: left;">한 페이지 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td style="text-align: left;">pageNo</td>
<td style="text-align: left;">페이지 번호</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">페이지 번호</td>
</tr>
<tr>
<td style="text-align: left;">ServiceKey</td>
<td style="text-align: left;">서비스키</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">공공데이터포탈에서 받은 인증키</td>
<td style="text-align: left;">공공데이터포탈에서 받은 인증키</td>
</tr>
<tr>
<td style="text-align: left;">type</td>
<td style="text-align: left;">타입</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">json</td>
<td style="text-align: left;">오픈API 리턴 타입을 JSON으로 받고 싶을 경우 'json' 으로 지정</td>
</tr>
<tr>
<td style="text-align: left;">inqryDiv</td>
<td style="text-align: left;">조회구분</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">검색하고자하는 조회구분<br />
1:등록일시 , 2.입찰공고번호</td>
</tr>
<tr>
<td style="text-align: left;">inqryBgnDt</td>
<td style="text-align: left;">조회시작일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">202507010000</td>
<td style="text-align: left;">검색하고자하는 조회시작일시 "YYYYMMDDHHMM"<br />
(조회구분이 1인 경우 필수)</td>
</tr>
<tr>
<td style="text-align: left;">inqryEndDt</td>
<td style="text-align: left;">조회종료일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">202507012359</td>
<td style="text-align: left;">검색하고자하는 조회종료일시 "YYYYMMDDHHMM"<br />
(조회구분이 1인 경우 필수)</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNo</td>
<td style="text-align: left;">입찰공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25BK00934251</td>
<td style="text-align: left;">검색하고자 하는 입찰공고번호<br />
(조회구분이 '2'인 경우 필수)</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceOrd</td>
<td style="text-align: left;">입찰공고차수</td>
<td style="text-align: left;">3</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">000</td>
<td style="text-align: left;">검색하고자 하는 입찰공고차수<br />
(조회구분이 2인 경우 필수)</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 응답 메시지 명세

<table style="width:100%;">
<colgroup>
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 13%" />
<col style="width: 11%" />
<col style="width: 13%" />
<col style="width: 21%" />
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
<td style="text-align: left;">resultCode</td>
<td style="text-align: left;">결과코드</td>
<td style="text-align: left;">2</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">00</td>
<td style="text-align: left;">결과코드</td>
</tr>
<tr>
<td style="text-align: left;">resultMsg</td>
<td style="text-align: left;">결과메세지</td>
<td style="text-align: left;">50</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">정상.</td>
<td style="text-align: left;">결과메세지</td>
</tr>
<tr>
<td style="text-align: left;">numOfRows</td>
<td style="text-align: left;">한 페이지 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td style="text-align: left;">pageNo</td>
<td style="text-align: left;">페이지 번호</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">페이지 번호</td>
</tr>
<tr>
<td style="text-align: left;">totalCount</td>
<td style="text-align: left;">데이터 총 개수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">17</td>
<td style="text-align: left;">데이터 총개수</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNo</td>
<td style="text-align: left;">입찰공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">R25BK00934251</td>
<td style="text-align: left;"><p>입찰공고 관리번입찰공고 관리번호이며 조달청나라장터 공고건의 형식은 년도(4)+월(2)+순번(5)이며 자체전자조달시스템 보유기관은 각 기관별 형식 별도 사용</p>
<p>*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성</p>
<p>-단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</p></td>
</tr>
<tr>
<td style="text-align: left;">bidNtceOrd</td>
<td style="text-align: left;">입찰공고차수</td>
<td style="text-align: left;">3</td>
<td style="text-align: left;">01</td>
<td style="text-align: left;">000</td>
<td style="text-align: left;">입찰공고차수는 해당 입찰공고에 대한 재공고 및 재입찰 등이 발생되었을 경우 증가되는 수</td>
</tr>
<tr>
<td style="text-align: left;">lmtGrpNo</td>
<td style="text-align: left;">제한그룹번호</td>
<td style="text-align: left;">3</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">제한면허의 제한그룹번호</td>
</tr>
<tr>
<td style="text-align: left;">lmtSno</td>
<td style="text-align: left;">제한순번</td>
<td style="text-align: left;">6</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">제한면허의 제한순번</td>
</tr>
<tr>
<td style="text-align: left;">lcnsLmtNm</td>
<td style="text-align: left;">면허제한명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">액화석유가스판매사업/4617</td>
<td style="text-align: left;">면허제한코드/면허제한명</td>
</tr>
<tr>
<td style="text-align: left;">permsnIndstrytyList</td>
<td style="text-align: left;">허용업종목록</td>
<td style="text-align: left;">4000</td>
<td style="text-align: left;">0..n</td>
<td style="text-align: left;">[액화석유가스충전사업/4615]</td>
<td style="text-align: left;">공고의 제한되는 면허에서 허용되는 업종 전체 목록 [허용업종명1/허용업종코드1],[허용업종명2/허용업종코드2]</td>
</tr>
<tr>
<td style="text-align: left;">rgstDt</td>
<td style="text-align: left;">등록일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">2025-07-01 08:33:52</td>
<td style="text-align: left;">등록일시(통합입찰공고의 등록일시)</td>
</tr>
<tr>
<td style="text-align: left;">bsnsDivNm</td>
<td style="text-align: left;">업무구분명</td>
<td style="text-align: left;">30</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">물품</td>
<td style="text-align: left;">입찰업무를 구분하는 명으로 물품, 용역, 공사, 외자로 구분함</td>
</tr>
<tr>
<td style="text-align: left;">indstrytyMfrcFldList</td>
<td style="text-align: left;">주력업종분야목록</td>
<td style="text-align: left;">4000</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">[1^포장공사^보링.그라우팅.파일공사],[2^토공사]</td>
<td style="text-align: left;">면허제한 업종의 주력분야 목록.[주력분야제한그룹순번^주력업종명1^주력업종명2^주력업종명3],[주력분야제한그룹순번^주력업종명1^주력업종명3]. 나라장터 화면에서 '와'는 '^'로 구분하여 표기하고 '또는'은 대괄호[]로 구분</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 요청 / 응답 메시지 예제

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr>
<td style="text-align: center;"><strong>REST(URI)</strong></td>
</tr>
<tr>
<td style="text-align: left;">http://apis.data.go.kr/1230000/ad/BidPublicInfoService/getBidPblancListInfoLicenseLimit?inqryDiv=2&amp;bidNtceNo=R25BK00934251&amp;bidNtceOrd=000&amp;pageNo=1&amp;numOfRows=10&amp;ServiceKey=인증키</td>
</tr>
<tr>
<td style="text-align: center;"><strong>응답 메시지</strong></td>
</tr>
<tr>
<td style="text-align: left;"><p>&lt;response&gt;</p>
<p>&lt;header&gt;</p>
<p>&lt;resultCode&gt;00&lt;/resultCode&gt;</p>
<p>&lt;resultMsg&gt;정상&lt;/resultMsg&gt;</p>
<p>&lt;/header&gt;</p>
<p>&lt;body&gt;</p>
<p>&lt;items&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00934251&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;lmtGrpNo&gt;2&lt;/lmtGrpNo&gt;</p>
<p>&lt;lmtSno&gt;2&lt;/lmtSno&gt;</p>
<p>&lt;lcnsLmtNm&gt;액화석유가스충전사업/4615&lt;/lcnsLmtNm&gt;</p>
<p>&lt;permsnIndstrytyList&gt;&lt;/permsnIndstrytyList&gt;</p>
<p>&lt;indstrytyMfrcFldList&gt;&lt;/indstrytyMfrcFldList&gt;</p>
<p>&lt;rgstDt&gt;2025-07-01 08:33:52&lt;/rgstDt&gt;</p>
<p>&lt;bsnsDivNm&gt;물품&lt;/bsnsDivNm&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00934251&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;lmtGrpNo&gt;1&lt;/lmtGrpNo&gt;</p>
<p>&lt;lmtSno&gt;1&lt;/lmtSno&gt;</p>
<p>&lt;lcnsLmtNm&gt;액화석유가스판매사업/4617&lt;/lcnsLmtNm&gt;</p>
<p>&lt;permsnIndstrytyList&gt;[액화석유가스충전사업/4615]&lt;/permsnIndstrytyList&gt;</p>
<p>&lt;indstrytyMfrcFldList&gt;&lt;/indstrytyMfrcFldList&gt;</p>
<p>&lt;rgstDt&gt;2025-07-01 08:33:52&lt;/rgstDt&gt;</p>
<p>&lt;bsnsDivNm&gt;물품&lt;/bsnsDivNm&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;/items&gt;</p>
<p>&lt;numOfRows&gt;999&lt;/numOfRows&gt;</p>
<p>&lt;pageNo&gt;1&lt;/pageNo&gt;</p>
<p>&lt;totalCount&gt;2&lt;/totalCount&gt;</p>
<p>&lt;/body&gt;</p>
<p>&lt;/response&gt;</p></td>
</tr>
</tbody>
</table>

#### \[입찰공고목록 정보에 대한 참가가능지역정보조회\] 오퍼레이션 명세

<table>
<colgroup>
<col style="width: 4%" />
<col style="width: 21%" />
<col style="width: 17%" />
<col style="width: 21%" />
<col style="width: 2%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr>
<td rowspan="6">오퍼레이션 정보</td>
<td>오퍼레이션 번호</td>
<td>16</td>
<td>오퍼레이션명(국문)</td>
<td colspan="2">입찰공고목록 정보에 대한 참가가능지역정보조회</td>
</tr>
<tr>
<td>오퍼레이션 유형</td>
<td>조회(목록)</td>
<td>오퍼레이션명(영문)</td>
<td colspan="2">getBidPblancListInfoPrtcptPsblRgn</td>
</tr>
<tr>
<td>오퍼레이션 설명</td>
<td colspan="4">검색조건에 등록일시범위(통합입찰공고)와 입찰공고번호를 입력하여 입찰공고번호, 입찰공고차수, 제한그룹번호, 참가가능지역명, 등록일시 등 참가가능지역정보조회</td>
</tr>
<tr>
<td>Call Back URL</td>
<td colspan="4">N/A</td>
</tr>
<tr>
<td>최대 메시지 사이즈</td>
<td colspan="4">[ 4000bytes]</td>
</tr>
<tr>
<td>평균 응답 시간</td>
<td>[ 500 ms]</td>
<td colspan="2">초당 최대 트랜잭션</td>
<td>[ 30 tps]</td>
</tr>
</tbody>
</table>

##### 요청 메시지 명세

<table>
<colgroup>
<col style="width: 19%" />
<col style="width: 19%" />
<col style="width: 13%" />
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 21%" />
</colgroup>
<tbody>
<tr>
<td style="text-align: left;">항목명(영문)</td>
<td style="text-align: left;">항목명(국문)</td>
<td style="text-align: left;">항목크기</td>
<td style="text-align: left;">항목구분</td>
<td style="text-align: left;">샘플데이터</td>
<td style="text-align: left;">항목설명</td>
</tr>
<tr>
<td style="text-align: left;">numOfRows</td>
<td style="text-align: left;">한 페이지 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td style="text-align: left;">pageNo</td>
<td style="text-align: left;">페이지 번호</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">페이지 번호</td>
</tr>
<tr>
<td style="text-align: left;">ServiceKey</td>
<td style="text-align: left;">서비스키</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">공공데이터포탈에서 받은 인증키</td>
<td style="text-align: left;">공공데이터포탈에서 받은 인증키</td>
</tr>
<tr>
<td style="text-align: left;">type</td>
<td style="text-align: left;">타입</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">json</td>
<td style="text-align: left;">오픈API 리턴 타입을 JSON으로 받고 싶을 경우 'json' 으로 지정</td>
</tr>
<tr>
<td style="text-align: left;">inqryDiv</td>
<td style="text-align: left;">조회구분</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">검색하고자하는 조회구분<br />
1:등록일시 , 2.입찰공고번호</td>
</tr>
<tr>
<td style="text-align: left;">inqryBgnDt</td>
<td style="text-align: left;">조회시작일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">202507010000</td>
<td style="text-align: left;">검색하고자하는 조회시작일시 "YYYYMMDDHHMM"<br />
(조회구분이 1인 경우 필수)</td>
</tr>
<tr>
<td style="text-align: left;">inqryEndDt</td>
<td style="text-align: left;">조회종료일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">202507012359</td>
<td style="text-align: left;">검색하고자하는 조회종료일시 "YYYYMMDDHHMM"<br />
(조회구분이 1인 경우 필수)</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNo</td>
<td style="text-align: left;">입찰공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25BK00932003</td>
<td style="text-align: left;">검색하고자 하는 입찰공고번호<br />
(조회구분이 '2'인 경우 필수)</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceOrd</td>
<td style="text-align: left;">입찰공고차수</td>
<td style="text-align: left;">3</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">000</td>
<td style="text-align: left;">검색하고자 하는 입찰공고차수<br />
(조회구분이 2인 경우 필수)</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 응답 메시지 명세

<table style="width:100%;">
<colgroup>
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 13%" />
<col style="width: 11%" />
<col style="width: 13%" />
<col style="width: 21%" />
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
<td style="text-align: left;">resultCode</td>
<td style="text-align: left;">결과코드</td>
<td style="text-align: left;">2</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">00</td>
<td style="text-align: left;">결과코드</td>
</tr>
<tr>
<td style="text-align: left;">resultMsg</td>
<td style="text-align: left;">결과메세지</td>
<td style="text-align: left;">50</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">정상.</td>
<td style="text-align: left;">결과메세지</td>
</tr>
<tr>
<td style="text-align: left;">numOfRows</td>
<td style="text-align: left;">한 페이지 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td style="text-align: left;">pageNo</td>
<td style="text-align: left;">페이지 번호</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">페이지 번호</td>
</tr>
<tr>
<td style="text-align: left;">totalCount</td>
<td style="text-align: left;">데이터 총 개수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">17</td>
<td style="text-align: left;">데이터 총개수</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNo</td>
<td style="text-align: left;">입찰공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">R25BK00932003</td>
<td style="text-align: left;"><p>입찰공고 관리번입찰공고 관리번호이며 조달청나라장터 공고건의 형식은 년도(4)+월(2)+순번(5)이며 자체전자조달시스템 보유기관은 각 기관별 형식 별도 사용</p>
<p>*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성</p>
<p>-단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</p></td>
</tr>
<tr>
<td style="text-align: left;">bidNtceOrd</td>
<td style="text-align: left;">입찰공고차수</td>
<td style="text-align: left;">3</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">000</td>
<td style="text-align: left;">입찰공고차수는 해당 입찰공고에 대한 재공고 및 재입찰 등이 발생되었을 경우 증가되는 수</td>
</tr>
<tr>
<td style="text-align: left;">lmtSno</td>
<td style="text-align: left;">제한순번</td>
<td style="text-align: left;">6</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">참가가능지역의 제한순번</td>
</tr>
<tr>
<td style="text-align: left;">prtcptPsblRgnNm</td>
<td style="text-align: left;">참가가능지역명</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">광주광역시</td>
<td style="text-align: left;">참가가능지역의 명</td>
</tr>
<tr>
<td style="text-align: left;">rgstDt</td>
<td style="text-align: left;">등록일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">2025-07-01 06:23:47</td>
<td style="text-align: left;">등록일시(통합입찰공고의 등록일시)</td>
</tr>
<tr>
<td style="text-align: left;"><mark>bsnsDivNm</mark></td>
<td style="text-align: left;"><mark>업무구분명</mark></td>
<td style="text-align: left;"><mark>30</mark></td>
<td style="text-align: left;"><mark>0</mark></td>
<td style="text-align: left;"><mark>공사</mark></td>
<td style="text-align: left;"><mark>입찰업무를 구분하는 명으로 물품, 용역, 공사, 외자로 구분함</mark></td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 요청 / 응답 메시지 예제

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr>
<td style="text-align: center;"><strong>REST(URI)</strong></td>
</tr>
<tr>
<td style="text-align: center;">http://apis.data.go.kr/1230000/ad/BidPublicInfoService/getBidPblancListInfoPrtcptPsblRgn?inqryDiv=2&amp; bidNtceNo= R25BK00932003&amp;bidNtceOrd=000&amp;pageNo=1&amp;numOfRows=10&amp;ServiceKey=인증키</td>
</tr>
<tr>
<td style="text-align: center;"><strong>응답 메시지</strong></td>
</tr>
<tr>
<td style="text-align: left;"><p>&lt;response&gt;</p>
<p>&lt;header&gt;</p>
<p>&lt;resultCode&gt;00&lt;/resultCode&gt;</p>
<p>&lt;resultMsg&gt;정상&lt;/resultMsg&gt;</p>
<p>&lt;/header&gt;</p>
<p>&lt;body&gt;</p>
<p>&lt;items&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00932003&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;lmtSno&gt;1&lt;/lmtSno&gt;</p>
<p>&lt;prtcptPsblRgnNm&gt;광주광역시&lt;/prtcptPsblRgnNm&gt;</p>
<p>&lt;rgstDt&gt;2025-07-01 06:23:47&lt;/rgstDt&gt;</p>
<p>&lt;bsnsDivNm&gt;공사&lt;/bsnsDivNm&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;/items&gt;</p>
<p>&lt;numOfRows&gt;999&lt;/numOfRows&gt;</p>
<p>&lt;pageNo&gt;1&lt;/pageNo&gt;</p>
<p>&lt;totalCount&gt;1&lt;/totalCount&gt;</p>
<p>&lt;/body&gt;</p>
<p>&lt;/response&gt;</p></td>
</tr>
</tbody>
</table>

#### \[입찰공고목록 정보에 대한 물품 구매대상물품조회\] 오퍼레이션 명세

<table>
<colgroup>
<col style="width: 4%" />
<col style="width: 21%" />
<col style="width: 17%" />
<col style="width: 21%" />
<col style="width: 2%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr>
<td rowspan="6">오퍼레이션 정보</td>
<td>오퍼레이션 번호</td>
<td>17</td>
<td>오퍼레이션명(국문)</td>
<td colspan="2">입찰공고목록 정보에 대한 물품 구매대상물품조회</td>
</tr>
<tr>
<td>오퍼레이션 유형</td>
<td>조회(목록)</td>
<td>오퍼레이션명(영문)</td>
<td colspan="2">getBidPblancListInfoThngPurchsObjPrdct</td>
</tr>
<tr>
<td>오퍼레이션 설명</td>
<td colspan="4">검색조건에 등록일시범위(통합입찰공고)와 입찰공고번호를 입력하여 입찰공고번호, 입찰공고차수, 입찰분류번호, 물품순번, 수요기관코드, 수요기관명, 물품분류번호, 품명, 세부품명번호, 세부품명, 수량, 단위, 단가, 납품기한일시, 납품일수, 납품장소, 인도조건명 등 물품 구매대상물품 정보 조회</td>
</tr>
<tr>
<td>Call Back URL</td>
<td colspan="4">N/A</td>
</tr>
<tr>
<td>최대 메시지 사이즈</td>
<td colspan="4">[ 4000bytes]</td>
</tr>
<tr>
<td>평균 응답 시간</td>
<td>[ 500 ms]</td>
<td colspan="2">초당 최대 트랜잭션</td>
<td>[ 30 tps]</td>
</tr>
</tbody>
</table>

##### 요청 메시지 명세

<table>
<colgroup>
<col style="width: 19%" />
<col style="width: 19%" />
<col style="width: 13%" />
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 21%" />
</colgroup>
<tbody>
<tr>
<td style="text-align: left;">항목명(영문)</td>
<td style="text-align: left;">항목명(국문)</td>
<td style="text-align: left;">항목크기</td>
<td style="text-align: left;">항목구분</td>
<td style="text-align: left;">샘플데이터</td>
<td style="text-align: left;">항목설명</td>
</tr>
<tr>
<td style="text-align: left;">numOfRows</td>
<td style="text-align: left;">한 페이지 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td style="text-align: left;">pageNo</td>
<td style="text-align: left;">페이지 번호</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">페이지 번호</td>
</tr>
<tr>
<td style="text-align: left;">ServiceKey</td>
<td style="text-align: left;">서비스키</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">공공데이터포탈에서 받은 인증키</td>
<td style="text-align: left;">공공데이터포탈에서 받은 인증키</td>
</tr>
<tr>
<td style="text-align: left;">type</td>
<td style="text-align: left;">타입</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">json</td>
<td style="text-align: left;">오픈API 리턴 타입을 JSON으로 받고 싶을 경우 'json' 으로 지정</td>
</tr>
<tr>
<td style="text-align: left;">inqryDiv</td>
<td style="text-align: left;">조회구분</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">검색하고자하는 조회구분<br />
1:공고게시일시(입찰공고) , 2.입찰공고번호</td>
</tr>
<tr>
<td style="text-align: left;">inqryBgnDt</td>
<td style="text-align: left;">조회시작일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">202507010000</td>
<td style="text-align: left;">검색하고자하는 공고게시일시 조회시작일시 "YYYYMMDDHHMM"<br />
(조회구분이 1인 경우 필수)</td>
</tr>
<tr>
<td style="text-align: left;">inqryEndDt</td>
<td style="text-align: left;">조회종료일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">202507012359</td>
<td style="text-align: left;">검색하고자하는 공고게시일시 조회종료일시 "YYYYMMDDHHMM"<br />
(조회구분이 1인 경우 필수)</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNo</td>
<td style="text-align: left;">입찰공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25BK00915548</td>
<td style="text-align: left;">검색하고자 하는 입찰공고번호<br />
(조회구분이 2인 경우 필수)</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceOrd</td>
<td style="text-align: left;">입찰공고차수</td>
<td style="text-align: left;">3</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">003</td>
<td style="text-align: left;">검색하고자 하는 입찰공고번호<br />
(조회구분이 2인 경우 필수)</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 응답 메시지 명세

<table style="width:100%;">
<colgroup>
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 13%" />
<col style="width: 11%" />
<col style="width: 13%" />
<col style="width: 21%" />
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
<td style="text-align: left;">resultCode</td>
<td style="text-align: left;">결과코드</td>
<td style="text-align: left;">2</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">00</td>
<td style="text-align: left;">결과코드</td>
</tr>
<tr>
<td style="text-align: left;">resultMsg</td>
<td style="text-align: left;">결과메세지</td>
<td style="text-align: left;">50</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">정상.</td>
<td style="text-align: left;">결과메세지</td>
</tr>
<tr>
<td style="text-align: left;">numOfRows</td>
<td style="text-align: left;">한 페이지 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td style="text-align: left;">pageNo</td>
<td style="text-align: left;">페이지 번호</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">페이지 번호</td>
</tr>
<tr>
<td style="text-align: left;">totalCount</td>
<td style="text-align: left;">데이터 총 개수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">데이터 총개수</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNo</td>
<td style="text-align: left;">입찰공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">R25BK00915548</td>
<td style="text-align: left;"><p>입찰공고 관리번입찰공고 관리번호이며 조달청나라장터 공고건의 형식은 년도(4)+월(2)+순번(5)이며 자체전자조달시스템 보유기관은 각 기관별 형식 별도 사용</p>
<p>*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성</p>
<p>-단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</p></td>
</tr>
<tr>
<td style="text-align: left;">bidNtceOrd</td>
<td style="text-align: left;">입찰공고차수</td>
<td style="text-align: left;">3</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">003</td>
<td style="text-align: left;">입찰공고차수는 해당 입찰공고에 대한 재공고 및 재입찰 등이 발생되었을 경우 증가되는 수</td>
</tr>
<tr>
<td style="text-align: left;">bidClsfcNo</td>
<td style="text-align: left;">입찰분류번호</td>
<td style="text-align: left;">5</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">입찰공고의 입찰분류번호</td>
</tr>
<tr>
<td style="text-align: left;">prdctSno</td>
<td style="text-align: left;">물품순번</td>
<td style="text-align: left;">6</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">입찰공고의 물품순번</td>
</tr>
<tr>
<td style="text-align: left;">dminsttCd</td>
<td style="text-align: left;">수요기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">ZT02254</td>
<td style="text-align: left;">공고를 하는 기관의 코드로 행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드가 행자부코드가 없는 경우 조달청에서 부여한 수요기관 코드가 표기됨</td>
</tr>
<tr>
<td style="text-align: left;">dminsttNm</td>
<td style="text-align: left;">수요기관명</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">수호영농조합법인</td>
<td style="text-align: left;">중앙조달인 경우 조달사업에 관한 법률 제2조(정의)에 따라 수요물자의 구매 공급 또는 시설공사 계약의 체결을 조달청장에게 요청할 수 있도록 조달청장이 인정하여 등록한 기관 또는 자체전자조달시스템을 이용하는 기관인 경우 계약을 의뢰한 기관의 명으로 공고기관과 수요기관이 동일할 수 있음</td>
</tr>
<tr>
<td style="text-align: left;">prdctClsfcNo</td>
<td style="text-align: left;">물품분류번호</td>
<td style="text-align: left;">8</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">47101524</td>
<td style="text-align: left;">품명에 대한 분류번호로서 8자리로 표시</td>
</tr>
<tr>
<td style="text-align: left;">prdctClsfcNoNm</td>
<td style="text-align: left;">품명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">슬러지퇴비화장치</td>
<td style="text-align: left;">물품분류번호 8자리에 대한 한글명</td>
</tr>
<tr>
<td style="text-align: left;">dtilPrdctClsfcNo</td>
<td style="text-align: left;">세부품명번호</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">4710152401</td>
<td style="text-align: left;">품명에 대한 분류번호로서 10자리로 표시</td>
</tr>
<tr>
<td style="text-align: left;">dtilPrdctClsfcNoNm</td>
<td style="text-align: left;">세부품명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">슬러지퇴비화장치</td>
<td style="text-align: left;">세부품명번호 10자리에 대한 한글명</td>
</tr>
<tr>
<td style="text-align: left;">prdctSpecNm</td>
<td style="text-align: left;">물품규격명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">원통형/4.5*4.5*8</td>
<td style="text-align: left;">물품의 규격명</td>
</tr>
<tr>
<td style="text-align: left;">qty</td>
<td style="text-align: left;">수량</td>
<td style="text-align: left;">18</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">물품의 수량</td>
</tr>
<tr>
<td style="text-align: left;">unit</td>
<td style="text-align: left;">단위</td>
<td style="text-align: left;">30</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">물품의 단위</td>
</tr>
<tr>
<td style="text-align: left;">uprc</td>
<td style="text-align: left;">단가</td>
<td style="text-align: left;">18</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">210000000</td>
<td style="text-align: left;">물품의 단가(원화, 원)</td>
</tr>
<tr>
<td style="text-align: left;">dlvrTmlmtDt</td>
<td style="text-align: left;">납품기한일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N/A</td>
<td style="text-align: left;">물품의 납품기한일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">dlvrDaynum</td>
<td style="text-align: left;">납품일수</td>
<td style="text-align: left;">5</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">60</td>
<td style="text-align: left;">물품의 납품일수</td>
</tr>
<tr>
<td style="text-align: left;">dlvrPlce</td>
<td style="text-align: left;">납품장소</td>
<td style="text-align: left;">256</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">전북 김제시 공덕면 유강로 342-39</td>
<td style="text-align: left;">물품의 납품장소</td>
</tr>
<tr>
<td style="text-align: left;">dlvryCndtnNm</td>
<td style="text-align: left;">인도조건명</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">현장설치도</td>
<td style="text-align: left;">물품의 인도조건명</td>
</tr>
<tr>
<td style="text-align: left;">ntceNticeDt</td>
<td style="text-align: left;">공고게시일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">2025-07-01 16:06:21</td>
<td style="text-align: left;">공고게시일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 요청 / 응답 메시지 예제

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr>
<td style="text-align: center;"><strong>REST(URI)</strong></td>
</tr>
<tr>
<td style="text-align: center;">http://apis.data.go.kr/1230000/ad/BidPublicInfoService/getBidPblancListInfoThngPurchsObjPrdct?inqryDiv=2&amp;bidNtceNo= R25BK00915548&amp;bidNtceOrd=003&amp;pageNo=1&amp;numOfRows=10&amp;ServiceKey=인증키</td>
</tr>
<tr>
<td style="text-align: center;"><strong>응답 메시지</strong></td>
</tr>
<tr>
<td style="text-align: left;"><p>&lt;response&gt;</p>
<p>&lt;header&gt;</p>
<p>&lt;resultCode&gt;00&lt;/resultCode&gt;</p>
<p>&lt;resultMsg&gt;정상&lt;/resultMsg&gt;</p>
<p>&lt;/header&gt;</p>
<p>&lt;body&gt;</p>
<p>&lt;items&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00915548&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;003&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;1&lt;/bidClsfcNo&gt;</p>
<p>&lt;prdctSno&gt;1&lt;/prdctSno&gt;</p>
<p>&lt;dminsttCd&gt;ZT02254&lt;/dminsttCd&gt;</p>
<p>&lt;dminsttNm&gt;수호영농조합법인&lt;/dminsttNm&gt;</p>
<p>&lt;prdctClsfcNo&gt;47101524&lt;/prdctClsfcNo&gt;</p>
<p>&lt;prdctClsfcNoNm&gt;슬러지퇴비화장치&lt;/prdctClsfcNoNm&gt;</p>
<p>&lt;dtilPrdctClsfcNo&gt;4710152401&lt;/dtilPrdctClsfcNo&gt;</p>
<p>&lt;dtilPrdctClsfcNoNm&gt;슬러지퇴비화장치&lt;/dtilPrdctClsfcNoNm&gt;</p>
<p>&lt;prdctSpecNm&gt;원통형/4.5*4.5*8&lt;/prdctSpecNm&gt;</p>
<p>&lt;qty&gt;1&lt;/qty&gt;</p>
<p>&lt;unit&gt;1&lt;/unit&gt;</p>
<p>&lt;uprc&gt;210000000&lt;/uprc&gt;</p>
<p>&lt;dlvrTmlmtDt&gt;&lt;/dlvrTmlmtDt&gt;</p>
<p>&lt;dlvrDaynum&gt;60&lt;/dlvrDaynum&gt;</p>
<p>&lt;dlvrPlce&gt;전북 김제시 공덕면 유강로 342-39&lt;/dlvrPlce&gt;</p>
<p>&lt;dlvryCndtnNm&gt;현장설치도&lt;/dlvryCndtnNm&gt;</p>
<p>&lt;ntceNticeDt&gt;2025-07-01 16:06:21&lt;/ntceNticeDt&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;/items&gt;</p>
<p>&lt;numOfRows&gt;999&lt;/numOfRows&gt;</p>
<p>&lt;pageNo&gt;1&lt;/pageNo&gt;</p>
<p>&lt;totalCount&gt;1&lt;/totalCount&gt;</p>
<p>&lt;/body&gt;</p>
<p>&lt;/response&gt;</p></td>
</tr>
</tbody>
</table>

#### \[입찰공고목록 정보에 대한 용역 구매대상물품조회\] 오퍼레이션 명세

<table>
<colgroup>
<col style="width: 4%" />
<col style="width: 21%" />
<col style="width: 17%" />
<col style="width: 21%" />
<col style="width: 2%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr>
<td rowspan="6">오퍼레이션 정보</td>
<td>오퍼레이션 번호</td>
<td>18</td>
<td>오퍼레이션명(국문)</td>
<td colspan="2">입찰공고목록 정보에 대한 용역 구매대상물품조회</td>
</tr>
<tr>
<td>오퍼레이션 유형</td>
<td>조회(목록)</td>
<td>오퍼레이션명(영문)</td>
<td colspan="2">getBidPblancListInfoServcPurchsObjPrdct</td>
</tr>
<tr>
<td>오퍼레이션 설명</td>
<td colspan="4">검색조건에 등록일시범위(통합입찰공고)와 입찰공고번호를 입력하여 입찰공고번호, 입찰공고차수, 입찰분류번호, 물품순번, 수요기관코드, 수요기관명, 물품분류번호, 품명, 세부품명번호, 세부품명, 수량, 단위, 단가, 납품기한일시, 납품일수, 납품장소, 인도조건명 등 용역 구매대상물품 정보 조회</td>
</tr>
<tr>
<td>Call Back URL</td>
<td colspan="4">N/A</td>
</tr>
<tr>
<td>최대 메시지 사이즈</td>
<td colspan="4">[ 4000bytes]</td>
</tr>
<tr>
<td>평균 응답 시간</td>
<td>[ 500 ms]</td>
<td colspan="2">초당 최대 트랜잭션</td>
<td>[ 30 tps]</td>
</tr>
</tbody>
</table>

##### 요청 메시지 명세

<table>
<colgroup>
<col style="width: 19%" />
<col style="width: 19%" />
<col style="width: 13%" />
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 21%" />
</colgroup>
<tbody>
<tr>
<td style="text-align: left;">항목명(영문)</td>
<td style="text-align: left;">항목명(국문)</td>
<td style="text-align: left;">항목크기</td>
<td style="text-align: left;">항목구분</td>
<td style="text-align: left;">샘플데이터</td>
<td style="text-align: left;">항목설명</td>
</tr>
<tr>
<td style="text-align: left;">numOfRows</td>
<td style="text-align: left;">한 페이지 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td style="text-align: left;">pageNo</td>
<td style="text-align: left;">페이지 번호</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">페이지 번호</td>
</tr>
<tr>
<td style="text-align: left;">ServiceKey</td>
<td style="text-align: left;">서비스키</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">공공데이터포탈에서 받은 인증키</td>
<td style="text-align: left;">공공데이터포탈에서 받은 인증키</td>
</tr>
<tr>
<td style="text-align: left;">type</td>
<td style="text-align: left;">타입</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">json</td>
<td style="text-align: left;">오픈API 리턴 타입을 JSON으로 받고 싶을 경우 'json' 으로 지정</td>
</tr>
<tr>
<td style="text-align: left;">inqryDiv</td>
<td style="text-align: left;">조회구분</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">검색하고자하는 조회구분<br />
1:공고게시일시(입찰공고) , 2.입찰공고번호</td>
</tr>
<tr>
<td style="text-align: left;">inqryBgnDt</td>
<td style="text-align: left;">조회시작일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">202507010000</td>
<td style="text-align: left;">검색하고자하는 공고게시일시 조회시작일시 "YYYYMMDDHHMM"<br />
(조회구분이 1인 경우 필수)</td>
</tr>
<tr>
<td style="text-align: left;">inqryEndDt</td>
<td style="text-align: left;">조회종료일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">202507012359</td>
<td style="text-align: left;">검색하고자하는 공고게시일시 조회종료일시 "YYYYMMDDHHMM"<br />
(조회구분이 1인 경우 필수)</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNo</td>
<td style="text-align: left;">입찰공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25BK00918796</td>
<td style="text-align: left;">검색하고자 하는 입찰공고번호<br />
(조회구분이 2인 경우 필수)</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceOrd</td>
<td style="text-align: left;">입찰공고차수</td>
<td style="text-align: left;">3</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">000</td>
<td style="text-align: left;">검색하고자 하는 입찰공고번호<br />
(조회구분이 2인 경우 필수)</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 응답 메시지 명세

<table style="width:100%;">
<colgroup>
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 13%" />
<col style="width: 11%" />
<col style="width: 13%" />
<col style="width: 21%" />
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
<td style="text-align: left;">resultCode</td>
<td style="text-align: left;">결과코드</td>
<td style="text-align: left;">2</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">00</td>
<td style="text-align: left;">결과코드</td>
</tr>
<tr>
<td style="text-align: left;">resultMsg</td>
<td style="text-align: left;">결과메세지</td>
<td style="text-align: left;">50</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">정상.</td>
<td style="text-align: left;">결과메세지</td>
</tr>
<tr>
<td style="text-align: left;">numOfRows</td>
<td style="text-align: left;">한 페이지 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td style="text-align: left;">pageNo</td>
<td style="text-align: left;">페이지 번호</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">페이지 번호</td>
</tr>
<tr>
<td style="text-align: left;">totalCount</td>
<td style="text-align: left;">데이터 총 개수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">17</td>
<td style="text-align: left;">데이터 총개수</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNo</td>
<td style="text-align: left;">입찰공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">R25BK00918796</td>
<td style="text-align: left;"><p>입찰공고 관리번입찰공고 관리번호이며 조달청나라장터 공고건의 형식은 년도(4)+월(2)+순번(5)이며 자체전자조달시스템 보유기관은 각 기관별 형식 별도 사용</p>
<p>*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성</p>
<p>-단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</p></td>
</tr>
<tr>
<td style="text-align: left;">bidNtceOrd</td>
<td style="text-align: left;">입찰공고차수</td>
<td style="text-align: left;">3</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">000</td>
<td style="text-align: left;">입찰공고차수는 해당 입찰공고에 대한 재공고 및 재입찰 등이 발생되었을 경우 증가되는 수</td>
</tr>
<tr>
<td style="text-align: left;">bidClsfcNo</td>
<td style="text-align: left;">입찰분류번호</td>
<td style="text-align: left;">5</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">입찰공고의 입찰분류번호</td>
</tr>
<tr>
<td style="text-align: left;">prdctSno</td>
<td style="text-align: left;">물품순번</td>
<td style="text-align: left;">6</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">입찰공고의 물품순번</td>
</tr>
<tr>
<td style="text-align: left;">dminsttCd</td>
<td style="text-align: left;">수요기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">1371577</td>
<td style="text-align: left;">공고를 하는 기관의 코드로 행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드가 행자부코드가 없는 경우 조달청에서 부여한 수요기관 코드가 표기됨</td>
</tr>
<tr>
<td style="text-align: left;">dminsttNm</td>
<td style="text-align: left;">수요기관명</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">문화체육관광부 국립한글박물관</td>
<td style="text-align: left;">중앙조달인 경우 조달사업에 관한 법률 제2조(정의)에 따라 수요물자의 구매 공급 또는 시설공사 계약의 체결을 조달청장에게 요청할 수 있도록 조달청장이 인정하여 등록한 기관 또는 자체전자조달시스템을 이용하는 기관인 경우 계약을 의뢰한 기관의 명으로 공고기관과 수요기관이 동일할 수 있음</td>
</tr>
<tr>
<td style="text-align: left;">prdctClsfcNo</td>
<td style="text-align: left;">물품분류번호</td>
<td style="text-align: left;">8</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">80141989</td>
<td style="text-align: left;">품명에 대한 분류번호로서 8자리로 표시</td>
</tr>
<tr>
<td style="text-align: left;">prdctClsfcNoNm</td>
<td style="text-align: left;">품명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">국제행사기획및대행서비스</td>
<td style="text-align: left;">물품분류번호 8자리에 대한 한글명</td>
</tr>
<tr>
<td style="text-align: left;">dtilPrdctClsfcNo</td>
<td style="text-align: left;">세부품명번호</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">8014198901</td>
<td style="text-align: left;">품명에 대한 분류번호로서 10자리로 표시</td>
</tr>
<tr>
<td style="text-align: left;">dtilPrdctClsfcNoNm</td>
<td style="text-align: left;">세부품명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">국제행사기획및대행서비스</td>
<td style="text-align: left;">세부품명번호 10자리에 대한 한글명</td>
</tr>
<tr>
<td style="text-align: left;">prdctSpecNm</td>
<td style="text-align: left;">물품규격명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">제안요청서에 따름</td>
<td style="text-align: left;">물품의 규격명</td>
</tr>
<tr>
<td style="text-align: left;">qty</td>
<td style="text-align: left;">수량</td>
<td style="text-align: left;">18</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">물품의 수량</td>
</tr>
<tr>
<td style="text-align: left;">unit</td>
<td style="text-align: left;">단위</td>
<td style="text-align: left;">30</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">식</td>
<td style="text-align: left;">물품의 단위</td>
</tr>
<tr>
<td style="text-align: left;">uprc</td>
<td style="text-align: left;">단가</td>
<td style="text-align: left;">18</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">120000000</td>
<td style="text-align: left;">물품의 단가</td>
</tr>
<tr>
<td style="text-align: left;">dlvrTmlmtDt</td>
<td style="text-align: left;">납품기한일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-11-14 00:00:00</td>
<td style="text-align: left;">물품의 납품기한일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">dlvrDaynum</td>
<td style="text-align: left;">납품일수</td>
<td style="text-align: left;">5</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N/A</td>
<td style="text-align: left;">물품의 납품일수</td>
</tr>
<tr>
<td style="text-align: left;">dlvrPlce</td>
<td style="text-align: left;">납품장소</td>
<td style="text-align: left;">256</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">한국프레스센터</td>
<td style="text-align: left;">물품의 납품장소</td>
</tr>
<tr>
<td style="text-align: left;">dlvryCndtnNm</td>
<td style="text-align: left;">인도조건명</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">과업내역에 따름</td>
<td style="text-align: left;">물품의 인도조건명</td>
</tr>
<tr>
<td style="text-align: left;">ntceNticeDt</td>
<td style="text-align: left;">공고게시일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">2025-07-01 16:47:08</td>
<td style="text-align: left;">공고게시일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 요청 / 응답 메시지 예제

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr>
<td style="text-align: center;"><strong>REST(URI)</strong></td>
</tr>
<tr>
<td style="text-align: center;">http://apis.data.go.kr/1230000/ad/BidPublicInfoService/getBidPblancListInfoServcPurchsObjPrdct?inqryDiv=2&amp;bidNtceNo= R25BK00918796&amp;bidNtceOrd=000&amp;pageNo=1&amp;numOfRows=10&amp;ServiceKey=인증키</td>
</tr>
<tr>
<td style="text-align: center;"><strong>응답 메시지</strong></td>
</tr>
<tr>
<td style="text-align: left;"><p>&lt;response&gt;</p>
<p>&lt;header&gt;</p>
<p>&lt;resultCode&gt;00&lt;/resultCode&gt;</p>
<p>&lt;resultMsg&gt;정상&lt;/resultMsg&gt;</p>
<p>&lt;/header&gt;</p>
<p>&lt;body&gt;</p>
<p>&lt;items&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00918796&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;1&lt;/bidClsfcNo&gt;</p>
<p>&lt;prdctSno&gt;1&lt;/prdctSno&gt;</p>
<p>&lt;dminsttCd&gt;1371577&lt;/dminsttCd&gt;</p>
<p>&lt;dminsttNm&gt;문화체육관광부 국립한글박물관&lt;/dminsttNm&gt;</p>
<p>&lt;prdctClsfcNo&gt;80141989&lt;/prdctClsfcNo&gt;</p>
<p>&lt;prdctClsfcNoNm&gt;국제행사기획및대행서비스&lt;/prdctClsfcNoNm&gt;</p>
<p>&lt;dtilPrdctClsfcNo&gt;8014198901&lt;/dtilPrdctClsfcNo&gt;</p>
<p>&lt;dtilPrdctClsfcNoNm&gt;국제행사기획및대행서비스&lt;/dtilPrdctClsfcNoNm&gt;</p>
<p>&lt;prdctSpecNm&gt;제안요청서에 따름&lt;/prdctSpecNm&gt;</p>
<p>&lt;qty&gt;1&lt;/qty&gt;</p>
<p>&lt;unit&gt;식&lt;/unit&gt;</p>
<p>&lt;uprc&gt;120000000&lt;/uprc&gt;</p>
<p>&lt;dlvrTmlmtDt&gt;2025-11-14 00:00:00&lt;/dlvrTmlmtDt&gt;</p>
<p>&lt;dlvrDaynum&gt;&lt;/dlvrDaynum&gt;</p>
<p>&lt;dlvrPlce&gt;한국프레스센터&lt;/dlvrPlce&gt;</p>
<p>&lt;dlvryCndtnNm&gt;과업내역에 따름&lt;/dlvryCndtnNm&gt;</p>
<p>&lt;ntceNticeDt&gt;2025-07-01 16:47:08&lt;/ntceNticeDt&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;/items&gt;</p>
<p>&lt;numOfRows&gt;999&lt;/numOfRows&gt;</p>
<p>&lt;pageNo&gt;1&lt;/pageNo&gt;</p>
<p>&lt;totalCount&gt;1&lt;/totalCount&gt;</p>
<p>&lt;/body&gt;</p>
<p>&lt;/response&gt;</p></td>
</tr>
</tbody>
</table>

#### \[입찰공고목록 정보에 대한 외자 구매대상물품조회\] 오퍼레이션 명세

<table>
<colgroup>
<col style="width: 4%" />
<col style="width: 21%" />
<col style="width: 17%" />
<col style="width: 21%" />
<col style="width: 2%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr>
<td rowspan="6">오퍼레이션 정보</td>
<td>오퍼레이션 번호</td>
<td>19</td>
<td>오퍼레이션명(국문)</td>
<td colspan="2">입찰공고목록 정보에 대한 외자 구매대상물품조회</td>
</tr>
<tr>
<td>오퍼레이션 유형</td>
<td>조회(목록)</td>
<td>오퍼레이션명(영문)</td>
<td colspan="2">getBidPblancListInfoFrgcptPurchsObjPrdct</td>
</tr>
<tr>
<td>오퍼레이션 설명</td>
<td colspan="4">검색조건에 등록일시범위(통합입찰공고)와 입찰공고번호를 입력하여 입찰공고번호, 입찰공고차수, 입찰분류번호, 물품순번, 수요기관코드, 수요기관명, HSK번호, 세부품명번호, 세부품명, 수량, 단위, 배정금액, 배정금액통화 등 외자 구매대상물품 정보 조회</td>
</tr>
<tr>
<td>Call Back URL</td>
<td colspan="4">N/A</td>
</tr>
<tr>
<td>최대 메시지 사이즈</td>
<td colspan="4">[ 4000bytes]</td>
</tr>
<tr>
<td>평균 응답 시간</td>
<td>[ 500 ms]</td>
<td colspan="2">초당 최대 트랜잭션</td>
<td>[ 30 tps]</td>
</tr>
</tbody>
</table>

##### 요청 메시지 명세

<table>
<colgroup>
<col style="width: 19%" />
<col style="width: 19%" />
<col style="width: 13%" />
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 21%" />
</colgroup>
<tbody>
<tr>
<td style="text-align: left;">항목명(영문)</td>
<td style="text-align: left;">항목명(국문)</td>
<td style="text-align: left;">항목크기</td>
<td style="text-align: left;">항목구분</td>
<td style="text-align: left;">샘플데이터</td>
<td style="text-align: left;">항목설명</td>
</tr>
<tr>
<td style="text-align: left;">numOfRows</td>
<td style="text-align: left;">한 페이지 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td style="text-align: left;">pageNo</td>
<td style="text-align: left;">페이지 번호</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">페이지 번호</td>
</tr>
<tr>
<td style="text-align: left;">ServiceKey</td>
<td style="text-align: left;">서비스키</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">공공데이터포탈에서 받은 인증키</td>
<td style="text-align: left;">공공데이터포탈에서 받은 인증키</td>
</tr>
<tr>
<td style="text-align: left;">type</td>
<td style="text-align: left;">타입</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">json</td>
<td style="text-align: left;">오픈API 리턴 타입을 JSON으로 받고 싶을 경우 'json' 으로 지정</td>
</tr>
<tr>
<td style="text-align: left;">inqryDiv</td>
<td style="text-align: left;">조회구분</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">검색하고자하는 조회구분<br />
1:공고게시일시(입찰공고) , 2.입찰공고번호</td>
</tr>
<tr>
<td style="text-align: left;">inqryBgnDt</td>
<td style="text-align: left;">조회시작일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">202507010000</td>
<td style="text-align: left;">검색하고자하는 공고게시일시 조회시작일시 "YYYYMMDDHHMM"<br />
(조회구분이 1인 경우 필수)</td>
</tr>
<tr>
<td style="text-align: left;">inqryEndDt</td>
<td style="text-align: left;">조회종료일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">202507042359</td>
<td style="text-align: left;">검색하고자하는 공고게시일시 조회종료일시 "YYYYMMDDHHMM"<br />
(조회구분이 1인 경우 필수)</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNo</td>
<td style="text-align: left;">입찰공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25BK00940768</td>
<td style="text-align: left;">검색하고자 하는 입찰공고번호<br />
(조회구분이 2인 경우 필수)</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceOrd</td>
<td style="text-align: left;">입찰공고차수</td>
<td style="text-align: left;">3</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">000</td>
<td style="text-align: left;">검색하고자 하는 입찰공고번호<br />
(조회구분이 2인 경우 필수)</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 응답 메시지 명세

<table style="width:100%;">
<colgroup>
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 13%" />
<col style="width: 11%" />
<col style="width: 13%" />
<col style="width: 21%" />
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
<td style="text-align: left;">resultCode</td>
<td style="text-align: left;">결과코드</td>
<td style="text-align: left;">2</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">00</td>
<td style="text-align: left;">결과코드</td>
</tr>
<tr>
<td style="text-align: left;">resultMsg</td>
<td style="text-align: left;">결과메세지</td>
<td style="text-align: left;">50</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">정상.</td>
<td style="text-align: left;">결과메세지</td>
</tr>
<tr>
<td style="text-align: left;">numOfRows</td>
<td style="text-align: left;">한 페이지 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td style="text-align: left;">pageNo</td>
<td style="text-align: left;">페이지 번호</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">페이지 번호</td>
</tr>
<tr>
<td style="text-align: left;">totalCount</td>
<td style="text-align: left;">데이터 총 개수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">17</td>
<td style="text-align: left;">데이터 총개수</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNo</td>
<td style="text-align: left;">입찰공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">R25BK00940768</td>
<td style="text-align: left;"><p>입찰공고 관리번입찰공고 관리번호이며 조달청나라장터 공고건의 형식은 년도(4)+월(2)+순번(5)이며 자체전자조달시스템 보유기관은 각 기관별 형식 별도 사용</p>
<p>*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성</p>
<p>-단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</p></td>
</tr>
<tr>
<td style="text-align: left;">bidNtceOrd</td>
<td style="text-align: left;">입찰공고차수</td>
<td style="text-align: left;">3</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">000</td>
<td style="text-align: left;">입찰공고차수는 해당 입찰공고에 대한 재공고 및 재입찰 등이 발생되었을 경우 증가되는 수</td>
</tr>
<tr>
<td style="text-align: left;">bidClsfcNo</td>
<td style="text-align: left;">입찰분류번호</td>
<td style="text-align: left;">5</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">입찰공고의 입찰분류번호</td>
</tr>
<tr>
<td style="text-align: left;">prdctSno</td>
<td style="text-align: left;">물품순번</td>
<td style="text-align: left;">6</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">입찰공고의 물품순번</td>
</tr>
<tr>
<td style="text-align: left;">dminsttCd</td>
<td style="text-align: left;">수요기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">6260409</td>
<td style="text-align: left;">공고를 하는 기관의 코드로 행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드가 행자부코드가 없는 경우 조달청에서 부여한 수요기관 코드가 표기됨</td>
</tr>
<tr>
<td style="text-align: left;">dminsttNm</td>
<td style="text-align: left;">수요기관명</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">부산광역시 건설안전시험사업소</td>
<td style="text-align: left;">중앙조달인 경우 조달사업에 관한 법률 제2조(정의)에 따라 수요물자의 구매 공급 또는 시설공사 계약의 체결을 조달청장에게 요청할 수 있도록 조달청장이 인정하여 등록한 기관 또는 자체전자조달시스템을 이용하는 기관인 경우 계약을 의뢰한 기관의 명으로 공고기관과 수요기관이 동일할 수 있음</td>
</tr>
<tr>
<td style="text-align: left;">hskNo</td>
<td style="text-align: left;">HSK번호</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">9022191000</td>
<td style="text-align: left;">물품에 대한 HSK번호</td>
</tr>
<tr>
<td style="text-align: left;">dtilPrdctClsfcNo</td>
<td style="text-align: left;">세부품명번호</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">4110270401</td>
<td style="text-align: left;">품명에 대한 분류번호로서 10자리로 표시</td>
</tr>
<tr>
<td style="text-align: left;">dtilPrdctClsfcNoNm</td>
<td style="text-align: left;">세부품명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">엑스선회절분석기</td>
<td style="text-align: left;">세부품명번호 10자리에 대한 한글명</td>
</tr>
<tr>
<td style="text-align: left;">qty</td>
<td style="text-align: left;">수량</td>
<td style="text-align: left;">18</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">물품의 수량</td>
</tr>
<tr>
<td style="text-align: left;">unit</td>
<td style="text-align: left;">단위</td>
<td style="text-align: left;">30</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">SYSTEM</td>
<td style="text-align: left;">물품의 단위</td>
</tr>
<tr>
<td style="text-align: left;">asignAmt</td>
<td style="text-align: left;">배정금액</td>
<td style="text-align: left;">18</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">105245</td>
<td style="text-align: left;">물품의 배정금액</td>
</tr>
<tr>
<td style="text-align: left;">asignAmtCrncy</td>
<td style="text-align: left;">배정금액통화</td>
<td style="text-align: left;">3</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">USD</td>
<td style="text-align: left;">배정금액의 통화</td>
</tr>
<tr>
<td style="text-align: left;">ntceNticeDt</td>
<td style="text-align: left;">공고게시일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">2025-07-04 09:00:33</td>
<td style="text-align: left;">공고게시일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 요청 / 응답 메시지 예제

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr>
<td style="text-align: center;"><strong>REST(URI)</strong></td>
</tr>
<tr>
<td style="text-align: center;">http://apis.data.go.kr/1230000/ad/BidPublicInfoService/getBidPblancListInfoFrgcptPurchsObjPrdct?inqryDiv=2&amp;bidNtceNo=R25BK00940768&amp;bidNtceOrd=000&amp;pageNo=1&amp;numOfRows=10&amp;ServiceKey=인증키</td>
</tr>
<tr>
<td style="text-align: center;"><strong>응답 메시지</strong></td>
</tr>
<tr>
<td style="text-align: left;"><p>&lt;response&gt;</p>
<p>&lt;header&gt;</p>
<p>&lt;resultCode&gt;00&lt;/resultCode&gt;</p>
<p>&lt;resultMsg&gt;정상&lt;/resultMsg&gt;</p>
<p>&lt;/header&gt;</p>
<p>&lt;body&gt;</p>
<p>&lt;items&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00940768&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;1&lt;/bidClsfcNo&gt;</p>
<p>&lt;prdctSno&gt;1&lt;/prdctSno&gt;</p>
<p>&lt;dminsttCd&gt;&lt;/dminsttCd&gt;</p>
<p>&lt;dminsttNm&gt;&lt;/dminsttNm&gt;</p>
<p>&lt;hskNo&gt;9022191000&lt;/hskNo&gt;</p>
<p>&lt;dtilPrdctClsfcNo&gt;4110270401&lt;/dtilPrdctClsfcNo&gt;</p>
<p>&lt;dtilPrdctClsfcNoNm&gt;엑스선회절분석기&lt;/dtilPrdctClsfcNoNm&gt;</p>
<p>&lt;qty&gt;1&lt;/qty&gt;</p>
<p>&lt;unit&gt;SYSTEM&lt;/unit&gt;</p>
<p>&lt;asignAmt&gt;105245&lt;/asignAmt&gt;</p>
<p>&lt;asignAmtCrncy&gt;USD&lt;/asignAmtCrncy&gt;</p>
<p>&lt;ntceNticeDt&gt;2025-07-04 09:00:33&lt;/ntceNticeDt&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;/items&gt;</p>
<p>&lt;numOfRows&gt;999&lt;/numOfRows&gt;</p>
<p>&lt;pageNo&gt;1&lt;/pageNo&gt;</p>
<p>&lt;totalCount&gt;1&lt;/totalCount&gt;</p>
<p>&lt;/body&gt;</p>
<p>&lt;/response&gt;</p></td>
</tr>
</tbody>
</table>

#### \[입찰공고목록 정보에 대한 e발주 첨부파일정보조회\] 오퍼레이션 명세

<table>
<colgroup>
<col style="width: 4%" />
<col style="width: 21%" />
<col style="width: 17%" />
<col style="width: 21%" />
<col style="width: 2%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr>
<td rowspan="6">오퍼레이션 정보</td>
<td>오퍼레이션 번호</td>
<td>20</td>
<td>오퍼레이션명(국문)</td>
<td colspan="2">입찰공고목록 정보에 대한 e발주 첨부파일정보조회</td>
</tr>
<tr>
<td>오퍼레이션 유형</td>
<td>조회(목록)</td>
<td>오퍼레이션명(영문)</td>
<td colspan="2">getBidPblancListInfoEorderAtchFileInfo</td>
</tr>
<tr>
<td>오퍼레이션 설명</td>
<td colspan="4">검색조건에 등록일시범위(통합입찰공고)와 입찰공고번호를 입력하여 입찰공고번호, 입찰공고차수, 첨부순번, e발주문서구분명, e발주첨부파일명, e발주첨부파일URL 정보 조회</td>
</tr>
<tr>
<td>Call Back URL</td>
<td colspan="4">N/A</td>
</tr>
<tr>
<td>최대 메시지 사이즈</td>
<td colspan="4">[ 4000bytes]</td>
</tr>
<tr>
<td>평균 응답 시간</td>
<td>[ 500 ms]</td>
<td colspan="2">초당 최대 트랜잭션</td>
<td>[ 30 tps]</td>
</tr>
</tbody>
</table>

##### 요청 메시지 명세

<table>
<colgroup>
<col style="width: 19%" />
<col style="width: 19%" />
<col style="width: 13%" />
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 21%" />
</colgroup>
<tbody>
<tr>
<td>항목명(영문)</td>
<td>항목명(국문)</td>
<td>항목크기</td>
<td>항목구분</td>
<td>샘플데이터</td>
<td>항목설명</td>
</tr>
<tr>
<td>numOfRows</td>
<td>한 페이지 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td>10</td>
<td>한 페이지 결과 수</td>
</tr>
<tr>
<td>pageNo</td>
<td>페이지 번호</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td>1</td>
<td>페이지 번호</td>
</tr>
<tr>
<td>ServiceKey</td>
<td>서비스키</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">1</td>
<td>공공데이터포탈에서 받은 인증키</td>
<td>공공데이터포탈에서 받은 인증키</td>
</tr>
<tr>
<td>type</td>
<td>타입</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">0</td>
<td>json</td>
<td>오픈API 리턴 타입을 JSON으로 받고 싶을 경우 'json' 으로 지정</td>
</tr>
<tr>
<td>inqryDiv</td>
<td>조회구분</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td>1</td>
<td>검색하고자하는 조회구분<br />
1:등록일시 , 2.입찰공고번호</td>
</tr>
<tr>
<td>inqryBgnDt</td>
<td>조회시작일시(등록일시시작)</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td>202507010000</td>
<td>검색하고자하는 등록일시 조회시작일시 "YYYYMMDDHHMM"<br />
(조회구분 '1' 선택시 필수)</td>
</tr>
<tr>
<td>inqryEndDt</td>
<td>조회종료일시(등록일시끝)</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td>202507012359</td>
<td>검색하고자하는 등록일시 조회종료일시 "YYYYMMDDHHMM"<br />
(조회구분 '1' 선택시 필수)</td>
</tr>
<tr>
<td>bidNtceNo</td>
<td>입찰공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">0</td>
<td>R25BK00936446</td>
<td>검색하고자 하는 입찰공고번호<br />
(조회구분 '2' 선택시 필수)</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 응답 메시지 명세

<table style="width:100%;">
<colgroup>
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 13%" />
<col style="width: 11%" />
<col style="width: 13%" />
<col style="width: 21%" />
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
<td>resultCode</td>
<td>결과코드</td>
<td style="text-align: center;">2</td>
<td style="text-align: center;">1</td>
<td>00</td>
<td>결과코드</td>
</tr>
<tr>
<td>resultMsg</td>
<td>결과메세지</td>
<td style="text-align: center;">50</td>
<td style="text-align: center;">1</td>
<td>정상.</td>
<td>결과메세지</td>
</tr>
<tr>
<td>numOfRows</td>
<td>한 페이지 결과 수</td>
<td style="text-align: center;">4</td>
<td style="text-align: center;">1</td>
<td>10</td>
<td>한 페이지 결과 수</td>
</tr>
<tr>
<td>pageNo</td>
<td>페이지 번호</td>
<td style="text-align: center;">4</td>
<td style="text-align: center;">1</td>
<td>1</td>
<td>페이지 번호</td>
</tr>
<tr>
<td>totalCount</td>
<td>전체 결과 수</td>
<td style="text-align: center;">4</td>
<td style="text-align: center;">1</td>
<td>1</td>
<td>전체 결과 수</td>
</tr>
<tr>
<td>bidNtceNo</td>
<td>입찰공고번호</td>
<td style="text-align: center;">40</td>
<td style="text-align: center;">1</td>
<td>R25BK00936446</td>
<td style="text-align: left;"><p>입찰공고 관리번입찰공고 관리번호이며 조달청나라장터 공고건의 형식은 년도(4)+월(2)+순번(5)이며 자체전자조달시스템 보유기관은 각 기관별 형식 별도 사용</p>
<p>*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성</p>
<p>-단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</p></td>
</tr>
<tr>
<td>bidNtceOrd</td>
<td>입찰공고차수</td>
<td style="text-align: center;">3</td>
<td style="text-align: center;">1</td>
<td>000</td>
<td>입찰공고차수는 해당 입찰공고에 대한 재공고 및 재입찰 등이 발생되었을 경우 증가되는 수</td>
</tr>
<tr>
<td>atchSno</td>
<td>첨부순번</td>
<td style="text-align: center;">7</td>
<td style="text-align: center;">0</td>
<td>1</td>
<td>공고의 e발주 첨부파일 순번</td>
</tr>
<tr>
<td>eorderDocDivNm</td>
<td>e발주문서구분명</td>
<td style="text-align: center;">50</td>
<td style="text-align: center;">0</td>
<td>제안요청서</td>
<td>공고의 e발주 첨부파일 문서구분</td>
</tr>
<tr>
<td>eorderAtchFileNm</td>
<td>e발주첨부파일명</td>
<td style="text-align: center;">200</td>
<td style="text-align: center;">0</td>
<td>제안요청서_2025년 유가보조금관리시스템 고도화 사업2차 감리-(최종) (1).hwpx</td>
<td>공고의 e발주 첨부 파일명</td>
</tr>
<tr>
<td>eorderAtchFileUrl</td>
<td>e발주첨부파일URL</td>
<td style="text-align: center;">800</td>
<td style="text-align: center;">0</td>
<td>https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadRfpFile.do?rfpNo=R25DH00015274&amp;rfpOrd=000&amp;rfpUntyAtchFileNo=1</td>
<td>공고의 e발주 첨부파일 URL</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 요청 / 응답 메시지 예제

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr>
<td style="text-align: center;"><strong>REST(URI)</strong></td>
</tr>
<tr>
<td style="text-align: center;">http://apis.data.go.kr/1230000/ad/BidPublicInfoService/getBidPblancListInfoEorderAtchFileInfo?inqryDiv=2&amp;bidNtceNo= R25BK00936446&amp;bidNtceOrd=000&amp;pageNo=1&amp;numOfRows=10&amp;ServiceKey=인증키</td>
</tr>
<tr>
<td style="text-align: center;"><strong>응답 메시지</strong></td>
</tr>
<tr>
<td style="text-align: left;"><p>&lt;response&gt;</p>
<p>&lt;header&gt;</p>
<p>&lt;resultCode&gt;00&lt;/resultCode&gt;</p>
<p>&lt;resultMsg&gt;정상&lt;/resultMsg&gt;</p>
<p>&lt;/header&gt;</p>
<p>&lt;body&gt;</p>
<p>&lt;items&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00936446&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;atchSno&gt;1&lt;/atchSno&gt;</p>
<p>&lt;eorderDocDivNm&gt;제안요청서&lt;/eorderDocDivNm&gt;</p>
<p>&lt;eorderAtchFileNm&gt;제안요청서_2025년 유가보조금관리시스템 고도화 사업2차 감리-(최종) (1).hwpx&lt;/eorderAtchFileNm&gt;</p>
<p>&lt;eorderAtchFileUrl&gt;https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadRfpFile.do?rfpNo=R25DH00015274&amp;rfpOrd=000&amp;rfpUntyAtchFileNo=1&lt;/eorderAtchFileUrl&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;/items&gt;</p>
<p>&lt;numOfRows&gt;10&lt;/numOfRows&gt;</p>
<p>&lt;pageNo&gt;1&lt;/pageNo&gt;</p>
<p>&lt;totalCount&gt;1&lt;/totalCount&gt;</p>
<p>&lt;/body&gt;</p>
<p>&lt;/response&gt;</p></td>
</tr>
</tbody>
</table>

#### \[입찰공고목록 정보에 대한 기타공고조회\] 오퍼레이션 명세

<table>
<colgroup>
<col style="width: 4%" />
<col style="width: 21%" />
<col style="width: 17%" />
<col style="width: 21%" />
<col style="width: 2%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr>
<td rowspan="6">오퍼레이션 정보</td>
<td>오퍼레이션 번호</td>
<td>21</td>
<td>오퍼레이션명(국문)</td>
<td colspan="2">입찰공고목록 정보에 대한 기타공고조회</td>
</tr>
<tr>
<td>오퍼레이션 유형</td>
<td>조회(목록)</td>
<td>오퍼레이션명(영문)</td>
<td colspan="2">getBidPblancListInfoEtc</td>
</tr>
<tr>
<td>오퍼레이션 설명</td>
<td colspan="4">검색조건에 등록일시, 입찰공고번호를 입력하여 나라장터의 입찰공고번호, 공고명, 발주기관, 수요기관, 계약체결방법명 등 기타공고정보를 조회</td>
</tr>
<tr>
<td>Call Back URL</td>
<td colspan="4">N/A</td>
</tr>
<tr>
<td>최대 메시지 사이즈</td>
<td colspan="4">[ 4000bytes]</td>
</tr>
<tr>
<td>평균 응답 시간</td>
<td>[ 500 ms]</td>
<td colspan="2">초당 최대 트랜잭션</td>
<td>[ 30 tps]</td>
</tr>
</tbody>
</table>

##### 요청 메시지 명세

<table>
<colgroup>
<col style="width: 19%" />
<col style="width: 19%" />
<col style="width: 13%" />
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 21%" />
</colgroup>
<tbody>
<tr>
<td>항목명(영문)</td>
<td>항목명(국문)</td>
<td>항목크기</td>
<td>항목구분</td>
<td>샘플데이터</td>
<td>항목설명</td>
</tr>
<tr>
<td>numOfRows</td>
<td>한 페이지 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td>10</td>
<td>한 페이지 결과 수</td>
</tr>
<tr>
<td>pageNo</td>
<td>페이지 번호</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td>1</td>
<td>페이지 번호</td>
</tr>
<tr>
<td>ServiceKey</td>
<td>서비스키</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">1</td>
<td>공공데이터포탈에서 받은 인증키</td>
<td>공공데이터포탈에서 받은 인증키</td>
</tr>
<tr>
<td>type</td>
<td>타입</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">0</td>
<td>json</td>
<td>오픈API 리턴 타입을 JSON으로 받고 싶을 경우 'json' 으로 지정</td>
</tr>
<tr>
<td>inqryDiv</td>
<td>조회구분</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td>1</td>
<td>검색하고자하는 조회구분<br />
1:등록일시 , 2.입찰공고번호</td>
</tr>
<tr>
<td>inqryBgnDt</td>
<td>조회시작일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td>202507010000</td>
<td>검색하고자하는 등록일시 조회시작일시 "YYYYMMDDHHMM"<br />
(조회구분 '1' 선택시 필수)</td>
</tr>
<tr>
<td>inqryEndDt</td>
<td>조회종료일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td>202507012359</td>
<td>검색하고자하는 등록일시 조회종료일시 "YYYYMMDDHHMM"<br />
(조회구분 '1' 선택시 필수)</td>
</tr>
<tr>
<td>bidNtceNo</td>
<td>입찰공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">0</td>
<td>R25BK00935328</td>
<td>검색하고자 하는 입찰공고번호<br />
(조회구분 '2' 선택시 필수)</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 응답 메시지 명세

<table>
<colgroup>
<col style="width: 20%" />
<col style="width: 18%" />
<col style="width: 14%" />
<col style="width: 13%" />
<col style="width: 13%" />
<col style="width: 19%" />
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
<td style="text-align: left;">resultCode</td>
<td style="text-align: left;">결과코드</td>
<td style="text-align: left;">2</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">00</td>
<td style="text-align: left;">결과코드</td>
</tr>
<tr>
<td style="text-align: left;">resultMsg</td>
<td style="text-align: left;">결과메세지</td>
<td style="text-align: left;">50</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">정상</td>
<td style="text-align: left;">결과메세지</td>
</tr>
<tr>
<td style="text-align: left;">numOfRows</td>
<td style="text-align: left;">한 페이지 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td style="text-align: left;">pageNo</td>
<td style="text-align: left;">페이지 번호</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">페이지 번호</td>
</tr>
<tr>
<td style="text-align: left;">totalCount</td>
<td style="text-align: left;">전체 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">전체 결과 수</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNo</td>
<td style="text-align: left;">입찰공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">R25BK00935328</td>
<td style="text-align: left;"><p>입찰공고 관리번입찰공고 관리번호이며 조달청나라장터 공고건의 형식은 년도(4)+월(2)+순번(5)이며 자체전자조달시스템 보유기관은 각 기관별 형식 별도 사용</p>
<p>*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성</p>
<p>-단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</p></td>
</tr>
<tr>
<td style="text-align: left;">bidNtceOrd</td>
<td style="text-align: left;">입찰공고차수</td>
<td style="text-align: left;">3</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">000</td>
<td style="text-align: left;">입찰공고차수는 해당 입찰공고에 대한 재공고 및 재입찰 등이 발생되었을 경우 증가되는 수</td>
</tr>
<tr>
<td style="text-align: left;">rgstTyNm</td>
<td style="text-align: left;">등록유형명</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">나라장터 기타 공고건</td>
<td style="text-align: left;">입찰공고가 "조달청 또는 나라장터 자체 공고건","'나라장터 기타 공고건"</td>
</tr>
<tr>
<td style="text-align: left;">ntceKindNm</td>
<td style="text-align: left;">공고종류명</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">등록공고</td>
<td style="text-align: left;">공고의 공고상태명으로 등록공고, 변경공고, 취소공고, 재공고 구분</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceDt</td>
<td style="text-align: left;">입찰공고일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-01 10:57</td>
<td style="text-align: left;">입찰공고서를 공고한 일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">refNo</td>
<td style="text-align: left;">참조번호</td>
<td style="text-align: left;">105</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N/A</td>
<td style="text-align: left;">조달청 입찰공고의 경우 참조공고번호는 자체 전자조달시스템에서 관리하는 공고번호를 의미하며 자체전자조달시스템의 경우 참조공고번호는 나라장터(G2B) 입찰공고번호를 의미함</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNm</td>
<td style="text-align: left;">입찰공고명</td>
<td style="text-align: left;">1000</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">임실치즈농협 1공장 분쇄라인 설비 교체, 훈연치즈 삼면포장기 설치 사업</td>
<td style="text-align: left;">공사명 또는 사업명이라고도 하며 입찰공고 내용을 요약한 이름</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttCd</td>
<td style="text-align: left;">공고기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">Z009205</td>
<td style="text-align: left;">공고를 하는 기관의 코드로 행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드가 행자부코드가 없는 경우 조달청에서 부여한 공고기관 코드가 표기됨</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttNm</td>
<td style="text-align: left;">공고기관명</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">임실치즈축산업협동조합</td>
<td style="text-align: left;">수요기관의 의뢰를 받아 공고하는 기관의 명</td>
</tr>
<tr>
<td style="text-align: left;">dminsttNm</td>
<td style="text-align: left;">수요기관명</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">임실치즈축산업협동조합</td>
<td style="text-align: left;">계약을 의뢰한 기관의 명으로 공고기관과 수요기관이 동일할 수 있음</td>
</tr>
<tr>
<td style="text-align: left;">bidMethdNm</td>
<td style="text-align: left;">입찰방식명</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">직찰</td>
<td style="text-align: left;">공고의 입찰방식명 직찰<br />
전자입찰,전자입찰/직찰,전자/직찰/우편/상시,직찰/우편/상시,우편/상시,전자시담,복수견적(역경매),직찰/우편,전자시담(다자간)</td>
</tr>
<tr>
<td style="text-align: left;">cntrctCnclsMthdNm</td>
<td style="text-align: left;">계약체결방법명</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">공고서참고</td>
<td style="text-align: left;">계약체결의 방법을 구분하는 명<br />
*일반경쟁계약은 계약 대상 물품의 규격 및 시방서와 계약조건 등을 널리 공고하여 일정한 자격을 가진 불특정 다수인의 입찰희망자를 모두 경쟁 입찰하는 계약방법<br />
*제한경쟁계약은 일반·지명경쟁계약제도의 단점을 보완하기 위해 실적제한, 기술보유제한, 특정물품제한, 지역제한 등을 두는 계약방법<br />
*지명경쟁계약은 계약상대자의 신용과 실적 등에 있어 적당하다고 인정하는 특정 다수의 경쟁 참가자를 지명하여 계약 상대방을 결정하는 계약방법<br />
*수의계약은 계약상대자를 결정함에 있어 경쟁방법에 의하지 않고 특정인을 선정하여 계약하는 계약방법</td>
</tr>
<tr>
<td style="text-align: left;">bidBeginDt</td>
<td style="text-align: left;">입찰개시일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-01 10:57</td>
<td style="text-align: left;">입찰서의 제출을 개시하는 일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">bidClseDt</td>
<td style="text-align: left;">입찰마감일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-23 15:00</td>
<td style="text-align: left;">입찰서의 제출을 마감하는 일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">opengDt</td>
<td style="text-align: left;">개찰일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-23 15:00</td>
<td style="text-align: left;">집행관이 개찰을 수행할 수 있는 시작일시이며<br />
개찰일시 이후에 개찰이 가능함<br />
실제 개찰을 수행한 시간을 의미하지 않음 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl1</td>
<td style="text-align: left;">공고규격서URL1</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00935328&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=1&amp;prcmBsneSeCd=09</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl2</td>
<td style="text-align: left;">공고규격서URL2</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00935328&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=2&amp;prcmBsneSeCd=09</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl3</td>
<td style="text-align: left;">공고규격서URL3</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00935328&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=3&amp;prcmBsneSeCd=09</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl4</td>
<td style="text-align: left;">공고규격서URL4</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00935328&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=4&amp;prcmBsneSeCd=09</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl5</td>
<td style="text-align: left;">공고규격서URL5</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00935328&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=5&amp;prcmBsneSeCd=09</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm1</td>
<td style="text-align: left;">공고규격파일명1</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">붙임1.입찰공고문(협상에 의한 계약).hwp</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm2</td>
<td style="text-align: left;">공고규격파일명2</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">붙임2.제안요청서(협상에 의한 계약).hwp</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm3</td>
<td style="text-align: left;">공고규격파일명3</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">붙임2.제안요청서(협상에 의한 계약).hwp</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm4</td>
<td style="text-align: left;">공고규격파일명4</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">붙임2.제안요청서(협상에 의한 계약).hwp</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm5</td>
<td style="text-align: left;">공고규격파일명5</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">붙임2.제안요청서(협상에 의한 계약).hwp</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">rbidPermsnYn</td>
<td style="text-align: left;">재입찰허용여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">입찰이 유찰되는 경우 재공고 없이 다시 입찰허용 여부(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">presmptPrce</td>
<td style="text-align: left;">추정가격</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">계약을 체결함에 있어 국제입찰 대상여부를 판단하는 기준 등으로 삼기 위하여 예정가격이 결정되기 전에 예산에 계상된 금액 등을 기준으로 하여 부가가치세 및 조달 수수료를 제외한 금액(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">opengPlce</td>
<td style="text-align: left;">개찰장소</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">임실치즈농협 본점 3층 회의실</td>
<td style="text-align: left;">집행관이 개찰을 하는 장소</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceDtlUrl</td>
<td style="text-align: left;">입찰공고상세URL</td>
<td style="text-align: left;">512</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/link/PNPE027_01/single/?bidPbancNo=R25BK00935328&amp;bidPbancOrd=000&amp;prcmBsneSeCd=09&amp;pbancType=pbanc&lt;</td>
<td style="text-align: left;">나라장터시스템의 입찰공고 상세화면 링크</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceUrl</td>
<td style="text-align: left;">입찰공고URL</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/link/PNPE027_01/single/?bidPbancNo=R25BK00935328&amp;bidPbancOrd=000&amp;prcmBsneSeCd=09&amp;pbancType=pbanc&lt;</td>
<td style="text-align: left;">해당 입찰공고를 인터넷상에서 확인할 수 있는 URL주소</td>
</tr>
<tr>
<td style="text-align: left;">bidPrtcptFee</td>
<td style="text-align: left;">입찰참가수수료</td>
<td style="text-align: left;">21</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">입찰에 참가하기위해 납부하는 수수료(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">bidGrntymnyPaymntObjYn</td>
<td style="text-align: left;">입찰보증금납부대상여부</td>
<td style="text-align: left;">30</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">Y</td>
<td style="text-align: left;">입찰보증금을 납부대상 여부(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">untyNtceNo</td>
<td style="text-align: left;">통합공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25BM00300744</td>
<td style="text-align: left;">입찰공고를 구분하는 번호로 입찰공고번호이며 형식은 년도(4)+월(2)+순번(5)<br />
*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성<br />
- 단계구분: BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격), BK(통합입찰)</td>
</tr>
<tr>
<td style="text-align: left;">cmmnSpldmdYn</td>
<td style="text-align: left;">공동수급여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">공동수급이라 함은 구성원을 2인 이상으로 하여 수급인이 해당계약을 공동으로 수행하기 위하여 잠정적으로 결성한 실체를 의미하며 공동수급체가도급을 받아 이행하는 방식으로 여부(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">bidQlfctRgstCntnts</td>
<td style="text-align: left;">입찰참가자격내용</td>
<td style="text-align: left;">4000</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;"><p>&gt;제안요청서</p>
<p>Ⅱ. 입찰계획 2.참가자격의 요건을 갖춘자</p></td>
<td style="text-align: left;">공고의 투찰 참가자격 내용</td>
</tr>
<tr>
<td style="text-align: left;">rgstDt</td>
<td style="text-align: left;">등록일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">2025-07-01 10:57</td>
<td style="text-align: left;">공고의 등록일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">sucsfbidMthdNm</td>
<td style="text-align: left;">낙찰방법명</td>
<td style="text-align: left;">700</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">공고서참조</td>
<td style="text-align: left;">낙찰자를 결정하는 방법-낙찰방법 세부기준</td>
</tr>
<tr>
<td style="text-align: left;">rmrkCntnts</td>
<td style="text-align: left;">비고내용</td>
<td style="text-align: left;">4000</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">기타 세부사항은 공고문 및 제안서를 참고하시기 바랍니다.</td>
<td style="text-align: left;">공고서의 비고 내용</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 요청 / 응답 메시지 예제

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr>
<td style="text-align: center;"><strong>REST(URI)</strong></td>
</tr>
<tr>
<td style="text-align: center;">http://apis.data.go.kr/1230000/ad/BidPublicInfoService/getBidPblancListInfoEorderAtchFileInfo?inqryDiv=2&amp;bidNtceNo= R25BK00935328&amp;bidNtceOrd=000&amp;pageNo=1&amp;numOfRows=10&amp;ServiceKey=인증키</td>
</tr>
<tr>
<td style="text-align: center;"><strong>응답 메시지</strong></td>
</tr>
<tr>
<td style="text-align: left;"><p>&lt;response&gt;</p>
<p>&lt;header&gt;</p>
<p>&lt;resultCode&gt;00&lt;/resultCode&gt;</p>
<p>&lt;resultMsg&gt;정상&lt;/resultMsg&gt;</p>
<p>&lt;/header&gt;</p>
<p>&lt;body&gt;</p>
<p>&lt;items&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00935328&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;untyNtceNo&gt;R25BM00300744&lt;/untyNtceNo&gt;</p>
<p>&lt;rgstTyNm&gt;나라장터 기타 공고건&lt;/rgstTyNm&gt;</p>
<p>&lt;ntceKindNm&gt;등록공고&lt;/ntceKindNm&gt;</p>
<p>&lt;bidNtceDt&gt;2025-07-01 10:57&lt;/bidNtceDt&gt;</p>
<p>&lt;refNo&gt;&lt;/refNo&gt;</p>
<p>&lt;bidNtceNm&gt;임실치즈농협 1공장 분쇄라인 설비 교체, 훈연치즈 삼면포장기 설치 사업&lt;/bidNtceNm&gt;</p>
<p>&lt;ntceInsttCd&gt;Z009205&lt;/ntceInsttCd&gt;</p>
<p>&lt;ntceInsttNm&gt;임실치즈축산업협동조합&lt;/ntceInsttNm&gt;</p>
<p>&lt;dminsttNm&gt;임실치즈축산업협동조합&lt;/dminsttNm&gt;</p>
<p>&lt;rbidPermsnYn&gt;N&lt;/rbidPermsnYn&gt;</p>
<p>&lt;bidMethdNm&gt;직찰&lt;/bidMethdNm&gt;</p>
<p>&lt;cntrctCnclsMthdNm&gt;&lt;/cntrctCnclsMthdNm&gt;</p>
<p>&lt;cmmnSpldmdYn&gt;N&lt;/cmmnSpldmdYn&gt;</p>
<p>&lt;bidBeginDt&gt;&lt;/bidBeginDt&gt;</p>
<p>&lt;bidClseDt&gt;&lt;/bidClseDt&gt;</p>
<p>&lt;sucsfbidMthdNm&gt;공고서참조&lt;/sucsfbidMthdNm&gt;</p>
<p>&lt;opengDt&gt;2025-07-23 15:00&lt;/opengDt&gt;</p>
<p>&lt;opengPlce&gt;임실치즈농협 본점 3층 회의실&lt;/opengPlce&gt;</p>
<p>&lt;bidQlfctRgstCntnts&gt;제안요청서</p>
<p>Ⅱ. 입찰계획 2.참가자격의 요건을 갖춘자</p>
<p>&lt;/bidQlfctRgstCntnts&gt;</p>
<p>&lt;bidPrtcptFee&gt;0&lt;/bidPrtcptFee&gt;</p>
<p>&lt;bidGrntymnyPaymntObjYn&gt;Y&lt;/bidGrntymnyPaymntObjYn&gt;</p>
<p>&lt;bidNtceDtlUrl&gt;https://www.g2b.go.kr/link/PNPE027_01/single/?bidPbancNo=R25BK00935328&amp;bidPbancOrd=000&amp;prcmBsneSeCd=09&amp;pbancType=pbanc&lt;/bidNtceDtlUrl&gt;</p>
<p>&lt;bidNtceUrl&gt;https://www.g2b.go.kr/link/PNPE027_01/single/?bidPbancNo=R25BK00935328&amp;bidPbancOrd=000&amp;prcmBsneSeCd=09&amp;pbancType=pbanc&lt;/bidNtceUrl&gt;</p>
<p>&lt;ntceSpecDocUrl1&gt;https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00935328&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=1&amp;prcmBsneSeCd=09&lt;/ntceSpecDocUrl1&gt;</p>
<p>&lt;ntceSpecDocUrl2&gt;https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00935328&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=2&amp;prcmBsneSeCd=09&lt;/ntceSpecDocUrl2&gt;</p>
<p>&lt;ntceSpecDocUrl3&gt;&lt;/ntceSpecDocUrl3&gt;</p>
<p>&lt;ntceSpecDocUrl4&gt;&lt;/ntceSpecDocUrl4&gt;</p>
<p>&lt;ntceSpecDocUrl5&gt;&lt;/ntceSpecDocUrl5&gt;</p>
<p>&lt;ntceSpecFileNm1&gt;붙임1.입찰공고문(협상에 의한 계약).hwp&lt;/ntceSpecFileNm1&gt;</p>
<p>&lt;ntceSpecFileNm2&gt;붙임2.제안요청서(협상에 의한 계약).hwp&lt;/ntceSpecFileNm2&gt;</p>
<p>&lt;ntceSpecFileNm3&gt;&lt;/ntceSpecFileNm3&gt;</p>
<p>&lt;ntceSpecFileNm4&gt;&lt;/ntceSpecFileNm4&gt;</p>
<p>&lt;ntceSpecFileNm5&gt;&lt;/ntceSpecFileNm5&gt;</p>
<p>&lt;presmptPrce&gt;&lt;/presmptPrce&gt;</p>
<p>&lt;rmrkCntnts&gt;기타 세부사항은 공고문 및 제안서를 참고하시기 바랍니다.&lt;/rmrkCntnts&gt;</p>
<p>&lt;rgstDt&gt;2025-07-01 10:57&lt;/rgstDt&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;/items&gt;</p>
<p>&lt;numOfRows&gt;10&lt;/numOfRows&gt;</p>
<p>&lt;pageNo&gt;1&lt;/pageNo&gt;</p>
<p>&lt;totalCount&gt;1&lt;/totalCount&gt;</p>
<p>&lt;/body&gt;</p>
<p>&lt;/response&gt;</p></td>
</tr>
</tbody>
</table>

#### \
\[나라장터검색조건에 의한 입찰공고 기타조회\] 오퍼레이션 명세

<table>
<colgroup>
<col style="width: 4%" />
<col style="width: 21%" />
<col style="width: 17%" />
<col style="width: 21%" />
<col style="width: 2%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr>
<td rowspan="6">오퍼레이션 정보</td>
<td>오퍼레이션 번호</td>
<td>22</td>
<td>오퍼레이션명(국문)</td>
<td colspan="2">나라장터검색조건에 의한 입찰공고 기타조회</td>
</tr>
<tr>
<td>오퍼레이션 유형</td>
<td>조회(목록)</td>
<td>오퍼레이션명(영문)</td>
<td colspan="2">getBidPblancListInfoEtcPPSSrch</td>
</tr>
<tr>
<td>오퍼레이션 설명</td>
<td colspan="4">검색조건에 공고게시일시, 개찰일시 범위, 공고기관, 수요기관, 참조번호 등을 입력하여 나라장터의 입찰공고번호, 공고명, 발주기관, 수요기관, 계약체결방법명 등 공사부분의 입찰공고정보를 조회함</td>
</tr>
<tr>
<td>Call Back URL</td>
<td colspan="4">N/A</td>
</tr>
<tr>
<td>최대 메시지 사이즈</td>
<td colspan="4">[ 4000bytes]</td>
</tr>
<tr>
<td>평균 응답 시간</td>
<td>[ 500 ms]</td>
<td colspan="2">초당 최대 트랜잭션</td>
<td>[ 30 tps]</td>
</tr>
</tbody>
</table>

##### 요청 메시지 명세

<table>
<colgroup>
<col style="width: 19%" />
<col style="width: 19%" />
<col style="width: 13%" />
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 21%" />
</colgroup>
<tbody>
<tr>
<td style="text-align: left;">항목명(영문)</td>
<td style="text-align: left;">항목명(국문)</td>
<td style="text-align: left;">항목크기</td>
<td style="text-align: left;">항목구분</td>
<td style="text-align: left;">샘플데이터</td>
<td style="text-align: left;">항목설명</td>
</tr>
<tr>
<td style="text-align: left;">numOfRows</td>
<td style="text-align: left;">한 페이지 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td style="text-align: left;">pageNo</td>
<td style="text-align: left;">페이지 번호</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">페이지 번호</td>
</tr>
<tr>
<td style="text-align: left;">ServiceKey</td>
<td style="text-align: left;">서비스키</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">공공데이터포탈에서 받은 인증키</td>
<td style="text-align: left;">공공데이터포탈에서 받은 인증키</td>
</tr>
<tr>
<td style="text-align: left;">type</td>
<td style="text-align: left;">타입</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">json</td>
<td style="text-align: left;">오픈API 리턴 타입을 JSON으로 받고 싶을 경우 'json' 으로 지정</td>
</tr>
<tr>
<td style="text-align: left;">inqryDiv</td>
<td style="text-align: left;">조회구분</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">검색하고자하는 조회구분<br />
1:공고게시일시, 2:개찰일시</td>
</tr>
<tr>
<td style="text-align: left;">inqryBgnDt</td>
<td style="text-align: left;">조회시작일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">202507010000</td>
<td style="text-align: left;">검색하고자 하는 조회시작일시 "YYYYMMDDHHMM"<br />
조회구분이 '1'인 경우 공고게시일시 필수, '2'인 경우 개찰일시 필수</td>
</tr>
<tr>
<td style="text-align: left;">inqryEndDt</td>
<td style="text-align: left;">조회종료일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">202507012359</td>
<td style="text-align: left;">검색하고자 하는 조회종료일시 "YYYYMMDDHHMM"<br />
조회구분이 '1'인 경우 공고게시일시 필수, '2'인 경우 개찰일시 필수</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNm</td>
<td style="text-align: left;">입찰공고명</td>
<td style="text-align: left;">1000</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">백업소프트웨어 구매업체 선정 입찰</td>
<td style="text-align: left;">검색하고자하는 공고명<br />
※ 공고명 일부 입력시에도 조회 가능</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttCd</td>
<td style="text-align: left;">공고기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">7001966</td>
<td style="text-align: left;">검색하고자하는 공고기관코드</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttNm</td>
<td style="text-align: left;">공고기관명</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">아주대학교</td>
<td style="text-align: left;">검색하고자하는 공고기관명<br />
※ 공고기관명 일부 입력시에도 조회 가능</td>
</tr>
<tr>
<td style="text-align: left;">dminsttNm</td>
<td style="text-align: left;">수요기관명</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">아주대학교</td>
<td style="text-align: left;">검색하고자하는 수요기관명<br />
※ 수요기관명 일부 입력시에도 조회 가능</td>
</tr>
<tr>
<td style="text-align: left;">refNo</td>
<td style="text-align: left;">참조번호</td>
<td style="text-align: left;">105</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">아주대학교5051</td>
<td style="text-align: left;">검색하고자하는 참조번호</td>
</tr>
<tr>
<td style="text-align: left;">presmptPrceBgn</td>
<td style="text-align: left;">추정가격시작</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">검색하고자하는 추정가격범위시작금액이상(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">presmptPrceEnd</td>
<td style="text-align: left;">추정가격종료</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">검색하고자하는 추정가격범위종료금액이하(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">bidClseExcpYn</td>
<td style="text-align: left;">입찰마감제외여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">검색하고자하는 입찰마감제외여부</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 응답 메시지 명세

<table>
<colgroup>
<col style="width: 20%" />
<col style="width: 18%" />
<col style="width: 14%" />
<col style="width: 13%" />
<col style="width: 13%" />
<col style="width: 19%" />
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
<td style="text-align: left;">resultCode</td>
<td style="text-align: left;">결과코드</td>
<td style="text-align: left;">2</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">00</td>
<td style="text-align: left;">결과코드</td>
</tr>
<tr>
<td style="text-align: left;">resultMsg</td>
<td style="text-align: left;">결과메세지</td>
<td style="text-align: left;">50</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">정상</td>
<td style="text-align: left;">결과메세지</td>
</tr>
<tr>
<td style="text-align: left;">numOfRows</td>
<td style="text-align: left;">한 페이지 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td style="text-align: left;">pageNo</td>
<td style="text-align: left;">페이지 번호</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">페이지 번호</td>
</tr>
<tr>
<td style="text-align: left;">totalCount</td>
<td style="text-align: left;">전체 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">전체 결과 수</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNo</td>
<td style="text-align: left;">입찰공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">R25BK00935310</td>
<td style="text-align: left;"><p>입찰공고 관리번입찰공고 관리번호이며 조달청나라장터 공고건의 형식은 년도(4)+월(2)+순번(5)이며 자체전자조달시스템 보유기관은 각 기관별 형식 별도 사용</p>
<p>*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성</p>
<p>-단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</p></td>
</tr>
<tr>
<td style="text-align: left;">bidNtceOrd</td>
<td style="text-align: left;">입찰공고차수</td>
<td style="text-align: left;">3</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">000</td>
<td style="text-align: left;">입찰공고차수는 해당 입찰공고에 대한 재공고 및 재입찰 등이 발생되었을 경우 증가되는 수</td>
</tr>
<tr>
<td style="text-align: left;">rgstTyNm</td>
<td style="text-align: left;">등록유형명</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">나라장터 기타 공고건</td>
<td style="text-align: left;">입찰공고가 "조달청 또는 나라장터 자체 공고건","'나라장터 기타 공고건"</td>
</tr>
<tr>
<td style="text-align: left;">ntceKindNm</td>
<td style="text-align: left;">공고종류명</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">등록공고</td>
<td style="text-align: left;">공고의 공고상태명으로 등록공고, 변경공고, 취소공고, 재공고 구분</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceDt</td>
<td style="text-align: left;">입찰공고일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-01 10:41</td>
<td style="text-align: left;">입찰공고서를 공고한 일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">refNo</td>
<td style="text-align: left;">참조번호</td>
<td style="text-align: left;">105</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">아주대학교5051</td>
<td style="text-align: left;">조달청 입찰공고의 경우 참조공고번호는 자체 전자조달시스템에서 관리하는 공고번호를 의미하며 자체전자조달시스템의 경우 참조공고번호는 나라장터(G2B) 입찰공고번호를 의미함</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNm</td>
<td style="text-align: left;">입찰공고명</td>
<td style="text-align: left;">1000</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">백업소프트웨어 구매업체 선정 입찰</td>
<td style="text-align: left;">공사명 또는 사업명이라고도 하며 입찰공고 내용을 요약한 이름</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttCd</td>
<td style="text-align: left;">공고기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">7001966</td>
<td style="text-align: left;">공고를 하는 기관의 코드로 행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드가 행자부코드가 없는 경우 조달청에서 부여한 공고기관 코드가 표기됨</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttNm</td>
<td style="text-align: left;">공고기관명</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">아주대학교</td>
<td style="text-align: left;">수요기관의 의뢰를 받아 공고하는 기관의 명</td>
</tr>
<tr>
<td style="text-align: left;">dminsttNm</td>
<td style="text-align: left;">수요기관명</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">아주대학교</td>
<td style="text-align: left;">계약을 의뢰한 기관의 명으로 공고기관과 수요기관이 동일할 수 있음</td>
</tr>
<tr>
<td style="text-align: left;">bidMethdNm</td>
<td style="text-align: left;">입찰방식명</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">직찰</td>
<td style="text-align: left;">공고의 입찰방식명 직찰<br />
전자입찰,전자입찰/직찰,전자/직찰/우편/상시,직찰/우편/상시,우편/상시,전자시담,복수견적(역경매),직찰/우편,전자시담(다자간)</td>
</tr>
<tr>
<td style="text-align: left;">cntrctCnclsMthdNm</td>
<td style="text-align: left;">계약체결방법명</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">제한경쟁</td>
<td style="text-align: left;">계약체결의 방법을 구분하는 명<br />
*일반경쟁계약은 계약 대상 물품의 규격 및 시방서와 계약조건 등을 널리 공고하여 일정한 자격을 가진 불특정 다수인의 입찰희망자를 모두 경쟁 입찰하는 계약방법<br />
*제한경쟁계약은 일반·지명경쟁계약제도의 단점을 보완하기 위해 실적제한, 기술보유제한, 특정물품제한, 지역제한 등을 두는 계약방법<br />
*지명경쟁계약은 계약상대자의 신용과 실적 등에 있어 적당하다고 인정하는 특정 다수의 경쟁 참가자를 지명하여 계약 상대방을 결정하는 계약방법<br />
*수의계약은 계약상대자를 결정함에 있어 경쟁방법에 의하지 않고 특정인을 선정하여 계약하는 계약방법</td>
</tr>
<tr>
<td style="text-align: left;">bidBeginDt</td>
<td style="text-align: left;">입찰개시일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-01 10:41</td>
<td style="text-align: left;">입찰서의 제출을 개시하는 일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">bidClseDt</td>
<td style="text-align: left;">입찰마감일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-09 12:00</td>
<td style="text-align: left;">입찰서의 제출을 마감하는 일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">opengDt</td>
<td style="text-align: left;">개찰일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-09 14:00</td>
<td style="text-align: left;">집행관이 개찰을 수행할 수 있는 시작일시이며<br />
개찰일시 이후에 개찰이 가능함<br />
실제 개찰을 수행한 시간을 의미하지 않음 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl1</td>
<td style="text-align: left;">공고규격서URL1</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00935310&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=1&amp;prcmBsneSeCd=09</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl2</td>
<td style="text-align: left;">공고규격서URL2</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00935310&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=2&amp;prcmBsneSeCd=09</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl3</td>
<td style="text-align: left;">공고규격서URL3</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00935310&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=3&amp;prcmBsneSeCd=09</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl4</td>
<td style="text-align: left;">공고규격서URL4</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00935310&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=4&amp;prcmBsneSeCd=09</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecDocUrl5</td>
<td style="text-align: left;">공고규격서URL5</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00935310&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=5&amp;prcmBsneSeCd=09</td>
<td style="text-align: left;">공고의 공고규격서URL</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm1</td>
<td style="text-align: left;">공고규격파일명1</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">1._입찰공고_및_관련서류.hwp</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm2</td>
<td style="text-align: left;">공고규격파일명2</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2. 아주대학교_정보시스템 소규모DR센터 고도화_백업소프트웨어 개선_과업지시서.hwp</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm3</td>
<td style="text-align: left;">공고규격파일명3</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">3. 물품규격서(백업소프트웨어).hwp</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm4</td>
<td style="text-align: left;">공고규격파일명4</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">4. 사양(규격)검토확인서.hwp</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">ntceSpecFileNm5</td>
<td style="text-align: left;">공고규격파일명5</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">5. 사양(규격)검토확인서.hwp</td>
<td style="text-align: left;">공고의 공고규격파일명</td>
</tr>
<tr>
<td style="text-align: left;">rbidPermsnYn</td>
<td style="text-align: left;">재입찰허용여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">입찰이 유찰되는 경우 재공고 없이 다시 입찰허용 여부(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">presmptPrce</td>
<td style="text-align: left;">추정가격</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">계약을 체결함에 있어 국제입찰 대상여부를 판단하는 기준 등으로 삼기 위하여 예정가격이 결정되기 전에 예산에 계상된 금액 등을 기준으로 하여 부가가치세 및 조달 수수료를 제외한 금액(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">opengPlce</td>
<td style="text-align: left;">개찰장소</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">글로컬캠퍼스 내 지정입찰장</td>
<td style="text-align: left;">집행관이 개찰을 하는 장소</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceDtlUrl</td>
<td style="text-align: left;">입찰공고상세URL</td>
<td style="text-align: left;">512</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/link/PNPE027_01/single/?bidPbancNo=R25BK00935310&amp;bidPbancOrd=000&amp;prcmBsneSeCd=09&amp;pbancType=pbanc</td>
<td style="text-align: left;">나라장터시스템의 입찰공고 상세화면 링크</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceUrl</td>
<td style="text-align: left;">입찰공고URL</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">https://www.g2b.go.kr/link/PNPE027_01/single/?bidPbancNo=R25BK00935310&amp;bidPbancOrd=000&amp;prcmBsneSeCd=09&amp;pbancType=pbanc</td>
<td style="text-align: left;">해당 입찰공고를 인터넷상에서 확인할 수 있는 URL주소</td>
</tr>
<tr>
<td style="text-align: left;">bidPrtcptFee</td>
<td style="text-align: left;">입찰참가수수료</td>
<td style="text-align: left;">21</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">입찰에 참가하기위해 납부하는 수수료(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">bidGrntymnyPaymntObjYn</td>
<td style="text-align: left;">입찰보증금납부대상여부</td>
<td style="text-align: left;">30</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">입찰보증금을 납부대상 여부(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">untyNtceNo</td>
<td style="text-align: left;">통합공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25BM00300704</td>
<td style="text-align: left;">입찰공고를 구분하는 번호로 입찰공고번호이며 형식은 년도(4)+월(2)+순번(5)<br />
*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성<br />
- 단계구분: BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격), BK(통합입찰)</td>
</tr>
<tr>
<td style="text-align: left;">cmmnSpldmdYn</td>
<td style="text-align: left;">공동수급여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">공동수급이라 함은 구성원을 2인 이상으로 하여 수급인이 해당계약을 공동으로 수행하기 위하여 잠정적으로 결성한 실체를 의미하며 공동수급체가도급을 받아 이행하는 방식으로 여부(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">bidQlfctRgstCntnts</td>
<td style="text-align: left;">입찰참가자격내용</td>
<td style="text-align: left;">4000</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;"><p>입찰참가자격 (아래 입찰참가자격을 모두 만족시키는 업체만 입찰참가 가능함)</p>
<p>가. 국가를 당사로 하는 계약에 관한 법률 시행령 제12조 및 동법 시행규칙 제14조 규정에 의한 경쟁입찰 참가 자격을 갖춘 자</p>
<p>나. 국가를 당사자로 하는 계약에 관한 법률 시행령 제76조(부정당업자의 입찰참가 자격제한)에 의한 결격사유가 없는 자</p>
<p>다. 정보통신공사업법 제 14조에 의해 정보통신공사업을 등록한 사업자 및 소트웨어진흥법 제24조에 의한 소프트웨어(컴퓨터관련서비스산업) 사업자</p>
<p>라. 물품 수요자로부터 사양 검토확인을 득한 업체(본교에서 제공하는 설계서 확인 필)</p>
<p>마. 전년도 매출액이 100억/년 이상(2024년도 표준재무제표증명 제출)</p>
<p>바. 공고일 기준 최근 3년간 시스템 구축 이행 실적이 1건 이상(국내 4년제 대학교 및 공공기관 대상)이며 각 계약 금액이 건당 1억원 이상인 업체(실적증명서 제출)</p>
<p>사. 사업장 소재지가 서울, 경기, 인천 지역인 업체</p>
<p>※ 공동 수급 불허</p>
<p>※ 사업수행자는 계약 후 10일 이내에 납품물품명세서(부품별 단가 명시), 제조사 기술지원확약서, 착수계, 보안서약서를 제출하여야 함</p></td>
<td style="text-align: left;">공고의 투찰 참가자격 내용</td>
</tr>
<tr>
<td style="text-align: left;">rgstDt</td>
<td style="text-align: left;">등록일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">2025-07-01 10:41</td>
<td style="text-align: left;">공고의 등록일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">sucsfbidMthdNm</td>
<td style="text-align: left;">낙찰방법명</td>
<td style="text-align: left;">700</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">공고서참조</td>
<td style="text-align: left;">낙찰자를 결정하는 방법-낙찰방법 세부기준</td>
</tr>
<tr>
<td style="text-align: left;">rmrkCntnts</td>
<td style="text-align: left;">비고내용</td>
<td style="text-align: left;">4000</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">공고서 참조https://www.ajou.ac.kr/kr/guide/bidding.do?mode=view&amp;articleNo=350802&amp;article.offset=0&amp;articleLimit=10</td>
<td style="text-align: left;">공고서의 비고 내용</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 요청 / 응답 메시지 예제

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr>
<td style="text-align: center;"><strong>REST(URI)</strong></td>
</tr>
<tr>
<td style="text-align: center;">http://apis.data.go.kr/1230000/ad/BidPublicInfoService/getBidPblancListInfoEtcPPSSrch?inqryDiv=1&amp;inqryBgnDt=202507010000&amp;inqryEndDt=202507012359&amp;numOfRows=10&amp;pageNo=1&amp;bidNtceNm=백업소프트웨어 구매업체 선정 입찰&amp;pageNo=1&amp;numOfRows=10&amp;ServiceKey=인증키</td>
</tr>
<tr>
<td style="text-align: center;"><strong>응답 메시지</strong></td>
</tr>
<tr>
<td style="text-align: left;"><p>&lt;response&gt;</p>
<p>&lt;header&gt;</p>
<p>&lt;resultCode&gt;00&lt;/resultCode&gt;</p>
<p>&lt;resultMsg&gt;정상&lt;/resultMsg&gt;</p>
<p>&lt;/header&gt;</p>
<p>&lt;body&gt;</p>
<p>&lt;items&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00935310&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;untyNtceNo&gt;R25BM00300704&lt;/untyNtceNo&gt;</p>
<p>&lt;rgstTyNm&gt;나라장터 기타 공고건&lt;/rgstTyNm&gt;</p>
<p>&lt;ntceKindNm&gt;등록공고&lt;/ntceKindNm&gt;</p>
<p>&lt;bidNtceDt&gt;2025-07-01 10:41&lt;/bidNtceDt&gt;</p>
<p>&lt;refNo&gt;아주대학교5051&lt;/refNo&gt;</p>
<p>&lt;bidNtceNm&gt;백업소프트웨어 구매업체 선정 입찰&lt;/bidNtceNm&gt;</p>
<p>&lt;ntceInsttCd&gt;7001966&lt;/ntceInsttCd&gt;</p>
<p>&lt;ntceInsttNm&gt;아주대학교&lt;/ntceInsttNm&gt;</p>
<p>&lt;dminsttNm&gt;아주대학교&lt;/dminsttNm&gt;</p>
<p>&lt;rbidPermsnYn&gt;N&lt;/rbidPermsnYn&gt;</p>
<p>&lt;bidMethdNm&gt;직찰&lt;/bidMethdNm&gt;</p>
<p>&lt;cntrctCnclsMthdNm&gt;공고서참조&lt;/cntrctCnclsMthdNm&gt;</p>
<p>&lt;cmmnSpldmdYn&gt;N&lt;/cmmnSpldmdYn&gt;</p>
<p>&lt;bidBeginDt&gt;&lt;/bidBeginDt&gt;</p>
<p>&lt;bidClseDt&gt;&lt;/bidClseDt&gt;</p>
<p>&lt;sucsfbidMthdNm&gt;공고서 참조&lt;/sucsfbidMthdNm&gt;</p>
<p>&lt;opengDt&gt;2025-07-09 14:00&lt;/opengDt&gt;</p>
<p>&lt;opengPlce&gt;&lt;/opengPlce&gt;</p>
<p>&lt;bidQlfctRgstCntnts&gt;입찰참가자격 (아래 입찰참가자격을 모두 만족시키는 업체만 입찰참가 가능함)</p>
<p>가. 국가를 당사로 하는 계약에 관한 법률 시행령 제12조 및 동법 시행규칙 제14조 규정에 의한 경쟁입찰 참가 자격을 갖춘 자</p>
<p>나. 국가를 당사자로 하는 계약에 관한 법률 시행령 제76조(부정당업자의 입찰참가 자격제한)에 의한 결격사유가 없는 자</p>
<p>다. 정보통신공사업법 제 14조에 의해 정보통신공사업을 등록한 사업자 및 소트웨어진흥법 제24조에 의한 소프트웨어(컴퓨터관련서비스산업) 사업자</p>
<p>라. 물품 수요자로부터 사양 검토확인을 득한 업체(본교에서 제공하는 설계서 확인 필)</p>
<p>마. 전년도 매출액이 100억/년 이상(2024년도 표준재무제표증명 제출)</p>
<p>바. 공고일 기준 최근 3년간 시스템 구축 이행 실적이 1건 이상(국내 4년제 대학교 및 공공기관 대상)이며 각 계약 금액이 건당 1억원 이상인 업체(실적증명서 제출)</p>
<p>사. 사업장 소재지가 서울, 경기, 인천 지역인 업체</p>
<p>※ 공동 수급 불허</p>
<p>※ 사업수행자는 계약 후 10일 이내에 납품물품명세서(부품별 단가 명시), 제조사 기술지원확약서, 착수계, 보안서약서를 제출하여야 함&lt;/bidQlfctRgstCntnts&gt;</p>
<p>&lt;bidPrtcptFee&gt;0&lt;/bidPrtcptFee&gt;</p>
<p>&lt;bidGrntymnyPaymntObjYn&gt;N&lt;/bidGrntymnyPaymntObjYn&gt;</p>
<p>&lt;bidNtceDtlUrl&gt;https://www.g2b.go.kr/link/PNPE027_01/single/?bidPbancNo=R25BK00935310&amp;bidPbancOrd=000&amp;prcmBsneSeCd=09&amp;pbancType=pbanc&lt;/bidNtceDtlUrl&gt;</p>
<p>&lt;bidNtceUrl&gt;https://www.g2b.go.kr/link/PNPE027_01/single/?bidPbancNo=R25BK00935310&amp;bidPbancOrd=000&amp;prcmBsneSeCd=09&amp;pbancType=pbanc&lt;/bidNtceUrl&gt;</p>
<p>&lt;ntceSpecDocUrl1&gt;https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00935310&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=1&amp;prcmBsneSeCd=09&lt;/ntceSpecDocUrl1&gt;</p>
<p>&lt;ntceSpecDocUrl2&gt;https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00935310&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=2&amp;prcmBsneSeCd=09&lt;/ntceSpecDocUrl2&gt;</p>
<p>&lt;ntceSpecDocUrl3&gt;https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00935310&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=3&amp;prcmBsneSeCd=09&lt;/ntceSpecDocUrl3&gt;</p>
<p>&lt;ntceSpecDocUrl4&gt;https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00935310&amp;bidPbancOrd=000&amp;fileType=&amp;fileSeq=4&amp;prcmBsneSeCd=09&lt;/ntceSpecDocUrl4&gt;</p>
<p>&lt;ntceSpecDocUrl5&gt;&lt;/ntceSpecDocUrl5&gt;</p>
<p>&lt;ntceSpecFileNm1&gt;1._입찰공고_및_관련서류.hwp&lt;/ntceSpecFileNm1&gt;</p>
<p>&lt;ntceSpecFileNm2&gt;2. 아주대학교_정보시스템 소규모DR센터 고도화_백업소프트웨어 개선_과업지시서.hwp&lt;/ntceSpecFileNm2&gt;</p>
<p>&lt;ntceSpecFileNm3&gt;3. 물품규격서(백업소프트웨어).hwp&lt;/ntceSpecFileNm3&gt;</p>
<p>&lt;ntceSpecFileNm4&gt;4. 사양(규격)검토확인서.hwp&lt;/ntceSpecFileNm4&gt;</p>
<p>&lt;ntceSpecFileNm5&gt;&lt;/ntceSpecFileNm5&gt;</p>
<p>&lt;presmptPrce&gt;&lt;/presmptPrce&gt;</p>
<p>&lt;rmrkCntnts&gt;공고서 참조</p>
<p>https://www.ajou.ac.kr/kr/guide/bidding.do?mode=view&amp;articleNo=350802&amp;article.offset=0&amp;articleLimit=10&lt;/rmrkCntnts&gt;</p>
<p>&lt;rgstDt&gt;2025-07-01 10:41&lt;/rgstDt&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;/items&gt;</p>
<p>&lt;numOfRows&gt;10&lt;/numOfRows&gt;</p>
<p>&lt;pageNo&gt;1&lt;/pageNo&gt;</p>
<p>&lt;totalCount&gt;1&lt;/totalCount&gt;</p>
<p>&lt;/body&gt;</p>
<p>&lt;/response&gt;</p></td>
</tr>
</tbody>
</table>

#### \[입찰공고목록 정보에 대한 혁신장터 최종제안요청서 교부 첨부파일정보조회\] 오퍼레이션 명세

<table>
<colgroup>
<col style="width: 4%" />
<col style="width: 21%" />
<col style="width: 17%" />
<col style="width: 21%" />
<col style="width: 2%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr>
<td rowspan="6">오퍼레이션 정보</td>
<td>오퍼레이션 번호</td>
<td>23</td>
<td>오퍼레이션명(국문)</td>
<td colspan="2">입찰공고목록 정보에 대한 혁신장터 최종제안요청서 교부 첨부파일정보조회</td>
</tr>
<tr>
<td>오퍼레이션 유형</td>
<td>조회(목록)</td>
<td>오퍼레이션명(영문)</td>
<td colspan="2">getBidPblancListPPIFnlRfpIssAtchFileInfo</td>
</tr>
<tr>
<td>오퍼레이션 설명</td>
<td colspan="4">낙찰자결정방법이 [경쟁적 대화에 의한 낙찰자 선정 낙찰방법] 일경우 검색조건에 등록일시, 입찰공고번호, 교부일시를 입력하여 혁신장터에서 교부된 최종제안요청서 첨부파일정보를 조회함</td>
</tr>
<tr>
<td>Call Back URL</td>
<td colspan="4">N/A</td>
</tr>
<tr>
<td>최대 메시지 사이즈</td>
<td colspan="4">[ 4000bytes]</td>
</tr>
<tr>
<td>평균 응답 시간</td>
<td>[ 500 ms]</td>
<td colspan="2">초당 최대 트랜잭션</td>
<td>[ 30 tps]</td>
</tr>
</tbody>
</table>

##### 요청 메시지 명세

<table>
<colgroup>
<col style="width: 19%" />
<col style="width: 19%" />
<col style="width: 13%" />
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 21%" />
</colgroup>
<tbody>
<tr>
<td>항목명(영문)</td>
<td>항목명(국문)</td>
<td>항목크기</td>
<td>항목구분</td>
<td>샘플데이터</td>
<td>항목설명</td>
</tr>
<tr>
<td>numOfRows</td>
<td>한 페이지 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td>10</td>
<td>한 페이지 결과 수</td>
</tr>
<tr>
<td>pageNo</td>
<td>페이지 번호</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td>1</td>
<td>페이지 번호</td>
</tr>
<tr>
<td>ServiceKey</td>
<td>서비스키</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">1</td>
<td>공공데이터포탈에서 받은 인증키</td>
<td>공공데이터포탈에서 받은 인증키</td>
</tr>
<tr>
<td>type</td>
<td>타입</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">0</td>
<td>json</td>
<td>오픈API 리턴 타입을 JSON으로 받고 싶을 경우 'json' 으로 지정</td>
</tr>
<tr>
<td>inqryDiv</td>
<td>조회구분</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td>1</td>
<td>검색하고자하는 조회구분<br />
1: 공고게시일시 , 2:교부일시, 3: 입찰공고번호</td>
</tr>
<tr>
<td>inqryBgnDt</td>
<td>조회시작일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td>202503100000</td>
<td>검색하고자하는 등록일시 조회시작일시 "YYYYMMDDHHMM"<br />
(조회구분 1,2인 경우 필수이며 범위는 최대 1개월로 제한 )</td>
</tr>
<tr>
<td>inqryEndDt</td>
<td>조회종료일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td>202503312359</td>
<td>검색하고자하는 등록일시 조회종료일시 "YYYYMMDDHHMM"<br />
(조회구분 1,2인 경우 필수이며 범위는 최대 1개월로 제한 )</td>
</tr>
<tr>
<td>bidNtceNo</td>
<td>입찰공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">0</td>
<td>R25BK00734839</td>
<td>검색하고자 하는 입찰공고번호<br />
(조회구분 '3' 선택시 필수)</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 응답 메시지 명세

<table style="width:100%;">
<colgroup>
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 13%" />
<col style="width: 11%" />
<col style="width: 13%" />
<col style="width: 21%" />
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
<td>resultCode</td>
<td>결과코드</td>
<td style="text-align: center;">2</td>
<td style="text-align: center;">1</td>
<td>00</td>
<td>결과코드</td>
</tr>
<tr>
<td>resultMsg</td>
<td>결과메세지</td>
<td style="text-align: center;">50</td>
<td style="text-align: center;">1</td>
<td>정상.</td>
<td>결과메세지</td>
</tr>
<tr>
<td>numOfRows</td>
<td>한 페이지 결과 수</td>
<td style="text-align: center;">4</td>
<td style="text-align: center;">1</td>
<td>10</td>
<td>한 페이지 결과 수</td>
</tr>
<tr>
<td>pageNo</td>
<td>페이지 번호</td>
<td style="text-align: center;">4</td>
<td style="text-align: center;">1</td>
<td>1</td>
<td>페이지 번호</td>
</tr>
<tr>
<td>totalCount</td>
<td>전체 결과 수</td>
<td style="text-align: center;">4</td>
<td style="text-align: center;">1</td>
<td>1</td>
<td>전체 결과 수</td>
</tr>
<tr>
<td>bidNtceNo</td>
<td>입찰공고번호</td>
<td style="text-align: center;">40</td>
<td style="text-align: center;">1</td>
<td>R25BK00734839</td>
<td style="text-align: left;"><p>입찰공고 관리번입찰공고 관리번호이며 조달청나라장터 공고건의 형식은 년도(4)+월(2)+순번(5)이며 자체전자조달시스템 보유기관은 각 기관별 형식 별도 사용</p>
<p>*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성</p>
<p>-단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</p></td>
</tr>
<tr>
<td>bidNtceOrd</td>
<td>입찰공고차수</td>
<td style="text-align: center;">3</td>
<td style="text-align: center;">1</td>
<td>000</td>
<td>입찰공고차수는 해당 입찰공고에 대한 재공고 및 재입찰 등이 발생되었을 경우 증가되는 수</td>
</tr>
<tr>
<td>issDt</td>
<td>교부일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-05-16 17:07:21</td>
<td style="text-align: left;">혁신장터 제안서 교부일시<br />
“YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td>bsnsDivNm</td>
<td>업무구분명</td>
<td style="text-align: left;">30</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">물품</td>
<td>입찰업무를 구분하는 명으로 물품, 용역, 공사, 외자로 구분함</td>
</tr>
<tr>
<td>atchSno</td>
<td>첨부순번</td>
<td style="text-align: center;">7</td>
<td style="text-align: center;">0</td>
<td>1</td>
<td>공고의 최종 제안요청서 교부 첨부파일 순번</td>
</tr>
<tr>
<td>atchDocDivNm</td>
<td>첨부문서구분명</td>
<td style="text-align: center;">50</td>
<td style="text-align: center;">0</td>
<td>최종제안요청서 교부안내서</td>
<td>공고의 최종 제안요청서 교부 첨부파일 문서구분</td>
</tr>
<tr>
<td>atchFileNm</td>
<td>첨부파일명</td>
<td style="text-align: center;">200</td>
<td style="text-align: center;">0</td>
<td>붙임_1. 최종제안요청서 교부 안내서.hwp</td>
<td>공고의 최종 제안요청서 교부 첨부 파일명</td>
</tr>
<tr>
<td>atchFileUrl</td>
<td>첨부파일URL</td>
<td style="text-align: center;">800</td>
<td style="text-align: center;">0</td>
<td>https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00734839&amp;amp;bidPbancOrd=000&amp;amp;fileType=LSTG&amp;amp;fileSeq=1&amp;prcmBsneSeCd=03</td>
<td>공고의 최종 제안요청서 교부 첨부파일 URL</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 요청 / 응답 메시지 예제

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr>
<td style="text-align: center;"><strong>REST(URI)</strong></td>
</tr>
<tr>
<td style="text-align: center;">http://apis.data.go.kr/1230000/ad/BidPublicInfoService/getBidPblancListPPIFnlRfpIssAtchFileInfo?inqryDiv=3&amp;bidNtceNo=R25BK00734839&amp;pageNo=1&amp;numOfRows=10&amp;ServiceKey=인증키*</td>
</tr>
<tr>
<td style="text-align: center;"><strong>응답 메시지</strong></td>
</tr>
<tr>
<td style="text-align: left;"><p>&lt;response&gt;</p>
<p>&lt;header&gt;</p>
<p>&lt;resultCode&gt;00&lt;/resultCode&gt;</p>
<p>&lt;resultMsg&gt;정상&lt;/resultMsg&gt;</p>
<p>&lt;/header&gt;</p>
<p>&lt;body&gt;</p>
<p>&lt;items&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00734839&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;issDt&gt;2025-05-16 17:07:21&lt;/issDt&gt;</p>
<p>&lt;bsnsDivNm&gt;물품&lt;/bsnsDivNm&gt;</p>
<p>&lt;atchSno&gt;1&lt;/atchSno&gt;</p>
<p>&lt;atchDocDivNm&gt;최종제안요청서 교부안내서&lt;/atchDocDivNm&gt;</p>
<p>&lt;atchFileNm&gt;붙임_1. 최종제안요청서 교부 안내서.hwp&lt;/atchFileNm&gt;</p>
<p>&lt;atchFileUrl&gt;https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00734839&amp;bidPbancOrd=000&amp;fileType=LSTG&amp;fileSeq=1&amp;prcmBsneSeCd=03&lt;/atchFileUrl&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00734839&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;issDt&gt;2025-05-16 17:07:21&lt;/issDt&gt;</p>
<p>&lt;bsnsDivNm&gt;물품&lt;/bsnsDivNm&gt;</p>
<p>&lt;atchSno&gt;2&lt;/atchSno&gt;</p>
<p>&lt;atchDocDivNm&gt;최종제안요청서&lt;/atchDocDivNm&gt;</p>
<p>&lt;atchFileNm&gt;최종제안요청서.pdf&lt;/atchFileNm&gt;</p>
<p>&lt;atchFileUrl&gt;https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00734839&amp;bidPbancOrd=000&amp;fileType=LSTD&amp;fileSeq=2&amp;prcmBsneSeCd=03&lt;/atchFileUrl&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00734839&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;issDt&gt;2025-05-16 17:07:21&lt;/issDt&gt;</p>
<p>&lt;bsnsDivNm&gt;물품&lt;/bsnsDivNm&gt;</p>
<p>&lt;atchSno&gt;3&lt;/atchSno&gt;</p>
<p>&lt;atchDocDivNm&gt;최종제안요청서&lt;/atchDocDivNm&gt;</p>
<p>&lt;atchFileNm&gt;최종제안요청서_제안관련 서식.hwp&lt;/atchFileNm&gt;</p>
<p>&lt;atchFileUrl&gt;https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK00734839&amp;bidPbancOrd=000&amp;fileType=LSTD&amp;fileSeq=3&amp;prcmBsneSeCd=03&lt;/atchFileUrl&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;/items&gt;</p>
<p>&lt;numOfRows&gt;999&lt;/numOfRows&gt;</p>
<p>&lt;pageNo&gt;1&lt;/pageNo&gt;</p>
<p>&lt;totalCount&gt;3&lt;/totalCount&gt;</p>
<p>&lt;/body&gt;</p>
<p>&lt;/response&gt;</p></td>
</tr>
</tbody>
</table>

#### \[입찰공고목록 정보에 대한 입찰가격산식A정보조회\] 오퍼레이션 명세

<table>
<colgroup>
<col style="width: 4%" />
<col style="width: 21%" />
<col style="width: 17%" />
<col style="width: 21%" />
<col style="width: 2%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr>
<td rowspan="6">오퍼레이션 정보</td>
<td>오퍼레이션 번호</td>
<td>24</td>
<td>오퍼레이션명(국문)</td>
<td colspan="2">입찰공고목록 정보에 대한 입찰가격산식A정보조회</td>
</tr>
<tr>
<td>오퍼레이션 유형</td>
<td>조회(목록)</td>
<td>오퍼레이션명(영문)</td>
<td colspan="2">getBidPblancListBidPrceCalclAInfo</td>
</tr>
<tr>
<td>오퍼레이션 설명</td>
<td colspan="4">검색조건에 공고게시일시와 입찰공고번호를 입력하여 입찰가격산식 A값 적용 공고의 합산항목인 국민연금보험료, 국민건강보험료, 퇴직공제부금비, 노인장기요양보험료, 산업안전보건관리비, 안전관리비, 품질관리비, 품질관리비 적용대상여부등 입찰가격산식A정보 조회 ( 복수예가는 A값 공개 시 제공)</td>
</tr>
<tr>
<td>Call Back URL</td>
<td colspan="4">N/A</td>
</tr>
<tr>
<td>최대 메시지 사이즈</td>
<td colspan="4">[ 4000bytes]</td>
</tr>
<tr>
<td>평균 응답 시간</td>
<td>[ 500 ms]</td>
<td colspan="2">초당 최대 트랜잭션</td>
<td>[ 30 tps]</td>
</tr>
</tbody>
</table>

##### 요청 메시지 명세

<table>
<colgroup>
<col style="width: 19%" />
<col style="width: 19%" />
<col style="width: 13%" />
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 21%" />
</colgroup>
<tbody>
<tr>
<td>항목명(영문)</td>
<td>항목명(국문)</td>
<td>항목크기</td>
<td>항목구분</td>
<td>샘플데이터</td>
<td>항목설명</td>
</tr>
<tr>
<td>numOfRows</td>
<td>한 페이지 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td>10</td>
<td>한 페이지 결과 수</td>
</tr>
<tr>
<td>pageNo</td>
<td>페이지 번호</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td>1</td>
<td>페이지 번호</td>
</tr>
<tr>
<td>ServiceKey</td>
<td>서비스키</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">1</td>
<td>공공데이터포탈에서 받은 인증키</td>
<td>공공데이터포탈에서 받은 인증키</td>
</tr>
<tr>
<td>type</td>
<td>타입</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">0</td>
<td>json</td>
<td>오픈API 리턴 타입을 JSON으로 받고 싶을 경우 'json' 으로 지정</td>
</tr>
<tr>
<td>inqryDiv</td>
<td>조회구분</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td>1</td>
<td>검색하고자하는 조회구분<br />
1: 공고게시일시 , 2: 입찰공고번호</td>
</tr>
<tr>
<td>inqryBgnDt</td>
<td>조회시작일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td>202509200000</td>
<td>검색하고자하는 등록일시 조회시작일시 "YYYYMMDDHHMM"<br />
(조회구분 1인 경우 필수이며 범위는 최대 1개월로 제한 )</td>
</tr>
<tr>
<td>inqryEndDt</td>
<td>조회종료일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td>202509302359</td>
<td>검색하고자하는 등록일시 조회종료일시 "YYYYMMDDHHMM"<br />
(조회구분 1인 경우 필수이며 범위는 최대 1개월로 제한 )</td>
</tr>
<tr>
<td>bidNtceNo</td>
<td>입찰공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">0</td>
<td>R25BK01063665</td>
<td>검색하고자 하는 입찰공고번호<br />
(조회구분 '2' 선택시 필수)</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 응답 메시지 명세

<table style="width:100%;">
<colgroup>
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 13%" />
<col style="width: 11%" />
<col style="width: 13%" />
<col style="width: 21%" />
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
<td>resultCode</td>
<td>결과코드</td>
<td style="text-align: center;">2</td>
<td style="text-align: center;">1</td>
<td>00</td>
<td>결과코드</td>
</tr>
<tr>
<td>resultMsg</td>
<td>결과메세지</td>
<td style="text-align: center;">50</td>
<td style="text-align: center;">1</td>
<td>정상.</td>
<td>결과메세지</td>
</tr>
<tr>
<td>numOfRows</td>
<td>한 페이지 결과 수</td>
<td style="text-align: center;">4</td>
<td style="text-align: center;">1</td>
<td>10</td>
<td>한 페이지 결과 수</td>
</tr>
<tr>
<td>pageNo</td>
<td>페이지 번호</td>
<td style="text-align: center;">4</td>
<td style="text-align: center;">1</td>
<td>1</td>
<td>페이지 번호</td>
</tr>
<tr>
<td>totalCount</td>
<td>전체 결과 수</td>
<td style="text-align: center;">4</td>
<td style="text-align: center;">1</td>
<td>1</td>
<td>전체 결과 수</td>
</tr>
<tr>
<td>bidNtceNo</td>
<td>입찰공고번호</td>
<td style="text-align: center;">40</td>
<td style="text-align: center;">1</td>
<td>R25BK01063665</td>
<td style="text-align: left;"><p>입찰공고 관리번입찰공고 관리번호이며 조달청나라장터 공고건의 형식은 년도(4)+월(2)+순번(5)이며 자체전자조달시스템 보유기관은 각 기관별 형식 별도 사용</p>
<p>*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성</p>
<p>-단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</p></td>
</tr>
<tr>
<td>bidNtceOrd</td>
<td>입찰공고차수</td>
<td style="text-align: left;">3</td>
<td style="text-align: left;">1</td>
<td>001</td>
<td>입찰공고차수는 해당 입찰공고에 대한 재공고 및 재입찰 등이 발생되었을 경우 증가되는 수</td>
</tr>
<tr>
<td style="text-align: left;">sftyMngcst</td>
<td style="text-align: left;">산업안전보건관리비</td>
<td style="text-align: left;">17</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">314503783</td>
<td style="text-align: left;">산업안전보건관리비 (원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">sftyChckMngcst</td>
<td style="text-align: left;">안전관리비</td>
<td style="text-align: left;">17</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">127430000</td>
<td style="text-align: left;">안전관리비 (원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">rtrfundNon</td>
<td style="text-align: left;">퇴직공제부금비</td>
<td style="text-align: left;">17</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">133325228</td>
<td style="text-align: left;">퇴직공제부금비(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">mrfnHealthInsrprm</td>
<td style="text-align: left;">국민건강보험료</td>
<td style="text-align: left;">18</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">205494753</td>
<td style="text-align: left;">국민건강보험료(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">npnInsrprm</td>
<td style="text-align: left;">국민연금보험료</td>
<td style="text-align: left;">18</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">260853707</td>
<td style="text-align: left;">국민연금보험료(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">odsnLngtrmrcprInsrprm</td>
<td style="text-align: left;">노인장기요양보험료</td>
<td style="text-align: left;">18</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">26611570</td>
<td style="text-align: left;">노인장기요양보험료(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">qltyMngcst</td>
<td style="text-align: left;">품질관리비</td>
<td style="text-align: left;">22</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">95795075</td>
<td style="text-align: left;">건설공사의 시설물 안전 및 유지관리에 관한 품질시험비(품질시험에 필요한 재료비, 노무비, 경비)와 품질관리활동비(품질시험비 외 품질관리활동에 필요한 비용)에 소요되는 비용</td>
</tr>
<tr>
<td style="text-align: left;">qltyMngcstAObjYn</td>
<td style="text-align: left;">품질관리비A적용대상여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">Y</td>
<td style="text-align: left;">품질관리비가 A값의 합산에 포함히 되는지 적용여부</td>
</tr>
<tr>
<td style="text-align: left;">prearngPrceDcsnMthdNm</td>
<td style="text-align: left;">예정가격결정방법명</td>
<td style="text-align: left;">20</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">복수예가</td>
<td style="text-align: left;">예정가격의 결정을 위해 복수예정가격방식으로 산정하는지 단일 예정가격으로 산정하는지를 구분하는 명</td>
</tr>
<tr>
<td>ntceNticeDt</td>
<td>공고게시일시</td>
<td style="text-align: center;">19</td>
<td style="text-align: center;">1</td>
<td>2025-09-24 09:39:16</td>
<td>공고게시일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td>bidPrceCalclAOpenDt</td>
<td>입찰가격산식A공개일시</td>
<td style="text-align: center;">19</td>
<td style="text-align: center;">1</td>
<td>2025-10-21 16:10:19</td>
<td>입찰가격산식 A 값공개일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">smkpAmt</td>
<td style="text-align: left;">표준시장단가금액</td>
<td style="text-align: left;">22</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2354369710</td>
<td style="text-align: left;">표준시장단가금액 (원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">smkpAmtYn</td>
<td style="text-align: left;">표준시장단가금액A적용대상여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">Y</td>
<td style="text-align: left;">표준시장단가금액이 A값의 합산에 포함히 되는지 적용여부</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 요청 / 응답 메시지 예제

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr>
<td style="text-align: center;"><strong>REST(URI)</strong></td>
</tr>
<tr>
<td style="text-align: center;">http://apis.data.go.kr/1230000/ad/BidPublicInfoService/getBidPblancListBidPrceCalclAInfo?numOfRows=10&amp;pageNo=1&amp;inqryDiv=2&amp;type=xml&amp;bidNtceNo= R25BK01063665&amp;ServiceKey=인증키*</td>
</tr>
<tr>
<td style="text-align: center;"><strong>응답 메시지</strong></td>
</tr>
<tr>
<td style="text-align: left;"><p>&lt;response&gt;</p>
<p>&lt;header&gt;</p>
<p>&lt;resultCode&gt;00&lt;/resultCode&gt;</p>
<p>&lt;resultMsg&gt;정상&lt;/resultMsg&gt;</p>
<p>&lt;/header&gt;</p>
<p>&lt;body&gt;</p>
<p>&lt;items&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK01063665&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;001&lt;/bidNtceOrd&gt;</p>
<p>&lt;sftyMngcst&gt;314503783&lt;/sftyMngcst&gt;</p>
<p>&lt;sftyChckMngcst&gt;127430000&lt;/sftyChckMngcst&gt;</p>
<p>&lt;rtrfundNon&gt;133325228&lt;/rtrfundNon&gt;</p>
<p>&lt;mrfnHealthInsrprm&gt;205494753&lt;/mrfnHealthInsrprm&gt;</p>
<p>&lt;npnInsrprm&gt;260853707&lt;/npnInsrprm&gt;</p>
<p>&lt;odsnLngtrmrcprInsrprm&gt;26611570&lt;/odsnLngtrmrcprInsrprm&gt;</p>
<p>&lt;qltyMngcst&gt;95795075&lt;/qltyMngcst&gt;</p>
<p>&lt;qltyMngcstAObjYn&gt;Y&lt;/qltyMngcstAObjYn&gt;</p>
<p>&lt;prearngPrceDcsnMthdNm&gt;복수예가&lt;/prearngPrceDcsnMthdNm&gt;</p>
<p>&lt;ntceNticeDt&gt;2025-09-24 09:39:16&lt;/ntceNticeDt&gt;</p>
<p>&lt;bidPrceCalclAOpenDt&gt;2025-10-21 16:10:19&lt;/bidPrceCalclAOpenDt&gt;</p>
<p>&lt;smkpAmt&gt;2354369710&lt;/smkpAmt&gt;</p>
<p>&lt;smkpAmtYn&gt;Y&lt;/smkpAmtYn&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;/items&gt;</p>
<p>&lt;numOfRows&gt;999&lt;/numOfRows&gt;</p>
<p>&lt;pageNo&gt;1&lt;/pageNo&gt;</p>
<p>&lt;totalCount&gt;1&lt;/totalCount&gt;</p>
<p>&lt;/body&gt;</p>
<p>&lt;/response&gt;</p></td>
</tr>
</tbody>
</table>

#### (25)\[입찰공고목록 정보에 대한 평가대상주력분야 조회\] 오퍼레이션 명세

<table>
<colgroup>
<col style="width: 4%" />
<col style="width: 21%" />
<col style="width: 17%" />
<col style="width: 21%" />
<col style="width: 2%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr>
<td rowspan="6">오퍼레이션 정보</td>
<td>오퍼레이션 번호</td>
<td>24</td>
<td>오퍼레이션명(국문)</td>
<td colspan="2">입찰공고목록 정보에 대한 평가대상주력분야 조회</td>
</tr>
<tr>
<td>오퍼레이션 유형</td>
<td>조회(목록)</td>
<td>오퍼레이션명(영문)</td>
<td colspan="2">getBidPblancListEvaluationIndstrytyMfrcInfo</td>
</tr>
<tr>
<td>오퍼레이션 설명</td>
<td colspan="4">검색조건에 등록일시와 입찰공고번호를 입력하여 입찰 평가대상주력분야의 건산법적용여부, 건설업역상호진출가능여부, 건설업역구분코드, 낙찰자선정적용기준코드, 공종유형명, 공사대상업종명, 업종주력분야명, 추정금액, 추정가격, 부가가치세, 평가비율을 조회</td>
</tr>
<tr>
<td>Call Back URL</td>
<td colspan="4">N/A</td>
</tr>
<tr>
<td>최대 메시지 사이즈</td>
<td colspan="4">[ 4000bytes]</td>
</tr>
<tr>
<td>평균 응답 시간</td>
<td>[ 500 ms ]</td>
<td colspan="2">초당 최대 트랜잭션</td>
<td>[ 30tps]</td>
</tr>
</tbody>
</table>

##### 요청 메시지 명세

<table>
<colgroup>
<col style="width: 19%" />
<col style="width: 19%" />
<col style="width: 13%" />
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 21%" />
</colgroup>
<tbody>
<tr>
<td>항목명(영문)</td>
<td>항목명(국문)</td>
<td>항목크기</td>
<td>항목구분</td>
<td>샘플데이터</td>
<td>항목설명</td>
</tr>
<tr>
<td>numOfRows</td>
<td>한 페이지 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td>10</td>
<td>한 페이지 결과 수</td>
</tr>
<tr>
<td>pageNo</td>
<td>페이지 번호</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td>1</td>
<td>페이지 번호</td>
</tr>
<tr>
<td>ServiceKey</td>
<td>서비스키</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">1</td>
<td>공공데이터포탈에서 받은 인증키</td>
<td>공공데이터포탈에서 받은 인증키</td>
</tr>
<tr>
<td>type</td>
<td>타입</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">0</td>
<td>json</td>
<td>오픈API 리턴 타입을 JSON으로 받고 싶을 경우 'json' 으로 지정</td>
</tr>
<tr>
<td>inqryDiv</td>
<td>조회구분</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td>1</td>
<td>검색하고자하는 조회구분<br />
1: 공고게시일시 , 2: 입찰공고번호</td>
</tr>
<tr>
<td>inqryBgnDt</td>
<td>조회시작일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td>202507010000</td>
<td>검색하고자하는 등록일시 조회시작일시 "YYYYMMDDHHMM"<br />
(조회구분 1인 경우 필수이며 범위는 최대 1개월로 제한 )</td>
</tr>
<tr>
<td>inqryEndDt</td>
<td>조회종료일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td>202507032359</td>
<td>검색하고자하는 등록일시 조회종료일시 "YYYYMMDDHHMM"<br />
(조회구분 1인 경우 필수이며 범위는 최대 1개월로 제한</td>
</tr>
<tr>
<td>bidNtceNo</td>
<td>입찰공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">0</td>
<td>R25BK00937461</td>
<td>검색하고자 하는 입찰공고번호<br />
(조회구분 '2' 선택시 필수)</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 응답 메시지 명세

<table style="width:100%;">
<colgroup>
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 13%" />
<col style="width: 11%" />
<col style="width: 13%" />
<col style="width: 21%" />
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
<td>resultCode</td>
<td>결과코드</td>
<td style="text-align: center;">2</td>
<td style="text-align: center;">1</td>
<td>00</td>
<td>결과코드</td>
</tr>
<tr>
<td>resultMsg</td>
<td>결과메세지</td>
<td style="text-align: center;">50</td>
<td style="text-align: center;">1</td>
<td>정상.</td>
<td>결과메세지</td>
</tr>
<tr>
<td>numOfRows</td>
<td>한 페이지 결과 수</td>
<td style="text-align: center;">4</td>
<td style="text-align: center;">1</td>
<td>10</td>
<td>한 페이지 결과 수</td>
</tr>
<tr>
<td>pageNo</td>
<td>페이지 번호</td>
<td style="text-align: center;">4</td>
<td style="text-align: center;">1</td>
<td>1</td>
<td>페이지 번호</td>
</tr>
<tr>
<td>totalCount</td>
<td>전체 결과 수</td>
<td style="text-align: center;">4</td>
<td style="text-align: center;">1</td>
<td>1</td>
<td>전체 결과 수</td>
</tr>
<tr>
<td>bidNtceNo</td>
<td>입찰공고번호</td>
<td style="text-align: center;">40</td>
<td style="text-align: center;">1</td>
<td>R25BK00937461</td>
<td style="text-align: left;"><p>입찰공고 관리번입찰공고 관리번호이며 조달청나라장터 공고건의 형식은 년도(4)+월(2)+순번(5)이며 자체전자조달시스템 보유기관은 각 기관별 형식 별도 사용</p>
<p>*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성</p>
<p>- 단계구분: BK(입찰)<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</p></td>
</tr>
<tr>
<td>bidNtceOrd</td>
<td>입찰공고차수</td>
<td style="text-align: center;">3</td>
<td style="text-align: center;">1</td>
<td>000</td>
<td>입찰공고차수는 해당 입찰공고에 대한 재공고 및 재입찰 등이 발생되었을 경우 증가되는 수</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceDt</td>
<td style="text-align: left;">입찰공고일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: center;">1</td>
<td>2025-07-02 16:06:25</td>
<td>입찰공고서를 공고한 일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">CiblAplYn</td>
<td>건산법적용여부</td>
<td style="text-align: center;">1</td>
<td style="text-align: center;">0</td>
<td>Y</td>
<td>건설산업기본법 적용 대상인지에 대한 여부</td>
</tr>
<tr>
<td style="text-align: left;">CnstrtWkaraMtltyAdvcPsblYn</td>
<td>건설업역상호진출가능여부</td>
<td style="text-align: center;">1</td>
<td style="text-align: center;">0</td>
<td>Y</td>
<td>건설업역(종합공사,전문공사)에 상호 진출 가능한지에 대한 여부</td>
</tr>
<tr>
<td style="text-align: left;">CnstrtWkrarDivCd</td>
<td>건설업역구분코드</td>
<td style="text-align: center;">9</td>
<td style="text-align: center;">0</td>
<td>건060002</td>
<td style="text-align: left;">건설 업종의 영역을 구분하는 코드<br />
건060001 : 종합공사<br />
건060002 : 전문공사<br />
건060003 : 유지보수공사<br />
건060004 : 기타</td>
</tr>
<tr>
<td style="text-align: left;">BidwinrSlctnBssCd</td>
<td>낙찰자선정적용기준코드</td>
<td style="text-align: center;">9</td>
<td style="text-align: center;">0</td>
<td>계040001</td>
<td>낙찰자선정적용기준코드<br />
계040000 : 해당없음<br />
계040001 : 국가계약법<br />
계040002 : 지방계약법<br />
계040003 : 자체기준</td>
</tr>
<tr>
<td style="text-align: left;">CnsttyTyNm</td>
<td>공종유형명</td>
<td style="text-align: center;">30</td>
<td style="text-align: center;">1</td>
<td>주공종</td>
<td>공종의 유형명</td>
</tr>
<tr>
<td style="text-align: left;">tmpNm</td>
<td>공사대상업종명</td>
<td style="text-align: center;">4000</td>
<td style="text-align: center;">1</td>
<td>토목공사업</td>
<td>공사대상업종명</td>
</tr>
<tr>
<td style="text-align: left;">IndstrytyMfrcFldNm</td>
<td>업종주력분야명</td>
<td style="text-align: center;">4000</td>
<td style="text-align: center;">1</td>
<td>금속구조물·창호·온실공사</td>
<td>업종에 대하여 주력하고 있는 분야의 명칭</td>
</tr>
<tr>
<td style="text-align: left;">PresmptAmt</td>
<td>추정금액</td>
<td style="text-align: center;">22</td>
<td style="text-align: center;">0</td>
<td>525746000</td>
<td>추정금액</td>
</tr>
<tr>
<td>presmptPrce</td>
<td>추정가격</td>
<td style="text-align: center;">22</td>
<td style="text-align: center;">1</td>
<td>123940000</td>
<td>물품/공사/용역 등의 조달 계약을 체결함에 있어 국제입찰 대상여부를 판단하는 기준 등으로 삼기 위하여 예정가격이 결정되기 전에 예산에 계상된 금액 등을 기준으로 하여 부가가치세 및 조달 수수료를 제외한 금액(원화,원)</td>
</tr>
<tr>
<td>VAT</td>
<td>부가가치세</td>
<td style="text-align: center;">22</td>
<td style="text-align: center;">0</td>
<td>12394000</td>
<td>부가가치세</td>
</tr>
<tr>
<td>EvlRt</td>
<td>평가비율</td>
<td style="text-align: center;">6</td>
<td style="text-align: center;">1</td>
<td>100</td>
<td>평가비율</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 요청 / 응답 메시지 예제

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr>
<td style="text-align: center;"><strong>REST(URI)</strong></td>
</tr>
<tr>
<td style="text-align: center;">http://apis.data.go.kr/1230000/ad/BidPublicInfoService/getBidPblancListEvaluationIndstrytyMfrcInfo?numOfRows=10&amp;pageNo=1&amp;inqryDiv=2&amp;bidNtceNo=R25BK00937461&amp;ServiceKey=인증키*</td>
</tr>
<tr>
<td style="text-align: center;"><strong>응답 메시지</strong></td>
</tr>
<tr>
<td style="text-align: left;"><p>&lt;response&gt;</p>
<p>&lt;header&gt;</p>
<p>&lt;resultCode&gt;00&lt;/resultCode&gt;</p>
<p>&lt;resultMsg&gt;정상&lt;/resultMsg&gt;</p>
<p>&lt;/header&gt;</p>
<p>&lt;body&gt;</p>
<p>&lt;items&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00937461&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidNtceDt&gt;2025-07-02 16:06:25&lt;/bidNtceDt&gt;</p>
<p>&lt;ciblAplYn&gt;Y&lt;/ciblAplYn&gt;</p>
<p>&lt;cnstrtWkaraMtltyAdvcPsblYn&gt;Y&lt;/cnstrtWkaraMtltyAdvcPsblYn&gt;</p>
<p>&lt;cnstrtWkrarDivCd&gt;건060002&lt;/cnstrtWkrarDivCd&gt;</p>
<p>&lt;bidwinrSlctnBssCd&gt;계040001&lt;/bidwinrSlctnBssCd&gt;</p>
<p>&lt;cnsttyTyNm&gt;주공종&lt;/cnsttyTyNm&gt;</p>
<p>&lt;tmpNm&gt;토목공사업&lt;/tmpNm&gt;</p>
<p>&lt;indstrytyMfrcFldNm&gt;금속구조물·창호·온실공사&lt;/indstrytyMfrcFldNm&gt;</p>
<p>&lt;presmptAmt&gt;525746000&lt;/presmptAmt&gt;</p>
<p>&lt;presmptPrce&gt;123940000&lt;/presmptPrce&gt;</p>
<p>&lt;VAT&gt;12394000&lt;/VAT&gt;</p>
<p>&lt;evlRt&gt;100&lt;/evlRt&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;/items&gt;</p>
<p>&lt;numOfRows&gt;90&lt;/numOfRows&gt;</p>
<p>&lt;pageNo&gt;1&lt;/pageNo&gt;</p>
<p>&lt;totalCount&gt;1&lt;/totalCount&gt;</p>
<p>&lt;/body&gt;</p>
<p>&lt;/response&gt;</p></td>
</tr>
</tbody>
</table>

#### **OPEN API 에러코드별 조치방안**

<table>
<colgroup>
<col style="width: 7%" />
<col style="width: 16%" />
<col style="width: 36%" />
<col style="width: 40%" />
</colgroup>
<thead>
<tr>
<th style="text-align: center;"><strong>Code</strong></th>
<th style="text-align: center;"><strong>코드값</strong></th>
<th style="text-align: center;"><strong>설명</strong></th>
<th style="text-align: center;"><strong>조치방안</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: center;">01</td>
<td style="text-align: left;">Application Error</td>
<td style="text-align: left;">제공기관 서비스 제공 상태가 원할하지 않습니다.</td>
<td style="text-align: left;">서비스 제공기관의 관리자에게 문의하시기 바랍니다.</td>
</tr>
<tr>
<td style="text-align: center;">02</td>
<td style="text-align: left;">DB Error</td>
<td style="text-align: left;">제공기관 서비스 제공 상태가 원할하지 않습니다.</td>
<td style="text-align: left;">서비스 제공기관의 관리자에게 문의하시기 바랍니다.</td>
</tr>
<tr>
<td style="text-align: center;">03</td>
<td style="text-align: left;">No Data</td>
<td style="text-align: left;">데이터 없음 에러</td>
<td style="text-align: left;"></td>
</tr>
<tr>
<td style="text-align: center;">04</td>
<td style="text-align: left;">HTTP Error</td>
<td style="text-align: left;">제공기관 서비스 제공 상태가 원할하지 않습니다.</td>
<td style="text-align: left;">서비스 제공기관의 관리자에게 문의하시기 바랍니다.</td>
</tr>
<tr>
<td style="text-align: center;">05</td>
<td style="text-align: left;">service time out</td>
<td style="text-align: left;">제공기관 서비스 제공 상태가 원할하지 않습니다</td>
<td style="text-align: left;">서비스 제공기관의 관리자에게 문의하시기 바랍니다.</td>
</tr>
<tr>
<td style="text-align: center;">06</td>
<td style="text-align: left;">날짜Format 에러</td>
<td style="text-align: left;">날짜 Default, Format Error</td>
<td style="text-align: left;">날짜형식을 확인 하시기 바랍니다.</td>
</tr>
<tr>
<td style="text-align: center;">07</td>
<td style="text-align: left;">입력범위값 초과 에러</td>
<td style="text-align: left;">요청하신 OpenAPI의 파라미터 입력값 범위가 초과 되었습니다.</td>
<td style="text-align: left;">기술문서를 다시 한번 확인하여 주시기 바랍니다.</td>
</tr>
<tr>
<td style="text-align: center;">08</td>
<td style="text-align: left;">필수값 입력 에러</td>
<td style="text-align: left;">요청하신 OpenAPI의 필수 파라미터가 누락되었습니다.</td>
<td style="text-align: left;">기술문서를 다시 한번 확인하여 주시기 바랍니다.</td>
</tr>
<tr>
<td style="text-align: center;">10</td>
<td style="text-align: left;">잘못된 요청 파라미터 에러</td>
<td style="text-align: left;">OpenAPI 요청시 ServiceKey 파라미터가 없음</td>
<td style="text-align: left;"><p>-OpenAPI 요청시 ServiceKey 파라미터가 누락되었습니다.</p>
<p>-OpenAPI 요청 URL을 확인하시기 바랍니다.</p></td>
</tr>
<tr>
<td style="text-align: center;">11</td>
<td style="text-align: left;">필수 요청 파라미터가 없음</td>
<td style="text-align: left;">요청하신 OpenAPI의 필수 파라미터가 누락되었습니다.</td>
<td style="text-align: left;">기술문서를 다시 한번 확인하여 주시기 바랍니다.</td>
</tr>
<tr>
<td style="text-align: center;">12</td>
<td style="text-align: left;">해당 오픈API 서비스가 없거나 폐기됨</td>
<td style="text-align: left;">OpenAPI 호출시 URL이 잘못됨</td>
<td style="text-align: left;"><p>-제공기관 관리자에게 폐기된 서비스인지 확인바랍니다.</p>
<p>폐기된 서비스가 아니면 개발가이드에서 OpenAPI요청 URL을 다시 확인하시기 바랍니다.</p></td>
</tr>
<tr>
<td style="text-align: center;">20</td>
<td style="text-align: left;">서비스 접근 거부</td>
<td style="text-align: left;">활용승인이 되지 않은 OpenAPI호출</td>
<td style="text-align: left;"><p>-OpenAPI활용신청정보의 승인상태를 확인하시기 바랍니다.</p>
<p>-활용신청에 대해 제공기관 담당자가 확인 후 '승인'이후 부터 사용할 수 있습니다.</p>
<p>-신청 후 2~3일 소요되고 결과는 회원가입 시 등록한 e-mail로 발송됩니다.</p></td>
</tr>
<tr>
<td style="text-align: center;">22</td>
<td style="text-align: left;">서비스 요청 제한 횟수 초과 에러</td>
<td style="text-align: left;">일일 활용건수가 초과함(활용건수 증가 필요)</td>
<td style="text-align: left;"><p>-OpenAPI활용신청정보의 서비스 상세기능별 일일 트래픽량을 확인하시기 바랍니다.</p>
<p>-개발계정의 경우 제공기관에서 정의한 트래픽을 초과하여 활용할 수 없습니다.</p>
<p>-운영계정의 경우 변경신청을 통해서 일일트래픽량을 변경 할 수 있습니다.</p></td>
</tr>
<tr>
<td style="text-align: center;">30</td>
<td style="text-align: left;">등록되지 않은 서비스 키</td>
<td style="text-align: left;">잘못된 서비스키를 사용하였거나 서비스키를 URL인코딩하지</td>
<td style="text-align: left;"><p>-OpenAPI활용신청정보의 발급받은 서비스키를 다시 확인하시기 바랍니다.</p>
<p>- 서비스키 값이 같다면 서비스키가 URL 인코등 되었는지 다시 확인하시기 바랍니다.</p></td>
</tr>
<tr>
<td style="text-align: center;">31</td>
<td style="text-align: left;">기한 만료된 서비스 키</td>
<td style="text-align: left;"><p>OpenAPI 사용기간이 만료됨</p>
<p>(활용연장신청 후 사용가능)</p></td>
<td style="text-align: left;"><p>-OpenAPI 활용신청정보의 활용기간을 확인합니다.</p>
<p>-활용기간이 지난 서비스는 이용할 수 없으며 연장신청을 통해 승인 받은 후 다시 이용가능 합니다.</p></td>
</tr>
<tr>
<td style="text-align: center;">32</td>
<td style="text-align: left;">등록되지 않은 도메인명 또는 IP주소</td>
<td style="text-align: left;">활용신청한 서버의 IP와 실제 OpenAPI호출한 서버가 다를 경우</td>
<td style="text-align: left;"><p>-OpenAPI 활용신청정보의 등록된 도메인명이나 IP주소를 다시 확인합니다.</p>
<p>-IP나 도메인의 정보를 변경하기 위해 변경신청을 할 수 있습니다.</p></td>
</tr>
</tbody>
</table>

####
