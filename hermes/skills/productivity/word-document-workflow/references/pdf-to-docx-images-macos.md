# PDF to DOCX Image Insertion (macOS Quartz + python-docx)

Renders PDF document pages to JPEG using macOS native CoreGraphics and inserts them into a Word DOCX via python-docx.

## Prerequisites

- macOS (uses Quartz/PDFKit via pyobjc)
- `python-docx` installed
- `pyobjc-framework-Quartz` installed (brings in Quartz, Cocoa, CoreGraphics)

## PDF to JPEG (first page, 150 DPI)

```python
import os
from Quartz import CoreGraphics as CG
from Quartz import PDFDocument, kPDFDisplayBoxMediaBox
import Cocoa

pdf_path = "/path/to/report.pdf"
out_path = "/tmp/report_page.jpg"

url = CG.CFURLCreateFromFileSystemRepresentation(
    None, pdf_path.encode('utf-8'), len(pdf_path.encode('utf-8')), False)
doc = PDFDocument.alloc().initWithURL_(url)
page = doc.pageAtIndex_(0)

bounds = page.boundsForBox_(kPDFDisplayBoxMediaBox)
w, h = int(CG.CGRectGetWidth(bounds)), int(CG.CGRectGetHeight(bounds))

scale = 150.0 / 72.0
rw, rh = int(w * scale), int(h * scale)

cs = CG.CGColorSpaceCreateDeviceRGB()
ctx = CG.CGBitmapContextCreate(None, rw, rh, 8, rw * 4, cs,
                                CG.kCGImageAlphaPremultipliedFirst)
CG.CGContextSetRGBFillColor(ctx, 1, 1, 1, 1)
CG.CGContextFillRect(ctx, CG.CGRectMake(0, 0, rw, rh))
CG.CGContextScaleCTM(ctx, scale, scale)
page.drawWithBox_toContext_(kPDFDisplayBoxMediaBox, ctx)

img = CG.CGBitmapContextCreateImage(ctx)

rep = Cocoa.NSBitmapImageRep.alloc().initWithCGImage_(img)
data = rep.representationUsingType_properties_(
    Cocoa.NSJPEGFileType,
    {Cocoa.NSImageCompressionFactor: 0.85}
)
data.writeToFile_atomically_(out_path, True)
```

## Insert JPEG into DOCX

```python
from docx import Document
from docx.shared import Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

d = Document("input.docx")

cap = d.add_paragraph()
run = cap.add_run("图1：检测报告（首页）")
run.font.color.rgb = RGBColor(0xFF, 0x00, 0x00)
run.font.size = Pt(10)
run.font.bold = True

img_para = d.add_paragraph()
img_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
pic_run = img_para.add_run()
pic_run.add_picture("/tmp/report_page.jpg", width=Cm(14))

target_para = d.paragraphs[target_idx]
for new_p in [cap, img_para]:
    new_p._element.getparent().remove(new_p._element)
    target_para._element.addprevious(new_p._element)

d.save("output.docx")
```

## Image-sizing notes

- Cm(14) → ~5.5 inches, ~2.5cm margins on both sides of A4
- Cm(16) → nearly full-width
- 150 DPI JPEG at ~1239x1754px yields 0.4–1.0 MB per page

## Multi-page batch rendering

```python
for page_idx in range(num_pages):
    page = doc.pageAtIndex_(page_idx)
    # ... render as above ...
    out_path = f'/tmp/pdf_images/{short}_p{page_idx+1:02d}.jpg'
    # ... save via NSBitmapImageRep ...
```

## Full appendix insertion pattern

```python
from docx import Document
from docx.shared import RGBColor, Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

d = Document("input.docx")

# Find the paragraph to insert BEFORE (e.g. the 结语 paragraph)
target = None
for p in d.paragraphs:
    if "target marker text" in p.text:
        target = p
        break

new_paras = []

# Heading 2 for appendix
h2 = d.add_paragraph()
r = h2.add_run("十、设备检测报告与认证资料附录")
r.font.bold = True
r.font.size = Pt(16)
r.font.color.rgb = RGBColor(0xFF, 0x00, 0x00)
h2.style = d.styles['Heading 2']
new_paras.append(h2)

# Sections: list of (heading_text, short_name, page_count)
sections = [
    ("10.1 产品A —— 检测报告", "product_a", 10),
    ("10.2 产品B —— 认证证书", "product_b", 1),
]

for title, short, num_pages in sections:
    h3 = d.add_paragraph()
    r = h3.add_run(title)
    r.font.bold = True
    r.font.size = Pt(14)
    r.font.color.rgb = RGBColor(0xFF, 0x00, 0x00)
    h3.style = d.styles['Heading 3']
    new_paras.append(h3)
    
    for pi in range(1, num_pages + 1):
        img_path = f'/tmp/pdf_images/{short}_p{pi:02d}.jpg'
        
        cap = d.add_paragraph()
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_cap = cap.add_run(f'第{pi}/{num_pages}页')
        run_cap.font.color.rgb = RGBColor(0xFF, 0x00, 0x00)
        run_cap.font.size = Pt(9)
        new_paras.append(cap)
        
        img_para = d.add_paragraph()
        img_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_pic = img_para.add_run()
        run_pic.add_picture(img_path, width=Cm(14))
        new_paras.append(img_para)

# Move all new paragraphs before target
for para in reversed(new_paras):
    para._element.getparent().remove(para._element)
    target._element.addprevious(para._element)

d.save("output.docx")
```

## Cleanup after insertion

If an earlier version of the appendix (e.g. first-pages-only) was already inserted, remove the old heading and old image paragraphs before adding the new full appendix. Find and remove them by text matching on heading strings and old image captions, then save.

## Versioning for bid documents

- Original: `投标文件技术部分_A.docx`
- v2 with content updates: `投标文件技术部分_A_v2_审核修正版.docx`
- v2 with images: still `_v2_审核修正版.docx` (same version, images appended)
- **Never overwrite the original file.** Always use `/tmp/` for intermediate backups.

## Pitfalls

- pyobjc modules are nested: use `from Quartz import PDFDocument, kPDFDisplayBoxMediaBox`
- `CGImageDestinationCreateWithURL` NOT available in Quartz pyobjc wrapper; use `Cocoa.NSBitmapImageRep` instead
- XML-created paragraphs lack `.part` attribute; do NOT call `.style = ...` on them. Use `d.add_paragraph()` then XML-move.
- When XML-moving paragraphs before a target, use `addprevious()` not `addnext()`. The order must be: add new_paras in reverse order using `addprevious()` so they appear in correct sequence.
- Rendering 48 PDF pages at 150 DPI takes ~3 minutes. Be patient.
- After adding images, the DOCX file grows significantly (e.g. 61KB → 17MB for 48 pages + 1 PNG). Warn the user about file size if they're on a slow network.
