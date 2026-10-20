# cmux 终端主题配置 & Codex CLI 颜色排错

## cmux 是什么

cmux 是一个基于 Ghostty 的 macOS 原生终端，支持 Ghostty 主题系统。
你的 cmux 版本：cmux（基于 libghostty），终端类型 xterm-256color。

## 主题配置

### 配置文件位置

```bash
~/.config/ghostty/config
```

### 格式

```bash
theme = Catppuccin Mocha
```

### 可用主题列表

```bash
ls /Applications/cmux.app/Contents/Resources/ghostty/themes/
```

常见选择：

| 主题 | 风格 |
|------|------|
| Catppuccin Mocha | 紫色调深色，当前在用 |
| Tokyo Night | VS Code 风格，蓝紫色 |
| Atom One Light | 浅色简洁 |
| GitHub Light Default | 浅色高对比度 |
| Nord | 冰雪蓝灰，护眼 |
| Dracula | 经典高对比度紫色系 |

### 重载配置

修改后按 **Cmd+Shift+,**（在 cmux 里）立即生效，无需重启 cmux。

## Codex CLI 颜色排错

### 典型问题

Codex CLI 的更新提示界面（`✨ Update available!`）或某些 UI 元素显示为**白底黑字**，
在深色 cmux 主题下黑字看不清楚。

### 原因

Codex CLI（当前版本 0.142.5）内部**硬编码颜色**：
- 更新提示界面强制使用白色背景 + 黑色文字
- 部分 UI 元素使用灰色背景（如输入框区域）
- 终端主题（cmux/Ghostty）无法控制这些内部颜色

这是 Codex 的已知问题（GitHub issue #2020）。

### 解决方法

在 Codex TUI 界面中输入 **`/theme`**：

1. 启动 Codex（`codex`）
2. 进入 TUI 后输入 `/theme` 并回车
3. 选择 **Dark** 主题
4. Codex 内部配色会切换到深色方案，文字变为白色

### 验证

```bash
codex --version
# 应看到 codex-cli 0.142.5
```

`/theme` 功能从 Codex 0.105.0 开始支持。

## Dotfiles 同步建议

```bash
# 将 cmux/Ghostty 配置加入 dotfiles
mkdir -p ~/dotfiles/ghostty
cp ~/.config/ghostty/config ~/dotfiles/ghostty/config
# 同时在 sync.sh 中添加：
# cp "$HOME/.config/ghostty/config" "$DOTFILES/ghostty/config"
```