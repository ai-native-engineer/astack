"""공통 경로 설정."""

from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = PROJECT_DIR / "scripts"

DATA_DIR = Path.home() / ".voice-memos"
TRANSCRIPTS_DIR = DATA_DIR / "transcripts"
LOGS_DIR = Path.home() / ".voice-memos/logs"  # 로그는 로컬 — launchd가 iCloud 경로엔 못 씀(EX_CONFIG)
CORRECTIONS_FILE = DATA_DIR / "corrections.json"
VOCAB_FILE = Path.home() / ".config" / "stt" / "vocab.txt"
ENV_FILE = PROJECT_DIR / ".env"
WATCHER_LOG_FILE = LOGS_DIR / "watcher.log"
CALL_RECORDINGS_DIR = (
    Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/녹음"
)
RECORDINGS_DIR = (
    Path.home()
    / "Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings"
)
CALL_TRANSCRIPT_SUFFIX = ".transcript.md"
CALL_SUMMARY_SUFFIX = ".summary.md"

PROCESS_MARKERS = (
    "<!-- corrected -->",
    "<!-- summarized -->",
    "<!-- notified -->",
)


def ensure_runtime_dirs() -> None:
    """런타임 디렉터리를 생성합니다."""
    for path in (TRANSCRIPTS_DIR, LOGS_DIR):
        path.mkdir(parents=True, exist_ok=True)


def is_call_transcript(path: Path) -> bool:
    """에이닷 통화 녹음 폴더에 있는 파생 전사 파일인지 확인합니다."""
    return path.parent == CALL_RECORDINGS_DIR and path.name.endswith(CALL_TRANSCRIPT_SUFFIX)


def is_call_summary(path: Path) -> bool:
    """에이닷 통화 녹음 폴더에 있는 파생 요약 파일인지 확인합니다."""
    return path.parent == CALL_RECORDINGS_DIR and path.name.endswith(CALL_SUMMARY_SUFFIX)


def iter_transcript_files(base_dir: Path) -> list[Path]:
    """전사 파일을 반환합니다.

    Voice Memos는 `~/.voice-memos/transcripts/**/transcript.md`, 에이닷 통화
    녹음은 iCloud `녹음/*.transcript.md`를 사용합니다.
    """
    files = sorted(base_dir.rglob("transcript.md")) if base_dir.exists() else []
    if base_dir == TRANSCRIPTS_DIR and CALL_RECORDINGS_DIR.exists():
        files.extend(sorted(CALL_RECORDINGS_DIR.glob(f"*{CALL_TRANSCRIPT_SUFFIX}")))
    return sorted(files)


def summary_path_for(transcript_path: Path) -> Path:
    """전사 파일에 대응하는 요약 파일 경로를 반환합니다."""
    if is_call_transcript(transcript_path):
        stem = transcript_path.name[: -len(CALL_TRANSCRIPT_SUFFIX)]
        return transcript_path.with_name(f"{stem}{CALL_SUMMARY_SUFFIX}")
    return transcript_path.parent / "summary.md"


def transcript_path_for(summary_path: Path) -> Path:
    """요약 파일에 대응하는 전사 파일 경로를 반환합니다."""
    if is_call_summary(summary_path):
        stem = summary_path.name[: -len(CALL_SUMMARY_SUFFIX)]
        return summary_path.with_name(f"{stem}{CALL_TRANSCRIPT_SUFFIX}")
    return summary_path.parent / "transcript.md"


def strip_process_markers(content: str) -> str:
    """처리 마커를 제거한 본문만 반환합니다."""
    lines = []
    for line in content.splitlines():
        if line.strip() in PROCESS_MARKERS:
            continue
        lines.append(line)

    return "\n".join(lines).strip()
