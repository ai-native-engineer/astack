#!/usr/bin/env python3
"""화자 타임라인(argmax diarize RTTM)을 전사본에 붙여 화자 라벨 뷰를 만든다.
   apple : apple-stt JSON(문장 단위) + RTTM  → 깨끗한 텍스트 / 굵은 화자
   argmax: argmax JSON(단어 단위)   + RTTM  → whisper 텍스트 / 정밀 화자
usage:
   diar_views.py apple  apple.json  diar.rttm
   diar_views.py argmax argmax.json diar.rttm
"""
import json, sys
from collections import defaultdict

mode, tr_path, rttm_path = sys.argv[1], sys.argv[2], sys.argv[3]

# RTTM: 파일명에 공백이 있어도 깨지지 않게 뒤 고정 필드(음수 인덱스)로 파싱
turns = []
for line in open(rttm_path):
    p = line.split()
    if len(p) < 9 or p[0] != "SPEAKER":
        continue
    st, dur, spk = float(p[-7]), float(p[-6]), p[-3]
    turns.append((st, st + dur, spk))


def speaker_of(s, e):
    ov = defaultdict(float)
    for ts, te, spk in turns:
        o = min(e, te) - max(s, ts)
        if o > 0:
            ov[spk] += o
    return max(ov, key=ov.get) if ov else "?"


def hhmmss(t):
    m, s = divmod(int(t), 60)
    return f"{m:02d}:{s:02d}"


doc = json.load(open(tr_path))

# 전사 단위 추출: apple=문장 세그먼트, argmax=단어
units = []  # (start, end, text)
if mode == "apple":
    for seg in doc:
        a = seg.get("start", 0.0)
        units.append((a, seg.get("end", a), seg.get("text", "").strip()))
elif mode == "argmax":
    for seg in doc.get("segments", []):
        for w in seg.get("words", []):
            t = w.get("word", "").strip()
            if t and not t.startswith("<|"):  # 특수토큰 제외
                units.append((w.get("start", 0.0), w.get("end", 0.0), t))
else:
    sys.exit("mode must be apple|argmax")

# 화자 배정 후 연속 동일 화자 묶기
rows, cur, start, buf = [], None, None, []
for a, b, text in units:
    spk = speaker_of(a, b)
    if spk != cur:
        if buf:
            rows.append(f"**[{cur}]** ({hhmmss(start)}) " + " ".join(buf))
        cur, start, buf = spk, a, [text]
    else:
        buf.append(text)
if buf:
    rows.append(f"**[{cur}]** ({hhmmss(start)}) " + " ".join(buf))

print("\n\n".join(rows))
