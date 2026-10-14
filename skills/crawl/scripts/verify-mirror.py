"""미러 발행 트리 검증 (mirror-generic, anthropic/openai 미러 공용).

크롤·전사·후처리가 끝난 out_dir에서 발행물이 계약대로인지 결정론으로 검사한다:
 1) YouTube 자막 커버리지 -- 발행 .md의 모든 영상 참조는 (a) 참조 뒤 500자 내 <details> 폴드,
    (b) 해당 파일에 captions: none 표기, (c) _yt-cache에 '자막 없음' 기록, 셋 중 하나여야 한다.
    셋 다 아니면 전사 누락(youtube-transcripts.sh + inline-transcripts.py, 채널 트리는 youtube-channels.py 재실행 대상).
 2) GitHub 렌더 리밋 -- 1MiB 초과 .md는 GitHub이 렌더를 거부한다(extract-images.py·split-markdown.py 누락 신호).
 3) 빈 이미지 참조 -- ![alt]() 는 어떤 자산도 가리키지 않는다. 수집기가 제거하거나 미수집 마커로 바꿔야 한다.
 4) 깨진 로컬 참조 -- 상대 경로 이미지와 확장자 있는 상대 링크는 미러 안의 실제 파일을 가리켜야 한다.
    인라인 `![](a)`, `[](a)` 와 레퍼런스 스타일 `![a][id]`, `[t][id]` + `[id]: 경로` 를 모두 본다.
    경로의 퍼센트 인코딩(%20)은 풀고 본다.
 5) 미해결 attachment: 이미지 -- Jupyter 첨부 참조는 미러에서 렌더되지 않는다.
경고(종료 코드에 반영 안 함):
 - root-relative 링크(/docs/...)는 미러 안에서 해석되지 않는다.
 - 닫히지 않은 코드 펜스. 원문이 예시 안에 같은 길이의 펜스를 중첩하면 CommonMark 기준으로
   블록이 안 닫혀 그 뒤 본문이 참조 검사에서 빠진다. 미러가 고칠 수 있는 게 아니라 경고다.

전사에서 의도적으로 제외한 트리(academy·docs 등)는 같은 --exclude 글롭으로 영상 검사에서만 뺀다.
참조·크기 검사(2~5)는 --exclude와 무관하게 전체 트리에 적용한다.
코드 블록·인라인 코드·HTML 주석 안은 참조로 보지 않는다. 4칸 들여쓴 코드 블록은 목록 본문과
구별할 수 없어 다루지 않으므로, 그 안의 예시 참조는 검사에 걸린다.
실행: python3 verify-mirror.py <out_dir> [--exclude <glob>]... [--json FILE]   문제 없으면 exit 0, 있으면 exit 1.
다른 검증기는 scan(out, excludes)를 import해 같은 결과를 합칠 수 있다.
"""

import argparse, fnmatch, json, os, re, sys, tempfile
from urllib.parse import unquote

IDS = re.compile(
    r"(?:youtube(?:-nocookie)?\.com/(?:watch\?(?:[^#\s)]*&)?v=|embed/|live/|shorts/)|youtu\.be/)"
    r"([A-Za-z0-9_-]{11})"
)
SKIP_FILES = {"README.md", "README.ko.md", "AGENTS.md", "CLAUDE.md", "MEMORY.md"}
SKIP_DIRS = {".git", ".agents", ".claude", "_yt-cache", "node_modules"}
MAX_MD_BYTES = 1024 * 1024
IMAGE_REF = re.compile(r"!\[([^\]]*)\]\(\s*(<[^>]*>|[^)\s]*)")
LINK_REF = re.compile(r"(?<!!)\[[^\]\n]*\]\(\s*(<[^>]*>|[^)\s]+)")
# 링크를 세기 전에 줄에서 걷어낼 이미지 전체. 안 걷어내면 [![alt](img)](url) 의 img가
# 이미지로 한 번, 바깥 링크의 대괄호에 삼켜져 링크로 또 한 번 집계된다.
IMAGE_FULL = re.compile(r"!\[[^\]]*\]\([^)]*\)")
# 레퍼런스 스타일: ![alt][id] / [text][id]. 빈 id는 alt를 id로 쓰는 collapsed 형식.
IMAGE_REFSTYLE = re.compile(r"!\[([^\]]*)\]\[([^\]]*)\]")
LINK_REFSTYLE = re.compile(r"(?<!!)\[([^\]\n]*)\]\[([^\]]*)\]")
# 목적지 앞 공백에 개행을 하나까지만 허용한다. \s* 로 두면 빈 줄을 넘어 다음 문단의
# 첫 토큰을 목적지로 잡는다.
LINK_DEF = re.compile(r"^ {0,3}\[([^\]]+)\]:[ \t]*(?:\n[ \t]*)?(<[^>]*>|\S+)", re.M)
# 여는 구분자의 문자와 길이를 따로 기억한다. 길이를 안 보면 ```` 안의 ``` 가,
# 문자를 안 보면 ``` 안의 ~~~ 가 블록을 조기에 닫는다.
FENCE_OPEN = re.compile(r"^\s*(`{3,}|~{3,})(.*)$")
BACKTICK_RUNS = re.compile(r"`+")
SCHEME = re.compile(r"^[a-z][a-z0-9+.-]*:|^//|^#", re.I)
# 경고 kind는 목록에는 남기되 종료 코드에는 반영하지 않는다.
# 닫히지 않은 펜스는 대개 예시 안에 같은 길이의 펜스를 중첩한 원문 탓이라 미러가
# 고칠 수 있는 게 아니다. 다만 그 뒤 본문이 검사에서 빠지므로 보이게는 남긴다.
WARN_KINDS = {"root-relative 링크", "닫히지 않은 코드 펜스"}


