# Obsidian URI (URL Scheme)

Obsidian 支持 `obsidian://` URL scheme 来打开笔记、执行搜索、创建新笔记。这是**跳转显示**的方案 — 让用户看到笔记内容，不替代文件系统级的读写。

## 基础语法

```bash
# 打开 vault 的根目录
open "obsidian://open?vault=VAULT_NAME"

# 打开特定笔记
open "obsidian://open?vault=VAULT_NAME&note=NoteName"

# 搜索
open "obsidian://search?vault=VAULT_NAME&query=keyword"

# 创建新笔记（Obsidian 会询问文件名）
open "obsidian://new?vault=VAULT_NAME&name=NewNote&content=Initial+content"
```

## macOS: `open` 命令

macOS 的 `open` 会自动注册 obsidian:// 协议，直接执行即可。

```bash
open "obsidian://open?vault=PKM&note=MyNote"
```

## 注意事项

1. **vault 名是 Obsidian 里显示的名称**，不是文件夹名（虽然通常一样）。不匹配时 Obsidian 会提示。
2. **NoteName 不带 `.md`** 后缀。
3. **空格用 URL 编码 `%20`**，但多数 Obsidian 版本也接受直接空格（被 `open` 自动处理）。
4. **非 macOS 平台**：Linux 用 `xdg-open`，Windows 用 `start`。
5. URI 仅用于跳转显示，**不能替代文件工具**来读写内容。创建笔记后仍需用 `write_file` 写入内容。

## 适用场景

| 场景 | 手段 | 原因 |
|------|------|------|
| 创建/编辑/搜索笔记 | 文件系统工具（read_file, write_file, search_files） | 更可靠，支持批量，不依赖 Obsidian 是否运行 |
| 跳转展示给用户看 | obsidian:// URI | 用户直接看到笔记在 Obsidian 里的渲染效果 |
| 提醒用户看某个笔记 | obsidian:// URI | 用户只需点一下就能跳转 |