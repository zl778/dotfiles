# dotfiles — zl778 的个人配置 + 脚本 + 知识库

统一管理我的开发环境配置、自定义脚本和 Obsidian 知识库。
用 git 做版本控制，方便回溯、迁移、备份。

## 目录结构

```
home/           ← 配置文件 (.zshrc, .gitconfig 等)
bin/            ← 自定义脚本
hermes/         ← Hermes Agent 配置快照
  config.yaml
  profiles/
  skills/
notes/          ← Obsidian PKM 知识库快照
```

## 工作流

```bash
# 1. 把当前状态同步到仓库
cd ~/dotfiles && bash sync.sh

# 2. 查看改了什么
git diff --stat

# 3. 提交
git add . && git commit -m "日常更新"

# 4. 推到 GitHub（远程已配的情况下）
git push
```

## 注意事项

- API key、token 等机密文件在 `.gitignore` 中，**绝对不要提交**
- `.env` 和 `auth.json` 只保留 `.template` 版本（脱敏后的结构参考）
- Obsidian 的图片附件等大文件被 `.gitignore` 排除
- 首次克隆后需手动安装依赖、复制 `.env.template` 为 `.env`
