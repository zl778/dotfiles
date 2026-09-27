# Codex openai-codex Provider Auth Workaround

## Problem

`hermes auth add openai-codex` runs a device code OAuth flow that asks the user to
open `https://auth.openai.com/codex/device` in their browser. This URL is behind
Cloudflare with a JS challenge (`Ray ID` header). The page redirects to a full
OAuth authorize page with no device-code input field, showing only a Cloudflare
"请稍候… / 正在进行安全验证" screen. The CLI waits 15 minutes then times out.

## Root Cause

Cloudflare challenges `auth.openai.com` for browser traffic. The device code
input form never renders. The backend API endpoints (`/api/accounts/deviceauth/*`)
work fine — the problem is only the user-facing verification page.

## Prerequisites

- Codex CLI installed (`npm install -g @openai/codex`)
- Codex CLI has working ChatGPT Plus OAuth in `~/.codex/auth.json`
  (`"auth_mode": "chatgpt"` with valid tokens)
- Hermes installed and configured

## Workaround: Manual Token Import

If the user already has Codex CLI authenticated with ChatGPT, import those
tokens into Hermes' auth store:

### Step 1: Read Codex auth

```python
import json, os

# Read existing Codex CLI auth
codex_auth_path = os.path.expanduser("~/.codex/auth.json")
with open(codex_auth_path) as f:
    codex_auth = json.load(f)

tokens = codex_auth["tokens"]
```

### Step 2: Read and update Hermes auth

```python
import datetime

hermes_auth_path = os.path.expanduser("~/.hermes/auth.json")
with open(hermes_auth_path) as f:
    hermes_auth = json.load(f)

now = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

# Add or update provider section
if "providers" not in hermes_auth:
    hermes_auth["providers"] = {}

hermes_auth["providers"]["openai-codex"] = {
    "tokens": {
        "access_token": tokens["access_token"],
        "refresh_token": tokens["refresh_token"]
    },
    "last_refresh": now
}

# Add credential pool entry
if "credential_pool" not in hermes_auth:
    hermes_auth["credential_pool"] = {}

if "openai-codex" not in hermes_auth["credential_pool"]:
    hermes_auth["credential_pool"]["openai-codex"] = []

hermes_auth["credential_pool"]["openai-codex"] = [
    {
        "id": "imported_codex",
        "label": "Codex CLI imported",
        "auth_type": "oauth_device_code",
        "access_token": tokens["access_token"],
        "refresh_token": tokens["refresh_token"],
        "source": "device_code",
        "priority": 0,
        "last_status": "ok",
        "last_status_at": now
    }
]

with open(hermes_auth_path, "w") as f:
    json.dump(hermes_auth, f, indent=2, ensure_ascii=False)

print("Done — Codex tokens imported into Hermes auth store.")
```

### Step 3: Verify

```bash
hermes auth list openai-codex    # → shows "1 credential"
hermes auth status openai-codex  # → shows "logged in"
```

### Step 4: Use the provider

```bash
# Interactive model picker
hermes model

# Or direct config
hermes config set model.provider openai-codex
```

## Caveats

- **Refresh token rotation**: Hermes maintains its OWN OAuth session separate
  from Codex CLI (`~/.codex/auth.json`). The Codex CLI stated that "Hermes
  maintains its own Codex OAuth session separate from the Codex CLI and VS
  Code extension. This prevents refresh token rotation conflicts where one
  app's refresh invalidates the other's session." The manual import bypasses
  this separation. If either side gets a 401 (`token_invalidated`), re-import.
- **No expiry detection**: The manual import does not check token expiry.
  Closed-source `access_token` JWTs don't carry standard `exp` claims.
  If Hermes starts getting 401s, the refresh flow in `auth.py` should handle
  it (`refresh_codex_oauth_pure`), but this has not been tested with imported
  tokens.
- **OpenAI may change the auth flow**: The `codex_cli_simplified_flow=true`
  parameter in the redirect URL suggests OpenAI is iterating on the device
  code flow. If the URL changes or a new flow is required, this workaround
  may stop working.
