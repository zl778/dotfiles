---
name: chromium-bookmarks-organization
description: Analyze and reorganize Chromium/Edge browser bookmarks - scan structure, classify by keyword, rebuild folder hierarchy
platforms: [macos]
---

# Chromium / Edge Bookmarks Organization

Bookmarks file: `~/Library/Application Support/<Browser>/Default/Bookmarks` (JSON format).

Edge auto-reloads the Bookmarks file on focus — no restart needed after saving.

## User-specific reference

This user (construction/smart building engineering 智能化弱电工程) has a keyword classification map at `references/pkm-vault-keyword-mapping.md`. Load it with `skill_view('chromium-bookmarks-organization', 'references/pkm-vault-keyword-mapping.md')` for category keywords covering bidding, procurement, AI tools, and domain-specific URLs.

## Workflow — synchronous mode

1. **Backup**: `cp .../Bookmarks .../Bookmarks.bak.$(date +%s)`
2. **Scan**: Parse JSON, report folder counts, duplicates, loose bookmarks, empty folders
3. **Plan**: Present proposed categories to user before executing
4. **Classify**: Write Python script to /tmp/ (not write_file — it may time out on large scripts), execute via terminal
5. **Verify**: Read back, confirm total bookmark count unchanged

## Workflow — async mode (user goes to sleep)

When the user requests a full reorganization and says they'll be away (e.g. "用 goal 模式吧，我要睡觉去了" or "用Goal模式吧，你继续"):

Use `delegate_task(goal="...", context="...", background=True)` to run the full classification in the background. **Do NOT combine background=True with acp_command/acp_args** — ACP mode does not support background tasks; the call will silently fail with "Provide either 'goal' or 'tasks'" error.

The background subagent should:
1. Load `chromium-bookmarks-organization` skill (this skill) for procedure reference
2. Load `references/pkm-vault-keyword-mapping.md` for user-specific keyword mapping
3. Write the Python script to /tmp/, execute it, verify the result
4. Report final structure in its summary

The result auto-reenters the conversation when complete — no polling needed.

Important: background subagents cannot use `clarify` (no user present). The task must be fully self-contained with all decisions made upfront (categories, rules, edge cases for unmatched items). They also suffer from the same write_file timeout on large scripts (see Pitfalls below for the workaround).

## Keyword classification strategy

Match on URL domain + name text combined (lowercased). Cover both English URL terms and Chinese keywords. Use the reference file for domain-specific keywords. Example categories: work (bid/procurement/construction), ai, tools, cloud/email, net/vpn, learn, life/shopping, news/entertainment. Unmatched items go to "待整理" folder for a second pass.

## Pitfalls

- `checksum` field at top of JSON is informational only — Edge recalculates on restart
- `guid` must be unique — use `uuid.uuid4()` when creating new nodes
- `id` values don't need to strictly sequential; the browser reassigns them on load
- `date_added` is a string of Chrome epoch microseconds — new entries can use `str(int(time.time() * 1000000))`
- Empty-name bookmarks (`"name": ""`) are real but invisible in UI — delete them
- Empty folders (no `children`, or `children: []`) — safe to delete
- Bookmarks with empty `name` or empty `url` — created by accidental drags, safe to remove
- Duplicates by URL: common from browser sync — collect with `Counter` and present list
- Chinese/emoji characters in names: JSON handles them natively with `ensure_ascii=False`
- Bookmarks file can exceed write_file limit — write Python script to /tmp/, run via terminal
- Some items will inevitably end up in "待整理" folder — offer a second pass
- Always backup before writing — one wrong write loses all bookmarks
- When writing large scripts, prefer `terminal` with a Python file written to /tmp/ over passing large content through `write_file` — the latter can silently fail on timeout with content exceeding ~8K tokens
- **`write_file` timeout workaround for large Python scripts (~6K+ bytes):** Split the script into 2-3 smaller files via `write_file`, then stitch and execute with `cat`:
  ```
  cat /tmp/edge_p1.py /tmp/edge_p2.py /tmp/edge_p3.py > /tmp/edge_full.py && python3 /tmp/edge_full.py
  ```
  Alternatively use `terminal heredoc` (`cat > /tmp/script.py << 'EOF'`) for small to medium scripts, or `cat >>` to append sections incrementally.
  After writing each fragment, lint it with `python3 -c "import ast; ast.parse(open('/tmp/x.py').read()); print('OK')"`.
- **Second-pass classification strategy:** After the first run, 20-35% of bookmarks often end up in "待整理" because the keyword rules miss domain-specific URLs. Run a debug script to list untagged items, add missing keywords to the rule set, then run a relabel script that moves items from "待整理" to their correct folders. Repeat until "待整理" is empty or acceptably small (≤5 items). This is easily wrapped in a background subagent task.
- **Extreme dedup on reorganize:** When the user already has messy folders (old nested folders + new partial folders from a prior failed run), flattening all bookmarks and reclassifying can produce dedup ratios of 50%+ (e.g. 476→234, removing 242 duplicates). This is normal — the same URLs were stored in multiple old folders. Warn the user if the drop seems extreme.
- Edge auto-reloads the Bookmarks file on focus — no browser restart needed after saving