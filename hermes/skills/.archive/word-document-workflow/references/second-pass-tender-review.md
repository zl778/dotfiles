# Second-pass tender review reference

## Minimum audit set

- Current bid version (not just a prior “reviewed” copy)
- Invitation/tender document
- Technical specification and drawings/schedules
- Project scoring rubric
- Technical/commercial deviation tables
- Price/supply list workbooks
- Product data sheets, authorization letters, type-test/certification reports

## Evidence rules

1. Match the exact full model, including suffixes. `Model-A` evidence does not prove `Model-A-zr` unless the manufacturer explicitly confirms equivalence.
2. A performance guarantee is a bid commitment, not independent evidence. Mark it `承诺待证` when the supplied certificate/data sheet does not cover the quoted model.
3. If the quotation says 8-port but the specification requires 20-port, report a material conflict even if a later response table says 20-port and “no deviation.”
4. If the specification requires outdoor multimode fiber but the quotation lists single-mode transceivers or an unspecified fiber mode, report the link as unresolved; core count alone does not establish fiber mode.
5. If a technical specification contains an old budget-table value (for example IP55) but the detailed mandatory technical clause says IP56, apply the detailed mandatory clause and flag any bid/quote using IP55.
6. Empty personnel, experience, qualification, authorization, or deviation tables are not neutral; map them to the invitation's mandatory submission requirements and flag possible qualification failure.

## Compact output template

1. **评分** — component points, weighting formula, total, pass-line judgment.
2. **硬性否决风险** — qualification, price cap, mandatory certificates/authorizations, contradictory “no deviation,” submission completeness.
3. **逐项缺失/冲突** — clause, required value, bid value, evidence value, status.
4. **必须修改** — ordered P0/P1 list; each action should name the document/table/model that must be synchronized.

Use factual labels: `已满足`, `缺失`, `证据不足`, `型号错配`, `明确冲突`, `待书面澄清`. Do not invent missing values and do not edit files while performing this review.