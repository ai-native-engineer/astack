#!/usr/bin/env python3
"""
Claude Code SDK를 사용하여 음성 메모 전사본의 요약을 생성합니다.

전사된 마크다운 파일을 읽어 Claude(claude-sonnet-4-6[1m])로 요약을 생성하고,
같은 디렉터리의 summary.md에 저장합니다.
"""

import sys
from datetime import datetime
from pathlib import Path

import anyio
from claude_agent_sdk import AssistantMessage, ClaudeAgentOptions, TextBlock, query

from config import (
    TRANSCRIPTS_DIR,
    VOCAB_FILE,
    ensure_runtime_dirs,
    iter_transcript_files,
    summary_path_for,
)

SYSTEM_PROMPT = """\
당신은 한국어 음성 메모 전사본을 교정하고 요약하는 전문가입니다.

아래 단계를 순서대로 수행하세요. 각 단계의 결과만 최종 출력에 포함하세요.

## 1단계: 전사본 분석

전사본을 처음부터 끝까지 읽고, 다음을 내부적으로 파악하세요 (출력하지 않음):
- 이 전사본의 유형 (독백/메모, 1:1 대화, 다자 회의)
- 전체 맥락과 주제
- 화자가 여러 명으로 추정되면 발화 전환 지점

## 2단계: 전사 오류 교정

음성 인식(ASR) 오류를 교정하세요:
- 인명, 지명, 전문 용어, 외래어가 잘못 전사된 경우
- 동음이의어 혼동 (예: "방역점" → "방향점", "커리큘러" → "커리큘럼", "엔시아드" → "INSEAD")
- 문맥상 의미가 통하지 않는 단어

교정 규칙:
- 확신이 높은 경우만 교정하세요. 애매하면 원문을 유지하세요.
- 고유명사(인명, 회사명, 제품명)는 고유명사 사전과 문맥을 근거로 교정하세요. 확신이 없으면 원문을 유지하세요.
- 필러(음, 어, 그, 뭐랄까 등), 반복, 미완성 발화는 교정 대상이 아닙니다 — 요약 단계에서 자연스럽게 제거됩니다.

## 3단계: 요약 생성

교정된 내용을 기반으로 요약을 생성하세요.

---

출력 형식 (마크다운):

## 제목
(전사본의 핵심 주제를 담은 20자 내외의 한국어 명사구 제목 한 줄. 날짜·따옴표·마침표 없이. 예: "비즈니스피치 교육과 대모산개발단 방향성 회고")

## 교정 사항
| 원문 | 교정 | 근거 |
|------|------|------|
| 잘못된 단어 | 올바른 단어 | 교정 이유 |

## 요약

### 핵심 내용
- (전사본 전체를 3-5개 문장으로 압축)

### 주요 논의 사항
- (주제별로 구조화하여 정리. 각 주제에 대해 맥락과 세부 내용을 포함)

### 결정 사항
- (구체적으로 무엇이 결정되었는지. 누가, 왜 결정했는지 포함)

### 액션 아이템
- [ ] (할 일) — 담당자 (기한이 언급된 경우 포함)

---

규칙:
- 제목은 반드시 첫 줄에 `## 제목` 섹션으로 출력하세요.
- 전사본에 없는 내용을 추가하지 마세요 (hallucination 금지).
- 구어체를 깔끔한 문어체로 변환하되, 원래 의미와 뉘앙스를 보존하세요.
- 불필요한 반복, 필러, 더듬음은 자연스럽게 제거하세요.
- 위의 마크다운 형식만 출력하세요. 인사말, 부연 설명 등은 붙이지 마세요.
- 해당 내용이 없는 섹션은 생략하세요.
"""

def load_vocab() -> list[str]:
    """~/.config/stt/vocab.txt 에서 고유명사 목록을 로드합니다."""
    if not VOCAB_FILE.exists():
        return []
    lines = VOCAB_FILE.read_text(encoding="utf-8").splitlines()
    return [l.strip() for l in lines if l.strip() and not l.startswith("#")]