def cache_captionless(out, vid):
    """_yt-cache 기록이 '자막 없음'인가. 캐시 자체가 없으면 None(전사 미시도)."""
    p = os.path.join(out, "_yt-cache", f"{vid}.md")
    if not os.path.exists(p):
        return None
    t = open(p, encoding="utf-8", errors="replace").read()
    return "captions: none" in t or len(t) < 500


def strip_code_spans(line):
    """인라인 코드를 걷어낸다. 백틱 런은 같은 길이의 다음 런에서 닫히고, 짝 없는 런은 글자다.

    정규식으로 쓰면(`` (`+)(?:(?!\\1).)+?\\1 ``) 백틱이 수백 개인 줄에서 역추적이 폭발해
    한 줄에 수 분이 걸린다. 입력이 크롤한 임의의 웹 문서라 그 줄이 언제든 들어올 수 있다.
    """
    if "`" not in line:
        return line
    runs = [(m.start(), m.end()) for m in BACKTICK_RUNS.finditer(line)]
    if len(runs) < 2:
        return line
    out, pos, i = [], 0, 0
    while i < len(runs):
        start, end = runs[i]
        width = end - start
        close = next(
            (k for k in range(i + 1, len(runs)) if runs[k][1] - runs[k][0] == width),
            None,
        )
        if close is None:
            i += 1
            continue
        out.append(line[pos:start])
        pos = runs[close][1]
        i = close + 1
    out.append(line[pos:])
    return "".join(out)


def strip_comment(line, inside):
    """(주석을 걷어낸 줄, 이 줄 끝에서도 주석 안인가).

    줄 단위로 처리한다. 본문 전체에 re.S로 걸면 코드 블록 안의 `<!--` 와 밖의 `-->` 가
    짝지어 그 사이 참조가 통째로 사라지고, 두 줄에 걸친 주석을 지우면서 `[text<!--` 와
    `-->](gone.md)` 를 이어 붙여 없던 참조를 만든다.
    """
    if not inside and "<!--" not in line:
        return line, False
    parts = []
    while line:
        if inside:
            end = line.find("-->")
            if end < 0:
                return "".join(parts), True
            line = line[end + 3 :]
            inside = False
            continue
        start = line.find("<!--")
        if start < 0:
            parts.append(line)
            return "".join(parts), False
        parts.append(line[:start])
        line = line[start + 4 :]
        inside = True
    return "".join(parts), inside


def split_prose(text):
    """(산문 줄 목록, 닫히지 않은 펜스를 연 줄 번호 또는 None).

    코드 예시 안의 ![]()·링크는 참조가 아니므로 코드 블록과 인라인 코드, HTML 주석을
    걷어낸다. 닫는 펜스는 여는 것과 같은 문자로 같거나 더 길고 info string이 없어야
    한다. 4칸 들여쓴 코드 블록은 목록 본문과 구별할 수 없어 다루지 않는다.
    """
    fence = None  # (문자, 길이, 연 줄 번호)
    inside_comment = False
    out = []
    skipped = 0
    for no, line in enumerate(text.splitlines(), 1):
        if inside_comment:
            end = line.find("-->")
            if end < 0:
                continue
            line, inside_comment = line[end + 3 :], False
        m = FENCE_OPEN.match(line)
        if m and m.group(1)[0] == "`" and "`" in m.group(2):
            # 백틱 펜스의 info string에는 백틱이 올 수 없다(CommonMark). 펜스가 아니라 산문이다.
            m = None
        if m:
            marker = m.group(1)
            char, length = marker[0], len(marker)
            if fence is None:
                fence = (char, length, no)
            elif char == fence[0] and length >= fence[1] and not m.group(2).strip():
                fence = None
            continue
        if fence is not None:
            skipped += 1
            continue
        line, inside_comment = strip_comment(line, inside_comment)
        out.append(strip_code_spans(line))
    return out, (fence[2], skipped) if fence else None


