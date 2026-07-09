# Debugging Hermes TUI Slash Commands

When a slash command is missing from autocomplete, works in CLI but not TUI, or config persists but the UI doesn't update, the bug is usually one layer out of sync with another.

## Three-Layer Architecture

```
Python backend (hermes_cli/commands.py)     ← canonical COMMAND_REGISTRY
       │
       ▼
TUI gateway (tui_gateway/server.py)         ← slash.exec / command.dispatch
       │
       ▼
TUI frontend (ui-tui/src/app/slash/)        ← local handlers + fallthrough
```

The Python `COMMAND_REGISTRY` is the source of truth for: CLI dispatch, gateway help, Telegram BotCommand menu, Slack subcommand map, and autocomplete data shipped to Ink.

## Investigation Steps

1. **Check TUI frontend:** `search_files --pattern "/commandname" --file_glob "*.ts" --path ui-tui/`
2. **Check Python backend:** `search_files --pattern "CommandDef" --file_glob "*.py" --path hermes_cli/`
3. **Check gateway:** `search_files --pattern "complete.slash|slash.exec" --path tui_gateway/`

## Fix: Missing Command Autocomplete

Add a `CommandDef` entry to `COMMAND_REGISTRY` in `hermes_cli/commands.py`:

```python
CommandDef("commandname", "Description of the command", "Session",
           cli_only=True, aliases=("alias",),
           args_hint="[arg1|arg2|arg3]",
           subcommands=("arg1", "arg2", "arg3")),
```

Flags: `cli_only=True` (CLI/TUI only), `gateway_only=True` (messaging only), neither (everywhere).

For server-side commands, add handler in `cli.py` → `process_command()`. For gateway, add in `gateway/run.py`.

## Common Issues

1. **Command in TUI but not autocomplete** — missing from `COMMAND_REGISTRY`
2. **Command in autocomplete but doesn't work** — check handlers in `tui_gateway/server.py` and frontend
3. **Different behavior CLI vs TUI** — local TUI handlers take precedence over gateway dispatch
4. **Config persists but UI doesn't update** — also patch nanostore state (`patchUiState(...)`)
5. **Gateway silently ignores** — check `GATEWAY_KNOWN_COMMANDS` includes the canonical name

## Debugging Tactics

- Python side: use `remote-pdb` inside `_SlashWorker.exec` or the command handler
- Ink side: use `node --inspect-brk dist/entry.js` with CDP breakpoints
- Registry mismatch: compare `COMMAND_REGISTRY` vs TUI local command list side-by-side

## Pitfalls

- Rebuild TUI after changes: `npm --prefix ui-tui run build`
- After adding live UI state, search every consumer of the old prop/helper
- TUI detail rendering has two important paths: live `StreamingAssistant`/`ToolTrail` and transcript/pending `MessageLine` rows
