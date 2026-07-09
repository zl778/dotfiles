---
name: obsidian-note-conventions
description: "Define consistent Obsidian note-authoring conventions for frontmatter, aliases, stable tags, and note structure."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [obsidian, note-taking, frontmatter, aliases, tags, pkm]
    related_skills: [obsidian]
---

# Obsidian Note Conventions

Use this skill when creating or editing Obsidian notes and the user cares about note structure, discoverability, or consistent metadata.

## Core convention

Prefer a frontmatter block at the top of new notes.

Recommended shape:

```yaml
---
title: Note title
aliases:
  - Flexible alias 1
  - Flexible alias 2
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: guide
tags:
  - stable/namespace/tag
---
```

## How to use `aliases` vs `tags`

- Put flexible names, variants, and human-friendly search terms in `aliases`.
- Keep `tags` structured, stable, and easy to filter.
- Prefer a namespace-style tag for a note family when the user asks for organization.

Example for Hermes-related notes:
- `tags: [r/tools/hermes]`
- `aliases:` can hold phrases like `会话管理`, `多Agent`, `任务流`, or other retrieval-friendly labels.

## When to use this skill

- The user asks to create an Obsidian note
- The user asks to reorganize note metadata
- The user wants cleaner tags and more flexible aliases
- The user wants a consistent note index or directory page

## Recommended note structure

1. Frontmatter first
2. Clear H1 title
3. Short intro explaining what the note is for
4. Bulleted conventions, tables, or templates as needed
5. Link related notes using wikilinks

## Pitfalls

- Do not put too many unstable phrases into tags.
- Do not omit aliases when the user asks for flexible searchability.
- Do not invent a random tagging style per note family; keep one namespace convention.
- Do not bury frontmatter below the title.

## Reference

Session-specific examples and a reusable frontmatter template live in `references/frontmatter-conventions.md`.
