---
name: obsidian-vault-maintenance
description: Obsidian vault-wide administration tasks — scanning structure, backing up, and cleaning up empty/stale notes.
platforms: [macos, linux, windows]
---

# Obsidian Vault Maintenance

Use this skill for vault-level operations: scanning structure, creating compressed backups, and finding/cleaning empty or near-empty notes.

## Resolve vault path

```bash
ls ~/Library/Mobile\ Documents/iCloud~md~obsidian/Documents/
```

Or use `find ~ -maxdepth 5 -name ".obsidian" -type d` to locate vaults. Pass the resolved absolute path to file tools (do NOT use shell variables like `$OBSIDIAN_VAULT_PATH`).

## Scan vault structure

Combine `search_files` and `terminal` for a complete picture:

1. Count all files: `search_files(target="files", pattern="*", path="<vault>", limit=200)`
2. Count markdown notes: `search_files(target="files", pattern="*.md", path="<vault>", output_mode="count")`
3. Check directory layout: `terminal(command="find <vault> -maxdepth 2 -not -path '*/.obsidian/*' -not -path '*/.trash/*' | sort")`
4. Check enabled plugins: `read_file(path="<vault>/.obsidian/community-plugins.json")`
5. Check config: `read_file(path="<vault>/.obsidian/app.json")` (newFileFolderPath, attachmentFolderPath, etc.)

## Backup vault to Downloads

```bash
tar czf ~/Downloads/<VaultName>-$(date +%Y%m%d_%H%M%S).tar.gz <vault_dir>/
```

Verify: `ls -lh ~/Downloads/<VaultName>-*.tar.gz`

## Find empty / near-empty notes

Use terminal with wc to scan a directory:

```bash
cd "<vault>/<subdir>"
for f in *.md; do
  lines=$(wc -l < "$f" 2>/dev/null)
  chars=$(wc -c < "$f" 2>/dev/null)
  if [ "$lines" -le 2 ] && [ "$chars" -le 30 ]; then echo "EMPTY   $chars B  $f"
  elif [ "$lines" -le 4 ] && [ "$chars" -le 100 ]; then echo "NEAR-EMPTY $chars B  $f"
  fi
done
```

Categories for review:
- **EMPTY (0-4 B)** — deletion candidates (zero content)
- **NEAR-EMPTY with only image/link** — check with `read_file`, likely cleanup candidates
- **NEAR-EMPTY with actual snippet** — retains useful info, keep

Move to trash: Obsidian's trash is `<vault>/.trash/` (by default). Use `mv` to move files there.

## Pitfalls

- iCloud vault path contains spaces — always quote or use file tools
- Obsidian `attachmentFolderPath` in app.json tells you where images are stored; don't delete images without checking if notes reference them
- The `.obsidian/` directory is the config folder — never modify it outside the user's explicit direction
- Untitled/unnamed notes may be transient drafts the user intended to fill later — present a categorized list before deleting