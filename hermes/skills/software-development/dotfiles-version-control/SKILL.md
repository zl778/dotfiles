---
name: dotfiles-version-control
description: "Set up and manage a unified git repo for personal workstation config — dotfiles, CLI scripts, Hermes config, and notes (Obsidian PKM)."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [dotfiles, git, version-control, workstation-setup, backup]
    related_skills: [github-auth, github-repo-management, obsidian]
---

# Dotfiles Version Control

Manage personal workstation configuration under git — one unified repo
covering shell config, CLI scripts, Hermes Agent configuration, and
personal notes (e.g. Obsidian PKM vault). Uses a **sync-based approach**
(sync.sh copies actual files into the repo) rather than symlinks, so
applications keep their expected paths (iCloud, ~/.hermes/, etc.)
while git tracks a clean snapshot.

## When to use

- Setting up version control for personal config for the first time
- Migrating from ad-hoc backups to git-managed history
- The user wants a single repo covering dotfiles + tools + notes
- The user wants to be able to clone and set up a new machine quickly

## Prerequisites

- Git installed (check with `git --version`)
- GitHub account and authentication configured (see `github-auth` skill)
- No existing `~/dotfiles/` directory (or user ok with replacing)

## Repo Structure

```
~/dotfiles/
├── .gitignore                  # Excludes secrets, OS junk, binaries, cache
├── README.md                    # What this is and how to use it
├── sync.sh                     # One-command sync from actual locations
├── home/                        # Shell config + CLI scripts
│   ├── .zshrc                   # Copied from ~/.zshrc
│   ├── .gitconfig               # Copied from ~/.gitconfig
│   └── bin/                      # Copied from ~/.local/bin/ + ~/bin/
│       ├── my-script.py
│       └── ...
├── hermes/                      # Hermes Agent config snapshot
│   ├── config.yaml              # From ~/.hermes/config.yaml
│   ├── config.yaml.template      # De-templated (secrets replaced)
│   ├── profiles/                 # From ~/.hermes/profiles/
│   └── skills/                    # User-created skills only
├── notes/                       # Obsidian PKM vault snapshot
│   ├── 00_Inbox/
│   ├── 10_Projects/
│   ├── 20_Areas/
│   ├── 30_Resources/
│   └── 90_Archives/
└── .github/workflows/           # Optional: auto-sync Actions
```

## .gitignore Template

```gitignore
# Secrets
.env
auth.json
**/credentials.json

# OS junk
.DS_Store
Thumbs.db

# Cache & temp
*.log
*.tmp
__pycache__/
*.pyc
.venv/
node_modules/

# Large binary attachments (Obsidian)
notes/**/*.png
notes/**/*.jpg
notes/**/*.jpeg
notes/**/*.gif
notes/**/*.pdf
notes/**/*.mp4

# Hermes session DB (large, cache)
hermes/*.db
```

## sync.sh Logic

```bash
#!/bin/bash
# Sync actual file locations into ~/DOTFILES/ repo for git tracking
set -euo pipefail
DOTFILES="$HOME/dotfiles"

# 1. Shell config
cp "$HOME/.zshrc"      "$DOTFILES/home/.zshrc"
cp "$HOME/.gitconfig"  "$DOTFILES/home/.gitconfig"

# 2. CLI scripts
rsync -a "$HOME/.local/bin/" "$DOTFILES/home/bin/"
[ -d "$HOME/bin" ] && rsync -a "$HOME/bin/" "$DOTFILES/home/bin/"

# 3. Hermes config (safe files only — skip .env, auth.json)
cp "$HOME/.hermes/config.yaml"   "$DOTFILES/hermes/config.yaml"
rsync -a "$HOME/.hermes/skills/" "$DOTFILES/hermes/skills/"
rsync -a "$HOME/.hermes/profiles/" "$DOTFILES/hermes/profiles/"

# 4. Obsidian notes (text only, exclude attachments)
OBSIDIAN_VAULT="$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/PKM"
rsync -a --exclude='*.png' --exclude='*.jpg' --exclude='*.jpeg' \
  --exclude='*.gif' --exclude='*.pdf' --exclude='*.mp4' \
  --exclude='.DS_Store' \
  "$OBSIDIAN_VAULT/" "$DOTFILES/notes/"

echo "Sync complete. Run: cd $DOTFILES && git add -A && git commit"
```

## Workflow

### First-time setup

```bash
# 1. Create the repo
mkdir -p ~/dotfiles && cd ~/dotfiles && git init

# 2. Write .gitignore (see template above)

# 3. Run sync once to populate
bash sync.sh

# 4. First commit
git add -A
git commit -m "Initial commit: dotfiles + Hermes + notes"

# 5. Push to GitHub (optional but recommended)
gh repo create dotfiles --private --push --source=.
# Or manually:
git remote add origin git@github.com:<user>/dotfiles.git
git push -u origin main
```

### Daily use

```bash
cd ~/dotfiles && bash sync.sh && git add -A && git commit -m "daily sync"
# Or one-liner:
git -C ~/dotfiles add -A && git -C ~/dotfiles commit -m "auto: $(date +%Y-%m-%d)" 
```

### Restore on a new machine

```bash
git clone git@github.com:<user>/dotfiles.git ~/dotfiles

# Restore home config
cp ~/dotfiles/home/.zshrc ~/
cp ~/dotfiles/home/.gitconfig ~/
cp -r ~/dotfiles/home/bin/* ~/.local/bin/

# Restore Hermes config (after Hermes is installed)
cp ~/dotfiles/hermes/config.yaml ~/.hermes/

# Restore notes (point Obsidian vault to ~/dotfiles/notes/)
```

## Key Rules

1. **Do NOT use symlinks for ~/.hermes/ or Obsidian vault** — both are
   expected at fixed paths by their applications. The sync approach is
   safer.
2. **Secrets never enter git** — .env and auth.json go in .gitignore.
   Keep a config.yaml.template with placeholder values for reference.
3. **Sync.sh is the single source of truth for what's tracked** — add
   new sections to sync.sh, not ad-hoc cp commands.
4. **Text-only for notes** — exclude binary attachments from the repo
   (they bloat git history). Use git LFS or a separate backup for
   images/PDFs.
5. **Commit frequency** — daily or after significant config changes,
   not after every note edit. The script captures a snapshot.

## Pitfalls

- **macOS cp -R vs rm -rf** — restoring .app bundles: `cp -R` merges
  into existing directories without overwriting. Always `rm -rf` the
  target first, then `cp -R`. Verify with `md5 -q`.
- **Obsidian iCloud path has spaces** — always double-quote the path
  in scripts. Never backslash-escape spaces in shell variables — use
  `"$VAULT_PATH"`
- **.env and auth.json are Hermes-managed** — do not manually
  reconstruct them. Run `hermes auth add` or restore from a trusted
  backup outside git.
- **Old git config changes** — `git config --global url."git@github.com:".insteadOf
  "https://github.com/"` rewrites all HTTPS remotes to SSH. User may
  deny this — respect the denial and continue with manual remote setup.

## Related Skills

- `github-auth` — Set up SSH keys, gh CLI, and GitHub authentication
- `github-repo-management` — Create, clone, fork repos; manage remotes
- `obsidian` — Work with Obsidian vault (read, search, create notes)
