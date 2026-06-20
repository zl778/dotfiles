---
name: dotfiles-repo-setup
description: "Set up a sync-based git repo for personal configs, scripts, and notes — the safe, symlink-free approach for non-developers."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [dotfiles, git, backup, env-management, secrets]
    related_skills: [github-auth, github-repo-management]
---

# Dotfiles Repo Setup (Sync-Based)

Set up a single git repository that tracks personal configuration files,
custom scripts, tool configs (Hermes, etc.), and knowledge notes — without
moving files from their application-expected locations.

## When to use

- User wants version control over their personal environment
- User is not a developer (doesn't use symlink-based dotfiles frameworks)
- User has multiple critical things to track: configs + scripts + notes
- User wants daily automatic backup to GitHub

## Architecture: Sync-Based (Not Symlink-Based)

| Feature | Sync-based (this skill) | Symlink-based |
|---------|------------------------|---------------|
| Working files stay put | ✅ Yes | ❌ Symlinks redirect them |
| Safe with iCloud paths | ✅ Yes | ❌ iCloud paths with spaces can break |
| Safe with app-fixed paths | ✅ Yes | ❌ ~/.hermes/ symlink may confuse Hermes |
| Changes auto-reflect | ❌ Need sync.sh | ✅ Yes, live symlinks |
| Rollback | ✅ git revert restores | ✅ git revert + re-link |

**Always prefer sync-based** for users who aren't comfortable managing
symlinks or who use apps with rigid path expectations (Obsidian iCloud
vault, Hermes ~/.hermes/, etc.).

## Directory Structure

```
~/dotfiles/
├── README.md         ← Purpose and workflow
├── .gitignore        ← Secrets, large files, OS junk, caches
├── sync.sh           ← One-command "capture current state"
├── daily-maintenance.sh  ← Optional: cron-able full cycle
├── home/             ← Shell configs (.zshrc, .gitconfig)
├── bin/              ← Custom scripts (~/.local/bin/)
├── hermes/           ← Hermes config.yaml + profiles + skills
│   ├── .env.template ← Stripped secrets for reference
│   └── config.yaml   ← WITH API KEYS REPLACED BY ENV VARS
├── notes/            ← Obsidian/notes vault (excludes large attachements)
```

## Step-by-Step

### 1. Create the repo and git init

```bash
mkdir -p ~/dotfiles && cd ~/dotfiles && git init
mkdir -p home bin hermes/skills hermes/profiles notes
```

### 2. Write .gitignore

Must exclude:

```gitignore
# Secrets — NEVER commit
.env
.env.*
auth.json
**/credentials.json
*.pem
*.key

# OS junk
.DS_Store
Thumbs.db

# Caches
*.log
*.tmp
__pycache__/
*.pyc

# Large binary attachements
notes/**/*.png
notes/**/*.jpg
notes/**/*.jpeg
notes/**/*.pdf
notes/**/*.xlsx
notes/**/*.docx
*.zip

# Tool caches
notes/.obsidian/workspace.json
hermes/sessions/
hermes/logs/
hermes/state.db
```

### 3. Write sync.sh

Sync.sh copies from actual locations into the repo (does NOT move anything):

```bash
#!/bin/bash
DOTFILES="$(cd "$(dirname "$0")" && pwd)"

# Config files
[ -f ~/.zshrc ] && cp ~/.zshrc "$DOTFILES/home/.zshrc"
[ -f ~/.gitconfig ] && cp ~/.gitconfig "$DOTFILES/home/.gitconfig"

# Scripts
[ -d ~/.local/bin ] && rsync -a --delete "$HOME/.local/bin/" "$DOTFILES/bin/"
[ -d ~/bin ] && rsync -a --delete "$HOME/bin/" "$DOTFILES/bin/"

# Hermes config
[ -f ~/.hermes/config.yaml ] && cp ~/.hermes/config.yaml "$DOTFILES/hermes/config.yaml"
[ -d ~/.hermes/skills ] && rsync -a --delete ~/.hermes/skills/ "$DOTFILES/hermes/skills/"
[ -d ~/.hermes/profiles ] && rsync -a --delete ~/.hermes/profiles/ "$DOTFILES/hermes/profiles/"

# Notes (exclude large attachements)
[ -d "$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/PKM" ] && \
  rsync -a --delete \
    --exclude='*.png' --exclude='*.jpg' --exclude='*.pdf' \
    --exclude='.obsidian/workspace.json' \
    "$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/PKM/" \
    "$DOTFILES/notes/"

echo "Sync complete. Run: git add . && git commit"
```

### 4. STRIP API KEYS before committing

**This is the most critical step.** Config files often contain live API
keys. Check and replace them before the first commit:

```bash
grep -n 'api_key\|token\|secret' hermes/config.yaml
```

Replace real keys with environment variable placeholders:

```yaml
# Before:
api_key: sk-real-key-here

# After:
api_key: ${PROVIDER_API_KEY}
```

Also create `.env.template` so anyone cloning knows what vars to set:

```bash
cat > hermes/.env.template << 'EOF'
# Required env vars (copy to ~/.hermes/.env)
PROVIDER_API_KEY=sk-your-key-here
EOF
```

### 5. First commit and push to GitHub

```bash
cd ~/dotfiles
git add .
git commit -m "Initial commit: dotfiles"
gh repo create <user>/dotfiles --public --source=. --push
```

## Daily Maintenance Cron

Create a `daily-maintenance.sh` that does everything in one go:

```bash
#!/bin/bash
set -e

# 1. Update Hermes (safe to fail — network issues)
hermes update 2>&1 || true

# 2. Sync current state into dotfiles
cd ~/dotfiles
bash sync.sh

# 3. Commit and push
git add .
if ! git diff --cached --quiet; then
  git commit -m "Auto-update $(date +%Y-%m-%d)"
  git push
fi
```

Place this script at `~/.hermes/scripts/daily-maintenance.sh` (cron's
script path MUST be under `~/.hermes/scripts/`). Then create the cron:

```bash
# Using the cronjob tool:
cronjob(
  action="create",
  name="Daily maintenance (hermes update + dotfiles sync)",
  no_agent=True,
  schedule="0 4 * * *",  # every day at 4am
  script="daily-maintenance.sh"
)
```

## Pitfalls

1. **API keys in git history are forever.** If you accidentally commit
a real key, rotate it immediately on the provider's website. There is
no way to "un-commit" a leaked key.
2. **`gh repo create` requires authentication first.** Run the gh auth
flow (see github-auth skill) before trying to push.
3. **iCloud paths with spaces.** Always use double quotes around
`~/Library/Mobile Documents/...` paths. Backslash escaping breaks in
some contexts.
4. **`gh auth login` times out in foreground terminal.** The device code
flow waits for the browser — always run in background PTY mode
(background=true, pty=true, notify_on_complete=true) and use the
process tool to read the device code for the user.
5. **sync.sh is not a backup of binaries.** It copies config files
and scripts, not installed applications (brew casks, npm packages, etc.)
6. **Large Obsidian vaults.** If the vault has many embedded images,
the git repo will bloat. The .gitignore excludes binary attachements.
Consider git LFS if you need them tracked.

## Verification

```bash
# Check no secrets leaked into the repo
git diff --cached | grep -i 'api_key\|token\|secret'

# Check repo size
du -sh ~/dotfiles/

# Check remote works
git remote -v && git ls-remote --heads origin

# Check cron is scheduled
hermes cron list
```
