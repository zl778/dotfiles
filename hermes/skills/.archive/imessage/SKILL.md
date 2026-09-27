---
name: imessage
description: Send and receive iMessages/SMS via the imsg CLI on macOS.
version: 1.3.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [iMessage, SMS, messaging, macOS, Apple]
prerequisites:
  commands: [imsg]
---

# iMessage

Two approaches for iMessage on macOS with Hermes:

| Approach | Best for |
|----------|----------|
| **imsg CLI** (Approach A) | One-off sends, reading history, terminal-only, no gateway needed |
| **BlueBubbles Gateway** (Approach B) | Full bidirectional integration, webhook-driven, media/reactions/typing, always-on server |

## Approach A: imsg CLI (轻量单次收发)

Use `imsg` to read and send iMessage/SMS via macOS Messages.app from the terminal.

### Prerequisites

- **macOS** with Messages.app signed in
- Install: `brew install steipete/tap/imsg`
- Grant Full Disk Access for terminal (System Settings → Privacy → Full Disk Access)
- Grant Automation permission for Messages.app when prompted

### When to Use

- User asks to send a specific iMessage or text message
- Reading iMessage conversation history
- Checking recent Messages.app chats
- Sending to phone numbers or Apple IDs

### When NOT to Use

- Telegram/Discord/Slack/WhatsApp messages → use the appropriate gateway channel
- Group chat management (adding/removing members) → not supported
- Bulk/mass messaging → always confirm with user first

## Quick Reference

### List Chats

```bash
imsg chats --limit 10 --json
```

### View History

```bash
# By chat ID
imsg history --chat-id 1 --limit 20 --json

# With attachments info
imsg history --chat-id 1 --limit 20 --attachments --json
```

### Send Messages

```bash
# Text only
imsg send --to "+14155551212" --text "Hello!"

# With attachment
imsg send --to "+14155551212" --text "Check this out" --file /path/to/image.jpg

# Force iMessage or SMS
imsg send --to "+14155551212" --text "Hi" --service imessage
imsg send --to "+14155551212" --text "Hi" --service sms
```

### AppleScript fallback when `imsg` is unavailable

If `imsg` is not installed or cannot be installed quickly, and the user has explicitly confirmed the recipient and message content, use Messages.app directly:

```bash
osascript -e '
tell application "Messages"
    set targetService to 1st service whose service type = iMessage
    set targetBuddy to buddy "+14155551212" of targetService
    send "Hello!" to targetBuddy
end tell
'
```

Notes:
- This may trigger macOS Automation permission prompts the first time.
- Use the exact recipient the user confirmed (phone number or Apple ID).
- If iMessage service lookup fails, ask whether to use SMS or another delivery method.

### Watch for New Messages

```bash
imsg watch --chat-id 1 --attachments
```


## Resources

- `references/telegram-vs-bluebubbles.md` — 平台选择指南
- `references/bluebubbles-api-endpoints.md` — BlueBubbles REST API 端点速查表，用于调试消息收发和查询聊天记录

## Service Options

- `--service imessage` — Force iMessage (requires recipient has iMessage)
- `--service sms` — Force SMS (green bubble)
- `--service auto` — Let Messages.app decide (default)

## Rules

1. **Always confirm recipient and message content** before sending
2. **Never send to unknown numbers** without explicit user approval
3. **Verify file paths** exist before attaching
4. **Don't spam** — rate-limit yourself

## Example Workflow

User: "Text mom that I'll be late"

```bash
# 1. Find mom's chat
imsg chats --limit 20 --json | jq '.[] | select(.displayName | contains("Mom"))'

# 2. Confirm with user: "Found Mom at +1555123456. Send 'I'll be late' via iMessage?"

# 3. Send after confirmation
imsg send --to "+1555123456" --text "I'll be late"
```

## Approach B: BlueBubbles Gateway (全双向集成)

