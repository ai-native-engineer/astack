# DART 고유번호 목록 다운로드

> provider: opendart.fss.or.kr
> official: https://opendart.fss.or.kr/api/corpCode.xml
> checked: 2026-06-28 · 상태: 실호출 검증됨

## 언제 쓰나

DART 공시·재무 API 호출 전에 회사명으로 `corp_code`를 찾을 때 쓴다. 회사명 중복, 상장/비상장 구분, `stock_code` 대조가 필요한 DART/다트 기업 공시 조회의 시작점이다.

## Endpoint

- base: `https://opendart.fss.or.kr`
- operation: `/api/corpCode.xml`
- method: `GET`

## 키

- env: `API_K_DART`
- 주입 예: `agents-env run API_K_DART -- <명령>`

## 호출 예시

```bash
agents-env run API_K_DART -- python3 - <<'PY'
import io, os, urllib.parse, urllib.request, zipfile, xml.etree.ElementTree as ET

url = "https://opendart.fss.or.kr/api/corpCode.xml?" + urllib.parse.urlencode({
    "crtfc_key": os.environ["API_K_DART"],
})
raw = urllib.request.urlopen(url, timeout=60).read()
with zipfile.ZipFile(io.BytesIO(raw)) as zf:
    root = ET.fromstring(zf.read("CORPCODE.xml"))
for row in root.findall("list"):
    if row.findtext("corp_name") == "삼성전자":
        print(row.findtext("corp_code"), row.findtext("stock_code"))
        break
PY
```

## 필수/주요 파라미터

| 이름 | 의미 | 형식·예 |
|---|---|---|
| `crtfc_key` | DART 인증키 | `$API_K_DART` |

## 응답 핵심 필드

| 필드 | 의미 |
|---|---|
| `corp_code` | DART 고유번호 |
| `corp_name` | 정식 회사명 |
| `stock_code` | 종목코드. 비상장 기타법인은 공란일 수 있음 |
| `modify_date` | 수정일 |

## 페이징

없음. 전체 목록 zip을 내려받는다.

## 함정

- 응답은 zip이고 내부 파일명은 `CORPCODE.xml`이다.
- 2026-06-28 테스트 기준 전체 `list` row는 118,371건이었다.
- `stock_code` 공란을 DART 비대상으로 해석하지 않는다.
