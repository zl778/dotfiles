---
name: obsidian-note-authoring
description: Compose new Obsidian notes with consistent frontmatter and note properties, especially for retained/reference notes.
platforms: [linux, macos, windows]
---

# Obsidian Note Authoring

Use this skill when creating new notes in an Obsidian vault and you want them to be easy to search, reuse, and maintain.

This skill is about the content and structure of notes, not filesystem mechanics. Use the `obsidian` skill for vault path discovery, file creation, search, and link operations.

## When to use

- Creating a new retained note, reference note, index note, or project note
- The user wants the note to start with properties/frontmatter
- The note should be easy to sort, search, or cross-link later
- You are creating an AI workflow note, prompt template, or stable reference

## Default structure

For retained notes, start with frontmatter before the heading:

```md
---
title: Note Title
type: reference
created: 2026-07-08
tags: [ai, hermes]
source: chat
---

# Note Title

Body text...
```

## Suggested fields

Use only the fields that add value. Typical fields:

- `title`
- `type`
- `created`
- `updated`
- `tags`
- `source`
- `status`
- `project`
- `related`

## Rules of thumb

1. Put frontmatter first when the note is meant to be retained or referenced later.
2. Keep the body concise and scannable.
3. Use clear headings for sections that may be updated later.
4. Link related notes with `[[wikilinks]]` when useful.
5. If the user only needs a temporary scratch note, frontmatter can be omitted.

## Pitfalls

- Don't add too many required properties; keep the note lightweight.
- Don't invent rigid schemas for every note type.
- Don't use frontmatter for throwaway notes unless the user explicitly wants it.

## Template pointer

See `templates/frontmatter-note.md` for a reusable starter snippet.
