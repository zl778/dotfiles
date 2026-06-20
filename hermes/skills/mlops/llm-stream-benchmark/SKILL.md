---
name: llm-stream-benchmark
description: >
  Benchmark streaming LLM inference performance — TTFT, total latency, and throughput.
  Use when asked to measure first-token time, generation speed, or streaming latency;
  when comparing providers/models; or when diagnosing why a chat UI feels slow.
version: 0.2.0
---

# LLM Stream Benchmark

Class-level skill for measuring latency and throughput of OpenAI-compatible streaming chat completions.

## Trigger

Activate when the user asks to:
- test TTFT / total latency / throughput
- measure streaming performance of a model/provider
- diagnose slow first-token or slow generation
- compare models on speed metrics

## Preferred Tool

Use the built-in `scripts/measure_stream.py` script. It issues a single OpenAI Chat Completions SSE request, measures TTFT from request start to first non-empty delta event, and reports latency plus throughput.

If running a one-off custom request, follow the same timing pattern as the script:
1. Record `start` immediately before `urllib.request.urlopen`.
2. Stream with `for raw_line in resp:` to preserve natural chunk arrival.
3. Treat the first non-empty `delta.content`, `delta.reasoning`, or `delta.reasoning_details[*].text` as the first-token event for TTFT.
4. Prefer API-provided `usage.prompt_tokens` / `usage.completion_tokens` over manual estimation.
5. TTFT share is `ttft_ms / latency_ms * 100`.

## Configuration Defaults

- Auth source: `~/.hermes/auth.json` (Hermes stored OAuth/API keys).
- Base URL fallback: check provider entry in Hermes config (`config.yaml` model.base_url`) and the provider's `inference_base_url` in auth.json.
- Model selection: honor user-specified model if provided; otherwise use current Hermes default.

## Pitfalls

- Some providers put the first token(s) in `delta.reasoning` or `delta.reasoning_details[*].text` instead of `delta.content`. Do not mark TTFT on `content` only. Measure on first non-empty delta of any type (content, reasoning, or reasoning_details text).
- Some providers omit `stream_options.include_usage` support. If `completion_tokens` is missing, fall back to estimating tokens from visible/reasoning character counts.
- **macOS SSL cert issue:** Python's urllib may fail with `SSL: CERTIFICATE_VERIFY_FAILED: self-signed certificate in certificate chain` against certain providers (observed on DeepSeek API). Fix: `pip install certifi` then pass `ssl.create_default_context(cafile=certifi.where())` to `urllib.request.urlopen`.
- Measurement includes HTTP+TLS handshake and routing. Repeat twice; report median if variance is high. When possible, reuse the same prompt, max_tokens, and temperature for fair cross-model comparisons.
- Do not benchmark through the Hermes gateway unless explicitly requested — measure the provider endpoint directly.
- **Compare apples to apples:** same user prompt, same max_tokens cap, same temperature (0 is recommended). One model may produce 30 tokens on a short-prompt query while another produces 200 — token rates are only comparable when completion_tokens is similar.

## Credential Resolution Strategy

The script resolves API keys in this order:

1. `--token` / `--api-key` CLI arg (if available)
2. `~/.hermes/auth.json` → credential_pool → matching provider entry
3. `~/.hermes/auth.json` → `providers.<name>.access_token`
4. `~/.hermes/.env` → `DEEPSEEK_API_KEY`, `OPENROUTER_API_KEY`, etc., parsed by reading the file directly (not via os.environ, which may not have `.env` sourced)
5. `os.environ` fallback for env vars exported before the session

When benchmarking Hermes-configured providers, prefer reading from `auth.json` credential_pool first — it's the canonical source.

## Results Persistence (Obsidian)

After collecting benchmark results, save them to the user's Obsidian PKM vault for trend tracking:

**Vault path:**
`/Users/liangzhu/Library/Mobile Documents/iCloud~md~obsidian/Documents/PKM/pages/`

**File structure:** Single report note per provider class (e.g. "DeepSeek 流式推理 API 性能报告.md") with a `## 时序趋势跟踪` table:

```
| 时间 | 模型 | TTFT | 总延迟 | prompt_tokens | completion_tokens | 首 token 后速度 (tok/s) | 整段速度 (tok/s) | 备注 |
|---|---|---|---|---|---|---|---|---|---|
| 2026-06-01 21:09 | deepseek-v4-flash | 1461.56 ms | 1745.05 ms | 18 | 78 | 275.14 | 44.70 | 正常 content 流 |
```

Append new rows for each measurement session rather than overwriting. Keep a `对比` section when comparing providers side by side.

## Provider-Specific Notes

| Provider | Endpoint | Content deltas | Known quirks |
|---|---|---|---|
| **Nous** (inference-api.nousresearch.com) | `/v1/chat/completions` | reasoning→content | First chunk arrives in `delta.reasoning` and `delta.reasoning_details[].text`. `delta.content` is empty until reasoning finishes. TTFT measured on reasoning is ~3614ms for stepfun/step-3.7-flash. |
| **DeepSeek** (api.deepseek.com) | `/v1/chat/completions` | content (direct) | Pure content stream, no reasoning field. Model names: deepseek-v4-flash, deepseek-v4-pro (not deepseek-chat). Requires `certifi` for SSL on macOS. Token generation speed ~275 tok/s on v4-flash. |

When the first-observed model switches between session notes (e.g. from Nous to DeepSeek), append a new provider section to the same report file for easier comparison.

## Support Files

- `references/provider-notes.md` — provider-specific quirks from benchmarks.
- `references/throughput-benchmark-chinese.md` — Chinese-language guide for throughput benchmarking with standard flow, pitfalls, and output format.
- `scripts/measure_stream.py` — reusable streaming benchmark script.
