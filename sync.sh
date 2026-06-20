#!/bin/bash
# sync.sh — 把当前系统状态同步到 ~/dotfiles/ 仓库
# 用法: cd ~/dotfiles && bash sync.sh

set -e

DOTFILES="$(cd "$(dirname "$0")" && pwd)"

echo "🔄 开始同步 dotfiles..."

# 1. 配置文件
if [ -f ~/.zshrc ]; then
  cp ~/.zshrc "$DOTFILES/home/.zshrc"
  echo "  ✅ .zshrc"
fi

if [ -f ~/.gitconfig ]; then
  cp ~/.gitconfig "$DOTFILES/home/.gitconfig"
  echo "  ✅ .gitconfig"
fi

# 2. 自定义脚本
if [ -d ~/.local/bin ]; then
  rsync -a --delete "$HOME/.local/bin/" "$DOTFILES/bin/"
  echo "  ✅ ~/.local/bin/ → bin/"
fi

if [ -d ~/bin ]; then
  rsync -a --delete "$HOME/bin/" "$DOTFILES/bin/"
  echo "  ✅ ~/bin/ → bin/"
fi

# 3. Hermes 配置（排除 secrets 和缓存）
if [ -f ~/.hermes/config.yaml ]; then
  cp ~/.hermes/config.yaml "$DOTFILES/hermes/config.yaml"
  echo "  ✅ Hermes config.yaml"
fi

if [ -d ~/.hermes/skills ]; then
  rsync -a --delete \
    --exclude='.git' \
    "$HOME/.hermes/skills/" "$DOTFILES/hermes/skills/"
  echo "  ✅ Hermes skills/"
fi

if [ -d ~/.hermes/profiles ]; then
  rsync -a --delete \
    --exclude='.git' \
    "$HOME/.hermes/profiles/" "$DOTFILES/hermes/profiles/"
  echo "  ✅ Hermes profiles/"
fi

# 4. Obsidian 知识库（排除大附件）
OBSIDIAN_VAULT="$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/PKM"
if [ -d "$OBSIDIAN_VAULT" ]; then
  rsync -a --delete \
    --exclude='*.png' --exclude='*.jpg' --exclude='*.jpeg' \
    --exclude='*.gif' --exclude='*.bmp' --exclude='*.svg' \
    --exclude='*.pdf' --exclude='*.xlsx' --exclude='*.docx' \
    --exclude='*.pptx' --exclude='*.zip' \
    --exclude='.obsidian/workspace.json' \
    --exclude='.obsidian/cache/' \
    "$OBSIDIAN_VAULT/" "$DOTFILES/notes/"
  echo "  ✅ Obsidian PKM（不含附件）"
fi

echo ""
echo "🎉 同步完成！"
echo "下一步：cd ~/dotfiles && git add . && git commit -m '日常更新'"
