#!/bin/bash
# launchd(gui 도메인) 컨텍스트에서 음성 메모 폴더 접근이 되는지 검증한다.
# 실제 워처와 동일한 'bash -> python3' 체인으로 일회성 잡을 띄워 폴더 파일 개수만 센다.
# 전사/요약/알림 부작용 없음. 기존 워처 plist는 손대지 않는다.
set -euo pipefail

UID_=$(id -u)
LABEL="com.user.fda-check"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
INNER="$SCRIPT_DIR/_fda_check_inner.sh"
CHECK_PY="$SCRIPT_DIR/check_fda.py"
LOG="$HOME/.voice-memos/logs/fda-check.log"

mkdir -p "$(dirname "$LOG")"
rm -f "$LOG"

# 실제 run.sh와 동일하게 bash가 python3를 호출하도록 inner 스크립트 생성
cat > "$INNER" <<EOF
#!/bin/bash
/opt/homebrew/bin/python3 "$CHECK_PY"
EOF
chmod +x "$INNER"

# 검증 전용 LaunchAgent 생성
cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>$LABEL</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>$INNER</string>
    </array>
    <key>StandardOutPath</key>
    <string>$LOG</string>
    <key>StandardErrorPath</key>
    <string>$LOG</string>
</dict>
</plist>
EOF

launchctl bootout "gui/$UID_/$LABEL" 2>/dev/null || true
launchctl bootstrap "gui/$UID_" "$PLIST"
launchctl kickstart -k "gui/$UID_/$LABEL"
sleep 3

echo "=== 검증 결과 (launchd 컨텍스트) ==="
cat "$LOG" 2>/dev/null || echo "(로그 없음)"
echo

COUNT=$(grep -oE 'count=[0-9]+' "$LOG" 2>/dev/null | grep -oE '[0-9]+' | head -1 || true)
if [ -n "${COUNT:-}" ] && [ "$COUNT" -gt 0 ]; then
    echo "✅ FDA 부여 성공: launchd가 음성 메모 ${COUNT}개를 봅니다. 워처가 정상 동작합니다."
else
    echo "❌ 아직 0개로 보입니다. FDA가 적용 안 됐거나 /bin/bash 외 다른 대상이 필요합니다."
fi

# 정리: 검증 잡 제거, 기존 워처는 무손상
launchctl bootout "gui/$UID_/$LABEL" 2>/dev/null || true
rm -f "$PLIST" "$INNER"
echo "정리 완료 (검증 잡 제거됨, 기존 워처 plist 무손상)"
