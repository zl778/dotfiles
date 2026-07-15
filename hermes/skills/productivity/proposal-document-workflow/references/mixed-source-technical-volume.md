# Mixed-source technical-volume checklist

Use for a tender folder containing invitation requirements, a legacy technical specification, and A/B/C internal formatting rules.

## Source precedence

1. Invitation tender document and clarifications: submission structure, deadlines, price ceiling, evaluation and mandatory signatures.
2. Technical specification: scope, quantities, performance requirements, standards, installation, testing, acceptance, warranty and service.
3. Electronic tender platform: upload format, naming, size, signing and any blind-bid rules.
4. Internal A/B/C notes: only fill formatting gaps not covered by the project.
5. Old drafts and `OLD/` backups: context only; never source of truth.

## Mac legacy DOC extraction

- Check format with `file`.
- Try `textutil` first.
- If it says the file is not in the correct format, use:

```bash
/Applications/LibreOffice.app/Contents/MacOS/soffice --headless \
  --convert-to txt:Text --outdir /tmp/doc-extract /absolute/path/spec.doc
```

- Re-read the generated text; do not dispatch workers from a failed extraction.

## Before dispatch

Freeze a brief containing: project facts, scope, quantities, schedule, price ceiling, starred clauses, evaluation weights, unknowns, conflicts, no-fabrication rules, target word counts, title depth and allowed list/table forms.

## Conflict examples to flag

- Approximate technical estimate versus a stricter invitation price ceiling: never exceed the invitation ceiling.
- Different experience-year wording in the body and an attachment: prepare the stricter/longer period unless the purchaser clarifies.
- Technical specification contains copied unrelated systems or inconsistent device models: answer the current project scope, state “满足或不低于技术规格书，最终型号以确认后的供货清单/深化设计为准”, and do not invent site facts.

## Three-version review

Keep facts identical but use different organizing units:

- A: lifecycle engineering / formal narrative; no bullets if required.
- B: evaluation-response matrix / task packages; bullets and tables allowed.
- C: risk scenario → control target → response → verification loop; retain C layout even when anonymity is waived.

Check independently: body character count (excluding headings/tables if requested), first-level and second-level heading trees, evaluation-factor coverage, forbidden商务 content, unsupported facts, and actual DOCX formatting.
