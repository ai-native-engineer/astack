#!/bin/bash
# YouTube 자막 추출 진입점. 실제 구현은 youtube 스킬 공용 fetch-subs.sh 하나에 있다.
# 이 경로는 crawl/transcribe-ids.sh 등 외부 소비자가 참조하므로 파일명을 유지한다.
# Usage: ./extract_transcript.sh <URL> [output_dir]
D="$(cd "$(dirname "$0")" && pwd)"
# astack 플러그인은 이 파일을 crawl/scripts/로 평면 복사하므로 같은 폴더도 후보에 넣는다.
for c in "$D/fetch-subs.sh" "$D/../../scripts/fetch-subs.sh"; do
  [ -f "$c" ] && exec bash "$c" "$@"
done
echo "fetch-subs.sh를 찾지 못했습니다 (탐색: $D, $D/../../scripts)" >&2
exit 69
