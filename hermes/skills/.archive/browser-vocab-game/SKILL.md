---
name: browser-vocab-game
description: "Build single-file HTML/JS browser interactive practice/quiz tools — vocabulary games, keyboard shortcut trainers, typing tests, or any key-detection-based exercise. Pure frontend, no server needed."
tags:
  - html
  - javascript
  - education
  - vocabulary
  - games
  - keyboard-shortcuts
  - quiz
related_skills:
  - excalidraw
  - claude-design
---

# Browser Interactive Practice Tools（浏览器交互练习工具）

## 适用场景

用户想做一款浏览器端的交互式练习/测验工具，用于记忆、技能训练或知识自测。支持实际键盘按键检测（不仅仅是输入文字匹配）。

## 已知类型
- **单词游戏**：单词从顶部飘落，输入正确拼写消除（browser-vocab-game 原始场景）
- **快捷键测验**：显示功能描述，用户按真实快捷键（Ctrl+W, Alt+B 等），页面用键盘事件检测对错
- **打字练习**：显示文本，用户逐字输入，实时统计速度和正确率

## 游戏设计模式

### 核心机制
- 单词从页面顶部**横向飘落**到底部
- 底部输入框，输入正确拼写按回车 → 单词消失（大小写不敏感，toLowerCase 对比）
- 单词掉到底部 = **miss**，记录到漏接列表
- 游戏结束时显示漏掉的单词用于复习
- 音效：正确「叮」、miss「哔」

### 可选特性
- **困难模式**：只显示中文释义，不显示英文（用户凭中文回忆英文拼写）
- **游戏前单词编辑**：开始画面提供 textarea，预填充默认词库，支持粘贴多种格式（`en - zh`、`en zh`、`编号. 日期 en /音标/ - zh`），自动限制最多 25 个单词
- **时长选择**：5 分钟或 10 分钟
- **暂停/结束按钮**：置于右下角，与输入框平齐

## 时长与结束
- 可配置时长：5 分钟或 10 分钟（开始画面下拉选择）
- 固定时长制，结束时展示漏掉单词列表
- 顶部进度条...
- HUD 显示：正确数、Miss 数、剩余活跃单词数、剩余时间
- 支持暂停/恢复（`gamePaused` 布尔值，暂停时清 interval 暂停 spawn 和 timer）
- 支持强制结束按钮（剩余单词全计 miss 后调用 endGame()）

### 难度渐变（基于 elapsedSeconds / totalSeconds 的 ratio）
- 开始时：同时活跃单词 2-3 个，下落速度 ~15px/s
- 结束时：同时活跃单词最多 10 个，下落速度 ~42px/s
- 每个单词有自己的速度（基准值 + 随机偏移）
- 生成间隔从 ~4s 逐渐缩短到 ~1.8s

---

## 快捷键测验模式（Key Detection Quiz）

### 核心机制
- 题库为 JSON 数组，每项含 `desc`（功能描述）、`name`（显示名）、`keys`（期望按键的修饰符+key）、`cat`（分类）
- 页面监听 `keydown` 事件，检测用户实际按键是否与 `keys` 匹配
- 答后显示反馈（正确/错误 + 预期键名），自动跳下一题
- 全部答完显示评分面板（正确率 + 分档颜色）

### 按键匹配逻辑

先定义题库的“规范答案”，再定义平台兼容别名；不要把浏览器 `event.key` 的显示字符直接当作物理按键真值。macOS Option/Shift 组合经常改变 `event.key`，应优先使用 `event.code` 判断物理键位，并在匹配层显式处理兼容别名。

```javascript
const KEY_MAP = {
  'a': 'a', 'b': 'b', /* ...全部字母 */ '_': '_', '.': '.',
};
// 特殊键名映射
const specialKeys = {
  'arrowleft': 'ArrowLeft', 'arrowright': 'ArrowRight',
  'arrowup': 'ArrowUp', 'arrowdown': 'ArrowDown',
  'backspace': 'Backspace', 'enter': 'Enter', 'escape': 'Escape',
  'delete': 'Delete', 'tab': 'Tab', ' ': ' ',
};
// 修饰键匹配
const ctrlMatch = (e.ctrlKey || e.metaKey) === !!expected.ctrl;
const altMatch = e.altKey === !!expected.alt;
const shiftMatch = e.shiftKey === !!expected.shift;
const keyMatch = expectedKey === pressedKey;
```

### 组合键格式化显示
```javascript
function formatKeyName(e) {
  const parts = [];
  if (e.ctrlKey || e.metaKey) parts.push('Ctrl');
  if (e.altKey) parts.push('Alt');
  if (e.shiftKey && !arrowKeys) parts.push('Shift');
  parts.push(keyDisplay);
  return parts.join('+');
}
```

