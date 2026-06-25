---
name: vps-server-backup
description: "Set up automated backups on a remote Linux VPS — backup script, cron scheduling, rotation policy, and verification. Covers the crontab-overwrite pitfall specific to pipe-based setup."
tags:
  - devops
  - backup
  - cron
  - vps
  - vps-server-mgmt
---

# VPS Server Backup

Set up automated backup scripts on a remote Linux VPS with cron scheduling,
rotation, and log tracking.

## When to use

User has a critical service (Vaultwarden, database, website data) running on a
remote VPS and needs automated daily backups with retention.

## Standard Backup Pattern

### 1. Create the backup script on the VPS

```bash
ssh root@<VPS-IP> 'cat > /usr/local/bin/<service>-backup.sh << '\"'\"'EOF'\"'\"'
#!/bin/bash
BACKUP_DIR="/backups"
mkdir -p $BACKUP_DIR

FILENAME="<prefix>-$(date +%Y%m%d).tar.gz"

# Archive the data directory
tar czf "$BACKUP_DIR/$FILENAME" -C / <data-dir>/

# Rotate: delete backups older than 7 days
find $BACKUP_DIR -name "<prefix>-*.tar.gz" -mtime +7 -delete

# Log
echo "[$(date "+%Y-%m-%d %H:%M:%S")] 备份完成: $FILENAME ($(du -h "$BACKUP_DIR/$FILENAME" | cut -f1))" >> /var/log/<service>-backup.log
EOF
chmod +x /usr/local/bin/<service>-backup.sh'
```

### 2. Set up cron (⚠️ WATCH THE PITFALL)

```bash
ssh root@<VPS-IP> '
# FIRST read existing crontab:
OLD_CRON=$(crontab -l 2>/dev/null)
# THEN add new entry:
(echo "$OLD_CRON"; echo "0 3 * * * /usr/local/bin/<service>-backup.sh") | crontab -
'
```

### 3. Test the backup

```bash
ssh root@<VPS-IP> '/usr/local/bin/<service>-backup.sh && ls -lh /backups/ && cat /var/log/<service>-backup.log'
```

### 4. Verify backup contents

```bash
ssh root@<VPS-IP> 'tar tzf /backups/<prefix>-$(date +%Y%m%d).tar.gz | head -10'
```

## ⚠️ CRITICAL PITFALL: crontab 会覆盖整个 crontab

**`crontab -` 不是追加，是替换！**

```bash
# ❌ 错误：这会删除所有已有的 cron 条目！
echo "0 3 * * * /script.sh" | crontab -

# ✅ 正确：先读取已有的，再追加
(OLD_CRON=$(crontab -l 2>/dev/null); echo "$OLD_CRON"; echo "0 3 * * * /script.sh") | crontab -
```

常见的有已有 cron 的场景：
- Let's Encrypt / acme.sh SSL 自动续期
- 系统自身的日志轮替
- 之前配过的其他备份

**最佳实践：** 始终用 `crontab -l 2>/dev/null` 读取现有条目，再用子 shell `(old; new) | crontab -` 合并写入。

## 备份策略建议

| 类型 | 频率 | 保留期 | 说明 |
|:----|:----:|:------:|:-----|
| **自动增量** | 每天 | 7 天 | VPS 本地 `/backups/` |
| **手动全量** | 每月 | 永久 | 下载到本地 Mac |
| **灾难恢复** | 迁移时 | — | 完整配置快照 |

## 验证步骤

部署完成后确认：

```bash
# 1. 脚本可执行
ssh root@<IP> 'ls -la /usr/local/bin/*-backup.sh'

# 2. 备份文件已生成
ssh root@<IP> 'ls -lh /backups/'

# 3. 备份内容正确
ssh root@<IP> 'tar tzf /backups/$(ls -t /backups/ | head -1) | head -10'

# 4. 日志正常
ssh root@<IP> 'tail -3 /var/log/*-backup.log'

# 5. cron 已注册
ssh root@<IP> 'crontab -l | grep backup'
```

## 安全考虑

- 备份文件包含敏感数据（数据库、密钥），VPS 上的 `/backups/` 应限制权限
  ```bash
  chmod 700 /backups/
  ```
- 下载到本地的备份同样需注意安全存放
- 如果怀疑 VPS 被入侵，建议停止下载备份到本地，先检查入侵范围

## 关联文件

- **`references/security-contingency-plan.md`** — 完整的自托管服务安全预案模板，可直接套用于任何自托管服务。用 `skill_view(name="vps-server-backup", file_path="references/security-contingency-plan.md")` 加载。