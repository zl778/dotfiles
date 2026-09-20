---
name: hermes-streaming-troubleshooting
description: "Diagnose and resolve Hermes streaming interruptions — partial-stream-stub, finish_reason='length' network errors, continuation retries, and provider-specific mitigations."
version: 1.0.0
author: agent
---

# Hermes Streaming Troubleshooting

Diagnose the "Stream interrupted by network error (finish_reason='length' on partial-stream-stub)" message and related streaming failures.

## What the Error Means

```
⚠️  Stream interrupted by network error (finish_reason='length' on partial-stream-stub)
```

**This is a recovery notification, not a fatal error.** Hermes caught a network drop mid-stream, created a stub response tagged `partial-stream-stub`, and will automatically retry.

### Internal Mechanism

Hermes code in `agent/chat_completion_helpers.py` and `agent/conversation_loop.py`:

1. The streaming connection to the LLM provider drops mid-flight (exception or clean end without finish_reason)
2. If deltas were already delivered to the platform, Hermes does NOT re-raise — instead it builds a partial response stub with:
   - `id = "partial-stream-stub"` (constant from `hermes_constants.PARTIAL_STREAM_STUB_ID`)
   - `finish_reason = "length"` (so the continuation machinery fires)
   - `tool_calls = None` (prevents auto-execution of incomplete tool calls)
   - `_dropped_tool_names` metadata if tool calls were being streamed
3. The conversation loop detects `id == "partial-stream-stub"` and:
   - Shows the warning "Stream interrupted by network error"
   - Automatically retries up to **3 times** with a continuation prompt
   - For text-only drops: asks model to continue where it left off
   - For mid-tool-call drops: asks model to break content into smaller chunks
4. If all 3 retries fail: returns partial response with `"Response remained truncated after 3 continuation attempts"`

The stub mechanism was introduced to fix issue #30963 — without it, a network drop mid-stream would end the turn immediately with no continuation, leaving the agent stuck.

### Key Distinction

| Condition | Response ID | Message Shown |
|-----------|-------------|---------------|
| Network drop mid-stream (partial data sent) | `partial-stream-stub` | "Stream interrupted by network error" |
| Genuine output-length cap (model hit max_tokens) | `stream-<uuid>` | "Response truncated (finish_reason='length')" |
| Thinking budget exhausted | `stream-<uuid>` | "Reasoning exhausted the output token budget" |

## Common Root Causes

### 1. Proxy / VPN Interruption (most common behind a proxy)

Streaming SSE (Server-Sent Events) connections are long-lived HTTP connections. Proxies often:
- Time out idle connections mid-stream
- Drop connections during protocol switch
- Interfere with chunked transfer encoding

**Fix:** Add the provider's API endpoint to direct-connect rules in your proxy tool.

For Clash Verge:
```
DOMAIN-SUFFIX,api.deepseek.com,DIRECT
DOMAIN-SUFFIX,deepseek.com,DIRECT
DOMAIN-SUFFIX,nousresearch.com,DIRECT  # if routing through Nous Portal
```

### 2. Provider-Side Instability

Some providers have less reliable streaming than others:
- **DeepSeek**: streaming connections drop more frequently during long responses
- **OpenAI / Codex**: generally more stable streaming
- **Local models** (llama.cpp, etc.): depends on hardware/network

**Fix:** Switch to a more stable provider or create a dedicated profile.

### 3. Tool Call Arguments Too Large

When the model writes large files or generates huge amounts of code in a single tool call, the JSON arguments may be too large for the stream to complete before the connection drops.

**Fix:** The continuation prompt already asks the model to break large content into smaller chunks. If it persists:
- Manually instruct the model to use multiple patch/write calls instead of one giant one
- Increase `max_tokens` so the model has room

### 4. Insufficient max_tokens

If the model consistently hits its output cap mid-thought, the continuation retries may all fail.

**Fix:**
```bash
hermes config set model.max_tokens 16384
```

### 5. Reasoning Budget Exhaustion (reasoning models)

Models with reasoning/thinking (DeepSeek V4 Flash, o-series, Claude Sonnet) may spend all output tokens on reasoning with none left for the actual response.

**Fix:** Lower reasoning effort:
- In-session: `/reasoning low` or `/thinkon low`
- Or switch to a non-reasoning model

### 6. ⚠️ Model Version Upgrade Misconception

A common mistaken assumption: "If I switch from the Flash version to the Pro version (e.g., DeepSeek V4 Flash → DeepSeek V4 Pro), the streaming will be more stable."

**This does NOT fix the problem.** Both model versions:
- Use the **same API endpoint** (same URL, same network path)
- Run on the **same provider infrastructure**
- Travel through the **same proxy/VPN rules**

In fact, Pro models often make things **worse**:
- Pro generates **longer responses** (more thinking tokens, more detailed output)
- The stream stays open **longer**, increasing the window for network jitter
- More thinking tokens mean more chance of hitting `finish_reason='length'` from the provider side

The root cause is the **network/proxy path** between Hermes and the API endpoint — not the model version on the other end. Fix the connection, not the model.

**Correct approach:**
- Fix proxy rules (direct connect for the provider domain)
- Switch to a provider with more stable streaming (e.g., OpenAI Codex)
- Use a dedicated profile with a stable provider (see Strategy B)
- Increase max_tokens to reduce truncation pressure

## Prevention Strategies

### Strategy A: Increase max_tokens

Gives the model more room before hitting the output cap:
```bash
hermes config set model.max_tokens 16384
```

### Strategy B: Dedicated Profile with Stable Provider

Create a separate Hermes profile using a provider with more reliable streaming (e.g., OpenAI Codex):

```bash
# Create profile
hermes profile create wukong

# Switch provider
hermes -p wukong config set model.provider openai-codex
hermes -p wukong config set model.default o4-mini

# Copy auth credentials (if using OAuth like openai-codex)
# Read global ~/.hermes/auth.json, copy the provider's credential block
# into the profile's ~/.hermes/profiles/<name>/auth.json
# under both `providers.<name>` and `credential_pool.<name>`

# Set up alias (optional)
hermes profile alias wukong
# → creates ~/.local/bin/wukong as a wrapper script
```

Then use the alias directly:
```bash
wukong chat -q "Your query here"
```

### Strategy C: Lower Reasoning Effort

For reasoning models (DeepSeek V4 Flash, o-series):
```
/reasoning low
```

### Strategy D: Switch Provider Mid-Session

```bash
hermes model
# Interactive picker
```

## Verification

After applying a fix, verify the streaming connection is stable:
```bash
hermes doctor
hermes config check
```

---

## Linked References

- `references/partial-stream-stub-source-analysis.md` — Full source-level flow: where the stub is built (`chat_completion_helpers.py`), where it's handled (`conversation_loop.py`), test suite, and constants.
- `references/cross-profile-auth-credential-copying.md` — How to copy OAuth credentials from global `auth.json` to a profile's `auth.json`, enabling separate profiles with different providers.
