---
name: memory-source-capture
description: "Capture durable user facts from an authoritative local source such as an Obsidian note, then persist a concise, verified memory entry."
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [memory, obsidian, source-verification, durable-context]
    related_skills: [hermes-memory, obsidian]
---

# Memory Source Capture

Use this skill when the user asks Hermes to remember, update, or retain a durable fact and supplies a local source, note title, file path, or other authoritative reference.

## Core principle

Treat the user's named source as evidence to verify, not merely as a label to copy. The source is the detailed record; Hermes memory is a compact pointer plus the stable facts needed to avoid asking again.

## Workflow

1. Identify the durable fact and the requested scope.
   - Keep stable identity, preference, environment, infrastructure, or completed migration facts.
   - Do not store transient task progress, raw logs, or a full note dump.
2. Resolve the authoritative source before writing memory.
   - For an Obsidian title, search the known vault path by filename.
   - If multiple matches exist, inspect enough context to select the intended note.
   - Read the note and extract only facts that support the user's statement.
3. Draft a compact declarative memory entry.
   - Include the stable outcome, important system/device attributes, and the source's relative path.
   - Prefer one entry over several fragmented entries.
   - Use an absolute path only when it is operationally useful and stable; otherwise use a vault-relative path.
4. Check memory capacity before adding.
   - If the memory tool rejects the addition because of the character limit, consolidate in the same turn.
   - Remove exact duplicates, stale one-off facts, and procedural details already covered by skills.
   - Prefer `memory(operations=[...])` so cleanup and addition are atomic.
5. Verify the write result.
   - Confirm the memory tool reports success and note the resulting usage.
   - Do not claim completion after a rejected write.

## What belongs where

| Detail | Destination |
|---|---|
| Stable fact the agent must remember across sessions | `memory` or `USER.md` |
| Full installation log, commands, troubleshooting chronology | Authoritative Obsidian note |
| Repeatable capture procedure | This skill |
| Temporary task status | Current session, not memory |

## Pitfalls

- Do not record only “see note X” when a short stable summary would prevent future clarification.
- Do not copy a long installation log into memory.
- Do not add a new entry blindly when memory is near capacity; consolidate duplicates first.
- Do not treat a successful note lookup as proof that the memory write succeeded; verify both independently.
- If the source is unavailable, state that limitation instead of inventing note contents.

## Support reference

See `references/obsidian-memory-capture.md` for a concise decision table and verification checklist.