[BlueBubbles](https://bluebubbles.app) is a free, open-source macOS server that bridges iMessage to any device via REST API + webhooks. Hermes connects to it as a gateway platform, enabling full two-way iMessage with media, reactions, typing indicators, and read receipts.

### When to Use
- User wants Hermes to **receive and respond** to iMessages automatically (not just send)
- Need rich features: images, voice messages, videos, documents, tapback reactions
- Need typing indicators and read receipts
- Running an always-on Hermes gateway

### Installation

Download the latest arm64 DMG from GitHub:
```bash
# Find latest version first, then download arm64 DMG
curl -sL https://api.github.com/repos/BlueBubblesApp/bluebubbles-server/releases/latest | jq -r '.assets[] | select(.name | endswith("arm64.dmg")) | .browser_download_url'
curl -L -o /tmp/BlueBubbles-arm64.dmg <DOWNLOAD_URL>
```

**Install with ditto** (preferred over `rm -rf + cp -R` — avoids macOS `.app` merge issues):
```bash
# Mount
hdiutil attach /tmp/BlueBubbles-arm64.dmg -nobrowse

# Install (ditto replaces .app bundles correctly)
ditto /Volumes/BlueBubbles*/BlueBubbles.app /Applications/BlueBubbles.app

# Cleanup
hdiutil detach /Volumes/BlueBubbles*
rm /tmp/BlueBubbles-arm64.dmg
```

### Initial Setup (GUI — manual step)
1. Sign into **Messages.app** with your Apple ID
2. Launch **BlueBubbles.app** — complete the setup wizard
3. Go to **Settings → API** and note:
   - **Server URL** (default `http://127.0.0.1:1234`)
   - **Server Password**

### Uninstalling BlueBubbles

To fully remove BlueBubbles and its Hermes configuration:

1. **Revoke pairing:** Delete the pairing files:
   ```bash
   rm -f ~/.hermes/pairing/bluebubbles-approved.json ~/.hermes/pairing/bluebubbles-pending.json
   ```

2. **Remove .env entries:** Delete the `BLUEBUBBLES_SERVER_URL` and `BLUEBUBBLES_PASSWORD` lines from `~/.hermes/.env`. (This file is protected from agent tool writes — the user must do it manually.)

3. **Uninstall the app:**
   ```bash
   killall BlueBubbles   # Stop if running
   osascript -e 'tell application "Finder" to delete file POSIX file "/Applications/BlueBubbles.app"'
   ```
   Or drag to Trash manually.

4. **Restart gateway** so it stops trying to connect:
   ```bash
   hermes gateway restart
   ```
   Verify it no longer shows BlueBubbles:
   ```bash
   tail -10 ~/.hermes/logs/gateway.log | grep -E 'connected|failed'
   ```

### General Hermes Constraint: `.env` Files Are Agent-Protected

Hermes protects `~/.hermes/.env` from agent tool modifications — the agent cannot use `write_file`, `patch`, `sed`, or `terminal echo >>` to modify it. This is a defense-in-depth measure, not a bug.

**Workarounds when you need to add env vars:**
- **Best:** Tell the user which lines to add and let them edit manually (open with `hermes config env-path` to see the path)
- **Alternative:** Use `hermes config set section.key value` for config.yaml settings (not env vars)
- **Interactive wizard:** `hermes gateway setup` prompts for platform tokens and may handle writing them

This applies to all platform tokens: `TELEGRAM_BOT_TOKEN`, `BLUEBUBBLES_PASSWORD`, `DISCORD_BOT_TOKEN`, `SLACK_BOT_TOKEN`, etc. Never promise the agent can write these directly.

### Setup Pitfalls

- **Self-messaging doesn't work:** When a user sends an iMessage to their **own phone number or Apple ID**, the Mac's Messages database marks the message as `isFromMe=True`. The Hermes webhook handler explicitly filters these out (bluebubbles.py lines 902-908) to prevent echo loops. **Do not promise** the user they can text themselves to talk to Hermes — it will never arrive. Instead:
  - **If imsg CLI is installed:** use `imsg send --to` from the agent side, or have another Apple ID send the user a message
  - **If using the gateway:** the user should message FROM a different Apple ID/number, OR Hermes initiates the conversation first (sends a message out, then the user replies directly — the *reply* will have `isFromMe=False`)
  - **Pairing flow (one exception):** the initial pairing code *does* reach the user because Hermes sends it out proactively. After approval, the user's reply iMessage will come through correctly as long as they're replying to a Hermes-initiated conversation, not starting a new self-addressed one.

- **"Next" button grayed out on Connection Setup:** The wizard requires both a password AND a proxy service selection. Choose "None" or "Local Network" from the proxy dropdown if connecting from the same machine — no internet proxy needed. The API serves on port 1234 even before the wizard is fully completed.
- **API is running before wizard completion:** The BlueBubbles HTTP API starts listening on port 1234 as soon as the app launches, even if the setup wizard isn't finished. You can test connectivity immediately:
  ```bash
  curl -s "http://127.0.0.1:1234/api/v1/ping?password=<YOUR_PASSWORD>"
  # Expected: {"status":200,"message":"Ping received!","data":"pong"}
  ```
  This means you can skip the wizard and configure Hermes directly if you already know the password.
- **Auth format:** BlueBubbles API uses query parameter for authentication: `?password=...` (not Bearer token, not header-based — though `x-password` header is also accepted for webhook verification).
- **Private API helper:** Tapback reactions, typing indicators, and read receipts require installing the BlueBubbles Private API helper (from docs.bluebubbles.app). Basic text + media works without it.
- **`.app` bundle updates:** When updating BlueBubbles.app, use `ditto` not `rm -rf + cp -R`. macOS `cp -R` merges into existing .app bundles leaving old files behind.

### Hermes Configuration

Add to `~/.hermes/.env`:
```env
BLUEBUBBLES_SERVER_URL=http://127.0.0.1:1234
BLUEBUBBLES_PASSWORD=your-server-password
```

Optional — pre-authorize users:
```env
BLUEBUBBLES_ALLOWED_USERS=user@icloud.com,+155****4567
# Or open access:
BLUEBUBBLES_ALLOW_ALL_USERS=true
```

Then restart gateway:
```bash
hermes gateway restart
```

### User Authorization (DM Pairing)

Recommended flow: the first time someone sends an iMessage to the BlueBubbles server's phone number/Apple ID, Hermes generates a pairing code. The user receives it via iMessage, then the agent approves it.

**Steps for the agent:**

1. User says "I received a pairing code" — approve it:
   ```bash
   hermes pairing approve bluebubbles <CODE>
   ```

2. If the user has already sent multiple messages, check for pending codes first:
   ```bash
   hermes pairing list
   ```
   This shows all pending requests with their codes, plus all already-approved users.

3. After approval, tell the user to send another iMessage to confirm pairing works. Check gateway logs:
   ```bash
   grep -i 'inbound\|unauthorized\|message' ~/.hermes/logs/gateway.log | tail -10
   ```

4. If the user's phone sends from the Apple ID (not phone number), a second pairing code may appear for the email address — approve it too.

### Troubleshooting

**After gateway restart, BlueBubbles may not forward webhook events:** Gateway restart unregisters and re-registers the BlueBubbles webhook. The webhook URL in BlueBubbles gets updated, but BlueBubbles may not immediately start forwarding events. If messages stop arriving after a gateway restart:
1. Check the webhook is registered: `curl -s '<SERVER_URL>/api/v1/webhook?password=<PASSWORD>'`
2. If registered but no events flowing, restart BlueBubbles itself: `killall BlueBubbles && open -a BlueBubbles`
3. Wait for BlueBubbles to reconnect to Messages.app, then have the user send a test message

**`isFromMe=True` filtering stops self-messages:** This is the most common "messages not arriving" cause. Hermes' webhook handler returns `200 ok` immediately for any message where `isFromMe=True` — it never reaches the conversation loop. This includes messages the user sends to their own phone number or Apple ID from their iPhone. To check if this is the issue: query the chat directly via BlueBubbles API and look at the `isFromMe` field on recent messages. If they're all `isFromMe=True`, the webhook is working but correctly filtering them.

**Dual identity"} (phone number vs Apple ID):** The user's iPhone sends iMessages from the **Apple ID email** (e.g. `user@icloud.com`), not the phone number. After approving the phone number, the Apple ID may still generate a separate pending pairing request:
```
WARNING gateway.run: Unauthorized user: user@icloud.com (user@icloud.com) on bluebubbles
```
Check `hermes pairing list` — there will be a separate entry for the Apple ID. Approve it with its own code.

**Rate limit lockout on approval:** After 5 failed `hermes pairing approve` attempts, the platform is locked out for 3600s (1 hour):
```
4. **Pairing code case sensitivity:** The `hermes pairing approve` command auto-uppercases the input code. If the pending list shows a lowercase code (e.g. `9b1bcadb`), the uppercased version may not match. Fix: clear pending codes and have the user send a fresh iMessage, then approve the new code.

5. **Rate limit lockout:** After 5 failed `hermes pairing approve` attempts, the platform is locked out for 3600s (1 hour). Reset by deleting the lockout file and restarting:
   ```bash
   rm ~/.hermes/pairing/_rate_limits.json
   hermes gateway restart
   ```

6. **Self-message API diagnosis:** When self-messages aren't arriving via webhook, directly query BlueBubbles API to check:
   ```bash
   curl -s -X POST 'http://<SERVER_URL>/api/v1/chat/query?password=<PASSWORD>' \
     -H 'Content-Type: application/json' \
     -d '{"limit":50,"offset":0,"with":["participants"]}'
   # Then check messages in the target chat:
   curl -s 'http://<SERVER_URL>/api/v1/chat/<GUID_ENCODED>/message?password=<PASSWORD>&limit=10'
   ```
   Look at `isFromMe` field — if it's `true`, Hermes will filter it out. This confirms the webhook IS working but the message is correctly ignored as a self-send.

**Pairing code "not found":** The `hermes pairing approve` command auto-uppercases the input code. If the pending list shows a lowercase code (e.g. `9b1bcadb`), the uppercased version may not match. Fix: clear pending codes and have the user send a fresh iMessage:
```bash
hermes pairing clear-pending
# User sends a new iMessage → new code appears
hermes pairing approve bluebubbles <NEW_CODE>
```

**Messages not reaching Hermes:** If the user sends an iMessage but no gateway log entry appears, check the chain:
1. BlueBubbles server running: `ps aux | grep BlueBubbles | grep -v grep`
2. BlueBubbles API responds: `curl -s "http://<SERVER_URL>/api/v1/ping?password=<PASSWORD>"` → expect `pong`
3. Webhook listener is up: `lsof -i :8645`
4. Messages.app is signed in and running on the Mac
5. Gateway log shows connected: `grep bluebubbles ~/.hermes/logs/gateway.log | tail -5`
6. **Direct API check:** Query recent chats to see if messages arrived:
   ```bash
   curl -s -X POST 'http://<SERVER_URL>/api/v1/chat/query?password=<PASSWORD>' \
     -H 'Content-Type: application/json' \
     -d '{"limit":10,"offset":0,"with":["participants"]}'
   ```

### Full Configuration Reference

See Hermes docs: [BlueBubbles (iMessage) Setup](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/other/bluebubbles)

### Approach Comparison

| Feature | imsg CLI | BlueBubbles Gateway |
|---------|----------|---------------------|
| Send messages | ✅ | ✅ |
| Receive messages (two-way) | ❌ (manual watch) | ✅ (webhooks) |
| Images & media | ❌ (file attach) | ✅ |
| Tapback reactions | ❌ | ✅ (Private API) |
| Typing indicators | ❌ | ✅ (Private API) |
| Read receipts | ❌ | ✅ (Private API) |
| Requires gateway running | ❌ | ✅ |
| Requires BlueBubbles Server | ❌ | ✅ |

