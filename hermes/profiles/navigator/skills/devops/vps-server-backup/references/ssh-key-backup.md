# SSH Key Backup (2026-06-29)

Session: The user asked which SSH keys are involved with their VPS and whether they need backup.

## Keys involved

| Key | Location | Purpose | Backup? |
|:----|:---------|:--------|:-------:|
| **User's private key** | `~/.ssh/id_ed25519` (or `id_rsa`) | SSH to VPS + GitHub auth | ✅ **Must backup** |
| VPS host keys | `/etc/ssh/ssh_host_*` (on VPS) | Server identity | ❌ Irrelevant if VPS lost |
| GitHub token | `gh auth` (macOS keyring) | GitHub CLI auth | ✅ Already in keyring |

**The private key is shared** — the same key authenticates to both the VPS and GitHub. If lost, both access paths break.

## Backup procedure

### Copy files (no encryption — for immediate safety)

```bash
mkdir -p ~/Downloads/ssh-backup
cp ~/.ssh/id_ed25519 ~/Downloads/ssh-backup/
cp ~/.ssh/id_ed25519.pub ~/Downloads/ssh-backup/
cp ~/.ssh/config ~/Downloads/ssh-backup/
```

### Encrypt (recommended)

Run this **in an interactive terminal** to set a password:
```bash
zip -e ~/Downloads/ssh-keys-backup.zip ~/Downloads/ssh-backup/id_ed25519
```

### Safe storage locations
- iCloud / OneDrive
- External drive / USB stick
- Bitwarden attachment (the vault itself is your password manager)

## Verifying the backup is usable

```bash
# Check key fingerprint matches what the VPS expects
ssh-keygen -l -f ~/Downloads/ssh-backup/id_ed25519
# Should match: ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI...
```

## Why NOT in dotfiles git repo

SSH private keys are sensitive credentials. Putting them in `~/dotfiles/` (a git repo pushed to GitHub) exposes them even if the repo is private. Best practice: manual encrypted backup to a separate storage medium.