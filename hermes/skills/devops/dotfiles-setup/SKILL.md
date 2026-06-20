---
name: dotfiles-setup
description: "设置同步式 dotfiles 仓库：将 Hermes 配置、Obsidian 知识库、自定义脚本统一纳入 git 版本管理并推送到 GitHub。同步式（copy-based），非软链接式。"
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [dotfiles, git, github, backup, obsidian, hermes-config]
    related_skills: [github-auth, hermes-agent]
---

# dotfiles-setup

建立统一 git 仓库管理个人配置（dotfiles）、自定义脚本和笔记知识库，推送到 GitHub 做远程备份。

## 适用场景

- 用户想对 Hermes 配置、脚本、笔记做版本控制
- 换电脑时一键恢复环境
- 日常自动备份到 GitHub

## 架构选择

有两种方案：

| 方案 | 做法 | 适合 |
|------|------|------|
| **同步式（推荐）** | 仓库在 `~/dotfiles/`，用 `sync.sh` 从实际位置 copy 过来 | 文件有固定路径依赖（iCloud、~/.hermes/），安全稳妥 |
| **软链接式** | 仓库是"真身"，实际路径软链接指向仓库文件 | 需要更流畅的改完即 commit 体验，但 iCloud 路径有空格时易出问题 |

## 步骤

### 1. 初始化仓库

```bash
mkdir ~/dotfiles && cd ~/dotfiles && git init
mkdir -p home bin hermes/skills hermes/profiles notes
```

### 2. 创建 .gitignore

必须排除的内容：

```
# 密钥和认证
.env
.env.*
auth.json
**/credentials.json

# OS 垃圾
.DS_Store
Thumbs.db

# Obsidian 大附件（如果只同步纯文本）
notes/**/*.png
notes/**/*.jpg
notes/**/*.jpeg
notes/**/*.gif
notes/**/*.pdf
notes/**/*.xlsx
notes/**/*.docx
notes/**/*.pptx
notes/**/*.zip

# Hermes 缓存
hermes/sessions/
hermes/logs/
hermes/audio_cache/
hermes/state.db

# 缓存
*.log
__pycache__/
.venv/
venv/
```

### 3. 编写 sync.sh

```bash
#!/bin/bash
DOTFILES="$(cd "$(dirname "$0")" && pwd)"

# 配置文件
[ -f ~/.zshrc ] && cp ~/.zshrc "$DOTFILES/home/.zshrc"
[ -f ~/.gitconfig ] && cp ~/.gitconfig "$DOTFILES/home/.gitconfig"

# 脚本
[ -d ~/.local/bin ] && rsync -a --delete "$HOME/.local/bin/" "$DOTFILES/bin/"
[ -d ~/bin ] && rsync -a --delete "$HOME/bin/" "$DOTFILES/bin/"

# Hermes 配置（排除 secrets/缓存）
[ -f ~/.hermes/config.yaml ] && cp ~/.hermes/config.yaml "$DOTFILES/hermes/config.yaml"
[ -d ~/.hermes/skills ] && rsync -a --delete --exclude='.git' "$HOME/.hermes/skills/" "$DOTFILES/hermes/skills/"
[ -d ~/.hermes/profiles ] && rsync -a --delete --exclude='.git' "$HOME/.hermes/profiles/" "$DOTFILES/hermes/profiles/"

# Obsidian 知识库（排除大附件）
OBSIDIAN_VAULT="$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/PKM"
[ -d "$OBSIDIAN_VAULT" ] && rsync -a --delete \
  --exclude='*.png' --exclude='*.jpg' --exclude='*.jpeg' \
  --exclude='*.gif' --exclude='*.pdf' --exclude='*.xlsx' \
  --exclude='*.docx' --exclude='*.pptx' --exclude='*.zip' \
  --exclude='.obsidian/workspace.json' --exclude='.obsidian/cache/' \
  "$OBSIDIAN_VAULT/" "$DOTFILES/notes/"

echo "同步完成，请运行 git add + git commit"
```

### 4. 脱敏 API Key

`config.yaml` 中的 `api_key` 必须替换为环境变量引用：

```yaml
# 改前
api_key: sk-real...key

# 改后（安全）
api_key: ${SILICONFLOW_API_KEY}
```

同时创建 `.env.template` 供参考：

```bash
[ -f ~/.hermes/.env ] && grep '^[A-Z]' ~/.hermes/.env | sed 's/=.*/=your...key/' > hermes/.env.template
```

### 5. 首次提交

```bash
cd ~/dotfiles && bash sync.sh
git add .
git commit -m "初始提交：dotfiles 仓库"
```

### 6. 推送到 GitHub

先完成 GitHub 认证（见 github-auth skill），然后：

```bash
cd ~/dotfiles
gh repo create zl778/dotfiles --public --source=. --push
# 或手动：
git remote add origin git@github.com:zl778/dotfiles.git
git push -u origin main
```

### 7. 日常维护

```bash
cd ~/dotfiles && bash sync.sh && git add . && git commit -m "日常更新" && git push
```

### 8. 可选：添加自动 cron

创建 `daily-maintenance.sh`（放在 `~/.hermes/scripts/` 下），合并 hermes update + sync + git push。然后用 cronjob 工具创建每天 4am 的定时任务，`no_agent=true`。

## 注意事项

- **同步式 vs 软链接式**：iCloud Obsidian 路径和 `~/.hermes/` 有固定位置，不适合搬迁，同步式更安全
- **API key 脱敏**：提交前务必用 `${VAR}` 替换真实 key，否则 git 历史里永远有明文
- **首次提交很大**（2000+ 文件正常），因为笔记和历史会话很多
- **cron 脚本必须放 `~/.hermes/scripts/`**，cronjob 工具只接受相对路径
- **跨 profile 写文件**：在默认 profile 下写 wukong profile 的记忆时，需要 `cross_profile=true`

## 验证

```bash
cd ~/dotfiles
git status  # 看看有没有未跟踪的 secret 文件
git log --oneline -3
git remote -v
```
