---
name: hermes-profile-worker-routing
description: Manage Hermes profiles, sticky defaults, wrapper aliases, and cross-machine worker routing.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes, profiles, aliases, workers, routing, ssh, windows, wsl, multi-agent]
---

# Hermes Profile & Worker Routing

Use this skill when a task involves:

- creating or organizing Hermes profiles
- understanding `default` vs cloned profiles
- using `profile use`, `profile rename`, or `profile alias`
- wiring a remote Windows / WSL worker into a Mac or Linux coordinator
- deciding whether to use direct SSH or a stable worker wrapper

## Core model

Think in three layers:

1. Profile identity
   - A profile is an isolated Hermes instance with its own config, sessions, skills, and gateway state.
2. Alias / wrapper
   - A convenience entry point. It helps invocation, but does not rename the profile.
3. Worker route
   - A stable path the coordinator uses to reach another machine’s Hermes instance.

## Recommended workflow

### 1) If the user wants a new main entry point

Do not try to rename `default` in place as the first move.

Prefer:

1. `hermes profile create <new-name> --clone-from default`
2. `hermes profile use <new-name>`
3. Verify with `hermes profile list` and `hermes profile show <new-name>`

If the user later decides the clone is unnecessary, delete the clone and keep `default`.

### 2) If the user wants a convenient launch name

Use `hermes profile alias` or a shell wrapper.

Remember:

- alias = convenience entry point
- profile = the actual Hermes instance

Never treat a wrapper script as if it changed the underlying profile identity.

### 3) If the user wants Mac default to call a Windows worker

Use a stable worker route instead of ad hoc SSH every time.

Record three fields in the worker registry /通讯录:

- host
- profile
- entry

For repeatable Windows tasks, prefer a stable wrapper such as `call-winner` (Mac side) or a `.bat` wrapper on the Windows side.

### 4) Routing preference

- Use the registered worker route for repeatable work
- Use raw SSH for one-off inspection or debugging
- When a Windows / WSL worker profile already exists, prefer routing through that worker rather than bypassing it

## Common pitfalls

- Trying to rename `default` instead of cloning a new profile
- Thinking a wrapper alias changes the profile name
- Using a remote machine by raw SSH in every turn, which makes the coordinator path inconsistent
- Confusing the coordinator’s local profile with a remote worker profile

## Verification checklist

- `hermes profile list` shows the expected profiles
- `hermes profile show <name>` confirms the profile path, alias, and gateway state
- The wrapper command runs end-to-end
- The worker registry includes host / profile / entry for the remote machine

## Support file

- `references/remote-worker-routing.md` — concise notes and example shapes for profile cloning, sticky defaults, aliases, and remote worker routing
