# Kanban Dashboard — Visual Web UI

Hermes ships a built-in Kanban Dashboard plugin that provides a **drag-and-drop visual board** in the browser.

## Location

```
~/.hermes/hermes-agent/plugins/kanban/dashboard/
├── manifest.json          # Tab at /kanban, position after:skills
├── plugin_api.py          # Backend API routes + WebSocket live events
└── dist/
    ├── index.js           # React frontend
    └── style.css
```

## How to access

```bash
hermes dashboard
```

Opens `http://127.0.0.1:9119` in the browser. The left sidebar has a **Kanban** tab showing:

- **Drag-and-drop columns** — move cards between triage/todo/ready/running/blocked/done
- **Per-task drawer** — click a card to see comments, events, runs, diagnostics
- **Recovery actions** — ⚠ badge on stuck tasks, with Reclaim/Reassign buttons
- **WebSocket live events** — real-time updates without refresh (via `/kanban/tail/<task_id>` WS endpoint)

## What the dashboard plugin provides

| Feature | Detail |
|---------|--------|
| Tab path | `/kanban` (dashboard plugin system) |
| Backend API | `/api/plugins/kanban/*` — router in `plugin_api.py` |
| WebSocket | `/kanban/tail/<task_id>` — live event stream (WAL-mode SQLite poll) |
| Auth | Inherits dashboard's session-token auth middleware; WS uses upgrade-header check |
| Board scope | Per-board (respects `--board` / `HERMES_KANBAN_BOARD`) |

## Three surfaces for Kanban

| Surface | How to access | When to use |
|---------|---------------|-------------|
| 🖥️ **Web Dashboard** | `hermes dashboard` → browser, click Kanban tab | Visual board with drag-and-drop, ideal for inspection & manual recovery |
| 💻 **CLI** | `hermes kanban <verb>` in terminal | Scripting, automation, human operators at the terminal |
| 🗨️ **In-chat** | `/kanban <sub>` in any Hermes conversation | Quick actions without leaving the chat session |

## Known limitation

The **Hermes Desktop app** (Electron) does **not** have a built-in web view for the dashboard. The Desktop app renders its own React UI (chat + file browser + settings) and does not embed dashboard plugin tabs. To see the visual Kanban board, use the browser-based `hermes dashboard`.

## Reference

- Web dashboard docs: `~/.hermes/hermes-agent/website/docs/user-guide/features/web-dashboard.md`
- Dashboard plugin system: `~/.hermes/hermes-agent/hermes_cli/web_server.py`