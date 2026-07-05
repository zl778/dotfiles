---
date: 2026-07-06T00:58:00
tags:
  - /r/tools/ssh
aliases:
  - ssh
id: <% tp.date.now("YYYYMMDDHHmmss") %>
---


> 环境：
>
> -   Windows 11 Main
> -   WSL2 Ubuntu
> -   MacBook Pro
> -   目标：通过 `ssh zl@192.168.26.26` 从 MacBook 登录 WSL Ubuntu

------------------------------------------------------------------------

# 一、安装 OpenSSH Server

``` bash
sudo apt update
sudo apt install -y openssh-server
```

检查是否安装：

``` bash
dpkg -l | grep openssh-server
```

------------------------------------------------------------------------

# 二、启动 SSH 服务

启动：

``` bash
sudo service ssh start
```

查看状态：

``` bash
sudo service ssh status
```

查看监听：

``` bash
sudo ss -tlnp | grep ssh
```

> **注意**
>
> `ss -tlnp` 中的 `-p` 参数需要 root 权限，因此建议使用：
>
> ``` bash
> sudo ss -tlnp | grep ssh
> ```
>
> 否则可能没有任何输出。

查看 WSL IP：

``` bash
hostname -I
```

------------------------------------------------------------------------

# 三、MacBook 测试连接

连接命令：

``` bash
ssh zl@192.168.26.26
```

------------------------------------------------------------------------

# 四、遇到的问题

## 现象

MacBook 无法连接：

``` text
ssh: connect to host 192.168.26.26 port 22: Operation timed out
```

已经确认：

-   SSH Server 已正常启动
-   `sshd` 正在监听 22 端口

说明问题不是 SSH 服务本身。

------------------------------------------------------------------------

## 原因

Windows Defender 防火墙没有放行 TCP 22 端口。

------------------------------------------------------------------------

# 五、解决方案

**必须使用「管理员 PowerShell」执行：**

``` powershell
New-NetFirewallRule `
    -DisplayName "WSL SSH" `
    -Direction Inbound `
    -Protocol TCP `
    -LocalPort 22 `
    -Action Allow
```

一行版本：

``` powershell
New-NetFirewallRule -DisplayName "WSL SSH" -Direction Inbound -Protocol TCP -LocalPort 22 -Action Allow
```

> 普通 PowerShell 会提示：
>
> ``` text
> 拒绝访问
> ```
>
> 因为修改防火墙规则需要管理员权限。

------------------------------------------------------------------------

# 六、最终结果

成功实现：

``` text
MacBook
      │
      │ ssh zl@192.168.26.26
      ▼
Windows 11
      │
      ▼
WSL Ubuntu（OpenSSH Server）
```

连接成功。

------------------------------------------------------------------------

# 七、排查命令速查

  -----------------------------------------------------------------------------------------------------------------------------------------------
  命令                                                                                                        作用
  ----------------------------------------------------------------------------------------------------------- -----------------------------------
  `dpkg -l \| grep openssh-server`                                                                            检查 SSH Server 是否安装

  `sudo service ssh start`                                                                                    启动 SSH 服务

  `sudo service ssh status`                                                                                   查看 SSH 状态

  `sudo ss -tlnp \| grep ssh`                                                                                 查看 SSH 是否监听

  `hostname -I`                                                                                               查看 WSL IP

  `ssh zl@192.168.26.26`                                                                                      从 MacBook 登录

  `Get-Service sshd`                                                                                          查看 Windows 是否安装 OpenSSH
                                                                                                              Server

  `netstat -ano \| findstr :22`                                                                               查看 Windows 是否监听 22 端口

  `New-NetFirewallRule -DisplayName "WSL SSH" -Direction Inbound -Protocol TCP -LocalPort 22 -Action Allow`   放行 Windows 防火墙
  -----------------------------------------------------------------------------------------------------------------------------------------------

------------------------------------------------------------------------

# 八、本次经验总结

-   SSH 服务运行在 **WSL Ubuntu**，不是 Windows。
-   `sudo ss -tlnp` 比 `ss -tlnp` 更可靠，因为 `-p` 需要 root 权限。
-   `Get-Service sshd` 找不到服务属于正常情况，因为 Windows 并未安装
    OpenSSH Server。
-   如果 MacBook 连接超时，而 WSL 中 `sshd` 已监听，优先检查 **Windows
    Defender 防火墙**。
-   添加入站规则后即可正常通过 Windows 局域网 IP 访问 WSL。

------------------------------------------------------------------------



