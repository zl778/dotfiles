---
date: 2026-06-25
tags: []
aliases: []
id: 20260625155242
---
# 🔐 

> 生成日期：2026-06-25
> 对应服务：vault.61877778.xyz（搬瓦工 VPS fair-cubes-1, Debian 13, Docker 29.6）

---

## ⚡ 快速应急卡

| 场景 | 一句话操作 |
|:----|:-----------|
| **忘记主密码** | ❌ 无法恢复。唯一补救：导出 `.csv` 前有本地备份？ |
| **数据库损坏** | 停止容器 → 恢复 `/backups/vw-*.tar.gz` → 重启容器 |
| **容器被删** | `docker run -d --name vaultwarden ...`（用之前的参数重建） |
| **VPS 宕机** | 登录搬瓦工面板 → 强制重启 / 救援模式 |
| **域名 DNS 异常** | Cloudflare 面板检查 DNS 记录 → 确保灰云（仅 DNS） |
| **SSL 证书过期** | VPS 运行 `~/.acme.sh/acme.sh --cron` |
| **服务器被入侵** | 立即关机 → 搬瓦工面板挂载救援 ISO → 备份数据 → 重装系统 |
| **误 rm -rf** | 停止写入 → 用 `extundelete` 尝试恢复（概率低） |

---

## 1. 密码类风险（最高优先级）

### ① 忘记主密码 ⚠️ 最严重

- **影响**：所有密码永久丢失，不可恢复
- **预防**：
  - 主密码写下来，放物理保险柜 / 家人保管
  - 主密码存入另一个密码管理器（如 Apple 钥匙串）
  - 定期登录确认记得密码
- **恢复**：❌ **无恢复手段**。Bitwarden/Vaultwarden 是零知识架构，服务端无法解密

### ② 两步验证（2FA）设备丢失

- **预防**：
  - 注册时保存 **恢复码**（打印纸质或存本地文件）
  - 恢复码位置：`~/dotfiles/...` 或打印放钱包
- **恢复**：用恢复码登录 → 重新绑定新 TOTP 设备
- **备用方案**：直接删除 `config.json` 中 2FA 条目（需要 SSH 到 VPS）

---

## 2. 数据存储风险

### ③ 数据库损坏 / 误删除

- **当前保护**：✅ 每日 3:00 自动备份到 `/backups/`
- **检测**：`docker logs vaultwarden` 查看错误日志
- **恢复步骤**：
  ```bash
  # 1. 停止容器
  docker stop vaultwarden

  # 2. 备份当前损坏数据（万一还有用）
  mv /vw-data /vw-data-corrupted

  # 3. 从备份恢复
  mkdir -p /vw-data
  tar xzf /backups/vw-20260625.tar.gz -C /
  # 注意：tar 包内路径是 vw-data/，所以解压到 / 即可

  # 4. 启动容器
  docker start vaultwarden
  ```

### ④ Docker 容器被删除

- **当前保护**：容器配置记录在 `~/dotfiles/`
- **恢复命令**（重建容器）：
  ```bash
  docker run -d \
    --name vaultwarden \
    --restart unless-stopped \
    -v /vw-data/:/data/ \
    -p 8080:80 \
    vaultwarden/server:latest
  ```

---

## 3. 基础设施风险

### ⑤ VPS 故障（宕机 / 磁盘损坏 / 供应商倒闭）

- **检测**：每天早上的 Hermes cron 可以加 ping 检测
- **恢复方案**：

  **方案 A：搬瓦工面板强制重启**
  - 登录搬瓦工 KiwiVM 面板 → 重启 / 救援模式

  **方案 B：迁移到新 VPS**（需要提前保留以下信息）：
  ```
  □ Vaultwarden 数据备份（/backups/vw-*.tar.gz）↔ 下载到本地
  □ Docker 运行命令（见上面第④条）
  □ Nginx 配置（/etc/nginx/sites-enabled/vaultwarden）
  □ SSL 证书（/root/.acme.sh/）
  □ UFW 规则
  ```
- **建议**：每季度手动下载一次备份到本地 Mac
  ```bash
  scp root@199.115.228.154:/backups/vw-$(date +%Y%m%d).tar.gz ~/Downloads/
  ```

### ⑥ 域名过期 / DNS 错误

- **预防**：
  - 域名开启 **自动续费**
  - 确保 Cloudflare 中 `vault` 记录为 **灰云（仅 DNS）**
- **恢复**：Cloudflare 面板 → DNS → 检查记录是否正确指向 `199.115.228.154`

### ⑦ SSL 证书过期

- **当前保护**：acme.sh 自动续期 cron（每日 10:43）
- **手动续期**：
  ```bash
  ~/.acme.sh/acme.sh --renew -d vault.61877778.xyz
  nginx -s reload
  ```
