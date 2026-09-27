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

## OfficeCLI unified path (optional, verify before replacing established tooling)

For AI-oriented `.docx`, `.xlsx`, and `.pptx` automation, evaluate OfficeCLI as a unified CLI layer before adding another Python script. It is a single binary with DOM-like paths, structured JSON, batch operations, validation, HTML/PNG rendering, template merge, and resident mode. It can reduce glue code for Agent workflows, but it does not remove the need for Word/Excel or LibreOffice visual/compatibility review.

Recommended rollout:

1. Install and verify `officecli --version`.
2. Test on copies of one real tender `.docx` and one real equipment/quotation `.xlsx`; never start with the confirmed source.
3. Read structure with `view ... outline`, `get ... --json`, and `dump`; make narrow edits with `set`/`add`/`remove`.
4. Flush resident edits with `save`/`close` before a non-OfficeCLI reader or delivery step.
5. Run `validate`, then `view ... html` or `view ... screenshot`; reopen/read back key fields.
6. Compare output against current `python-docx`/`openpyxl` and actual Word/Excel for pagination, formulas, merged cells, headers/footers, fonts, and embedded objects.

For Hermes, start with direct terminal calls under a dedicated document workflow Skill/worker. Add OfficeCLI MCP only after CLI behavior and file-verification contracts are stable. See `references/officecli-evaluation.md` for the capability matrix, rollout plan, and Hermes task contract.
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

## Colored text and highlighting

Use `Run.font.color.rgb` from `python-docx` to add colored text to existing paragraphs or table cells:

```python
from docx.shared import RGBColor

# Append a red run to an existing paragraph
run = paragraph.add_run("new red text here")
run.font.color.rgb = RGBColor(0xFF, 0x00, 0x00)

# Set font size if needed
run.font.size = Pt(10.5)

# For table cells, get the last paragraph and add a run
last_p = cell.paragraphs[-1]
run = last_p.add_run(" | appended red text")
run.font.color.rgb = RGBColor(0xFF, 0x00, 0x00)
```

### Inserting a new paragraph after an existing one (preserving XML order)

`python-docx` has `insert_paragraph_before()` but **no** `insert_paragraph_after()`. The correct approach uses `deepcopy` of the source paragraph element + `addnext()`, which preserves the source paragraph's style, alignment, and numbering properties:

```python
from copy import deepcopy
from docx.text.paragraph import Paragraph
from docx.oxml.ns import qn

def insert_paragraph_after(paragraph):
    """Insert a new empty paragraph after the given paragraph using XML operations.
    Preserves paragraph properties (pPr) from the source paragraph."""
    new_p_elem = deepcopy(paragraph._element)
    # Clear content (runs) but keep paragraph properties (pPr — style, alignment, spacing, numbering)
    for child in list(new_p_elem):
        if child.tag == qn('w:r'):
            new_p_elem.remove(child)
        elif child.tag not in (qn('w:pPr'),):
            new_p_elem.remove(child)
    paragraph._element.addnext(new_p_elem)
    return Paragraph(new_p_elem, paragraph._p.getroottree().getroot())

def add_red_paragraph_after(paragraph, text, bold=False, size=11):
    """Insert a new red-text paragraph after the given paragraph."""
    from docx.shared import RGBColor, Pt
    new_p = insert_paragraph_after(paragraph)
    run = new_p.add_run(text)
    run.font.color.rgb = RGBColor(0xFF, 0x00, 0x00)
    run.font.size = Pt(size)
    run.font.name = '宋体'
    if bold:
        run.font.bold = True
    # Set East Asian font in XML
    rPr = run._r.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        from docx.oxml import parse_xml, nsdecls
        rFonts = parse_xml(f'<w:rFonts {nsdecls("w")} w:eastAsia="宋体"/>')
        rPr.append(rFonts)
    else:
        rFonts.set(qn('w:eastAsia'), '宋体')
    return new_p
```

**Important**: After `addnext()`, the new paragraph does NOT appear at a stable index in `doc.paragraphs` for subsequent `doc.paragraphs[i]` lookups. Save references to the paragraph objects you need to insert after, or re-locate them by text content.

### Replacing existing text in a table cell with colored text

```python
# Clear the cell's runs first
for p in cell.paragraphs:
    for run in p.runs:
        run.text = ""
# Then write your colored text into the first paragraph
first_p = cell.paragraphs[0]
run = first_p.add_run("replacement text")
run.font.color.rgb = RGBColor(0xFF, 0x00, 0x00)
# Add additional paragraphs to the same cell
second_p = cell.add_paragraph()
run2 = second_p.add_run("more detail")
run2.font.color.rgb = RGBColor(0xFF, 0x00, 0x00)
```

### Finding a table by its content (no stable ID)

