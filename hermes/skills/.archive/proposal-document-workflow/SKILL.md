---
name: proposal-document-workflow
description: Produce bid/proposal/tender documents with multi-agent draft diversity and reliable Word formatting.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [proposal, tender, bid, docx, word, formatting, multi-agent, drafting, routing]
---

# Proposal Document Workflow

Use this skill when the user asks for bid/proposal/tender document work that combines:
- multiple draft variants from different workers/models
- directory outlines, technical sections, or response matrices
- Word `.doc` / `.docx` formatting and final document styling

## When to use

- Generate multiple different outlines for the same tender
- Ask different workers to produce stylistically distinct versions of the same document section
- Convert extracted requirements into a bid response structure
- Format the final content into a business-grade Word document
- Repair a Word document whose displayed font or spacing does not match the intended style

## Recommended orchestration pattern

1. Keep one primary Hermes as the coordinator.
2. Route the same scope to multiple workers when the goal is deliberate stylistic diversity.
3. Preserve the same factual scope, but vary:
   - section ordering
   - subheading granularity
   - emphasis on implementation vs. formal structure
   - wording style
4. Compare the outputs and keep the best structure or merge them into a final version.

Common role pairing:
- technical / implementation-heavy draft → engineer-capable worker
- formal / polished tender language → writer-capable worker

## Word-document workflow

### Read and extract
- `.docx` → use `python-docx`
- legacy `.doc` → prefer text extraction/conversion first; on macOS, `wvText` is a good first try
- If starting from a drafted outline, write it in Markdown first and convert with `pandoc`

### Format the final document
For Chinese business-document正文, a reliable baseline is:
- Chinese font: 宋体
- Default font: 宋体
- Font size: 小四 (12pt)
- Line spacing: 1.5
- Paragraph spacing after: 8 磅
- First-line indent: 2 characters
- Show style in style gallery: enable `quick_style`

### Verification
- Reopen the generated `.docx` after saving
- Confirm the displayed font/spacing, not just the XML
- Keep a backup before bulk formatting changes

### Content-quality check after worker output
- Worker content may contain internal reasoning text ("Reasoning", "Let me", "I need to", markdown reasoning boxes, `⚠ tirith` banners, or agent status output) that the worker's own `-Q` flag fails to suppress — especially with deepseek or openai-codex providers when the instruction is complex.
- After collecting each worker's output, scan the first ~10 lines for these patterns and strip them before insertion. A post-processing script using `read_clean()` is more reliable than re-running the worker.
- Stripping pattern: skip lines that match reasoning-prefix patterns (`Reasoning`, `Looking`, `Checking`, `Reading`, `Preparing`, `I need`, `I 'm`, `Let me`, `Thinking`) or that appear inside agent decoration borders (`┌─`, `└─`, `│`, `╭─`, `╰─`, `session_id:`). Start collecting from the first substantive line.
- wukong (openai-codex) tends to suppress reasoning well with `-Q` alone; writer (deepseek) and writer on openai-codex fallback may need: `-Q --provider openai-codex -m gpt-5.4-mini` plus in-query instruction "只输出正文，不解释，不要任何推理过程"。

### Style extraction and template normalization

When extracting a reusable format specification from an existing Chinese tender `.docx`, separate three layers instead of collapsing them into one rule:

1. Page/section settings: paper size, orientation, margins, header/footer distances, sections, and page breaks.
2. Style definitions: `Normal`, `Heading 1`–`Heading 4`, table styles, base styles, and their XML-level paragraph/font settings.
3. Direct formatting actually used by paragraphs/runs: effective font, font size, bold, alignment, indentation, spacing, and line spacing.

Report both the source observation and the proposed reusable standard. A source document may have `Normal` defaulting to Calibri while its actual Chinese runs use 宋体/仿宋; it may also have heading styles with one line-spacing definition while direct paragraphs use another. Do not label an observed mixture as a unified template rule.

Before applying the extracted format to other tenders, confirm the user's normalization choice when the source is inconsistent:
- exact visual reproduction, or
- style-preserving normalization into a clean template.

For the normalization path, explicitly choose one body font/size, one heading line-spacing rule, and a Word multilevel list bound to `Heading 1`–`Heading 4`. Keep manual numbering and space-based cover alignment out of the reusable standard unless the user explicitly wants a replica.

### Verification for format extraction

- Reopen the source and inspect both style XML and representative paragraph/run formatting.
- Convert Word internal units before reporting them (e.g., EMU/twips to mm or points) and sanity-check A4 dimensions and margins.
- Compare non-empty paragraph counts separately from all styled paragraphs; empty/special paragraphs can make counts differ.
- Record table count, row/column dimensions, merged cells, widths, borders, cell padding, header repetition, and pagination separately; do not infer precise table geometry from the table style name alone.
- Save the extraction as a Markdown report, then re-read the saved report and audit it for contradictions before using it as a template specification.

### Tender-format variants and project overrides

Maintain separate format specifications instead of collapsing every tender into one universal rule:

- General company baseline (e.g. format A/B): can use automatic TOC, page numbers, unified Heading styles, and a standard body style.
- Technical blind-bid baseline (e.g. format C): treat anonymity as a hard constraint; default to no header/footer/page numbers/TOC, no bold/color/italic/underline, and no company/person/project-identifying content.
- Project-specific requirements always override the company baseline. Before editing a document, create a compact format override table recording the tender clause/page, the company default, and the final value.

