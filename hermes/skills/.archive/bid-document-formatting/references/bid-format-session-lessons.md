# Bid-format session lessons

## Reusable standard families

- **A**: basic ordinary-bid house standard; useful for quick drafting but not sufficiently strict for blind bids.
- **B**: normalized ordinary-bid standard; use for open technical/business/price volumes with an automatic TOC, heading styles, table rules, and a project override checklist.
- **C**: technical blind-bid standard; use only when the tender permits/requires it. No header/footer/page number by default, exact fixed line spacing, neutral formatting, and identity-information scanning.

These are alternatives, not settings to mix casually in one volume. A project may legitimately use B for business/price volumes and C for a technical blind volume.

## Numbering failure and recovery

A prior DOCX had `Heading` styles and `numPr` XML, but Word/LibreOffice did not visibly render the Chinese numbering. The reliable recovery was:

1. Keep real `Heading 1`–`Heading 3` styles for document structure.
2. Remove the ineffective/conflicting `numPr` from heading paragraphs.
3. Put visible prefixes directly in heading text (for example `一、`, `（一）`, `1.`) to guarantee cross-engine rendering.
4. Convert the DOCX with `/Applications/LibreOffice.app/Contents/MacOS/soffice`.
5. Use PDF text extraction and/or rendered page inspection to confirm headings and numbering are visible and not duplicated.

Do not stop at a style/XML inspection when the user reports that the file has “no headings” or “no structure”.

## Scoped technical-volume editing

When a combined document contains cover, TOC, business volume, and technical volume:

- locate the actual body marker (not merely a TOC entry such as “二、技术卷”);
- back up the original;
- preserve all non-empty text before the marker by comparing against the backup;
- add a section break when technical margins differ from business margins;
- apply formatting only after the marker;
- leave suspicious content untouched during a formatting-only request unless the user authorizes cleanup;
- report the section-specific margins, heading counts, table counts, and backup path.

## Blind-bid identity check

Search the technical body for bidder/company names, logos, contact details, staff names, phone numbers, email addresses, and distinctive company/project clues. A project owner name may not be the bidder identity; flag it for user confirmation rather than silently deleting it when preserving content is required.
