"""공통 경로 설정."""

from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = PROJECT_DIR / "scripts"

DATA_DIR = Path.home() / ".voice-memos"
TRANSCRIPTS_DIR = DATA_DIR / "transcripts"
LOGS_DIR = DATA_DIR / "logs"
CORRECTIONS_FILE = DATA_DIR / "corrections.json"
VOCAB_FILE = Path.home() / ".config" / "stt" / "vocab.txt"
ENV_FILE = PROJECT_DIR / ".env"
WATCHER_LOG_FILE = LOGS_DIR / "watcher.log"
RECORDINGS_DIR = (
    Path.home()
    / "Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings"
)

PROCESS_MARKERS = (
    "<!-- corrected -->",
    "<!-- summarized -->",
    "<!-- notified -->",
)


def ensure_runtime_dirs() -> None:
    """런타임 디렉터리를 생성합니다."""
    for path in (TRANSCRIPTS_DIR, LOGS_DIR):
        path.mkdir(parents=True, exist_ok=True)


def iter_transcript_files(base_dir: Path) -> list[Path]:
    """디렉터리 아래의 모든 transcript.md 파일을 재귀적으로 반환합니다."""
    if not base_dir.exists():
        return []

    return sorted(base_dir.rglob("transcript.md"))


def summary_path_for(transcript_path: Path) -> Path:
    """전사 파일에 대응하는 요약 파일 경로를 반환합니다 (같은 디렉터리의 summary.md)."""
    return transcript_path.parent / "summary.md"


def transcript_path_for(summary_path: Path) -> Path:
    """요약 파일에 대응하는 전사 파일 경로를 반환합니다 (같은 디렉터리의 transcript.md)."""
    return summary_path.parent / "transcript.md"


def strip_process_markers(content: str) -> str:
    """처리 마커를 제거한 본문만 반환합니다."""
    lines = []
    for line in content.splitlines():
        if line.strip() in PROCESS_MARKERS:
            continue
        lines.append(line)

    return "\n".join(lines).strip()
