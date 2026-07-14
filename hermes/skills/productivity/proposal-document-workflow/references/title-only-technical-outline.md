# Title-only technical-outline reference

## Reusable coverage checklist

Before dispatch:

- Identify the exact tender `.docx` and project `规范/` directory; prefer the user-facing synced path after checking duplicate OneDrive copies.
- Extract the detailed evaluation table, not only the table of contents.
- Create three buckets: technical-score factors, service-score factors, and excluded business/price factors.
- Add mandatory service requirements that may not be scored separately, such as network and information security.

For a technical-service section, check whether the headings explicitly cover:

- technical service solution
- technical service standard/guarantee measures
- technical service schedule
- implementation organization: daily inspection, emergency response, team configuration, project management
- service team headcount and required proof (for example, social-security evidence)
- team stability / turnover commitment
- training plan
- service commitment
- response commitment and exact SLA values
- network and information security

## Worker dispatch and verification

Use the same factual brief for A/B/C and vary only the intended format or organizational style. For a short heading-only task, prefer a compact prompt such as:

```text
Only write the first-level heading list to <absolute-output-path>.
No reasoning, explanation, second-level headings, body text, business, or pricing.
Use the required numbering style.
```

After each worker returns:

1. Verify the absolute output file exists.
2. Read the file rather than trusting the worker's session ID or stdout.
3. Check every scored factor and mandatory technical requirement against the coverage matrix.
4. Check that a retry did not overwrite or remove a previously covered requirement.
5. Normalize omissions in the coordinator's reviewed copy and report the corrections.

A successful worker draft may still merge separately scored factors (for example, service commitment and response commitment) or omit a non-scored mandatory requirement (for example, information security). The coordinator should split or add headings when this improves direct evaluation traceability.

## Format variants

- A/B general bid: Chinese first-level numbering such as `一、` and `二、`; A may be plain text Markdown, while B may use Markdown heading markers if the format note is being used as a heading specification.
- C technical blind bid: Arabic first-level numbering such as `1.` and `2.`; no identity information or decorative identity cues. The blind-bid style must be applied later in Word as regular, unbolded, black text when the project rules require it.
