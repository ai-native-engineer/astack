# 비용·쿼터 측정 (token_usage)

로컬 세션 로그로 **토큰 실사용**과 **API 환산 비용**, 선택적으로 **구독 한도(live)** 를 본다. 구독 청구서가 아니라 같은 사용량을 list API 단가로 환산한 대체비용이다.

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

Claude `usage.cache_creation.ephemeral_5m_input_tokens` / `ephemeral_1h_input_tokens`가 있으면 각각 5m·1h write 단가로 잡는다. split이 없고 total만 있으면 5m 단가로 합산(1h 비중을 과소평가할 수 있음).

## 모델 해석 정책

정본: `scripts/pricing.py`의 `resolve_model_key` / `is_non_model_id`.

| 입력 | 결과 | 비용 출처 |
|---|---|---|
| 빈 모델, 또는 provider/synthetic placeholder (`openai`, `codex`, `<synthetic>` 등) | 도구 기본 모델 | `default` (Codex→`gpt-5.6-sol`, Claude→`claude-opus-5`, Grok→`grok-4.5`) |
| 표에 있는 id / alias / safe prefix | 해당 단가 | `rate_card` (Grok ticks 있으면 `provider_ticks`) |
| **실모델 id인데 표에 없음** | unpriced | 합계 **미포함**, `missing_models`에 이름·event 수 표시 |

미매칭 실모델을 플래그십 단가로 조용히 채우지 않는다. 단가를 넣으려면 `DEFAULT_RATES`를 고치거나 `--pricing-file`을 쓴다.

Codex는 `thread_settings.model`만 모델로 쓴다. `model_provider` 필드는 무시한다. 모델이 비어 있으면 도구 기본 단가(default)로 환산한다.

## 단가표

정본 코드: `scripts/pricing.py`의 `DEFAULT_RATES` (USD / MTok 스냅샷).

가격 출처(유지보수 시 대조):

- OpenAI GPT-5.6 Sol/Terra/Luna, Codex 계열: OpenAI API / GPT-5.6 pricing 공지
- Anthropic Opus/Sonnet/Haiku 및 Fable 5 (`claude-fable-5`, $10/$50): Anthropic list price
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
    "gpt-5.6-sol": {
      "input": 5.0,
      "output": 30.0,
      "cached_input": 0.5,
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
- `scripts/adapters/{claude,codex,grok}.py` — 로그 파서
- `tests/test_pricing.py`, `tests/test_token_cost_integration.py`
