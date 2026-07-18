#!/usr/bin/env python3
"""tts chunk 산출물에서 챕터 타임스탬프를 계산한다.

대본 한 줄이 한 청크(norm_NNNN.wav)이므로, 꼭지 시작 라인 번호를 주면
그 청크의 시작 시각을 쇼노트 컨벤션 형식(hh:mm:ss)으로 출력한다.
"""

import argparse
import glob
import os
import subprocess
import sys


def duration(path):
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", path],
        text=True,
    )
    return float(out.strip())


def hms(seconds):
    s = int(seconds)
    return f"{s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--proj", required=True,
                        help="tts chunk 프로젝트 디렉토리 (chunks/norm_*.wav 포함)")
    parser.add_argument("--lines", required=True,
                        help="꼭지 시작 라인 번호(1부터), 쉼표 구분. 예: 1,5,15")
    args = parser.parse_args()

    chunks = sorted(glob.glob(os.path.join(args.proj, "chunks", "norm_*.wav")))
    if not chunks:
        sys.exit(f"no chunks under {args.proj}/chunks")

    starts, total = [], 0.0
    for chunk in chunks:
        starts.append(total)
        total += duration(chunk)

    for line in (int(x) for x in args.lines.split(",")):
        if not 1 <= line <= len(chunks):
            sys.exit(f"line {line} out of range 1..{len(chunks)}")
        print(f"{hms(starts[line - 1])} line {line}")
    print(f"total {hms(total)}")


if __name__ == "__main__":
    main()
