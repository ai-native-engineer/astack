# 설치와 권한 진단

## 설치와 버전

```bash
command -v katok || cargo install katok
katok --help
```

`katok`이 없으면 읽기와 검색을 중단한다. 접근성 스크래핑으로 폴백하지 않는다.

`--help` 목록에 필요한 서브커맨드가 없으면 설치본이 오래된 것이다. `cargo install katok`으로 올린다. 발송은 기본 빌드에 들어 있고, 읽기 전용으로만 설치하려면 `cargo install katok --no-default-features`를 쓴다.

## 읽기와 검색 전제 조건

1. `katok permissions macos`로 System Settings를 열고, 현재 터미널 앱 또는 `katok` 실행 파일에 Full Disk Access를 허용한다.
2. `katok doctor --json`으로 아카이브와 최신성을 확인한다.
3. 앱, 컨테이너, DB 권한 진단이 필요할 때만 `katok doctor --macos-probe --json`을 실행한다. macOS 권한 prompt가 뜰 수 있다.

최초 `katok sync --source macos --json`은 오래 걸리고 도는 동안 검색과 읽기가 함께 막히므로, 실행 전에 사용자에게 알린다.

## 발송 전제 조건

1. macOS용 카카오톡 앱을 실행한다.
2. System Settings > Privacy & Security > Accessibility에서 현재 터미널 앱을 허용한다.
3. 텍스트, 이미지, draft 모드에는 `--accept-use-policy`를 준다. 없으면 카카오톡 UI에 닿기 전에 거부된다.

## 발송 실패 원인 가르기

방 이름 문제와 권한 문제를 먼저 갈라야 엉뚱한 곳을 고치지 않는다.

| 신호 | 원인 | 다음 |
|---|---|---|
| 접근성 권한이 없다는 오류 | Accessibility 미허용 | 위 발송 전제 조건 2번, 필요하면 카카오톡과 터미널 재실행 |
| 카카오톡이 실행 중이 아니라는 오류 | 앱 미실행 | 앱 실행 |
| 이름이 모호해 거부됨 | 같은 이름의 방이 여럿 | `chatroom-lookup.md`의 `--chat` 지정 |
| 방을 찾지 못함 | 이름 불일치 또는 오픈채팅 탭 | `chatroom-lookup.md` |
| 정책 승인이 필요하다는 오류 | `--accept-use-policy` 누락 | 플래그 추가 |

권한이 실제로 반영됐는지는 목록 명령으로 확인한다. 전달이 일어나지 않는다.

```bash
katok send --list-windows --json
```
