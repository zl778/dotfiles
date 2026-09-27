---
name: hermes-messaging-platforms
description: Configure, verify, and troubleshoot Hermes messaging platform integrations.
version: 1.0.0
---

# Hermes Messaging Platforms

Use this skill when setting up or troubleshooting Hermes connections to messaging platforms such as Telegram, Discord, Slack, WhatsApp, Matrix, BlueBubbles, Photon iMessage, SMS, email, and similar gateway adapters.

## Core workflow
1. Start from the unified gateway surface when available: `hermes gateway setup`.
2. Prefer the platform’s own setup flow only when the platform-specific CLI is actually exposed on the current install.
3. Verify the platform appears in the gateway setup list and that the gateway service is running.
4. Check platform-specific config/credential state with `hermes config check` and the relevant `hermes <platform> status` command when available.
5. Keep runtime credentials in `~/.hermes/.env` and management metadata in `~/.hermes/auth.json` when the platform uses Hermes-managed credentials.

## Common best practices
- Use allowlists for production access control.
- Gate group chats with a mention/wake-word policy unless always-on replies are desired.
- Re-run setup safely when recovery is needed; good setup flows should be idempotent or at least partial-setup friendly.
- Treat persistent-connection channels differently from webhook channels: if the platform has a long-lived SDK stream, there is usually no public URL or signing secret to manage.

## Photon iMessage notes
- Photon is a persistent-connection iMessage bridge through managed Spectrum.
- Preferred starting point: free shared-line tier.
- Setup usually provisions device login, project, user, and sidecar dependencies in one pass.
- Recommended security defaults:
  - `PHOTON_ALLOWED_USERS` for explicit sender allowlists
  - `PHOTON_REQUIRE_MENTION=true` for group-chat opt-in behavior
- Runtime credentials are stored in `~/.hermes/.env`; management metadata lives in `~/.hermes/auth.json`.
- Verification signals:
  - `hermes gateway setup` shows “iMessage via Photon”
  - `hermes config check` lists `PHOTON_*` options
  - `hermes plugins enable photon-platform` can be used when the plugin is present but not active

## Troubleshooting pattern
- If a platform-specific command is missing, confirm whether the plugin is installed/active before assuming the feature is absent.
- If the unified wizard exposes the platform but the standalone command does not, use the unified wizard as the source of truth for that install.
- For updates and migrations, prefer the gateway’s built-in setup/status commands over manual file edits when the platform provides them.

## Support files
- `references/messaging-platforms.md` — condensed notes and session-derived platform quirks, including Photon setup and verification details.
