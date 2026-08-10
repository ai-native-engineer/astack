"""미러 발행 트리 검증 (mirror-generic, anthropic/openai 미러 공용).

크롤·전사·후처리가 끝난 out_dir에서 발행물이 계약대로인지 결정론으로 검사한다:
 1) YouTube 자막 커버리지 -- 발행 .md의 모든 영상 참조는 (a) 참조 뒤 500자 내 <details> 폴드,
    (b) 해당 파일에 captions: none 표기, (c) _yt-cache에 '자막 없음' 기록, 셋 중 하나여야 한다.
    셋 다 아니면 전사 누락(youtube-transcripts.sh + inline-transcripts.py, 채널 트리는 youtube-channels.py 재실행 대상).
 2) GitHub 렌더 리밋 -- 1MB 초과 .md는 GitHub이 렌더를 거부한다(extract-images.py 누락 신호).

전사에서 의도적으로 제외한 트리(academy·docs 등)는 같은 --exclude 글롭으로 검사에서도 뺀다.
실행: python3 verify-mirror.py <out_dir> [--exclude <glob>]...   문제 없으면 exit 0, 있으면 exit 1.
"""
import argparse, fnmatch, glob, os, re, sys

IDS = re.compile(
    r'(?:youtube(?:-nocookie)?\.com/(?:watch\?(?:[^#\s)]*&)?v=|embed/|live/|shorts/)|youtu\.be/)'
    r'([A-Za-z0-9_-]{11})'
)
SKIP_FILES = {"README.md", "README.ko.md", "AGENTS.md", "CLAUDE.md", "MEMORY.md"}


def cache_captionless(out, vid):
    """_yt-cache 기록이 '자막 없음'인가. 캐시 자체가 없으면 None(전사 미시도)."""
    p = os.path.join(out, "_yt-cache", f"{vid}.md")
    if not os.path.exists(p):
        return None
    t = open(p, encoding="utf-8", errors="replace").read()
    return "captions: none" in t or len(t) < 500


def self_test():
    vid = "abcdefghijk"
    forms = [
        f"https://www.youtube.com/watch?list=x&v={vid}",
        f"https://www.youtube.com/embed/{vid}",
        f"https://www.youtube.com/live/{vid}",
        f"https://www.youtube.com/shorts/{vid}",
        f"https://www.youtube-nocookie.com/embed/{vid}",
        f"https://youtu.be/{vid}",
    ]
    assert all(IDS.search(url).group(1) == vid for url in forms)
    print("self-test ok")


def main():
    if sys.argv[1:] == ["--self-test"]:
        self_test()
        return
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--exclude", action="append", default=[], help="검사 제외 글롭(전사 제외 트리와 동일하게)")
    a = ap.parse_args()

    missing, oversized, checked = [], [], 0
    for p in glob.glob(os.path.join(a.out, "**/*.md"), recursive=True):
        rel = os.path.relpath(p, a.out)
        if rel.startswith("_yt-cache/") or os.path.basename(rel) in SKIP_FILES:
            continue
        if any(fnmatch.fnmatch(rel, g) for g in a.exclude):
            continue
        if os.path.getsize(p) > 1024 * 1024:
            oversized.append(rel)
        t = open(p, encoding="utf-8", errors="replace").read()
        for vid in set(IDS.findall(t)):
            checked += 1
            if re.search(rf'{re.escape(vid)}[\s\S]{{0,500}}<details>', t):
                continue
            if "captions: none" in t:
                continue  # 무자막 채널 stub은 폴드 생략이 계약
            if cache_captionless(a.out, vid):
                continue  # 전사 시도했으나 자막 없음 -> 폴드 없는 게 정상
            missing.append((rel, vid))

    print(f"영상 참조 {checked}건 검사: 자막 누락 {len(missing)}건 / 1MB 초과 .md {len(oversized)}건")
    for rel, vid in missing[:20]:
        print(f"  전사 누락: {rel} [{vid}]")
    for rel in oversized[:20]:
        print(f"  1MB 초과(extract-images 필요): {rel}")
    sys.exit(1 if (missing or oversized) else 0)


if __name__ == "__main__":
    main()
