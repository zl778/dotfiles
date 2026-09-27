# OrbStack 卸载 & 重装记录

## 环境

- macOS 26.5.1 (Apple Silicon M4 Max)
- OrbStack 此前通过 Homebrew cask 安装（旧版 v2.0.5），后通过 App Store 渠道和手动方式混淆
- 用户从旧电脑迁移到新电脑后 OrbStack 损坏

## 卸载清单

OrbStack 安装的文件分散在多个位置，需要全部清理：

### 1. 停止服务

```bash
orbctl status      # 检查是否运行
# 如果运行中：orbctl stop
```

### 2. 主程序

```bash
sudo rm -rf /Applications/OrbStack.app
```

### 3. CLI 符号链接

```bash
# 检查路径（brew cask 安装走 /opt/homebrew/bin/，手动安装走 /usr/local/bin/）
ls -la /usr/local/bin/ | grep orb
ls -la /opt/homebrew/bin/ | grep orb

# 删除
sudo rm -f /usr/local/bin/orb /usr/local/bin/orbctl
# 或如果走 brew 路径：
# 注：brew uninstall --cask orbstack 可自动处理 brew 路径的 symlink，但不会删手动放置的
```

### 4. 配置目录

```bash
rm -rf ~/.orbstack/
```

包含：

| 路径 | 内容 |
|------|------|
| `~/.orbstack/config/` | Docker 配置 |
| `~/.orbstack/shell/` | Shell init 脚本 |
| `~/.orbstack/ssh/` | SSH 密钥对、known_hosts |
| `~/.orbstack/log/` | 日志（gui.log, vmgr.log 可能很大） |
| `~/.orbstack/bin/` | 内置工具 |
| `~/.orbstack/vmconfig.json` | VM 配置 |
| `~/.orbstack/vmstate.json` | VM 状态 |
| `~/.orbstack/.installid` | 安装标识 |

### 5. Shell 初始化行

检查 `.zprofile` 和 `.zshrc`：

```
# Added by OrbStack: command-line tools and integration
# This won't be added again if you remove it.
source ~/.orbstack/shell/init.zsh 2>/dev/null || :
```

删除这几行。移除后 `.zshrc`/`.zprofile` 中不应再包含 `orbstack` 引用。

### 6. Docker socket 残链

```bash
# 检查
ls -la /var/run/docker.sock
# 如果指向 ~/.docker/run/docker.sock（OrbStack 管理的）
sudo rm -f /var/run/docker.sock
rm -rf ~/.docker/run
```

### 7. 验证卸载

```bash
find /Applications -name "*OrbStack*" -maxdepth 1 2>/dev/null || echo "App not found"
find /usr/local/bin /opt/homebrew/bin -name "orb*" 2>/dev/null || echo "CLI not found"
[ -d ~/.orbstack ] || echo "Config not found"
grep -rn 'orbstack' ~/.zshrc ~/.zprofile 2>/dev/null || echo "No shell rc references"
```

## 重装

### 通过 Homebrew cask（推荐）

```bash
HOMEBREW_NO_AUTO_UPDATE=1 brew install --cask orbstack
```

安装后提示："Open the OrbStack app to finish setup." 用户需要手动打开 App 完成初始化（同意协议、配置权限等）。

### 版本信息

- 旧版：v2.0.5
- 新版（2025-06）：v2.1.3
- CLI 安装到：`/opt/homebrew/bin/orb` 和 `orbctl`（Apple Silicon 路径）
- Homebrew 自动补全 shell completion（zsh/fish/bash）

### 重装后 App 首次启动

Homebrew cask 安装后，App 在 `/Applications/OrbStack.app`，但需要用户手动打开：

1. 打开 OrbStack.app（从 Launchpad 或 Finder）
2. 同意系统权限（辅助功能、文件访问等）
3. 完成初始设置（创建默认 Linux 机器等）

## 注意事项

- 如果卸载后重装，`~/.orbstack/` 会被重新创建（但之前的 SSH 密钥、VM 快照丢失）
- 如果用户同时有 Docker Desktop 和 OrbStack，Docker socket 会打架。卸载 OrbStack 后 Docker Desktop 的 socket 会接管（如果 Docker Desktop 也在运行）
- OrbStack CLI（`orb`/`orbctl`）在 `/opt/homebrew/bin/` 下，不在 `/usr/local/bin/`，`which orb` 应显示 brew 路径
- `.zprofile` 中的 OrbStack init 行在重装后会自动由第一次启动的 OrbStack 重新添加
