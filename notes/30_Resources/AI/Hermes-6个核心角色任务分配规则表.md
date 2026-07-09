---
title: Hermes 6 个核心角色任务分配规则表
aliases:
  - 6个核心角色任务分配规则表
  - 任务分配规则表
created: 2026-07-08
updated: 2026-07-08
type: guide
tags:
  - r/tools/hermes
---

# Hermes 6 个核心角色任务分配规则表

这是一份给主 Agent Hermes 用的任务分配速查表。你以后只需要把任务交给 Hermes，由它根据任务类型分配给合适的子角色。

## 核心任务分配规则表

| 角色 | 主要接什么任务 | 典型触发条件 | 不适合接什么 | 输出形式 |
|---|---|---|---|---|
| Hermes | 任务拆解、调度、汇总、跨角色协调、最终判断 | 任务不清晰、涉及多个步骤、需要决定先后顺序、需要整合多个子结果 | 不适合直接承担重体力执行型任务 | 任务分解、分派清单、最终总结 |
| Researcher | 搜索资料、读文档、查标准、做技术调研、信息归纳 | 需要“先搞清楚是什么”、需要对比方案、需要查外部知识、需要引用资料 | 不适合直接改代码、直接操作系统、直接做网页操作 | 资料摘要、对比表、结论、来源清单 |
| Engineer | 编程、调试、重构、写脚本、修 bug、写测试代码 | 任务明确要“产出可运行代码”、需要修改项目、需要定位 bug、需要实现功能 | 不适合只做资料搜集，也不适合大量网页点选 | 代码变更、补丁、脚本、测试结果 |
| Navigator | 浏览器自动化、登录、下载、网页操作、表单提交、页面验证 | 任务涉及网页、后台系统、在线表单、需要点击/登录/下载/验证页面 | 不适合写复杂代码，也不适合做长期知识整理 | 操作结果、页面状态、下载文件、表单提交结果 |
| Operator | Linux / WSL / Windows / SSH / Docker / 服务器运维 / 终端操作 | 任务涉及命令行、远程机器、服务启动/停止、容器、文件系统、进程管理 | 不适合做纯文案、纯研究、纯浏览器交互 | 命令输出、运行结果、部署状态、故障信息 |
| Writer | 文档、邮件、Markdown、Prompt、总结、对外表达整理 | 任务要“写得清楚”、需要生成可读文本、需要把结果整理成人类可读内容 | 不适合做底层运维或复杂代码实现 | 文档、邮件、报告、总结、说明稿 |

## 分配判断规则

1. 先判断任务本质是什么
- 要查资料 → Researcher
- 要写代码 → Engineer
- 要点网页 → Navigator
- 要跑命令 → Operator
- 要写成文 → Writer
- 要拆任务和统筹 → Hermes

2. 看任务有没有“执行动作”
- 动手做 → Engineer / Navigator / Operator
- 理解、归纳、表达 → Researcher / Writer / Hermes

3. 看是否需要先后顺序
- 先查资料再编码：Researcher → Hermes → Engineer
- 先执行命令再看结果：Operator → Hermes → Writer

4. 看工具依赖
- 需要浏览器权限 → Navigator
- 需要 shell / SSH / Docker → Operator
- 需要改文件 / 代码仓库 → Engineer
- 需要外部资料 / 文档 → Researcher

## 常见任务流

### 1. 新功能开发
- Hermes：拆解需求
- Researcher：查相关资料
- Engineer：开始编码
- Writer：整理说明

### 2. 故障排查
- Operator：先看日志、服务、端口、进程
- Researcher：补充相关技术资料
- Engineer：修代码或脚本
- Hermes：最终判断和收口
- Writer：输出排障结论

### 3. 网页业务操作
- Navigator：登录、点击、下载、提交
- Hermes：判断是否需要继续
- Writer：整理结果

### 4. 写方案或邮件
- Researcher：补事实和资料
- Hermes：确定结构
- Writer：成文

## 简单口令

- 查资料，给 Researcher
- 写代码，给 Engineer
- 点网页，给 Navigator
- 跑命令，给 Operator
- 写成文，给 Writer
- 要拆单、协调、收口，给 Hermes

## 并行建议

可以并行：
- Researcher 查资料，同时 Writer 整理已有内容
- Operator 看日志，同时 Researcher 查文档
- Navigator 做网页验证，同时 Engineer 修代码

不建议并行：
- 同一个代码文件让多个 Engineer 同时改
- 同一个网页会话让多个 Navigator 同时操作
- 同一个服务器环境让多个 Operator 同时做高风险命令

## 最后建议

默认流程：
1. 先交给 Hermes
2. 再由 Hermes 分配给对应执行角色
3. 最后回到 Hermes 汇总、确认、收口
