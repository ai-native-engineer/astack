"""미러 페이지에 인라인된 base64 이미지를 옆 images/ 폴더의 파일로 빼고 마크다운을 상대경로로 치환.

[실행하라] python3 extract-images.py <out_dir 또는 .md 파일>
이유: transformer-circuits.pub 등은 본문에 base64 이미지가 통째로 박혀 파일이 수십 MB가 되고
GitHub가 1MB 넘는 마크다운 렌더링을 거부한다. 이미지를 빼면 글이 1MB 미만이 돼 정상 렌더된다(본문·그림 모두 보존).

두 래핑 방식 모두 처리: (1) literal 개행으로 줄바꿈된 base64, (2) URL 인코딩 %0A로 줄바꿈된 단일 라인.
malformed 마크다운(닫는 ) 누락) 대응: base64 청크가 (개행|%XX)로 이어지고 본문 prose에서 자동 종료.
증분: data:image 없는 파일은 무변경. 멱등(이미 추출된 파일은 재실행해도 그대로)."""
import re, base64, hashlib, os, sys, urllib.parse, glob, tempfile

EXT = {"png":"png","jpeg":"jpg","jpg":"jpg","gif":"gif","webp":"webp","svg+xml":"svg","bmp":"bmp","x-icon":"ico","tiff":"tiff"}
PAT = re.compile(
    r'!\[([^\]]*)\]\(\s*data:image/([a-zA-Z0-9.+-]+);base64,'
    r'([A-Za-z0-9+/=]+(?:(?:\r?\n|%[0-9A-Fa-f]{2})[A-Za-z0-9+/=]+)*)\)?',
    re.IGNORECASE)
URLENC_PAT = re.compile(
    r'!\[([^\]]*)\]\(\s*data:image/([a-zA-Z0-9.+-]+),([^\s)]+)\)',
    re.IGNORECASE)
# 추출 직후 남는 URL인코딩 찌꺼기(이미지 참조 뒤 %0A·고아 닫는 괄호) 정리
ARTIFACT = re.compile(r'(\]\(images/[a-zA-Z0-9._-]+\))(?:%0[Aa])+\)?')


def process(fp):
    txt = open(fp, encoding="utf-8", errors="ignore").read()
    if "data:image" not in txt:
        return 0
    imgdir = os.path.join(os.path.dirname(fp), "images")
    n = [0]
    def save(alt, typ, raw, original):
        if len(raw) < 64:  # 깨진/장식용 초소형은 인라인 유지
            return original
        ext = EXT.get(typ, typ.replace("+", "-"))
        n[0] += 1
        name = f"{hashlib.sha256(raw).hexdigest()[:16]}.{ext}"
        os.makedirs(imgdir, exist_ok=True)
        open(os.path.join(imgdir, name), "wb").write(raw)
        return f'![{alt}](images/{name})'

    def repl(m):
        alt, typ = m.group(1), m.group(2).lower()
        b64 = re.sub(r'\s+', '', urllib.parse.unquote(m.group(3)))
        try:
            raw = base64.b64decode(b64 + "=" * (-len(b64) % 4), validate=False)
        except Exception:
            return m.group(0)
        return save(alt, typ, raw, m.group(0))

    def repl_urlencoded(m):
        alt, typ = m.group(1), m.group(2).lower()
        try:
            raw = urllib.parse.unquote_to_bytes(m.group(3))
        except Exception:
            return m.group(0)
        return save(alt, typ, raw, m.group(0))

    new = ARTIFACT.sub(r'\1', URLENC_PAT.sub(repl_urlencoded, PAT.sub(repl, txt)))
    if new != txt:
        open(fp, "w", encoding="utf-8").write(new)
    return n[0]


def main():
    if sys.argv[1:] == ["--self-test"]:
        with tempfile.TemporaryDirectory() as d:
            fp = os.path.join(d, "x.md")
            svg = "%3Csvg%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%3E%3Cpath%20d%3D%22M0%200h100v100H0z%22/%3E%3C/svg%3E"
            open(fp, "w").write(f"![](data:image/svg+xml,{svg})\n")
            assert process(fp) == 1
            name = hashlib.sha256(urllib.parse.unquote_to_bytes(svg)).hexdigest()[:16] + ".svg"
            assert f"images/{name}" in open(fp).read()
            assert open(os.path.join(d, "images", name), "rb").read().startswith(b"<svg")
        print("self-test ok")
        return
    if len(sys.argv) < 2:
        print("usage: extract-images.py <out_dir 또는 .md 파일>"); return
    target = sys.argv[1]
    files = [target] if target.endswith(".md") else [
        f for f in glob.glob(os.path.join(target, "**", "*.md"), recursive=True) if "/images/" not in f]
    total = touched = 0
    for f in files:
        n = process(f)
        if n:
            touched += 1; total += n
            print(f"  +{n}  {os.path.relpath(f, target if os.path.isdir(target) else '.')}", flush=True)
    print(f"이미지 추출: {total}개 / {touched}개 파일")


if __name__ == "__main__":
    main()
