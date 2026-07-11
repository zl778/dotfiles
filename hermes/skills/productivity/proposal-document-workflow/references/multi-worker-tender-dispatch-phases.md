# Multi-worker tender dispatch phases

Source: 2026-07-11 session — full technical-spec response for a fire-safety retrofit tender (～400 lines B, ～200 lines C), dispatched across wukong + writer profiles.

## Phase 1: Inspect & build a factual brief

Before dispatching any worker, the coordinator must:

1. Read the existing target documents (.docx) — extract both the outline and the current content to know what's already written.
2. Read the source tender (.docx) and technical specification (.doc — convert with `wvText` or `pandoc`).
3. Compile a **compact factual brief** (no more than 8KB) containing:
   - Project name, location, deadlines, budget caps
   - All applicable areas and quantities from the spec
   - System architecture requirements (which zones use heat cameras vs. smoke detectors, storage requirements, protocol standards)
   - Explicit **no-fabrication boundary**: "do not write specific company names, person names, cert numbers, final model numbers, quote values, or unverified site dimensions"
   - List of quantities, brands (as ranges: 海康/大华/宇视), cable lengths (as approximate)
   - Section numbering for both target documents (B and C have different section structures)
4. Store this as a plain `.md` in `/tmp/` so workers can read it.

## Phase 2: Dispatch workers in parallel

Use independent background terminal commands:

```
hermes -p wukong chat -q "read /tmp/brief.md, write sections X...Y" -Q > /tmp/wukong_output.md
hermes -p writer chat -q "read /tmp/brief.md, write sections X...Y" -Q > /tmp/writer_output.md
```

Key flags:
- `-Q` suppresses the agent banner but may NOT suppress internal reasoning.
- Set `timeout` to 600s (or use `background=true` + `notify_on_complete=true` for extra-long tasks).
- If a worker's default provider is down, force an override: `--provider openai-codex -m gpt-5.4-mini`.

Security approval note:
- The first command to `hermes -p <profile> ...` may trigger the security prompt for profile-spawning. Notify the user and wait. Do not pretend the dispatch succeeded.

## Phase 3: Sanitize worker output

Worker output often begins with reasoning text. Wukong/openai-codex produces clean output with `-Q`. Writer (any provider) may produce several hundred lines of internal monologue, reasoning boxes, or agent-status banners.

A reliable `read_clean(path)` function in Python:

```python
import re
def read_clean(path):
    raw = Path(path).read_text(errors='replace')
    lines = raw.replace('\r', '').splitlines()
    clean = []
    skip_header = True
    for line in lines:
        if skip_header:
            s = line.strip()
            # Skip reasoning markers
            if any(kw in s for kw in ['Reasoning', 'Looking', 'Preparing',
                'Checking', 'Reading', 'I need', "I'm", 'I ’', 'Let me',
                'Thinking', 'Planning']):
                continue
            # Skip agent decoration borders
            if s.startswith(('┌─', '└─', '│', '╭─', '╰─', '───')):
                continue
            if s.startswith(('⚠', 'session_id')):
                continue
            if s == '':
                continue
            skip_header = False
        clean.append(line)
    return '\n'.join(clean)
```

Apply this BEFORE any insertion logic.

## Phase 4: Insert into target documents

1. Back up the target `.docx` with a numbered suffix (`.bak`, `.bak2`, ...).
2. Open the doc with `python-docx`.
3. Append content at a page break with a section marker heading ("技术卷正文（第X部分起）").
4. Use a simple add-paragraph approach for markdown text, and `add_table` for markdown tables.
5. Set font=宋体-简, size=12pt, line-spacing=1.5 as the baseline.
6. Save and verify.

## Phase 5: Verify

For each updated `.docx`:

```
python3 - <<'PY'
from docx import Document
from pathlib import Path
text = '\n'.join(p.text for p in Document(path).paragraphs)
expected_headings = ['5. 总体技术方案', '8. 施工组织设计', ...]
present = [h for h in expected_headings if h in text]
missing = [h for h in expected_headings if h not in text]
print(f"present={len(present)}/{len(expected_headings)} missing={missing}")
PY
```

Check for leaked reasoning (`'Reasoning' in text`, `'Let me' in text`). Check file bytes increased since the last backup.

## Known per-model behavior

| Model/Provider | Output cleanliness with -Q | Notes |
|----------------|---------------------------|-------|
| wukong (gpt-5.5, Codex) | ✅ Clean | No reasoning leak observed |
| writer (deepseek-v4-flash, deepseek) | ❌ Leaks reasoning | Use fallback provider |
| writer (gpt-5.4-mini, openai-codex) | ⚠️ Occasional reasoning on first 3-5 lines | In-query: "只输出正文，不解释，不要任何推理过程" helps but may not eliminate |
| default (gpt-5.4-mini, codex) | ✅ Generally clean | Safe fallback for any profile |
