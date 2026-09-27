# PARA + Decimal 标签系统设计指南

## 适用场景

用户需要重新设计或优化 Obsidian vault 的标签体系时使用。

## 工作流

### 1. 发现阶段

- 读取 vault 根目录结构（文件夹）
- 搜索 .md 文件的标签使用情况（`#tag` 正则提取）
- 查找已有的标签系统文档（如 `标签系统搭建.md`、`PARA 系统.md`）
- 列出实际笔记文件清单

### 2. 分析现有问题

常见问题模式：
- 设计与实践脱节（设计了层级树但游离标签很多）
- 标签颗粒度不一（`#excel` 和 `#excel宏` 并存）
- 子层级太深（3层以上使用率很低）
- 没有 MOC 索引笔记聚合内容

### 3. 设计方案

PARA + Johnny Decimal 混合：
- **P** (10-19) Projects — 有截止日期的项目任务，用完即归档
- **A** (20-49) Areas — 长期责任领域，需持续维护
- **R** (50-79) Resources — 持续感兴趣的主题/知识库
- **Z** (90-99) Archives — 非活跃条目
- **d/** — 日记/日志
- **t/** — 模板

设计原则：
- 编码范围预留扩展空间（每10个之间留空）
- 标签深度 ≤ 2 层（如 `#a/工作/弱电` 可，`#a/工作/弱电/视频监控` 不可）
- 一笔记一核心标签，最多不超过 3 个
- 项目标签用完即删，归档改标
- 标签 + 文件夹双轨制

### 4. 迁移对照表

为每个游离标签建立映射关系：
```
旧标签 → 新标签
#excel宏 → #r/tools/excel
#AI → #r/AI
```

### 5. 落地文件

生成一个架构文档存放在 vault 中（如 `pages/标签系统-PARA架构.md`），包含：
- 核心理念说明
- 编码总览表
- 每个分区的标签/编码/说明表
- 迁移对照表
- 使用规则

### 6. 执行迁移

架构和迁移计划确认后，开始物理迁移：

**6a. 搬文件**

用 bash 脚本批量 move，避免逐条手动操作：

```bash
cat > /tmp/migrate_batch.sh << 'SCRIPT'
cd "/path/to/vault"
mv "00_Inbox/某个笔记.md" "20_Areas/"
mv "00_Inbox/另一个笔记.md" "30_Resources/"
SCRIPT
bash /tmp/migrate_batch.sh
```

技巧：
- 按目标文件夹分组，每批 5-10 个文件
- `cat > /tmp/xxx.sh << 'SCRIPT'` 搭配 `bash /tmp/xxx.sh` 避免流超时
- 文件名含特殊字符（`[`、`（`、空格）时加双引号
- 每批执行完后检查目标文件夹确认已搬入

**6b. 添加标签**

同样用脚本批量处理，推荐 Python：

```python
import os
def tag(folder, filename, tag_text):
    path = os.path.join(vault, folder, filename)
    if not os.path.exists(path): return
    with open(path,'r') as f: c = f.read()
    with open(path,'w') as f: f.write(tag_text + '\n\n' + c)
```

将脚本写入 `/tmp/tag_all.py` 后执行 `python3 /tmp/tag_all.py`。

**6c. 收尾**
- 确认每个 PARA 文件夹的文件数合理
- 验证几个重点文件的标签已正确添加（`head -1`）
- 更新迁移计划中的执行步骤状态
- 未分类笔记留在 `00_Inbox/` 中

## 相关技巧

### 提取 vault 中所有标签

用 Python 配合正则提取，排除十六进制颜色值：

```python
import re, os
tag_re = re.compile(r'(?<![#\w])#([\w/]+)(?![#\w])')
hex_re = re.compile(r'^[0-9a-fA-F]{3,8}$|^(fff|000)$')
```

### 大文件写入变通

当 `write_file` 内容过大导致超时，改用 `terminal` + heredoc 分批追加：

```bash
cat > "path/to/file.md" << 'ENDOFFILE'
# 第一部分内容
ENDOFFILE

cat >> "path/to/file.md" << 'ENDOFFILE'
## 第二部分内容
ENDOFFILE
```

### 2026-06-17 补充

#### 文件夹命名规范
- 使用下划线代替空格：`10_Projects/`、`20_Areas/`
- Archives 建议用 90 范围（而非 80），避免与 Resources 冲突：`90_Archives/`
- 收件箱命名：`00_Inbox/`（替代传统的 `pages/` 或 `Inbox/`）

#### 迁移计划生成（第 5.5 步）

设计完标签架构后，补充迁移计划文档：

1. 批量读取 00_Inbox 中所有笔记的第一行内容
2. 根据文件名 + 内容判断分类
3. 生成迁移计划 MD，格式：

```
| 笔记 | 目标文件夹 | 建议标签 |
|------|-----------|----------|
| xxx.md | 20_Areas/ | #a/工作/广联达 |
```

4. 包含一个迁移对照表（旧标签 → 新标签）
5. 未分类笔记留在 00_Inbox/

#### 大文件编辑变通

当 patch/write_file 因内容过大超时时：

- 优先用 sed 单行操作（替换、插入）
- 对复杂内容先用 sed 删除大块（`sed -i '' 'M,Nd'`），再少量追加
- 每一步只加 5-10 行内容，避免超时