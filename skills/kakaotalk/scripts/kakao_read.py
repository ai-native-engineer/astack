#!/usr/bin/env python3
"""
KakaoTalk 채팅방 읽기 CLI

Usage:
    # 기본: 채팅방 열고 메시지 읽기
    python kakao_read.py "채팅방이름"
    python kakao_read.py "채팅방이름" --limit 50
    python kakao_read.py "채팅방이름" --close

    # 채팅 목록
    python kakao_read.py --list

    # 검색어로 채팅방 검색
    python kakao_read.py --search "검색어"
"""

import argparse
import json
import re
import subprocess
import sys
import time

try:
    import atomacos
except ImportError:
    print("Error: atomacos not installed. Run: uv sync")
    sys.exit(1)

# Constants
KAKAO_BUNDLE_ID = "com.kakao.KakaoTalkMac"
CLAUDE_SIGNATURE = "sent with claude code"
FILE_EXTENSIONS = ['.heic', '.jpg', '.jpeg', '.png', '.gif', '.mp4', '.mov', '.pdf', '.zip']
IGNORED_KEYWORDS = ['유효기간', '용량', 'KB', 'MB']
TIME_PATTERNS = ['오전', '오후', '어제', '그제', '월', '일',
                 'AM', 'PM', 'Yesterday', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', ':']
MAIN_WINDOW_TITLES = ('카카오톡', 'KakaoTalk')


# ============================================================================
# AppleScript & Keyboard Helpers
# ============================================================================

def run_applescript(script: str) -> str:
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    return result.stdout.strip()


def key_code(code: int, modifiers: str = ""):
    modifier_clause = f"using {{{modifiers}}}" if modifiers else ""
    run_applescript(f'''
        tell application "System Events"
            tell process "KakaoTalk"
                key code {code} {modifier_clause}
            end tell
        end tell
    ''')


# ============================================================================
# KakaoTalk App & Window Management
# ============================================================================

def get_kakao_app():
    try:
        return atomacos.getAppRefByBundleId(KAKAO_BUNDLE_ID)
    except ValueError:
        print("Error: KakaoTalk is not running.")
        sys.exit(1)
    except atomacos.ErrorAPIDisabled:
        print("Error: Accessibility API disabled.")
        sys.exit(1)


def activate_kakaotalk(max_retries: int = 3):
    """카카오톡을 활성화하고 메인 창이 보일 때까지 대기. 앱 참조를 반환."""
    _dbg("activate: activate + reopen")
    run_applescript('''
        tell application "KakaoTalk"
            activate
            reopen
        end tell
    ''')
    for i in range(max_retries):
        time.sleep(0.3)
        kakao = get_kakao_app()
        if find_main_window(kakao):
            _dbg(f"activate: found main window (attempt {i+1})")
            return kakao
    _dbg("activate: main window NOT found after retries")
    return get_kakao_app()


def find_main_window(kakao_app):
    """메인 창(카카오톡 채팅 목록 창) 찾기."""
    for win in kakao_app.windows():
        if win.AXTitle in MAIN_WINDOW_TITLES:
            return win
    return None


def find_open_chat(kakao_app, chat_name: str):
    """이미 열린 채팅방 창에서 이름이 일치하는 것 찾기.
    부분 문자열 매치 + 키워드 전체 포함 매치를 모두 시도."""
    chat_lower = chat_name.lower()
    keywords = [k.strip().lower() for k in re.split(r'[\sxX×]+', chat_name) if k.strip()]

    for win in kakao_app.windows():
        title = win.AXTitle
        if title in MAIN_WINDOW_TITLES:
            continue
        title_lower = title.lower()
        # 부분 문자열 매치
        if chat_lower in title_lower:
            return win
        # 키워드 전체 포함 매치 (순서 무관)
        if keywords and all(kw in title_lower for kw in keywords):
            return win
    return None


def get_all_chat_windows(kakao_app) -> list:
    return [win for win in kakao_app.windows() if win.AXTitle not in MAIN_WINDOW_TITLES]


def ensure_main_window_focused():
    """메인 창(채팅 목록)이 확실히 포커스되도록 함."""
    kakao = activate_kakaotalk()
    main_win = find_main_window(kakao)
    if not main_win:
        return False

    try:
        main_win.Raise()
        time.sleep(0.3)
    except Exception:
        pass

    return True


_DEBUG = False


def _dbg(msg: str):
    """디버그 메시지를 stderr로 출력 (--debug 플래그 필요)."""
    if _DEBUG:
        print(f"[kakao] {msg}", file=sys.stderr, flush=True)


def go_to_chat_tab():
    """어떤 상태에서든 채팅 탭으로 이동."""
    _dbg("go_to_chat_tab: activate")
    activate_kakaotalk()

    _dbg("go_to_chat_tab: Cmd+2")
    key_code(19, "command down")  # Cmd+2 = 채팅 탭
    time.sleep(0.5)

    kakao = get_kakao_app()
    win = find_main_window(kakao)
    _dbg(f"go_to_chat_tab: main_win={'found' if win else 'NOT FOUND'}")
    return win


def open_search():
    """Cmd+F로 검색 모드 진입 후 기존 텍스트 초기화."""
    main_win = go_to_chat_tab()
    if not main_win:
        return None

    _dbg("open_search: Cmd+F")
    key_code(3, "command down")  # Cmd+F
    time.sleep(0.5)

    _dbg("open_search: Cmd+A (select all to clear)")
    key_code(0, "command down")  # Cmd+A
    time.sleep(0.1)

    return main_win


def _read_search_results(limit: int = 20) -> list[str]:
    """현재 검색 결과 목록을 읽어서 반환."""
    kakao = get_kakao_app()
    chats = []
    for win in kakao.windows():
        if safe_get_attr(win, 'AXTitle') not in MAIN_WINDOW_TITLES:
            continue
        for child in safe_get_attr(win, 'AXChildren', []):
            if safe_get_attr(child, 'AXRole') != 'AXScrollArea':
                continue
            for table_child in safe_get_attr(child, 'AXChildren', []):
                if safe_get_attr(table_child, 'AXRole') != 'AXTable':
                    continue
                rows = safe_get_attr(table_child, 'AXChildren', [])
                for row in rows[:limit]:
                    if safe_get_attr(row, 'AXRole') != 'AXRow':
                        continue
                    texts = _extract_row_texts(row)
                    if texts:
                        chats.append(texts[0])
                break
            break
    return chats


def search_and_open_chat(chat_name: str):
    """검색 후 일치하는 채팅방을 찾아서 열기."""
    open_search()

    _dbg(f"search_and_open_chat: typing '{chat_name}'")
    subprocess.run(["pbcopy"], input=chat_name.encode(), check=True)
    key_code(9, "command down")  # Cmd+V
    time.sleep(1.0)

    # 검색 결과 목록 읽기
    results = _read_search_results()
    _dbg(f"search_and_open_chat: results={results[:5]}")

    if not results:
        _dbg("search_and_open_chat: no results")
        return

    # 일치하는 항목의 인덱스 찾기
    target_idx = _find_matching_index(results, chat_name)
    _dbg(f"search_and_open_chat: target_idx={target_idx} ('{results[target_idx] if target_idx < len(results) else '?'}')")

    # Down arrow로 해당 위치까지 이동 후 Enter
    for _ in range(target_idx + 1):  # +1: 검색창에서 첫 결과로 이동하는 1회 포함
        key_code(125)  # Down arrow
        time.sleep(0.1)
    key_code(36)  # Enter
    time.sleep(0.8)


def _find_matching_index(results: list[str], chat_name: str) -> int:
    """검색 결과에서 가장 적합한 채팅방의 인덱스를 반환."""
    chat_lower = chat_name.lower()
    keywords = [k.strip().lower() for k in re.split(r'[\sxX×_\-]+', chat_name) if k.strip()]

    for i, name in enumerate(results):
        name_lower = name.lower()
        # 정확히 포함
        if chat_lower in name_lower:
            return i
        # 키워드 전체 포함 (순서 무관)
        if keywords and all(kw in name_lower for kw in keywords):
            return i

    # 키워드 하나라도 포함하는 첫 번째
    for i, name in enumerate(results):
        name_lower = name.lower()
        meaningful = [kw for kw in keywords if len(kw) >= 2]
        if meaningful and any(kw in name_lower for kw in meaningful):
            return i

    # 못 찾으면 첫 번째
    return 0


def close_chat():
    """현재 채팅창 닫기."""
    key_code(53)  # Escape
    time.sleep(0.2)


# ============================================================================
# Pattern Matching Helpers
# ============================================================================

def is_date_pattern(val: str) -> bool:
    """날짜 구분선 패턴인지 확인 (예: '1월 17일', '2025. 1. 17.', '어제', '그제')"""
    if not val:
        return False
    if re.match(r'^\d{1,2}월\s*\d{1,2}일', val):
        return True
    if re.match(r'^\d{4}\.\s*\d{1,2}\.\s*\d{1,2}', val):
        return True
    if val in ['어제', '그제']:
        return True
    return False


def is_time_pattern(val: str) -> bool:
    """시간 패턴인지 확인 (예: '오전 10:30', '오후 7:41')"""
    if not val:
        return False
    return bool(re.match(r'^(오전|오후)\s*\d{1,2}:\d{2}$', val))


def is_valid_sender_name(val: str) -> bool:
    """유효한 발신자 이름인지 확인."""
    if not val or len(val) >= 20:
        return False
    if val.startswith('[') or val.isdigit():
        return False

    # 특수문자/공백만 있는 경우 무시
    cleaned = val.strip().replace('·', '').replace('•', '').replace(' ', '')
    if not cleaned:
        return False

    # 파일명 패턴 무시
    if any(val.lower().endswith(ext) for ext in FILE_EXTENSIONS):
        return False

    # 무시할 키워드 포함 시 무시
    if any(kw in val for kw in IGNORED_KEYWORDS):
        return False

    return True


# ============================================================================
# Accessibility Helpers
# ============================================================================

def safe_get_attr(elem, attr_name, default=None):
    """안전하게 AX 속성 가져오기."""
    try:
        return getattr(elem, attr_name, default)
    except AttributeError:
        return default


def get_window_width(chat_window) -> int:
    """창 너비 가져오기."""
    try:
        win_size = chat_window.AXSize
        return win_size.width if win_size else 400
    except Exception:
        return 400


# ============================================================================
# Message Extraction
# ============================================================================

def _find_scroll_area_and_table(chat_window):
    """채팅 창에서 ScrollArea와 Table 요소를 찾아 반환."""
    children = safe_get_attr(chat_window, 'AXChildren', [])
    for child in children:
        if safe_get_attr(child, 'AXRole') != 'AXScrollArea':
            continue
        for table_child in safe_get_attr(child, 'AXChildren', []):
            if safe_get_attr(table_child, 'AXRole') == 'AXTable':
                return child, table_child
    return None, None


def _extract_visible_messages(chat_window, table, limit: int = 100) -> list[dict]:
    """현재 보이는 메시지들을 추출."""
    messages = []
    chat_name = safe_get_attr(chat_window, 'AXTitle', '')
    partner_name = None
    current_date = None
    current_time = None
    win_width = get_window_width(chat_window)
    rows = safe_get_attr(table, 'AXChildren', [])

    for row in rows[:limit]:
        if safe_get_attr(row, 'AXRole') != 'AXRow':
            continue

        row_sender = None
        row_time = None

        for cell in safe_get_attr(row, 'AXChildren', []):
            if safe_get_attr(cell, 'AXRole') != 'AXCell':
                continue

            cell_pos = None
            try:
                cell_pos = cell.AXPosition
            except Exception:
                pass

            for elem in safe_get_attr(cell, 'AXChildren', []):
                role = safe_get_attr(elem, 'AXRole')

                if role == 'AXStaticText':
                    row_sender, row_time, current_date, partner_name = _parse_static_text(
                        elem, row_sender, row_time, current_date, partner_name
                    )

                elif role == 'AXTextArea':
                    msg_data = _parse_message(
                        elem, cell_pos, win_width, row_sender, row_time,
                        current_date, current_time, partner_name, chat_name
                    )
                    if msg_data:
                        messages.append(msg_data)
                        if row_time:
                            current_time = row_time

    return messages


def _msg_key(msg: dict) -> str:
    """메시지 중복 판별용 키 생성."""
    return f"{msg['sender']}|{msg['time']}|{msg['message'][:80]}"


def _focus_message_area(scroll_area) -> None:
    """메시지 영역(스크롤 영역/내부 테이블)에 접근성 키보드 포커스를 준다.

    좌표 클릭은 사용자의 실제 커서를 빼앗으므로 쓰지 않는다. 포커스를 주면
    가상화된 메시지 행 렌더링이 유도돼, 앱이 비활성이어도 빈 읽기를 줄인다.
    """
    try:
        scroll_area.AXFocused = True
        return
    except Exception:
        pass
    try:
        for child in safe_get_attr(scroll_area, 'AXChildren', []) or []:
            if safe_get_attr(child, 'AXRole') in ('AXTable', 'AXList', 'AXOutline'):
                child.AXFocused = True
                return
    except Exception:
        pass


def _scroll_to_top(chat_window):
    """채팅 최상단으로 스크롤 (마우스 없이: 접근성 포커스 + Page Up)."""
    _dbg("_scroll_to_top: AX focus message area + Page Up")
    _focus_message_area(chat_window)
    time.sleep(0.3)

    # Fn+Up (Page Up) 반복으로 최상단 이동
    _dbg("_scroll_to_top: Page Up x20")
    run_applescript('''
        tell application "System Events"
            tell process "KakaoTalk"
                repeat 20 times
                    key code 116
                    delay 0.2
                end repeat
            end tell
        end tell
    ''')  # key code 116 = Page Up
    time.sleep(0.5)


def extract_messages(chat_window, limit: int = 100) -> list[dict]:
    """채팅 창에서 현재 보이는 메시지 추출.

    빈 결과는 보통 메시지 영역이 아직 렌더링되지 않은 것(앱 비활성/뷰포트 미정)이다.
    마우스 없이 접근성 포커스를 줘 행 렌더링을 유도한 뒤 한 번 더 시도한다.
    """
    scroll_area, table = _find_scroll_area_and_table(chat_window)
    if not table:
        return []
    messages = _extract_visible_messages(chat_window, table, limit)
    if not messages:
        _dbg("extract_messages: empty result, AX focus + retry once")
        _focus_message_area(scroll_area)
        time.sleep(0.4)
        scroll_area, table = _find_scroll_area_and_table(chat_window)
        if table:
            messages = _extract_visible_messages(chat_window, table, limit)
    return messages


def extract_all_messages(chat_window, max_scrolls: int = 50) -> list[dict]:
    """스크롤하면서 전체 대화 내역 추출.

    1. 최상단으로 이동
    2. 아래로 스크롤하면서 메시지 수집
    3. 중복 제거 후 반환
    """
    scroll_area, table = _find_scroll_area_and_table(chat_window)
    if not table:
        return []

    # 최상단으로 스크롤
    _scroll_to_top(scroll_area)
    time.sleep(0.5)

    all_messages = []
    seen_keys = set()
    no_new_count = 0

    for i in range(max_scrolls):
        visible = _extract_visible_messages(chat_window, table, limit=200)

        new_count = 0
        for msg in visible:
            key = _msg_key(msg)
            if key not in seen_keys:
                seen_keys.add(key)
                all_messages.append(msg)
                new_count += 1

        _dbg(f"extract_all: scroll {i+1}, new={new_count}, total={len(all_messages)}")

        if new_count == 0:
            no_new_count += 1
            if no_new_count >= 3:
                _dbg(f"extract_all: done (no new messages 3 times)")
                break
        else:
            no_new_count = 0

        # 아래로 스크롤 (Page Down)
        run_applescript('''
            tell application "System Events"
                tell process "KakaoTalk"
                    key code 121
                    delay 0.3
                end tell
            end tell
        ''')  # key code 121 = Page Down
        time.sleep(0.3)

    return all_messages


def _parse_static_text(elem, row_sender, row_time, current_date, partner_name):
    """StaticText 요소 파싱."""
    try:
        val = elem.AXValue
        if not val:
            return row_sender, row_time, current_date, partner_name

        # 줄바꿈으로 값이 합쳐진 경우
        if '\n' in val:
            for part in val.split('\n'):
                part = part.strip()
                if part.isdigit():
                    continue
                if is_date_pattern(part):
                    current_date = part.split()[0] if '요일' in part else part
                elif is_time_pattern(part):
                    row_time = part
        elif is_date_pattern(val):
            current_date = val.split()[0] if '요일' in val else val
        elif is_time_pattern(val):
            row_time = val
        elif is_valid_sender_name(val):
            row_sender = val
            partner_name = val
    except Exception:
        pass

    return row_sender, row_time, current_date, partner_name


def _parse_message(elem, cell_pos, win_width, row_sender, row_time,
                   current_date, current_time, partner_name, chat_name) -> dict | None:
    """TextArea 요소에서 메시지 파싱."""
    try:
        msg = elem.AXValue
        if not msg or not msg.strip():
            return None

        # is_me 판단 1: Claude Code 시그니처
        is_me = CLAUDE_SIGNATURE in msg

        # is_me 판단 2: 좌표 기반
        if not is_me and cell_pos:
            try:
                elem_pos = elem.AXPosition
                center_threshold = cell_pos.x + (win_width * 0.4)
                is_me = elem_pos.x > center_threshold
            except Exception:
                pass

        # 발신자 결정
        if is_me:
            sender = "나"
        elif row_sender:
            sender = row_sender
        else:
            sender = partner_name or chat_name or "상대방"

        # 시간 문자열 생성
        time_val = row_time or current_time
        if current_date and time_val:
            time_str = f"{current_date} {time_val}"
        else:
            time_str = time_val or current_date

        return {
            'sender': sender,
            'time': time_str,
            'message': msg,
            'is_me': is_me
        }
    except Exception:
        return None


# ============================================================================
# Chat List Operations
# ============================================================================

def list_chats(kakao_app=None, limit: int = 30) -> list[str]:
    """메인 창에서 채팅방 목록 추출. 먼저 채팅 탭으로 이동."""
    main_win = go_to_chat_tab()
    if not main_win:
        return []

    chats = []
    for child in safe_get_attr(main_win, 'AXChildren', []):
        if safe_get_attr(child, 'AXRole') != 'AXScrollArea':
            continue

        for table_child in safe_get_attr(child, 'AXChildren', []):
            if safe_get_attr(table_child, 'AXRole') != 'AXTable':
                continue

            rows = safe_get_attr(table_child, 'AXChildren', [])
            for row in rows[:limit]:
                if safe_get_attr(row, 'AXRole') != 'AXRow':
                    continue

                texts = _extract_row_texts(row)
                if len(texts) >= 2 and any(t in texts[1] for t in TIME_PATTERNS):
                    chats.append(texts[0])
            break
        break

    return chats


def search_chats(query: str, limit: int = 20) -> list[str]:
    """카카오톡 검색창에서 검색 후 결과 목록 반환."""
    _dbg(f"search_chats: query='{query}'")
    open_search()

    _dbg("search_chats: pasting query")
    subprocess.run(["pbcopy"], input=query.encode(), check=True)
    key_code(9, "command down")  # Cmd+V
    time.sleep(1.0)

    chats = _read_search_results(limit)
    _dbg(f"search_chats: found {len(chats)} results")

    # ESC로 검색 닫기
    key_code(53)
    time.sleep(0.2)

    return chats


def _extract_row_texts(row) -> list[str]:
    """Row에서 모든 StaticText 값 추출."""
    texts = []
    for cell in safe_get_attr(row, 'AXChildren', []):
        if safe_get_attr(cell, 'AXRole') != 'AXCell':
            continue
        for elem in safe_get_attr(cell, 'AXChildren', []):
            if safe_get_attr(elem, 'AXRole') == 'AXStaticText':
                try:
                    val = elem.AXValue
                    if val:
                        texts.append(val)
                except Exception:
                    pass
    return texts


# ============================================================================
# Main API
# ============================================================================

def _matches_chat_name(window_title: str, chat_name: str) -> bool:
    """열린 창 제목이 요청한 채팅방과 일치하는지 검증."""
    title_lower = window_title.lower()
    chat_lower = chat_name.lower()

    # 부분 문자열 매치
    if chat_lower in title_lower:
        return True

    # 키워드 전체 포함 매치 (순서 무관, 구분자: 공백/x/X/×/_/-)
    keywords = [k.strip().lower() for k in re.split(r'[\sxX×_\-]+', chat_name) if k.strip()]
    if keywords and all(kw in title_lower for kw in keywords):
        return True

    # 키워드 중 하나라도 포함 (최소 2글자 키워드만)
    meaningful_keywords = [kw for kw in keywords if len(kw) >= 2]
    if meaningful_keywords and any(kw in title_lower for kw in meaningful_keywords):
        return True

    return False


def _open_chat_window(chat_name: str, search_term: str):
    """검색어로 채팅방을 열고 검증된 창을 반환.
    열린 창이 요청한 채팅방과 일치하지 않으면 닫고 None 반환."""
    kakao = activate_kakaotalk()

    before_titles = set(win.AXTitle for win in get_all_chat_windows(kakao))
    search_and_open_chat(search_term)
    kakao = get_kakao_app()

    after_windows = get_all_chat_windows(kakao)
    new_windows = [win for win in after_windows if win.AXTitle not in before_titles]

    # 새로 열린 창 검증
    if new_windows:
        win = new_windows[0]
        if _matches_chat_name(win.AXTitle, chat_name):
            return win
        # 일치하지 않으면 닫기
        close_chat()
        time.sleep(0.3)
        return None

    # 이미 열린 창에서 키워드 매치 시도
    if (chat_win := find_open_chat(kakao, chat_name)):
        return chat_win

    return None


def _find_chat_window(chat_name: str):
    """채팅방 창 찾기."""
    kakao = activate_kakaotalk()

    # 1차: 이미 열린 창에서 찾기
    chat_win = find_open_chat(kakao, chat_name)
    if chat_win:
        _dbg(f"_find_chat_window: found open chat '{chat_win.AXTitle}'")
        return chat_win

    # 2차: 검색으로 열기
    chat_win = _open_chat_window(chat_name, chat_name)
    if chat_win:
        _dbg(f"_find_chat_window: opened '{chat_win.AXTitle}'")
        return chat_win

    _dbg(f"_find_chat_window: not found '{chat_name}'")
    return None


def read_chat(chat_name: str, limit: int = 100, read_all: bool = False) -> tuple[str | None, list[dict]]:
    """채팅방 열고 메시지 읽기."""
    # 키보드 기반 검색/열기는 카카오톡이 앞에 있어야 한다. 사용자가 컴퓨터를
    # 쓰는 중이면 포커스를 뺏겨 한 번에 안 열릴 수 있으니 몇 번 재시도한다.
    chat_win = None
    for attempt in range(3):
        chat_win = _find_chat_window(chat_name)
        if chat_win:
            break
        _dbg(f"read_chat: open attempt {attempt + 1} failed, retrying")
        time.sleep(0.6)
    if not chat_win:
        return None, []

    if read_all:
        messages = extract_all_messages(chat_win)
    else:
        messages = extract_messages(chat_win, limit)

    return chat_win.AXTitle, messages


# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description='KakaoTalk 채팅방 읽기 CLI')
    parser.add_argument('chat_name', nargs='?', help='채팅방 이름 (부분 일치)')
    parser.add_argument('--limit', '-l', type=int, default=100, help='최대 메시지 수 (기본: 100)')
    parser.add_argument('--all', '-a', action='store_true', help='스크롤하여 전체 대화 읽기')
    parser.add_argument('--list', action='store_true', help='채팅방 목록 보기')
    parser.add_argument('--search', '-s', type=str, help='카카오톡 검색창에서 검색 후 결과 목록')
    parser.add_argument('--close', '-c', action='store_true', help='읽고 나서 창 닫기')
    parser.add_argument('--json', '-j', action='store_true', help='JSON 출력')
    parser.add_argument('--debug', '-d', action='store_true', help='디버그 로그 출력 (stderr)')

    args = parser.parse_args()

    if args.debug:
        global _DEBUG
        _DEBUG = True

    # 모드 1: 카카오톡 검색창에서 검색
    if args.search:
        chats = search_chats(args.search)
        if args.json:
            print(json.dumps({'search': args.search, 'chats': chats}, ensure_ascii=False, indent=2))
        else:
            print(f"=== '{args.search}' 검색 결과 ===\n")
            for c in chats:
                print(f"  • {c}")
            print(f"\n총 {len(chats)}개")
        return

    # 모드 2: 전체 채팅방 목록
    if args.list:
        chats = list_chats()
        if args.json:
            print(json.dumps({'chats': chats}, ensure_ascii=False, indent=2))
        else:
            print("=== 채팅방 목록 ===\n")
            for c in chats:
                print(f"  • {c}")
            print(f"\n총 {len(chats)}개")
        return

    # 모드 3: 기본 - 채팅방 열고 메시지 읽기
    if not args.chat_name:
        parser.print_help()
        return

    chat_name, messages = read_chat(args.chat_name, args.limit, read_all=args.all)

    if not messages:
        if args.json:
            print(json.dumps({
                'error': f"'{args.chat_name}' 채팅방을 찾을 수 없습니다.",
                'chat': None,
                'messages': []
            }, ensure_ascii=False, indent=2))
        else:
            print(f"'{args.chat_name}' 채팅방을 찾을 수 없거나 메시지가 없습니다.")
        return

    if args.json:
        print(json.dumps({'chat': chat_name, 'messages': messages}, ensure_ascii=False, indent=2))
    else:
        print(f"\n=== {chat_name} ({len(messages)}개) ===\n")
        for m in messages:
            sender = m['sender']
            time_str = m['time'] or ''
            msg = m['message'].replace('\n', ' ')
            if len(msg) > 80:
                msg = msg[:80] + '...'
            print(f"[{time_str}] {sender}: {msg}")

    if args.close:
        close_chat()
        if not args.json:
            print("\n[창 닫힘]")


if __name__ == '__main__':
    main()
