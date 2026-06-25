---
date: 2026-06-24
tags: []
aliases: []
id: 20260624224443
---
# **1. 重要的建议：不要同时使用多个密码管理器**

这是很多新用户最容易忽略的。

Bitwarden 官方明确建议：

如果你决定使用 Bitwarden，就应该关闭浏览器和系统自带的密码管理功能。  

原因：

如果同时开启：

- Apple Passwords（原 iCloud Keychain）
- Chrome Password Manager
- Edge Password Manager
- Bitwarden

就会出现：

- 重复弹窗
- 保存两份密码
- 自动填充混乱
- Passkey 存在不同地方

---

## **对你的苹果生态**

你目前：

- MacBook Pro
- iPhone
- iPad
- Pixel 8a
- Vaultwarden

推荐：

### **Mac**

系统设置 →

```text
Passwords
Password Options
```

关闭：

```text
AutoFill Passwords and Passkeys
```

或只保留 Bitwarden。  

---

### **iPhone / iPad**

进入：

```text
设置
→ 密码
→ 密码选项
```

开启：

```text
AutoFill Passwords and Passkeys
Bitwarden
```

关闭：

```text
Passwords（苹果密码）
```

即：

```text
✓ Bitwarden
✗ Passwords
```

官方论坛大量案例证明这样最稳定。  

---

# **2. 不要把主密码保存在 Bitwarden 里**

官方一直强调：

主密码（Master Password）是唯一不能丢的东西。

不要：

```text
Bitwarden
└── 主密码.txt
```

这种做法毫无意义。

---

推荐：

### **方法一**

纸质记录

放保险柜。

---

### **方法二**

离线保存

例如：

```text
加密U盘
NAS
纸质备份
```

---

# **3. Face ID ≠ 主密码**

很多人误解：

```text
开启 Face ID
=
不需要主密码
```

错误。

实际上：

```text
Face ID
只是解锁方式
```

真正密钥仍然来自主密码。  

---

# **4. 官方推荐开启生物识别**

对于：

- iPhone
- iPad
- Mac

建议：

```text
Unlock with Face ID
```

开启。

---

这样日常使用体验接近 Apple Passwords：

```text
点登录
↓
Face ID
↓
自动填充
```

---

# **5. 导入完成后删除 CSV**

这是官方特别强调的。  

很多人：

```text
Apple Passwords
↓
导出 CSV
↓
导入 Bitwarden
```

然后：

```text
passwords.csv
```

一直放在桌面。

这非常危险。

CSV 是明文。

官方建议：

```text
导入成功
↓
立即删除 CSV
↓
清空废纸篓
```

---

# **6. 自动清空剪贴板**

这是很多老用户都会开的功能。

例如：

```text
复制密码
↓
登录
↓
忘记清除
```

别人：

```text
Ctrl+V
```

直接看到密码。

---

Bitwarden 提供：

```text
Clear Clipboard
```

推荐：

```text
30 秒
或
60 秒
```

自动清除。  

---

# **7. URI 是自动填充的关键**

很多人抱怨：

```text
Bitwarden 不自动匹配
```

实际上是条目缺 URI。

例如：

错误：

```text
Github
用户名
密码
```

正确：

```text
Github
https://github.com
用户名
密码
```

Bitwarden 自动填充主要依赖 URI。  

---

# **8. 使用快捷键自动填充**

这是高手最常用的方式。

Mac：

```text
⌘ + Shift + L
```

Windows：

```text
Ctrl + Shift + L
```

直接填充当前网页。官方长期推荐这种方式，而不是鼠标点击插件。  

---

# **9. Passkey 尽量统一管理**

现在很多网站支持：

- Passkey
- FIDO2

官方建议：

选择一个主密码管理器。  

例如：

### **方案 A**

全部放 Bitwarden

```text
密码
Passkey
TOTP
```

全部在 Vaultwarden。

---

### **方案 B**

全部放 Apple Passwords

---

不要：

```text
Github Passkey → Apple
Google Passkey → Bitwarden
Microsoft Passkey → Chrome
```

半年后肯定忘。

---

# **10. Bitwarden 最容易被忽略的功能：Send**

很多人不知道。

Bitwarden Send：

```text
生成一次性分享链接
```

用途：

发送：

- Wi-Fi 密码
- VPS Root 密码
- API Key

给别人。

支持：

```text
访问次数限制
过期时间
密码保护
```

比微信发密码安全很多。

---

# **11. 官方推荐开启两步验证**

你的 Vaultwarden 已经上线。

下一步应该是：

开启：

```text
2FA
```

推荐顺序：

### **第一梯队**

- Aegis（Android）
- Ente Auth
- Bitwarden Authenticator

---

### **第二梯队**

- Google Authenticator

---

不要只依赖密码登录。

---

# **12. Vaultwarden 用户特别要注意**

这是你目前最需要关注的。

很多人认为：

```text
用了 Vaultwarden
=
安全
```

实际上：

自托管以后：

你自己负责：

- SSL证书
- 数据备份
- 数据库备份
- VPS安全
- Docker升级

官方 Bitwarden 会帮你做这些。

Vaultwarden 不会。

---

# **针对你目前环境的推荐配置**

结合你现在：

- 搬瓦工 VPS
- Docker
- Vaultwarden
- MacBook Pro M5
- iPhone
- iPad
- Pixel 8a

我建议：

### **苹果设备**

```text
关闭 Apple Passwords 自动填充
开启 Bitwarden 自动填充
```

### **浏览器**

```text
关闭 Chrome 密码管理器
关闭 Edge 密码管理器
只保留 Bitwarden
```

### **Vaultwarden**

```text
开启 HTTPS
开启 2FA
每周自动备份数据库
每月导出加密 JSON
```

### **日常习惯**

```text
每个网站独立密码
全部使用随机生成
长度 ≥ 20
```

这基本就是 Bitwarden 官方文档、官方论坛和资深用户长期实践下来的一套比较成熟的使用方式。