"""YouTube 채널 전 영상을 미러에 발행. enumerate -> 전사(공용 캐시) -> 캐시에서 발행 페이지 렌더.

[실행하라] python3 youtube-channels.py <out_dir> <handle>:<channel_id> [<handle>:<channel_id> ...]
예) python3 youtube-channels.py . anthropic-ai:UCrDwWp7EBBv4NwvScIpBDOA claude:UCV03SRZXJEz-hchIAogeJOg
    python3 youtube-channels.py . openai:UCXZCJLdBC09xxGZ6gcdrc6A

설계(두 미러 공용, 단일 enumerator):
1. enumerate: yt-dlp --flat-playlist로 채널 전 영상 ID (메타데이터만 -- 전사의 'raw yt-dlp 금지'와 다른 작업).
2. 전사: ID를 transcribe-ids.sh로 직접 흘려 <out>/_yt-cache/<ID>.md 공용 캐시 생성
   (srt-to-md.sh가 --dump-json으로 title/date/duration/lang 주입. 기존 캐시는 skip = 재요청 0).
3. 렌더: 그 캐시에서 <out>/youtube.com/<handle>/<yymmdd>-<slug>.md 발행 페이지를 [썸네일 + 접이식 <details> 자막]으로 생성
   (render-video-refs.py·inline-transcripts.py와 동일 형태 -> 미러 전체 일관). 채널 인덱스 <out>/youtube.com/<handle>.md 도.

핵심:
- 발행은 호스트 디렉터리 youtube.com/<handle>/ (다른 소스의 <host>/ 트리와 동일 컨벤션). 파일명은 사람이 구별되게
  yymmdd-제목슬러그.md (yymmdd=업로드일, slug=영상제목). 같은 날 동일 슬러그 충돌 시 -<ID6> 접미.
- 전사 캐시는 _yt-cache/<ID>.md(점/호스트 아닌 이름, gitignore, ID-keyed -- inline-transcripts가 youtube_id로 조회).
- 전사는 캐시 한 벌, 발행은 거기서 렌더 = 자막 중복 0. 같은 영상이 글에 인용되면 inline-transcripts가 같은 캐시에서 인라인.
- 멱등/증분: 캐시·발행 페이지 있으면 skip. --render-only(전사 생략, 캐시에서 렌더만), --force(재렌더), --refetch(재전사).
- 범용: 채널을 인자로 받아 두 미러가 같은 스크립트를 쓴다.
"""
import glob
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = "_yt-cache"        # 전사 캐시 디렉터리(gitignore, ID-keyed)
PUB = "youtube.com"        # 발행 디렉터리(추적, <host> 컨벤션)
ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")


def yaml_str(s):
    return s.replace('"', "'").replace("\n", " ").replace("\r", " ").strip()


def slugify(s):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s[:60].strip("-")


def make_filename(meta, vid, seen):
    """yymmdd-slug.md (yymmdd=업로드일). 충돌 시 -<ID6>. seen=핸들 내 사용된 이름 집합."""
    date = meta.get("date", "")
    yymmdd = date[2:4] + date[5:7] + date[8:10] if re.match(r"\d{4}-\d{2}-\d{2}", date) else ""
    slug = slugify(meta.get("title", "") or vid) or vid
    base = f"{yymmdd}-{slug}" if yymmdd else slug
    name = base if base not in seen else f"{base}-{vid[:6]}"
    seen.add(name)
    return name + ".md"


def enumerate_channel(channel_id):
    """채널 영상 (id, title) 목록(재생순=최신 먼저). 실패 시 None.
    title은 무자막 stub(캐시 title='YouTube <id>')의 파일명·H1 보강용 -- flat-playlist는 자막 유무와 무관히 제목을 준다."""
    url = f"https://www.youtube.com/channel/{channel_id}/videos"
    r = subprocess.run(
        ["yt-dlp", "--flat-playlist", "--print", "%(id)s\t%(title)s", url],
        stdin=subprocess.DEVNULL, capture_output=True, text=True,
    )
    if r.returncode != 0 and not r.stdout.strip():
        sys.stderr.write(f"  yt-dlp 실패: {channel_id}\n{r.stderr[-300:]}\n")
        return None
    out = []
    for ln in r.stdout.splitlines():
        parts = ln.split("\t", 1)
        if parts and ID_RE.match(parts[0]):
            out.append((parts[0], parts[1] if len(parts) > 1 else ""))
    return out


