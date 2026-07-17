---
created: 2026-07-05
tags:
  - r/tools/ssh
aliases:
  - WSL
updated: 2026-07-18
---

# WSL SSH 启动与连接排查命令简表

## 最常用命令

| 命令 | 简单说明 |
| --- | --- |
| `sudo systemctl enable --now ssh` | 启动 SSH 服务，并设为以后随 WSL 自动启动。通常只需执行一次。 |
| `systemctl status ssh` | 查看 SSH 服务当前是否运行；看到 `active (running)` 表示正常。 |
| `sudo systemctl restart ssh` | SSH 服务异常时重新启动。 |
| `ssh zl@192.168.26.26` | 从另一台电脑以用户 `zl` 连接这台 WSL。 |
| `hostname -I` | 查看 WSL 当前 IP 地址；WSL 重启后 IP 可能变化。 |

## 服务和端口排查

| 命令 | 简单说明 |
| --- | --- |
| `sudo systemctl status sshd` | 查看 SSH 服务状态；在 Ubuntu 中通常会指向实际的 `ssh.service`。更建议直接使用 `systemctl status ssh`。 |
| `sudo systemctl status ssh.socket` | 检查 SSH 的 systemd 套接字激活状态。 |
| `sudo ss -lntp \| grep ':22'` | 检查 TCP 22 端口是否正在监听。看到 `0.0.0.0:22` 或 `[::]:22` 通常表示 SSH 已监听。 |
| `sudo journalctl -u ssh.service -u ssh.socket -n 100` | 查看 SSH 服务和套接字最近 100 条日志，用于寻找启动失败或连接被断开的原因。 |

## 从客户端检查连接

| 命令 | 简单说明 |
| --- | --- |
| `ping 192.168.26.26` | 检查目标 IP 在网络层是否可达。部分防火墙会禁止 ping，因此 ping 失败不一定代表机器关机。 |
| `nc -vz 192.168.26.26 22` | 快速测试目标机器的 TCP 22 端口是否可以连接。 |
| `ssh -vvv root@192.168.26.26` | 输出详细的 SSH 连接过程，适合定位连接在哪一步失败。 |
| `ssh root@192.168.26.26` | 尝试以 `root` 用户连接；一般更建议使用普通用户登录后再执行 `sudo`。 |

## 常见报错含义

| 报错 | 含义 |
| --- | --- |
| `No route to host` | 当前无法到达目标 IP，常见原因是 IP 错误、网络/VLAN/路由问题、防火墙阻断，或目标机器未接入网络。 |
| `Connection refused` | 已到达目标机器，但目标端口没有服务监听；常见于 SSH 服务未启动。 |
| `Connection reset by peer` | 已连接到目标端口，但对端在握手过程中主动断开；可能是 SSH 服务异常、防火墙、连接限制或 IP 冲突。 |
| `Permission denied` | 网络和 SSH 服务基本正常，但用户名、密码、密钥或登录权限不正确。 |

## WSL 重启后的操作

首次配置：

```bash
sudo systemctl enable --now ssh
```

以后 WSL 启动后一般不需要再运行启动命令。需要确认时执行：

```bash
systemctl status ssh
hostname -I
```

> [!note]
> Windows 开机不一定会立即启动 WSL 发行版。需要先启动该 WSL；随后已启用的 SSH 服务才会自动运行。
