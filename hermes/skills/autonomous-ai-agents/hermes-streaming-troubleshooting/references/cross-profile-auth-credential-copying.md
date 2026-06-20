# Cross-Profile Auth Credential Copying

When creating a Hermes profile that uses an OAuth-based provider (like `openai-codex`), the profile needs its own copy of the auth credentials. The standard `hermes auth add openai-codex` flow goes to the global `~/.hermes/auth.json`, not to a specific profile.

## Pattern: Copy Provider Credentials from Global to Profile

### When to Use

When a profile needs an OAuth provider that's already authenticated in the global `~/.hermes/auth.json`, but the standard `hermes -p <profile> auth add <provider>` flow doesn't work (e.g., Cloudflare blocking the device code page for openai-codex).

### Steps

#### 1. Verify global auth has the credential

```bash
hermes auth status <provider>          # global check
cat ~/.hermes/auth.json | python3 -c "
import json,sys
d = json.load(sys.stdin)
print(<provider> in d.get('providers',{}))
"
```

#### 2. Check if profile has its own auth.json

```bash
ls ~/.hermes/profiles/<name>/auth.json
```

If it exists, check if the credential is already there:

```bash
cat ~/.hermes/profiles/<name>/auth.json | python3 -c "
import json,sys
d = json.load(sys.stdin)
print(<provider> in d.get('providers',{}))
"
```

#### 3. Copy the credential

Read both auth files, copy the provider block (from `providers.<name>`) and the credential pool entry (from `credential_pool.<name>`) into the profile's auth.json:

```python
import json

# Read global
global_path = '/Users/liangzhu/.hermes/auth.json'
with open(global_path) as f:
    global_auth = json.load(f)

# Extract credential
cred = global_auth['providers']['<provider>']
pool_cred = global_auth['credential_pool']['<provider>']

# Read profile
profile_path = '/Users/liangzhu/.hermes/profiles/<name>/auth.json'
with open(profile_path) as f:
    profile_auth = json.load(f)

# Copy to both places
if 'providers' not in profile_auth:
    profile_auth['providers'] = {}
if 'credential_pool' not in profile_auth:
    profile_auth['credential_pool'] = {}

profile_auth['providers']['<provider>'] = cred
profile_auth['credential_pool']['<provider>'] = pool_cred

with open(profile_path, 'w') as f:
    json.dump(profile_auth, f, indent=2, ensure_ascii=False)
```

#### 4. Verify

```bash
hermes -p <name> auth status <provider>
# Should say "logged in"
```

#### 5. Switch provider in profile config

```bash
hermes -p <name> config set model.provider <provider>
hermes -p <name> config set model.default <model>
```

Or patch the config.yaml directly:

```bash
# Change from:
# model:
#   default: deepseek-v4-flash
#   provider: deepseek
#   base_url: https://api.deepseek.com/v1
#
# To:
# model:
#   default: o4-mini
#   provider: openai-codex
```

#### 6. Create wrapper alias (optional)

```bash
hermes profile alias <name>
# Creates ~/.local/bin/<name> -> hermes -p <name>
```

## Why This Works

Hermes profiles are self-contained: each profile has its own `config.yaml`, `auth.json`, `sessions/`, `memories/`, `skills/`, etc. The `hermes -p <name>` flag switches the `$HERMES_HOME` to the profile directory. So the OAuth credential must live inside the profile's `auth.json`, not in the global one.

The `providers.<name>` section holds the active credential metadata; the `credential_pool.<name>` section holds the pool rotation strategy. Both need to be populated for the auth system to work correctly.

## Caveats

- **Refresh token isolation**: The global and profile copies are independent. If one side refreshes its tokens, the other side's tokens become stale. Re-import if one side gets 401s.
- **No auto-propagation**: There is no mechanism to sync credentials across profiles. Manual import is the only way.
