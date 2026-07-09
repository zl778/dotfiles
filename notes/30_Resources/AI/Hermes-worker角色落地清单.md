---
title: Hermes Worker 角色落地清单
aliases:
  - Hermes worker 角色落地
  - Worker 角色清单
created: 2026-07-09
updated: 2026-07-09
type: guide
tags:
  - r/tools/hermes
---

# Hermes Worker 角色落地清单

这份笔记记录已经落地的角色 worker，供主 Hermes 路由和日常查阅。

## 已落地角色

| 角色 | 主要职责 | profile | 入口 |
|---|---|---|---|
| researcher | 资料搜索、阅读、筛选、研究整理 | researcher | `researcher` |
| engineer | 编码、调试、重构、脚本实现 | engineer | `engineer` |
| navigator | 浏览器操作、点击、登录、下载、网页验证 | navigator | `navigator` |
| operator | 系统、终端、WSL、SSH、Docker、运维 | operator | `operator` |
| writer | 文档、邮件、Markdown、总结、改写 | writer | `writer` |

## 路由建议

- 研究 / 查证 / 阅读 → researcher
- 编码 / 调试 / 改造 → engineer 或 wukong
- 网页 / 登录 / 下载 / 验证 → navigator
- 系统 / 终端 / WSL / Docker / SSH → operator
- 文档 / 邮件 / Markdown / 改写 → writer

## 关联笔记

- [[Hermes-worker通讯录模板]]
- [[Hermes-worker通讯录精简版]]
- [[主Hermes读取worker通讯录的使用规范]]
