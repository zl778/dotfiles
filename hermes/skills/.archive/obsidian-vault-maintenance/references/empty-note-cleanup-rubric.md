# Empty-Note Cleanup Rubric

Used during 2026-06-17 session on vault `PKM`.

## Thresholds (per note)

| Category | Lines | Bytes | Action |
|----------|-------|-------|--------|
| EMPTY | ≤ 2 | ≤ 30 | Delete candidate |
| NEAR-EMPTY | ≤ 4 | ≤ 100 | Inspect content |

## Content inspection checklist (for near-empty)

- **Only an embedded image** (`![[Pasted image ...]]`) — cleanup candidate, image may still be useful
- **Only links to other notes** (`[[Note]]` or `[[Note]]` link list) — index page, keep
- **Tags only** (`#tag/subtag`) — draft, cleanup candidate
- **Has actual useful snippet** (command, step, tip) — keep regardless of size
- **Frontmatter only** (YAML `---` block) — draft, cleanup candidate

## Additional files moved to trash (2026-06-17, PKM vault)

Move via `mv <file> <vault>/.trash/` (consistent with Obsidian `trashOption: local`).

**EMPTY (0 B):**
- pages/未命名.md
- pages/未命名 1.md
- pages/Moby Dick Or, The Whale by Herman Melville.md
- journals/2026_06_17.md

**NEAR-EMPTY (2-4 B):**
- pages/Untitled 2Untitled 1.md
- pages/Untitled 3.md

**Image-only (no text):**
- pages/日记 2025-11.md
- pages/excel定制化日志.md
- pages/SUM SUBTOTAL AGGREGATE 求和比较.md
- pages/SUM SUBTOTAL AGGREGGATE 总结.md
- pages/PureRef 操作快捷 截图.md

## Vault layout note

PARA structure (10 Projects, 20 Areas, 30 Resources, 40 Archives) exists but is empty. All notes live in pages/. Journals in journals/.