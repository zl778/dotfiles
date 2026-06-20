
### **重装前建议先备份**

在 Ghostty 里执行：

```bash
cp -R ~/.codex ~/.codex-backup-$(date +%Y%m%d)
```

或者：

```bash
tar -czvf ~/Desktop/codex-backup.tar.gz ~/.codex
```

这样即使重装失败也能恢复。

---

### **我建议的顺序**

不要直接删：

```bash
~/.codex
```

而是：

#### **1. 退出 Codex**

```bash
pkill -f codex
```

#### **2. 备份 ~/.codex**

#### **3. 卸载并重新安装 Codex**

#### **4. 登录后查看历史**

如果历史还在：

- 不需要进一步操作

如果历史不在：

- 把备份的 `.codex` 恢复回来

---

### **我比较关心的一点**

你的目录里：

```text
sessions/
archived_sessions/
```

都显示只有：

```text
96B
```

这有点异常。

正常使用过很多对话的话，里面应该有多个文件。

建议再执行：

```bash
ls -lah ~/.codex/sessions
```

以及：

```bash
ls -lah ~/.codex/archived_sessions
```

把结果发给我。

这样我可以判断：

- 历史会话是真的保存在本地
- 还是实际上你的历史已经同步到云端
- 重装后能恢复到什么程度

目前根据这张图来看，**直接重装 Codex 不一定会丢失历史，但一定要先备份整个** **`~/.codex`** **目录再动手。**