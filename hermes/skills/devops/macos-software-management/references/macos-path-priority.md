# macOS PATH Priority: Apple System vs Homebrew

## Problem

A CLI tool (e.g. `git`) is installed via Homebrew at `/opt/homebrew/bin/<tool>` but the default `which <tool>` still picks up Apple's system-built version at `/usr/bin/<tool>`.

## Root Cause

macOS PATH order (typical):

```
/usr/local/bin        ← position 4-5
/usr/bin              ← position 6-7  (Apple system tools)
/opt/homebrew/bin     ← position ~15  (Homebrew, appended by brew shellenv)
```

`/usr/bin` comes before `/opt/homebrew/bin` in the inherited PATH, so the Apple version wins even though Homebrew has a newer version installed.

## Fix: Symlink in /usr/local/bin

`/usr/local/bin` is before `/usr/bin` in PATH, so a symlink there takes priority:

```bash
sudo ln -s /opt/homebrew/bin/<tool> /usr/local/bin/<tool>
```

Verify:

```bash
which <tool>   # should show /usr/local/bin/<tool>
<tool> --version  # should show Homebrew version
```

Apple's original version remains at `/usr/bin/<tool>` and is unaffected.

## Real Example (from session)

```bash
# Before
$ which -a git
/usr/bin/git          # Apple Git 2.39.5
/opt/homebrew/bin/git # Homebrew Git 2.54.0

# Fix
$ sudo ln -s /opt/homebrew/bin/git /usr/local/bin/git

# After
$ which git
/usr/local/bin/git
$ git --version
git version 2.54.0
```

## Alternative: Adjust PATH Order

Update `.zprofile` so `brew shellenv` runs earlier, or rearrange PATH entries so `/opt/homebrew/bin` comes before `/usr/bin`. The symlink approach is more targeted and avoids changing shell init order which can have subtle side effects.

## Affected Common Tools

| Tool | Apple System Version | Homebrew Version |
|------|---------------------|-----------------|
| git | `/usr/bin/git` (~2.39) | `/opt/homebrew/bin/git` (~2.54) |
| python3 | `/usr/bin/python3` | `/opt/homebrew/bin/python3` |
| vim | `/usr/bin/vim` | `/opt/homebrew/bin/vim` |
| curl | `/usr/bin/curl` | `/opt/homebrew/bin/curl` |
| ssh | `/usr/bin/ssh` | `/opt/homebrew/bin/ssh` (via openssh) |

Check `which -a <tool>` to see if both versions exist.
