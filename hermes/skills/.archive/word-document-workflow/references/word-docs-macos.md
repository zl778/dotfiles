# Word docs on macOS

Concise recipe for common Word-document work.

## Read / extract

- `.docx` → use `python-docx`.
- Legacy `.doc` → try `wvText <input.doc> <output.txt>` first for plain-text extraction.
- If you need to draft from scratch, use Markdown and convert with `pandoc` to `.docx`.

## Edit / format

Recommended Chinese business-document body style:

- Chinese font: 宋体
- Default font: 宋体
- Font size: 小四 (12pt)
- Line spacing: 1.5
- Paragraph spacing after: 8 磅
- First-line indent: 2 characters
- Show style in style gallery: enable `quick_style`

Implementation note:

- For consistent body formatting, change the paragraph style once and apply it to body paragraphs.
- For exact first-line indentation, XML-based `w:firstLineChars` can be more reliable than point-based indentation.
- Keep a backup of the original `.docx` before bulk style edits.

## Convert

- Markdown → `.docx`: `pandoc input.md -o output.docx`
- After conversion, reopen and verify headings/body styles still look correct.
