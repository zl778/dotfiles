---
name: browser-vocab-game
description: "Build single-file HTML/JS browser games for vocabulary practice — words fall from top, user types to dismiss, difficulty ramps over time. Pure frontend, no server needed."
tags:
  - html
  - javascript
  - education
  - vocabulary
  - games
---

# 浏览器单词游戏（Browser Vocabulary Game）

## 适用场景

用户有 Markdown 格式的单词列表（如 Obsidian 里收集的单词），想做一款打字练习游戏来背单词。

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

### 难度渐进（基于 elapsedSeconds / totalSeconds 的 ratio）
- 开始时：同时活跃单词 2-3 个，下落速度 ~15px/s
- 结束时：同时活跃单词最多 10 个，下落速度 ~42px/s
- 每个单词有自己的速度（基准值 + 随机偏移）
- 生成间隔从 ~4s 逐渐缩短到 ~1.8s

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

## Pitfalls

### 音效\n- 使用 Web Audio API 生成简单音效（不需要外部音频文件）\n- 正确音：短促高音（880→1100Hz，正弦波）\n- miss 音：低频短促（200→150Hz，正弦波）\n- 浏览器需要用户交互后才能播放音频（AudioContext 必须在用户点击后创建）\n- **必须复用同一个 AudioContext**：全局 `let audioCtx = null`，`initAudio()` 只在首次调用时 new，之后复用。每次 play 都 new AudioContext 会导致声音重叠/混乱\n- 增益（gain）控制在 0.1~0.15\n- `exponentialRampToValueAtTime(0.001, ...)` 做淡出，避免截断声

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