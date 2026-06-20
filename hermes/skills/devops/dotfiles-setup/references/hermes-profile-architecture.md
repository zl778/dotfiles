# Hermes Profile 架构

## 核心概念

每个 Hermes profile 像一台独立机器，拥有完全隔离的配置文件、认证、会话历史、记忆和技能。

```
~/.hermes/                           ← default profile
├── config.yaml                      ← 配置
├── auth.json                        ← 认证
├── .env                             ← API key
├── state.db                         ← 会话历史（独立隔离）
├── memories/{MEMORY.md, USER.md}   ← 持久记忆
├── skills/                          ← 技能
├── cron/                            ← 定时任务
├── sessions/                        ← 会话转储
├── logs/                            ← 日志
│
└── profiles/wukong/                 ← wukong profile
    ├── config.yaml                  ← 独立配置
    ├── auth.json                    ← 独立 OAuth
    ├── ... 同上结构
```

## 影响 profile 上下文的文件

每次会话启动时，system prompt 由以下文件拼接：

| 文件 | 影响什么 |
|------|----------|
| **config.yaml** | 模型选择、工具集、行为参数（max_turns, reasoning_effort 等）|
| **SOUL.md** | 固定的"人格设定"，追加到系统提示 |
| **memories/MEMORY.md** | 跨会话的持久事实（Hermes 自动管理）|
| **memories/USER.md** | 用户偏好画像（Hermes 自动管理）|
| **skills/** | 按需加载的技能内容注入 |
| **state.db** | 历史会话（供 session_search）|

## 切换 profile

```bash
hermes -p wukong              # 启动 wukong 会话
hermes -p wukong chat -q ...  # 单次查询
# 也可以用别名：
alias wukong='hermes -p wukong'
```

## 跨 profile 操作

**默认 profile 不能直接写其他 profile 的记忆/技能/配置**——有 cross-profile 软保护。
在用户明确确认后，工具调用加 `cross_profile=true` 参数可绕过。

```python
# 在被保护时：
write_file(path=".../profiles/wukong/memories/MEMORY.md", content="...", cross_profile=True)
```

## 配置同步

技能默认不跨 profile 共享。要让不同 profile 共享技能目录，可配：

```bash
hermes config set skills.external_dirs ["~/.hermes/skills"]
```

（在目标 profile 的 config.yaml 中设置）

## 典型搭配

| profile | 主要用途 | 推荐模型 |
|---------|---------|---------|
| default | 日常查询、研究 | DeepSeek / Claude Haiku（低成本）|
| wukong  | 编码、复杂任务 | OpenAI Codex o4-mini（高能力）|
