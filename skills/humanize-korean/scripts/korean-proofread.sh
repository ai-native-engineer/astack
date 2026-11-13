#!/usr/bin/env bash
# 한국어 특화 모델에 교정 의견을 한 번 받는다. 윤문 초안을 stdin으로 받아 교정문을 stdout에 쓴다.
#
#   korean-proofread.sh < draft.md > proofread.md
#
# 모델 선택자는 머신 설정 HUMANIZE_KOREAN_PROOFREAD_MODEL(omp 모델 선택자)에서 읽는다.
# 이 단계는 선택이다. 설정이나 omp가 없거나 모델 호출이 실패하면(일일 한도 소진 등) 교정 없이 종료 코드 3으로 끝나고,
# 호출한 쪽은 건너뛰고 계속한다.
#
# 종료 코드: 0 성공, 2 입력 없음, 3 건너뜀(설정, omp 없음 또는 모델 호출 실패).
set -euo pipefail

AGENTS_ROOT="${AGENTS_HOME:-$HOME/.agents}"
MACHINE_CONFIG="$AGENTS_ROOT/scripts/machine-config.sh"

if ! command -v omp >/dev/null 2>&1; then
  echo "korean-proofread: omp가 없어 교정 단계를 건너뛴다." >&2
  exit 3
fi
if [[ ! -x "$MACHINE_CONFIG" ]] || ! "$MACHINE_CONFIG" has HUMANIZE_KOREAN_PROOFREAD_MODEL; then
  echo "korean-proofread: HUMANIZE_KOREAN_PROOFREAD_MODEL이 없어 교정 단계를 건너뛴다. 키는 machine.env.example에 있다." >&2
  exit 3
fi
model="$("$MACHINE_CONFIG" get HUMANIZE_KOREAN_PROOFREAD_MODEL)"

draft="$(cat)"
if [[ -z "${draft//[[:space:]]/}" ]]; then
  echo "korean-proofread: stdin이 비어 있다. 교정할 글을 stdin으로 넘긴다." >&2
  exit 2
fi

system_prompt='너는 한국어 교정자다. 받은 글을 자연스러운 한국어로 고친다. 사실, 주장, 수치, 날짜, 고유명사, 직접 인용, 코드, 영어 약어는 그대로 둔다. 내용을 더하거나 빼지 않는다. 문단 구성과 Markdown 서식을 유지한다. 교정한 글만 출력한다.'

# 한도 소진 때 omp가 재시도로 몇 분씩 기다리지 않게 재시도와 모델 대체를 끈다.
overlay="$(mktemp "${TMPDIR:-/tmp}/korean-proofread.XXXXXX")"
errlog="$(mktemp "${TMPDIR:-/tmp}/korean-proofread-err.XXXXXX")"
trap 'rm -f "$overlay" "$errlog"' EXIT
printf 'retry:\n  maxRetries: 0\n  modelFallback: false\n' >"$overlay"

# 도구, 스킬, 규칙, 컨텍스트 파일을 끈다. 교정 모델이 에이전트 지침을 읽고 과제 밖 행동을 하지 않게 한다.
# 실패한 호출의 부분 출력이 교정문으로 섞이지 않게 성공했을 때만 출력한다.
if ! result="$(omp -p --no-session --no-tools --no-skills --no-rules --no-context-files --no-extensions --no-title \
  --config "$overlay" --model "$model" --system-prompt "$system_prompt" "$draft" 2>"$errlog")"; then
  printf 'korean-proofread: %s 호출이 실패해 교정 단계를 건너뛴다.\n' "$model" >&2
  grep -v '^Working' "$errlog" | tail -n 1 >&2 || true
  exit 3
fi
# omp가 앞에 넣는 빈 줄만 지운다. 첫 줄의 들여쓰기(Markdown 코드 블록 등)는 보존한다.
printf '%s\n' "${result#"${result%%[!$'\n']*}"}"
