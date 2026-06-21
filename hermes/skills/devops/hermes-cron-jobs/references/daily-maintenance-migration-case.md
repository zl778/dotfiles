# 案例：每日维护任务（no_agent → Agent 模式迁移）

## 原始配置（失败）

```yaml
name: 每日维护（hermes update + dotfiles sync）
schedule: "0 4 * * *"
deliver: origin
no_agent: true
script: daily-maintenance.sh
```

## 失败原因

1. **超时**：`no_agent` 脚本 120 秒超时 — `hermes update` + `sync.sh` + `git commit && git push` 三项超过 2 分钟
   - 输出日志：`Script timed out after 120s`
   - 日志位置：`~/.hermes/cron/output/<job_id>/2026-06-21_04-42-17.md`

2. **投递失败**：`deliver: origin` 在凌晨 4 点无活跃会话 → 回退到 email 投递 → email 插件未注册
   - 错误信息：`delivery error: email plugin not registered or missing standalone_sender_fn`

## 修复后的配置（成功）

```yaml
name: 每日维护（hermes update + dotfiles sync）
schedule: "0 4 * * *"
deliver: local
no_agent: false
script: ''
prompt: |
  运行每日维护任务，按顺序执行以下步骤：
  1. Hermes 升级：运行 `hermes update`，记录输出
  2. Dotfiles 同步：进入 ~/dotfiles，运行 `bash sync.sh`，记录输出
  3. Git 提交 + 推送：进入 ~/dotfiles，依次执行 git add .、git diff --cached --quiet（判断变更）、git commit -m "每日自动更新 $(date +%F)"、git push
  如果某一步失败，报告错误但继续下一步。最后汇总一个简洁的状态报告。用中文回答。
```

## 结果

Agent 模式运行成功，所有步骤完成无超时：

| 步骤 | 状态 | 详情 |
|------|------|------|
| Hermes 升级 | ✅ 无需更新 | 已是最新 |
| Dotfiles 同步 | ✅ 完成 | .zshrc、.gitconfig、bin、Hermes 配置、Obsidian 笔记均已同步 |
| Git 提交+推送 | ✅ 成功 | 16 文件变更（+320/-24），已推送 GitHub |

## 复现步骤

```
# 1. 列出所有 job 找到 job_id
cronjob(action='list')

# 2. 检查上次运行日志
cat ~/.hermes/cron/output/<job_id>/*.md

# 3. 更新为 Agent 模式
cronjob(
  action='update',
  job_id='<id>',
  no_agent=False,
  script='',
  deliver='local',
  prompt='...'
)

# 4. 手动触发测试
cronjob(action='run', job_id='<id>')
# 等待 30-60s
cat ~/.hermes/cron/output/<job_id>/<new-timestamp>.md
```
