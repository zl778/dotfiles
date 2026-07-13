# Obsidian → Hermes Memory Capture

## Decision table

| Situation | Action |
|---|---|
| User gives an exact note title | Search the resolved vault for the filename, then read it |
| User gives a path | Read that exact path and verify it exists |
| Several notes match | Inspect headings/frontmatter and choose the explicitly intended source |
| Note contains a long procedure | Keep the procedure in Obsidian; store only the durable outcome and a pointer |
| Memory write hits the limit | Batch-remove duplicates/stale entries and add the new fact atomically |
| Source cannot be found | Ask for clarification or report the limitation; do not infer contents |

## Verification checklist

- [ ] Source note was found using a concrete absolute vault path.
- [ ] Note content was read, not merely matched by filename.
- [ ] Memory entry is declarative, concise, and stable.
- [ ] Entry includes a useful vault-relative source path when applicable.
- [ ] Duplicate/stale memory entries were consolidated if capacity was tight.
- [ ] Memory tool returned success after the final write.
