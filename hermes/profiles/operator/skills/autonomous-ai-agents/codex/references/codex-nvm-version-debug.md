# Codex NVM 版本调试记录

## 问题现象

`codex --version` 报 0.130.0，即使 `npm install -g @openai/codex` 显示成功（added 2 packages），且 `~/.nvm/versions/node/v24.13.0/bin/npm list -g` 似乎显示 0.139.0。

## 根本原因

**NVM npm 在未加载 nvm.sh 时读取 Hermes 的 node_modules。**

当直接调用 NVM 的 npm 二进制而不先 `source ~/.nvm/nvm.sh` 时，npm 的 prefix 解析会落到 `~/.hermes/node/`（Hermes 自带的 Node 环境），而不是 NVM 的目录。所以 `npm list -g` 显示的是 Hermes 的 codex（0.139.0），而非 NVM 的 codex（0.130.0）。

## 完整修复步骤

```bash
# 1. 确认问题
which codex                    # → NVM 路径
codex --version                # → 0.130.0（旧的）

# 2. 加载 NVM 上下文
source ~/.nvm/nvm.sh

# 3. 检查真实版本（现在 npm 读的是 NVM 的 node_modules）
npm ls -g @openai/codex --depth=0   # → @openai/codex@0.130.0

# 4. 卸载旧版
npm uninstall -g @openai/codex       # → removed 2 packages

# 5. 清理缓存
npm cache clean --force

# 6. 安装指定版本
npm install -g @openai/codex@0.139.0 # → added 2 packages

# 7. 验证
hash -r
which codex                          # → ~/.nvm/versions/node/v24.13.0/bin/codex
codex --version                      # → codex-cli 0.139.0
npm ls -g @openai/codex --depth=0    # → @openai/codex@0.139.0
cat ~/.nvm/versions/node/v24.13.0/lib/node_modules/@openai/codex/package.json | grep version
# → "version": "0.139.0"
```

## 环境上下文

- macOS 26.5.1
- NVM node v24.13.0 (`~/.nvm/versions/node/v24.13.0/`)
- Hermes Agent (`~/.hermes/node/` 自建 Node)
- Hermes 的 codex: `~/.hermes/node/bin/codex` → 0.139.0（不受影响）
- 用户偏好：NVM 是主力 Node/npm 环境，Hermes node 仅供内部使用
