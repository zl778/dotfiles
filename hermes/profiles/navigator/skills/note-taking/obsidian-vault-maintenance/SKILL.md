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

## Batch tag operations

Useful for standardizing, renaming, or translating tags across the vault.

### 1. List all tags in use

```bash
# Via Obsidian CLI (requires Obsidian running)
~/bin/obsidian tags vault=<VaultName>

# Via rg (no Obsidian needed)
# Matches inline tags (#tag/path) — captures any non-whitespace chars including Chinese
rg -o '#[^\s#,:\[\]]+' '<vault>' --include '*.md' | sort | uniq -c | sort -rn

# Matches YAML frontmatter tags (- /tag/path)
rg -o '^  - /[^\s]+' '<vault>' --include '*.md' | sort | uniq -c | sort -rn
```

### 2. Count occurrences per tag

```bash
# Inline tag
rg -c --fixed-strings '#tag/path' '<vault>' --include '*.md' | grep -v ':0$'

# YAML frontmatter tag
rg -c --fixed-strings '/tag/path' '<vault>' --include '*.md' | grep -v ':0$'
```

### 3. Batch replace tags

**CRITICAL ORDER: replace from most-specific (deepest sub-tag) to least-specific (parent tag).**
If you replace `#a/生活` before `#a/生活/通信`, the latter becomes `#a/life/通信` and the second pass won't match.

**Pattern 1 — Inline tags** (written as `#tag/path` in note body):

```bash
find '<vault>' -name '*.md' -exec sed -i '' 's|#OLD/TAG/PATH|#NEW/TAG/PATH|g' {} +
```

**Pattern 2 — YAML frontmatter tags** (written as `- /tag/path` or `tags: [/tag/path]`):

```bash
find '<vault>' -name '*.md' -exec sed -i '' 's|/OLD/TAG/PATH|/NEW/TAG/PATH|g' {} +
```

Both patterns are independent — run both for full coverage.

### 4. Verify results

```bash
# Confirm no old tags remain
rg -c --fixed-strings '#OLD/TAG' '<vault>' --include '*.md' | grep -v ':0$'

# Confirm new tags exist
rg -c --fixed-strings '#NEW/TAG' '<vault>' --include '*.md' | awk -F: '{s+=$2} END {print s+0}'
```

### 5. Spot-check sample files

```bash
head -3 '<vault>/<path>/<file>.md'
```

### 6. Handle plan-only tags in index documents

Some tags exist only in a planning/index document (e.g., `标签系统-PARA架构.md`) but have zero actual notes using them.

**Check if a tag is actually used:**

```bash
# Exclude the index file itself from the count
rg -c --fixed-strings '#the/tag' '<vault>' \
  | grep -v '标签系统-PARA' | awk -F: '{s+=$2} END {print s+0}'
```

If count is 0, the tag exists only in the plan — no note replacement needed, just update the index file.

### Reference

See `references/batch-tag-rename.md` for a complete session example — covers both active tag conversion (Chinese→English, ~155 occurrences across ~90 files) and plan-only tags in index documents.

## Pitfalls

- iCloud vault path contains spaces — always quote or use file tools
- Obsidian `attachmentFolderPath` in app.json tells you where images are stored; don't delete images without checking if notes reference them
- The `.obsidian/` directory is the config folder — never modify it outside the user's explicit direction
- Untitled/unnamed notes may be transient drafts the user intended to fill later — present a categorized list before deleting
- **Obsidian CLI requires the app to be running** — `~/bin/obsidian tags vault=<Name>` fails silently if Obsidian is closed. Fall back to `rg -o` for offline tag listing.
- **Check tag usage before renaming** — Always run `rg -c --fixed-strings` first to confirm the tag actually exists in notes. Tags listed in planning documents may have zero usage.