def transcribe(ids, cache_dir, force=False):
    if not ids:
        return
    cmd = ["bash", os.path.join(HERE, "transcribe-ids.sh"), cache_dir]
    if force:
        cmd.append("--force")
    p = subprocess.run(cmd, input="\n".join(ids) + "\n", text=True)
    if p.returncode != 0:
        sys.stderr.write("  transcribe-ids.sh 비정상 종료(부분 실패는 재실행 시 증분 재시도)\n")


def backfill_date(vid, meta, cache_fp):
    """무자막 stub은 date가 없다(전사 안 해 srt-to-md가 안 돎). upload_date만 따로 받아 meta+캐시에 채운다.
    메타 fetch는 자막 다운로드와 달리 throttle이 적다. 멱등(캐시에 date 생기면 다음 실행은 skip), 실패 시 그냥 무날짜."""
    if meta.get("date"):
        return
    r = subprocess.run(["yt-dlp", "--print", "%(upload_date)s", "--skip-download",
                        "--cookies-from-browser", "chrome", f"https://www.youtube.com/watch?v={vid}"],
                       stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=60)
    d = r.stdout.strip()
    if re.match(r"^\d{8}$", d):
        iso = f"{d[:4]}-{d[4:6]}-{d[6:8]}"
        meta["date"] = iso
        t = open(cache_fp, encoding="utf-8", errors="ignore").read()
        if "\ndate:" not in t and "\nyoutube_id:" in t:  # 캐시 stub에 persist
            open(cache_fp, "w", encoding="utf-8").write(t.replace("\nyoutube_id:", f"\ndate: {iso}\nyoutube_id:", 1))


def parse_cache(fp):
    """캐시 .md -> {title,date,duration,youtube_id, transcript}. inline-transcripts.py와 동일 파싱."""
    t = open(fp, encoding="utf-8", errors="ignore").read()
    fm = {}
    m = re.match(r"---\n(.*?)\n---", t, re.S)
    if m:
        for k, v in re.findall(r'^(\w+):\s*"?(.*?)"?\s*$', m.group(1), re.M):
            fm[k] = v
    body = ""
    if "## 자막" in t:
        body = t.split("## 자막", 1)[1].split("\n", 1)[1].strip()
    fm["transcript"] = body
    fm.setdefault("youtube_id", os.path.basename(fp)[:-3])
    return fm


def render_page(vid, handle, meta, out_page):
    """발행 페이지 렌더. 자막 있으면 [썸네일 + 접이식 <details> 자막], 없으면 폴드 없이 최소형.
    무자막은 frontmatter captions:none(AI 1차 신호) + 본문 한 줄. 빈 <details> 폴드는 노이즈라 안 쓴다."""
    title = meta.get("title") or f"YouTube {vid}"
    watch = f"https://www.youtube.com/watch?v={vid}"
    thumb = f"https://img.youtube.com/vi/{vid}/hqdefault.jpg"
    transcript = meta.get("transcript", "")
    has_caption = len(transcript) >= 40
    dur = meta.get("duration", "")
    fm = ["---", f'title: "{yaml_str(title)}"', f"channel: {handle}",
          f"url: {watch}", f"youtube_id: {vid}"]
    if meta.get("date"):
        fm.append(f"published: {meta['date']}")
    if dur:
        fm.append(f'duration: "{dur}"')
    fm.append(f"captions: {(meta.get('lang') or 'en') if has_caption else 'none'}")
    fm.append("---")
    body = [f"# {title}", "", f"[![{title}]({thumb})]({watch})"]
    if has_caption:
        summ = f"자막: {title}" + (f" ({dur})" if dur else "")
        body += ["", "<details>", f"<summary>{summ}</summary>", "", transcript, "", "</details>"]
    else:
        body += ["", "_(자막 없음)_"]
    open(out_page, "w", encoding="utf-8").write("\n".join(fm) + "\n\n" + "\n".join(body) + "\n")


