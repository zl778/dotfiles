---
date: 2026-07-06T00:58:00
tags:
  - /r/tools/ssh
aliases:
  - ssh
id: "20260706155620"
---

> 环境：
>
> -   Windows 11 Main
> -   WSL2 Ubuntu
> -   MacBook Pro
> -   目标：通过 `ssh zl@192.168.26.26` 从 MacBook 登录 WSL Ubuntu

------------------------------------------------------------------------

# 一、WSL安装 OpenSSH Server

``` bash
sudo apt update
sudo apt install -y openssh-server
```

检查是否安装：

``` bash
dpkg -l | grep openssh-server
```

------------------------------------------------------------------------

# 二、WSL启动 SSH 服务

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

    **现象**

MacBook 无法连接：

``` text
ssh: connect to host 192.168.26.26 port 22: Operation timed out
```

已经确认：

-   SSH Server 已正常启动
-   `sshd` 正在监听 22 端口

说明问题不是 SSH 服务本身。

------------------------------------------------------------------------
    **原因**

Windows Defender 防火墙没有放行 TCP 22 端口。

------------------------------------------------------------------------

    **解决方案**

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

# 五、最终结果

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
# 六、使用密钥替代密码


    1. Mac 上生成密钥（如果已有 ~/.ssh/id_ed25519 可跳过）
    bash
    ssh-keygen -t ed25519 -C "your@email"
    一路回车，设置 passphrase（可选）

    2. 把公钥传到 WSL
    bash
    在 Mac 上执行
    ssh-copy-id -i ~/.ssh/id_ed25519.pub <WSL用户名>@<Windows11的IP>

    3. 测试免密登录
    bash
    ssh <WSL用户名>@<Windows11的IP>

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
  
  ----------------------------------------------------------------
# 八、本次经验总结

-   SSH 服务运行在 **WSL Ubuntu**，不是 Windows。
-   `sudo ss -tlnp` 比 `ss -tlnp` 更可靠，因为 `-p` 需要 root 权限。
-   `Get-Service sshd` 找不到服务属于正常情况，因为 Windows 并未安装
    OpenSSH Server。
-   如果 MacBook 连接超时，而 WSL 中 `sshd` 已监听，优先检查 **Windows
    Defender 防火墙**。
-   添加入站规则后即可正常通过 Windows 局域网 IP 访问 WSL。

------------------------------------------------------------------------




# 九、win11部署 SSHServer
## 1、确认 OpenSSH Server 是否已安装

管理员 PowerShell：

```powershell
Get-WindowsCapability -Online | Where-Object Name -like 'OpenSSH*'
```

正常会看到类似：

```text
OpenSSH.Client~~~~0.0.1.0   Installed
OpenSSH.Server~~~~0.0.1.0   NotPresent
```

如果 Server 已经是 Installed，可以跳到第三步。

---

## 2、安装 OpenSSH Server

管理员 PowerShell：

```powershell
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
```

安装完成后查看：

```powershell
Get-WindowsCapability -Online | Where-Object Name -like 'OpenSSH*'
```

应该变成

```text
OpenSSH.Server~~~~0.0.1.0   Installed
```

---

## 3、启动 SSH 服务

```powershell
Start-Service sshd
```

设置开机启动：

```powershell
Set-Service -Name sshd -StartupType Automatic
```

查看状态：

```powershell
Get-Service sshd
```

应该看到

```text
Status   Name
------   ----
Running  sshd
```

---

##4、开放防火墙

一般安装时会自动创建规则。

检查：

```powershell
Get-NetFirewallRule -DisplayName *ssh*
```

如果没有规则，执行：

```powershell
New-NetFirewallRule `
-Name sshd `
-DisplayName "OpenSSH Server" `
-Enabled True `
-Direction Inbound `
-Protocol TCP `
-Action Allow `
-LocalPort 22
```

---

## 5、确认监听 22 端口

```powershell
netstat -ano | findstr :22
```

应该看到类似：

```text
TCP    0.0.0.0:22
TCP    [::]:22
```

也可以：

```powershell
Get-NetTCPConnection -LocalPort 22
```

---
## 6、查看 Windows 用户名

```powershell
whoami
```

例如：

```text
desktop-05kgevt\zl
```

真正 SSH 使用的是：

```text
zl
```

---

##7、查看本机 IP

```powershell
ipconfig
```

找到

```text
IPv4 Address
```

例如：

```
192.168.26.26
```

---

## 8、从另一台电脑连接

例如你的 Mac：

```bash
ssh zl@192.168.26.62
```

第一次会提示：

```
Are you sure you want to continue connecting?
```

输入：

```
yes
```

然后输入 **Windows 登录密码**（不是 PIN）。

---

## 9、配置免密登录
因为 192.168.26.62 上的 zl 是管理员，
所以在 Mac 上：
cat ~/.ssh/id_ed25519.pub
复制公钥；

在 Win11 上管理员 PowerShell：
nano C:\ProgramData\ssh\administrators_authorized_keys
粘贴公钥和保存退出；

对公钥文件改权限：
icacls C:\ProgramData\ssh\administrators_authorized_keys /inheritance:r
icacls C:\ProgramData\ssh\administrators_authorized_keys /grant "Administrators:(F)"
icacls C:\ProgramData\ssh\administrators_authorized_keys /grant "SYSTEM:(F)"

重启SSH 服务：
Restart-Service sshd

MAC 上 ssh zl@192.168.26.62
完成

---

## 10、与之前在 WSL 内安装 SSH 的区别

| **方案**               | **登录目标**                          | **推荐程度** | **适用场景**        |
| -------------------- | --------------------------------- | -------- | --------------- |
| Win11 OpenSSH Server | Windows 主机，可进入 PowerShell、CMD、WSL | ⭐⭐⭐⭐⭐ 推荐 | 日常远程管理整台电脑      |
| WSL OpenSSH Server   | Ubuntu 环境                         | ⭐⭐⭐      | 只想直接进入 Linux 环境 |

---

# 十、解决 WSL 和 WIN11 的 SSH 端口同是 22

## 1、把 WSL 端口改为 2222
	关闭 socket activation
	sudo systemctl disable --now ssh.socket
	
	sudo systemctl enable ssh
	
	sudo systemctl restart ssh
	
	sudo systemctl status ssh
	
	sudo ss -tlnp | grep :2222

	<--! 添加 2222 防火墙规则 -->
	New-NetFirewallRule -DisplayName "WSL SSH 2222" -Direction Inbound -Protocol TCP -LocalPort 2222 -Action Allow
	
	sshd
	
	MAC连接
	ssh -p 2222 zl@192.168.26.62

