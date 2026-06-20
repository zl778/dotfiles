# Provider-Specific Notes (LLM Stream Benchmark)

Captured from real-world benchmark runs.

## Nous Inference API

- **Endpoint:** `https://inference-api.nousresearch.com/v1/chat/completions`
- **Auth:** OAuth via `~/.hermes/auth.json` → `providers.nous.access_token`
- **Token type:** Bearer, OAuth2 device code flow
- **Known models:** `stepfun/step-3.7-flash:free`

### Streaming behaviour

The first chunk arrives empty on `delta.content` and instead carries:
- `delta.reasoning`: string (first CoT text)
- `delta.reasoning_details[].text`: structured reasoning steps
- TTFT measured on reasoning: ~3614ms with 200 completion_tokens
- Generation speed (reasoning tokens): ~122 tok/s

Visible `delta.content` stays empty for the entire response if the model emits only reasoning. The API still returns the final `usage` in the last stream event.

### Observations

High TTFT (3.6s) is dominated by model internal reasoning preparation, not network. Actual token production is reasonable once started.

## DeepSeek API

- **Endpoint:** `https://api.deepseek.com/v1/chat/completions`
- **Auth:** Environment variable `DEEPSEEK_API_KEY` (in `~/.hermes/.env`)
- **Available models** (from `/v1/models`):
  - `deepseek-v4-flash`: fast flash model
  - `deepseek-v4-pro`: pro tier
- **Model name note:** Use `deepseek-v4-flash`, not `deepseek-chat` or other aliases. The `/v1/models` endpoint is the source of truth.

### Streaming behaviour

Pure content stream — `delta.content` carries everything directly. No `reasoning` or `reasoning_details` fields emitted (for these models). Generation speed observed: ~275 tok/s after TTFT.

### SSL on macOS

Python's `urllib` fails with `SSL: CERTIFICATE_VERIFY_FAILED` when hitting `api.deepseek.com` without `certifi`. Fix:

```python
import ssl
import certifi
ctx = ssl.create_default_context(cafile=certifi.where())
urllib.request.urlopen(req, context=ctx)
```

### Observations

TTFT: ~1461ms with 78 completion_tokens. Low cold-start time compared to Nous. Token generation efficiency is excellent (275 tok/s). TTFT still accounts for ~84% of total latency.

## Credential Source Priority

When benchmarking a new provider, resolve credentials in this order:

1. `--token` CLI flag
2. `~/.hermes/auth.json` → `credential_pool` → any entry with a non-`***` access_token
3. `~/.hermes/auth.json` → `providers.<name>.access_token`
4. `~/.hermes/.env` → key=value parse (skip comment lines, `***` values)
5. `os.environ` fallback