```python
def find_table_by_content(doc, search_terms):
    """Find table whose combined cell text matches all search_terms."""
    for table in doc.tables:
        all_text = " ".join(cell.text for row in table.rows for cell in row.cells)
        if all(term in all_text for term in search_terms):
            return table
    return None
```

### Finding a paragraph by text fragment

```python
def find_para_by_text(doc, text_fragment):
    for i, p in enumerate(doc.paragraphs):
        if text_fragment in p.text:
            return i, p
    return None, None
```

## Metadata cleaning

When delivering a `.docx` to a client or submission system, strip author, company, last-modified-by, and revision metadata. See `references/clean-docx-metadata.md` for a complete script with tag reference and verification steps.

### PDF-rendered images in DOCX

See `references/pdf-to-docx-images-macos.md` for the complete workflow: render PDF pages to JPEG via macOS CoreGraphics, insert into DOCX with red-font captions, and XML-move before the target paragraph.

#### Multi-page PDF appendix pattern

When inserting a multi-page PDF report as image series:

1. Render ALL pages to JPEG first (not just page 1). Use `doc.pageAtIndex_(i)` in a loop.
2. Structure with Heading 2 (appendix title) + one Heading 3 per PDF file, each containing every page of that PDF.
3. Each page image gets a `第X/Y页` caption (red font, Pt(9), bold).  
4. Insert the entire appendix BEFORE the final "结语" paragraph (not after).
5. Use `d.add_paragraph()` → `run.add_picture(img_path, width=Cm(14))` → XML-move each paragraph before the target paragraph via `addprevious()`.
6. PNG images (product photos) follow the same pattern: one Heading 3, one image paragraph.

Example structure:
```
Heading 2: 十、设备检测报告与认证资料附录
├── Heading 3: 10.1 产品A — 检测报告 (10页)
│   ├── 第1/10页 [image]
│   ├── 第2/10页 [image]
│   └── ...
├── Heading 3: 10.2 产品B — 认证证书 (1页)
│   └── 第1/1页 [image]
└── ...
```

#### Versioning and backup conventions for bid documents

**CRITICAL: Do NOT overwrite the original file. Always save as a new versioned file.**

- Original: `投标文件技术部分_A.docx`
- First update: `投标文件技术部分_A_v2_审核修正版.docx`
- Subsequent updates: `_v3_`, `_v4_`, etc.

Before any modification:
1. Rediscover the exact source path and confirm the requested version exists.
2. Copy the source to `/tmp/` as a safety backup (`投标文件技术部分_A_v3_原始备份.docx`).
3. Copy the source to a new sibling versioned file before editing.
4. Write changes only to the NEW versioned file (never the original or the confirmed source).
5. Verify the source checksum/size is unchanged after editing and verify the new package independently.

This prevents OneDrive sync cache issues and preserves the audit trail of versions. If a mistake happens (original got overwritten), restore from the `/tmp/` backup immediately, then continue from a new versioned copy.

#### Performance guarantee value table for tender technical volumes

When a second-pass tender review identifies missing verifiable evidence, append a blue/red-marked `性能保证值表` as a new final section rather than scattering unsupported claims through the body. Use a six-column matrix:

`序号 | 系统/设备 | 招标要求/基准 | 投标性能保证值 | 偏差/复核说明 | 证明资料位置`

Include rows for quantities, principal models, key performance thresholds, storage/retention, network topology, control boxes, power redundancy, interlocks, testing/commissioning, manufacturer authorization, three-party approval, standards submission, training deliverables, schedule/warranty, and environmental boundary conditions. Keep the table evidence-oriented: each guarantee must point to the tender/spec clause, product data, test report, authorization, drawing, or commissioning record.

Never silently normalize source conflicts. If the quotation/list says `8-port` while the specification requires `20-port`, or says `IP55` while the specification requires `IP56`, write the specification value as the required guarantee and explicitly mark the listed item as a deviation requiring replacement or written clarification. Do not label it “满足” until resolved. If a product model's available data does not prove a required parameter, write a conditional verification/approval requirement rather than inventing a value. Never transfer specifications from one model to another: a V1W product sheet cannot prove the performance of a listed DH-HY-SAV849HA-zr, and a DH-HDW4443LD camera report cannot prove a DH-HFW4443LF-PV-AXYT-zr. Keep the listed model, evidence model, and tender-required model visibly separate; record model mismatches as a deviation or pending confirmation.

For a user-requested color mark, set every newly added heading, note, table header, cell run, and closing conclusion explicitly with `Run.font.color.rgb` (for blue: `RGBColor(0x00, 0x00, 0xFF)`). Add the section at the absolute end of the document, including after an existing image appendix. Reopen the DOCX and verify: new table row/column count, all new runs have the requested color, no new table run is uncolored, original version checksum/size is unchanged, core package passes `unzip -t`, and the source backup remains available. A large image-heavy DOCX may exceed a short LibreOffice conversion timeout; report that visual PDF pagination was not verified rather than fabricating a PDF result.

