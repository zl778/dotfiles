---
name: proposal-document-workflow
description: Produce bid/proposal/tender documents with multi-agent draft diversity and reliable Word formatting.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [proposal, tender, bid, docx, word, formatting, multi-agent, drafting, routing]
---

# Proposal Document Workflow

Use this skill when the user asks for bid/proposal/tender document work that combines:
- multiple draft variants from different workers/models
- directory outlines, technical sections, or response matrices
- Word `.doc` / `.docx` formatting and final document styling

## When to use

- Generate multiple different outlines for the same tender
- Ask different workers to produce stylistically distinct versions of the same document section
- Convert extracted requirements into a bid response structure
- Format the final content into a business-grade Word document
- Repair a Word document whose displayed font or spacing does not match the intended style

## Recommended orchestration pattern

1. Keep one primary Hermes as the coordinator.
2. Route the same scope to multiple workers when the goal is deliberate stylistic diversity.
3. Preserve the same factual scope, but vary:
   - section ordering
   - subheading granularity
   - emphasis on implementation vs. formal structure
   - wording style
4. Compare the outputs and keep the best structure or merge them into a final version.

Common role pairing:
- technical / implementation-heavy draft → engineer-capable worker
- formal / polished tender language → writer-capable worker

## Word-document workflow

### Read and extract
- `.docx` → use `python-docx`
- legacy `.doc` → prefer text extraction/conversion first; on macOS, `wvText` is a good first try
- If starting from a drafted outline, write it in Markdown first and convert with `pandoc`

### Format the final document
For Chinese business-document正文, a reliable baseline is:
- Chinese font: 宋体
- Default font: 宋体
- Font size: 小四 (12pt)
- Line spacing: 1.5
- Paragraph spacing after: 8 磅
- First-line indent: 2 characters
- Show style in style gallery: enable `quick_style`

### Verification
- Reopen the generated `.docx` after saving
- Confirm the displayed font/spacing, not just the XML
- Keep a backup before bulk formatting changes

### Content-quality check after worker output
- Worker content may contain internal reasoning text ("Reasoning", "Let me", "I need to", markdown reasoning boxes, `⚠ tirith` banners, or agent status output) that the worker's own `-Q` flag fails to suppress — especially with deepseek or openai-codex providers when the instruction is complex.
- After collecting each worker's output, scan the first ~10 lines for these patterns and strip them before insertion. A post-processing script using `read_clean()` is more reliable than re-running the worker.
- Stripping pattern: skip lines that match reasoning-prefix patterns (`Reasoning`, `Looking`, `Checking`, `Reading`, `Preparing`, `I need`, `I 'm`, `Let me`, `Thinking`) or that appear inside agent decoration borders (`┌─`, `└─`, `│`, `╭─`, `╰─`, `session_id:`). Start collecting from the first substantive line.
- wukong (openai-codex) tends to suppress reasoning well with `-Q` alone; writer (deepseek) and writer on openai-codex fallback may need: `-Q --provider openai-codex -m gpt-5.4-mini` plus in-query instruction "只输出正文，不解释，不要任何推理过程"。

## Pitfalls

- A Word document may visually substitute the intended Chinese font. If that happens, try the exact installed face name that Word renders correctly and verify after reopening.
- For stubborn formatting, set paragraph/run formatting directly on the body text instead of relying only on style definitions.
- Old `.doc` files often need extraction/conversion before editing.
- When one worker's default provider fails auth or is unavailable, rerun the same role with an explicit known-good `-m` / `--provider` override for that task rather than changing the whole architecture.
- **Security approvals interrupt multi-agent dispatch.** When dispatching parallel workers via `hermes -p <profile> chat -q "... " -Q > file`, the security/approval layer may block the command if it detects "spawning profiles". Do not claim completion; stop, inform the user, and wait for approval. After approval, verify each worker's output file exists before proceeding to merge.
- **Worker output timeout on large tasks.** Generating hundreds of lines of tender body text may exceed the default `hermes chat -q` timeout (typically 180s). Set `--timeout` to at least 600s, or split the task across multiple smaller queries (e.g., sections 1–3, then 4–7). Between 300–600 lines is the boundary where timeout starts to bite.
- **Backup incrementally.** Name backups `.bak`, `.bak2` etc. to preserve a chain of intermediate states. The coordinator should not delete the backups — let the user clean up if needed.

## Good use cases

- Generating two or more tender outlines for comparison
- Producing a formal version and a practical version of the same proposal
- Turning a tender spec into a directory structure and then into a formatted `.docx`
- Standardizing the body style of a bid document after conversion

## Reference

- `references/tender-routing-and-formatting-notes.md` — session-derived routing and formatting notes for multi-model bid drafting and Word font fixes
- `references/multi-worker-tender-dispatch-phases.md` — phased workflow for dispatching parallel workers (inspect→brief→dispatch→sanitize→insert→verify), including content-cleaning patterns and per-model output-behavior table