def main():
    args = sys.argv[1:]
    force = "--force" in args              # 발행 페이지만 재렌더(저렴)
    refetch = "--refetch" in args          # 전사까지 재추출(비쌈)
    render_only = "--render-only" in args  # 전사 호출 생략, 기존 캐시에서 렌더만
    args = [a for a in args if a not in ("--force", "--refetch", "--render-only")]
    if len(args) < 2:
        print("usage: youtube-channels.py <out_dir> <handle>:<channel_id> [...] [--force] [--refetch] [--render-only]"); return
    out = args[0]
    cache_dir = os.path.join(out, CACHE)
    for spec in args[1:]:
        if ":" not in spec:
            print(f"  잘못된 인자(무시): {spec}  -- 형식은 handle:channel_id"); continue
        handle, cid = spec.split(":", 1)
        ids = enumerate_channel(cid)
        if ids is None:
            print(f"{handle}: enumerate 실패 -- 기존 발행물 보존"); continue
        print(f"{handle}: 채널 영상 {len(ids)}개")
        if not render_only:
            transcribe([v for v, _ in ids], cache_dir, force=refetch)
        ddir = os.path.join(out, PUB, handle)
        os.makedirs(ddir, exist_ok=True)
        rendered = 0
        seen_names = set()
        index = []
        for vid, enum_title in ids:
            cache_fp = os.path.join(cache_dir, f"{vid}.md")
            if not os.path.exists(cache_fp):  # 전사 실패(429 등) -> 다음 실행에 증분 채움
                continue
            meta = parse_cache(cache_fp)
            # 무자막 stub은 title='YouTube <id>'·date 없음 -> enumerate 제목으로 보강(파일명·H1 정상화)
            if (not meta.get("title") or meta["title"].startswith("YouTube ")) and enum_title:
                meta["title"] = enum_title
            if not meta.get("date"):  # 무자막 stub은 date 없음 -> 메타만 받아 yymmdd 통일(throttle 적음)
                backfill_date(vid, meta, cache_fp)
            fname = make_filename(meta, vid, seen_names)
            page_fp = os.path.join(ddir, fname)
            if force or not os.path.exists(page_fp):
                render_page(vid, handle, meta, page_fp)
                rendered += 1
            d = f" — {meta['date']}" if meta.get("date") else ""
            nc = "" if len(meta.get("transcript", "")) >= 40 else " (자막없음)"
            index.append(f"- [{meta.get('title', vid)}]({handle}/{fname}){d}{nc}")
        idx = [f"# {handle} (YouTube)\n", f"영상 {len(index)}개. 썸네일 + 자막(있으면 접이식, 없으면 '자막없음').\n"] + index
        open(os.path.join(out, PUB, f"{handle}.md"), "w", encoding="utf-8").write("\n".join(idx) + "\n")
        print(f"{handle}: 발행 {len(index)}개 (신규 렌더 {rendered}개) -> {PUB}/{handle}/")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--self-test":
        seen = set()
        assert make_filename({"date": "2026-04-09", "title": "Cowork is now GA!"}, "AbcdEfghIjk", seen) == "260409-cowork-is-now-ga.md"
        assert make_filename({"date": "2026-04-09", "title": "Cowork is now GA!"}, "ZZZZZZZZZZZ", seen) == "260409-cowork-is-now-ga-ZZZZZZ.md", "충돌 접미"
        assert make_filename({"title": "No Date Here"}, "Vid12345678", set()) == "no-date-here.md", "무날짜"
        import tempfile
        d = tempfile.mkdtemp()
        page = os.path.join(d, "p.md")
        render_page("ABCDEFGHIJK", "ch",
                    {"title": "Hello: A Test", "date": "2025-01-02", "duration": "3:14", "transcript": "word " * 30},
                    page)
        out = open(page).read()
        assert "img.youtube.com/vi/ABCDEFGHIJK/hqdefault.jpg" in out and "<details>" in out, "렌더 형식"
        assert "published: 2025-01-02" in out and 'duration: "3:14"' in out, "메타데이터"
        assert "captions: en" in out, "유자막 captions 필드"
        assert out.split("---", 2)[1].count("<details>") == 0, "frontmatter 오염"
        # 무자막: <details> 없이 captions:none + 본문 노트
        page2 = os.path.join(d, "p2.md")
        render_page("NocapVid123", "ch", {"title": "Promo Clip", "transcript": ""}, page2)
        o2 = open(page2).read()
        assert "<details>" not in o2, "무자막엔 폴드 없어야"
        assert "captions: none" in o2 and "_(자막 없음)_" in o2, "무자막 신호"
        assert "# Promo Clip" in o2 and "hqdefault.jpg" in o2, "무자막도 제목+썸네일"
        print("self-test ok")
    else:
        main()
