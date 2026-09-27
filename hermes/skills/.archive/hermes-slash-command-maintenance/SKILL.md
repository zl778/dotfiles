---
name: hermes-slash-command-maintenance
description: "Maintain Hermes slash commands and verify behavior."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes-agent, slash-commands, cli, gateway, maintenance, verification]
    related_skills: [debugging-hermes-tui-commands, systematic-debugging]
---

# Hermes Slash-Command Maintenance

## Trigger

Use when changing the behavior, output size, selection rules, or persistence semantics of an existing Hermes slash command such as `/resume`, rather than merely debugging a command that is missing or broken.

## Core Workflow

1. Inspect the installed Hermes source and identify every surface that implements the command.
   - CLI slash handling commonly lives in `hermes_cli/cli_commands_mixin.py` and display helpers in `cli.py`.
   - Messaging/Gateway handling commonly lives in `gateway/slash_commands.py` or the platform runner.
   - Do not assume a change to one surface affects the others.
2. Search for all hard-coded limits and repeated selection logic before editing. For a list command, change both the database query limit and the final output slice; otherwise the query may still truncate the result before rendering.
3. Preserve index-selection consistency. The list displayed to the user, the list stored for pending numeric selection, and the list reloaded for `/command N` must use the same limit and ordering.
4. Keep unrelated commands unchanged. For example, if a shared helper defaults to 10 for `/history`, pass the new limit only from `/resume` rather than globally changing the helper default.
5. Patch source files atomically and inspect the resulting diff. Ignore unrelated pre-existing untracked files.
6. Restart the relevant long-running process after source changes: restart the Gateway for messaging surfaces; relaunch the CLI for interactive CLI behavior.

## Verification

Run focused tests if the development environment includes pytest. If pytest is unavailable, do not fabricate test results; use the Hermes virtual-environment interpreter where available and fall back to deterministic checks:

- Python compilation (`py_compile`) for each modified Python file.
- Source assertions that each intended query, display slice, and numeric-selection path uses the requested limit.
- A read-only CLI command such as `hermes sessions list --limit N` to confirm the installed wrapper and source tree are aligned.
- Report unavailable tests separately from successful compilation/source verification.

For `/resume`-style list changes, verify these paths independently:

- Bare command displays the requested number of recent records.
- Bare-command pending numeric selection uses the same list.
- Explicit numeric selection accepts the new upper index and rejects the next one.
- Title/ID selection remains unaffected.
- Gateway output, when supported, uses the same intended cap.

## Pitfalls

- A default function parameter used by multiple commands is not automatically the right place to change a single command's behavior.
- Changing only the renderer is insufficient if the database query still requests the old number.
- Changing only the query is insufficient if a later `[:old_limit]` slice remains.
- Do not claim that tests passed after a failed test invocation or missing `pytest`; clearly distinguish failed setup from code verification.
- Source edits take effect only after restarting the process that imported the old module.

## Support Files

- `references/resume-list-limit-change.md` — concrete `/resume` limit-change recipe and verification notes from the CLI/Gateway implementation.
