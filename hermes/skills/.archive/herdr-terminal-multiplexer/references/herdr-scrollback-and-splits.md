# Herdr 分屏与滚动：核验笔记

## 官方键盘文档要点

来源：<https://herdr.dev/docs/keyboard>

- Herdr 使用 prefix 将按键从 pane 内程序中接管；默认 prefix 是 `Ctrl+B`。
- 进入 copy mode：`Ctrl+B`，然后 `[`。
- copy mode 中可用 `h/j/k/l`、tmux 风格的 `w/b/e`、`{`/`}`、`PageUp`/`PageDown`、`Ctrl+B`/`Ctrl+F`、`Ctrl+U`/`Ctrl+D` 移动。
- 默认 prefix 在 copy mode 中仍有特殊含义；如果希望把 `Ctrl+B` 当作向上翻页，需要更换 prefix。

## 关键限制

### Copy mode 视图可能无法冻结

GitHub issue #680：
<https://github.com/ogulcancelik/herdr/issues/680>

报告称 pane 持续输出时，进入 copy mode、鼠标滚动或选择文本后，显示缓冲区仍继续推进，无法稳定停在开始阅读的位置。这是解释“滚动时上下内容似乎一起动”时的重要已知线索，但不能据此断定所有分屏都共享同一个 scroll buffer。

### Alternate-screen TUI 没有完整普通 scrollback

GitHub issue #1304：
<https://github.com/ogulcancelik/herdr/issues/1304>

全屏 TUI（例如 vim、less、htop 和部分 Agent CLI）使用 alternate screen 时，`pane read --source recent` 只能获得接近当前视口的内容，无法像普通 Shell pane 那样获得完整历史。用户想要 tmux 的 `alternate-screen off` 等价配置，但该 issue 记录的需求并非完整解决方案。

## 推荐复现记录格式

报告 Herdr 分屏滚动问题时收集：

```text
Herdr version:
OS:
Terminal emulator:
Shell:
Split shortcut:
Scroll method: mouse / trackpad / keyboard
Foreground app in pane 1:
Foreground app in pane 2:
Does selecting the pane change the result?
Does Ctrl+B then [ isolate the view?
Does the pane use a full-screen TUI / alternate screen?
```

## 解释边界

- Terminal.app 的原生分屏是两个独立终端视图，因此用户通常感受到滚动局部化。
- Herdr 的分屏是一个 multiplexer/server 管理的多个 PTY pane；焦点、输入路由、viewport 和前台程序的鼠标协议会影响滚动表现。
- 不要把“视觉上两个 pane”直接等同于“两个独立的 Terminal.app scrollback”。先区分普通模式、copy mode、前台程序接管鼠标，以及 alternate-screen。
