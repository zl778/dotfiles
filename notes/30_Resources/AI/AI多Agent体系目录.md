---
title: AI 多 Agent 体系目录
aliases:
  - 多Agent体系目录
  - Hermes AI 体系目录
created: 2026-07-08
updated: 2026-07-08
type: index
tags:
  - r/tools/hermes
---

# AI 多 Agent 体系目录

这里汇总当前已经整理好的几份 Hermes / worker 相关笔记，方便统一查看和维护。

## 1. Win11 winner 调用说明

- [[Win11 winner 调用说明]]
- 路径：/Users/liangzhu/Library/Mobile Documents/iCloud~md~obsidian/Documents/PKM/30_Resources/AI/Win11-winner调用说明.md

用途：
- 说明 Mac 上的 default 如何调用 Win11 上的 winner
- 记录脚本、通讯录、测试方式

## 2. 多 Agent 总架构图

- [[Hermes 多 Agent 总架构图]]
- 路径：/Users/liangzhu/Library/Mobile Documents/iCloud~md~obsidian/Documents/PKM/30_Resources/AI/Hermes-多Agent总架构图.md

用途：
- 把入口层、调度层、职责层、执行层、记忆层统一起来
- 作为最终总图查看

## 2. 角色关系图

- [[Hermes 角色关系图]]
- 路径：/Users/liangzhu/Library/Mobile Documents/iCloud~md~obsidian/Documents/PKM/30_Resources/AI/Hermes-角色关系图.md

用途：
- 说明主调度、职责层、执行层的关系
- 方便一眼看懂多 Agent 架构

## 2. 主 Agent：Hermes

- [[Hermes]]
- 路径：/Users/liangzhu/Library/Mobile Documents/iCloud~md~obsidian/Documents/PKM/30_Resources/AI/Hermes-Hermes.md

用途：
- 主调度、拆解任务、协调子 agent

## 2. Researcher

- [[Researcher]]
- 路径：/Users/liangzhu/Library/Mobile Documents/iCloud~md~obsidian/Documents/PKM/30_Resources/AI/Hermes-Researcher.md

用途：
- 搜索资料、阅读文档、技术调研、信息整理

## 3. Engineer

- [[Engineer]]
- 路径：/Users/liangzhu/Library/Mobile Documents/iCloud~md~obsidian/Documents/PKM/30_Resources/AI/Hermes-Engineer.md

用途：
- 编程、调试、重构、脚本开发

## 4. Navigator

- [[Navigator]]
- 路径：/Users/liangzhu/Library/Mobile Documents/iCloud~md~obsidian/Documents/PKM/30_Resources/AI/Hermes-Navigator.md

用途：
- 浏览器自动化、登录、下载、网页操作

## 5. Operator

- [[Operator]]
- 路径：/Users/liangzhu/Library/Mobile Documents/iCloud~md~obsidian/Documents/PKM/30_Resources/AI/Hermes-Operator.md

用途：
- Linux / WSL / Windows / SSH / Docker / 运维

## 6. Writer

- [[Writer]]
- 路径：/Users/liangzhu/Library/Mobile Documents/iCloud~md~obsidian/Documents/PKM/30_Resources/AI/Hermes-Writer.md

用途：
- 文档、邮件、Markdown、Prompt、总结

## 7. 任务下达模板

- [[Hermes-主Agent任务下达模板]]
- 路径：/Users/liangzhu/Library/Mobile Documents/iCloud~md~obsidian/Documents/PKM/30_Resources/AI/Hermes-主Agent任务下达模板.md

用途：
- 以后只对主 Agent Hermes 下任务
- 给出通用模板、写作模板、排障模板等

## 8. 6 个核心角色任务分配规则表

- [[Hermes-6个核心角色任务分配规则表]]
- 路径：/Users/liangzhu/Library/Mobile Documents/iCloud~md~obsidian/Documents/PKM/30_Resources/AI/Hermes-6个核心角色任务分配规则表.md

用途：
- Hermes / Researcher / Engineer / Navigator / Operator / Writer 的任务分工
- 任务怎么分配、怎么并行、怎么收口

## 9. Worker 通讯录模板

- [[Hermes-worker通讯录模板]]
- 路径：/Users/liangzhu/Library/Mobile Documents/iCloud~md~obsidian/Documents/PKM/30_Resources/AI/Hermes-worker通讯录模板.md

用途：
- 给主 Hermes 看的完整 worker 通讯录
- 便于后续新增 worker 和扩展字段

## 10. Worker 通讯录精简版

- [[Hermes-worker通讯录精简版]]
- 路径：/Users/liangzhu/Library/Mobile Documents/iCloud~md~obsidian/Documents/PKM/30_Resources/AI/Hermes-worker通讯录精简版.md

用途：
- 给主 Hermes 快速读取的精简版
- 适合日常路由和派单

## 11. 主 Hermes 读取 worker 通讯录的使用规范

- [[主Hermes读取worker通讯录的使用规范]]
- 路径：/Users/liangzhu/Library/Mobile Documents/iCloud~md~obsidian/Documents/PKM/30_Resources/AI/主Hermes读取worker通讯录的使用规范.md

用途：
- 规定先读精简版还是完整版
- 规定什么时候切换到完整版
- 规定主 Hermes 的读取流程

## 12. AI 多 Agent 模型分配建议表

- [[AI多Agent模型分配建议表]]
- 路径：/Users/liangzhu/Library/Mobile Documents/iCloud~md~obsidian/Documents/PKM/30_Resources/AI/AI多Agent模型分配建议表.md

用途：
- 给不同 agent / worker 分配不同模型
- 兼顾成本、速度和执行效果
- 方便后续按角色调整模型

## 建议使用顺序

1. 先看「主 Agent：Hermes」
2. 再看「Researcher / Engineer / Navigator / Operator / Writer」
3. 再看「任务下达模板」
4. 再看「6 个核心角色任务分配规则表」
5. 再看「Worker 通讯录精简版」
6. 需要扩展时再看「Worker 通讯录模板」
7. 最后参考「主 Hermes 读取 worker 通讯录的使用规范」
8. 需要调模型时再看「AI 多 Agent 模型分配建议表」

## 备注

后续如果再补充 Researcher、Navigator、Writer、Reviewer、Tester、Archivist 等角色，可以继续加到这里统一管理。
