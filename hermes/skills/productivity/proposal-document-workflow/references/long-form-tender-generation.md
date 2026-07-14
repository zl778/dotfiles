# Long-form Tender Generation — Reusable Procedure

## Trigger
Use this procedure for multi-version Chinese tender sections above roughly 12,000 characters, especially when three Profiles must produce A/B/C Word outputs.

## Source freeze

1. Identify the main `.docx` and the project `规范/` directory by exact path.
2. List the relevant format files and extract the tender's evaluation table and service requirements.
3. Back up any existing draft before launching workers. In synced folders, a background worker may modify the draft after the coordinator has read it.
4. Build one compact brief containing project facts, scoring factors, mandatory service metrics, format rules, and explicit no-fabrication boundaries.

## Dispatch pattern

1. Send identical facts to each worker; vary only role/style/format.
2. Do not combine source reading, 15,000-character drafting, Word creation, and verification in one background query.
3. Prefer three bounded content phases per worker, around 3,000–6,000 characters each. Plain text/Markdown is more reliable than worker-side long `.docx` creation.
4. Keep prompts short and explicit: "只输出正文，不解释、不推理、不使用工具" when the worker is expected to return text. Use an absolute output path if asking the worker to write.
5. After each phase, independently check file existence, size, content, and character count. Empty logs and self-reported paths are not completion evidence.

## Coordinator assembly

1. Sanitize worker output before insertion: strip reasoning borders, `Reasoning`, session metadata, and tool-status text.
2. Assemble the final `.docx` centrally when workers cannot reliably complete long `python-docx` runs.
3. Keep A/B/C content factually aligned but apply each format's page setup, fonts, paragraph spacing, heading numbering, and table conventions.
4. For C with anonymity waived, retain C layout/numbering/font rules but do not apply anonymity restrictions.
5. Enforce a maximum of four heading levels. For C numbering, use `1.`, `1.1`, `1.1.1`, `1.1.1.1`; do not produce `1.1.`.

## Verification checklist

- Reopen each `.docx` with `python-docx`.
- Count non-empty body paragraph characters separately from table-cell characters; compare body count to the requested range.
- List headings and verify maximum level <= 4.
- Detect `numPr`/list styles and scan for project-bullet symbols when bullets are forbidden.
- Check every scored factor and mandatory technical requirement is present.
- Scan for excluded content: business evaluation, service performance, price evaluation, quotation, and unrelated qualification material.
- Verify file size is non-zero and conversion to PDF succeeds with the macOS LibreOffice absolute path when available.
- Report artifact paths and real verification results, not worker claims.

## Failure recovery

If a long worker run exits with an empty log or only reasoning text:

1. Run a minimal Profile write test to distinguish permission/tool access from generation-size failure.
2. Retry with direct text output and shell redirection, not worker-side `.docx` creation.
3. If direct generation remains unstable, use an existing verified project draft as the factual base, expand only with grounded technical operating procedures, and have the coordinator format and audit the final files.
4. Preserve a backup of the pre-expansion draft and do not report completion until independent verification passes.
