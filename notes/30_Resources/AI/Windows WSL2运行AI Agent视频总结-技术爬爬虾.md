---
title: Windows WSL2 运行 AI Agent 视频总结
aliases:
  - WSL2 AI Agent
  - Windows 运行 AI Agent
  - WSL 保姆级攻略
created: 2026-07-14
updated: 2026-07-14
type: reference
tags:
  - r/tools/hermes
  - r/tools/wsl
  - r/ai/agent
source: https://www.bilibili.com/video/BV1pYNm69EPm/
---



视频：《Windows跑AI Agent，WSL才是终极答案，别羡慕Mac了，WSL保姆级全攻略》

视频时长约 31 分 31 秒，UP 主：技术爬爬虾。

> [!summary] 核心结论
> Windows 运行 AI Agent 时，推荐使用 WSL2 作为 Linux 执行环境：Windows 负责桌面、浏览器和 GUI 软件，WSL2 负责 Agent、Shell、Git、Python、Node.js、Docker 以及本地模型。这样既保留 Windows 的桌面体验，又能获得接近 Linux 服务器的开发环境。

## 一、为什么用 WSL2 运行 AI Agent

视频给出三个主要原因：

1. **Agent 执行更稳定**：AI 模型训练语料中大量命令是 Linux/macOS 风格，Linux Shell 相比 PowerShell 更容易被 Agent 正确使用。
2. **更接近生产环境**：代码最终通常部署到 Linux 服务器或 Docker 中，在 WSL2 内开发和测试可以减少环境差异。
3. **环境隔离更安全**：WSL2 是相对独立的 Linux 环境，即使 Agent 误操作破坏了系统，也通常不会影响 Windows 主系统；严重时可以删除并重新创建 WSL 实例。

## 二、WSL2 基础安装与管理

### 检查 CPU 虚拟化

Windows：

```text
任务管理器 → 性能 → CPU → 虚拟化
```

如果没有启用，需要在 BIOS 中开启：

- Intel：Intel VMX / Intel Virtualization Technology
- AMD：SVM Mode

### 安装 WSL

```powershell
wsl --install
```

国内网络下载较慢时可以尝试：

```powershell
wsl --install --web-download
```

安装过程中如果要求重启，重启后重新打开 Windows Terminal，再执行安装命令。

### 常用管理命令

```powershell
# 查看在线可安装发行版
wsl -l -o

# 查看已经安装的发行版及 WSL 版本
wsl -l -v

# 启动默认发行版
wsl

# 启动指定发行版
wsl -d Ubuntu

# 退出 Linux
exit

# 设置默认发行版
wsl --set-default Ubuntu

# 更新 WSL 本体
wsl --update

# 查看 WSL 版本
wsl --version
```

应确保实际使用的是 WSL2，而不是 WSL1。

> [!warning] 命令版本差异
> 视频中的部分发行版安装、指定安装目录和创建多个实例的命令可能随 WSL 版本变化。实际执行前应以 `wsl --help` 和微软当前文档为准。

## 三、Linux 开发环境

视频将 Git、Python、Node.js 作为运行 AI Agent 前的基础环境。

```bash
git --version
python3 --version
node -v
npm -v
```

Ubuntu 通常自带 `python3`，但不一定提供 `python` 命令，可以安装兼容命令：

```bash
sudo apt update
sudo apt install python-is-python3
```

Node.js 推荐使用 NVM 管理，而不是直接依赖 apt 安装：

```bash
node -v
npm -v
```

本机已有 NVM 和 Node.js 24，不需要按视频重复安装。

## 四、项目文件应该放在哪里

推荐把项目放在 WSL 的 Linux 原生目录：

```text
/home/用户名/projects/
```

不推荐长期放在 Windows 挂载目录：

```text
/mnt/c/Users/用户名/projects/
```

原因是跨操作系统文件读写会产生额外 I/O 开销，尤其会影响：

- Node.js 项目
- `node_modules`
- Git 操作
- Python 虚拟环境
- Agent 扫描大量项目文件

Windows 资源管理器可以通过以下方式访问 WSL 文件：

```bash
explorer.exe .
```

也可以在资源管理器地址栏中使用：

```text
\\wsl$\Ubuntu\
```

