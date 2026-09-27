# Batch Tag Rename: Chinese → English (2026-06-29)

Full vault-wide tag rename converting all Chinese tag names to English in Obsidian PKM vault.

## Scope

~155 tag occurrences across ~90 markdown files. Two tag formats:
- **Inline**: `#a/学习/单词` — written at the top of the note body
- **YAML frontmatter**: `tags:
  - /r/工具/vps` — with leading `/`

## Translation map

### #r/ (Resources)
| Original | English |
|:---------|:--------|
| #r/工具 | #r/tools |
| #r/工具/网络 | #r/tools/network |
| #r/工具/云同步 | #r/tools/cloud-sync |
| #r/代码 | #r/code |
| #r/代码/正则 | #r/code/regex |
| #r/设计 | #r/design |
| #r/AI/工具 | #r/AI/tools |
| #r/AI/模型 | #r/AI/models |
| #r/AI/提示词 | #r/AI/prompts |

### #a/ (Areas)
| Original | English |
|:---------|:--------|
| #a/工作 | #a/work |
| #a/工作/广联达 | #a/work/glodon |
| #a/工作/政采 | #a/work/procurement |
| #a/健康 | #a/health |
| #a/健康/运动 | #a/health/exercise |
| #a/生活 | #a/life |
| #a/生活/出行 | #a/life/travel |
| #a/生活/金融 | #a/life/finance |
| #a/生活/通信 | #a/life/telecom |
| #a/学习 | #a/learning |
| #a/学习/单词 | #a/learning/vocabulary |
| #a/学习/软件 | #a/learning/software |
| #a/学习/系统 | #a/learning/system |

### #p/ (Projects)
| Original | English |
|:---------|:--------|
| #p/当前项目 | #p/current |
| #p/投标 | #p/bidding |

### Plan-only tags (in index file, no notes use them)
| Original | English |
|:---------|:--------|
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

## Execution notes

- **sed `find -exec` with `+|` separator** handles file paths with spaces and Chinese characters
- The `#` prefix and `/` prefix patterns are independent — both must be replaced
- Plan-only tags (in the index file) need to be checked first: `rg -c 'the/tag' | grep -v '标签系统-PARA'` to confirm zero actual usage
- Replace parent tags AFTER child tags to avoid partial-match issues
- Verify with `rg -c --fixed-strings` after each batch