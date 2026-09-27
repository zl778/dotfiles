# DOCX Colored Text — Full Working Example

This reference captures the complete workflow for inserting red (or any colored) text into an existing `.docx` document, specifically for Chinese bid/proposal technical documents. Derived from a real session where inline Python heredocs were blocked and a script-file workaround was required.

## Workflow

1. **Backup** the original document to `/tmp/` (avoid OneDrive interference).
2. **Read** the document content first via `read_file` (which auto-extracts DOCX to text) to understand structure.
3. **Write a complete Python script** to disk via `write_file`, then run it with `terminal`.
4. **Verify** by re-reading the saved file.

## Key API Patterns

### Append red text to end of existing table cell

```python
from docx.shared import RGBColor

def add_red_to_cell(cell, text, sep=" | "):
    last_p = cell.paragraphs[-1]
    run = last_p.add_run(sep + text)
    run.font.color.rgb = RGBColor(0xFF, 0x00, 0x00)
    run.font.size = Pt(10.5)
```

### Insert a new paragraph after a specific existing paragraph

`python-docx` has `insert_paragraph_before()` but **no** `insert_paragraph_after()`. Use `deepcopy` of the source paragraph element + `addnext()` to preserve style, alignment, and numbering:

```python
from copy import deepcopy
from docx.text.paragraph import Paragraph
from docx.oxml.ns import qn

def insert_paragraph_after(paragraph):
    new_p_elem = deepcopy(paragraph._element)
    for child in list(new_p_elem):
        if child.tag == qn('w:r'):
            new_p_elem.remove(child)
        elif child.tag not in (qn('w:pPr'),):
            new_p_elem.remove(child)
    paragraph._element.addnext(new_p_elem)
    return Paragraph(new_p_elem, paragraph._p.getroottree().getroot())

def add_red_paragraph_after(paragraph, text, bold=False, size=11):
    from docx.shared import RGBColor, Pt
    new_p = insert_paragraph_after(paragraph)
    run = new_p.add_run(text)
    run.font.color.rgb = RGBColor(0xFF, 0x00, 0x00)
    run.font.size = Pt(size)
    run.font.name = '宋体'
    if bold:
        run.font.bold = True
    # Set East Asian font
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

**Important**: After `addnext()`, the inserted paragraph does NOT appear at a stable index in `doc.paragraphs`, so save references to the paragraph objects you need to insert after.

### Replace table cell content with colored multi-paragraph text

```python
# Clear existing runs
for p in cell.paragraphs:
    for run in p.runs:
        run.text = ""

# Write first line
first_p = cell.paragraphs[0]
run = first_p.add_run("拟定，以下为投标基准配置")
run.font.color.rgb = RGBColor(0xFF, 0x00, 0x00)

# Add subsequent lines as new paragraphs in the same cell
second_p = cell.add_paragraph()
run2 = second_p.add_run("详细配置清单...")
run2.font.color.rgb = RGBColor(0xFF, 0x00, 0x00)
run2.font.size = Pt(10)
```

### Find a table by multiple content matches (no stable ID)

```python
def find_table_by_content(doc, search_terms):
    for table in doc.tables:
        all_text = " ".join(cell.text for row in table.rows for cell in row.cells)
        if all(term in all_text for term in search_terms):
            return table
    return None
```

### Find a paragraph by text fragment

```python
def find_para_by_text(doc, text_fragment):
    for i, p in enumerate(doc.paragraphs):
        if text_fragment in p.text:
            return i, p
    return None, None
```

## Pitfalls Specific to Colored Text

- **Inline Python heredocs (`python3 << 'PYEOF'`) get blocked** when they involve the `docx` library. Always write the script file to disk first as a `.py` file under `/tmp/`, then run it.
- After adding a paragraph with `deepcopy` + `addnext()`, the new paragraph doesn't appear at a stable index in `doc.paragraphs` for subsequent steps. Do not rely on index-based lookup after insertion — save references to the paragraph objects, or re-locate them by text content.
- Table cells may contain multiple paragraphs. `cell.text` concatenates all of them. To target a specific paragraph within a cell, iterate `cell.paragraphs`.
- When replacing existing text in a table cell, `run.text = ""` clears content but the run remains; if you want an entirely fresh start, use a new `add_run()` after clearing.
- Font size: for body text use `Pt(10.5)` (五号); for fine print inside table cells `Pt(10)` is acceptable. Do not skip setting font size — inherited sizes may not carry the color property correctly.

## Full Script Skeleton

```python
#!/usr/bin/env python3
from docx import Document
from docx.shared import RGBColor, Pt

SRC = "path/to/your.docx"
BAK = "/tmp/your.docx_backup"

# 1. Backup
import shutil
shutil.copy2(SRC, BAK)

# 2. Load
doc = Document(SRC)

# 3. Manipulate — find paragraphs, tables, add red runs
# ... (use patterns above)

# 4. Save
doc.save(SRC)
print(f"Saved. Size: {os.path.getsize(SRC)} bytes")
```

## Verification

After saving, re-read the DOCX and confirm:

```python
doc = Document(SRC)
red_count = 0
for p in doc.paragraphs:
    for run in p.runs:
        if run.font.color.rgb == RGBColor(0xFF, 0x00, 0x00):
            red_count += 1
for ti, table in enumerate(doc.tables):
    for row in table.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                for run in p.runs:
                    if run.font.color and run.font.color.rgb == RGBColor(0xFF, 0x00, 0x00):
                        red_count += 1
print(f"Total red-colored runs: {red_count}")
```
