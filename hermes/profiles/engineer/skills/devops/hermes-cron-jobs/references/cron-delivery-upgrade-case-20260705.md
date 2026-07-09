# 案例：每日维护任务 delivery 升级（local → Telegram）

## 背景

用户设置的每日维护 job（hermes update + dotfiles sync），`deliver: local`。

某天用户问\"今天凌晨 4:00 的任务执行了吗\"，发现是 error 状态但未被通知。

## 处理流程

### Step 1: 检查状态

```bash
cronjob(action='list')
```

发现了每日维护 job：
- `last_run_at`: 2026-07-05 04:24:05+08:00
- `last_status`: error
- `deliver`: local
- `next_run_at`: 2026-07-06 04:00:00+08:00

### Step 2: 用户选择重跑验证

```bash
cronjob(action='run', job_id='9f46b8d0a0d3')
```

结果：`execution_success: true`, `last_status: ok` ✅

说明凌晨的 error 是临时问题（可能是凌晨网络波动），重跑就修复了。

### Step 3: 用户要求以后通知

```bash
cronjob(
  action='update',
  job_id='9f46b8d0a0d3',
  deliver='telegram:-1005584761717'
)
```

## 要点

- `deliver` 更新后立即生效，不需要重启或重新创建 job
- 用 `telegram:-1005584761717` 精确指定群，不包含 `origin` 前缀
- 重跑验证优先——先确认 job 能成功，再改 delivery，避免误报