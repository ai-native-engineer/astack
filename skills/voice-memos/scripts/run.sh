#!/bin/bash
set -Eeuo pipefail
umask 077

export PATH="$HOME/scripts:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="${VOICE_MEMOS_CONFIG_FILE:-$HOME/.config/voice-memos/.env}"
RUNTIME_DIR="${VOICE_MEMOS_RUNTIME_DIR:-$HOME/.voice-memos}"
LOG_DIR="$RUNTIME_DIR/logs"
LOG_FILE="$LOG_DIR/watcher.log"
LOCK_DIR="$RUNTIME_DIR/run.lock"
OWNER_FILE="$LOCK_DIR/owner"
QUEUE_DIR="$RUNTIME_DIR/run-queue"
PENDING_MARKER="$QUEUE_DIR/pending"
PYTHON="${VOICE_MEMOS_PYTHON:-python3}"
UV="${VOICE_MEMOS_UV:-uv}"
CURL="${VOICE_MEMOS_CURL:-curl}"
SKIP_NOTIFY=false
TEMP_LOG=""
LOCK_TOKEN="$$.$(date +%s).${RANDOM:-0}"
ALERT_SENT=false

if [ "${1:-}" = "--skip-notify" ]; then
    SKIP_NOTIFY=true
fi

mkdir -p "$LOG_DIR" "$QUEUE_DIR"
chmod 700 "$RUNTIME_DIR" "$LOG_DIR" "$QUEUE_DIR"
touch "$LOG_FILE"
chmod 600 "$LOG_FILE"

boot_identity() {
    /usr/sbin/sysctl -n kern.boottime 2>/dev/null || uname -a
}

process_start_identity() {
    ps -p "$1" -o lstart= 2>/dev/null | sed 's/^[[:space:]]*//;s/[[:space:]]*$//'
}

CURRENT_BOOT="$(boot_identity)"
CURRENT_START="$(process_start_identity $$)"

queue_pending() {
    if mkdir "$PENDING_MARKER" 2>/dev/null; then
        return 0
    fi
    if [ -d "$PENDING_MARKER" ] && [ ! -L "$PENDING_MARKER" ]; then
        return 0
    fi
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] PendingQueueWriteError" >> "$LOG_FILE"
    return 1
}

lock_is_live() {
    if [ ! -f "$OWNER_FILE" ]; then
        # ponytail: an incomplete lock gets five minutes to finish owner publication.
        [ -z "$(find "$LOCK_DIR" -prune -mmin +5 -print 2>/dev/null)" ]
        return
    fi
    local pid start boot
    pid="$(sed -n 's/^pid=//p' "$OWNER_FILE")"
    start="$(sed -n 's/^start=//p' "$OWNER_FILE")"
    boot="$(sed -n 's/^boot=//p' "$OWNER_FILE")"
    [[ "$pid" =~ ^[0-9]+$ ]] || return 1
    [ "$boot" = "$CURRENT_BOOT" ] || return 1
    kill -0 "$pid" 2>/dev/null || return 1
    [ "$(process_start_identity "$pid")" = "$start" ]
}

publish_owner() {
    local temporary="$LOCK_DIR/owner.tmp.$$"
    {
        printf 'pid=%s\n' "$$"
        printf 'start=%s\n' "$CURRENT_START"
        printf 'boot=%s\n' "$CURRENT_BOOT"
        printf 'token=%s\n' "$LOCK_TOKEN"
    } > "$temporary"
    mv "$temporary" "$OWNER_FILE"
}

acquire_lock() {
    if mkdir "$LOCK_DIR" 2>/dev/null; then
        publish_owner
        return 0
    fi
    if lock_is_live; then
        if ! queue_pending; then
            return 2
        fi
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] PipelineBusy" >> "$LOG_FILE"
        return 1
    fi

    echo "[$(date '+%Y-%m-%d %H:%M:%S')] StalePipelineLock" >> "$LOG_FILE"
    rm -f -- "$OWNER_FILE" "$LOCK_DIR"/owner.tmp.* 2>/dev/null || true
    rmdir "$LOCK_DIR" 2>/dev/null || true
    if mkdir "$LOCK_DIR" 2>/dev/null; then
        publish_owner
        return 0
    fi
    if ! queue_pending; then
        return 2
    fi
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] PipelineBusy" >> "$LOG_FILE"
    return 1
}

ACQUIRE_STATUS=0
acquire_lock || ACQUIRE_STATUS=$?
case "$ACQUIRE_STATUS" in
    0) ;;
    1) exit 0 ;;
    *) exit 1 ;;