WSL 中访问 Windows 磁盘：

```bash
cd /mnt/c
cd /mnt/d
```

## 五、AI Agent 与开发工具

视频演示了在 WSL 中运行多种 Agent：

- 轻量级 Coding Agent
- Hermes Agent
- Claude Code
- Codex CLI

总体模式是：

```text
Agent 在 WSL 中运行
代码放在 WSL Linux 目录
Windows 浏览器、VS Code 和 GUI 软件作为前端
```

### VS Code

在 WSL 项目目录中执行：

```bash
code .
```

可使用 Windows 版 VS Code 打开 WSL 项目，并继续使用：

- 代码编辑
- 调试
- Git 操作
- GitHub 发布

### Codex

Windows 桌面版 Codex/ChatGPT 应用可以把 Agent 环境切换到 WSL：

```text
设置 → 常规 → 智能体环境 → WSL
```

不过视频指出，桌面版连接 WSL 时通常会把 Windows 文件夹挂载进 WSL，存在跨文件系统 I/O 性能损失。长期开发更推荐直接在 WSL 内运行 Codex CLI。

## 六、WSL 与 Windows 的网络互通

WSL 默认会自动转发监听端口。

例如 WSL 中的 Node.js 服务监听 3000 端口，Windows 浏览器通常可以直接访问：

```text
http://localhost:3000
```

默认网络关系：

```text
Windows 宿主机 localhost
        ↓ 自动端口转发
WSL Linux 服务
```

WSL 也可以通过 Windows 宿主机的局域网 IP 访问 Windows 上运行的服务。

### 让局域网设备访问 WSL 服务

在 Windows 用户目录创建：

```text
C:\Users\用户名\.wslconfig
```

示例：

```ini
[wsl2]
networkingMode=mirrored
```

保存后关闭所有 WSL 窗口，等待 WSL 完全退出，再重新启动。

镜像网络模式可以让 Windows 和 WSL 使用相同的网络环境，使手机等局域网设备访问 WSL 服务更加方便。必要时还要配置 Windows/WSL 防火墙规则。

> [!warning] 暴露服务的安全风险
> 使用 mirrored network 和防火墙放行后，WSL 中监听的服务可能被局域网其他设备访问。只应开放确实需要的端口，并避免把开发服务直接暴露到公网。

## 七、Docker

最新版 WSL2 支持 systemd 后，在 WSL 中运行 Docker 的体验已经接近真正的 Linux 电脑。

视频使用 Redis 作为示例：

```bash
sudo docker run -d \
  -p 6379:6379 \
  --name redis \
  redis
```

管理容器：

```bash
sudo docker ps -a
sudo docker start <容器ID或容器名称>
```

Windows 上的 Redis GUI 客户端可以连接：

```text
Host: localhost
Port: 6379
```

关闭 WSL 虚拟机后，里面运行的 Docker 容器也会停止；重新启动 WSL 后需要手动启动容器，除非配置了自动启动策略。

## 八、WSL2、GPU 直通与本地模型

WSL2 基于 Hyper-V，并使用真正的 Linux 内核。它支持 Windows 主机 GPU 直通。

NVIDIA 环境中可以在 WSL 内执行：

```bash
nvidia-smi
```

可以看到：

- 显卡型号
- 驱动版本
- CUDA 版本
- 显存使用情况

> [!warning] 不要在 WSL 内重复安装 NVIDIA 驱动
> WSL 使用 Windows 主机上的 NVIDIA 驱动。WSL 内部不应再安装一套独立的 Windows NVIDIA 驱动。根据具体框架需要安装 CUDA 用户态组件和 AI 框架即可。

视频使用 vLLM 演示本地模型部署，流程包括：

1. 安装 uv；
2. 创建 Python 环境；
3. 安装 vLLM；
4. 启动 Qwen 等模型；
5. 通过 Postman 调用推理 API；
6. 根据显存情况调整启动参数。

这说明 WSL2 适合运行：

- vLLM
- Ollama
- llama.cpp
- PyTorch
- CUDA
- 本地大模型推理

## 九、图形界面

### WSLg

WSLg 可以把单个 Linux 图形程序直接显示在 Windows 桌面中，例如：

```bash
sudo apt install gimp
gimp
```

