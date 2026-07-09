---
name: codex
description: "Delegate coding to OpenAI Codex CLI (features, PRs)."
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Coding-Agent, Codex, OpenAI, Code-Review, Refactoring]
    related_skills: [claude-code, hermes-agent]
---

# Codex CLI

Delegate coding tasks to [Codex](https://github.com/openai/codex) via the Hermes terminal. Codex is OpenAI's autonomous coding agent CLI.

## When to use

- Building features
- Refactoring
- PR reviews
- Batch issue fixing

Requires the codex CLI and a git repository.

## Prerequisites

- Codex installed: `npm install -g @openai/codex`
- OpenAI auth configured: either `OPENAI_API_KEY` or Codex OAuth credentials
  from the Codex CLI login flow
- **Must run inside a git repository** — Codex refuses to run outside one
- Use `pty=true` in terminal calls — Codex is an interactive terminal app

### NVM vs Hermes Node Environment

On macOS, **Hermes Agent bundles its own Node** at `~/.hermes/node/`. If you also
use NVM (or another Node version manager), you have two separate global npm
environments. Codex must be installed and run from the **correct** one.

**Primary environment rule:** NVM is the primary Node/npm environment for
user-facing tools like Codex CLI. Hermes's bundled Node (`~/.hermes/node/`) is
Hermes internal only and should not be the target of user `npm install -g`
commands.

**How to verify which codex is on your PATH:**

```bash
source ~/.nvm/nvm.sh   # ensure NVM context
which codex             # should show ~/.nvm/versions/node/.../bin/codex
codex --version
npm ls -g @openai/codex --depth=0   # confirms version in NVM's global modules
```

**Pitfall: npm list shows wrong version without NVM loaded**

If you run NVM's npm (`/Users/liangzhu/.nvm/versions/node/v24.13.0/bin/npm`)
**without sourcing nvm.sh first**, npm detects `~/.hermes/node/` as the prefix
and reads *Hermes's* node_modules — not NVM's. This makes it look like the
install succeeded when it didn't. Always `source ~/.nvm/nvm.sh` first.

**Debugging a version mismatch:**

```bash
# 1. Check PATH precedence
which codex

# 2. Load NVM and recheck
source ~/.nvm/nvm.sh
codex --version

# 3. Force reinstall a specific version
npm uninstall -g @openai/codex
npm cache clean --force
npm install -g @openai/codex@<version>
hash -r

# 4. Verify both PATH and NVM agree
which codex          # → NVM path
codex --version      # → expected version
npm ls -g @openai/codex --depth=0  # → matches
```

For Hermes itself, `model.provider: openai-codex` uses Hermes-managed Codex
OAuth from `~/.hermes/auth.json` after `hermes auth add openai-codex`. For the
standalone Codex CLI, a valid CLI OAuth session may live under
`~/.codex/auth.json`; do not treat a missing `OPENAI_API_KEY` alone as proof
that Codex auth is missing.

## Configuring Hermes openai-codex Provider

To use ChatGPT models (gpt-5.x, o-series) directly through Hermes (not via
Codex subprocess), set up the `openai-codex` provider:

### Standard OAuth Flow

```bash
hermes auth add openai-codex
```

This runs a device code OAuth flow. It prints a URL and user code; open the
URL in your browser and enter the code. After authentication, Hermes stores
its own OAuth session (separate from Codex CLI).

If the OAuth flow times out (common behind Cloudflare), try with a longer
timeout:
```bash
hermes auth add openai-codex --timeout 120
```

### Pitfall: Cloudflare Blocks auth.openai.com

`https://auth.openai.com/codex/device` is behind Cloudflare with a JS
challenge. The URL may redirect to a full OAuth authorize page with no
device-code input field visible, showing only "请稍候…" / "正在进行安全验证".

**Workaround — manual token import** (when standard OAuth is blocked):

1. Verify Codex CLI already has ChatGPT auth:
   ```bash
   cat ~/.codex/auth.json
   ```
   Look for `"auth_mode": "chatgpt"` with valid `access_token` and
   `refresh_token`.

2. Import the tokens into Hermes' auth store using the helper script at
   `references/codex-auth-openai-provider.md` (run via `execute_code`).

3. Verify:
   ```bash
   hermes auth list openai-codex    # should show 1 credential
   hermes auth status openai-codex  # should say "logged in"
   ```

4. Switch to the provider:
   ```bash
   hermes config set model.provider openai-codex
   ```
   Or run `hermes model` interactively and select `openai-codex`.

### Switching Models

Once `openai-codex` provider is configured, the available ChatGPT models
include:
- `gpt-5.x` (default for chat)
- `o-series` (reasoning models)
- `gpt-4o` and variants

Set the model:
```bash
hermes config set model.default "gpt-5.5"
```

## One-Shot Tasks

```
terminal(command="codex exec 'Add dark mode toggle to settings'", workdir="~/project", pty=true)
```

For scratch work (Codex needs a git repo):
```
terminal(command="cd $(mktemp -d) && git init && codex exec 'Build a snake game in Python'", pty=true)
```

## Background Mode (Long Tasks)

```
# Start in background with PTY
terminal(command="codex exec --full-auto 'Refactor the auth module'", workdir="~/project", background=true, pty=true)
# Returns session_id

# Monitor progress
process(action="poll", session_id="<id>")
process(action="log", session_id="<id>")

# Send input if Codex asks a question
process(action="submit", session_id="<id>", data="yes")

# Kill if needed
process(action="kill", session_id="<id>")
```

## Key Flags

| Flag | Effect |
|------|--------|
| `exec "prompt"` | One-shot execution, exits when done |
| `--full-auto` | Sandboxed but auto-approves file changes in workspace |
| `--yolo` | No sandbox, no approvals (fastest, most dangerous) |

## PR Reviews

Clone to a temp directory for safe review:

```
terminal(command="REVIEW=$(mktemp -d) && git clone https://github.com/user/repo.git $REVIEW && cd $REVIEW && gh pr checkout 42 && codex review --base origin/main", pty=true)
```

## Parallel Issue Fixing with Worktrees

```
# Create worktrees
terminal(command="git worktree add -b fix/issue-78 /tmp/issue-78 main", workdir="~/project")
terminal(command="git worktree add -b fix/issue-99 /tmp/issue-99 main", workdir="~/project")

# Launch Codex in each
terminal(command="codex --yolo exec 'Fix issue #78: <description>. Commit when done.'", workdir="/tmp/issue-78", background=true, pty=true)
terminal(command="codex --yolo exec 'Fix issue #99: <description>. Commit when done.'", workdir="/tmp/issue-99", background=true, pty=true)

# Monitor
process(action="list")

# After completion, push and create PRs
terminal(command="cd /tmp/issue-78 && git push -u origin fix/issue-78")
terminal(command="gh pr create --repo user/repo --head fix/issue-78 --title 'fix: ...' --body '...'")

# Cleanup
terminal(command="git worktree remove /tmp/issue-78", workdir="~/project")
```

## Batch PR Reviews

```
# Fetch all PR refs
terminal(command="git fetch origin '+refs/pull/*/head:refs/remotes/origin/pr/*'", workdir="~/project")

# Review multiple PRs in parallel
terminal(command="codex exec 'Review PR #86. git diff origin/main...origin/pr/86'", workdir="~/project", background=true, pty=true)
terminal(command="codex exec 'Review PR #87. git diff origin/main...origin/pr/87'", workdir="~/project", background=true, pty=true)

# Post results
terminal(command="gh pr comment 86 --body '<review>'", workdir="~/project")
```

## Rules

1. **Always use `pty=true`** — Codex is an interactive terminal app and hangs without a PTY
2. **Git repo required** — Codex won't run outside a git directory. Use `mktemp -d && git init` for scratch
3. **Use `exec` for one-shots** — `codex exec "prompt"` runs and exits cleanly
4. **`--full-auto` for building** — auto-approves changes within the sandbox
5. **Background for long tasks** — use `background=true` and monitor with `process` tool
6. **Don't interfere** — monitor with `poll`/`log`, be patient with long-running tasks
7. **Parallel is fine** — run multiple Codex processes at once for batch work
