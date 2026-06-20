# Python Debugging Reference

## Full pdb Command Reference

| Command | Action |
|---------|--------|
| `h` / `h cmd` | help |
| `n` | next line (step over) |
| `s` | step into |
| `r` | return from current function |
| `c` | continue |
| `unt N` | continue until line N |
| `j N` | jump to line N (same function only) |
| `l` / `ll` | list source around current line / full function |
| `w` | where (stack trace) |
| `u` / `d` | move up / down in the stack |
| `a` | print args of the current function |
| `p expr` / `pp expr` | print / pretty-print expression |
| `display expr` | auto-print expr on every stop |
| `b file:line` | set breakpoint |
| `b func` | break on function entry |
| `b file:line, cond` | conditional breakpoint |
| `cl N` | clear breakpoint N |
| `tbreak file:line` | one-shot breakpoint |
| `!stmt` | execute arbitrary Python (assignments included) |
| `interact` | drop into full Python REPL in current scope (Ctrl+D to exit) |
| `q` | quit |

## Debugpy Remote Debug (DAP Protocol)

### Setup
```bash
source .venv/bin/activate
pip install debugpy
```

### Pattern A: Source-edit — process waits for debugger at launch
```python
import debugpy
debugpy.listen(("127.0.0.1", 5678))
print("debugpy listening on 5678, waiting for client...", flush=True)
debugpy.wait_for_client()
debugpy.breakpoint()  # optional: pause immediately once attached
```

### Pattern B: No source edit — launch with -m debugpy
```bash
python -m debugpy --listen 127.0.0.1:5678 --wait-for-client your_script.py arg1
```

### Pattern C: Attach to already-running process
```bash
python -m debugpy --listen 127.0.0.1:5678 --pid <pid>
```

### Connecting a client from terminal

**Option 1: remote-pdb** (cleanest agent-friendly approach):
```bash
pip install remote-pdb
```
In code:
```python
from remote_pdb import set_trace
set_trace(host="127.0.0.1", port=4444)
```
Then: `nc 127.0.0.1 4444` — you get a full (Pdb) prompt.

**Option 2: Attach from VS Code:**
```json
{
  "name": "Attach to Hermes",
  "type": "debugpy",
  "request": "attach",
  "connect": { "host": "127.0.0.1", "port": 5678 },
  "justMyCode": false
}
```

### Debugging Hermes-Specific Processes

| Process | Approach |
|---------|----------|
| `run_agent.py` / CLI | `breakpoint()` near suspect line, run `hermes` normally |
| `tui_gateway` subprocess | `remote-pdb` at the RPC handler |
| `_SlashWorker` subprocess | `set_trace()` inside worker's `exec` path |
| Gateway (`gateway/run.py`) | `remote-pdb` at handler, or `debugpy --wait-for-client` |

### Debugging pytest Tests
```bash
# Drop to pdb on failure
scripts/run_tests.sh tests/path/test.py::test_name --pdb -p no:xdist

# Drop to pdb at START of test
scripts/run_tests.sh tests/path/test.py::test_name --trace -p no:xdist

# Show locals without pdb
scripts/run_tests.sh tests/path/test.py --showlocals --tb=long
```

⚠️ pdb does NOT work under xdist. Always add `-p no:xdist` or use `-n 0`.

### Post-Mortem Debugging

```python
import pdb, sys
try:
    run_the_thing()
except Exception:
    pdb.post_mortem(sys.exc_info()[2])
```

Or wrap whole script:
```bash
python -m pdb -c continue script.py
```

### Common Pitfalls
1. **pdb under xdist silently does nothing** — use `-p no:xdist` or `-n 0`
2. **breakpoint() in CI hangs** — never commit. Add pre-commit grep.
3. **PYTHONBREAKPOINT=0** disables all breakpoint() calls
4. **debugpy.listen blocks only if you also call wait_for_client()**
5. **Attach to PID fails on hardened kernels** — ptrace_scope=1 blocks same-user ptrace
6. **pdb only debugs current thread** — use debugpy for multithreaded
7. **scripts/run_tests.sh strips credentials** — debug with raw pytest first
8. **Forking/multiprocessing** — pdb does not follow forks

### Cleanup check before committing
```bash
rg -n 'breakpoint\(\)|set_trace\(|debugpy\.listen' --type py
```
