---
name: macos-software-management
description: "Install, uninstall, and troubleshoot macOS applications — Homebrew cask management, finding all app-related files, cleaning up symlinks/config/shellrc, and handling macOS-specific app lifecycle."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [macOS, Homebrew, App-Management, Uninstall, Troubleshooting]
    related_skills: [hermes-update-manual, debugging-hermes-tui-commands]
---

# macOS Software Management

Install, fully uninstall, and troubleshoot macOS applications. On macOS, simply dragging an app to Trash often leaves behind symlinks, config directories, shell init lines, plists, and Docker sockets.

## When to use

- User asks to install/uninstall/reinstall a macOS app (desktop app, CLI tool, or service)
- Investigating "why is this app broken after a machine migration"
- Checking what VM/container software is installed

## Prerequisites

- macOS (verified on 26.5.1, Apple Silicon)
- Homebrew installed (`brew` on PATH)
- `sudo` access for system-level removal

## Finding Installed Apps

### Check common locations

```bash
# /Applications (user-facing desktop apps)
ls /Applications/ | grep -iE '<app-name>'

# ~/Applications (user-installed)
ls ~/Applications/ 2>/dev/null

# CLI tools
which <tool-name> 2>/dev/null

# Homebrew casks (desktop apps installed via brew)
brew list --cask 2>/dev/null | grep -iE '<app>'

# Homebrew formulae (CLI tools)
brew list --formula 2>/dev/null | grep -iE '<tool>'
```

### Find all app-related files

When uninstalling a macOS app, check these locations:

| Location | What's there |
|----------|-------------|
| `/Applications/<App>.app` | Main app bundle |
| `~/Library/Preferences/` | Per-user plists |
| `/Library/Preferences/` | System plists |
| `~/Library/Application Support/` | App data |
| `~/Library/Caches/` | Cached data |
| `~/Library/Containers/` | Sandboxed app data |
| `~/Library/LaunchAgents/` | Per-user background services |
| `/Library/LaunchDaemons/` | System background services |
| `/Library/LaunchAgents/` | System per-user services |
| `/Library/Receipts/` | Install receipts |
| `~/.<app>/` | Dotfiles in home directory |
| `/usr/local/bin/` | CLI symlinks |
| `/opt/homebrew/bin/` | Apple Silicon brew CLI path |
| `~/.zshrc`, `~/.zprofile`, `~/.bashrc` | Shell init lines |
| `/var/run/` | Runtime sockets/Docker sockets |

## Installing Apps

### Via Homebrew cask (desktop apps)

```bash
# Standard install
brew install --cask <app-name>

# Without auto-update (faster)
HOMEBREW_NO_AUTO_UPDATE=1 brew install --cask <app-name>
```

After install, the caveats may say "Open the app to finish setup." The user needs to do this manually for first-run onboarding.

### Via direct download

Use `web_search` to find the official download page, then `web_extract` or `browser_navigate` to follow the download link. After downloading, either mount a `.dmg` or copy the `.app` bundle:

```bash
# dmg mount
hdiutil attach /path/to/download.dmg
cp -R /Volumes/<App>/\<App\>.app /Applications/
hdiutil detach /Volumes/<App>

# Direct .app copy
cp -R ~/Downloads/\<App\>.app /Applications/
```

## Fully Uninstalling Apps

### Step 1: Check what's installed

Run a comprehensive sweep for app-related files across all the locations listed above.

### Step 2: Stop the app (if running)

```bash
# Check if running
pgrep -l -i '<app>'

# Stop via launchctl if it's a service
launchctl list | grep -i '<app>'
launchctl bootout gui/$(id -u)/<label> 2>/dev/null || launchctl stop <label>
sudo launchctl bootout system/<label> 2>/dev/null || sudo launchctl stop <label>

# Or just kill
pkill -i '<app>' 2>/dev/null
```

### Step 3: Remove app bundle

```bash
sudo rm -rf "/Applications/<App>.app"
```

### Step 4: Remove CLI symlinks

```bash
# Check what's symlinked
ls -la /usr/local/bin/ | grep -i '<app>'
ls -la /opt/homebrew/bin/ | grep -i '<app>'

# Remove (note: for brew-installed, just brew uninstall; for manual, rm directly)
sudo rm -f /usr/local/bin/<symlink-name>
```

