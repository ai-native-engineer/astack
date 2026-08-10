# Meta Ads CLI 설정 가이드

설치 → 인증(토큰) → 설정 구성 순서. 공식 문서가 흩어 놓은 절차를 실측 함정과 함께 한 곳에 정리한 것. 전체 명령 옵션은 `meta <cmd> --help`, 공식 절차는 `developers.facebook.com/.../ads-cli/setup/get-started` 참조.

## 1. 설치

```bash
uv tool install meta-ads --python 3.13   # python 3.14 환경은 wheel 없음 → 3.13 명시
meta --version                            # 실행 파일은 `meta`
```

## 2. 인증 — 시스템 사용자 토큰 (장기, 운영용)

정석 경로. **전제: 비즈니스 포트폴리오(Business Manager)에 광고 계정이 연결돼 있어야** 한다. 전부 브라우저 작업이라 자동화 불가 — 사용자가 직접 수행한다.

1. **앱 준비** — [developers.facebook.com/apps](https://developers.facebook.com/apps)에서 앱 생성(유형: 비즈니스). 토큰은 특정 앱에 묶여 발급된다.
2. **Admin 시스템 사용자 생성** — 비즈니스 설정 → `사용자` → `시스템 사용자` → `추가`, 역할 **관리자(Admin)**.
3. **광고 계정 할당** — ⚠️ **핵심 함정**: 시스템 사용자 화면의 `자산 할당` 팝업에는 자산 유형이 *Facebook 페이지 / 앱 / Instagram 계정*만 나오고 **광고 계정이 없다**. 비즈니스에 등록 안 된 광고 계정은 안 뜬다. → 광고 계정을 비즈니스에 먼저 연결한 뒤, `계정 → 광고 계정 → 해당 계정 → 사람`에서 **"사람(시스템 유저) 할당"**으로 붙인다 (시스템 사용자 쪽 "자산 할당"이 아니라 광고 계정 쪽 "사람 할당"이 정답).
4. **시스템 사용자를 앱 Admin으로** — 앱 → `앱 설정` → `역할(Roles)`에 시스템 사용자를 App Admin으로 추가.
5. **토큰 생성** — 시스템 사용자 화면 → `토큰 생성` → 앱 선택 → 스코프 7개 체크:
   ```
   business_management   ads_management        pages_show_list
   pages_read_engagement pages_manage_ads      catalog_management
   read_insights
   ```
   ⚠️ 권한 목록은 **알파벳순**이라 `ads_management`·`business_management`·`catalog_management`(a/b/c)와 `pages_manage_ads`가 위로 잘려 안 보이기 쉽다 → 검색창에 이름을 직접 입력. 검색해도 `ads_management`가 없으면 앱에 **마케팅 API(Marketing API) 제품**이 추가 안 된 것 → 앱 대시보드에서 제품 추가 후 재시도.
6. **토큰은 한 번만 표시된다.** 즉시 복사. 비밀번호처럼 취급(채팅·커밋에 노출 금지).

### 빠른 대안 — 임시 토큰 (테스트용)
비즈니스 매니저 연결이 막히면 [Graph API Explorer](https://developers.facebook.com/tools/explorer)에서 즉시 발급. 1~2시간 만료. 본인이 관리자인 광고 계정에 개인 자격으로 접근 가능. CLI 동작 확인용으로만.

## 3. 설정 구성

`meta`는 토큰·계정을 다음 순서로 읽는다: **CLI 플래그 > 셸 env > `.env`(cwd부터 상위 탐색) > `~/.config/meta/credentials`(토큰만)**.

### A. 프로젝트 단위 — `.env`

`meta`를 실행할 디렉토리(또는 그 상위)에 둔다. `.env`는 `find_dotenv`로 **cwd부터 상위**로 탐색하므로 그 경로에서 실행해야 적용된다.

```bash
ACCESS_TOKEN=<발급받은 토큰>
AD_ACCOUNT_ID=<숫자 ID>          # adaccount list의 id에서 act_ 떼고 숫자만
# BUSINESS_ID=<ID>              # 카탈로그/데이터셋 명령 쓸 때만
```

```bash
chmod 600 .env                  # 본인만 접근
printf '.env\n' >> .gitignore   # 실수 커밋 방지
```

### B. 글로벌 단위 — 어느 디렉토리에서나

토큰과 계정의 저장 위치가 **다르다**:

```bash
# 토큰: ~/.config/meta/credentials — 토큰 문자열 그 자체만 (plain text, JSON 아님)
printf '%s' "<발급받은 토큰>" > ~/.config/meta/credentials   # trailing newline 없이
chmod 600 ~/.config/meta/credentials

# 계정: 글로벌 전용 저장소 없음 → 셸 env로 export (계정 ID는 비밀값 아님)
echo 'export AD_ACCOUNT_ID=<숫자 ID>' >> ~/.zshrc
```

⚠️ `~/.config/meta/credentials`는 **토큰 전용**. `AD_ACCOUNT_ID`는 여기 못 둔다(`~/.config/meta/.env`도 안 읽힘) → `~/.zshrc` export 또는 매번 `--ad-account-id`.

경로가 의심되면 추측하지 말고 도구에 직접 묻는다 — 소스가 컴파일된 `.so`라 파일을 읽어서는 확인되지 않는다.

```bash
~/.local/share/uv/tools/meta-ads/bin/python -c "from meta import config; print(config.get_credentials_path())"
```

## 검증 체크리스트

- `meta auth status` → `Authenticated`
- `meta ads adaccount current` → 설정한 계정 ID
- `meta ads campaign list` → 캠페인 목록(없으면 빈 표)
