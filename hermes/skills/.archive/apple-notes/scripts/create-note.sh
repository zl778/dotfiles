#!/bin/bash
# create-note.sh — Non-interactive Apple Notes creation
# Usage: ./create-note.sh "Note Title" "Note body text" [FolderName]
# Default folder: Notes

set -euo pipefail

TITLE="${1:?Usage: create-note.sh \"Title\" \"Body\" [Folder]}"
BODY="${2:-}"
FOLDER="${3:-Notes}"

TMPFILE=$(mktemp)
trap 'rm -f "$TMPFILE" "$WRAPPER"' EXIT

# Write note content
printf '%s\n\n%s\n' "$TITLE" "$BODY" > "$TMPFILE"

# Create EDITOR wrapper
WRAPPER=$(mktemp)
cat > "$WRAPPER" << 'SCRIPT'
#!/bin/bash
TMPFILE="'"$TMPFILE"'"
cp "$TMPFILE" "$1"
SCRIPT
chmod +x "$WRAPPER"

EDITOR="$WRAPPER" memo notes -a -f "$FOLDER"
echo "✓ Note '$TITLE' created in folder '$FOLDER'"
