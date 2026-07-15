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
   - Inspect headings, styles, section structure, tables, headers/footers, and numbering XML
   - Back up the original document before any destructive change
   - Record both style definitions and actual paragraph/run direct formatting; do not collapse them into one claim

3. Choose the right path
   - View only: extract text to plain text/Markdown
   - Drafting: write in Markdown first, then convert to `.docx`
   - Formatting: edit the existing `.docx` styles rather than rewriting every paragraph
   - For a reusable company template, separate source observations from normalized template decisions; project-specific tender requirements always override the company standard

4. Numbering and hierarchy
   - Inspect both style-level numbering and paragraph-level `numPr`; a document may have a multilevel list bound to heading styles even when individual paragraphs have no direct `numPr`
   - Also detect hand-typed prefixes such as `1.` or `1、`; remove only confirmed duplicate prefixes before applying automatic numbering
   - Bind one Word multilevel list to `Heading 1`–`Heading 4` and keep body-item numbering separate from heading numbering

5. Verify after changes
   - Re-open the generated file with `python-docx`
   - Confirm page setup, paragraph/run styles, heading numbering XML, table count/content, and header/footer fields
   - Confirm file size changed and headings/paragraphs still exist
   - Prefer a real PDF/rendering spot-check when a renderer is available; if not, report that structural verification passed but visual pagination was not independently checked

## Extraction and conversion choices

- `.docx` reading/editing: `python-docx`
- legacy `.doc` text extraction: `wvText` is a good first try on macOS
- Markdown → `.docx`: `pandoc`
- Complex style edits on `.docx`: use `python-docx`; if precise spacing/indent is needed, edit the underlying Word XML

## Formatting baseline for Chinese tender documents

Use the project specification first. When no project-specific rule is provided and the goal is a reusable company template, use this normalized baseline:

- Chinese body font: 仿宋
- Latin/digits: Times New Roman or a project-specified font
- Body size: 12 pt (小四)
- Alignment: justified
- Line spacing: 1.5 or fixed 22 pt
- Paragraph spacing: 0 pt before/after
- First-line indent: 2 Chinese characters
- Heading indentation: 0; do not simulate alignment with spaces
- Heading numbering: one automatic multilevel list, not hand-typed prefixes
- Tables: preserve merges/content, then normalize cell font, alignment, borders, and repeated header rows

## Metadata cleaning

When delivering a `.docx` to a client or submission system, strip author, company, last-modified-by, and revision metadata. See `references/clean-docx-metadata.md` for a complete script with tag reference and verification steps.

## Pitfalls

- Do not assume `.doc` and `.docx` behave the same; old `.doc` often needs a conversion step.
- If a document already has mixed styles, prefer changing the body paragraph style and then reassign paragraphs to that style.
- For exact first-line indentation in Chinese business docs, character-based XML indentation can be more reliable than point-based indentation.
- Always keep a backup copy before bulk formatting changes.

## Reference

See `references/word-docs-macos.md` for a concise, reusable recipe covering legacy `.doc` extraction, `.docx` formatting, and Markdown-to-Word conversion.
