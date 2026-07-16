# Surgical DOCX update from supplementary materials

## Concrete session pattern (消防安全整改零星工程, Jul 2026)

The user had three existing DOCX technical volumes (A/B/C) and provided two supplementary sources:
- `标书A清单.xlsx` — a quotation sheet with 46 rows of device/spray-pipe items (model, brand, quantity, unit price, total)
- `标书A资料/` — product spec `.doc` files for NVR, camera, alarm, smoke detector, plus certification PDFs

The goal: update only the A-version DOCX with red-font marked content from these sources, without rewriting or regenerating the whole document.

### Step-by-step

1. **Read the XLSX with openpyxl** — `load_workbook(data_only=True)`, then `iter_rows(values_only=True)`. Note that `.xlsx` cells outside the visible A-H region may contain extra data (alternate model numbers, long product descriptions). Inspect all 17 columns, not just the first 8.

2. **Convert legacy .doc specs** — `textutil -convert txt -output /tmp/file.txt source.doc`, then `head -120` to sample. The `.doc` files contained full product datasheets with model-specific performance parameters.

3. **Map existing DOCX paragraphs** — Re-read the existing `python-docx` `Document()` paragraph by paragraph. Print index, style name, and first 130 chars. The target DOCX had 207 paragraphs and 8 tables. Key insertion points:
   - Paragraph 0037 (供货方案 — main device list)
   - Paragraph 0039 (NVR/storage description)
   - Paragraph 0041 (cable/cabinet specs)
   - Paragraph 0043 (spray-pipe materials)
   - Paragraph 0045 (power supply)
   - Table 7 (technical response matrix, row 9 — "具体型号和点位")

4. **Apply red-font content** — Use `RGBColor(0xFF, 0x00, 0x00)` on new runs. **Do not use `paragraph.insert_paragraph_after()` — this method does not exist in python-docx** (raises `AttributeError`). Instead, use `deepcopy` of the source paragraph's XML element + `addnext()`:

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
```

This preserves the source paragraph's style, alignment, and numbering. For table cells, append a new `Run` to the cell's last paragraph via `cell.paragraphs[-1].add_run()`.

**Important**: After `addnext()`, the inserted paragraph does NOT appear at a stable index in `doc.paragraphs`, so save references to the paragraph objects you need to insert after.

5. **Exclude prices** — The XLSX had unit prices and totals for every item (e.g., 摄像机 ¥1,300/台, 总价 ¥24,700). Only model numbers and quantities went into the technical volume; prices were left out of the technical DOCX.

6. **Verify** — After modification, re-read the DOCX, check file size increased (~61KB → ~68KB), count paragraphs with red runs, confirm backup exists, scan for any leaked price digits.

### Key tools

- `openpyxl` with `data_only=True` (formula evaluation is on)
- `textutil -convert txt` for legacy `.doc` product specs
- `python-docx` for reading and writing `.docx`
- `RGBColor(0xFF, 0x00, 0x00)` for red runs

### Pitfalls from this session

- The user renamed `主标资料` → `标书A资料` during the session. Rediscover the actual directory name before reading; old session context may have stale paths.
- The XLSX had hidden columns J–Q with alternate model numbers and cost analysis formulas. Always inspect all columns, not just the visible first nine.
- The product spec `.doc` files were not plain text; `textutil -convert txt` succeeded but the original `textutil -stdin` call failed because `-stdin` requires input from stdin, not a file argument.
- The user's `cd` command with Chinese characters in the path was blocked by the tool's shell metacharacter check. Always use absolute paths via `workdir` parameter or full path strings instead of `cd`.