For blind bids, verify at minimum: A4/orientation/margins, fixed line spacing and zero paragraph spacing, title numbering/indentation, whether a cover or TOC is allowed, prohibited identity clues, table/figure text size, pagination, metadata, and PDF output. Do not import normal明标 conventions such as logos, named headers, page numbers, or decorative title styling into a blind-bid document.

### Cross-profile worker dispatch for tender-format notes

When the user asks a named Hermes worker such as `wukong` or `writer` to produce a format note:

1. Invoke the named wrapper/profile, not an arbitrary `delegate_task` child.
2. Do not rely on the caller's current shell directory; run `cd <absolute project path> && <worker> chat -q ...` and pass the source/output paths explicitly.
3. Tell the worker to read the existing format note, create only the new output file, and report an absolute path.
4. Verify the output independently from the coordinator by reading the file, checking its size/line count, and listing headings. A worker's self-report is not proof.
5. If a first attempt runs in `/Users/<user>` and cannot find the source, retry with the absolute project path; do not let it write a guessed file elsewhere.

### LibreOffice verification on macOS

A successful `python-docx` reopen validates the package/XML but not visual pagination. After formatting a `.docx`, also try a headless PDF conversion:

```bash
/Applications/LibreOffice.app/Contents/MacOS/soffice \
  --headless --convert-to pdf \
  --outdir /tmp/docx-verification \
  /absolute/path/input.docx
```

Do not assume `libreoffice` or `soffice` is on `PATH`; probe `command -v` and the known macOS application path. If conversion succeeds, record the PDF path and then inspect page count/text or render pages when those utilities are available. If the GUI app is installed but not on `PATH`, use the absolute `soffice` path rather than reporting that LibreOffice is unavailable.

### Source-file discovery in synced tender folders

Before reading or editing a tender package, locate the source by exact filename and inspect the containing directory rather than assuming the current working directory. In OneDrive on macOS, the same synchronized tree may appear both under `~/Library/CloudStorage/OneDrive-个人/` and under `~/Library/Group Containers/.../OneDrive.noindex/OneDrive/`. Prefer the user-facing `CloudStorage` path for subsequent work, but if both copies exist, verify that the target documents match (for example with file size and `md5`) before choosing one. Record the absolute paths of the main tender document and any project-specific `规范/` directory; list the specification files before drafting.

### Mixed-source tender package and technical-volume workflow

When a project folder contains an invitation tender document, a legacy `.doc` technical specification, and multiple internal A/B/C format notes:

1. Treat the invitation document and technical specification as the factual source of truth; treat A/B/C notes as formatting rules only. Do not let old drafts under `OLD/` override the current source package.
2. Locate duplicate copies under synced `接收/` folders and compare them by checksum before choosing a working copy. Record the selected absolute paths and ignore stale-looking duplicates only after verifying equality.
3. On macOS, if `textutil` reports that a legacy `.doc` is not in the correct format, inspect it with `file` and use the known LibreOffice binary `/Applications/LibreOffice.app/Contents/MacOS/soffice --headless --convert-to txt:Text` as the fallback. Re-read the converted text before dispatching writers.
4. Extract and freeze a compact factual brief before dispatch: project facts, deadlines, price ceiling, scope, quantities, starred/mandatory technical clauses, evaluation weights, unknowns, and no-fabrication boundaries. Give every writer the same brief.
5. Build technical volumes around the detailed evaluation criteria, while explicitly excluding商务卷 content when the user asks for技术部分 only. If an invitation and specification conflict (for example, price ceiling versus approximate estimate or different experience-year wording), preserve the stricter/controlling tender requirement and flag the conflict for coordinator review rather than silently choosing a value.
6. Do not infer that a project is blind-bid merely because an internal C-format exists. Require an explicit tender/platform blind-bid clause; if the user waives C anonymity, retain C's numbering and visual format but omit only the anonymity restrictions.
7. For three named variants, keep the facts identical but assign genuinely different organizing logics (for example, lifecycle engineering, task packages, and risk-control loops). A mere renumbering or synonym rewrite is not sufficient. Enforce the requested word-count range independently for each version.
8. Generate DOCX only after coordinator review. Reopen each DOCX with `python-docx`, check headings, tables, page setup, effective fonts, line spacing, numbering, and excluded content, then perform a real LibreOffice PDF conversion when available.

A concise project-specific extraction and conflict checklist is maintained in `references/mixed-source-technical-volume.md`.

### Title-only technical-outline workflow

When the deliverable is only first-level headings for a tender's technical/service section:

