---
name: hermes-maintenance
description: "Use when updating Hermes."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [hermes, update, maintenance, dependencies, uv, verification]
---

# Hermes maintenance

## When to Use

Use this skill for Hermes upgrades, dependency/runtime repair after an upgrade, and verification of source-versus-installed state.

## Procedure

1. Load the `hermes-agent` skill before changing Hermes itself; use its documented CLI and path conventions.
2. Run the requested update exactly once with the user's requested approval mode:
   `hermes --yolo update`
3. Read the complete result. Separate these states rather than treating the command's exit code as sufficient:
   - source tree updated and clean;
   - dependency/runtime preparation succeeded;
   - services or profiles were restarted successfully;
   - stale update stashes were reported;
   - update stopped at dependency or network preparation.
4. If the updater says that `uv.lock` needs updating, do not use the system `uv` blindly. Check the Hermes-managed resolver first:
   `~/.hermes/bin/uv --version`
   Then, from the Hermes source checkout, validate or regenerate the lock with the managed resolver:
   `cd ~/.hermes/hermes-agent && ~/.hermes/bin/uv lock --check`
   If the check fails because the lock is genuinely stale, run:
   `~/.hermes/bin/uv lock`
   and rerun the update.
5. If the source update is current but runtime preparation still fails, test the managed environment directly with the same locked dependency graph before claiming completion:
   `~/.hermes/bin/uv sync --locked --all-packages --all-extras --python <managed-python> --compile-bytecode`
   Treat a dependency download/build failure as an incomplete update, not as a successful update.
6. Verify after every attempt with:
   - `hermes --version`
   - source checkout status: `git -C ~/.hermes/hermes-agent status --short --branch`
   - `hermes pm doctor` when the runtime is in doubt.
7. Report the result in three parts: completed state, exact blocker (if any), and safe follow-up. Do not claim the runtime is updated merely because Git reports that the source is current.

## Safety and recovery rules

- Preserve updater-created stashes until their contents are reviewed; a clean working tree does not prove that local changes were restored.
- Never discard stale update stashes automatically; `git stash show -p <stash>` is the review step, and `git stash apply <stash>` is the recovery step.
- Keep the system `uv` and Hermes-managed `uv` distinct: the project may require a newer resolver or syntax than the user's PATH provides, so invoking the wrong binary can produce a misleading lockfile error.
- Do not convert an unresolved dependency or network failure into a recommended workaround; record only a procedure that has been successfully exercised and verify it before reporting success.

## References

- For the full Hermes CLI and profile/gateway behavior, consult the protected `hermes-agent` skill.
