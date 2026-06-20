---
name: language-debugging-tools
description: "Debug Python, Node.js, and Hermes TUI via breakpoints, step-through, remote DAP/CDP, and post-mortem inspection."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [debugging, python, nodejs, breakpoints, dap, cdp, pdb, inspect, post-mortem]
    related_skills: [systematic-debugging, debugging-hermes-tui-commands]
---

# Language Debugging Tools

Three debugger toolkits, one per language family:

| Section | Language | Tool | When |
|---------|----------|------|------|
| [Python (pdb + debugpy)](#python-pdb--debugpy) | Python | `breakpoint()`, `pdb`, `debugpy` | Local, remote, or headless Python debugging |
| [Node.js (node inspect + CDP)](#nodejs-node-inspect--cdp) | Node.js | `node inspect`, CDP via `chrome-remote-interface` | Node/TypeScript debugging, ui-tui troubleshooting |
| [Hermes TUI Slash Commands](#hermes-tui-slash-commands) | Python + TypeScript | TUI gateway, Ink frontend | Debugging Hermes TUI-specific slash command issues |

**Start with `breakpoint()` for Python or `node inspect` for Node.js** — they're always available zero-install. Escalate to remote debuggers only when you need to attach to a long-lived process or automate breakpoints.

---

## Python (pdb + debugpy)

### Quick Reference

| Tool | Command / Setup | Best for |
|------|----------------|----------|
| **breakpoint()** | Add `breakpoint()` in source, run normally | Local interactive debugging |
| **python -m pdb** | `python -m pdb script.py` | Launch under pdb with no source edits |
| **remote-pdb** | `pip install remote-pdb`; `set_trace(host='127.0.0.1', port=4444)` | Terminal-friendly remote debug |
| **debugpy** | `pip install debugpy`; `debugpy.listen(...)` + `wait_for_client()` | DAP / IDE integration |

### pdb Commands (at `(Pdb)` prompt)

| Cmd | Action |
|-----|--------|
| `n` / `s` / `r` / `c` | Next line, step into, return, continue |
| `l` / `ll` / `w` | List source, full function, stack trace |
| `p expr` / `pp expr` | Print / pretty-print |
| `b file:line` / `b func` | Set breakpoint |
| `cl N` | Clear breakpoint N |
| `interact` | Full Python REPL in current scope (Ctrl+D to exit) |
| `!stmt` | Execute arbitrary Python (mutations) |
| `display expr` | Auto-print expression on every stop |
| `u` / `d` | Move up / down the call stack |

### Debugging Under pytest

```bash
# pdb on failure
scripts/run_tests.sh tests/path/test.py::test_name --pdb -p no:xdist

# pdb at test start
scripts/run_tests.sh tests/path/test.py::test_name --trace -p no:xdist

# Show locals in tracebacks
scripts/run_tests.sh tests/path/test.py --showlocals --tb=long
```

**xdist note**: pdb does NOT work under xdist (`-n 4`). Always add `-p no:xdist` or `-n 0`.

### Remote Debug with remote-pdb (Terminal-Friendly)

```python
from remote_pdb import set_trace
set_trace(host="127.0.0.1", port=4444)   # blocks until connection
```

Then from another terminal: `nc 127.0.0.1 4444` — you get a `(Pdb)` prompt.

Best for debugging long-lived processes (gateway, daemon, PTY children) where you can't restart cleanly.

### Remote Debug with debugpy (DAP / IDE)

```python
import debugpy
debugpy.listen(("127.0.0.1", 5678))
debugpy.wait_for_client()
debugpy.breakpoint()
```

Attach from VS Code via launch.json:

```json
{
  "name": "Attach to Hermes",
  "type": "debugpy",
  "request": "attach",
  "connect": { "host": "127.0.0.1", "port": 5678 }
}
```

Or launch from CLI: `python -m debugpy --listen 127.0.0.1:5678 --wait-for-client script.py`

### Python Pitfalls

- **breakpoint() under pytest-xdist silently hangs** — always use `-p no:xdist`
- **`PYTHONBREAKPOINT=0` disables all breakpoint() calls** — check env if not hitting
- **debugpy attach to PID** may fail on hardened kernels (`ptrace_scope=1`). Fix: `echo 0 | sudo tee /proc/sys/kernel/yama/ptrace_scope`
- **Threads:** pdb only debugs current thread. Use debugpy (thread-aware DAP) for multithreaded code.
- **asyncio:** `await` inside pdb requires Python 3.13+. For 3.11/3.12, use `asyncio.run_coroutine_threadsafe` tricks.
- **scripts/run_tests.sh** strips credentials and sets HOME to tmpdir — debug with raw `pytest` first.

---

## Node.js (node inspect + CDP)

### Quick Reference

| Tool | Command / Setup | Best for |
|------|----------------|----------|
| **node inspect** | `node inspect script.js` | Local interactive, zero install |
| **CDP via chrome-remote-interface** | `npm i -g chrome-remote-interface` | Automating breakpoints, scope dumps |
| **--inspect / --inspect-brk** | `node --inspect-brk script.js` | Enable inspector from process start |

### node inspect REPL (at `debug>` prompt)

| Cmd | Action |
|-----|--------|
| `c` / `cont` | Continue |
| `n` / `next` | Step over |
| `s` / `step` | Step into |
| `o` / `out` | Step out |
| `sb('file.js', 42)` | Set breakpoint at file.js:42 |
| `sb('funcName')` | Break on function entry |
| `cb('file.js', 42)` | Clear breakpoint |
| `bt` | Backtrace (call stack) |
| `watch('expr')` | Auto-evaluate expr on every pause |
| `repl` | Drop into Node REPL in paused scope (Ctrl+C to exit) |
| `exec expr` | Evaluate expression once |
| `list(N)` | Show N lines of source around current position |

### Attaching to Running Processes

```bash
# Enable inspector on existing process
kill -SIGUSR1 <pid>
# Node prints: Debugger listening on ws://127.0.0.1:9229/<uuid>

# Attach
node inspect -p <pid>
# or by URL
node inspect ws://127.0.0.1:9229/<uuid>
```

Start with inspector from beginning:
```bash
node --inspect script.js          # listen on 9229, keep running
node --inspect-brk script.js      # pause on first line
```

For TypeScript via tsx:
```bash
node --inspect-brk --import tsx script.ts
```

### Programmatic CDP

Install: `npm i chrome-remote-interface` (use a throwaway dir to avoid dirtying projects)

```javascript
const CDP = require('chrome-remote-interface');
(async () => {
  const client = await CDP({ port: 9229 });
  const { Debugger, Runtime } = client;
  Debugger.paused(async ({ callFrames }) => {
    // Walk scopes, evaluate expressions, resume
    await Debugger.resume();
  });
  await Debugger.enable();
  await Debugger.setBreakpointByUrl({ urlRegex: '.*app\\.tsx$', lineNumber: 119 });
  await Runtime.runIfWaitingForDebugger();
})();
```

### Debugging Hermes ui-tui

```bash
cd ~/hermes-agent/ui-tui
npm run build
node --inspect-brk dist/entry.js
# In another terminal:
node inspect -p <node pid>
# Then:
debug> sb('dist/app.js', 220)
debug> cont
```

For running TUI: `pgrep -f 'ui-tui/dist/entry'`, then `kill -SIGUSR1 <pid>`, then attach.

### Node.js Pitfalls

- **Wrong line numbers in TS source.** Breakpoints hit emitted JS, not `.ts`. Break in `dist/*.js`, or use CDP clients that support sourcemaps.
- **`--inspect` vs `--inspect-brk`.** `--inspect` doesn't pause; code races past first breakpoint. Use `--inspect-brk` for setup.
- **Port collisions (default 9229).** Use `--inspect=0` for random port, read actual URL via `curl http://127.0.0.1:9229/json/list`.
- **Child processes.** `--inspect` on parent does not inspect children. Use `NODE_OPTIONS='--inspect-brk'` to propagate.
- **Running through agent terminal.** Launch with `pty=true` or `background=true` + `process(action='submit')`.
- **Security.** Never bind `--inspect` to `0.0.0.0` — it exposes arbitrary code execution.

---

## Hermes TUI Slash Commands

Debugging slash commands in the Hermes TUI spans three layers (Python registry → TUI gateway → Ink frontend). For full detail load the `debugging-hermes-tui-commands` skill. Quick reference:

**Python side hangs or misbehaves**: use remote-pdb inside `_SlashWorker.exec` or the command handler.

**Ink side not reacting**: use `node --inspect-brk dist/entry.js` with CDP breakpoints in `app.tsx` slash dispatch.

**Registry mismatch**: compare the canonical `CommandDef` in `hermes_cli/commands.py` against the TUI's local command list.

---

## Common Patterns

### Post-mortem on crash

```bash
# Python
python -m pdb -c continue script.py

# Node.js (inspect running process after crash)
# Inspector must have been enabled before crash
```

### Debugging a subprocess / child

Hermes-specific: `_SlashWorker` and PTY bridge workers are Python. Use `remote-pdb` with `set_trace()` inside the worker's `exec` path. The worker persists across slash commands — first trigger blocks until you connect.

### Heap snapshots & CPU profiles (Node.js)

```javascript
// CPU profile for 5s
await client.Profiler.enable();
await client.Profiler.start();
await new Promise(r => setTimeout(r, 5000));
const { profile } = await client.Profiler.stop();

// Heap snapshot
const chunks = [];
client.HeapProfiler.addHeapSnapshotChunk(({ chunk }) => chunks.push(chunk));
await client.HeapProfiler.takeHeapSnapshot();
```

### One-Shot Recipes

**"Why is this dict missing a key?" (Python)**
```python
breakpoint()
# (Pdb) pp d
# (Pdb) pp list(d.keys())
# (Pdb) w
```

**"What's the call path into this function?" (Node.js)**
```
debug> sb('suspectFn')
debug> cont
debug> bt
```

**"This async chain hangs — where?" (Node.js)**
```
# Start with --inspect (no -brk), let it hang
debug> pause
debug> bt
```

## Verification Checklist

- [ ] First breakpoint actually hits (if not, check `PYTHONBREAKPOINT=0` or missed `--inspect-brk`)
- [ ] Post-debug cleanup: no stray `breakpoint()` / `set_trace()` in committed code
- [ ] For remote debug, confirm port is listening: `ss -tlnp | grep 4444` or `curl http://127.0.0.1:9229/json/list`
