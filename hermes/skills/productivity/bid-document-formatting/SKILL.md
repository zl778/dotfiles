---
name: bid-document-formatting
description: "Create, compare, audit, and apply reusable Word formatting standards for Chinese bid/proposal documents, including ordinary open bids and technical blind bids."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [bids, tenders, docx, word, formatting, blind-bid, headings, numbering, libreoffice]
---

# Bid Document Formatting

Use this skill when extracting formatting from a Chinese tender document, authoring a reusable formatting standard, comparing multiple standards, or applying a standard to a `.docx` while preserving content and document scope.

## Core principle

Separate three things in every report and implementation:

1. **Observed source formatting** — what the DOCX actually contains in its sections, styles, direct paragraph formatting, run formatting, numbering XML, tables, headers, and footers.
2. **Company default standard** — the reusable house rule chosen for future documents.
3. **Project override** — the specific tender document, clarification, electronic-trading-system requirement, or blind-bid rule that supersedes the company default.

The priority order is:

`具体招标文件/澄清答疑 > 电子交易系统 > 公司模板 > 一般排版习惯`.

Never present an observed inconsistency as a clean standard, and never apply a company default when the project specification overrides it.

## Workflow

1. Locate the exact source and target files. If names are ambiguous, inspect the directory and identify the real `.docx` rather than guessing.
2. Before destructive editing, create a same-directory backup with a descriptive suffix such as `.before-formatB.docx`.
3. Inspect the DOCX with `python-docx` and, when needed, unzip/XML inspection:
   - section count, page dimensions, margins, header/footer distances;
   - paragraph styles and actual style counts;
   - direct paragraph formatting and run-level fonts/sizes/bold/italic/underline;
   - `Heading 1`–`Heading 6` usage;
   - `numPr`, `abstractNum`, and `numId` numbering definitions;
   - table count, dimensions, style names, merged cells, and cell text formatting.
4. Produce a clear standard with separate columns/sections for source observation, company default, and project override. Record unresolved decisions explicitly.
5. When applying a standard to a DOCX, identify the exact scope marker (for example, the technical volume body) and modify only that scope. Preserve pre-scope text, tables, images, and business sections. If page settings must differ by scope, create a section break and apply margins only to the target section.
6. Apply styles and direct formatting consistently:
   - set East Asian font explicitly in XML (`w:eastAsia`), not just `font.name`;
   - set paragraph alignment, first-line/left/right indents, before/after spacing, and line-spacing rule explicitly;
   - format table cells separately from body paragraphs.
7. For ordinary/open bids, use a project-approved heading hierarchy and bind it to a Word multilevel list. For technical blind bids, default to no header/footer/page number, no identity-bearing content, and the exact line spacing/font rules in the tender.
8. **Visible numbering fallback:** do not assume a `numPr`-only list will render in both Word and LibreOffice. After applying numbering, convert to PDF and inspect extracted text or a rendered screenshot. If numbering disappears, remove the conflicting `numPr` and write visible numbering prefixes into heading text while retaining `Heading` styles. Recheck for duplicate numbers.
9. Reopen the modified DOCX, validate ZIP integrity, compare the pre-scope non-empty text against the backup, and convert it with LibreOffice using the macOS executable path when it is not on PATH:
   `/Applications/LibreOffice.app/Contents/MacOS/soffice`.
10. Verify the PDF, not only the XML: check page count, sample heading text, visible numbering, margins/section behavior, and obvious pagination problems. Report the output path, backup path, actual counts, and any remaining human decision.

## Ordinary bid vs technical blind bid

### Ordinary/open bid default

Use the project-approved values, commonly A4 portrait, a normal body font/size, first-line indent of two characters, 1.5-line spacing, visible headings, automatic TOC, optional header/footer/page number, and tables with readable fixed widths. A reusable company standard should distinguish the default from project overrides.

### Technical blind bid default

Treat the project rule as strict, not aesthetic:

- remove header/footer/page number unless explicitly permitted;
- do not include bidder name, logo, contact details, staff names, company-specific identifiers, or other clues that can reveal identity;
- default to the specified body/title font, fixed line spacing, zero paragraph spacing, and top-level page breaks;
- do not add a TOC unless the tender explicitly allows it;
- use neutral, consistent table and figure formatting;
- run an identity-information scan before delivery.

A project or owner name may still be ambiguous: do not silently remove it when content preservation matters. Flag it for user confirmation against the tender's blind-bid prohibited-information list.

## Heading and numbering rules

- Do not mix `一、`, `1.`, `1.1`, `（一）`, `（1）`, and `①` at the same level.
- Keep title numbering separate from ordinary body list numbering; body lists should not enter the TOC.
- Titles should normally have zero first-line indent; body paragraphs may use two-character first-line indent.
- For long documents, use Heading styles for the hierarchy and an automatic TOC only when the project permits/requires it.
- If a rendering engine fails to display a custom Chinese numbering format, prefer visible text prefixes plus Heading styles over a visually empty or duplicate automatic list.

## Content audit for supplier quotations

When reviewing a supplier quotation against an inquiry letter and a bill-of-materials workbook, perform a documentary compliance audit in addition to formatting review:

1. Identify the actual files by directory listing; supplier labels in the task may differ from filenames or workbook sheet labels. Record the resolved mapping (for example, company letter, brand, and source sheet).
2. Extract paragraphs and every table from all DOCX sources, and dump the relevant workbook sheet with formulas and displayed values. Build a requirement matrix with columns: requirement, supplier response, source evidence, status, and severity.
3. Recalculate every price subtotal and total independently. Check budget ceiling, tax/inclusion language, and whether installation, training, freight, warranty, and options are separately priced or explicitly included.
4. Treat a response marked “满足” as unsupported unless the quotation or source material contains evidence. Distinguish: (a) contradiction with source data, (b) omitted evidence, and (c) an unverified enhancement claim. Do not silently upgrade any of these to compliance.
5. Pay special attention to wording changes such as “扩容后最高” becoming “基础吞吐量”, optional hardware becoming configured hardware, and one-year versus three-year authorization text. Require an original manufacturer authorization/warranty document when the source text is internally inconsistent.
6. Check mandatory submission materials separately from technical compliance. An absent original authorization/agency certificate is a procedural compliance issue even if the product and price appear correct.
7. Report confirmed no-problem items explicitly: arithmetic, budget, company/brand/model consistency, option configuration, validity period, and service commitments. State when conclusions are documentary only and do not authenticate the physical product.

For this audit pattern, use a concise table with severity, location, specific discrepancy, and audit judgment, followed by price checks,重点事项, and no-problem items. Do not modify supplier files.

## Pitfalls

- `Normal` style defaults can disagree with actual run-level fonts. Always report both the style definition and actual display-oriented formatting.
- A style may be bound to a numbering definition while individual paragraphs use direct numbering or manual text prefixes. Inspect all three mechanisms.
- A `numPr` existing in XML is not proof that numbering is visible in Word/LibreOffice. PDF verification is mandatory.
- Page margins are section-level, not paragraph-level. If only the technical volume should change, split sections rather than changing the entire document.
- Do not use spaces or tabs to fake first-line indentation or cover alignment; use paragraph settings, tabs, borderless tables, or text boxes.
- Do not claim that business content was preserved merely because paragraph indices match; compare non-empty text before the scope marker against the backup, allowing for inserted section-break empty paragraphs.
- Do not remove suspicious or malformed technical text during a formatting-only task unless the user explicitly authorizes content cleanup.

## Support reference

See `references/bid-format-session-lessons.md` for the reusable lessons from the A/B/C standards and the visible-numbering failure/recovery path.
