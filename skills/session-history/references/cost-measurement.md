# 비용·쿼터 측정 (token_usage)

Claude, Codex, Grok 로컬 세션 로그로 **토큰 실사용**과 **API 환산 비용**, 선택적으로 **구독 한도(live)** 를 본다. 구독 청구서가 아니라 같은 사용량을 list API 단가로 환산한 대체비용이다.

## 목차

- 대표 명령
- 데이터 정본
- 모델 해석 정책
- 단가표
- 구독 한도
- 해석 주의

## 언제 이 문서를 읽나

- 이번 달/최근 N일 “얼마 썼지”, 모델별 비중, 구독 대비 API 가치가 필요할 때
- `token_usage.py`의 `--cost` / `--by-model` / `--month` / `--quota` 동작을 확인할 때
- 단가가 바뀌었거나 새 모델을 표에 넣을 때

## 대표 명령

스킬 루트(`session-history/`)에서 실행한다.

```bash
python3 scripts/token_usage.py --days 7 --cost --by-model
python3 scripts/token_usage.py --month --cost --by-model   # 이번 달
python3 scripts/token_usage.py --month 2026-07 --cost
python3 scripts/token_usage.py --days 1 --quota
python3 scripts/token_usage.py --days 7 --cost --quota --format json
```

전체 플래그는 `python3 scripts/token_usage.py -h`.

## 데이터 정본

| 도구 | 토큰 소스 | 모델 | 비용 |
|---|---|---|---|
| Claude | projects `*.jsonl` assistant `usage` (requestId dedupe) | `message.model` | 단가표 + cache 5m/1h split |
| Codex | rollout `event_msg.token_count` | `thread_settings_applied.thread_settings.model` (provider 이름 아님) | 단가표 |
| Grok | `updates.jsonl` `turn_completed.usage` | summary/`modelUsage` 키 | **`costUsdTicks` 우선** (10_000_000_000 ticks = $1), 없으면 단가표 |
| opencode | `part.data` assistant token 필드 | `message.data.modelID` | 단가표 |
| Aside | `session_runs.token_usage` JSON (`input`/`output`/`cacheRead`/`cacheWrite`) | `sessions.model` JSON | 단가표 |
| OpenClaw | message `usage` (`input`/`output`/`cacheRead`/`cacheWrite`) | `message.model` | 단가표 |
| Copilot | `session.shutdown.data.modelMetrics[model].tokenDetails` | modelMetrics 키 | 단가표 |

`token_usage.py`는 위 adapter만 집계한다. Cursor, Gemini CLI/Antigravity, VS Code Copilot Chat 로컬 transcript는 안정적인 token usage를 제공하지 않아 token과 cost 합계에서 제외된다.

Copilot의 `modelMetrics[model].usage.inputTokens`는 cache read/write를 이미 더한 값이다. `tokenDetails.input`(순수 input)을 쓰지 않으면 캐시가 이중 계상된다. 표에 보이는 합계 열은 cache를 뺀 `pure_tokens`(input+output)이고, cache 포함 처리량은 `전체처리량` 줄에 따로 나온다.

Claude `usage.cache_creation.ephemeral_5m_input_tokens` / `ephemeral_1h_input_tokens`가 있으면 각각 5m·1h write 단가로 잡는다. split이 없고 total만 있으면 5m 단가로 합산(1h 비중을 과소평가할 수 있음).

## 모델 해석 정책

정본: `scripts/pricing.py`의 `resolve_model_key` / `is_non_model_id`.

| 입력 | 결과 | 비용 출처 |
|---|---|---|
| 빈 모델, 또는 provider/synthetic placeholder (`openai`, `codex`, `<synthetic>` 등) | 도구 기본 모델 | `default` (Codex→`gpt-6.1-sol`, Claude→`claude-opus-5.5`, Grok→`grok-4.5`) |
| 표에 있는 id / alias / safe prefix | 해당 단가 | `rate_card` (Grok ticks 있으면 `provider_ticks`) |
| **실모델 id인데 표에 없음** | unpriced | 합계 **미포함**, `missing_models`에 이름·event 수 표시 |

