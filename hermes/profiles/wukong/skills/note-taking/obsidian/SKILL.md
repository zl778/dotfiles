---
name: obsidian
description: Read, search, create, and edit notes in the Obsidian vault.
platforms: [linux, macos, windows]
---

# Obsidian Vault

Use this skill for filesystem-first Obsidian vault work: reading notes, listing notes, searching note files, creating notes, appending content, and adding wikilinks.

## Vault path

Use a known or resolved vault path before calling file tools.

**Step 0 — Check user memory/profile first (fastest path):** Before searching the filesystem, check the user's persistent memory and profile for a recorded vault path via `memory(action='list')`. Users often inform the agent of their vault path in a prior session. This avoids an unnecessary filesystem search and handles non-standard vault locations (e.g. `~/Documents/GitHub/Obs_vault`).

**Step 1 — Check environment variable:** The documented vault-path convention is the `OBSIDIAN_VAULT_PATH` environment variable, for example from `~/.hermes/.env`. `terminal` is acceptable for checking this.

**Step 2 — Fallback to default path:** If unset, use `~/Documents/Obsidian Vault`.

File tools do not expand shell variables. Do not pass paths containing `$OBSIDIAN_VAULT_PATH` to `read_file`, `write_file`, `patch`, or `search_files`; resolve the vault path first and pass a concrete absolute path. Vault paths may contain spaces, which is another reason to prefer file tools over shell commands.

If the vault path is unknown, `terminal` is acceptable for resolving `OBSIDIAN_VAULT_PATH` or checking whether the fallback path exists.

**Common iCloud vault path:** Many macOS users sync Obsidian via iCloud. These vaults live under:
```
~/Library/Mobile Documents/iCloud~md~obsidian/Documents/<VaultName>/
```
Check this path *before* doing a broad filesystem search — it's the most common alternative to `~/Documents/Obsidian Vault`.

**Fallback search when neither env var, default path, nor iCloud path works:** If none of the known paths exist, search for `.obsidian` directories on the filesystem. The vault root is the *parent directory* of each `.obsidian` match. Use:
```
find <search_root> -maxdepth 4 -type d -name ".obsidian" 2>/dev/null | head -5
```
Start with `~/Documents` and expand scope (to `~`) if nothing found. The `.obsidian` directory itself is not the vault — its parent is.

**Multiple vaults found:** When the search returns more than one `.obsidian` match, check which is the *active* vault by comparing how many `.md` files exist under each parent (use `find <parent> -name "*.md" 2>/dev/null | wc -l`). Prioritize the vault with substantive content (10+ notes) over empty/stale vaults. If the user provides a hint ("pkm", "work", "personal"), use it as a subdirectory name filter under the iCloud path or Documents directory.

Once the path is known, switch back to file tools.

## Read a note

Use `read_file` with the resolved absolute path to the note. Prefer this over `cat` because it provides line numbers and pagination.

## List notes

Use `search_files` with `target: "files"` and the resolved vault path. Prefer this over `find` or `ls`.

- To list all markdown notes, use `pattern: "*.md"` under the vault path.
- To list a subfolder, search under that subfolder's absolute path.

## Search

Use `search_files` for both filename and content searches. Prefer this over `grep`, `find`, or `ls`.

- For filenames, use `search_files` with `target: "files"` and a filename `pattern`.
- For note contents, use `search_files` with `target: "content"`, the content regex as `pattern`, and `file_glob: "*.md"` when you want to restrict matches to markdown notes.

## Create a note

Use `write_file` with the resolved absolute path and the full markdown content. Prefer this over shell heredocs or `echo` because it avoids shell quoting issues and returns structured results.

## Append to a note

Prefer a native file-tool workflow when it is not awkward:

- Read the target note with `read_file`.
- Use `patch` for an anchored append when there is stable context, such as adding a section after an existing heading or appending before a known trailing block.
- Use `write_file` when rewriting the whole note is clearer than constructing a fragile patch.

For an anchored append with `patch`, replace the anchor with the anchor plus the new content.

For a simple append with no stable context, `terminal` is acceptable if it is the clearest safe option.

## Targeted edits

Use `patch` for focused note changes when the current content gives you stable context. Prefer this over shell text rewriting.

## Wikilinks

Obsidian links notes with `[[Note Name]]` syntax. When creating notes, use these to link related content.