1. Extract the detailed evaluation table and the technical/service requirements before dispatching workers. Build a coverage matrix with one row per scored factor and one row per mandatory technical requirement.
2. Separate business and price factors explicitly. Do not assume “technical part” means only the technical-score rows: if the user excludes only business, include service-score rows when they belong in the technical-service response section.
3. Dispatch A/B/C with the same factual brief but different numbering/format rules. Keep the coordinator responsible for the final coverage review; workers are drafts, not authorities.
4. For short title-only tasks, use a compact prompt with explicit output constraints and a required absolute output path. Long prompts can cause a worker to spend its turn reasoning instead of producing the file.
5. Independently verify every output file exists and read it back. Check: all scored factors covered, mandatory security/service requirements included, no business/price content, and numbering matches the requested A/B/C format.
6. If a worker merges two scored factors into one title, split them in the reviewed version when the evaluation table scores them separately. Make high-value items explicit, such as “服务团队总人数及人员配置” when proof of social security is required.
7. Preserve worker diversity in wording or structure, but do not preserve omissions. The coordinator may normalize the final heading list after review and should report what was corrected.

The project-specific reproduction notes and the scoring-coverage checklist are in `references/title-only-technical-outline.md`.

### Model-owned structural diversity for multi-version tenders

When the user wants genuinely differentiated B/C/A tender versions, do not give every worker the same `一级标题` file, shared chapter skeleton, or coordinator-designed parent目录. That produces superficially different wording with identical Word navigation panes and second-level headings.

Use this order:

1. Freeze facts and hard constraints only: tender source, scored factors, mandatory service indicators, format rules, forbidden business content, word-count scope, and title-depth limit.
2. Ask each worker for an independent outline first. The prompt must explicitly say not to read or reuse old B/C正文 and not to treat a shared outline as mandatory. Compare the actual level-1 and level-2 headings; reject outputs whose navigation structure is substantially identical.
3. Review each outline for unsupported inventions before approving it. Workers may propose creative structure, but the coordinator must remove invented device models, quantities, locations, thresholds, performance figures, or unprovided scenario facts. Keep the structure, replace unsupported specifics with “以招标文件/进场核查为准”.
4. Send each worker its own approved outline and generate bounded content chunks. Preserve each version's organizing metaphor (for example, engineering work packages vs. system/event/service chains) through assembly.
5. Assemble each DOCX from that version's chunks without importing the other version's headings. Use the coordinator only for factual normalization, format application, word-count control, and compliance review.

Useful diversity checks are structural, not lexical: compare heading trees, count repeated level-2 titles, identify the dominant organizing unit, and inspect the Word navigation pane after reopening. A version is not differentiated merely because its sentences or numbering marks changed.

### Long-form Markdown technical-volume drafting

When the deliverable is a plain-Markdown technical volume rather than DOCX, treat the user's character-count unit as a hard acceptance criterion. If the user says “中文字符”, count Han characters separately from total Unicode characters and target the Han-character range itself, not only the broader total-character range. Reserve a buffer above the lower bound because Markdown punctuation, Latin model numbers, tables, and headings may otherwise make the Han count fall short.

For format-A technical volumes, enforce all of the following before delivery: use the exact Chinese heading hierarchy specified by the format (`一、`, `（一）`, `1.`, `（1）`), keep heading depth at or below four levels, use no Markdown bullet-list lines in the body, and keep the structure centered on the scored technical factors while preserving the requested lifecycle logic. Tables are allowed, but do not use tables merely to inflate the count. Scan the finished file for bullet markers, heading depth, forbidden business/price sections, unsupported names or certificate numbers, and accidental content copied from unrelated tenders.

Do not stop after the first count. Run a final verification after every expansion or patch and report the exact file path, total character count, and first-level heading list. If the user asks for “只返回” those fields, do not add a narrative, methodology, caveat, or status explanation.

### Post-generation audit and version-safe repair

When the user points to a specific project subdirectory or says a version was already confirmed, treat that directory/version as authoritative. Do not silently replace it with a newer coordinator-generated document. Locate the exact three files first, record their paths and modification context, and make any correction as a sibling file such as `*_审核修正版.docx`; preserve the originals.

Run three independent audits when the user assigns one document per worker. A worker's empty output, helper script, diff banner, or claimed completion is not an audit report. Verify that its report contains concrete findings; if it is empty, retry with a short read-only prompt or perform the same check locally. After any worker recommends a fix, independently reopen the corrected docx and verify the fix.

Do not infer Word formatting from a navigation-pane screenshot or from model prose. Inspect `python-docx` and the actual XML/package for A4 dimensions, margins, effective run fonts/sizes, line spacing, paragraph indents, heading styles/numbering, tables, headers/footers, and list numbering. Compare these values with the project format file, not with a generic company baseline. In particular, detect Letter pages (215.9×279.4 mm) masquerading as Chinese tender documents; normalize to A4 only in the repair copy.

Word may cache styles, fields, and the navigation tree. After changing headings/styles/TOC, close the Word process completely and reopen the sibling repair copy before judging the displayed result. A successful `python-docx` reopen and LibreOffice conversion validates the package, but does not replace the user's fully closed-and-reopened Word visual check.

### Long-form Word generation with multiple workers

For a 12,000+ Chinese-character tender section, do not make one worker responsible for source reading, full drafting, `.docx` creation, and verification in a single background run. Use a staged pipeline:

