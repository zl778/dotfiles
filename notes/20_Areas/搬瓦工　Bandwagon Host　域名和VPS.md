#a/life/telecom

# **域名申请**
https://www.spaceship.com/zh/
61877778.xyz
pistachio26@gmail.com Cc..@spaceship

// 域名解析
https://dash.cloudflare.com/
pistachio26@gmail.com  

//3x-ui入口
https://3x.61877778.xyz:53540/eRW2L0Con5ebDZOGNW/
账户、密码：　5OrUV5ZNxA、UQrxtgHn5C8aTd4qY3
#  VPS购买　Server Details  
=============================

Hostname: fair-cubes-1.localdomain
To manage your VPS, please navigate to the KiwiVM Server Control Panel:  
  1. Log in to your Client area on [https://bandwagonhost.com](https://bandwagonhost.com/ "https://bandwagonhost.com")  
2. Navigate to My Services menu, then click View Details  
3. Click Login to KiwiVM Control Panel

  
IP and SSH Access Information:

  
Main IP Address: you can see your VPS Main IP in the KiwiVM control panel (please see steps above); additionally it was just emailed to you.  
SSH port: was just emailed to you. Additionally, SSH port is showin in KiwiVM (on main page).  
Root Password: For security reasons, we no longer send root passwords via email. Please set a root password in the KiwiVM panel.  
  
Before connecting to the VPS, please start it - this can be done in the KiwiVM control panel.

## cat ~/.ssh/id_ed25519.pub
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIMEvonedleA6CuUq480XvqPmaShcoeS38vbIIgOfoRrA pistachio26@gmail.com

 **私钥**（~/.ssh/id_ed25519）是你的身份凭证，用于 SSH 认证登录。工作原理：

1. 你先把公钥（.pub 文件）放到服务器上（比如 GitHub、云服务器等）

2. 连接时，服务器会发一个只有私钥才能解开的挑战

3. 你的 SSH 客户端用私钥完成认证——全程不需要输密码

简单说：私钥 ≈ 你的数字签名，公钥 ≈ 你留给各处的签名样本。

私钥的安全红线

私钥绝对不能泄露给任何人。 谁拿到你的私钥，谁就能登录你所有绑定了对应公钥的服务器。

下次如何查看私钥（正确做法）

不要用 cat 查看私钥内容——终端输出可能会有日志记录、截图共享等泄露风险。

正确做法是检查私钥是否存在且权限正确：

bash

ls -la ~/.ssh/id_ed25519

期望输出：

-rw------- 1 liangzhu staff 411 Jun 15 13:16 /Users/liangzhu/.ssh/id_ed25519
关键点：
- 权限必须为 600（-rw-------）——只有你自己可读
- 如果权限不对，运行 chmod 600 ~/.ssh/id_ed25519 修复

一旦怀疑私钥泄露，立即生成新密钥对，并从所有服务器上移除旧公钥。

# 登录:开机 和安装3x-ui
**ssh root@199.115.228.154** 
UfpSRx854fK9 (aUX3rjG8u4kd也可能是这个)
The authenticity of host '199.115.228.154 (199.115.228.154)' can't be established. ED25519 key fingerprint is: HA256:2l0lcNbBdo7F/1MYpXE7ZUlSgHZJU2jbDRcl9obwnJ8 
This key is not known by any other names. 
Are you sure you want to continue connecting (yes/no/[fingerprint])? **yes**
'199.115.228.154' (ED25519) to the list of known hosts. 
root@199.115.228.154's password:  UfpSRx854fK9
Linux fair-cubes-1.localdomain 6.12.88+deb13-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.12.88-1 (2026-05-15) x86_64 
The programs included with the Debian GNU/Linux system are free software; the exact distribution terms for each program are described in the individual files in /usr/share/doc/*/copyright. 
Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent permitted by applicable law.

root@fair-cubes-1:~# **apt update** 
Hit:1 http://anycast-mirrors.as25820.net/debian trixie InRelease 
Get:2 http://anycast-mirrors.as25820.net/debian trixie-updates InRelease [47.3 kB] 
Hit:3 http://security.debian.org/debian-security trixie-security InRelease Fetched 47.3 kB in 0s (689 kB/s)

8 packages can be upgraded. Run 'apt list --upgradable' to see them.

root@fair-cubes-1:~# **apt upgrade -y** 
Upgrading:
libgssapi-krb5-2 libkrb5-3 libssl3t64 openssl
libk5crypto3 libkrb5support0 linux-image-amd64 openssl-provider-legacy

Installing dependencies:
apparmor linux-image-6.12.90+deb13.1-amd64

Suggested packages: 
apparmor-profiles-extra firmware-linux-free debian-kernel-handbook apparmor-utils linux-doc-6.12 
Summary: Upgrading: 8, Installing: 2, Removing: 0, Not Upgrading: 0 
Download size: 113 MB 
Space needed: 114 MB / 17.3 GB available 
└─ in /boot: 53.1 MB / 1320 MB available

## KIWIVM 登录密码
https://kiwivm.64clouds.com/auth-login
199.115.228.154
Cctvsdxc5@bandwagon

## **设置SSH 公钥**
//把公钥写进系统
`echo 'AAAAC3NzaC1lZDI1NTE5AAAAIMEvonedleA6CuUq480XvqPmaShcoeS38vbIIgOfoRrA [pistachio26@gmail.com](mailto:pistachio26@gmail.com)' >> ~/.ssh/authorized_keys
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys`

//把私钥绑定VPS
`ssh -i ~/.ssh/id_ed25519.pub root@199.115.228.154`

## 3x-ui安装前 核对时间
//看时区
`timedatectl`
//设时区为上海
`timedatectl set-timezone Asia/Shanghai`

## 创建Snapshots
	在KiwiVM 左侧 Snapshots

https://kiwivm.64clouds.com/auth-login
199.115.228.154
Cctvsdxc5@bandwagon

//3x-ui入口
https://3x.61877778.xyz:53540/eRW2L0Con5ebDZOGNW/
账户、密码：　5OrUV5ZNxA、UQrxtgHn5C8aTd4qY3

//生成了订阅　pixel8a clash 不认
https://3x.61877778.xyz:2096/sub/7jw89pe2ziotibkp

//转换　用订阅转换
[https://sub.v1.mk/](https://sub.v1.mk/)

//成功了
[https://api.v1.mk/sub?target=clash&url=https%3A%2F%2F3x.61877778.xyz%3A2096%2Fsub%2F7jw89pe2ziotibkp&insert=false&config=https%3A%2F%2Fraw.githubusercontent.com%2FACL4SSR%2FACL4SSR%2Fmaster%2FClash%2Fconfig%2FACL4SSR_Online_Full_NoAuto.ini&emoji=true&list=false&xudp=false&udp=false&tfo=false&expand=true&scv=false&fdn=false&new_name=true&diyua=ShadowRocket](https://api.v1.mk/sub?target=clash&url=https%3A%2F%2F3x.61877778.xyz%3A2096%2Fsub%2F7jw89pe2ziotibkp&insert=false&config=https%3A%2F%2Fraw.githubusercontent.com%2FACL4SSR%2FACL4SSR%2Fmaster%2FClash%2Fconfig%2FACL4SSR_Online_Full_NoAuto.ini&emoji=true&list=false&xudp=false&udp=false&tfo=false&expand=true&scv=false&fdn=false&new_name=true&diyua=ShadowRocket)

//增加58320和47068端口、重新加载、确认状态
`sudo ufw allow 58320
sudo ufw allow 47068
sudo ufw allow 17761
sudo ufw reload
sudo ufw status`