미매칭 실모델을 플래그십 단가로 조용히 채우지 않는다. 단가를 넣으려면 `DEFAULT_RATES`를 고치거나 `--pricing-file`을 쓴다.

Codex는 `thread_settings.model`만 모델로 쓴다. `model_provider` 필드는 무시한다. 모델이 비어 있으면 도구 기본 단가(default)로 환산한다.

## 단가표

정본 코드: `scripts/pricing.py`의 `DEFAULT_RATES` (USD / MTok 스냅샷).

가격 출처(유지보수 시 대조):

- OpenAI GPT-6.1 Sol, GPT-6 Astra/Sol/Luna, GPT-5.6 Sol/Terra/Luna: OpenAI API 모델 페이지의 가격표
- Anthropic Opus/Sonnet/Haiku/Fable: Anthropic pricing 문서. Opus 5.5와 Fable 5.1은 cache hit 배율이 다른 모델(0.1x)과 달라(0.05x, 0.025x) 표에 따로 둔다
- 점 릴리스(`claude-opus-5-5`, `claude-fable-5-1` 등)는 계열 alias(`opus-5`, `fable-5`)에도 걸리므로 `_ALIAS_RULES`에서 계열 규칙보다 앞에 둔다
- xAI Grok: xAI 공개 단가; 세션에 `costUsdTicks`가 있으면 공급자 집계 우선

오버라이드:

```bash
export SESSION_HISTORY_PRICING=~/.config/session-history/pricing.json
# 또는
python3 scripts/token_usage.py --cost --pricing-file ./pricing.json
```

JSON 형식 예:

```json
{
  "models": {
    "gpt-6-astra": {
      "input": 10.0,
      "output": 50.0,
      "cached_input": 1.0,
      "style": "openai"
    }
  }
}
```

Anthropic 스타일은 `cache_write_5m`, `cache_write_1h`, `cache_read` 키를 쓴다.

## 구독 한도 (`--quota`)

| 도구 | 엔드포인트 | 자격 증명 |
|---|---|---|
| Claude | `api.anthropic.com/api/oauth/usage` | `~/.claude/.credentials.json` 또는 Keychain `Claude Code-credentials` |
| Codex | `chatgpt.com/backend-api/wham/usage` | `~/.codex/auth.json` tokens |
| Grok | 미지원 | — |
| 그 외 | 미지원 | — |

토큰 값을 출력하지 않는다. 401/만료면 에러 문구만 남긴다.

## 해석 주의

1. **API 환산 ≠ 청구서**. Max/Pro/SuperGrok 정액 구간 안이면 현금 비용은 플랜 가격이 상한이다.
2. **캐시 hit가 비용을 좌우**한다. Claude는 cache_read/create 비중이 크고, Codex는 cached input 비중이 클 수 있다.
3. Codex reasoning 토큰은 보통 `output_tokens`에 이미 포함된다. 이중 합산하지 않는다.
4. 단가는 공식 list price 스냅샷이다. 프로모션·intro 기간·지역 가산은 표 note를 본다.
5. 모델별 표의 `unpriced`는 단가 미매칭이다. 토큰 합에는 들어가고 비용 합에는 빠진다.

## 관련 파일

- `scripts/token_usage.py` — CLI (토큰+비용 단일 패스 집계)
- `scripts/pricing.py` — 단가·해석·환산
- `scripts/quota.py` — live 한도
- `scripts/adapters/{claude,codex,grok,opencode,aside,openclaw,copilot}.py` — 토큰을 남기는 로그 파서
- `scripts/adapters/{cursor,gemini}.py` — 대화만 있고 토큰은 없는 파서
- `tests/test_pricing.py`, `tests/test_token_cost_integration.py`
