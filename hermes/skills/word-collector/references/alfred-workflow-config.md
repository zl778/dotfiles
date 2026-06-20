# Alfred Workflow 配置

## Run Script 动作设置

在 Alfred 的 Workflow 编辑器中：

1. 添加 **Run Script** 动作
2. 设置：
   - **Language**: `/usr/bin/python3`（或 `bin/bash`）
   - **Escaping（转义）**: 不需要特殊转义，`{query}` 直接接收
   - **Script 内容**:

```
python3 /Users/liangzhu/.local/bin/word-collector.py "{query}"
```

## 关键字触发（可选）

在 Run Script 前加一个 **Keyword** 输入：
- Keyword: `word`（或 `w`）
- Argument: 必填
- 标题：记录单词

## 输出提示

脚本运行后会打印 `Saved: {word} - {翻译}`，Alfred 会显示为通知。
不会弹出大段内容。

## 错误处理

如果脚本报错，在 Alfred 里会看到错误信息。
常见错误：查不到词典数据 → 换一个常见词。