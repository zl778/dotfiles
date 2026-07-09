# TUI Gateway Python Interpreter Resolution

## Error Signal

**"Voice transcription failed — Timed out connecting to Hermes backend after 15000ms"**

This error appears as a macOS notification or in-app toast from the Hermes desktop app (Hermes.app, an Electron application). The 15,000ms is the `STARTUP_TIMEOUT_MS` constant in `ui-tui/src/gatewayClient.ts`.

## Root Cause

The Hermes desktop app's `GatewayClient` spawns a Python subprocess running `python -m tui_gateway.entry`. It waits for the process to emit a `gateway.ready` JSON-RPC event on stdout. If this doesn't arrive within 15 seconds, it fires `gateway.start_timeout` which surfaces as the error above.

The TUI gateway imports `hermes_cli.env_loader` → `dotenv` early in its startup (`tui_gateway/server.py`). If the Python interpreter chosen by `resolvePython()` does **not** have `python-dotenv` installed, the import fails immediately with `ModuleNotFoundError`, the process crashes silently, and the TUI times out.

## Python Resolution Order

`gatewayClient.ts` → `resolvePython(root)`:

```typescript
const resolvePython = (root: string) => {
  const configured = process.env.HERMES_PYTHON?.trim() || process.env.PYTHON?.trim()
  if (configured) return configured                         // (1)

  const venv = process.env.VIRTUAL_ENV?.trim()              // (2)
  const hit = [
    venv && resolve(venv, 'bin/python'),                    // (2a)
    venv && resolve(venv, 'Scripts/python.exe'),            // (2b)
    resolve(root, '.venv/bin/python'),                      // (3a)
    resolve(root, '.venv/bin/python3'),                     // (3b)
    resolve(root, 'venv/bin/python'),                       // (3c)
    resolve(root, 'venv/bin/python3')                       // (3d)
  ].find(p => p && existsSync(p))

  return hit || (process.platform === 'win32' ? 'python' : 'python3')   // (4)
}
```

Where `root = process.env.HERMES_PYTHON_SRC_ROOT ?? resolve(import.meta.dirname, '../../')`.

If none of (1)–(3) find a usable Python, it falls back to the system `python3` (4), which typically lacks `python-dotenv` and other Hermes dependencies.

## Diagnosis

1. **Check what TUI gateway actually runs:**
   ```bash
   # Simulate what GatewayClient does
   HERMES_PYTHON_SRC_ROOT="$HOME/.hermes/hermes-agent"
   python3 -c "from tui_gateway import server; import dotenv; print('OK')"
   ```
   If this fails with `ModuleNotFoundError: No module named 'dotenv'`, the system Python is the culprit.

2. **Find the correct Python:**
   ```bash
   ls ~/.hermes/hermes-agent/venv/bin/python3
   ```

3. **Verify the correct one works:**
   ```bash
   ~/.hermes/hermes-agent/venv/bin/python3 -c "from tui_gateway import server; import dotenv; print('OK')"
   ```

## Fix

Set `HERMES_PYTHON` to the Hermes venv Python **before launching the desktop app**:

```bash
export HERMES_PYTHON="$HOME/.hermes/hermes-agent/venv/bin/python3"
export HERMES_PYTHON_SRC_ROOT="$HOME/.hermes/hermes-agent"
open /Applications/Hermes.app
```

### Wrapper Script

A drop-in script at `~/bin/hermes-app`:

```bash
#!/bin/bash
export HERMES_PYTHON="$HOME/.hermes/hermes-agent/venv/bin/python3"
export HERMES_PYTHON_SRC_ROOT="$HOME/.hermes/hermes-agent"
open /Applications/Hermes.app
```

Make it executable (`chmod +x ~/bin/hermes-app`) and run `hermes-app` from the terminal afterwards.

## Why This Happens

The packaged Hermes.app Electron bundle ships with its own asar archive. When the GatewayClient resolves `root` from `import.meta.dirname`, it gets a path inside the asar (`/Applications/Hermes.app/Contents/Resources/app.asar/...`), and `../../` doesn't point to the hermes-agent source tree. Without `HERMES_PYTHON_SRC_ROOT`, the venv lookups under `root/` fail, and the fallback `python3` (system) lacks Hermes's dependencies.

## Related

- `tui_gateway/entry.py` — entry point, emits `gateway.ready`
- `tui_gateway/server.py` — imports `hermes_cli.env_loader` which requires `dotenv`
- `ui-tui/src/gatewayClient.ts` — `startReadyTimer()`, `startSpawnedGateway()`, `resolvePython()`
