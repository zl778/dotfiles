---
name: word-collector
description: "Alfred workflow 单词收集器：查英文单词的音标、中文释义、例句，追加到 Obsidian 单词收集器.md。支持从 Alfred 直接调用。"
tags:
  - alfred
  - obsidian
  - dictionary
  - vocabulary
---

# 单词收集器（Word Collector）

## 安装

脚本已安装在 `/Users/liangzhu/.local/bin/word-collector.py`。

## 使用方法

```bash
# 命令行
python3 /Users/liangzhu/.local/bin/word-collector.py "elaborate"

# Alfred workflow：配置为 "Run Script" 动作
# Language: /usr/bin/python3
# 参数传递方式：argv
python3 /Users/liangzhu/.local/bin/word-collector.py "{query}"
```

## 输出格式

每一条记录的格式与文件中已有的前14个条目一致：

```
{N}. {date} {word} /{phonetic}/ - {中文释义}
   - {加粗**单词**的英文例句} {例句中文翻译}
   - {第二个例句}
```

## API 依赖

- **Free Dictionary API** (`api.dictionaryapi.dev`) — 获取音标、定义和例句。免费，无需 API key。
- **MyMemory API** (`api.mymemory.translated.net`) — 英文→中文翻译。免费，有 rate limit。

## 文件路径 & 编号逻辑

**路径：** `/Users/liangzhu/Library/Mobile Documents/iCloud~md~obsidian/Documents/PKM/20_Areas/单词收集器.md`

路径包含空格和 `~`，必须写为**双引号包裹的单行完整路径**。不要用反斜杠转义（双引号内 `\` 是字面量，会造成幽灵目录），也不要多行拼接。

**编号：** 脚本取文件中已有的最大编号 +1（`stripped[:1].isdigit() and ". 20" in stripped[:10]`），不重复。

## 音标处理

API 返回的音标有些带双斜杠（`//ˈsɪn.tæks//`），有些带单斜杠。脚本通过 `phonetic.strip('/')` 统一处理，保证输出 `/{phonetic}/` 始终是单层斜杠。

## Pitfalls

- 有些单词（如 `vivid`）API 不返回例句，此时只有音标和释义，没有例句行。
- 某些罕见词可能查不到字典数据，会报 Error 退出。
- MyMemory API 偶尔超时或返回空，此时翻译回退为英文原文。