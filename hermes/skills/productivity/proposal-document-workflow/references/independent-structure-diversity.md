# Independent Structure Diversity for Multi-Model Tender Drafts

## Trigger

Use this when a user wants multiple tender versions that are genuinely different, not merely synonymically rewritten.

## Failure pattern

A shared `技术部分一级标题_*.md`, common chapter skeleton, or coordinator-designed parent目录 can make A/B/C look different in prose while their Word navigation panes remain identical. Changing Chinese numbering to Arabic numbering does not create structural diversity.

## Reliable sequence

1. Extract only the immutable facts and constraints from the tender: scored factors, mandatory service indicators, forbidden business/price scope, format rules, word-count definition, and maximum heading depth.
2. Dispatch each worker a short independent-outline task. Explicitly forbid reading old B/C正文 and forbid treating another version's outline as a template.
3. Compare outline trees before full drafting. Record each version's organizing unit:
   - work packages / deliverables / acceptance evidence;
   - system chains / event chains / lifecycle;
   - formal scored-factor response;
   - another worker-originated structure.
4. Reject near-duplicates by checking level-1 and level-2 heading overlap. Require at least a different dominant organizing unit and materially different second-level groupings.
5. Audit creative outlines for unsupported specifics. Remove invented brands, models, quantities, thresholds, performance seconds, extra locations, or unprovided scenario facts. Keep the structure and replace the detail with an evidence boundary such as “以招标文件和进场核查为准”.
6. Generate content in bounded chunks under each worker's own outline. Do not merge chunks by importing the other version's headings.
7. Assemble each DOCX with its own heading tree, then reopen it and inspect the actual Word navigation hierarchy. Compare heading trees, not just text similarity.

## Example differentiated shapes

- B engineering/work-package version: demand and site survey package → signal-chain package → algorithm/rules package → hardware and installation package → platform/work-order package → security/SLA package → implementation/acceptance package → team/training/quality package.
- C runtime/lifecycle version: system runtime chain → event handling chain → alert closure → service lifecycle → operations assurance → service management and continuous improvement.

These are examples, not a mandatory template. The workers must be allowed to invent a better structure for the actual tender.

## Word-count and compliance

Count the user-selected scope explicitly. If the user says正文段落、标题和表格计入 but cover and TOC do not, count paragraph text + heading text + table-cell text, excluding cover/TOC. Keep the count in the requested interval after final assembly. Then verify required phrases, title depth, bullet/list XML, business/price exclusion, and PDF conversion.

## Model/provider provenance

Record the effective Profile provider, endpoint, and model before dispatch. A final file is not evidence that a named worker generated it. Keep worker output in temporary paths, verify non-zero files and session results, and only then replace the final project artifact. If a provider is changed to recover a failed endpoint, report the actual model identity used.
