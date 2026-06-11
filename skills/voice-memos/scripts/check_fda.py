"""launchd 컨텍스트에서 Recordings 폴더가 보이는지 확인하는 FDA 검증용 스크립트."""

import os

p = os.path.expanduser(
    "~/Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings"
)
try:
    n = len([f for f in os.listdir(p) if f.endswith((".m4a", ".qta"))])
    print(f"FDA_CHECK count={n}")
except Exception as e:  # noqa: BLE001 - 권한 거부 포함 모든 예외를 그대로 보고
    print(f"FDA_CHECK error={e!r}")