1. Freeze or checksum the source draft before dispatching. Synced folders and asynchronous workers can update the same document after dispatch; never assume the file read initially is still the file later merged.
2. Give each worker bounded content goals, normally 3,000–6,000 Chinese characters per phase. Require plain Markdown/text output first, and repeat the factual brief and no-fabrication boundary in every phase.
3. Treat a worker's final response, an empty log, or a claimed output path as unverified. Check existence and non-zero size, re-read the artifact, and count it independently.
4. If worker-side long `python-docx` jobs are unstable, assemble the final `.docx` in the coordinator. Preserve wording/model diversity, but centralize page setup, heading styles, tables, and final validation.
5. Count body paragraph characters separately from table-cell characters. Do not use tables or headings to reach the requested body range; record both figures in the review log.
6. Before delivery, reopen the `.docx`, check every scoring-factor phrase, scan for forbidden business/price sections, inspect heading levels and numbering XML, detect bullet/list numbering, and perform real PDF conversion when available.

If the user waives C-format anonymity but keeps the C layout, retain C's numbering/font/page structure while removing only anonymity restrictions. Validate numbering explicitly: level 1 uses `1.`; levels 2–4 use `1.1`, `1.1.1`, and `1.1.1.1` without an extra trailing period.

See `references/long-form-tender-generation.md` for the staged dispatch, verification, and failure-recovery pattern. For the independent-worker, provider-consistency, provenance, explicit word-count, and B-bullet lessons from recent work, also use `references/independent-multi-model-long-form.md`.

### Model provenance and provider consistency

When the user asks for A/B/C drafts from named Profiles, treat model identity as a deliverable attribute that must be verified, not assumed from the launch command. Before dispatch, record each Profile's effective `provider`, `base_url`, and `model`; after dispatch, verify the worker's output artifact and inspect its session/log result. A successful-looking final document is not proof that the named worker generated it.

For OpenAI-compatible endpoints, keep provider, endpoint, and credential source aligned. A native `deepseek` or `nvidia` provider pointed at a SiliconFlow URL can send the wrong API key and produce 401 errors; a `custom` SiliconFlow provider without the Profile's provider mapping/API key can produce an empty-key error. Test with a minimal request before a long generation. If SiliconFlow is unavailable, switch to a native endpoint and a model supported by that native provider, and report that the requested SiliconFlow model identity was not preserved.

Synced folders and asynchronous workers can overwrite the same `.docx` after the coordinator thinks a task ended. Freeze the source draft (backup/checksum), generate worker outputs in temporary paths, and only copy an independently verified artifact into the final project path. If a worker fails or returns an empty/partial result, do not describe the final document as independently generated by that worker; state whether the coordinator assembled it from a shared base.

### B-version bullet-list override

If the user explicitly permits project bullets for format B, bullets may be used for short parallel items such as inspection checks, fault-response steps, or deliverable lists. Keep the main explanation in complete paragraphs and tables, keep bullets out of A/C unless separately allowed, and verify the final `.docx` for the actual bullet/list XML rather than inferring it from Markdown.

### Pre-submission quote audit and cross-version integrity check

When reviewing multiple supplier quotation DOCX files against one inquiry and one equipment list, run two separate audits before delivery:

1. **Within-file compliance audit:** map every inquiry requirement to the actual quotation table and technical response. Recalculate each line-item subtotal, tax, and final total independently; compare the corrected total with the budget ceiling. Check whether installation, training, freight, warranty, and support are included or silently omitted. Verify mandatory attachments such as business license, manufacturer authorization, and after-sales commitment. Treat supplier code-to-real-company mapping as a required fact, not an assumption.
2. **Cross-file integrity audit:** extract company names, brands, exact models, quantities, prices, dates, metadata, and substantive paragraphs from all versions. Flag cross-contamination or long identical passages, but do not label the result “串标” from similarity alone; report concrete evidence and uncertainty. Different structures and wording are not proof of independence either.

For technical responses, never accept a blanket `满足`/`无偏离` when the source list only proves a related or conditional capability. Common traps include: “扩容后最高” rewritten as base throughput; an optional redundant power module rewritten as factory dual power; IPv4/IPv6 dual stack, 1:N virtualization, transparent mode, threat intelligence, or ACG inferred from generic firewall functions; and a family-page parameter used as proof for the exact model. Use `待厂家书面确认`, `部分满足/待确认`, or `存在偏差` and identify the evidence gap.

For pricing, show the arithmetic basis explicitly. If a source spreadsheet formula omits a listed line item, preserve the source value as a disclosed reference but calculate the complete total independently and mark the budget/validity risk. Never silently repair a quote into compliance. Reopen the current renamed files rather than assuming earlier generated filenames still exist; synced folders may rename or replace artifacts after worker generation. Run `python-docx` extraction plus OfficeCLI `validate` after any repair, closing resident OfficeCLI documents first to avoid stale-cache results.

### Post-generation scoring and second-pass audit

When the user provides a separate review/scoring prompt after the DOCX files exist, audit the actual DOCX packages, not only the Markdown drafts. Run three independent checks:

1. Scope check: distinguish technical-volume omissions from business-volume materials intentionally outside the requested deliverable. Do not mark missing营业执照、授权委托书、保证金、签章页 as technical red lines when the user explicitly requested only the technical section; report them as“商务卷/提交包另行确认”.
2. Requirement check: compare each document against the invitation and technical specification using concrete anchors: project number, 60 calendar days, 12-month warranty, 90-day video retention, spray-pipe pressure/hold/drop/flush thresholds, complete supply scope, design-installation-commissioning-acceptance, training, safety/environment, schedule/resources/project organization, and technical deviations.
3. Artifact check: reopen each DOCX with `python-docx`, inspect A4 dimensions/margins, heading levels, paragraph/table counts, effective styles, and core metadata (`author`, `last_modified_by`). A file can be structurally readable while retaining an identifiable last editor; clear and re-open/verify metadata on every version.