## Second-pass tender review (read-only)

Use this workflow when auditing a bid against an invitation, technical specification, scoring rubric, and supporting certificates. The deliverable is an evidence-based review, not a document edit.

1. Identify the exact bid version and freeze scope. Read the bid, invitation, technical specification, scoring rule, price/technical schedules, and supplied certificates. Do not rely on an earlier review report as the sole source of truth; use it only as a checklist and re-verify each finding against the current files.
2. Extract structure and text before judging. For `.docx`, inspect paragraphs, styles, tables, headers/footers, embedded images, and attachments. For legacy `.doc`, convert to text/PDF with LibreOffice when available, then preserve the source path and conversion result in the audit notes. For `.xlsx`, read all relevant sheets, especially performance, quotation, and item-list sheets.
3. Build a requirement-to-evidence matrix with columns: `spec clause | requirement | bid response | exact model/quantity | evidence file/page | status | risk`. Never treat a generic product sheet as proof for a different model, suffix, or variant. Keep tender-required model, quoted model, evidence model, and proposed substitute visibly separate.
4. Check hard gates before awarding soft points: qualification/permit documents, joint-bid restrictions, price cap, submission/validity requirements, mandatory authorization, mandatory type-test/certification, and declared deviations. Flag “no deviation” claims that conflict with the quotation or response table.
5. Check cross-document consistency mechanically: model, brand, quantity, unit, port count, fiber mode/core count, enclosure IP rating/material/thickness, power redundancy, storage duration, voltage, pressure, and regional point counts. A later performance table cannot silently repair a conflicting quotation or supply list; record both values and require a written clarification/replacement.
6. Score only after the matrix is complete. Use the project rubric exactly, show each component score and weighted arithmetic, and explain any score held back by an unresolved hard contradiction. If a prior score exists, state whether it was retained or recalibrated and why.
7. Report in the user's requested compact order: total and component scores; hard-veto risks; itemized missing/conflicting requirements with clause references; mandatory modification list. Clearly distinguish `缺失`, `证据不足`, `型号错配`, `明确冲突`, and `待书面澄清`. Do not modify the bid during review.

For a reusable checklist and a worked evidence-mismatch pattern, see `references/second-pass-tender-review.md`.

## Pitfalls

- **Never overwrite the original file.** The user has a strict OneDrive sync + file caching concern. Always write updates to a new versioned file (e.g. `原文件_v2_审核修正版.docx`). If you accidentally overwrite the original, immediately restore from `/tmp/` backup.
- **Inline Python heredocs (`python3 << 'PYEOF'`) may be blocked** by the runtime when they involve the `docx` library (imports or file I/O). Always write the script to disk first (`write_file` → path under `/tmp/`), then run it with `terminal`. This sidesteps the block cleanly.
- When adding a new paragraph after an existing one, use `after_para._element.addnext(new_p._element)` instead of relying on `doc.paragraphs` index ordering. The index position is unreliable immediately after insertion.
- Table cells can contain multiple paragraphs. Use `cell.paragraphs[-1]` to access the last paragraph for appending, or `cell.add_paragraph()` to start a new one.
- Do not assume `.doc` and `.docx` behave the same; old `.doc` often needs a conversion step.
- If a document already has mixed styles, prefer changing the body paragraph style and then reassign paragraphs to that style.
- For exact first-line indentation in Chinese business docs, character-based XML indentation can be more reliable than point-based indentation.
- Always keep a backup copy before bulk formatting changes. Use `/tmp/` for the backup so it does not interfere with OneDrive sync.
- After saving, verify by re-reading the file and checking that colored runs exist with `run.font.color.rgb == RGBColor(0xFF, 0x00, 0x00)`.
- XML-created paragraphs (via `deepcopy` + `addprevious`/`addnext`) lack a `.part` attribute and cannot have `.style` assigned. Use `d.add_paragraph()` instead for paragraphs that need style assignment.
- When inserting images before a target paragraph, use `addprevious()` to insert BEFORE the target, not `addnext()` (which inserts AFTER). Images + captions should be added as normal paragraphs at the end via `d.add_paragraph()`, then XML-moved as a batch before the target.

## Reference

See `references/word-docs-macos.md` for a concise, reusable recipe covering legacy `.doc` extraction, `.docx` formatting, and Markdown-to-Word conversion.

See `references/docx-colored-text.md` for a full working example script covering reading, table finding, paragraph insertion, table cell update, and backup workflow with colored text.
