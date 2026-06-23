---
name: Telegram vs BlueBubbles (iMessage) — 平台选择指南
source: Hermes Agent docs + gateway platform adapter analysis
---

# Telegram vs BlueBubbles (iMessage) — 平台选择指南

## 架构差异

| 维度 | Telegram | BlueBubbles (iMessage) |
|------|----------|----------------------|
| **中间件** | 无 — 直连 Bot API | 需要 BlueBubbles Server 作为桥梁 |
| **数据流** | Hermes ↔ Telegram 服务器 | iMessage → Messages.app → BlueBubbles Server → Hermes |
| **网络要求** | 直连公网（或 proxy） | 全部本地（127.0.0.1） |
| **平台限制** | 全平台通用 | **仅 macOS**（依赖 Messages.app） |
| **连接方式** | 长轮询 或 Webhook | HTTP 轮询 + 回调 |

## 功能对比

| 功能 | Telegram | BlueBubbles (iMessage) |
|------|----------|----------------------|
| **文字消息** | ✅ | ✅ |
| **图片/视频/文件** | ✅ | ✅ |
| **语音消息输入** | ✅ STT 自动转录 | ✅ 文件形式 |
| **语音回复 (TTS)** | ✅ 原生语音泡泡 | ✅ 文件形式 |
| **流式输出 (Streaming)** | ✅ 原生 drafts API | ❌ 不支持 |
| **打字指示器** | ✅ | ✅（需 Private API） |
| **Reaction** | ✅（👀 ✅ ❌ 处理反馈） | ✅ Tapback（需 Private API） |
| **群聊** | ✅ 功能完整 | ✅ |
| **话题/子线程** | ✅ 原生 Forum Topics | ❌ iMessage 无此概念 |
| **多会话隔离** | ✅ /topic 模式 / DM Topics | ❌ |
| **每频道提示词** | ✅ channel_prompts | ❌ |
| **配对授权** | ✅ DM pairing | ✅ DM pairing |
| **消息编辑** | ✅ 编辑已有消息 | ❌ iMessage 不可编辑 |

## 配置复杂度

**Telegram（3 步）：**
1. @BotFather 创建 bot → 拿到 token
2. 在 .env 加 TELEGRAM_BOT_TOKEN + TELEGRAM_ALLOWED_USERS
3. hermes gateway restart → 完成

**BlueBubbles（iMessage）（6 步）：**
1. 下载安装 BlueBubbles Server（~300MB）
2. 打开 BlueBubbles 完成 GUI 设置向导
3. 允许系统权限（辅助功能、完全磁盘访问等）
4. 在 Settings → API 找到 URL + Password
5. 在 .env 加 BLUEBUBBLES_SERVER_URL + BLUEBUBBLES_PASSWORD
6. hermes gateway restart → 完成

## 选择建议

**选 Telegram 当：**
- 功能丰富需求（流式输出、话题隔离、频道提示词）
- 需要跨平台（不依赖 macOS）
- 想要最快配置（3 步搞定）
- 可以接受对方看到的是 bot 而非你本人

**选 BlueBubbles（iMessage）当：**
- **用真实手机号** — 对方看到的不是 bot 是你本人
- 对方无需装任何 App，原生蓝色泡泡
- 需要 Tapback（点赞❤️、哈哈😄等原生反应）
- 对接已有联系人，无需对方添加 bot

**两者不冲突，可以同时启用。**

## 常见误解

> "Hermes 最新版是不是就不需要 BlueBubbles 了？"

**不是。** Hermes v0.17.0 的 iMessage 支持仍然通过 BlueBubbles Server 作为桥梁。Hermes gateway 的 `gateway/platforms/bluebubbles.py` 是 BlueBubbles API 的客户端，没有原生 iMessage 适配器。文档侧边栏有 "Photon iMessage" 链接但页面 404，说明尚未实现。

## 参考

- Hermes Telegram 文档: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/popular/telegram
- Hermes BlueBubbles 文档: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/other/bluebubbles
- BlueBubbles 官网: https://bluebubbles.app
- BlueBubbles GitHub: https://github.com/BlueBubblesApp/bluebubbles-server