适合运行单个 GUI 应用，不等于完整 Linux 桌面。

### 完整桌面

视频还演示了：

- Kali Linux + Win-KeX
- Ubuntu + 远程桌面 RDP

Ubuntu 方案可以通过获取 WSL IP，再使用 Windows 远程桌面连接：

```text
WSL_IP:3389
```

## 十、`.wslconfig` 与 `wsl.conf`

两者不要混淆。

| 文件 | 所在位置 | 作用范围 | 主要用途 |
|---|---|---|---|
| `.wslconfig` | Windows 用户目录 | 所有 WSL 实例 | 内存、CPU、网络、内核等全局设置 |
| `wsl.conf` | Linux 内部 `/etc/wsl.conf` | 单个发行版 | systemd、自动挂载、默认用户等 |

示例：关闭某个发行版自动挂载 Windows 磁盘：

```ini
[automount]
enabled=false
```

这样可以减少 Agent 看到 Windows 文件的范围，提高隔离性，但也会降低 WSL 与 Windows 文件之间的便利性。

## 十一、WSL 备份、恢复和克隆

导出发行版：

```powershell
wsl --export Ubuntu Ubuntu.tar
```

删除发行版：

```powershell
wsl --unregister Ubuntu
```

从备份恢复：

```powershell
wsl --import Ubuntu D:\WSL\Ubuntu Ubuntu.tar
```

用途：

- 备份整个 Linux 环境
- 重装 Windows 后恢复
- 迁移到另一台电脑
- 克隆多个相同的 Agent 环境

但 API Key、Telegram Token、SSH 密钥和环境变量仍应单独备份，不能把 WSL 导出包作为唯一备份。

## 十二、对当前 Hermes 架构的启示

视频推荐的分工与当前架构基本一致：

```text
Windows：
- Telegram
- 浏览器
- VS Code
- Codex Desktop
- GUI 软件

WSL：
- Hermes
- Codex CLI
- Claude Code
- Git
- Node.js
- Python
- Docker
- 项目代码和服务
```

结合当前多节点架构：

```text
macOS Hermes：主控、总调度、任务汇总
Win11 WSL Hermes：Windows 侧执行节点
Telegram：统一任务入口
WSL Linux 原生目录：项目和 Agent 工作目录
Windows GUI：浏览器、VS Code、桌面端 Codex
Docker：本地服务和开发依赖
```

## 十三、视频内容中的语音识别纠正

原始转写中存在一些识别错误，阅读时应按以下内容理解：

| 转写错误 | 正确内容 |
|---|---|
| AA Agent / AA | AI Agent |
| Carly Linux | Kali Linux |
| Hermis Agent | Hermes Agent |
| Cloud Code | Claude Code |
| Grip | grep |
| 速度 apt | sudo apt |
| WSL-L | `wsl -l` |
| WSL-D | `wsl -d` |
| WSL-update | `wsl --update` |
| WSL-install | `wsl --install` |
| 挂载券 | 挂载卷 |
| Python ispython3 | `python-is-python3` |
| NVIDIA-SMI | `nvidia-smi` |

视频适合作为架构和实践思路参考，但不能把语音识别文本直接当作命令手册。具体命令应以当前 WSL、Hermes、Docker 和模型官方文档为准。

## 十四、最终结论

Windows 不需要在桌面体验和 Linux 开发能力之间二选一。WSL2 可以把两者结合起来：

```text
Windows 负责桌面体验
WSL2 负责 Linux 开发和 Agent 执行
Windows 软件负责界面、浏览器和 GUI
WSL 负责命令、Docker、Git、模型和服务
```

对当前环境而言，最值得落实的三点是：

1. Hermes、Codex CLI 和其他 Agent 放在 WSL2 中运行；
2. 项目长期放在 WSL Linux 原生目录，而不是 `/mnt/c`；
3. 定期使用 `wsl --export` 备份 Win11 的 Hermes WSL 实例，同时单独备份密钥和配置。

## 相关笔记

- [[Hermes 备份 2026-06-12]]
- [[WSL Ubuntu部署SSHServer（MacBook登录）]]
- [[WSL SSH 启动与连接排查命令简表]]
- [[Hermes-6个核心角色任务分配规则表]]
