# Messaging platforms reference

Session-derived condensed notes for Hermes gateway integrations.

## Photon iMessage
- Best entry point in current installs: `hermes gateway setup`.
- Plugin-specific setup may also exist on some installs, but only use it if the CLI exposes it.
- Photon is a persistent-connection iMessage bridge via managed Spectrum.
- It does not use a webhook/public URL/signing secret model.
- Safe default access posture:
  - `PHOTON_ALLOWED_USERS` for explicit sender allowlists
  - `PHOTON_REQUIRE_MENTION=true` for group-chat opt-in
- Runtime credentials go to `~/.hermes/.env`; management metadata goes to `~/.hermes/auth.json`.
- Verification checklist:
  - `hermes gateway setup` includes “iMessage via Photon”
  - `hermes config check` lists Photon env vars
  - `hermes plugins enable photon-platform` if the plugin is visible but inactive

## General gateway heuristics
- Use unified gateway setup/status surfaces first.
- Distinguish persistent-connection platforms from webhook platforms.
- Favor allowlists and mention gates for anything that can receive unsolicited messages.
- When a platform-specific CLI seems absent, confirm plugin activation before changing configs by hand.
