# Remote worker routing notes

This reference captures a reusable pattern for connecting a coordinator profile to a remote worker profile.

## Example pattern

- Local coordinator profile: `default`
- Remote worker host: Windows machine reachable by SSH
- Remote worker profile: `winner`
- Local wrapper: `/Users/liangzhu/bin/call-winner`
- Windows wrapper: `%USERPROFILE%\\.local\\bin\\winner.bat`

## Example flow

1. Create or confirm the remote profile on the remote machine.
2. Make sure the remote profile can run on its own.
3. Add a stable wrapper on the local machine.
4. Add a worker registry entry with:
   - host
   - profile
   - entry
   - capabilities
   - return format
5. Route repeatable remote tasks through the worker entry.

## Important distinction

- `profile` is the actual Hermes instance.
- `alias` is only a convenience wrapper.
- `worker` is the stable route the coordinator uses.

## Useful verification commands

- `hermes profile list`
- `hermes profile show <profile>`
- `ssh <host> "<wrapper>"`
- local wrapper smoke test: run the wrapper with a trivial prompt and confirm the remote profile answers

## Pitfalls

- Do not assume a wrapper renamed a profile.
- Do not assume the root profile can always be renamed.
- Prefer the registered worker route for repeatable Windows / WSL work rather than ad hoc SSH in every turn.