### 测验生命周期控制（纯按钮，无快捷键）
- **"开始"按钮**：调用 resetQuiz() 重置全部状态
- **"结束"按钮**：提前终止测验，所有剩余未答题记为错误/跳过，立即显示评分
- **不要在键盘事件中绑定 Ctrl+R 或 Ctrl+S 作为控制快捷键**，它们可能与题库冲突

### 按钮布局策略
- 按钮顺序（从左到右）：**开始（主题色）** | **结束 →** | **继续 →（默认隐藏）**
- 最右侧独立放置 ↻ 重新开始图标按钮（`margin-left: auto` 实现右对齐）
- "开始"按钮调用 resetQuiz() 重置所有状态
- "结束"按钮提前终止测验，剩余题目全记错误
- "继续"按钮只在答错或知识题时可见
- ↻ 按钮在任何时候点击都完全重置

### 知识题（无法键盘检测的题目）
- 题库中 `keys: null` 的题目标记为知识题（如 `!!`、`!$`）
- 知识题自动显示答案和描述，不要求用户按键
- 用户点击继续时直接记为正确（因为这只是展示性知识题）

### 分类筛选
- 题库每项有 `cat` 分类字段（cursor, delete, edit, history, system 等）
- 顶部渲染分类按钮栏，点击后只展示选中分类的题目
- 切换分类时自动重置测验状态

## 关键实现要点

### 词库提取
从 Markdown 单词文件提取英文词和中文释义：

```javascript
// 标准格式：
// 15. 2026-06-18 syntax /ˈsɪn.tæks/ - 中文释义
//    - 例句
const words = [
  { en: "syntax", cn: "语法" },
  { en: "vector", cn: "向量" },
];
```

### 下落动画
- 每个单词是一个 `div`，绝对定位
- 用 `requestAnimationFrame` 更新 `top` 值
- 每个单词有自己的速度变量（`baseSpeed + randomOffset`）
- 到达底部阈值 → 触发 miss（从数组中移除 + 移除 DOM 节点）

### 难度控制：getDifficulty 函数
```javascript
function getDifficulty(t) {
  const ratio = Math.min(t / totalSeconds, 1);
  return {
    spawnInterval: Math.max(1800, 4000 - ratio * 2500),
    speed: 0.25 + ratio * 0.45,  // px per frame (~60fps)
    maxActive: Math.floor(3 + ratio * 7),
  };
}
```
ratio 从 0→1 线性渐变，所有参数平滑变化。

### 计时器
```javascript
let timeLeft = 600; // 10 minutes
const timerInterval = setInterval(() => {
  if (timeLeft <= 0) { endGame(); return; }
  timeLeft--;
}, 1000);
```
- 顶部进度条 = `(timeLeft / totalSeconds) * 100%`
- CSS transition: width 1s linear 实现平滑动画

### 音效（Web Audio API，无需外部文件）
```javascript
function playCorrect() {
  const ctx = new AudioContext();
  const osc = ctx.createOscillator();
  const gain = ctx.createGain();
  osc.connect(gain).connect(ctx.destination);
  osc.type = 'sine';
  osc.frequency.setValueAtTime(880, ctx.currentTime);
  osc.frequency.setValueAtTime(1100, ctx.currentTime + 0.08);
  gain.gain.setValueAtTime(0.15, ctx.currentTime);
  gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.3);
  osc.start(); osc.stop(ctx.currentTime + 0.3);
}

function playMiss() {
  const ctx = new AudioContext();
  const osc = ctx.createOscillator();
  const gain = ctx.createGain();
  osc.frequency.setValueAtTime(200, ctx.currentTime);
  gain.gain.setValueAtTime(0.1, ctx.currentTime);
  gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.4);
  osc.start(); osc.stop(ctx.currentTime + 0.4);
}
```
- 使用 `sine` 波形，轻柔不刺耳
- `AudioContext` 需要在用户交互后初始化（点击"开始"时创建）

### 结束画面
- 游戏停止：清除所有 interval 和 animation frame
- 遍历 activeWords 中仍 active 的单词 → 去重 → 按字母排序 → 渲染到 miss-list DOM
- 显示总分和总 miss 数
- "再来一局"按钮调用 startGame() 重置所有状态

### 输入匹配 — 优先消最靠近底部的单词
- 输入框监听 `keydown` 事件，回车时触发匹配
- 当页面出现多个相同的单词时，**优先消除最靠近输入框的那个**（y 坐标最大的）
- 遍历所有活跃单词，找出匹配英文且 y 值最大的索引，而不是从数组末尾找
- 正确匹配后，单词先变绿（加 correct class），250ms 后移除 DOM
- 输入框边框闪绿（正确）或闪红（错误），200ms 恢复
- 匹配后清空输入框

