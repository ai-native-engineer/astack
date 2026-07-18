"""미러 페이지에 인라인된 base64 이미지를 옆 images/ 폴더의 파일로 빼고 마크다운을 상대경로로 치환.

[실행하라] python3 extract-images.py <out_dir 또는 .md 파일>
이유: transformer-circuits.pub 등은 본문에 base64 이미지가 통째로 박혀 파일이 수십 MB가 되고
GitHub가 1MB 넘는 마크다운 렌더링을 거부한다. 이미지를 빼면 글이 1MB 미만이 돼 정상 렌더된다(본문·그림 모두 보존).

두 래핑 방식 모두 처리: (1) literal 개행으로 줄바꿈된 base64, (2) URL 인코딩 %0A로 줄바꿈된 단일 라인.
malformed 마크다운(닫는 ) 누락) 대응: base64 청크가 (개행|%XX)로 이어지고 본문 prose에서 자동 종료.
증분: data:image 없는 파일은 무변경. 멱등(이미 추출된 파일은 재실행해도 그대로)."""
import re, base64, os, sys, urllib.parse, glob

EXT = {"png":"png","jpeg":"jpg","jpg":"jpg","gif":"gif","webp":"webp","svg+xml":"svg","bmp":"bmp","x-icon":"ico","tiff":"tiff"}
PAT = re.compile(
    r'!\[([^\]]*)\]\(\s*data:image/([a-zA-Z0-9.+-]+);base64,'
    r'([A-Za-z0-9+/=]+(?:(?:\r?\n|%[0-9A-Fa-f]{2})[A-Za-z0-9+/=]+)*)\)?',
    re.IGNORECASE)
# 추출 직후 남는 URL인코딩 찌꺼기(이미지 참조 뒤 %0A·고아 닫는 괄호) 정리
ARTIFACT = re.compile(r'(\]\(images/img-\d+\.[a-zA-Z0-9]+\))(?:%0[Aa])+\)?')


def process(fp):
    txt = open(fp, encoding="utf-8", errors="ignore").read()
    if "data:image" not in txt:
        return 0
    imgdir = os.path.join(os.path.dirname(fp), "images")
    n = [0]
    def repl(m):
        alt, typ = m.group(1), m.group(2).lower()
        b64 = re.sub(r'\s+', '', urllib.parse.unquote(m.group(3)))
        ext = EXT.get(typ, typ.replace("+", "-"))
        try:
            raw = base64.b64decode(b64 + "=" * (-len(b64) % 4), validate=False)
        except Exception:
            return m.group(0)
        if len(raw) < 64:  # 깨진/장식용 초소형은 인라인 유지
            return m.group(0)
        n[0] += 1
        name = f"img-{n[0]:03d}.{ext}"
        os.makedirs(imgdir, exist_ok=True)
        open(os.path.join(imgdir, name), "wb").write(raw)
        return f'![{alt}](images/{name})'
    new = ARTIFACT.sub(r'\1', PAT.sub(repl, txt))
    if new != txt:
        open(fp, "w", encoding="utf-8").write(new)
    return n[0]


def main():
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
