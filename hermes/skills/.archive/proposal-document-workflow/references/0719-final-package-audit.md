# Versioned Tender Final-Package Audit

Use this reference when a project keeps dated folders such as `标书0719` and a prior scoring note.

## Audit order

1. Rediscover the exact A/B/C DOCX files under the dated folder; do not assume the root-level or older filename is current.
2. Read the invitation and technical specification as the controlling source; treat old score notes as historical baseline only.
3. Reopen each DOCX with `python-docx`; inspect tables, paragraphs, core metadata, blank form fields, and the actual equipment list.
4. Compare three layers: equipment/quotation list, performance-guarantee matrix, and deviation table/body.
5. Score technical quality separately from preliminary eligibility.
6. Report the score, hard risks, contradictions, evidence gaps, and repair priority for each version.

## High-risk cross-checks

- Price must not exceed the tender ceiling. A technically strong version can still be rejected at preliminary commercial review.
- Confirm bidder name, total price, VAT rate, validity period, date, signature/seal fields, and qualification attachments are not blank.
- Recompute NVR storage. For 19 channels at 4Mbps continuously for 90 days, theoretical demand is approximately 73.872TB before RAID and filesystem overhead; 8×8TB is not an unconditional 90-day solution.
- Match device role to model: a thermal/visible-light camera is not an independent photoelectric smoke detector.
- Match cable/transceiver medium: 6-core outdoor multimode is not automatically satisfied by 12-core single-mode/single-fiber equipment.
- Match protection grade exactly: IP55 is not IP56.
- Treat a local siren as a local output device; APP push, video review, acknowledgement, reset, and logs belong to the controller/NVR/platform unless the device datasheet proves otherwise.
- Do not let a matrix say `无偏离` when the quoted model or available evidence contradicts the technical specification. Use `待厂家确认`, `需更换型号`, or `存在偏差`.

## Scoring report format

For each version report:

- 响应度 /40
- 逻辑性 /30
- 专业性 /30
- 技术估分 /100
- 是否达到技术80分线
- 商务/初审资格状态
- hard rejection risks
- must-fix items before submission

Keep historical and current scores visibly separate. A repair copy must be a sibling file; never overwrite the source artifact.