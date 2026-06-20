# Node.js Debugging Reference

## node inspect REPL — Full Command Reference

| Command | Action |
|---------|--------|
| `c` / `cont` | continue |
| `n` / `next` | step over |
| `s` / `step` | step into |
| `o` / `out` | step out |
| `pause` | pause running code |
| `sb('file.js', 42)` | set breakpoint at line 42 |
| `sb(42)` | set breakpoint at line 42 of current file |
| `sb('functionName')` | break when function is called |
| `cb('file.js', 42)` | clear breakpoint |
| `breakpoints` | list all breakpoints |
| `bt` | backtrace (call stack) |
| `list(5)` | show 5 lines of source around current position |
| `watch('expr')` | evaluate expr on every pause |
| `watchers` | show watched expressions |
| `repl` | drop into REPL in current scope (Ctrl+C to exit) |
| `exec expr` | evaluate expression once |
| `restart` | restart script |
| `kill` | kill the script |
| `.exit` | quit debugger |

### Launching

```bash
# Pause on first line
node --inspect-brk path/to/script.js

# For TypeScript via tsx
node --inspect-brk --import tsx script.ts

# Custom port
node --inspect=0.0.0.0:9230 script.js
```

## Attaching to a Running Process

```bash
# 1. Enable inspector on existing process
kill -SIGUSR1 <pid>
# Node prints: Debugger listening on ws://127.0.0.1:9229/<uuid>

# 2. Attach CLI
node inspect -p <pid>
# or by URL
node inspect ws://127.0.0.1:9229/<uuid>
```

## Programmatic CDP (for automation)

Install chrome-remote-interface:
```bash
npm i -g chrome-remote-interface
```

Driver script example:
```javascript
const CDP = require('chrome-remote-interface');
(async () => {
  const client = await CDP({ port: 9229 });
  const { Debugger, Runtime } = client;

  Debugger.paused(async ({ callFrames, reason }) => {
    const top = callFrames[0];
    console.log(`PAUSED: ${reason} @ ${top.url}:${top.location.lineNumber + 1}`);

    // Walk scopes
    for (const scope of top.scopeChain) {
      if (scope.type === 'local' || scope.type === 'closure') {
        const { result } = await Runtime.getProperties({
          objectId: scope.object.objectId,
          ownProperties: true,
        });
        for (const p of result) {
          console.log(`  ${scope.type}.${p.name} =`, p.value?.value ?? p.value?.description);
        }
      }
    }
    await Debugger.resume();
  });

  await Runtime.enable();
  await Debugger.enable();
  await Debugger.setBreakpointByUrl({
    urlRegex: '.*app\\.tsx$',
    lineNumber: 119,
  });
  await Runtime.runIfWaitingForDebugger();
})();
```

## Debugging Hermes ui-tui

### Debugging a single Ink component
```bash
cd /path/to/hermes-agent/ui-tui
npm run build
node --inspect-brk dist/entry.js
# In another terminal:
node inspect -p $!
# debug> sb('dist/app.js', 220)
# debug> cont
```

### Debugging a running `hermes --tui`
```bash
hermes --tui &
TUI_PID=$(pgrep -f 'ui-tui/dist/entry' | head -1)
kill -SIGUSR1 "$TUI_PID"
curl -s http://127.0.0.1:9229/json/list  # Find WS URL
node inspect ws://127.0.0.1:9229/<uuid>
```

### Running Vitest under debugger
```bash
cd /path/to/hermes-agent/ui-tui
node --inspect-brk ./node_modules/vitest/vitest.mjs run --no-file-parallelism src/app/foo.test.tsx
```

## Heap Snapshots & CPU Profiles

```javascript
// CPU profile (5 seconds)
await client.Profiler.enable();
await client.Profiler.start();
await new Promise(r => setTimeout(r, 5000));
const { profile } = await client.Profiler.stop();
require('fs').writeFileSync('/tmp/cpu.cpuprofile', JSON.stringify(profile));

// Heap snapshot
const chunks = [];
client.HeapProfiler.addHeapSnapshotChunk(({ chunk }) => chunks.push(chunk));
await client.HeapProfiler.takeHeapSnapshot({ reportProgress: false });
require('fs').writeFileSync('/tmp/heap.heapsnapshot', chunks.join(''));
```

## Common Pitfalls
1. **Wrong line numbers in TS source** — breakpoints hit emitted JS, not `.ts`
2. **`--inspect` vs `--inspect-brk`** — `--inspect` doesn't pause; script races past your breakpoint
3. **Port collisions** — default 9229. Use `--inspect=0` for random port
4. **Child processes** — `--inspect` on parent does NOT inspect children
5. **Ctrl+C out of `node inspect`** — target stays paused. `cont` first, or `kill` explicitly
6. **Run via agent terminal** — use `terminal(pty=true)` or `background=true` + `process(action='submit')`
7. **Security** — never bind inspector to `0.0.0.0` (remote code execution)
