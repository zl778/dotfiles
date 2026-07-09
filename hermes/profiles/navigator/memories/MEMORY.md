CLI 工具布局：复杂工具 ~/.local/opt/<name>/，纯二进制 ~/.local/bin/，软链接 ~/bin/。已装 memo、mlx-whisper、word-collector.py。NVM 是主 Node（~/.nvm/versions/node/v24.13.0/bin/），Hermes 内部 node 不混用。Codex CLI 固定在 0.139.0。
§
Obsidian vault: ~/Library/Mobile Documents/iCloud~md~obsidian/Documents/PKM/。大文件写入超时用 terminal heredoc。Obsidian CLI 已验证连通（v1.12.7）。
§
PARA 文件夹用下划线：`10_Projects/`, `20_Areas/`, `30_Resources/`, `90_Archives/`, `00_Inbox/`。
§
解释风格：类比+对比表格 + 实际场景举例，非定义式。用户非全栈，需要基础易懂。
§
wukong profile：别名 ~/.local/bin/wukong，provider=openai-codex model=o4-mini，fallback DeepSeek。auth.json 已导入全局 credential。
§
.env 受保护不能直接写入。环境变量需用户手动编辑或用 `hermes gateway setup` 向导。
§
Telegram 群 H26: 5584761717，用户: 8588918249。主力 bot + wukong bot 已入群。Uptime Kuma 通知也配到该群。
§
域名 61877778.xyz（Cloudflare 灰云）。VPS: 199.115.228.154, Debian 13, UFW, fair-cubes-1。NPM 代理用容器 IP。
§
macOS .app 替换必须用 `ditto`（`cp -R` 会合并遗留旧文件）。不用 `rm -rf + cp -R`。验证用 `md5 -q` 对比 checksum。
§
用户倾向把 Hermes 的 Research/Coding/Browser 视为逻辑角色，而不是一开始就创建独立实例。
§
用户希望用 Telegram 群作为 Hermes 任务入口，由 Mac Hermes 统一调度；cmux 负责执行，多任务状态通过 Kanban 管理。
§
User prefers a single main Hermes as the primary conversational entry point; worker agents should sit behind a routing layer rather than be chatted with directly. They treat Telegram as a mobile interaction mode, cmux as an execution mode, and the desktop Hermes app as a management/overview mode. They also value a stable always-on Win11 desktop node to offload the Mac and handle long-running or heavier tasks.
§
用户在 Obsidian 笔记中偏好：frontmatter 置顶，aliases 放灵活别名/检索词，tags 保持稳定命名空间（如 r/tools/hermes）。
§
用户偏好只向主 Hermes 下达任务，由主 Hermes 负责分配给子 agent，不直接对多个子角色分别交互。
§
用户使用场景偏好：外出时用 Telegram 与 Hermes 交互；在电脑前同时操作 Codex CLI、Hermes 和终端时用 cmux；用 Hermes 桌面端做任务总览、整理和管理。
§
用户在多主题会话中更偏好用 /new 分隔话题；例如在讨论多 Agent 方案时若临时转去 Kanban，倾向先开新会话把 Kanban 讲完，再回到原会话。
§
用户偏好 Obsidian 笔记前置属性中使用 aliases 存放灵活别名；tags 偏好保持更有条理、使用更稳定的命名空间，例如 r/tools/hermes。
§
Mac 可以通过 SSH 访问 Win11：ssh zl@192.168.26.62（已配置 SSH 密钥）；Win11-main 的下载目录重定向到 C:\Users\zl\Win11-Main_downloads。
§
用户希望 Hermes 的 default / Supervisor 角色采用 delegate-first 风格：优先分配给子 agent，先理解再执行，中文为主，先给结论再给解释，输出要清晰、可执行、可靠。