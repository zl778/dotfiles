---
name: apple-notes
description: "Manage Apple Notes via memo CLI: create, search, edit."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [Notes, Apple, macOS, note-taking]
    related_skills: [obsidian]
prerequisites:
  commands: [memo]
---

# Apple Notes

Use `memo` to manage Apple Notes directly from the terminal. Notes sync across all Apple devices via iCloud.

## Prerequisites

- **macOS** with Notes.app
- Grant Automation access to Notes.app when prompted (System Settings → Privacy → Automation)

### Install memo

**Preferred method (Homebrew):**
```bash
HOMEBREW_NO_AUTO_UPDATE=1 brew tap antoniorodr/memo && HOMEBREW_NO_AUTO_UPDATE=1 brew install antoniorodr/memo/memo
```

**Fallback (manual from source)** — use when brew fails due to outdated Command Line Tools or other brew errors:
```bash
cd ~/Downloads
curl -sL "https://github.com/antoniorodr/memo/releases/download/v0.6.0/memo-0.6.0.tar.gz" -o memo-0.6.0.tar.gz
tar xzf memo-0.6.0.tar.gz
cd memo-0.6.0
python3 -m venv memo_venv
source memo_venv/bin/activate
pip install -e .
# Create symlink so PATH finds it:
mkdir -p ~/bin
ln -sf "$PWD/memo_venv/bin/memo" ~/bin/memo
```

### Related Dependencies

- `fzf` is used for interactive selection (`memo notes -e`, `-d`, `-m`). If missing, these commands fail silently or return empty. Install: `brew install fzf`

## When to Use

- User asks to create, view, or search Apple Notes
- Saving information to Notes.app for cross-device access
- Organizing notes into folders
- Exporting notes to Markdown/HTML

## When NOT to Use

- Obsidian vault management → use the `obsidian` skill
- Bear Notes → separate app (not supported here)
- Quick agent-only notes → use the `memory` tool instead

## Quick Reference

### View Notes

```bash
memo notes                        # List all notes
memo notes -f "Folder Name"       # Filter by folder
memo notes -s "query"             # Search notes (fuzzy)
```

### Create Notes

```bash
memo notes -a                     # Interactive editor (opens vim/nano)
memo notes -a -f "Folder Name"    # Create note in a specific folder
```

**Non-interactive creation** (for automation / CI / agent usage):
The `-a` flag opens the system `$EDITOR`. To create a note without interactive input, use a wrapper script as EDITOR:

```bash
# 1. Prepare content in a temp file
cat > /tmp/note.md << 'EOF'
Note Title

Your note body here...
EOF

# 2. Create with EDITOR pointing to a cp wrapper
cat > /tmp/memo_wrapper.sh << 'SCRIPT'
#!/bin/bash
cp /tmp/note.md "$1"
SCRIPT
chmod +x /tmp/memo_wrapper.sh
EDITOR=/tmp/memo_wrapper.sh memo notes -a -f "Notes"
```

### Edit Notes

```bash
memo notes -e                     # Interactive selection to edit
```

### Delete Notes

```bash
memo notes -d                     # Interactive selection to delete
```

### Move Notes

```bash
memo notes -m                     # Move note to folder (interactive)
```

### Export Notes

```bash
memo notes -ex                    # Export to HTML/Markdown
```

## Pitfalls

- **`-a` does NOT accept a title argument.** `memo notes -a "My Title"` will error with `Got unexpected extra argument`. The `-a` flag is purely boolean — it opens the system editor. Use the EDITOR trick above to create notes non-interactively.
- **Editor defaults to vim.** If vim is not desired, set `$EDITOR` to nano or your preferred editor.
- **fzf is required for interactive selection.** `memo notes -e`, `-d`, and `-m` fail silently without `fzf`. Install: `brew install fzf`.

## Limitations

- Cannot edit notes containing images or attachments
- Interactive prompts require terminal access (use pty=true if needed)
- macOS only — requires Apple Notes.app

## Rules

1. Prefer Apple Notes when user wants cross-device sync (iPhone/iPad/Mac)
2. Use the `memory` tool for agent-internal notes that don't need to sync
3. Use the `obsidian` skill for Markdown-native knowledge management
