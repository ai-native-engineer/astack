#!/bin/bash
set -euo pipefail
# 전사 추출 → 사전 교정 → 요약 생성 → 알림 전송을 순차 실행합니다.
# launchd WatchPaths에서 호출됩니다.
# 사용법: run.sh [--skip-notify]

# launchd는 최소 PATH(/usr/bin:/bin:...)만 주므로 apple-stt(~/scripts)와
# homebrew 도구를 못 찾는다. 비대화형 실행에서도 도구를 찾도록 PATH를 명시한다.
export PATH="$HOME/scripts:/opt/homebrew/bin:$PATH"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
LOG_DIR="$HOME/.voice-memos/logs"
LOG_FILE="$LOG_DIR/watcher.log"
TEMP_LOG=$(mktemp)
SKIP_NOTIFY=false

if [ "${1:-}" = "--skip-notify" ]; then
    SKIP_NOTIFY=true
fi

mkdir -p "$LOG_DIR"

# .env에서 Telegram 설정 로드
if [ -f "$PROJECT_DIR/.env" ]; then
    TELEGRAM_BOT_TOKEN=$(grep -s '^TELEGRAM_BOT_TOKEN=' "$PROJECT_DIR/.env" | cut -d'=' -f2)
    TELEGRAM_CHAT_ID=$(grep -s '^TELEGRAM_CHAT_ID=' "$PROJECT_DIR/.env" | cut -d'=' -f2)
fi

send_error_alert() {
    local msg="$1"
    if [ -n "${TELEGRAM_BOT_TOKEN:-}" ] && [ -n "${TELEGRAM_CHAT_ID:-}" ]; then
        local text
        text=$(printf '⚠️ *Voice Memos 파이프라인 에러*\n\n%s\n\n```\n%s\n```' "$msg" "$(tail -20 "$TEMP_LOG" 2>/dev/null)")
        local payload
        payload=$(printf '{"chat_id":"%s","text":"%s","parse_mode":"Markdown"}' "$TELEGRAM_CHAT_ID" "$text")
        curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
            -H "Content-Type: application/json" \
            -d "$payload" > /dev/null 2>&1 || true
    fi
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [ERROR] $msg" >> "$LOG_FILE"
}

trap 'send_error_alert "단계 실패 (exit code: $?)"' ERR

# 로그 로테이션: 1000줄 초과 시 최근 500줄만 유지
if [ -f "$LOG_FILE" ] && [ "$(wc -l < "$LOG_FILE")" -gt 1000 ]; then
    tail -500 "$LOG_FILE" > "$LOG_FILE.tmp" && mv "$LOG_FILE.tmp" "$LOG_FILE"
fi

# extract.py가 파일별로 lsof+안정화 대기(wait_until_settled)를 수행하므로
# 여기서는 짧게만 대기한다.
sleep 2

{
    echo "[$(date '+%H:%M:%S')] 1/4 음성메모 전사 추출"
    /opt/homebrew/bin/python3 "$SCRIPT_DIR/extract.py" --all

    echo "[$(date '+%H:%M:%S')] 2/4 통화 녹음 전사"
    /opt/homebrew/bin/python3 "$SCRIPT_DIR/transcribe_calls.py"

    echo "[$(date '+%H:%M:%S')] 3/4 요약 생성"
    cd "$PROJECT_DIR"
    unset CLAUDECODE
    /opt/homebrew/bin/uv run python "$SCRIPT_DIR/summarize.py"

    if [ "$SKIP_NOTIFY" = false ]; then
        echo "[$(date '+%H:%M:%S')] 4/4 알림 전송"
        /opt/homebrew/bin/python3 "$SCRIPT_DIR/notify.py"
    else
        echo "[$(date '+%H:%M:%S')] 4/4 알림 전송 (스킵)"
    fi
} > "$TEMP_LOG" 2>&1

if /opt/homebrew/bin/rg -q '[1-9]+/[0-9]+ (처리됨|전사됨|교정됨|요약됨|전송됨)' "$TEMP_LOG"; then
    {
        echo ""
        echo "=========================================="
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] 파이프라인 시작"
        echo "=========================================="
        cat "$TEMP_LOG"
        echo "[$(date '+%H:%M:%S')] 완료"
    } >> "$LOG_FILE"
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 변경 없음" >> "$LOG_FILE"
fi

rm "$TEMP_LOG"
