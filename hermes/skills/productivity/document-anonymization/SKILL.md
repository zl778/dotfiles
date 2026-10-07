---
name: document-anonymization
description: Use for Office anonymization. Strip metadata and validate.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [office, metadata, anonymization, ooxml]
    related_skills: [officecli]
---

# Office 文档匿名化

## When to Use

用户要求 Office 文件另存为无作者、无元数据、匿名或可脱敏版本时使用。

适用于需要“另存一份、去除作者/元数据、保留原文件”的 `.docx`、`.xlsx`、`.pptx` 等 OOXML 文档。

## 标准流程

1. 先枚举并确认输入文件，按用户要求匹配文件名；不要凭猜测处理相似文件。
2. 生成同目录副本，使用明确的 `_无元数据` 或 `_匿名` 后缀，绝不覆盖原文件。
3. 对副本执行 OOXML 包级处理：
   - 清空 `docProps/core.xml` 与 `docProps/app.xml` 的属性子元素；
   - 删除 `docProps/custom.xml`；
   - 在所有 XML 和关系文件中将 `author`、`creator`、`lastModifiedBy` 等作者类属性置空，覆盖评论、修订和其他部件中的身份字段；
   - 不改动正文、表格、图片、格式和可见业务内容。
4. 对每个副本运行 `officecli validate <file>`；验证失败时不得声称完成。
5. 回读验证：检查输出数量与输入数量一致，确认核心/应用属性为空、自定义属性不存在，并检查 XML 中没有残留作者类属性。
6. 最终报告原目录、确切输出文件名、未覆盖原文件和验证结果。

## 工具选择与可靠性

优先使用可重复运行的 Python `zipfile` + XML 脚本（见 `scripts/strip_ooxml_metadata.py`），而不是把长脚本塞入 shell 的 `python -c`。对含中文、空格或 OneDrive 同步路径的文件，脚本内部使用 `pathlib.Path`；shell 转义可能把 Unicode 路径变成字面量 `\\uXXXX`，造成误报文件不存在。

对于大型文件，使用低压缩级别或保留 ZIP 条目结构以减少等待，但仍须完成最终 `officecli validate`。写入外部目录前先确认副本命名和范围；用户明确同意后再执行批量写入。

## 边界

“去元数据”不等于删除正文中出现的公司名、签名、联系方式或扫描件中的可见信息；这类内容属于业务内容，除非用户另行要求，不要修改。图片 EXIF、嵌入对象和 PDF 内部元数据可能需要对应格式的专用处理，不要把 OOXML 验证结果扩大解释为所有嵌入内容都已匿名化。

## 验收标准

- 原文件仍存在且未被覆盖；
- 每个目标副本都能打开并通过 `officecli validate`；
- `docProps/core.xml`、`docProps/app.xml` 无属性子元素；
- `docProps/custom.xml` 不存在；
- XML 中作者类属性无非空值；
- 输出数量与用户要求一致。
