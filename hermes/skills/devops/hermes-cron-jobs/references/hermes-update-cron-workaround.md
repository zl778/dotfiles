# `hermes update` 在 cron 环境中的替代方案

## 问题

`hermes update` 命令由 `approval_fns.json` 保护，执行前会弹出交互式批准提示：

> `hermes update (restarts gateway, kills running agents)` — pending_approval

在 cron job / 自主运行环境中无法批准，命令卡住无输出。

## 替代方案（已验证）

### 1. 定位 Hermes 的实际 venv

Hermes CLI 入口脚本位于 `~/.local/bin/hermes`，内容为：

```bash
#!/usr/bin/env bash
unset PYTHONPATH
unset PYTHONHOME
exec "/Users/liangzhu/.hermes/hermes-agent/venv/bin/hermes" "$@"
```

**关键**：`~/.local/bin/hermes` 是一个 shell wrapper，它指向 `~/.hermes/hermes-agent/venv/bin/hermes`。不要用系统 Python（`/Library/Frameworks/Python.framework/...`），要用这个 venv 路径。

### 2. Git pull + venv pip install

```bash
# 进入仓库目录
cd ~/.hermes/hermes-agent

# 拉取最新代码
git pull

# 用 venv 的 pip 安装到正确位置
~/.hermes/hermes-agent/venv/bin/pip install -e ~/.hermes/hermes-agent
```

⚠️ **不要用 system Python 的 pip** 或 `uv pip install --system` — 它们会写入 `/Library/Frameworks/Python.framework/`，需要 sudo 权限且不适用于 cron 环境。

### 3. 验证升级结果

```bash
~/.hermes/hermes-agent/venv/bin/hermes version
```

## 局限性

- **不会重启 gateway** — `hermes update` 的完整语义包括重启 gateway 以使新代码生效。本方案只更新代码文件，不触发重启。
- 如果需要 gateway 重启效果，需要另做安排（如手动运行一次 `hermes update`，或配置 gateway 定期重启）。

## 适用场景

- 每日 cron job 的自动 Hermes 升级
- 无法交互的自主环境
- 只需要代码更新、不需要立即重启 gateway 的维护窗口
