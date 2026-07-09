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

## Obsidian URI (jump display)

For showing the user a note inside the Obsidian app (jump-to-display), use `obsidian://` URL scheme via the system `open` command. This is NOT a replacement for file-system tools — see `references/obsidian-uri.md` for syntax, per-platform commands, and the decision table of when to use URI vs file tools.

## Obsidian CLI (已验证连通)

Obsidian 1.12.7+ ships a CLI binary (`obsidian-cli`) that communicates with the running Obsidian app via IPC. It provides capabilities beyond raw filesystem access: searched indexes, link graphs, Sync control, properties, tasks, and `eval` for executing JavaScript inside Obsidian.

### 连通性验证

本用户环境已验证通过（macOS 26.5.1，Apple M5）：

| 项目 | 结果 |
|------|------|
| CLI 版本 | Obsidian 1.12.7 |
| 二进制路径 | `~/bin/obsidian` → `/Applications/Obsidian.app/Contents/MacOS/obsidian-cli` |
| 可用 Vault | PKM（主库，211 文件）、work、Obs_vault |
| PKM Vault 路径 | `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/PKM/` |
| read / search / tags / tasks | 全部正常工作 |

首次使用前确保 Obsidian **正在运行**，否则 CLI 命令会尝试启动 Obsidian（较慢）。

### Prerequisites & Setup

- Obsidian app **must be running** for CLI commands to work
- Enable CLI in Obsidian: **Settings → General → Command line interface** (toggle on)
- macOS auto-creates `/usr/local/bin/obsidian` symlink (requires admin dialog), OR create manually:
  ```bash
  ln -sf /Applications/Obsidian.app/Contents/MacOS/obsidian-cli ~/bin/obsidian
  ```
- Verify: `obsidian version`

### When to use CLI vs Filesystem

| Task | Approach | Reasoning |
|------|----------|-----------|
| Read/write a note's content | Filesystem (read_file/write_file/patch) | Fast, no IPC overhead, works with Obsidian closed |
| Search vault by keyword | Filesystem (search_files) | ripgrep is fast, no IPC overhead |
| **Backlinks/incoming links** | **CLI**: `obsidian backlinks file=NoteName` | Filesystem can't resolve link graph without parsing all files |
| **Tags with counts** | **CLI**: `obsidian tags counts` | Uses Obsidian's index cache, not raw YAML parsing |
| **Properties** | **CLI**: `obsidian properties` / `obsidian property:read name=X` | Reads from Obsidian's indexed metadata |
| **Tasks (with status filter)** | **CLI**: `obsidian tasks todo` / `obsidian tasks daily` | Indexed task view across vault |
| **Daily notes** | **CLI**: `obsidian daily:append content="..."` | Auto-resolves daily note path, appends cleanly |
| **Link graph queries** | **CLI**: `obsidian orphans`, `obsidian unresolved` | Filesystem would require full-vault link parsing |
| **Execute JS in Obsidian** | **CLI**: `obsidian eval code="app.vault.getFiles().length"` | **Only CLI can do this** — accesses Obsidian API (app.vault, app.metadataCache, etc.) |
| **Version diff (Sync/File Recovery)** | **CLI**: `obsidian diff file=Note from=2 to=1` | Accesses Obsidian's version history |
| **Bulk operations (batch create 10+ notes)** | Filesystem | No IPC overhead per call |
| **Plugin/Theme management** | **CLI**: `obsidian plugins`, `obsidian theme:set name=X` | CLI can toggle/install plugins |

### Key CLI commands

See `references/obsidian-cli-commands.md` for the full command reference. Most useful ones:

```bash
# Everyday
obsidian daily:append content="- [ ] Buy groceries"   # Add to daily note
obsidian search query="meeting notes"                  # Search vault
obsidian tasks todo                                     # List incomplete tasks
obsidian tags counts                                    # Tag cloud with counts
obsidian backlinks file=Note                            # Show backlinks
obsidian orphans                                        # Find orphaned notes

# Developer
obsidian eval code="app.vault.getFiles().length"        # Execute JS
obsidian dev:console                                    # View console logs
obsidian dev:errors                                     # View captured errors
obsidian plugin:reload id=my-plugin                      # Reload dev plugin
```

### Pitfalls

- **Obsidian must be running** — CLI connects via IPC to the desktop app. First command may launch Obsidian (slow).
- **CLI after app update** — if you updated Obsidian via a version-skewed installer (e.g. installer 1.9.14 with CLI 1.12.7), the CLI may not register correctly. Update to latest installer DMG, then re-enable CLI in Settings.
- **Updating Obsidian.app safely** — do NOT `rm -rf + cp -R` to replace .app bundles. macOS `cp -R` merges into existing directories, leaving old files behind. Use `ditto` instead:
  ```bash
  ditto "/Volumes/New Obsidian.app" /Applications/Obsidian.app
  ```
- **eval output** — `obsidian eval` returns raw JS return value serialized. For complex operations, print structured output from within the eval.
- **CLI symlink location** — `/usr/local/bin/obsidian` requires sudo. Put it in `~/bin/` (already in user PATH) to avoid admin prompts.

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
