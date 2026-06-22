---
name: hermes-oauth-troubleshooting
description: "Diagnose, reset, and re-import OAuth tokens for Hermes providers (openai-codex, nous, xai-oauth, qwen-oauth). Covers credential exhaustion, token refresh conflicts, and cross-profile token management."
version: 1.0.0
---

# Hermes OAuth Troubleshooting

Diagnose and fix OAuth token issues across Hermes providers, particularly
when tokens are invalidated by other clients that share the same OAuth
session (e.g. Codex CLI and VS Code both refreshing the ChatGPT token,
wukong profile using stale Codex tokens).

**OAuth providers in Hermes:** openai-codex, nous (Portal), xai-oauth,
qwen-oauth — all rely on stored access/refresh tokens that can expire
or get invalidated by concurrent logins.

## Triggers (load this skill when user reports)

- `HTTP 401: Could not parse your authentication token`
- `Non-retryable client error (HTTP 401). Aborting.`
- `Authentication failed` for an OAuth provider
- A profile-specific session fails while the main profile works
- `last_status: "exhausted"` shown in `hermes auth list`

## Diagnosis

### 1. Check auth status

```bash
hermes auth status <provider> --profile <name>
```

Returns 'logged in' even if token is stale — this only checks whether
auth is configured, not whether the token is currently valid.

### 2. Check credential pool exhaustion

```bash
hermes auth list <provider> --profile <name>
# or check directly:
python3 -c "import json; d=json.load(open('~/.hermes/profiles/<profile>/auth.json')); c=d['credential_pool']['<provider>'][0]; print('status:', c.get('last_status'), '| error:', c.get('last_error_code'))"
```

A credential with `last_status: "exhausted"` and `last_error_code: 401`
means the provider tried the token and the server rejected it.

### 3. Check token age vs other clients

Compare `last_refresh` timestamps between:
- `~/.hermes/profiles/<profile>/auth.json` → `providers.<provider>.last_refresh`
- The relevant client's auth file (e.g. `~/.codex/auth.json` → `last_refresh`)

If the other client has a **newer** timestamp, the token was refreshed
by that client, invalidating the old token stored in Hermes.

## Fix Procedures

### Fix: Codex (openai-codex) token expired

When another Codex client (VS Code, Codex CLI) refreshed the ChatGPT
token, Hermes' stored old token is rejected.

**Approach A — Interactive OAuth re-login (slow, opens browser):**

```bash
hermes auth add openai-codex --profile <name>
```

This opens a browser-based ChatGPT OAuth flow. Works reliably but takes
30+ seconds and requires a browser.

**Approach B — Direct token import from codex (fast, non-interactive):**

This is the preferred approach when:
- Codex CLI is installed and has valid tokens (`codex doctor` shows `✓ auth`)
- The user is in a terminal without a browser available

```python
import json
from datetime import datetime, timezone

codex_file = '/Users/liangzhu/.codex/auth.json'
hermes_file = '/Users/liangzhu/.hermes/profiles/<profile>/auth.json'

with open(codex_file) as f:
    codex_auth = json.load(f)

with open(hermes_file) as f:
    hermes_auth = json.load(f)

# Update provider tokens
provider = hermes_auth['providers']['openai-codex']
provider['tokens']['access_token'] = codex_auth['tokens']['access_token']
provider['tokens']['refresh_token'] = codex_auth['tokens']['refresh_token']
provider['last_refresh'] = codex_auth['last_refresh']

# Update credential pool entry
cred = hermes_auth['credential_pool']['openai-codex'][0]
cred['access_token'] = codex_auth['tokens']['access_token']
cred['refresh_token'] = codex_auth['tokens']['refresh_token']
cred['last_refresh'] = codex_auth['last_refresh']
cred['last_status'] = None
cred['last_status_at'] = None
cred['last_error_code'] = None
cred['last_error_reason'] = None
cred['last_error_message'] = None
cred['last_error_reset_at'] = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')

with open(hermes_file, 'w') as f:
    json.dump(hermes_auth, f, indent=2)
```

**Step 1 — Reset exhaustion before import:**

```bash
hermes auth reset openai-codex --profile <name>
```

This clears the `last_status: "exhausted"` marker so the new token isn't
skipped by the credential pool's backoff logic.

### Fix: Nous Portal token expired

```bash
hermes auth add nous --profile <name>
```

This triggers a device-code OAuth flow. Follow the printed URL and enter
the given code.

### Fix: xAI (xai-oauth) token expired

```bash
hermes auth add xai-oauth --profile <name>
```

Triggers a loopback PKCE flow that opens the browser.

### Fix: Qwen OAuth token expired

```bash
hermes auth add qwen-oauth --profile <name>
```

Triggers a browser-based OAuth flow.

## Pitfalls

- **`hermes auth status <provider>` shows 'logged in' even with stale tokens.**
  This only confirms auth is configured, not that the token is valid.
  Always check `hermes auth list` for exhaustion markers.
- **`hermes auth add <provider>` is interactive.** It opens a browser
  (or prints a URL for device-code flows). In non-interactive terminal
  sessions (cron, background scripts), use the direct-token-import approach.
- **Direct JSON editing bypasses Hermes' internal auth refresh logic.**
  Only do this as a fast workaround. The token will need the normal
  OAuth refresh eventually.
- **Multiple profiles using the same OAuth provider compete for the same
  refresh token.** Only the last client to refresh keeps a valid token.
  If you frequently switch between profiles, you'll need to re-import
  the token each time.
- **`.codex/auth.json` may also have stale tokens.** Always verify with
  `codex doctor` before importing. If `codex doctor` shows `✓ websocket`
  then the token is valid. If it shows a websocket error, run `codex`
  interactively to re-authenticate first.

## Verification

After applying the fix, verify the credential is no longer exhausted:

```bash
python3 -c "import json; d=json.load(open('~/.hermes/profiles/<profile>/auth.json')); c=d['credential_pool']['<provider>'][0]; print('OK' if c.get('last_status') is None else c['last_status'])"
```

Then start a new session with the profile:

```bash
hermes chat -p <profile> -q 'hello' --quiet
```

If it returns a response without a 401 error, the fix worked.
