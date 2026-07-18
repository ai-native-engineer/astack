"""미러 academy 영상 레슨을 [썸네일 링크 + 접이식 자막(<details>)] 형태로 렌더.

academy-video.py(anthropic)·academy-extract.py(openai)는 영상 레슨을 [숨은 마커 + 인라인 전사]로 저장한다.
숨은 HTML 주석은 GitHub에서 안 보이고, 펼친 전사는 페이지가 한없이 길어진다 -> 마커 아래에
보이는 임베드(YouTube=공식 썸네일 링크, Vimeo=watch 링크, jwplayer=JW 썸네일+레슨 링크,
jwplayer-srt=링크 없음) + 전사를 접이식 <details>로 감싼다. Track-A 블로그 youtube는
inline-transcripts.py가 따로 처리하므로 여기선 academy 마커만 본다.

발행 형태(youtube 예):
    <!-- youtube: ID -->
    [![{title}](https://img.youtube.com/vi/ID/hqdefault.jpg)](https://www.youtube.com/watch?v=ID)

    <details>
    <summary>자막: {title}</summary>

    {전사}

    </details>

[실행하라] python3 render-video-refs.py <out_dir>
멱등: 이미 <summary>자막 가 있으면 건너뛴다. 옛 포맷(## 자막 (영상 전사) / [![Watch on YouTube] / vid-ref)도
이 스크립트가 새 포맷으로 마이그레이션한다(전사 본문은 그대로 보존). academy 레슨은 영상 1개·전사가 항상 마지막.
"""
import re, os, glob, sys

# academy 마커(레슨당 1개). youtube=11자 ID, vimeo=숫자 ID, jwplayer=JW media ID(썸네일 O, 재생은 source URL),
# jwplayer-srt=수동자막 코스(공개 watch URL 없음). jwplayer-srt를 jwplayer보다 먼저 둬 정확히 매칭.
MARKER = re.compile(r"<!--\s*(youtube|vimeo|jwplayer-srt|jwplayer):\s*([^\s|>]+)")
SOURCE = re.compile(r"<!--\s*(https?://\S+?)\s*-->")
# 전사 영역 위에 남아있을 수 있는 옛 렌더 아티팩트(마이그레이션 시 제거 후 재생성)
ARTIFACT = re.compile(r"^(<!--\s*vid-ref:|\[!\[Watch on YouTube\]|\[▶ Watch on Vimeo\]|\[!\[.*\]\(https://img\.youtube\.com|## 자막 \(영상 전사\)\s*$)")
ACRONYMS = {"ai", "api", "mcp", "llm", "sdk", "ui", "ux", "ide", "cli", "gpt", "rag", "it"}


def title_from_filename(fp):
    base = re.sub(r"^\d+-", "", os.path.splitext(os.path.basename(fp))[0])
    return " ".join(w.upper() if w in ACRONYMS else w.capitalize() for w in base.split("-")).strip()


def embed_line(kind, vid, title, source_url=""):
    if kind == "youtube":
        return f"[![{title}](https://img.youtube.com/vi/{vid}/hqdefault.jpg)](https://www.youtube.com/watch?v={vid})"
    if kind == "vimeo":
        return f"[▶ Watch on Vimeo](https://vimeo.com/{vid})"
    if kind == "jwplayer":  # JW 썸네일 임베드, 재생은 source(레슨) URL이 있으면 링크로
        thumb = f"https://cdn.jwplayer.com/thumbs/{vid}.jpg"
        return f"[![{title}]({thumb})]({source_url})" if source_url else f"![{title}]({thumb})"
    return ""  # jwplayer-srt: 공개 watch URL 없음


def process(fp):
    txt = open(fp, encoding="utf-8", errors="ignore").read()
    lines = txt.split("\n")
    mi = next((i for i, l in enumerate(lines) if MARKER.search(l)), None)
    if mi is None:
        return 0
    if any("<summary>자막" in l for l in lines[mi + 1:]):
        return 0  # 이미 새 포맷(멱등)
    m = MARKER.search(lines[mi])
    kind, vid = m.group(1), m.group(2)
    src_m = SOURCE.search(txt)  # jwplayer 재생 링크용 레슨 URL(파일 첫 source 주석)
    source_url = src_m.group(1) if src_m else ""
    before, tail = lines[:mi + 1], lines[mi + 1:]

    # tail 앞부분: 빈 줄·옛 아티팩트 제거, 마커 뒤 "# 제목" 헤딩이 있으면 보존(페이지 제목)
    title_after, j = None, 0
    while j < len(tail):
        if tail[j].strip() == "" or ARTIFACT.match(tail[j]):
            j += 1; continue
        if tail[j].startswith("# ") and title_after is None:
            title_after = tail[j][2:].strip(); j += 1; continue
        break
    transcript = "\n".join(tail[j:]).strip()
    if len(transcript) < 30:
        return 0  # 전사 없음 -> 손대지 않음

    # summary/alt 제목: 마커 뒤 헤딩 > 마커 앞 가장 가까운 # 헤딩 > 파일명
    title = title_after
    if not title:
        title = next((l[2:].strip() for l in reversed(before) if l.startswith("# ")), None)
    if not title:
        title = title_from_filename(fp)

    block = []
    if title_after:
        block += [f"# {title_after}", ""]
    emb = embed_line(kind, vid, title, source_url)
    if emb:
        block += [emb, ""]
    block += ["<details>", f"<summary>자막: {title}</summary>", "", transcript, "", "</details>"]
    new = "\n".join(before + [""] + block) + "\n"
    if new != txt:
        open(fp, "w", encoding="utf-8").write(new)
        return 1
    return 0


def main():
    if len(sys.argv) < 2:
        print("usage: render-video-refs.py <out_dir>"); return
    total = 0
    for fp in glob.glob(os.path.join(sys.argv[1], "**", "*.md"), recursive=True):
        if "/images/" in fp or os.sep + "youtube.com" + os.sep in fp:
            continue
        total += process(fp)
    print(f"영상 레슨 렌더(접이식 자막): {total}개 파일")


if __name__ == "__main__":
    main()
