用户要求所有回复使用简体中文（永久生效）。
§
用户说"提醒我"时用 Apple Reminders（osascript），不用 Hermes cron。
§
主 provider：OpenAI Codex（OAuth），不稳定时 fallback DeepSeek（deepseek-v4-flash）。已配置 fallback_model：provider=deepseek, model=deepseek-v4-flash。
§
从事智能化弱电工程（投标、采购、安防、政府项目）。Obsidian 以工具类内容为主。
§
Alfred 查单词用 word-collector，要求输出：音标、中文释义、2条带**加粗**单词的例句 + 中文翻译。偏好 Python 脚本。
§
MacBook Pro (Mac17,2) — M5 10核, 32GB, macOS 26.5.1。
§
注重安全。Telegram bot 需白名单授权（TELEGRAM_ALLOWED_USERS + group_allowed_chats）。
§
多 bot 架构：mac_honey_bot（macOS Hermes, Tg H26 主调度入口）通过 SSH 委托给 win11_main_bot（Win11 WSL, H26 副手）和 wukong（macOS Codex profile, 未来编码副手）；主 agent 自动判断任务归属后委托。任务上下文在 H26 群内互通，但跨会话偏好/经验默认不互通（需要共享记忆后端）。
§
习惯先讨论架构再动手，喜欢理解为什么这样设计。适合用类比+对比解释（如保安 vs 水电表）。
§
已掌握 Docker 自托管部署，熟悉 Nginx Proxy Manager。
§
Web 搜索首选 Tavily（免费额度每月 1000 次查询）
§
终端环境：cmux（基于 Ghostty 的 macOS 原生终端，TERM_PROGRAM=ghostty），主题通过 ~/.config/ghostty/config 配置
§
多 bot 架构：mac_honey_bot（macOS Hermes，Telegram H26）为主 agent 总调度，win11_main_bot（Win11 WSL Hermes，Telegram H26）为副手，wukong（macOS Codex profile）为未来的编码副手。mac_honey_bot 负责判断任务归属并通过 SSH 委托给 win11_main_bot。
§
Win11 Hermes 装在 WSL 下（非 Windows 原生版），通过 SSH 从 macOS 可达。
§
用户架构理解：当说"win版hermes"通常指 WSL 下的（同一台机器一个实例）。SSH 进去直接 wsl hermes 即可，不要把 Windows 原生版和 WSL 版当作两台机器的两实例。
§
用户偏好只向主 Agent Hermes 下达任务，由 Hermes 统一拆解并调度子 agent；不希望直接分别与子角色交互。