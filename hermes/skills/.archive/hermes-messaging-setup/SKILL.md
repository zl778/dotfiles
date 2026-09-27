---
name: hermes-messaging-setup
description: "Best practices for configuring Hermes messaging platforms and gateway onboarding."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [hermes, gateway, messaging, setup, troubleshooting, photon, bluebubbles, telegram, discord, slack]
---

# Hermes Messaging Platform Setup

Use this skill when setting up, enabling, troubleshooting, or verifying a Hermes messaging platform integration.

## Core principle
Prefer the unified gateway setup surface first:

1. Run `hermes gateway setup`.
2. Choose the platform from the menu.
3. Complete the platform-specific setup flow.
4. Restart the gateway when prompted.
5. Verify with `hermes gateway status` or the platform status command.

This keeps platform onboarding consistent and avoids chasing plugin-specific commands when the gateway wizard already dispatches to the correct setup handler.

## When a plugin provides its own setup helper
Some platforms expose a plugin-backed setup function that is surfaced inside the unified gateway wizard. In those cases:

- Treat `hermes gateway setup` as the canonical entry point.
- Use the plugin-specific CLI only when the docs explicitly say it is the preferred path.
- If the top-level subcommand is not present in the current install, do not assume the feature is missing; check the gateway wizard and plugin docs first.

## Access control defaults
When configuring a chat platform, choose the least-privilege access model that still works for your use case:

- Prefer an explicit allowlist for your own number/user/account.
- Use mention gating for group chats when the platform supports it.
- Avoid allow-all mode except for short-lived testing.
- If the setup flow offers to auto-configure the operator’s own access, accept it when you want the bot to reply only to that account.
## Photon / iMessage pattern

Photon follows the same general gateway pattern as other Hermes messaging platforms:

- It is a persistent-connection channel.
- There is no webhook, public URL, or signing secret to manage.
- Runtime credentials belong in `~/.hermes/.env`.
- Setup should register the operator account, provision a project secret, and install sidecar dependencies.
- Use `hermes gateway setup` → select `iMessage via Photon` as the standard onboarding path.
- Standalone outbound sends need a live Photon sidecar plus `PHOTON_SIDECAR_TOKEN`; don’t confuse a sidecar auth failure with a gateway wiring failure.
- If outbound sends are rejected with `Target not allowed for this project`, verify the Photon project/assigned-line permissions before changing Hermes routing.
- For “only me can message Hermes”, configure both the allowlist and the home channel to the operator’s own number/line.

See `references/photon-imessage-setup.md` for Photon-specific notes and verification steps.

## Verification checklist
After setup, confirm all of the following:

- The gateway service is running.
- The platform appears as configured in `hermes status` / `hermes gateway status`.
- The platform’s status command reports valid credentials or assigned endpoints.
- A test DM from an authorized account is received and answered.
- If applicable, group mention gating behaves as expected.

## Common pitfalls
- Don’t stop after editing config; many gateway changes require a restart.
- Don’t rely on a plugin command that may not exist in the current install when the gateway wizard is available.
- Don’t leave group chats open by default if the platform supports mention gating.
- Don’t confuse runtime credentials with management metadata; keep secrets in `.env` and opaque IDs in `auth.json` or the platform’s equivalent.

## Support files
- `references/photon-imessage-setup.md` — Photon iMessage setup notes, access control, and verification details.