def prose_lines(text):
    """코드 블록 밖 줄만 돌려준다."""
    return split_prose(text)[0]


def local_missing(base, ref):
    """미러 안 상대 경로인데 그 파일이 없으면 True.

    적힌 그대로와 퍼센트 인코딩을 푼 것 둘 다 본다. 디스크의 'a b.png'를 가리키는
    'a%20b.png'는 풀어야 찾고, 파일명에 리터럴 '%20'이 든 파일(미러에 실재한다)은
    풀지 말아야 찾는다.
    """
    target = ref.split("#")[0].split("?")[0]
    if not target:
        return False
    raw = os.path.join(base, target)
    return not os.path.exists(raw) and not os.path.exists(os.path.join(base, unquote(target)))


def reference_issues(out, rel, text):
    base = os.path.dirname(os.path.join(out, rel))
    lines, unclosed = split_prose(text)
    found = []
    if unclosed:
        # 그냥 두면 펜스 뒤 본문 전체가 코드로 분류돼 검사에서 조용히 빠진다.
        # 몇 줄이 빠졌는지 적어야 사람이 원문 탓인지 수집기 탓인지 가릴 수 있다.
        opener, skipped = unclosed
        found.append(
            ("닫히지 않은 코드 펜스", rel, f"{opener}행에서 열림, 뒤 {skipped}줄이 검사에서 빠짐")
        )
    # 레퍼런스 스타일의 타깃은 본문이 아니라 파일 아래쪽 정의에 있다. 코드 블록 안의
    # `[k: string]: unknown` 같은 줄을 정의로 주우면 없는 파일을 가리키는 거짓 양성이
    # 되므로 산문 줄에서만 모은다. 같은 id가 겹치면 CommonMark대로 첫 정의가 이긴다.
    defs = {}
    for name, target in LINK_DEF.findall("\n".join(lines)):
        defs.setdefault(name.strip().lower(), target.strip("<>").strip())

    def image(alt, ref):
        if not ref:
            found.append(("빈 이미지 참조", rel, f"![{alt[:40]}]()"))
        elif ref.startswith("attachment:"):
            found.append(("미해결 attachment 이미지", rel, ref[:60]))
        elif ref.startswith("/") and not ref.startswith("//"):
            found.append(("root-relative 링크", rel, ref[:80]))
        elif not SCHEME.match(ref) and local_missing(base, ref):
            found.append(("깨진 로컬 이미지 참조", rel, ref[:80]))

    def link(ref):
        if not ref or SCHEME.match(ref):
            return
        if ref.startswith("/"):
            found.append(("root-relative 링크", rel, ref[:80]))
            return
        target = ref.split("#")[0].split("?")[0]
        # 확장자가 있는 상대 경로만 로컬 파일 참조로 본다. 'URL'·'2' 같은 괄호 속 텍스트는 참조가 아니다.
        if re.search(r"\.[A-Za-z0-9]{1,5}$", target) and local_missing(base, ref):
            found.append(("깨진 로컬 링크", rel, ref[:80]))

    def resolve(alt, name):
        """collapsed 형식 ![alt][] 은 alt를 id로 쓴다. 정의가 없으면 참조가 아니다."""
        return defs.get((name or alt).strip().lower())

    for line in lines:
        for alt, ref in IMAGE_REF.findall(line):
            ref = ref.strip()
            if ref.startswith("<") and ref.endswith(">"):
                ref = ref[1:-1].strip()
            image(alt, ref)
        for alt, name in IMAGE_REFSTYLE.findall(line):
            target = resolve(alt, name)
            if target is not None:
                image(alt, target)
        # 인라인·레퍼런스 이미지를 걷어낸 뒤 링크를 센다. 안 걷으면 [![alt](img)](url)
        # 의 img가 이미지와 링크로 두 번 집계된다.
        rest = IMAGE_REFSTYLE.sub("", IMAGE_FULL.sub("", line))
        for ref in LINK_REF.findall(rest):
            link(ref.strip("<>").strip())
        for text_, name in LINK_REFSTYLE.findall(rest):
            target = resolve(text_, name)
            if target is not None:
                link(target)
    return found


