---
name: Obsidian CLI Commands Reference
source: https://obsidian.md/help/cli (Obsidian 1.12.7)
---

# Obsidian CLI Command Reference

Every command below requires Obsidian.app to be running. Add `--copy` to any command to copy output to clipboard.

## General

| Command | Description |
|---------|-------------|
| `version` | Show Obsidian version |
| `reload` | Reload the app window |
| `restart` | Restart the app |

## File Operations

| Command | Key params |
|---------|------------|
| `read [file=<name>] [path=<path>]` | Read file (default: active) |
| `create name=<name> [content=...] [template=<name>] [open] [overwrite]` | Create a note |
| `append [file=<name>] content=... [inline]` | Append to file |
| `prepend [file=<name>] content=... [inline]` | Prepend after frontmatter |
| `open [file=<name>] [newtab]` | Open file |
| `move [file=<name>] to=<path>` | Move/rename file |
| `rename [file=<name>] name=<new>` | Rename (preserves extension) |
| `delete [file=<name>] [permanent]` | Delete (to trash by default) |
| `file [file=<name>]` | Show file metadata |
| `files [folder=<path>] [ext=<ext>] [total]` | List files |
| `folder path=<path>` | Show folder info |
| `folders [folder=<path>] [total]` | List folders |

## Daily Notes

| Command | Key params |
|---------|------------|
| `daily` | Open daily note |
| `daily:path` | Get daily note path |
| `daily:read` | Read daily note |
| `daily:append content=... [open] [inline]` | Append to daily note |
| `daily:prepend content=... [open] [inline]` | Prepend to daily note |

## Search

| Command | Key params |
|---------|------------|
| `search query=<text> [path=<folder>] [limit=<n>] [format=text|json] [case] [total]` | Search vault |
| `search:context query=<text> [path=...] [limit=<n>]` | Search with grep-style context |
| `search:open [query=<text>]` | Open search view |

## Tags

| Command | Key params |
|---------|------------|
| `tags [active] [file=<name>] [sort=count] [counts] [total] [format=json|tsv|csv]` | List tags |
| `tag name=<tag> [total] [verbose]` | Tag occurrences & files |

## Properties

| Command | Key params |
|---------|------------|
| `properties [active] [file=<name>] [name=<prop>] [sort=count] [counts] [total] [format=yaml|json|tsv]` | List properties |
| `property:read name=<prop> [file=<name>]` | Read a property |
| `property:set name=<prop> value=<val> [type=text|list|number|checkbox|date|datetime]` | Set a property |
| `property:remove name=<prop> [file=<name>]` | Remove a property |
| `aliases [active] [file=<name>] [total] [verbose]` | List aliases |

## Tasks

| Command | Key params |
|---------|------------|
| `tasks [file=<name>] [status="<char>"] [done] [todo] [verbose] [total] [format=text|json|tsv|csv] [daily]` | List tasks |
| `task [file=<name>] line=<n> [toggle] [done] [todo] [status="<char>"]` | Show/update a task |

## Links & Graph

| Command | Key params |
|---------|------------|
| `backlinks [file=<name>] [counts] [total] [format=json|tsv|csv]` | Show backlinks |
| `links [file=<name>] [total]` | Outgoing links |
| `unresolved [total] [counts] [verbose] [format=json|tsv|csv]` | Broken wikilinks |
| `orphans [total]` | Files with no incoming links |
| `deadends [total]` | Files with no outgoing links |

## Outline

| Command | Key params |
|---------|------------|
| `outline [file=<name>] [format=tree|md|json] [total]` | Show headings |

## Templates

| Command | Key params |
|---------|------------|
| `templates [total]` | List templates |
| `template:read name=<template> [title=<title>] [resolve]` | Read template |
| `template:insert name=<template>` | Insert into active file |

## Plugins & Themes

| Command | Key params |
|---------|------------|
| `plugins [filter=core|community] [versions] [format=json|tsv|csv]` | List plugins |
| `plugin id=<id>` | Get plugin info |
| `plugin:enable id=<id>` | Enable plugin |
| `plugin:disable id=<id>` | Disable plugin |
| `plugin:install id=<id> [enable]` | Install community plugin |
| `plugin:uninstall id=<id>` | Uninstall |
| `plugin:reload id=<id>` | Reload (dev) |
| `themes [versions]` | List themes |
| `theme [name=<name>]` | Get theme info |
| `theme:set name=<name>` | Set theme |

## Sync & Publish

| Command | Key params |
|---------|------------|
| `sync [on|off]` | Pause/resume sync |
| `sync:status` | Show sync status & usage |
| `sync:history [file=<name>] [total]` | Sync version history |
| `sync:read [file=<name>] version=<n>` | Read sync version |
| `sync:restore [file=<name>] version=<n>` | Restore sync version |
| `publish:list [total]` | List published files |
| `publish:add [file=<name>] [changed]` | Publish file |

## Vault

| Command | Key params |
|---------|------------|
| `vault [info=name|path|files|folders|size]` | Vault info |
| `vaults [total] [verbose]` | List known vaults |

## Developer Commands

| Command | Key params | Description |
|---------|------------|-------------|
| `devtools` | — | Toggle Electron dev tools |
| `dev:debug [on|off]` | — | Attach/detach CDP debugger |
| `dev:cdp method=<CDP.method> [params=<json>]` | — | Run CDP command |
| `dev:errors [clear]` | — | Show captured JS errors |
| `dev:console [limit=<n>] [level=log|warn|error|info|debug] [clear]` | — | Show console messages |
| `dev:screenshot [path=<filename>]` | — | Take screenshot (base64 PNG) |
| `dev:css selector=<css> [prop=<name>]` | — | Inspect CSS |
| `dev:dom selector=<css> [attr=<name>] [css=<prop>] [text] [inner] [all] [total]` | — | Query DOM |
| `dev:mobile [on|off]` | — | Toggle mobile emulation |
| `eval code=<javascript>` | — | Execute JS in Obsidian |

## Target a specific vault

Use `vault=<name>` or `vault=<id>` as the **first parameter**:

```bash
obsidian vault="PKM" daily:append content="- [ ] Task"
```

## Target a specific file

- `file=<name>` — resolves like a wikilink (no extension needed)
- `path=<path>` — exact vault-relative path, e.g. `path=folder/note.md`

## Vault targeting from Hermes

The user's PKM vault is:
```
~/Library/Mobile Documents/iCloud~md~obsidian/Documents/PKM/
```
Vault name: `PKM`
Use `vault=PKM` prefix in CLI commands.
