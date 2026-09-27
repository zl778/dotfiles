---
name: hermes-gateway-telegram
description: Configure Telegram as a Hermes gateway platform — bot creation, token setup, group chat authorization, multi-bot architecture, security hardening, and troubleshooting.
---

# Hermes Gateway: Telegram Setup

Connect Telegram as a full-featured conversational platform for Hermes Agent.

## Quick Start

```bash
# 1. @BotFather → /newbot → get token
# 2. @userinfobot → /start → get your user ID
# 3. Add to ~/.hermes/.env (user must edit or approve):
#      TELEGRAM_BOT_TOKEN=123456789:ABCdef...
#      TELEGRAM_ALLOWED_USERS=8588918249
# 4. Restart gateway
hermes gateway restart
```

## Step-by-Step

### 1. Create Bot

Search **@BotFather** (verified blue checkmark ✅ — fake bots redirect to @Manybot).
Send `/newbot`, choose display name + username ending in `bot`.

### 2. Get Your User ID

Send `/start` to **@userinfobot**.

### 3. Configure Hermes

Add to `~/.hermes/.env`:
```env
TELEGRAM_BOT_TOKEN=123456789:ABCdef...
TELEGRAM_ALLOWED_USERS=8588918249
```

`.env` is protected from agent tool writes — the user must edit it manually or approve terminal commands.

### 4. Private Chat → Test

Message your bot on Telegram. If no response, check:
- `TELEGRAM_ALLOWED_USERS` includes your user ID
- Gateway logs: `grep telegram ~/.hermes/logs/gateway.log | tail -10`

### 5. Group Chat Setup

#### 5a. Disable Privacy Mode

@BotFather → `/mybots` → select bot → **Bot Settings → Group Privacy → Turn off**
Without this, the bot shows "无权读取消息" in the group member list.

#### 5b. Find the Real Group Chat ID

@get_id_bot can give the **wrong** ID (positive vs negative). The definitive way:

```python
import requests
TOKEN = "your_bot_token"

# Try the ID from @get_id_bot
r = requests.get(f"https://api.telegram.org/bot{TOKEN}/getChat",
                 params={"chat_id": 5584761717})
if not r.json().get("ok"):
    print(f"ID 5584761717 is wrong: {r.json()}")
    # Try negative
    r = requests.get(f"https://api.telegram.org/bot{TOKEN}/getChat",
                     params={"chat_id": -5584761717})
    if r.json().get("ok"):
        print(f"Correct ID: {r.json()['result']['id']}")
```

The bot API's `getChat` returning `200` = the bot can see this chat. `400 "chat not found"` = wrong ID.

#### 5c. Configure Group Access

**CRITICAL: Values must be YAML lists, not strings.**
`hermes config set telegram.allowed_chats 5584761717` creates a **string** (`'5584761717'`)
which silently fails. Use Python + PyYAML to write proper lists:

```python
import yaml

with open('/Users/liangzhu/.hermes/config.yaml') as f:
    config = yaml.safe_load(f)

config['telegram']['allowed_chats'] = [-5584761717]
config['telegram']['group_allowed_chats'] = [-5584761717]
config['telegram']['group_allow_from'] = [8588918249]

with open('/Users/liangzhu/.hermes/config.yaml', 'w') as f:
    yaml.dump(config, f, default_flow_style=False,
              allow_unicode=True, sort_keys=False)
```

Then restart: `hermes gateway restart`

Or use env vars (bypass YAML list problem):
```env
TELEGRAM_GROUP_ALLOWED_CHATS=-5584761717
TELEGRAM_GROUP_ALLOWED_USERS=8588918249
```

### 6. Verify Group Messages

Send a message in the group @mentioning the bot. Check gateway logs:

```bash
grep 'inbound.*platform=telegram\|unauthorized\|ignored' ~/.hermes/logs/gateway.log | tail -10
```

Expected: `inbound message: platform=telegram user=... chat=-5584761717 msg='...'`

## Multi-Bot Architecture

Each Hermes profile needs its own Telegram bot token + gateway:

```bash
hermes -p wukong gateway start    # wukong profile with its own bot token
hermes -p windows gateway start   # windows profile
```

Recommended group config:
```yaml
telegram:
  require_mention: true
  exclusive_bot_mentions: true
  mention_patterns: []
```

### Routing Patterns (Step-by-Step Approach)

When running multiple bots in one group, decide the routing pattern explicitly before scaling:

1. **Phase 1 — Manual mention:** Each bot in the group, user @mentions the right one per task. Zero infra needed.
2. **Phase 2 — Orchestrator + SSH delegation:** One bot (e.g. on macOS, always-on) plays orchestrator. Subordinate bots on other machines (e.g. Windows) run SSH-able. Orchestrator decides task → SSH to subordinate's machine → runs `hermes chat -q '...'` → returns result to group.
3. **Phase 3 — Kanban board:** Shared SQLite board, dispatcher polls, true async workers. Heavier setup; benefits are durable task tracking, audit log, retries.

**Why start at Phase 1:**
- Setup cost = ~10 minutes per new bot (create @BotFather bot, add allowed_chats, restart gateway)
- No shared infra required
- You actually learn the workload split before automating it
- Automation in Phase 2/3 without Phase 1 experience usually encodes wrong assumptions into the wrong layer

**When to skip to Phase 2:**
- One machine is intermittently offline (e.g. laptop goes to sleep) and you want the orchestrator to keep the workforce stable
- Tasks routinely involve running software that only exists on the subordinate machine (e.g. Windows-only executables, WSL-only tooling)
- You want a single "always-available" number for clients/colleagues to message

**When Phase 3 is worth it:**
- Tasks take minutes to hours and you'd lose track of them in chat scrollback
- You want retries, status dashboards, audit history
- The roster grows beyond 2–3 workers

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| No response in DM | ALLOWED_USERS not set | Add user ID to .env, restart |
| "无权读取消息" in group | Privacy mode ON | Disable in BotFather |
| Privacy OFF but no group response | Group chat ID wrong OR not a YAML list | Verify with `getChat` API; use PyYAML to write lists |
| `hermes config set` creates string | CLI limitation | Use `python3 -c` with PyYAML instead |
| Bot joins group but never receives messages | Bot was removed/re-added; gateway needs restart | `hermes gateway restart` |
| Concurrent polling error | Same token in two gateways | Create separate bots per profile |

## Pitfalls

- **Fake BotFather** — only the verified (blue checkmark) @BotFather is real
- **Group IDs from third-party bots can be wrong** — always verify with `getChat` Bot API
- **`hermes config set` writes YAML strings, not lists** — use PyYAML workaround or env vars
- **`.env` is protected** — user must manually edit or approve terminal writes
- **Gateway restart is required after any config change** — `hermes gateway restart`

## Related

- `hermes-agent` skill for general CLI reference
- Hermes Telegram docs: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/telegram