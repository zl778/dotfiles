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

## 日常维护

### 向已有仓库添加新文件

需要把一个新的配置文件（如 `.nanorc`、`.vimrc`）纳入 dotfiles 管理时，三步搞定：

```bash
# 1. 复制到仓库
cp ~/.nanorc ~/dotfiles/home/.nanorc

# 2. 更新 sync.sh，在「配置文件」区域添加一行
# 找到 ~/.gitconfig 那一段，在后面加：
# if [ -f ~/.nanorc ]; then
#   cp ~/.nanorc "$DOTFILES/home/.nanorc"
#   echo "  ✅ .nanorc"
# fi\n\n# 3. 提交推送\ncd ~/dotfiles\ngit add home/.nanorc sync.sh\ngit commit -m \"添加 .nanorc 到 dotfiles\"\ngit push\n```\n\n### 多机同步工作流\n\n有三台以上环境时（如 macOS + WSL + VPS），正确的同步顺序是：\n\n```\n机器A: 改配置 → sync.sh → commit + push\n                                          ↓\n机器B: git pull --rebase → 部署到本机 → sync.sh → commit + push\n                                          ↓\n机器C: git pull --rebase → 部署到本机 → sync.sh → commit + push\n```\n\n部署到本机的意思是将仓库里的配置复制到实际位置：\n\n```bash\ncd ~/dotfiles && git pull --rebase\n[ -f home/.nanorc ] && cp home/.nanorc ~/.nanorc\n[ -f home/.zshrc ] && cp home/.zshrc ~/.zshrc\n# ... 其他配置文件同理\n```\n\n### 自动化维护（cron）\n\n`daily-maintenance.sh` 是可选自动化脚本，通常放 `~/.hermes/scripts/`，每天 4am 运行。\n\n**警告：修改这个脚本涉及系统级自动化操作，必须经过用户明确确认。** 先展示改动内容，等用户同意后再写入。\n\n推荐的完整流程：\n\n```bash\n#!/bin/bash\nset -e\n\nDOTFILES=\"$HOME/dotfiles\"\n\n# 0. 拉取远端变更 + 部署到本机\ncd \"$DOTFILES\"\ngit pull --rebase 2>&1 || true\n[ -f home/.nanorc ] && cp home/.nanorc ~/.nanorc\n[ -f home/.zshrc ] && cp home/.zshrc ~/.zshrc\n\n# 1. Hermes 升级\nhermes update 2>&1 || true\n\n# 2. 同步本机状态到仓库\nbash sync.sh\n\n# 3. 提交推送\ncd \"$DOTFILES\"\ngit add .\ngit diff --cached --quiet || {\n  git commit -m \"每日自动更新 $(date +%F)\"\n  git push\n}\n```\n\n## 注意事项\n\n- **同步式 vs 软链接式**：iCloud Obsidian 路径和 `~/.hermes/` 有固定位置，不适合搬迁，同步式更安全\n- **API key 脱敏**：提交前务必用 `${VAR}` 替换真实 key，否则 git 历史里永远有明文\n- **首次提交很大**（2000+ 文件正常），因为笔记和历史会话很多\n- **cron 脚本必须放 `~/.hermes/scripts/`**，cronjob 工具只接受相对路径\n- **跨 profile 写文件**：在默认 profile 下写 wukong profile 的记忆时，需要 `cross_profile=true`\n- **多机同步时先 pull 再 push**：防止冲突，永远先拉取别人的变更\n\n## 验证\n\n```bash\n# 确认无 secret 泄露\ncd ~/dotfiles\ngit diff --cached | grep -i 'api_key\\\\|token\\\\|secret' || echo \"✅ 无密钥泄露\"\n\n# 检查仓库状态\ngit status\ngit log --oneline -3\ngit remote -v\n\n# 测试同步流程\nbash sync.sh && git status\ngit diff --cached --quiet && echo \"✅ 无变更，同步正常\"\n```\n\n## 跨技能重叠说明\n\n当前 Hermes 库中有两个 dotfiles 相关 skill：\n- `dotfiles-setup`（中文）— 本文件，面向中文用户\n- `dotfiles-repo-setup`（英文）— 英文版，内容高度重叠\n\n这两个技能内容重复，后续 curator 应考虑合并或归档其中之一。"}
