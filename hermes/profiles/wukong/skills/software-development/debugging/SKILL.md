---
name: debugging
description: "4-phase root cause debugging methodology + Python/Node.js/Hermes TUI debugging tools."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [debugging, troubleshooting, python, nodejs, pdb, breakpoints, root-cause, investigation]
    related_skills: [test-driven-development, writing-plans]
---

# Debugging

## Overview

Unified debugging skill covering the **systematic methodology** for finding root causes, plus the **concrete tools** for Python and Node.js debugging. Start with the methodology, then pick the right tool.

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

## When to Use

Use for ANY technical issue:
- Test failures, bugs, unexpected behavior
- Performance problems, build failures, integration issues
- Python or Node.js code that needs breakpoint inspection
- Hermes TUI slash commands that misbehave

## Sections

- [Methodology: 4-Phase Root Cause Debugging](#section-a-methodology-4-phase-root-cause-debugging)
- [Python Debugging Tools](#section-b-python-debugging-tools)
- [Node.js Debugging Tools](#section-c-nodejs-debugging-tools)
- [Hermes TUI Slash Command Debugging](#section-d-hermes-tui-slash-command-debugging)

---

## Section A: Methodology — 4-Phase Root Cause Debugging

Adapted from obra/superpowers. Systematic > guessing.

### The Iron Law
```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

### Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

1. **Read error messages carefully** — line numbers, file paths, error codes
2. **Reproduce consistently** — can you trigger it reliably every time?
3. **Check recent changes** — `git log --oneline -10`, `git diff`
4. **Trace data flow** — where does the bad value originate? Fix at the source, not the symptom
5. **Gather evidence** — logs, state at each component boundary

### Phase 2: Pattern Analysis

1. Find working examples similar to what's broken
2. Compare against references — read completely, don't skim
3. Identify every difference between working and broken
4. Understand dependencies and assumptions

### Phase 3: Hypothesis and Testing

1. Form a single hypothesis: "I think X is root cause because Y"
2. Make the SMALLEST possible change to test it
3. One variable at a time
4. Verify before continuing

### Phase 4: Implementation

1. Create a failing test case first (see `test-driven-development` skill)
2. Fix the root cause — ONE change at a time
3. Verify fix with tests
4. If fix doesn't work after 3 tries → STOP and question the architecture

### Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Multiple changes at once saves time"
- "I don't fully understand but this might work"

ALL of these mean: STOP. Return to Phase 1.

### Tools

| Phase | Hermes Tool |
|-------|------------|
| Phase 1 | `search_files`, `read_file`, `terminal` (tests, git history), `web_search` |
| Phase 2 | `search_files` (find similar patterns), `read_file` (compare) |
| Phase 3 | `terminal` (run minimal test), `execute_code` (quick prototype) |
| Phase 4 | `patch`, `write_file`, `terminal` (pytest) |

For complex multi-component debugging, use `delegate_task`:
```python
delegate_task(
    goal="Investigate why [specific test/behavior] fails",
    context="Follow debugging skill: read errors, reproduce, trace data flow. Report findings — do NOT fix yet.",
    toolsets=['terminal', 'file']
)
```

See `references/root-cause-methodology.md` for the full expanded methodology.

---

## Section B: Python Debugging Tools

Three tools, picked by situation:

| Tool | When |
|------|------|
| **`breakpoint()` + pdb** | Local, simplest. Add `breakpoint()` in source, run normally. |
| **`python -m pdb`** | Launch existing script under pdb with no source edits. |
| **`debugpy`** | Remote/headless/"attach to running process" via DAP. |
| **`remote-pdb`** | Agent-friendly remote debugging via `nc` — cleanest choice for terminal agents. |

**Start with `breakpoint()`.** It's the cheapest thing that works.

### Quick Reference: pdb REPL

| Command | Action |
|---------|--------|
| `n` | Next line (step over) |
| `s` | Step into |
| `c` | Continue |
| `l` / `ll` | List source / full function |
| `w` | Where (stack trace) |
| `u` / `d` | Move up/down in stack |
| `p expr` / `pp expr` | Print / pretty-print |
| `display expr` | Auto-print on every stop |
| `b file:line` | Set breakpoint |
| `!stmt` | Execute arbitrary Python |
| `interact` | Full Python REPL in scope |
| `q` | Quit |

### Common Recipes

**Local breakpoint:** Edit file: `breakpoint()` at the suspect line. Run code normally. Remove before committing.

**Debug a pytest test:**
```bash
scripts/run_tests.sh tests/path/test.py::test_name --pdb -p no:xdist
# or
python -m pytest tests/test.py --pdb
```

**Post-mortem on any exception:**
```python
import pdb, sys
try:
    run_the_thing()
except Exception:
    pdb.post_mortem(sys.exc_info()[2])
```

**Remote debug with remote-pdb** (agent-friendly):
```bash
pip install remote-pdb
```
In code:
```python
from remote_pdb import set_trace
set_trace(host="127.0.0.1", port=4444)
```
From terminal: `nc 127.0.0.1 4444` — you get a (Pdb) prompt.

**Remote debug with debugpy** (IDE integration):
```python
import debugpy
debugpy.listen(("127.0.0.1", 5678))
debugpy.wait_for_client()
debugpy.breakpoint()
```
Then attach VS Code via `launch.json` with `"request": "attach"`.

### Hermes-Specific Python Debugging

| Process | Approach |
|---------|----------|
| `run_agent.py` / CLI | `breakpoint()` near suspect line, run `hermes` normally |
| `tui_gateway` subprocess | `remote-pdb` at the RPC handler |
| `_SlashWorker` subprocess | `set_trace()` inside worker's `exec` path |
| `gateway/run.py` (long-lived) | `remote-pdb` at handler, or `debugpy --wait-for-client` |

### Pitfalls

- **pdb under pytest-xdist silently does nothing** — use `-p no:xdist` or `-n 0`
- **`breakpoint()` in CI hangs** — never commit it. Use pre-commit grep.
- **`PYTHONBREAKPOINT=0`** disables all `breakpoint()` calls
- **pdb doesn't follow forks** — each child needs its own `set_trace()`
- **`scripts/run_tests.sh` strips credentials** — if bug depends on user config, debug with raw `pytest` first

See `references/python-debugging.md` for the full expanded reference including `debugpy` DAP client scripts, heap snapshots, CPU profiles, and asyncio debugging.

---

## Section C: Node.js Debugging Tools

Two tools:

- **`node inspect`** — built-in, zero install, CLI REPL. Prefer first.
- **CDP via `chrome-remote-interface`** — scriptable from Node; best for automating breakpoints programmatically.

### Quick Reference: `node inspect` REPL

Launch paused on first line:
```bash
node inspect path/to/script.js
node --inspect-brk $(which tsx) path/to/script.ts
```

| Command | Action |
|---------|--------|
| `c` / `cont` | continue |
| `n` / `next` | step over |
| `s` / `step` | step into |
| `sb('file.js', 42)` | set breakpoint at line 42 |
| `sb('functionName')` | break on function entry |
| `bt` | backtrace |
| `list(5)` | show 5 lines of source |
| `repl` | JS REPL in current scope |

### Attaching to a Running Process

```bash
kill -SIGUSR1 <pid>                # enable inspector
node inspect -p <pid>              # attach CLI
```

### Common Recipes

**Debugging Hermes ui-tui:**
```bash
node --inspect-brk dist/entry.js    # from ui-tui/
# In another terminal:
node inspect -p $!
# debug> sb('dist/app.js', 220)
# debug> cont
```

**Debugging a running `hermes --tui`:**
```bash
hermes --tui &
TUI_PID=$(pgrep -f 'ui-tui/dist/entry' | head -1)
kill -SIGUSR1 "$TUI_PID"
```

**Running Vitest under debugger:**
```bash
node --inspect-brk ./node_modules/vitest/vitest.mjs run --no-file-parallelism src/app/foo.test.tsx
```

### Pitfalls

- Breakpoints hit emitted JS, not `.ts` — use `dist/*.js` line numbers
- `--inspect` starts inspector but doesn't pause; `--inspect-brk` pauses on first line
- Port collisions on 9229 — use `--inspect=0` for random port
- `--inspect` on parent does NOT inspect children

See `references/node-debugging.md` for the full expanded reference including CDP scripting, heap snapshots, CPU profiles, and Vitest debugging.

---

## Section D: Hermes TUI Slash Command Debugging

### Architecture Overview

```
Python backend (hermes_cli/commands.py)     <- canonical COMMAND_REGISTRY
       │
       ▼
TUI gateway (tui_gateway/server.py)         <- slash.exec / command.dispatch
       │
       ▼
TUI frontend (ui-tui/src/app/slash/)        <- local handlers + fallthrough
```

Command definitions must be registered consistently across Python and TypeScript.

### Investigation Steps

1. **Check TUI frontend**: `search_files --pattern "/commandname" --file_glob "*.ts" --path ui-tui/`
2. **Check Python backend**: `search_files --pattern "CommandDef" --file_glob "*.py" --path hermes_cli/`
3. **Check gateway**: `search_files --pattern "complete.slash|slash.exec" --path tui_gateway/`

### Common Issues

| Symptom | Likely Cause |
|---------|-------------|
| Command in TUI but not autocomplete | Missing from `COMMAND_REGISTRY` in `hermes_cli/commands.py` |
| Command in autocomplete but doesn't work | Missing handler in `cli.py` or TUI frontend |
| CLI vs TUI behavior differs | Different implementations in each layer |
| Config persists but UI doesn't update | Need to patch nanostore state, not just config |

### Fix: Adding a Command

1. Add `CommandDef` to `COMMAND_REGISTRY` in `hermes_cli/commands.py`
2. Add handler in `cli.py` → `process_command()`
3. For gateway: add handler in `gateway/run.py`

### Debugging Tactics

- **Python side hangs**: use Python debugging tools (Section B) with `remote-pdb` at handler entry
- **Ink side not reacting**: use Node.js debugging tools (Section C) with `node inspect` at the suspect render
- **Registry mismatch**: compare canonical `COMMAND_REGISTRY` vs TUI's local command list

### Verification

After fixing:
```bash
cd /path/to/hermes-agent && npm --prefix ui-tui run build
hermes --tui
```
Type `/` and verify command appears in autocomplete with expected description.

---

## References

| File | Description |
|------|-------------|
| `references/root-cause-methodology.md` | Full expanded 4-phase methodology with examples |
| `references/python-debugging.md` | Python debugging deep reference (debugpy DAP, asyncio, heap snapshots) |
| `references/node-debugging.md` | Node.js debugging deep reference (CDP scripting, CPU profiles) |

## Common Pitfalls

1. **pdb under pytest-xdist silently does nothing** — use `-p no:xdist` or `-n 0`
2. **`breakpoint()` in CI** — never commit it. Use pre-commit grep.
3. **Python `--inspect` vs `--inspect-brk`** — only `--inspect-brk` pauses on first line
4. **TUI slash command debugging** — check all three layers (Python registry, gateway, frontend)
5. **Wrong tool for the job** — use Python tools for Python code, Node tools for Node code, methodology for any bug

## Verification Checklist

- [ ] Error message fully read and understood
- [ ] Issue reproduced consistently
- [ ] Recent changes identified
- [ ] Root cause hypothesis formed before attempting fix
- [ ] Right debugging tool chosen for the language
- [ ] If Python: pdb not running under xdist
- [ ] If Node: source maps enabled for TypeScript
- [ ] If TUI: all three layers checked
- [ ] Post-debug cleanup: no `breakpoint()` / `set_trace()` in committed code
