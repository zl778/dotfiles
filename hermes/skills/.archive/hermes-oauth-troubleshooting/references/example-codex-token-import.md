# Example: Codex Token Import for wukong Profile

## Session Transcript (2026-06-22)

### Error

wukong profile failed with:

```
⚠️ API call failed (attempt 1/3): AuthenticationError [HTTP 401]
Provider: openai-codex Model: gpt-5.4-mini
Endpoint: https://chatgpt.com/backend-api/codex
Error: HTTP 401: Could not parse your authentication token.
💡 Codex OAuth token was rejected (HTTP 401). Your token may have
   been refreshed by another client (Codex CLI, VS Code).
```

### Diagnosis

1. `codex doctor` → websocket connected OK (codex itself had valid tokens)
2. Compared `last_refresh`:
   - `~/.codex/auth.json`: 2026-06-19 (fresh)
   - `~/.hermes/profiles/wukong/auth.json`: 2026-06-09 (stale)
3. `hermes auth list openai-codex --profile wukong`
   → `last_status: "exhausted"`, `last_error_code: 401`

### Fix Applied

1. Reset exhaustion:
   ```bash
   hermes auth reset openai-codex --profile wukong
   ```

2. Copied tokens from `~/.codex/auth.json` into
   `~/.hermes/profiles/wukong/auth.json`:
   - `providers.openai-codex.tokens.access_token`
   - `providers.openai-codex.tokens.refresh_token`
   - `providers.openai-codex.last_refresh`
   - `credential_pool.openai-codex[0].access_token`
   - `credential_pool.openai-codex[0].refresh_token`
   - `credential_pool.openai-codex[0].last_refresh`
   - Cleared all `last_status`, `last_error_*` fields

3. Verified: auth.json showed `last_status: None`, `last_error_code: None`,
   `last_refresh: 2026-06-19T02:22:56`

### Key Insight

The `.codex/auth.json` had newer tokens because VS Code triggered a
token refresh when the user used Codex in the editor. This invalidated
the old token stored in wukong's profile. The direct import approach
avoids re-running the full OAuth flow.