Score the versions with the user's rubric (for example, response 40%, logic 30%, professionalism 30%) and record evidence-based findings with locations or section names. Preserve real structural diversity; do not select a winner merely because its wording is longer. If the review identifies a repair, create a sibling repair copy or a final merged copy, never silently overwrite the confirmed source.

For a synthesis requested by the review prompt, select the strongest framework only after scoring, then merge missing high-value requirements from the other drafts. Re-run the full audit after synthesis, including duplicate heading labels, inconsistent project facts, template residue, unsupported claims, character-count range, and A/B/C-specific formatting.

### 0719-style final-package audit: score the artifact, then test eligibility

When a tender package contains a dated/versioned folder such as `标书0719`, treat the actual DOCX files in that folder as authoritative for the review. Do not score an older path, an earlier Markdown draft, or a previous `二次检查和评分.md` table without reconciling it to the current artifacts. First rediscover the exact A/B/C filenames and record their paths; then reopen each DOCX with `python-docx` and inspect paragraphs, tables, metadata, and key form fields.

Run two separate judgments:

1. **Technical estimate** — score the requested rubric (for this project: response 40, logic 30, professionalism 30) using evidence from the actual technical volume. A long narrative does not compensate for missing or contradictory requirement rows.
2. **Tender eligibility / preliminary review** — independently check hard risks such as price ceiling, bid validity, mandatory qualification, signatures/seals, blank bidder/price/tax fields, mandatory starred clauses, payment terms, and explicit equipment noncompliance. A document may have a technical estimate at or above 80 while still being ineligible because of a commercial or preliminary-review failure.

For every version, cross-check three layers row by row:

- quotation/equipment list: brand, exact model, quantity, unit, price form and remarks;
- performance-guarantee table: claimed values, storage calculations, port counts, protection grades and evidence status;
- technical deviation table/body: whether the response honestly says `无偏离`, `待确认`, or `存在偏差`.

Flag these high-value contradictions explicitly instead of accepting a blanket `无偏离`:

- an 8-port switch listed against a 20-port requirement;
- IP55 listed against IP56 required;
- single-mode/single-fiber transceiver or 12-core cable against a 6-core outdoor multimode link;
- 8 × 8TB disks claimed to provide 90 days when 19 channels × 4Mbps continuous recording theoretically requires about 73.872TB before RAID/filesystem overhead;
- a thermal/visible-light camera model entered as an independent photoelectric smoke detector;
- a passive external siren described as independently providing APP push, video review, acknowledgement, reset, or logs;
- a family-page or similar-model parameter presented as proof for the exact supplied model.

When calculating storage, show the basis (camera count, bitrate, frame rate, continuous duration, raw capacity, RAID usable capacity, and practical overhead). Never allow a performance table to say “满足90天” unless the calculation supports it. When a version has an incomplete or over-limit price, blank VAT/bidder/date fields, or missing signatures, state the direct preliminary-review risk even if the technical prose is strong.

In the final report, give each version: technical sub-scores, technical total, eligibility status, hard rejection risks, evidence-backed omissions, and a prioritized repair list. Preserve the prior score as a historical baseline only; do not silently reuse it as the current result.

### Structure freedom without format drift

When the user asks workers to design genuinely different B/C structures, treat content architecture and document format as separate layers:

1. Let each worker independently propose its own level-1/level-2 outline. Do not force a shared chapter skeleton or reuse a common `一级标题` file as a mandatory parent tree.
2. After choosing the independent outline, map it into the project format's numbering system. Creative structure does **not** authorize changing page size, margins, body font, line spacing, directory rules, or title-depth limits.
3. Never assemble a final DOCX with generic defaults without checking the project spec. `python-docx` defaults can silently produce Letter paper, inconsistent direct formatting, mixed line spacing, or unbound Heading styles.
4. Verify the actual Word navigation tree after reopening. Compare level-1 and level-2 headings, not just wording; a version is still structurally identical if its second-level tree is the same.
5. If the user confirms a specific synced-folder version visually, treat that file as the baseline. Write repairs to a new `*_审核修正版.docx`, never overwrite the confirmed original.

For the Shanghai telecom project, the observed defaults were B: A4, margins 2.6/2.2/2.5/2.5 cm, 宋体小四, 1.5-line spacing, two-character first-line indent; C: A4, margins 2.0/2.5/2.5/2.5 cm, 宋体四号, fixed 25 pt line spacing, Arabic numbering. Confirm the actual project override before applying these values.

### Tender scoring versus document-quality scoring

When a user supplies a meta-review prompt with a 100-point rubric, report it separately from the tender's official score:

- Meta quality score: use the prompt's dimensions (for example response 40, logic 30, professionalism 30).
- Official tender score: extract the actual evaluation table and score only the applicable technical/service factors. Business performance and price are separate.
- Team-headcount points may depend on external evidence such as a recent social-security certificate. Score the prose response conditionally and state the evidence-dependent alternative; do not infer proof from a sentence claiming that proof exists.
- Signature pages, guarantees, qualification files, and price forms are full-response-package checks, not automatically defects in a technical-only section. Mark them as `[CRITICAL—需核验完整响应文件]` when outside the artifact under review.