### Step 5: Remove config and data directories

```bash
rm -rf ~/.<app>/          # dotfile config
rm -rf ~/Library/Preferences/<app>*   # plists
rm -rf "~/Library/Application Support/<app>"
rm -rf ~/Library/Caches/<app>*
```

### Step 6: Remove shell init lines

Check `~/.zshrc`, `~/.zprofile`, `~/.bashrc`, `~/.profile` for lines referencing the app and remove them.

### Step 7: Clean up stale sockets/symlinks

```bash
# Check run-time paths
ls -la /var/run/ | grep -i '<app>'
ls -la /tmp/ | grep -i '<app>'

# Remove stale Docker sockets if applicable
sudo rm -f /var/run/docker.sock  # only if managed by the removed app
```

### Step 8: Verify removal

```bash
which <tool-name> 2>/dev/null || echo "CLI removed"
ls "/Applications/<App>.app" 2>/dev/null || echo "App removed"
```

## Reinstalling Apps

After full uninstall, reinstall is clean:

```bash
HOMEBREW_NO_AUTO_UPDATE=1 brew install --cask <app-name>
```

After brew install, the caveat "Open the app to finish setup" is expected. The user should launch the app once to complete first-run initialization (agreements, permissions, etc.).

## Diagnosing PATH Priority Issues

On macOS, Apple ships system-built versions of common CLI tools (`git`, `python3`, `vim`, `curl`, `ssh`, etc.) in `/usr/bin/`. Homebrew installs its own versions in `/opt/homebrew/bin/`. Because PATH typically lists `/usr/bin/` before `/opt/homebrew/bin/`, the Apple version wins by default.

### Detect

```bash
# Check all available locations for a tool
which -a <tool>

# Check PATH order (lower number = higher priority)
echo "$PATH" | tr ':' '\n' | nl
```

If `which -a` shows both `/usr/bin/<tool>` and `/opt/homebrew/bin/<tool>`, and `/usr/bin/` comes first:

### Fix

Create a symlink in `/usr/local/bin/` (which is before `/usr/bin/` in PATH):

```bash
sudo ln -s /opt/homebrew/bin/<tool> /usr/local/bin/<tool>
which <tool>  # verify
<tool> --version  # verify version
```

Apple's original binary remains untouched at `/usr/bin/<tool>` — only the default resolution changes.

### Reference

See `references/macos-path-priority.md` for full details, real session example, and list of commonly affected tools.

## References

- `references/orbstack.md` — OrbStack-specific uninstall/reinstall procedures

## Pitfalls

- **macOS `.app` bundles are directories** — `rm -rf` not `rm`. Don't use `rm /Applications/Foo.app` without `-rf`.
- **Shell init persistence** — App installers often add lines to `.zshrc` or `.zprofile`. After removing the app, those lines cause benign `source: no such file` errors. Always clean them.
- **Docker socket orphan** — When OrbStack or a similar Docker engine is removed, `/var/run/docker.sock` becomes a dangling symlink. Docker CLI will try to use it and fail.
- **Brew vs manual installs** — Apps installed via `brew install --cask` leave behind symlinks in `/opt/homebrew/bin/`. Manual installs that create symlinks in `/usr/local/bin/` are separate — removing the brew cask does NOT clean manually-placed symlinks.
- **Hardlinks vs symlinks** — `ls -la` shows symlinks with `->`. Real files don't have `->`. Hardlinks look like regular files but share the same inode. Use `stat -f '%i'` to compare inodes.
- **NVM context matters** — when debugging Node-based CLI tools (Codex, etc.), NVM's npm reads the wrong prefix if `nvm.sh` isn't sourced first. Always `source ~/.nvm/nvm.sh` before running npm commands.
- **Apple system tools overshadow Homebrew installations** — `/usr/bin/` typically appears before `/opt/homebrew/bin/` in PATH, causing `which <tool>` to resolve Apple's built-in version even when Homebrew has a newer one installed. `which -a <tool>` reveals both. Fix with `sudo ln -s /opt/homebrew/bin/<tool> /usr/local/bin/<tool>` since `/usr/local/bin/` precedes `/usr/bin/`. See `references/macos-path-priority.md`.
