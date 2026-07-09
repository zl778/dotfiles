---
name: word-document-workflow
description: "Work with Word documents (.doc/.docx): extract text, convert formats, and apply consistent document styling."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [word, docx, doc, documents, formatting, extraction, conversion]
---

# Word Document Workflow

Use this skill when the user gives you a Word document task: read a `.doc`/`.docx`, convert it, extract text, or standardize formatting for business documents such as bids, proposals, contracts, and technical specs.

## Trigger conditions

- Read or compare `.doc` / `.docx` files
- Extract text from Word documents for review or summarization
- Generate a `.docx` from Markdown or plain text
- Apply consistent styles to a document body
- Standardize a tender / proposal / contract template

## Recommended workflow

1. Identify the format
   - `.docx` → use `python-docx`
   - legacy `.doc` → prefer text extraction/conversion first

2. Read before editing
   - Inspect headings, styles, and section structure
   - Back up the original document before any destructive change

3. Choose the right path
   - View only: extract text to plain text/Markdown
   - Drafting: write in Markdown first, then convert to `.docx`
   - Formatting: edit the existing `.docx` styles rather than rewriting every paragraph

4. Verify after changes
   - Re-open the generated file
   - Confirm file size changed and headings/paragraphs still exist
   - Spot-check the first pages and style names

## Extraction and conversion choices

- `.docx` reading/editing: `python-docx`
- legacy `.doc` text extraction: `wvText` is a good first try on macOS
- Markdown → `.docx`: `pandoc`
- Complex style edits on `.docx`: use `python-docx`; if precise spacing/indent is needed, edit the underlying Word XML

## Formatting baseline for business正文

Typical body style for Chinese business documents:

- Chinese font: 宋体
- Default font: 宋体
- Font size: 小四 (12pt)
- Line spacing: 1.5
- Paragraph spacing after: 8 磅
- First-line indent: 2 characters
- Show style in style gallery: enable `quick_style`

## Pitfalls

- Do not assume `.doc` and `.docx` behave the same; old `.doc` often needs a conversion step.
- If a document already has mixed styles, prefer changing the body paragraph style and then reassign paragraphs to that style.
- For exact first-line indentation in Chinese business docs, character-based XML indentation can be more reliable than point-based indentation.
- Always keep a backup copy before bulk formatting changes.

## Reference

See `references/word-docs-macos.md` for a concise, reusable recipe covering legacy `.doc` extraction, `.docx` formatting, and Markdown-to-Word conversion.
