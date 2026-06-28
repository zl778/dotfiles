#a/learning/system

## 壹 起因：
mac系统级快捷键 协同了word
- **移动光标**
 - Ctrl + A：到行首（你已经在用）。StartOfLine
 - Ctrl + E：到行尾（你已经在用）。EndOfLine
 - Ctrl + F：向右移动一个字符（相当于右方向键）。CharRight
 - Ctrl + B：向左移动一个字符（相当于左方向键）。CharLeft
 - Ctrl + N：向下一行。LineDown
 - Ctrl + P：向上一行。LineUp
 -  **删除与编辑**
- Ctrl + D：删除光标后的一个字符（类似 Delete）。
- Ctrl + H：删除光标前的一个字符（类似退格 Backspace）。
- Ctrl + K：从光标删到行尾。（很多人拿它当「清空到行尾」用。）
- Ctrl + U：从光标删到行首（部分场景等价于 Command + Delete）。DeleteBackWord

## 贰 基本情况了解：
### 一、基础生存技巧（需强记）

| 操作    | 快捷键       | 说明                                        |
| ----- | --------- | ----------------------------------------- |
| 退出    | `C-x C-c` | `C` = Ctrl，先按 `Ctrl+x` 再按 `Ctrl+c`        |
| 保存    | `C-x C-s` | 保存当前文件                                    |
| 打开文件  | `C-x C-f` | "find file"，可新建文件                         |
| 切换缓冲区 | `C-x b`   | 列出已打开文件，快速切换                              |
| 取消命令  | `C-g`     | 任何操作卡住时按它                                 |
| 帮助系统  | `C-h t`   | 官方交互式教程（新手必做）  <br>`C-h k` + 快捷键：查看该快捷键功能 |
|       |           |                                           |
|       |           |                                           |

> 💡 **记忆法**：`C-x` 是“文件级操作”前缀（如保存/打开），`C-c` 是“用户自定义操作”前缀。
---

### 二、高效编辑技巧（日常高频，M键其它应用无法映射）

#### 1. 光标移动（比方向键快 3 倍）

| 操作     | 快捷键                |
| ------ | ------------------ |
| 前/后移一字 | `M-f` / `M-b`      |
| 上/下移一行 | `C-n` / `C-p`      |
| 行首/行尾  | `C-a` / `C-e`      |
| 滚动一屏   | `C-v`（下）/ `M-v`（上） |
#### 2. 选择与编辑（需强记）

C-@ 或 C-SPC   →  开始选中（set mark）
然后移动光标    →  自动高亮选中区域
M-w            →  复制（copy）
C-w            →  剪切（kill）
C-y            →  粘贴（yank）
M-y            →  粘贴历史中上一个剪切内容（循环切换）
#### 3. 撤销/重做

- 撤销：`C-/` 或 `C-_` 或 `C-x u`
- 重做：较新版本支持 `C-x C-/`，或重复撤销回到目标状态

---
### 三、进阶效率技巧

#### 1. 多窗口操作

| 操作     | 快捷键              |
| ------ | ---------------- |
| 水平分屏   | `C-x 2`          |
| 垂直分屏   | `C-x 3`          |
| 切换窗口   | `C-x o`（"other"） |
| 关闭当前窗口 | `C-x 0`（数字零）     |
| 关闭其他窗口 | `C-x 1`          |

> ✅ 场景：一边看代码一边查文档，无需频繁切换文件。

#### 2. 搜索与替换

- 增量搜索：`C-s`（向前）/ `C-r`（向后），边输入边匹配
- 替换：`M-%` → 输入查找词 → 输入替换词 → 按 `y/n/a` 逐个/跳过/全部替换

#### 3. 快速跳转

- 跳转到行号：`M-g g` → 输入行号 → 回车
- 回到上次编辑位置：`C-x C-SPC`（配合 `C-SPC` 标记位置）

---

### 四、macOS 特定优化

#### 1. 解决快捷键冲突

macOS 中 `Option` 键默认是输入特殊字符（如 `Option+e` → ´），需在 Emacs 配置中声明：
;; ~/.emacs 或 ~/.emacs.d/init.el 中添加
(setq mac-option-key-is-meta t)    ;; Option 作为 Meta
(setq mac-command-key-is-meta nil) ;; Command 保持原功能

#### 2. 快速调用系统剪贴板

- 复制到系统剪贴板：`M-w` 后内容自动同步（GUI 版）
- 从系统粘贴：`C-y` 或直接 `Cmd+V`（GUI 版）



### 五、最小化配置建议（`~/.emacs`）

elisp
;; 基础体验优化
(setq inhibit-startup-message t)        ; 去掉启动画面
(global-linum-mode t)                   ; 显示行号（Emacs 26+ 用 (global-display-line-numbers-mode)）
(setq-default indent-tabs-mode nil)     ; 用空格代替 Tab
(setq-default tab-width 4)              ; Tab 宽度 4 空格

;; 快捷键增强
(global-set-key (kbd "C-c l") 'goto-line)  ; C-c l 快速跳转行号

;; 主题（可选）
(load-theme 'wombat t)  ; 内置暗色主题

> 💡 配置后重启 Emacs 或 `M-x eval-buffer` 重载配置。

---

### 六、避坑指南

|问题|解决方案|
|---|---|
|按 `C-g` 退出“卡住”状态|例如误触 `C-x` 后不知下一步，按 `C-g` 取消|
|想退出却弹出保存提示|先 `C-x C-s` 保存，再 `C-x C-c` 退出|
|`M-` 快捷键无效|检查终端设置 → Terminal → Preferences → Profiles → Keyboard → 勾选 "Use Option as Meta key"|
|想用鼠标但没反应|GUI 版支持鼠标；终端版建议专注键盘操作|

---

### 七、学习路径推荐

1. **第一天**：运行 `emacs -nw` → 按 `C-h t` 完成官方教程（约 30 分钟）
2. **第一周**：强制自己只用 `C-f/b/n/p/a/e` 移动，放弃方向键
3. **第二周**：练习 `C-SPC` 选中 + `M-w/C-w/C-y` 复制剪切粘贴
4. **长期**：逐步添加配置，按需安装插件（如 `magit` 管理 Git）

> 🔑 核心理念：**Emacs 不是“记住所有快捷键”，而是形成肌肉记忆后“思考不停顿”**。初期慢，熟练后效率远超 GUI 编辑器。

---

### 附：常用快捷键速查卡

text
C = Ctrl    M = Meta (Option/Esc)
C-x C-f   打开文件        C-x C-s   保存
C-x C-c   退出            C-g       取消
C-a / C-e 行首/行尾       C-n / C-p 上/下一行
M-f / M-b 前/后移一字     C-v / M-v 下/上翻页
C-SPC     开始选中        M-w       复制
C-w       剪切            C-y       粘贴
C-s       搜索            M-%       替换
C-x 2/3   分屏            C-x o     切换窗口
需坚持 2~3 周刻意练习，你会感受到“手指自己知道该按什么”的流畅感

## 叁 试用日志：
安装：
brew install emacs
制裁主程序
brew uninstall emacs
清理无用依赖
brew autoremove
验证卸载
which emacs
emacs --version

## 肆 放弃原因：
备忘录、Word、Obsidian、Vscode均不支持扩展EMACS。软件过于古早，社区支持很差，学习成本高，适用场景少。