## 项目文件建议
- `index.html` — 主页面（HTML + CSS + JS 全部内嵌或用 `<link>/<script>` 引入）
- 运行时只需在浏览器打开

## 参考文件
- `references/terminal-shortcuts-quiz.md` — 终端快捷键测验完整题库 JSON 数据（含该用户最新版 27 题），可直接嵌入 HTML
- `references/10min-timer-implementation.md` — 10 分钟计时器实现细节
- `references/known-bugs.md` — 快捷键测验已知 Bug：Ctrl+_ Mac 兼容性、Alt+. 输入法干扰、Ctrl+F/→ 功能重复等

## Pitfalls

### 音效
- 使用 Web Audio API 生成简单音效（不需要外部音频文件）
- 正确音：短促高音（880→1100Hz，正弦波）
- miss 音：低频短促（200→150Hz，正弦波）
- 浏览器需要用户交互后才能播放音频（AudioContext 必须在用户点击后创建）
- **必须复用同一个 AudioContext**：全局 `let audioCtx = null`，`initAudio()` 只在首次调用时 new，之后复用。每次 play 都 new AudioContext 会导致声音重叠/混乱
- 增益（gain）控制在 0.1~0.15
- `exponentialRampToValueAtTime(0.001, ...)` 做淡出，避免截断声

### 键盘检测（快捷键测验模式）
- **过滤纯修饰键**：`e.key === 'Control'`、`e.key === 'Alt'` 等必须在前置判断中跳过，否则用户按 Ctrl 准备按 Ctrl+B 时，Ctrl 单独就会触发一次错误判定
- **"按任意键开始"不判题**：初始状态 `state.started = false`，按任意键只设置 started=true 并切换到第一题，不调用 checkShortcut
- **Ctrl+_ 在 Mac 无法直接触发**：Mac 键盘上 `_` 需要 Shift+-，浏览器事件为 `Ctrl+Shift+-` 或 `Ctrl+Shift+_`。匹配 `expected.key === '_'` 时必须放宽 `shiftMatch`，并接受 `event.key` 为 `_`、`-`、`=` 的情况；不能只改 `keyMatch`，否则会被前面的 `shiftMatch` 拦截。详见 `references/known-bugs.md`
- **Alt+. 受输入法/Option 键干扰**：中文输入法或 macOS Option 可能让 `event.key` 变成 `≥`、`>`、`。`；按 `expected.alt && expected.key === '.'` 时接受这些别名，并不要强制排除 `shiftKey`。最好同时用 `event.code === 'Period'`，但保留字符别名兼容。
- **Alt+B / Alt+F 误判**：macOS Option 可能把字符变成特殊 Unicode；当期望为 Alt+B/F 时，用 `event.code === 'KeyB'/'KeyF'` + `altKey` 判断，不要只比较 `event.key`。
- **“按任意键开始”不判题**：初始状态 `state.started = false`，按任意键只设置 started=true 并切换到第一题，不调用 checkShortcut
- **避免功能重复的快捷键同时入库**：如 Ctrl+F 和 → 都做“光标右移”，通常只保留一个；若保留多个，必须在题目中明确它们是等价答案，并让匹配器按功能组处理
- **方向键 ↑↓ 保留默认行为**：只对方向键放行 `e.preventDefault()`，防止用户无法滚动页面
- **不要使用 Ctrl+R/S 作为全局快捷键**：它们很可能在题库中作为题目出现
- **错误后不要自动跳题**：错误时固定显示实际按键和正确答案，显示“继续”按钮；回车只在继续按钮可见时触发 continue，避免用户误按导致重复判题

### 性能
- 单词 DOM 元素超过 50 个时可能卡顿
- 用 `requestAnimationFrame` 而不是 `setInterval` 驱动动画
- 离开的单词要移除 DOM 节点（不是隐藏）

### 输入体验
- 输入框需要 `autofocus`，但浏览器只在用户交互后允许 autofocus
- 正确匹配后清空输入框并保持焦点
- 支持大小写不敏感匹配（`.toLowerCase()` 对比）
- 用户误输后按退格可以修改，不影响游戏

### 页面结构
- 开始画面和结束画面是独立的 full-screen overlay（position: fixed, z-index: 200）
- 开始画面包含标题 + 一句话说明 + 开始按钮
- 结束画面包含漏掉单词列表 + 再来一局按钮
- 游戏区域（#game-area）在 overlay 下方
- 输入框固定在 bottom，输入区域需要 backdrop-filter 提升可读性