# 终端快捷键测验题库

用于 browser-vocab-game 技能中的"快捷键测验"模式。完整的题库 JSON 数据可直接嵌入 HTML。

## 题库结构

每项格式：
```javascript
{
  keys: {
    ctrl: true/false,    // 需要 Ctrl（macOS 上 Cmd 也视为 Ctrl）
    alt: true/false,     // 需要 Alt/Option
    shift: true/false,   // 需要 Shift
    key: '键名'           // event.key 的值，如 'a', 'Backspace'
  },
  name: '显示名（如 Ctrl+W）',
  desc: '功能描述',
  cat: '分类标识符',
}

// 无法键盘检测的题目（如 !!、!$）：
{
  keys: null,             // 标记为知识题
  name: '!!',
  desc: '执行上一条命令',
  cat: 'special',
}
```

## 该用户最新题库（24 题）

按用户最新提供的列表顺序（2026-07-17 最终版），已删除方向键 ←→ 两题：

```javascript
const SHORTCUTS = [
  // 编辑/移动
  { keys: { ctrl: true, key: 'q' },     name: 'Ctrl+Q',      desc: '消除当前输入',                        cat: 'edit' },
  { keys: { ctrl: true, key: 't' },     name: 'Ctrl+T',      desc: '交换光标前面的两个字符',              cat: 'edit' },
  { keys: { ctrl: true, key: 'y' },     name: 'Ctrl+Y',      desc: '粘贴',                                  cat: 'edit' },
  { keys: { ctrl: true, key: 'w' },     name: 'Ctrl+W',      desc: '剪切光标前面的一个空格段',            cat: 'edit' },
  { keys: { alt: true, key: 'Backspace' }, name: 'Alt+Backspace', desc: '剪切光标前面的一个单词',        cat: 'edit' },
  { keys: { ctrl: true, key: 'u' },     name: 'Ctrl+U',      desc: '剪切光标到行首之间的全部内容',        cat: 'edit' },
  { keys: { ctrl: true, key: 'k' },     name: 'Ctrl+K',      desc: '剪切光标到行尾之间的全部内容',        cat: 'edit' },
  { keys: { ctrl: true, key: 'a' },     name: 'Ctrl+A',      desc: '光标移动到行首',                      cat: 'cursor' },
  { keys: { ctrl: true, key: 'e' },     name: 'Ctrl+E',      desc: '光标移动到行尾',                      cat: 'cursor' },
  { keys: { ctrl: true, key: 'b' },     name: 'Ctrl+B',      desc: '光标向左移动一个字符',                cat: 'cursor' },
  { keys: { ctrl: true, key: 'f' },     name: 'Ctrl+F',      desc: '光标向右移动一个字符',                cat: 'cursor' },
  { keys: { alt: true, key: 'b' },      name: 'Alt+B',       desc: '光标向左移动一个单词',                cat: 'cursor' },
  { keys: { alt: true, key: 'f' },      name: 'Alt+F',       desc: '光标向右移动一个单词',                cat: 'cursor' },
  { keys: { ctrl: true, key: 'h' },     name: 'Ctrl+H',      desc: '删除光标前面的一个字符 (同Backspace)', cat: 'edit' },
  { keys: { ctrl: true, key: 'd' },     name: 'Ctrl+D',      desc: '删除光标处的字符 (空行则退出shell)',  cat: 'edit' },
  { keys: { ctrl: true, key: '_' },     name: 'Ctrl+_',      desc: '撤销上一次编辑操作',                  cat: 'edit' },
  // 历史
  { keys: { ctrl: true, key: 'p' },     name: 'Ctrl+P',      desc: '上一条历史命令 (同 ↑)',               cat: 'history' },
  { keys: { ctrl: true, key: 'n' },     name: 'Ctrl+N',      desc: '下一条历史命令 (同 ↓)',               cat: 'history' },
  { keys: { alt: true, key: '.' },      name: 'Alt+.',       desc: '插入上一条命令的最后一个参数',        cat: 'history' },
  // 系统
  { keys: { ctrl: true, key: 'c' },     name: 'Ctrl+C',      desc: '取消当前命令或清除正在输入的命令',    cat: 'system' },
  { keys: { ctrl: true, key: 'l' },     name: 'Ctrl+L',      desc: '清屏，保留已输入的命令',              cat: 'system' },
  { keys: { ctrl: true, key: 'g' },     name: 'Ctrl+G',      desc: '取消当前搜索/补全/编辑状态',          cat: 'system' },
  // 特殊（无法键盘检测，算知识题）
  { keys: null,                         name: '!!',          desc: '执行上一条命令',                      cat: 'special' },
  { keys: null,                         name: '!$',          desc: '引用上一条命令的最后一个参数',        cat: 'special' },
];
```

## 分类和标签对照

| cat 字段 | 中文标签 |
|----------|---------|
| cursor   | 光标移动 |
| edit     | 编辑     |
| history  | 历史命令 |
| system   | 系统控制 |
| special  | 知识     |

## 特殊键名映射

| event.key | expected.key |
|-----------|-------------|
| ArrowLeft | ArrowLeft |
| ArrowRight | ArrowRight |
| ArrowUp | ArrowUp |
| ArrowDown | ArrowDown |
| Backspace | Backspace |
| Enter | Enter |
| Escape | Escape |
| Delete | Delete |
| Tab | Tab |
| ' ' (space) | ' ' |

## 注意事项

- **Ctrl 和 Cmd**: macOS 上 Ctrl 和 Command 都映射为 Ctrl 检测（`e.ctrlKey || e.metaKey`）
- **Ctrl+H 和 Backspace**: 终端中 Ctrl+H 等于 Backspace，但硬件按键不同
- **Ctrl+M 和 Enter**: 终端中 Ctrl+M 等于 Enter，是同一个 \\r 字符
- **纯修饰键过滤**: `e.key === 'Control'`、`e.key === 'Alt'` 等必须跳过
- **不要使用 Ctrl+R/S 作为控制快捷键**: 这些本身可能是题目，占用会导致冲突
- **Ctrl+_（撤销）**: Mac 上需要 Ctrl+Shift+- 才能触发，见 known-bugs.md
- **方向键**: ArrowUp/ArrowDown 应保留默认行为（页面滚动）
