# 用户问"任务执行了吗"的排查流程

## 典型场景

用户清晨或夜间问"今天早上4:00/凌晨的任务执行了吗"。

## 排查步骤

### 1. 列出 cron jobs 看状态

```bash
cronjob(action='list')
```

关键字段：
- `last_run_at` — 最后执行时间戳（时区）
- `last_status` — `ok` / `error`
- `deliver` — `local` / `origin` / `platform:chat_id` 等
- `enabled` — 是否启用

### 2. 向用户汇报结果

**成功时：**
> 执行了，今天凌晨 4:xx 成功完成 ✅
> （deliver=local 所以没有通知你）

**出错时：**
> 执行了但状态是 error
> 是否重新运行一次看看具体报什么？

### 3. 如果用户说要重跑

```bash
cronjob(action='run', job_id='<id>')
```

然后检查 `last_status` 是否变为 `ok`。

### 4. 如果用户说"以后通知我"

将 delivery 从 `local` 改为指定平台：

```bash
cronjob(
  action='update',
  job_id='<id>',
  deliver='telegram:-1005584761717'  # 或其他目标
)
```

注意：`deliver` 参数不需要 `origin` 前缀——直接在 cronjob 创建/更新时指定目标即可。
`telegram:chat_id` 格式发到特定群，不需要 `origin` 复合值。

### 5. 验证

```bash
cronjob(action='run', job_id='<id>')
# 检查 last_status == 'ok'
```