"""미러 페이지의 YouTube 링크 바로 아래에 [썸네일 임베드 + 접이식 자막]을 인라인 삽입.

[실행하라] python3 inline-transcripts.py <out_dir>
이유: 자막을 youtube.com/<ID>.md 별도 트리에 두면 어느 글의 영상인지 연관을 못 찾는다.
대신 영상이 인용된 위치 바로 아래에 자막을 붙여 맥락과 함께 읽히게 한다.

선행: youtube-transcripts.sh가 <out>/youtube.com/<ID>.md 캐시(frontmatter+자막)를 먼저 만든다.
이 스크립트는 그 캐시를 읽어 각 페이지에 인라인한다. 캐시(youtube.com/)는 gitignore -- 발행되는 건 인라인 형태.
멱등: <!-- yt-inline:ID --> 마커로 재실행 시 중복 삽입 안 함. 자막 없는 영상은 "자막 없음" 블록을 붙인다."""
import glob
import os
import re
import sys

ID_RE = re.compile(
    r'(?:youtu\.be/|youtube(?:-nocookie)?\.com/(?:watch\?v=|embed/|live/|shorts/))'
    r'([A-Za-z0-9_-]{11})',
    re.I,
)


def load_transcripts(mirror):
    m = {}
    for fp in glob.glob(os.path.join(mirror, "_yt-cache", "*.md")):
        t = open(fp, encoding="utf-8", errors="ignore").read()
        fm, fmm = {}, re.match(r'---\n(.*?)\n---', t, re.S)
        if fmm:
            for k, v in re.findall(r'^(\w+):\s*"?(.*?)"?\s*$', fmm.group(1), re.M):
                fm[k] = v
        vid = fm.get("youtube_id") or os.path.basename(fp)[:-3]
        body = t.split("## 자막", 1)[1].split("\n", 1)[1].strip() if "## 자막" in t else ""
        m[vid] = {"title": fm.get("title", vid), "duration": fm.get("duration", ""), "body": body}
    return m


def block(vid, tr):
    dur = f" ({tr['duration']})" if tr["duration"] else ""
    thumb = f"https://img.youtube.com/vi/{vid}/hqdefault.jpg"
    url = f"https://www.youtube.com/watch?v={vid}"
    body = tr["body"] if len(tr["body"]) >= 40 else "_(자막 없음)_"
    return (f"\n<!-- yt-inline:{vid} -->\n"
            f"[![{tr['title']}]({thumb})]({url})\n\n"
            f"<details>\n<summary>자막: {tr['title']}{dur}</summary>\n\n{body}\n\n</details>\n")


def process(fp, trmap):
    txt = open(fp, encoding="utf-8", errors="ignore").read()
    if "<!-- youtube:" in txt or "<!-- vimeo:" in txt:
        return 0  # academy/채널 페이지: render-video-refs가 이미 전사를 인라인함(중복 방지, 도메인 무관)
    lines = txt.split("\n")
    out, seen, added = [], set(), 0
    # 선행 YAML 프론트매터(---...---) 안의 url은 앵커 금지: 블록이 frontmatter를 쪼개 깨뜨린다
    fm_end = -1
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                fm_end = i; break
    for i, line in enumerate(lines):
        out.append(line)
        if i <= fm_end:
            continue
        for vid in dict.fromkeys(ID_RE.findall(line)):
            if vid in seen or vid not in trmap:
                continue
            seen.add(vid)
            if f"yt-inline:{vid}" in txt:  # 이미 삽입됨
                continue
            out.append(block(vid, trmap[vid])); added += 1
    if added:
        open(fp, "w", encoding="utf-8").write("\n".join(out).rstrip() + "\n")
    return added


def main():
    if len(sys.argv) < 2:
        print("usage: inline-transcripts.py <out_dir>"); return
    if sys.argv[1] == "--self-test":
        sample = "\n".join([
            "https://youtu.be/ABCDEFGHIJK",
            "https://www.youtube.com/watch?v=1234567890_&t=1",
            "https://www.youtube.com/embed/abcDEF12345",
            "https://www.youtube-nocookie.com/embed/ZyxwvUT9876",
            "https://youtube.com/live/EvtPBaaykdo?t=1",
            "https://youtube.com/shorts/shortsID_01",
        ])
        assert ID_RE.findall(sample) == [
            "ABCDEFGHIJK",
            "1234567890_",
            "abcDEF12345",
            "ZyxwvUT9876",
            "EvtPBaaykdo",
            "shortsID_01",
        ]
        import tempfile
        vid = "ABCDEFGHIJK"
        doc = (f'---\ntitle: "x"\nurl: https://www.youtube.com/watch?v={vid}\n---\n'
               f'\n# x\n\nhttps://www.youtube.com/watch?v={vid}\n')
        tf = os.path.join(tempfile.mkdtemp(), "v.md")
        open(tf, "w").write(doc)
        process(tf, {vid: {"title": "x", "duration": "", "body": "x" * 50}})
        res = open(tf).read()
        assert res.count(f"yt-inline:{vid}") == 1, "블록이 정확히 1번 삽입돼야 함"
        assert "yt-inline" not in res.split("---", 2)[1], "frontmatter 안엔 블록이 들어가면 안 됨"
        print("self-test ok")
        return
    mirror = sys.argv[1]
    tr = load_transcripts(mirror)
    print(f"자막 캐시 {len(tr)}개 로드")
    total = files = 0
    # 범용 비대상 트리만 경로로 제외(이미지·전사 캐시·채널 발행). academy 등 도메인은 하드코딩하지 않는다 ->
    # 대신 process()가 render-video-refs 마커(<!-- youtube/vimeo:)를 가진 파일을 건너뛴다(도메인 무관, 중복 방지).
    skip = ("/images/", os.sep + "_yt-cache" + os.sep, os.sep + "youtube.com" + os.sep)
    for fp in glob.glob(os.path.join(mirror, "**", "*.md"), recursive=True):
        if any(s in fp for s in skip):
            continue
        n = process(fp, tr)
        if n:
            total += n; files += 1
            print(f"  +{n}  {os.path.relpath(fp, mirror)}", flush=True)
    print(f"인라인 삽입: {total}건 / {files}개 파일")


if __name__ == "__main__":
    main()
