# cmux & Ghostty 终端配置参考

> cmux 是基于 Ghostty 的 macOS 原生终端应用，支持 Ghostty 主题系统

## 主题配置

cmux 使用 Ghostty 的主题系统。配置方式：

1. **创建配置文件** `~/.config/ghostty/config`：

```
theme = Atom One Light
```

2. **生效方式**：重启 cmux 或按 `Cmd+Shift+,` 重载配置

3. **主题文件查找顺序**：
   - `~/.config/ghostty/themes/<名称>`（自定义主题）
   - cmux.app bundle 内：`/Applications/cmux.app/Contents/Resources/ghostty/themes/`
   - Ghostty.app bundle 内（如果安装了）

## 推荐浅色主题

| 主题 | 特点 |
|------|------|
| **Atom One Light** | VS Code 默认浅色主题的蓝本，简洁清晰 |
| **GitHub Light Default** | GitHub 风格，对比度更高 |
| **Catppuccin Latte** | 流行浅色方案，柔和护眼 |
| **Solarized Light** | 经典护眼浅色主题 |
| **Xcode Light** | Xcode 风格 |

## 自定义主题

创建 `~/.config/ghostty/themes/my-theme`，格式与 Ghostty config 相同：

```
palette = 0=#000000
palette = 1=#cc0000
...
background = #ffffff
foreground = #000000
```

然后在 `~/.config/ghostty/config` 中引用：

```
theme = ~/.config/ghostty/themes/my-theme
```

## 条件主题（明/暗）

支持根据系统外观自动切换：

```
theme = dark:monokai,light:solarized light
```

## 常用终端信息查看命令

```bash
echo "$TERM"                # 终端类型（cmux 下为 xterm-256color）
echo "$TERM_PROGRAM"        # 终端程序名（ghostty）
cat ~/.config/ghostty/config
```

## 排查黑色字看不清的问题

Codex CLI 等工具的更新界面使用黑色文字。在白色背景 + cmux 默认主题下可能难以辨认。解决：

1. 设置一个浅色主题（如 `Atom One Light`），确保前景色有足够对比度
2. 或直接在配置中覆盖 `foreground` 颜色为更深色号

## 注意

- cmux 的 `~/.config/cmux/cmux.json` 默认配置模板不包含主题设置，主题由 Ghostty config 控制
- 主题名称中带空格的需要原样写入：`theme = Atom One Light`