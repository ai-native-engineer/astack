국민연금공단 OpenAPI 활용가이드

\[국민연금 가입 사업장 내역\]

문서 정보

|  |  |
|----|----|
| 프로젝트 | 공공데이터 개방 활용 관리체계 개발 |
| 단계 | 개발 |
| 활동 | 활용가이드 |
| 작업 | 활용가이드작성 |
| 산출물 | OpenAPI 활용가이드 |
| 파일명 | IROS5_OA_DV_0401_OpenAPI활용가이드_사업장정보서비스(국민연금공단)\_v2.0 |

개정 이력

<table style="width:100%;">
<colgroup>
<col style="width: 8%" />
<col style="width: 13%" />
<col style="width: 14%" />
<col style="width: 46%" />
<col style="width: 8%" />
<col style="width: 8%" />
</colgroup>
<tbody>
<tr>
<td>버 전</td>
<td>변경일</td>
<td>변경 사유</td>
<td>변경 내용</td>
<td>작성자</td>
<td>승인</td>
</tr>
<tr>
<td>1.0</td>
<td style="text-align: left;">2015-10-29</td>
<td>최초작성</td>
<td>OpenAPI 활용가이드 작성 및 승인</td>
<td>문성무</td>
<td></td>
</tr>
<tr>
<td>1.1</td>
<td style="text-align: left;">2017-08-28</td>
<td>품질관리</td>
<td>오퍼레이션 명칭 일치(사업장 정보조회 서비스)</td>
<td>이종임</td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td style="text-align: center;">1.2</td>
<td>2017-09-14</td>
<td style="text-align: center;">품질관리</td>
<td><p>요청항목 조건(필수/선택) 일치</p>
<ul>
<li><p>사업장 정보조회(9page)</p></li>
<li><p>wkpl_nm 항목구분(선택 🡪 필수)</p></li>
<li><p>기간별 현황 정보조회(13page)</p></li>
<li><p>data_crt_ym 항목구분 (필수 🡪 선택)</p></li>
</ul></td>
<td style="text-align: center;">이종임</td>
<td></td>
</tr>
<tr>
<td style="text-align: center;">1.3</td>
<td>2018-01-11</td>
<td style="text-align: center;">사용자 문의</td>
<td><p>요청항목 조건(필수/선택) 수정(9page)</p>
<ul>
<li><p>wkpl_nm, bzowr_rgst_no</p></li>
</ul>
<p>요청 메시지 한글 입력 안내(10page)</p></td>
<td style="text-align: center;">이종임</td>
<td></td>
</tr>
<tr>
<td style="text-align: center;">1.4</td>
<td>2018-01-25</td>
<td style="text-align: center;">사용자 문의</td>
<td><p>요청항목 삭제(개인사업장 정보 없음)</p>
<ul>
<li><p>wkpl_styl_dvcd(사업장형태구분코드)</p></li>
<li><p>1:법인, 2:개인</p></li>
</ul></td>
<td style="text-align: center;">이종임</td>
<td></td>
</tr>
<tr>
<td style="text-align: center;">1.5</td>
<td>2018-03-14</td>
<td style="text-align: center;">데이터 변경</td>
<td>응답메시지 변경</td>
<td style="text-align: center;">이종임</td>
<td></td>
</tr>
<tr>
<td style="text-align: center;">1.6</td>
<td>2018-06-14</td>
<td style="text-align: center;">사용자 문의</td>
<td>서비스 WADL 미제공</td>
<td style="text-align: center;">이종임</td>
<td></td>
</tr>
<tr>
<td style="text-align: center;">2.0</td>
<td>2025-05-07</td>
<td style="text-align: center;">데이터 변경</td>
<td><p>서비스 URL 변경</p>
<p>응답자료형식 추가 및 요청 표기법 변경</p></td>
<td style="text-align: center;">홍성민</td>
<td></td>
</tr>
</tbody>
</table>

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr>
<th><p>국민연금공단이 오픈 API로 제공하는 ‘국민연금 가입 사업장 내역 (사업장 정보조회 서비스)’의 데이터 기준이 아래와 같이 변경(‘18. 03. 14 ~)됨을 알려드립니다.</p>
<p>* 현재 제공하는 모든 데이터는 새로운 기준이 적용된 데이터입니다.</p>
<p><strong>O 데이터 추출 기준</strong></p>
<p>- (변경 전) 신고 월과 취득·상실 월이 동일한 경우만 추출 (소급 적용 제외)</p>
<p>- (변경 후) 당월 고지서의 가입자 취득·상실 신고 건 추출</p>
<p><strong>O 데이터 제공 일시</strong></p>
<p>- (변경 전) 매월 3일 이후</p>
<p>- (변경 후) 매월 15일 이후</p>
<p><strong>O 기준 변경 데이터 제공</strong> : ‘18. 03. 14 ~</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr>
<th><p>국민연금공단이 오픈 API로 제공하는 ‘국민연금 가입 사업장 내역 (사업장 정보조회 서비스)’이 아래와 같이 변경되오니 서비스 이용에 참고바랍니다.</p>
<p>* 변경사유 : 오픈API 서버의 과부하로 인한 데이터 삭제</p>
<ul>
<li><p><strong>아래 -</strong></p>
<p><strong>제공기관 : 국민연금공단</strong></p>
<p><strong>제공서비스 : 사업장정보조회서비스</strong></p>
<p><strong>변경내용 : 제공시점을 기준으로 1년치 데이터만 제공</strong></p>
<p><strong>적용일자 : 2018.7.2(월) 이후(1년에 한번씩 공공데이터 포털 공지를 통하여 데이터 삭제조치)</strong></p></li>
</ul></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr>
<th><p>[국민연금공단] 새로운 전산시스템 개통으로 인한 OPEN API 서비스 변경 안내</p>
<p>안녕하세요? 국민연금공단에서 제공 중인 OPEN API 서비스 변경 안내드립니다.</p>
<p>ㅁ 변경시간: 2025. 5. 7.(수) 09:00</p>
<p>ㅁ 변경사유: 국민연금공단 새로운 전산시스템(지능형 연금복지 통합플랫폼) 전환</p>
<p>ㅁ 변경내용:</p>
<p>- 요청항목 'dataType 응답자료형식(xml/json)' 추가</p>
<p>- 요청항목 표기법 변경</p>
<p>* 스네이크 케이스 -&gt; 카멜케이스</p>
<p>ex) 1. ldong_addr_mgpl_dg_cd -&gt; ldongAddrMgplDgCd</p>
<p>2. ldong_addr_mgpl_sggu_cd -&gt; ldongAddrMgplSgguCd</p>
<p>3. ldong_addr_mgpl_sggu_emd_cd -&gt; ldongAddrMgplSgguEmdCd</p>
<p>- 응답항목 구조 변경</p>
<p>item -&gt; items.item[]</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