### Performance-guarantee matrix and conflict disclosure

For a second-pass technical bid review, convert the review findings into a final `性能保证值表` rather than only a prose audit. Append it after all existing sections and appendices, using a stable six-column structure: `序号、系统/设备、招标要求/基准、投标性能保证值、偏差/复核说明、证明资料位置`. Cover quantities, key device thresholds, storage retention, network ports/fiber, control-box protection, redundant power, interlocks, pressure/flush tests, authorization/evidence, three-party approval, standards submission, training, warranty and schedule.

Treat quotation lists and technical specifications as separate evidence layers. When they conflict (for example an 8-port listed switch versus a 20-port specification, or IP55 listed enclosure versus IP56 required), do not silently upgrade the listed item or write “满足”. State the required guarantee, identify the current item as a deviation, and require replacement or written clarification before submission. Use conditional verification language for parameters not proven by the available product data. If the user asks for change marking, set every newly added heading, note, table header, cell run and conclusion to the requested color, then independently verify the color across all new table runs.

### Official product-page verification and equipment-list population

When a tender names a manufacturer and requires model-level device parameters, use the manufacturer's official product page as an evidence source, but do not treat a family page, search snippet, or similar model as proof for the exact model. Search by product family and exact model, then open the official product detail page and record the URL, model, and every visible specification relevant to the tender. Build a requirement-versus-evidence matrix with these statuses: `已明确满足`, `官网未列出`, `仅同系列证明`, or `存在偏差`.

For fire-safety/thermal cameras, verify separately: visible-light megapixel class, selectable 1920×1080 and 25fps, H.264 High Profile, MJPEG, multi-stream count, bitrate range, ONVIF/API, alarm input/output count and electrical contact parameters, thermal measurement accuracy/method, and the exact PoE standard. Do not convert “告警2出” into “2路NO、DC12V/20mA”, and do not convert “支持PoE” into `802.3at` without the page or a manufacturer confirmation explicitly stating it. If no exact model satisfies all requirements in public evidence, nominate the closest candidate but mark the unresolved items for a written manufacturer confirmation or model replacement.

When populating an existing equipment-list `.xlsx`, inspect the workbook's actual sheet name and header row first. Back up the source and create a versioned sibling (for example `设备清单_参数要求版.xlsx`); use OfficeCLI batch cell updates for the exact `参数要求` column, enable wrapping/vertical-top alignment for long Chinese requirements, then run OfficeCLI validation and re-read the finished workbook to verify every intended row. Keep conflicts visible in the cell text—never silently upgrade an 8-port listed switch to a 20-port requirement or IP55 enclosure to IP56. For fire-camera, NVR, smoke-detector, optical-transceiver, switch, and alarm-device selection examples and exact official URLs, see `references/fire-device-selection.md` and `references/vendor-equipment-selection.md`; the OfficeCLI/evidence workflow remains in `references/official-product-evidence-and-officecli.xlsx.md`.

### System-function boundary for external devices

For device-selection tasks, separate functions proven by the physical device from functions supplied by the surrounding system. An external siren/stack light may provide only local sound/light output; temperature detection, video analytics, smoke input, alarm forwarding, APP/platform push, video verification, acknowledgement, reset, and log retention may belong to the camera, NVR, alarm controller, gateway, or platform. State the architecture explicitly and never claim that a passive output device independently provides platform functions. If the manufacturer's public page lists only a model name and no electrical/environmental specifications, recommend it only as a basic/near match and require a formal datasheet or confirmation letter before marking compliance.

For exact-match selection, prefer a model whose port count and core parameters match the tender exactly. If a higher model exceeds the requirement, disclose the excess (for example, 16 SATA bays versus an 8-bay minimum) and explain why it is acceptable. For cross-brand systems, verify interface/protocol compatibility separately; manufacturer brand consistency is a hard constraint when the user says the whole set must use one brand.

### Technical deviation-table workflow

When the tender provides a fixed “投标偏离表” format, reproduce its column structure and wording before adding content. For the common format in this project, use exactly three columns: `序号、询价文件重述、偏离或供应商建议（条件）`, followed by the tender's note and signature block. Do not replace the fixed table with a richer internal matrix unless the user explicitly asks for an additional working table.

Keep technical and commercial deviations separate. Technical tables belong in the technical volume; contract/payment/tax/price deviations belong in the commercial volume. If the tender says the bidder has no deviation, do not fill technical rows with a blanket “完全响应” while silently overlooking equipment-list conflicts or unverified model parameters.

Build the table from the controlling technical specification, not only the equipment quotation list. For every major system or scored requirement, write the tender requirement in the middle column and the response in the right column. Use these response statuses consistently:
- `无偏离` only when the requirement is directly accepted and the supporting model/evidence is adequate;
- `无偏离，最终型号/参数以厂家正式规格书和甲方确认清单为准` when the design commitment is clear but model evidence is not yet complete;
- `待厂家书面确认或更换满足型号` when a parameter such as NTC method, alarm-contact electrical values, PoE class, 4G, acoustic level, or storage capacity is not proven;
- `存在资料不一致，按技术规格书较高要求执行` when the quotation list conflicts with the technical specification.

