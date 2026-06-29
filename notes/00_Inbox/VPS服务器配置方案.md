---
date: 2026-06-23
tags:
  - /r/tools/vps
aliases: []
id: "20260623202803"
---
结合你目前的情况：

- 已有搬瓦工 VPS
- 已部署 3X-UI
- 有自己的域名
- 准备做 Hugo 个人网站
- 使用 MacBook Pro + iPhone + iPad
- 对自动化、知识管理、个人效率工具比较感兴趣

我会把「个人 VPS 十大必装应用」分成 **基础设施、效率工具、内容服务、安全管理** 四类。

# **一、基础设施类（优先部署）**

## **1. Uptime Kuma**

用途：

- 网站监控
- VPS监控
- SSL证书到期提醒
- Telegram通知

例如：

```text
https://yourdomain.com
↓
5分钟检测一次
↓
挂了立即发Telegram
```

推荐指数：

⭐⭐⭐⭐⭐

资源占用：

- 内存：100~200MB

---

## **2. Vaultwarden**

用途：

- 密码管理
- Passkey管理
- TOTP验证码

相当于自建 Bitwarden。

推荐指数：

⭐⭐⭐⭐⭐

资源占用：

- 内存：50~150MB

---

## **3. Nginx Proxy Manager**

用途：

- 域名管理
- HTTPS证书自动签发
- 反向代理

例如：

```text
vault.yourdomain.com
blog.yourdomain.com
uptime.yourdomain.com
```

统一管理。

推荐指数：

⭐⭐⭐⭐⭐

资源占用：

- 内存：150~300MB

---

# **二、个人内容服务**

## **4. Hugo**

用途：

- 个人主页
- 博客
- 项目展示

你已经准备折腾 Hugo。

推荐指数：

⭐⭐⭐⭐⭐

资源占用：

几乎为零（生成静态页面）。

---

## **5. FreshRSS**

用途：

- RSS阅读器
- AI新闻聚合
- 技术博客订阅

可以订阅：

- OpenAI
- Anthropic
- Google AI
- Hacker News

推荐指数：

⭐⭐⭐⭐

资源占用：

- 内存：100MB左右

---

## **6. Miniflux**

如果你喜欢极简风格：

Miniflux 比 FreshRSS 更轻量。

二选一即可。

推荐指数：

⭐⭐⭐⭐

---

# **三、效率与协作**

## **7. n8n**

用途：

- 自动化工作流

例如：

```text
RSS更新
↓
AI总结
↓
发Telegram
```

或者：

```text
GitHub更新
↓
通知自己
```

推荐指数：

⭐⭐⭐⭐⭐

资源占用：

- 300~600MB

---

## **8. Memos**

用途：

- 类似微博
- 灵感记录
- 快速笔记

非常适合：

```text
手机想到一个点子
↓
立即记录
↓
电脑继续整理
```

推荐指数：

⭐⭐⭐⭐

---

# **四、安全与文件**

## **9. File Browser**

用途：

- 浏览服务器文件
- 上传下载文件
- 替代部分FTP

推荐指数：

⭐⭐⭐⭐

资源占用：

极低。

---

## **10. Beszel**

新一代监控工具。

监控：

- CPU
- 内存
- 磁盘
- Docker

比传统监控方案轻量很多。

推荐指数：

⭐⭐⭐⭐

---

# **如果是你的 VPS，我会这样排部署顺序**

### **第一阶段（立刻装）**

1. 3X-UI（已完成）
2. Uptime Kuma（已完成）
3. Nginx Proxy Manager  （已完成）
4. Vaultwarden（已完成）

---

### **第二阶段（内容建设）**

5. Hugo （已完成）
6. FreshRSS（暂时跳过）

---

### **第三阶段（效率提升）**

7. n8n（暂时跳过）
8. Memos（暂时跳过）

---

### **第四阶段（运维增强）**

9. File Browser （暂时跳过）
10. Beszel （已完成）

---

最终你的 VPS 会变成这样：

```text
域名
│
├── blog.xxx.com      → Hugo
├── vault.xxx.com     → Vaultwarden
├── rss.xxx.com       → FreshRSS
├── uptime.xxx.com    → Uptime Kuma
├── flow.xxx.com      → n8n
├── memo.xxx.com      → Memos
└── files.xxx.com     → File Browser
```

对于个人用户来说，这套组合已经接近一个小型“个人云平台”了，而且在你这类搬瓦工 VPS 上通常都能运行得很好。