SUMMARIZED_MARKER = "<!-- summarized -->"
NOTIFIED_MARKER = "<!-- notified -->"


def parse_title(summary: str) -> str:
    """요약 결과의 `## 제목` 섹션에서 제목 한 줄을 추출합니다."""
    lines = summary.splitlines()
    for i, line in enumerate(lines):
        if line.strip() == "## 제목":
            for next_line in lines[i + 1 :]:
                text = next_line.strip()
                if not text:
                    continue
                if text.startswith("#"):
                    break
                # 따옴표/마침표 등 군더더기 제거
                return text.strip(" \"'`.").strip()
            break
    return ""


def apply_title_to_transcript(filepath: Path, title: str) -> bool:
    """transcript.md의 H1 헤딩을 제목으로 바꾸고 frontmatter에 제목을 주입합니다.

    멱등: 이미 `- **제목**:` 이 있으면 갱신, 없으면 추가.
    """
    if not title:
        return False
    content = filepath.read_text(encoding="utf-8")
    lines = content.splitlines()

    # 1) H1 헤딩(`# ...`)을 제목으로 교체
    for i, line in enumerate(lines):
        if line.startswith("# "):
            lines[i] = f"# {title}"
            break

    # 2) frontmatter 제목 줄 갱신 또는 추가 (녹음일시 줄 위)
    title_line = f"- **제목**: {title}"
    has_title = False
    for i, line in enumerate(lines):
        if line.startswith("- **제목**:"):
            lines[i] = title_line
            has_title = True
            break
    if not has_title:
        for i, line in enumerate(lines):
            if line.startswith("- **녹음일시**:"):
                lines.insert(i, title_line)
                break

    new_content = "\n".join(lines)
    if not new_content.endswith("\n"):
        new_content += "\n"
    filepath.write_text(new_content, encoding="utf-8")
    return True


def parse_corrections(summary: str) -> list[tuple[str, str]]:
    """요약 결과에서 교정 테이블을 파싱합니다. [(원문, 교정)] 리스트 반환."""
    corrections = []
    in_table = False
    for line in summary.splitlines():
        if "| 원문 |" in line or "|---" in line:
            in_table = True
            continue
        if in_table:
            if not line.strip().startswith("|"):
                break
            cols = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cols) >= 2 and cols[0] and cols[1]:
                corrections.append((cols[0], cols[1]))
    return corrections


def apply_corrections_to_transcript(filepath: Path, corrections: list[tuple[str, str]]) -> int:
    """교정 사항을 transcript.md에 적용합니다. 적용 건수 반환."""
    content = filepath.read_text(encoding="utf-8")
    applied = 0
    for original, corrected in corrections:
        if original in content:
            content = content.replace(original, corrected)
            applied += 1
    if applied > 0:
        filepath.write_text(content, encoding="utf-8")
    return applied


def has_summary(filepath: Path) -> bool:
    """전사 파일에 대응하는 요약 파일이 이미 있는지 확인합니다."""
    return summary_path_for(filepath).exists()


def extract_transcript(filepath: Path) -> str:
    """마크다운 파일에서 전사 내용만 추출합니다."""
    content = filepath.read_text(encoding="utf-8")
    marker = "## 전사 내용"
    idx = content.find(marker)
    if idx == -1:
        return content
    return content[idx + len(marker) :].strip()


def build_summary_content(summary: str, preserve_notified: bool) -> str:
    """요약 파일 내용을 구성합니다."""
    markers = [SUMMARIZED_MARKER]
    if preserve_notified:
        markers.append(NOTIFIED_MARKER)

    return summary.strip().rstrip() + "\n\n" + "\n".join(markers) + "\n"