esac

load_local_config() {
    [ -f "$CONFIG_FILE" ] || return 0
    while IFS='=' read -r key value; do
        case "$key" in
            TELEGRAM_BOT_TOKEN) TELEGRAM_BOT_TOKEN="$value" ;;
            TELEGRAM_CHAT_ID) TELEGRAM_CHAT_ID="$value" ;;
        esac
    done < "$CONFIG_FILE"
}

send_error_alert() {
    ALERT_SENT=true
    local message="Voice Memos batch failed: stage=run code=PipelineFailed"
    if [ -n "${TELEGRAM_BOT_TOKEN:-}" ] && [ -n "${TELEGRAM_CHAT_ID:-}" ]; then
        local payload
        if payload="$($PYTHON -c 'import json,sys; print(json.dumps({"chat_id":sys.argv[1],"text":sys.argv[2]}))' "$TELEGRAM_CHAT_ID" "$message")"; then
            "$CURL" -sS -X POST \
                "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
                -H "Content-Type: application/json" -d "$payload" >/dev/null 2>&1 || true
        fi
    fi
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [ERROR] PipelineFailed" >> "$LOG_FILE"
}

cleanup() {
    local status=$?
    if [ "$status" -ne 0 ] && [ "$ALERT_SENT" = false ]; then
        send_error_alert
    fi
    if [ -n "$TEMP_LOG" ]; then
        rm -f -- "$TEMP_LOG"
    fi
    if [ -f "$OWNER_FILE" ] && grep -Fqx "token=$LOCK_TOKEN" "$OWNER_FILE"; then
        rm -f -- "$OWNER_FILE"
        rmdir "$LOCK_DIR" 2>/dev/null || true
    fi
}
trap cleanup EXIT

load_local_config
TEMP_LOG="$(mktemp "$RUNTIME_DIR/run.XXXXXX")"

if [ -f "$LOG_FILE" ] && [ "$(wc -l < "$LOG_FILE")" -gt 1000 ]; then
    tail -500 "$LOG_FILE" > "$LOG_FILE.tmp"
    mv "$LOG_FILE.tmp" "$LOG_FILE"
fi

run_pass() {
    local status=0
    {
        echo "[$(date '+%H:%M:%S')] 1/4 voice memo transcription"
        "$PYTHON" "$SCRIPT_DIR/extract.py" --all || status=1

        echo "[$(date '+%H:%M:%S')] 2/4 call transcription"
        "$PYTHON" "$SCRIPT_DIR/transcribe_calls.py" || status=1

        echo "[$(date '+%H:%M:%S')] 3/4 summary"
        cd "$PROJECT_DIR"
        unset CLAUDECODE
        "$UV" run python "$SCRIPT_DIR/summarize.py" || status=1

        if [ "$SKIP_NOTIFY" = false ]; then
            echo "[$(date '+%H:%M:%S')] 4/4 notification"
            "$PYTHON" "$SCRIPT_DIR/notify.py" || status=1
        else
            echo "[$(date '+%H:%M:%S')] 4/4 notification skipped"
        fi
    } >> "$TEMP_LOG" 2>&1
    return "$status"
}

# Normalize a marker left by a killed owner before starting discovery.
for abandoned in "$QUEUE_DIR"/running-*; do
    [ -d "$abandoned" ] || continue
    queue_pending
    rmdir "$abandoned" 2>/dev/null || true
done

if ! run_pass; then
    queue_pending
    exit 1
fi

# Claim then drain pending work while still holding the global lock.
while [ -d "$PENDING_MARKER" ]; do
    CLAIMED_MARKER="$QUEUE_DIR/running-$LOCK_TOKEN"
    if ! mv "$PENDING_MARKER" "$CLAIMED_MARKER" 2>/dev/null; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] PendingQueueClaimError" >> "$LOG_FILE"
        exit 1
    fi
    if ! run_pass; then
        queue_pending
        rmdir "$CLAIMED_MARKER" 2>/dev/null || true
        exit 1
    fi
    rmdir "$CLAIMED_MARKER" 2>/dev/null || true
done

if grep -Eq 'processed=[1-9]|[1-9]+/[0-9]+ (요약됨|전송됨)' "$TEMP_LOG"; then
    {
        echo ""
        echo "=========================================="
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] pipeline start"
        echo "=========================================="
        cat "$TEMP_LOG"
        echo "[$(date '+%H:%M:%S')] complete"
    } >> "$LOG_FILE"
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] no changes" >> "$LOG_FILE"
fi
