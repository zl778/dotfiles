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

### Style extraction and template normalization

When extracting a reusable format specification from an existing Chinese tender `.docx`, separate three layers instead of collapsing them into one rule:

1. Page/section settings: paper size, orientation, margins, header/footer distances, sections, and page breaks.
2. Style definitions: `Normal`, `Heading 1`–`Heading 4`, table styles, base styles, and their XML-level paragraph/font settings.
3. Direct formatting actually used by paragraphs/runs: effective font, font size, bold, alignment, indentation, spacing, and line spacing.

Report both the source observation and the proposed reusable standard. A source document may have `Normal` defaulting to Calibri while its actual Chinese runs use 宋体/仿宋; it may also have heading styles with one line-spacing definition while direct paragraphs use another. Do not label an observed mixture as a unified template rule.

Before applying the extracted format to other tenders, confirm the user's normalization choice when the source is inconsistent:
- exact visual reproduction, or
- style-preserving normalization into a clean template.

For the normalization path, explicitly choose one body font/size, one heading line-spacing rule, and a Word multilevel list bound to `Heading 1`–`Heading 4`. Keep manual numbering and space-based cover alignment out of the reusable standard unless the user explicitly wants a replica.

### Verification for format extraction

- Reopen the source and inspect both style XML and representative paragraph/run formatting.
- Convert Word internal units before reporting them (e.g., EMU/twips to mm or points) and sanity-check A4 dimensions and margins.
- Compare non-empty paragraph counts separately from all styled paragraphs; empty/special paragraphs can make counts differ.
- Record table count, row/column dimensions, merged cells, widths, borders, cell padding, header repetition, and pagination separately; do not infer precise table geometry from the table style name alone.
- Save the extraction as a Markdown report, then re-read the saved report and audit it for contradictions before using it as a template specification.

### Tender-format variants and project overrides

Maintain separate format specifications instead of collapsing every tender into one universal rule:

- General company baseline (e.g. format A/B): can use automatic TOC, page numbers, unified Heading styles, and a standard body style.
- Technical blind-bid baseline (e.g. format C): treat anonymity as a hard constraint; default to no header/footer/page numbers/TOC, no bold/color/italic/underline, and no company/person/project-identifying content.
- Project-specific requirements always override the company baseline. Before editing a document, create a compact format override table recording the tender clause/page, the company default, and the final value.

For blind bids, verify at minimum: A4/orientation/margins, fixed line spacing and zero paragraph spacing, title numbering/indentation, whether a cover or TOC is allowed, prohibited identity clues, table/figure text size, pagination, metadata, and PDF output. Do not import normal明标 conventions such as logos, named headers, page numbers, or decorative title styling into a blind-bid document.

### Cross-profile worker dispatch for tender-format notes

When the user asks a named Hermes worker such as `wukong` or `writer` to produce a format note:

1. Invoke the named wrapper/profile, not an arbitrary `delegate_task` child.
2. Do not rely on the caller's current shell directory; run `cd <absolute project path> && <worker> chat -q ...` and pass the source/output paths explicitly.
3. Tell the worker to read the existing format note, create only the new output file, and report an absolute path.
4. Verify the output independently from the coordinator by reading the file, checking its size/line count, and listing headings. A worker's self-report is not proof.
5. If a first attempt runs in `/Users/<user>` and cannot find the source, retry with the absolute project path; do not let it write a guessed file elsewhere.

### LibreOffice verification on macOS

A successful `python-docx` reopen validates the package/XML but not visual pagination. After formatting a `.docx`, also try a headless PDF conversion:

```bash
/Applications/LibreOffice.app/Contents/MacOS/soffice \
  --headless --convert-to pdf \
  --outdir /tmp/docx-verification \
  /absolute/path/input.docx
```

Do not assume `libreoffice` or `soffice` is on `PATH`; probe `command -v` and the known macOS application path. If conversion succeeds, record the PDF path and then inspect page count/text or render pages when those utilities are available. If the GUI app is installed but not on `PATH`, use the absolute `soffice` path rather than reporting that LibreOffice is unavailable.

### Pitfalls

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