async def summarize_file(filepath: Path, force: bool = False) -> bool:
    """단일 전사 파일을 요약합니다."""
    filepath = filepath.expanduser()
    if not filepath.exists():
        print(f"File not found: {filepath}", file=sys.stderr)
        return False

    summary_path = summary_path_for(filepath)
    if summary_path.exists() and not force:
        return False

    transcript = extract_transcript(filepath)
    if not transcript or len(transcript) < 200:
        return False

    options = ClaudeAgentOptions(
        system_prompt=SYSTEM_PROMPT,
        model="claude-sonnet-4-6[1m]",
        max_turns=3,
    )

    # 디렉터리 경로에서 날짜/시간 추출
    try:
        time_part = filepath.parent.name
        date_part = filepath.parent.parent.name
        dt = datetime.strptime(f"{date_part} {time_part}", "%Y%m%d %H%M%S")
        date_str = dt.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        date_str = "알 수 없음"

    vocab = load_vocab()
    vocab_section = ""
    if vocab:
        vocab_section = f"\n## 고유명사 사전 (전사 교정 시 우선 참고)\n{', '.join(vocab)}\n"

    prompt = f"""\
다음 음성 메모 전사본을 교정하고 요약해주세요.

- 녹음일시: {date_str}
{vocab_section}
## 전사본

{transcript}"""

    summary_parts: list[str] = []
    async for message in query(
        prompt=prompt,
        options=options,
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    summary_parts.append(block.text)

    summary = "\n".join(summary_parts).strip()
    if not summary:
        raise RuntimeError("SDK가 빈 응답을 반환 (claude CLI 인증 또는 API 장애 가능)")

    preserve_notified = False
    if summary_path.exists():
        preserve_notified = NOTIFIED_MARKER in summary_path.read_text(encoding="utf-8")

    ensure_runtime_dirs()
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(
        build_summary_content(summary, preserve_notified=preserve_notified),
        encoding="utf-8",
    )

    # LLM이 생성한 제목을 transcript.md에 주입
    title = parse_title(summary)
    if title and apply_title_to_transcript(filepath, title):
        print(f"    ↳ 제목: {title}")

    # LLM이 발견한 교정 사항을 transcript.md에 적용
    corrections = parse_corrections(summary)
    if corrections:
        applied = apply_corrections_to_transcript(filepath, corrections)
        if applied > 0:
            print(f"    ↳ 전사 {applied}건 교정")

    try:
        relative_path = summary_path.relative_to(TRANSCRIPTS_DIR)
    except ValueError:
        relative_path = summary_path

    print(f"  {filepath.name} → {relative_path}")
    return True


async def async_main():
    import argparse

    parser = argparse.ArgumentParser(description="음성 메모 전사본 요약 생성")
    parser.add_argument("--file", type=str, help="특정 마크다운 파일만 요약")
    parser.add_argument("--force", action="store_true", help="이미 요약된 파일도 재생성")
    parser.add_argument("--all", action="store_true", help="모든 전사 파일 요약")
    parser.add_argument("--recent", type=int, default=0, help="최근 N개 파일만 요약")
    args = parser.parse_args()

    if args.file:
        await summarize_file(Path(args.file).expanduser(), force=args.force)
        return

    files = sorted(iter_transcript_files(TRANSCRIPTS_DIR), reverse=True)
    if args.recent:
        files = files[: args.recent]

    processed = 0
    errors = 0
    error_details: list[str] = []
    for file in files:
        if not args.all and not args.recent and has_summary(file) and not args.force:
            continue
        try:
            if await summarize_file(file, force=args.force):
                processed += 1
        except Exception as exc:
            errors += 1
            error_details.append(f"{file.name}: {exc}")
            print(f"  [ERROR] {file.name}: {exc}", file=sys.stderr)

    print(f"  {processed}/{len(files)} 요약됨")

    if errors > 0:
        print(f"  [ERROR] 요약 실패 {errors}건", file=sys.stderr)
        for detail in error_details[:5]:
            print(f"    - {detail}", file=sys.stderr)
        sys.exit(1)


def main():
    anyio.run(async_main)


if __name__ == "__main__":
    main()