def scan(out, excludes=()):
    """전체 결과 [(kind, rel, detail)]. WARN_KINDS에 속한 kind는 경고다."""
    results = []
    for root, dirs, files in os.walk(out):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not d.startswith("."))  # 숨김 폴더는 작업 상태다
        for name in sorted(files):
            if not name.endswith(".md") or name in SKIP_FILES:
                continue
            p = os.path.join(root, name)
            rel = os.path.relpath(p, out)
            if os.path.getsize(p) > MAX_MD_BYTES:
                results.append(("1MiB 초과 .md", rel, f"{os.path.getsize(p)} bytes"))
            t = open(p, encoding="utf-8", errors="replace").read()
            results.extend(reference_issues(out, rel, t))
            if any(fnmatch.fnmatch(rel, g) for g in excludes):
                continue
            for vid in sorted(set(IDS.findall(t))):
                if re.search(rf"{re.escape(vid)}[\s\S]{{0,500}}<details>", t):
                    continue
                if "captions: none" in t:
                    continue  # 무자막 채널 stub은 폴드 생략이 계약
                if cache_captionless(out, vid):
                    continue  # 전사 시도했으나 자막 없음 -> 폴드 없는 게 정상
                results.append(("영상 자막 누락", rel, vid))
    return results


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
    with tempfile.TemporaryDirectory() as out:
        os.makedirs(os.path.join(out, "site", "images"))
        open(os.path.join(out, "site", "images", "ok.png"), "wb").write(b"x")
        pages = {
            "site/ok.md": "![a](images/ok.png) [b](other.md#x) [c](https://x) `![]()` (URL) [d](URL)\n```\n![]()\n```\n",
            "site/other.md": f"https://youtu.be/{vid}\n<details>t</details>\n",
            "site/bad.md": "![]() ![x](<>) ![y](images/missing.png) [z](gone.md) ![w](attachment:image.png) [r](/docs/x)\n",
            "site/big.md": "x" * (MAX_MD_BYTES + 1),
            "skip/video.md": f"https://youtu.be/{vid}\n",
            ".audit/report.md": "![]()\n",
        }
        for rel, text in pages.items():
            os.makedirs(os.path.dirname(os.path.join(out, rel)), exist_ok=True)
            open(os.path.join(out, rel), "w", encoding="utf-8").write(text)
        by_file = {}
        for kind, rel, _ in scan(out):
            by_file.setdefault(rel, []).append(kind)
        assert "site/ok.md" not in by_file, by_file
        assert ".audit/report.md" not in by_file, "숨김 폴더는 검사하지 않는다"
        assert sorted(by_file["site/bad.md"]) == sorted(
            [
                "빈 이미지 참조",
                "빈 이미지 참조",
                "깨진 로컬 이미지 참조",
                "깨진 로컬 링크",
                "미해결 attachment 이미지",
                "root-relative 링크",
            ]
        ), by_file
        assert by_file["site/big.md"] == ["1MiB 초과 .md"]
        assert by_file["skip/video.md"] == ["영상 자막 누락"]
        assert "skip/video.md" not in {r for _, r, _ in scan(out, ["skip/**"])}
    print("self-test ok")


def main():
    if sys.argv[1:] == ["--self-test"]:
        self_test()
        return
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="영상 자막 검사 제외 글롭(전사 제외 트리와 동일하게)",
    )
    ap.add_argument("--json", help="전체 결과를 JSON으로 저장")
    a = ap.parse_args()

    results = scan(a.out, a.exclude)
    failures = [r for r in results if r[0] not in WARN_KINDS]
    counts = {}
    for kind, _, _ in results:
        counts[kind] = counts.get(kind, 0) + 1
    print(f"문제 {len(failures)}건 / 경고 {len(results) - len(failures)}건")
    for kind, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"  {n:6d}  {kind}{' (경고)' if kind in WARN_KINDS else ''}")
    for kind, rel, detail in failures[:30]:
        print(f"  - {kind}: {rel} [{detail}]")
    if len(failures) > 30:
        print(f"  ... 나머지 {len(failures) - 30}건 (--json으로 전체 확인)")
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump(
                [
                    {"kind": k, "path": r, "detail": d, "warning": k in WARN_KINDS}
                    for k, r, d in results
                ],
                f,
                ensure_ascii=False,
                indent=2,
            )
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
