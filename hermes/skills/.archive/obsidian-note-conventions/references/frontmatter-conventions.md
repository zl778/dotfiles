# Frontmatter Conventions for Hermes Notes

Session-derived conventions for creating Obsidian notes in a stable, searchable format.

## Preferred header

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
  - r/tools/hermes
---
```

## User preference to preserve

- Use `aliases` for flexible search terms and near-synonyms.
- Keep `tags` tidy and stable.
- For Hermes-related notes, prefer the namespace tag `r/tools/hermes`.
- Put the flexible conceptual labels that would otherwise clutter tags into `aliases` instead.

## Notes that fit this pattern

- task templates
- role definitions
- worker registries
- model routing tables
- session-management rules
- index pages

## Writing rule

If the note is part of a Hermes knowledge family, start with frontmatter first, then write the H1 title and body.