- **证书信息**：`~/.acme.sh/vault.61877778.xyz_ecc/`

---

## 4. 安全风险

### ⑧ VPS 被入侵

- **预防**：
  - ✅ UFW 防火墙，只开放必要端口（22, 80, 443, 2053 等）
  - ✅ SSH 密钥登录（建议禁用密码登录）
  - ✅ 保持系统更新：`apt update && apt upgrade -y`
  - 定期检查：`last` 查看登录记录，`journalctl -u ssh` 看 SSH 日志
- **入侵后的应急流程**：

  ```
  ① 立即关机（搬瓦工面板）
  ② 搬瓦工 → 救援模式 → 挂载 ISO → 备份 /vw-data/ 和 /backups/
  ③ 重装系统
  ④ 重新部署 Vaultwarden + 从备份恢复数据
  ⑤ 在所有客户端上更换密码（仅当怀疑主密码泄露时）
  ```

### ⑨ 数据泄露（数据库被窃取）

- **Vaultwarden 加密存储**：即使 `db.sqlite3` 被窃取，攻击者也看不到明文密码
- **但风险仍在**：
  - 攻击者可尝试离线暴力破解主密码（取决于主密码强度）
  - 建议：主密码 **20位以上 + 大小写 + 数字 + 符号**
  - 建议：开启 2FA 增加保护层

---

## 5. 操作风险

### ⑩ 误操作（rm -rf / docker 误删）

- **预防**：
  - 永远不要在 VPS 上执行 `rm -rf /` 或 `rm -rf /vw-data/`
  - 使用 Docker 命令时仔细核对容器名
  - 操作前先 `ls` 确认路径
- **恢复**：依赖每日备份

### ⑪ 网络问题（国内访问异常）

- **当前情况**：VPS 在美西，国内访问可能不稳定
- **临时方案**：开代理访问
- **长期方案**：考虑国内 VPS 做反代（备用方案）

---

## 6. 迁移与连续性

### ⑫ 搬家 / 换 VPS

- **迁移清单**：

  ```bash
  # 1. 在新 VPS 上安装 Docker
  apt install docker.io docker-compose -y

  # 2. 复制备份到新服务器
  scp /backups/vw-*.tar.gz root@新IP:/tmp/

  # 3. 解压数据
  tar xzf /tmp/vw-*.tar.gz -C /

  # 4. 启动容器
  docker run -d --name vaultwarden --restart unless-stopped \
    -v /vw-data/:/data/ -p 8080:80 vaultwarden/server:latest

  # 5. 配置 Nginx 反代 + SSL 证书 + UFW
  # （参照之前的配置过程）

  # 6. 更新 Cloudflare DNS 指向新 IP
  ```

### ⑬ VPS 供应商倒闭 / 账号被封

- **预防**：定期本地备份（建议每月）
- **恢复**：迁移到新 VPS（同上）

---

## 7. 日常维护清单

|     频率     | 操作                      | 备注                                               |
| :--------: | :---------------------- | :----------------------------------------------- |
|   **每天**   | ✅ 自动备份（3:00 cron）       | 已配置                                              |
|   **每天**   | ✅ SSL 续期检查（10:43 cron）  | 已配置                                              |
|   **每月**   | 下载一份备份到本地 Mac           | `scp root@...:/backups/vw-*.tar.gz ~/Downloads/` |
|  **每季度**   | 登录 Vaultwarden Web 确认可用 | 浏览器打开 `https://vault.61877778.xyz`               |
|  **每半年**   | VPS 系统更新                | `apt update && apt upgrade -y && reboot`         |
| **主密码变更时** | 更新纸质记录 + Apple 钥匙串      |                                                  |

---

## 8. 配置快照（便于重建时参考）

| 配置项 | 值 |
|:------|:---|
| VPS IP | `199.115.228.154` |
| 域名 | `vault.61877778.xyz`（Cloudflare 灰云）|
| Docker 镜像 | `vaultwarden/server:latest` |
| 本地端口映射 | `8080 → 80` |
| 数据卷 | `/vw-data/ → /data/` |
| Nginx 反代 | `443/80 → localhost:8080` |
| SSL | Let's Encrypt ECDSA（acme.sh 自动续期）|
| 防火墙 UFW | 开放 22, 80, 443, 2053 等 |
| 备份路径 | `/backups/vw-YYYYMMDD.tar.gz`，保留 7 天 |
| 备份日志 | `/var/log/vaultwarden-backup.log` |

---

> **最后一道防线：主密码。** 所有技术措施（备份、迁移、重建）都可以挽救服务或数据，但一旦**忘记主密码，一切归零**。请确保主密码以物理方式备份（写下来放安全的地方）。