# Batch Tag Rename: Chinese → English (2026-06-28)

Vault: `PKM` (iCloud Obsidian vault)
Scope: ~155 tag occurrences across ~90 files

## Translation table

### #r/ (Resources)

| Original | New | Occurrences |
|----------|-----|:-----------:|
| #r/工具/vps | #r/tools/vps | 0 |
| #r/工具/网络 | #r/tools/network | 5 |
| #r/工具/云同步 | #r/tools/cloud-sync | 2 |
| #r/工具 | #r/tools | 31 |
| #r/代码/正则 | #r/code/regex | 2 |
| #r/代码 | #r/code | 8 |
| #r/设计 | #r/design | 10 |
| #r/AI/工具 | #r/AI/tools | 3 |
| #r/AI/模型 | #r/AI/models | 3 |
| #r/AI/提示词 | #r/AI/prompts | 3 |

### #a/ (Areas)

| Original | New | Occurrences |
|----------|-----|:-----------:|
| #a/工作/广联达 | #a/work/glodon | 5 |
| #a/工作/政采 | #a/work/procurement | 1 |
| #a/工作 | #a/work | 7 |
| #a/健康/运动 | #a/health/exercise | 4 |
| #a/健康 | #a/health | 4 |
| #a/生活/出行 | #a/life/travel | 3 |
| #a/生活/金融 | #a/life/finance | 9 |
| #a/生活/通信 | #a/life/telecom | 12 |
| #a/生活 | #a/life | 5+ |
| #a/学习/单词 | #a/learning/vocabulary | 1 |
| #a/学习/软件 | #a/learning/software | 14 |
| #a/学习/系统 | #a/learning/system | 10 |
| #a/学习 | #a/learning | 7+ |

### #p/ (Projects)

| Original | New | Occurrences |
|----------|-----|:-----------:|
| #p/当前项目 | #p/current | 1 |
| #p/投标 | #p/bidding | 2 |

## Commands used

### Phase 1 — Inline tags (`#tag`)

```bash
cd "<vault>"
find . -name "*.md" -exec sed -i '' 's|#r/工具/网络|#r/tools/network|g' {} +
find . -name "*.md" -exec sed -i '' 's|#r/工具|#r/tools|g' {} +
# ... repeat for all tags, most-specific first
```

### Phase 2 — YAML frontmatter tags (`- /tag`)

```bash
find . -name "*.md" -exec sed -i '' 's|/r/工具/网络|/r/tools/network|g' {} +
find . -name "*.md" -exec sed -i '' 's|/r/工具|/r/tools|g' {} +
# ... same order
```

### Verification

```bash
# Check no old tags remain
rg -c --fixed-strings '#a/生活' . --include '*.md' | grep -v ':0$'

# Count new tags
rg -c --fixed-strings '#a/life' . --include '*.md' | awk -F: '{s+=$2} END {print s+0}'

```bash
head -3 "20_Areas/Google Play账号.md"
head -3 "20_Areas/单词收集器.md"
```

## Pitfalls encountered

1. **Replace order is critical**: Always do most-specific (deepest) sub-tags first, then parent tags. If `#a/生活` is replaced before `#a/生活/通信`, the latter becomes `#a/life/通信` and the second pass misses it.

2. **Two tag formats**: Obsidian supports both inline (`#tag/path` at the top of a note) and YAML frontmatter (`- /tag/path` under `tags:`). Both must be handled separately — the first uses `#` prefix, the second uses `/` prefix.

3. **Tag index files**: The vault's tag-system reference document (e.g., `标签系统-PARA架构.md`) contains tags in its documentation table. These get replaced automatically by the same sed commands.

4. **English sub-tags are fine**: Tags like `#r/tools/Excel`, `#r/tools/Mac`, `#r/tools/NAS`, `#r/tools/Word`, `#r/code/Python`, `#r/design/PS`, `#r/AI/Hermes` were already English and didn't need translation.

5. **Dotfiles sync**: After modifying the vault, the next daily cron sync will push the updated notes to dotfiles repo automatically.

6. **Check actual usage first**: Not all tags in the planning table are actually used in notes. Run `rg -c --fixed-strings '#the/tag' '<vault>' | grep -v '标签系统-PARA' | awk -F: '{s+=$2} END {print s+0}'` to check. If count is 0, the tag exists only in the plan document.

---

## Phase 2 — Plan-only tags in index document (2026-06-29)

Tags that existed ONLY in `20_Areas/标签系统-PARA架构.md` (the planning table) with zero actual note usage.

### Translation table (plan-only)

| Original | New |
|----------|-----|
| #p/跟踪 | #p/followup |
| #p/采购 | #p/procurement |
| #p/装修 | #p/renovation |
| #a/work/技术标 | #a/work/tech-bid |
| #a/work/弱电 | #a/work/low-current |
| #a/work/外网 | #a/work/external-net |
| #a/health/跑步 | #a/health/running |
| #a/health/体检 | #a/health/checkup |
| #a/health/饮食 | #a/health/diet |
| #r/tools/终端 | #r/tools/terminal |
| #z/项目 | #z/project |
| #z/旧设备 | #z/old-device |
| #z/其他 | #z/other |
| #d/日志 | #d/journal |
| #t/模板 | #t/template |
| #d/周记 | #d/weekly |

### Replacement method

Same sed approach as Phase 1 — the commands were run across all .md files and caught both inline tags (`#`) and YAML frontmatter tags (`/`) in one pass.