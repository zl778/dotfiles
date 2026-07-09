---
title: AI 多 Agent 模型分配建议表
aliases:
  - 多Agent模型分配建议表
  - 模型分配建议表
created: 2026-07-08
updated: 2026-07-08
type: guide
tags:
  - r/tools/hermes
---

# AI 多 Agent 模型分配建议表

这份笔记用于给不同 agent / worker 配置不同模型，以兼顾成本、速度和执行效果。

## 配置原则

1. 主 Hermes 用最强的通用模型
- 负责任务拆解、协调、最终判断、结果汇总
- 不能太弱

2. 执行型 agent 用更快更省的模型
- 主要做执行、查询、操作、回传
- 真正负担通常在工具，而不是推理

3. 编程型 agent 用更强的代码模型
- 重点是代码质量、调试能力、稳定性
- 宁可稍贵一点，也不要频繁返工

4. 写作类 agent 优先语言表达强的模型
- 适合总结、文档、邮件、对外输出

---

## 推荐模型表

| 角色 / 节点 | 推荐主模型 | 推荐备用模型 | 适合的任务类型 | 说明 |
|---|---|---|---|---|
| Hermes（主 agent） | GPT-5 / Claude Sonnet 4 | GPT-5-mini / DeepSeek-V3.1 | 任务拆解、协调、最终判断、汇总 | 作为总调度，优先要稳 |
| Researcher | GPT-4.1-mini / DeepSeek-V3.1 | GPT-5-mini | 搜索资料、阅读文档、技术调研、信息整理 | 以性价比为主 |
| Engineer / wukong | OpenAI Codex / o4-mini | GPT-5 / DeepSeek-V3.1 | 编程、调试、重构、脚本开发 | 编码能力优先 |
| Navigator | GPT-4.1-mini / Claude Haiku 3.5 | DeepSeek-V3.1 | 浏览器自动化、登录、下载、网页验证 | 主要看速度和稳定性 |
| Operator / Win11 Hermes / WSL Hermes | GPT-4.1-mini / DeepSeek-V3.1 | GPT-5-mini | Linux、WSL、Windows、SSH、Docker、服务器运维 | 执行型任务优先省钱 |
| Writer | Claude Sonnet 4 / GPT-4.1-mini | DeepSeek-V3.1 | 文档、邮件、Markdown、Prompt、总结 | 语言表达要顺 |
| Reviewer（以后扩展） | GPT-5 / Claude Sonnet 4 | GPT-5-mini | 审核代码、文档、方案 | 需要更强判断力 |
| Tester（以后扩展） | GPT-4.1-mini / GPT-5-mini | DeepSeek-V3.1 | 测试、验证、复现问题、QA | 偏验证，不必最贵 |
| Archivist（以后扩展） | GPT-4.1-mini / DeepSeek-V3.1 | - | 管理知识库、整理 Obsidian、维护长期记忆 | 归档整理，重稳定 |
| Scheduler（以后扩展） | GPT-4.1-mini / DeepSeek-V3.1 | - | 日程、待办、提醒、时间规划 | 更像工具能力 |

---

## 两套常见配法

### 1. 省钱优先版

- Hermes：GPT-5-mini
- Researcher：DeepSeek-V3.1
- Engineer / wukong：o4-mini
- Navigator：GPT-4.1-mini
- Operator / Win11 / WSL：DeepSeek-V3.1
- Writer：GPT-4.1-mini

适合：
- 日常高频使用
- 想控制成本
- 任务以执行为主

### 2. 效果优先版

- Hermes：GPT-5 / Claude Sonnet 4
- Researcher：GPT-5-mini
- Engineer / wukong：OpenAI Codex / GPT-5
- Navigator：GPT-4.1-mini
- Operator / Win11 / WSL：GPT-4.1-mini
- Writer：Claude Sonnet 4

适合：
- 更看重结果质量
- 编程和统筹任务较多
- 可以接受更高成本

---

## 推荐的实用混合版

这是更适合当前阶段的折中方案：

- Hermes：GPT-5
- wukong：o4-mini / Codex
- Win11 Hermes：GPT-4.1-mini
- WSL Hermes：DeepSeek-V3.1
- Researcher：DeepSeek-V3.1
- Navigator：GPT-4.1-mini
- Writer：Claude Sonnet 4

这个组合比较平衡：
- 主 Hermes 保持强判断力
- 编码副手有专门代码模型
- 执行节点尽量省钱稳定
- 写作类保留较好的语言模型

---

## 简单口诀

- 总调度，用最强
- 编程，用最专
- 执行，用最快
- 写作，用最顺
- 研究，用最省

---

## 后续维护建议

以后如果：
- 某个模型太贵
- 某个模型太慢
- 某个 worker 经常出错
- 某个任务类型明显更适合另一个模型

就直接在这份表里更新对应项。