Always surface internal conflicts instead of silently upgrading the item. Typical examples are an 8-port switch listed in the quotation versus a 20-port switch required in the specification, or IP55 in the list versus IP56 in the specification. State the controlling source, the required correction, and whether the equipment list/deepening drawings must be updated.

Include system-boundary language where necessary: a local sounder does not itself provide APP push, video verification, acknowledgement, reset, or logs; those functions must be assigned to the NVR/platform/controller and tested in the linkage matrix. For storage, include the actual calculation basis (camera count, bitrate, frame rate, continuous duration, RAID/overhead assumptions) rather than asserting that a disk count is sufficient.

After generating the deviation DOCX, independently verify: the table has the expected three columns and row count; the fixed note/signature block is present; unresolved items remain conditional; no commercial content leaked into the technical table; the DOCX reopens with `python-docx`; and LibreOffice converts it successfully to PDF. Preserve the original tender and existing technical volume; create a sibling output such as `标书C技术投标偏离表.docx`.

### Source path and Word refresh verification

Synced OneDrive project folders may be renamed or moved while old paths remain in session context. Before reviewing or editing, rediscover the exact filename and containing folder and use the user-facing `CloudStorage` copy. After changing styles, numbering, TOC fields, or page setup, close Word completely and reopen the DOCX before judging the displayed result; Word may cache the old navigation tree and formatting within the same process.

### Recovery when a Word file appears to disappear after saving

When a user says a Word file was edited and saved but cannot be found, do not conclude that it was lost after checking only the expected filename. Use this recovery order:

1. Search the exact project tree recursively for same-title variants, hidden/temporary names, and extension changes (`.docx`, `.doc`, `~$*`, `~WRF*`, `~WRS*`). Sort by modification time and size.
2. Inspect every plausible variant with `python-docx`: paragraph count, table count, headings, and distinctive added text. A modified copy often has more paragraphs/tables than the original even when the filename only says `副本` or `副本2`.
3. Compare candidates with MD5 only after content inspection. Identical MD5 between `副本` and `副本2` means they are duplicate saved copies, not proof that no edited version exists; compare both against the original.
4. Check Word's macOS `AutoRecovery`, `Data/tmp`, `Application Support/Microsoft/Temp`, and OfficeFileCache. Treat a non-empty `~WRF*` file as a candidate, but validate its actual format before claiming recoverability; Word temporary files may be compound/partial files that neither `textutil` nor LibreOffice can open.
5. Read Word's MRU file at `~/Library/Containers/com.microsoft.Word/Data/Library/Application Support/Microsoft/Office/16.0/aggmru/*/w-mru4-zh-CN-sr.json`. Extract matching titles, OneDrive URLs, breadcrumbs, timestamps, and modification metadata. This can reveal that the file was saved under a OneDrive cloud path or a renamed copy.
6. Check both user-facing `~/Library/CloudStorage/OneDrive-个人/` and any other indexed OneDrive tree, plus `.Trash`; do not modify or delete recovery candidates during discovery.
7. If a verified modified copy exists, create a sibling named clearly, for example `原文件名_已编辑恢复版.docx`, and verify the copied file's MD5 and `python-docx` readability. Preserve the original and all candidates.

The acceptance evidence is: exact absolute path, modified-vs-original structural comparison, checksum of the recovery copy, and an explicit statement if Word/OneDrive temporary candidates were not parseable. Do not report a file as unrecoverable until these checks are complete. The re-runnable search notes and MRU parsing recipe are in `references/word-save-recovery.md`.

### Surgical DOCX update from supplementary materials

When the user provides supplementary materials (XLSX quotation sheets, product spec `.doc` files, certification PDFs) and asks you to update an existing technical-volume DOCX with concrete device models, quantities, and performance parameters:

1. **Read the supplementary material first.** Use `openpyxl` for XLSX (column-merges and hidden rows are common; inspect the full table row-by-row with `iter_rows()`). Use `textutil -convert txt` on macOS for legacy `.doc` product specs — `.docx` product specs are rare but can be read directly with `python-docx`. For PDF specs, try `pymupdf` or `marker-pdf` if available. Record model names, quantities, performance numbers, and the manufacturer/brand for each item.

2. **Map data to existing document paragraphs.** Read the existing DOCX paragraph-by-paragraph and table-by-table. Identify which paragraphs should be updated (e.g., "供货方案" paragraph for the main device list, "存储" paragraph for NVR/hardware specs, the technical response table for specific model numbers) and which table cells need augmentation. Do not guess at paragraph content — re-read the current text.

3. **Back up before modification.** Copy the source DOCX to a timestamped backup path before editing. Never overwrite the backup later; let the user clean it up.

4. **Use red font for new/updated content.** When the user explicitly asks to mark changes, set the run text color to red (`RGBColor(0xFF, 0x00, 0x00)`). Add new paragraphs immediately after the existing target paragraph (using `paragraph.insert_paragraph_after()`). For table cells, append a new red-text run to the cell's first paragraph.

