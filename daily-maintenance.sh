#!/bin/bash
# daily-maintenance.sh — 每天早上 4 点运行
# 1. 升级 Hermes
# 2. 同步 dotfiles 仓库
# 3. 提交并推送到 GitHub

set -e

echo "=== 每天 4 点维护任务 ==="
echo ""

# 1. Hermes 升级
echo "[1/3] 升级 Hermes..."
hermes update 2>&1 || echo "⚠️  hermes update 失败（网络或权限问题），跳过"
echo ""

# 2. 同步 dotfiles
DOTFILES="$HOME/dotfiles"
echo "[2/3] 同步 dotfiles..."
if [ -d "$DOTFILES" ]; then
  cd "$DOTFILES"
  bash sync.sh 2>&1
  echo "✅ 同步完成"
else
  echo "⚠️  ~/dotfiles 不存在，跳过"
fi
echo ""

# 3. 提交并推送
echo "[3/3] 提交到 Git..."
if [ -d "$DOTFILES/.git" ]; then
  cd "$DOTFILES"
  git add .
  if git diff --cached --quiet; then
    echo "ℹ️  无变更，跳过提交"
  else
    git commit -m "每日自动更新 $(date +%F)"
    git push 2>&1 && echo "✅ 已推送到 GitHub" || echo "⚠️  push 失败"
  fi
else
  echo "⚠️  ~/dotfiles 不是 git 仓库，跳过"
fi
echo ""
echo "=== 维护任务完成 ==="