1\. 서비스 사용 [5](#_Toc1745996788)

**1.1.** 서비스 Key 발급 및 활용 [5](#_Toc1745996789)

가. 서비스 Key발급(인증신청 및 발급) [5](#_Toc1745996790)

나. 서비스 인증키 활용 [8](#_Toc1745996791)

2\. 서비스 목록 [9](#_Toc1745996792)

3\. 서비스 명세 [9](#_Toc1745996793)

**3.1.** 사업장 정보조회 서비스 [9](#_Toc1745996794)

가. 서비스 개요 [9](#_Toc1745996795)

나. 오퍼레이션 목록 [10](#_Toc1745996796)

#

##

###

####

[\
<span id="_Toc1745996788" class="anchor"></span>서비스 사용\
※ 오픈API를 통해 제공되는 데이터는 통계자료로 활용할 수 없습니다.<span id="_Toc1745996789" class="anchor"></span>서비스 Key 발급 및 활용<span id="_Toc1745996790" class="anchor"></span>서비스 Key발급(인증신청 및 발급)공공데이터포털(https://www.data.go.kr/) 활용자활용 신청 하고자 하는 API를 검색하여 클릭](#_Toc1745996796)

[<img src="media/image1.png" style="width:6.27414in;height:5.89982in" />](#_Toc1745996796)

[\
](#_Toc1745996796)

[활용 신청 하고자 하는 서비스 항목 오른쪽 파란색 활용신청 버튼 클릭](#_Toc1745996796)

[<img src="media/image2.png" style="width:6.69306in;height:2.48681in" />](#_Toc1745996796)

[\
](#_Toc1745996796)

[해당되는 내용을 기재하고 이용하고자 하는 상세 기능을 체크 한 뒤 가장 아래 쪽 파란 신청 버튼을 클릭](#_Toc1745996796)

[<img src="media/image3.png" style="width:5.94097in;height:8.48958in" />](#_Toc1745996796)

[신청이 완료되면 신청목록이 조회 되어 출력](#_Toc1745996796)

[<img src="media/image4.png" style="width:6.69306in;height:4.61736in" />](#_Toc1745996796)

[왼쪽의 메뉴에 인증키 발급현황을 클릭하면 인증키 확인 가능](#_Toc1745996796)

[<img src="media/image5.png" style="width:6.69306in;height:2.22847in" />](#_Toc1745996796)

###

####

[<span id="_Toc1745996791" class="anchor"></span>서비스 인증키 활용REST 방식의 인증키 활용<https://apis.data.go.kr/B552015/NpsSbscrbInfoProvdServiceV2/getSbscrbSttusInfoSearchV2?serviceKey=서비스인증키>](#_Toc1745996796)

#

| [<span id="_Toc1745996792" class="anchor"></span>서비스 목록순번](#_Toc1745996796) | [서비스 ID](#_Toc1745996796) | [서비스명(영문)](#_Toc1745996796) | [서비스명(국문)](#_Toc1745996796) |
|----|----|----|----|
| [1](#_Toc1745996796) | [SC-OA-04-03](#_Toc1745996796) | [국민연금 가입 사업장 내역](#_Toc1745996796) | [NpsBplcInfoInqireServiceV2](#_Toc1745996796) |

#

##

###

<table style="width:100%;">
<colgroup>
<col style="width: 14%" />
<col style="width: 23%" />
<col style="width: 8%" />
<col style="width: 11%" />
<col style="width: 10%" />
<col style="width: 7%" />
<col style="width: 1%" />
<col style="width: 21%" />
</colgroup>
<thead>
<tr>
<th rowspan="4"><a href="#_Toc1745996796"><span id="_Toc1745996793" class="anchor"></span>서비스 명세<span id="_Toc1745996794" class="anchor"></span>사업장 정보조회 서비스 <span id="_Toc1745996795" class="anchor"></span>서비스 개요서비스 정보</a></th>
<th><a href="#_Toc1745996796">서비스 ID</a></th>
<th colspan="6"><a href="#_Toc1745996796">SC-OA-04-03</a></th>
</tr>
<tr>
<th><a href="#_Toc1745996796">서비스명(국문)</a></th>
<th colspan="6"><a href="#_Toc1745996796">국민연금 가입 사업장 내역</a></th>
</tr>
<tr>
<th><a href="#_Toc1745996796">서비스명(영문)</a></th>
<th colspan="6"><a href="#_Toc1745996796">NpsBplcInfoInqireServiceV2</a></th>
</tr>
<tr>
<th><a href="#_Toc1745996796">서비스 설명</a></th>
<th colspan="6"><a href="#_Toc1745996796">국민연금 가입 사업장 정보조회 제공</a></th>
</tr>
</thead>
<tbody>
<tr>
<td><a href="#_Toc1745996796">서비스 제공자정보</a></td>
<td><a href="#_Toc1745996796">기관명</a></td>
<td colspan="6"><a href="#_Toc1745996796">국민연금공단</a></td>
</tr>
<tr>
<td rowspan="3"><a href="#_Toc1745996796">서비스 보안</a></td>
<td><a href="#_Toc1745996796">서비스 인증/권한</a></td>
<td colspan="5"><p><a href="#_Toc1745996796">[ O ] 서비스 Key[ ] 인증서 (GPKI)</a></p>
<p><a href="#_Toc1745996796">[ ] Basic (ID/PW) [ ] 없음</a></p></td>
<td rowspan="2"><p><a href="#_Toc1745996796">[ O ] 서비스 Key[ ] 인증서 (GPKI)</a></p>
<p><a href="#_Toc1745996796">[ ] Basic (ID/PW) [ ] 없음</a></p>
<p><a href="#_Toc1745996796">[ ] 전자서명 [ ] 암호화 [ ] 없음</a></p></td>
</tr>
<tr>
<td><a href="#_Toc1745996796">메시지 레벨 암호화</a></td>
<td colspan="5"><a href="#_Toc1745996796">[ ] 전자서명 [ ] 암호화 [ ] 없음</a></td>
</tr>
<tr>
<td><a href="#_Toc1745996796">전송 레벨 암호화</a></td>
<td colspan="6"><a href="#_Toc1745996796">[ ] SSL [ ] 없음</a></td>
</tr>
<tr>
<td rowspan="2"><a href="#_Toc1745996796">적용 기술 수준</a></td>
<td><a href="#_Toc1745996796">인터페이스 표준</a></td>
<td colspan="6"><p><a href="#_Toc1745996796">[ ] SOAP 1.2</a></p>
<p><a href="#_Toc1745996796">(RPC-Encoded, Document Literal, Document Literal Wrapped)</a></p>
<p><a href="#_Toc1745996796">[ O ] REST (GET, POST, PUT, DELETE)</a></p>
<p><a href="#_Toc1745996796">[ ] RSS 1.0 [ ] RSS 2.0 [ ] Atom 1.0 [ ] 기타</a></p></td>
</tr>
<tr>
<td><a href="#_Toc1745996796">교환 데이터 표준</a></td>
<td colspan="6"><a href="#_Toc1745996796">[ O ] XML [ O ] JSON [ ] MIME [ ] MTOM</a></td>
</tr>
<tr>
<td rowspan="2"><a href="#_Toc1745996796">서비스 URL</a></td>
<td><a href="#_Toc1745996796">개발환경</a></td>
<td colspan="6"><a href="#_Toc1745996796"><span>http://apis.data.go.kr/B552015/NpsBplcInfoInqireServiceV2</span></a></td>
</tr>
<tr>
<td><a href="#_Toc1745996796">운영환경</a></td>
<td colspan="6"><a href="#_Toc1745996796"><span>http://apis.data.go.kr/B552015/NpsBplcInfoInqireServiceV2</span></a></td>
</tr>
<tr>
<td rowspan="2"><a href="#_Toc1745996796">서비스 WADL</a></td>
<td><a href="#_Toc1745996796">개발환경</a></td>
<td colspan="6"></td>
</tr>
<tr>
<td><a href="#_Toc1745996796">운영환경</a></td>
<td colspan="6"></td>
</tr>
<tr>
<td rowspan="3"><a href="#_Toc1745996796">서비스 배포 정보</a></td>
<td><a href="#_Toc1745996796">서비스 버전</a></td>
<td colspan="6"><a href="#_Toc1745996796">2.0</a></td>
</tr>
<tr>
<td><a href="#_Toc1745996796">유효일자</a></td>
<td colspan="2"><a href="#_Toc1745996796">N/A</a></td>
<td colspan="3"><a href="#_Toc1745996796">배포 일자</a></td>
<td><a href="#_Toc1745996796">N/A</a></td>
</tr>
<tr>
<td><a href="#_Toc1745996796">서비스 이력</a></td>
<td colspan="6"><a href="#_Toc1745996796">N/A</a></td>
</tr>
<tr>
<td colspan="2"><a href="#_Toc1745996796">메시지 교환 유형</a></td>
<td colspan="6"><p><a href="#_Toc1745996796">[ O ] Request-Response [ ] Publish-Subscribe</a></p>
<p><a href="#_Toc1745996796">[ ] Fire-and-Forgot [ ] Notification</a></p></td>
</tr>
<tr>
<td colspan="2"><a href="#_Toc1745996796">메시지 로깅 수준</a></td>
<td><a href="#_Toc1745996796">성공</a></td>
<td colspan="2"><a href="#_Toc1745996796">[O] Header [ ] Body</a></td>
<td><a href="#_Toc1745996796">실패</a></td>
<td colspan="2"><a href="#_Toc1745996796">[O] Header [O} Body</a></td>
</tr>
<tr>
<td colspan="2"><a href="#_Toc1745996796">사용 제약 사항 (비고)</a></td>
<td colspan="6"></td>
</tr>
</tbody>
</table>

###

<table style="width:100%;">
<colgroup>
<col style="width: 6%" />
<col style="width: 16%" />
<col style="width: 28%" />
<col style="width: 48%" />
</colgroup>
<thead>
<tr>
<th><a href="#_Toc1745996796"><span id="_Toc1745996796" class="anchor"></span>오퍼레이션 목록일련번호</a></th>
<th><a href="#_Toc1745996796">서비스명(국문)</a></th>
<th><a href="#_Toc1745996796">오퍼레이션명(영문)</a></th>
<th><a href="#_Toc1745996796">오퍼레이션명(국문)</a></th>
</tr>
</thead>
<tbody>
<tr>
<td><a href="#_Toc1745996796">1</a></td>
<td rowspan="3"><a href="#_Toc1745996796">국민연금 가입 사업장 내역</a></td>
<td><a href="#_Toc1745996796">getBassInfoSearchV2</a></td>
<td><a href="#_Toc1745996796">사업장 정보조회</a></td>
</tr>
<tr>
<td><a href="#_Toc1745996796">2</a></td>
<td><a href="#_Toc1745996796">getDetailInfoSearchV2</a></td>
<td><a href="#_Toc1745996796">상세 정보조회</a></td>
</tr>
<tr>
<td><a href="#_Toc1745996796">3</a></td>
<td><a href="#_Toc1745996796">getPdAcctoSttuInfoSearchV2</a></td>
<td><a href="#_Toc1745996796">기간별 현황 정보조회</a></td>
</tr>
</tbody>
</table>

####

<table style="width:100%;">
<colgroup>
<col style="width: 14%" />
<col style="width: 23%" />
<col style="width: 16%" />
<col style="width: 23%" />
<col style="width: 22%" />
</colgroup>
<thead>
<tr>
<th rowspan="6"><a href="#_Toc1745996796">사업장 정보조회 오퍼레이션 명세오퍼레이션 정보</a></th>
<th><a href="#_Toc1745996796">오퍼레이션 번호</a></th>
<th><a href="#_Toc1745996796">1</a></th>
<th><a href="#_Toc1745996796">오퍼레이션명(국문)</a></th>
<th><a href="#_Toc1745996796">사업장 정보조회</a></th>
</tr>
<tr>
<th><a href="#_Toc1745996796">오퍼레이션 유형</a></th>
<th><a href="#_Toc1745996796">조회(목록)</a></th>
<th><a href="#_Toc1745996796">오퍼레이션명(영문)</a></th>
<th><a href="#_Toc1745996796">getBassInfoSearchV2</a></th>
</tr>
<tr>
<th><a href="#_Toc1745996796">오퍼레이션 설명</a></th>
<th colspan="3"><a href="#_Toc1745996796">사업장 기본정보 조회</a></th>
</tr>
<tr>
<th><a href="#_Toc1745996796">Call Back URL</a></th>
<th colspan="3"><a href="#_Toc1745996796">N/A</a></th>
</tr>
<tr>
<th><a href="#_Toc1745996796">최대 메시지 사이즈</a></th>
<th colspan="3"><a href="#_Toc1745996796">[ 4000 bytes]</a></th>
</tr>
<tr>
<th><a href="#_Toc1745996796">평균 응답 시간</a></th>
<th><a href="#_Toc1745996796">[ 500 ms]</a></th>
<th><a href="#_Toc1745996796"><strong>초당 최대 트랜잭션</strong></a></th>
<th><a href="#_Toc1745996796">[ 30 ms]</a></th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="2"><a href="#_Toc1745996796">HTTP Method</a></td>
<td colspan="3"><a href="#_Toc1745996796">[ O ] REST (GET, POST, PUT, DELETE)</a></td>
</tr>
</tbody>
</table>

#####

<table style="width:100%;">
<colgroup>
<col style="width: 31%" />
<col style="width: 17%" />
<col style="width: 9%" />
<col style="width: 8%" />
<col style="width: 13%" />
<col style="width: 20%" />
</colgroup>
<thead>
<tr>
<th><a href="#_Toc1745996796">요청 메시지 명세항목명(영문)</a></th>
<th><a href="#_Toc1745996796">항목명(국문)</a></th>
<th><a href="#_Toc1745996796">항목크기</a></th>
<th><a href="#_Toc1745996796">항목구분</a></th>
<th><a href="#_Toc1745996796">샘플데이터</a></th>
<th><a href="#_Toc1745996796">항목설명</a></th>
</tr>
</thead>
<tbody>
<tr>
<td><a href="#_Toc1745996796">ldongAddrMgplDgCd</a></td>
<td><a href="#_Toc1745996796">법정동주소광역시도코드</a></td>
<td><a href="#_Toc1745996796">2</a></td>
<td><a href="#_Toc1745996796">0</a></td>
<td><a href="#_Toc1745996796">41</a></td>
<td><a href="#_Toc1745996796">시도(행정자치부 법정동 주소코드 참조)</a></td>
</tr>
<tr>
<td><a href="#_Toc1745996796">ldongAddrMgplSgguCd</a></td>
<td><a href="#_Toc1745996796">법정동주소시군구코드</a></td>
<td><a href="#_Toc1745996796">5</a></td>
<td><a href="#_Toc1745996796">0</a></td>
<td><a href="#_Toc1745996796">117</a></td>
<td><a href="#_Toc1745996796">시군구(행정자치부 법정동 주소코드 참조)</a></td>
</tr>
<tr>
<td><a href="#_Toc1745996796">ldongAddrMgplSgguEmdCd</a></td>
<td><a href="#_Toc1745996796">법정동주소읍면동코드</a></td>
<td><a href="#_Toc1745996796">8</a></td>
<td><a href="#_Toc1745996796">0</a></td>
<td><a href="#_Toc1745996796">102</a></td>
<td><a href="#_Toc1745996796">읍면동(행정자치부 법정동 주소코드 참조)</a></td>
</tr>
<tr>
<td><a href="#_Toc1745996796">wkplNm</a></td>
<td><a href="#_Toc1745996796">사업장명</a></td>
<td><a href="#_Toc1745996796">100</a></td>
<td><a href="#_Toc1745996796">1</a></td>
<td><a href="#_Toc1745996796">삼성전자로지텍주식회사</a></td>
<td><a href="#_Toc1745996796">사업장명</a></td>
</tr>
<tr>
<td><a href="#_Toc1745996796">bzowrRgstNo</a></td>
<td><a href="#_Toc1745996796">사업자등록번호</a></td>
<td><a href="#_Toc1745996796">10</a></td>
<td><a href="#_Toc1745996796">0</a></td>
<td><a href="#_Toc1745996796">124815</a></td>
<td><a href="#_Toc1745996796">사업자등록번호(앞에서 6자리)</a></td>
</tr>
<tr>
<td><a href="#_Toc1745996796">dataType</a></td>
<td><a href="#_Toc1745996796">응답자료형식</a></td>
<td><a href="#_Toc1745996796">4</a></td>
<td><a href="#_Toc1745996796">0</a></td>
<td><a href="#_Toc1745996796">json</a></td>
<td><a href="#_Toc1745996796">xml 또는 json<br />
기본값: xml</a></td>
</tr>
<tr>
<td><a href="#_Toc1745996796">pageNo</a></td>
<td><a href="#_Toc1745996796">페이지번호</a></td>
<td><a href="#_Toc1745996796">4</a></td>
<td><a href="#_Toc1745996796">0</a></td>
<td><a href="#_Toc1745996796">1</a></td>
<td><p><a href="#_Toc1745996796">페이지번호</a></p>
<p><a href="#_Toc1745996796">기본값: 1</a></p></td>
</tr>
<tr>
<td><a href="#_Toc1745996796">numOfRows</a></td>
<td><a href="#_Toc1745996796">한 페이지 결과 수</a></td>
<td><a href="#_Toc1745996796">4</a></td>
<td><a href="#_Toc1745996796">0</a></td>
<td><a href="#_Toc1745996796">10</a></td>
<td><p><a href="#_Toc1745996796">한 페이지 결과 수</a></p>
<p><a href="#_Toc1745996796">기본값: 10</a></p></td>
</tr>
<tr>
<td><a href="#_Toc1745996796">serviceKey</a></td>
<td><a href="#_Toc1745996796">서비스인증키</a></td>
<td><a href="#_Toc1745996796">400</a></td>
<td><a href="#_Toc1745996796">1</a></td>
<td><a href="#_Toc1745996796">서비스인증키</a></td>
<td><a href="#_Toc1745996796">공공데이터포털에서 발급받은 인증키</a></td>
</tr>
</tbody>
</table>

-
-
-

[항목구분 : 필수(1), 옵션(0)사업장명(wkplNm)과 사업자등록번호(bzowrRgstNo) 둘 다 필수(1)로 입력하거나 둘 중 하나만 입력해도 결과 출력.3인이상 법인사업장 정보만 개방되므로 요청항목 중 불필요한 ‘wkplStylDvcd 사업장형태구분코드 (1:법인, 2:개인)’ 삭제(2018.01.25.)](#_Toc1745996796)

#####

| [응답 메시지 명세항목명(영문)](#_Toc1745996796) | [항목명(국문)](#_Toc1745996796) | [항목크기](#_Toc1745996796) | [항목구분](#_Toc1745996796) | [샘플데이터](#_Toc1745996796) | [항목설명](#_Toc1745996796) |
|----|----|----|----|----|----|
| [dataCrtYm](#_Toc1745996796) | [자료생성년월](#_Toc1745996796) | [6](#_Toc1745996796) | [0..n](#_Toc1745996796) | [월별 누적데이터로 조회시점에 따라 해당월 표출](#_Toc1745996796) | [자료생성년월](#_Toc1745996796) |
| [seq](#_Toc1745996796) | [식별번호](#_Toc1745996796) | [10](#_Toc1745996796) | [0..n](#_Toc1745996796) | [월별 누적데이터로 조회시점에 따라 누적식별번호 표출](#_Toc1745996796) | [식별번호](#_Toc1745996796) |
| [wkplNm](#_Toc1745996796) | [사업장명](#_Toc1745996796) | [100](#_Toc1745996796) | [0..n](#_Toc1745996796) | [삼성전자로지텍주식회사](#_Toc1745996796) | [사업장명](#_Toc1745996796) |
| [bzowrRgstNo](#_Toc1745996796) | [사업자등록번호](#_Toc1745996796) | [10](#_Toc1745996796) | [0..n](#_Toc1745996796) | [124815\*\*\*\*](#_Toc1745996796) | [사업자등록번호(앞에서 6자리)](#_Toc1745996796) |
| [wkplRoadNmDtlAddr](#_Toc1745996796) | [사업장도로명상세주소](#_Toc1745996796) | [300](#_Toc1745996796) | [0..n](#_Toc1745996796) | [경기도 수원시 영통구 삼성로](#_Toc1745996796) | [사업장도로명상세주소](#_Toc1745996796) |
| [wkplJnngStcd](#_Toc1745996796) | [사업장가입상태코드](#_Toc1745996796) | [1](#_Toc1745996796) | [0..n](#_Toc1745996796) | [1](#_Toc1745996796) | [1:등록, 2:탈퇴](#_Toc1745996796) |
| [wkplStylDvcd](#_Toc1745996796) | [사업장형태구분코드](#_Toc1745996796) | [1](#_Toc1745996796) | [0..n](#_Toc1745996796) | [1](#_Toc1745996796) | [1:법인, 2:개인](#_Toc1745996796) |
| [ldongAddrMgplDgCd](#_Toc1745996796) | [법정동주소광역시도코드](#_Toc1745996796) | [2](#_Toc1745996796) | [0..n](#_Toc1745996796) | [41](#_Toc1745996796) | [시도(행정자치부 법정동 주소코드 참조)](#_Toc1745996796) |
| [ldongAddrMgplSgguCd](#_Toc1745996796) | [법정동주소시군구코드](#_Toc1745996796) | [5](#_Toc1745996796) | [0..n](#_Toc1745996796) | [117](#_Toc1745996796) | [시군구(행정자치부 법정동 주소코드 참조)](#_Toc1745996796) |
| [ldongAddrMgplSgguEmdCd](#_Toc1745996796) | [법정동주소읍면동코드](#_Toc1745996796) | [8](#_Toc1745996796) | [0..n](#_Toc1745996796) | [102](#_Toc1745996796) | [읍면동(행정자치부 법정동 주소코드 참조)](#_Toc1745996796) |
| [pageNo](#_Toc1745996796) | [페이지 번호](#_Toc1745996796) | [4](#_Toc1745996796) | [1](#_Toc1745996796) | [1](#_Toc1745996796) | [페이지번호](#_Toc1745996796) |
| [numOfRows](#_Toc1745996796) | [한 페이지 결과 수](#_Toc1745996796) | [4](#_Toc1745996796) | [1](#_Toc1745996796) | [10](#_Toc1745996796) | [한 페이지 결과 수](#_Toc1745996796) |
| [totalCount](#_Toc1745996796) | [데이터 총 개수](#_Toc1745996796) | [4](#_Toc1745996796) | [1](#_Toc1745996796) | [1](#_Toc1745996796) | [데이터 총 개수](#_Toc1745996796) |

[※ 항목구분 : 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)](#_Toc1745996796)

#####

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr>
<th><a href="#_Toc1745996796">요청 / 응답 메시지 예제REST(URI)</a></th>
</tr>
</thead>
<tbody>
<tr>
<td><p><a href="#_Toc1745996796">http://apis.data.go.kr/B552015/NpsBplcInfoInqireServiceV2/getBassInfoSearchV2?ldongAddrMgplDgCd=11&amp;ldongAddrMgplSgguCd=117&amp;ldongAddrMgplSgguEmdCd=102&amp;wkplNm=삼성전자로지텍주식회사&amp;bzowrRgstNo=124815&amp;dataType=json&amp;pageNo=10&amp;numOfRows=1&amp;serviceKey=서비스인증키</a></p>
<p><a href="#_Toc1745996796">(단, 익스플로러에서 확인 시 파라미터 입력이 한글인 경우 utf-8로 인코딩 필요)</a></p>
<ul>
<li></li>
</ul>
<p><a href="#_Toc1745996796">Explorer:http://apis.data.go.kr/B552015/NpsBplcInfoInqireServiceV2/getBassInfoSearchV2?ldongAddrMgplDgCd=41&amp;ldongAddrMgplSgguCd=117&amp;ldongAddrMgplSgguEmdCd=102&amp;wkplNm%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90%EB%A1%9C%EC%A7%80%ED%85%8D%EC%A3%BC%EC%8B%9D%ED%9A%8C%EC%82%AC&amp;bzowrRgstNo=124815&amp;dataType=json&amp;pageNo=1&amp;&amp;numOfRows=1&amp;serviceKey=서비스인증키</a></p></td>
</tr>
<tr>
<td><a href="#_Toc1745996796">응답 메시지</a></td>
</tr>
<tr>
<td style="text-align: left;"><p><a href="#_Toc1745996796">{</a></p>
<p><a href="#_Toc1745996796">“response”: {</a></p>
<p><a href="#_Toc1745996796">“header”: {</a></p>
<p><a href="#_Toc1745996796">“resultCode”: “00”,</a></p>
<p><a href="#_Toc1745996796">“resultMsg”: “NORMAL_CODE”</a></p>
<p><a href="#_Toc1745996796">},</a></p>
<p><a href="#_Toc1745996796">“body”: {</a></p>
<p><a href="#_Toc1745996796">“items”: {</a></p>
<p><a href="#_Toc1745996796">“item”: [{</a></p>
<blockquote>
<p><a href="#_Toc1745996796">“dataCrtYm”: “202501”,</a></p>
<p><a href="#_Toc1745996796">“seq”: 561457,</a></p>
<p><a href="#_Toc1745996796">“wkplNm”: “삼성전자로지텍주식회사”,</a></p>
<p><a href="#_Toc1745996796">“bzowrRgstNo”: “124815****”,</a></p>
<p><a href="#_Toc1745996796">“wkplRoadNmDtlAddr”: “경기도 수원시 영통구 삼성로”,</a></p>
<p><a href="#_Toc1745996796">“wkplJnngStcd”: “1”,</a></p>
<p><a href="#_Toc1745996796">“wkplStylDvcd”: “1”</a></p>
</blockquote>
<p><a href="#_Toc1745996796">“ldongAddrMgplDgCd”: “41”,</a></p>
<p><a href="#_Toc1745996796">“ldongAddrMgplSgguCd”: “117”,</a></p>
<p><a href="#_Toc1745996796">“ldongAddrMgplSgguEmdCd”: “102”</a></p>
<p><a href="#_Toc1745996796">}]</a></p>
<p><a href="#_Toc1745996796">},</a></p>
<p><a href="#_Toc1745996796">“pageNo”: 1,</a></p>
<p><a href="#_Toc1745996796">“numOfRows”: 10</a></p>
<p><a href="#_Toc1745996796">“totalCount”: 14</a></p>
<p><a href="#_Toc1745996796">}</a></p>
<p><a href="#_Toc1745996796">}</a></p>
<p><a href="#_Toc1745996796">}</a></p></td>
</tr>
</tbody>
</table>

####

<table style="width:100%;">
<colgroup>
<col style="width: 14%" />
<col style="width: 23%" />
<col style="width: 16%" />
<col style="width: 23%" />
<col style="width: 22%" />
</colgroup>
<thead>
<tr>
<th rowspan="6"><a href="#_Toc1745996796">상세 정보조회 오퍼레이션 명세오퍼레이션 정보</a></th>
<th><a href="#_Toc1745996796">오퍼레이션 번호</a></th>
<th><a href="#_Toc1745996796">2</a></th>
<th><a href="#_Toc1745996796">오퍼레이션명(국문)</a></th>
<th><a href="#_Toc1745996796">상세 정보조회</a></th>
</tr>
<tr>
<th><a href="#_Toc1745996796">오퍼레이션 유형</a></th>
<th><a href="#_Toc1745996796">조회</a></th>
<th><a href="#_Toc1745996796">오퍼레이션명(영문)</a></th>
<th><a href="#_Toc1745996796">getDetailInfoSearchV2</a></th>
</tr>
<tr>
<th><a href="#_Toc1745996796">오퍼레이션 설명</a></th>
<th colspan="3"><a href="#_Toc1745996796">사업장 상세정보 조회</a></th>
</tr>
<tr>
<th><a href="#_Toc1745996796">Call Back URL</a></th>
<th colspan="3"><a href="#_Toc1745996796">N/A</a></th>
</tr>
<tr>
<th><a href="#_Toc1745996796">최대 메시지 사이즈</a></th>
<th colspan="3"><a href="#_Toc1745996796">[ 4000 bytes]</a></th>
</tr>
<tr>
<th><a href="#_Toc1745996796">평균 응답 시간</a></th>
<th><a href="#_Toc1745996796">[ 500 ms]</a></th>
<th><a href="#_Toc1745996796"><strong>초당 최대 트랜잭션</strong></a></th>
<th><a href="#_Toc1745996796">[ 30 ms]</a></th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="2"><a href="#_Toc1745996796">HTTP Method</a></td>
<td colspan="3"><a href="#_Toc1745996796">[ O ] REST (GET, POST, PUT, DELETE)</a></td>
</tr>
</tbody>
</table>

#####

<table style="width:100%;">
<colgroup>
<col style="width: 15%" />
<col style="width: 14%" />
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 15%" />
<col style="width: 31%" />
</colgroup>
<thead>
<tr>
<th><a href="#_Toc1745996796">요청 메시지 명세항목명(영문)</a></th>
<th><a href="#_Toc1745996796">항목명(국문)</a></th>
<th><a href="#_Toc1745996796">항목크기</a></th>
<th><a href="#_Toc1745996796">항목구분</a></th>
<th><a href="#_Toc1745996796">샘플데이터</a></th>
<th><a href="#_Toc1745996796">항목설명</a></th>
</tr>
</thead>
<tbody>
<tr>
<td><a href="#_Toc1745996796">seq</a></td>
<td><a href="#_Toc1745996796">식별번호</a></td>
<td><a href="#_Toc1745996796">10</a></td>
<td><a href="#_Toc1745996796">1</a></td>
<td><a href="#_Toc1745996796">5614757</a></td>
<td><a href="#_Toc1745996796">식별번호</a></td>
</tr>
<tr>
<td><a href="#_Toc1745996796">dataType</a></td>
<td><a href="#_Toc1745996796">응답자료형식</a></td>
<td><a href="#_Toc1745996796">4</a></td>
<td><a href="#_Toc1745996796">0</a></td>
<td><a href="#_Toc1745996796">json</a></td>
<td><a href="#_Toc1745996796">xml 또는 json<br />
기본값: xml</a></td>
</tr>
<tr>
<td><a href="#_Toc1745996796">pageNo</a></td>
<td><a href="#_Toc1745996796">페이지번호</a></td>
<td><a href="#_Toc1745996796">4</a></td>
<td><a href="#_Toc1745996796">0</a></td>
<td><a href="#_Toc1745996796">1</a></td>
<td><p><a href="#_Toc1745996796">페이지번호</a></p>
<p><a href="#_Toc1745996796">기본값: 1</a></p></td>
</tr>
<tr>
<td><a href="#_Toc1745996796">numOfRows</a></td>
<td><a href="#_Toc1745996796">한 페이지 결과 수</a></td>
<td><a href="#_Toc1745996796">4</a></td>
<td><a href="#_Toc1745996796">0</a></td>
<td><a href="#_Toc1745996796">10</a></td>
<td><p><a href="#_Toc1745996796">한 페이지 결과 수</a></p>
<p><a href="#_Toc1745996796">기본값: 10</a></p></td>
</tr>
<tr>
<td><a href="#_Toc1745996796">serviceKey</a></td>
<td><a href="#_Toc1745996796">서비스인증키</a></td>
<td><a href="#_Toc1745996796">400</a></td>
<td><a href="#_Toc1745996796">1</a></td>
<td><a href="#_Toc1745996796">서비스인증키</a></td>
<td><a href="#_Toc1745996796">공공데이터포털에서 발급받은 인증키</a></td>
</tr>
</tbody>
</table>

-

[항목구분 : 필수(1), 옵션(0)](#_Toc1745996796)

#####

| [응답 메시지 명세항목명(영문)](#_Toc1745996796) | [항목명(국문)](#_Toc1745996796) | [항목크기](#_Toc1745996796) | [항목구분](#_Toc1745996796) | [샘플데이터](#_Toc1745996796) | [항목설명](#_Toc1745996796) |
|----|----|----|----|----|----|
| [wkplNm](#_Toc1745996796) | [사업장명](#_Toc1745996796) | [100](#_Toc1745996796) | [0..1](#_Toc1745996796) | [삼성전자로지텍주식회사](#_Toc1745996796) | [사업장명](#_Toc1745996796) |
| [bzowrRgstNo](#_Toc1745996796) | [사업자등록번호](#_Toc1745996796) | [10](#_Toc1745996796) | [0..1](#_Toc1745996796) | [124815\*\*\*\*](#_Toc1745996796) | [사업자등록번호(앞에서 6자리)](#_Toc1745996796) |
| [wkplRoadNmDtlAddr](#_Toc1745996796) | [사업장도로명상세주소](#_Toc1745996796) | [300](#_Toc1745996796) | [0..1](#_Toc1745996796) | [경기도 수원시 영통구 삼성로](#_Toc1745996796) | [사업장도로명상세주소](#_Toc1745996796) |
| [wkplJnngStcd](#_Toc1745996796) | [사업장가입상태코드](#_Toc1745996796) | [1](#_Toc1745996796) | [0..1](#_Toc1745996796) | [1](#_Toc1745996796) | [1:등록, 2:탈퇴](#_Toc1745996796) |
| [ldongAddrMgplDgCd](#_Toc1745996796) | [법정동주소광역시도코드](#_Toc1745996796) | [2](#_Toc1745996796) | [0..1](#_Toc1745996796) | [41](#_Toc1745996796) | [시도(행정자치부 법정동 주소코드 참조)](#_Toc1745996796) |
| [ldongAddrMgplSgguCd](#_Toc1745996796) | [법정동주소시군구코드](#_Toc1745996796) | [5](#_Toc1745996796) | [0..1](#_Toc1745996796) | [117](#_Toc1745996796) | [시군구(행정자치부 법정동 주소코드 참조)](#_Toc1745996796) |
| [ldongAddrMgplSgguEmdCd](#_Toc1745996796) | [법정동주소읍면동코드](#_Toc1745996796) | [8](#_Toc1745996796) | [0..1](#_Toc1745996796) | [102](#_Toc1745996796) | [읍면동(행정자치부 법정동 주소코드 참조)](#_Toc1745996796) |
| [wkplStylDvcd](#_Toc1745996796) | [사업장형태구분코드](#_Toc1745996796) | [1](#_Toc1745996796) | [0..1](#_Toc1745996796) | [1](#_Toc1745996796) | [1:법인, 2:개인](#_Toc1745996796) |
| [wkplIntpCd](#_Toc1745996796) | [사업업종코드](#_Toc1745996796) | [6](#_Toc1745996796) | [0..1](#_Toc1745996796) | [630201](#_Toc1745996796) | [사업업종코드(국세청 업종코드 참조)](#_Toc1745996796) |
| [vldtVlKrnNm](#_Toc1745996796) | [사업장업종코드명](#_Toc1745996796) | [200](#_Toc1745996796) | [0..1](#_Toc1745996796) | [일반 창고업](#_Toc1745996796) | [사업장업종코드명](#_Toc1745996796) |
| [adptDt](#_Toc1745996796) | [사업장등록일](#_Toc1745996796) | [8](#_Toc1745996796) | [0..1](#_Toc1745996796) | [19980401](#_Toc1745996796) | [사업장등록일](#_Toc1745996796) |
| [scsnDt](#_Toc1745996796) | [사업장탈퇴일](#_Toc1745996796) | [8](#_Toc1745996796) | [0..1](#_Toc1745996796) | [00010101](#_Toc1745996796) | [사업장탈퇴일](#_Toc1745996796) |
| [jnngpCnt](#_Toc1745996796) | [가입자수](#_Toc1745996796) | [4](#_Toc1745996796) | [0..1](#_Toc1745996796) | [556](#_Toc1745996796) | [가입자수](#_Toc1745996796) |
| [crrmmNtcAmt](#_Toc1745996796) | [당월고지금액](#_Toc1745996796) | [4](#_Toc1745996796) | [0..1](#_Toc1745996796) | [299087800](#_Toc1745996796) | [당월고지금액](#_Toc1745996796) |
| [pageNo](#_Toc1745996796) | [페이지 번호](#_Toc1745996796) | [4](#_Toc1745996796) | [1](#_Toc1745996796) | [1](#_Toc1745996796) | [페이지번호](#_Toc1745996796) |
| [numOfRows](#_Toc1745996796) | [한 페이지 결과 수](#_Toc1745996796) | [4](#_Toc1745996796) | [1](#_Toc1745996796) | [10](#_Toc1745996796) | [한 페이지 결과 수](#_Toc1745996796) |
| [totalCount](#_Toc1745996796) | [데이터 총 개수](#_Toc1745996796) | [4](#_Toc1745996796) | [1](#_Toc1745996796) | [1](#_Toc1745996796) | [데이터 총 개수](#_Toc1745996796) |

[※ 항목구분 : 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)](#_Toc1745996796)

#####

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr>
<th><a href="#_Toc1745996796">요청 / 응답 메시지 예제REST(URI)</a></th>
</tr>
</thead>
<tbody>
<tr>
<td><a href="#_Toc1745996796">http://apis.data.go.kr/B552015/NpsBplcInfoInqireServiceV2/getDetailInfoSearchV2?seq=5614757&amp;dataType=json&amp;pageNo=1&amp;numOfRows=10&amp;serviceKey=서비스인증키</a></td>
</tr>
<tr>
<td><a href="#_Toc1745996796">응답 메시지</a></td>
</tr>
<tr>
<td style="text-align: left;"><p><a href="#_Toc1745996796">{</a></p>
<p><a href="#_Toc1745996796">“response”: {</a></p>
<p><a href="#_Toc1745996796">“header”: {</a></p>
<p><a href="#_Toc1745996796">“resultCode”: “00”,</a></p>
<p><a href="#_Toc1745996796">“resultMsg”: “NORMAL_CODE”</a></p>
<p><a href="#_Toc1745996796">},</a></p>
<p><a href="#_Toc1745996796">“body”: {</a></p>
<p><a href="#_Toc1745996796">“items”: {</a></p>
<p><a href="#_Toc1745996796">“item”: [{</a></p>
<blockquote>
<p><a href="#_Toc1745996796">“wkplNm”: “삼성전자로지텍주식회사”,</a></p>
<p><a href="#_Toc1745996796">“bzowrRgstNo”: “124815****”,</a></p>
<p><a href="#_Toc1745996796">“wkplRoadNmDtlAddr”: “경기도 수원시 영통구 삼성로”,</a></p>
<p><a href="#_Toc1745996796">“wkplJnngStcd”: “1”,</a></p>
<p><a href="#_Toc1745996796">“ldongAddrMgplDgCd”: “41”,</a></p>
</blockquote>
<p><a href="#_Toc1745996796">“ldongAddrMgplSgguCd”: “117”,</a></p>
<p><a href="#_Toc1745996796">“ldongAddrMgplSgguEmdCd”: “102”,</a></p>
<blockquote>
<p><a href="#_Toc1745996796">“wkplStylDvcd”: “1”</a></p>
<p><a href="#_Toc1745996796">“wkplIntpCd”: “630201”,</a></p>
<p><a href="#_Toc1745996796">“vldtVlKrnNm”: “일반 창고업”,</a></p>
<p><a href="#_Toc1745996796">“adptDt”: “19880101”,</a></p>
<p><a href="#_Toc1745996796">“scsnDt”: “00010101”,</a></p>
<p><a href="#_Toc1745996796">“jnngpCnt”: 556,</a></p>
<p><a href="#_Toc1745996796">“crrmmNtcAmt”: “299087800”</a></p>
</blockquote>
<p><a href="#_Toc1745996796">}]</a></p>
<p><a href="#_Toc1745996796">},</a></p>
<p><a href="#_Toc1745996796">“pageNo”: 1,</a></p>
<p><a href="#_Toc1745996796">“numOfRows”: 10</a></p>
<p><a href="#_Toc1745996796">“totalCount”: 1</a></p>
<p><a href="#_Toc1745996796">}</a></p>
<p><a href="#_Toc1745996796">}</a></p>
<p><a href="#_Toc1745996796">}</a></p></td>
</tr>
</tbody>
</table>

####

<table>
<colgroup>
<col style="width: 12%" />
<col style="width: 21%" />
<col style="width: 14%" />
<col style="width: 21%" />
<col style="width: 29%" />
</colgroup>
<thead>
<tr>
<th rowspan="6"><a href="#_Toc1745996796">기간별 현황 정보조회 오퍼레이션 명세 오퍼레이션 정보</a></th>
<th><a href="#_Toc1745996796">오퍼레이션 번호</a></th>
<th><a href="#_Toc1745996796">3</a></th>
<th><a href="#_Toc1745996796">오퍼레이션명(국문)</a></th>
<th><a href="#_Toc1745996796">기간별 현황 정보조회</a></th>
</tr>
<tr>
<th><a href="#_Toc1745996796">오퍼레이션 유형</a></th>
<th><a href="#_Toc1745996796">조회</a></th>
<th><a href="#_Toc1745996796">오퍼레이션명(영문)</a></th>
<th><a href="#_Toc1745996796">getPdAcctoSttusInfoSearchV2</a></th>
</tr>
<tr>
<th><a href="#_Toc1745996796">오퍼레이션 설명</a></th>
<th colspan="3"><a href="#_Toc1745996796">사업장 기간별 현황 정보조회</a></th>
</tr>
<tr>
<th><a href="#_Toc1745996796">Call Back URL</a></th>
<th colspan="3"><a href="#_Toc1745996796">N/A</a></th>
</tr>
<tr>
<th><a href="#_Toc1745996796">최대 메시지 사이즈</a></th>
<th colspan="3"><a href="#_Toc1745996796">[ 4000 bytes]</a></th>
</tr>
<tr>
<th><a href="#_Toc1745996796">평균 응답 시간</a></th>
<th><a href="#_Toc1745996796">[ 500 ms]</a></th>
<th><a href="#_Toc1745996796"><strong>초당 최대 트랜잭션</strong></a></th>
<th><a href="#_Toc1745996796">[ 30 ms]</a></th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="2"><a href="#_Toc1745996796">HTTP Method</a></td>
<td colspan="3"><a href="#_Toc1745996796">[ O ] REST (GET, POST, PUT, DELETE)</a></td>
</tr>
</tbody>
</table>

#####

<table style="width:100%;">
<colgroup>
<col style="width: 15%" />
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 20%" />
<col style="width: 21%" />
</colgroup>
<thead>
<tr>
<th><a href="#_Toc1745996796">요청 메시지 명세항목명(영문)</a></th>
<th><a href="#_Toc1745996796">항목명(국문)</a></th>
<th><a href="#_Toc1745996796">항목크기</a></th>
<th><a href="#_Toc1745996796">항목구분</a></th>
<th><a href="#_Toc1745996796">샘플데이터</a></th>
<th><a href="#_Toc1745996796">항목설명</a></th>
</tr>
</thead>
<tbody>
<tr>
<td><a href="#_Toc1745996796">seq</a></td>
<td><a href="#_Toc1745996796">식별번호</a></td>
<td><a href="#_Toc1745996796">10</a></td>
<td><a href="#_Toc1745996796">1</a></td>
<td><a href="#_Toc1745996796">5614757</a></td>
<td><a href="#_Toc1745996796">식별번호</a></td>
</tr>
<tr>
<td><a href="#_Toc1745996796">dataCrtYm</a></td>
<td><a href="#_Toc1745996796">년월(yyyymm)</a></td>
<td><a href="#_Toc1745996796">6</a></td>
<td><a href="#_Toc1745996796">0</a></td>
<td><a href="#_Toc1745996796">202502</a></td>
<td><a href="#_Toc1745996796">년월(yyyymm)</a></td>
</tr>
<tr>
<td><a href="#_Toc1745996796">dataType</a></td>
<td><a href="#_Toc1745996796">응답자료형식</a></td>
<td><a href="#_Toc1745996796">4</a></td>
<td><a href="#_Toc1745996796">0</a></td>
<td><a href="#_Toc1745996796">json</a></td>
<td><a href="#_Toc1745996796">xml 또는 json<br />
기본값: xml</a></td>
</tr>
<tr>
<td><a href="#_Toc1745996796">pageNo</a></td>
<td><a href="#_Toc1745996796">페이지번호</a></td>
<td><a href="#_Toc1745996796">4</a></td>
<td><a href="#_Toc1745996796">0</a></td>
<td><a href="#_Toc1745996796">1</a></td>
<td><p><a href="#_Toc1745996796">페이지번호</a></p>
<p><a href="#_Toc1745996796">기본값: 1</a></p></td>
</tr>
<tr>
<td><a href="#_Toc1745996796">numOfRows</a></td>
<td><a href="#_Toc1745996796">한 페이지 결과 수</a></td>
<td><a href="#_Toc1745996796">4</a></td>
<td><a href="#_Toc1745996796">0</a></td>
<td><a href="#_Toc1745996796">10</a></td>
<td><p><a href="#_Toc1745996796">한 페이지 결과 수</a></p>
<p><a href="#_Toc1745996796">기본값: 10</a></p></td>
</tr>
<tr>
<td><a href="#_Toc1745996796">serviceKey</a></td>
<td><a href="#_Toc1745996796">서비스인증키</a></td>
<td><a href="#_Toc1745996796">400</a></td>
<td><a href="#_Toc1745996796">1</a></td>
<td><a href="#_Toc1745996796">서비스인증키</a></td>
<td><a href="#_Toc1745996796">공공데이터포털에서 발급받은 인증키</a></td>
</tr>
</tbody>
</table>

-

[항목구분 : 필수(1), 옵션(0)](#_Toc1745996796)

#####

| [응답 메시지 명세항목명(영문)](#_Toc1745996796) | [항목명(국문)](#_Toc1745996796) | [항목크기](#_Toc1745996796) | [항목구분](#_Toc1745996796) | [샘플데이터](#_Toc1745996796) | [항목설명](#_Toc1745996796) |
|----|----|----|----|----|----|
| [nwAcqzrCnt](#_Toc1745996796) | [월별 취업자수](#_Toc1745996796) | [4](#_Toc1745996796) | [0..1](#_Toc1745996796) | [12](#_Toc1745996796) | [월별 취업자수](#_Toc1745996796) |
| [lssJnngpCnt](#_Toc1745996796) | [월별 퇴직자수](#_Toc1745996796) | [4](#_Toc1745996796) | [0..1](#_Toc1745996796) | [5](#_Toc1745996796) | [월별 퇴직자수](#_Toc1745996796) |
| [pageNo](#_Toc1745996796) | [페이지 번호](#_Toc1745996796) | [4](#_Toc1745996796) | [1](#_Toc1745996796) | [1](#_Toc1745996796) | [페이지번호](#_Toc1745996796) |
| [numOfRows](#_Toc1745996796) | [한 페이지 결과 수](#_Toc1745996796) | [4](#_Toc1745996796) | [1](#_Toc1745996796) | [10](#_Toc1745996796) | [한 페이지 결과 수](#_Toc1745996796) |
| [totalCount](#_Toc1745996796) | [데이터 총 개수](#_Toc1745996796) | [4](#_Toc1745996796) | [1](#_Toc1745996796) | [1](#_Toc1745996796) | [데이터 총 개수](#_Toc1745996796) |

[※ 항목구분 : 1건 이상 복수건(1..n), 0건 또는 복수건(0..n)](#_Toc1745996796)

#####

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr>
<th><a href="#_Toc1745996796">요청 / 응답 메시지 예제REST(URI)</a></th>
</tr>
</thead>
<tbody>
<tr>
<td><a href="#_Toc1745996796">http://apis.data.go.kr/B552015/NpsBplcInfoInqireServiceV2/getPdAcctoSttusInfoSearchV2?seq=5614757&amp;dataCrtYm=202502&amp;serviceKey=서비스인증키</a></td>
</tr>
<tr>
<td><a href="#_Toc1745996796">응답 메시지</a></td>
</tr>
<tr>
<td style="text-align: left;"><p><a href="#_Toc1745996796">{</a></p>
<p><a href="#_Toc1745996796">“response”: {</a></p>
<p><a href="#_Toc1745996796">“header”: {</a></p>
<p><a href="#_Toc1745996796">“resultCode”: “00”,</a></p>
<p><a href="#_Toc1745996796">“resultMsg”: “NORMAL_CODE”</a></p>
<p><a href="#_Toc1745996796">},</a></p>
<p><a href="#_Toc1745996796">“body”: {</a></p>
<p><a href="#_Toc1745996796">“items”: {</a></p>
<p><a href="#_Toc1745996796">“item”: [{</a></p>
<p><a href="#_Toc1745996796">“lssJnngpCnt”: 12,</a></p>
<p><a href="#_Toc1745996796">“nwAcqzrCnt”: 5</a></p>
<p><a href="#_Toc1745996796">}]</a></p>
<p><a href="#_Toc1745996796">},</a></p>
<p><a href="#_Toc1745996796">“pageNo”: 1,</a></p>
<p><a href="#_Toc1745996796">“numOfRows”: 10</a></p>
<p><a href="#_Toc1745996796">“totalCount”: 1</a></p>
<p><a href="#_Toc1745996796">}</a></p>
<p><a href="#_Toc1745996796">}</a></p>
<p><a href="#_Toc1745996796">}</a></p></td>
</tr>
</tbody>
</table>
