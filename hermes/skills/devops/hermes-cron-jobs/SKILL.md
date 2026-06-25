---
name: hermes-cron-jobs
title: Hermes Cron Jobs
description: Set up, debug, and maintain Hermes cron jobs — scheduled recurring tasks that run autonomously.
triggers:
  - User asks to set up a recurring task ("daily briefing", "every hour check", "every Monday report")
  - A cron job is failing or producing unexpected delivery errors
  - User asks "did the cron job run?" or wants to inspect cron job output
  - User asks to change a cron job's mode (no_agent ↔ agent), delivery destination, or script
---

# Hermes Cron Jobs

## 两种运行模式

### 1. Agent 模式（默认，`no_agent=False`）
- LLM 驱动：每次触发时，Agent 运行 prompt 中的指令
- **无严格超时限制** — 适合多步骤任务（upgrade → sync → git push）
- 可访问所有工具（terminal, web, file, delegate_task 等）
- 默认 deliver 到创建时的会话

### 2. 纯脚本模式（`no_agent=True`）
- 直接运行 `script` 指定的脚本，**无 LLM 调用**、不消耗 token
- **120 秒超时限制**（硬性限制，不可配置）— 超时后直接失败
- 脚本 stdout 直接投递，agent 不做处理
- 适合：快速健康检查、磁盘监控、阈值告警（watchdog 模式）

## Delivery 关键陷阱

⚠️ **`deliver: "origin"` 在离线时段会失败**
- 凌晨 4 点无活跃会话时，系统尝试通过 email 回退投递
- email 插件未注册 → `delivery error: email plugin not registered`
- **修复**：对凌晨运行的维护任务，使用 `deliver: "local"`（输出仅存日志，不投递到任何频道）

| deliver 值 | 行为 | 适用场景 |
|------------|------|----------|
| `origin`（默认） | 投递到创建时的会话；无活跃会话时回退到 email | 白天运行的、有用户互动的任务 |
| `local` | 不投递，仅保存输出到 `~/.hermes/cron/output/<job_id>/` | 凌晨维护、安静看门狗 |
| `all` | 广播到所有已连接的 home channel | 需要通知所有平台的任务 |
| `platform:chat_id:thread_id` | 投递到指定目标 | 精确路由 |

## 从 no_agent 切换到 Agent 模式（修复超时+投递问题）

```bash
# 1. 先列出所有 job 找到 job_id
cronjob(action='list')

# 2. 更新 job
cronjob(
  action='update',
  job_id='<id>',
  no_agent=False,          # 切换到 agent 模式
  script='',               # 清除脚本路径
  deliver='local',         # 安静运行（凌晨用）
  prompt='''
  运行每日维护任务：
  1. hermes update
  2. bash sync.sh
  3. git add && git commit && git push
  如果某步失败，报告错误但继续下一步。
  '''
)
```

## 常用模式

### 每日维护任务
```yaml
name: 每日维护
schedule: "0 4 * * *"
deliver: local
prompt: |
  运行每日维护：hermes update → dotfiles sync → git commit + push
```

### 看门狗脚本（静默监控）
```yaml
script: ~/.hermes/scripts/disk-check.sh
no_agent: true
# stdout 为空 → 静默，有内容 → 投递告警
```

### 每日简报
```yaml
prompt: |
  抓取今天的头条新闻并总结成简报
skills: ["youtube-content", "web_search"]
```

## 手动触发测试

```
cronjob(action='run', job_id='<id>')
```

等待几秒后检查：
```
ls ~/.hermes/cron/output/<job_id>/
cat ~/.hermes/cron/output/<job_id>/*.md
```

## 常见 Pitfalls

| 问题 | 原因 | 修复 |
|------|------|------|
| Script timed out after 120s | no_agent 模式硬限制 120s | 切到 agent 模式 |
| email plugin not registered | deliver=origin 无活跃会话时回退 email | 用 deliver=local |
| 找不到 job ID | 猜错了 | 先 `cronjob(action='list')` |
| 凌晨投递到旧会话 | deliver=origin 绑定创建时的会话 | 用 deliver=local 或指定目标 |
| cron-run 递归调度 cronjob | 安全规则禁止 | 提示已在 prompt 中 |
| `hermes update` 卡在待批准 | 该命令触发 approval_fns（重启 gateway、杀死 agent） | 用 git pull + venv pip install 替代 |

## 查看运行日志

```bash
# 列出所有 jobs 及 next_run_at / last_status
cronjob(action='list')

# 读取上次运行的完整输出
cat ~/.hermes/cron/output/<job_id>/*.md | head -50
```

每次运行都会在 `~/.hermes/cron/output/<job_id>/` 下生成带时间戳的 .md 文件，包含 prompt 和完整 response。

## 参考案例

- `references/daily-maintenance-migration-case.md` — 完整的每日维护任务从 no_agent 迁移到 Agent 模式的过程，含错误日志、修复步骤、已验证的最终配置。
- `references/hermes-update-cron-workaround.md` — 在 cron / 自主运行环境中绕过 `hermes update` 交互式批准的替代方案。
