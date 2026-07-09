# 10分钟倒计时单词游戏 — 完整实现参考

## 项目位置

`/Users/liangzhu/Project/word-rain/index.html`

## 核心架构

### 文件拆分（参考用，实际全部内嵌在 index.html）

- `words.js` — 词库 JSON 数组
- `index.html` — 所有 HTML + CSS + JS（内嵌）
- 无需构建工具，浏览器直接打开

### 状态变量

```
gameRunning: bool          — 游戏是否运行中
activeWords: []            — 当前活跃的单词对象数组
score/missCount            — 统计数据
timeLeft: 600              — 10分钟计时
wordIdCounter              — 生成唯一 ID
```

### 生命周期

1. **开始画面** → 点击"开始游戏" → `startGame()`
2. **游戏循环** — `requestAnimationFrame` 驱动动画 + `setInterval` 驱动计时器 + `setInterval` 驱动生成
3. **时间到** → `endGame()` → 显示漏掉单词列表

### 单词对象结构

```javascript
{
  el: DOM元素,
  en: "vector",
  zh: "向量",
  x: Number,           // left px
  y: Number,           // top px
  speed: Number,       // px/frame
  active: Boolean,
  domId: Number
}
```

### 词库 18 单词（当前内容）

vector, slice, frame, section, established, regenerate, collaborators, hover, component, variant, inspection, blur, dispersion, rectangular, identical, suppression, orientation, tangent

## 样式要点

- 深色背景 `#0f0f1a`，亮白蓝色字体 `#7ec8e3`
- 中文释义用较小字号 `#8888aa`
- 正确：变绿 `#4ade80` + 发光阴影
- HUD：半透明浮动顶栏，四个指标
- 进度条：顶部 3px 渐变条 `#7ec8e3 → #4ade80`
- 输入框：底部固定，半透明模糊背景，圆角
- 结束画面：漏掉列表红色英文 + 灰色中文

## 扩展方式

- 新单词只需追加到 `WORD_DB` 数组
- 调整 `GAME_DURATION` 常量可以改游戏时长
- 调整 `getDifficulty` 的系数可以改难度曲线
- 可添加计分规则（正确连续数、速度加分等）