---
date: 2026-07-03
tags:
  - /r/tools/linux
aliases: []
id: 20260703102249
---

# **一、WSL 管理命令（Windows PowerShell）**

这些命令是在 **PowerShell/CMD** 中执行，不是在 Ubuntu 里面。

## **查看所有 WSL**

```powershell
wsl -l -v
```

输出类似：

```text
  NAME              STATE           VERSION
* Ubuntu            Running         2
  docker-desktop    Running         2
```

---

## **启动 Ubuntu**

```powershell
wsl
```

或者

```powershell
wsl -d Ubuntu
```

指定发行版：

```powershell
wsl -d Debian
```

---

## **关闭 WSL**

关闭当前发行版

```powershell
wsl --terminate Ubuntu
```

关闭整个 WSL

```powershell
wsl --shutdown
```

这个命令非常常用。

例如：

- 修改 `.wslconfig`
- 修改内存
- 修改 CPU
- 网络异常

几乎都需要：

```powershell
wsl --shutdown
```

---

## **查看状态**

```powershell
wsl --status
```

---

## **更新 WSL**

```powershell
wsl --update
```

---

## **查看版本**

```powershell
wsl --version
```

---

## **设置默认发行版**

```powershell
wsl --set-default Ubuntu
```

---

## **导出发行版（备份）**

```powershell
wsl --export Ubuntu D:\Backup\ubuntu.tar
```

---

## **导入**

```powershell
wsl --import Ubuntu D:\WSL D:\Backup\ubuntu.tar
```

---

## **注销（删除）**

⚠️ 会删除整个 Ubuntu

```powershell
wsl --unregister Ubuntu
```

---

# **二、Linux 基本命令**

## **当前目录**

```bash
pwd
```

例如

```text
/home/zl
```

---

## **查看文件**

```bash
ls
```

显示详细信息

```bash
ls -l
```

显示隐藏文件

```bash
ls -la
```

---

## **切换目录**

```bash
cd
```

进入

```bash
cd Downloads
```

回上一级

```bash
cd ..
```

回 HOME

```bash
cd ~
```

---

## **创建目录**

```bash
mkdir test
```

递归创建

```bash
mkdir -p a/b/c
```

---

## **删除**

删除文件

```bash
rm file.txt
```

删除目录

```bash
rm -rf test
```

⚠️

```bash
rm -rf /
```

千万不要执行。

---

## **复制**

```bash
cp a.txt b.txt
```

复制目录

```bash
cp -r dir1 dir2
```

---

## **移动/重命名**

```bash
mv old.txt new.txt
```

---

# **三、查看系统**

查看系统版本

```bash
cat /etc/os-release
```

查看内核

```bash
uname -a
```

查看 CPU

```bash
lscpu
```

查看内存

```bash
free -h
```

查看磁盘

```bash
df -h
```

查看目录大小

```bash
du -sh *
```

---

# **四、软件管理（Ubuntu）**

更新软件源

```bash
sudo apt update
```

升级

```bash
sudo apt upgrade
```

安装

```bash
sudo apt install git
```

删除

```bash
sudo apt remove git
```

搜索

```bash
apt search python
```

查看已安装

```bash
apt list --installed
```

---

# **五、文件查看**

查看内容

```bash
cat file.txt
```

分页

```bash
less file.txt
```

查看前十行

```bash
head file.txt
```

查看后十行

```bash
tail file.txt
```

实时日志

```bash
tail -f logfile
```

---

# **六、查找**

查找文件

```bash
find . -name "*.py"
```

全文搜索

```bash
grep hello file.txt
```

递归搜索

```bash
grep -rn "hello" .
```

---

# **七、权限**

修改权限

```bash
chmod +x test.sh
```

修改所有者

```bash
sudo chown zl:zl test.sh
```

---

# **八、网络**

查看 IP

```bash
ip addr
```

查看路由

```bash
ip route
```

测试网络

```bash
ping google.com
```

下载文件

```bash
curl URL
```

例如：

```bash
curl https://example.com
```

下载保存

```bash
curl -O URL
```

---

# **九、进程**

查看进程

```bash
ps aux
```

实时

```bash
top
```

结束

```bash
kill PID
```

强制

```bash
kill -9 PID
```

---

# **十、Git**

查看状态

```bash
git status
```

克隆

```bash
git clone URL
```

提交

```bash
git add .
git commit -m "init"
```

推送

```bash
git push
```

拉取

```bash
git pull
```

---

# **十一、Python**

版本

```bash
python3 --version
```

虚拟环境

```bash
python3 -m venv .venv
```

激活

```bash
source .venv/bin/activate
```

退出

```bash
deactivate
```

安装

```bash
pip install 包名
```

---

# **十二、SSH**

连接

```bash
ssh user@IP
```

生成密钥

```bash
ssh-keygen
```

复制公钥

```bash
ssh-copy-id user@IP
```

---

# **十三、WSL 与 Windows 互通（非常实用）**

打开 Windows 资源管理器

```bash
explorer.exe .
```

打开当前目录。

---

打开 VS Code

```bash
code .
```

（需要安装 VS Code 和 WSL 扩展。）

---

访问 Windows C 盘

```bash
cd /mnt/c
```

例如：

```bash
cd /mnt/c/Users/zl/Downloads
```

---

执行 Windows 程序

```bash
notepad.exe
```

或者

```bash
powershell.exe
```

---

# **十四、Hermes Agent 常用**

查看版本

```bash
hermes --version
```

健康检查

```bash
hermes doctor
```

更新

```bash
hermes self-update
```

---

# **十五、我最推荐优先掌握的 20 个命令（按使用频率）**

| **命令**             | **用途**   |
| ------------------ | -------- |
| `pwd`              | 当前目录     |
| `ls -la`           | 查看文件     |
| `cd`               | 切换目录     |
| `mkdir`            | 新建目录     |
| `cp`               | 复制       |
| `mv`               | 移动/重命名   |
| `rm -rf`           | 删除（谨慎使用） |
| `cat`              | 查看文件     |
| `nano`             | 编辑文件     |
| `find`             | 查找文件     |
| `grep`             | 搜索内容     |
| `sudo apt update`  | 更新软件源    |
| `sudo apt install` | 安装软件     |
| `df -h`            | 查看磁盘     |
| `free -h`          | 查看内存     |
| `ip addr`          | 查看 IP    |
| `ps aux`           | 查看进程     |
| `top`              | 实时监控     |
| `curl`             | 下载/请求    |
| `ssh`              | 远程连接     |

---

结合你目前的使用场景（Windows 11 + WSL2 + Ubuntu + Hermes Agent + Python + Git + Vaultwarden），我还建议额外整理一份**《WSL 高频命令速查手册（100+ 命令，按场景分类）》**，涵盖文件管理、系统维护、网络排障、Git、Python、Docker、SSH、磁盘管理和 Windows/WSL 互操作等内容，作为长期参考会很实用。