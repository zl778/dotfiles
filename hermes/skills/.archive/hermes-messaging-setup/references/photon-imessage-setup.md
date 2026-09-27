# Photon iMessage setup notes

Scope: Hermes Agent + Photon iMessage integration.

Authoritative docs:
- https://hermes-agent.nousresearch.com/docs/user-guide/messaging/photon
- https://hermes-agent.nousresearch.com/docs/reference/environment-variables#photon

Best-practice setup path
1. Run `hermes gateway setup` and select `iMessage via Photon` in the messaging platform menu.
2. Complete Photon device-code login when prompted (browser approval + code).
3. Let setup reuse or create the Hermes Agent project, then provision Spectrum credentials.
4. Register the operator phone number with `--phone` when possible.
5. Install sidecar deps, then start or restart the gateway.

Important operational details
- Photon is a persistent-connection channel: no webhook, public URL, or signing secret.
- Runtime credentials live in `~/.hermes/.env` as `PHOTON_PROJECT_ID` and `PHOTON_PROJECT_SECRET`.
- Management metadata lives in `~/.hermes/auth.json`.
- The setup flow can auto-configure operator access and the default home channel when a phone number is supplied:
  - `PHOTON_ALLOWED_USERS=<operator E.164>`
  - `PHOTON_HOME_CHANNEL=<operator E.164>`
- For tighter group behavior, enable mention gating with `PHOTON_REQUIRE_MENTION=true`.
- Standalone outbound sends need the Photon sidecar running and `PHOTON_SIDECAR_TOKEN` exported.
- If outbound fails with `Target not allowed for this project`, verify Photon project permissions / assigned line rather than reworking Hermes routing first.

Verification / troubleshooting
- `hermes photon status` reports token, project, assigned line, and sidecar health.
- `hermes gateway status` confirms the gateway service is running.
- If a Photon-specific top-level command is unavailable in a given install, use the gateway wizard as the canonical onboarding path.
- After setup, send a DM from the authorized number and confirm Hermes replies.
