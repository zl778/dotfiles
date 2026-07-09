---
title: Hermes profile 常驻与按需启动方案
aliases:
  - Hermes 常驻与按需启动方案
  - profile 启动策略
created: 2026-07-09
updated: 2026-07-09
type: guide
tags:
  - r/tools/hermes
---

# Hermes profile 常驻与按需启动方案

这份笔记用于决定哪些 profile 保持常驻，哪些 profile 采用按需启动。

## 一、推荐结论

默认推荐：

- 常驻：default、wukong
- 按需启动：researcher、engineer、navigator、operator、writer

如果后续发现 engineer 使用频率很高，可以把 engineer 升级为常驻。

## 二、推荐方案 A：省资源优先

适合希望系统更轻、但保持可用性。

| Profile | 推荐 | 理由 |
|---|---|---|
| default | 常驻 | 主调度必须在线 |
| wukong | 常驻 | 编码副手，高频使用 |
| researcher | 按需 | 查资料才启动 |
| engineer | 按需 | 编码频率不高时没必要常驻 |
| navigator | 按需 | 浏览器任务通常是事件型 |
| operator | 按需 | 运维任务多为临时性 |
| writer | 按需 | 写作/整理更适合任务型启动 |

## 三、推荐方案 B：效率优先

适合编码任务很多、希望减少拉起等待。

| Profile | 推荐 | 理由 |
|---|---|---|
| default | 常驻 | 总调度 |
| wukong | 常驻 | 编码副手 |
| engineer | 常驻 | 编码/调试副手，和 wukong 分工更明确 |
| researcher | 按需 | 资料任务不连续 |
| navigator | 按需 | 网页任务事件型 |
| operator | 按需 | 运维任务按需拉起更稳 |
| writer | 按需 | 文案整理不需要常驻 |

## 四、我的建议

基于当前使用习惯，更推荐下面这个分层：

1. 第一阶段
- 常驻：default、wukong
- 按需：researcher、engineer、navigator、operator、writer

2. 观察一周后
- 如果 engineer 每天用 3 次以上，再改成常驻

## 五、简单阈值

可用下面的经验线判断是否要常驻：

- engineer：每天 3 次以上，考虑常驻
- researcher / navigator / writer：通常保持按需
- operator：只有经常折腾 WSL / SSH / Docker 时才考虑常驻

## 六、关联笔记

- [[Hermes-worker角色落地清单]]
- [[Hermes-worker通讯录模板]]
- [[Hermes-worker通讯录精简版]]
- [[主Hermes读取worker通讯录的使用规范]]
