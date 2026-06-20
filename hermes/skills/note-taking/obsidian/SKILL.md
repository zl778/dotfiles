---
name: obsidian
description: Read, search, create, and edit notes in the Obsidian vault.
platforms: [linux, macos, windows]
---

# Obsidian Vault

Use this skill for filesystem-first Obsidian vault work: reading notes, listing notes, searching note files, creating notes, appending content, and adding wikilinks.

## Vault path

Use a known or resolved vault path before calling file tools.

The documented vault-path convention is the `OBSIDIAN_VAULT_PATH` environment variable, for example from `~/.hermes/.env`. If it is unset, use `~/Documents/Obsidian Vault`.

**macOS iCloud vault:** Many macOS users sync Obsidian via iCloud. The vault lives under:
```
~/Library/Mobile Documents/iCloud~md~obsidian/Documents/<VaultName>/
```
If both the env var and default path fail, search for `.obsidian` directories:
```bash
find ~ -maxdepth 5 -name ".obsidian" -type d
```
Each parent directory of a `.obsidian/` is a vault root.

File tools do not expand shell variables. Do not pass paths containing `$OBSIDIAN_VAULT_PATH` to `read_file`, `write_file`, `patch`, or `search_files`; resolve the vault path first and pass a concrete absolute path. Vault paths may contain spaces (especially the iCloud container path), which is another reason to prefer file tools over shell commands.

If the vault path is unknown, `terminal` is acceptable for:
1. Checking `OBSIDIAN_VAULT_PATH` env var
2. Checking `~/Documents/Obsidian Vault`
3. Probing the iCloud path via `find` for `.obsidian` directories (see above)
4. Listing the iCloud Obsidian documents: `ls ~/Library/Mobile\ Documents/iCloud~md~obsidian/Documents/`

Once the path is known, switch back to file tools. Do not hardcode vault path resolution steps into a note — record the resolved path in memory so future sessions know it immediately.

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

### iCloud path quoting pitfall

When the iCloud vault path is assigned in a shell script or tool, **do NOT use backslash-escaped spaces inside double quotes**:

```bash
# WRONG — backslashes inside double quotes are literal
WORD_FILE="/Users/liangzhu/Library/Mobile\ Documents/iCloud\~md\~obsidian/..."

# RIGHT — either no wrapping quotes with escapes, OR a single pair of quotes without escapes
WORD_FILE=/Users/liangzhu/Library/Mobile\ Documents/iCloud\~md\~obsidian/...
# or
WORD_FILE="/Users/liangzhu/Library/Mobile Documents/iCloud~md~obsidian/..."
```

Within double quotes `"…"` backslash `\` is a literal character, not an escape. This creates phantom directories named `Mobile\ Documents` (with a literal backslash in the name). When writing agent code or giving the user a script snippet, always prefer the clean single-quote-wrapped or no-escape form.

## Wikilinks

Obsidian links notes with `[[Note Name]]` syntax. When creating notes, use these to link related content.

## Tag system design

See `references/para-tag-system-design.md` for the workflow on designing and migrating a PARA + Decimal tag system for an Obsidian vault.

This covers:
- Discovery phase (analyzing current tags and vault structure)
- Common problems to look for
- PARA 4-quadrant design with numeric encoding (10-19 Projects, 20-49 Areas, 50-79 Resources, 90-99 Archives)
- Migration mapping from old to new tags
- Migration plan generation (categorize every note to target PARA folder)
- Batch migration execution (move files + add tags reliably)
- Large-file handling workarounds (heredoc, sed, Python scripts in /tmp)
