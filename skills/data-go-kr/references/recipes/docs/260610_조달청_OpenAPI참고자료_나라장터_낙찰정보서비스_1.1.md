![](media/image1.png)조달청 공공데이터 개방

OpenAPI 참고자료

[1. 서비스 명세 [3](#서비스-명세)](#서비스-명세)

[1.1 나라장터 낙찰정보서비스 [3](#나라장터-낙찰정보서비스)](#나라장터-낙찰정보서비스)

[가. 서비스 개요 [3](#서비스-개요)](#서비스-개요)

[나. 오퍼레이션 목록 [4](#오퍼레이션-목록)](#오퍼레이션-목록)

**\**

**개정 이력**

<table style="width:100%;">
<colgroup>
<col style="width: 11%" />
<col style="width: 16%" />
<col style="width: 17%" />
<col style="width: 54%" />
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
<td style="text-align: left;">2025</td>
<td style="text-align: left;">최초 개정</td>
<td style="text-align: left;">최초 개정</td>
</tr>
<tr>
<td style="text-align: left;">1.1</td>
<td style="text-align: left;">2025.09.25</td>
<td style="text-align: left;">항목추가</td>
<td style="text-align: left;"><p>-요청메시지 사업자번호(bizno) 공공데이터 제공신청으로 인한 추가</p>
<p>-대상오퍼레이션</p>
<ul>
<li><p>나라장터 검색조건에 의한 낙찰된 목록 현황 물품조회</p></li>
<li><p>나라장터 검색조건에 의한 낙찰된 목록 현황 공사조회</p></li>
<li><p>나라장터 검색조건에 의한 낙찰된 목록 현황 용역조회</p></li>
<li><p>나라장터 검색조건에 의한 낙찰된 목록 현황 외자조회</p></li>
</ul>
<p>-응답메시지 입찰가격점수(bidPrceEvlVal), 기술평가점수(techEvlVal),기술평가원점수(techEvlNaturVal) 종합평가점수(totalEvlAmtVal) 공공데이터 제공신청으로 인한 추가</p>
<p>-대상오퍼레이션</p>
<ul>
<li><p>개찰결과 개찰완료 목록 조회</p></li>
</ul></td>
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
<td style="text-align: left;"></td>
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
<td style="text-align: left;"></td>
</tr>
</tbody>
</table>

# 1. 서비스 명세

## 1.1 나라장터 낙찰정보서비스

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
<td colspan="6"><strong>ScsbidInfoService</strong></td>
</tr>
<tr>
<td colspan="2">서비스명(국문)</td>
<td colspan="6">나라장터 낙찰정보서비스</td>
</tr>
<tr>
<td colspan="2">서비스명(영문)</td>
<td colspan="6"><strong>ScsbidInfoService</strong></td>
</tr>
<tr>
<td colspan="2">서비스 설명</td>
<td colspan="6">나라장터 개찰결과를 물품, 공사, 용역, 외자의 업무별로 제공하는 서비스로 각 업무별로 최종낙찰자, 개찰순위, 복수예비가 및 예비가격 정보를 제공하며 개찰완료목록, 재입찰목록, 유찰목록 또한 제공하는 나라장터 낙찰정보서비스</td>
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
<td colspan="6">http://apis.data.go.kr/1230000/as/<strong>ScsbidInfoService</strong></td>
</tr>
<tr>
<td colspan="2">운영환경</td>
<td colspan="6">http://apis.data.go.kr/1230000/as/<strong>ScsbidInfoService</strong></td>
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
<td colspan="6">1.5</td>
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
<td colspan="8" style="text-align: left;">안정우 / 조달청 조달데이터관리팀 / 042-724-7685 / eureka3112@korea.kr</td>
</tr>
<tr>
<td>데이터 갱신주기</td>
<td colspan="8">수시</td>
</tr>
</tbody>
</table>

### 오퍼레이션 목록 

<table style="width:100%;">
<colgroup>
<col style="width: 12%" />
<col style="width: 16%" />
<col style="width: 29%" />
<col style="width: 22%" />
<col style="width: 18%" />
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
<td rowspan="4">나라장터 낙찰정보서비스</td>
<td style="text-align: left;"><strong>getScsbidListSttusThng</strong></td>
<td>낙찰된 목록 현황 물품조회</td>
<td>N/A</td>
</tr>
<tr>
<td>2</td>
<td><strong>getScsbidListSttusCnstwk</strong></td>
<td>낙찰된 목록 현황 공사조회</td>
<td>N/A</td>
</tr>
<tr>
<td>3</td>
<td><strong>getScsbidListSttusServc</strong></td>
<td>낙찰된 목록 현황 용역조회</td>
<td>N/A</td>
</tr>
<tr>
<td>4</td>
<td><strong>getScsbidListSttusFrgcpt</strong></td>
<td>낙찰된 목록 현황 외자조회</td>
<td>N/A</td>
</tr>
</tbody>
</table>

<table style="width:100%;">
<colgroup>
<col style="width: 12%" />
<col style="width: 16%" />
<col style="width: 29%" />
<col style="width: 22%" />
<col style="width: 18%" />
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
<td>5</td>
<td rowspan="19">나라장터 낙찰정보서비스</td>
<td style="text-align: left;"><strong>getOpengResultListInfoThng</strong></td>
<td style="text-align: left;">개찰결과 물품 목록 조회</td>
<td>N/A</td>
</tr>
<tr>
<td>6</td>
<td><strong>getOpengResultListInfoCnstwk</strong></td>
<td style="text-align: left;">개찰결과 공사 목록 조회</td>
<td>N/A</td>
</tr>
<tr>
<td>7</td>
<td><strong>getOpengResultListInfoServc</strong></td>
<td style="text-align: left;">개찰결과 용역 목록 조회</td>
<td>N/A</td>
</tr>
<tr>
<td>8</td>
<td><strong>getOpengResultListInfoFrgcpt</strong></td>
<td style="text-align: left;">개찰결과 외자 목록 조회</td>
<td>N/A</td>
</tr>
<tr>
<td>9</td>
<td><strong>getOpengResultListInfoThngPreparPcDetail</strong></td>
<td style="text-align: left;">개찰결과 물품 예비가격상세 목록 조회</td>
<td>N/A</td>
</tr>
<tr>
<td>10</td>
<td><strong>getOpengResultListInfoCnstwkPreparPcDetail</strong></td>
<td style="text-align: left;">개찰결과 공사 예비가격상세 목록 조회</td>
<td>N/A</td>
</tr>
<tr>
<td>11</td>
<td><strong>getOpengResultListInfoServcPreparPcDetail</strong></td>
<td style="text-align: left;">개찰결과 용역 예비가격상세 목록 조회</td>
<td>N/A</td>
</tr>
<tr>
<td>12</td>
<td><strong>getOpengResultListInfoFrgcptPreparPcDetail</strong></td>
<td style="text-align: left;">개찰결과 외자 예비가격상세 목록 조회</td>
<td>N/A</td>
</tr>
<tr>
<td>13</td>
<td><strong>getOpengResultListInfoOpengCompt</strong></td>
<td style="text-align: left;">개찰결과 개찰완료 목록 조회</td>
<td>N/A</td>
</tr>
<tr>
<td>14</td>
<td><strong>getOpengResultListInfoFailing</strong></td>
<td style="text-align: left;">개찰결과 유찰 목록 조회</td>
<td>N/A</td>
</tr>
<tr>
<td>15</td>
<td><strong>getOpengResultListInfoRebid</strong></td>
<td style="text-align: left;">개찰결과 재입찰 목록 조회</td>
<td>N/A</td>
</tr>
<tr>
<td>16.</td>
<td><strong>getScsbidListSttusThngPPSSrch</strong></td>
<td style="text-align: left;">나라장터 검색조건에 의한 낙찰된 목록 현황 물품조회</td>
<td>N/A</td>
</tr>
<tr>
<td>17</td>
<td><strong>getScsbidListSttusCnstwkPPSSrch</strong></td>
<td style="text-align: left;">나라장터 검색조건에 의한 낙찰된 목록 현황 공사조회</td>
<td>N/A</td>
</tr>
<tr>
<td>18</td>
<td><strong>getScsbidListSttusServcPPSSrch</strong></td>
<td style="text-align: left;">나라장터 검색조건에 의한 낙찰된 목록 현황 용역조회</td>
<td>N/A</td>
</tr>
<tr>
<td>19</td>
<td><strong>getScsbidListSttusFrgcptPPSSrch</strong></td>
<td style="text-align: left;">나라장터 검색조건에 의한 낙찰된 목록 현황 외자조회</td>
<td>N/A</td>
</tr>
<tr>
<td>20</td>
<td><strong>getOpengResultListInfoThngPPSSrch</strong></td>
<td style="text-align: left;">나라장터 검색조건에 의한 개찰결과 물품 목록 조회</td>
<td>N/A</td>
</tr>
<tr>
<td>21</td>
<td><strong>getOpengResultListInfoCnstwkPPSSrch</strong></td>
<td style="text-align: left;">나라장터 검색조건에 의한 개찰결과 공사 목록 조회</td>
<td>N/A</td>
</tr>
<tr>
<td>22</td>
<td><strong>getOpengResultListInfoServcPPSSrch</strong></td>
<td style="text-align: left;">나라장터 검색조건에 의한 개찰결과 용역 목록 조회</td>
<td>N/A</td>
</tr>
<tr>
<td>23</td>
<td><strong>getOpengResultListInfoFrgcptPPSSrch</strong></td>
<td style="text-align: left;">나라장터 검색조건에 의한 개찰결과 외자 목록 조회</td>
<td>N/A</td>
</tr>
</tbody>
</table>

#### \
\[낙찰된 목록 현황 물품조회\] 오퍼레이션 명세

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
<td colspan="2">낙찰된 목록 현황 물품조회</td>
</tr>
<tr>
<td>오퍼레이션 유형</td>
<td>조회(목록)</td>
<td>오퍼레이션명(영문)</td>
<td colspan="2">getScsbidListSttusThng</td>
</tr>
<tr>
<td>오퍼레이션 설명</td>
<td colspan="4">검색조건을 등록일시, 공고일시, 개찰일시, 입찰공고번호로 물품에 대한 나라장터 최종낙찰자 목록(입찰공고번호, 입찰공고명, 참가업체수, 최종낙찰업체명, 사업자번호, 최종낙찰률, 실개찰일시, 수요기관, 최종낙찰일, 최종낙찰업체담당자)을 조회</td>
</tr>
<tr>
<td>Call Back URL</td>
<td colspan="4" style="text-align: left;">N/A</td>
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

<table style="width:100%;">
<colgroup>
<col style="width: 19%" />
<col style="width: 19%" />
<col style="width: 13%" />
<col style="width: 11%" />
<col style="width: 14%" />
<col style="width: 20%" />
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
<td style="text-align: left;">공공데이터포털에서 받은 인증키</td>
<td style="text-align: left;">공공데이터포털에서 받은 인증키</td>
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
1.등록일시, 2.공고일시,3.개찰일시, 4.입찰공고번호</td>
</tr>
<tr>
<td style="text-align: left;">inqryBgnDt</td>
<td style="text-align: left;">조회시작일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">202507010000</td>
<td style="text-align: left;">검색하고자하는 시작일시<br />
'YYYYMMDDHHMM'<br />
조회구분 1,2,3일 경우 필수</td>
</tr>
<tr>
<td style="text-align: left;">inqryEndDt</td>
<td style="text-align: left;">조회종료일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">202507012359</td>
<td style="text-align: left;">검색하고자하는 종료일시<br />
'YYYYMMDDHHMM'<br />
조회구분 1,2,3일 경우 필수</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNo</td>
<td style="text-align: left;">입찰공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25BK00965123</td>
<td style="text-align: left;">검색하고자하는 입찰공고번호<br />
조회구분 4인 경우 필수</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 응답 메시지 명세

<table style="width:100%;">
<colgroup>
<col style="width: 21%" />
<col style="width: 21%" />
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 13%" />
<col style="width: 20%" />
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
<td style="text-align: left;">데이터 총 개수</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNo</td>
<td style="text-align: left;">입찰공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">R25BK00965123</td>
<td style="text-align: left;">입찰공고 관리번호이며 조달청나라장터 공고건의 형식은 년도(4)+월(2)+순번(5)이며 자체전자조달시스템 보유기관은 각 기관별 형식 별도 사용<br />
*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성<br />
- 단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</td>
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
<td style="text-align: left;">동일한 입찰공고번호에 대한 집행일련번호</td>
</tr>
<tr>
<td style="text-align: left;">rbidNo</td>
<td style="text-align: left;">재입찰번호</td>
<td style="text-align: left;">3</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">000</td>
<td style="text-align: left;">재입찰번호</td>
</tr>
<tr>
<td style="text-align: left;">ntceDivCd</td>
<td style="text-align: left;">공고구분코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">통050001</td>
<td style="text-align: left;">공고구분<br />
통050001 : 조달청 또는 나라장터 자체 공고건</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNm</td>
<td style="text-align: left;">입찰공고명</td>
<td style="text-align: left;">1000</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">혁신육아복합센터 건립공사(기계) 관급자재(간접가열보일러)</td>
<td style="text-align: left;">공사명 또는 사업명이라고도 하며 입찰공고 내용을 요약한 이름</td>
</tr>
<tr>
<td style="text-align: left;">prtcptCnum</td>
<td style="text-align: left;">참가업체수</td>
<td style="text-align: left;">6</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2</td>
<td style="text-align: left;">참가업체수</td>
</tr>
<tr>
<td style="text-align: left;">bidwinnrNm</td>
<td style="text-align: left;">최종낙찰업체명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">주식회사 동광보일러</td>
<td style="text-align: left;">최종낙찰된 업체의 명으로 개찰완료된 건에 대하여 제공</td>
</tr>
<tr>
<td style="text-align: left;">bidwinnrBizno</td>
<td style="text-align: left;">최종낙찰업체사업자등록번호</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1408121883</td>
<td style="text-align: left;">협상이 완료 후 최종낙찰된 업체의 사업자등록번호임</td>
</tr>
<tr>
<td style="text-align: left;">bidwinnrCeoNm</td>
<td style="text-align: left;">최종낙찰업체대표자명</td>
<td style="text-align: left;">35</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">박정연</td>
<td style="text-align: left;">최종낙찰된 업체의 대표자명으로 개찰완료된 건에 대하여 제공</td>
</tr>
<tr>
<td style="text-align: left;">bidwinnrAdrs</td>
<td style="text-align: left;">최종낙찰업체주소</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">충청남도 아산시 수장로 67-0 (배미동)</td>
<td style="text-align: left;">협상이 완료 후 최종낙찰된 업체의 주소임</td>
</tr>
<tr>
<td style="text-align: left;">bidwinnrTelNo</td>
<td style="text-align: left;">최종낙찰업체전화번호</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">02-6258-8989</td>
<td style="text-align: left;">협상이 완료 후 최종낙찰된 업체의 연락 전화번호임<br />
핸드폰번호는 “*”로 표기</td>
</tr>
<tr>
<td style="text-align: left;">sucsfbidAmt</td>
<td style="text-align: left;">최종낙찰금액</td>
<td style="text-align: left;">21</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">83500000</td>
<td style="text-align: left;">최종낙찰은 개찰순위 순서대로 협상등을 통해 최종 낙찰된정보를 의미하며 최종낙찰금액은 최종낙찰된 금액 (원화,원)으로 개찰완료된건에 대하여 제공</td>
</tr>
<tr>
<td style="text-align: left;">sucsfbidRate</td>
<td style="text-align: left;">최종낙찰률</td>
<td style="text-align: left;">18</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">97.82</td>
<td style="text-align: left;">예정가격대비 최종낙찰금액으로 최종낙찰금액/예정가격 * 100 으로 계산되며 개찰완료된 건에 대하여 제공 (%)</td>
</tr>
<tr>
<td style="text-align: left;">rlOpengDt</td>
<td style="text-align: left;">실개찰일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-23 11:00:00</td>
<td style="text-align: left;">실제 개찰일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">dminsttCd</td>
<td style="text-align: left;">수요기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">6280147</td>
<td style="text-align: left;">실제 수요기관의 코드로 행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드가 행자부코드가 없는 경우 조달청에서 부여한 수요기관 코드가 표기됨</td>
</tr>
<tr>
<td style="text-align: left;">dminsttNm</td>
<td style="text-align: left;">수요기관명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">인천광역시 종합건설본부</td>
<td style="text-align: left;">중앙조달인 경우 조달사업에 관한 법률 제2조(정의)에 따라 수요물자의 구매 공급 또는 시설공사 계약의 체결을 조달청장에게 요청할 수 있도록 조달청장이 인정하여 등록한 기관 또는 자체전자조달시스템을 이용하는 기관인 경우 계약을 의뢰한 기관의 명으로 공고기관과 수요기관이 동일할 수 있음</td>
</tr>
<tr>
<td style="text-align: left;">rgstDt</td>
<td>등록일시</td>
<td style="text-align: left;">19</td>
<td>1</td>
<td>2025-07-23 15:20:05</td>
<td style="text-align: left;">등록일시 "YYYY-MM-DD HH:MM:SS"</td>
</tr>
<tr>
<td>fnlSucsfDate</td>
<td>최종낙찰일자</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">0</td>
<td>2025-07-23</td>
<td style="text-align: left;">최종낙찰된 일자로 개찰완료된 건에 대하여 제공</td>
</tr>
<tr>
<td>fnlSucsfCorpOfcl</td>
<td>최종낙찰업체담당자</td>
<td style="text-align: left;">35</td>
<td style="text-align: left;">0</td>
<td>N/A</td>
<td style="text-align: left;">최종낙찰된 업체의 담당자명으로 개찰완료된 건에 대하여 제공</td>
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
<td>REST(URI)</td>
</tr>
<tr>
<td style="text-align: left;">http://apis.data.go.kr/1230000/as/ScsbidInfoService/getScsbidListSttusThng?inqryDiv=4&amp;bidNtceNo =R25BK00965123&amp;pageNo=1&amp;numOfRows=10&amp;ServiceKey=인증키</td>
</tr>
<tr>
<td>응답 메시지</td>
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
<p>&lt;bidNtceNo&gt;R25BK00965123&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;1&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;ntceDivCd&gt;통050001&lt;/ntceDivCd&gt;</p>
<p>&lt;bidNtceNm&gt;혁신육아복합센터 건립공사(기계) 관급자재(간접가열보일러)&lt;/bidNtceNm&gt;</p>
<p>&lt;prtcptCnum&gt;2&lt;/prtcptCnum&gt;</p>
<p>&lt;bidwinnrNm&gt;주식회사 동광보일러&lt;/bidwinnrNm&gt;</p>
<p>&lt;bidwinnrBizno&gt;1408121883&lt;/bidwinnrBizno&gt;</p>
<p>&lt;bidwinnrCeoNm&gt;박정연&lt;/bidwinnrCeoNm&gt;</p>
<p>&lt;bidwinnrAdrs&gt;충청남도 아산시 수장로 67-0 (배미동)&lt;/bidwinnrAdrs&gt;</p>
<p>&lt;bidwinnrTelNo&gt;02-6258-8989&lt;/bidwinnrTelNo&gt;</p>
<p>&lt;sucsfbidAmt&gt;83500000&lt;/sucsfbidAmt&gt;</p>
<p>&lt;sucsfbidRate&gt;97.82&lt;/sucsfbidRate&gt;</p>
<p>&lt;rlOpengDt&gt;2025-07-23 11:00:00&lt;/rlOpengDt&gt;</p>
<p>&lt;dminsttCd&gt;6280147&lt;/dminsttCd&gt;</p>
<p>&lt;dminsttNm&gt;인천광역시 종합건설본부&lt;/dminsttNm&gt;</p>
<p>&lt;rgstDt&gt;2025-07-23 15:20:05&lt;/rgstDt&gt;</p>
<p>&lt;fnlSucsfDate&gt;2025-07-23&lt;/fnlSucsfDate&gt;</p>
<p>&lt;fnlSucsfCorpOfcl&gt;&lt;/fnlSucsfCorpOfcl&gt;</p>
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

####  \[낙찰된 목록 현황 공사조회\] 오퍼레이션 명세

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
<td colspan="2">낙찰된 목록 현황 공사조회</td>
</tr>
<tr>
<td>오퍼레이션 유형</td>
<td>조회(목록)</td>
<td>오퍼레이션명(영문)</td>
<td colspan="2"><strong>getScsbidListSttusCnstwk</strong></td>
</tr>
<tr>
<td>오퍼레이션 설명</td>
<td colspan="4">검색조건을 등록일시, 공고일시, 개찰일시, 입찰공고번호로 공사에대한 나라장터 최종낙찰자 목록(입찰공고번호, 입찰공고명, 참가업체수, 최종낙찰업체명, 사업자번호, 최종낙찰률, 실개찰일시, 수요기관, 최종낙찰일, 최종낙찰업체담당자)을 조회</td>
</tr>
<tr>
<td>Call Back URL</td>
<td colspan="4" style="text-align: left;">N/A</td>
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
<col style="width: 14%" />
<col style="width: 20%" />
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
<td style="text-align: left;">공공데이터포털에서 받은 인증키</td>
<td style="text-align: left;">공공데이터포털에서 받은 인증키</td>
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
1.등록일시, 2.공고일시,3.개찰일시,4.입찰공고번호</td>
</tr>
<tr>
<td style="text-align: left;">inqryBgnDt</td>
<td style="text-align: left;">조회시작일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">202507010000</td>
<td style="text-align: left;">검색하고자하는 시작일시<br />
'YYYYMMDDHHMM'<br />
조회구분 1,2,3일 경우 필수</td>
</tr>
<tr>
<td style="text-align: left;">inqryEndDt</td>
<td style="text-align: left;">조회종료일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">202507012359</td>
<td style="text-align: left;">검색하고자하는 종료일시<br />
'YYYYMMDDHHMM'<br />
조회구분 1,2,3일 경우 필수</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNo</td>
<td style="text-align: left;">입찰공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25BK00922727</td>
<td style="text-align: left;">검색하고자하는 입찰공고번호<br />
조회구분 4인 경우 필수</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 응답 메시지 명세

<table style="width:100%;">
<colgroup>
<col style="width: 21%" />
<col style="width: 21%" />
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 13%" />
<col style="width: 20%" />
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
<td style="text-align: left;">데이터 총 개수</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNo</td>
<td style="text-align: left;">입찰공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">R25BK00922727</td>
<td style="text-align: left;">입찰공고 관리번호이며 조달청나라장터 공고건의 형식은 년도(4)+월(2)+순번(5)이며 자체전자조달시스템 보유기관은 각 기관별 형식 별도 사용<br />
*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성<br />
- 단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</td>
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
<td style="text-align: left;">동일한 입찰공고번호에 대한 집행일련번호</td>
</tr>
<tr>
<td style="text-align: left;">rbidNo</td>
<td style="text-align: left;">재입찰번호</td>
<td style="text-align: left;">3</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">000</td>
<td style="text-align: left;">재입찰번호</td>
</tr>
<tr>
<td style="text-align: left;">ntceDivCd</td>
<td style="text-align: left;">공고구분코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">통050001</td>
<td style="text-align: left;">공고구분<br />
통050001 : 조달청 또는 나라장터 자체 공고건</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNm</td>
<td style="text-align: left;">입찰공고명</td>
<td style="text-align: left;">1000</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">(입찰대행)신활력플러스 군지정형 어르신영농단 지원사업</td>
<td style="text-align: left;">공사명 또는 사업명이라고도 하며 입찰공고 내용을 요약한 이름</td>
</tr>
<tr>
<td style="text-align: left;">prtcptCnum</td>
<td style="text-align: left;">참가업체수</td>
<td style="text-align: left;">6</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">15</td>
<td style="text-align: left;">참가업체수</td>
</tr>
<tr>
<td style="text-align: left;">bidwinnrNm</td>
<td style="text-align: left;">최종낙찰업체명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">유한회사대가건설</td>
<td style="text-align: left;">최종낙찰된 업체의 명으로 개찰완료된 건에 대하여 제공</td>
</tr>
<tr>
<td style="text-align: left;">bidwinnrBizno</td>
<td style="text-align: left;">최종낙찰업체사업자등록번호</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">4188124255</td>
<td style="text-align: left;">협상이 완료 후 최종낙찰된 업체의 사업자등록번호임</td>
</tr>
<tr>
<td style="text-align: left;">bidwinnrCeoNm</td>
<td style="text-align: left;">최종낙찰업체대표자명</td>
<td style="text-align: left;">35</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">강훈희</td>
<td style="text-align: left;">최종낙찰된 업체의 대표자명으로 개찰완료된 건에 대하여 제공</td>
</tr>
<tr>
<td style="text-align: left;">bidwinnrAdrs</td>
<td style="text-align: left;">최종낙찰업체주소</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">전북특별자치도 부안군 부안읍 서외리 455-3,제1층 제3호</td>
<td style="text-align: left;">협상이 완료 후 최종낙찰된 업체의 주소임</td>
</tr>
<tr>
<td style="text-align: left;">bidwinnrTelNo</td>
<td style="text-align: left;">최종낙찰업체전화번호</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">063-581-8121</td>
<td style="text-align: left;">협상이 완료 후 최종낙찰된 업체의 연락 전화번호임<br />
핸드폰번호는 “*”로 표기</td>
</tr>
<tr>
<td style="text-align: left;">sucsfbidAmt</td>
<td style="text-align: left;">최종낙찰금액</td>
<td style="text-align: left;">21</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">58708988</td>
<td style="text-align: left;">최종낙찰은 개찰순위 순서대로 협상등을 통해 최종 낙찰된정보를 의미하며 최종낙찰금액은 최종낙찰된 금액 (원화,원)으로 개찰완료된건에 대하여 제공</td>
</tr>
<tr>
<td style="text-align: left;">sucsfbidRate</td>
<td style="text-align: left;">최종낙찰률</td>
<td style="text-align: left;">18</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">90.278</td>
<td style="text-align: left;">예정가격대비 최종낙찰금액으로 최종낙찰금액/예정가격 * 100 으로 계산되며 개찰완료된 건에 대하여 제공 (%)</td>
</tr>
<tr>
<td style="text-align: left;">rlOpengDt</td>
<td style="text-align: left;">실개찰일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-06-27 12:00:00</td>
<td style="text-align: left;">실제 개찰일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">dminsttCd</td>
<td style="text-align: left;">수요기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">4791000</td>
<td style="text-align: left;">실제 수요기관의 코드로 행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드가 행자부코드가 없는 경우 조달청에서 부여한 수요기관 코드가 표기됨</td>
</tr>
<tr>
<td style="text-align: left;">dminsttNm</td>
<td style="text-align: left;">수요기관명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">전북특별자치도 부안군</td>
<td style="text-align: left;">중앙조달인 경우 조달사업에 관한 법률 제2조(정의)에 따라 수요물자의 구매 공급 또는 시설공사 계약의 체결을 조달청장에게 요청할 수 있도록 조달청장이 인정하여 등록한 기관 또는 자체전자조달시스템을 이용하는 기관인 경우 계약을 의뢰한 기관의 명으로 공고기관과 수요기관이 동일할 수 있음</td>
</tr>
<tr>
<td style="text-align: left;">rgstDt</td>
<td>등록일시</td>
<td style="text-align: left;">19</td>
<td>1</td>
<td>2025-07-01 13:54:43</td>
<td style="text-align: left;">등록일시 "YYYY-MM-DD HH:MM:SS"</td>
</tr>
<tr>
<td>fnlSucsfDate</td>
<td>최종낙찰일자</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">0</td>
<td>2025-07-01</td>
<td style="text-align: left;">최종낙찰된 일자로 개찰완료된 건에 대하여 제공</td>
</tr>
<tr>
<td>fnlSucsfCorpOfcl</td>
<td>최종낙찰업체담당자</td>
<td style="text-align: left;">35</td>
<td style="text-align: left;">0</td>
<td>N/A</td>
<td>최종낙찰된 업체의 담당자명으로 개찰완료된 건에 대하여 제공</td>
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
<td>REST(URI)</td>
</tr>
<tr>
<td style="text-align: left;">http://apis.data.go.kr/1230000/as/ScsbidInfoService/getScsbidListSttusCnstwk?inqryDiv=4&amp; bidNtceNo= R25BK00922727&amp;pageNo=1&amp;numOfRows=10&amp;ServiceKey=인증키</td>
</tr>
<tr>
<td>응답 메시지</td>
</tr>
<tr>
<td><p>&lt;response&gt;</p>
<p>&lt;header&gt;</p>
<p>&lt;resultCode&gt;00&lt;/resultCode&gt;</p>
<p>&lt;resultMsg&gt;정상&lt;/resultMsg&gt;</p>
<p>&lt;/header&gt;</p>
<p>&lt;body&gt;</p>
<p>&lt;items&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00922727&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;0&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;ntceDivCd&gt;통050001&lt;/ntceDivCd&gt;</p>
<p>&lt;bidNtceNm&gt;(입찰대행)신활력플러스 군지정형 어르신영농단 지원사업&lt;/bidNtceNm&gt;</p>
<p>&lt;prtcptCnum&gt;15&lt;/prtcptCnum&gt;</p>
<p>&lt;bidwinnrNm&gt;유한회사대가건설&lt;/bidwinnrNm&gt;</p>
<p>&lt;bidwinnrBizno&gt;4188124255&lt;/bidwinnrBizno&gt;</p>
<p>&lt;bidwinnrCeoNm&gt;강훈희&lt;/bidwinnrCeoNm&gt;</p>
<p>&lt;bidwinnrAdrs&gt;전북특별자치도 부안군 부안읍 서외리 455-3,제1층 제3호&lt;/bidwinnrAdrs&gt;</p>
<p>&lt;bidwinnrTelNo&gt;063-581-8121&lt;/bidwinnrTelNo&gt;</p>
<p>&lt;sucsfbidAmt&gt;58708988&lt;/sucsfbidAmt&gt;</p>
<p>&lt;sucsfbidRate&gt;90.278&lt;/sucsfbidRate&gt;</p>
<p>&lt;rlOpengDt&gt;2025-06-27 12:00:00&lt;/rlOpengDt&gt;</p>
<p>&lt;dminsttCd&gt;4791000&lt;/dminsttCd&gt;</p>
<p>&lt;dminsttNm&gt;전북특별자치도 부안군&lt;/dminsttNm&gt;</p>
<p>&lt;rgstDt&gt;2025-07-01 13:54:43&lt;/rgstDt&gt;</p>
<p>&lt;fnlSucsfDate&gt;2025-07-01&lt;/fnlSucsfDate&gt;</p>
<p>&lt;fnlSucsfCorpOfcl&gt;&lt;/fnlSucsfCorpOfcl&gt;</p>
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

#### \[낙찰된 목록 현황 용역조회\] 오퍼레이션 명세

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
<td colspan="2">낙찰된 목록 현황 용역조회</td>
</tr>
<tr>
<td>오퍼레이션 유형</td>
<td>조회(목록)</td>
<td>오퍼레이션명(영문)</td>
<td colspan="2"><strong>getScsbidListSttusServc</strong></td>
</tr>
<tr>
<td>오퍼레이션 설명</td>
<td colspan="4">검색조건을 등록일시, 공고일시, 개찰일시, 입찰공고번호로 용역에 대한 나라장터 최종낙찰자 목록(입찰공고번호, 입찰공고명, 참가업체수, 최종낙찰업체명, 사업자번호, 최종낙찰률, 실개찰일시, 수요기관, 최종낙찰일, 최종낙찰업체담당자)을 조회</td>
</tr>
<tr>
<td>Call Back URL</td>
<td colspan="4" style="text-align: left;">N/A</td>
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
<col style="width: 11%" />
<col style="width: 14%" />
<col style="width: 20%" />
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
<td>4</td>
<td>1</td>
<td>10</td>
<td>한 페이지 결과 수</td>
</tr>
<tr>
<td>pageNo</td>
<td>페이지 번호</td>
<td>4</td>
<td>1</td>
<td>1</td>
<td style="text-align: left;">페이지 번호</td>
</tr>
<tr>
<td style="text-align: left;">ServiceKey</td>
<td style="text-align: left;">서비스키</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">공공데이터포털에서 받은 인증키</td>
<td style="text-align: left;">공공데이터포털에서 받은 인증키</td>
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
<td>조회구분</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">검색하고자하는 조회구분<br />
1.등록일시, 2.공고일시, 3.개찰일시, 4.입찰공고번호</td>
</tr>
<tr>
<td>inqryBgnDt</td>
<td>조회시작일시</td>
<td>12</td>
<td style="text-align: left;">0</td>
<td>202507010000</td>
<td>검색하고자하는 시작일시<br />
'YYYYMMDDHHMM'<br />
조회구분 1,2,3일 경우 필수</td>
</tr>
<tr>
<td>inqryEndDt</td>
<td>조회종료일시</td>
<td>12</td>
<td style="text-align: left;">0</td>
<td>202507012359</td>
<td>검색하고자하는 종료일시<br />
'YYYYMMDDHHMM'<br />
조회구분 1,2,3일 경우 필수</td>
</tr>
<tr>
<td>bidNtceNo</td>
<td>입찰공고번호</td>
<td>40</td>
<td style="text-align: left;">0</td>
<td>R25BK00927163</td>
<td style="text-align: left;">검색하고자하는 입찰공고번호<br />
조회구분 4인 경우 필수</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 응답 메시지 명세

<table style="width:100%;">
<colgroup>
<col style="width: 21%" />
<col style="width: 21%" />
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 13%" />
<col style="width: 20%" />
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
<td>numOfRows</td>
<td>한 페이지 결과 수</td>
<td>4</td>
<td>1</td>
<td>10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td>pageNo</td>
<td>페이지 번호</td>
<td>4</td>
<td>1</td>
<td>1</td>
<td style="text-align: left;">페이지 수</td>
</tr>
<tr>
<td>totalCount</td>
<td>데이터 총 개수</td>
<td>4</td>
<td>1</td>
<td>10</td>
<td style="text-align: left;">데이터 총 개수</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNo</td>
<td>입찰공고번호</td>
<td>40</td>
<td style="text-align: left;">1</td>
<td>R25BK00927163</td>
<td style="text-align: left;">입찰공고 관리번호이며 조달청나라장터 공고건의 형식은 년도(4)+월(2)+순번(5)이며 자체전자조달시스템 보유기관은 각 기관별 형식 별도 사용<br />
*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성<br />
- 단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceOrd</td>
<td>입찰공고차수</td>
<td>3</td>
<td style="text-align: left;">1</td>
<td>000</td>
<td style="text-align: left;">입찰공고차수는 해당 입찰공고에 대한 재공고 및 재입찰 등이 발생되었을 경우 증가되는 수</td>
</tr>
<tr>
<td>bidClsfcNo</td>
<td>입찰분류번호</td>
<td>5</td>
<td style="text-align: left;">1</td>
<td>0</td>
<td style="text-align: left;">동일한 입찰공고번호에 대한 집행일련번호</td>
</tr>
<tr>
<td>rbidNo</td>
<td>재입찰번호</td>
<td>3</td>
<td style="text-align: left;">1</td>
<td>000</td>
<td style="text-align: left;">재입찰번호</td>
</tr>
<tr>
<td>ntceDivCd</td>
<td>공고구분코드</td>
<td>7</td>
<td style="text-align: left;">1</td>
<td>통050001</td>
<td style="text-align: left;">공고구분<br />
통050001 : 조달청 또는 나라장터 자체 공고건</td>
</tr>
<tr>
<td>bidNtceNm</td>
<td>입찰공고명</td>
<td>1000</td>
<td style="text-align: left;">1</td>
<td>동물원(해양관, 남미관) 종합안내판 변경 제작 시행</td>
<td style="text-align: left;">공사명 또는 사업명이라고도 하며 입찰공고 내용을 요약한 이름</td>
</tr>
<tr>
<td>prtcptCnum</td>
<td>참가업체수</td>
<td>6</td>
<td style="text-align: left;">0</td>
<td>1</td>
<td style="text-align: left;">참가업체수</td>
</tr>
<tr>
<td>bidwinnrNm</td>
<td>최종낙찰업체명</td>
<td>200</td>
<td style="text-align: left;">1</td>
<td>주식회사 나무조각 에코사인</td>
<td style="text-align: left;">최종낙찰된 업체의 명으로 개찰완료된 건에 대하여 제공</td>
</tr>
<tr>
<td>bidwinnrBizno</td>
<td>최종낙찰업체사업자등록번호</td>
<td>10</td>
<td style="text-align: left;">1</td>
<td>1238640842</td>
<td style="text-align: left;">협상이 완료 후 최종낙찰된 업체의 사업자등록번호임</td>
</tr>
<tr>
<td>bidwinnrCeoNm</td>
<td>최종낙찰업체대표자명</td>
<td>35</td>
<td style="text-align: left;">0</td>
<td>조선미</td>
<td style="text-align: left;">최종낙찰된 업체의 대표자명으로 개찰완료된 건에 대하여 제공</td>
</tr>
<tr>
<td>bidwinnrAdrs</td>
<td>최종낙찰업체주소</td>
<td>200</td>
<td style="text-align: left;">0</td>
<td>경기도 화성시 기안말길 17-0 (기안동)</td>
<td style="text-align: left;">협상이 완료 후 최종낙찰된 업체의 주소임</td>
</tr>
<tr>
<td>bidwinnrTelNo</td>
<td>최종낙찰업체전화번호</td>
<td>25</td>
<td style="text-align: left;">0</td>
<td>070-8273-0625</td>
<td style="text-align: left;">협상이 완료 후 최종낙찰된 업체의 연락 전화번호임<br />
핸드폰번호는 “*”로 표기</td>
</tr>
<tr>
<td>sucsfbidAmt</td>
<td>최종낙찰금액</td>
<td>21</td>
<td style="text-align: left;">0</td>
<td>38832000</td>
<td style="text-align: left;">최종낙찰은 개찰순위 순서대로 협상등을 통해 최종 낙찰된정보를 의미하며 최종낙찰금액은 최종낙찰된 금액 (원화,원)으로 개찰완료된건에 대하여 제공</td>
</tr>
<tr>
<td>sucsfbidRate</td>
<td>최종낙찰률</td>
<td>18</td>
<td style="text-align: left;">0</td>
<td>94.999</td>
<td style="text-align: left;">예정가격대비 최종낙찰금액으로 최종낙찰금액/예정가격 * 100 으로 계산되며 개찰완료된 건에 대하여 제공 (%)</td>
</tr>
<tr>
<td>rlOpengDt</td>
<td>실개찰일시</td>
<td>19</td>
<td style="text-align: left;">0</td>
<td>2025-06-30 18:00:00</td>
<td style="text-align: left;">실제 개찰일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td>dminsttCd</td>
<td>수요기관코드</td>
<td>7</td>
<td style="text-align: left;">0</td>
<td>6112581</td>
<td style="text-align: left;">실제 수요기관의 코드로 행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드가 행자부코드가 없는 경우 조달청에서 부여한 수요기관 코드가 표기됨</td>
</tr>
<tr>
<td>dminsttNm</td>
<td>수요기관명</td>
<td>200</td>
<td style="text-align: left;">0</td>
<td>서울특별시 서울대공원</td>
<td style="text-align: left;">중앙조달인 경우 조달사업에 관한 법률 제2조(정의)에 따라 수요물자의 구매 공급 또는 시설공사 계약의 체결을 조달청장에게 요청할 수 있도록 조달청장이 인정하여 등록한 기관 또는 자체전자조달시스템을 이용하는 기관인 경우 계약을 의뢰한 기관의 명으로 공고기관과 수요기관이 동일할 수 있음</td>
</tr>
<tr>
<td style="text-align: left;">rgstDt</td>
<td>등록일시</td>
<td style="text-align: left;">19</td>
<td>1</td>
<td>2025-07-01 13:39:16</td>
<td style="text-align: left;">등록일시 "YYYY-MM-DD HH:MM:SS"</td>
</tr>
<tr>
<td>fnlSucsfDate</td>
<td>최종낙찰일자</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">0</td>
<td>2025-07-01</td>
<td style="text-align: left;">최종낙찰된 일자로 개찰완료된 건에 대하여 제공</td>
</tr>
<tr>
<td>fnlSucsfCorpOfcl</td>
<td>최종낙찰업체담당자</td>
<td style="text-align: left;">35</td>
<td style="text-align: left;">0</td>
<td>N/A</td>
<td>최종낙찰된 업체의 담당자명으로 개찰완료된 건에 대하여 제공</td>
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
<td>REST(URI)</td>
</tr>
<tr>
<td style="text-align: left;">http://apis.data.go.kr/1230000/as/ScsbidInfoService/getScsbidListSttusServc?inqryDiv=4&amp; bidNtceNo=R25BK00927163&amp;pageNo=1&amp;numOfRows=10&amp;ServiceKey=인증키</td>
</tr>
<tr>
<td>응답 메시지</td>
</tr>
<tr>
<td><p>&lt;response&gt;</p>
<p>&lt;header&gt;</p>
<p>&lt;resultCode&gt;00&lt;/resultCode&gt;</p>
<p>&lt;resultMsg&gt;정상&lt;/resultMsg&gt;</p>
<p>&lt;/header&gt;</p>
<p>&lt;body&gt;</p>
<p>&lt;items&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00927163&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;0&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;ntceDivCd&gt;통050001&lt;/ntceDivCd&gt;</p>
<p>&lt;bidNtceNm&gt;동물원(해양관, 남미관) 종합안내판 변경 제작 시행&lt;/bidNtceNm&gt;</p>
<p>&lt;prtcptCnum&gt;1&lt;/prtcptCnum&gt;</p>
<p>&lt;bidwinnrNm&gt;주식회사 나무조각 에코사인&lt;/bidwinnrNm&gt;</p>
<p>&lt;bidwinnrBizno&gt;1238640842&lt;/bidwinnrBizno&gt;</p>
<p>&lt;bidwinnrCeoNm&gt;조선미&lt;/bidwinnrCeoNm&gt;</p>
<p>&lt;bidwinnrAdrs&gt;경기도 화성시 기안말길 17-0 (기안동)&lt;/bidwinnrAdrs&gt;</p>
<p>&lt;bidwinnrTelNo&gt;070-8273-0625&lt;/bidwinnrTelNo&gt;</p>
<p>&lt;sucsfbidAmt&gt;38832000&lt;/sucsfbidAmt&gt;</p>
<p>&lt;sucsfbidRate&gt;94.999&lt;/sucsfbidRate&gt;</p>
<p>&lt;rlOpengDt&gt;2025-06-30 18:00:00&lt;/rlOpengDt&gt;</p>
<p>&lt;dminsttCd&gt;6112581&lt;/dminsttCd&gt;</p>
<p>&lt;dminsttNm&gt;서울특별시 서울대공원&lt;/dminsttNm&gt;</p>
<p>&lt;rgstDt&gt;2025-07-01 13:39:16&lt;/rgstDt&gt;</p>
<p>&lt;fnlSucsfDate&gt;2025-07-01&lt;/fnlSucsfDate&gt;</p>
<p>&lt;fnlSucsfCorpOfcl&gt;&lt;/fnlSucsfCorpOfcl&gt;</p>
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

#### \[낙찰된 목록 현황 외자조회\] 오퍼레이션 명세

<table style="width:100%;">
<colgroup>
<col style="width: 4%" />
<col style="width: 21%" />
<col style="width: 17%" />
<col style="width: 21%" />
<col style="width: 2%" />
<col style="width: 32%" />
</colgroup>
<tbody>
<tr>
<td rowspan="6">오퍼레이션 정보</td>
<td>오퍼레이션 번호</td>
<td>4</td>
<td>오퍼레이션명(국문)</td>
<td colspan="2">낙찰된 목록 현황 외자조회</td>
</tr>
<tr>
<td>오퍼레이션 유형</td>
<td>조회(목록)</td>
<td>오퍼레이션명(영문)</td>
<td colspan="2"><strong>getScsbidListSttusFrgcpt</strong></td>
</tr>
<tr>
<td>오퍼레이션 설명</td>
<td colspan="4">검색조건을 등록일시, 공고일시, 개찰일시, 입찰공고번호로 외자에 대한 나라장터 최종낙찰자 목록(입찰공고번호, 입찰공고명, 참가업체수, 최종낙찰업체명, 사업자번호, 최종낙찰률, 실개찰일시, 수요기관, 최종낙찰일, 최종낙찰업체담당자)을 조회</td>
</tr>
<tr>
<td>Call Back URL</td>
<td colspan="4" style="text-align: left;">N/A</td>
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

<table style="width:100%;">
<colgroup>
<col style="width: 19%" />
<col style="width: 19%" />
<col style="width: 13%" />
<col style="width: 11%" />
<col style="width: 14%" />
<col style="width: 19%" />
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
<td>4</td>
<td>1</td>
<td>10</td>
<td>한 페이지 결과 수</td>
</tr>
<tr>
<td>pageNo</td>
<td>페이지 번호</td>
<td>4</td>
<td>1</td>
<td>1</td>
<td>페이지 번호</td>
</tr>
<tr>
<td style="text-align: left;">ServiceKey</td>
<td style="text-align: left;">서비스키</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">공공데이터포털에서 받은 인증키</td>
<td style="text-align: left;">공공데이터포털에서 받은 인증키</td>
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
1.등록일시, 2.공고일시,3.개찰일시,4.입찰공고번호</td>
</tr>
<tr>
<td>inqryBgnDt</td>
<td>조회시작일시</td>
<td>12</td>
<td style="text-align: left;">0</td>
<td>202507010000</td>
<td>검색하고자하는 시작일시<br />
'YYYYMMDDHHMM'<br />
조회구분 1,2,3일 경우 필수</td>
</tr>
<tr>
<td>inqryEndDt</td>
<td>조회종료일시</td>
<td>12</td>
<td style="text-align: left;">0</td>
<td>202507102359</td>
<td>검색하고자하는 종료일시<br />
'YYYYMMDDHHMM'<br />
조회구분 1,2,3일 경우 필수</td>
</tr>
<tr>
<td>bidNtceNo</td>
<td>입찰공고번호</td>
<td>40</td>
<td style="text-align: left;">0</td>
<td>R25BK00857114</td>
<td style="text-align: left;">검색하고자하는 입찰공고번호<br />
조회구분 4인 경우 필수</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 응답 메시지 명세

<table style="width:100%;">
<colgroup>
<col style="width: 21%" />
<col style="width: 21%" />
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 13%" />
<col style="width: 20%" />
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
<td>numOfRows</td>
<td>한 페이지 결과 수</td>
<td>4</td>
<td>1</td>
<td>10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td>pageNo</td>
<td>페이지 번호</td>
<td>4</td>
<td>1</td>
<td>1</td>
<td style="text-align: left;">페이지 수</td>
</tr>
<tr>
<td>totalCount</td>
<td>데이터 총 개수</td>
<td>4</td>
<td>1</td>
<td>17</td>
<td style="text-align: left;">데이터 총 개수</td>
</tr>
<tr>
<td>bidNtceNo</td>
<td>입찰공고번호</td>
<td>40</td>
<td>1</td>
<td>R25BK00857114</td>
<td style="text-align: left;">입찰공고 관리번호이며 조달청나라장터 공고건의 형식은 년도(4)+월(2)+순번(5)이며 자체전자조달시스템 보유기관은 각 기관별 형식 별도 사용<br />
*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성<br />
- 단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</td>
</tr>
<tr>
<td>bidNtceOrd</td>
<td>입찰공고차수</td>
<td>3</td>
<td style="text-align: left;">1</td>
<td>000</td>
<td style="text-align: left;">입찰공고차수는 해당 입찰공고에 대한 재공고 및 재입찰 등이 발생되었을 경우 증가되는 수</td>
</tr>
<tr>
<td>bidClsfcNo</td>
<td>입찰분류번호</td>
<td>5</td>
<td style="text-align: left;">1</td>
<td>1</td>
<td style="text-align: left;">동일한 입찰공고번호에 대한 집행일련번호</td>
</tr>
<tr>
<td>rbidNo</td>
<td>재입찰번호</td>
<td>3</td>
<td style="text-align: left;">1</td>
<td>000</td>
<td style="text-align: left;">재입찰번호</td>
</tr>
<tr>
<td>ntceDivCd</td>
<td>공고구분코드</td>
<td>7</td>
<td style="text-align: left;">1</td>
<td>통050001</td>
<td style="text-align: left;">공고구분<br />
통050001 : 조달청 또는 나라장터 자체 공고건</td>
</tr>
<tr>
<td>bidNtceNm</td>
<td>입찰공고명</td>
<td>1000</td>
<td style="text-align: left;">1</td>
<td>(외자)가스크로마토그래프-질량분석기</td>
<td style="text-align: left;">공사명 또는 사업명이라고도 하며 입찰공고 내용을 요약한 이름</td>
</tr>
<tr>
<td>prtcptCnum</td>
<td>참가업체수</td>
<td>6</td>
<td style="text-align: left;">0</td>
<td>1</td>
<td style="text-align: left;">참가업체수</td>
</tr>
<tr>
<td>bidwinnrNm</td>
<td>최종낙찰업체명</td>
<td>200</td>
<td style="text-align: left;">1</td>
<td>주식회사 시마즈 사이언티픽 코리아</td>
<td style="text-align: left;">최종낙찰된 업체의 명으로 개찰완료된 건에 대하여 제공</td>
</tr>
<tr>
<td>bidwinnrBizno</td>
<td>최종낙찰업체사업자등록번호</td>
<td>10</td>
<td style="text-align: left;">1</td>
<td>3078701124</td>
<td style="text-align: left;">협상이 완료 후 최종낙찰된 업체의 사업자등록번호임</td>
</tr>
<tr>
<td>bidwinnrCeoNm</td>
<td>최종낙찰업체대표자명</td>
<td>35</td>
<td style="text-align: left;">0</td>
<td>야마다 타케시</td>
<td style="text-align: left;">최종낙찰된 업체의 대표자명으로 개찰완료된 건에 대하여 제공</td>
</tr>
<tr>
<td>bidwinnrAdrs</td>
<td>최종낙찰업체주소</td>
<td>200</td>
<td style="text-align: left;">0</td>
<td>서울특별시 강남구 언주로 609, 9층(논현동 , 팍스타워)</td>
<td style="text-align: left;">협상이 완료 후 최종낙찰된 업체의 주소임</td>
</tr>
<tr>
<td>bidwinnrTelNo</td>
<td>최종낙찰업체전화번호</td>
<td>25</td>
<td style="text-align: left;">0</td>
<td>042-864-1161</td>
<td style="text-align: left;">협상이 완료 후 최종낙찰된 업체의 연락 전화번호임<br />
핸드폰번호는 “*”로 표기</td>
</tr>
<tr>
<td>sucsfbidAmt</td>
<td>최종낙찰금액</td>
<td>21</td>
<td style="text-align: left;">0</td>
<td>27538049</td>
<td style="text-align: left;">최종낙찰은 개찰순위 순서대로 협상등을 통해 최종 낙찰된정보를 의미하며 최종낙찰금액은 최종낙찰된 금액 (원화,원)으로 개찰완료된건에 대하여 제공</td>
</tr>
<tr>
<td>sucsfbidRate</td>
<td>최종낙찰률</td>
<td>18</td>
<td style="text-align: left;">0</td>
<td>0</td>
<td style="text-align: left;">예정가격대비 최종낙찰금액으로 최종낙찰금액/예정가격 * 100 으로 계산되며 개찰완료된 건에 대하여 제공 (%)</td>
</tr>
<tr>
<td>rlOpengDt</td>
<td>실개찰일시</td>
<td>19</td>
<td style="text-align: left;">0</td>
<td>2025-06-05 15:00:00</td>
<td style="text-align: left;">실제 개찰일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td>dminsttCd</td>
<td>수요기관코드</td>
<td>7</td>
<td style="text-align: left;">0</td>
<td>1482021</td>
<td style="text-align: left;">실제 수요기관의 코드로 행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드가 행자부코드가 없는 경우 조달청에서 부여한 수요기관 코드가 표기됨</td>
</tr>
<tr>
<td style="text-align: left;">dminsttNm</td>
<td>수요기관명</td>
<td>200</td>
<td style="text-align: left;">0</td>
<td>환경부 국립환경과학원</td>
<td style="text-align: left;">중앙조달인 경우 조달사업에 관한 법률 제2조(정의)에 따라 수요물자의 구매 공급 또는 시설공사 계약의 체결을 조달청장에게 요청할 수 있도록 조달청장이 인정하여 등록한 기관 또는 자체전자조달시스템을 이용하는 기관인 경우 계약을 의뢰한 기관의 명으로 공고기관과 수요기관이 동일할 수 있음</td>
</tr>
<tr>
<td style="text-align: left;">rgstDt</td>
<td>등록일시</td>
<td style="text-align: left;">19</td>
<td>1</td>
<td>2025-07-07 09:17:48</td>
<td style="text-align: left;">등록일시 "YYYY-MM-DD HH:MM:SS"</td>
</tr>
<tr>
<td>FnlSucsfDate</td>
<td>최종낙찰일자</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">0</td>
<td>2025-07-07</td>
<td style="text-align: left;">최종낙찰된 일자로 개찰완료된 건에 대하여 제공</td>
</tr>
<tr>
<td>fnlSucsfCorpOfcl</td>
<td>최종낙찰업체담당자</td>
<td style="text-align: left;">35</td>
<td style="text-align: left;">0</td>
<td>N/A</td>
<td style="text-align: left;">최종낙찰된 업체의 담당자명으로 개찰완료된 건에 대하여 제공</td>
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
<td>REST(URI)</td>
</tr>
<tr>
<td style="text-align: left;">http://apis.data.go.kr/1230000/as/ScsbidInfoService/getScsbidListSttusFrgcpt?inqryDiv=4&amp; bidNtceNo= R25BK00857114&amp;pageNo=1&amp;numOfRows=10&amp;ServiceKey=인증키</td>
</tr>
<tr>
<td>응답 메시지</td>
</tr>
<tr>
<td><p>&lt;response&gt;</p>
<p>&lt;header&gt;</p>
<p>&lt;resultCode&gt;00&lt;/resultCode&gt;</p>
<p>&lt;resultMsg&gt;정상&lt;/resultMsg&gt;</p>
<p>&lt;/header&gt;</p>
<p>&lt;body&gt;</p>
<p>&lt;items&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00857114&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;1&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;ntceDivCd&gt;통050001&lt;/ntceDivCd&gt;</p>
<p>&lt;bidNtceNm&gt;(외자)가스크로마토그래프-질량분석기&lt;/bidNtceNm&gt;</p>
<p>&lt;prtcptCnum&gt;1&lt;/prtcptCnum&gt;</p>
<p>&lt;bidwinnrNm&gt;주식회사 시마즈 사이언티픽 코리아&lt;/bidwinnrNm&gt;</p>
<p>&lt;bidwinnrBizno&gt;3078701124&lt;/bidwinnrBizno&gt;</p>
<p>&lt;bidwinnrCeoNm&gt;야마다 타케시&lt;/bidwinnrCeoNm&gt;</p>
<p>&lt;bidwinnrAdrs&gt;서울특별시 강남구 언주로 609, 9층(논현동 , 팍스타워)&lt;/bidwinnrAdrs&gt;</p>
<p>&lt;bidwinnrTelNo&gt;042-864-1161&lt;/bidwinnrTelNo&gt;</p>
<p>&lt;sucsfbidAmt&gt;27538049&lt;/sucsfbidAmt&gt;</p>
<p>&lt;sucsfbidRate&gt;&lt;/sucsfbidRate&gt;</p>
<p>&lt;rlOpengDt&gt;2025-06-05 15:00:00&lt;/rlOpengDt&gt;</p>
<p>&lt;dminsttCd&gt;1482021&lt;/dminsttCd&gt;</p>
<p>&lt;dminsttNm&gt;환경부 국립환경과학원&lt;/dminsttNm&gt;</p>
<p>&lt;rgstDt&gt;2025-07-07 09:17:48&lt;/rgstDt&gt;</p>
<p>&lt;fnlSucsfDate&gt;2025-07-07&lt;/fnlSucsfDate&gt;</p>
<p>&lt;fnlSucsfCorpOfcl&gt;&lt;/fnlSucsfCorpOfcl&gt;</p>
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

#### \[개찰결과 물품 목록 조회\] 오퍼레이션 명세

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
<td colspan="2">개찰결과 물품 목록 조회</td>
</tr>
<tr>
<td>오퍼레이션 유형</td>
<td>조회(목록)</td>
<td>오퍼레이션명(영문)</td>
<td colspan="2"><strong>getOpengResultListInfoThng</strong></td>
</tr>
<tr>
<td>오퍼레이션 설명</td>
<td colspan="4">유찰, 개찰완료, 재입찰건에 대한 개찰결과를 제공하며 검색조건을 입력일시, 공고일시, 개찰일시, 입찰공고번호로하여 물품에 대한 나라장터 개찰결과 목록(입찰공고번호, 입찰공고명, 개찰일시, 참가업체수, 개찰업체정보, 진행구분코드명, 입력일시, 예비가격파일존재여부, 공고기관명, 수요기관명)을 조회</td>
</tr>
<tr>
<td>Call Back URL</td>
<td colspan="4" style="text-align: left;">N/A</td>
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
<col style="width: 22%" />
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 14%" />
<col style="width: 20%" />
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
<td>4</td>
<td>1</td>
<td>10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td>pageNo</td>
<td>페이지 번호</td>
<td>4</td>
<td>1</td>
<td>1</td>
<td style="text-align: left;">페이지 번호</td>
</tr>
<tr>
<td style="text-align: left;">ServiceKey</td>
<td style="text-align: left;">서비스키</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">공공데이터포털에서 받은 인증키</td>
<td style="text-align: left;">공공데이터포털에서 받은 인증키</td>
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
<td>조회구분</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">검색하고자하는 조회구분<br />
1.입력일시, 2.공고일시, 3.개찰일시, 4.입찰공고번호</td>
</tr>
<tr>
<td>inqryBgnDt</td>
<td>조회시작일시</td>
<td>12</td>
<td style="text-align: left;">0</td>
<td>202507010000</td>
<td>검색하고자하는 시작일시<br />
'YYYYMMDDHHMM'<br />
조회구분 1,2,3일 경우 필수</td>
</tr>
<tr>
<td>inqryEndDt</td>
<td>조회종료일시</td>
<td>12</td>
<td style="text-align: left;">0</td>
<td>202507012359</td>
<td>검색하고자하는 종료일시<br />
'YYYYMMDDHHMM'<br />
조회구분 1,2,3일 경우 필수</td>
</tr>
<tr>
<td>bidNtceNo</td>
<td>입찰공고번호</td>
<td>11</td>
<td style="text-align: left;">0</td>
<td>R25BK00840922</td>
<td style="text-align: left;">검색하고자하는 입찰공고번호<br />
조회구분 4인 경우 필수</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 응답 메시지 명세

<table style="width:100%;">
<colgroup>
<col style="width: 21%" />
<col style="width: 21%" />
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 13%" />
<col style="width: 20%" />
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
<td style="text-align: left;">데이터 총 개수</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNo</td>
<td style="text-align: left;">입찰공고번호</td>
<td style="text-align: left;">11</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">R25BK00840922</td>
<td style="text-align: left;">입찰공고 관리번호이며 조달청나라장터 공고건의 형식은 년도(4)+월(2)+순번(5)이며 자체전자조달시스템 보유기관은 각 기관별 형식 별도 사용<br />
*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성<br />
- 단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</td>
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
<td style="text-align: left;">동일한 입찰공고번호에 대한 집행일련번호</td>
</tr>
<tr>
<td style="text-align: left;">rbidNo</td>
<td style="text-align: left;">재입찰번호</td>
<td style="text-align: left;">3</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">000</td>
<td style="text-align: left;">재입찰번호</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNm</td>
<td style="text-align: left;">입찰공고명</td>
<td style="text-align: left;">1000</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">근접전자기장 내성 시험 시스템 구축</td>
<td style="text-align: left;">공사명 또는 사업명이라고도 하며 입찰공고 내용을 요약한 이름</td>
</tr>
<tr>
<td style="text-align: left;">opengDt</td>
<td style="text-align: left;">개찰일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">2025-06-17 11:00:00</td>
<td style="text-align: left;">조달업체가 제출한 입찰서를 개찰하는 일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">prtcptCnum</td>
<td style="text-align: left;">참가업체수</td>
<td style="text-align: left;">6</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2</td>
<td style="text-align: left;">참가업체수</td>
</tr>
<tr>
<td style="text-align: left;">opengCorpInfo</td>
<td style="text-align: left;">개찰업체정보</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">이엠테스트코리아 주식회사^1428139282^김종인^178750000^97.992</td>
<td style="text-align: left;"><p>개찰업체정보<br />
다수 낙찰자의 경우 ”낙찰예정자 다수”와 개찰순위 1위의 투찰금액과 투찰율<br />
을 보여줌</p>
<p>단일 낙찰자 의 경우 업체명과 사업자번호, 대표자명, 투찰금액, 투찰율을 보여줌</p>
<p>단, 협상에 의한 계약일 경우는 투찰금액,투찰율 안나옴</p></td>
</tr>
<tr>
<td style="text-align: left;">progrsDivCdNm</td>
<td style="text-align: left;">진행구분코드명</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">개찰완료</td>
<td style="text-align: left;"><p>진행구분이</p>
<p>유찰, 개찰완료, 재입찰로 구분 됨</p></td>
</tr>
<tr>
<td style="text-align: left;">inptDt</td>
<td style="text-align: left;">입력일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-14 09:57:49</td>
<td style="text-align: left;">입력일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">rsrvtnPrceFileExistnceYn</td>
<td style="text-align: left;">예비가격파일존재여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">Y</td>
<td style="text-align: left;">예비가격파일존재여부(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttCd</td>
<td style="text-align: left;">공고기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1230137</td>
<td style="text-align: left;">공고를 하는 기관의 코드로 행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드가 행자부코드가 없는 경우 조달청에서 부여한 수요기관 코드가 표기됨</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttNm</td>
<td style="text-align: left;">공고기관명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">조달청 대구지방조달청</td>
<td style="text-align: left;">수요기관의 의뢰를 받아 공고하는 기관의 명</td>
</tr>
<tr>
<td style="text-align: left;">dminsttCd</td>
<td style="text-align: left;">수요기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">Z021943</td>
<td style="text-align: left;">실제 수요기관의 코드로 행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드가 행자부코드가 없는 경우 조달청에서 부여한 수요기관 코드가 표기됨</td>
</tr>
<tr>
<td style="text-align: left;">dminsttNm</td>
<td style="text-align: left;">수요기관명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">대구경북첨단의료산업진흥재단</td>
<td style="text-align: left;">중앙조달인 경우 조달사업에 관한 법률 제2조(정의)에 따라 수요물자의 구매 공급 또는 시설공사 계약의 체결을 조달청장에게 요청할 수 있도록 조달청장이 인정하여 등록한 기관 또는 자체전자조달시스템을 이용하는 기관인 경우 계약을 의뢰한 기관의 명으로 공고기관과 수요기관이 동일할 수 있음</td>
</tr>
<tr>
<td style="text-align: left;">opengRsltNtcCntnts</td>
<td style="text-align: left;">개찰결과공지내용</td>
<td style="text-align: left;">4000</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">공지내용참고</td>
<td style="text-align: left;">입찰공고번호, 입찰공고차수, 입찰분류번호, 재입찰번호 에 해당하는 공지사항 내용</td>
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
<td>REST(URI)</td>
</tr>
<tr>
<td style="text-align: left;">http://apis.data.go.kr/1230000/as/ScsbidInfoService/getOpengResultListInfoThng?inqryDiv=4&amp; bidNtceNo=R25BK00840922&amp;pageNo=1&amp;numOfRows=10&amp;ServiceKey=인증키</td>
</tr>
<tr>
<td>응답 메시지</td>
</tr>
<tr>
<td><p>&lt;response&gt;</p>
<p>&lt;header&gt;</p>
<p>&lt;resultCode&gt;00&lt;/resultCode&gt;</p>
<p>&lt;resultMsg&gt;정상&lt;/resultMsg&gt;</p>
<p>&lt;/header&gt;</p>
<p>&lt;body&gt;</p>
<p>&lt;items&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00840922&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;1&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;bidNtceNm&gt;근접전자기장 내성 시험 시스템 구축&lt;/bidNtceNm&gt;</p>
<p>&lt;opengDt&gt;2025-06-17 11:00:00&lt;/opengDt&gt;</p>
<p>&lt;prtcptCnum&gt;2&lt;/prtcptCnum&gt;</p>
<p>&lt;opengCorpInfo&gt;이엠테스트코리아 주식회사^1428139282^김종인^178750000^97.992&lt;/opengCorpInfo&gt;</p>
<p>&lt;progrsDivCdNm&gt;개찰완료&lt;/progrsDivCdNm&gt;</p>
<p>&lt;inptDt&gt;2025-07-14 09:57:49&lt;/inptDt&gt;</p>
<p>&lt;rsrvtnPrceFileExistnceYn&gt;Y&lt;/rsrvtnPrceFileExistnceYn&gt;</p>
<p>&lt;ntceInsttCd&gt;1230137&lt;/ntceInsttCd&gt;</p>
<p>&lt;ntceInsttNm&gt;조달청 대구지방조달청&lt;/ntceInsttNm&gt;</p>
<p>&lt;dminsttCd&gt;Z021943&lt;/dminsttCd&gt;</p>
<p>&lt;dminsttNm&gt;대구경북첨단의료산업진흥재단&lt;/dminsttNm&gt;</p>
<p>&lt;opengRsltNtcCntnts&gt;&lt;/opengRsltNtcCntnts&gt;</p>
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

#### \[개찰결과 공사 목록 조회\] 오퍼레이션 명세

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
<td colspan="2">개찰결과 공사 목록 조회</td>
</tr>
<tr>
<td>오퍼레이션 유형</td>
<td>조회(목록)</td>
<td>오퍼레이션명(영문)</td>
<td colspan="2"><strong>getOpengResultListInfoCnstwk</strong></td>
</tr>
<tr>
<td>오퍼레이션 설명</td>
<td colspan="4">유찰, 개찰완료, 재입찰건에 대한 개찰결과를 제공하며 검색조건을 입력일시, 공고일시, 개찰일시, 입찰공고번호로하여 공사에 대한 나라장터 개찰결과 목록(입찰공고번호, 입찰공고명, 개찰일시, 참가업체수, 개찰업체정보, 진행구분코드명, 입력일시, 예비가격파일존재여부, 공고기관명, 수요기관명)을 조회</td>
</tr>
<tr>
<td>Call Back URL</td>
<td colspan="4" style="text-align: left;">N/A</td>
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
<col style="width: 11%" />
<col style="width: 12%" />
<col style="width: 22%" />
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
<td>4</td>
<td>0</td>
<td>10</td>
<td>한 페이지 결과 수</td>
</tr>
<tr>
<td>pageNo</td>
<td>페이지 번호</td>
<td>4</td>
<td>0</td>
<td>1</td>
<td>페이지 번호</td>
</tr>
<tr>
<td style="text-align: left;">ServiceKey</td>
<td style="text-align: left;">서비스키</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">공공데이터포털에서 받은 인증키</td>
<td style="text-align: left;">공공데이터포털에서 받은 인증키</td>
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
<td>조회구분</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">검색하고자하는 조회구분<br />
1.입력일시, 2.공고일시,3.개찰일시,4.입찰공고번호</td>
</tr>
<tr>
<td>inqryBgnDt</td>
<td>조회시작일시</td>
<td>12</td>
<td style="text-align: left;">0</td>
<td>202507010000</td>
<td>검색하고자하는 시작일시<br />
'YYYYMMDDHHMM'<br />
조회구분 1,2,3일 경우 필수</td>
</tr>
<tr>
<td>inqryEndDt</td>
<td>조회종료일시</td>
<td>12</td>
<td style="text-align: left;">0</td>
<td>202507012359</td>
<td>검색하고자하는 종료일시<br />
'YYYYMMDDHHMM'<br />
조회구분 1,2,3일 경우 필수</td>
</tr>
<tr>
<td>bidNtceNo</td>
<td>입찰공고번호</td>
<td>11</td>
<td style="text-align: left;">0</td>
<td>R25BK00926014</td>
<td style="text-align: left;">검색하고자하는 입찰공고번호<br />
조회구분 4인 경우 필수</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 응답 메시지 명세

<table>
<colgroup>
<col style="width: 23%" />
<col style="width: 17%" />
<col style="width: 9%" />
<col style="width: 8%" />
<col style="width: 22%" />
<col style="width: 17%" />
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
<td>numOfRows</td>
<td>한 페이지 결과 수</td>
<td>4</td>
<td>1</td>
<td>10</td>
<td>한 페이지 결과 수</td>
</tr>
<tr>
<td>pageNo</td>
<td>페이지 번호</td>
<td>4</td>
<td>1</td>
<td>1</td>
<td>페이지 번호</td>
</tr>
<tr>
<td>totalCount</td>
<td>데이터 총 개수</td>
<td>4</td>
<td>1</td>
<td>17</td>
<td>데이터 총 개수</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNo</td>
<td>입찰공고번호</td>
<td>11</td>
<td style="text-align: left;">1</td>
<td>R25BK00926014</td>
<td>입찰공고 관리번호이며 조달청나라장터 공고건의 형식은 년도(4)+월(2)+순번(5)이며 자체전자조달시스템 보유기관은 각 기관별 형식 별도 사용<br />
*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성<br />
- 단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</td>
</tr>
<tr>
<td>bidNtceOrd</td>
<td>입찰공고차수</td>
<td>3</td>
<td style="text-align: left;">1</td>
<td>000</td>
<td>입찰공고차수는 해당 입찰공고에 대한 재공고 및 재입찰 등이 발생되었을 경우 증가되는 수</td>
</tr>
<tr>
<td>bidClsfcNo</td>
<td>입찰분류번호</td>
<td>5</td>
<td style="text-align: left;">1</td>
<td>0</td>
<td>동일한 입찰공고번호에 대한 집행일련번호</td>
</tr>
<tr>
<td>rbidNo</td>
<td>재입찰번호</td>
<td>3</td>
<td style="text-align: left;">1</td>
<td>000</td>
<td>재입찰번호</td>
</tr>
<tr>
<td>bidNtceNm</td>
<td>입찰공고명</td>
<td>1000</td>
<td style="text-align: left;">1</td>
<td>낭주중학교 인조 잔디 조성 및 담장 교체 공사 입찰 공고[긴급]</td>
<td>공사명 또는 사업명이라고도 하며 입찰공고 내용을 요약한 이름</td>
</tr>
<tr>
<td>opengDt</td>
<td>개찰일시</td>
<td>19</td>
<td style="text-align: left;">1</td>
<td>2025-07-01 11:00:00</td>
<td>조달업체가 제출한 입찰서를 개찰하는 일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td>prtcptCnum</td>
<td>참가업체수</td>
<td>6</td>
<td style="text-align: left;">0</td>
<td>374</td>
<td>참가업체수</td>
</tr>
<tr>
<td>opengCorpInfo</td>
<td>개찰업체정보</td>
<td>500</td>
<td style="text-align: left;">1</td>
<td>유한회사 진무건설^4028138623^이세윤^462119000^88.393</td>
<td><p>개찰업체정보<br />
다수 낙찰자의 경우 ”낙찰예정자 다수”와 개찰순위 1위의 투찰금액과 투찰율<br />
을 보여줌</p>
<p>단일 낙찰자 의 경우 업체명과 사업자번호, 대표자명, 투찰금액, 투찰율을 보여줌</p>
<p>단, 협상에 의한 계약일 경우는 투찰금액,투찰율 안나옴</p></td>
</tr>
<tr>
<td>progrsDivCdNm</td>
<td>진행구분코드명</td>
<td>4</td>
<td style="text-align: left;">1</td>
<td>개찰완료</td>
<td><p>진행구분이</p>
<p>유찰, 개찰완료, 재입찰로 구분 됨</p></td>
</tr>
<tr>
<td>inptDt</td>
<td>입력일시</td>
<td>19</td>
<td style="text-align: left;">0</td>
<td>2025-07-01 11:08:48</td>
<td>입력일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td>rsrvtnPrceFileExistnceYn</td>
<td>예비가격파일존재여부</td>
<td>1</td>
<td style="text-align: left;">1</td>
<td>Y</td>
<td>예비가격파일존재여부(Y/N)</td>
</tr>
<tr>
<td>ntceInsttCd</td>
<td>공고기관코드</td>
<td>7</td>
<td style="text-align: left;">1</td>
<td>8462058</td>
<td>공고를 하는 기관의 코드로 행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드가 행자부코드가 없는 경우 조달청에서 부여한 수요기관 코드가 표기됨</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttNm</td>
<td>공고기관명</td>
<td>200</td>
<td style="text-align: left;">0</td>
<td>전북특별자치도교육청 전북특별자치도부안교육지원청 낭주중학교</td>
<td>수요기관의 의뢰를 받아 공고하는 기관의 명</td>
</tr>
<tr>
<td style="text-align: left;">dminsttCd</td>
<td>수요기관코드</td>
<td>7</td>
<td style="text-align: left;">0</td>
<td>8462058</td>
<td>실제 수요기관의 코드로 행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드가 행자부코드가 없는 경우 조달청에서 부여한 수요기관 코드가 표기됨</td>
</tr>
<tr>
<td style="text-align: left;">dminsttNm</td>
<td>수요기관명</td>
<td>200</td>
<td style="text-align: left;">0</td>
<td>전북특별자치도교육청 전북특별자치도부안교육지원청 낭주중학교</td>
<td>중앙조달인 경우 조달사업에 관한 법률 제2조(정의)에 따라 수요물자의 구매 공급 또는 시설공사 계약의 체결을 조달청장에게 요청할 수 있도록 조달청장이 인정하여 등록한 기관 또는 자체전자조달시스템을 이용하는 기관인 경우 계약을 의뢰한 기관의 명으로 공고기관과 수요기관이 동일할 수 있음</td>
</tr>
<tr>
<td style="text-align: left;">opengRsltNtcCntnts</td>
<td style="text-align: left;">개찰결과공지내용</td>
<td style="text-align: left;">4000</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">개찰완료되었습니다.</td>
<td style="text-align: left;">입찰공고번호, 입찰공고차수, 입찰분류번호, 재입찰번호에 해당하는 공지사항 내용</td>
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
<td>REST(URI)</td>
</tr>
<tr>
<td style="text-align: left;">http://apis.data.go.kr/1230000/as/ScsbidInfoService/getOpengResultListInfoCnstwk?inqryDiv=4&amp; bidNtceNo=R25BK00926014&amp;pageNo=1&amp;numOfRows=10&amp;ServiceKey=인증키</td>
</tr>
<tr>
<td>응답 메시지</td>
</tr>
<tr>
<td><p>&lt;response&gt;</p>
<p>&lt;header&gt;</p>
<p>&lt;resultCode&gt;00&lt;/resultCode&gt;</p>
<p>&lt;resultMsg&gt;정상&lt;/resultMsg&gt;</p>
<p>&lt;/header&gt;</p>
<p>&lt;body&gt;</p>
<p>&lt;items&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00926014&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;0&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;bidNtceNm&gt;낭주중학교 인조 잔디 조성 및 담장 교체 공사 입찰 공고[긴급]&lt;/bidNtceNm&gt;</p>
<p>&lt;opengDt&gt;2025-07-01 11:00:00&lt;/opengDt&gt;</p>
<p>&lt;prtcptCnum&gt;374&lt;/prtcptCnum&gt;</p>
<p>&lt;opengCorpInfo&gt;유한회사 진무건설^4028138623^이세윤^462119000^88.393&lt;/opengCorpInfo&gt;</p>
<p>&lt;progrsDivCdNm&gt;개찰완료&lt;/progrsDivCdNm&gt;</p>
<p>&lt;inptDt&gt;2025-07-01 11:08:48&lt;/inptDt&gt;</p>
<p>&lt;rsrvtnPrceFileExistnceYn&gt;Y&lt;/rsrvtnPrceFileExistnceYn&gt;</p>
<p>&lt;ntceInsttCd&gt;8462058&lt;/ntceInsttCd&gt;</p>
<p>&lt;ntceInsttNm&gt;전북특별자치도교육청 전북특별자치도부안교육지원청 낭주중학교&lt;/ntceInsttNm&gt;</p>
<p>&lt;dminsttCd&gt;8462058&lt;/dminsttCd&gt;</p>
<p>&lt;dminsttNm&gt;전북특별자치도교육청 전북특별자치도부안교육지원청 낭주중학교&lt;/dminsttNm&gt;</p>
<p>&lt;opengRsltNtcCntnts&gt;&lt;/opengRsltNtcCntnts&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;/items&gt;</p>
<p>&lt;numOfRows&gt;999&lt;/numOfRows&gt;</p>
<p>&lt;pageNo&gt;1&lt;/pageNo&gt;</p>
<p>&lt;totalCount&gt;1&lt;/totalCount&gt;</p>
<p>&lt;/body&gt;</p>
<p>&lt;/response</p></td>
</tr>
</tbody>
</table>

#### \[개찰결과 용역 목록 조회\] 오퍼레이션 명세

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
<td colspan="2">개찰결과 용역 목록 조회</td>
</tr>
<tr>
<td>오퍼레이션 유형</td>
<td>조회(목록)</td>
<td>오퍼레이션명(영문)</td>
<td colspan="2"><strong>getOpengResultListInfoServc</strong></td>
</tr>
<tr>
<td>오퍼레이션 설명</td>
<td colspan="4">유찰, 개찰완료, 재입찰건에 대한 개찰결과를 제공하며 검색조건을 입력일시, 공고일시, 개찰일시, 입찰공고번호로하여 용역에 대한 나라장터 개찰결과 목록(입찰공고번호, 입찰공고명, 개찰일시, 참가업체수, 개찰업체정보, 진행구분코드명, 입력일시, 예비가격파일존재여부, 공고기관명, 수요기관명)을 조회</td>
</tr>
<tr>
<td>Call Back URL</td>
<td colspan="4" style="text-align: left;">N/A</td>
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
<col style="width: 11%" />
<col style="width: 12%" />
<col style="width: 22%" />
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
<td>4</td>
<td>0</td>
<td>10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td>pageNo</td>
<td>페이지 번호</td>
<td>4</td>
<td>0</td>
<td>1</td>
<td style="text-align: left;">페이지 번호</td>
</tr>
<tr>
<td style="text-align: left;">ServiceKey</td>
<td style="text-align: left;">서비스키</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">공공데이터포털에서 받은 인증키</td>
<td style="text-align: left;">공공데이터포털에서 받은 인증키</td>
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
<td>조회구분</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">검색하고자하는 조회구분<br />
1.입력일시, 2.공고일시,3.개찰일시,4.입찰공고번호</td>
</tr>
<tr>
<td>inqryBgnDt</td>
<td>조회시작일시</td>
<td>12</td>
<td style="text-align: left;">0</td>
<td>20250701000</td>
<td>검색하고자하는 시작일시<br />
'YYYYMMDDHHMM'<br />
조회구분 1,2,3일 경우 필수</td>
</tr>
<tr>
<td>inqryEndDt</td>
<td>조회종료일시</td>
<td>12</td>
<td style="text-align: left;">0</td>
<td>202507012359</td>
<td>검색하고자하는 종료일시<br />
'YYYYMMDDHHMM'<br />
조회구분 1,2,3일 경우 필수</td>
</tr>
<tr>
<td>bidNtceNo</td>
<td>입찰공고번호</td>
<td>11</td>
<td style="text-align: left;">0</td>
<td>R25BK00882586</td>
<td style="text-align: left;">검색하고자하는 입찰공고번호<br />
조회구분 4인 경우 필수</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 응답 메시지 명세

<table style="width:100%;">
<colgroup>
<col style="width: 23%" />
<col style="width: 18%" />
<col style="width: 9%" />
<col style="width: 9%" />
<col style="width: 19%" />
<col style="width: 18%" />
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
<td>numOfRows</td>
<td>한 페이지 결과 수</td>
<td>4</td>
<td>1</td>
<td>10</td>
<td>한 페이지 결과 수</td>
</tr>
<tr>
<td>pageNo</td>
<td>페이지 번호</td>
<td>4</td>
<td>1</td>
<td>1</td>
<td>페이지 번호</td>
</tr>
<tr>
<td>totalCount</td>
<td>데이터 총 개수</td>
<td>4</td>
<td>1</td>
<td>17</td>
<td>데이터 총 개수</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNo</td>
<td>입찰공고번호</td>
<td>11</td>
<td style="text-align: left;">1</td>
<td>R25BK00882586</td>
<td style="text-align: left;">입찰공고 관리번호이며 조달청나라장터 공고건의 형식은 년도(4)+월(2)+순번(5)이며 자체전자조달시스템 보유기관은 각 기관별 형식 별도 사용<br />
*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성<br />
- 단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</td>
</tr>
<tr>
<td>bidNtceOrd</td>
<td>입찰공고차수</td>
<td>3</td>
<td style="text-align: left;">1</td>
<td>000</td>
<td>입찰공고차수는 해당 입찰공고에 대한 재공고 및 재입찰 등이 발생되었을 경우 증가되는 수</td>
</tr>
<tr>
<td>bidClsfcNo</td>
<td>입찰분류번호</td>
<td>5</td>
<td style="text-align: left;">1</td>
<td>1</td>
<td>동일한 입찰공고번호에 대한 집행일련번호</td>
</tr>
<tr>
<td>rbidNo</td>
<td>재입찰번호</td>
<td>3</td>
<td style="text-align: left;">1</td>
<td>000</td>
<td>재입찰번호</td>
</tr>
<tr>
<td>bidNtceNm</td>
<td>입찰공고명</td>
<td>1000</td>
<td style="text-align: left;">1</td>
<td>한국생명공학연구원 지역조직 중기 발전전략 수립</td>
<td>공사명 또는 사업명이라고도 하며 입찰공고 내용을 요약한 이름</td>
</tr>
<tr>
<td>opengDt</td>
<td>개찰일시</td>
<td>19</td>
<td style="text-align: left;">1</td>
<td>2025-06-13 11:00:00</td>
<td>조달업체가 제출한 입찰서를 개찰하는 일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td>prtcptCnum</td>
<td>참가업체수</td>
<td>6</td>
<td style="text-align: left;">0</td>
<td>2</td>
<td>참가업체수</td>
</tr>
<tr>
<td>opengCorpInfo</td>
<td>개찰업체정보</td>
<td>500</td>
<td style="text-align: left;">1</td>
<td>(주식회사 과학기술전략연구소^5088702880^유경만^72000000^0</td>
<td><p>개찰업체정보<br />
다수 낙찰자의 경우 ”낙찰예정자 다수”와 개찰순위 1위의 투찰금액과 투찰율을 보여줌</p>
<p>단일 낙찰자 의 경우 업체명과 사업자번호, 대표자명, 투찰금액, 투찰율을 보여줌</p>
<p>단, 협상에 의한 계약일 경우는 투찰금액, 투찰율 안나옴</p></td>
</tr>
<tr>
<td>progrsDivCdNm</td>
<td>진행구분코드명</td>
<td>4</td>
<td style="text-align: left;">1</td>
<td>개찰완료</td>
<td><p>진행구분이</p>
<p>유찰, 개찰완료, 재입찰로 구분 됨</p></td>
</tr>
<tr>
<td>inptDt</td>
<td>입력일시</td>
<td>19</td>
<td style="text-align: left;">0</td>
<td>2025-07-01 16:52:39</td>
<td>입력일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td>rsrvtnPrceFileExistnceYn</td>
<td>예비가격파일존재여부</td>
<td>1</td>
<td style="text-align: left;">1</td>
<td>N</td>
<td>예비가격파일존재여부(Y/N)</td>
</tr>
<tr>
<td>ntceInsttCd</td>
<td>공고기관코드</td>
<td>7</td>
<td style="text-align: left;">1</td>
<td>Z004836</td>
<td>공고를 하는 기관의 코드로 행정자치부에서 부여한 기관코드임</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttNm</td>
<td>공고기관명</td>
<td>200</td>
<td style="text-align: left;">0</td>
<td>한국생명공학연구원</td>
<td>수요기관의 의뢰를 받아 공고하는 기관의 명</td>
</tr>
<tr>
<td style="text-align: left;">dminsttCd</td>
<td>수요기관코드</td>
<td>7</td>
<td style="text-align: left;">0</td>
<td>Z004836</td>
<td>실제 수요기관의 코드로 행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드가 행자부코드가 없는 경우 조달청에서 부여한 수요기관 코드가 표기됨</td>
</tr>
<tr>
<td style="text-align: left;">dminsttNm</td>
<td>수요기관명</td>
<td>200</td>
<td style="text-align: left;">0</td>
<td>한국생명공학연구원</td>
<td>중앙조달인 경우 조달사업에 관한 법률 제2조(정의)에 따라 수요물자의 구매 공급 또는 시설공사 계약의 체결을 조달청장에게 요청할 수 있도록 조달청장이 인정하여 등록한 기관 또는 자체전자조달시스템을 이용하는 기관인 경우 계약을 의뢰한 기관의 명으로 공고기관과 수요기관이 동일할 수 있음</td>
</tr>
<tr>
<td style="text-align: left;">opengRsltNtcCntnts</td>
<td style="text-align: left;">개찰결과공지내용</td>
<td style="text-align: left;">4000</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">개찰결과공지내용</td>
<td style="text-align: left;">입찰공고번호, 입찰공고차수, 입찰분류번호, 재입찰번호에 해당하는 공지사항 내용</td>
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
<td>REST(URI)</td>
</tr>
<tr>
<td style="text-align: left;">http://apis.data.go.kr/1230000/as/ScsbidInfoService/getOpengResultListInfoServc?inqryDiv=4&amp; bidNtceNo=R25BK00882586&amp;pageNo=1&amp;numOfRows=10&amp;ServiceKey=인증키</td>
</tr>
<tr>
<td>응답 메시지</td>
</tr>
<tr>
<td><p>&lt;response&gt;</p>
<p>&lt;header&gt;</p>
<p>&lt;resultCode&gt;00&lt;/resultCode&gt;</p>
<p>&lt;resultMsg&gt;정상&lt;/resultMsg&gt;</p>
<p>&lt;/header&gt;</p>
<p>&lt;body&gt;</p>
<p>&lt;items&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00882586&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;0&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;bidNtceNm&gt;한국생명공학연구원 지역조직 중기 발전전략 수립&lt;/bidNtceNm&gt;</p>
<p>&lt;opengDt&gt;2025-06-13 11:00:00&lt;/opengDt&gt;</p>
<p>&lt;prtcptCnum&gt;2&lt;/prtcptCnum&gt;</p>
<p>&lt;opengCorpInfo&gt;주식회사 과학기술전략연구소^5088702880^유경만^72000000^0&lt;/opengCorpInfo&gt;</p>
<p>&lt;progrsDivCdNm&gt;개찰완료&lt;/progrsDivCdNm&gt;</p>
<p>&lt;inptDt&gt;2025-07-01 16:52:39&lt;/inptDt&gt;</p>
<p>&lt;rsrvtnPrceFileExistnceYn&gt;N&lt;/rsrvtnPrceFileExistnceYn&gt;</p>
<p>&lt;ntceInsttCd&gt;Z004836&lt;/ntceInsttCd&gt;</p>
<p>&lt;ntceInsttNm&gt;한국생명공학연구원&lt;/ntceInsttNm&gt;</p>
<p>&lt;dminsttCd&gt;Z004836&lt;/dminsttCd&gt;</p>
<p>&lt;dminsttNm&gt;한국생명공학연구원&lt;/dminsttNm&gt;</p>
<p>&lt;opengRsltNtcCntnts&gt;&lt;/opengRsltNtcCntnts&gt;</p>
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

#### \[개찰결과 외자 목록 조회\] 오퍼레이션 명세

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
<td colspan="2">개찰결과 외자 목록 조회</td>
</tr>
<tr>
<td>오퍼레이션 유형</td>
<td>조회(목록)</td>
<td>오퍼레이션명(영문)</td>
<td colspan="2"><strong>getOpengResultListInfoFrgcpt</strong></td>
</tr>
<tr>
<td>오퍼레이션 설명</td>
<td colspan="4">유찰, 개찰완료, 재입찰건에 대한 개찰결과를 제공하며 검색조건을 입력일시, 공고일시, 개찰일시, 입찰공고번호로하여 외자에 대한 나라장터 개찰결과 목록(입찰공고번호, 입찰공고명, 개찰일시, 참가업체수, 개찰업체정보, 진행구분코드명, 입력일시, 예비가격파일존재여부, 공고기관명, 수요기관명)을 조회</td>
</tr>
<tr>
<td>Call Back URL</td>
<td colspan="4" style="text-align: left;">N/A</td>
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
<col style="width: 11%" />
<col style="width: 13%" />
<col style="width: 22%" />
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
<td>4</td>
<td>0</td>
<td>10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td>pageNo</td>
<td>페이지 번호</td>
<td>4</td>
<td>0</td>
<td>1</td>
<td style="text-align: left;">페이지 번호</td>
</tr>
<tr>
<td style="text-align: left;">ServiceKey</td>
<td style="text-align: left;">서비스키</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">공공데이터포털에서 받은 인증키</td>
<td style="text-align: left;">공공데이터포털에서 받은 인증키</td>
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
<td>조회구분</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">검색하고자하는 조회구분<br />
1.입력일시, 2.공고일시,3.개찰일시,4.입찰공고번호</td>
</tr>
<tr>
<td>inqryBgnDt</td>
<td>조회시작일시</td>
<td>12</td>
<td style="text-align: left;">0</td>
<td>202507010000</td>
<td>검색하고자하는 시작일시<br />
'YYYYMMDDHHMM'<br />
조회구분 1,2,3일 경우 필수</td>
</tr>
<tr>
<td>inqryEndDt</td>
<td>조회종료일시</td>
<td>12</td>
<td style="text-align: left;">0</td>
<td>202507012359</td>
<td>검색하고자하는 종료일시<br />
'YYYYMMDDHHMM'<br />
조회구분 1,2,3일 경우 필수</td>
</tr>
<tr>
<td>bidNtceNo</td>
<td>입찰공고번호</td>
<td>11</td>
<td style="text-align: left;">0</td>
<td>R25BK00916730</td>
<td style="text-align: left;">검색하고자하는 입찰공고번호<br />
조회구분 4인 경우 필수</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 응답 메시지 명세

<table style="width:100%;">
<colgroup>
<col style="width: 18%" />
<col style="width: 18%" />
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 14%" />
<col style="width: 25%" />
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
<td>numOfRows</td>
<td>한 페이지 결과 수</td>
<td>4</td>
<td>1</td>
<td>10</td>
<td>한 페이지 결과 수</td>
</tr>
<tr>
<td>pageNo</td>
<td>페이지 번호</td>
<td>4</td>
<td>1</td>
<td>1</td>
<td>페이지 번호</td>
</tr>
<tr>
<td>totalCount</td>
<td>데이터 총 개수</td>
<td>4</td>
<td>1</td>
<td>17</td>
<td>데이터 총 개수</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNo</td>
<td>입찰공고번호</td>
<td>11</td>
<td style="text-align: left;">1</td>
<td>R25BK00916730</td>
<td style="text-align: left;">입찰공고 관리번호이며 조달청나라장터 공고건의 형식은 년도(4)+월(2)+순번(5)이며 자체전자조달시스템 보유기관은 각 기관별 형식 별도 사용<br />
*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성<br />
- 단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</td>
</tr>
<tr>
<td>bidNtceOrd</td>
<td>입찰공고차수</td>
<td>3</td>
<td style="text-align: left;">1</td>
<td>000</td>
<td>입찰공고차수는 해당 입찰공고에 대한 재공고 및 재입찰 등이 발생되었을 경우 증가되는 수</td>
</tr>
<tr>
<td>bidClsfcNo</td>
<td>입찰분류번호</td>
<td>5</td>
<td style="text-align: left;">1</td>
<td>1</td>
<td>동일한 입찰공고번호에 대한 집행일련번호</td>
</tr>
<tr>
<td>rbidNo</td>
<td>재입찰번호</td>
<td>3</td>
<td style="text-align: left;">1</td>
<td>000</td>
<td>재입찰번호</td>
</tr>
<tr>
<td>bidNtceNm</td>
<td>입찰공고명</td>
<td>1000</td>
<td style="text-align: left;">1</td>
<td>외자조달요청(북부지원 유도결합플라즈마 질량분석기)</td>
<td>공사명 또는 사업명이라고도 하며 입찰공고 내용을 요약한 이름</td>
</tr>
<tr>
<td>opengDt</td>
<td>개찰일시</td>
<td>19</td>
<td style="text-align: left;">1</td>
<td>2025-07-01 13:00:00</td>
<td>조달업체가 제출한 입찰서를 개찰하는 일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td>prtcptCnum</td>
<td>참가업체수</td>
<td>6</td>
<td style="text-align: left;">0</td>
<td>1</td>
<td>참가업체수</td>
</tr>
<tr>
<td>opengCorpInfo</td>
<td>개찰업체정보</td>
<td>500</td>
<td style="text-align: left;">1</td>
<td>써모피셔사이언티픽코리아 주식회사^1178146910^석수진^173500^0</td>
<td><p>개찰업체정보<br />
다수 낙찰자의 경우 ”낙찰예정자 다수”와 개찰순위 1위의 투찰금액과 투찰율을 보여줌</p>
<p>단일 낙찰자 의 경우 업체명과 사업자번호, 대표자명, 투찰금액, 투찰율을 보여줌</p>
<p>단, 협상에 의한 계약일 경우는 투찰금액,투찰율 안나옴</p></td>
</tr>
<tr>
<td>progrsDivCdNm</td>
<td>진행구분코드명</td>
<td>4</td>
<td style="text-align: left;">1</td>
<td>개찰완료</td>
<td><p>진행구분이</p>
<p>유찰, 개찰완료, 재입찰로 구분 됨</p></td>
</tr>
<tr>
<td>inptDt</td>
<td>입력일시</td>
<td>19</td>
<td style="text-align: left;">0</td>
<td>2025-07-01 13:10:54</td>
<td>입력일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td>rsrvtnPrceFileExistnceYn</td>
<td>예비가격파일존재여부</td>
<td>1</td>
<td style="text-align: left;">1</td>
<td>N</td>
<td>예비가격파일존재여부(Y/N)</td>
</tr>
<tr>
<td>ntceInsttCd</td>
<td>공고기관코드</td>
<td>7</td>
<td style="text-align: left;">1</td>
<td>1230000</td>
<td>공고를 하는 기관의 코드로 행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드가 행자부코드가 없는 경우 조달청에서 부여한 수요기관 코드가 표기됨</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttNm</td>
<td>공고기관명</td>
<td>200</td>
<td style="text-align: left;">0</td>
<td>조달청</td>
<td>수요기관의 의뢰를 받아 공고하는 기관의 명</td>
</tr>
<tr>
<td style="text-align: left;">dminsttCd</td>
<td>수요기관코드</td>
<td>7</td>
<td style="text-align: left;">0</td>
<td>6440071</td>
<td>실제 수요기관의 코드로 행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드가 행자부코드가 없는 경우 조달청에서 부여한 수요기관 코드가 표기됨</td>
</tr>
<tr>
<td style="text-align: left;">dminsttNm</td>
<td>수요기관명</td>
<td>200</td>
<td style="text-align: left;">0</td>
<td>충청남도 보건환경연구원</td>
<td>중앙조달인 경우 조달사업에 관한 법률 제2조(정의)에 따라 수요물자의 구매 공급 또는 시설공사 계약의 체결을 조달청장에게 요청할 수 있도록 조달청장이 인정하여 등록한 기관 또는 자체전자조달시스템을 이용하는 기관인 경우 계약을 의뢰한 기관의 명으로 공고기관과 수요기관이 동일할 수 있음</td>
</tr>
<tr>
<td style="text-align: left;">opengRsltNtcCntnts</td>
<td style="text-align: left;">개찰결과공지내용</td>
<td style="text-align: left;">4000</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">개찰결과공지내용</td>
<td style="text-align: left;">입찰공고번호, 입찰공고차수, 입찰분류번호, 재입찰번호에 해당하는 공지사항 내용</td>
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
<td>REST(URI)</td>
</tr>
<tr>
<td style="text-align: left;">http://apis.data.go.kr/1230000/as/ScsbidInfoService/getOpengResultListInfoFrgcpt?inqryDiv=4&amp; bidNtceNo=R25BK00916730&amp;pageNo=1&amp;numOfRows=10&amp;ServiceKey=인증키</td>
</tr>
<tr>
<td>응답 메시지</td>
</tr>
<tr>
<td><p>&lt;response&gt;</p>
<p>&lt;header&gt;</p>
<p>&lt;resultCode&gt;00&lt;/resultCode&gt;</p>
<p>&lt;resultMsg&gt;정상&lt;/resultMsg&gt;</p>
<p>&lt;/header&gt;</p>
<p>&lt;body&gt;</p>
<p>&lt;items&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00916730&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;1&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;bidNtceNm&gt;외자조달요청(북부지원 유도결합플라즈마 질량분석기)&lt;/bidNtceNm&gt;</p>
<p>&lt;opengDt&gt;2025-07-01 13:00:00&lt;/opengDt&gt;</p>
<p>&lt;prtcptCnum&gt;1&lt;/prtcptCnum&gt;</p>
<p>&lt;opengCorpInfo&gt;써모피셔사이언티픽코리아 주식회사^1178146910^석수진^173500^0&lt;/opengCorpInfo&gt;</p>
<p>&lt;progrsDivCdNm&gt;개찰완료&lt;/progrsDivCdNm&gt;</p>
<p>&lt;inptDt&gt;2025-07-01 13:10:54&lt;/inptDt&gt;</p>
<p>&lt;rsrvtnPrceFileExistnceYn&gt;N&lt;/rsrvtnPrceFileExistnceYn&gt;</p>
<p>&lt;ntceInsttCd&gt;1230000&lt;/ntceInsttCd&gt;</p>
<p>&lt;ntceInsttNm&gt;조달청&lt;/ntceInsttNm&gt;</p>
<p>&lt;dminsttCd&gt;6440071&lt;/dminsttCd&gt;</p>
<p>&lt;dminsttNm&gt;충청남도 보건환경연구원&lt;/dminsttNm&gt;</p>
<p>&lt;opengRsltNtcCntnts&gt;&lt;/opengRsltNtcCntnts&gt;</p>
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

#### \[개찰결과 물품 예비가격상세 목록 조회\] 오퍼레이션 명세

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
<td>9</td>
<td>오퍼레이션명(국문)</td>
<td colspan="2">개찰결과 물품 예비가격상세 목록 조회</td>
</tr>
<tr>
<td>오퍼레이션 유형</td>
<td>조회(목록)</td>
<td>오퍼레이션명(영문)</td>
<td colspan="2"><strong>getOpengResultListInfoThngPreparPcDetail</strong></td>
</tr>
<tr>
<td>오퍼레이션 설명</td>
<td colspan="4">검색조건을 입력일시, 입찰공고번호로 물품에 대한 나라장터 개찰결과 예비가격상세 목록(입찰공고번호, 입찰공고명, 예정가격, 기초금액, 총예가건수, 복수예가순번, 기초예정가격, 추첨여부, 추첨횟수, 실개찰일시, 기초금액기준상위건수, 복수예비가격작성일시, 입력일시)을 조회</td>
</tr>
<tr>
<td>Call Back URL</td>
<td colspan="4" style="text-align: left;">N/A</td>
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
<col style="width: 11%" />
<col style="width: 12%" />
<col style="width: 22%" />
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
<td>4</td>
<td>0</td>
<td>10</td>
<td>한 페이지 결과 수</td>
</tr>
<tr>
<td>pageNo</td>
<td>페이지 번호</td>
<td>4</td>
<td>0</td>
<td>1</td>
<td>페이지 번호</td>
</tr>
<tr>
<td style="text-align: left;">ServiceKey</td>
<td style="text-align: left;">서비스키</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">공공데이터포털에서 받은 인증키</td>
<td style="text-align: left;">공공데이터포털에서 받은 인증키</td>
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
<td>조회구분</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">검색하고자하는 조회구분<br />
1.입력일시, 2.입찰공고번호</td>
</tr>
<tr>
<td>inqryBgnDt</td>
<td>조회시작일시</td>
<td>12</td>
<td style="text-align: left;">0</td>
<td>202507010000</td>
<td>검색하고자하는 시작일시<br />
'YYYYMMDDHHMM'<br />
조회구분이 1일 경우 필수</td>
</tr>
<tr>
<td>inqryEndDt</td>
<td>조회종료일시</td>
<td>12</td>
<td style="text-align: left;">0</td>
<td>202507012359</td>
<td>검색하고자하는 종료일시<br />
'YYYYMMDDHHMM'<br />
조회구분이 1일 경우 필수</td>
</tr>
<tr>
<td>bidNtceNo</td>
<td>입찰공고번호</td>
<td>11</td>
<td style="text-align: left;">0</td>
<td>R25BK00845027</td>
<td><p>검색하고자하는 입찰공고번호</p>
<p>조회구분이 2일 경우 필수</p></td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 응답 메시지 명세

<table style="width:100%;">
<colgroup>
<col style="width: 21%" />
<col style="width: 21%" />
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 13%" />
<col style="width: 20%" />
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
<td>numOfRows</td>
<td>한 페이지 결과 수</td>
<td>4</td>
<td>1</td>
<td>10</td>
<td>한 페이지 결과 수</td>
</tr>
<tr>
<td>pageNo</td>
<td>페이지 번호</td>
<td>4</td>
<td>1</td>
<td>1</td>
<td>페이지 번호</td>
</tr>
<tr>
<td>totalCount</td>
<td>데이터 총 개수</td>
<td>4</td>
<td>1</td>
<td>17</td>
<td>데이터 총 개수</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNo</td>
<td>입찰공고번호</td>
<td>11</td>
<td style="text-align: left;">1</td>
<td>R25BK00845027</td>
<td style="text-align: left;">입찰공고 관리번호이며 조달청나라장터 공고건의 형식은 년도(4)+월(2)+순번(5)이며 자체전자조달시스템 보유기관은 각 기관별 형식 별도 사용<br />
*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성<br />
- 단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</td>
</tr>
<tr>
<td>bidNtceOrd</td>
<td>입찰공고차수</td>
<td>3</td>
<td style="text-align: left;">1</td>
<td>000</td>
<td>입찰공고차수는 해당 입찰공고에 대한 재공고 및 재입찰 등이 발생되었을 경우 증가되는 수</td>
</tr>
<tr>
<td>bidClsfcNo</td>
<td>입찰분류번호</td>
<td>5</td>
<td style="text-align: left;">1</td>
<td>1</td>
<td>동일한 입찰공고번호에 대한 집행일련번호</td>
</tr>
<tr>
<td>rbidNo</td>
<td>재입찰번호</td>
<td>3</td>
<td style="text-align: left;">1</td>
<td>000</td>
<td>재입찰번호</td>
</tr>
<tr>
<td>bidNtceNm</td>
<td>입찰공고명</td>
<td>1000</td>
<td style="text-align: left;">1</td>
<td>CT 및 X-ray 구매</td>
<td>공사명 또는 사업명이라고도 하며 입찰공고 내용을 요약한 이름</td>
</tr>
<tr>
<td>plnprc</td>
<td>예정가격</td>
<td>21</td>
<td style="text-align: left;">0</td>
<td>270648500</td>
<td>예정가격은 계약담당공무원이 구매를 위한 경쟁입찰 또는 수의시담을 하기 전에 당해 계약 목적물의 특성 및 계약 여건 등을 고려하여 예산의 범위 내에서 경제적으로 구매가 가능하고 구매가격으로서 적정하다고 판단하여 정한 가격을 말하며 동 가격은 입찰 또는 시담에 의한 낙찰자 선정의 기준이고 계약체결에 대한 최고 상한 금액을 의미함. (원화,원)</td>
</tr>
<tr>
<td>bssamt</td>
<td>기초금액</td>
<td>21</td>
<td style="text-align: left;">0</td>
<td>270499000</td>
<td>예정가격 작성 과정에서 거래실례가격, 원가계산가격 등에 의하여 조사한 가격이나 설계가격에 대하여 계약담당공무원이 그 적정여부를 검토조정한 가격(원화,원)</td>
</tr>
<tr>
<td>totRsrvtnPrceNum</td>
<td>총예가건수</td>
<td>2</td>
<td style="text-align: left;">0</td>
<td>15</td>
<td>총예가건수</td>
</tr>
<tr>
<td>compnoRsrvtnPrceSno</td>
<td>복수예가순번</td>
<td>6</td>
<td style="text-align: left;">0</td>
<td>7</td>
<td>복수예가순번</td>
</tr>
<tr>
<td>bsisPlnprc</td>
<td>기초예정가격</td>
<td>21</td>
<td style="text-align: left;">0</td>
<td>265727400</td>
<td>기초예정가격(원화,원)</td>
</tr>
<tr>
<td>drwtYn</td>
<td>추첨여부</td>
<td>1</td>
<td style="text-align: left;">1</td>
<td>Y</td>
<td>추첨여부(Y/N)</td>
</tr>
<tr>
<td>drwtNum</td>
<td>추첨횟수</td>
<td>22</td>
<td style="text-align: left;">0</td>
<td>1</td>
<td>추첨횟수</td>
</tr>
<tr>
<td style="text-align: left;">bidwinrSlctnAplBssCntnts</td>
<td>최종낙찰자선정적용기준내용</td>
<td>200</td>
<td style="text-align: left;">0</td>
<td>조달청</td>
<td>낙찰자선정적용기준내용</td>
</tr>
<tr>
<td style="text-align: left;">rlOpengDt</td>
<td>실개찰일시</td>
<td>19</td>
<td style="text-align: left;">0</td>
<td>2025-07-01 11:07:08</td>
<td>실제 개찰일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">bssamtBssUpNum</td>
<td>기초금액기준상위건수</td>
<td>2</td>
<td style="text-align: left;">0</td>
<td>8</td>
<td>기초금액기준상위건수</td>
</tr>
<tr>
<td style="text-align: left;">compnoRsrvtnPrceMkngDt</td>
<td>복수예비가격작성일시</td>
<td>19</td>
<td style="text-align: left;">0</td>
<td>2015-11-05 16:28:28</td>
<td>복수예비가격작성시각”YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">inptDt</td>
<td>입력일시</td>
<td style="text-align: left;">19</td>
<td>1</td>
<td>2025-07-01 11:07:08</td>
<td style="text-align: left;">입력일시 "YYYY-MM-DD HH:MM:SS"</td>
</tr>
<tr>
<td style="text-align: left;">PrearngPrcePurcnstcst</td>
<td>예정가격순공사비</td>
<td style="text-align: left;">22</td>
<td>0</td>
<td>0</td>
<td style="text-align: left;">예정가격 중 순공사 원가(재료비,노무비,경비,및 이에 대한 부가가치세 합산금액)</td>
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
<td>REST(URI)</td>
</tr>
<tr>
<td style="text-align: left;">http://apis.data.go.kr/1230000/as/ScsbidInfoService/getOpengResultListInfoThngPreparPcDetail?inqryDiv=2&amp;bidNtceNo=R25BK00845027&amp;bidNtceOrd=000&amp;pageNo=1&amp;numOfRows=15&amp;ServiceKey=인증키</td>
</tr>
<tr>
<td>응답 메시지</td>
</tr>
<tr>
<td><p>&lt;response&gt;</p>
<p>&lt;header&gt;</p>
<p>&lt;resultCode&gt;00&lt;/resultCode&gt;</p>
<p>&lt;resultMsg&gt;정상&lt;/resultMsg&gt;</p>
<p>&lt;/header&gt;</p>
<p>&lt;body&gt;</p>
<p>&lt;items&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00845027&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;1&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;bidNtceNm&gt;CT 및 X-ray 구매&lt;/bidNtceNm&gt;</p>
<p>&lt;plnprc&gt;270648500&lt;/plnprc&gt;</p>
<p>&lt;bssamt&gt;270499000&lt;/bssamt&gt;</p>
<p>&lt;totRsrvtnPrceNum&gt;15&lt;/totRsrvtnPrceNum&gt;</p>
<p>&lt;compnoRsrvtnPrceSno&gt;1&lt;/compnoRsrvtnPrceSno&gt;</p>
<p>&lt;bsisPlnprc&gt;268378300&lt;/bsisPlnprc&gt;</p>
<p>&lt;drwtYn&gt;N&lt;/drwtYn&gt;</p>
<p>&lt;drwtNum&gt;0&lt;/drwtNum&gt;</p>
<p>&lt;bidwinrSlctnAplBssCntnts&gt;조달청&lt;/bidwinrSlctnAplBssCntnts&gt;</p>
<p>&lt;rlOpengDt&gt;2025-07-01 11:07:08&lt;/rlOpengDt&gt;</p>
<p>&lt;bssamtBssUpNum&gt;8&lt;/bssamtBssUpNum&gt;</p>
<p>&lt;compnoRsrvtnPrceMkngDt&gt;2025-07-01 10:47:30&lt;/compnoRsrvtnPrceMkngDt&gt;</p>
<p>&lt;inptDt&gt;2025-07-01 11:07:08&lt;/inptDt&gt;</p>
<p>&lt;PrearngPrcePurcnstcst&gt;&lt;/PrearngPrcePurcnstcst&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00845027&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;1&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;bidNtceNm&gt;CT 및 X-ray 구매&lt;/bidNtceNm&gt;</p>
<p>&lt;plnprc&gt;270648500&lt;/plnprc&gt;</p>
<p>&lt;bssamt&gt;270499000&lt;/bssamt&gt;</p>
<p>&lt;totRsrvtnPrceNum&gt;15&lt;/totRsrvtnPrceNum&gt;</p>
<p>&lt;compnoRsrvtnPrceSno&gt;2&lt;/compnoRsrvtnPrceSno&gt;</p>
<p>&lt;bsisPlnprc&gt;273106700&lt;/bsisPlnprc&gt;</p>
<p>&lt;drwtYn&gt;N&lt;/drwtYn&gt;</p>
<p>&lt;drwtNum&gt;0&lt;/drwtNum&gt;</p>
<p>&lt;bidwinrSlctnAplBssCntnts&gt;조달청&lt;/bidwinrSlctnAplBssCntnts&gt;</p>
<p>&lt;rlOpengDt&gt;2025-07-01 11:07:08&lt;/rlOpengDt&gt;</p>
<p>&lt;bssamtBssUpNum&gt;8&lt;/bssamtBssUpNum&gt;</p>
<p>&lt;compnoRsrvtnPrceMkngDt&gt;2025-07-01 10:47:30&lt;/compnoRsrvtnPrceMkngDt&gt;</p>
<p>&lt;inptDt&gt;2025-07-01 11:07:08&lt;/inptDt&gt;</p>
<p>&lt;PrearngPrcePurcnstcst&gt;&lt;/PrearngPrcePurcnstcst&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00845027&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;1&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;bidNtceNm&gt;CT 및 X-ray 구매&lt;/bidNtceNm&gt;</p>
<p>&lt;plnprc&gt;270648500&lt;/plnprc&gt;</p>
<p>&lt;bssamt&gt;270499000&lt;/bssamt&gt;</p>
<p>&lt;totRsrvtnPrceNum&gt;15&lt;/totRsrvtnPrceNum&gt;</p>
<p>&lt;compnoRsrvtnPrceSno&gt;3&lt;/compnoRsrvtnPrceSno&gt;</p>
<p>&lt;bsisPlnprc&gt;267875200&lt;/bsisPlnprc&gt;</p>
<p>&lt;drwtYn&gt;N&lt;/drwtYn&gt;</p>
<p>&lt;drwtNum&gt;0&lt;/drwtNum&gt;</p>
<p>&lt;bidwinrSlctnAplBssCntnts&gt;조달청&lt;/bidwinrSlctnAplBssCntnts&gt;</p>
<p>&lt;rlOpengDt&gt;2025-07-01 11:07:08&lt;/rlOpengDt&gt;</p>
<p>&lt;bssamtBssUpNum&gt;8&lt;/bssamtBssUpNum&gt;</p>
<p>&lt;compnoRsrvtnPrceMkngDt&gt;2025-07-01 10:47:30&lt;/compnoRsrvtnPrceMkngDt&gt;</p>
<p>&lt;inptDt&gt;2025-07-01 11:07:08&lt;/inptDt&gt;</p>
<p>&lt;PrearngPrcePurcnstcst&gt;&lt;/PrearngPrcePurcnstcst&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00845027&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;1&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;bidNtceNm&gt;CT 및 X-ray 구매&lt;/bidNtceNm&gt;</p>
<p>&lt;plnprc&gt;270648500&lt;/plnprc&gt;</p>
<p>&lt;bssamt&gt;270499000&lt;/bssamt&gt;</p>
<p>&lt;totRsrvtnPrceNum&gt;15&lt;/totRsrvtnPrceNum&gt;</p>
<p>&lt;compnoRsrvtnPrceSno&gt;4&lt;/compnoRsrvtnPrceSno&gt;</p>
<p>&lt;bsisPlnprc&gt;269928300&lt;/bsisPlnprc&gt;</p>
<p>&lt;drwtYn&gt;Y&lt;/drwtYn&gt;</p>
<p>&lt;drwtNum&gt;1&lt;/drwtNum&gt;</p>
<p>&lt;bidwinrSlctnAplBssCntnts&gt;조달청&lt;/bidwinrSlctnAplBssCntnts&gt;</p>
<p>&lt;rlOpengDt&gt;2025-07-01 11:07:08&lt;/rlOpengDt&gt;</p>
<p>&lt;bssamtBssUpNum&gt;8&lt;/bssamtBssUpNum&gt;</p>
<p>&lt;compnoRsrvtnPrceMkngDt&gt;2025-07-01 10:47:30&lt;/compnoRsrvtnPrceMkngDt&gt;</p>
<p>&lt;inptDt&gt;2025-07-01 11:07:08&lt;/inptDt&gt;</p>
<p>&lt;PrearngPrcePurcnstcst&gt;&lt;/PrearngPrcePurcnstcst&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00845027&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;1&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;bidNtceNm&gt;CT 및 X-ray 구매&lt;/bidNtceNm&gt;</p>
<p>&lt;plnprc&gt;270648500&lt;/plnprc&gt;</p>
<p>&lt;bssamt&gt;270499000&lt;/bssamt&gt;</p>
<p>&lt;totRsrvtnPrceNum&gt;15&lt;/totRsrvtnPrceNum&gt;</p>
<p>&lt;compnoRsrvtnPrceSno&gt;5&lt;/compnoRsrvtnPrceSno&gt;</p>
<p>&lt;bsisPlnprc&gt;274583600&lt;/bsisPlnprc&gt;</p>
<p>&lt;drwtYn&gt;Y&lt;/drwtYn&gt;</p>
<p>&lt;drwtNum&gt;1&lt;/drwtNum&gt;</p>
<p>&lt;bidwinrSlctnAplBssCntnts&gt;조달청&lt;/bidwinrSlctnAplBssCntnts&gt;</p>
<p>&lt;rlOpengDt&gt;2025-07-01 11:07:08&lt;/rlOpengDt&gt;</p>
<p>&lt;bssamtBssUpNum&gt;8&lt;/bssamtBssUpNum&gt;</p>
<p>&lt;compnoRsrvtnPrceMkngDt&gt;2025-07-01 10:47:30&lt;/compnoRsrvtnPrceMkngDt&gt;</p>
<p>&lt;inptDt&gt;2025-07-01 11:07:08&lt;/inptDt&gt;</p>
<p>&lt;PrearngPrcePurcnstcst&gt;&lt;/PrearngPrcePurcnstcst&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00845027&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;1&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;bidNtceNm&gt;CT 및 X-ray 구매&lt;/bidNtceNm&gt;</p>
<p>&lt;plnprc&gt;270648500&lt;/plnprc&gt;</p>
<p>&lt;bssamt&gt;270499000&lt;/bssamt&gt;</p>
<p>&lt;totRsrvtnPrceNum&gt;15&lt;/totRsrvtnPrceNum&gt;</p>
<p>&lt;compnoRsrvtnPrceSno&gt;6&lt;/compnoRsrvtnPrceSno&gt;</p>
<p>&lt;bsisPlnprc&gt;275706200&lt;/bsisPlnprc&gt;</p>
<p>&lt;drwtYn&gt;N&lt;/drwtYn&gt;</p>
<p>&lt;drwtNum&gt;0&lt;/drwtNum&gt;</p>
<p>&lt;bidwinrSlctnAplBssCntnts&gt;조달청&lt;/bidwinrSlctnAplBssCntnts&gt;</p>
<p>&lt;rlOpengDt&gt;2025-07-01 11:07:08&lt;/rlOpengDt&gt;</p>
<p>&lt;bssamtBssUpNum&gt;8&lt;/bssamtBssUpNum&gt;</p>
<p>&lt;compnoRsrvtnPrceMkngDt&gt;2025-07-01 10:47:30&lt;/compnoRsrvtnPrceMkngDt&gt;</p>
<p>&lt;inptDt&gt;2025-07-01 11:07:08&lt;/inptDt&gt;</p>
<p>&lt;PrearngPrcePurcnstcst&gt;&lt;/PrearngPrcePurcnstcst&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00845027&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;1&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;bidNtceNm&gt;CT 및 X-ray 구매&lt;/bidNtceNm&gt;</p>
<p>&lt;plnprc&gt;270648500&lt;/plnprc&gt;</p>
<p>&lt;bssamt&gt;270499000&lt;/bssamt&gt;</p>
<p>&lt;totRsrvtnPrceNum&gt;15&lt;/totRsrvtnPrceNum&gt;</p>
<p>&lt;compnoRsrvtnPrceSno&gt;7&lt;/compnoRsrvtnPrceSno&gt;</p>
<p>&lt;bsisPlnprc&gt;265727400&lt;/bsisPlnprc&gt;</p>
<p>&lt;drwtYn&gt;Y&lt;/drwtYn&gt;</p>
<p>&lt;drwtNum&gt;1&lt;/drwtNum&gt;</p>
<p>&lt;bidwinrSlctnAplBssCntnts&gt;조달청&lt;/bidwinrSlctnAplBssCntnts&gt;</p>
<p>&lt;rlOpengDt&gt;2025-07-01 11:07:08&lt;/rlOpengDt&gt;</p>
<p>&lt;bssamtBssUpNum&gt;8&lt;/bssamtBssUpNum&gt;</p>
<p>&lt;compnoRsrvtnPrceMkngDt&gt;2025-07-01 10:47:30&lt;/compnoRsrvtnPrceMkngDt&gt;</p>
<p>&lt;inptDt&gt;2025-07-01 11:07:08&lt;/inptDt&gt;</p>
<p>&lt;PrearngPrcePurcnstcst&gt;&lt;/PrearngPrcePurcnstcst&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00845027&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;1&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;bidNtceNm&gt;CT 및 X-ray 구매&lt;/bidNtceNm&gt;</p>
<p>&lt;plnprc&gt;270648500&lt;/plnprc&gt;</p>
<p>&lt;bssamt&gt;270499000&lt;/bssamt&gt;</p>
<p>&lt;totRsrvtnPrceNum&gt;15&lt;/totRsrvtnPrceNum&gt;</p>
<p>&lt;compnoRsrvtnPrceSno&gt;8&lt;/compnoRsrvtnPrceSno&gt;</p>
<p>&lt;bsisPlnprc&gt;268984300&lt;/bsisPlnprc&gt;</p>
<p>&lt;drwtYn&gt;N&lt;/drwtYn&gt;</p>
<p>&lt;drwtNum&gt;0&lt;/drwtNum&gt;</p>
<p>&lt;bidwinrSlctnAplBssCntnts&gt;조달청&lt;/bidwinrSlctnAplBssCntnts&gt;</p>
<p>&lt;rlOpengDt&gt;2025-07-01 11:07:08&lt;/rlOpengDt&gt;</p>
<p>&lt;bssamtBssUpNum&gt;8&lt;/bssamtBssUpNum&gt;</p>
<p>&lt;compnoRsrvtnPrceMkngDt&gt;2025-07-01 10:47:30&lt;/compnoRsrvtnPrceMkngDt&gt;</p>
<p>&lt;inptDt&gt;2025-07-01 11:07:08&lt;/inptDt&gt;</p>
<p>&lt;PrearngPrcePurcnstcst&gt;&lt;/PrearngPrcePurcnstcst&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00845027&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;1&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;bidNtceNm&gt;CT 및 X-ray 구매&lt;/bidNtceNm&gt;</p>
<p>&lt;plnprc&gt;270648500&lt;/plnprc&gt;</p>
<p>&lt;bssamt&gt;270499000&lt;/bssamt&gt;</p>
<p>&lt;totRsrvtnPrceNum&gt;15&lt;/totRsrvtnPrceNum&gt;</p>
<p>&lt;compnoRsrvtnPrceSno&gt;9&lt;/compnoRsrvtnPrceSno&gt;</p>
<p>&lt;bsisPlnprc&gt;270512600&lt;/bsisPlnprc&gt;</p>
<p>&lt;drwtYn&gt;N&lt;/drwtYn&gt;</p>
<p>&lt;drwtNum&gt;0&lt;/drwtNum&gt;</p>
<p>&lt;bidwinrSlctnAplBssCntnts&gt;조달청&lt;/bidwinrSlctnAplBssCntnts&gt;</p>
<p>&lt;rlOpengDt&gt;2025-07-01 11:07:08&lt;/rlOpengDt&gt;</p>
<p>&lt;bssamtBssUpNum&gt;8&lt;/bssamtBssUpNum&gt;</p>
<p>&lt;compnoRsrvtnPrceMkngDt&gt;2025-07-01 10:47:30&lt;/compnoRsrvtnPrceMkngDt&gt;</p>
<p>&lt;inptDt&gt;2025-07-01 11:07:08&lt;/inptDt&gt;</p>
<p>&lt;PrearngPrcePurcnstcst&gt;&lt;/PrearngPrcePurcnstcst&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00845027&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;1&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;bidNtceNm&gt;CT 및 X-ray 구매&lt;/bidNtceNm&gt;</p>
<p>&lt;plnprc&gt;270648500&lt;/plnprc&gt;</p>
<p>&lt;bssamt&gt;270499000&lt;/bssamt&gt;</p>
<p>&lt;totRsrvtnPrceNum&gt;15&lt;/totRsrvtnPrceNum&gt;</p>
<p>&lt;compnoRsrvtnPrceSno&gt;10&lt;/compnoRsrvtnPrceSno&gt;</p>
<p>&lt;bsisPlnprc&gt;273842400&lt;/bsisPlnprc&gt;</p>
<p>&lt;drwtYn&gt;N&lt;/drwtYn&gt;</p>
<p>&lt;drwtNum&gt;0&lt;/drwtNum&gt;</p>
<p>&lt;bidwinrSlctnAplBssCntnts&gt;조달청&lt;/bidwinrSlctnAplBssCntnts&gt;</p>
<p>&lt;rlOpengDt&gt;2025-07-01 11:07:08&lt;/rlOpengDt&gt;</p>
<p>&lt;bssamtBssUpNum&gt;8&lt;/bssamtBssUpNum&gt;</p>
<p>&lt;compnoRsrvtnPrceMkngDt&gt;2025-07-01 10:47:30&lt;/compnoRsrvtnPrceMkngDt&gt;</p>
<p>&lt;inptDt&gt;2025-07-01 11:07:08&lt;/inptDt&gt;</p>
<p>&lt;PrearngPrcePurcnstcst&gt;&lt;/PrearngPrcePurcnstcst&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;/items&gt;</p>
<p>&lt;numOfRows&gt;10&lt;/numOfRows&gt;</p>
<p>&lt;pageNo&gt;1&lt;/pageNo&gt;</p>
<p>&lt;totalCount&gt;15&lt;/totalCount&gt;</p>
<p>&lt;/body&gt;</p>
<p>&lt;/response&gt;</p></td>
</tr>
</tbody>
</table>

#### \[개찰결과 공사 예비가격상세 목록 조회\] 오퍼레이션 명세

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
<td>10</td>
<td>오퍼레이션명(국문)</td>
<td colspan="2">개찰결과 공사 예비가격상세 목록 조회</td>
</tr>
<tr>
<td>오퍼레이션 유형</td>
<td>조회(목록)</td>
<td>오퍼레이션명(영문)</td>
<td colspan="2"><strong>getOpengResultListInfoCnstwkPreparPcDetail</strong></td>
</tr>
<tr>
<td>오퍼레이션 설명</td>
<td colspan="4">검색조건을 등록일시, 입찰공고번호로 공사에 대한 나라장터 개찰결과 예비가격상세 목록(입찰공고번호, 입찰공고명, 예정가격, 기초금액, 총예가건수, 복수예가순번, 기초예정가격, 추첨여부, 추첨횟수, 실개찰일시, 기초금액기준상위건수, 복수예비가격작성일시, 입력일시)을 조회</td>
</tr>
<tr>
<td>Call Back URL</td>
<td colspan="4" style="text-align: left;">N/A</td>
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
<col style="width: 11%" />
<col style="width: 14%" />
<col style="width: 20%" />
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
<td>4</td>
<td>1</td>
<td>10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td>pageNo</td>
<td>페이지 번호</td>
<td>4</td>
<td>1</td>
<td>1</td>
<td style="text-align: left;">페이지 번호</td>
</tr>
<tr>
<td style="text-align: left;">ServiceKey</td>
<td style="text-align: left;">서비스키</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">공공데이터포털에서 받은 인증키</td>
<td style="text-align: left;">공공데이터포털에서 받은 인증키</td>
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
<td>조회구분</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">검색하고자하는 조회구분<br />
1.입력일시, 2.입찰공고번호</td>
</tr>
<tr>
<td>inqryBgnDt</td>
<td>조회시작일시</td>
<td>12</td>
<td style="text-align: left;">0</td>
<td>202507010000</td>
<td>검색하고자하는 시작일시<br />
'YYYYMMDDHHMM'<br />
조회구분이 1일 경우 필수</td>
</tr>
<tr>
<td>inqryEndDt</td>
<td>조회종료일시</td>
<td>12</td>
<td style="text-align: left;">0</td>
<td>202507012359</td>
<td>검색하고자하는 종료일시<br />
'YYYYMMDDHHMM'<br />
조회구분이 1일 경우 필수</td>
</tr>
<tr>
<td>bidNtceNo</td>
<td>입찰공고번호</td>
<td>11</td>
<td style="text-align: left;">0</td>
<td>R25BK00888538</td>
<td><p>검색하고자하는 입찰공고번호</p>
<p>조회구분이 2일 경우 필수</p></td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 응답 메시지 명세

<table style="width:100%;">
<colgroup>
<col style="width: 21%" />
<col style="width: 21%" />
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 13%" />
<col style="width: 20%" />
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
<td>numOfRows</td>
<td>한 페이지 결과 수</td>
<td>4</td>
<td>1</td>
<td>10</td>
<td>한 페이지 결과 수</td>
</tr>
<tr>
<td>pageNo</td>
<td>페이지 번호</td>
<td>4</td>
<td>1</td>
<td>1</td>
<td>페이지 번호</td>
</tr>
<tr>
<td>totalCount</td>
<td>데이터 총 개수</td>
<td>4</td>
<td>1</td>
<td>17</td>
<td>데이터 총 개수</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNo</td>
<td>입찰공고번호</td>
<td>11</td>
<td style="text-align: left;">1</td>
<td>R25BK00888538</td>
<td style="text-align: left;">입찰공고 관리번호이며 조달청나라장터 공고건의 형식은 년도(4)+월(2)+순번(5)이며 자체전자조달시스템 보유기관은 각 기관별 형식 별도 사용<br />
*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성<br />
- 단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</td>
</tr>
<tr>
<td>bidNtceOrd</td>
<td>입찰공고차수</td>
<td>3</td>
<td style="text-align: left;">1</td>
<td>003</td>
<td>입찰공고차수는 해당 입찰공고에 대한 재공고 및 재입찰 등이 발생되었을 경우 증가되는 수</td>
</tr>
<tr>
<td>bidClsfcNo</td>
<td>입찰분류번호</td>
<td>5</td>
<td style="text-align: left;">1</td>
<td>0</td>
<td>동일한 입찰공고번호에 대한 집행일련번호</td>
</tr>
<tr>
<td>rbidNo</td>
<td>재입찰번호</td>
<td>3</td>
<td style="text-align: left;">1</td>
<td>000</td>
<td>재입찰번호</td>
</tr>
<tr>
<td>bidNtceNm</td>
<td>입찰공고명</td>
<td>1000</td>
<td style="text-align: left;">1</td>
<td>하동군수협 유통단계 위생안전체계 구축사업 (친환경 위판장) (건축,기계,냉동)</td>
<td>공사명 또는 사업명이라고도 하며 입찰공고 내용을 요약한 이름</td>
</tr>
<tr>
<td>plnprc</td>
<td>예정가격</td>
<td>21</td>
<td style="text-align: left;">0</td>
<td>1773240950</td>
<td>예정가격은 계약담당공무원이 구매를 위한 경쟁입찰 또는 수의시담을 하기 전에 당해 계약 목적물의 특성 및 계약 여건 등을 고려하여 예산의 범위 내에서 경제적으로 구매가 가능하고 구매가격으로서 적정하다고 판단하여 정한 가격을 말하며 동 가격은 입찰 또는 시담에 의한 낙찰자 선정의 기준이고 계약체결에 대한 최고 상한 금액을 의미함. (원화,원)</td>
</tr>
<tr>
<td>bssamt</td>
<td>기초금액</td>
<td>21</td>
<td style="text-align: left;">0</td>
<td>1797931000</td>
<td>예정가격 작성 과정에서 거래실례가격, 원가계산가격 등에 의하여 조사한 가격이나 설계가격에 대하여 계약담당공무원이 그 적정여부를 검토조정한 가격(원화,원)</td>
</tr>
<tr>
<td>totRsrvtnPrceNum</td>
<td>총예가건수</td>
<td>2</td>
<td style="text-align: left;">0</td>
<td>15</td>
<td>총예가건수</td>
</tr>
<tr>
<td>compnoRsrvtnPrceSno</td>
<td>복수예가순번</td>
<td>6</td>
<td style="text-align: left;">0</td>
<td>1</td>
<td>복수예가순번</td>
</tr>
<tr>
<td>bsisPlnprc</td>
<td>기초예정가격</td>
<td>21</td>
<td style="text-align: left;">0</td>
<td>1825493300</td>
<td>기초예정가격(원화,원)</td>
</tr>
<tr>
<td>drwtYn</td>
<td>추첨여부</td>
<td>1</td>
<td style="text-align: left;">1</td>
<td>Y</td>
<td>추첨여부(Y/N)</td>
</tr>
<tr>
<td>drwtNum</td>
<td>추첨횟수</td>
<td>22</td>
<td style="text-align: left;">0</td>
<td>11</td>
<td>추첨횟수</td>
</tr>
<tr>
<td>bidwinrSlctnAplBssCntnts</td>
<td>최종낙찰자선정적용기준내용</td>
<td>200</td>
<td style="text-align: left;">0</td>
<td>행자부</td>
<td>낙찰자선정적용기준내용</td>
</tr>
<tr>
<td style="text-align: left;">rlOpengDt</td>
<td>실개찰일시</td>
<td>19</td>
<td style="text-align: left;">0</td>
<td>2025-07-01 13:14:24</td>
<td>실제 개찰일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">bssamtBssUpNum</td>
<td>기초금액기준상위건수</td>
<td>2</td>
<td style="text-align: left;">0</td>
<td>7</td>
<td>기초금액기준상위건수</td>
</tr>
<tr>
<td style="text-align: left;">compnoRsrvtnPrceMkngDt</td>
<td>복수예비가격작성일시</td>
<td>19</td>
<td style="text-align: left;">0</td>
<td>2025-07-01 13:07:31</td>
<td>복수예비가격작성시각”YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">inptDt</td>
<td>입력일시</td>
<td style="text-align: left;">19</td>
<td>1</td>
<td>2025-07-01 13:14:24</td>
<td style="text-align: left;">입력일시 "YYYY-MM-DD HH:MM:SS"</td>
</tr>
<tr>
<td style="text-align: left;">PrearngPrcePurcnstcst</td>
<td>예정가격순공사비</td>
<td style="text-align: left;">22</td>
<td>0</td>
<td>1470841837</td>
<td style="text-align: left;">예정가격 중 순공사 원가(재료비,노무비,경비,및 이에 대한 부가가치세 합산금액)</td>
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
<td>REST(URI)</td>
</tr>
<tr>
<td style="text-align: left;">http://apis.data.go.kr/1230000/as/ScsbidInfoService/getOpengResultListInfoCnstwkPreparPcDetail?inqryDiv=2&amp;bidNtceNo=R25BK00888538&amp;bidNtceOrd=003&amp;pageNo=1&amp;numOfRows=15&amp;ServiceKey=인증키</td>
</tr>
<tr>
<td>응답 메시지</td>
</tr>
<tr>
<td><p>&lt;response&gt;</p>
<p>&lt;header&gt;</p>
<p>&lt;resultCode&gt;00&lt;/resultCode&gt;</p>
<p>&lt;resultMsg&gt;정상&lt;/resultMsg&gt;</p>
<p>&lt;/header&gt;</p>
<p>&lt;body&gt;</p>
<p>&lt;items&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00888538&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;003&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;0&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;bidNtceNm&gt;하동군수협 유통단계 위생안전체계 구축사업 (친환경 위판장) (건축,기계,냉동)&lt;/bidNtceNm&gt;</p>
<p>&lt;plnprc&gt;1773240950&lt;/plnprc&gt;</p>
<p>&lt;bssamt&gt;1797931000&lt;/bssamt&gt;</p>
<p>&lt;totRsrvtnPrceNum&gt;15&lt;/totRsrvtnPrceNum&gt;</p>
<p>&lt;compnoRsrvtnPrceSno&gt;1&lt;/compnoRsrvtnPrceSno&gt;</p>
<p>&lt;bsisPlnprc&gt;1825493300&lt;/bsisPlnprc&gt;</p>
<p>&lt;drwtYn&gt;Y&lt;/drwtYn&gt;</p>
<p>&lt;drwtNum&gt;11&lt;/drwtNum&gt;</p>
<p>&lt;bidwinrSlctnAplBssCntnts&gt;행자부&lt;/bidwinrSlctnAplBssCntnts&gt;</p>
<p>&lt;rlOpengDt&gt;2025-07-01 13:14:24&lt;/rlOpengDt&gt;</p>
<p>&lt;bssamtBssUpNum&gt;7&lt;/bssamtBssUpNum&gt;</p>
<p>&lt;compnoRsrvtnPrceMkngDt&gt;2025-07-01 13:07:31&lt;/compnoRsrvtnPrceMkngDt&gt;</p>
<p>&lt;inptDt&gt;2025-07-01 13:14:24&lt;/inptDt&gt;</p>
<p>&lt;PrearngPrcePurcnstcst&gt;1470841837&lt;/PrearngPrcePurcnstcst&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00888538&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;003&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;0&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;bidNtceNm&gt;하동군수협 유통단계 위생안전체계 구축사업 (친환경 위판장) (건축,기계,냉동)&lt;/bidNtceNm&gt;</p>
<p>&lt;plnprc&gt;1773240950&lt;/plnprc&gt;</p>
<p>&lt;bssamt&gt;1797931000&lt;/bssamt&gt;</p>
<p>&lt;totRsrvtnPrceNum&gt;15&lt;/totRsrvtnPrceNum&gt;</p>
<p>&lt;compnoRsrvtnPrceSno&gt;2&lt;/compnoRsrvtnPrceSno&gt;</p>
<p>&lt;bsisPlnprc&gt;1759904800&lt;/bsisPlnprc&gt;</p>
<p>&lt;drwtYn&gt;Y&lt;/drwtYn&gt;</p>
<p>&lt;drwtNum&gt;13&lt;/drwtNum&gt;</p>
<p>&lt;bidwinrSlctnAplBssCntnts&gt;행자부&lt;/bidwinrSlctnAplBssCntnts&gt;</p>
<p>&lt;rlOpengDt&gt;2025-07-01 13:14:24&lt;/rlOpengDt&gt;</p>
<p>&lt;bssamtBssUpNum&gt;7&lt;/bssamtBssUpNum&gt;</p>
<p>&lt;compnoRsrvtnPrceMkngDt&gt;2025-07-01 13:07:31&lt;/compnoRsrvtnPrceMkngDt&gt;</p>
<p>&lt;inptDt&gt;2025-07-01 13:14:24&lt;/inptDt&gt;</p>
<p>&lt;PrearngPrcePurcnstcst&gt;1470841837&lt;/PrearngPrcePurcnstcst&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00888538&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;003&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;0&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;bidNtceNm&gt;하동군수협 유통단계 위생안전체계 구축사업 (친환경 위판장) (건축,기계,냉동)&lt;/bidNtceNm&gt;</p>
<p>&lt;plnprc&gt;1773240950&lt;/plnprc&gt;</p>
<p>&lt;bssamt&gt;1797931000&lt;/bssamt&gt;</p>
<p>&lt;totRsrvtnPrceNum&gt;15&lt;/totRsrvtnPrceNum&gt;</p>
<p>&lt;compnoRsrvtnPrceSno&gt;3&lt;/compnoRsrvtnPrceSno&gt;</p>
<p>&lt;bsisPlnprc&gt;1757387700&lt;/bsisPlnprc&gt;</p>
<p>&lt;drwtYn&gt;Y&lt;/drwtYn&gt;</p>
<p>&lt;drwtNum&gt;9&lt;/drwtNum&gt;</p>
<p>&lt;bidwinrSlctnAplBssCntnts&gt;행자부&lt;/bidwinrSlctnAplBssCntnts&gt;</p>
<p>&lt;rlOpengDt&gt;2025-07-01 13:14:24&lt;/rlOpengDt&gt;</p>
<p>&lt;bssamtBssUpNum&gt;7&lt;/bssamtBssUpNum&gt;</p>
<p>&lt;compnoRsrvtnPrceMkngDt&gt;2025-07-01 13:07:31&lt;/compnoRsrvtnPrceMkngDt&gt;</p>
<p>&lt;inptDt&gt;2025-07-01 13:14:24&lt;/inptDt&gt;</p>
<p>&lt;PrearngPrcePurcnstcst&gt;1470841837&lt;/PrearngPrcePurcnstcst&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00888538&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;003&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;0&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;bidNtceNm&gt;하동군수협 유통단계 위생안전체계 구축사업 (친환경 위판장) (건축,기계,냉동)&lt;/bidNtceNm&gt;</p>
<p>&lt;plnprc&gt;1773240950&lt;/plnprc&gt;</p>
<p>&lt;bssamt&gt;1797931000&lt;/bssamt&gt;</p>
<p>&lt;totRsrvtnPrceNum&gt;15&lt;/totRsrvtnPrceNum&gt;</p>
<p>&lt;compnoRsrvtnPrceSno&gt;4&lt;/compnoRsrvtnPrceSno&gt;</p>
<p>&lt;bsisPlnprc&gt;1772418400&lt;/bsisPlnprc&gt;</p>
<p>&lt;drwtYn&gt;N&lt;/drwtYn&gt;</p>
<p>&lt;drwtNum&gt;7&lt;/drwtNum&gt;</p>
<p>&lt;bidwinrSlctnAplBssCntnts&gt;행자부&lt;/bidwinrSlctnAplBssCntnts&gt;</p>
<p>&lt;rlOpengDt&gt;2025-07-01 13:14:24&lt;/rlOpengDt&gt;</p>
<p>&lt;bssamtBssUpNum&gt;7&lt;/bssamtBssUpNum&gt;</p>
<p>&lt;compnoRsrvtnPrceMkngDt&gt;2025-07-01 13:07:31&lt;/compnoRsrvtnPrceMkngDt&gt;</p>
<p>&lt;inptDt&gt;2025-07-01 13:14:24&lt;/inptDt&gt;</p>
<p>&lt;PrearngPrcePurcnstcst&gt;1470841837&lt;/PrearngPrcePurcnstcst&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00888538&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;003&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;0&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;bidNtceNm&gt;하동군수협 유통단계 위생안전체계 구축사업 (친환경 위판장) (건축,기계,냉동)&lt;/bidNtceNm&gt;</p>
<p>&lt;plnprc&gt;1773240950&lt;/plnprc&gt;</p>
<p>&lt;bssamt&gt;1797931000&lt;/bssamt&gt;</p>
<p>&lt;totRsrvtnPrceNum&gt;15&lt;/totRsrvtnPrceNum&gt;</p>
<p>&lt;compnoRsrvtnPrceSno&gt;5&lt;/compnoRsrvtnPrceSno&gt;</p>
<p>&lt;bsisPlnprc&gt;1780023700&lt;/bsisPlnprc&gt;</p>
<p>&lt;drwtYn&gt;N&lt;/drwtYn&gt;</p>
<p>&lt;drwtNum&gt;7&lt;/drwtNum&gt;</p>
<p>&lt;bidwinrSlctnAplBssCntnts&gt;행자부&lt;/bidwinrSlctnAplBssCntnts&gt;</p>
<p>&lt;rlOpengDt&gt;2025-07-01 13:14:24&lt;/rlOpengDt&gt;</p>
<p>&lt;bssamtBssUpNum&gt;7&lt;/bssamtBssUpNum&gt;</p>
<p>&lt;compnoRsrvtnPrceMkngDt&gt;2025-07-01 13:07:31&lt;/compnoRsrvtnPrceMkngDt&gt;</p>
<p>&lt;inptDt&gt;2025-07-01 13:14:24&lt;/inptDt&gt;</p>
<p>&lt;PrearngPrcePurcnstcst&gt;1470841837&lt;/PrearngPrcePurcnstcst&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00888538&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;003&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;0&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;bidNtceNm&gt;하동군수협 유통단계 위생안전체계 구축사업 (친환경 위판장) (건축,기계,냉동)&lt;/bidNtceNm&gt;</p>
<p>&lt;plnprc&gt;1773240950&lt;/plnprc&gt;</p>
<p>&lt;bssamt&gt;1797931000&lt;/bssamt&gt;</p>
<p>&lt;totRsrvtnPrceNum&gt;15&lt;/totRsrvtnPrceNum&gt;</p>
<p>&lt;compnoRsrvtnPrceSno&gt;6&lt;/compnoRsrvtnPrceSno&gt;</p>
<p>&lt;bsisPlnprc&gt;1750178000&lt;/bsisPlnprc&gt;</p>
<p>&lt;drwtYn&gt;Y&lt;/drwtYn&gt;</p>
<p>&lt;drwtNum&gt;11&lt;/drwtNum&gt;</p>
<p>&lt;bidwinrSlctnAplBssCntnts&gt;행자부&lt;/bidwinrSlctnAplBssCntnts&gt;</p>
<p>&lt;rlOpengDt&gt;2025-07-01 13:14:24&lt;/rlOpengDt&gt;</p>
<p>&lt;bssamtBssUpNum&gt;7&lt;/bssamtBssUpNum&gt;</p>
<p>&lt;compnoRsrvtnPrceMkngDt&gt;2025-07-01 13:07:31&lt;/compnoRsrvtnPrceMkngDt&gt;</p>
<p>&lt;inptDt&gt;2025-07-01 13:14:24&lt;/inptDt&gt;</p>
<p>&lt;PrearngPrcePurcnstcst&gt;1470841837&lt;/PrearngPrcePurcnstcst&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00888538&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;003&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;0&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;bidNtceNm&gt;하동군수협 유통단계 위생안전체계 구축사업 (친환경 위판장) (건축,기계,냉동)&lt;/bidNtceNm&gt;</p>
<p>&lt;plnprc&gt;1773240950&lt;/plnprc&gt;</p>
<p>&lt;bssamt&gt;1797931000&lt;/bssamt&gt;</p>
<p>&lt;totRsrvtnPrceNum&gt;15&lt;/totRsrvtnPrceNum&gt;</p>
<p>&lt;compnoRsrvtnPrceSno&gt;7&lt;/compnoRsrvtnPrceSno&gt;</p>
<p>&lt;bsisPlnprc&gt;1808377000&lt;/bsisPlnprc&gt;</p>
<p>&lt;drwtYn&gt;N&lt;/drwtYn&gt;</p>
<p>&lt;drwtNum&gt;4&lt;/drwtNum&gt;</p>
<p>&lt;bidwinrSlctnAplBssCntnts&gt;행자부&lt;/bidwinrSlctnAplBssCntnts&gt;</p>
<p>&lt;rlOpengDt&gt;2025-07-01 13:14:24&lt;/rlOpengDt&gt;</p>
<p>&lt;bssamtBssUpNum&gt;7&lt;/bssamtBssUpNum&gt;</p>
<p>&lt;compnoRsrvtnPrceMkngDt&gt;2025-07-01 13:07:31&lt;/compnoRsrvtnPrceMkngDt&gt;</p>
<p>&lt;inptDt&gt;2025-07-01 13:14:24&lt;/inptDt&gt;</p>
<p>&lt;PrearngPrcePurcnstcst&gt;1470841837&lt;/PrearngPrcePurcnstcst&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00888538&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;003&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;0&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;bidNtceNm&gt;하동군수협 유통단계 위생안전체계 구축사업 (친환경 위판장) (건축,기계,냉동)&lt;/bidNtceNm&gt;</p>
<p>&lt;plnprc&gt;1773240950&lt;/plnprc&gt;</p>
<p>&lt;bssamt&gt;1797931000&lt;/bssamt&gt;</p>
<p>&lt;totRsrvtnPrceNum&gt;15&lt;/totRsrvtnPrceNum&gt;</p>
<p>&lt;compnoRsrvtnPrceSno&gt;8&lt;/compnoRsrvtnPrceSno&gt;</p>
<p>&lt;bsisPlnprc&gt;1830293800&lt;/bsisPlnprc&gt;</p>
<p>&lt;drwtYn&gt;N&lt;/drwtYn&gt;</p>
<p>&lt;drwtNum&gt;9&lt;/drwtNum&gt;</p>
<p>&lt;bidwinrSlctnAplBssCntnts&gt;행자부&lt;/bidwinrSlctnAplBssCntnts&gt;</p>
<p>&lt;rlOpengDt&gt;2025-07-01 13:14:24&lt;/rlOpengDt&gt;</p>
<p>&lt;bssamtBssUpNum&gt;7&lt;/bssamtBssUpNum&gt;</p>
<p>&lt;compnoRsrvtnPrceMkngDt&gt;2025-07-01 13:07:31&lt;/compnoRsrvtnPrceMkngDt&gt;</p>
<p>&lt;inptDt&gt;2025-07-01 13:14:24&lt;/inptDt&gt;</p>
<p>&lt;PrearngPrcePurcnstcst&gt;1470841837&lt;/PrearngPrcePurcnstcst&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00888538&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;003&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;0&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;bidNtceNm&gt;하동군수협 유통단계 위생안전체계 구축사업 (친환경 위판장) (건축,기계,냉동)&lt;/bidNtceNm&gt;</p>
<p>&lt;plnprc&gt;1773240950&lt;/plnprc&gt;</p>
<p>&lt;bssamt&gt;1797931000&lt;/bssamt&gt;</p>
<p>&lt;totRsrvtnPrceNum&gt;15&lt;/totRsrvtnPrceNum&gt;</p>
<p>&lt;compnoRsrvtnPrceSno&gt;9&lt;/compnoRsrvtnPrceSno&gt;</p>
<p>&lt;bsisPlnprc&gt;1804133900&lt;/bsisPlnprc&gt;</p>
<p>&lt;drwtYn&gt;N&lt;/drwtYn&gt;</p>
<p>&lt;drwtNum&gt;9&lt;/drwtNum&gt;</p>
<p>&lt;bidwinrSlctnAplBssCntnts&gt;행자부&lt;/bidwinrSlctnAplBssCntnts&gt;</p>
<p>&lt;rlOpengDt&gt;2025-07-01 13:14:24&lt;/rlOpengDt&gt;</p>
<p>&lt;bssamtBssUpNum&gt;7&lt;/bssamtBssUpNum&gt;</p>
<p>&lt;compnoRsrvtnPrceMkngDt&gt;2025-07-01 13:07:31&lt;/compnoRsrvtnPrceMkngDt&gt;</p>
<p>&lt;inptDt&gt;2025-07-01 13:14:24&lt;/inptDt&gt;</p>
<p>&lt;PrearngPrcePurcnstcst&gt;1470841837&lt;/PrearngPrcePurcnstcst&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00888538&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;003&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;0&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;bidNtceNm&gt;하동군수협 유통단계 위생안전체계 구축사업 (친환경 위판장) (건축,기계,냉동)&lt;/bidNtceNm&gt;</p>
<p>&lt;plnprc&gt;1773240950&lt;/plnprc&gt;</p>
<p>&lt;bssamt&gt;1797931000&lt;/bssamt&gt;</p>
<p>&lt;totRsrvtnPrceNum&gt;15&lt;/totRsrvtnPrceNum&gt;</p>
<p>&lt;compnoRsrvtnPrceSno&gt;10&lt;/compnoRsrvtnPrceSno&gt;</p>
<p>&lt;bsisPlnprc&gt;1769775500&lt;/bsisPlnprc&gt;</p>
<p>&lt;drwtYn&gt;N&lt;/drwtYn&gt;</p>
<p>&lt;drwtNum&gt;8&lt;/drwtNum&gt;</p>
<p>&lt;bidwinrSlctnAplBssCntnts&gt;행자부&lt;/bidwinrSlctnAplBssCntnts&gt;</p>
<p>&lt;rlOpengDt&gt;2025-07-01 13:14:24&lt;/rlOpengDt&gt;</p>
<p>&lt;bssamtBssUpNum&gt;7&lt;/bssamtBssUpNum&gt;</p>
<p>&lt;compnoRsrvtnPrceMkngDt&gt;2025-07-01 13:07:31&lt;/compnoRsrvtnPrceMkngDt&gt;</p>
<p>&lt;inptDt&gt;2025-07-01 13:14:24&lt;/inptDt&gt;</p>
<p>&lt;PrearngPrcePurcnstcst&gt;1470841837&lt;/PrearngPrcePurcnstcst&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00888538&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;003&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;0&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;bidNtceNm&gt;하동군수협 유통단계 위생안전체계 구축사업 (친환경 위판장) (건축,기계,냉동)&lt;/bidNtceNm&gt;</p>
<p>&lt;plnprc&gt;1773240950&lt;/plnprc&gt;</p>
<p>&lt;bssamt&gt;1797931000&lt;/bssamt&gt;</p>
<p>&lt;totRsrvtnPrceNum&gt;15&lt;/totRsrvtnPrceNum&gt;</p>
<p>&lt;compnoRsrvtnPrceSno&gt;11&lt;/compnoRsrvtnPrceSno&gt;</p>
<p>&lt;bsisPlnprc&gt;1785381500&lt;/bsisPlnprc&gt;</p>
<p>&lt;drwtYn&gt;N&lt;/drwtYn&gt;</p>
<p>&lt;drwtNum&gt;7&lt;/drwtNum&gt;</p>
<p>&lt;bidwinrSlctnAplBssCntnts&gt;행자부&lt;/bidwinrSlctnAplBssCntnts&gt;</p>
<p>&lt;rlOpengDt&gt;2025-07-01 13:14:24&lt;/rlOpengDt&gt;</p>
<p>&lt;bssamtBssUpNum&gt;7&lt;/bssamtBssUpNum&gt;</p>
<p>&lt;compnoRsrvtnPrceMkngDt&gt;2025-07-01 13:07:31&lt;/compnoRsrvtnPrceMkngDt&gt;</p>
<p>&lt;inptDt&gt;2025-07-01 13:14:24&lt;/inptDt&gt;</p>
<p>&lt;PrearngPrcePurcnstcst&gt;1470841837&lt;/PrearngPrcePurcnstcst&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00888538&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;003&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;0&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;bidNtceNm&gt;하동군수협 유통단계 위생안전체계 구축사업 (친환경 위판장) (건축,기계,냉동)&lt;/bidNtceNm&gt;</p>
<p>&lt;plnprc&gt;1773240950&lt;/plnprc&gt;</p>
<p>&lt;bssamt&gt;1797931000&lt;/bssamt&gt;</p>
<p>&lt;totRsrvtnPrceNum&gt;15&lt;/totRsrvtnPrceNum&gt;</p>
<p>&lt;compnoRsrvtnPrceSno&gt;12&lt;/compnoRsrvtnPrceSno&gt;</p>
<p>&lt;bsisPlnprc&gt;1837413600&lt;/bsisPlnprc&gt;</p>
<p>&lt;drwtYn&gt;N&lt;/drwtYn&gt;</p>
<p>&lt;drwtNum&gt;5&lt;/drwtNum&gt;</p>
<p>&lt;bidwinrSlctnAplBssCntnts&gt;행자부&lt;/bidwinrSlctnAplBssCntnts&gt;</p>
<p>&lt;rlOpengDt&gt;2025-07-01 13:14:24&lt;/rlOpengDt&gt;</p>
<p>&lt;bssamtBssUpNum&gt;7&lt;/bssamtBssUpNum&gt;</p>
<p>&lt;compnoRsrvtnPrceMkngDt&gt;2025-07-01 13:07:31&lt;/compnoRsrvtnPrceMkngDt&gt;</p>
<p>&lt;inptDt&gt;2025-07-01 13:14:24&lt;/inptDt&gt;</p>
<p>&lt;PrearngPrcePurcnstcst&gt;1470841837&lt;/PrearngPrcePurcnstcst&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00888538&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;003&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;0&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;bidNtceNm&gt;하동군수협 유통단계 위생안전체계 구축사업 (친환경 위판장) (건축,기계,냉동)&lt;/bidNtceNm&gt;</p>
<p>&lt;plnprc&gt;1773240950&lt;/plnprc&gt;</p>
<p>&lt;bssamt&gt;1797931000&lt;/bssamt&gt;</p>
<p>&lt;totRsrvtnPrceNum&gt;15&lt;/totRsrvtnPrceNum&gt;</p>
<p>&lt;compnoRsrvtnPrceSno&gt;13&lt;/compnoRsrvtnPrceSno&gt;</p>
<p>&lt;bsisPlnprc&gt;1795306100&lt;/bsisPlnprc&gt;</p>
<p>&lt;drwtYn&gt;N&lt;/drwtYn&gt;</p>
<p>&lt;drwtNum&gt;7&lt;/drwtNum&gt;</p>
<p>&lt;bidwinrSlctnAplBssCntnts&gt;행자부&lt;/bidwinrSlctnAplBssCntnts&gt;</p>
<p>&lt;rlOpengDt&gt;2025-07-01 13:14:24&lt;/rlOpengDt&gt;</p>
<p>&lt;bssamtBssUpNum&gt;7&lt;/bssamtBssUpNum&gt;</p>
<p>&lt;compnoRsrvtnPrceMkngDt&gt;2025-07-01 13:07:31&lt;/compnoRsrvtnPrceMkngDt&gt;</p>
<p>&lt;inptDt&gt;2025-07-01 13:14:24&lt;/inptDt&gt;</p>
<p>&lt;PrearngPrcePurcnstcst&gt;1470841837&lt;/PrearngPrcePurcnstcst&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00888538&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;003&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;0&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;bidNtceNm&gt;하동군수협 유통단계 위생안전체계 구축사업 (친환경 위판장) (건축,기계,냉동)&lt;/bidNtceNm&gt;</p>
<p>&lt;plnprc&gt;1773240950&lt;/plnprc&gt;</p>
<p>&lt;bssamt&gt;1797931000&lt;/bssamt&gt;</p>
<p>&lt;totRsrvtnPrceNum&gt;15&lt;/totRsrvtnPrceNum&gt;</p>
<p>&lt;compnoRsrvtnPrceSno&gt;14&lt;/compnoRsrvtnPrceSno&gt;</p>
<p>&lt;bsisPlnprc&gt;1848381000&lt;/bsisPlnprc&gt;</p>
<p>&lt;drwtYn&gt;N&lt;/drwtYn&gt;</p>
<p>&lt;drwtNum&gt;9&lt;/drwtNum&gt;</p>
<p>&lt;bidwinrSlctnAplBssCntnts&gt;행자부&lt;/bidwinrSlctnAplBssCntnts&gt;</p>
<p>&lt;rlOpengDt&gt;2025-07-01 13:14:24&lt;/rlOpengDt&gt;</p>
<p>&lt;bssamtBssUpNum&gt;7&lt;/bssamtBssUpNum&gt;</p>
<p>&lt;compnoRsrvtnPrceMkngDt&gt;2025-07-01 13:07:31&lt;/compnoRsrvtnPrceMkngDt&gt;</p>
<p>&lt;inptDt&gt;2025-07-01 13:14:24&lt;/inptDt&gt;</p>
<p>&lt;PrearngPrcePurcnstcst&gt;1470841837&lt;/PrearngPrcePurcnstcst&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00888538&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;003&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;0&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;bidNtceNm&gt;하동군수협 유통단계 위생안전체계 구축사업 (친환경 위판장) (건축,기계,냉동)&lt;/bidNtceNm&gt;</p>
<p>&lt;plnprc&gt;1773240950&lt;/plnprc&gt;</p>
<p>&lt;bssamt&gt;1797931000&lt;/bssamt&gt;</p>
<p>&lt;totRsrvtnPrceNum&gt;15&lt;/totRsrvtnPrceNum&gt;</p>
<p>&lt;compnoRsrvtnPrceSno&gt;15&lt;/compnoRsrvtnPrceSno&gt;</p>
<p>&lt;bsisPlnprc&gt;1815730600&lt;/bsisPlnprc&gt;</p>
<p>&lt;drwtYn&gt;N&lt;/drwtYn&gt;</p>
<p>&lt;drwtNum&gt;4&lt;/drwtNum&gt;</p>
<p>&lt;bidwinrSlctnAplBssCntnts&gt;행자부&lt;/bidwinrSlctnAplBssCntnts&gt;</p>
<p>&lt;rlOpengDt&gt;2025-07-01 13:14:24&lt;/rlOpengDt&gt;</p>
<p>&lt;bssamtBssUpNum&gt;7&lt;/bssamtBssUpNum&gt;</p>
<p>&lt;compnoRsrvtnPrceMkngDt&gt;2025-07-01 13:07:31&lt;/compnoRsrvtnPrceMkngDt&gt;</p>
<p>&lt;inptDt&gt;2025-07-01 13:14:24&lt;/inptDt&gt;</p>
<p>&lt;PrearngPrcePurcnstcst&gt;1470841837&lt;/PrearngPrcePurcnstcst&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;/items&gt;</p>
<p>&lt;numOfRows&gt;500&lt;/numOfRows&gt;</p>
<p>&lt;pageNo&gt;1&lt;/pageNo&gt;</p>
<p>&lt;totalCount&gt;15&lt;/totalCount&gt;</p>
<p>&lt;/body&gt;</p>
<p>&lt;/response&gt;</p></td>
</tr>
</tbody>
</table>

#### \[개찰결과 용역 예비가격상세 목록 조회\] 오퍼레이션 명세

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
<td>11</td>
<td>오퍼레이션명(국문)</td>
<td colspan="2">개찰결과 용역 예비가격상세 목록 조회</td>
</tr>
<tr>
<td>오퍼레이션 유형</td>
<td>조회(목록)</td>
<td>오퍼레이션명(영문)</td>
<td colspan="2"><strong>getOpengResultListInfoServcPreparPcDetail</strong></td>
</tr>
<tr>
<td>오퍼레이션 설명</td>
<td colspan="4">검색조건을 등록일시, 입찰공고번호로 용역에 대한 나라장터 개찰결과 예비가격상세 목록(입찰공고번호, 입찰공고명, 예정가격, 기초금액, 총예가건수, 복수예가순번, 기초예정가격, 추첨여부, 추첨횟수, 실개찰일시, 기초금액기준상위건수, 복수예비가격작성일시, 입력일시)을 조회</td>
</tr>
<tr>
<td>Call Back URL</td>
<td colspan="4" style="text-align: left;">N/A</td>
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
<col style="width: 20%" />
<col style="width: 12%" />
<col style="width: 11%" />
<col style="width: 13%" />
<col style="width: 22%" />
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
<td>4</td>
<td>1</td>
<td>10</td>
<td>한 페이지 결과 수</td>
</tr>
<tr>
<td>pageNo</td>
<td>페이지 번호</td>
<td>4</td>
<td>1</td>
<td>1</td>
<td>페이지 번호</td>
</tr>
<tr>
<td style="text-align: left;">ServiceKey</td>
<td style="text-align: left;">서비스키</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">공공데이터포털에서 받은 인증키</td>
<td style="text-align: left;">공공데이터포털에서 받은 인증키</td>
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
<td>조회구분</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">검색하고자하는 조회구분<br />
1.입력일시, 2.입찰공고번호</td>
</tr>
<tr>
<td>inqryBgnDt</td>
<td>조회시작일시</td>
<td>12</td>
<td style="text-align: left;">0</td>
<td>202507010000</td>
<td>검색하고자하는 시작일시<br />
'YYYYMMDDHHMM'<br />
조회구분이 1일 경우 필수</td>
</tr>
<tr>
<td>inqryEndDt</td>
<td>조회종료일시</td>
<td>12</td>
<td style="text-align: left;">0</td>
<td>202507012359</td>
<td>검색하고자하는 종료일시<br />
'YYYYMMDDHHMM'<br />
조회구분이 1일 경우 필수</td>
</tr>
<tr>
<td>bidNtceNo</td>
<td>입찰공고번호</td>
<td>11</td>
<td style="text-align: left;">0</td>
<td>R25BK00811340</td>
<td><p>검색하고자하는 입찰공고번호</p>
<p>조회구분이 2일 경우 필수</p></td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 응답 메시지 명세

<table style="width:100%;">
<colgroup>
<col style="width: 21%" />
<col style="width: 21%" />
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 13%" />
<col style="width: 20%" />
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
<td style="text-align: left;">데이터 총 개수</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNo</td>
<td style="text-align: left;">입찰공고번호</td>
<td style="text-align: left;">11</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">R25BK00811340</td>
<td style="text-align: left;">입찰공고 관리번호이며 조달청나라장터 공고건의 형식은 년도(4)+월(2)+순번(5)이며 자체전자조달시스템 보유기관은 각 기관별 형식 별도 사용<br />
*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성<br />
- 단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</td>
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
<td style="text-align: left;">동일한 입찰공고번호에 대한 집행일련번호</td>
</tr>
<tr>
<td style="text-align: left;">rbidNo</td>
<td style="text-align: left;">재입찰번호</td>
<td style="text-align: left;">3</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">000</td>
<td style="text-align: left;">재입찰번호</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNm</td>
<td style="text-align: left;">입찰공고명</td>
<td style="text-align: left;">1000</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">천안시 성남면 및 수신면 기초생활거점조성사업 기본계획수립 용역</td>
<td style="text-align: left;">공사명 또는 사업명이라고도 하며 입찰공고 내용을 요약한 이름</td>
</tr>
<tr>
<td style="text-align: left;">plnprc</td>
<td style="text-align: left;">예정가격</td>
<td style="text-align: left;">21</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">404158750</td>
<td style="text-align: left;">예정가격은 계약담당공무원이 구매를 위한 경쟁입찰 또는 수의시담을 하기 전에 당해 계약 목적물의 특성 및 계약 여건 등을 고려하여 예산의 범위 내에서 경제적으로 구매가 가능하고 구매가격으로서 적정하다고 판단하여 정한 가격을 말하며 동 가격은 입찰 또는 시담에 의한 낙찰자 선정의 기준이고 계약체결에 대한 최고 상한 금액을 의미함. (원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">bssamt</td>
<td style="text-align: left;">기초금액</td>
<td style="text-align: left;">21</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">404282000</td>
<td style="text-align: left;">예정가격 작성 과정에서 거래실례가격, 원가계산가격 등에 의하여 조사한 가격이나 설계가격에 대하여 계약담당공무원이 그 적정여부를 검토조정한 가격(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">totRsrvtnPrceNum</td>
<td style="text-align: left;">총예가건수</td>
<td style="text-align: left;">2</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">15</td>
<td style="text-align: left;">총예가건수</td>
</tr>
<tr>
<td style="text-align: left;">compnoRsrvtnPrceSno</td>
<td style="text-align: left;">복수예가순번</td>
<td style="text-align: left;">6</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">복수예가순번</td>
</tr>
<tr>
<td style="text-align: left;">bsisPlnprc</td>
<td style="text-align: left;">기초예정가격</td>
<td style="text-align: left;">21</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">405745600</td>
<td style="text-align: left;">기초예정가격(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">drwtYn</td>
<td style="text-align: left;">추첨여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">Y</td>
<td style="text-align: left;">추첨여부(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">drwtNum</td>
<td style="text-align: left;">추첨횟수</td>
<td style="text-align: left;">22</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">추첨횟수</td>
</tr>
<tr>
<td style="text-align: left;">bidwinrSlctnAplBssCntnts</td>
<td style="text-align: left;">최종낙찰자선정적용기준내용</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">조달청</td>
<td style="text-align: left;">낙찰자선정적용기준내용</td>
</tr>
<tr>
<td style="text-align: left;">rlOpengDt</td>
<td style="text-align: left;">실개찰일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-01 13:54:13</td>
<td style="text-align: left;">실제 개찰일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">bssamtBssUpNum</td>
<td style="text-align: left;">기초금액기준상위건수</td>
<td style="text-align: left;">2</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">8</td>
<td style="text-align: left;">기초금액기준상위건수</td>
</tr>
<tr>
<td style="text-align: left;">compnoRsrvtnPrceMkngDt</td>
<td style="text-align: left;">복수예비가격작성일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-01 13:53:36</td>
<td style="text-align: left;">복수예비가격작성시각”YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">inptDt</td>
<td>입력일시</td>
<td style="text-align: left;">19</td>
<td>1</td>
<td>2025-07-01 13:54:13</td>
<td style="text-align: left;">입력일시 "YYYY-MM-DD HH:MM:SS"</td>
</tr>
<tr>
<td style="text-align: left;">PrearngPrcePurcnstcst</td>
<td>예정가격순공사비</td>
<td style="text-align: left;">22</td>
<td>0</td>
<td>0</td>
<td style="text-align: left;">예정가격 중 순공사 원가(재료비,노무비,경비,및 이에 대한 부가가치세 합산금액)</td>
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
<td>REST(URI)</td>
</tr>
<tr>
<td style="text-align: left;">http://apis.data.go.kr/1230000/as/ScsbidInfoService/getOpengResultListInfoServcPreparPcDetail?inqryDiv=2&amp;bidNtceNo=R25BK00811340&amp;bidNtceOrd=000&amp;pageNo=1&amp;numOfRows=15&amp;ServiceKey=인증키</td>
</tr>
<tr>
<td>응답 메시지</td>
</tr>
<tr>
<td><p>&lt;response&gt;</p>
<p>&lt;header&gt;</p>
<p>&lt;resultCode&gt;00&lt;/resultCode&gt;</p>
<p>&lt;resultMsg&gt;정상&lt;/resultMsg&gt;</p>
<p>&lt;/header&gt;</p>
<p>&lt;body&gt;</p>
<p>&lt;items&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00811340&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;0&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;bidNtceNm&gt;천안시 성남면 및 수신면 기초생활거점조성사업 기본계획수립 용역&lt;/bidNtceNm&gt;</p>
<p>&lt;plnprc&gt;404158750&lt;/plnprc&gt;</p>
<p>&lt;bssamt&gt;404282000&lt;/bssamt&gt;</p>
<p>&lt;totRsrvtnPrceNum&gt;15&lt;/totRsrvtnPrceNum&gt;</p>
<p>&lt;compnoRsrvtnPrceSno&gt;1&lt;/compnoRsrvtnPrceSno&gt;</p>
<p>&lt;bsisPlnprc&gt;409780300&lt;/bsisPlnprc&gt;</p>
<p>&lt;drwtYn&gt;N&lt;/drwtYn&gt;</p>
<p>&lt;drwtNum&gt;0&lt;/drwtNum&gt;</p>
<p>&lt;bidwinrSlctnAplBssCntnts&gt;조달청&lt;/bidwinrSlctnAplBssCntnts&gt;</p>
<p>&lt;rlOpengDt&gt;2025-07-01 13:54:13&lt;/rlOpengDt&gt;</p>
<p>&lt;bssamtBssUpNum&gt;8&lt;/bssamtBssUpNum&gt;</p>
<p>&lt;compnoRsrvtnPrceMkngDt&gt;2025-07-01 13:53:36&lt;/compnoRsrvtnPrceMkngDt&gt;</p>
<p>&lt;inptDt&gt;2025-07-01 13:54:13&lt;/inptDt&gt;</p>
<p>&lt;PrearngPrcePurcnstcst&gt;&lt;/PrearngPrcePurcnstcst&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00811340&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;0&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;bidNtceNm&gt;천안시 성남면 및 수신면 기초생활거점조성사업 기본계획수립 용역&lt;/bidNtceNm&gt;</p>
<p>&lt;plnprc&gt;404158750&lt;/plnprc&gt;</p>
<p>&lt;bssamt&gt;404282000&lt;/bssamt&gt;</p>
<p>&lt;totRsrvtnPrceNum&gt;15&lt;/totRsrvtnPrceNum&gt;</p>
<p>&lt;compnoRsrvtnPrceSno&gt;2&lt;/compnoRsrvtnPrceSno&gt;</p>
<p>&lt;bsisPlnprc&gt;408587700&lt;/bsisPlnprc&gt;</p>
<p>&lt;drwtYn&gt;N&lt;/drwtYn&gt;</p>
<p>&lt;drwtNum&gt;0&lt;/drwtNum&gt;</p>
<p>&lt;bidwinrSlctnAplBssCntnts&gt;조달청&lt;/bidwinrSlctnAplBssCntnts&gt;</p>
<p>&lt;rlOpengDt&gt;2025-07-01 13:54:13&lt;/rlOpengDt&gt;</p>
<p>&lt;bssamtBssUpNum&gt;8&lt;/bssamtBssUpNum&gt;</p>
<p>&lt;compnoRsrvtnPrceMkngDt&gt;2025-07-01 13:53:36&lt;/compnoRsrvtnPrceMkngDt&gt;</p>
<p>&lt;inptDt&gt;2025-07-01 13:54:13&lt;/inptDt&gt;</p>
<p>&lt;PrearngPrcePurcnstcst&gt;&lt;/PrearngPrcePurcnstcst&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00811340&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;0&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;bidNtceNm&gt;천안시 성남면 및 수신면 기초생활거점조성사업 기본계획수립 용역&lt;/bidNtceNm&gt;</p>
<p>&lt;plnprc&gt;404158750&lt;/plnprc&gt;</p>
<p>&lt;bssamt&gt;404282000&lt;/bssamt&gt;</p>
<p>&lt;totRsrvtnPrceNum&gt;15&lt;/totRsrvtnPrceNum&gt;</p>
<p>&lt;compnoRsrvtnPrceSno&gt;3&lt;/compnoRsrvtnPrceSno&gt;</p>
<p>&lt;bsisPlnprc&gt;400930600&lt;/bsisPlnprc&gt;</p>
<p>&lt;drwtYn&gt;N&lt;/drwtYn&gt;</p>
<p>&lt;drwtNum&gt;0&lt;/drwtNum&gt;</p>
<p>&lt;bidwinrSlctnAplBssCntnts&gt;조달청&lt;/bidwinrSlctnAplBssCntnts&gt;</p>
<p>&lt;rlOpengDt&gt;2025-07-01 13:54:13&lt;/rlOpengDt&gt;</p>
<p>&lt;bssamtBssUpNum&gt;8&lt;/bssamtBssUpNum&gt;</p>
<p>&lt;compnoRsrvtnPrceMkngDt&gt;2025-07-01 13:53:36&lt;/compnoRsrvtnPrceMkngDt&gt;</p>
<p>&lt;inptDt&gt;2025-07-01 13:54:13&lt;/inptDt&gt;</p>
<p>&lt;PrearngPrcePurcnstcst&gt;&lt;/PrearngPrcePurcnstcst&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00811340&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;0&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;bidNtceNm&gt;천안시 성남면 및 수신면 기초생활거점조성사업 기본계획수립 용역&lt;/bidNtceNm&gt;</p>
<p>&lt;plnprc&gt;404158750&lt;/plnprc&gt;</p>
<p>&lt;bssamt&gt;404282000&lt;/bssamt&gt;</p>
<p>&lt;totRsrvtnPrceNum&gt;15&lt;/totRsrvtnPrceNum&gt;</p>
<p>&lt;compnoRsrvtnPrceSno&gt;4&lt;/compnoRsrvtnPrceSno&gt;</p>
<p>&lt;bsisPlnprc&gt;405745600&lt;/bsisPlnprc&gt;</p>
<p>&lt;drwtYn&gt;Y&lt;/drwtYn&gt;</p>
<p>&lt;drwtNum&gt;1&lt;/drwtNum&gt;</p>
<p>&lt;bidwinrSlctnAplBssCntnts&gt;조달청&lt;/bidwinrSlctnAplBssCntnts&gt;</p>
<p>&lt;rlOpengDt&gt;2025-07-01 13:54:13&lt;/rlOpengDt&gt;</p>
<p>&lt;bssamtBssUpNum&gt;8&lt;/bssamtBssUpNum&gt;</p>
<p>&lt;compnoRsrvtnPrceMkngDt&gt;2025-07-01 13:53:36&lt;/compnoRsrvtnPrceMkngDt&gt;</p>
<p>&lt;inptDt&gt;2025-07-01 13:54:13&lt;/inptDt&gt;</p>
<p>&lt;PrearngPrcePurcnstcst&gt;&lt;/PrearngPrcePurcnstcst&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00811340&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;0&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;bidNtceNm&gt;천안시 성남면 및 수신면 기초생활거점조성사업 기본계획수립 용역&lt;/bidNtceNm&gt;</p>
<p>&lt;plnprc&gt;404158750&lt;/plnprc&gt;</p>
<p>&lt;bssamt&gt;404282000&lt;/bssamt&gt;</p>
<p>&lt;totRsrvtnPrceNum&gt;15&lt;/totRsrvtnPrceNum&gt;</p>
<p>&lt;compnoRsrvtnPrceSno&gt;5&lt;/compnoRsrvtnPrceSno&gt;</p>
<p>&lt;bsisPlnprc&gt;407184800&lt;/bsisPlnprc&gt;</p>
<p>&lt;drwtYn&gt;N&lt;/drwtYn&gt;</p>
<p>&lt;drwtNum&gt;0&lt;/drwtNum&gt;</p>
<p>&lt;bidwinrSlctnAplBssCntnts&gt;조달청&lt;/bidwinrSlctnAplBssCntnts&gt;</p>
<p>&lt;rlOpengDt&gt;2025-07-01 13:54:13&lt;/rlOpengDt&gt;</p>
<p>&lt;bssamtBssUpNum&gt;8&lt;/bssamtBssUpNum&gt;</p>
<p>&lt;compnoRsrvtnPrceMkngDt&gt;2025-07-01 13:53:36&lt;/compnoRsrvtnPrceMkngDt&gt;</p>
<p>&lt;inptDt&gt;2025-07-01 13:54:13&lt;/inptDt&gt;</p>
<p>&lt;PrearngPrcePurcnstcst&gt;&lt;/PrearngPrcePurcnstcst&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00811340&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;0&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;bidNtceNm&gt;천안시 성남면 및 수신면 기초생활거점조성사업 기본계획수립 용역&lt;/bidNtceNm&gt;</p>
<p>&lt;plnprc&gt;404158750&lt;/plnprc&gt;</p>
<p>&lt;bssamt&gt;404282000&lt;/bssamt&gt;</p>
<p>&lt;totRsrvtnPrceNum&gt;15&lt;/totRsrvtnPrceNum&gt;</p>
<p>&lt;compnoRsrvtnPrceSno&gt;6&lt;/compnoRsrvtnPrceSno&gt;</p>
<p>&lt;bsisPlnprc&gt;402782200&lt;/bsisPlnprc&gt;</p>
<p>&lt;drwtYn&gt;Y&lt;/drwtYn&gt;</p>
<p>&lt;drwtNum&gt;1&lt;/drwtNum&gt;</p>
<p>&lt;bidwinrSlctnAplBssCntnts&gt;조달청&lt;/bidwinrSlctnAplBssCntnts&gt;</p>
<p>&lt;rlOpengDt&gt;2025-07-01 13:54:13&lt;/rlOpengDt&gt;</p>
<p>&lt;bssamtBssUpNum&gt;8&lt;/bssamtBssUpNum&gt;</p>
<p>&lt;compnoRsrvtnPrceMkngDt&gt;2025-07-01 13:53:36&lt;/compnoRsrvtnPrceMkngDt&gt;</p>
<p>&lt;inptDt&gt;2025-07-01 13:54:13&lt;/inptDt&gt;</p>
<p>&lt;PrearngPrcePurcnstcst&gt;&lt;/PrearngPrcePurcnstcst&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00811340&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;0&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;bidNtceNm&gt;천안시 성남면 및 수신면 기초생활거점조성사업 기본계획수립 용역&lt;/bidNtceNm&gt;</p>
<p>&lt;plnprc&gt;404158750&lt;/plnprc&gt;</p>
<p>&lt;bssamt&gt;404282000&lt;/bssamt&gt;</p>
<p>&lt;totRsrvtnPrceNum&gt;15&lt;/totRsrvtnPrceNum&gt;</p>
<p>&lt;compnoRsrvtnPrceSno&gt;7&lt;/compnoRsrvtnPrceSno&gt;</p>
<p>&lt;bsisPlnprc&gt;399394300&lt;/bsisPlnprc&gt;</p>
<p>&lt;drwtYn&gt;N&lt;/drwtYn&gt;</p>
<p>&lt;drwtNum&gt;0&lt;/drwtNum&gt;</p>
<p>&lt;bidwinrSlctnAplBssCntnts&gt;조달청&lt;/bidwinrSlctnAplBssCntnts&gt;</p>
<p>&lt;rlOpengDt&gt;2025-07-01 13:54:13&lt;/rlOpengDt&gt;</p>
<p>&lt;bssamtBssUpNum&gt;8&lt;/bssamtBssUpNum&gt;</p>
<p>&lt;compnoRsrvtnPrceMkngDt&gt;2025-07-01 13:53:36&lt;/compnoRsrvtnPrceMkngDt&gt;</p>
<p>&lt;inptDt&gt;2025-07-01 13:54:13&lt;/inptDt&gt;</p>
<p>&lt;PrearngPrcePurcnstcst&gt;&lt;/PrearngPrcePurcnstcst&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00811340&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;0&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;bidNtceNm&gt;천안시 성남면 및 수신면 기초생활거점조성사업 기본계획수립 용역&lt;/bidNtceNm&gt;</p>
<p>&lt;plnprc&gt;404158750&lt;/plnprc&gt;</p>
<p>&lt;bssamt&gt;404282000&lt;/bssamt&gt;</p>
<p>&lt;totRsrvtnPrceNum&gt;15&lt;/totRsrvtnPrceNum&gt;</p>
<p>&lt;compnoRsrvtnPrceSno&gt;8&lt;/compnoRsrvtnPrceSno&gt;</p>
<p>&lt;bsisPlnprc&gt;397482000&lt;/bsisPlnprc&gt;</p>
<p>&lt;drwtYn&gt;Y&lt;/drwtYn&gt;</p>
<p>&lt;drwtNum&gt;3&lt;/drwtNum&gt;</p>
<p>&lt;bidwinrSlctnAplBssCntnts&gt;조달청&lt;/bidwinrSlctnAplBssCntnts&gt;</p>
<p>&lt;rlOpengDt&gt;2025-07-01 13:54:13&lt;/rlOpengDt&gt;</p>
<p>&lt;bssamtBssUpNum&gt;8&lt;/bssamtBssUpNum&gt;</p>
<p>&lt;compnoRsrvtnPrceMkngDt&gt;2025-07-01 13:53:36&lt;/compnoRsrvtnPrceMkngDt&gt;</p>
<p>&lt;inptDt&gt;2025-07-01 13:54:13&lt;/inptDt&gt;</p>
<p>&lt;PrearngPrcePurcnstcst&gt;&lt;/PrearngPrcePurcnstcst&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00811340&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;0&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;bidNtceNm&gt;천안시 성남면 및 수신면 기초생활거점조성사업 기본계획수립 용역&lt;/bidNtceNm&gt;</p>
<p>&lt;plnprc&gt;404158750&lt;/plnprc&gt;</p>
<p>&lt;bssamt&gt;404282000&lt;/bssamt&gt;</p>
<p>&lt;totRsrvtnPrceNum&gt;15&lt;/totRsrvtnPrceNum&gt;</p>
<p>&lt;compnoRsrvtnPrceSno&gt;9&lt;/compnoRsrvtnPrceSno&gt;</p>
<p>&lt;bsisPlnprc&gt;406659200&lt;/bsisPlnprc&gt;</p>
<p>&lt;drwtYn&gt;N&lt;/drwtYn&gt;</p>
<p>&lt;drwtNum&gt;0&lt;/drwtNum&gt;</p>
<p>&lt;bidwinrSlctnAplBssCntnts&gt;조달청&lt;/bidwinrSlctnAplBssCntnts&gt;</p>
<p>&lt;rlOpengDt&gt;2025-07-01 13:54:13&lt;/rlOpengDt&gt;</p>
<p>&lt;bssamtBssUpNum&gt;8&lt;/bssamtBssUpNum&gt;</p>
<p>&lt;compnoRsrvtnPrceMkngDt&gt;2025-07-01 13:53:36&lt;/compnoRsrvtnPrceMkngDt&gt;</p>
<p>&lt;inptDt&gt;2025-07-01 13:54:13&lt;/inptDt&gt;</p>
<p>&lt;PrearngPrcePurcnstcst&gt;&lt;/PrearngPrcePurcnstcst&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00811340&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;0&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;bidNtceNm&gt;천안시 성남면 및 수신면 기초생활거점조성사업 기본계획수립 용역&lt;/bidNtceNm&gt;</p>
<p>&lt;plnprc&gt;404158750&lt;/plnprc&gt;</p>
<p>&lt;bssamt&gt;404282000&lt;/bssamt&gt;</p>
<p>&lt;totRsrvtnPrceNum&gt;15&lt;/totRsrvtnPrceNum&gt;</p>
<p>&lt;compnoRsrvtnPrceSno&gt;10&lt;/compnoRsrvtnPrceSno&gt;</p>
<p>&lt;bsisPlnprc&gt;401941300&lt;/bsisPlnprc&gt;</p>
<p>&lt;drwtYn&gt;N&lt;/drwtYn&gt;</p>
<p>&lt;drwtNum&gt;1&lt;/drwtNum&gt;</p>
<p>&lt;bidwinrSlctnAplBssCntnts&gt;조달청&lt;/bidwinrSlctnAplBssCntnts&gt;</p>
<p>&lt;rlOpengDt&gt;2025-07-01 13:54:13&lt;/rlOpengDt&gt;</p>
<p>&lt;bssamtBssUpNum&gt;8&lt;/bssamtBssUpNum&gt;</p>
<p>&lt;compnoRsrvtnPrceMkngDt&gt;2025-07-01 13:53:36&lt;/compnoRsrvtnPrceMkngDt&gt;</p>
<p>&lt;inptDt&gt;2025-07-01 13:54:13&lt;/inptDt&gt;</p>
<p>&lt;PrearngPrcePurcnstcst&gt;&lt;/PrearngPrcePurcnstcst&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00811340&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;0&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;bidNtceNm&gt;천안시 성남면 및 수신면 기초생활거점조성사업 기본계획수립 용역&lt;/bidNtceNm&gt;</p>
<p>&lt;plnprc&gt;404158750&lt;/plnprc&gt;</p>
<p>&lt;bssamt&gt;404282000&lt;/bssamt&gt;</p>
<p>&lt;totRsrvtnPrceNum&gt;15&lt;/totRsrvtnPrceNum&gt;</p>
<p>&lt;compnoRsrvtnPrceSno&gt;11&lt;/compnoRsrvtnPrceSno&gt;</p>
<p>&lt;bsisPlnprc&gt;396928200&lt;/bsisPlnprc&gt;</p>
<p>&lt;drwtYn&gt;N&lt;/drwtYn&gt;</p>
<p>&lt;drwtNum&gt;0&lt;/drwtNum&gt;</p>
<p>&lt;bidwinrSlctnAplBssCntnts&gt;조달청&lt;/bidwinrSlctnAplBssCntnts&gt;</p>
<p>&lt;rlOpengDt&gt;2025-07-01 13:54:13&lt;/rlOpengDt&gt;</p>
<p>&lt;bssamtBssUpNum&gt;8&lt;/bssamtBssUpNum&gt;</p>
<p>&lt;compnoRsrvtnPrceMkngDt&gt;2025-07-01 13:53:36&lt;/compnoRsrvtnPrceMkngDt&gt;</p>
<p>&lt;inptDt&gt;2025-07-01 13:54:13&lt;/inptDt&gt;</p>
<p>&lt;PrearngPrcePurcnstcst&gt;&lt;/PrearngPrcePurcnstcst&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00811340&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;0&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;bidNtceNm&gt;천안시 성남면 및 수신면 기초생활거점조성사업 기본계획수립 용역&lt;/bidNtceNm&gt;</p>
<p>&lt;plnprc&gt;404158750&lt;/plnprc&gt;</p>
<p>&lt;bssamt&gt;404282000&lt;/bssamt&gt;</p>
<p>&lt;totRsrvtnPrceNum&gt;15&lt;/totRsrvtnPrceNum&gt;</p>
<p>&lt;compnoRsrvtnPrceSno&gt;12&lt;/compnoRsrvtnPrceSno&gt;</p>
<p>&lt;bsisPlnprc&gt;410625200&lt;/bsisPlnprc&gt;</p>
<p>&lt;drwtYn&gt;Y&lt;/drwtYn&gt;</p>
<p>&lt;drwtNum&gt;2&lt;/drwtNum&gt;</p>
<p>&lt;bidwinrSlctnAplBssCntnts&gt;조달청&lt;/bidwinrSlctnAplBssCntnts&gt;</p>
<p>&lt;rlOpengDt&gt;2025-07-01 13:54:13&lt;/rlOpengDt&gt;</p>
<p>&lt;bssamtBssUpNum&gt;8&lt;/bssamtBssUpNum&gt;</p>
<p>&lt;compnoRsrvtnPrceMkngDt&gt;2025-07-01 13:53:36&lt;/compnoRsrvtnPrceMkngDt&gt;</p>
<p>&lt;inptDt&gt;2025-07-01 13:54:13&lt;/inptDt&gt;</p>
<p>&lt;PrearngPrcePurcnstcst&gt;&lt;/PrearngPrcePurcnstcst&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00811340&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;0&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;bidNtceNm&gt;천안시 성남면 및 수신면 기초생활거점조성사업 기본계획수립 용역&lt;/bidNtceNm&gt;</p>
<p>&lt;plnprc&gt;404158750&lt;/plnprc&gt;</p>
<p>&lt;bssamt&gt;404282000&lt;/bssamt&gt;</p>
<p>&lt;totRsrvtnPrceNum&gt;15&lt;/totRsrvtnPrceNum&gt;</p>
<p>&lt;compnoRsrvtnPrceSno&gt;13&lt;/compnoRsrvtnPrceSno&gt;</p>
<p>&lt;bsisPlnprc&gt;399774300&lt;/bsisPlnprc&gt;</p>
<p>&lt;drwtYn&gt;N&lt;/drwtYn&gt;</p>
<p>&lt;drwtNum&gt;1&lt;/drwtNum&gt;</p>
<p>&lt;bidwinrSlctnAplBssCntnts&gt;조달청&lt;/bidwinrSlctnAplBssCntnts&gt;</p>
<p>&lt;rlOpengDt&gt;2025-07-01 13:54:13&lt;/rlOpengDt&gt;</p>
<p>&lt;bssamtBssUpNum&gt;8&lt;/bssamtBssUpNum&gt;</p>
<p>&lt;compnoRsrvtnPrceMkngDt&gt;2025-07-01 13:53:36&lt;/compnoRsrvtnPrceMkngDt&gt;</p>
<p>&lt;inptDt&gt;2025-07-01 13:54:13&lt;/inptDt&gt;</p>
<p>&lt;PrearngPrcePurcnstcst&gt;&lt;/PrearngPrcePurcnstcst&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00811340&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;0&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;bidNtceNm&gt;천안시 성남면 및 수신면 기초생활거점조성사업 기본계획수립 용역&lt;/bidNtceNm&gt;</p>
<p>&lt;plnprc&gt;404158750&lt;/plnprc&gt;</p>
<p>&lt;bssamt&gt;404282000&lt;/bssamt&gt;</p>
<p>&lt;totRsrvtnPrceNum&gt;15&lt;/totRsrvtnPrceNum&gt;</p>
<p>&lt;compnoRsrvtnPrceSno&gt;14&lt;/compnoRsrvtnPrceSno&gt;</p>
<p>&lt;bsisPlnprc&gt;411644000&lt;/bsisPlnprc&gt;</p>
<p>&lt;drwtYn&gt;N&lt;/drwtYn&gt;</p>
<p>&lt;drwtNum&gt;0&lt;/drwtNum&gt;</p>
<p>&lt;bidwinrSlctnAplBssCntnts&gt;조달청&lt;/bidwinrSlctnAplBssCntnts&gt;</p>
<p>&lt;rlOpengDt&gt;2025-07-01 13:54:13&lt;/rlOpengDt&gt;</p>
<p>&lt;bssamtBssUpNum&gt;8&lt;/bssamtBssUpNum&gt;</p>
<p>&lt;compnoRsrvtnPrceMkngDt&gt;2025-07-01 13:53:36&lt;/compnoRsrvtnPrceMkngDt&gt;</p>
<p>&lt;inptDt&gt;2025-07-01 13:54:13&lt;/inptDt&gt;</p>
<p>&lt;PrearngPrcePurcnstcst&gt;&lt;/PrearngPrcePurcnstcst&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00811340&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;0&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;bidNtceNm&gt;천안시 성남면 및 수신면 기초생활거점조성사업 기본계획수립 용역&lt;/bidNtceNm&gt;</p>
<p>&lt;plnprc&gt;404158750&lt;/plnprc&gt;</p>
<p>&lt;bssamt&gt;404282000&lt;/bssamt&gt;</p>
<p>&lt;totRsrvtnPrceNum&gt;15&lt;/totRsrvtnPrceNum&gt;</p>
<p>&lt;compnoRsrvtnPrceSno&gt;15&lt;/compnoRsrvtnPrceSno&gt;</p>
<p>&lt;bsisPlnprc&gt;404419500&lt;/bsisPlnprc&gt;</p>
<p>&lt;drwtYn&gt;N&lt;/drwtYn&gt;</p>
<p>&lt;drwtNum&gt;1&lt;/drwtNum&gt;</p>
<p>&lt;bidwinrSlctnAplBssCntnts&gt;조달청&lt;/bidwinrSlctnAplBssCntnts&gt;</p>
<p>&lt;rlOpengDt&gt;2025-07-01 13:54:13&lt;/rlOpengDt&gt;</p>
<p>&lt;bssamtBssUpNum&gt;8&lt;/bssamtBssUpNum&gt;</p>
<p>&lt;compnoRsrvtnPrceMkngDt&gt;2025-07-01 13:53:36&lt;/compnoRsrvtnPrceMkngDt&gt;</p>
<p>&lt;inptDt&gt;2025-07-01 13:54:13&lt;/inptDt&gt;</p>
<p>&lt;PrearngPrcePurcnstcst&gt;&lt;/PrearngPrcePurcnstcst&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;/items&gt;</p>
<p>&lt;numOfRows&gt;999&lt;/numOfRows&gt;</p>
<p>&lt;pageNo&gt;1&lt;/pageNo&gt;</p>
<p>&lt;totalCount&gt;15&lt;/totalCount&gt;</p>
<p>&lt;/body&gt;</p>
<p>&lt;/response&gt;</p></td>
</tr>
</tbody>
</table>

#### \[개찰결과 외자 예비가격상세 목록 조회\] 오퍼레이션 명세

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
<td>12</td>
<td>오퍼레이션명(국문)</td>
<td colspan="2">개찰결과 외자 예비가격상세 목록 조회</td>
</tr>
<tr>
<td>오퍼레이션 유형</td>
<td>조회(목록)</td>
<td>오퍼레이션명(영문)</td>
<td colspan="2"><strong>getOpengResultListInfoFrgcptPreparPcDetail</strong></td>
</tr>
<tr>
<td>오퍼레이션 설명</td>
<td colspan="4">검색조건을 등록일시, 입찰공고번호로 외자에 대한 나라장터 개찰결과 외자 예비가격상세 목록(입찰공고번호, 입찰공고명, 예정가격, 기초금액, 총예가건수, 복수예가순번, 기초예정가격, 추첨여부, 추첨횟수, 실개찰일시, 기초금액기준상위건수, 복수예비가격작성일시, 입력일시)을 조회</td>
</tr>
<tr>
<td>Call Back URL</td>
<td colspan="4" style="text-align: left;">N/A</td>
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
<col style="width: 11%" />
<col style="width: 12%" />
<col style="width: 22%" />
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
<td>4</td>
<td>1</td>
<td>10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td>pageNo</td>
<td>페이지 번호</td>
<td>4</td>
<td>1</td>
<td>1</td>
<td style="text-align: left;">페이지 번호</td>
</tr>
<tr>
<td style="text-align: left;">ServiceKey</td>
<td style="text-align: left;">서비스키</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">공공데이터포털에서 받은 인증키</td>
<td style="text-align: left;">공공데이터포털에서 받은 인증키</td>
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
<td>조회구분</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">검색하고자하는 조회구분<br />
1.입력일시, 2.입찰공고번호</td>
</tr>
<tr>
<td>inqryBgnDt</td>
<td>조회시작일시</td>
<td>12</td>
<td style="text-align: left;">0</td>
<td>202507010000</td>
<td>검색하고자하는 시작일시<br />
'YYYYMMDDHHMM'<br />
조회구분이 1일 경우 필수</td>
</tr>
<tr>
<td>inqryEndDt</td>
<td>조회종료일시</td>
<td>12</td>
<td style="text-align: left;">0</td>
<td>202507012359</td>
<td>검색하고자하는 종료일시<br />
'YYYYMMDDHHMM'<br />
조회구분이 1일 경우 필수</td>
</tr>
<tr>
<td>bidNtceNo</td>
<td>입찰공고번호</td>
<td>11</td>
<td style="text-align: left;">0</td>
<td>R25BK00883422</td>
<td><p>검색하고자하는 입찰공고번호</p>
<p>조회구분이 2일 경우 필수</p></td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 응답 메시지 명세

<table style="width:100%;">
<colgroup>
<col style="width: 21%" />
<col style="width: 21%" />
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 13%" />
<col style="width: 20%" />
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
<td style="text-align: left;">데이터 총 개수</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNo</td>
<td style="text-align: left;">입찰공고번호</td>
<td style="text-align: left;">11</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">R25BK00883422</td>
<td style="text-align: left;">입찰공고 관리번호이며 조달청나라장터 공고건의 형식은 년도(4)+월(2)+순번(5)이며 자체전자조달시스템 보유기관은 각 기관별 형식 별도 사용<br />
*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성<br />
- 단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</td>
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
<td style="text-align: left;">동일한 입찰공고번호에 대한 집행일련번호</td>
</tr>
<tr>
<td style="text-align: left;">rbidNo</td>
<td style="text-align: left;">재입찰번호</td>
<td style="text-align: left;">3</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">000</td>
<td style="text-align: left;">재입찰번호</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNm</td>
<td style="text-align: left;">입찰공고명</td>
<td style="text-align: left;">1000</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">호흡용 고압공기압축기 고정형</td>
<td style="text-align: left;">공사명 또는 사업명이라고도 하며 입찰공고 내용을 요약한 이름</td>
</tr>
<tr>
<td style="text-align: left;">plnprc</td>
<td style="text-align: left;">예정가격</td>
<td style="text-align: left;">21</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">예정가격은 계약담당공무원이 구매를 위한 경쟁입찰 또는 수의시담을 하기 전에 당해 계약 목적물의 특성 및 계약 여건 등을 고려하여 예산의 범위 내에서 경제적으로 구매가 가능하고 구매가격으로서 적정하다고 판단하여 정한 가격을 말하며 동 가격은 입찰 또는 시담에 의한 낙찰자 선정의 기준이고 계약체결에 대한 최고 상한 금액을 의미함. (원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">bssamt</td>
<td style="text-align: left;">기초금액</td>
<td style="text-align: left;">21</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">예정가격 작성 과정에서 거래실례가격, 원가계산가격 등에 의하여 조사한 가격이나 설계가격에 대하여 계약담당공무원이 그 적정여부를 검토조정한 가격(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">totRsrvtnPrceNum</td>
<td style="text-align: left;">총예가건수</td>
<td style="text-align: left;">2</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">총예가건수</td>
</tr>
<tr>
<td style="text-align: left;">compnoRsrvtnPrceSno</td>
<td style="text-align: left;">복수예가순번</td>
<td style="text-align: left;">6</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">복수예가순번</td>
</tr>
<tr>
<td style="text-align: left;">bsisPlnprc</td>
<td style="text-align: left;">기초예정가격</td>
<td style="text-align: left;">21</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">기초예정가격(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">drwtYn</td>
<td style="text-align: left;">추첨여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">추첨여부(Y/N)</td>
</tr>
<tr>
<td style="text-align: left;">drwtNum</td>
<td style="text-align: left;">추첨횟수</td>
<td style="text-align: left;">22</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">추첨횟수</td>
</tr>
<tr>
<td style="text-align: left;">bidwinrSlctnAplBssCntnts</td>
<td style="text-align: left;">최종낙찰자선정적용기준내용</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">조달청</td>
<td style="text-align: left;">낙찰자선정적용기준내용</td>
</tr>
<tr>
<td style="text-align: left;">rlOpengDt</td>
<td style="text-align: left;">실개찰일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-01 13:35:42</td>
<td style="text-align: left;">실제 개찰일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">bssamtBssUpNum</td>
<td style="text-align: left;">기초금액기준상위건수</td>
<td style="text-align: left;">2</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">기초금액기준상위건수</td>
</tr>
<tr>
<td style="text-align: left;">compnoRsrvtnPrceMkngDt</td>
<td style="text-align: left;">복수예비가격작성일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-01 13:35:42</td>
<td style="text-align: left;">복수예비가격작성시각”YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">inptDt</td>
<td>입력일시</td>
<td style="text-align: left;">19</td>
<td>1</td>
<td>2025-07-01 13:35:42</td>
<td style="text-align: left;">입력일시 "YYYY-MM-DD HH:MM:SS"</td>
</tr>
<tr>
<td style="text-align: left;">PrearngPrcePurcnstcst</td>
<td>예정가격순공사비</td>
<td style="text-align: left;">22</td>
<td>0</td>
<td>0</td>
<td style="text-align: left;">예정가격 중 순공사 원가(재료비,노무비,경비,및 이에 대한 부가가치세 합산금액)</td>
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
<td>REST(URI)</td>
</tr>
<tr>
<td style="text-align: left;">http://apis.data.go.kr/1230000/as/ScsbidInfoService/getOpengResultListInfoFrgcptPreparPcDetail?inqryDiv=2&amp; bidNtceNo= R25BK00883422&amp; bidNtceOrd=000&amp;pageNo=1&amp;numOfRows=10&amp;ServiceKey=인증키</td>
</tr>
<tr>
<td>응답 메시지</td>
</tr>
<tr>
<td><p>&lt;response&gt;</p>
<p>&lt;header&gt;</p>
<p>&lt;resultCode&gt;00&lt;/resultCode&gt;</p>
<p>&lt;resultMsg&gt;정상&lt;/resultMsg&gt;</p>
<p>&lt;/header&gt;</p>
<p>&lt;body&gt;</p>
<p>&lt;items&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00883422&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;1&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;bidNtceNm&gt;호흡용 고압공기압축기 고정형&lt;/bidNtceNm&gt;</p>
<p>&lt;plnprc&gt;&lt;/plnprc&gt;</p>
<p>&lt;bssamt&gt;&lt;/bssamt&gt;</p>
<p>&lt;totRsrvtnPrceNum&gt;&lt;/totRsrvtnPrceNum&gt;</p>
<p>&lt;compnoRsrvtnPrceSno&gt;&lt;/compnoRsrvtnPrceSno&gt;</p>
<p>&lt;bsisPlnprc&gt;&lt;/bsisPlnprc&gt;</p>
<p>&lt;drwtYn&gt;N&lt;/drwtYn&gt;</p>
<p>&lt;drwtNum&gt;0&lt;/drwtNum&gt;</p>
<p>&lt;bidwinrSlctnAplBssCntnts&gt;조달청&lt;/bidwinrSlctnAplBssCntnts&gt;</p>
<p>&lt;rlOpengDt&gt;2025-07-01 13:35:42&lt;/rlOpengDt&gt;</p>
<p>&lt;bssamtBssUpNum&gt;&lt;/bssamtBssUpNum&gt;</p>
<p>&lt;compnoRsrvtnPrceMkngDt&gt;&lt;/compnoRsrvtnPrceMkngDt&gt;</p>
<p>&lt;inptDt&gt;2025-07-01 13:35:42&lt;/inptDt&gt;</p>
<p>&lt;PrearngPrcePurcnstcst&gt;&lt;/PrearngPrcePurcnstcst&gt;</p>
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

#### \[개찰결과 개찰완료 목록 조회\] 오퍼레이션 명세

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
<td colspan="2">개찰결과 개찰완료 목록 조회</td>
</tr>
<tr>
<td>오퍼레이션 유형</td>
<td>조회(목록)</td>
<td>오퍼레이션명(영문)</td>
<td colspan="2"><strong>getOpengResultListInfoOpengCompt</strong></td>
</tr>
<tr>
<td>오퍼레이션 설명</td>
<td colspan="4">물품, 공사, 용역, 외자의 개찰완료된 건에 대하여 최종낙찰업체 및 투찰업체의 개찰순위 정보를 제공하며 검색조건을 입찰공고번호하여 나라장터 개찰결과 개찰완료 목록(개찰결과구분명, 입찰공고번호, 입찰공고차수, 입찰분류번호, 재입찰번호, 개찰순위, 최종낙찰업체사업자등록번호, 최종낙찰업체명, 최종낙찰업체대표자명, 투찰금액, 투찰룰, 비고, 공종별입찰금액URL), 추첨번호1, 추첨번호2, 투찰일시 등 개찰완료 조회</td>
</tr>
<tr>
<td>Call Back URL</td>
<td colspan="4" style="text-align: left;">N/A</td>
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

|  |  |  |  |  |  |
|----|----|----|----|----|----|
| 항목명(영문) | 항목명(국문) | 항목크기 | 항목구분 | 샘플데이터 | 항목설명 |
| numOfRows | 한 페이지 결과 수 | 4 | 1 | 10 | 한 페이지 결과 수 |
| pageNo | 페이지 번호 | 4 | 1 | 1 | 페이지 번호 |
| ServiceKey | 서비스키 | 400 | 1 | 공공데이터포털에서 받은 인증키 | 공공데이터포털에서 받은 인증키 |
| type | 타입 | 4 | 0 | json | 오픈API 리턴 타입을 JSON으로 받고 싶을 경우 'json' 으로 지정 |
| bidNtceNo | 입찰공고번호 | 11 | 1 | R25BK01027145 | 검색하고자하는 입찰공고번호 |
| bidNtceOrd | 입찰공고차수 | 2 | 0 | 002 | 검색하고자하는 입찰공고차수 |
| bidClsfcNo | 입찰분류번호 | 5 | 0 | 0 | 검색하고자하는 입찰분류번호 |
| rbidNo | 재입찰번호 | 3 | 0 | 000 | 검색하고자하는 재입찰번호 |

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 응답 메시지 명세

<table style="width:100%;">
<colgroup>
<col style="width: 21%" />
<col style="width: 21%" />
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 17%" />
<col style="width: 16%" />
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
<td>numOfRows</td>
<td>한 페이지 결과 수</td>
<td>4</td>
<td>1</td>
<td>10</td>
<td>한 페이지 결과 수</td>
</tr>
<tr>
<td>pageNo</td>
<td>페이지 번호</td>
<td>4</td>
<td>1</td>
<td>1</td>
<td>페이지 번호</td>
</tr>
<tr>
<td>totalCount</td>
<td>데이터 총 개수</td>
<td>4</td>
<td>1</td>
<td>6</td>
<td>데이터 총 개수</td>
</tr>
<tr>
<td style="text-align: left;">opengRsltDivNm</td>
<td>개찰결과구분명</td>
<td>30</td>
<td style="text-align: left;">1</td>
<td>개찰완료</td>
<td>해당 공고건에 대한 개찰결과를 구분하는 것으로 개찰이 완료되었는지, 유찰되었는지, 재입찰 할것인지 등을 구분하는 명으로 이 오퍼레이션은 개찰완료인 정보 조회</td>
</tr>
<tr>
<td>bidNtceNo</td>
<td>입찰공고번호</td>
<td>11</td>
<td style="text-align: left;">1</td>
<td>R25BK01027145</td>
<td style="text-align: left;">입찰공고 관리번호이며 조달청나라장터 공고건의 형식은 년도(4)+월(2)+순번(5)이며 자체전자조달시스템 보유기관은 각 기관별 형식 별도 사용<br />
*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성<br />
- 단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</td>
</tr>
<tr>
<td>bidNtceOrd</td>
<td>입찰공고차수</td>
<td>3</td>
<td style="text-align: left;">1</td>
<td>002</td>
<td>입찰공고차수는 해당 입찰공고에 대한 재공고 및 재입찰 등이 발생되었을 경우 증가되는 수</td>
</tr>
<tr>
<td>bidClsfcNo</td>
<td>입찰분류번호</td>
<td>5</td>
<td style="text-align: left;">1</td>
<td>0</td>
<td>동일한 입찰공고번호에 대한 집행일련번호</td>
</tr>
<tr>
<td>rbidNo</td>
<td>재입찰번호</td>
<td>3</td>
<td style="text-align: left;">1</td>
<td>000</td>
<td>재입찰번호</td>
</tr>
<tr>
<td>opengRank</td>
<td>개찰순위</td>
<td>7</td>
<td style="text-align: left;">0</td>
<td>1</td>
<td>개찰순위는 협상기술능력 평가점수와 입찰가격 평가점수의 합산하여 고득점 순에 따라 결정되는 순위로 협상에 의한 계약일 경우, 협상순위를 의미함</td>
</tr>
<tr>
<td>prcbdrBizno</td>
<td>투찰업체사업자등록번호</td>
<td>10</td>
<td style="text-align: left;">1</td>
<td>6438701544</td>
<td>협상이 완료 후 투찰업체의 사업자등록번호임</td>
</tr>
<tr>
<td>prcbdrNm</td>
<td>투찰업체명</td>
<td>200</td>
<td style="text-align: left;">0</td>
<td>주식회사 예신뷰</td>
<td>투찰업체의 명으로 개찰결과구분명이 “개찰완료”일 경우 필수 입력 항목임</td>
</tr>
<tr>
<td>prcbdrCeoNm</td>
<td>투찰업체대표자명</td>
<td>35</td>
<td style="text-align: left;">0</td>
<td>최인아</td>
<td>투찰업체의 대표자명으로 개찰결과구분명이 “개찰완료”일 경우 필수 입력 항목임</td>
</tr>
<tr>
<td>bidprcAmt</td>
<td>투찰금액</td>
<td>21</td>
<td style="text-align: left;">0</td>
<td>100111000</td>
<td>투찰한 금액(원화,원)</td>
</tr>
<tr>
<td>bidprcrt</td>
<td>투찰률</td>
<td>18</td>
<td style="text-align: left;">0</td>
<td>91.01</td>
<td>예정가격에 대한 투찰금액의 비율로 투찰금액/예정가격 *100 임(%)</td>
</tr>
<tr>
<td>rmrk</td>
<td>비고</td>
<td>200</td>
<td style="text-align: left;">0</td>
<td>낙찰</td>
<td>개찰완료내역의 비고</td>
</tr>
<tr>
<td>cnsttyAccotBidAmtUrl</td>
<td>공종별입찰금액URL</td>
<td>150</td>
<td style="text-align: left;">0</td>
<td>N/A</td>
<td>*차세대 나라장터 개편 이후 제공 불가</td>
</tr>
<tr>
<td>drwtNo1</td>
<td>추첨번호1</td>
<td>3</td>
<td>0</td>
<td>10</td>
<td>추첨번호1</td>
</tr>
<tr>
<td>drwtNo2</td>
<td>추첨번호2</td>
<td>3</td>
<td>0</td>
<td>02</td>
<td>추첨번호2</td>
</tr>
<tr>
<td>bidprcDt</td>
<td>투찰일시</td>
<td>19</td>
<td>0</td>
<td>2025-09-16 09:40:35</td>
<td>투찰일시 "YYYY-MM-DD HH:MM:SS"</td>
</tr>
<tr>
<td>bidPrceEvlVal</td>
<td>입찰가격점수</td>
<td>25</td>
<td>0</td>
<td>9.5894</td>
<td>낙찰방법이 협상에 의한 계약의 입찰가격평가점수</td>
</tr>
<tr>
<td>techEvlNaturVal</td>
<td>기술평가원점수</td>
<td>25</td>
<td>0</td>
<td>0</td>
<td>낙찰방법이 협상에 의한 계약의 차등점수제적용의 기술평가 원점수</td>
</tr>
<tr>
<td>techEvlVal</td>
<td>기술평가점수</td>
<td>25</td>
<td>0</td>
<td>81.5</td>
<td>낙찰방법이 협상에 의한 계약의 기술평가점수<br />
* 차등점수제적용의 경우 기술평가총점수</td>
</tr>
<tr>
<td>totalEvlAmtVal</td>
<td>종합평가점수</td>
<td>25</td>
<td>0</td>
<td>91.0894</td>
<td>낙찰방법이 협상에 의한 계약의 종합평가점수</td>
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
<td>REST(URI)</td>
</tr>
<tr>
<td style="text-align: left;">http://apis.data.go.kr/1230000/as/ScsbidInfoService/getOpengResultListInfoOpengCompt?bidNtceNo= R25BK01027145 &amp;bidNtceOrd=002&amp;bidClsfcNo=0&amp;rbidNo=000&amp;pageNo=1&amp;numOfRows=10&amp;ServiceKey=인증키</td>
</tr>
<tr>
<td>응답 메시지</td>
</tr>
<tr>
<td><p>&lt;response&gt;</p>
<p>&lt;header&gt;</p>
<p>&lt;resultCode&gt;00&lt;/resultCode&gt;</p>
<p>&lt;resultMsg&gt;정상&lt;/resultMsg&gt;</p>
<p>&lt;/header&gt;</p>
<p>&lt;body&gt;</p>
<p>&lt;items&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;opengRsltDivNm&gt;개찰완료&lt;/opengRsltDivNm&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK01027145&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;002&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;0&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;opengRank&gt;1&lt;/opengRank&gt;</p>
<p>&lt;prcbdrBizno&gt;6438701544&lt;/prcbdrBizno&gt;</p>
<p>&lt;prcbdrNm&gt;주식회사 예신뷰&lt;/prcbdrNm&gt;</p>
<p>&lt;prcbdrCeoNm&gt;최인아&lt;/prcbdrCeoNm&gt;</p>
<p>&lt;bidprcAmt&gt;100111000&lt;/bidprcAmt&gt;</p>
<p>&lt;bidprcrt&gt;91.01&lt;/bidprcrt&gt;</p>
<p>&lt;rmrk&gt;&lt;/rmrk&gt;</p>
<p>&lt;cnsttyAccotBidAmtUrl&gt;&lt;/cnsttyAccotBidAmtUrl&gt;</p>
<p>&lt;drwtNo1&gt;&lt;/drwtNo1&gt;</p>
<p>&lt;drwtNo2&gt;&lt;/drwtNo2&gt;</p>
<p>&lt;bidprcDt&gt;2025-09-16 09:40:35&lt;/bidprcDt&gt;</p>
<p>&lt;bidPrceEvlVal&gt;9.5894&lt;/bidPrceEvlVal&gt;</p>
<p>&lt;techEvlVal&gt;81.5&lt;/techEvlVal&gt;</p>
<p>&lt;totalEvlAmtVal&gt;91.0894&lt;/totalEvlAmtVal&gt;</p>
<p>&lt;techEvlNaturVal&gt;&lt;/techEvlNaturVal&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;opengRsltDivNm&gt;개찰완료&lt;/opengRsltDivNm&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK01027145&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;002&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;0&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;opengRank&gt;2&lt;/opengRank&gt;</p>
<p>&lt;prcbdrBizno&gt;1078648444&lt;/prcbdrBizno&gt;</p>
<p>&lt;prcbdrNm&gt;주식회사 명진씨앤피&lt;/prcbdrNm&gt;</p>
<p>&lt;prcbdrCeoNm&gt;최영무&lt;/prcbdrCeoNm&gt;</p>
<p>&lt;bidprcAmt&gt;98000000&lt;/bidprcAmt&gt;</p>
<p>&lt;bidprcrt&gt;89.09&lt;/bidprcrt&gt;</p>
<p>&lt;rmrk&gt;&lt;/rmrk&gt;</p>
<p>&lt;cnsttyAccotBidAmtUrl&gt;&lt;/cnsttyAccotBidAmtUrl&gt;</p>
<p>&lt;drwtNo1&gt;&lt;/drwtNo1&gt;</p>
<p>&lt;drwtNo2&gt;&lt;/drwtNo2&gt;</p>
<p>&lt;bidprcDt&gt;2025-09-16 09:40:35&lt;/bidprcDt&gt;</p>
<p>&lt;bidPrceEvlVal&gt;9.7959&lt;/bidPrceEvlVal&gt;</p>
<p>&lt;techEvlVal&gt;80.3&lt;/techEvlVal&gt;</p>
<p>&lt;totalEvlAmtVal&gt;90.0959&lt;/totalEvlAmtVal&gt;</p>
<p>&lt;techEvlNaturVal&gt;&lt;/techEvlNaturVal&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;opengRsltDivNm&gt;개찰완료&lt;/opengRsltDivNm&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK01027145&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;002&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;0&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;opengRank&gt;3&lt;/opengRank&gt;</p>
<p>&lt;prcbdrBizno&gt;1051842348&lt;/prcbdrBizno&gt;</p>
<p>&lt;prcbdrNm&gt;칼리그램&lt;/prcbdrNm&gt;</p>
<p>&lt;prcbdrCeoNm&gt;김용운&lt;/prcbdrCeoNm&gt;</p>
<p>&lt;bidprcAmt&gt;100000000&lt;/bidprcAmt&gt;</p>
<p>&lt;bidprcrt&gt;90.909&lt;/bidprcrt&gt;</p>
<p>&lt;rmrk&gt;&lt;/rmrk&gt;</p>
<p>&lt;cnsttyAccotBidAmtUrl&gt;&lt;/cnsttyAccotBidAmtUrl&gt;</p>
<p>&lt;drwtNo1&gt;&lt;/drwtNo1&gt;</p>
<p>&lt;drwtNo2&gt;&lt;/drwtNo2&gt;</p>
<p>&lt;bidprcDt&gt;2025-09-16 09:40:35&lt;/bidprcDt&gt;</p>
<p>&lt;bidPrceEvlVal&gt;9.6&lt;/bidPrceEvlVal&gt;</p>
<p>&lt;techEvlVal&gt;78.3&lt;/techEvlVal&gt;</p>
<p>&lt;totalEvlAmtVal&gt;87.9&lt;/totalEvlAmtVal&gt;</p>
<p>&lt;techEvlNaturVal&gt;&lt;/techEvlNaturVal&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;opengRsltDivNm&gt;개찰완료&lt;/opengRsltDivNm&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK01027145&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;002&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;0&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;opengRank&gt;4&lt;/opengRank&gt;</p>
<p>&lt;prcbdrBizno&gt;1160178265&lt;/prcbdrBizno&gt;</p>
<p>&lt;prcbdrNm&gt;경성문화사&lt;/prcbdrNm&gt;</p>
<p>&lt;prcbdrCeoNm&gt;박진태&lt;/prcbdrCeoNm&gt;</p>
<p>&lt;bidprcAmt&gt;100000000&lt;/bidprcAmt&gt;</p>
<p>&lt;bidprcrt&gt;90.909&lt;/bidprcrt&gt;</p>
<p>&lt;rmrk&gt;&lt;/rmrk&gt;</p>
<p>&lt;cnsttyAccotBidAmtUrl&gt;&lt;/cnsttyAccotBidAmtUrl&gt;</p>
<p>&lt;drwtNo1&gt;&lt;/drwtNo1&gt;</p>
<p>&lt;drwtNo2&gt;&lt;/drwtNo2&gt;</p>
<p>&lt;bidprcDt&gt;2025-09-16 09:40:35&lt;/bidprcDt&gt;</p>
<p>&lt;bidPrceEvlVal&gt;9.6&lt;/bidPrceEvlVal&gt;</p>
<p>&lt;techEvlVal&gt;78.2&lt;/techEvlVal&gt;</p>
<p>&lt;totalEvlAmtVal&gt;87.8&lt;/totalEvlAmtVal&gt;</p>
<p>&lt;techEvlNaturVal&gt;&lt;/techEvlNaturVal&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;opengRsltDivNm&gt;개찰완료&lt;/opengRsltDivNm&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK01027145&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;002&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;0&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;opengRank&gt;5&lt;/opengRank&gt;</p>
<p>&lt;prcbdrBizno&gt;1058763392&lt;/prcbdrBizno&gt;</p>
<p>&lt;prcbdrNm&gt;주식회사 도서출판알투스&lt;/prcbdrNm&gt;</p>
<p>&lt;prcbdrCeoNm&gt;손은주&lt;/prcbdrCeoNm&gt;</p>
<p>&lt;bidprcAmt&gt;96000000&lt;/bidprcAmt&gt;</p>
<p>&lt;bidprcrt&gt;87.272&lt;/bidprcrt&gt;</p>
<p>&lt;rmrk&gt;&lt;/rmrk&gt;</p>
<p>&lt;cnsttyAccotBidAmtUrl&gt;&lt;/cnsttyAccotBidAmtUrl&gt;</p>
<p>&lt;drwtNo1&gt;&lt;/drwtNo1&gt;</p>
<p>&lt;drwtNo2&gt;&lt;/drwtNo2&gt;</p>
<p>&lt;bidprcDt&gt;2025-09-16 09:40:35&lt;/bidprcDt&gt;</p>
<p>&lt;bidPrceEvlVal&gt;10&lt;/bidPrceEvlVal&gt;</p>
<p>&lt;techEvlVal&gt;75.7&lt;/techEvlVal&gt;</p>
<p>&lt;totalEvlAmtVal&gt;85.7&lt;/totalEvlAmtVal&gt;</p>
<p>&lt;techEvlNaturVal&gt;&lt;/techEvlNaturVal&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;opengRsltDivNm&gt;개찰완료&lt;/opengRsltDivNm&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK01027145&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;002&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;0&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;opengRank&gt;6&lt;/opengRank&gt;</p>
<p>&lt;prcbdrBizno&gt;3123161127&lt;/prcbdrBizno&gt;</p>
<p>&lt;prcbdrNm&gt;디자인소나무&lt;/prcbdrNm&gt;</p>
<p>&lt;prcbdrCeoNm&gt;유영주&lt;/prcbdrCeoNm&gt;</p>
<p>&lt;bidprcAmt&gt;108520000&lt;/bidprcAmt&gt;</p>
<p>&lt;bidprcrt&gt;98.654&lt;/bidprcrt&gt;</p>
<p>&lt;rmrk&gt;&lt;/rmrk&gt;</p>
<p>&lt;cnsttyAccotBidAmtUrl&gt;&lt;/cnsttyAccotBidAmtUrl&gt;</p>
<p>&lt;drwtNo1&gt;&lt;/drwtNo1&gt;</p>
<p>&lt;drwtNo2&gt;&lt;/drwtNo2&gt;</p>
<p>&lt;bidprcDt&gt;2025-09-16 09:40:35&lt;/bidprcDt&gt;</p>
<p>&lt;bidPrceEvlVal&gt;8.8463&lt;/bidPrceEvlVal&gt;</p>
<p>&lt;techEvlVal&gt;68.7&lt;/techEvlVal&gt;</p>
<p>&lt;totalEvlAmtVal&gt;77.5463&lt;/totalEvlAmtVal&gt;</p>
<p>&lt;techEvlNaturVal&gt;&lt;/techEvlNaturVal&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;/items&gt;</p>
<p>&lt;numOfRows&gt;10&lt;/numOfRows&gt;</p>
<p>&lt;pageNo&gt;1&lt;/pageNo&gt;</p>
<p>&lt;totalCount&gt;6&lt;/totalCount&gt;</p>
<p>&lt;/body&gt;</p>
<p>&lt;/response&gt;</p></td>
</tr>
</tbody>
</table>

#### \[개찰결과 유찰 목록 조회\] 오퍼레이션 명세

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
<td colspan="2">개찰결과 유찰 목록 조회</td>
</tr>
<tr>
<td>오퍼레이션 유형</td>
<td>조회(목록)</td>
<td>오퍼레이션명(영문)</td>
<td colspan="2"><strong>getOpengResultListInfoFailing</strong></td>
</tr>
<tr>
<td>오퍼레이션 설명</td>
<td colspan="4">검색조건을 입찰공고번호 입력하여 물품, 공사, 용역, 외자의 나라장터 개찰결과 유찰 목록(개찰결과구분명, 입찰공고번호, 입찰공고차수, 입찰분류번호, 재입찰번호, 유찰사유)을 조회</td>
</tr>
<tr>
<td>Call Back URL</td>
<td colspan="4" style="text-align: left;">N/A</td>
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

|  |  |  |  |  |  |
|----|----|----|----|----|----|
| 항목명(영문) | 항목명(국문) | 항목크기 | 항목구분 | 샘플데이터 | 항목설명 |
| numOfRows | 한 페이지 결과 수 | 4 | 1 | 10 | 한 페이지 결과 수 |
| pageNo | 페이지 번호 | 4 | 1 | 1 | 페이지 번호 |
| ServiceKey | 서비스키 | 400 | 1 | 공공데이터포털에서 받은 인증키 | 공공데이터포털에서 받은 인증키 |
| type | 타입 | 4 | 0 | json | 오픈API 리턴 타입을 JSON으로 받고 싶을 경우 'json' 으로 지정 |
| bidNtceNo | 입찰공고번호 | 11 | 1 | R25BK00936962 | 검색하고자하는 입찰공고번호 |
| bidNtceOrd | 입찰공고차수 | 3 | 0 | 000 | 검색하고자하는 입찰공고차수 |
| bidClsfcNo | 입찰분류번호 | 5 | 0 | 1 | 검색하고자하는 입찰분류번호 |
| rbidNo | 재입찰번호 | 3 | 0 | 000 | 검색하고자하는 재입찰번호 |

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 응답 메시지 명세

<table style="width:100%;">
<colgroup>
<col style="width: 21%" />
<col style="width: 21%" />
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 16%" />
<col style="width: 17%" />
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
<td>numOfRows</td>
<td>한 페이지 결과 수</td>
<td>4</td>
<td>1</td>
<td>10</td>
<td>한 페이지 결과 수</td>
</tr>
<tr>
<td>pageNo</td>
<td>페이지 번호</td>
<td>4</td>
<td>1</td>
<td>1</td>
<td>페이지 번호</td>
</tr>
<tr>
<td>totalCount</td>
<td>데이터 총 개수</td>
<td>4</td>
<td>1</td>
<td>17</td>
<td>데이터 총 개수</td>
</tr>
<tr>
<td style="text-align: left;">opengRsltDivNm</td>
<td>개찰결과구분명</td>
<td style="text-align: left;">30</td>
<td>1</td>
<td>유찰</td>
<td>해당 공고건에 대한 개찰결과를 구분하는 것으로 개찰이 완료되었는지, 유찰되었는지, 재입찰 할것인지 등을 구분하는 명으로 이 오퍼레이션은 유찰인 정보 조회</td>
</tr>
<tr>
<td>bidNtceNo</td>
<td>입찰공고번호</td>
<td style="text-align: left;">11</td>
<td>1</td>
<td>R25BK00936962</td>
<td style="text-align: left;">입찰공고 관리번호이며 조달청나라장터 공고건의 형식은 년도(4)+월(2)+순번(5)이며 자체전자조달시스템 보유기관은 각 기관별 형식 별도 사용<br />
*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성<br />
- 단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</td>
</tr>
<tr>
<td>bidNtceOrd</td>
<td>입찰공고차수</td>
<td style="text-align: left;">3</td>
<td>1</td>
<td>000</td>
<td>입찰공고차수는 해당 입찰공고에 대한 재공고 및 재입찰 등이 발생되었을 경우 증가되는 수</td>
</tr>
<tr>
<td>bidClsfcNo</td>
<td>입찰분류번호</td>
<td style="text-align: left;">5</td>
<td>1</td>
<td>1</td>
<td>동일한 입찰공고번호에 대한 집행일련번호</td>
</tr>
<tr>
<td>rbidNo</td>
<td>재입찰번호</td>
<td style="text-align: left;">3</td>
<td>1</td>
<td>000</td>
<td>재입찰번호</td>
</tr>
<tr>
<td>nobidRsn</td>
<td>유찰사유</td>
<td style="text-align: left;">200</td>
<td>0</td>
<td>단독응찰</td>
<td>유찰사유</td>
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
<td>REST(URI)</td>
</tr>
<tr>
<td style="text-align: left;">http://apis.data.go.kr/1230000/as/ScsbidInfoService/getOpengResultListInfoFailing?bidNtceNo=R25BK00936962&amp;bidNtceOrd=000&amp;bidClsfcNo=1&amp;rbidNo=000&amp;pageNo=1&amp;numOfRows=10&amp;ServiceKey=인증키</td>
</tr>
<tr>
<td>응답 메시지</td>
</tr>
<tr>
<td><p>&lt;response&gt;</p>
<p>&lt;header&gt;</p>
<p>&lt;resultCode&gt;00&lt;/resultCode&gt;</p>
<p>&lt;resultMsg&gt;정상&lt;/resultMsg&gt;</p>
<p>&lt;/header&gt;</p>
<p>&lt;body&gt;</p>
<p>&lt;items&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;opengRsltDivNm&gt;유찰&lt;/opengRsltDivNm&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00936962&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;1&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;nobidRsn&gt;단독응찰&lt;/nobidRsn&gt;</p>
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

#### \[개찰결과 재입찰 목록 조회\] 오퍼레이션 명세

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
<td colspan="2">개찰결과 재입찰 목록 조회</td>
</tr>
<tr>
<td>오퍼레이션 유형</td>
<td>조회(목록)</td>
<td>오퍼레이션명(영문)</td>
<td colspan="2"><strong>getOpengResultListInfoRebid</strong></td>
</tr>
<tr>
<td>오퍼레이션 설명</td>
<td colspan="4">검색조건을 입찰공고번호 입력하여 물품, 공사, 용역, 외자의 나라장터 개찰결과 재입찰 목록(개찰결과구분명, 입찰공고번호, 입찰공고차수, 입찰분류번호, 재입찰번호, 입찰마감일시, 개찰일시, 재입찰사유, 공동수급협정마감일시)을 조회.</td>
</tr>
<tr>
<td>Call Back URL</td>
<td colspan="4" style="text-align: left;">N/A</td>
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

|  |  |  |  |  |  |
|----|----|----|----|----|----|
| 항목명(영문) | 항목명(국문) | 항목크기 | 항목구분 | 샘플데이터 | 항목설명 |
| numOfRows | 한 페이지 결과 수 | 4 | 1 | 10 | 한 페이지 결과 수 |
| pageNo | 페이지 번호 | 4 | 1 | 1 | 페이지 번호 |
| ServiceKey | 서비스키 | 400 | 1 | 공공데이터포털에서 받은 인증키 | 공공데이터포털에서 받은 인증키 |
| type | 타입 | 4 | 0 | json | 오픈API 리턴 타입을 JSON으로 받고 싶을 경우 'json' 으로 지정 |
| bidNtceNo | 입찰공고번호 | 11 | 1 | R25BK00922094 | 검색하고자하는 입찰공고번호 |
| bidNtceOrd | 입찰공고차수 | 2 | 0 | 000 | 검색하고자하는 입찰공고차수 |
| bidClsfcNo | 입찰분류번호 | 5 | 0 | 1 | 검색하고자하는 입찰분류번호 |
| rbidNo | 재입찰번호 | 3 | 0 | 000 | 검색하고자하는 재입찰번호 |

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 응답 메시지 명세

<table style="width:100%;">
<colgroup>
<col style="width: 21%" />
<col style="width: 21%" />
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 18%" />
<col style="width: 15%" />
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
<td>numOfRows</td>
<td>한 페이지 결과 수</td>
<td>4</td>
<td>1</td>
<td>10</td>
<td>한 페이지 결과 수</td>
</tr>
<tr>
<td>pageNo</td>
<td>페이지 번호</td>
<td>4</td>
<td>1</td>
<td>1</td>
<td>페이지 번호</td>
</tr>
<tr>
<td>totalCount</td>
<td>데이터 총 개수</td>
<td>4</td>
<td>1</td>
<td>17</td>
<td>데이터 총 개수</td>
</tr>
<tr>
<td style="text-align: left;">opengRsltDivNm</td>
<td>개찰결과구분명</td>
<td>30</td>
<td style="text-align: left;">1</td>
<td>재입찰</td>
<td>해당 공고건에 대한 개찰결과를 구분하는 것으로 개찰이 완료되었는지, 유찰되었는지, 재입찰 할것인지 등을 구분하는 명으로 이 오퍼레이션은 재입찰인 정보 조회</td>
</tr>
<tr>
<td>bidNtceNo</td>
<td>입찰공고번호</td>
<td>11</td>
<td style="text-align: left;">1</td>
<td>R25BK00922094</td>
<td style="text-align: left;">입찰공고 관리번호이며 조달청나라장터 공고건의 형식은 년도(4)+월(2)+순번(5)이며 자체전자조달시스템 보유기관은 각 기관별 형식 별도 사용<br />
*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성<br />
- 단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</td>
</tr>
<tr>
<td>bidNtceOrd</td>
<td>입찰공고차수</td>
<td>3</td>
<td style="text-align: left;">1</td>
<td>000</td>
<td>입찰공고차수는 해당 입찰공고에 대한 재공고 및 재입찰 등이 발생되었을 경우 증가되는 수</td>
</tr>
<tr>
<td>bidClsfcNo</td>
<td>입찰분류번호</td>
<td>5</td>
<td style="text-align: left;">1</td>
<td>1</td>
<td>동일한 입찰공고번호에 대한 집행일련번호</td>
</tr>
<tr>
<td>rbidNo</td>
<td>재입찰번호</td>
<td>2</td>
<td style="text-align: left;">1</td>
<td>001</td>
<td>재입찰이 발생되었을 경우 증가되는 재입찰번호</td>
</tr>
<tr>
<td>bidClseDt</td>
<td>입찰마감일시</td>
<td>19</td>
<td style="text-align: left;">1</td>
<td>2025-07-15 18:00:00</td>
<td>입찰마감일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td>opengDt</td>
<td>개찰일시</td>
<td>19</td>
<td style="text-align: left;">1</td>
<td>2025-07-15 19:00:00</td>
<td>조달업체가 제출한 입찰서를 개찰하는 일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td>rbidRsn</td>
<td>재입찰사유</td>
<td>200</td>
<td style="text-align: left;">0</td>
<td>낙찰자 없음</td>
<td>재입찰사유</td>
</tr>
<tr>
<td>cmmnSpldmdAgrmntClseDt</td>
<td>공동수급혐정마감일시</td>
<td>19</td>
<td style="text-align: left;">0</td>
<td>2025-07-15 18:00:00</td>
<td>공동수급혐정마감일시 “YYYY-MM-DD HH:MM:SS”</td>
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
<td>REST(URI)</td>
</tr>
<tr>
<td style="text-align: left;">http://apis.data.go.kr/1230000/as/ScsbidInfoService/getOpengResultListInfoRebid?bidNtceNo=R25BK00922094&amp;bidNtceOrd=000&amp;bidClsfcNo=1&amp;rbidNo=000&amp;pageNo=1&amp;numOfRows=10&amp;ServiceKey=인증키</td>
</tr>
<tr>
<td>응답 메시지</td>
</tr>
<tr>
<td><p>&lt;response&gt;</p>
<p>&lt;header&gt;</p>
<p>&lt;resultCode&gt;00&lt;/resultCode&gt;</p>
<p>&lt;resultMsg&gt;정상&lt;/resultMsg&gt;</p>
<p>&lt;/header&gt;</p>
<p>&lt;body&gt;</p>
<p>&lt;items&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;opengRsltDivNm&gt;재입찰&lt;/opengRsltDivNm&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00922094&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;1&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;001&lt;/rbidNo&gt;</p>
<p>&lt;bidClseDt&gt;2025-07-15 18:00:00&lt;/bidClseDt&gt;</p>
<p>&lt;opengDt&gt;2025-07-15 19:00:00&lt;/opengDt&gt;</p>
<p>&lt;rbidRsn&gt;낙찰자 없음&lt;/rbidRsn&gt;</p>
<p>&lt;cmmnSpldmdAgrmntClseDt&gt;&lt;/cmmnSpldmdAgrmntClseDt&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;/items&gt;</p>
<p>&lt;numOfRows&gt;10&lt;/numOfRows&gt;</p>
<p>&lt;pageNo&gt;1&lt;/pageNo&gt;</p>
<p>&lt;totalCount&gt;1&lt;/totalCount&gt;</p>
<p>&lt;/body&gt;</p>
<p>&lt;/response</p></td>
</tr>
</tbody>
</table>

#### \[나라장터 검색조건에 의한 낙찰된 목록 현황 물품조회\] 오퍼레이션 명세

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
<td colspan="2">나라장터 검색조건에 의한 낙찰된 목록 현황 물품조회</td>
</tr>
<tr>
<td>오퍼레이션 유형</td>
<td>조회(목록)</td>
<td>오퍼레이션명(영문)</td>
<td colspan="2"><strong>getScsbidListSttusThngPPSSrch</strong></td>
</tr>
<tr>
<td>오퍼레이션 설명</td>
<td colspan="4">검색조건을 공고일시, 개찰일시, 입찰공고번호, 입찰공고명, 공고기관코드, 공고기관명, 수요기관코드, 수요기관명, 참조번호, 참가제한지역코드, 참가제한지역명, 업종코드, 업종명, 추정가격시작, 추정가격종료, 세부품명번호, 다수공급경쟁자여부, 조달요청번호, 국제구분코드로 물품에 대한 나라장터 최종낙찰자 목록(입찰공고번호, 입찰공고명, 참가업체수, 최종낙찰업체명, 사업자번호, 최종낙찰률, 실개찰일시, 수요기관)을 조회</td>
</tr>
<tr>
<td>Call Back URL</td>
<td colspan="4" style="text-align: left;">N/A</td>
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

<table style="width:100%;">
<colgroup>
<col style="width: 19%" />
<col style="width: 19%" />
<col style="width: 13%" />
<col style="width: 11%" />
<col style="width: 14%" />
<col style="width: 20%" />
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
<td style="text-align: left;">공공데이터포털에서 받은 인증키</td>
<td style="text-align: left;">공공데이터포털에서 받은 인증키</td>
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
<td>inqryDiv</td>
<td>조회구분</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td>1</td>
<td>검색하고자하는 조회구분<br />
1:공고게시일시, 2:개찰일시, 3:입찰공고번호</td>
</tr>
<tr>
<td>inqryBgnDt</td>
<td>조회시작일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td>202507010000</td>
<td>검색하고자 하는 조회시작일시 "YYYYMMDDHHMM"<br />
조회구분이 '1'인 경우 공고게시일시 필수, '2'인 경우 개찰일시 필수</td>
</tr>
<tr>
<td>inqryEndDt</td>
<td>조회종료일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td>202507012359</td>
<td>검색하고자 하는 조회종료일시 "YYYYMMDDHHMM"<br />
조회구분이 '1'인 경우 공고게시일시 필수, '2'인 경우 개찰일시 필수</td>
</tr>
<tr>
<td>bidNtceNo</td>
<td>입찰공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">0</td>
<td>R25BK00965123</td>
<td>검색하고자하는 입찰공고번호<br />
조회구분이 '3'인 경우 필수</td>
</tr>
<tr>
<td>bidNtceNm</td>
<td>입찰공고명</td>
<td style="text-align: left;">1000</td>
<td style="text-align: left;">0</td>
<td>혁신육아복합센터 건립공사(기계) 관급자재(간접가열보일러)</td>
<td>검색하고자하는 공고명<br />
※ 공고명 일부 입력시에도 조회 가능</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttCd</td>
<td style="text-align: left;">공고기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">6280147</td>
<td style="text-align: left;">검색하고자하는 공고기관코드</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttNm</td>
<td style="text-align: left;">공고기관명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">인천광역시 종합건설본부</td>
<td style="text-align: left;">검색하고자하는 공고기관명<br />
※ 공고기관명 일부 입력시에도 조회 가능</td>
</tr>
<tr>
<td style="text-align: left;">dminsttCd</td>
<td style="text-align: left;">수요기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">6280147</td>
<td style="text-align: left;"><p>검색하고자하는 수요기관코드</p>
<p>행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드 입력</p>
<p>행자부코드가 없는 경우 조달청에서 부여한 수요기관 코드 입력</p></td>
</tr>
<tr>
<td style="text-align: left;">dminsttNm</td>
<td style="text-align: left;">수요기관명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">인천광역시 종합건설본부</td>
<td style="text-align: left;">검색하고자하는 수요기관명<br />
※ 수요기관명 일부 입력시에도 조회 가능</td>
</tr>
<tr>
<td style="text-align: left;">refNo</td>
<td style="text-align: left;">참조번호</td>
<td style="text-align: left;">105</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">제2025</td>
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
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">4119</td>
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
<td style="text-align: left;">77409000</td>
<td style="text-align: left;">검색하고자하는 추정가격범위시작금액이상(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">presmptPrceEnd</td>
<td style="text-align: left;">추정가격종료</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">77410000</td>
<td style="text-align: left;">검색하고자하는 추정가격범위종료금액이하(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">dtilPrdctClsfcNo</td>
<td style="text-align: left;">세부품명번호</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">4010209501</td>
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
<td style="text-align: left;">제2025</td>
<td style="text-align: left;">검색하고자하는 조달요청번호</td>
</tr>
<tr>
<td style="text-align: left;">intrntnlDivCd</td>
<td style="text-align: left;">국제구분코드</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">검색하고자하는 국제구분코드<br />
국내:1, 국제:2</td>
</tr>
<tr>
<td style="text-align: left;">bizno</td>
<td style="text-align: left;">사업자번호</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">1408121883</td>
<td style="text-align: left;">검색하고자 하는 업체의 사업자번호</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 응답 메시지 명세

<table style="width:100%;">
<colgroup>
<col style="width: 21%" />
<col style="width: 21%" />
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 13%" />
<col style="width: 20%" />
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
<td>resultCode</td>
<td>결과코드</td>
<td style="text-align: left;">2</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">00</td>
<td style="text-align: left;">결과코드</td>
</tr>
<tr>
<td>resultMsg</td>
<td>결과메세지</td>
<td style="text-align: left;">50</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">정상.</td>
<td style="text-align: left;">결과메세지</td>
</tr>
<tr>
<td>numOfRows</td>
<td>한 페이지 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td>pageNo</td>
<td>페이지 번호</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">페이지 수</td>
</tr>
<tr>
<td>totalCount</td>
<td>데이터 총 개수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">17</td>
<td style="text-align: left;">데이터 총 개수</td>
</tr>
<tr>
<td>bidNtceNo</td>
<td>입찰공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">R25BK00965123</td>
<td style="text-align: left;">입찰공고 관리번호이며 조달청나라장터 공고건의 형식은 년도(4)+월(2)+순번(5)이며 자체전자조달시스템 보유기관은 각 기관별 형식 별도 사용<br />
*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성<br />
- 단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</td>
</tr>
<tr>
<td>bidNtceOrd</td>
<td>입찰공고차수</td>
<td style="text-align: left;">3</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">000</td>
<td style="text-align: left;">입찰공고차수는 해당 입찰공고에 대한 재공고 및 재입찰 등이 발생되었을 경우 증가되는 수</td>
</tr>
<tr>
<td>bidClsfcNo</td>
<td>입찰분류번호</td>
<td style="text-align: left;">5</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">동일한 입찰공고번호에 대한 집행일련번호</td>
</tr>
<tr>
<td>rbidNo</td>
<td>재입찰번호</td>
<td style="text-align: left;">3</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">000</td>
<td style="text-align: left;">재입찰번호</td>
</tr>
<tr>
<td>ntceDivCd</td>
<td>공고구분코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">통050001</td>
<td style="text-align: left;">공고구분<br />
통050001 : 조달청 또는 나라장터 자체 공고건</td>
</tr>
<tr>
<td>bidNtceNm</td>
<td>입찰공고명</td>
<td style="text-align: left;">1000</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">혁신육아복합센터 건립공사(기계) 관급자재(간접가열보일러)</td>
<td style="text-align: left;">공사명 또는 사업명이라고도 하며 입찰공고 내용을 요약한 이름</td>
</tr>
<tr>
<td>prtcptCnum</td>
<td>참가업체수</td>
<td style="text-align: left;">6</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2</td>
<td style="text-align: left;">참가업체수</td>
</tr>
<tr>
<td>bidwinnrNm</td>
<td>최종낙찰업체명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">주식회사 동광보일러</td>
<td style="text-align: left;">최종낙찰된 업체의 명으로 개찰완료된 건에 대하여 제공</td>
</tr>
<tr>
<td>bidwinnrBizno</td>
<td>최종낙찰업체사업자등록번호</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1408121883</td>
<td style="text-align: left;">협상이 완료 후 최종낙찰된 업체의 사업자등록번호임</td>
</tr>
<tr>
<td>bidwinnrCeoNm</td>
<td>최종낙찰업체대표자명</td>
<td style="text-align: left;">35</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">박정연</td>
<td style="text-align: left;">최종낙찰된 업체의 대표자명으로 개찰완료된 건에 대하여 제공</td>
</tr>
<tr>
<td>bidwinnrAdrs</td>
<td>최종낙찰업체주소</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">충청남도 아산시 수장로 67-0 (배미동)</td>
<td style="text-align: left;">협상이 완료 후 최종낙찰된 업체의 주소임</td>
</tr>
<tr>
<td>bidwinnrTelNo</td>
<td>최종낙찰업체전화번호</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">02-6258-8989</td>
<td style="text-align: left;">협상이 완료 후 최종낙찰된 업체의 연락 전화번호임<br />
핸드폰번호는 “*”로 표기</td>
</tr>
<tr>
<td>sucsfbidAmt</td>
<td>최종낙찰금액</td>
<td style="text-align: left;">21</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">83500000</td>
<td style="text-align: left;">최종낙찰은 개찰순위 순서대로 협상등을 통해 최종 낙찰된정보를 의미하며 최종낙찰금액은 최종낙찰된 금액 (원화,원)으로 개찰완료된건에 대하여 제공</td>
</tr>
<tr>
<td>sucsfbidRate</td>
<td>최종낙찰률</td>
<td style="text-align: left;">18</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">97.82</td>
<td style="text-align: left;">예정가격대비 최종낙찰금액으로 최종낙찰금액/예정가격 * 100 으로 계산되며 개찰완료된 건에 대하여 제공 (%)</td>
</tr>
<tr>
<td>rlOpengDt</td>
<td>실개찰일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-23 11:00:00</td>
<td style="text-align: left;">실제 개찰일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td>dminsttCd</td>
<td>수요기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">6280147</td>
<td style="text-align: left;">실제 수요기관의 코드로 행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드가 행자부코드가 없는 경우 조달청에서 부여한 수요기관 코드가 표기됨</td>
</tr>
<tr>
<td>dminsttNm</td>
<td>수요기관명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">인천광역시 종합건설본부</td>
<td style="text-align: left;">중앙조달인 경우 조달사업에 관한 법률 제2조(정의)에 따라 수요물자의 구매 공급 또는 시설공사 계약의 체결을 조달청장에게 요청할 수 있도록 조달청장이 인정하여 등록한 기관 또는 자체전자조달시스템을 이용하는 기관인 경우 계약을 의뢰한 기관의 명으로 공고기관과 수요기관이 동일할 수 있음</td>
</tr>
<tr>
<td>rgstDt</td>
<td>등록일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">1</td>
<td>2025-07-23 15:20:05</td>
<td style="text-align: left;">등록일시 "YYYY-MM-DD HH:MM:SS"</td>
</tr>
<tr>
<td>fnlSucsfDate</td>
<td>최종낙찰일자</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">0</td>
<td>2025-07-23</td>
<td style="text-align: left;">최종낙찰된 일자로 개찰완료된 건에 대하여 제공</td>
</tr>
<tr>
<td>fnlSucsfCorpOfcl</td>
<td>최종낙찰업체담당자</td>
<td style="text-align: left;">35</td>
<td style="text-align: left;">0</td>
<td>N/A</td>
<td style="text-align: left;">최종낙찰된 업체의 담당자명으로 개찰완료된 건에 대하여 제공</td>
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
<td>REST(URI)</td>
</tr>
<tr>
<td style="text-align: left;">http://apis.data.go.kr/1230000/as/ScsbidInfoService/getScsbidListSttusThngPPSSrch?inqryDiv=1&amp;inqryBgnDt=202507010000&amp;inqryEndDt=202507012359&amp;bidNtceNm=혁신육아복합센터 건립공사(기계) 관급자재(간접가열보일러)&amp;pageNo=1&amp;numOfRows=10&amp;ServiceKey=인증키</td>
</tr>
<tr>
<td>응답 메시지</td>
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
<p>&lt;bidNtceNo&gt;R25BK00965123&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;1&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;ntceDivCd&gt;통050001&lt;/ntceDivCd&gt;</p>
<p>&lt;bidNtceNm&gt;혁신육아복합센터 건립공사(기계) 관급자재(간접가열보일러)&lt;/bidNtceNm&gt;</p>
<p>&lt;prtcptCnum&gt;2&lt;/prtcptCnum&gt;</p>
<p>&lt;bidwinnrNm&gt;주식회사 동광보일러&lt;/bidwinnrNm&gt;</p>
<p>&lt;bidwinnrBizno&gt;1408121883&lt;/bidwinnrBizno&gt;</p>
<p>&lt;bidwinnrCeoNm&gt;박정연&lt;/bidwinnrCeoNm&gt;</p>
<p>&lt;bidwinnrAdrs&gt;충청남도 아산시 수장로 67-0 (배미동)&lt;/bidwinnrAdrs&gt;</p>
<p>&lt;bidwinnrTelNo&gt;02-6258-8989&lt;/bidwinnrTelNo&gt;</p>
<p>&lt;sucsfbidAmt&gt;83500000&lt;/sucsfbidAmt&gt;</p>
<p>&lt;sucsfbidRate&gt;97.82&lt;/sucsfbidRate&gt;</p>
<p>&lt;rlOpengDt&gt;2025-07-23 11:00:00&lt;/rlOpengDt&gt;</p>
<p>&lt;dminsttCd&gt;6280147&lt;/dminsttCd&gt;</p>
<p>&lt;dminsttNm&gt;인천광역시 종합건설본부&lt;/dminsttNm&gt;</p>
<p>&lt;rgstDt&gt;2025-07-23 15:20:05&lt;/rgstDt&gt;</p>
<p>&lt;fnlSucsfDate&gt;2025-07-23&lt;/fnlSucsfDate&gt;</p>
<p>&lt;fnlSucsfCorpOfcl&gt;&lt;/fnlSucsfCorpOfcl&gt;</p>
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

#### \[나라장터 검색조건에 의한 낙찰된 목록 현황 공사조회\] 오퍼레이션 명세

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
<td colspan="2">나라장터 검색조건에 의한 낙찰된 목록 현황 공사조회</td>
</tr>
<tr>
<td>오퍼레이션 유형</td>
<td>조회(목록)</td>
<td>오퍼레이션명(영문)</td>
<td colspan="2"><strong>getScsbidListSttusCnstwkPPSSrch</strong></td>
</tr>
<tr>
<td>오퍼레이션 설명</td>
<td colspan="4">검색조건을 공고일시, 개찰일시, 입찰공고번호, 입찰공고명, 공고기관코드, 공고기관명, 수요기관코드, 수요기관명, 참조번호, 참가제한지역코드, 참가제한지역명, 업종코드, 업종명, 추정가격시작, 추정가격종료, 세부품명번호, 다수공급경쟁자여부, 조달요청번호, 국제구분코드로 공사에대한 나라장터 최종낙찰자 목록(입찰공고번호, 입찰공고명, 참가업체수, 최종낙찰업체명, 사업자번호, 최종낙찰률, 실개찰일시, 수요기관)을 조회</td>
</tr>
<tr>
<td>Call Back URL</td>
<td colspan="4" style="text-align: left;">N/A</td>
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
<col style="width: 14%" />
<col style="width: 20%" />
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
<td style="text-align: left;">공공데이터포털에서 받은 인증키</td>
<td style="text-align: left;">공공데이터포털에서 받은 인증키</td>
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
<td>inqryDiv</td>
<td>조회구분</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td>1</td>
<td>검색하고자하는 조회구분<br />
1:공고게시일시, 2:개찰일시, 3:입찰공고번호</td>
</tr>
<tr>
<td>inqryBgnDt</td>
<td>조회시작일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td>202507010000</td>
<td>검색하고자 하는 조회시작일시 "YYYYMMDDHHMM"<br />
조회구분이 '1'인 경우 공고게시일시 필수, '2'인 경우 개찰일시 필수</td>
</tr>
<tr>
<td>inqryEndDt</td>
<td>조회종료일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td>202507012359</td>
<td>검색하고자 하는 조회종료일시 "YYYYMMDDHHMM"<br />
조회구분이 '1'인 경우 공고게시일시 필수, '2'인 경우 개찰일시 필수</td>
</tr>
<tr>
<td>bidNtceNo</td>
<td>입찰공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">0</td>
<td>R25BK00922727</td>
<td>검색하고자하는 입찰공고번호<br />
조회구분이 '3'인 경우 필수</td>
</tr>
<tr>
<td>bidNtceNm</td>
<td>입찰공고명</td>
<td style="text-align: left;">1000</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">(입찰대행)신활력플러스 군지정형 어르신영농단 지원사업</td>
<td style="text-align: left;">검색하고자하는 공고명<br />
※ 공고명 일부 입력시에도 조회 가능</td>
</tr>
<tr>
<td>ntceInsttCd</td>
<td>공고기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">4791000</td>
<td style="text-align: left;">검색하고자하는 공고기관코드</td>
</tr>
<tr>
<td>ntceInsttNm</td>
<td>공고기관명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">전북특별자치도 부안군</td>
<td style="text-align: left;">검색하고자하는 공고기관명<br />
※ 공고기관명 일부 입력시에도 조회 가능</td>
</tr>
<tr>
<td>dminsttCd</td>
<td>수요기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">4791000</td>
<td style="text-align: left;"><p>검색하고자하는 수요기관코드</p>
<p>행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드 입력</p>
<p>행자부코드가 없는 경우 조달청에서 부여한 수요기관 코드 입력</p></td>
</tr>
<tr>
<td>dminsttNm</td>
<td>수요기관명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">전북특별자치도 부안군</td>
<td style="text-align: left;">검색하고자하는 수요기관명<br />
※ 수요기관명 일부 입력시에도 조회 가능</td>
</tr>
<tr>
<td>refNo</td>
<td>참조번호</td>
<td style="text-align: left;">105</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">부안군 공고 제2025-1121호</td>
<td style="text-align: left;">검색하고자하는 참조번호</td>
</tr>
<tr>
<td>prtcptLmtRgnCd</td>
<td>참가제한지역코드</td>
<td style="text-align: left;">2</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">11</td>
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
<td>prtcptLmtRgnNm</td>
<td>참가제한지역명</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">서울특별시</td>
<td style="text-align: left;">검색하고자하는 참가제한지역명<br />
※ 참가제한지역명 일부 입력시에도 조회 가능<br />
*전국 : 지역제한을 설정하지 않은 공고</td>
</tr>
<tr>
<td>indstrytyCd</td>
<td>업종코드</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td>4991</td>
<td>검색하고자하는 업종코드</td>
</tr>
<tr>
<td>indstrytyNm</td>
<td>업종명</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">금속창호ㆍ지붕건축물조립공사업</td>
<td style="text-align: left;">검색하고자하는 업종명<br />
※ 업종명 일부 입력시에도 조회 가능</td>
</tr>
<tr>
<td>presmptPrceBgn</td>
<td>추정가격시작</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">59090900</td>
<td style="text-align: left;">검색하고자하는 추정가격범위시작금액이상(원화,원)</td>
</tr>
<tr>
<td>presmptPrceEnd</td>
<td>추정가격종료</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">59091000</td>
<td style="text-align: left;">검색하고자하는 추정가격범위종료금액이하(원화,원)</td>
</tr>
<tr>
<td>dtilPrdctClsfcNo</td>
<td>세부품명번호</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">1012159801</td>
<td style="text-align: left;">검색하고자하는 세부품명번호</td>
</tr>
<tr>
<td>masYn</td>
<td>다수공급경쟁자여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">검색하고자하는 다수공급경쟁자여부</td>
</tr>
<tr>
<td>prcrmntReqNo</td>
<td>조달요청번호</td>
<td style="text-align: left;">13</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">부안군 공고 제2025-1121호</td>
<td style="text-align: left;">검색하고자하는 조달요청번호</td>
</tr>
<tr>
<td>intrntnlDivCd</td>
<td>국제구분코드</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">검색하고자하는 국제구분코드<br />
국내:1, 국제:2</td>
</tr>
<tr>
<td style="text-align: left;">bizno</td>
<td style="text-align: left;">사업자번호</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">4188124255</td>
<td style="text-align: left;">검색하고자 하는 업체의 사업자번호</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 응답 메시지 명세

<table style="width:100%;">
<colgroup>
<col style="width: 21%" />
<col style="width: 21%" />
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 13%" />
<col style="width: 20%" />
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
<td style="text-align: left;">데이터 총 개수</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNo</td>
<td style="text-align: left;">입찰공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">R25BK00922727</td>
<td style="text-align: left;">입찰공고 관리번호이며 조달청나라장터 공고건의 형식은 년도(4)+월(2)+순번(5)이며 자체전자조달시스템 보유기관은 각 기관별 형식 별도 사용<br />
*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성<br />
- 단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</td>
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
<td style="text-align: left;">동일한 입찰공고번호에 대한 집행일련번호</td>
</tr>
<tr>
<td style="text-align: left;">rbidNo</td>
<td style="text-align: left;">재입찰번호</td>
<td style="text-align: left;">3</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">000</td>
<td style="text-align: left;">재입찰번호</td>
</tr>
<tr>
<td style="text-align: left;">ntceDivCd</td>
<td style="text-align: left;">공고구분코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">통050001</td>
<td style="text-align: left;">공고구분<br />
통050001 : 조달청 또는 나라장터 자체 공고건</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNm</td>
<td style="text-align: left;">입찰공고명</td>
<td style="text-align: left;">1000</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">(입찰대행)신활력플러스 군지정형 어르신영농단 지원사업</td>
<td style="text-align: left;">공사명 또는 사업명이라고도 하며 입찰공고 내용을 요약한 이름</td>
</tr>
<tr>
<td style="text-align: left;">prtcptCnum</td>
<td style="text-align: left;">참가업체수</td>
<td style="text-align: left;">6</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">15</td>
<td style="text-align: left;">참가업체수</td>
</tr>
<tr>
<td style="text-align: left;">bidwinnrNm</td>
<td style="text-align: left;">최종낙찰업체명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">유한회사대가건설</td>
<td style="text-align: left;">최종낙찰된 업체의 명으로 개찰완료된 건에 대하여 제공</td>
</tr>
<tr>
<td style="text-align: left;">bidwinnrBizno</td>
<td style="text-align: left;">최종낙찰업체사업자등록번호</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">4188124255</td>
<td style="text-align: left;">협상이 완료 후 최종낙찰된 업체의 사업자등록번호임</td>
</tr>
<tr>
<td style="text-align: left;">bidwinnrCeoNm</td>
<td style="text-align: left;">최종낙찰업체대표자명</td>
<td style="text-align: left;">35</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">강훈희</td>
<td style="text-align: left;">최종낙찰된 업체의 대표자명으로 개찰완료된 건에 대하여 제공</td>
</tr>
<tr>
<td style="text-align: left;">bidwinnrAdrs</td>
<td style="text-align: left;">최종낙찰업체주소</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">전북특별자치도 부안군 부안읍 서외리 455-3,제1층 제3호</td>
<td style="text-align: left;">협상이 완료 후 최종낙찰된 업체의 주소임</td>
</tr>
<tr>
<td style="text-align: left;">bidwinnrTelNo</td>
<td style="text-align: left;">최종낙찰업체전화번호</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">063-581-8121</td>
<td style="text-align: left;">협상이 완료 후 최종낙찰된 업체의 연락 전화번호임<br />
핸드폰번호는 “*”로 표기</td>
</tr>
<tr>
<td style="text-align: left;">sucsfbidAmt</td>
<td style="text-align: left;">최종낙찰금액</td>
<td style="text-align: left;">21</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">58708988</td>
<td style="text-align: left;">최종낙찰은 개찰순위 순서대로 협상등을 통해 최종 낙찰된정보를 의미하며 최종낙찰금액은 최종낙찰된 금액 (원화,원)으로 개찰완료된건에 대하여 제공</td>
</tr>
<tr>
<td style="text-align: left;">sucsfbidRate</td>
<td style="text-align: left;">최종낙찰률</td>
<td style="text-align: left;">18</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">90.278</td>
<td style="text-align: left;">예정가격대비 최종낙찰금액으로 최종낙찰금액/예정가격 * 100 으로 계산되며 개찰완료된 건에 대하여 제공 (%)</td>
</tr>
<tr>
<td style="text-align: left;">rlOpengDt</td>
<td style="text-align: left;">실개찰일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-06-27 12:00:00</td>
<td style="text-align: left;">실제 개찰일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td style="text-align: left;">dminsttCd</td>
<td style="text-align: left;">수요기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">4791000</td>
<td style="text-align: left;">실제 수요기관의 코드로 행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드가 행자부코드가 없는 경우 조달청에서 부여한 수요기관 코드가 표기됨</td>
</tr>
<tr>
<td style="text-align: left;">dminsttNm</td>
<td style="text-align: left;">수요기관명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">전북특별자치도 부안군</td>
<td style="text-align: left;">중앙조달인 경우 조달사업에 관한 법률 제2조(정의)에 따라 수요물자의 구매 공급 또는 시설공사 계약의 체결을 조달청장에게 요청할 수 있도록 조달청장이 인정하여 등록한 기관 또는 자체전자조달시스템을 이용하는 기관인 경우 계약을 의뢰한 기관의 명으로 공고기관과 수요기관이 동일할 수 있음</td>
</tr>
<tr>
<td style="text-align: left;">rgstDt</td>
<td style="text-align: left;">등록일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">1</td>
<td>2025-07-01 13:54:43</td>
<td style="text-align: left;">등록일시 "YYYY-MM-DD HH:MM:SS"</td>
</tr>
<tr>
<td>fnlSucsfDate</td>
<td>최종낙찰일자</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">0</td>
<td>2025-07-01</td>
<td style="text-align: left;">최종낙찰된 일자로 개찰완료된 건에 대하여 제공</td>
</tr>
<tr>
<td>fnlSucsfCorpOfcl</td>
<td>최종낙찰업체담당자</td>
<td style="text-align: left;">35</td>
<td style="text-align: left;">0</td>
<td>N/A</td>
<td>최종낙찰된 업체의 담당자명으로 개찰완료된 건에 대하여 제공</td>
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
<td>REST(URI)</td>
</tr>
<tr>
<td style="text-align: left;">http://apis.data.go.kr/1230000/as/ScsbidInfoService/ getScsbidListSttusCnstwkPPSSrch?inqryDiv=1&amp;inqryBgnDt=202507010000&amp;inqryEndDt=202507012359&amp;bidNtceNm=(입찰대행)신활력플러스 군지정형 어르신영농단 지원사업&amp;pageNo=1&amp;numOfRows=10&amp;ServiceKey=인증키</td>
</tr>
<tr>
<td>응답 메시지</td>
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
<p>&lt;bidNtceNo&gt;R25BK00922727&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;0&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;ntceDivCd&gt;통050001&lt;/ntceDivCd&gt;</p>
<p>&lt;bidNtceNm&gt;(입찰대행)신활력플러스 군지정형 어르신영농단 지원사업&lt;/bidNtceNm&gt;</p>
<p>&lt;prtcptCnum&gt;15&lt;/prtcptCnum&gt;</p>
<p>&lt;bidwinnrNm&gt;유한회사대가건설&lt;/bidwinnrNm&gt;</p>
<p>&lt;bidwinnrBizno&gt;4188124255&lt;/bidwinnrBizno&gt;</p>
<p>&lt;bidwinnrCeoNm&gt;강훈희&lt;/bidwinnrCeoNm&gt;</p>
<p>&lt;bidwinnrAdrs&gt;전북특별자치도 부안군 부안읍 서외리 455-3,제1층 제3호&lt;/bidwinnrAdrs&gt;</p>
<p>&lt;bidwinnrTelNo&gt;063-581-8121&lt;/bidwinnrTelNo&gt;</p>
<p>&lt;sucsfbidAmt&gt;58708988&lt;/sucsfbidAmt&gt;</p>
<p>&lt;sucsfbidRate&gt;90.278&lt;/sucsfbidRate&gt;</p>
<p>&lt;rlOpengDt&gt;2025-06-27 12:00:00&lt;/rlOpengDt&gt;</p>
<p>&lt;dminsttCd&gt;4791000&lt;/dminsttCd&gt;</p>
<p>&lt;dminsttNm&gt;전북특별자치도 부안군&lt;/dminsttNm&gt;</p>
<p>&lt;rgstDt&gt;2025-07-01 13:54:43&lt;/rgstDt&gt;</p>
<p>&lt;fnlSucsfDate&gt;2025-07-01&lt;/fnlSucsfDate&gt;</p>
<p>&lt;fnlSucsfCorpOfcl&gt;&lt;/fnlSucsfCorpOfcl&gt;</p>
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

#### \[나라장터 검색조건에 의한 낙찰된 목록 현황 용역조회\] 오퍼레이션 명세

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
<td colspan="2">나라장터 검색조건에 의한 낙찰된 목록 현황 용역조회</td>
</tr>
<tr>
<td>오퍼레이션 유형</td>
<td>조회(목록)</td>
<td>오퍼레이션명(영문)</td>
<td colspan="2"><strong>getScsbidListSttusServcPPSSrch</strong></td>
</tr>
<tr>
<td>오퍼레이션 설명</td>
<td colspan="4">검색조건을 공고일시, 개찰일시, 입찰공고번호, 입찰공고명, 공고기관코드, 공고기관명, 수요기관코드, 수요기관명, 참조번호, 참가제한지역코드, 참가제한지역명, 업종코드, 업종명, 추정가격시작, 추정가격종료, 세부품명번호, 다수공급경쟁자여부, 조달요청번호, 국제구분코드로 용역에 대한 나라장터 최종낙찰자 목록(입찰공고번호, 입찰공고명, 참가업체수, 최종낙찰업체명, 사업자번호, 최종낙찰률, 실개찰일시, 수요기관)을 조회</td>
</tr>
<tr>
<td>Call Back URL</td>
<td colspan="4" style="text-align: left;">N/A</td>
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
<col style="width: 11%" />
<col style="width: 14%" />
<col style="width: 20%" />
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
<td>4</td>
<td>1</td>
<td>10</td>
<td>한 페이지 결과 수</td>
</tr>
<tr>
<td>pageNo</td>
<td>페이지 번호</td>
<td>4</td>
<td>1</td>
<td>1</td>
<td style="text-align: left;">페이지 번호</td>
</tr>
<tr>
<td style="text-align: left;">ServiceKey</td>
<td style="text-align: left;">서비스키</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">공공데이터포털에서 받은 인증키</td>
<td style="text-align: left;">공공데이터포털에서 받은 인증키</td>
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
<td>inqryDiv</td>
<td>조회구분</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td>1</td>
<td>검색하고자하는 조회구분<br />
1:공고게시일시, 2:개찰일시, 3:입찰공고번호</td>
</tr>
<tr>
<td>inqryBgnDt</td>
<td>조회시작일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td>202507010000</td>
<td>검색하고자 하는 조회시작일시 "YYYYMMDDHHMM"<br />
조회구분이 '1'인 경우 공고게시일시 필수, '2'인 경우 개찰일시 필수</td>
</tr>
<tr>
<td>inqryEndDt</td>
<td>조회종료일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td>202507012359</td>
<td>검색하고자 하는 조회종료일시 "YYYYMMDDHHMM"<br />
조회구분이 '1'인 경우 공고게시일시 필수, '2'인 경우 개찰일시 필수</td>
</tr>
<tr>
<td>bidNtceNo</td>
<td>입찰공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">0</td>
<td>R25BK00927163</td>
<td>검색하고자하는 입찰공고번호<br />
조회구분이 '3'인 경우 필수</td>
</tr>
<tr>
<td>bidNtceNm</td>
<td>입찰공고명</td>
<td style="text-align: left;">1000</td>
<td style="text-align: left;">0</td>
<td>동물원(해양관, 남미관) 종합안내판 변경 제작 시행</td>
<td>검색하고자하는 공고명<br />
※ 공고명 일부 입력시에도 조회 가능</td>
</tr>
<tr>
<td>ntceInsttCd</td>
<td>공고기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td>6112581</td>
<td>검색하고자하는 공고기관코드</td>
</tr>
<tr>
<td>ntceInsttNm</td>
<td>공고기관명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td>서울특별시 서울대공원</td>
<td>검색하고자하는 공고기관명<br />
※ 공고기관명 일부 입력시에도 조회 가능</td>
</tr>
<tr>
<td>dminsttCd</td>
<td>수요기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td>6112581</td>
<td><p>검색하고자하는 수요기관코드</p>
<p>행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드 입력</p>
<p>행자부코드가 없는 경우 조달청에서 부여한 수요기관 코드 입력</p></td>
</tr>
<tr>
<td>dminsttNm</td>
<td>수요기관명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td>서울특별시 서울대공원</td>
<td>검색하고자하는 수요기관명<br />
※ 수요기관명 일부 입력시에도 조회 가능</td>
</tr>
<tr>
<td>refNo</td>
<td>참조번호</td>
<td style="text-align: left;">105</td>
<td style="text-align: left;">0</td>
<td>전략기획실-4945</td>
<td>검색하고자하는 참조번호</td>
</tr>
<tr>
<td>prtcptLmtRgnCd</td>
<td>참가제한지역코드</td>
<td style="text-align: left;">2</td>
<td style="text-align: left;">0</td>
<td>11</td>
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
<td>prtcptLmtRgnNm</td>
<td>참가제한지역명</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">서울특별시</td>
<td style="text-align: left;">검색하고자하는 참가제한지역명<br />
※ 참가제한지역명 일부 입력시에도 조회 가능<br />
*전국 : 지역제한을 설정하지 않은 공고</td>
</tr>
<tr>
<td>indstrytyCd</td>
<td>업종코드</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td>4119</td>
<td>검색하고자하는 업종코드</td>
</tr>
<tr>
<td>indstrytyNm</td>
<td>업종명</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td>토목공사업</td>
<td>검색하고자하는 업종명<br />
※ 업종명 일부 입력시에도 조회 가능</td>
</tr>
<tr>
<td>presmptPrceBgn</td>
<td>추정가격시작</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td>37150000</td>
<td>검색하고자하는 추정가격범위시작금액이상(원화,원)</td>
</tr>
<tr>
<td>presmptPrceEnd</td>
<td>추정가격종료</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td>37170000</td>
<td>검색하고자하는 추정가격범위종료금액이하(원화,원)</td>
</tr>
<tr>
<td>dtilPrdctClsfcNo</td>
<td>세부품명번호</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">0</td>
<td>1012159801</td>
<td>검색하고자하는 세부품명번호</td>
</tr>
<tr>
<td>masYn</td>
<td>다수공급경쟁자여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td>N</td>
<td>검색하고자하는 다수공급경쟁자여부</td>
</tr>
<tr>
<td>prcrmntReqNo</td>
<td>조달요청번호</td>
<td style="text-align: left;">13</td>
<td style="text-align: left;">0</td>
<td>800</td>
<td>검색하고자하는 조달요청번호</td>
</tr>
<tr>
<td>intrntnlDivCd</td>
<td>국제구분코드</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td>1</td>
<td>검색하고자하는 국제구분코드<br />
국내:1, 국제:2</td>
</tr>
<tr>
<td style="text-align: left;">bizno</td>
<td style="text-align: left;">사업자번호</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">1238640842</td>
<td style="text-align: left;">검색하고자 하는 업체의 사업자번호</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 응답 메시지 명세

<table style="width:100%;">
<colgroup>
<col style="width: 21%" />
<col style="width: 21%" />
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 13%" />
<col style="width: 20%" />
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
<td>numOfRows</td>
<td>한 페이지 결과 수</td>
<td>4</td>
<td>1</td>
<td>10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td>pageNo</td>
<td>페이지 번호</td>
<td>4</td>
<td>1</td>
<td>1</td>
<td style="text-align: left;">페이지 수</td>
</tr>
<tr>
<td>totalCount</td>
<td>데이터 총 개수</td>
<td>4</td>
<td>1</td>
<td>10</td>
<td style="text-align: left;">데이터 총 개수</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNo</td>
<td>입찰공고번호</td>
<td>40</td>
<td style="text-align: left;">1</td>
<td>R25BK00927163</td>
<td style="text-align: left;">입찰공고 관리번호이며 조달청나라장터 공고건의 형식은 년도(4)+월(2)+순번(5)이며 자체전자조달시스템 보유기관은 각 기관별 형식 별도 사용<br />
*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성<br />
- 단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceOrd</td>
<td>입찰공고차수</td>
<td>3</td>
<td style="text-align: left;">1</td>
<td>000</td>
<td style="text-align: left;">입찰공고차수는 해당 입찰공고에 대한 재공고 및 재입찰 등이 발생되었을 경우 증가되는 수</td>
</tr>
<tr>
<td>bidClsfcNo</td>
<td>입찰분류번호</td>
<td>5</td>
<td style="text-align: left;">1</td>
<td>0</td>
<td style="text-align: left;">동일한 입찰공고번호에 대한 집행일련번호</td>
</tr>
<tr>
<td>rbidNo</td>
<td>재입찰번호</td>
<td>3</td>
<td style="text-align: left;">1</td>
<td>000</td>
<td style="text-align: left;">재입찰번호</td>
</tr>
<tr>
<td>ntceDivCd</td>
<td>공고구분코드</td>
<td>7</td>
<td style="text-align: left;">1</td>
<td>통050001</td>
<td style="text-align: left;">공고구분<br />
통050001 : 조달청 또는 나라장터 자체 공고건</td>
</tr>
<tr>
<td>bidNtceNm</td>
<td>입찰공고명</td>
<td>1000</td>
<td style="text-align: left;">1</td>
<td>동물원(해양관, 남미관) 종합안내판 변경 제작 시행</td>
<td style="text-align: left;">공사명 또는 사업명이라고도 하며 입찰공고 내용을 요약한 이름</td>
</tr>
<tr>
<td>prtcptCnum</td>
<td>참가업체수</td>
<td>6</td>
<td style="text-align: left;">0</td>
<td>1</td>
<td style="text-align: left;">참가업체수</td>
</tr>
<tr>
<td>bidwinnrNm</td>
<td>최종낙찰업체명</td>
<td>200</td>
<td style="text-align: left;">1</td>
<td>주식회사 나무조각 에코사인</td>
<td style="text-align: left;">최종낙찰된 업체의 명으로 개찰완료된 건에 대하여 제공</td>
</tr>
<tr>
<td>bidwinnrBizno</td>
<td>최종낙찰업체사업자등록번호</td>
<td>10</td>
<td style="text-align: left;">1</td>
<td>1238640842</td>
<td style="text-align: left;">협상이 완료 후 최종낙찰된 업체의 사업자등록번호임</td>
</tr>
<tr>
<td>bidwinnrCeoNm</td>
<td>최종낙찰업체대표자명</td>
<td>35</td>
<td style="text-align: left;">0</td>
<td>조선미</td>
<td style="text-align: left;">최종낙찰된 업체의 대표자명으로 개찰완료된 건에 대하여 제공</td>
</tr>
<tr>
<td>bidwinnrAdrs</td>
<td>최종낙찰업체주소</td>
<td>200</td>
<td style="text-align: left;">0</td>
<td>경기도 화성시 기안말길 17-0 (기안동)</td>
<td style="text-align: left;">협상이 완료 후 최종낙찰된 업체의 주소임</td>
</tr>
<tr>
<td>bidwinnrTelNo</td>
<td>최종낙찰업체전화번호</td>
<td>25</td>
<td style="text-align: left;">0</td>
<td>070-8273-0625</td>
<td style="text-align: left;">협상이 완료 후 최종낙찰된 업체의 연락 전화번호임<br />
핸드폰번호는 “*”로 표기</td>
</tr>
<tr>
<td>sucsfbidAmt</td>
<td>최종낙찰금액</td>
<td>21</td>
<td style="text-align: left;">0</td>
<td>38832000</td>
<td style="text-align: left;">최종낙찰은 개찰순위 순서대로 협상등을 통해 최종 낙찰된정보를 의미하며 최종낙찰금액은 최종낙찰된 금액 (원화,원)으로 개찰완료된건에 대하여 제공</td>
</tr>
<tr>
<td>sucsfbidRate</td>
<td>최종낙찰률</td>
<td>18</td>
<td style="text-align: left;">0</td>
<td>94.999</td>
<td style="text-align: left;">예정가격대비 최종낙찰금액으로 최종낙찰금액/예정가격 * 100 으로 계산되며 개찰완료된 건에 대하여 제공 (%)</td>
</tr>
<tr>
<td>rlOpengDt</td>
<td>실개찰일시</td>
<td>19</td>
<td style="text-align: left;">0</td>
<td>2025-06-30 18:00:00</td>
<td style="text-align: left;">실제 개찰일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td>dminsttCd</td>
<td>수요기관코드</td>
<td>7</td>
<td style="text-align: left;">0</td>
<td>6112581</td>
<td style="text-align: left;">실제 수요기관의 코드로 행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드가 행자부코드가 없는 경우 조달청에서 부여한 수요기관 코드가 표기됨</td>
</tr>
<tr>
<td>dminsttNm</td>
<td>수요기관명</td>
<td>200</td>
<td style="text-align: left;">0</td>
<td>서울특별시 서울대공원</td>
<td style="text-align: left;">중앙조달인 경우 조달사업에 관한 법률 제2조(정의)에 따라 수요물자의 구매 공급 또는 시설공사 계약의 체결을 조달청장에게 요청할 수 있도록 조달청장이 인정하여 등록한 기관 또는 자체전자조달시스템을 이용하는 기관인 경우 계약을 의뢰한 기관의 명으로 공고기관과 수요기관이 동일할 수 있음</td>
</tr>
<tr>
<td style="text-align: left;">rgstDt</td>
<td>등록일시</td>
<td style="text-align: left;">19</td>
<td>1</td>
<td>2025-07-01 13:39:16</td>
<td style="text-align: left;">등록일시 "YYYY-MM-DD HH:MM:SS"</td>
</tr>
<tr>
<td>fnlSucsfDate</td>
<td>최종낙찰일자</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">0</td>
<td>2025-07-01</td>
<td style="text-align: left;">최종낙찰된 일자로 개찰완료된 건에 대하여 제공</td>
</tr>
<tr>
<td>fnlSucsfCorpOfcl</td>
<td>최종낙찰업체담당자</td>
<td style="text-align: left;">35</td>
<td style="text-align: left;">0</td>
<td>N/A</td>
<td>최종낙찰된 업체의 담당자명으로 개찰완료된 건에 대하여 제공</td>
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
<td>REST(URI)</td>
</tr>
<tr>
<td style="text-align: left;">http://apis.data.go.kr/1230000/as/getScsbidListSttusServcPPSSrch?inqryDiv=1&amp;inqryBgnDt=202507010000&amp;inqryEndDt=202507012359&amp;bidNtceNm 동물원(해양관, 남미관) 종합안내판 변경 제작 시행&amp;pageNo=1&amp;numOfRows=10&amp;ServiceKey=인증키</td>
</tr>
<tr>
<td>응답 메시지</td>
</tr>
<tr>
<td><p>&lt;response&gt;</p>
<p>&lt;header&gt;</p>
<p>&lt;resultCode&gt;00&lt;/resultCode&gt;</p>
<p>&lt;resultMsg&gt;정상&lt;/resultMsg&gt;</p>
<p>&lt;/header&gt;</p>
<p>&lt;body&gt;</p>
<p>&lt;items&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00927163&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;0&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;ntceDivCd&gt;통050001&lt;/ntceDivCd&gt;</p>
<p>&lt;bidNtceNm&gt;동물원(해양관, 남미관) 종합안내판 변경 제작 시행&lt;/bidNtceNm&gt;</p>
<p>&lt;prtcptCnum&gt;1&lt;/prtcptCnum&gt;</p>
<p>&lt;bidwinnrNm&gt;주식회사 나무조각 에코사인&lt;/bidwinnrNm&gt;</p>
<p>&lt;bidwinnrBizno&gt;1238640842&lt;/bidwinnrBizno&gt;</p>
<p>&lt;bidwinnrCeoNm&gt;조선미&lt;/bidwinnrCeoNm&gt;</p>
<p>&lt;bidwinnrAdrs&gt;경기도 화성시 기안말길 17-0 (기안동)&lt;/bidwinnrAdrs&gt;</p>
<p>&lt;bidwinnrTelNo&gt;070-8273-0625&lt;/bidwinnrTelNo&gt;</p>
<p>&lt;sucsfbidAmt&gt;38832000&lt;/sucsfbidAmt&gt;</p>
<p>&lt;sucsfbidRate&gt;94.999&lt;/sucsfbidRate&gt;</p>
<p>&lt;rlOpengDt&gt;2025-06-30 18:00:00&lt;/rlOpengDt&gt;</p>
<p>&lt;dminsttCd&gt;6112581&lt;/dminsttCd&gt;</p>
<p>&lt;dminsttNm&gt;서울특별시 서울대공원&lt;/dminsttNm&gt;</p>
<p>&lt;rgstDt&gt;2025-07-01 13:39:16&lt;/rgstDt&gt;</p>
<p>&lt;fnlSucsfDate&gt;2025-07-01&lt;/fnlSucsfDate&gt;</p>
<p>&lt;fnlSucsfCorpOfcl&gt;&lt;/fnlSucsfCorpOfcl&gt;</p>
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

#### \[나라장터 검색조건에 의한 낙찰된 목록 현황 외자조회\] 오퍼레이션 명세

<table style="width:100%;">
<colgroup>
<col style="width: 4%" />
<col style="width: 21%" />
<col style="width: 17%" />
<col style="width: 21%" />
<col style="width: 2%" />
<col style="width: 32%" />
</colgroup>
<tbody>
<tr>
<td rowspan="6">오퍼레이션 정보</td>
<td>오퍼레이션 번호</td>
<td>19</td>
<td>오퍼레이션명(국문)</td>
<td colspan="2">나라장터 검색조건에 의한 낙찰된 목록 현황 외자조회</td>
</tr>
<tr>
<td>오퍼레이션 유형</td>
<td>조회(목록)</td>
<td>오퍼레이션명(영문)</td>
<td colspan="2"><strong>getScsbidListSttusFrgcptPPSSrch</strong></td>
</tr>
<tr>
<td>오퍼레이션 설명</td>
<td colspan="4">검색조건을 공고일시, 개찰일시, 입찰공고번호, 입찰공고명, 공고기관코드, 공고기관명, 수요기관코드, 수요기관명, 참조번호, 참가제한지역코드, 참가제한지역명, 업종코드, 업종명, 추정가격시작, 추정가격종료, 세부품명번호, 다수공급경쟁자여부, 조달요청번호, 국제구분코드로 외자에 대한 나라장터 최종낙찰자 목록(입찰공고번호, 입찰공고명, 참가업체수, 최종낙찰업체명, 사업자번호, 최종낙찰률, 실개찰일시, 수요기관)을 조회</td>
</tr>
<tr>
<td>Call Back URL</td>
<td colspan="4" style="text-align: left;">N/A</td>
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

<table style="width:100%;">
<colgroup>
<col style="width: 19%" />
<col style="width: 19%" />
<col style="width: 13%" />
<col style="width: 11%" />
<col style="width: 14%" />
<col style="width: 19%" />
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
<td>4</td>
<td>1</td>
<td>10</td>
<td>한 페이지 결과 수</td>
</tr>
<tr>
<td>pageNo</td>
<td>페이지 번호</td>
<td>4</td>
<td>1</td>
<td>1</td>
<td>페이지 번호</td>
</tr>
<tr>
<td style="text-align: left;">ServiceKey</td>
<td style="text-align: left;">서비스키</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">공공데이터포털에서 받은 인증키</td>
<td style="text-align: left;">공공데이터포털에서 받은 인증키</td>
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
<td>inqryDiv</td>
<td>조회구분</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td>1</td>
<td>검색하고자하는 조회구분<br />
1:공고게시일시, 2:개찰일시, 3:입찰공고번호</td>
</tr>
<tr>
<td>inqryBgnDt</td>
<td>조회시작일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td>202507010000</td>
<td>검색하고자 하는 조회시작일시 "YYYYMMDDHHMM"<br />
조회구분이 '1'인 경우 공고게시일시 필수, '2'인 경우 개찰일시 필수</td>
</tr>
<tr>
<td>inqryEndDt</td>
<td>조회종료일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td>202507102359</td>
<td>검색하고자 하는 조회종료일시 "YYYYMMDDHHMM"<br />
조회구분이 '1'인 경우 공고게시일시 필수, '2'인 경우 개찰일시 필수</td>
</tr>
<tr>
<td>bidNtceNo</td>
<td>입찰공고번호</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">0</td>
<td>R25BK00857114</td>
<td>검색하고자하는 입찰공고번호<br />
조회구분이 '3'인 경우 필수</td>
</tr>
<tr>
<td>bidNtceNm</td>
<td>입찰공고명</td>
<td style="text-align: left;">1000</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">가스크로마토그래프-질량분석기</td>
<td style="text-align: left;">검색하고자하는 공고명<br />
※ 공고명 일부 입력시에도 조회 가능</td>
</tr>
<tr>
<td>ntceInsttCd</td>
<td>공고기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">1482021</td>
<td style="text-align: left;">검색하고자하는 공고기관코드</td>
</tr>
<tr>
<td>ntceInsttNm</td>
<td>공고기관명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">환경부 국립환경과학원</td>
<td style="text-align: left;">검색하고자하는 공고기관명<br />
※ 공고기관명 일부 입력시에도 조회 가능</td>
</tr>
<tr>
<td>dminsttCd</td>
<td>수요기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">1482021</td>
<td style="text-align: left;"><p>검색하고자하는 수요기관코드</p>
<p>행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드 입력</p>
<p>행자부코드가 없는 경우 조달청에서 부여한 수요기관 코드 입력</p></td>
</tr>
<tr>
<td>dminsttNm</td>
<td>수요기관명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">환경부 국립환경과학원</td>
<td style="text-align: left;">검색하고자하는 수요기관명<br />
※ 수요기관명 일부 입력시에도 조회 가능</td>
</tr>
<tr>
<td>refNo</td>
<td>참조번호</td>
<td style="text-align: left;">105</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25DC00044773</td>
<td style="text-align: left;">검색하고자하는 참조번호</td>
</tr>
<tr>
<td>prtcptLmtRgnCd</td>
<td>참가제한지역코드</td>
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
<td>prtcptLmtRgnNm</td>
<td>참가제한지역명</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">전국</td>
<td style="text-align: left;">검색하고자하는 참가제한지역명<br />
※ 참가제한지역명 일부 입력시에도 조회 가능<br />
*전국 : 지역제한을 설정하지 않은 공고</td>
</tr>
<tr>
<td>indstrytyCd</td>
<td>업종코드</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td>4119</td>
<td>검색하고자하는 업종코드</td>
</tr>
<tr>
<td>indstrytyNm</td>
<td>업종명</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">토목공사업</td>
<td style="text-align: left;">검색하고자하는 업종명<br />
※ 업종명 일부 입력시에도 조회 가능</td>
</tr>
<tr>
<td>presmptPrceBgn</td>
<td>추정가격시작</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">검색하고자하는 추정가격범위시작금액이상(원화,원)</td>
</tr>
<tr>
<td>presmptPrceEnd</td>
<td>추정가격종료</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">검색하고자하는 추정가격범위종료금액이하(원화,원)</td>
</tr>
<tr>
<td>dtilPrdctClsfcNo</td>
<td>세부품명번호</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">4111540401</td>
<td style="text-align: left;">검색하고자하는 세부품명번호</td>
</tr>
<tr>
<td>masYn</td>
<td>다수공급경쟁자여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">N</td>
<td style="text-align: left;">검색하고자하는 다수공급경쟁자여부</td>
</tr>
<tr>
<td>prcrmntReqNo</td>
<td>조달요청번호</td>
<td style="text-align: left;">13</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">R25DC00044773</td>
<td style="text-align: left;">검색하고자하는 조달요청번호</td>
</tr>
<tr>
<td>intrntnlDivCd</td>
<td>국제구분코드</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2</td>
<td style="text-align: left;">검색하고자하는 국제구분코드<br />
국내:1, 국제:2</td>
</tr>
<tr>
<td style="text-align: left;">bizno</td>
<td style="text-align: left;">사업자번호</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">3078701124</td>
<td style="text-align: left;">검색하고자 하는 업체의 사업자번호</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 응답 메시지 명세

<table style="width:100%;">
<colgroup>
<col style="width: 21%" />
<col style="width: 21%" />
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 13%" />
<col style="width: 20%" />
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
<td>numOfRows</td>
<td>한 페이지 결과 수</td>
<td>4</td>
<td>1</td>
<td>10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td>pageNo</td>
<td>페이지 번호</td>
<td>4</td>
<td>1</td>
<td>1</td>
<td style="text-align: left;">페이지 수</td>
</tr>
<tr>
<td>totalCount</td>
<td>데이터 총 개수</td>
<td>4</td>
<td>1</td>
<td>17</td>
<td style="text-align: left;">데이터 총 개수</td>
</tr>
<tr>
<td>bidNtceNo</td>
<td>입찰공고번호</td>
<td>40</td>
<td>1</td>
<td>R25BK00857114</td>
<td style="text-align: left;">입찰공고 관리번호이며 조달청나라장터 공고건의 형식은 년도(4)+월(2)+순번(5)이며 자체전자조달시스템 보유기관은 각 기관별 형식 별도 사용<br />
*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성<br />
- 단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</td>
</tr>
<tr>
<td>bidNtceOrd</td>
<td>입찰공고차수</td>
<td>3</td>
<td style="text-align: left;">1</td>
<td>000</td>
<td style="text-align: left;">입찰공고차수는 해당 입찰공고에 대한 재공고 및 재입찰 등이 발생되었을 경우 증가되는 수</td>
</tr>
<tr>
<td>bidClsfcNo</td>
<td>입찰분류번호</td>
<td>5</td>
<td style="text-align: left;">1</td>
<td>1</td>
<td style="text-align: left;">동일한 입찰공고번호에 대한 집행일련번호</td>
</tr>
<tr>
<td>rbidNo</td>
<td>재입찰번호</td>
<td>3</td>
<td style="text-align: left;">1</td>
<td>000</td>
<td style="text-align: left;">재입찰번호</td>
</tr>
<tr>
<td>ntceDivCd</td>
<td>공고구분코드</td>
<td>7</td>
<td style="text-align: left;">1</td>
<td>통050001</td>
<td style="text-align: left;">공고구분<br />
통050001 : 조달청 또는 나라장터 자체 공고건</td>
</tr>
<tr>
<td>bidNtceNm</td>
<td>입찰공고명</td>
<td>1000</td>
<td style="text-align: left;">1</td>
<td>(외자)가스크로마토그래프-질량분석기</td>
<td style="text-align: left;">공사명 또는 사업명이라고도 하며 입찰공고 내용을 요약한 이름</td>
</tr>
<tr>
<td>prtcptCnum</td>
<td>참가업체수</td>
<td>6</td>
<td style="text-align: left;">0</td>
<td>1</td>
<td style="text-align: left;">참가업체수</td>
</tr>
<tr>
<td>bidwinnrNm</td>
<td>최종낙찰업체명</td>
<td>200</td>
<td style="text-align: left;">1</td>
<td>주식회사 시마즈 사이언티픽 코리아</td>
<td style="text-align: left;">최종낙찰된 업체의 명으로 개찰완료된 건에 대하여 제공</td>
</tr>
<tr>
<td>bidwinnrBizno</td>
<td>최종낙찰업체사업자등록번호</td>
<td>10</td>
<td style="text-align: left;">1</td>
<td>3078701124</td>
<td style="text-align: left;">협상이 완료 후 최종낙찰된 업체의 사업자등록번호임</td>
</tr>
<tr>
<td>bidwinnrCeoNm</td>
<td>최종낙찰업체대표자명</td>
<td>35</td>
<td style="text-align: left;">0</td>
<td>야마다 타케시</td>
<td style="text-align: left;">최종낙찰된 업체의 대표자명으로 개찰완료된 건에 대하여 제공</td>
</tr>
<tr>
<td>bidwinnrAdrs</td>
<td>최종낙찰업체주소</td>
<td>200</td>
<td style="text-align: left;">0</td>
<td>서울특별시 강남구 언주로 609, 9층(논현동 , 팍스타워)</td>
<td style="text-align: left;">협상이 완료 후 최종낙찰된 업체의 주소임</td>
</tr>
<tr>
<td>bidwinnrTelNo</td>
<td>최종낙찰업체전화번호</td>
<td>25</td>
<td style="text-align: left;">0</td>
<td>042-864-1161</td>
<td style="text-align: left;">협상이 완료 후 최종낙찰된 업체의 연락 전화번호임<br />
핸드폰번호는 “*”로 표기</td>
</tr>
<tr>
<td>sucsfbidAmt</td>
<td>최종낙찰금액</td>
<td>21</td>
<td style="text-align: left;">0</td>
<td>27538049</td>
<td style="text-align: left;">최종낙찰은 개찰순위 순서대로 협상등을 통해 최종 낙찰된정보를 의미하며 최종낙찰금액은 최종낙찰된 금액 (원화,원)으로 개찰완료된건에 대하여 제공</td>
</tr>
<tr>
<td>sucsfbidRate</td>
<td>최종낙찰률</td>
<td>18</td>
<td style="text-align: left;">0</td>
<td>0</td>
<td style="text-align: left;">예정가격대비 최종낙찰금액으로 최종낙찰금액/예정가격 * 100 으로 계산되며 개찰완료된 건에 대하여 제공 (%)</td>
</tr>
<tr>
<td>rlOpengDt</td>
<td>실개찰일시</td>
<td>19</td>
<td style="text-align: left;">0</td>
<td>2025-06-05 15:00:00</td>
<td style="text-align: left;">실제 개찰일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td>dminsttCd</td>
<td>수요기관코드</td>
<td>7</td>
<td style="text-align: left;">0</td>
<td>1482021</td>
<td style="text-align: left;">실제 수요기관의 코드로 행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드가 행자부코드가 없는 경우 조달청에서 부여한 수요기관 코드가 표기됨</td>
</tr>
<tr>
<td style="text-align: left;">dminsttNm</td>
<td>수요기관명</td>
<td>200</td>
<td style="text-align: left;">0</td>
<td>환경부 국립환경과학원</td>
<td style="text-align: left;">중앙조달인 경우 조달사업에 관한 법률 제2조(정의)에 따라 수요물자의 구매 공급 또는 시설공사 계약의 체결을 조달청장에게 요청할 수 있도록 조달청장이 인정하여 등록한 기관 또는 자체전자조달시스템을 이용하는 기관인 경우 계약을 의뢰한 기관의 명으로 공고기관과 수요기관이 동일할 수 있음</td>
</tr>
<tr>
<td style="text-align: left;">rgstDt</td>
<td>등록일시</td>
<td style="text-align: left;">19</td>
<td>1</td>
<td>2025-07-07 09:17:48</td>
<td style="text-align: left;">등록일시 "YYYY-MM-DD HH:MM:SS"</td>
</tr>
<tr>
<td>FnlSucsfDate</td>
<td>최종낙찰일자</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">0</td>
<td>2025-07-07</td>
<td style="text-align: left;">최종낙찰된 일자로 개찰완료된 건에 대하여 제공</td>
</tr>
<tr>
<td>fnlSucsfCorpOfcl</td>
<td>최종낙찰업체담당자</td>
<td style="text-align: left;">35</td>
<td style="text-align: left;">0</td>
<td>N/A</td>
<td style="text-align: left;">최종낙찰된 업체의 담당자명으로 개찰완료된 건에 대하여 제공</td>
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
<td>REST(URI)</td>
</tr>
<tr>
<td style="text-align: left;">http://apis.data.go.kr/1230000/as/ScsbidInfoService/getScsbidListSttusFrgcptPPSSrch?inqryDiv=1&amp;inqryBgnDt=202507010000&amp;inqryEndDt=202507012359&amp;bidNtceNm=(외자)가스크로마토그래프-질량분석기 &amp;pageNo=1&amp;numOfRows=10&amp;ServiceKey=인증키</td>
</tr>
<tr>
<td>응답 메시지</td>
</tr>
<tr>
<td><p>&lt;response&gt;</p>
<p>&lt;header&gt;</p>
<p>&lt;resultCode&gt;00&lt;/resultCode&gt;</p>
<p>&lt;resultMsg&gt;정상&lt;/resultMsg&gt;</p>
<p>&lt;/header&gt;</p>
<p>&lt;body&gt;</p>
<p>&lt;items&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00857114&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;1&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;ntceDivCd&gt;통050001&lt;/ntceDivCd&gt;</p>
<p>&lt;bidNtceNm&gt;(외자)가스크로마토그래프-질량분석기&lt;/bidNtceNm&gt;</p>
<p>&lt;prtcptCnum&gt;1&lt;/prtcptCnum&gt;</p>
<p>&lt;bidwinnrNm&gt;주식회사 시마즈 사이언티픽 코리아&lt;/bidwinnrNm&gt;</p>
<p>&lt;bidwinnrBizno&gt;3078701124&lt;/bidwinnrBizno&gt;</p>
<p>&lt;bidwinnrCeoNm&gt;야마다 타케시&lt;/bidwinnrCeoNm&gt;</p>
<p>&lt;bidwinnrAdrs&gt;서울특별시 강남구 언주로 609, 9층(논현동 , 팍스타워)&lt;/bidwinnrAdrs&gt;</p>
<p>&lt;bidwinnrTelNo&gt;042-864-1161&lt;/bidwinnrTelNo&gt;</p>
<p>&lt;sucsfbidAmt&gt;27538049&lt;/sucsfbidAmt&gt;</p>
<p>&lt;sucsfbidRate&gt;&lt;/sucsfbidRate&gt;</p>
<p>&lt;rlOpengDt&gt;2025-06-05 15:00:00&lt;/rlOpengDt&gt;</p>
<p>&lt;dminsttCd&gt;1482021&lt;/dminsttCd&gt;</p>
<p>&lt;dminsttNm&gt;환경부 국립환경과학원&lt;/dminsttNm&gt;</p>
<p>&lt;rgstDt&gt;2025-07-07 09:17:48&lt;/rgstDt&gt;</p>
<p>&lt;fnlSucsfDate&gt;2025-07-07&lt;/fnlSucsfDate&gt;</p>
<p>&lt;fnlSucsfCorpOfcl&gt;&lt;/fnlSucsfCorpOfcl&gt;</p>
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

#### \[나라장터 검색조건에 의한 개찰결과 물품 목록 조회\] 오퍼레이션 명세

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
<td colspan="2">나라장터 검색조건에 의한 개찰결과 물품 목록 조회</td>
</tr>
<tr>
<td>오퍼레이션 유형</td>
<td>조회(목록)</td>
<td>오퍼레이션명(영문)</td>
<td colspan="2"><strong>getOpengResultListInfoThngPPSSrch</strong></td>
</tr>
<tr>
<td>오퍼레이션 설명</td>
<td colspan="4">유찰, 개찰완료, 재입찰건에 대한 개찰결과를 제공하며 검색조건을 공고일시, 개찰일시, 입찰공고번호, 입찰공고명, 공고기관코드, 공고기관명, 수요기관코드, 수요기관명, 참조번호, 참가제한지역코드, 참가제한지역명, 업종코드, 업종명, 추정가격시작, 추정가격종료, 세부품명번호, 다수공급경쟁자여부, 조달요청번호, 국제구분코드로 하여 물품에 대한 나라장터 개찰결과 목록(입찰공고번호, 입찰공고명, 개찰일시, 참가업체수, 개찰업체정보, 진행구분코드명, 입력일시, 예비가격파일존재여부, 공고기관명, 수요기관명)을 조회</td>
</tr>
<tr>
<td>Call Back URL</td>
<td colspan="4" style="text-align: left;">N/A</td>
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
<col style="width: 22%" />
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 14%" />
<col style="width: 20%" />
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
<td>10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td style="text-align: left;">pageNo</td>
<td style="text-align: left;">페이지 번호</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td>1</td>
<td style="text-align: left;">페이지 번호</td>
</tr>
<tr>
<td style="text-align: left;">ServiceKey</td>
<td style="text-align: left;">서비스키</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">공공데이터포털에서 받은 인증키</td>
<td style="text-align: left;">공공데이터포털에서 받은 인증키</td>
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
1..공고일시, 2.개찰일시, 3.입찰공고번호</td>
</tr>
<tr>
<td style="text-align: left;">inqryBgnDt</td>
<td style="text-align: left;">조회시작일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td>202507010000</td>
<td>검색하고자하는 시작일시<br />
'YYYYMMDDHHMM'<br />
조회구분 1,2일 경우 필수</td>
</tr>
<tr>
<td style="text-align: left;">inqryEndDt</td>
<td style="text-align: left;">조회종료일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td>202507012359</td>
<td>검색하고자하는 종료일시<br />
'YYYYMMDDHHMM'<br />
조회구분 1,2일 경우 필수</td>
</tr>
<tr>
<td>bidNtceNo</td>
<td>입찰공고번호</td>
<td style="text-align: left;">11</td>
<td style="text-align: left;">0</td>
<td>R25BK00840922</td>
<td>검색하고자하는 입찰공고번호<br />
조회구분이 '3'인 경우 필수</td>
</tr>
<tr>
<td style="text-align: left;">bidNtceNm</td>
<td style="text-align: left;">입찰공고명</td>
<td style="text-align: left;">1000</td>
<td style="text-align: left;">0</td>
<td>근접전자기장 내성 시험 시스템 구축</td>
<td>검색하고자하는 공고명<br />
※ 공고명 일부 입력시에도 조회 가능</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttCd</td>
<td style="text-align: left;">공고기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td>1230137</td>
<td>검색하고자하는 공고기관코드</td>
</tr>
<tr>
<td style="text-align: left;">ntceInsttNm</td>
<td style="text-align: left;">공고기관명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td>조달청 대구지방조달청</td>
<td>검색하고자하는 공고기관명<br />
※ 공고기관명 일부 입력시에도 조회 가능</td>
</tr>
<tr>
<td style="text-align: left;">dminsttCd</td>
<td style="text-align: left;">수요기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td>Z021943</td>
<td><p>검색하고자하는 수요기관코드</p>
<p>행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드 입력</p>
<p>행자부코드가 없는 경우 조달청에서 부여한 수요기관 코드 입력</p></td>
</tr>
<tr>
<td style="text-align: left;">dminsttNm</td>
<td style="text-align: left;">수요기관명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td>대구경북첨단의료산업진흥재단</td>
<td>검색하고자하는 수요기관명<br />
※ 수요기관명 일부 입력시에도 조회 가능</td>
</tr>
<tr>
<td style="text-align: left;">refNo</td>
<td style="text-align: left;">참조번호</td>
<td style="text-align: left;">105</td>
<td style="text-align: left;">0</td>
<td>곡성군 공고 2019- 1955호</td>
<td>검색하고자하는 참조번호</td>
</tr>
<tr>
<td style="text-align: left;">prtcptLmtRgnCd</td>
<td style="text-align: left;">참가제한지역코드</td>
<td style="text-align: left;">2</td>
<td style="text-align: left;">0</td>
<td>11</td>
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
<td>서울특별시</td>
<td>검색하고자하는 참가제한지역명<br />
※ 참가제한지역명 일부 입력시에도 조회 가능<br />
*전국 : 지역제한을 설정하지 않은 공고</td>
</tr>
<tr>
<td style="text-align: left;">indstrytyCd</td>
<td style="text-align: left;">업종코드</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td>4119</td>
<td>검색하고자하는 업종코드</td>
</tr>
<tr>
<td style="text-align: left;">indstrytyNm</td>
<td style="text-align: left;">업종명</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td>토목공사업</td>
<td>검색하고자하는 업종명<br />
※ 업종명 일부 입력시에도 조회 가능</td>
</tr>
<tr>
<td style="text-align: left;">presmptPrceBgn</td>
<td style="text-align: left;">추정가격시작</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td>171750000</td>
<td>검색하고자하는 추정가격범위시작금액이상(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">presmptPrceEnd</td>
<td style="text-align: left;">추정가격종료</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td>171770000</td>
<td>검색하고자하는 추정가격범위종료금액이하(원화,원)</td>
</tr>
<tr>
<td style="text-align: left;">dtilPrdctClsfcNo</td>
<td style="text-align: left;">세부품명번호</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">0</td>
<td>1112170101</td>
<td>검색하고자하는 세부품명번호</td>
</tr>
<tr>
<td style="text-align: left;">masYn</td>
<td style="text-align: left;">다수공급경쟁자여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td>N</td>
<td>검색하고자하는 다수공급경쟁자여부</td>
</tr>
<tr>
<td style="text-align: left;">prcrmntReqNo</td>
<td style="text-align: left;">조달요청번호</td>
<td style="text-align: left;">13</td>
<td style="text-align: left;">0</td>
<td>R25DC00058294</td>
<td>검색하고자하는 조달요청번호</td>
</tr>
<tr>
<td style="text-align: left;">intrntnlDivCd</td>
<td style="text-align: left;">국제구분코드</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td>1</td>
<td>검색하고자하는 국제구분코드<br />
국내:1, 국제:2</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 응답 메시지 명세

<table>
<colgroup>
<col style="width: 23%" />
<col style="width: 17%" />
<col style="width: 11%" />
<col style="width: 10%" />
<col style="width: 16%" />
<col style="width: 19%" />
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
<td>resultCode</td>
<td>결과코드</td>
<td style="text-align: left;">2</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">00</td>
<td style="text-align: left;">결과코드</td>
</tr>
<tr>
<td>resultMsg</td>
<td>결과메세지</td>
<td style="text-align: left;">50</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">정상.</td>
<td style="text-align: left;">결과메세지</td>
</tr>
<tr>
<td>numOfRows</td>
<td>한 페이지 결과 수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td>pageNo</td>
<td>페이지 번호</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">페이지 번호</td>
</tr>
<tr>
<td>totalCount</td>
<td>데이터 총 개수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">17</td>
<td style="text-align: left;">데이터 총 개수</td>
</tr>
<tr>
<td>bidNtceNo</td>
<td>입찰공고번호</td>
<td style="text-align: left;">11</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">R25BK00840922</td>
<td style="text-align: left;">입찰공고 관리번호이며 조달청나라장터 공고건의 형식은 년도(4)+월(2)+순번(5)이며 자체전자조달시스템 보유기관은 각 기관별 형식 별도 사용<br />
*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성<br />
- 단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</td>
</tr>
<tr>
<td>bidNtceOrd</td>
<td>입찰공고차수</td>
<td style="text-align: left;">3</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">000</td>
<td style="text-align: left;">입찰공고차수는 해당 입찰공고에 대한 재공고 및 재입찰 등이 발생되었을 경우 증가되는 수</td>
</tr>
<tr>
<td>bidClsfcNo</td>
<td>입찰분류번호</td>
<td style="text-align: left;">5</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">동일한 입찰공고번호에 대한 집행일련번호</td>
</tr>
<tr>
<td>rbidNo</td>
<td>재입찰번호</td>
<td style="text-align: left;">3</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">000</td>
<td style="text-align: left;">재입찰번호</td>
</tr>
<tr>
<td>bidNtceNm</td>
<td>입찰공고명</td>
<td style="text-align: left;">1000</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">근접전자기장 내성 시험 시스템 구축</td>
<td style="text-align: left;">공사명 또는 사업명이라고도 하며 입찰공고 내용을 요약한 이름</td>
</tr>
<tr>
<td>opengDt</td>
<td>개찰일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">2025-06-17 11:00:00</td>
<td style="text-align: left;">조달업체가 제출한 입찰서를 개찰하는 일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td>prtcptCnum</td>
<td>참가업체수</td>
<td style="text-align: left;">6</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2</td>
<td style="text-align: left;">참가업체수</td>
</tr>
<tr>
<td>opengCorpInfo</td>
<td>개찰업체정보</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">이엠테스트코리아 주식회사^1428139282^김종인^178750000^97.992</td>
<td style="text-align: left;">개찰업체정보<br />
다수 낙찰자의 경우 ”낙찰예정자 다수”와 개찰순위 1위의 투찰금액과 투찰율<br />
을 보여줌<br />
단일 낙찰자 의 경우 업체명과 사업자번호, 대표자명, 투찰금액, 투찰율을 보여줌<br />
단, 협상에 의한 계약일 경우는 투찰금액,투찰율 안나옴</td>
</tr>
<tr>
<td>progrsDivCdNm</td>
<td>진행구분코드명</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">개찰완료</td>
<td style="text-align: left;">진행구분이<br />
유찰, 개찰완료, 재입찰로 구분 됨</td>
</tr>
<tr>
<td>inptDt</td>
<td>입력일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">2025-07-14 09:57:49</td>
<td style="text-align: left;">입력일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td>rsrvtnPrceFileExistnceYn</td>
<td>예비가격파일존재여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">Y</td>
<td style="text-align: left;">예비가격파일존재여부(Y/N)</td>
</tr>
<tr>
<td>ntceInsttCd</td>
<td>공고기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1230137</td>
<td style="text-align: left;">공고를 하는 기관의 코드로 행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드가 행자부코드가 없는 경우 조달청에서 부여한 수요기관 코드가 표기됨</td>
</tr>
<tr>
<td>ntceInsttNm</td>
<td>공고기관명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">조달청 대구지방조달청</td>
<td style="text-align: left;">수요기관의 의뢰를 받아 공고하는 기관의 명</td>
</tr>
<tr>
<td>dminsttCd</td>
<td>수요기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">Z021943</td>
<td style="text-align: left;">실제 수요기관의 코드로 행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드가 행자부코드가 없는 경우 조달청에서 부여한 수요기관 코드가 표기됨</td>
</tr>
<tr>
<td>dminsttNm</td>
<td>수요기관명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">대구경북첨단의료산업진흥재단</td>
<td style="text-align: left;">중앙조달인 경우 조달사업에 관한 법률 제2조(정의)에 따라 수요물자의 구매 공급 또는 시설공사 계약의 체결을 조달청장에게 요청할 수 있도록 조달청장이 인정하여 등록한 기관 또는 자체전자조달시스템을 이용하는 기관인 경우 계약을 의뢰한 기관의 명으로 공고기관과 수요기관이 동일할 수 있음</td>
</tr>
<tr>
<td style="text-align: left;">opengRsltNtcCntnts</td>
<td style="text-align: left;">개찰결과공지내용</td>
<td style="text-align: left;">4000</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">공지내용참고</td>
<td style="text-align: left;">입찰공고번호, 입찰공고차수, 입찰분류번호, 재입찰번호에 해당하는 공지사항 내용</td>
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
<td>REST(URI)</td>
</tr>
<tr>
<td style="text-align: left;">http://apis.data.go.kr/1230000/as/<strong>ScsbidInfoService</strong>/<strong>getOpengResultListInfoThngPPSSrch</strong>?inqryDiv=1&amp;inqryBgnDt=201605010000&amp;inqryEndDt=201605052359&amp;pageNo=1&amp;numOfRows=10&amp;ServiceKey=인증키</td>
</tr>
<tr>
<td>응답 메시지</td>
</tr>
<tr>
<td><p>&lt;response&gt;</p>
<p>&lt;header&gt;</p>
<p>&lt;resultCode&gt;00&lt;/resultCode&gt;</p>
<p>&lt;resultMsg&gt;정상&lt;/resultMsg&gt;</p>
<p>&lt;/header&gt;</p>
<p>&lt;body&gt;</p>
<p>&lt;items&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;20160505843&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;00&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;1&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;0&lt;/rbidNo&gt;</p>
<p>&lt;bidNtceNm&gt;중앙제어실 GATEWAY 구매설치&lt;/bidNtceNm&gt;</p>
<p>&lt;opengDt&gt;2016-05-17 10:00:00&lt;/opengDt&gt;</p>
<p>&lt;prtcptCnum&gt;5&lt;/prtcptCnum&gt;</p>
<p>&lt;opengCorpInfo&gt;(주)디스엔지니어링^2208619067^남병단^11769000^89.842&lt;/opengCorpInfo&gt;</p>
<p>&lt;progrsDivCdNm&gt;개찰완료&lt;/progrsDivCdNm&gt;</p>
<p>&lt;inptDt&gt;2016-05-17 10:05:09&lt;/inptDt&gt;</p>
<p>&lt;rsrvtnPrceFileExistnceYn&gt;Y&lt;/rsrvtnPrceFileExistnceYn&gt;</p>
<p>&lt;ntceInsttCd&gt;6110136&lt;/ntceInsttCd&gt;</p>
<p>&lt;ntceInsttNm&gt;서울특별시 상수도사업본부 강동수도사업소&lt;/ntceInsttNm&gt;</p>
<p>&lt;dminsttCd&gt;6110136&lt;/dminsttCd&gt;</p>
<p>&lt;dminsttNm&gt;서울특별시 상수도사업본부 강동수도사업소&lt;/dminsttNm&gt;</p>
<p>&lt;opengRsltNtcCntnts / &gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;20160503769&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;00&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;1&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;0&lt;/rbidNo&gt;</p>
<p>&lt;bidNtceNm&gt;광학(RapidEye) 위성영상 조달 구매&lt;/bidNtceNm&gt;</p>
<p>&lt;opengDt&gt;2016-05-10 16:00:00&lt;/opengDt&gt;</p>
<p>&lt;prtcptCnum&gt;1&lt;/prtcptCnum&gt;</p>
<p>&lt;opengCorpInfo&gt;주식회사 지오포커스^1358600090^윤병현^133300000^99.925&lt;/opengCorpInfo&gt;</p>
<p>&lt;progrsDivCdNm&gt;개찰완료&lt;/progrsDivCdNm&gt;</p>
<p>&lt;inptDt&gt;2016-05-10 17:09:10&lt;/inptDt&gt;</p>
<p>&lt;rsrvtnPrceFileExistnceYn&gt;Y&lt;/rsrvtnPrceFileExistnceYn&gt;</p>
<p>&lt;ntceInsttCd&gt;1230152&lt;/ntceInsttCd&gt;</p>
<p>&lt;ntceInsttNm&gt;조달청 전북지방조달청&lt;/ntceInsttNm&gt;</p>
<p>&lt;dminsttCd&gt;1390802&lt;/dminsttCd&gt;</p>
<p>&lt;dminsttNm&gt;농촌진흥청 국립농업과학원&lt;/dminsttNm&gt;</p>
<p>&lt;opengRsltNtcCntnts / &gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;20160505826&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;00&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;1&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;0&lt;/rbidNo&gt;</p>
<p>&lt;bidNtceNm&gt;연소시험용 점화추진제 구매&lt;/bidNtceNm&gt;</p>
<p>&lt;opengDt&gt;2016-05-09 16:00:00&lt;/opengDt&gt;</p>
<p>&lt;prtcptCnum&gt;0&lt;/prtcptCnum&gt;</p>
<p>&lt;opengCorpInfo /&gt;</p>
<p>&lt;progrsDivCdNm&gt;유찰&lt;/progrsDivCdNm&gt;</p>
<p>&lt;inptDt&gt;2016-05-10 14:53:58&lt;/inptDt&gt;</p>
<p>&lt;rsrvtnPrceFileExistnceYn&gt;N&lt;/rsrvtnPrceFileExistnceYn&gt;</p>
<p>&lt;ntceInsttCd&gt;Z004843&lt;/ntceInsttCd&gt;</p>
<p>&lt;ntceInsttNm&gt;한국항공우주연구원&lt;/ntceInsttNm&gt;</p>
<p>&lt;dminsttCd&gt;Z004843&lt;/dminsttCd&gt;</p>
<p>&lt;dminsttNm&gt;한국항공우주연구원&lt;/dminsttNm&gt;</p>
<p>&lt;opengRsltNtcCntnts&gt;본 건은 최종낙찰자가 없습니다. 사유 : 적격자없음&lt;/opengRsltNtcCntnts&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;/items&gt;</p>
<p>&lt;numOfRows&gt;10&lt;/numOfRows&gt;</p>
<p>&lt;pageNo&gt;1&lt;/pageNo&gt;</p>
<p>&lt;totalCount&gt;1684&lt;/totalCount&gt;</p>
<p>&lt;/body&gt;</p>
<p>&lt;/response&gt;</p></td>
</tr>
</tbody>
</table>

#### \[나라장터 검색조건에 의한 개찰결과 공사 목록 조회\] 오퍼레이션 명세

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
<td colspan="2">나라장터 검색조건에 의한 개찰결과 공사 목록 조회</td>
</tr>
<tr>
<td>오퍼레이션 유형</td>
<td>조회(목록)</td>
<td>오퍼레이션명(영문)</td>
<td colspan="2"><strong>getOpengResultListInfoCnstwkPPSSrch</strong></td>
</tr>
<tr>
<td>오퍼레이션 설명</td>
<td colspan="4">유찰, 개찰완료, 재입찰건에 대한 개찰결과를 제공하며 검색조건을 공고일시, 개찰일시, 입찰공고번호, 입찰공고명, 공고기관코드, 공고기관명, 수요기관코드, 수요기관명, 참조번호, 참가제한지역코드, 참가제한지역명, 업종코드, 업종명, 추정가격시작, 추정가격종료, 세부품명번호, 다수공급경쟁자여부, 조달요청번호, 국제구분코드로 하여 공사에 대한 나라장터 개찰결과 목록(입찰공고번호, 입찰공고명, 개찰일시, 참가업체수, 개찰업체정보, 진행구분코드명, 입력일시, 예비가격파일존재여부, 공고기관명, 수요기관명)을 조회</td>
</tr>
<tr>
<td>Call Back URL</td>
<td colspan="4" style="text-align: left;">N/A</td>
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
<col style="width: 11%" />
<col style="width: 12%" />
<col style="width: 22%" />
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
<td>4</td>
<td>1</td>
<td>10</td>
<td>한 페이지 결과 수</td>
</tr>
<tr>
<td>pageNo</td>
<td>페이지 번호</td>
<td>4</td>
<td>1</td>
<td>1</td>
<td>페이지 번호</td>
</tr>
<tr>
<td style="text-align: left;">ServiceKey</td>
<td style="text-align: left;">서비스키</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">공공데이터포털에서 받은 인증키</td>
<td style="text-align: left;">공공데이터포털에서 받은 인증키</td>
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
<td>조회구분</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">검색하고자하는 조회구분<br />
1.공고일시,2.개찰일시,3.입찰공고번호</td>
</tr>
<tr>
<td>inqryBgnDt</td>
<td>조회시작일시</td>
<td>12</td>
<td style="text-align: left;">0</td>
<td>202507010000</td>
<td>검색하고자하는 시작일시<br />
'YYYYMMDDHHMM'<br />
조회구분 1,2일 경우 필수</td>
</tr>
<tr>
<td>inqryEndDt</td>
<td>조회종료일시</td>
<td>12</td>
<td style="text-align: left;">0</td>
<td>202507012359</td>
<td>검색하고자하는 종료일시<br />
'YYYYMMDDHHMM'<br />
조회구분 1,2일 경우 필수</td>
</tr>
<tr>
<td>bidNtceNo</td>
<td>입찰공고번호</td>
<td style="text-align: left;">11</td>
<td style="text-align: left;">0</td>
<td>R25BK00926014</td>
<td>검색하고자하는 입찰공고번호<br />
조회구분이 '3'인 경우 필수</td>
</tr>
<tr>
<td>bidNtceNm</td>
<td>입찰공고명</td>
<td style="text-align: left;">1000</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">낭주중학교 인조 잔디 조성 및 담장 교체 공사 입찰 공고[긴급]</td>
<td style="text-align: left;">검색하고자하는 공고명<br />
※ 공고명 일부 입력시에도 조회 가능</td>
</tr>
<tr>
<td>ntceInsttCd</td>
<td>공고기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">8462058</td>
<td style="text-align: left;">검색하고자하는 공고기관코드</td>
</tr>
<tr>
<td>ntceInsttNm</td>
<td>공고기관명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">전북특별자치도교육청 전북특별자치도부안교육지원청 낭주중학교</td>
<td style="text-align: left;">검색하고자하는 공고기관명<br />
※ 공고기관명 일부 입력시에도 조회 가능</td>
</tr>
<tr>
<td>dminsttCd</td>
<td>수요기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">8462058</td>
<td style="text-align: left;"><p>검색하고자하는 수요기관코드</p>
<p>행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드 입력</p>
<p>행자부코드가 없는 경우 조달청에서 부여한 수요기관 코드 입력</p></td>
</tr>
<tr>
<td>dminsttNm</td>
<td>수요기관명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td>전북특별자치도교육청 전북특별자치도부안교육지원청 낭주중학교</td>
<td style="text-align: left;">검색하고자하는 수요기관명<br />
※ 수요기관명 일부 입력시에도 조회 가능</td>
</tr>
<tr>
<td>refNo</td>
<td>참조번호</td>
<td style="text-align: left;">105</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">전북특별자치도부안교육지원청 낭주중학교 공고 제2025 - 11호</td>
<td style="text-align: left;">검색하고자하는 참조번호</td>
</tr>
<tr>
<td>prtcptLmtRgnCd</td>
<td>참가제한지역코드</td>
<td style="text-align: left;">2</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">50</td>
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
<td>prtcptLmtRgnNm</td>
<td>참가제한지역명</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">제주</td>
<td style="text-align: left;">검색하고자하는 참가제한지역명<br />
※ 참가제한지역명 일부 입력시에도 조회 가능<br />
*전국 : 지역제한을 설정하지 않은 공고</td>
</tr>
<tr>
<td>indstrytyCd</td>
<td>업종코드</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td>0006</td>
<td>검색하고자하는 업종코드</td>
</tr>
<tr>
<td>indstrytyNm</td>
<td>업종명</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">실내건축공사업</td>
<td style="text-align: left;">검색하고자하는 업종명<br />
※ 업종명 일부 입력시에도 조회 가능</td>
</tr>
<tr>
<td>presmptPrceBgn</td>
<td>추정가격시작</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">475700000</td>
<td style="text-align: left;">검색하고자하는 추정가격범위시작금액이상(원화,원)</td>
</tr>
<tr>
<td>presmptPrceEnd</td>
<td>추정가격종료</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">475800000</td>
<td style="text-align: left;">검색하고자하는 추정가격범위종료금액이하(원화,원)</td>
</tr>
<tr>
<td>dtilPrdctClsfcNo</td>
<td>세부품명번호</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">1012159801</td>
<td style="text-align: left;">검색하고자하는 세부품명번호</td>
</tr>
<tr>
<td>masYn</td>
<td>다수공급경쟁자여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">Y</td>
<td style="text-align: left;">검색하고자하는 다수공급경쟁자여부</td>
</tr>
<tr>
<td>prcrmntReqNo</td>
<td>조달요청번호</td>
<td style="text-align: left;">13</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">검색하고자하는 조달요청번호</td>
</tr>
<tr>
<td>intrntnlDivCd</td>
<td>국제구분코드</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">검색하고자하는 국제구분코드<br />
국내:1, 국제:2</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 응답 메시지 명세

<table style="width:100%;">
<colgroup>
<col style="width: 23%" />
<col style="width: 16%" />
<col style="width: 12%" />
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 18%" />
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
<td>resultCode</td>
<td>결과코드</td>
<td style="text-align: left;">2</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">00</td>
<td>결과코드</td>
</tr>
<tr>
<td>resultMsg</td>
<td>결과메세지</td>
<td style="text-align: left;">50</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">정상.</td>
<td>결과메세지</td>
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
<td>totalCount</td>
<td>데이터 총 개수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td>17</td>
<td>데이터 총 개수</td>
</tr>
<tr>
<td>bidNtceNo</td>
<td>입찰공고번호</td>
<td style="text-align: left;">11</td>
<td style="text-align: left;">1</td>
<td>R25BK00926014</td>
<td style="text-align: left;">입찰공고 관리번호이며 조달청나라장터 공고건의 형식은 년도(4)+월(2)+순번(5)이며 자체전자조달시스템 보유기관은 각 기관별 형식 별도 사용<br />
*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성<br />
- 단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</td>
</tr>
<tr>
<td>bidNtceOrd</td>
<td>입찰공고차수</td>
<td style="text-align: left;">3</td>
<td style="text-align: left;">1</td>
<td>000</td>
<td style="text-align: left;">입찰공고 관리번호이며 조달청나라장터 공고건의 형식은 년도(4)+월(2)+순번(5)이며 자체전자조달시스템 보유기관은 각 기관별 형식 별도 사용<br />
*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성<br />
- 단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</td>
</tr>
<tr>
<td>bidClsfcNo</td>
<td>입찰분류번호</td>
<td style="text-align: left;">5</td>
<td style="text-align: left;">1</td>
<td>0</td>
<td>동일한 입찰공고번호에 대한 집행일련번호</td>
</tr>
<tr>
<td>rbidNo</td>
<td>재입찰번호</td>
<td style="text-align: left;">3</td>
<td style="text-align: left;">1</td>
<td>000</td>
<td>재입찰번호</td>
</tr>
<tr>
<td>bidNtceNm</td>
<td>입찰공고명</td>
<td style="text-align: left;">1000</td>
<td style="text-align: left;">1</td>
<td>낭주중학교 인조 잔디 조성 및 담장 교체 공사 입찰 공고[긴급]</td>
<td>공사명 또는 사업명이라고도 하며 입찰공고 내용을 요약한 이름</td>
</tr>
<tr>
<td>opengDt</td>
<td>개찰일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">1</td>
<td>2025-07-01 11:00:00</td>
<td>조달업체가 제출한 입찰서를 개찰하는 일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td>prtcptCnum</td>
<td>참가업체수</td>
<td style="text-align: left;">6</td>
<td style="text-align: left;">0</td>
<td>374</td>
<td>참가업체수</td>
</tr>
<tr>
<td>opengCorpInfo</td>
<td>개찰업체정보</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">1</td>
<td>유한회사 진무건설^4028138623^이세윤^462119000^88.393</td>
<td>개찰업체정보<br />
다수 낙찰자의 경우 ”낙찰예정자 다수”와 개찰순위 1위의 투찰금액과 투찰율<br />
을 보여줌<br />
단일 낙찰자 의 경우 업체명과 사업자번호, 대표자명, 투찰금액, 투찰율을 보여줌<br />
단, 협상에 의한 계약일 경우는 투찰금액,투찰율 안나옴</td>
</tr>
<tr>
<td>progrsDivCdNm</td>
<td>진행구분코드명</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td>개찰완료</td>
<td>진행구분이<br />
유찰, 개찰완료, 재입찰로 구분 됨</td>
</tr>
<tr>
<td>inptDt</td>
<td>입력일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td>2025-07-01 11:08:48</td>
<td>입력일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td>rsrvtnPrceFileExistnceYn</td>
<td>예비가격파일존재여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td>Y</td>
<td>예비가격파일존재여부(Y/N)</td>
</tr>
<tr>
<td>ntceInsttCd</td>
<td>공고기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">1</td>
<td>8462058</td>
<td>공고를 하는 기관의 코드로 행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드가 행자부코드가 없는 경우 조달청에서 부여한 수요기관 코드가 표기됨</td>
</tr>
<tr>
<td>ntceInsttNm</td>
<td>공고기관명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td>전북특별자치도교육청 전북특별자치도부안교육지원청 낭주중학교</td>
<td>수요기관의 의뢰를 받아 공고하는 기관의 명</td>
</tr>
<tr>
<td>dminsttCd</td>
<td>수요기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td>8462058</td>
<td>실제 수요기관의 코드로 행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드가 행자부코드가 없는 경우 조달청에서 부여한 수요기관 코드가 표기됨</td>
</tr>
<tr>
<td>dminsttNm</td>
<td>수요기관명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td>전북특별자치도교육청 전북특별자치도부안교육지원청 낭주중학교</td>
<td>중앙조달인 경우 조달사업에 관한 법률 제2조(정의)에 따라 수요물자의 구매 공급 또는 시설공사 계약의 체결을 조달청장에게 요청할 수 있도록 조달청장이 인정하여 등록한 기관 또는 자체전자조달시스템을 이용하는 기관인 경우 계약을 의뢰한 기관의 명으로 공고기관과 수요기관이 동일할 수 있음</td>
</tr>
<tr>
<td style="text-align: left;">opengRsltNtcCntnts</td>
<td style="text-align: left;">개찰결과공지내용</td>
<td style="text-align: left;">4000</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">개찰완료되었습니다.</td>
<td style="text-align: left;">입찰공고번호, 입찰공고차수, 입찰분류번호, 재입찰번호에 해당하는 공지사항 내용</td>
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
<td>REST(URI)</td>
</tr>
<tr>
<td style="text-align: left;">http://apis.data.go.kr/1230000/as/<strong>ScsbidInfoService</strong>/<strong>getOpengResultListInfoCnstwkPPSSrch</strong>?inqryDiv=1&amp;inqryBgnDt=201605010000&amp;inqryEndDt=201605052359&amp;pageNo=1&amp;numOfRows=10&amp;ServiceKey=인증키</td>
</tr>
<tr>
<td>응답 메시지</td>
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
<p>&lt;bidNtceNo&gt;R25BK00926014&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;0&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;bidNtceNm&gt;낭주중학교 인조 잔디 조성 및 담장 교체 공사 입찰 공고[긴급]&lt;/bidNtceNm&gt;</p>
<p>&lt;opengDt&gt;2025-07-01 11:00:00&lt;/opengDt&gt;</p>
<p>&lt;prtcptCnum&gt;374&lt;/prtcptCnum&gt;</p>
<p>&lt;opengCorpInfo&gt;유한회사 진무건설^4028138623^이세윤^462119000^88.393&lt;/opengCorpInfo&gt;</p>
<p>&lt;progrsDivCdNm&gt;개찰완료&lt;/progrsDivCdNm&gt;</p>
<p>&lt;inptDt&gt;2025-07-01 11:08:48&lt;/inptDt&gt;</p>
<p>&lt;rsrvtnPrceFileExistnceYn&gt;Y&lt;/rsrvtnPrceFileExistnceYn&gt;</p>
<p>&lt;ntceInsttCd&gt;8462058&lt;/ntceInsttCd&gt;</p>
<p>&lt;ntceInsttNm&gt;전북특별자치도교육청 전북특별자치도부안교육지원청 낭주중학교&lt;/ntceInsttNm&gt;</p>
<p>&lt;dminsttCd&gt;8462058&lt;/dminsttCd&gt;</p>
<p>&lt;dminsttNm&gt;전북특별자치도교육청 전북특별자치도부안교육지원청 낭주중학교&lt;/dminsttNm&gt;</p>
<p>&lt;opengRsltNtcCntnts&gt;&lt;/opengRsltNtcCntnts&gt;</p>
<p>&lt;/item&gt;</p>
<p>&lt;/items&gt;</p>
<p>&lt;numOfRows&gt;999&lt;/numOfRows&gt;</p>
<p>&lt;pageNo&gt;1&lt;/pageNo&gt;</p>
<p>&lt;totalCount&gt;1&lt;/totalCount&gt;</p>
<p>&lt;/body&gt;</p>
<p>&lt;/response</p></td>
</tr>
</tbody>
</table>

#### \[나라장터 검색조건에 의한 개찰결과 용역 목록 조회\] 오퍼레이션 명세

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
<td colspan="2">나라장터 검색조건에 의한 개찰결과 용역 목록 조회</td>
</tr>
<tr>
<td>오퍼레이션 유형</td>
<td>조회(목록)</td>
<td>오퍼레이션명(영문)</td>
<td colspan="2"><strong>getOpengResultListInfoServcPPSSrch</strong></td>
</tr>
<tr>
<td>오퍼레이션 설명</td>
<td colspan="4">유찰, 개찰완료, 재입찰건에 대한 개찰결과를 제공하며 검색조건을 공고일시, 개찰일시, 입찰공고번호, 입찰공고명, 공고기관코드, 공고기관명, 수요기관코드, 수요기관명, 참조번호, 참가제한지역코드, 참가제한지역명, 업종코드, 업종명, 추정가격시작, 추정가격종료, 세부품명번호, 다수공급경쟁자여부, 조달요청번호, 국제구분코드로하여 용역에 대한 나라장터 개찰결과 목록(입찰공고번호, 입찰공고명, 개찰일시, 참가업체수, 개찰업체정보, 진행구분코드명, 입력일시, 예비가격파일존재여부, 공고기관명, 수요기관명)을 조회</td>
</tr>
<tr>
<td>Call Back URL</td>
<td colspan="4" style="text-align: left;">N/A</td>
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
<col style="width: 11%" />
<col style="width: 12%" />
<col style="width: 22%" />
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
<td>4</td>
<td>1</td>
<td>10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td>pageNo</td>
<td>페이지 번호</td>
<td>4</td>
<td>1</td>
<td>1</td>
<td style="text-align: left;">페이지 번호</td>
</tr>
<tr>
<td style="text-align: left;">ServiceKey</td>
<td style="text-align: left;">서비스키</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">공공데이터포털에서 받은 인증키</td>
<td style="text-align: left;">공공데이터포털에서 받은 인증키</td>
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
<td>조회구분</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">검색하고자하는 조회구분<br />
1.공고일시,2.개찰일시,3.입찰공고번호</td>
</tr>
<tr>
<td>inqryBgnDt</td>
<td>조회시작일시</td>
<td>12</td>
<td style="text-align: left;">0</td>
<td>20250701000</td>
<td>검색하고자하는 시작일시<br />
'YYYYMMDDHHMM'<br />
조회구분 1,2일 경우 필수</td>
</tr>
<tr>
<td>inqryEndDt</td>
<td>조회종료일시</td>
<td>12</td>
<td style="text-align: left;">0</td>
<td>202507012359</td>
<td>검색하고자하는 종료일시<br />
'YYYYMMDDHHMM'<br />
조회구분 1,2일 경우 필수</td>
</tr>
<tr>
<td>bidNtceNo</td>
<td>입찰공고번호</td>
<td style="text-align: left;">11</td>
<td style="text-align: left;">0</td>
<td>R25BK00882586</td>
<td>검색하고자하는 입찰공고번호<br />
조회구분이 '3'인 경우 필수</td>
</tr>
<tr>
<td>bidNtceNm</td>
<td>입찰공고명</td>
<td style="text-align: left;">1000</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">한국생명공학연구원 지역조직 중기 발전전략 수립</td>
<td style="text-align: left;">검색하고자하는 공고명<br />
※ 공고명 일부 입력시에도 조회 가능</td>
</tr>
<tr>
<td>ntceInsttCd</td>
<td>공고기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">Z004836</td>
<td style="text-align: left;">검색하고자하는 공고기관코드</td>
</tr>
<tr>
<td>ntceInsttNm</td>
<td>공고기관명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">한국생명공학연구원</td>
<td style="text-align: left;">검색하고자하는 공고기관명<br />
※ 공고기관명 일부 입력시에도 조회 가능</td>
</tr>
<tr>
<td>dminsttCd</td>
<td>수요기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">Z004836</td>
<td style="text-align: left;"><p>검색하고자하는 수요기관코드</p>
<p>행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드 입력</p>
<p>행자부코드가 없는 경우 조달청에서 부여한 수요기관 코드 입력</p></td>
</tr>
<tr>
<td>dminsttNm</td>
<td>수요기관명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">한국생명공학연구원</td>
<td style="text-align: left;">검색하고자하는 수요기관명<br />
※ 수요기관명 일부 입력시에도 조회 가능</td>
</tr>
<tr>
<td>refNo</td>
<td>참조번호</td>
<td style="text-align: left;">105</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">제20250602-용-1호</td>
<td style="text-align: left;">검색하고자하는 참조번호</td>
</tr>
<tr>
<td>prtcptLmtRgnCd</td>
<td>참가제한지역코드</td>
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
<td>prtcptLmtRgnNm</td>
<td>참가제한지역명</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">전국</td>
<td style="text-align: left;">검색하고자하는 참가제한지역명<br />
※ 참가제한지역명 일부 입력시에도 조회 가능<br />
*전국 : 지역제한을 설정하지 않은 공고</td>
</tr>
<tr>
<td>indstrytyCd</td>
<td>업종코드</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td>1261</td>
<td>검색하고자하는 업종코드</td>
</tr>
<tr>
<td>indstrytyNm</td>
<td>업종명</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">종합여행업</td>
<td style="text-align: left;">검색하고자하는 업종명<br />
※ 업종명 일부 입력시에도 조회 가능</td>
</tr>
<tr>
<td>presmptPrceBgn</td>
<td>추정가격시작</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">72550000</td>
<td style="text-align: left;">검색하고자하는 추정가격범위시작금액이상(원화,원)</td>
</tr>
<tr>
<td>presmptPrceEnd</td>
<td>추정가격종료</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">72590000</td>
<td style="text-align: left;">검색하고자하는 추정가격범위종료금액이하(원화,원)</td>
</tr>
<tr>
<td>dtilPrdctClsfcNo</td>
<td>세부품명번호</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">1012159801</td>
<td style="text-align: left;">검색하고자하는 세부품명번호</td>
</tr>
<tr>
<td>masYn</td>
<td>다수공급경쟁자여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">Y</td>
<td style="text-align: left;">검색하고자하는 다수공급경쟁자여부</td>
</tr>
<tr>
<td>prcrmntReqNo</td>
<td>조달요청번호</td>
<td style="text-align: left;">13</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">800</td>
<td style="text-align: left;">검색하고자하는 조달요청번호</td>
</tr>
<tr>
<td>intrntnlDivCd</td>
<td>국제구분코드</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">검색하고자하는 국제구분코드<br />
국내:1, 국제:2</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 응답 메시지 명세

<table style="width:100%;">
<colgroup>
<col style="width: 23%" />
<col style="width: 16%" />
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 18%" />
<col style="width: 18%" />
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
<td>resultCode</td>
<td>결과코드</td>
<td style="text-align: left;">2</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">00</td>
<td>결과코드</td>
</tr>
<tr>
<td>resultMsg</td>
<td>결과메세지</td>
<td style="text-align: left;">50</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">정상.</td>
<td>결과메세지</td>
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
<td>totalCount</td>
<td>데이터 총 개수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td>17</td>
<td>데이터 총 개수</td>
</tr>
<tr>
<td>bidNtceNo</td>
<td>입찰공고번호</td>
<td style="text-align: left;">11</td>
<td style="text-align: left;">1</td>
<td>R25BK00882586</td>
<td style="text-align: left;">입찰공고 관리번호이며 조달청나라장터 공고건의 형식은 년도(4)+월(2)+순번(5)이며 자체전자조달시스템 보유기관은 각 기관별 형식 별도 사용<br />
*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성<br />
- 단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</td>
</tr>
<tr>
<td>bidNtceOrd</td>
<td>입찰공고차수</td>
<td style="text-align: left;">3</td>
<td style="text-align: left;">1</td>
<td>000</td>
<td>입찰공고차수는 해당 입찰공고에 대한 재공고 및 재입찰 등이 발생되었을 경우 증가되는 수</td>
</tr>
<tr>
<td>bidClsfcNo</td>
<td>입찰분류번호</td>
<td style="text-align: left;">5</td>
<td style="text-align: left;">1</td>
<td>1</td>
<td>동일한 입찰공고번호에 대한 집행일련번호</td>
</tr>
<tr>
<td>rbidNo</td>
<td>재입찰번호</td>
<td style="text-align: left;">3</td>
<td style="text-align: left;">1</td>
<td>000</td>
<td>재입찰번호</td>
</tr>
<tr>
<td>bidNtceNm</td>
<td>입찰공고명</td>
<td style="text-align: left;">1000</td>
<td style="text-align: left;">1</td>
<td>한국생명공학연구원 지역조직 중기 발전전략 수립</td>
<td>공사명 또는 사업명이라고도 하며 입찰공고 내용을 요약한 이름</td>
</tr>
<tr>
<td>opengDt</td>
<td>개찰일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">1</td>
<td>2025-06-13 11:00:00</td>
<td>조달업체가 제출한 입찰서를 개찰하는 일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td>prtcptCnum</td>
<td>참가업체수</td>
<td style="text-align: left;">6</td>
<td style="text-align: left;">0</td>
<td>2</td>
<td>참가업체수</td>
</tr>
<tr>
<td>opengCorpInfo</td>
<td>개찰업체정보</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">1</td>
<td>(주식회사 과학기술전략연구소^5088702880^유경만^72000000^0</td>
<td>개찰업체정보<br />
다수 낙찰자의 경우 ”낙찰예정자 다수”와 개찰순위 1위의 투찰금액과 투찰율<br />
을 보여줌<br />
단일 낙찰자 의 경우 업체명과 사업자번호, 대표자명, 투찰금액, 투찰율을 보여줌<br />
단, 협상에 의한 계약일 경우는 투찰금액,투찰율 안나옴</td>
</tr>
<tr>
<td>progrsDivCdNm</td>
<td>진행구분코드명</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td>개찰완료</td>
<td>진행구분이<br />
유찰, 개찰완료, 재입찰로 구분 됨</td>
</tr>
<tr>
<td>inptDt</td>
<td>입력일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td>2025-07-01 16:52:39</td>
<td>입력일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td>rsrvtnPrceFileExistnceYn</td>
<td>예비가격파일존재여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td>N</td>
<td>예비가격파일존재여부(Y/N)</td>
</tr>
<tr>
<td>ntceInsttCd</td>
<td>공고기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">1</td>
<td>Z004836</td>
<td>공고를 하는 기관의 코드로 행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드가 행자부코드가 없는 경우 조달청에서 부여한 수요기관 코드가 표기됨</td>
</tr>
<tr>
<td>ntceInsttNm</td>
<td>공고기관명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td>한국생명공학연구원</td>
<td>수요기관의 의뢰를 받아 공고하는 기관의 명</td>
</tr>
<tr>
<td>dminsttCd</td>
<td>수요기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td>Z004836</td>
<td>실제 수요기관의 코드로 행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드가 행자부코드가 없는 경우 조달청에서 부여한 수요기관 코드가 표기됨</td>
</tr>
<tr>
<td>dminsttNm</td>
<td>수요기관명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td>한국생명공학연구원</td>
<td>중앙조달인 경우 조달사업에 관한 법률 제2조(정의)에 따라 수요물자의 구매 공급 또는 시설공사 계약의 체결을 조달청장에게 요청할 수 있도록 조달청장이 인정하여 등록한 기관 또는 자체전자조달시스템을 이용하는 기관인 경우 계약을 의뢰한 기관의 명으로 공고기관과 수요기관이 동일할 수 있음</td>
</tr>
<tr>
<td style="text-align: left;">opengRsltNtcCntnts</td>
<td style="text-align: left;">개찰결과공지내용</td>
<td style="text-align: left;">4000</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">개찰결과공지내용</td>
<td style="text-align: left;">입찰공고번호, 입찰공고차수, 입찰분류번호, 재입찰번호에 해당하는 공지사항 내용</td>
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
<td>REST(URI)</td>
</tr>
<tr>
<td style="text-align: left;">http://apis.data.go.kr/1230000/as/<strong>ScsbidInfoService</strong>/<strong>getOpengResultListInfoServcPPSSrch</strong>?inqryDiv=1&amp;inqryBgnDt=201605010000&amp;inqryEndDt=201605052359&amp;pageNo=1&amp;numOfRows=10&amp;ServiceKey=인증키</td>
</tr>
<tr>
<td>응답 메시지</td>
</tr>
<tr>
<td><p>&lt;response&gt;</p>
<p>&lt;header&gt;</p>
<p>&lt;resultCode&gt;00&lt;/resultCode&gt;</p>
<p>&lt;resultMsg&gt;정상&lt;/resultMsg&gt;</p>
<p>&lt;/header&gt;</p>
<p>&lt;body&gt;</p>
<p>&lt;items&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00882586&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;0&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;bidNtceNm&gt;한국생명공학연구원 지역조직 중기 발전전략 수립&lt;/bidNtceNm&gt;</p>
<p>&lt;opengDt&gt;2025-06-13 11:00:00&lt;/opengDt&gt;</p>
<p>&lt;prtcptCnum&gt;2&lt;/prtcptCnum&gt;</p>
<p>&lt;opengCorpInfo&gt;주식회사 과학기술전략연구소^5088702880^유경만^72000000^0&lt;/opengCorpInfo&gt;</p>
<p>&lt;progrsDivCdNm&gt;개찰완료&lt;/progrsDivCdNm&gt;</p>
<p>&lt;inptDt&gt;2025-07-01 16:52:39&lt;/inptDt&gt;</p>
<p>&lt;rsrvtnPrceFileExistnceYn&gt;N&lt;/rsrvtnPrceFileExistnceYn&gt;</p>
<p>&lt;ntceInsttCd&gt;Z004836&lt;/ntceInsttCd&gt;</p>
<p>&lt;ntceInsttNm&gt;한국생명공학연구원&lt;/ntceInsttNm&gt;</p>
<p>&lt;dminsttCd&gt;Z004836&lt;/dminsttCd&gt;</p>
<p>&lt;dminsttNm&gt;한국생명공학연구원&lt;/dminsttNm&gt;</p>
<p>&lt;opengRsltNtcCntnts&gt;&lt;/opengRsltNtcCntnts&gt;</p>
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

#### \[나라장터 검색조건에 의한 개찰결과 외자 목록 조회\] 오퍼레이션 명세

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
<td colspan="2">나라장터 검색조건에 의한 개찰결과 외자 목록 조회</td>
</tr>
<tr>
<td>오퍼레이션 유형</td>
<td>조회(목록)</td>
<td>오퍼레이션명(영문)</td>
<td colspan="2"><strong>getOpengResultListInfoFrgcptPPSSrch</strong></td>
</tr>
<tr>
<td>오퍼레이션 설명</td>
<td colspan="4">유찰, 개찰완료, 재입찰건에 대한 개찰결과를 제공하며 검색조건을 공고일시, 개찰일시, 입찰공고번호, 입찰공고명, 공고기관코드, 공고기관명, 수요기관코드, 수요기관명, 참조번호, 참가제한지역코드, 참가제한지역명, 업종코드, 업종명, 추정가격시작, 추정가격종료, 세부품명번호, 다수공급경쟁자여부, 조달요청번호, 국제구분코드로 하여 외자에 대한 나라장터 개찰결과 목록(입찰공고번호, 입찰공고명, 개찰일시, 참가업체수, 개찰업체정보, 진행구분코드명, 입력일시, 예비가격파일존재여부, 공고기관명, 수요기관명)을 조회</td>
</tr>
<tr>
<td>Call Back URL</td>
<td colspan="4" style="text-align: left;">N/A</td>
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
<col style="width: 11%" />
<col style="width: 13%" />
<col style="width: 22%" />
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
<td>4</td>
<td>1</td>
<td>10</td>
<td style="text-align: left;">한 페이지 결과 수</td>
</tr>
<tr>
<td>pageNo</td>
<td>페이지 번호</td>
<td>4</td>
<td>1</td>
<td>1</td>
<td style="text-align: left;">페이지 번호</td>
</tr>
<tr>
<td style="text-align: left;">ServiceKey</td>
<td style="text-align: left;">서비스키</td>
<td style="text-align: left;">400</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">공공데이터포털에서 받은 인증키</td>
<td style="text-align: left;">공공데이터포털에서 받은 인증키</td>
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
<td>조회구분</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">검색하고자하는 조회구분<br />
1.공고일시, 2.개찰일시, 3.입찰공고번호</td>
</tr>
<tr>
<td>inqryBgnDt</td>
<td>조회시작일시</td>
<td>12</td>
<td style="text-align: left;">0</td>
<td>202507010000</td>
<td>검색하고자하는 시작일시<br />
'YYYYMMDDHHMM'<br />
조회구분 1,2일 경우 필수</td>
</tr>
<tr>
<td>inqryEndDt</td>
<td>조회종료일시</td>
<td style="text-align: left;">12</td>
<td style="text-align: left;">0</td>
<td>202507012359</td>
<td>검색하고자하는 종료일시<br />
'YYYYMMDDHHMM'<br />
조회구분 1,2일 경우 필수</td>
</tr>
<tr>
<td>bidNtceNo</td>
<td>입찰공고번호</td>
<td style="text-align: left;">11</td>
<td style="text-align: left;">0</td>
<td>R25BK00916730</td>
<td>검색하고자하는 입찰공고번호<br />
조회구분이 '3'인 경우 필수</td>
</tr>
<tr>
<td>bidNtceNm</td>
<td>입찰공고명</td>
<td style="text-align: left;">1000</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">외자조달요청(북부지원 유도결합플라즈마 질량분석기</td>
<td>검색하고자하는 공고명<br />
※ 공고명 일부 입력시에도 조회 가능</td>
</tr>
<tr>
<td>ntceInsttCd</td>
<td>공고기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td>1230000</td>
<td>검색하고자하는 공고기관코드</td>
</tr>
<tr>
<td>ntceInsttNm</td>
<td>공고기관명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td>조달청</td>
<td>검색하고자하는 공고기관명<br />
※ 공고기관명 일부 입력시에도 조회 가능</td>
</tr>
<tr>
<td>dminsttCd</td>
<td>수요기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td>1230000</td>
<td><p>검색하고자하는 수요기관코드</p>
<p>행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드 입력</p>
<p>행자부코드가 없는 경우 조달청에서 부여한 수요기관 코드 입력</p></td>
</tr>
<tr>
<td>dminsttNm</td>
<td>수요기관명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td>조달청</td>
<td>검색하고자하는 수요기관명<br />
※ 수요기관명 일부 입력시에도 조회 가능</td>
</tr>
<tr>
<td>refNo</td>
<td>참조번호</td>
<td style="text-align: left;">105</td>
<td style="text-align: left;">0</td>
<td>R25DC00054022</td>
<td>검색하고자하는 참조번호</td>
</tr>
<tr>
<td>prtcptLmtRgnCd</td>
<td>참가제한지역코드</td>
<td style="text-align: left;">2</td>
<td style="text-align: left;">0</td>
<td>00</td>
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
<td>prtcptLmtRgnNm</td>
<td>참가제한지역명</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td>전국</td>
<td style="text-align: left;">검색하고자하는 참가제한지역명<br />
※ 참가제한지역명 일부 입력시에도 조회 가능<br />
*전국 : 지역제한을 설정하지 않은 공고</td>
</tr>
<tr>
<td>indstrytyCd</td>
<td>업종코드</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td>4119</td>
<td>검색하고자하는 업종코드</td>
</tr>
<tr>
<td>indstrytyNm</td>
<td>업종명</td>
<td style="text-align: left;">100</td>
<td style="text-align: left;">0</td>
<td>토목공사업</td>
<td>검색하고자하는 업종명<br />
※ 업종명 일부 입력시에도 조회 가능</td>
</tr>
<tr>
<td>presmptPrceBgn</td>
<td>추정가격시작</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td>0</td>
<td>검색하고자하는 추정가격범위시작금액이상(원화,원)</td>
</tr>
<tr>
<td>presmptPrceEnd</td>
<td>추정가격종료</td>
<td style="text-align: left;">25</td>
<td style="text-align: left;">0</td>
<td>0</td>
<td>검색하고자하는 추정가격범위종료금액이하(원화,원)</td>
</tr>
<tr>
<td>dtilPrdctClsfcNo</td>
<td>세부품명번호</td>
<td style="text-align: left;">10</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">4111540401</td>
<td>검색하고자하는 세부품명번호</td>
</tr>
<tr>
<td>masYn</td>
<td>다수공급경쟁자여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td>Y</td>
<td>검색하고자하는 다수공급경쟁자여부</td>
</tr>
<tr>
<td>prcrmntReqNo</td>
<td>조달요청번호</td>
<td style="text-align: left;">13</td>
<td style="text-align: left;">0</td>
<td>R25DC00054022</td>
<td>검색하고자하는 조달요청번호</td>
</tr>
<tr>
<td>intrntnlDivCd</td>
<td>국제구분코드</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">0</td>
<td>1</td>
<td>검색하고자하는 국제구분코드<br />
국내:1, 국제:2</td>
</tr>
</tbody>
</table>

※ 항목구분 : 필수(1), 옵션(0), 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)

##### 응답 메시지 명세

<table style="width:100%;">
<colgroup>
<col style="width: 23%" />
<col style="width: 16%" />
<col style="width: 9%" />
<col style="width: 9%" />
<col style="width: 22%" />
<col style="width: 18%" />
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
<td>resultCode</td>
<td>결과코드</td>
<td style="text-align: left;">2</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">00</td>
<td>결과코드</td>
</tr>
<tr>
<td>resultMsg</td>
<td>결과메세지</td>
<td style="text-align: left;">50</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">정상.</td>
<td>결과메세지</td>
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
<td>totalCount</td>
<td>데이터 총 개수</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td>17</td>
<td>데이터 총 개수</td>
</tr>
<tr>
<td>bidNtceNo</td>
<td>입찰공고번호</td>
<td style="text-align: left;">11</td>
<td style="text-align: left;">1</td>
<td>R25BK00916730</td>
<td style="text-align: left;">입찰공고 관리번호이며 조달청나라장터 공고건의 형식은 년도(4)+월(2)+순번(5)이며 자체전자조달시스템 보유기관은 각 기관별 형식 별도 사용<br />
*차세대나라장터 번호체계 개편 : R+년도(2)+단계구분(2)+순번(8) 총 13자리 구성<br />
- 단계구분:<br />
BK(입찰),<br />
TA(계약),<br />
DD:(발주계획),<br />
BD(사전규격),<br />
BK(통합입찰)</td>
</tr>
<tr>
<td>bidNtceOrd</td>
<td>입찰공고차수</td>
<td style="text-align: left;">3</td>
<td style="text-align: left;">1</td>
<td>000</td>
<td>입찰공고차수는 해당 입찰공고에 대한 재공고 및 재입찰 등이 발생되었을 경우 증가되는 수</td>
</tr>
<tr>
<td>bidClsfcNo</td>
<td>입찰분류번호</td>
<td style="text-align: left;">5</td>
<td style="text-align: left;">1</td>
<td>1</td>
<td>동일한 입찰공고번호에 대한 집행일련번호</td>
</tr>
<tr>
<td>rbidNo</td>
<td>재입찰번호</td>
<td style="text-align: left;">3</td>
<td style="text-align: left;">1</td>
<td>000</td>
<td>재입찰번호</td>
</tr>
<tr>
<td>bidNtceNm</td>
<td>입찰공고명</td>
<td style="text-align: left;">1000</td>
<td style="text-align: left;">1</td>
<td>외자조달요청(북부지원 유도결합플라즈마 질량분석기)</td>
<td>공사명 또는 사업명이라고도 하며 입찰공고 내용을 요약한 이름</td>
</tr>
<tr>
<td>opengDt</td>
<td>개찰일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">1</td>
<td>2025-07-01 13:00:00</td>
<td>조달업체가 제출한 입찰서를 개찰하는 일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td>prtcptCnum</td>
<td>참가업체수</td>
<td style="text-align: left;">6</td>
<td style="text-align: left;">0</td>
<td>1</td>
<td>참가업체수</td>
</tr>
<tr>
<td>opengCorpInfo</td>
<td>개찰업체정보</td>
<td style="text-align: left;">500</td>
<td style="text-align: left;">1</td>
<td>써모피셔사이언티픽코리아 주식회사^1178146910^석수진^173500^0</td>
<td>개찰업체정보<br />
다수 낙찰자의 경우 ”낙찰예정자 다수”와 개찰순위 1위의 투찰금액과 투찰율<br />
을 보여줌<br />
단일 낙찰자 의 경우 업체명과 사업자번호, 대표자명, 투찰금액, 투찰율을 보여줌<br />
단, 협상에 의한 계약일 경우는 투찰금액,투찰율 안나옴</td>
</tr>
<tr>
<td>progrsDivCdNm</td>
<td>진행구분코드명</td>
<td style="text-align: left;">4</td>
<td style="text-align: left;">1</td>
<td>개찰완료</td>
<td>진행구분이<br />
유찰, 개찰완료, 재입찰로 구분 됨</td>
</tr>
<tr>
<td>inptDt</td>
<td>입력일시</td>
<td style="text-align: left;">19</td>
<td style="text-align: left;">0</td>
<td>2025-07-01 13:10:54</td>
<td>입력일시 “YYYY-MM-DD HH:MM:SS”</td>
</tr>
<tr>
<td>rsrvtnPrceFileExistnceYn</td>
<td>예비가격파일존재여부</td>
<td style="text-align: left;">1</td>
<td style="text-align: left;">1</td>
<td>N</td>
<td>예비가격파일존재여부(Y/N)</td>
</tr>
<tr>
<td>ntceInsttCd</td>
<td>공고기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">1</td>
<td>1230000</td>
<td>공고를 하는 기관의 코드로 행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드가 행자부코드가 없는 경우 조달청에서 부여한 수요기관 코드가 표기됨</td>
</tr>
<tr>
<td>ntceInsttNm</td>
<td>공고기관명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td>조달청</td>
<td>수요기관의 의뢰를 받아 공고하는 기관의 명</td>
</tr>
<tr>
<td>dminsttCd</td>
<td>수요기관코드</td>
<td style="text-align: left;">7</td>
<td style="text-align: left;">0</td>
<td>6440071</td>
<td>실제 수요기관의 코드로 행자부코드(행정자치부에서 부여한 기관코드)가 있는 경우 행자부코드가 행자부코드가 없는 경우 조달청에서 부여한 수요기관 코드가 표기됨</td>
</tr>
<tr>
<td>dminsttNm</td>
<td>수요기관명</td>
<td style="text-align: left;">200</td>
<td style="text-align: left;">0</td>
<td>충청남도 보건환경연구원</td>
<td>중앙조달인 경우 조달사업에 관한 법률 제2조(정의)에 따라 수요물자의 구매 공급 또는 시설공사 계약의 체결을 조달청장에게 요청할 수 있도록 조달청장이 인정하여 등록한 기관 또는 자체전자조달시스템을 이용하는 기관인 경우 계약을 의뢰한 기관의 명으로 공고기관과 수요기관이 동일할 수 있음</td>
</tr>
<tr>
<td style="text-align: left;">opengRsltNtcCntnts</td>
<td style="text-align: left;">개찰결과공지내용</td>
<td style="text-align: left;">4000</td>
<td style="text-align: left;">0</td>
<td style="text-align: left;">개찰결과공지내용</td>
<td style="text-align: left;">입찰공고번호, 입찰공고차수, 입찰분류번호, 재입찰번호에 해당하는 공지사항 내용</td>
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
<td>REST(URI)</td>
</tr>
<tr>
<td style="text-align: left;">http://apis.data.go.kr/1230000/as/<strong>ScsbidInfoService</strong>/<strong>getOpengResultListInfoFrgcptPPSSrch</strong>?inqryDiv=1&amp;inqryBgnDt=201605010000&amp;inqryEndDt=201605052359&amp;pageNo=1&amp;numOfRows=10&amp;ServiceKey=인증키</td>
</tr>
<tr>
<td>응답 메시지</td>
</tr>
<tr>
<td><p>&lt;response&gt;</p>
<p>&lt;header&gt;</p>
<p>&lt;resultCode&gt;00&lt;/resultCode&gt;</p>
<p>&lt;resultMsg&gt;정상&lt;/resultMsg&gt;</p>
<p>&lt;/header&gt;</p>
<p>&lt;body&gt;</p>
<p>&lt;items&gt;</p>
<p>&lt;item&gt;</p>
<p>&lt;bidNtceNo&gt;R25BK00916730&lt;/bidNtceNo&gt;</p>
<p>&lt;bidNtceOrd&gt;000&lt;/bidNtceOrd&gt;</p>
<p>&lt;bidClsfcNo&gt;1&lt;/bidClsfcNo&gt;</p>
<p>&lt;rbidNo&gt;000&lt;/rbidNo&gt;</p>
<p>&lt;bidNtceNm&gt;외자조달요청(북부지원 유도결합플라즈마 질량분석기)&lt;/bidNtceNm&gt;</p>
<p>&lt;opengDt&gt;2025-07-01 13:00:00&lt;/opengDt&gt;</p>
<p>&lt;prtcptCnum&gt;1&lt;/prtcptCnum&gt;</p>
<p>&lt;opengCorpInfo&gt;써모피셔사이언티픽코리아 주식회사^1178146910^석수진^173500^0&lt;/opengCorpInfo&gt;</p>
<p>&lt;progrsDivCdNm&gt;개찰완료&lt;/progrsDivCdNm&gt;</p>
<p>&lt;inptDt&gt;2025-07-01 13:10:54&lt;/inptDt&gt;</p>
<p>&lt;rsrvtnPrceFileExistnceYn&gt;N&lt;/rsrvtnPrceFileExistnceYn&gt;</p>
<p>&lt;ntceInsttCd&gt;1230000&lt;/ntceInsttCd&gt;</p>
<p>&lt;ntceInsttNm&gt;조달청&lt;/ntceInsttNm&gt;</p>
<p>&lt;dminsttCd&gt;6440071&lt;/dminsttCd&gt;</p>
<p>&lt;dminsttNm&gt;충청남도 보건환경연구원&lt;/dminsttNm&gt;</p>
<p>&lt;opengRsltNtcCntnts&gt;&lt;/opengRsltNtcCntnts&gt;</p>
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
<td style="text-align: left;">잘못된 서비스키를 사용하였거나 서비스키를 URL인코딩하지 않음</td>
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