5. **Surgically update, don't rewrite the whole document.** Only modify the identified paragraphs/tables — do not regenerate the entire DOCX from scratch. Keep all existing content and formatting unchanged. If a supplementary source lists prices (e.g., a quotation sheet), include the model numbers and quantities but NOT the unit prices/totals in the technical volume; prices belong in the商务卷.

6. **Verify after modification.** Re-read the modified DOCX with `python-docx`, inspect file size, paragraph count, the red-text runs (count paragraphs containing a red run), verify that no prices leaked into the technical volume, and confirm the backup still exists at its original path. Report: backup path, file size before/after, paragraphs modified, tables modified.

7. **No-fabrication boundary.** If a supplementary source is missing a device model or quantity for a required item, mark it as `[待补充]` in red font rather than inventing a number. The user can correct from the actual procurement list.

### Procurement quotation package: source arithmetic and artifact gates

When producing multiple vendor quotation DOCX files from an invitation plus an XLSX equipment list:

1. Freeze a factual brief before dispatch. Extract the invitation's controlling budget, delivery, validity, service, and every technical row; extract each vendor sheet's exact model, quantity, unit price, formula, and remarks. Keep the invitation as the controlling requirement and the spreadsheet as the pricing source, but do not silently trust spreadsheet formulas.
2. Recalculate every vendor total independently from line items. Compare the source formula result with the line-item sum, tax basis, and budget cap. If a formula omits a line (for example, a jump-wire row), disclose both the source result and the corrected full-list result; never hide an over-budget result by copying the erroneous cached formula.
3. Dispatch named profiles with distinct output paths and keep the coordinator responsible for the third version. If a named profile's default provider returns an authentication error, retry the same profile with a known-good explicit provider/model and disclose that provider fallback; do not claim the original model identity was preserved.
4. Stage and verify outputs independently. A worker's final message or generated diff is not completion proof. Reopen each DOCX with `python-docx`, check project number, vendor/brand/model, all prices, service promises, technical response rows, pending-confirmation labels, tables, and metadata. Clean worker-tool metadata such as `python-docx` before delivery.
5. Run `officecli validate` on every final DOCX. Close the OfficeCLI resident for each file before validation or before reading it with another library; otherwise validation may inspect a stale in-memory copy. If strict schema validation reports `w:shd` table-cell shading errors from a python-docx-produced file, remove the nonessential shading elements (or regenerate with schema-valid shading) and revalidate. Preserve a `/tmp/` backup before XML repair.
6. For technical evidence, use `满足` only when the supplied vendor row explicitly proves the invitation requirement. Use `待厂家书面确认` for missing IPv4/IPv6, virtualization semantics, transparent mode, threat-intelligence scope, capacity, or similar evidence. Keep optionals (such as a redundant power module) and source-description contradictions visible in a deviation/risk table.

See `references/quotation-package-verification.md` for the reusable extraction, arithmetic, provider-fallback, resident-cache, and validation checklist.

### Pitfalls

- A Word document may visually substitute the intended Chinese font. If that happens, try the exact installed Chinese face name that Word renders correctly and verify after reopening.
- For stubborn formatting, set paragraph/run formatting directly on the body text instead of relying only on style definitions.
- Old `.doc` files often need extraction/conversion before editing.
- Old `.doc` files often need extraction/conversion before editing.
- When one worker's default provider fails auth or is unavailable, rerun the same role with an explicit known-good `-m` / `--provider` override for that task rather than changing the whole architecture.
- **Security approvals interrupt multi-agent dispatch.** When dispatching parallel workers via `hermes -p <profile> chat -q "... " -Q > file`, the security/approval layer may block the command if it detects "spawning profiles". Do not claim completion; stop, inform the user, and wait for approval. After approval, verify each worker's output file exists before proceeding to merge.
- **Worker output timeout on large tasks.** Generating hundreds of lines of tender body text may exceed the default `hermes chat -q` timeout (typically 180s). Set `--timeout` to at least 600s, or split the task across multiple smaller queries (e.g., sections 1–3, then 4–7). Between 300–600 lines is the boundary where timeout starts to bite.
- **Backup incrementally.** Name backups `.bak`, `.bak2` etc. to preserve a chain of intermediate states. The coordinator should not delete the backups — let the user clean up if needed.
- **版本优先：新建而非覆盖。** 更新已确认的 DOCX 时绝不覆盖原文件。原文件是用户确认的基线。修正结果应另存为带后缀的新文件（如 `*_v2_审核修正版.docx`）。生成更新前先将源文件复制到 `/tmp/` 做备份——OneDrive 同步可能有缓存问题，/tmp/ 备份确保可恢复。用户明确纠正过这个行为：修正永远是新版本，不是覆盖。

## Good use cases

- Generating two or more tender outlines for comparison
- Producing a formal version and a practical version of the same proposal
- Turning a tender spec into a directory structure and then into a formatted `.docx`
- Standardizing the body style of a bid document after conversion

## Reference

- `references/tender-routing-and-formatting-notes.md` — session-derived routing and formatting notes for multi-model bid drafting and Word font fixes
- `references/multi-worker-tender-dispatch-phases.md` — phased workflow for dispatching parallel workers (inspect→brief→dispatch→sanitize→insert→verify), including content-cleaning patterns and per-model output-behavior table
